import asyncio
import random
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor

# --- TIPOS & INTERFACES ---

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class SystemMode(Enum):
    SAFE = "SAFE"
    BALANCED = "BALANCED"
    QUANTUM = "QUANTUM"
    AGGRESSIVE = "AGGRESSIVE"
    PASSIVE = "PASSIVE"

class ActionType(Enum):
    BUY_SIGNAL = "BUY_SIGNAL"
    SELL_SIGNAL = "SELL_SIGNAL"
    HOLD = "HOLD"
    OPTIMIZE = "OPTIMIZE"
    RECALIBRATE = "RECALIBRATE"

@dataclass
class AutoLog:
    """Log do sistema autônomo"""
    id: str
    timestamp: datetime
    level: LogLevel
    module: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def format_log(self) -> str:
        """Formata log para exibição"""
        return f"[{self.timestamp.strftime('%H:%M:%S')}] [{self.level.value}] {self.module}: {self.message}"
    
    def get_log_info(self) -> Dict[str, Any]:
        """Retorna informações do log"""
        return {
            'id': self.id,
            'time': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'level': self.level.value,
            'module': self.module,
            'message': self.message,
            'metadata': self.metadata
        }

@dataclass
class SystemHealth:
    """Saúde do sistema"""
    cpu_load: float = 0.0  # 0-100%
    memory_usage: float = 0.0  # 0-100%
    network_latency: float = 20.0  # ms
    integrity_score: float = 100.0  # 0-100
    last_sync: datetime = field(default_factory=datetime.now)
    active_threads: int = 0
    error_rate: float = 0.0  # 0-1
    uptime: float = 0.0  # segundos
    
    def __post_init__(self):
        if self.cpu_load > 100:
            self.cpu_load = 100.0
        if self.memory_usage > 100:
            self.memory_usage = 100.0
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Retorna resumo da saúde do sistema"""
        status = "HEALTHY"
        if self.integrity_score < 70:
            status = "DEGRADED"
        if self.integrity_score < 40:
            status = "CRITICAL"
        
        return {
            'status': status,
            'cpu': f"{self.cpu_load:.1f}%",
            'memory': f"{self.memory_usage:.1f}%",
            'latency': f"{self.network_latency:.1f}ms",
            'integrity': f"{self.integrity_score:.1f}/100",
            'last_sync': self.last_sync.strftime('%H:%M:%S'),
            'uptime': f"{self.uptime:.0f}s"
        }

@dataclass
class AutoSystemConfig:
    """Configuração do sistema autônomo"""
    execution_interval: int = 1000  # ms
    monitoring_interval: int = 5000  # ms
    adjustment_threshold: float = 0.02  # 2%
    sync_interval: int = 30000  # ms
    max_retry_attempts: int = 3
    active_mode: SystemMode = SystemMode.BALANCED
    enable_agi_integration: bool = True
    enable_self_optimization: bool = True
    max_concurrent_operations: int = 5
    
    def update(self, **kwargs):
        """Atualiza configuração"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

# --- SIMULAÇÃO DAS DEPENDÊNCIAS ---

class SentimentVector:
    """Vetor de sentimentos (simulação)"""
    
    def __init__(self):
        self.confidence = random.uniform(60, 90)
        self.stability = random.uniform(60, 90)
        self.focus = random.uniform(60, 90)
        self.aggression = random.uniform(10, 40)
        self.curiosity = random.uniform(50, 90)
        self.timestamp = datetime.now()
    
    def update(self):
        """Atualiza sentimentos com variação aleatória"""
        for attr in ['confidence', 'stability', 'focus', 'aggression', 'curiosity']:
            current = getattr(self, attr)
            change = random.uniform(-5, 5)
            setattr(self, attr, max(0.0, min(100.0, current + change)))
        self.timestamp = datetime.now()

class SentientCore:
    """Núcleo Senciente (simulação)"""
    
    def __init__(self):
        self.vector = SentimentVector()
        self.thoughts = []
        self.state = "ANALYTICAL"
    
    def get_vector(self) -> SentimentVector:
        """Retorna vetor de sentimentos"""
        self.vector.update()  # Atualiza com variação aleatória
        return self.vector
    
    def add_thought(self, thought: str):
        """Adiciona pensamento"""
        self.thoughts.append({
            'timestamp': datetime.now(),
            'thought': thought
        })
        if len(self.thoughts) > 100:
            self.thoughts = self.thoughts[-100:]
    
    def get_state(self) -> str:
        """Retorna estado atual"""
        if self.vector.stability < 40:
            return "ANXIOUS"
        elif self.vector.confidence > 80 and self.vector.focus > 80:
            return "FOCUSED_CONFIDENT"
        elif self.vector.aggression > 70:
            return "AGGRESSIVE"
        else:
            return "ANALYTICAL"

