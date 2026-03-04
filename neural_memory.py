# neural_memory.py
import asyncio
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import json
import pickle
from enum import Enum

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    TRADING_EXPERIENCE = "trading_experience"
    MARKET_PATTERN = "market_pattern"
    STRATEGY_PERFORMANCE = "strategy_performance"
    RISK_EVENT = "risk_event"
    SYSTEM_LEARNING = "system_learning"

class NeuralMemory:
    """Sistema de memória neural para aprendizado contínuo"""
    
    def __init__(self, system_type: str, max_memories: int = 10000):
        self.system_type = system_type
        self.max_memories = max_memories
        self.memories: List[Dict[str, Any]] = []
        self.memory_index: Dict[str, List[int]] = {}
        self.associations: Dict[str, List[str]] = {}
        self.learning_rate = 0.1
        self.retention_rate = 0.95
        
    async def initialize(self):
        """Inicializa o sistema de memória neural"""
        logger.info("🧠 Inicializando Memória Neural...")
        
        # Carregar memórias persistentes se existirem
        await self.load_persistent_memories()
        
        # Inicializar estruturas de indexação
        await self.initialize_memory_index()
        
        logger.info(f"✅ Memória Neural inicializada: {len(self.memories)} memórias carregadas")
        
    async def store_memory(self, data: Dict[str, Any], memory_type: MemoryType, 
                          importance: float = 0.5, tags: List[str] = None) -> str:
        """Armazena uma nova memória no sistema"""
        try:
            memory_id = f"mem_{datetime.now().timestamp()}_{len(self.memories)}"
            
            memory = {
                'id': memory_id,
                'type': memory_type.value,
                'data': data,
                'timestamp': datetime.now(),
                'importance': importance,
                'tags': tags or [],
                'access_count': 0,
                'last_accessed': datetime.now(),
                'associations': [],
                'embedding': await self.generate_embedding(data)
            }
            
            # Adicionar à lista de memórias
            self.memories.append(memory)
            
            # Atualizar índice
            await self.update_memory_index(memory)
            
            # Estabelecer associações
            await self.establish_associations(memory)
            
            # Gerenciar limite de memórias
            if len(self.memories) > self.max_memories:
                await self.forget_least_important()
                
            # Salvar persistentemente
            await self.save_persistent_memories()
            
            logger.debug(f"💾 Memória armazenada: {memory_type.value} - {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao armazenar memória: {e}")
            return ""
            
    async def retrieve_memory(self, query: Dict[str, Any], max_results: int = 10, 
                             memory_type: Optional[MemoryType] = None) -> List[Dict[str, Any]]:
        """Recupera memórias relevantes baseado na consulta"""
        try:
            query_embedding = await self.generate_embedding(query)
            
            # Calcular similaridade com todas as memórias
            similarities = []
            for memory in self.memories:
                if memory_type and memory['type'] != memory_type.value:
                    continue
                    
                similarity = await self.calculate_similarity(
                    query_embedding, memory['embedding']
                )
                
                # Ajustar pela importância e frequência de acesso
                adjusted_score = (
                    similarity * 0.6 +
                    memory['importance'] * 0.3 +
                    (memory['access_count'] / 100) * 0.1
                )
                
                similarities.append((adjusted_score, memory))
                
            # Ordenar por similaridade
            similarities.sort(key=lambda x: x[0], reverse=True)
            
            # Retornar top resultados
            results = []
            for score, memory in similarities[:max_results]:
                # Atualizar contador de acesso
                memory['access_count'] += 1
                memory['last_accessed'] = datetime.now()
                
                results.append({
                    'memory': memory,
                    'relevance_score': score,
                    'associations': await self.get_related_memories(memory['id'])
                })
                
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar memórias: {e}")
            return []
            
    async def generate_embedding(self, data: Dict[str, Any]) -> np.ndarray:
        """Gera embedding vetorial para os dados"""
        # Implementação simplificada de embedding
        features = []
        
        # Extrair features numéricas
        for key, value in data.items():
            if isinstance(value, (int, float)):
                features.append(float(value))
            elif isinstance(value, str):
                # Hash simples para strings
                features.append(hash(value) % 1000 / 1000.0)
            elif isinstance(value, bool):
                features.append(1.0 if value else 0.0)
                
        # Preencher com zeros se necessário
        while len(features) < 16:
            features.append(0.0)
            
        # Manter apenas 16 dimensões para simplificar
        embedding = np.array(features[:16], dtype=np.float32)
        
        # Normalizar
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
            
        return embedding
        
    async def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calcula similaridade entre embeddings"""
        return float(np.dot(embedding1, embedding2))
        
    async def establish_associations(self, memory: Dict[str, Any]):
        """Estabelece associações entre memórias"""
        try:
            associations = []
            
            # Encontrar memórias similares
            for other_memory in self.memories:
                if other_memory['id'] == memory['id']:
                    continue
                    
                similarity = await self.calculate_similarity(
                    memory['embedding'], other_memory['embedding']
                )
                
                if similarity > 0.7:  # Threshold para associação
                    associations.append(other_memory['id'])
                    
                    # Atualizar associação bidirecional
                    if 'associations' not in other_memory:
                        other_memory['associations'] = []
                    if memory['id'] not in other_memory['associations']:
                        other_memory['associations'].append(memory['id'])
                        
            memory['associations'] = associations
            
        except Exception as e:
            logger.error(f"❌ Erro ao estabelecer associações: {e}")
            
    async def get_related_memories(self, memory_id: str) -> List[Dict[str, Any]]:
        """Obtém memórias relacionadas"""
        for memory in self.memories:
            if memory['id'] == memory_id:
                related = []
                for related_id in memory.get('associations', []):
                    related_memory = await self.get_memory_by_id(related_id)
                    if related_memory:
                        related.append(related_memory)
                return related
        return []
        
    async def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Obtém memória pelo ID"""
        for memory in self.memories:
            if memory['id'] == memory_id:
                return memory
        return None
        
    async def update_memory_index(self, memory: Dict[str, Any]):
        """Atualiza o índice de memórias"""
        # Indexar por tipo
        if memory['type'] not in self.memory_index:
            self.memory_index[memory['type']] = []
        self.memory_index[memory['type']].append(len(self.memories) - 1)
        
        # Indexar por tags
        for tag in memory['tags']:
            if tag not in self.memory_index:
                self.memory_index[tag] = []
            self.memory_index[tag].append(len(self.memories) - 1)
            
    async def initialize_memory_index(self):
        """Inicializa o índice de memórias"""
        self.memory_index.clear()
        for i, memory in enumerate(self.memories):
            await self.update_memory_index(memory)
            
    async def forget_least_important(self):
        """Esquece memórias menos importantes"""
        if len(self.memories) <= self.max_memories:
            return
            
        # Calcular scores de esquecimento
        forget_scores = []
        current_time = datetime.now()
        
        for i, memory in enumerate(self.memories):
            # Score baseado na importância, acesso e idade
            age_days = (current_time - memory['timestamp']).days
            forget_score = (
                (1 - memory['importance']) * 0.4 +
                (1 - min(memory['access_count'] / 100, 1)) * 0.3 +
                min(age_days / 365, 1) * 0.3
            )
            forget_scores.append((forget_score, i))
            
        # Ordenar por score de esquecimento
        forget_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Esquecer memórias excedentes
        num_to_forget = len(self.memories) - self.max_memories
        indices_to_remove = [i for _, i in forget_scores[:num_to_forget]]
        
        # Remover em ordem reversa para preservar índices
        for i in sorted(indices_to_remove, reverse=True):
            if i < len(self.memories):
                removed_memory = self.memories.pop(i)
                logger.debug(f"🧹 Memória esquecida: {removed_memory['id']}")
                
        # Reconstruir índice
        await self.initialize_memory_index()
        
    async def save_persistent_memories(self):
        """Salva memórias persistentemente"""
        try:
            data = {
                'memories': self.memories,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(f'neural_memory_{self.system_type}.pkl', 'wb') as f:
                pickle.dump(data, f)
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar memórias: {e}")
            
    async def load_persistent_memories(self):
        """Carrega memórias persistentes"""
        try:
            with open(f'neural_memory_{self.system_type}.pkl', 'rb') as f:
                data = pickle.load(f)
                self.memories = data.get('memories', [])
                
            logger.info(f"📂 Memórias carregadas: {len(self.memories)}")
        except FileNotFoundError:
            logger.info("📂 Nenhuma memória persistente encontrada")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar memórias: {e}")
            
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da memória"""
        type_counts = {}
        for memory in self.memories:
            mem_type = memory['type']
            type_counts[mem_type] = type_counts.get(mem_type, 0) + 1
            
        return {
            'total_memories': len(self.memories),
            'memory_types': type_counts,
            'average_importance': np.mean([m['importance'] for m in self.memories]),
            'total_accesses': sum(m['access_count'] for m in self.memories),
            'index_size': len(self.memory_index)
        }
        
    async def shutdown(self):
        """Desliga o sistema de memória"""
        logger.info("🔌 Desligando Memória Neural...")
        await self.save_persistent_memories()
        logger.info("✅ Memória Neural desligada")