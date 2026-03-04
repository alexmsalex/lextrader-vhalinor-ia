import threading
import asyncio
from typing import Any, Dict, Optional, Callable, List, Tuple, Union, Set
import time
import inspect
import weakref
from dataclasses import dataclass, field
from enum import Enum
import logging
from concurrent.futures import Future, ThreadPoolExecutor, TimeoutError
import uuid
import json
import pickle
from contextlib import contextmanager
import heapq
from collections import defaultdict, deque
import psutil
import gc

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('NeuralBus')

class MessagePriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class MessageType(Enum):
    EVENT = "event"
    REQUEST = "request"
    RESPONSE = "response"
    COMMAND = "command"
    STATUS = "status"
    ERROR = "error"

@dataclass
class NeuralMessage:
    id: str
    source: str
    destination: Optional[str]
    message_type: MessageType
    priority: MessagePriority
    payload: Any
    timestamp: float = field(default_factory=time.time)
    ttl: float = 30.0  # Time to live in seconds
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'source': self.source,
            'destination': self.destination,
            'message_type': self.message_type.value,
            'priority': self.priority.value,
            'payload': self.payload,
            'timestamp': self.timestamp,
            'ttl': self.ttl,
            'correlation_id': self.correlation_id,
            'metadata': self.metadata
        }

class NeuralComponent:
    """Classe base para componentes que se integram ao NeuralBus."""
    
    def __init__(self, name: str, bus: 'NeuralBus'):
        self.name = name
        self.bus = bus
        self._is_registered = False
        
    def register(self, metadata: Optional[Dict[str, Any]] = None):
        """Registra o componente no barramento."""
        self.bus.register(self.name, self, metadata)
        self._is_registered = True
        
    def unregister(self):
        """Remove o componente do barramento."""
        if self._is_registered:
            self.bus.unregister(self.name)
            self._is_registered = False
            
    def on_neural_event(self, event: str, payload: Any):
        """Callback para eventos recebidos."""
        logger.debug(f"Component {self.name} received event {event}: {payload}")
        
    def send_event(self, event: str, payload: Any = None, priority: MessagePriority = MessagePriority.NORMAL):
        """Envia evento através do barramento."""
        self.bus.broadcast(event, payload, self.name, priority)
        
    def request(self, target: str, method: str, *args, **kwargs):
        """Faz requisição para outro componente."""
        return self.bus.request(target, method, *args, **kwargs)

class NeuralBusMetrics:
    """Coletor de métricas de performance do barramento."""
    
    def __init__(self):
        self.message_count = 0
        self.message_count_by_type = defaultdict(int)
        self.message_count_by_priority = defaultdict(int)
        self.avg_processing_time = 0.0
        self.total_processing_time = 0.0
        self.error_count = 0
        self.registry_size = 0
        self.subscription_count = 0
        self.last_update = time.time()
        
    def update_message_stats(self, message: NeuralMessage, processing_time: float = 0.0):
        """Atualiza estatísticas de mensagens."""
        self.message_count += 1
        self.message_count_by_type[message.message_type] += 1
        self.message_count_by_priority[message.priority] += 1
        self.total_processing_time += processing_time
        self.avg_processing_time = self.total_processing_time / self.message_count
        
    def to_dict(self) -> Dict[str, Any]:
        """Converte métricas para dicionário."""
        return {
            'message_count': self.message_count,
            'message_count_by_type': dict(self.message_count_by_type),
            'message_count_by_priority': dict(self.message_count_by_priority),
            'avg_processing_time_ms': self.avg_processing_time * 1000,
            'error_count': self.error_count,
            'registry_size': self.registry_size,
            'subscription_count': self.subscription_count,
            'uptime_seconds': time.time() - self.last_update
        }

