"""
QUANTUM PERFORMANCE OPTIMIZATOR
================================
Otimizador Centralizado para Inteligência Quântica Geral (AGI)
Sistema avançado de otimização com caching inteligente, pool de memória,
monitoramento em tempo real e processamento paralelo assíncrono.
"""

import asyncio
import functools
import time
import numpy as np
from typing import Dict, List, Any, Optional, Callable, Tuple, Union, Generic, TypeVar
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import hashlib
import json
import pickle
from enum import Enum
from contextlib import contextmanager
from abc import ABC, abstractmethod
import warnings
from pathlib import Path
import gc

# ============================================================================
# TIPOS E CONSTANTES
# ============================================================================

T = TypeVar('T')
R = TypeVar('R')


class CacheStrategy(Enum):
    """Estratégias de cache disponíveis."""
    LRU = "lru"
    LFU = "lfu"
    ARC = "arc"
    FIFO = "fifo"
    TTL_ONLY = "ttl_only"


class MemoryPriority(Enum):
    """Prioridades para alocação de memória."""
    HIGH = 0
    MEDIUM = 1
    LOW = 2
    BACKGROUND = 3


class OperationType(Enum):
    """Tipos de operações quânticas."""
    GATE_APPLICATION = "gate_application"
    STATE_PREPARATION = "state_preparation"
    MEASUREMENT = "measurement"
    ENTANGLEMENT = "entanglement"
    ERROR_CORRECTION = "error_correction"
    OPTIMIZATION = "optimization"

# ============================================================================
# CONFIGURAÇÃO DE LOGGING AVANÇADA
# ============================================================================


class QuantumLogger:
    """Logger avançado para sistema quântico."""
    
    @staticmethod
    def setup_logging(
        level: int=logging.INFO,
        log_file: Optional[str]=None,
        max_bytes: int=10 * 1024 * 1024,  # 10MB
        backup_count: int=5
    ) -> logging.Logger:
        """Configura logging avançado."""
        logger = logging.getLogger("quantum_optimizer")
        logger.setLevel(level)
        logger.propagate = False
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (se especificado)
        if log_file:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger


logger = QuantumLogger.setup_logging()

# ============================================================================
# CACHE INTELIGENTE COM MÚLTIPLAS ESTRATÉGIAS
# ============================================================================