class QuantumNeuralNetwork:
    """Rede Neural Quântica (simulação)"""
    
    def __init__(self):
        self.initialized = False
        self.prediction_history = []
    
    async def initialize(self):
        """Inicializa a rede"""
        await asyncio.sleep(0.5)  # Simula inicialização
        self.initialized = True
        print("⚛️ Núcleo Executivo Quântico inicializado")
    
    async def predict(self, inputs: List[float]) -> Dict[str, Any]:
        """Faz uma predição"""
        if not self.initialized:
            await self.initialize()
        
        # Simulação de predição quântica
        weighted_sum = sum(inputs) / len(inputs) if inputs else 0.5
        quantum_noise = random.uniform(-0.15, 0.15)  # Ruído quântico
        
        prediction = max(0.0, min(1.0, weighted_sum + quantum_noise))
        
        # Calcula confiança baseada na coerência
        coherence = 1.0 - abs(quantum_noise) * 3
        confidence = 0.7 + (coherence * 0.3)
        
        result = {
            'prediction': prediction,
            'confidence': confidence,
            'coherence': coherence,
            'quantum_state': "SUPERPOSITION_MEASURED",
            'inputs': inputs
        }
        
        self.prediction_history.append({
            'timestamp': datetime.now(),
            'result': result
        })
        
        if len(self.prediction_history) > 1000:
            self.prediction_history = self.prediction_history[-1000:]
        
        return result

class MemorySystem:
    """Sistema de Memória (simulação)"""
    
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.working_memory = WorkingMemory()
    
    def add_experience(self, experience: Dict[str, Any], priority: int = 1):
        """Adiciona experiência"""
        self.short_term.store(experience, priority)
        
        # Se alta prioridade, também armazena em longo prazo
        if priority >= 2:
            self.long_term.archive(experience)

class ShortTermMemory:
    """Memória de Curto Prazo"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.memories = []
    
    def store(self, memory: Dict[str, Any], priority: int = 1):
        """Armazena memória"""
        memory_with_meta = {
            **memory,
            'timestamp': datetime.now(),
            'priority': priority,
            'id': f"STM-{int(time.time())}-{random.randint(1000, 9999)}"
        }
        
        self.memories.append(memory_with_meta)
        
        # Mantém capacidade
        if len(self.memories) > self.capacity:
            # Remove memórias de baixa prioridade primeiro
            self.memories.sort(key=lambda x: x.get('priority', 0))
            self.memories = self.memories[-self.capacity:]
    
    def retrieve(self, pattern: Optional[Dict[str, Any]] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera memórias"""
        if not pattern:
            return self.memories[-limit:] if self.memories else []
        
        # Filtra por padrão (simplificado)
        results = []
        for memory in reversed(self.memories):
            if all(memory.get(k) == v for k, v in pattern.items()):
                results.append(memory)
            if len(results) >= limit:
                break
        
        return results

class LongTermMemory:
    """Memória de Longo Prazo"""
    
    def __init__(self):
        self.archives = []
        self.categories = {}
    
    def archive(self, memory: Dict[str, Any]):
        """Arquiva memória"""
        archived = {
            **memory,
            'archived_at': datetime.now(),
            'id': f"LTM-{int(time.time())}-{random.randint(1000, 9999)}"
        }
        
        self.archives.append(archived)
        
        # Categoriza automaticamente
        memory_type = memory.get('type', 'UNKNOWN')
        if memory_type not in self.categories:
            self.categories[memory_type] = []
        self.categories[memory_type].append(archived)

