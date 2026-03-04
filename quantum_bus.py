#!/usr/bin/env python3
"""
Quantum Bus - Barramento singleton para módulos quânticos

Fornece comunicação entre módulos quânticos e faz bridge com o NeuralBus.
Implementa padrão singleton com thread safety.
"""

import threading
import time
import importlib
from typing import Any, Dict, Optional, Callable, List, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from functools import wraps

# Configuração de logging
logger = logging.getLogger(__name__)


class BusEventType(Enum):
    """Tipos de eventos suportados pelo barramento."""
    MODULE_REGISTERED = "module_registered"
    MODULE_UNREGISTERED = "module_unregistered"
    DATA_UPDATED = "data_updated"
    STATE_CHANGED = "state_changed"
    ERROR_OCCURRED = "error_occurred"
    CUSTOM = "custom"


@dataclass
class BusEvent:
    """Estrutura padronizada para eventos do barramento."""
    event_type: BusEventType
    source: str
    target: Optional[str] = None
    payload: Any = None
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converte evento para dicionário serializável."""
        return {
            "event_type": self.event_type.value,
            "source": self.source,
            "target": self.target,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


def synchronized(lock: threading.RLock):
    """Decorator para sincronização de métodos."""

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorator


class QuantumBus:
    """
    Barramento singleton para comunicação entre módulos quânticos.
    
    Implementa registro de módulos, sistema de publish/subscribe e bridge
    bidirecional com NeuralBus.
    
    Attributes:
        _instance: Instância singleton
        _lock: Lock para thread-safe singleton
    """
    
    _instance: Optional["QuantumBus"] = None
    _lock: threading.Lock = threading.Lock()
    
    def __init__(self):
        """Inicializa o barramento quântico (privado - usar get_instance)."""
        # Registro de módulos
        self._registry: Dict[str, Dict[str, Any]] = {}
        
        # Sistema de eventos
        self._subscriptions: Dict[str, List[Callable[[BusEvent], None]]] = {}
        self._wildcard_subscriptions: List[Callable[[BusEvent], None]] = []
        
        # Locks para thread safety
        self._reg_lock = threading.RLock()
        self._sub_lock = threading.RLock()
        
        # Bridge com NeuralBus
        self._neural_bridge = None
        self._bridge_initialized = False
        self._bridge_lock = threading.RLock()
        
        # Cache para performance
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._cache_ttl = 5.0  # 5 segundos
        
        # Estatísticas
        self._stats = {
            "events_sent": 0,
            "events_received": 0,
            "requests_served": 0,
            "bridge_calls": 0,
            "errors": 0
        }
        self._stats_lock = threading.RLock()
        
        logger.info("QuantumBus initialized")

    @classmethod
    def get_instance(cls) -> "QuantumBus":
        """
        Retorna a instância singleton do QuantumBus.
        
        Returns:
            Instância singleton do QuantumBus
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = QuantumBus()
            return cls._instance

    @synchronized
    def register(self, name: str, instance: Any,
                metadata: Optional[Dict[str, Any]]=None) -> bool:
        """
        Registra um módulo no barramento.
        
        Args:
            name: Nome único do módulo
            instance: Instância do módulo
            metadata: Metadados adicionais
            
        Returns:
            True se registro foi bem-sucedido
            
        Raises:
            ValueError: Se o nome já estiver registrado
        """
        if name in self._registry:
            raise ValueError(f"Módulo '{name}' já registrado")
        
        self._registry[name] = {
            "instance": instance,
            "metadata": metadata or {},
            "registered_at": time.time(),
            "last_accessed": time.time()
        }
        
        # Notificar registro
        event = BusEvent(
            event_type=BusEventType.MODULE_REGISTERED,
            source="quantum_bus",
            payload={"module": name, "metadata": metadata}
        )
        self._broadcast_local(event)
        
        logger.info(f"Módulo registrado: {name}")
        return True

    @synchronized
    def unregister(self, name: str) -> bool:
        """
        Remove um módulo do registro.
        
        Args:
            name: Nome do módulo a remover
            
        Returns:
            True se módulo foi removido
        """
        if name not in self._registry:
            logger.warning(f"Tentativa de remover módulo não registrado: {name}")
            return False
        
        del self._registry[name]
        
        # Notificar remoção
        event = BusEvent(
            event_type=BusEventType.MODULE_UNREGISTERED,
            source="quantum_bus",
            payload={"module": name}
        )
        self._broadcast_local(event)
        
        logger.info(f"Módulo removido: {name}")
        return True

    @synchronized
    def get(self, name: str, update_access: bool=True) -> Optional[Any]:
        """
        Retorna instância de um módulo registrado.
        
        Args:
            name: Nome do módulo
            update_access: Atualizar timestamp de acesso
            
        Returns:
            Instância do módulo ou None se não encontrado
        """
        if name not in self._registry:
            return None
        
        module_info = self._registry[name]
        if update_access:
            module_info["last_accessed"] = time.time()
        
        return module_info["instance"]

    @synchronized
    def get_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """Retorna metadados de um módulo."""
        if name in self._registry:
            return self._registry[name].get("metadata")
        return None

    @synchronized
    def list_modules(self) -> Dict[str, Dict[str, Any]]:
        """
        Lista todos os módulos registrados.
        
        Returns:
            Dicionário com informações dos módulos
        """
        result = {}
        for name, info in self._registry.items():
            result[name] = {
                "metadata": info["metadata"],
                "registered_at": info["registered_at"],
                "last_accessed": info["last_accessed"]
            }
        return result

    def subscribe(self, event_pattern: str,
                  handler: Callable[[BusEvent], None]) -> bool:
        """
        Inscreve um handler para eventos.
        
        Args:
            event_pattern: Padrão do evento (ou "*" para todos)
            handler: Função callback
            
        Returns:
            True se inscrição foi bem-sucedida
        """
        with self._sub_lock:
            if event_pattern == "*":
                if handler not in self._wildcard_subscriptions:
                    self._wildcard_subscriptions.append(handler)
                    logger.debug(f"Wildcard subscription added: {handler.__name__}")
                return True
            
            if event_pattern not in self._subscriptions:
                self._subscriptions[event_pattern] = []
            
            if handler not in self._subscriptions[event_pattern]:
                self._subscriptions[event_pattern].append(handler)
                logger.debug(f"Subscription added: {event_pattern} -> {handler.__name__}")
                return True
            
            return False

    def unsubscribe(self, event_pattern: str,
                    handler: Callable[[BusEvent], None]) -> bool:
        """
        Remove inscrição de um handler.
        
        Args:
            event_pattern: Padrão do evento
            handler: Função callback
            
        Returns:
            True se remoção foi bem-sucedida
        """
        with self._sub_lock:
            if event_pattern == "*":
                if handler in self._wildcard_subscriptions:
                    self._wildcard_subscriptions.remove(handler)
                    return True
                return False
            
            if event_pattern in self._subscriptions:
                if handler in self._subscriptions[event_pattern]:
                    self._subscriptions[event_pattern].remove(handler)
                    return True
            
            return False

    def broadcast(self, event: Union[str, BusEvent],
                  payload: Any=None,
                  source: str="unknown",
                  target: Optional[str]=None,
                  metadata: Optional[Dict[str, Any]]=None) -> bool:
        """
        Publica um evento no barramento.
        
        Args:
            event: Nome do evento ou objeto BusEvent
            payload: Dados do evento
            source: Origem do evento
            target: Destinatário específico (opcional)
            metadata: Metadados adicionais
            
        Returns:
            True se publicação foi bem-sucedida
        """
        try:
            # Criar objeto de evento se necessário
            if isinstance(event, str):
                bus_event = BusEvent(
                    event_type=BusEventType.CUSTOM,
                    source=source,
                    target=target,
                    payload=payload,
                    metadata=metadata or {}
                )
            else:
                bus_event = event
            
            # Atualizar estatísticas
            with self._stats_lock:
                self._stats["events_sent"] += 1
            
            # Notificar assinantes locais
            self._broadcast_local(bus_event)
            
            # Notificar módulos registrados
            self._notify_registered_modules(bus_event)
            
            # Encaminhar para NeuralBus se disponível
            if self._ensure_bridge():
                try:
                    with self._stats_lock:
                        self._stats["bridge_calls"] += 1
                    
                    self._neural_bridge.bridge_receive(
                        from_namespace="quantum",
                        event=bus_event.event_type.value,
                        payload=bus_event.to_dict()
                    )
                except Exception as e:
                    logger.error(f"Erro ao encaminhar para NeuralBus: {e}")
                    with self._stats_lock:
                        self._stats["errors"] += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao publicar evento: {e}")
            with self._stats_lock:
                self._stats["errors"] += 1
            return False

    def _broadcast_local(self, event: BusEvent) -> None:
        """Notifica assinantes locais do evento."""
        handlers = []
        
        with self._sub_lock:
            # Handlers específicos
            if event.event_type.value in self._subscriptions:
                handlers.extend(self._subscriptions[event.event_type.value])
            
            # Wildcard handlers
            handlers.extend(self._wildcard_subscriptions)
        
        # Executar handlers
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Erro no handler {handler.__name__}: {e}")

    def _notify_registered_modules(self, event: BusEvent) -> None:
        """Notifica módulos registrados que implementam on_quantum_event."""
        modules_to_notify = []
        
        with self._reg_lock:
            for name, info in self._registry.items():
                modules_to_notify.append((name, info["instance"]))
        
        for name, instance in modules_to_notify:
            try:
                callback = getattr(instance, "on_quantum_event", None)
                if callable(callback):
                    callback(event)
            except Exception as e:
                logger.error(f"Erro ao notificar módulo {name}: {e}")

    def request(self, target_name: str, method: str, *args,
                timeout: float=2.0, **kwargs) -> Tuple[bool, Any]:
        """
        Envia requisição para um módulo registrado.
        
        Args:
            target_name: Nome do módulo alvo
            method: Nome do método a chamar
            *args: Argumentos posicionais
            timeout: Timeout em segundos
            **kwargs: Argumentos nomeados
            
        Returns:
            Tupla (success, result_or_error)
        """
        start_time = time.time()
        
        try:
            # Tentar módulo local primeiro
            target = self.get(target_name)
            if target:
                fn = getattr(target, method, None)
                if callable(fn):
                    with self._stats_lock:
                        self._stats["requests_served"] += 1
                    
                    # Executar com timeout
                    result = self._execute_with_timeout(
                        fn, args, kwargs, timeout
                    )
                    return True, result
                else:
                    return False, AttributeError(
                        f"Método '{method}' não encontrado em '{target_name}'"
                    )
            
            # Tentar via bridge se disponível
            if self._ensure_bridge():
                try:
                    return self._neural_bridge.request_from_bridge(
                        target_name, method, args, kwargs, timeout=timeout
                    )
                except Exception as e:
                    return False, e
            
            return False, LookupError(f"Módulo '{target_name}' não encontrado")
            
        except Exception as e:
            logger.error(f"Erro na requisição {target_name}.{method}: {e}")
            with self._stats_lock:
                self._stats["errors"] += 1
            return False, e

    def _execute_with_timeout(self, func: Callable, args: tuple,
                             kwargs: dict, timeout: float) -> Any:
        """Executa função com timeout."""
        if timeout <= 0:
            return func(*args, **kwargs)
        
        result = None
        exception = None
        
        def worker():
            nonlocal result, exception
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                exception = e
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            raise TimeoutError(f"Timeout após {timeout} segundos")
        
        if exception:
            raise exception
        
        return result

    def _ensure_bridge(self) -> bool:
        """
        Inicializa bridge com NeuralBus se disponível.
        
        Returns:
            True se bridge está disponível
        """
        with self._bridge_lock:
            if self._bridge_initialized:
                return self._neural_bridge is not None
            
            self._bridge_initialized = True
            
            try:
                # Tentar importar NeuralBus dinamicamente
                neural_module = importlib.import_module("neural.neural_bus")
                NeuralBus = getattr(neural_module, "NeuralBus")
                self._neural_bridge = NeuralBus.get_instance()
                
                # Registrar callback no NeuralBus
                self._neural_bridge.register_bridge_callback("quantum", self)
                
                logger.info("Bridge com NeuralBus estabelecida")
                return True
                
            except ImportError:
                logger.debug("NeuralBus não disponível - operando em modo standalone")
                self._neural_bridge = None
                return False
            except Exception as e:
                logger.warning(f"Erro ao estabelecer bridge: {e}")
                self._neural_bridge = None
                return False

    def bridge_receive(self, from_namespace: str, event: str,
                       payload: Any) -> None:
        """
        Recebe eventos da ponte (neural -> quantum).
        
        Args:
            from_namespace: Namespace de origem
            event: Nome do evento
            payload: Dados do evento
        """
        try:
            with self._stats_lock:
                self._stats["events_received"] += 1
            
            # Criar evento
            bus_event = BusEvent(
                event_type=BusEventType.CUSTOM,
                source=f"{from_namespace}_bridge",
                payload=payload,
                metadata={"from_namespace": from_namespace}
            )
            
            # Publicar localmente
            self.broadcast(bus_event)
            
        except Exception as e:
            logger.error(f"Erro ao processar evento da bridge: {e}")

    def request_from_bridge(self, target_name: str, method: str,
                           args: tuple, kwargs: dict,
                           timeout: float=2.0) -> Tuple[bool, Any]:
        """
        Processa requisição da outra ponta da bridge.
        
        Args:
            target_name: Nome do módulo alvo
            method: Método a chamar
            args: Argumentos posicionais
            kwargs: Argumentos nomeados
            timeout: Timeout em segundos
            
        Returns:
            Tupla (success, result_or_error)
        """
        return self.request(target_name, method, *args, timeout=timeout, **kwargs)

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do barramento.
        
        Returns:
            Dicionário com estatísticas
        """
        with self._stats_lock:
            stats = self._stats.copy()
        
        with self._reg_lock:
            stats["modules_registered"] = len(self._registry)
        
        with self._sub_lock:
            stats["subscriptions"] = len(self._subscriptions)
            stats["wildcard_subscriptions"] = len(self._wildcard_subscriptions)
        
        return stats

    def clear_cache(self) -> None:
        """Limpa cache interno."""
        self._cache.clear()

    def shutdown(self) -> None:
        """
        Desliga o barramento de forma segura.
        
        Notifica todos os módulos e limpa recursos.
        """
        logger.info("Desligando QuantumBus...")
        
        # Notificar desligamento
        event = BusEvent(
            event_type=BusEventType.STATE_CHANGED,
            source="quantum_bus",
            payload={"action": "shutdown"}
        )
        self._broadcast_local(event)
        
        # Limpar registros
        with self._reg_lock:
            self._registry.clear()
        
        with self._sub_lock:
            self._subscriptions.clear()
            self._wildcard_subscriptions.clear()
        
        self.clear_cache()
        logger.info("QuantumBus desligado")

# ============================================================================
# MÓDULO DE OTIMIZAÇÃO QUÂNTICA
# ============================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Optimization Engine - Otimização com algoritmos quânticos

Implementa algoritmos de otimização quântica para parâmetros de estratégia,
incluindo Quantum Annealing e Variational Quantum Eigensolver (VQE).
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class OptimizationAlgorithm(Enum):
    """Algoritmos de otimização disponíveis."""
    QUANTUM_ANNEALING = "quantum_annealing"
    VQE = "variational_quantum_eigensolver"
    QAOA = "quantum_approximate_optimization_algorithm"
    GRADIENT_DESCENT = "gradient_descent"
    GENETIC_ALGORITHM = "genetic_algorithm"


class ConvergenceStatus(Enum):
    """Status de convergência da otimização."""
    CONVERGED = "converged"
    MAX_ITERATIONS = "max_iterations"
    NOT_CONVERGED = "not_converged"
    ERROR = "error"


@dataclass
class OptimizationResult:
    """Resultado completo de uma otimização."""
    optimal_value: float
    optimal_parameters: Dict[str, float]
    optimal_vector: Optional[np.ndarray] = None
    iterations: int = 0
    convergence_status: ConvergenceStatus = ConvergenceStatus.NOT_CONVERGED
    convergence_history: List[float] = field(default_factory=list)
    parameter_history: List[Dict[str, float]] = field(default_factory=list)
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte resultado para dicionário serializável."""
        return {
            "optimal_value": self.optimal_value,
            "optimal_parameters": self.optimal_parameters,
            "optimal_vector": self.optimal_vector.tolist() 
                if self.optimal_vector is not None else None,
            "iterations": self.iterations,
            "convergence_status": self.convergence_status.value,
            "convergence_history": self.convergence_history,
            "execution_time": self.execution_time,
            "metadata": self.metadata
        }