@dataclass
class CacheEntry:
    """Entrada no cache com metadados avançados."""
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: Optional[float] = None
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    size_bytes: int = 0
    tags: Dict[str, str] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Verifica se cache expirou."""
        if self.ttl is None:
            return False
        return (datetime.now() - self.timestamp).total_seconds() > self.ttl
    
    def age(self) -> float:
        """Idade da entrada em segundos."""
        return (datetime.now() - self.timestamp).total_seconds()
    
    def cost(self) -> float:
        """Custo da entrada (para algoritmos de evicção)."""
        return (self.age() / max(1, self.access_count)) * (self.size_bytes / 1024)


class AdaptiveCache:
    """
    Cache adaptativo com suporte a múltiplas estratégias e auto-otimização.
    """
    
    def __init__(
        self,
        max_size_bytes: int=100 * 1024 * 1024,  # 100MB
        default_ttl: Optional[float]=300.0,
        strategy: CacheStrategy=CacheStrategy.ARC,
        enable_compression: bool=True
    ):
        self.max_size_bytes = max_size_bytes
        self.default_ttl = default_ttl
        self.strategy = strategy
        self.enable_compression = enable_compression
        
        # Estruturas de dados baseadas na estratégia
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._frequency: Dict[str, int] = defaultdict(int)
        self._size_bytes = 0
        self._hits = 0
        self._misses = 0
        self._lock = threading.RLock()
        
        # Para ARC
        self._t1 = OrderedDict()  # Recência recente
        self._t2 = OrderedDict()  # Recência frequente
        self._b1 = OrderedDict()  # Fantasmas T1
        self._b2 = OrderedDict()  # Fantasmas T2
        self._p = 0  # Parâmetro adaptativo
        
        logger.info(
            f"🗄️ Cache adaptativo inicializado: "
            f"max={self.max_size_bytes/1024/1024:.1f}MB, "
            f"strategy={strategy.value}"
        )
    
    def _compute_key(self, *args, **kwargs) -> str:
        """Computa chave única para argumentos."""
        try:
            # Tentar usar JSON para dados serializáveis
            data = json.dumps(
                {'args': args, 'kwargs': kwargs},
                default=str,
                sort_keys=True,
                separators=(',', ':')
            ).encode()
        except (TypeError, ValueError):
            # Fallback para pickle
            data = pickle.dumps((args, kwargs))
        
        return hashlib.blake2b(data, digest_size=16).hexdigest()
    
    def _compress(self, value: Any) -> Any:
        """Compressão opcional de dados."""
        if not self.enable_compression:
            return value
        
        if isinstance(value, np.ndarray):
            # Para arrays NumPy, usar compressão eficiente
            return {
                '__type__': 'numpy_array',
                'data': value.tobytes(),
                'dtype': str(value.dtype),
                'shape': value.shape
            }
        return value
    
    def _decompress(self, value: Any) -> Any:
        """Descompressão de dados."""
        if isinstance(value, dict) and value.get('__type__') == 'numpy_array':
            return np.frombuffer(
                value['data'],
                dtype=np.dtype(value['dtype'])
            ).reshape(value['shape'])
        return value
    
    def _estimate_size(self, value: Any) -> int:
        """Estimativa do tamanho em bytes."""
        if isinstance(value, np.ndarray):
            return value.nbytes
        elif isinstance(value, (list, tuple, dict)):
            return len(pickle.dumps(value))
        else:
            return len(pickle.dumps(value))
    
    def _evict(self) -> None:
        """Executa evicção baseada na estratégia."""
        if self.strategy == CacheStrategy.LRU:
            self._evict_lru()
        elif self.strategy == CacheStrategy.LFU:
            self._evict_lfu()
        elif self.strategy == CacheStrategy.ARC:
            self._evict_arc()
        elif self.strategy == CacheStrategy.FIFO:
            self._evict_fifo()
    
    def _evict_lru(self) -> None:
        """Evicção LRU (Least Recently Used)."""
        if self._cache:
            key, entry = next(iter(self._cache.items()))
            self._size_bytes -= entry.size_bytes
            del self._cache[key]
            logger.debug(f"♻️ Evicção LRU: {key}")
    
    def _evict_lfu(self) -> None:
        """Evicção LFU (Least Frequently Used)."""
        if self._cache:
            # Encontrar chave com menor frequência
            key = min(self._cache.keys(), key=lambda k: self._frequency.get(k, 0))
            entry = self._cache[key]
            self._size_bytes -= entry.size_bytes
            del self._cache[key]
            del self._frequency[key]
            logger.debug(f"♻️ Evicção LFU: {key}")
    
    def _evict_arc(self) -> None:
        """Evicção ARC (Adaptive Replacement Cache)."""
        # Implementação simplificada do ARC
        if self._size_bytes > self.max_size_bytes:
            if self._t1 and (len(self._t1) > self._p or 
                            (self._b2 and len(self._t1) == self._p)):
                key, _ = self._t1.popitem(last=False)
                self._b1[key] = True
            else:
                key, _ = self._t2.popitem(last=False)
                self._b2[key] = True
            logger.debug(f"♻️ Evicção ARC: {key}")
    
    def _evict_fifo(self) -> None:
        """Evicção FIFO (First In First Out)."""
        if self._cache:
            key, entry = next(iter(self._cache.items()))
            self._size_bytes -= entry.size_bytes
            del self._cache[key]
            logger.debug(f"♻️ Evicção FIFO: {key}")
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache."""
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            entry = self._cache[key]
            
            if entry.is_expired():
                self._size_bytes -= entry.size_bytes
                del self._cache[key]
                self._misses += 1
                return None
            
            # Atualizar estatísticas de acesso
            entry.access_count += 1
            entry.last_accessed = datetime.now()
            self._frequency[key] = self._frequency.get(key, 0) + 1
            self._hits += 1
            
            # Mover para final (LRU)
            if self.strategy in [CacheStrategy.LRU, CacheStrategy.ARC]:
                self._cache.move_to_end(key)
            
            return self._decompress(entry.value)
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[float]=None,
        tags: Optional[Dict[str, str]]=None
    ) -> None:
        """Armazena valor no cache."""
        with self._lock:
            # Compressão
            compressed = self._compress(value)
            
            # Estimativa de tamanho
            size = self._estimate_size(compressed)
            
            # Remover se já existir
            if key in self._cache:
                old_entry = self._cache[key]
                self._size_bytes -= old_entry.size_bytes
                del self._cache[key]
            
            # Evicção se necessário
            while self._size_bytes + size > self.max_size_bytes and self._cache:
                self._evict()
            
            # Criar entrada
            entry = CacheEntry(
                value=compressed,
                ttl=ttl or self.default_ttl,
                size_bytes=size,
                tags=tags or {}
            )
            
            self._cache[key] = entry
            self._size_bytes += size
            
            # Estratégia específica
            if self.strategy == CacheStrategy.ARC:
                if key in self._b1:
                    self._p = min(self.max_size_bytes,
                                self._p + max(1, len(self._b2) / len(self._b1)))
                    self._replace(key)
                elif key in self._b2:
                    self._p = max(0,
                                self._p - max(1, len(self._b1) / len(self._b2)))
                    self._replace(key)
    
    def clear_expired(self) -> int:
        """Remove entradas expiradas e retorna contagem."""
        with self._lock:
            expired_keys = [
                k for k, v in self._cache.items()
                if v.is_expired()
            ]
            
            for key in expired_keys:
                entry = self._cache[key]
                self._size_bytes -= entry.size_bytes
                del self._cache[key]
                if key in self._frequency:
                    del self._frequency[key]
            
            if expired_keys:
                logger.info(f"🧹 Removidas {len(expired_keys)} entradas expiradas")
            
            return len(expired_keys)
    
    def clear_by_tag(self, tag_key: str, tag_value: str) -> int:
        """Remove entradas por tag."""
        with self._lock:
            tagged_keys = [
                k for k, v in self._cache.items()
                if v.tags.get(tag_key) == tag_value
            ]
            
            for key in tagged_keys:
                entry = self._cache[key]
                self._size_bytes -= entry.size_bytes
                del self._cache[key]
                if key in self._frequency:
                    del self._frequency[key]
            
            return len(tagged_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas."""
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0
            
            # Distribuição de tamanhos
            sizes = [e.size_bytes for e in self._cache.values()]
            
            return {
                'current_size_bytes': self._size_bytes,
                'max_size_bytes': self.max_size_bytes,
                'entry_count': len(self._cache),
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate_percent': hit_rate,
                'avg_entry_size_bytes': np.mean(sizes) if sizes else 0,
                'strategy': self.strategy.value,
                'memory_usage_percent': (self._size_bytes / self.max_size_bytes * 100)
            }

# ============================================================================
# DECORADOR DE CACHE AVANÇADO
# ============================================================================


def quantum_cache(
    ttl: Optional[float]=300.0,
    max_size_mb: int=100,
    strategy: CacheStrategy=CacheStrategy.LRU,
    tags: Optional[Dict[str, str]]=None,
    cache_instance: Optional[AdaptiveCache]=None
):
    """
    Decorador avançado para cache automático com múltiplas estratégias.
    
    Args:
        ttl: Time-to-live em segundos
        max_size_mb: Tamanho máximo do cache em MB
        strategy: Estratégia de cache
        tags: Tags para agrupamento de cache
        cache_instance: Instância de cache personalizada
    
    Returns:
        Decorator function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Usar cache existente ou criar novo
        cache = cache_instance or AdaptiveCache(
            max_size_bytes=max_size_mb * 1024 * 1024,
            default_ttl=ttl,
            strategy=strategy
        )
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            # Gerar chave de cache
            cache_key = cache._compute_key(*args, **kwargs)
            
            # Tentar obter do cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"⚡ Cache HIT: {func.__qualname__}")
                return cached_result
            
            logger.debug(f"📊 Cache MISS: {func.__qualname__}")
            result = func(*args, **kwargs)
            
            # Armazenar no cache
            cache.set(cache_key, result, ttl=ttl, tags=tags)
            
            return result
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            cache_key = cache._compute_key(*args, **kwargs)
            
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"⚡ Cache HIT (async): {func.__qualname__}")
                return cached_result
            
            logger.debug(f"📊 Cache MISS (async): {func.__qualname__}")
            result = await func(*args, **kwargs)
            
            cache.set(cache_key, result, ttl=ttl, tags=tags)
            
            return result
        
        wrapper = async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        wrapper.cache = cache  # Anexar cache à função para acesso direto
        return wrapper
    
    return decorator