class NeuralBus:
    """
    Barramento neural avançado com suporte a:
    - Registro dinâmico de componentes
    - Sistema de pub/sub com prioridades
    - Request/response assíncrono
    - Bridge para sistemas quânticos
    - Métricas de performance
    - Persistência e recovery
    - Load balancing
    - Security context
    """
    
    _instance = None
    _lock = threading.RLock()
    
    def __init__(self, max_queue_size: int = 10000, enable_metrics: bool = True):
        # Registros e subscriptions
        self._registry: Dict[str, Any] = {}
        self._meta: Dict[str, Dict[str, Any]] = {}
        self._subs: Dict[str, List[Tuple[Callable[[str, Any], None], MessagePriority]]] = {}
        self._wildcard_subs: List[Tuple[Callable[[str, Any], None], MessagePriority]] = []
        
        # Sistema de mensagens
        self._message_queues: Dict[MessagePriority, deque] = {
            MessagePriority.LOW: deque(maxlen=max_queue_size),
            MessagePriority.NORMAL: deque(maxlen=max_queue_size),
            MessagePriority.HIGH: deque(maxlen=max_queue_size),
            MessagePriority.CRITICAL: deque(maxlen=max_queue_size // 10)  # Fila menor para crítico
        }
        
        # Request/response tracking
        self._pending_requests: Dict[str, Future] = {}
        self._request_timeouts: Dict[str, float] = {}
        
        # Bridges e integrações
        self._bridge_checked = False
        self._quantum_bridge = None
        self._external_bridges: Dict[str, Any] = {}
        
        # Sistema de workers
        self._workers: List[threading.Thread] = []
        self._is_running = False
        self._worker_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="neural_bus")
        
        # Locks e sincronização
        self._reg_lock = threading.RLock()
        self._msg_lock = threading.RLock()
        self._req_lock = threading.RLock()
        
        # Métricas e monitoramento
        self.metrics = NeuralBusMetrics() if enable_metrics else None
        self._security_context: Dict[str, Any] = {}
        
        # Cache de mensagens recentes
        self._message_cache: deque = deque(maxlen=1000)
        
        logger.info("NeuralBus inicializado com sistema avançado de mensagens")

    @classmethod
    def get_instance(cls, **kwargs) -> "NeuralBus":
        """Obter instância singleton do barramento."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = NeuralBus(**kwargs)
            return cls._instance

    def start(self):
        """Inicia o processamento de mensagens do barramento."""
        if self._is_running:
            return
            
        self._is_running = True
        # Worker para processamento de mensagens por prioridade
        for priority in MessagePriority:
            worker = threading.Thread(
                target=self._message_worker,
                args=(priority,),
                name=f"NeuralBusWorker-{priority.name}",
                daemon=True
            )
            worker.start()
            self._workers.append(worker)
            
        # Worker para limpeza de requests expirados
        cleanup_worker = threading.Thread(
            target=self._cleanup_worker,
            name="NeuralBusCleanup",
            daemon=True
        )
        cleanup_worker.start()
        self._workers.append(cleanup_worker)
        
        logger.info("NeuralBus iniciado com workers de processamento")

    def stop(self):
        """Para o barramento e libera recursos."""
        self._is_running = False
        self._worker_pool.shutdown(wait=True)
        
        # Cancelar requests pendentes
        with self._req_lock:
            for future in self._pending_requests.values():
                if not future.done():
                    future.cancel()
            self._pending_requests.clear()
            self._request_timeouts.clear()
            
        logger.info("NeuralBus parado")

    # === REGISTRO DE COMPONENTES ===
    
    def register(self, name: str, instance: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Registra um componente no barramento."""
        with self._reg_lock:
            if name in self._registry:
                logger.warning(f"Componente {name} já registrado, substituindo")
                
            self._registry[name] = instance
            self._meta[name] = metadata or {}
            self._meta[name].update({
                'registered_at': time.time(),
                'last_activity': time.time()
            })
            
            if self.metrics:
                self.metrics.registry_size = len(self._registry)
                
            logger.info(f"Componente registrado: {name}")
            self._ensure_bridge()

    def unregister(self, name: str) -> None:
        """Remove um componente do barramento."""
        with self._reg_lock:
            instance = self._registry.pop(name, None)
            self._meta.pop(name, None)
            
            if self.metrics:
                self.metrics.registry_size = len(self._registry)
                
            if instance:
                logger.info(f"Componente removido: {name}")

    def get(self, name: str) -> Optional[Any]:
        """Obtém um componente pelo nome."""
        with self._reg_lock:
            return self._registry.get(name)

    def list_components(self) -> Dict[str, Dict[str, Any]]:
        """Lista todos os componentes com metadados."""
        with self._reg_lock:
            return {
                name: {**meta, 'type': type(instance).__name__}
                for name, instance, meta in (
                    (name, self._registry[name], self._meta.get(name, {}))
                    for name in self._registry
                )
            }

    # === SISTEMA DE PUB/SUB AVANÇADO ===
    
    def subscribe(self, event: str, handler: Callable[[str, Any], None], 
                  priority: MessagePriority = MessagePriority.NORMAL) -> None:
        """Inscreve um handler para um evento específico."""
        with self._reg_lock:
            if event == "*":
                self._wildcard_subs.append((handler, priority))
            else:
                self._subs.setdefault(event, []).append((handler, priority))
                
            if self.metrics:
                self.metrics.subscription_count = (
                    len(self._subs) + len(self._wildcard_subs)
                )
                
            logger.debug(f"Handler inscrito para evento: {event}")

    def unsubscribe(self, event: str, handler: Callable[[str, Any], None]) -> None:
        """Remove inscrição de um handler."""
        with self._reg_lock:
            if event == "*":
                self._wildcard_subs = [(h, p) for h, p in self._wildcard_subs if h != handler]
            elif event in self._subs:
                self._subs[event] = [(h, p) for h, p in self._subs[event] if h != handler]
                
            if self.metrics:
                self.metrics.subscription_count = (
                    len(self._subs) + len(self._wildcard_subs)
                )

    def broadcast(self, event: str, payload: Any = None, source: str = "system",
                  priority: MessagePriority = MessagePriority.NORMAL) -> str:
        """
        Broadcast de evento com sistema de prioridades e tracking.
        Retorna ID da mensagem para tracking.
        """
        message = NeuralMessage(
            id=str(uuid.uuid4()),
            source=source,
            destination=None,
            message_type=MessageType.EVENT,
            priority=priority,
            payload=payload,
            metadata={'event': event}
        )
        
        # Adicionar à fila apropriada
        with self._msg_lock:
            self._message_queues[priority].append(message)
            self._message_cache.append(message)
            
        logger.debug(f"Evento broadcast: {event} from {source} (pri: {priority.name})")
        return message.id

    def _message_worker(self, priority: MessagePriority):
        """Worker para processar mensagens de uma prioridade específica."""
        queue = self._message_queues[priority]
        
        while self._is_running:
            try:
                if queue:
                    message = queue.popleft()
                    
                    if message.is_expired():
                        continue
                        
                    start_time = time.time()
                    self._process_message(message)
                    processing_time = time.time() - start_time
                    
                    if self.metrics:
                        self.metrics.update_message_stats(message, processing_time)
                        
                else:
                    time.sleep(0.01)  # Pequena pausa para evitar CPU spinning
                    
            except Exception as e:
                logger.error(f"Erro no worker de mensagens {priority.name}: {e}")
                if self.metrics:
                    self.metrics.error_count += 1

    def _process_message(self, message: NeuralMessage):
        """Processa uma mensagem individual."""
        handlers = []
        
        # Coletar handlers específicos do evento
        with self._reg_lock:
            event_name = message.metadata.get('event', '')
            if event_name in self._subs:
                handlers.extend(self._subs[event_name])
            
            # Adicionar wildcard handlers
            handlers.extend(self._wildcard_subs)
            
            # Notificar componentes registrados
            for instance in self._registry.values():
                if hasattr(instance, 'on_neural_event'):
                    handlers.append((instance.on_neural_event, MessagePriority.NORMAL))
        
        # Executar handlers
        for handler, handler_priority in handlers:
            if handler_priority.value >= message.priority.value:
                try:
                    handler(message.metadata.get('event', ''), message.payload)
                except Exception as e:
                    logger.error(f"Erro no handler para evento {message.metadata.get('event', '')}: {e}")

        # Bridge para sistemas externos
        self._bridge_message(message)

    # === SISTEMA REQUEST/RESPONSE AVANÇADO ===
    
    def request(self, target_name: str, method: str, *args, 
                timeout: float = 10.0, priority: MessagePriority = MessagePriority.NORMAL,
                **kwargs) -> Future:
        """
        Faz requisição assíncrona para um componente.
        Retorna um Future que pode ser aguardado.
        """
        future = Future()
        request_id = str(uuid.uuid4())
        
        with self._req_lock:
            self._pending_requests[request_id] = future
            self._request_timeouts[request_id] = time.time() + timeout
        
        # Tentar execução local primeiro
        def execute_request():
            try:
                target = self.get(target_name)
                if target:
                    fn = getattr(target, method, None)
                    if callable(fn):
                        result = fn(*args, **kwargs)
                        future.set_result(result)
                        return
                
                # Se não encontrado localmente, tentar bridge
                if self._ensure_bridge():
                    try:
                        result = self._quantum_bridge.request_from_bridge(
                            target_name, method, args, kwargs, timeout=timeout
                        )
                        future.set_result(result)
                        return
                    except Exception as e:
                        future.set_exception(e)
                        return
                
                future.set_exception(LookupError(f"Target {target_name} not found"))
                
            except Exception as e:
                future.set_exception(e)
        
        # Executar em thread separada para não bloquear
        self._worker_pool.submit(execute_request)
        return future

    async def request_async(self, target_name: str, method: str, *args,
                          timeout: float = 10.0, **kwargs) -> Any:
        """Versão assíncrona do request."""
        loop = asyncio.get_event_loop()
        future = self.request(target_name, method, *args, timeout=timeout, **kwargs)
        return await loop.run_in_executor(None, future.result)

    def send_response(self, request_id: str, result: Any, success: bool = True):
        """Envia resposta para uma requisição pendente."""
        with self._req_lock:
            future = self._pending_requests.pop(request_id, None)
            self._request_timeouts.pop(request_id, None)
            
        if future and not future.done():
            if success:
                future.set_result(result)
            else:
                future.set_exception(result)

    def _cleanup_worker(self):
        """Worker para limpar requests expirados."""
        while self._is_running:
            try:
                current_time = time.time()
                expired_requests = []
                
                with self._req_lock:
                    for req_id, expiry in list(self._request_timeouts.items()):
                        if current_time > expiry:
                            expired_requests.append(req_id)
                    
                    for req_id in expired_requests:
                        future = self._pending_requests.pop(req_id, None)
                        self._request_timeouts.pop(req_id, None)
                        if future and not future.done():
                            future.set_exception(TimeoutError("Request timeout"))
                
                time.sleep(1.0)  # Verificar a cada segundo
                
            except Exception as e:
                logger.error(f"Erro no worker de cleanup: {e}")
                time.sleep(5.0)

    # === BRIDGE E INTEGRAÇÕES ===
    
    def _ensure_bridge(self) -> bool:
        """Descobre e configura bridges para sistemas externos."""
        if self._bridge_checked:
            return self._quantum_bridge is not None
            
        self._bridge_checked = True
        
        # Tentar conectar com QuantumBus
        try:
            import importlib
            qmod = importlib.import_module("quantum.quantum_bus")
            qinstance = getattr(qmod, "QuantumBus").get_instance()
            self._quantum_bridge = qinstance
            
            # Registrar callback no quantum bus
            if hasattr(qinstance, 'register_neural_bridge'):
                qinstance.register_neural_bridge(self)
                
            logger.info("Bridge Quantum conectada com sucesso")
            return True
            
        except Exception as e:
            logger.debug(f"Quantum bridge não disponível: {e}")
            self._quantum_bridge = None
            return False

    def _bridge_message(self, message: NeuralMessage):
        """Encaminha mensagem para bridges externas."""
        if self._quantum_bridge and hasattr(self._quantum_bridge, 'bridge_receive'):
            try:
                self._quantum_bridge.bridge_receive(
                    from_namespace="neural",
                    event=message.metadata.get('event', ''),
                    payload=message.payload
                )
            except Exception as e:
                logger.debug(f"Falha ao encaminhar para quantum bridge: {e}")

    def bridge_receive(self, from_namespace: str, event: str, payload: Any):
        """Recebe mensagens de bridges externas."""
        logger.info(f"Mensagem recebida da bridge {from_namespace}: {event}")
        self.broadcast(f"{from_namespace}.{event}", payload, from_namespace)

    # === MÉTRICAS E MONITORAMENTO ===
    
    def get_metrics(self) -> Optional[Dict[str, Any]]:
        """Obtém métricas de performance do barramento."""
        if self.metrics:
            return self.metrics.to_dict()
        return None

    def get_message_stats(self) -> Dict[str, Any]:
        """Estatísticas detalhadas das mensagens."""
        stats = {
            'total_queued': sum(len(q) for q in self._message_queues.values()),
            'queues': {}
        }
        
        for priority, queue in self._message_queues.items():
            stats['queues'][priority.name] = len(queue)
            
        return stats

    def get_component_stats(self) -> Dict[str, Any]:
        """Estatísticas dos componentes registrados."""
        with self._reg_lock:
            return {
                'total_components': len(self._registry),
                'components': list(self._registry.keys()),
                'subscriptions': len(self._subs) + len(self._wildcard_subs)
            }

    # === UTILITÁRIOS AVANÇADOS ===
    
    @contextmanager
    def temporary_component(self, name: str, component: Any, metadata: Dict[str, Any] = None):
        """
        Context manager para componente temporário.
        Componente é automaticamente removido ao sair do contexto.
        """
        self.register(name, component, metadata)
        try:
            yield component
        finally:
            self.unregister(name)

    def create_component_proxy(self, target_name: str, timeout: float = 5.0):
        """
        Cria um proxy dinâmico para um componente remoto.
        Permite chamar métodos como se o componente estivesse local.
        """
        class ComponentProxy:
            def __init__(self, bus, target, timeout):
                self._bus = bus
                self._target = target
                self._timeout = timeout
                
            def __getattr__(self, name):
                def method(*args, **kwargs):
                    return self._bus.request(
                        self._target, name, *args, 
                        timeout=self._timeout, **kwargs
                    ).result()
                return method
                
        return ComponentProxy(self, target_name, timeout)