@dataclass
class OptimizationConfig:
    """Configuração para otimização."""
    algorithm: OptimizationAlgorithm
    max_iterations: int = 1000
    tolerance: float = 1e-6
    population_size: int = 50  # Para algoritmos genéticos
    learning_rate: float = 0.01  # Para gradient descent
    temperature: float = 1.0  # Para simulated annealing
    cooling_rate: float = 0.95
    quantum_shots: int = 1024  # Número de medições quânticas
    seed: Optional[int] = None


class QuantumOptimizationEngine:
    """
    Engine de otimização usando algoritmos quânticos e clássicos.
    
    Suporta múltiplos algoritmos de otimização com interface unificada.
    """
    
    def __init__(self, config: Optional[OptimizationConfig]=None):
        """
        Inicializa o engine de otimização.
        
        Args:
            config: Configuração da otimização (usa padrão se None)
        """
        self.config = config or OptimizationConfig(
            algorithm=OptimizationAlgorithm.QUANTUM_ANNEALING
        )
        
        # Histórico de execuções
        self.history: List[OptimizationResult] = []
        
        # Random seed
        if self.config.seed is not None:
            np.random.seed(self.config.seed)
        
        # Executor para paralelização
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Registro no QuantumBus
        self._register_with_bus()
        
        logger.info(f"QuantumOptimizationEngine inicializado com algoritmo: "
                   f"{self.config.algorithm.value}")

    def _register_with_bus(self) -> None:
        """Registra engine no QuantumBus."""
        try:
            bus = QuantumBus.get_instance()
            bus.register(
                name="optimization_engine",
                instance=self,
                metadata={
                    "type": "optimization",
                    "algorithm": self.config.algorithm.value,
                    "version": "1.0.0"
                }
            )
            logger.info("OptimizationEngine registrado no QuantumBus")
        except Exception as e:
            logger.warning(f"Não foi possível registrar no QuantumBus: {e}")

    def optimize(self, objective_function: Callable[[Dict[str, float]], float],
                 parameter_bounds: Dict[str, Tuple[float, float]],
                 initial_guess: Optional[Dict[str, float]]=None) -> OptimizationResult:
        """
        Otimiza parâmetros usando o algoritmo configurado.
        
        Args:
            objective_function: Função objetivo a minimizar
            parameter_bounds: Limites para cada parâmetro
            initial_guess: Palpite inicial (opcional)
            
        Returns:
            Resultado da otimização
        """
        start_time = time.time()
        
        try:
            # Validar inputs
            self._validate_inputs(parameter_bounds, initial_guess)
            
            # Selecionar algoritmo
            algorithm_map = {
                OptimizationAlgorithm.QUANTUM_ANNEALING: self._quantum_annealing,
                OptimizationAlgorithm.VQE: self._variational_quantum_eigensolver,
                OptimizationAlgorithm.QAOA: self._quantum_approximate_optimization,
                OptimizationAlgorithm.GRADIENT_DESCENT: self._gradient_descent,
                OptimizationAlgorithm.GENETIC_ALGORITHM: self._genetic_algorithm,
            }
            
            optimizer = algorithm_map.get(self.config.algorithm)
            if optimizer is None:
                raise ValueError(f"Algoritmo não suportado: {self.config.algorithm}")
            
            # Executar otimização
            result = optimizer(objective_function, parameter_bounds, initial_guess)
            result.execution_time = time.time() - start_time
            
            # Armazenar no histórico
            self.history.append(result)
            
            # Notificar via bus
            self._notify_optimization_complete(result)
            
            logger.info(f"Otimização concluída em {result.execution_time:.2f}s: "
                       f"valor={result.optimal_value:.6f}, "
                       f"iterações={result.iterations}, "
                       f"status={result.convergence_status.value}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na otimização: {e}")
            return self._create_error_result(e, time.time() - start_time)

    def _validate_inputs(self, parameter_bounds: Dict[str, Tuple[float, float]],
                        initial_guess: Optional[Dict[str, float]]) -> None:
        """Valida parâmetros de entrada."""
        if not parameter_bounds:
            raise ValueError("parameter_bounds não pode ser vazio")
        
        for param_name, (lower, upper) in parameter_bounds.items():
            if lower >= upper:
                raise ValueError(f"Limites inválidos para {param_name}: {lower} >= {upper}")
        
        if initial_guess:
            for param_name, value in initial_guess.items():
                if param_name not in parameter_bounds:
                    raise ValueError(f"Parâmetro {param_name} não definido em bounds")
                lower, upper = parameter_bounds[param_name]
                if not (lower <= value <= upper):
                    raise ValueError(f"Valor inicial {value} fora dos limites para {param_name}")

    def _quantum_annealing(self, objective_function: Callable,
                          parameter_bounds: Dict[str, Tuple[float, float]],
                          initial_guess: Optional[Dict[str, float]]) -> OptimizationResult:
        """
        Implementa Quantum Annealing simplificado.
        
        Args:
            objective_function: Função objetivo
            parameter_bounds: Limites dos parâmetros
            initial_guess: Palpite inicial
            
        Returns:
            Resultado da otimização
        """
        param_names = list(parameter_bounds.keys())
        n_params = len(param_names)
        
        # Inicializar parâmetros
        if initial_guess:
            current_params = np.array([initial_guess[name] for name in param_names])
        else:
            # Ponto médio dos bounds
            current_params = np.array([
                (lower + upper) / 2 for lower, upper in parameter_bounds.values()
            ])
        
        current_value = objective_function(dict(zip(param_names, current_params)))
        
        # Histórico
        convergence_history = [current_value]
        parameter_history = [dict(zip(param_names, current_params))]
        
        temperature = self.config.temperature
        best_params = current_params.copy()
        best_value = current_value
        
        for iteration in range(self.config.max_iterations):
            # Propor novo ponto (tunelamento quântico)
            delta = np.random.randn(n_params) * temperature
            new_params = current_params + delta
            
            # Aplicar bounds
            for i, (lower, upper) in enumerate(parameter_bounds.values()):
                new_params[i] = np.clip(new_params[i], lower, upper)
            
            # Avaliar novo ponto
            new_value = objective_function(dict(zip(param_names, new_params)))
            
            # Critério de aceitação (com tunelamento)
            delta_energy = new_value - current_value
            acceptance_prob = np.exp(-delta_energy / temperature)
            
            if delta_energy < 0 or np.random.random() < acceptance_prob:
                current_params = new_params
                current_value = new_value
                
                # Atualizar melhor
                if new_value < best_value:
                    best_params = new_params.copy()
                    best_value = new_value
            
            # Registrar histórico
            convergence_history.append(current_value)
            parameter_history.append(dict(zip(param_names, current_params)))
            
            # Resfriamento
            temperature *= self.config.cooling_rate
            
            # Critério de convergência
            if len(convergence_history) > 10:
                recent_improvement = abs(convergence_history[-10] - convergence_history[-1])
                if recent_improvement < self.config.tolerance:
                    return OptimizationResult(
                        optimal_value=best_value,
                        optimal_parameters=dict(zip(param_names, best_params)),
                        optimal_vector=best_params,
                        iterations=iteration + 1,
                        convergence_status=ConvergenceStatus.CONVERGED,
                        convergence_history=convergence_history,
                        parameter_history=parameter_history,
                        metadata={"algorithm": "quantum_annealing"}
                    )
        
        return OptimizationResult(
            optimal_value=best_value,
            optimal_parameters=dict(zip(param_names, best_params)),
            optimal_vector=best_params,
            iterations=self.config.max_iterations,
            convergence_status=ConvergenceStatus.MAX_ITERATIONS,
            convergence_history=convergence_history,
            parameter_history=parameter_history,
            metadata={"algorithm": "quantum_annealing"}
        )

    def _variational_quantum_eigensolver(self, objective_function: Callable,
                                        parameter_bounds: Dict[str, Tuple[float, float]],
                                        initial_guess: Optional[Dict[str, float]]) -> OptimizationResult:
        """
        Implementa Variational Quantum Eigensolver (VQE) simplificado.
        
        Args:
            objective_function: Função objetivo
            parameter_bounds: Limites dos parâmetros
            initial_guess: Palpite inicial
            
        Returns:
            Resultado da otimização
        """
        # Implementação simplificada do VQE
        # Em implementação real, isso usaria um circuito quântico
        param_names = list(parameter_bounds.keys())
        n_params = len(param_names)
        
        # Parâmetros do ansatz
        if initial_guess:
            theta = np.array([initial_guess[name] for name in param_names])
        else:
            theta = np.random.uniform(0, 2 * np.pi, size=n_params)
        
        best_theta = theta.copy()
        best_value = float('inf')
        convergence_history = []
        parameter_history = []
        
        learning_rate = 0.1
        
        for iteration in range(self.config.max_iterations):
            # Avaliar função custo
            current_params = dict(zip(param_names, theta))
            current_value = objective_function(current_params)
            
            # Estimativa de gradiente quântico
            gradient = np.zeros_like(theta)
            for i in range(n_params):
                # Shift de parâmetro para estimativa de gradiente
                theta_plus = theta.copy()
                theta_plus[i] += np.pi / 2
                value_plus = objective_function(dict(zip(param_names, theta_plus)))
                
                theta_minus = theta.copy()
                theta_minus[i] -= np.pi / 2
                value_minus = objective_function(dict(zip(param_names, theta_minus)))
                
                gradient[i] = (value_plus - value_minus) / 2
            
            # Atualizar parâmetros
            theta -= learning_rate * gradient
            
            # Aplicar bounds
            for i, (lower, upper) in enumerate(parameter_bounds.values()):
                theta[i] = np.clip(theta[i], lower, upper)
            
            # Atualizar melhor valor
            if current_value < best_value:
                best_value = current_value
                best_theta = theta.copy()
            
            # Registrar histórico
            convergence_history.append(current_value)
            parameter_history.append(current_params.copy())
            
            # Verificar convergência
            if len(convergence_history) > 5:
                improvement = abs(convergence_history[-5] - convergence_history[-1])
                if improvement < self.config.tolerance:
                    return OptimizationResult(
                        optimal_value=best_value,
                        optimal_parameters=dict(zip(param_names, best_theta)),
                        optimal_vector=best_theta,
                        iterations=iteration + 1,
                        convergence_status=ConvergenceStatus.CONVERGED,
                        convergence_history=convergence_history,
                        parameter_history=parameter_history,
                        metadata={"algorithm": "vqe"}
                    )
            
            # Reduzir learning rate
            learning_rate *= 0.99
        
        return OptimizationResult(
            optimal_value=best_value,
            optimal_parameters=dict(zip(param_names, best_theta)),
            optimal_vector=best_theta,
            iterations=self.config.max_iterations,
            convergence_status=ConvergenceStatus.MAX_ITERATIONS,
            convergence_history=convergence_history,
            parameter_history=parameter_history,
            metadata={"algorithm": "vqe"}
        )

    def _quantum_approximate_optimization(self, objective_function: Callable,
                                         parameter_bounds: Dict[str, Tuple[float, float]],
                                         initial_guess: Optional[Dict[str, float]]) -> OptimizationResult:
        """
        Implementa Quantum Approximate Optimization Algorithm (QAOA) simplificado.
        """
        # Similar ao VQE, mas com estrutura específica do QAOA
        return self._variational_quantum_eigensolver(
            objective_function, parameter_bounds, initial_guess
        )

    def _gradient_descent(self, objective_function: Callable,
                         parameter_bounds: Dict[str, Tuple[float, float]],
                         initial_guess: Optional[Dict[str, float]]) -> OptimizationResult:
        """
        Implementa Gradient Descent clássico.
        """
        param_names = list(parameter_bounds.keys())
        n_params = len(param_names)
        
        if initial_guess:
            params = np.array([initial_guess[name] for name in param_names])
        else:
            params = np.array([(lower + upper) / 2 
                             for lower, upper in parameter_bounds.values()])
        
        convergence_history = []
        parameter_history = []
        learning_rate = self.config.learning_rate
        
        for iteration in range(self.config.max_iterations):
            # Avaliar
            current_params = dict(zip(param_names, params))
            current_value = objective_function(current_params)
            convergence_history.append(current_value)
            parameter_history.append(current_params.copy())
            
            # Estimativa numérica do gradiente
            gradient = np.zeros(n_params)
            epsilon = 1e-8
            
            for i in range(n_params):
                params_plus = params.copy()
                params_plus[i] += epsilon
                value_plus = objective_function(dict(zip(param_names, params_plus)))
                
                params_minus = params.copy()
                params_minus[i] -= epsilon
                value_minus = objective_function(dict(zip(param_names, params_minus)))
                
                gradient[i] = (value_plus - value_minus) / (2 * epsilon)
            
            # Atualizar parâmetros
            params -= learning_rate * gradient
            
            # Aplicar bounds
            for i, (lower, upper) in enumerate(parameter_bounds.values()):
                params[i] = np.clip(params[i], lower, upper)
            
            # Verificar convergência
            if len(convergence_history) > 1:
                improvement = abs(convergence_history[-2] - convergence_history[-1])
                if improvement < self.config.tolerance:
                    return OptimizationResult(
                        optimal_value=current_value,
                        optimal_parameters=current_params,
                        optimal_vector=params,
                        iterations=iteration + 1,
                        convergence_status=ConvergenceStatus.CONVERGED,
                        convergence_history=convergence_history,
                        parameter_history=parameter_history,
                        metadata={"algorithm": "gradient_descent"}
                    )
            
            # Reduzir learning rate
            learning_rate *= 0.995
        
        final_value = objective_function(dict(zip(param_names, params)))
        return OptimizationResult(
            optimal_value=final_value,
            optimal_parameters=dict(zip(param_names, params)),
            optimal_vector=params,
            iterations=self.config.max_iterations,
            convergence_status=ConvergenceStatus.MAX_ITERATIONS,
            convergence_history=convergence_history,
            parameter_history=parameter_history,
            metadata={"algorithm": "gradient_descent"}
        )

    def _genetic_algorithm(self, objective_function: Callable,
                          parameter_bounds: Dict[str, Tuple[float, float]],
                          initial_guess: Optional[Dict[str, float]]) -> OptimizationResult:
        """
        Implementa algoritmo genético para otimização.
        """
        param_names = list(parameter_bounds.keys())
        n_params = len(param_names)
        population_size = self.config.population_size
        
        # Inicializar população
        population = []
        if initial_guess:
            # Incluir palpite inicial
            initial_individual = np.array([initial_guess[name] for name in param_names])
            population.append(initial_individual)
        
        # Preencher população com indivíduos aleatórios
        while len(population) < population_size:
            individual = np.array([
                np.random.uniform(low, high) 
                for low, high in parameter_bounds.values()
            ])
            population.append(individual)
        
        convergence_history = []
        best_individual = None
        best_value = float('inf')
        
        for generation in range(self.config.max_iterations // population_size):
            # Avaliar fitness
            fitness = []
            for individual in population:
                params_dict = dict(zip(param_names, individual))
                value = objective_function(params_dict)
                fitness.append(value)
                
                if value < best_value:
                    best_value = value
                    best_individual = individual.copy()
            
            convergence_history.append(best_value)
            
            # Selecionar pais (roleta viciada)
            fitness_array = np.array(fitness)
            fitness_array = np.max(fitness_array) - fitness_array + 1e-10
            probabilities = fitness_array / fitness_array.sum()
            
            # Gerar nova população
            new_population = []
            
            # Elitismo: manter o melhor
            if best_individual is not None:
                new_population.append(best_individual.copy())
            
            while len(new_population) < population_size:
                # Selecionar pais
                parent_indices = np.random.choice(
                    len(population), size=2, p=probabilities
                )
                parent1 = population[parent_indices[0]]
                parent2 = population[parent_indices[1]]
                
                # Cruzamento (crossover)
                crossover_point = np.random.randint(1, n_params - 1)
                child = np.concatenate([
                    parent1[:crossover_point],
                    parent2[crossover_point:]
                ])
                
                # Mutação
                if np.random.random() < 0.1:  # 10% de chance de mutação
                    mutation_point = np.random.randint(n_params)
                    low, high = list(parameter_bounds.values())[mutation_point]
                    child[mutation_point] = np.random.uniform(low, high)
                
                new_population.append(child)
            
            population = new_population
            
            # Verificar convergência
            if len(convergence_history) > 10:
                improvement = abs(convergence_history[-10] - convergence_history[-1])
                if improvement < self.config.tolerance:
                    return OptimizationResult(
                        optimal_value=best_value,
                        optimal_parameters=dict(zip(param_names, best_individual)),
                        optimal_vector=best_individual,
                        iterations=generation * population_size,
                        convergence_status=ConvergenceStatus.CONVERGED,
                        convergence_history=convergence_history,
                        metadata={"algorithm": "genetic_algorithm"}
                    )
        
        return OptimizationResult(
            optimal_value=best_value,
            optimal_parameters=dict(zip(param_names, best_individual)),
            optimal_vector=best_individual,
            iterations=self.config.max_iterations,
            convergence_status=ConvergenceStatus.MAX_ITERATIONS,
            convergence_history=convergence_history,
            metadata={"algorithm": "genetic_algorithm"}
        )

    def _create_error_result(self, error: Exception, execution_time: float) -> OptimizationResult:
        """Cria resultado de erro."""
        return OptimizationResult(
            optimal_value=float('inf'),
            optimal_parameters={},
            iterations=0,
            convergence_status=ConvergenceStatus.ERROR,
            execution_time=execution_time,
            metadata={"error": str(error), "error_type": type(error).__name__}
        )

    def _notify_optimization_complete(self, result: OptimizationResult) -> None:
        """Notifica conclusão da otimização via QuantumBus."""
        try:
            bus = QuantumBus.get_instance()
            bus.broadcast(
                event="optimization_complete",
                payload=result.to_dict(),
                source="optimization_engine"
            )
        except Exception as e:
            logger.debug(f"Não foi possível notificar otimização: {e}")

    def optimize_multiple(self, objective_functions: List[Callable],
                         parameter_bounds_list: List[Dict[str, Tuple[float, float]]],
                         parallel: bool=True) -> List[OptimizationResult]:
        """
        Otimiza múltiplas funções objetivo simultaneamente.
        
        Args:
            objective_functions: Lista de funções objetivo
            parameter_bounds_list: Lista de limites de parâmetros
            parallel: Executar em paralelo
            
        Returns:
            Lista de resultados
        """
        if len(objective_functions) != len(parameter_bounds_list):
            raise ValueError("Número de funções e bounds deve ser igual")
        
        if parallel and len(objective_functions) > 1:
            futures = []
            for func, bounds in zip(objective_functions, parameter_bounds_list):
                future = self.executor.submit(self.optimize, func, bounds)
                futures.append(future)
            
            results = []
            for future in as_completed(futures):
                results.append(future.result())
            
            return results
        else:
            return [self.optimize(func, bounds) 
                   for func, bounds in zip(objective_functions, parameter_bounds_list)]

    def get_history(self, limit: Optional[int]=None) -> List[Dict[str, Any]]:
        """
        Retorna histórico de otimizações.
        
        Args:
            limit: Número máximo de resultados a retornar
            
        Returns:
            Lista de resultados em formato de dicionário
        """
        if limit:
            history = self.history[-limit:]
        else:
            history = self.history
        
        return [result.to_dict() for result in history]

    def clear_history(self) -> None:
        """Limpa histórico de otimizações."""
        self.history.clear()

    def on_quantum_event(self, event: Any) -> None:
        """
        Callback para eventos do QuantumBus.
        
        Args:
            event: Evento recebido
        """
        try:
            if isinstance(event, BusEvent):
                event_type = event.event_type
                
                if event_type == BusEventType.CUSTOM:
                    if event.payload and isinstance(event.payload, dict):
                        action = event.payload.get("action")
                        
                        if action == "optimize":
                            # Processar requisição de otimização
                            objective_data = event.payload.get("objective")
                            bounds = event.payload.get("bounds")
                            
                            if objective_data and bounds:
                                # Aqui você criaria a função objetivo dos dados
                                # Por simplicidade, vamos apenas logar
                                logger.info(f"Recebida requisição de otimização: {event.payload}")
        except Exception as e:
            logger.error(f"Erro ao processar evento: {e}")

    def shutdown(self) -> None:
        """Desliga o engine de forma segura."""
        logger.info("Desligando QuantumOptimizationEngine...")
        self.executor.shutdown(wait=True)
        logger.info("QuantumOptimizationEngine desligado")

# ============================================================================
# FUNÇÕES AUXILIARES E EXEMPLOS
# ============================================================================


def create_sample_objective_function(optimal_point: Dict[str, float]=None) -> Callable:
    """
    Cria função objetivo de exemplo (esfera n-dimensional).
    
    Args:
        optimal_point: Ponto ótimo (se None, usa origem)
    
    Returns:
        Função objetivo
    """
    if optimal_point is None:
        optimal_point = {f"x{i}": 0.0 for i in range(3)}
    
    def objective(params: Dict[str, float]) -> float:
        value = 0.0
        for key, param_value in params.items():
            if key in optimal_point:
                diff = param_value - optimal_point[key]
                value += diff ** 2
        return value
    
    return objective


def main():
    """Função principal de demonstração."""
    import json
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Demonstração Quantum Optimization Engine")
    print("=" * 50)
    
    try:
        # Criar engine com Quantum Annealing
        config = OptimizationConfig(
            algorithm=OptimizationAlgorithm.QUANTUM_ANNEALING,
            max_iterations=200,
            tolerance=1e-4,
            seed=42
        )
        
        engine = QuantumOptimizationEngine(config)
        
        # Definir problema de otimização
        bounds = {
            "x1": (-5.0, 5.0),
            "x2": (-5.0, 5.0),
            "x3": (-5.0, 5.0)
        }
        
        optimal_point = {"x1": 1.5, "x2":-2.0, "x3": 0.5}
        objective_func = create_sample_objective_function(optimal_point)
        
        print(f"\n🔍 Otimizando função esfera com ótimo em {optimal_point}")
        print(f"📐 Parâmetros: {list(bounds.keys())}")
        print(f"🎯 Algoritmo: {config.algorithm.value}")
        
        # Executar otimização
        result = engine.optimize(objective_func, bounds)
        
        print(f"\n✅ Resultado:")
        print(f"   Valor ótimo: {result.optimal_value:.6f}")
        print(f"   Parâmetros ótimos: {result.optimal_parameters}")
        print(f"   Iterações: {result.iterations}")
        print(f"   Status: {result.convergence_status.value}")
        print(f"   Tempo: {result.execution_time:.2f}s")
        
        # Mostrar histórico
        print(f"\n📊 Histórico (últimos 5 valores):")
        if result.convergence_history:
            for i, val in enumerate(result.convergence_history[-5:]):
                print(f"   Iteração {i+1}: {val:.6f}")
        
        # Testar múltiplas otimizações
        print(f"\n🧪 Testando otimização múltipla...")
        
        bounds_list = [
            {"x": (-10, 10), "y": (-10, 10)},
            {"a": (-5, 5), "b": (-5, 5), "c": (-5, 5)}
        ]
        
        objectives = [
            lambda p: p["x"] ** 2 + p["y"] ** 2,
            lambda p: p["a"] ** 2 + p["b"] ** 2 + p["c"] ** 2
        ]
        
        results = engine.optimize_multiple(objectives, bounds_list, parallel=True)
        
        for i, res in enumerate(results):
            print(f"\n   Problema {i+1}:")
            print(f"      Valor: {res.optimal_value:.6f}")
            print(f"      Status: {res.convergence_status.value}")
        
        # Estatísticas do QuantumBus
        bus = QuantumBus.get_instance()
        stats = bus.get_stats()
        
        print(f"\n📡 Estatísticas QuantumBus:")
        print(f"   Módulos registrados: {stats.get('modules_registered', 0)}")
        print(f"   Eventos enviados: {stats.get('events_sent', 0)}")
        print(f"   Eventos recebidos: {stats.get('events_received', 0)}")
        print(f"   Requisições servidas: {stats.get('requests_served', 0)}")
        
        # Desligar
        engine.shutdown()
        bus.shutdown()
        
        print(f"\n🎉 Demonstração concluída com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