# ============================================================================
# POOL DE MEMÓRIA COM ALOCAÇÃO INTELIGENTE
# ============================================================================


@dataclass
class MemoryBlock:
    """Bloco de memória com metadados avançados."""
    data: np.ndarray
    allocated: bool = False
    last_used: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    priority: MemoryPriority = MemoryPriority.MEDIUM
    lock: threading.Lock = field(default_factory=threading.Lock)
    
    def is_stale(self, timeout_seconds: float) -> bool:
        """Verifica se bloco está obsoleto."""
        if self.allocated:
            return False
        return (datetime.now() - self.last_used).total_seconds() > timeout_seconds


class SmartMemoryPool:
    """
    Pool de memória inteligente com múltiplas estratégias de alocação.
    """
    
    def __init__(
        self,
        block_sizes: List[int]=None,
        blocks_per_size: int=50,
        enable_oversubscription: bool=True,
        max_oversubscription: float=2.0
    ):
        self.block_sizes = block_sizes or [128, 256, 512, 1024, 2048, 4096]
        self.blocks_per_size = blocks_per_size
        self.enable_oversubscription = enable_oversubscription
        self.max_oversubscription = max_oversubscription
        
        # Estruturas de dados
        self.blocks: Dict[int, List[MemoryBlock]] = defaultdict(list)
        self.allocated_blocks: Dict[str, MemoryBlock] = {}
        self.lock = threading.RLock()
        self.total_allocated = 0
        
        # Inicializar pool
        self._initialize_pool()
        
        logger.info(
            f"💾 Smart Memory Pool inicializado: "
            f"{len(self.block_sizes)} tamanhos, "
            f"{blocks_per_size} blocos/tamanho"
        )
    
    def _initialize_pool(self) -> None:
        """Inicializa blocos de memória."""
        for size in self.block_sizes:
            dtype = np.float32  # Padrão para computação quântica
            for _ in range(self.blocks_per_size):
                block = MemoryBlock(
                    data=np.zeros(size, dtype=dtype),
                    priority=MemoryPriority.MEDIUM
                )
                self.blocks[size].append(block)
    
    def _find_best_fit(self, size: int) -> Optional[MemoryBlock]:
        """Encontra melhor bloco para tamanho solicitado."""
        # Buscar tamanho exato ou maior mais próximo
        for block_size in sorted(self.blocks.keys()):
            if block_size >= size:
                for block in self.blocks[block_size]:
                    if not block.allocated:
                        return block
        return None
    
    def allocate(
        self,
        size: int,
        dtype: np.dtype=np.float32,
        priority: MemoryPriority=MemoryPriority.MEDIUM
    ) -> np.ndarray:
        """
        Aloca memória do pool.
        
        Args:
            size: Tamanho necessário
            dtype: Tipo de dados NumPy
            priority: Prioridade da alocação
        
        Returns:
            Array NumPy alocado
        """
        with self.lock:
            # Buscar bloco existente
            block = self._find_best_fit(size)
            
            if block:
                block.allocated = True
                block.priority = priority
                block.last_used = datetime.now()
                
                # Gerar ID único
                block_id = f"block_{id(block.data)}_{datetime.now().timestamp()}"
                self.allocated_blocks[block_id] = block
                self.total_allocated += 1
                
                # Retornar slice do tamanho correto
                return block.data[:size].astype(dtype)
            
            # Oversubscription (se habilitado)
            if self.enable_oversubscription:
                max_size = max(self.block_sizes)
                if size <= max_size * self.max_oversubscription:
                    logger.debug(f"⚠️ Oversubscription: alocando novo bloco de {size}")
                    
                    # Criar novo bloco dinâmico
                    new_block = MemoryBlock(
                        data=np.zeros(max(size, max_size), dtype=dtype),
                        allocated=True,
                        priority=priority
                    )
                    
                    # Adicionar ao pool dinâmico
                    dynamic_size = max(size, max_size)
                    if dynamic_size not in self.blocks:
                        self.blocks[dynamic_size] = []
                    self.blocks[dynamic_size].append(new_block)
                    
                    block_id = f"dyn_{id(new_block.data)}"
                    self.allocated_blocks[block_id] = new_block
                    self.total_allocated += 1
                    
                    return new_block.data[:size]
            
            # Fallback: alocação direta
            logger.warning(f"⚠️ Pool exaurido - alocação direta de {size}")
            return np.zeros(size, dtype=dtype)
    
    def deallocate(self, data: np.ndarray) -> bool:
        """Libera memória de volta ao pool."""
        with self.lock:
            # Encontrar bloco correspondente
            for block_id, block in list(self.allocated_blocks.items()):
                if block.data.base is data.base:  # Verificar se é a mesma memória
                    block.allocated = False
                    block.data.fill(0)  # Zerar dados para segurança
                    
                    # Remover do dicionário de alocados
                    del self.allocated_blocks[block_id]
                    self.total_allocated -= 1
                    
                    return True
            
            logger.debug("⚠️ Tentativa de liberar memória não alocada pelo pool")
            return False
    
    def cleanup(self, timeout_seconds: float=3600.0) -> int:
        """Limpa blocos não utilizados."""
        with self.lock:
            cleaned = 0
            
            for size, blocks in list(self.blocks.items()):
                # Filtrar blocos inativos
                active_blocks = []
                
                for block in blocks:
                    if block.allocated or not block.is_stale(timeout_seconds):
                        active_blocks.append(block)
                    else:
                        cleaned += 1
                
                self.blocks[size] = active_blocks
            
            if cleaned > 0:
                logger.info(f"🧹 {cleaned} blocos de memória limpos")
            
            return cleaned
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do pool."""
        with self.lock:
            total_blocks = sum(len(blocks) for blocks in self.blocks.values())
            allocated_blocks = sum(1 for blocks in self.blocks.values() 
                                 for b in blocks if b.allocated)
            
            total_memory = sum(
                b.data.nbytes for blocks in self.blocks.values() 
                for b in blocks
            )
            
            return {
                'total_blocks': total_blocks,
                'allocated_blocks': allocated_blocks,
                'available_blocks': total_blocks - allocated_blocks,
                'total_memory_bytes': total_memory,
                'allocation_ratio': allocated_blocks / max(1, total_blocks),
                'block_sizes': list(self.blocks.keys())
            }

# ============================================================================
# OTIMIZADOR DE OPERAÇÕES COM PRIORIDADE
# ============================================================================


@dataclass
class QuantumOperation:
    """Operação quântica com metadados avançados."""
    id: str
    op_type: OperationType
    data: Any
    priority: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_overdue(self) -> bool:
        """Verifica se operação está atrasada."""
        if self.deadline is None:
            return False
        return datetime.now() > self.deadline
    
    def urgency(self) -> float:
        """Calcula urgência da operação."""
        base_urgency = self.priority / 10.0
        
        if self.deadline:
            time_left = (self.deadline - datetime.now()).total_seconds()
            if time_left <= 0:
                return float('inf')
            base_urgency += 1.0 / (time_left + 1)
        
        return base_urgency


class QuantumOperationScheduler:
    """
    Agendador inteligente de operações quânticas.
    """
    
    def __init__(
        self,
        batch_size: int=32,
        timeout_ms: int=50,
        enable_dynamic_batching: bool=True
    ):
        self.batch_size = batch_size
        self.timeout_ms = timeout_ms
        self.enable_dynamic_batching = enable_dynamic_batching
        
        self.queue: List[QuantumOperation] = []
        self.pending_deps: Dict[str, List[QuantumOperation]] = defaultdict(list)
        self.completed_ops: Dict[str, Any] = {}
        self.lock = threading.RLock()
        self.last_flush = datetime.now()
        
        logger.info(
            f"📦 Quantum Operation Scheduler inicializado: "
            f"batch={batch_size}, timeout={timeout_ms}ms"
        )
    
    def add_operation(self, op: QuantumOperation) -> str:
        """Adiciona operação ao scheduler."""
        with self.lock:
            # Verificar dependências
            ready = True
            for dep_id in op.dependencies:
                if dep_id not in self.completed_ops:
                    ready = False
                    self.pending_deps[dep_id].append(op)
            
            if ready:
                self.queue.append(op)
                # Ordenar por urgência
                self.queue.sort(key=lambda x:-x.urgency())
            else:
                logger.debug(f"⏳ Operação {op.id} aguardando dependências")
            
            return op.id
    
    def mark_completed(self, op_id: str, result: Any=None) -> None:
        """Marca operação como concluída."""
        with self.lock:
            self.completed_ops[op_id] = result
            
            # Liberar operações dependentes
            if op_id in self.pending_deps:
                for dependent_op in self.pending_deps[op_id]:
                    # Verificar se todas as dependências estão satisfeitas
                    if all(dep in self.completed_ops 
                          for dep in dependent_op.dependencies):
                        self.queue.append(dependent_op)
                
                del self.pending_deps[op_id]
            
            logger.debug(f"✅ Operação {op_id} concluída")
    
    def get_batch(self) -> Optional[List[QuantumOperation]]:
        """Obtém lote de operações para processamento."""
        with self.lock:
            if not self.queue:
                return None
            
            # Tamanho de lote dinâmico
            current_batch_size = self.batch_size
            if self.enable_dynamic_batching:
                # Ajustar baseado na urgência
                urgent_ops = sum(1 for op in self.queue if op.urgency() > 5.0)
                if urgent_ops > 0:
                    current_batch_size = min(current_batch_size, urgent_ops)
            
            # Selecionar operações
            batch = self.queue[:current_batch_size]
            self.queue = self.queue[current_batch_size:]
            
            # Ordenar por prioridade e deadline
            batch.sort(key=lambda op: (-op.priority,
                                     op.deadline or datetime.max))
            
            self.last_flush = datetime.now()
            
            logger.info(f"🚀 Batch de {len(batch)} operações agendado")
            return batch
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do scheduler."""
        with self.lock:
            return {
                'queue_size': len(self.queue),
                'pending_dependencies': len(self.pending_deps),
                'completed_operations': len(self.completed_ops),
                'avg_wait_time': self._calculate_avg_wait_time(),
                'dependency_chains': len(self.pending_deps)
            }
    
    def _calculate_avg_wait_time(self) -> float:
        """Calcula tempo médio de espera."""
        if not self.queue:
            return 0.0
        
        wait_times = [
            (datetime.now() - op.timestamp).total_seconds()
            for op in self.queue
        ]
        return np.mean(wait_times) if wait_times else 0.0