class WorkingMemory:
    """Memória de Trabalho"""
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.active_items = []
    
    def load(self, item: Dict[str, Any]):
        """Carrega item na memória de trabalho"""
        self.active_items.append({
            **item,
            'loaded_at': datetime.now(),
            'access_count': 0
        })
        
        if len(self.active_items) > self.capacity:
            # Remove item menos acessado
            self.active_items.sort(key=lambda x: x.get('access_count', 0))
            self.active_items = self.active_items[-self.capacity:]
    
    def access(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Acessa um item"""
        for item in self.active_items:
            if item.get('id') == item_id:
                item['access_count'] = item.get('access_count', 0) + 1
                item['last_accessed'] = datetime.now()
                return item
        return None

# Instâncias dedicadas para decisões executivas rápidas
executive_core = QuantumNeuralNetwork()
sentient_core = SentientCore()
memory_system = MemorySystem()

# --- SERVIÇO DE SISTEMA AUTÔNOMO ---

class AutonomousSystemService:
    """Serviço de Sistema Autônomo"""
    
    def __init__(self):
        self.config = AutoSystemConfig()
        self.logs: List[AutoLog] = []
        self.active = False
        self.health = SystemHealth()
        self.start_time = datetime.now()
        
        # Referências de intervalos
        self.exec_interval_id = None
        self.monitor_interval_id = None
        self.sync_interval_id = None
        
        # Executor para operações concorrentes
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_operations)
        
        # Estatísticas
        self.stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'mode_changes': 0,
            'last_error': None,
            'average_decision_time': 0.0
        }
        
        self.log("Sistema Autônomo Inicializado", LogLevel.INFO, "SYSTEM")
        print("🤖 Sistema Autônomo: Pronto para inicialização")
    
    def log(self, message: str, level: LogLevel, module: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Registra log do sistema
        
        Args:
            message: Mensagem do log
            level: Nível do log
            module: Módulo origem
            metadata: Metadados adicionais
        """
        log = AutoLog(
            id=f"LOG-{int(time.time()*1000)}-{random.randint(1000, 9999)}",
            timestamp=datetime.now(),
            level=level,
            module=module,
            message=message,
            metadata=metadata or {}
        )
        
        self.logs.insert(0, log)
        
        # Limita logs
        if len(self.logs) > 200:
            self.logs = self.logs[:200]
        
        # Exibe logs importantes
        if level in [LogLevel.ERROR, LogLevel.CRITICAL, LogLevel.WARNING]:
            print(f"📝 {log.format_log()}")
    
    def toggle_system(self):
        """Alterna estado do sistema"""
        if self.active:
            self.stop()
        else:
            self.start()
    
    async def start(self):
        """Inicia o sistema autônomo"""
        if self.active:
            self.log("Sistema já está ativo", LogLevel.WARNING, "CORE")
            return
        
        self.active = True
        self.start_time = datetime.now()
        self.log("Iniciando Protocolos Autônomos...", LogLevel.INFO, "CORE")
        
        try:
            # Inicializa núcleo executivo
            await executive_core.initialize()
            
            # Inicia loops em threads separadas
            self._start_loops()
            
            self.log("Sistema Autônomo Ativado com Sucesso", LogLevel.INFO, "CORE")
            print("✅ Sistema Autônomo: ATIVADO")
            
        except Exception as e:
            self.log(f"Erro ao iniciar sistema: {str(e)}", LogLevel.ERROR, "CORE")
            self.active = False
            raise
    
    def _start_loops(self):
        """Inicia os loops de execução em threads separadas"""
        # Loop de execução
        self.exec_interval_id = threading.Thread(
            target=self._run_execution_loop,
            daemon=True
        )
        self.exec_interval_id.start()
        
        # Loop de monitoramento
        self.monitor_interval_id = threading.Thread(
            target=self._run_monitoring_loop,
            daemon=True
        )
        self.monitor_interval_id.start()
        
        # Loop de sincronização
        self.sync_interval_id = threading.Thread(
            target=self._run_sync_loop,
            daemon=True
        )
        self.sync_interval_id.start()
    
    def stop(self):
        """Para o sistema autônomo"""
        if not self.active:
            return
        
        self.active = False
        
        # Para threads (elas são daemon, então serão encerradas)
        if self.exec_interval_id and self.exec_interval_id.is_alive():
            self.exec_interval_id.join(timeout=1.0)
        
        if self.monitor_interval_id and self.monitor_interval_id.is_alive():
            self.monitor_interval_id.join(timeout=1.0)
        
        if self.sync_interval_id and self.sync_interval_id.is_alive():
            self.sync_interval_id.join(timeout=1.0)
        
        # Encerra executor
        self.executor.shutdown(wait=False)
        
        self.log("Sistema Autônomo Parado.", LogLevel.WARNING, "CORE")
        print("⏹️ Sistema Autônomo: DESATIVADO")
    
    # --- LOOPS PRINCIPAIS ---
    
    def _run_execution_loop(self):
        """Loop de execução (executado em thread separada)"""
        last_execution = time.time()
        
        while self.active:
            try:
                # Calcula tempo desde última execução
                current_time = time.time()
                elapsed = current_time - last_execution
                
                # Executa se passou o intervalo
                if elapsed * 1000 >= self.config.execution_interval:
                    # Executa em thread separada para não bloquear
                    self.executor.submit(self._execute_cycle)
                    last_execution = current_time
                
                # Sleep curto para não consumir muita CPU
                time.sleep(0.01)
                
            except Exception as e:
                self.log(f"Erro no loop de execução: {str(e)}", LogLevel.ERROR, "EXECUTION_LOOP")
                time.sleep(1)  # Espera antes de tentar novamente
    
    def _run_monitoring_loop(self):
        """Loop de monitoramento (executado em thread separada)"""
        last_monitor = time.time()
        
        while self.active:
            try:
                current_time = time.time()
                elapsed = current_time - last_monitor
                
                if elapsed * 1000 >= self.config.monitoring_interval:
                    self._monitor_cycle()
                    last_monitor = current_time
                
                time.sleep(0.1)
                
            except Exception as e:
                self.log(f"Erro no loop de monitoramento: {str(e)}", LogLevel.ERROR, "MONITOR_LOOP")
                time.sleep(5)
    
    def _run_sync_loop(self):
        """Loop de sincronização (executado em thread separada)"""
        last_sync = time.time()
        
        while self.active:
            try:
                current_time = time.time()
                elapsed = current_time - last_sync
                
                if elapsed * 1000 >= self.config.sync_interval:
                    self._sync_cycle()
                    last_sync = current_time
                
                time.sleep(0.5)
                
            except Exception as e:
                self.log(f"Erro no loop de sincronização: {str(e)}", LogLevel.ERROR, "SYNC_LOOP")
                time.sleep(10)
    
    async def _execute_cycle(self):
        """Ciclo de execução"""
        if not self.active:
            return
        
        try:
            self.stats['total_executions'] += 1
            start_time = time.time()
            
            # 1. Analisa condições de mercado via Quantum Core
            # Dados de entrada simulados
            inputs = [random.random() for _ in range(4)]
            decision = await executive_core.predict(inputs)
            
            # 2. Verifica influência da AGI
            if self.config.enable_agi_integration:
                self._adjust_parameters_based_on_agi()
            
            # 3. Lógica de execução
            if decision['confidence'] > 0.8:
                if decision['prediction'] > 0.6:
                    action = ActionType.BUY_SIGNAL
                elif decision['prediction'] < 0.4:
                    action = ActionType.SELL_SIGNAL
                else:
                    action = ActionType.HOLD
                
                if action != ActionType.HOLD:
                    confidence_percent = decision['confidence'] * 100
                    self.log(
                        f"Executando {action.value} com confiança {confidence_percent:.1f}%",
                        LogLevel.INFO,
                        "EXECUTION",
                        {
                            'prediction': decision['prediction'],
                            'confidence': decision['confidence'],
                            'inputs': inputs
                        }
                    )
                    
                    # Feedback para memória
                    memory_system.add_experience({
                        'type': 'AUTO_EXEC',
                        'action': action.value,
                        'result': 'PENDING',
                        'confidence': decision['confidence'],
                        'timestamp': datetime.now()
                    }, priority=2)
                    
                    # Simula execução
                    self._simulate_execution(action, decision)
            
            # Calcula tempo de decisão
            decision_time = time.time() - start_time
            
            # Atualiza estatística de tempo médio
            alpha = 0.1  # Fator de suavização
            self.stats['average_decision_time'] = (
                (1 - alpha) * self.stats['average_decision_time'] + 
                alpha * decision_time
            )
            
            self.stats['successful_executions'] += 1
            
        except Exception as e:
            self.stats['failed_executions'] += 1
            self.stats['last_error'] = str(e)
            self.log(f"Erro na execução: {str(e)}", LogLevel.ERROR, "EXECUTION", {'error': str(e)})
    
    def _simulate_execution(self, action: ActionType, decision: Dict[str, Any]):
        """Simula execução de uma ação"""
        # Simulação de resultado
        success_probability = decision['confidence'] * 0.9
        
        if random.random() < success_probability:
            result = "SUCCESS"
            reward = random.uniform(0.5, 2.0)
        else:
            result = "FAILURE"
            reward = -random.uniform(0.5, 1.5)
        
        # Atualiza memória com resultado
        memory_system.add_experience({
            'type': 'EXECUTION_RESULT',
            'action': action.value,
            'result': result,
            'reward': reward,
            'confidence': decision['confidence'],
            'timestamp': datetime.now()
        }, priority=3 if result == "SUCCESS" else 1)
        
        # Log do resultado
        self.log(
            f"Execução {action.value}: {result} (recompensa: {reward:+.2f})",
            LogLevel.INFO if result == "SUCCESS" else LogLevel.WARNING,
            "EXECUTION_RESULT"
        )
    
    def _monitor_cycle(self):
        """Ciclo de monitoramento"""
        if not self.active:
            return
        
        # Simula métricas
        self.health.cpu_load = random.uniform(20, 50)
        self.health.memory_usage = random.uniform(30, 70)
        self.health.network_latency = random.uniform(10, 60)
        
        # Atualiza tempo de atividade
        self.health.uptime = (datetime.now() - self.start_time).total_seconds()
        
        # Detecta anomalias
        if self.health.cpu_load > 80:
            self.log(
                "Sobrecarga de CPU detectada. Otimizando threads.",
                LogLevel.WARNING,
                "MONITOR",
                {'cpu_load': self.health.cpu_load}
            )
            self.health.integrity_score = max(0, self.health.integrity_score - 5)
        elif self.health.memory_usage > 85:
            self.log(
                "Uso alto de memória detectado. Limpando cache.",
                LogLevel.WARNING,
                "MONITOR",
                {'memory_usage': self.health.memory_usage}
            )
            self.health.integrity_score = max(0, self.health.integrity_score - 3)
        else:
            # Recuperação gradual
            self.health.integrity_score = min(100, self.health.integrity_score + 1)
        
        # Atualiza threads ativas
        self.health.active_threads = threading.active_count()
        
        # Log periódico de saúde
        if random.random() > 0.7:  # 30% de chance de log
            health_summary = self.health.get_health_summary()
            self.log(
                f"Checkup de saúde: {health_summary['status']}",
                LogLevel.DEBUG,
                "HEALTH_CHECK",
                health_summary
            )
    
    def _sync_cycle(self):
        """Ciclo de sincronização"""
        if not self.active:
            return
        
        self.log("Sincronizando estado global...", LogLevel.INFO, "SYNC")
        self.health.last_sync = datetime.now()
        
        # Simula lógica de sincronização
        sync_success = random.random() > 0.1  # 90% de sucesso
        
        if sync_success:
            if random.random() > 0.9:  # 10% de chance de divergência
                self.log(
                    "Pequena divergência de dados corrigida.",
                    LogLevel.WARNING,
                    "SYNC",
                    {'correction_type': 'data_divergence'}
                )
            else:
                self.log(
                    "Sincronização completa sem problemas.",
                    LogLevel.INFO,
                    "SYNC",
                    {'sync_time': datetime.now().strftime('%H:%M:%S')}
                )
        else:
            self.log(
                "Falha na sincronização. Tentando novamente...",
                LogLevel.ERROR,
                "SYNC",
                {'retry_count': 1}
            )
    
    # --- INTEGRAÇÃO AGI ---
    
    def _adjust_parameters_based_on_agi(self):
        """Ajusta parâmetros baseados no estado da AGI"""
        if not self.config.enable_agi_integration:
            return
        
        agi_vector = sentient_core.get_vector()
        previous_mode = self.config.active_mode
        
        # Alta Ansiedade -> Modo Seguro
        if agi_vector.stability < 30 and self.config.active_mode != SystemMode.SAFE:
            self.config.active_mode = SystemMode.SAFE
            self.config.execution_interval = 2000  # Desacelera
            self.config.adjustment_threshold = 0.01  # Threshold mais conservador
            self.log(
                "AGI Instável: Modo de Segurança Ativado",
                LogLevel.CRITICAL,
                "AGI_BRIDGE",
                {
                    'stability': agi_vector.stability,
                    'previous_mode': previous_mode.value,
                    'new_mode': self.config.active_mode.value
                }
            )
            self.stats['mode_changes'] += 1
        
        # Alta Confiança + Foco -> Modo Quântico/Agressivo
        elif (agi_vector.confidence > 80 and agi_vector.focus > 80 and 
              self.config.active_mode != SystemMode.QUANTUM):
            self.config.active_mode = SystemMode.QUANTUM
            self.config.execution_interval = 500  # Acelera
            self.config.adjustment_threshold = 0.03  # Threshold mais agressivo
            self.log(
                "AGI Focada: Modo Quântico Ativado",
                LogLevel.INFO,
                "AGI_BRIDGE",
                {
                    'confidence': agi_vector.confidence,
                    'focus': agi_vector.focus,
                    'previous_mode': previous_mode.value,
                    'new_mode': self.config.active_mode.value
                }
            )
            self.stats['mode_changes'] += 1
        
        # Volta para modo balanceado se estável
        elif (self.config.active_mode != SystemMode.BALANCED and 
              agi_vector.stability > 50 and agi_vector.confidence > 60):
            self.config.active_mode = SystemMode.BALANCED
            self.config.execution_interval = 1000
            self.config.adjustment_threshold = 0.02
            self.log(
                "AGI Estável: Retornando ao Modo Balanceado",
                LogLevel.INFO,
                "AGI_BRIDGE",
                {
                    'stability': agi_vector.stability,
                    'confidence': agi_vector.confidence,
                    'previous_mode': previous_mode.value,
                    'new_mode': self.config.active_mode.value
                }
            )
            self.stats['mode_changes'] += 1
    
    # --- MÉTODOS PÚBLICOS ---
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        recent_logs = [log.get_log_info() for log in self.logs[:10]]
        
        return {
            'active': self.active,
            'uptime': self.health.uptime,
            'config': {
                'execution_interval': self.config.execution_interval,
                'active_mode': self.config.active_mode.value,
                'adjustment_threshold': self.config.adjustment_threshold,
                'enable_agi_integration': self.config.enable_agi_integration
            },
            'health': self.health.get_health_summary(),
            'statistics': {
                'total_executions': self.stats['total_executions'],
                'success_rate': (
                    self.stats['successful_executions'] / self.stats['total_executions'] 
                    if self.stats['total_executions'] > 0 else 0
                ),
                'mode_changes': self.stats['mode_changes'],
                'average_decision_time_ms': self.stats['average_decision_time'] * 1000,
                'active_threads': self.health.active_threads
            },
            'recent_logs': recent_logs,
            'memory_stats': {
                'short_term': len(memory_system.short_term.memories),
                'long_term': len(memory_system.long_term.archives),
                'working': len(memory_system.working_memory.active_items)
            }
        }
    
    def get_recent_logs(self, limit: int = 20, level: Optional[LogLevel] = None) -> List[Dict[str, Any]]:
        """Retorna logs recentes"""
        filtered_logs = self.logs
        
        if level:
            filtered_logs = [log for log in filtered_logs if log.level == level]
        
        return [log.get_log_info() for log in filtered_logs[:limit]]
    
    def get_system_report(self) -> Dict[str, Any]:
        """Retorna relatório completo do sistema"""
        status = self.get_status()
        
        # Adiciona informações do núcleo senciente
        agi_state = sentient_core.get_state()
        agi_vector = sentient_core.get_vector()
        
        report = {
            **status,
            'agi_integration': {
                'state': agi_state,
                'confidence': agi_vector.confidence,
                'stability': agi_vector.stability,
                'focus': agi_vector.focus,
                'thoughts_count': len(sentient_core.thoughts)
            },
            'neural_core': {
                'initialized': executive_core.initialized,
                'prediction_count': len(executive_core.prediction_history),
                'last_prediction': (
                    executive_core.prediction_history[-1] if executive_core.prediction_history else None
                )
            },
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Gera recomendações baseadas no estado do sistema"""
        recommendations = []
        
        # Verifica integridade
        if self.health.integrity_score < 70:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'OPTIMIZE_RESOURCES',
                'description': 'Integridade do sistema abaixo de 70%. Considere otimizar recursos.',
                'suggested_change': 'Reduzir carga de processamento ou aumentar limites'
            })
        
        # Verifica uso de CPU
        if self.health.cpu_load > 75:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'ADJUST_EXECUTION_INTERVAL',
                'description': f'Uso de CPU alto ({self.health.cpu_load:.1f}%).',
                'suggested_change': f'Aumentar execution_interval para {self.config.execution_interval + 500}ms'
            })
        
        # Verifica modo atual
        if self.config.active_mode == SystemMode.SAFE and self.health.integrity_score > 80:
            recommendations.append({
                'priority': 'LOW',
                'action': 'SWITCH_TO_BALANCED',
                'description': 'Sistema estável em modo seguro. Pode retornar ao modo balanceado.',
                'suggested_change': 'Alterar active_mode para BALANCED'
            })
        
        return recommendations

# --- INSTÂNCIA GLOBAL ---

autonomous_system = AutonomousSystemService()

# --- FUNÇÃO DE DEMONSTRAÇÃO ---

async def demonstrate_autonomous_system():
    """Demonstra o sistema autônomo"""
    
    print("=" * 60)
    print("SISTEMA AUTÔNOMO INTEGRADO - DEMONSTRAÇÃO")
    print("=" * 60)
    
    # Status inicial
    print("\n📊 STATUS INICIAL:")
    initial_status = autonomous_system.get_status()
    print(f"  Ativo: {'✅' if initial_status['active'] else '❌'}")
    print(f"  Modo: {initial_status['config']['active_mode']}")
    print(f"  Integridade: {initial_status['health']['integrity']}")
    
    # Inicia sistema
    print("\n🚀 INICIANDO SISTEMA...")
    await autonomous_system.start()
    
    # Aguarda alguns ciclos
    print("\n⏳ EXECUTANDO CICLOS (aguarde 10 segundos)...")
    await asyncio.sleep(10)
    
    # Obtém relatório
    print("\n📈 RELATÓRIO DO SISTEMA:")
    report = autonomous_system.get_system_report()
    
    print(f"\n  ESTADO GERAL:")
    print(f"    Ativo: {'✅' if report['active'] else '❌'}")
    print(f"    Tempo de atividade: {report['uptime']:.0f}s")
    print(f"    Modo atual: {report['config']['active_mode']}")
    
    print(f"\n  SAÚDE DO SISTEMA:")
    for key, value in report['health'].items():
        print(f"    {key}: {value}")
    
    print(f"\n  ESTATÍSTICAS:")
    for key, value in report['statistics'].items():
        if key == 'success_rate':
            print(f"    {key}: {value:.1%}")
        elif key == 'average_decision_time_ms':
            print(f"    {key}: {value:.1f}ms")
        else:
            print(f"    {key}: {value}")
    
    print(f"\n  INTEGRAÇÃO AGI:")
    agi_info = report['agi_integration']
    print(f"    Estado: {agi_info['state']}")
    print(f"    Confiança: {agi_info['confidence']:.1f}")
    print(f"    Estabilidade: {agi_info['stability']:.1f}")
    print(f"    Foco: {agi_info['focus']:.1f}")
    
    print(f"\n  RECOMENDAÇÕES:")
    recommendations = report['recommendations']
    if recommendations:
        for rec in recommendations:
            print(f"    [{rec['priority']}] {rec['action']}: {rec['description']}")
    else:
        print("    ✅ Nenhuma recomendação no momento")
    
    # Logs recentes
    print(f"\n  LOGS RECENTES:")
    recent_logs = autonomous_system.get_recent_logs(limit=5)
    for log in recent_logs:
        print(f"    [{log['time'][11:]}][{log['level']}] {log['message'][:50]}...")
    
    # Para o sistema
    print("\n🛑 PARANDO SISTEMA...")
    autonomous_system.stop()
    
    # Status final
    print("\n📋 STATUS FINAL:")
    final_status = autonomous_system.get_status()
    print(f"  Execuções totais: {final_status['statistics']['total_executions']}")
    print(f"  Taxa de sucesso: {final_status['statistics']['success_rate']:.1%}")
    print(f"  Mudanças de modo: {final_status['statistics']['mode_changes']}")
    
    print("\n" + "=" * 60)
    print("✅ Demonstração do Sistema Autônomo completa!")
    print("=" * 60)

if __name__ == "__main__":
    # Executa demonstração
    asyncio.run(demonstrate_autonomous_system())