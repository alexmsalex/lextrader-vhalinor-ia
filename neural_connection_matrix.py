import importlib.util
import os
import sys
import logging
from typing import Any, Optional, Dict, List, Callable, Tuple
from pathlib import Path
import hashlib
import time
from datetime import datetime
import inspect
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
import gc
import psutil
from dataclasses import dataclass, field
from enum import Enum
import json

# Configuração de logging avançada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('module_loader_advanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AdvancedModuleLoader')

class ModuleStatus(Enum):
    LOADED = "loaded"
    CACHED = "cached"
    FALLBACK = "fallback"
    ERROR = "error"
    PENDING = "pending"

@dataclass
class ModuleMetrics:
    load_time: float = 0.0
    memory_usage: int = 0
    dependencies: List[str] = field(default_factory=list)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    error_count: int = 0

@dataclass
class LoaderConfig:
    cache_ttl: int = 300
    max_cache_size: int = 100
    enable_hot_reload: bool = True
    hot_reload_interval: int = 5
    enable_prefetch: bool = True
    prefetch_threads: int = 4
    memory_limit_mb: int = 512
    enable_compression: bool = False

class OptimizedModuleCache:
    """Sistema de cache otimizado com compressão e monitoramento de memória."""
    
    def __init__(self, max_size: int = 100):
        self._cache: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict] = {}
        self._access_count: Dict[str, int] = {}
        self._max_size = max_size
        self._hits = 0
        self._misses = 0
        
    def get(self, key: str) -> Optional[Any]:
        """Obtém item do cache com política LRU."""
        if key in self._cache:
            self._access_count[key] = self._access_count.get(key, 0) + 1
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        return None
    
    def set(self, key: str, value: Any, metadata: Dict = None):
        """Armazena item no cache com controle de tamanho."""
        if len(self._cache) >= self._max_size:
            self._evict_least_used()
        
        self._cache[key] = value
        self._metadata[key] = metadata or {}
        self._access_count[key] = 0
        
    def _evict_least_used(self):
        """Remove itens menos usados do cache."""
        if not self._access_count:
            # Remove primeiro item se não houver contagem de acesso
            key_to_remove = next(iter(self._cache.keys()))
        else:
            key_to_remove = min(self._access_count.items(), key=lambda x: x[1])[0]
        
        self.remove(key_to_remove)
    
    def remove(self, key: str):
        """Remove item do cache."""
        if key in self._cache:
            # Limpar referências para ajudar garbage collector
            module = self._cache.pop(key)
            if hasattr(module, '__dict__'):
                module.__dict__.clear()
            self._metadata.pop(key, None)
            self._access_count.pop(key, None)
            gc.collect()
    
    def clear(self):
        """Limpa todo o cache."""
        self._cache.clear()
        self._metadata.clear()
        self._access_count.clear()
        gc.collect()
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        total_accesses = self._hits + self._misses
        hit_rate = self._hits / total_accesses if total_accesses > 0 else 0
        
        return {
            'size': len(self._cache),
            'max_size': self._max_size,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': f"{hit_rate:.2%}",
            'memory_usage_mb': self._estimate_memory_usage() / 1024 / 1024
        }
    
    def _estimate_memory_usage(self) -> int:
        """Estima uso de memória do cache."""
        total_size = 0
        for obj in self._cache.values():
            total_size += sys.getsizeof(obj)
            if hasattr(obj, '__dict__'):
                total_size += sys.getsizeof(obj.__dict__)
        return total_size

class HotReloadMonitor:
    """Monitor para hot-reload de módulos modificados."""
    
    def __init__(self, loader: 'AdvancedModuleLoader', interval: int = 5):
        self.loader = loader
        self.interval = interval
        self._file_timestamps: Dict[str, float] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
    
    def start(self):
        """Inicia monitoramento."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.info("Hot-reload monitor iniciado")
    
    def stop(self):
        """Para monitoramento."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Hot-reload monitor parado")
    
    def _monitor_loop(self):
        """Loop principal de monitoramento."""
        while self._running:
            try:
                self._check_file_changes()
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Erro no hot-reload monitor: {e}")
                time.sleep(self.interval * 2)  # Backoff em caso de erro
    
    def _check_file_changes(self):
        """Verifica mudanças nos arquivos monitorados."""
        current_time = time.time()
        
        for module_path in list(self.loader.loaded_modules.keys()):
            if not os.path.exists(module_path):
                continue
            
            try:
                current_mtime = os.path.getmtime(module_path)
                previous_mtime = self._file_timestamps.get(module_path, 0)
                
                if current_mtime > previous_mtime:
                    logger.info(f"Arquivo modificado detectado: {module_path}")
                    self.loader.reload_module(module_path)
                    self._file_timestamps[module_path] = current_mtime
                    
            except Exception as e:
                logger.error(f"Erro ao verificar {module_path}: {e}")
        
        # Atualizar timestamps para novos arquivos
        for module_path in self.loader.loaded_modules.keys():
            if module_path not in self._file_timestamps and os.path.exists(module_path):
                self._file_timestamps[module_path] = os.path.getmtime(module_path)