# ============================================================================
# SISTEMA DE MONITORAMENTO EM TEMPO REAL
# ============================================================================


@dataclass
class PerformanceMetric:
    """Métrica de performance com histórico."""
    name: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TelemetryCollector:
    """
    Coletor de telemetria em tempo real para sistema quântico.
    """
    
    def __init__(self, retention_days: int=7):
        self.metrics: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        self.alerts: List[Dict[str, Any]] = []
        self.lock = threading.RLock()
        self.start_time = time.time()
        self.retention_days = retention_days
        
        # Alertas configuráveis
        self.thresholds = {
            'cache_hit_rate': {'min': 70.0, 'max': 100.0},
            'memory_usage': {'min': 0.0, 'max': 90.0},
            'operation_latency': {'min': 0.0, 'max': 1000.0},  # ms
        }
        
        logger.info("📊 Telemetry Collector inicializado")
    
    def record_metric(
        self,
        name: str,
        value: float,
        unit: str,
        tags: Optional[Dict[str, str]]=None,
        metadata: Optional[Dict[str, Any]]=None
    ) -> None:
        """Registra métrica."""
        with self.lock:
            metric = PerformanceMetric(
                name=name,
                value=value,
                unit=unit,
                tags=tags or {},
                metadata=metadata or {}
            )
            
            self.metrics[name].append(metric)
            
            # Verificar alertas
            self._check_thresholds(name, value, tags or {})
            
            # Limitar histórico
            if len(self.metrics[name]) > 10000:
                self.metrics[name] = self.metrics[name][-5000:]
    
    def _check_thresholds(self, name: str, value: float, tags: Dict[str, str]) -> None:
        """Verifica se métrica ultrapassou thresholds."""
        if name in self.thresholds:
            threshold = self.thresholds[name]
            
            if value < threshold.get('min', float('-inf')):
                self._create_alert(
                    name=name,
                    level='WARNING',
                    message=f"{name} abaixo do mínimo: {value} < {threshold['min']}",
                    value=value,
                    tags=tags
                )
            elif value > threshold.get('max', float('inf')):
                self._create_alert(
                    name=name,
                    level='CRITICAL',
                    message=f"{name} acima do máximo: {value} > {threshold['max']}",
                    value=value,
                    tags=tags
                )
    
    def _create_alert(
        self,
        name: str,
        level: str,
        message: str,
        value: float,
        tags: Dict[str, str]
    ) -> None:
        """Cria alerta."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'level': level,
            'message': message,
            'value': value,
            'tags': tags
        }
        
        self.alerts.append(alert)
        logger.warning(f"🚨 {level}: {message}")
        
        # Manter apenas últimos 100 alertas
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-50:]
    
    def get_aggregated_metrics(
        self,
        name: str,
        aggregation: str='mean',
        window_minutes: int=5
    ) -> Optional[Dict[str, Any]]:
        """Retorna métricas agregadas."""
        with self.lock:
            if name not in self.metrics:
                return None
            
            window_start = datetime.now() - timedelta(minutes=window_minutes)
            recent_metrics = [
                m for m in self.metrics[name]
                if m.timestamp > window_start
            ]
            
            if not recent_metrics:
                return None
            
            values = [m.value for m in recent_metrics]
            
            aggregates = {
                'mean': np.mean(values),
                'median': np.median(values),
                'min': np.min(values),
                'max': np.max(values),
                'std': np.std(values),
                'count': len(values),
                'last': recent_metrics[-1].value,
                'timestamp': recent_metrics[-1].timestamp
            }
            
            return {aggregation: aggregates[aggregation], **aggregates}
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Retorna dados para dashboard."""
        with self.lock:
            uptime = time.time() - self.start_time
            
            # Métricas principais
            main_metrics = {}
            for metric_name in ['cache_hit_rate', 'memory_usage', 'operation_latency']:
                if metric_name in self.metrics:
                    recent = self.get_aggregated_metrics(metric_name, 'mean', 1)
                    if recent:
                        main_metrics[metric_name] = recent
            
            return {
                'uptime_seconds': uptime,
                'uptime_human': str(timedelta(seconds=int(uptime))),
                'metrics_tracked': len(self.metrics),
                'total_measurements': sum(len(m) for m in self.metrics.values()),
                'active_alerts': len([a for a in self.alerts 
                                    if a['level'] == 'CRITICAL']),
                'main_metrics': main_metrics,
                'recent_alerts': self.alerts[-10:] if self.alerts else []
            }

