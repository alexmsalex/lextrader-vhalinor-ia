import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import random
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import websockets
from cryptography.fernet import Fernet
import heapq
import threading
from collections import defaultdict, deque
import pickle
import zlib

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AdvancedDistributedSystem')

class NodeStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    BOOTSTRAPPING = "bootstrapping"
    MAINTENANCE = "maintenance"

class MessageType(Enum):
    HEARTBEAT = "heartbeat"
    DATA_SYNC = "data_sync"
    CONSENSUS = "consensus"
    TRANSACTION = "transaction"
    QUERY = "query"
    REPLICATION = "replication"
    LEADER_ELECTION = "leader_election"
    GOSSIP = "gossip"

class ConsistencyLevel(Enum):
    STRONG = "strong"
    EVENTUAL = "eventual"
    CAUSAL = "causal"
    SEQUENTIAL = "sequential"

@dataclass
class Node:
    id: str
    address: str
    port: int
    status: NodeStatus = NodeStatus.OFFLINE
    last_heartbeat: Optional[datetime] = None
    capabilities: List[str] = field(default_factory=list)
    load: float = 0.0
    version: str = "1.0.0"

@dataclass
class DistributedMessage:
    id: str
    type: MessageType
    source: str
    destination: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: int = 300  # Time to live in seconds
    consistency: ConsistencyLevel = ConsistencyLevel.EVENTUAL
    signature: Optional[str] = None

@dataclass
class Partition:
    id: str
    name: str
    nodes: List[str]
    replication_factor: int = 3
    consistency_level: ConsistencyLevel = ConsistencyLevel.EVENTUAL

@dataclass
class ConsensusResult:
    success: bool
    value: Any
    quorum_size: int
    participants: List[str]
    timestamp: datetime