class NeuralConnectionMatrixFallback:
    """Implementação otimizada de fallback para NeuralConnectionMatrix."""
    
    def __init__(self, original_path: str = ""):
        self.module_name = "NeuralConnectionMatrix"
        self.original_path = original_path
        self.creation_time = datetime.now()
        self.is_fallback = True
        
        # Estruturas otimizadas
        self.connections: Dict[Tuple[str, str], float] = {}
        self.neurons: Dict[str, Dict] = {}
        self.activation_level = 0.0
        self.throughput_cache = None
        self.cache_dirty = True
    
    def connect_neurons(self, source: str, target: str, weight: float = 1.0):
        """Conecta dois neurônios de forma otimizada."""
        connection_key = (source, target)
        self.connections[connection_key] = weight
        self.cache_dirty = True
        
        # Inicializar neurônios se não existirem
        if source not in self.neurons:
            self.neurons[source] = {'type': 'standard', 'activation': 0.0}
        if target not in self.neurons:
            self.neurons[target] = {'type': 'standard', 'activation': 0.0}
        
        logger.debug(f"Conexão neural: {source} -> {target} (peso: {weight})")
    
    def activate(self, level: float):
        """Ativa a matriz neural."""
        self.activation_level = max(0.0, min(1.0, level))
        self.cache_dirty = True
        logger.debug(f"Matriz neural ativada: {self.activation_level:.2f}")
    
    def get_connections(self) -> List[Dict]:
        """Retorna conexões em formato otimizado."""
        return [
            {
                'source': source,
                'target': target,
                'weight': weight,
                'throughput': weight * self.activation_level
            }
            for (source, target), weight in self.connections.items()
        ]
    
    def calculate_throughput(self) -> float:
        """Calcula throughput com cache."""
        if not self.cache_dirty and self.throughput_cache is not None:
            return self.throughput_cache
        
        total_weight = sum(self.connections.values())
        self.throughput_cache = total_weight * self.activation_level
        self.cache_dirty = False
        
        return self.throughput_cache
    
    def propagate_signal(self, source: str, signal_strength: float = 1.0) -> Dict[str, float]:
        """Propaga sinal através da rede neural."""
        activations = {source: signal_strength}
        
        # Algoritmo de propagação otimizado
        queue = [(source, signal_strength)]
        visited = set([source])
        
        while queue:
            current_neuron, current_strength = queue.pop(0)
            
            # Encontrar conexões de saída
            for (src, tgt), weight in self.connections.items():
                if src == current_neuron and tgt not in visited:
                    propagated_strength = current_strength * weight * self.activation_level
                    activations[tgt] = activations.get(tgt, 0) + propagated_strength
                    visited.add(tgt)
                    queue.append((tgt, propagated_strength))
        
        return activations
    
    def get_network_info(self) -> Dict[str, Any]:
        """Retorna informações completas da rede."""
        return {
            'total_neurons': len(self.neurons),
            'total_connections': len(self.connections),
            'activation_level': self.activation_level,
            'throughput': self.calculate_throughput(),
            'density': len(self.connections) / max(1, len(self.neurons) ** 2)
        }
    
    def render_html(self) -> str:
        """Renderização HTML otimizada."""
        network_info = self.get_network_info()
        connections_html = "".join(
            f"<tr><td>{src}</td><td>→</td><td>{tgt}</td><td>{weight:.2f}</td><td>{weight * self.activation_level:.2f}</td></tr>"
            for (src, tgt), weight in list(self.connections.items())[:10]  # Limitar para performance
        )
        
        return f"""
        <div class='neural-matrix-card'>
            <div class='card-header'>
                <h3>🧠 NeuralConnectionMatrix (Fallback Mode)</h3>
                <div class='status-badges'>
                    <span class='badge badge-warning'>Fallback</span>
                    <span class='badge badge-info'>Neurons: {network_info['total_neurons']}</span>
                    <span class='badge badge-success'>Connections: {network_info['total_connections']}</span>
                </div>
            </div>
            <div class='card-body'>
                <div class='metrics-grid'>
                    <div class='metric'>
                        <label>Ativação</label>
                        <div class='value'>{self.activation_level:.2f}</div>
                    </div>
                    <div class='metric'>
                        <label>Throughput</label>
                        <div class='value'>{network_info['throughput']:.2f}</div>
                    </div>
                    <div class='metric'>
                        <label>Densidade</label>
                        <div class='value'>{network_info['density']:.3f}</div>
                    </div>
                </div>
                
                <div class='connections-table'>
                    <h5>Top Conexões</h5>
                    <table>
                        <thead>
                            <tr><th>Origem</th><th></th><th>Destino</th><th>Peso</th><th>Throughput</th></tr>
                        </thead>
                        <tbody>
                            {connections_html if connections_html else "<tr><td colspan='5'>Sem conexões</td></tr>"}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """

class AdvancedModuleLoader:
    """
    Carregador avançado de módulos com performance otimizada.
    """
    
    def __init__(self, config: LoaderConfig = None):
        self.config = config or LoaderConfig()
        self.cache = OptimizedModuleCache(self.config.max_cache_size)
        self.loaded_modules: Dict[str, Any] = {}
        self.fallback_modules: Dict[str, Any] = {}
        self.metrics: Dict[str, ModuleMetrics] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        
        # Sistemas auxiliares
        self.hot_reload_monitor = HotReloadMonitor(self, self.config.hot_reload_interval)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.config.prefetch_threads)
        
        # Estatísticas avançadas
        self.stats = {
            'total_loads': 0,
            'cache_hits': 0,
            'fallback_used': 0,
            'failed_loads': 0,
            'hot_reloads': 0,
            'memory_peak_mb': 0
        }
        
        # Iniciar sistemas
        if self.config.enable_hot_reload:
            self.hot_reload_monitor.start()
    
    def load_module(self, 
                   module_path: str, 
                   class_name: str = None,
                   enable_cache: bool = True,
                   enable_fallback: bool = True,
                   fallback_class: Callable = None,
                   dependencies: List[str] = None) -> Any:
        """
        Carrega módulo com múltiplas otimizações.
        """
        self.stats['total_loads'] += 1
        start_time = time.time()
        module_key = self._generate_module_key(module_path, class_name)
        
        # Verificar dependências primeiro
        if dependencies:
            missing_deps = self._check_dependencies(dependencies)
            if missing_deps:
                logger.warning(f"Dependências faltando para {module_path}: {missing_deps}")
        
        # Tentar cache (mais rápido)
        if enable_cache:
            cached_module = self.cache.get(module_key)
            if cached_module is not None:
                self.stats['cache_hits'] += 1
                self._update_metrics(module_key, time.time() - start_time)
                return cached_module
        
        # Carregamento principal
        module = self._load_module_optimized(module_path, class_name, dependencies)
        
        if module is not None:
            if enable_cache:
                self.cache.set(module_key, module, {
                    'load_time': time.time(),
                    'dependencies': dependencies or []
                })
            
            self.loaded_modules[module_key] = module
            self._update_metrics(module_key, time.time() - start_time, dependencies)
            logger.info(f"✅ Módulo carregado: {module_path}")
            return module
        
        # Fallback
        if enable_fallback:
            self.stats['fallback_used'] += 1
            fallback = self._create_optimized_fallback(module_path, class_name, fallback_class)
            self.fallback_modules[module_key] = fallback
            self._update_metrics(module_key, time.time() - start_time)
            logger.warning(f"🔄 Usando fallback para: {module_path}")
            return fallback
        
        self.stats['failed_loads'] += 1
        logger.error(f"❌ Falha ao carregar: {module_path}")
        return None
    
    def _load_module_optimized(self, module_path: str, class_name: str = None, 
                             dependencies: List[str] = None) -> Any:
        """Carregamento otimizado com tratamento de erro robusto."""
        try:
            if not os.path.exists(module_path):
                logger.error(f"Arquivo não encontrado: {module_path}")
                return None
            
            # Carregar dependências primeiro
            if dependencies:
                for dep in dependencies:
                    self.load_module(dep, enable_cache=True, enable_fallback=False)
            
            # Carregar módulo principal
            module_name = f"dynamic_{hashlib.md5(module_path.encode()).hexdigest()[:16]}"
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            
            if spec is None or spec.loader is None:
                logger.error(f"Spec inválido para: {module_path}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            
            # Adicionar ao sys.modules antes de executar
            sys.modules[module_name] = module
            
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                logger.error(f"Erro na execução do módulo {module_path}: {e}")
                # Limpar referência em caso de erro
                sys.modules.pop(module_name, None)
                return None
            
            # Retornar classe específica ou módulo completo
            if class_name:
                if hasattr(module, class_name):
                    cls = getattr(module, class_name)
                    instance = cls()
                    
                    # Adicionar metadados úteis
                    if hasattr(instance, '__dict__'):
                        instance.__dict__['_module_metadata'] = {
                            'loaded_at': datetime.now(),
                            'source_file': module_path,
                            'class_name': class_name
                        }
                    
                    return instance
                else:
                    logger.error(f"Classe {class_name} não encontrada em {module_path}")
                    return None
            
            return module
            
        except Exception as e:
            logger.error(f"Erro crítico ao carregar {module_path}: {e}")
            return None
    
    def _create_optimized_fallback(self, module_path: str, class_name: str = None,
                                 fallback_class: Callable = None) -> Any:
        """Cria fallback otimizado."""
        if fallback_class:
            return fallback_class()
        
        # Fallbacks específicos otimizados
        if class_name == "NeuralConnectionMatrix":
            return NeuralConnectionMatrixFallback(module_path)
        
        # Fallback genérico otimizado
        return NeuralConnectionMatrixFallback(module_path)
    
    def _generate_module_key(self, module_path: str, class_name: str = None) -> str:
        """Gera chave única para o módulo."""
        base_key = hashlib.md5(module_path.encode()).hexdigest()[:16]
        if class_name:
            base_key += f"_{hashlib.md5(class_name.encode()).hexdigest()[:8]}"
        return base_key
    
    def _check_dependencies(self, dependencies: List[str]) -> List[str]:
        """Verifica dependências faltando."""
        missing = []
        for dep in dependencies:
            if not self._is_dependency_available(dep):
                missing.append(dep)
        return missing
    
    def _is_dependency_available(self, dependency: str) -> bool:
        """Verifica se dependência está disponível."""
        try:
            importlib.import_module(dependency)
            return True
        except ImportError:
            return False
    
    def _update_metrics(self, module_key: str, load_time: float, dependencies: List[str] = None):
        """Atualiza métricas do módulo."""
        if module_key not in self.metrics:
            self.metrics[module_key] = ModuleMetrics()
        
        self.metrics[module_key].load_time = load_time
        self.metrics[module_key].last_accessed = datetime.now()
        self.metrics[module_key].access_count += 1
        self.metrics[module_key].dependencies = dependencies or []
        
        # Atualizar pico de memória
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024
        self.stats['memory_peak_mb'] = max(self.stats['memory_peak_mb'], current_memory)
    
    async def load_module_async(self, module_path: str, class_name: str = None, **kwargs) -> Any:
        """Carrega módulo de forma assíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.thread_pool, 
            lambda: self.load_module(module_path, class_name, **kwargs)
        )
    
    def reload_module(self, module_path: str, class_name: str = None) -> Any:
        """Recarrega um módulo específico."""
        module_key = self._generate_module_key(module_path, class_name)
        
        # Limpar cache e referências
        self.cache.remove(module_key)
        self.loaded_modules.pop(module_key, None)
        self.fallback_modules.pop(module_key, None)
        
        # Forçar garbage collection
        gc.collect()
        
        self.stats['hot_reloads'] += 1
        logger.info(f"♻️ Recarregando módulo: {module_path}")
        
        return self.load_module(module_path, class_name)
    
    def prefetch_modules(self, module_paths: List[str]):
        """Pré-carrega módulos em background."""
        if not self.config.enable_prefetch:
            return
        
        for module_path in module_paths:
            self.thread_pool.submit(self.load_module, module_path, enable_cache=True)
    
    def get_detailed_stats(self) -> Dict[str, Any]:
        """Estatísticas detalhadas do carregador."""
        stats = self.stats.copy()
        stats.update(self.cache.get_stats())
        
        # Métricas de performance
        total_load_time = sum(metric.load_time for metric in self.metrics.values())
        avg_load_time = total_load_time / len(self.metrics) if self.metrics else 0
        
        stats.update({
            'total_modules_loaded': len(self.loaded_modules),
            'total_fallbacks': len(self.fallback_modules),
            'avg_load_time_ms': avg_load_time * 1000,
            'active_threads': self.thread_pool._max_workers,
            'hot_reload_enabled': self.config.enable_hot_reload
        })
        
        return stats
    
    def cleanup(self):
        """Limpeza completa do carregador."""
        self.hot_reload_monitor.stop()
        self.thread_pool.shutdown(wait=False)
        self.cache.clear()
        self.loaded_modules.clear()
        self.fallback_modules.clear()
        gc.collect()
        logger.info("✅ Carregador limpo e recursos liberados")

# Instância global otimizada
module_loader = AdvancedModuleLoader(LoaderConfig(
    cache_ttl=300,
    max_cache_size=50,
    enable_hot_reload=True,
    hot_reload_interval=3,
    enable_prefetch=True,
    prefetch_threads=2,
    memory_limit_mb=256
))

# Caminho específico para NeuralConnectionMatrix
NEURAL_MATRIX_PATH = r"C:\Users\ALEXMS-PC\Desktop\LEXTRADER-IAG\.venv\IAG\rede neural\neural_connection_matrix.py"

def load_neural_connection_matrix() -> Any:
    """
    Função otimizada para carregar NeuralConnectionMatrix.
    """
    return module_loader.load_module(
        module_path=NEURAL_MATRIX_PATH,
        class_name="NeuralConnectionMatrix",
        enable_cache=True,
        enable_fallback=True,
        fallback_class=NeuralConnectionMatrixFallback,
        dependencies=['numpy', 'torch']  # Dependências comuns em redes neurais
    )

async def load_neural_connection_matrix_async() -> Any:
    """Versão assíncrona para carregamento não-bloqueante."""
    return await module_loader.load_module_async(
        module_path=NEURAL_MATRIX_PATH,
        class_name="NeuralConnectionMatrix"
    )

# Interface de compatibilidade
NeuralConnectionMatrix = load_neural_connection_matrix

# Funções utilitárias otimizadas
def reload_neural_matrix() -> Any:
    """Recarrega especificamente a matriz neural."""
    return module_loader.reload_module(NEURAL_MATRIX_PATH, "NeuralConnectionMatrix")

def get_detailed_loader_stats() -> Dict[str, Any]:
    """Estatísticas detalhadas do carregador."""
    return module_loader.get_detailed_stats()

def prefetch_common_modules():
    """Pré-carrega módulos comuns."""
    common_modules = [
        NEURAL_MATRIX_PATH,
        # Adicionar outros módulos comuns aqui
    ]
    module_loader.prefetch_modules(common_modules)

# Exemplo de uso avançado
async def demo_advanced_usage():
    """Demonstração do uso avançado do carregador."""
    
    # Carregar módulo de forma assíncrona
    neural_matrix = await load_neural_connection_matrix_async()
    
    # Usar funcionalidades
    if hasattr(neural_matrix, 'connect_neurons'):
        # Criar rede neural de exemplo
        neural_matrix.connect_neurons("input_layer", "hidden_1", 0.8)
        neural_matrix.connect_neurons("hidden_1", "hidden_2", 1.2)
        neural_matrix.connect_neurons("hidden_2", "output_layer", 0.9)
        neural_matrix.activate(0.75)
        
        # Propagação de sinal
        activations = neural_matrix.propagate_signal("input_layer", 1.0)
        print("Ativações:", activations)
    
    # Estatísticas
    stats = get_detailed_loader_stats()
    print("\n=== Estatísticas Avançadas ===")
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    # Pré-carregar módulos comuns
    prefetch_common_modules()
    
    # Executar demonstração
    asyncio.run(demo_advanced_usage())
    
    # Manter sistema rodando para hot-reload
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        module_loader.cleanup()
        print("✅ Sistema finalizado corretamente")