# ============================================================================
# COORDENADOR PRINCIPAL
# ============================================================================


class QuantumOptimizationCoordinator:
    """
    Coordenador principal de otimizações quânticas (Singleton).
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(
        self,
        config: Optional[Dict[str, Any]]=None
    ):
        if getattr(self, '_initialized', False):
            return
        
        self.config = config or {}
        
        # Componentes
        self.cache = AdaptiveCache(
            max_size_bytes=self.config.get('cache_size_mb', 100) * 1024 * 1024,
            strategy=CacheStrategy[self.config.get('cache_strategy', 'LRU')],
            default_ttl=self.config.get('cache_ttl', 300.0)
        )
        
        self.memory_pool = SmartMemoryPool(
            block_sizes=self.config.get('memory_block_sizes',
                                      [128, 256, 512, 1024, 2048, 4096]),
            blocks_per_size=self.config.get('blocks_per_size', 50)
        )
        
        self.scheduler = QuantumOperationScheduler(
            batch_size=self.config.get('batch_size', 32),
            timeout_ms=self.config.get('batch_timeout_ms', 50)
        )
        
        self.telemetry = TelemetryCollector(
            retention_days=self.config.get('retention_days', 7)
        )
        
        # Executores
        self.thread_executor = ThreadPoolExecutor(
            max_workers=self.config.get('thread_workers', 8),
            thread_name_prefix="quantum_worker"
        )
        
        self.process_executor = ProcessPoolExecutor(
            max_workers=self.config.get('process_workers', 4)
        )
        
        # Background tasks
        self._cleanup_task = None
        self._monitoring_task = None
        self._running = False
        
        self._initialized = True
        logger.info("🚀 Quantum Optimization Coordinator inicializado")
    
    def start_background_tasks(self) -> None:
        """Inicia tarefas em background."""
        if self._running:
            return
        
        self._running = True
        
        # Tarefa de limpeza periódica
        self._cleanup_task = threading.Thread(
            target=self._cleanup_loop,
            daemon=True,
            name="cleanup_thread"
        )
        self._cleanup_task.start()
        
        # Tarefa de monitoramento
        self._monitoring_task = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="monitoring_thread"
        )
        self._monitoring_task.start()
        
        logger.info("🔄 Tarefas em background iniciadas")
    
    def _cleanup_loop(self) -> None:
        """Loop de limpeza periódica."""
        while self._running:
            try:
                time.sleep(300)  # 5 minutos
                
                logger.debug("🧹 Executando limpeza periódica...")
                
                # Limpar cache expirado
                expired = self.cache.clear_expired()
                if expired > 0:
                    self.telemetry.record_metric(
                        'cache_cleaned',
                        expired,
                        'entries',
                        {'type': 'expired'}
                    )
                
                # Limpar memória
                memory_cleaned = self.memory_pool.cleanup(timeout_seconds=1800)
                if memory_cleaned > 0:
                    self.telemetry.record_metric(
                        'memory_cleaned',
                        memory_cleaned,
                        'blocks',
                        {'type': 'stale'}
                    )
                
                # Coletar lixo
                gc.collect()
                
            except Exception as e:
                logger.error(f"Erro no loop de limpeza: {e}")
    
    def _monitoring_loop(self) -> None:
        """Loop de monitoramento."""
        while self._running:
            try:
                time.sleep(10)  # 10 segundos
                
                # Coletar métricas
                cache_stats = self.cache.get_stats()
                self.telemetry.record_metric(
                    'cache_hit_rate',
                    cache_stats['hit_rate_percent'],
                    'percent',
                    {'strategy': cache_stats['strategy']}
                )
                
                self.telemetry.record_metric(
                    'cache_memory_usage',
                    cache_stats['memory_usage_percent'],
                    'percent'
                )
                
                pool_stats = self.memory_pool.get_stats()
                self.telemetry.record_metric(
                    'memory_allocation_ratio',
                    pool_stats['allocation_ratio'] * 100,
                    'percent'
                )
                
                scheduler_stats = self.scheduler.get_stats()
                self.telemetry.record_metric(
                    'operation_queue_size',
                    scheduler_stats['queue_size'],
                    'operations'
                )
                
            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")
    
    def optimize_function(
        self,
        func: Callable,
        ttl: Optional[float]=None,
        tags: Optional[Dict[str, str]]=None
    ) -> Callable:
        """Otimiza função com cache."""
        return quantum_cache(
            ttl=ttl or self.config.get('default_ttl', 300.0),
            cache_instance=self.cache,
            tags=tags
        )(func)
    
    def allocate_memory(
        self,
        size: int,
        dtype: np.dtype=np.float32,
        priority: MemoryPriority=MemoryPriority.MEDIUM
    ) -> np.ndarray:
        """Aloca memória otimizada."""
        memory = self.memory_pool.allocate(size, dtype, priority)
        
        self.telemetry.record_metric(
            'memory_allocated',
            size,
            'elements',
            {'dtype': str(dtype), 'priority': priority.name}
        )
        
        return memory
    
    def schedule_operation(
        self,
        op_type: OperationType,
        data: Any,
        priority: int=0,
        dependencies: Optional[List[str]]=None,
        deadline_seconds: Optional[float]=None
    ) -> str:
        """Agenda operação quântica."""
        deadline = None
        if deadline_seconds:
            deadline = datetime.now() + timedelta(seconds=deadline_seconds)
        
        operation = QuantumOperation(
            id=f"op_{int(time.time() * 1000)}_{hash(data) % 10000:04d}",
            op_type=op_type,
            data=data,
            priority=priority,
            dependencies=dependencies or [],
            deadline=deadline
        )
        
        op_id = self.scheduler.add_operation(operation)
        
        self.telemetry.record_metric(
            'operations_scheduled',
            1,
            'count',
            {'type': op_type.value, 'priority': priority}
        )
        
        return op_id
    
    def execute_batch(self) -> Optional[List[Tuple[str, Any]]]:
        """Executa lote de operações agendadas."""
        batch = self.scheduler.get_batch()
        if not batch:
            return None
        
        results = []
        
        for operation in batch:
            try:
                # Simulação de execução
                result = self._execute_operation(operation)
                results.append((operation.id, result))
                self.scheduler.mark_completed(operation.id, result)
                
                self.telemetry.record_metric(
                    'operation_execution_time',
                    (datetime.now() - operation.timestamp).total_seconds(),
                    'seconds',
                    {'type': operation.op_type.value}
                )
                
            except Exception as e:
                logger.error(f"Erro executando operação {operation.id}: {e}")
                self.telemetry.record_metric(
                    'operation_errors',
                    1,
                    'count',
                    {'type': operation.op_type.value, 'error': str(e)}
                )
        
        return results
    
    def _execute_operation(self, operation: QuantumOperation) -> Any:
        """Executa uma operação quântica (simulação)."""
        # Em um sistema real, aqui estaria a execução real do circuito quântico
        time.sleep(0.01)  # Simulação de latência
        
        return {
            'operation_id': operation.id,
            'type': operation.op_type.value,
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_system_report(self) -> Dict[str, Any]:
        """Gera relatório completo do sistema."""
        cache_stats = self.cache.get_stats()
        pool_stats = self.memory_pool.get_stats()
        scheduler_stats = self.scheduler.get_stats()
        dashboard = self.telemetry.get_dashboard_data()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system_status': {
                'running': self._running,
                'background_tasks': {
                    'cleanup': self._cleanup_task.is_alive() if self._cleanup_task else False,
                    'monitoring': self._monitoring_task.is_alive() if self._monitoring_task else False
                }
            },
            'cache': cache_stats,
            'memory_pool': pool_stats,
            'scheduler': scheduler_stats,
            'telemetry': dashboard,
            'config': self.config
        }
    
    def shutdown(self) -> None:
        """Desliga o sistema graciosamente."""
        logger.info("🛑 Desligando Quantum Optimization Coordinator...")
        
        self._running = False
        
        # Parar executores
        self.thread_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)
        
        # Aguardar tarefas em background
        if self._cleanup_task:
            self._cleanup_task.join(timeout=5.0)
        if self._monitoring_task:
            self._monitoring_task.join(timeout=5.0)
        
        # Limpar recursos
        self.cache.clear_expired()
        self.memory_pool.cleanup(timeout_seconds=0)
        
        logger.info("✅ Sistema desligado com sucesso")

# ============================================================================
# UTILIDADES ASSÍNCRONAS AVANÇADAS
# ============================================================================


class AsyncQuantumExecutor:
    """Executor assíncrono avançado para operações quânticas."""
    
    def __init__(self, coordinator: QuantumOptimizationCoordinator):
        self.coordinator = coordinator
        self.semaphore = asyncio.Semaphore(
            coordinator.config.get('max_concurrent_async', 16)
        )
    
    async def execute_parallel(
        self,
        operations: List[Callable[[], Any]],
        timeout_per_op: Optional[float]=None
    ) -> List[Any]:
        """
        Executa operações em paralelo com controle de concorrência.
        
        Args:
            operations: Lista de funções para executar
            timeout_per_op: Timeout por operação em segundos
        
        Returns:
            Lista de resultados
        """

        async def bounded_operation(op: Callable[[], Any]) -> Any:
            async with self.semaphore:
                try:
                    if asyncio.iscoroutinefunction(op):
                        if timeout_per_op:
                            return await asyncio.wait_for(
                                op(),
                                timeout=timeout_per_op
                            )
                        return await op()
                    else:
                        # Executar em thread pool para funções síncronas
                        loop = asyncio.get_event_loop()
                        if timeout_per_op:
                            return await asyncio.wait_for(
                                loop.run_in_executor(
                                    self.coordinator.thread_executor,
                                    op
                                ),
                                timeout=timeout_per_op
                            )
                        return await loop.run_in_executor(
                            self.coordinator.thread_executor,
                            op
                        )
                except asyncio.TimeoutError:
                    self.coordinator.telemetry.record_metric(
                        'async_timeouts',
                        1,
                        'count'
                    )
                    raise
                except Exception as e:
                    logger.error(f"Erro em operação assíncrona: {e}")
                    raise
        
        start_time = time.time()
        
        # Executar todas as operações
        tasks = [bounded_operation(op) for op in operations]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar exceções
        final_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Operação falhou: {result}")
                final_results.append(None)
            else:
                final_results.append(result)
        
        total_time = time.time() - start_time
        
        self.coordinator.telemetry.record_metric(
            'async_batch_time',
            total_time,
            'seconds',
            {'operations': len(operations)}
        )
        
        return final_results
    
    async def process_stream(
        self,
        data_stream: List[Any],
        process_func: Callable[[Any], Any],
        batch_size: int=32,
        max_concurrent_batches: int=4
    ) -> List[Any]:
        """
        Processa stream de dados em lotes concorrentes.
        
        Args:
            data_stream: Stream de dados
            process_func: Função de processamento
            batch_size: Tamanho do lote
            max_concurrent_batches: Máximo de lotes concorrentes
        
        Returns:
            Lista de resultados
        """
        results = []
        batch_semaphore = asyncio.Semaphore(max_concurrent_batches)
        
        async def process_batch(batch: List[Any]) -> List[Any]:
            async with batch_semaphore:
                batch_ops = [lambda x = item: process_func(x) for item in batch]
                return await self.execute_parallel(batch_ops)
        
        # Processar em lotes
        batches = [
            data_stream[i:i + batch_size]
            for i in range(0, len(data_stream), batch_size)
        ]
        
        batch_tasks = [process_batch(batch) for batch in batches]
        batch_results = await asyncio.gather(*batch_tasks)
        
        # Concatenar resultados
        for batch in batch_results:
            results.extend(batch)
        
        return results

# ============================================================================
# FÁBRICA E INICIALIZAÇÃO
# ============================================================================


def create_quantum_optimizer(
    config: Optional[Dict[str, Any]]=None
) -> QuantumOptimizationCoordinator:
    """
    Cria e inicializa otimizador quântico.
    
    Args:
        config: Configuração personalizada
    
    Returns:
        Instância do otimizador
    """
    default_config = {
        'cache_size_mb': 100,
        'cache_strategy': 'ARC',
        'cache_ttl': 300.0,
        'memory_block_sizes': [128, 256, 512, 1024, 2048, 4096],
        'blocks_per_size': 50,
        'batch_size': 32,
        'batch_timeout_ms': 50,
        'thread_workers': 8,
        'process_workers': 4,
        'retention_days': 7,
        'max_concurrent_async': 16,
        'auto_start_background': True
    }
    
    if config:
        default_config.update(config)
    
    optimizer = QuantumOptimizationCoordinator(default_config)
    
    if default_config.get('auto_start_background', True):
        optimizer.start_background_tasks()
    
    return optimizer


def get_global_optimizer() -> QuantumOptimizationCoordinator:
    """Retorna instância global do otimizador."""
    return create_quantum_optimizer()

# ============================================================================
# DECORADORES ÚTEIS
# ============================================================================


def optimized_quantum_computation(
    ttl: float=300.0,
    memory_size: Optional[int]=None,
    priority: int=0
):
    """
    Decorador para computação quântica otimizada.
    
    Combina caching, alocação de memória e telemetria.
    """

    def decorator(func: Callable) -> Callable:
        optimizer = get_global_optimizer()
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Alocar memória se necessário
            memory = None
            if memory_size:
                memory = optimizer.allocate_memory(
                    memory_size,
                    priority=MemoryPriority.HIGH
                )
                kwargs['memory_buffer'] = memory
            
            try:
                # Usar função otimizada com cache
                cached_func = optimizer.optimize_function(func, ttl=ttl)
                return cached_func(*args, **kwargs)
            finally:
                # Liberar memória
                if memory is not None:
                    optimizer.memory_pool.deallocate(memory)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            memory = None
            if memory_size:
                memory = optimizer.allocate_memory(
                    memory_size,
                    priority=MemoryPriority.HIGH
                )
                kwargs['memory_buffer'] = memory
            
            try:
                cached_func = optimizer.optimize_function(func, ttl=ttl)
                return await cached_func(*args, **kwargs)
            finally:
                if memory is not None:
                    optimizer.memory_pool.deallocate(memory)
        
        wrapper = async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        
        # Adicionar metadados
        wrapper.metadata = {
            'optimized': True,
            'ttl': ttl,
            'memory_size': memory_size,
            'priority': priority
        }
        
        return wrapper
    
    return decorator

# ============================================================================
# TESTES E DEMONSTRAÇÃO
# ============================================================================


async def demo_advanced_features():
    """Demonstração das funcionalidades avançadas."""
    print("🧪 Demonstração do Quantum Performance Optimizer")
    print("=" * 60)
    
    # Criar otimizador com configuração personalizada
    optimizer = create_quantum_optimizer({
        'cache_size_mb': 50,
        'cache_strategy': 'ARC',
        'thread_workers': 4
    })
    
    # 1. Teste de cache avançado
    print("\n1. 🗄️ Teste de Cache Adaptativo (ARC):")
    
    @quantum_cache(ttl=10.0, strategy=CacheStrategy.ARC)
    def compute_quantum_state(n: int) -> np.ndarray:
        """Simulação de computação quântica pesada."""
        time.sleep(0.1)
        return np.random.randn(n)
    
    # Primeira execução (miss)
    start = time.time()
    result1 = compute_quantum_state(1000)
    time1 = time.time() - start
    
    # Segunda execução (hit)
    start = time.time()
    result2 = compute_quantum_state(1000)
    time2 = time.time() - start
    
    print(f"   Primeira execução: {time1:.3f}s")
    print(f"   Segunda execução (cache): {time2:.3f}s")
    print(f"   Speedup: {time1/time2:.1f}x")
    print(f"   Resultados iguais: {np.allclose(result1, result2)}")
    
    # 2. Teste de pool de memória
    print("\n2. 💾 Teste de Smart Memory Pool:")
    
    # Alocar múltiplos blocos
    blocks = []
    for i in range(5):
        mem = optimizer.allocate_memory(512, priority=MemoryPriority.HIGH)
        blocks.append(mem)
        print(f"   Bloco {i}: shape={mem.shape}, dtype={mem.dtype}")
    
    # Liberar alguns
    for i in range(2):
        optimizer.memory_pool.deallocate(blocks[i])
        print(f"   Bloco {i} liberado")
    
    pool_stats = optimizer.memory_pool.get_stats()
    print(f"   Estatísticas do pool: {pool_stats['allocated_blocks']}/{pool_stats['total_blocks']} alocados")
    
    # 3. Teste de agendamento de operações
    print("\n3. 📦 Teste de Quantum Operation Scheduler:")
    
    # Agendar operações com dependências
    op1_id = optimizer.schedule_operation(
        OperationType.GATE_APPLICATION,
        data={"gate": "H", "qubit": 0},
        priority=10
    )
    
    op2_id = optimizer.schedule_operation(
        OperationType.ENTANGLEMENT,
        data={"qubits": [0, 1]},
        priority=5,
        dependencies=[op1_id]  # Depende da primeira operação
    )
    
    print(f"   Operação 1 ID: {op1_id}")
    print(f"   Operação 2 ID: {op2_id} (depende de {op1_id})")
    
    # Executar batch
    results = optimizer.execute_batch()
    if results:
        print(f"   Batch executado: {len(results)} operações")
        for op_id, result in results:
            print(f"     {op_id}: {result['status']}")
    
    # 4. Teste assíncrono
    print("\n4. ⚡ Teste de Execução Assíncrona:")
    
    async_processor = AsyncQuantumExecutor(optimizer)
    
    # Criar operações assíncronas
    async_ops = [
        lambda x = i: time.sleep(0.05) or f"result_{x}"
        for i in range(10)
    ]
    
    start = time.time()
    async_results = await async_processor.execute_parallel(async_ops)
    async_time = time.time() - start
    
    print(f"   {len(async_results)} operações em {async_time:.3f}s")
    print(f"   ~{len(async_results)/async_time:.1f} ops/segundo")
    
    # 5. Relatório do sistema
    print("\n5. 📊 Relatório Completo do Sistema:")
    report = optimizer.get_system_report()
    
    print(f"   Status: {'Running' if report['system_status']['running'] else 'Stopped'}")
    print(f"   Cache Hit Rate: {report['cache']['hit_rate_percent']:.1f}%")
    print(f"   Memória Alocada: {report['memory_pool']['allocation_ratio']*100:.1f}%")
    print(f"   Operações na Fila: {report['scheduler']['queue_size']}")
    
    # 6. Limpeza
    print("\n6. 🧹 Limpeza de Recursos:")
    optimizer.shutdown()
    
    print("\n" + "=" * 60)
    print("✅ Demonstração concluída com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    
    # Executar demonstração
    asyncio.run(demo_advanced_features())