# === EXEMPLOS DE USO AVANÇADO ===

class AdvancedNeuralComponent(NeuralComponent):
    """Exemplo de componente avançado."""
    
    def __init__(self, name: str, bus: NeuralBus):
        super().__init__(name, bus)
        self.message_count = 0
        
    def process_data(self, data: str) -> str:
        """Método de processamento exemplo."""
        self.message_count += 1
        result = f"Processed {data} (msg #{self.message_count})"
        logger.info(f"{self.name} processing: {result}")
        return result
        
    def on_neural_event(self, event: str, payload: Any):
        """Handler de eventos customizado."""
        if event == "data.ready":
            result = self.process_data(payload)
            self.send_event("data.processed", result)

async def demo_advanced_features():
    """Demonstração das funcionalidades avançadas."""
    bus = NeuralBus.get_instance()
    bus.start()
    
    # Criar componentes
    comp1 = AdvancedNeuralComponent("processor_1", bus)
    comp2 = AdvancedNeuralComponent("processor_2", bus)
    
    comp1.register({"type": "processor", "version": "1.0"})
    comp2.register({"type": "processor", "version": "1.0"})
    
    # Subscribe para eventos
    def event_handler(event: str, payload: Any):
        logger.info(f"Event handler received {event}: {payload}")
    
    bus.subscribe("data.processed", event_handler)
    
    # Enviar eventos
    bus.broadcast("data.ready", "sample data", "demo", MessagePriority.HIGH)
    
    # Fazer requests assíncronos
    future = bus.request("processor_1", "process_data", "async data")
    try:
        result = future.result(timeout=5.0)
        logger.info(f"Request result: {result}")
    except Exception as e:
        logger.error(f"Request failed: {e}")
    
    # Usar proxy para chamada transparente
    proxy = bus.create_component_proxy("processor_2")
    try:
        result = proxy.process_data("proxy data")
        logger.info(f"Proxy result: {result}")
    except Exception as e:
        logger.error(f"Proxy call failed: {e}")
    
    # Mostrar métricas
    metrics = bus.get_metrics()
    logger.info(f"Bus metrics: {metrics}")
    
    # Cleanup
    comp1.unregister()
    comp2.unregister()
    bus.stop()

if __name__ == "__main__":
    asyncio.run(demo_advanced_features())