class AdvancedDistributedSystem:
    """
    Sistema Distribuído Avançado com múltiplas funcionalidades:
    - Descoberta automática de nós
    - Consenso distribuído (Paxos/Raft)
    - Particionamento de dados
    - Replicação automática
    - Balanceamento de carga
    - Tolerância a falhas
    - Comunicação segura
    - Monitoramento em tempo real
    """
    
    def __init__(self, node_id: Optional[str] = None, host: str = "localhost", port: int = 8000):
        self.node_id = node_id or str(uuid.uuid4())
        self.host = host
        self.port = port
        self.address = f"{host}:{port}"
        
        # Estado do sistema
        self.nodes: Dict[str, Node] = {}
        self.partitions: Dict[str, Partition] = {}
        self.data_store: Dict[str, Any] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.leader_id: Optional[str] = None
        self.term: int = 0
        self.voted_for: Optional[str] = None
        
        # Configurações
        self.heartbeat_interval = 5  # segundos
        self.election_timeout_range = (150, 300)  # ms
        self.replication_factor = 3
        self.quorum_size = 2
        
        # Criptografia
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Estatísticas e monitoramento
        self.metrics: Dict[str, Any] = {
            'messages_sent': 0,
            'messages_received': 0,
            'consensus_operations': 0,
            'failed_operations': 0,
            'average_latency': 0.0,
            'node_uptime': {}
        }
        
        # Thread pools e execução assíncrona
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        self.background_tasks: List[asyncio.Task] = []
        
        # Sistema de gossip para disseminação de estado
        self.gossip_state: Dict[str, Any] = {}
        self.gossip_peers: List[str] = []
        
        # Cache distribuído
        self.cache: Dict[str, Any] = {}
        self.cache_ttl: Dict[str, datetime] = {}
        
        # Lock para operações concorrentes
        self._lock = threading.RLock()
        self._consensus_lock = asyncio.Lock()
        
        logger.info(f"Sistema Distribuído inicializado - Nó: {self.node_id}")

    async def initialize(self, bootstrap_nodes: List[str] = None):
        """Inicializa o sistema distribuído"""
        try:
            # Registrar próprio nó
            self._register_self()
            
            # Iniciar tarefas em background
            self.background_tasks = [
                asyncio.create_task(self._heartbeat_loop()),
                asyncio.create_task(self._message_processor()),
                asyncio.create_task(self._gossip_loop()),
                asyncio.create_task(self._cache_cleanup_loop()),
                asyncio.create_task(self._monitoring_loop())
            ]
            
            # Bootstrap com outros nós
            if bootstrap_nodes:
                await self._bootstrap(bootstrap_nodes)
            
            # Iniciar eleição de líder se necessário
            await asyncio.sleep(random.uniform(*self.election_timeout_range) / 1000)
            if not self.leader_id:
                await self._start_election()
            
            logger.info(f"Sistema Distribuído inicializado com sucesso - Líder: {self.leader_id}")
            
        except Exception as e:
            logger.error(f"Erro na inicialização: {e}")
            raise

    def _register_self(self):
        """Registra o próprio nó no sistema"""
        self_node = Node(
            id=self.node_id,
            address=self.host,
            port=self.port,
            status=NodeStatus.ONLINE,
            last_heartbeat=datetime.now(),
            capabilities=['storage', 'compute', 'routing'],
            load=0.0
        )
        self.nodes[self.node_id] = self_node

    async def _bootstrap(self, bootstrap_nodes: List[str]):
        """Conecta com nós de bootstrap para entrar no cluster"""
        for node_addr in bootstrap_nodes:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"http://{node_addr}/cluster/join",
                        json={
                            'node_id': self.node_id,
                            'address': self.address,
                            'capabilities': ['storage', 'compute', 'routing']
                        },
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            # Atualizar lista de nós
                            for node_info in data.get('nodes', []):
                                node = Node(**node_info)
                                self.nodes[node.id] = node
                            logger.info(f"Bootstrap bem-sucedido com {node_addr}")
                            break
            except Exception as e:
                logger.warning(f"Falha no bootstrap com {node_addr}: {e}")
                continue

    async def _heartbeat_loop(self):
        """Loop para enviar heartbeats periódicos"""
        while True:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                
                # Atualizar próprio heartbeat
                self.nodes[self.node_id].last_heartbeat = datetime.now()
                self.nodes[self.node_id].load = self._calculate_current_load()
                
                # Enviar heartbeats para outros nós
                heartbeat_msg = DistributedMessage(
                    id=str(uuid.uuid4()),
                    type=MessageType.HEARTBEAT,
                    source=self.node_id,
                    destination="broadcast",
                    payload={
                        'node_id': self.node_id,
                        'status': NodeStatus.ONLINE.value,
                        'load': self.nodes[self.node_id].load,
                        'timestamp': datetime.now().isoformat()
                    }
                )
                
                await self._broadcast_message(heartbeat_msg)
                
                # Verificar nós inativos
                await self._check_inactive_nodes()
                
            except Exception as e:
                logger.error(f"Erro no heartbeat loop: {e}")

    async def _message_processor(self):
        """Processa mensagens da fila"""
        while True:
            try:
                message = await self.message_queue.get()
                await self._handle_message(message)
                self.message_queue.task_done()
            except Exception as e:
                logger.error(f"Erro no processamento de mensagem: {e}")

    async def _handle_message(self, message: DistributedMessage):
        """Processa uma mensagem recebida"""
        self.metrics['messages_received'] += 1
        
        try:
            if message.type == MessageType.HEARTBEAT:
                await self._handle_heartbeat(message)
            elif message.type == MessageType.DATA_SYNC:
                await self._handle_data_sync(message)
            elif message.type == MessageType.CONSENSUS:
                await self._handle_consensus(message)
            elif message.type == MessageType.LEADER_ELECTION:
                await self._handle_leader_election(message)
            elif message.type == MessageType.GOSSIP:
                await self._handle_gossip(message)
            else:
                logger.warning(f"Tipo de mensagem não reconhecido: {message.type}")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem {message.id}: {e}")
            self.metrics['failed_operations'] += 1

    async def _handle_heartbeat(self, message: DistributedMessage):
        """Processa mensagem de heartbeat"""
        node_id = message.payload['node_id']
        
        with self._lock:
            if node_id in self.nodes:
                self.nodes[node_id].last_heartbeat = datetime.now()
                self.nodes[node_id].load = message.payload['load']
                self.nodes[node_id].status = NodeStatus(message.payload['status'])
            else:
                # Novo nó descoberto
                new_node = Node(
                    id=node_id,
                    address=message.payload.get('address', 'unknown'),
                    port=message.payload.get('port', 0),
                    status=NodeStatus(message.payload['status']),
                    last_heartbeat=datetime.now(),
                    load=message.payload['load']
                )
                self.nodes[node_id] = new_node
                logger.info(f"Novo nó descoberto: {node_id}")

    async def _handle_leader_election(self, message: DistributedMessage):
        """Processa mensagens de eleição de líder"""
        if message.payload['type'] == 'election':
            # Recebeu pedido de eleição
            if (self.voted_for is None or 
                message.payload['term'] > self.term):
                
                self.term = message.payload['term']
                self.voted_for = message.source
                
                # Enviar voto
                vote_msg = DistributedMessage(
                    id=str(uuid.uuid4()),
                    type=MessageType.LEADER_ELECTION,
                    source=self.node_id,
                    destination=message.source,
                    payload={
                        'type': 'vote',
                        'term': self.term,
                        'voter_id': self.node_id
                    }
                )
                await self._send_message(vote_msg)
                
        elif message.payload['type'] == 'victory':
            # Novo líder eleito
            self.leader_id = message.source
            self.term = message.payload['term']
            logger.info(f"Novo líder eleito: {self.leader_id}")

    async def _start_election(self):
        """Inicia uma eleição de líder"""
        with self._lock:
            self.term += 1
            self.voted_for = self.node_id
        
        election_msg = DistributedMessage(
            id=str(uuid.uuid4()),
            type=MessageType.LEADER_ELECTION,
            source=self.node_id,
            destination="broadcast",
            payload={
                'type': 'election',
                'term': self.term,
                'candidate_id': self.node_id
            }
        )
        
        votes_received = 1  # Vota em si mesmo
        votes_needed = (len(self.nodes) // 2) + 1
        
        # Enviar pedidos de votação
        await self._broadcast_message(election_msg)
        
        # Aguardar votos (simulação simplificada)
        await asyncio.sleep(0.1)
        
        if votes_received >= votes_needed:
            # Tornar-se líder
            self.leader_id = self.node_id
            victory_msg = DistributedMessage(
                id=str(uuid.uuid4()),
                type=MessageType.LEADER_ELECTION,
                source=self.node_id,
                destination="broadcast",
                payload={
                    'type': 'victory',
                    'term': self.term,
                    'leader_id': self.node_id
                }
            )
            await self._broadcast_message(victory_msg)
            logger.info(f"Eleito como líder para o termo {self.term}")

    async def _check_inactive_nodes(self):
        """Verifica e remove nós inativos"""
        current_time = datetime.now()
        inactive_threshold = timedelta(seconds=self.heartbeat_interval * 3)
        
        with self._lock:
            nodes_to_remove = []
            for node_id, node in self.nodes.items():
                if (node.last_heartbeat and 
                    current_time - node.last_heartbeat > inactive_threshold and
                    node_id != self.node_id):
                    
                    node.status = NodeStatus.OFFLINE
                    nodes_to_remove.append(node_id)
                    logger.warning(f"Nó {node_id} marcado como inativo")
            
            # Se o líder está inativo, iniciar nova eleição
            if self.leader_id in nodes_to_remove:
                logger.warning(f"Líder {self.leader_id} está inativo. Iniciando nova eleição...")
                self.leader_id = None
                await self._start_election()

    async def store_data(self, key: str, value: Any, consistency: ConsistencyLevel = ConsistencyLevel.EVENTUAL) -> bool:
        """
        Armazena dados no sistema distribuído
        """
        try:
            # Serializar e comprimir dados
            serialized_data = pickle.dumps(value)
            compressed_data = zlib.compress(serialized_data)
            
            # Determinar partição
            partition_id = self._get_partition_for_key(key)
            
            if consistency == ConsistencyLevel.STRONG:
                # Consenso forte - requer quorum
                result = await self._strong_consensus_operation(
                    operation='store',
                    key=key,
                    value=compressed_data,
                    partition_id=partition_id
                )
                return result.success
            else:
                # Consenso eventual - replica para nós da partição
                partition = self.partitions[partition_id]
                success_count = 0
                
                for node_id in partition.nodes:
                    if node_id in self.nodes and self.nodes[node_id].status == NodeStatus.ONLINE:
                        store_msg = DistributedMessage(
                            id=str(uuid.uuid4()),
                            type=MessageType.DATA_SYNC,
                            source=self.node_id,
                            destination=node_id,
                            payload={
                                'operation': 'store',
                                'key': key,
                                'value': compressed_data,
                                'partition': partition_id
                            }
                        )
                        await self._send_message(store_msg)
                        success_count += 1
                
                return success_count >= self.quorum_size
                
        except Exception as e:
            logger.error(f"Erro ao armazenar dados para chave {key}: {e}")
            return False

    async def retrieve_data(self, key: str, consistency: ConsistencyLevel = ConsistencyLevel.EVENTUAL) -> Optional[Any]:
        """
        Recupera dados do sistema distribuído
        """
        try:
            partition_id = self._get_partition_for_key(key)
            partition = self.partitions[partition_id]
            
            if consistency == ConsistencyLevel.STRONG:
                # Ler do líder ou com quorum
                if self.leader_id and self.leader_id in partition.nodes:
                    # Tentar ler do líder primeiro
                    leader_data = await self._retrieve_from_node(key, self.leader_id)
                    if leader_data is not None:
                        return self._decompress_data(leader_data)
                
                # Ler com quorum
                results = []
                for node_id in partition.nodes[:self.quorum_size]:
                    if node_id in self.nodes and self.nodes[node_id].status == NodeStatus.ONLINE:
                        data = await self._retrieve_from_node(key, node_id)
                        if data is not None:
                            results.append(data)
                
                if results:
                    # Retornar o valor mais recente (simplificado)
                    return self._decompress_data(results[0])
                    
            else:
                # Ler de qualquer nó disponível
                for node_id in partition.nodes:
                    if node_id in self.nodes and self.nodes[node_id].status == NodeStatus.ONLINE:
                        data = await self._retrieve_from_node(key, node_id)
                        if data is not None:
                            return self._decompress_data(data)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao recuperar dados para chave {key}: {e}")
            return None

    async def _retrieve_from_node(self, key: str, node_id: str) -> Optional[bytes]:
        """Recupera dados de um nó específico"""
        # Em implementação real, enviaria mensagem RPC
        # Aqui simulamos acessando o data_store local
        if node_id == self.node_id:
            return self.data_store.get(key)
        
        # Para outros nós, enviaríamos mensagem de consulta
        query_msg = DistributedMessage(
            id=str(uuid.uuid4()),
            type=MessageType.QUERY,
            source=self.node_id,
            destination=node_id,
            payload={'key': key, 'operation': 'retrieve'}
        )
        
        # Simulação - em implementação real aguardaria resposta
        return None

    def _get_partition_for_key(self, key: str) -> str:
        """Determina a partição para uma chave usando hashing consistente"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        partition_keys = sorted(self.partitions.keys())
        
        if not partition_keys:
            # Criar partição padrão se não existir
            default_partition = Partition(
                id="default",
                name="Default Partition",
                nodes=[self.node_id],
                replication_factor=self.replication_factor
            )
            self.partitions["default"] = default_partition
            return "default"
        
        # Encontrar a partição apropriada
        for partition_id in partition_keys:
            if key_hash <= partition_id:
                return partition_id
        
        # Circular - retornar a primeira partição
        return partition_keys[0]

    async def _strong_consensus_operation(self, operation: str, **kwargs) -> ConsensusResult:
        """
        Executa operação com consenso forte (Paxos simplificado)
        """
        async with self._consensus_lock:
            proposal_id = f"{self.node_id}-{int(time.time() * 1000)}"
            participants = list(self.nodes.keys())[:self.quorum_size]
            
            # Fase 1: Prepare
            prepare_responses = []
            for node_id in participants:
                if node_id != self.node_id and self.nodes[node_id].status == NodeStatus.ONLINE:
                    prepare_msg = DistributedMessage(
                        id=str(uuid.uuid4()),
                        type=MessageType.CONSENSUS,
                        source=self.node_id,
                        destination=node_id,
                        payload={
                            'phase': 'prepare',
                            'proposal_id': proposal_id,
                            'operation': operation,
                            **kwargs
                        }
                    )
                    # Simular resposta (em implementação real aguardaria resposta)
                    prepare_responses.append(True)
            
            # Fase 2: Accept
            if len(prepare_responses) >= (self.quorum_size - 1):
                accept_responses = []
                for node_id in participants:
                    if node_id != self.node_id and self.nodes[node_id].status == NodeStatus.ONLINE:
                        accept_msg = DistributedMessage(
                            id=str(uuid.uuid4()),
                            type=MessageType.CONSENSUS,
                            source=self.node_id,
                            destination=node_id,
                            payload={
                                'phase': 'accept',
                                'proposal_id': proposal_id,
                                'operation': operation,
                                **kwargs
                            }
                        )
                        # Simular resposta
                        accept_responses.append(True)
                
                if len(accept_responses) >= (self.quorum_size - 1):
                    self.metrics['consensus_operations'] += 1
                    return ConsensusResult(
                        success=True,
                        value=None,
                        quorum_size=self.quorum_size,
                        participants=participants,
                        timestamp=datetime.now()
                    )
            
            return ConsensusResult(
                success=False,
                value=None,
                quorum_size=self.quorum_size,
                participants=participants,
                timestamp=datetime.now()
            )

    async def _broadcast_message(self, message: DistributedMessage):
        """Transmite mensagem para todos os nós"""
        for node_id, node in self.nodes.items():
            if node_id != self.node_id and node.status == NodeStatus.ONLINE:
                message.destination = node_id
                await self._send_message(message)

    async def _send_message(self, message: DistributedMessage):
        """Envia mensagem para um nó específico"""
        try:
            # Em implementação real, usaria WebSocket ou HTTP
            # Aqui simulamos adicionando à fila do nó destino
            if message.destination in self.nodes:
                # Simular latência de rede
                await asyncio.sleep(random.uniform(0.001, 0.01))
                self.metrics['messages_sent'] += 1
                
                # Atualizar métricas de latência
                latency = (datetime.now() - message.timestamp).total_seconds()
                self.metrics['average_latency'] = (
                    self.metrics['average_latency'] * 0.9 + latency * 0.1
                )
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem {message.id}: {e}")

    async def _gossip_loop(self):
        """Loop para disseminação de estado via gossip"""
        while True:
            try:
                await asyncio.sleep(10)  # A cada 10 segundos
                
                if not self.gossip_peers:
                    continue
                
                # Selecionar peer aleatório para gossip
                peer_id = random.choice(self.gossip_peers)
                if peer_id in self.nodes and self.nodes[peer_id].status == NodeStatus.ONLINE:
                    
                    gossip_msg = DistributedMessage(
                        id=str(uuid.uuid4()),
                        type=MessageType.GOSSIP,
                        source=self.node_id,
                        destination=peer_id,
                        payload={
                            'state': self.gossip_state,
                            'timestamp': datetime.now().isoformat()
                        }
                    )
                    
                    await self._send_message(gossip_msg)
                    
            except Exception as e:
                logger.error(f"Erro no gossip loop: {e}")

    async def _handle_gossip(self, message: DistributedMessage):
        """Processa mensagem de gossip"""
        try:
            received_state = message.payload['state']
            received_timestamp = datetime.fromisoformat(message.payload['timestamp'])
            
            # Mesclar estados (usando timestamp mais recente)
            for key, (value, timestamp) in received_state.items():
                current_timestamp = self.gossip_state.get(key, (None, datetime.min))[1]
                if timestamp > current_timestamp:
                    self.gossip_state[key] = (value, timestamp)
                    
        except Exception as e:
            logger.error(f"Erro ao processar gossip: {e}")

    async def _cache_cleanup_loop(self):
        """Limpa cache expirado periodicamente"""
        while True:
            try:
                await asyncio.sleep(60)  # A cada minuto
                
                current_time = datetime.now()
                expired_keys = [
                    key for key, expiry in self.cache_ttl.items()
                    if expiry < current_time
                ]
                
                for key in expired_keys:
                    del self.cache[key]
                    del self.cache_ttl[key]
                    
            except Exception as e:
                logger.error(f"Erro na limpeza de cache: {e}")

    async def _monitoring_loop(self):
        """Loop de monitoramento e coleta de métricas"""
        while True:
            try:
                await asyncio.sleep(30)  # A cada 30 segundos
                
                # Coletar métricas do sistema
                system_metrics = {
                    'total_nodes': len(self.nodes),
                    'online_nodes': sum(1 for n in self.nodes.values() 
                                      if n.status == NodeStatus.ONLINE),
                    'system_load': self._calculate_system_load(),
                    'message_throughput': self.metrics['messages_sent'] / 30,  # mensagens/segundo
                    'consensus_success_rate': (
                        self.metrics['consensus_operations'] / 
                        (self.metrics['consensus_operations'] + self.metrics['failed_operations'] + 1)
                    )
                }
                
                # Atualizar estado de gossip com métricas
                self.gossip_state['system_metrics'] = (system_metrics, datetime.now())
                
                logger.info(f"Métricas do sistema: {system_metrics}")
                
            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")

    def _calculate_current_load(self) -> float:
        """Calcula carga atual do nó"""
        # Simulação - em implementação real usaria métricas reais
        return random.uniform(0.0, 1.0)

    def _calculate_system_load(self) -> float:
        """Calcula carga média do sistema"""
        if not self.nodes:
            return 0.0
        return sum(node.load for node in self.nodes.values()) / len(self.nodes)

    def _decompress_data(self, compressed_data: bytes) -> Any:
        """Descomprime e desserializa dados"""
        try:
            decompressed = zlib.decompress(compressed_data)
            return pickle.loads(decompressed)
        except Exception as e:
            logger.error(f"Erro ao descomprimir dados: {e}")
            return None

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        with self._lock:
            return {
                'node_id': self.node_id,
                'leader_id': self.leader_id,
                'term': self.term,
                'total_nodes': len(self.nodes),
                'online_nodes': [n.id for n in self.nodes.values() 
                               if n.status == NodeStatus.ONLINE],
                'partitions': {pid: len(p.nodes) for pid, p in self.partitions.items()},
                'metrics': self.metrics.copy(),
                'system_load': self._calculate_system_load()
            }

    async def shutdown(self):
        """Desliga o sistema distribuído graciosamente"""
        logger.info("Iniciando desligamento gracioso...")
        
        # Cancelar tarefas em background
        for task in self.background_tasks:
            task.cancel()
        
        # Aguardar conclusão das tarefas
        await asyncio.gather(*self.background_tasks, return_exceptions=True)
        
        # Fechar thread pool
        self.thread_pool.shutdown(wait=True)
        
        logger.info("Sistema distribuído desligado com sucesso")

# Exemplo de uso
async def demo_advanced_distributed_system():
    """Demonstração do sistema distribuído avançado"""
    
    # Criar sistema
    system = AdvancedDistributedSystem(host="localhost", port=8000)
    
    try:
        # Inicializar
        await system.initialize(bootstrap_nodes=["localhost:8001", "localhost:8002"])
        
        # Aguardar estabilização
        await asyncio.sleep(2)
        
        # Armazenar alguns dados
        print("Armazenando dados no sistema distribuído...")
        
        success = await system.store_data(
            key="user:123",
            value={"name": "João Silva", "email": "joao@email.com", "age": 30},
            consistency=ConsistencyLevel.EVENTUAL
        )
        
        print(f"Dados armazenados: {success}")
        
        # Recuperar dados
        print("Recuperando dados...")
        retrieved_data = await system.retrieve_data("user:123")
        print(f"Dados recuperados: {retrieved_data}")
        
        # Mostrar status do sistema
        status = system.get_system_status()
        print(f"Status do sistema: {json.dumps(status, indent=2, default=str)}")
        
        # Manter sistema rodando por um tempo
        await asyncio.sleep(10)
        
    finally:
        # Desligar graciosamente
        await system.shutdown()

if __name__ == "__main__":
    # Executar demonstração
    asyncio.run(demo_advanced_distributed_system())