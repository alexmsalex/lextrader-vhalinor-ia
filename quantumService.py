import numpy as np
import random
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from collections import defaultdict, deque
import math
import asyncio
import json

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enums e Tipos
class LayerType(Enum):
    # Classical Layers
    DENSE_RELU = "DENSE_RELU"
    CONV1D_FEATURE = "CONV1D_FEATURE"
    LSTM_TEMPORAL = "LSTM_TEMPORAL"
    DROPOUT_STOCHASTIC = "DROPOUT_STOCHASTIC"
    
    # Quantum Layers
    QUANTUM_SUPERPOSITION = "QUANTUM_SUPERPOSITION"
    QUANTUM_ENTANGLEMENT = "QUANTUM_ENTANGLEMENT"
    QUANTUM_INTERFERENCE = "QUANTUM_INTERFERENCE"
    QUANTUM_MEASUREMENT = "QUANTUM_MEASUREMENT"
    
    # Hybrid Layers
    HOLOGRAPHIC_FUSION = "HOLOGRAPHIC_FUSION"
    ASI_CONSCIOUSNESS_FIELD = "ASI_CONSCIOUSNESS_FIELD"

class LogicType(Enum):
    CLASSICAL = "CLASSICAL"
    QUANTUM = "QUANTUM"
    HYBRID = "HYBRID"

class TimeHorizon(Enum):
    SCALP_IMEDIATO = "SCALP_IMEDIATO"
    INTRADAY_SWING = "INTRADAY_SWING"
    WAIT_AND_SEE = "WAIT_AND_SEE"
    SHORT_TERM = "SHORT_TERM"
    MEDIUM_TERM = "MEDIUM_TERM"
    LONG_TERM = "LONG_TERM"

# Estruturas de dados
@dataclass
class NeuralLayer:
    id: str
    type: LayerType
    nodes: int  # Neurons or Qubits
    activation: np.ndarray  # Current state
    weights: np.ndarray  # Synaptic connections
    bias: np.ndarray
    parameters: Dict[str, Any]
    gradients: Optional[np.ndarray] = None
    memory_cell: Optional[np.ndarray] = None  # For LSTM
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = LayerType(self.type)
        
        # Garantir que arrays sejam numpy arrays
        if isinstance(self.activation, list):
            self.activation = np.array(self.activation)
        if isinstance(self.weights, list):
            self.weights = np.array(self.weights)
        if isinstance(self.bias, list):
            self.bias = np.array(self.bias)

@dataclass
class LayerState:
    id: str
    activity: float
    coherence: float = 0.0
    entropy: float = 0.0

@dataclass
class NeuralState:
    coherence: float  # 0-1 Quantum Coherence
    plasticity: float  # 0-1 Synaptic Adaptability
    entropy: float  # System Uncertainty
    active_pathways: List[str]  # Active concepts
    layer_states: List[LayerState]
    evolution_epoch: int = 0
    last_update: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'coherence': self.coherence,
            'plasticity': self.plasticity,
            'entropy': self.entropy,
            'active_pathways': self.active_pathways,
            'layer_states': [{'id': ls.id, 'activity': ls.activity, 
                              'coherence': ls.coherence, 'entropy': ls.entropy} 
                            for ls in self.layer_states],
            'evolution_epoch': self.evolution_epoch,
            'last_update': self.last_update.isoformat()
        }

@dataclass
class PredictionOutput:
    prediction: float  # 0-1 Normalized Prediction
    confidence: float
    time_horizon: TimeHorizon
    dominant_logic: LogicType
    vector: np.ndarray  # Feature vector
    quantum_coherence: float = 0.0
    classical_confidence: float = 0.0
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'prediction': self.prediction,
            'confidence': self.confidence,
            'time_horizon': self.time_horizon.value,
            'dominant_logic': self.dominant_logic.value,
            'vector': self.vector.tolist(),
            'quantum_coherence': self.quantum_coherence,
            'classical_confidence': self.classical_confidence,
            'processing_time': self.processing_time
        }

@dataclass
class TrainingConfig:
    learning_rate: float = 0.001
    mutation_rate: float = 0.01
    plasticity_threshold: float = 0.6
    coherence_threshold: float = 0.9
    neurogenesis_probability: float = 0.1
    dropout_rate: float = 0.2
    batch_size: int = 32

# Operações matemáticas
class MathOps:
    """Operações matemáticas para processamento neural"""
    
    @staticmethod
    def sigmoid(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        return 1 / (1 + np.exp(-x))
    
    @staticmethod
    def tanh(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        return np.tanh(x)
    
    @staticmethod
    def relu(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        return np.maximum(0, x)
    
    @staticmethod
    def leaky_relu(x: Union[float, np.ndarray], alpha: float = 0.01) -> Union[float, np.ndarray]:
        return np.where(x > 0, x, alpha * x)
    
    @staticmethod
    def softmax(x: np.ndarray) -> np.ndarray:
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()
    
    @staticmethod
    def dot(vec: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """Multiplicação matriz-vetor"""
        if weights.size == 0:
            return vec
        return np.dot(weights, vec)
    
    @staticmethod
    def quantum_rotate(state: float, theta: float) -> float:
        """Simulação de rotação quântica (porta Ry)"""
        amplitude = math.cos(theta/2) * math.sqrt(state) + math.sin(theta/2) * math.sqrt(1-state)
        return amplitude ** 2
    
    @staticmethod
    def hadamard_transform(state: np.ndarray) -> np.ndarray:
        """Transformada de Hadamard para superposição quântica"""
        n = len(state)
        H = 1/math.sqrt(2) * np.array([[1, 1], [1, -1]])
        # Aplicar para cada qubit (simplificado)
        return np.array([(state[i] + state[(i+1)%n])/math.sqrt(2) for i in range(n)])
    
    @staticmethod
    def cnot_gate(control: float, target: float) -> Tuple[float, float]:
        """Porta CNOT quântica"""
        if control > 0.5:  # Se control está no estado |1>
            target = 1 - target  # Inverte o target
        return control, target
    
    @staticmethod
    def quantum_interference(state: np.ndarray) -> np.ndarray:
        """Interferência quântica construtiva/destrutiva"""
        n = len(state)
        interfered = np.zeros(n)
        
        for i in range(n):
            # Soma de ondas com diferentes fases
            phase_sum = 0
            for j in range(n):
                phase = (state[j] * 2 * math.pi * (i - j)) / n
                phase_sum += math.cos(phase)
            interfered[i] = (phase_sum / n + 1) / 2  # Normalizar para 0-1
        
        return interfered
    
    @staticmethod
    def xavier_init(n_input: int, n_output: int) -> np.ndarray:
        """Inicialização Xavier para pesos"""
        limit = math.sqrt(6 / (n_input + n_output))
        return np.random.uniform(-limit, limit, (n_output, n_input))

# Classe principal
class QuantumNeuralNetwork:
    """Arquitetura Híbrida Neural-Quântica LEXTRADER-IAG v4.0 Omega"""
    
    def __init__(self, config: Optional[TrainingConfig] = None):
        self.layers: List[NeuralLayer] = []
        self.memory_cell: np.ndarray = np.array([])  # Estado da célula LSTM
        self.evolution_epoch: int = 0
        self.config = config or TrainingConfig()
        
        # Estado do sistema
        self.state = NeuralState(
            coherence=1.0,
            plasticity=0.5,
            entropy=0.0,
            active_pathways=[],
            layer_states=[],
            evolution_epoch=0
        )
        
        # Histórico
        self.training_history: List[Dict[str, Any]] = []
        self.prediction_history: List[PredictionOutput] = []
        
        # Inicializar arquitetura
        self._initialize_architecture()
        
        logger.info("🧠 LEXTRADER-IAG: Arquitetura Híbrida inicializada")
    
    async def initialize(self):
        """Inicialização assíncrona completa"""
        logger.info("🧠 LEXTRADER-IAG: Inicializando Arquitetura Híbrida...")
        await self._initialize_architecture_async()
        logger.info("✅ Redes Neurais Gerais e Quânticas Sincronizadas.")
        
        # Pré-aquecimento
        await self._warmup()
        
        return self
    
    async def _initialize_architecture_async(self):
        """Inicialização assíncrona da arquitetura"""
        # Simular algum processamento assíncrono
        await asyncio.sleep(0.1)
        self._initialize_architecture()
    
    def _initialize_architecture(self):
        """Inicializa a arquitetura híbrida"""
        self.layers = []
        
        # 1. PROCESSAMENTO DE ENTRADA (CLÁSSICO)
        # CNN para reconhecimento de padrões locais (micro-estrutura)
        self._add_layer('L1_CNN_Visual', LayerType.CONV1D_FEATURE, 64, {'kernel': 3, 'stride': 1})
        
        # 2. MEMÓRIA TEMPORAL (CLÁSSICO)
        # LSTM para contexto de série temporal
        self._add_layer('L2_LSTM_Memory', LayerType.LSTM_TEMPORAL, 32, {'lookback': 10, 'return_sequences': False})
        
        # 3. CODIFICAÇÃO QUÂNTICA
        # Mapeando características clássicas para estado quântico
        self._add_layer('Q1_Superposition', LayerType.QUANTUM_SUPERPOSITION, 32, 
                       {'encoding': 'amplitude', 'num_qubits': 5})
        
        # 4. PROCESSAMENTO QUÂNTICO
        # Entrelaçamento de qubits para encontrar correlações não-locais
        self._add_layer('Q2_Entanglement', LayerType.QUANTUM_ENTANGLEMENT, 32, 
                       {'topology': 'all-to-all', 'entanglement_depth': 2})
        
        self._add_layer('Q3_Interference', LayerType.QUANTUM_INTERFERENCE, 16, 
                       {'interference_type': 'constructive_destructive'})
        
        # 5. FUSÃO HÍBRIDA
        # Fusão da Lógica Clássica com Intuição Quântica
        self._add_layer('H1_Holographic', LayerType.HOLOGRAPHIC_FUSION, 64, 
                       {'integration_rate': 0.7, 'fusion_method': 'non_linear'})
        
        # 6. RACIOCÍNIO PROFUNDO (CLÁSSICO)
        self._add_layer('L3_Dense_Reasoning', LayerType.DENSE_RELU, 128, 
                       {'activation': 'relu', 'dropout': self.config.dropout_rate})
        
        # 7. CAMPO DE CONSCIÊNCIA (ASI)
        # Moldagem da decisão final baseada em restrições éticas/de risco
        self._add_layer('ASI_Core', LayerType.ASI_CONSCIOUSNESS_FIELD, 1, 
                       {'risk_tolerance': 0.3, 'certainty_amplifier': 1.1})
        
        # Inicializar pesos
        self._initialize_weights()
        
        # Inicializar célula de memória LSTM
        self.memory_cell = np.zeros(32)
        
        logger.info(f"📐 Arquitetura inicializada com {len(self.layers)} camadas")
    
    def _add_layer(self, layer_id: str, layer_type: LayerType, nodes: int, params: Dict[str, Any]):
        """Adiciona uma camada à rede"""
        layer = NeuralLayer(
            id=layer_id,
            type=layer_type,
            nodes=nodes,
            activation=np.zeros(nodes),
            weights=np.array([]),  # Será inicializado depois
            bias=np.full(nodes, 0.01),
            parameters=params
        )
        
        # Adicionar célula de memória para LSTM
        if layer_type == LayerType.LSTM_TEMPORAL:
            layer.memory_cell = np.zeros(nodes)
        
        self.layers.append(layer)
    
    def _initialize_weights(self):
        """Inicializa pesos para todas as camadas"""
        for i, layer in enumerate(self.layers):
            prev_nodes = 4 if i == 0 else self.layers[i-1].nodes
            
            # Inicialização baseada no tipo de camada
            if layer.type in [LayerType.DENSE_RELU, LayerType.CONV1D_FEATURE, 
                            LayerType.HOLOGRAPHIC_FUSION, LayerType.ASI_CONSCIOUSNESS_FIELD]:
                # Inicialização Xavier
                layer.weights = MathOps.xavier_init(prev_nodes, layer.nodes)
            
            elif layer.type == LayerType.LSTM_TEMPORAL:
                # Pesos para LSTM (simplificado)
                layer.weights = np.random.randn(layer.nodes, prev_nodes) * 0.1
            
            elif layer.type in [LayerType.QUANTUM_SUPERPOSITION, LayerType.QUANTUM_ENTANGLEMENT,
                               LayerType.QUANTUM_INTERFERENCE]:
                # Pesos quânticos (matrizes unitárias)
                layer.weights = np.random.randn(layer.nodes, prev_nodes) * 0.05
                
                # Garantir que a matriz seja aproximadamente unitária
                if layer.nodes == prev_nodes:
                    U, _, V = np.linalg.svd(layer.weights)
                    layer.weights = U @ V
            
            # Inicializar bias com pequenos valores
            layer.bias = np.random.randn(layer.nodes) * 0.01
    
    # --- PASSAGEM PARA FRENTE (INFERÊNCIA) ---
    
    async def predict(self, features: np.ndarray) -> PredictionOutput:
        """Executa predição através da rede"""
        start_time = datetime.now()
        
        try:
            # 1. Normalizar entrada
            signal = np.array(features, dtype=np.float32)
            signal = MathOps.tanh(signal)
            
            quantum_signal = np.array([])
            classical_signal = np.array([])
            
            # 2. Processar através de todas as camadas
            for layer in self.layers:
                # Processamento baseado no tipo de camada
                if self._is_classical(layer.type):
                    signal = self._process_classical(layer, signal)
                    if layer.id == 'L2_LSTM_Memory':
                        classical_signal = signal.copy()
                
                elif self._is_quantum(layer.type):
                    # Se entrando no domínio quântico, codificar sinal clássico
                    if layer.type == LayerType.QUANTUM_SUPERPOSITION:
                        # Codificação: Amplitude Clássica -> Probabilidade Quântica
                        signal = signal[:layer.nodes]
                        signal = np.array([(math.sin(v * math.pi) + 1) / 2 for v in signal])
                    
                    signal = self._process_quantum(layer, signal)
                    
                    if layer.type == LayerType.QUANTUM_INTERFERENCE:
                        quantum_signal = signal.copy()
                
                elif layer.type == LayerType.HOLOGRAPHIC_FUSION:
                    # FUSÃO DE SINAIS
                    signal = self._process_fusion(layer, classical_signal, quantum_signal)
                
                elif layer.type == LayerType.ASI_CONSCIOUSNESS_FIELD:
                    signal = self._process_asi(layer, signal)
                
                # Atualizar ativação da camada para visualização
                layer.activation = signal.copy()
            
            # 3. Calcular métricas
            output = float(signal[0]) if signal.size > 0 else 0.5
            
            quantum_coherence = 0.0
            if quantum_signal.size > 0:
                quantum_coherence = float(np.mean(np.abs(quantum_signal)))
            
            classical_confidence = abs(output - 0.5) * 2
            
            # 4. Atualizar estado do sistema
            self._update_system_state(quantum_coherence, classical_confidence)
            
            # 5. Determinar horizonte de tempo e lógica dominante
            time_horizon = self._determine_time_horizon(output, quantum_coherence)
            dominant_logic = self._determine_dominant_logic(quantum_coherence, classical_confidence)
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Criar resultado
            result = PredictionOutput(
                prediction=output,
                confidence=(classical_confidence + quantum_coherence) / 2,
                time_horizon=time_horizon,
                dominant_logic=dominant_logic,
                vector=signal,
                quantum_coherence=quantum_coherence,
                classical_confidence=classical_confidence,
                processing_time=processing_time
            )
            
            # Adicionar ao histórico
            self.prediction_history.append(result)
            if len(self.prediction_history) > 1000:
                self.prediction_history.pop(0)
            
            logger.debug(f"📊 Predição: {output:.3f} | Confiança: {result.confidence:.3f} | "
                        f"Lógica: {dominant_logic.value} | Tempo: {processing_time:.1f}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na predição: {e}")
            # Retornar resultado neutro em caso de erro
            return PredictionOutput(
                prediction=0.5,
                confidence=0.0,
                time_horizon=TimeHorizon.WAIT_AND_SEE,
                dominant_logic=LogicType.CLASSICAL,
                vector=np.array([0.5]),
                quantum_coherence=0.0,
                classical_confidence=0.0,
                processing_time=0.0
            )
    
    # --- PROCESSADORES DE CAMADAS ---
    
    def _is_classical(self, layer_type: LayerType) -> bool:
        """Verifica se a camada é clássica"""
        classical_types = {
            LayerType.DENSE_RELU,
            LayerType.CONV1D_FEATURE,
            LayerType.LSTM_TEMPORAL,
            LayerType.DROPOUT_STOCHASTIC
        }
        return layer_type in classical_types
    
    def _is_quantum(self, layer_type: LayerType) -> bool:
        """Verifica se a camada é quântica"""
        return layer_type.value.startswith('QUANTUM')
    
    def _process_classical(self, layer: NeuralLayer, input_signal: np.ndarray) -> np.ndarray:
        """Processa camada clássica"""
        # Garantir tamanhos compatíveis
        if layer.weights.size == 0 or input_signal.size == 0:
            return input_signal
        
        # Aplicar dropout estocástico se necessário
        if layer.type == LayerType.DROPOUT_STOCHASTIC and self.config.dropout_rate > 0:
            mask = np.random.binomial(1, 1 - self.config.dropout_rate, size=input_signal.shape)
            input_signal = input_signal * mask / (1 - self.config.dropout_rate)
        
        # Calcular saída
        output = MathOps.dot(input_signal, layer.weights)
        output = output + layer.bias
        
        # Aplicar função de ativação
        if layer.type == LayerType.DENSE_RELU:
            return MathOps.relu(output)
        
        elif layer.type == LayerType.LSTM_TEMPORAL:
            # Lógica LSTM simplificada
            forget_gate = MathOps.sigmoid(output + 0.1)
            input_gate = MathOps.sigmoid(output)
            candidate = MathOps.tanh(output + 0.2)
            
            # Atualizar célula de memória
            layer.memory_cell = (layer.memory_cell * forget_gate) + (input_gate * candidate)
            
            # Porta de saída
            output_gate = MathOps.sigmoid(output + 0.3)
            return MathOps.tanh(layer.memory_cell) * output_gate
        
        elif layer.type == LayerType.CONV1D_FEATURE:
            # Convolução 1D simplificada
            kernel_size = layer.parameters.get('kernel', 3)
            stride = layer.parameters.get('stride', 1)
            
            # Convolução simples
            convolved = []
            for i in range(0, len(output) - kernel_size + 1, stride):
                convolved.append(np.mean(output[i:i+kernel_size]))
            
            return np.array(convolved) if convolved else output
        
        # Padrão: sigmoid
        return MathOps.sigmoid(output)
    
    def _process_quantum(self, layer: NeuralLayer, input_signal: np.ndarray) -> np.ndarray:
        """Processa camada quântica"""
        if input_signal.size == 0:
            return input_signal
        
        if layer.type == LayerType.QUANTUM_SUPERPOSITION:
            # Transformada de Hadamard para criar superposição
            return MathOps.hadamard_transform(input_signal)
        
        elif layer.type == LayerType.QUANTUM_ENTANGLEMENT:
            # Simular entrelaçamento: estados médios entre vizinhos
            n = len(input_signal)
            entangled = input_signal.copy()
            
            for i in range(n):
                neighbor1 = input_signal[(i + 1) % n]
                neighbor2 = input_signal[(i - 1) % n]
                
                # Estado de Bell simplificado
                entangled[i] = (input_signal[i] + neighbor1 + neighbor2) / 3
            
            return entangled
        
        elif layer.type == LayerType.QUANTUM_INTERFERENCE:
            # Interferência quântica
            return MathOps.quantum_interference(input_signal)
        
        elif layer.type == LayerType.QUANTUM_MEASUREMENT:
            # Medição quântica (colapso para estado clássico)
            return np.array([1.0 if x > 0.5 else 0.0 for x in input_signal])
        
        return input_signal
    
    def _process_fusion(self, layer: NeuralLayer, classical_signal: np.ndarray, 
                       quantum_signal: np.ndarray) -> np.ndarray:
        """Processa fusão holográfica"""
        if classical_signal.size == 0 or quantum_signal.size == 0:
            return classical_signal if classical_signal.size > 0 else quantum_signal
        
        size = layer.nodes
        fused = np.zeros(size)
        
        integration_rate = layer.parameters.get('integration_rate', 0.5)
        fusion_method = layer.parameters.get('fusion_method', 'non_linear')
        
        for i in range(size):
            c_val = classical_signal[i % len(classical_signal)]
            q_val = quantum_signal[i % len(quantum_signal)]
            
            if fusion_method == 'non_linear':
                # Fusão não-linear
                fused[i] = (c_val ** (1 - integration_rate)) * (q_val ** integration_rate)
            elif fusion_method == 'weighted':
                # Média ponderada
                fused[i] = (c_val * (1 - integration_rate)) + (q_val * integration_rate)
            else:
                # Padrão: média simples
                fused[i] = (c_val + q_val) / 2
        
        return fused
    
    def _process_asi(self, layer: NeuralLayer, input_signal: np.ndarray) -> np.ndarray:
        """Processa campo de consciência ASI"""
        if input_signal.size == 0:
            return input_signal
        
        output = input_signal.copy()
        risk_tolerance = layer.parameters.get('risk_tolerance', 0.3)
        certainty_amplifier = layer.parameters.get('certainty_amplifier', 1.1)
        
        for i in range(len(output)):
            val = output[i]
            
            # Amplificador de certeza: empurra sinais fracos para neutro ou fortes para extremos
            if val > 0.8 - risk_tolerance:
                output[i] = min(1.0, val * certainty_amplifier)  # Convicção alta
            elif val < 0.2 + risk_tolerance:
                output[i] = max(0.0, val * (2 - certainty_amplifier))  # Convicção baixa
            # Sinais intermediários: mantém incerteza
            
            # Aplicar tolerância ao risco
            if val > 0.5:
                output[i] = 0.5 + (val - 0.5) * (1 - risk_tolerance)
            else:
                output[i] = 0.5 - (0.5 - val) * (1 - risk_tolerance)
        
        return output
    
    # --- NEUROGÊNESE (NOVOS NEURÔNIOS) ---
    
    def neurogenesis(self, layer_id: str) -> bool:
        """Adiciona novos neurônios a uma camada (neurogênese)"""
        layer_idx = -1
        for i, layer in enumerate(self.layers):
            if layer.id == layer_id:
                layer_idx = i
                break
        
        if layer_idx == -1:
            logger.warning(f"Camada {layer_id} não encontrada para neurogênese")
            return False
        
        layer = self.layers[layer_idx]
        prev_layer = self.layers[layer_idx - 1] if layer_idx > 0 else None
        next_layer = self.layers[layer_idx + 1] if layer_idx < len(self.layers) - 1 else None
        
        logger.info(f"✨ Neurogênese: Adicionando neurônio à camada {layer.id}. "
                   f"Total: {layer.nodes + 1}")
        
        # 1. Aumentar contagem de nós
        layer.nodes += 1
        
        # 2. Adicionar bias e inicializar ativação
        new_bias = (random.random() - 0.5) * 0.05
        layer.bias = np.append(layer.bias, new_bias)
        layer.activation = np.append(layer.activation, 0)
        
        # 3. Adicionar pesos sinápticos da camada anterior
        input_size = prev_layer.nodes if prev_layer else 4  # entradas padrão
        
        # Expandir matriz de pesos
        if layer.weights.size == 0:
            layer.weights = np.random.randn(layer.nodes, input_size) * 0.1
        else:
            # Adicionar nova linha para o novo neurônio
            new_weights = np.random.randn(1, input_size) * 0.1
            layer.weights = np.vstack([layer.weights, new_weights])
        
        # 4. Atualizar pesos da próxima camada
        if next_layer and next_layer.weights.size > 0:
            # Adicionar nova coluna para conexão com o novo neurônio
            new_col_weights = np.random.randn(next_layer.nodes, 1) * 0.1
            next_layer.weights = np.hstack([next_layer.weights, new_col_weights])
        
        # 5. Atualizar célula de memória se for LSTM
        if layer.type == LayerType.LSTM_TEMPORAL and layer.memory_cell is not None:
            layer.memory_cell = np.append(layer.memory_cell, 0)
        
        logger.info(f"✅ Neurogênese concluída para {layer.id}. Novo tamanho: {layer.nodes}")
        return True
    
    # --- EVOLUÇÃO E APRENDIZADO ---
    
    def evolve(self):
        """Evolui a rede através de aprendizado e neuroplasticidade"""
        self.evolution_epoch += 1
        
        # 1. Ajuste de pesos sinápticos (aprendizado)
        mutation_rate = self.config.mutation_rate
        
        for layer in self.layers:
            if layer.weights.size > 0:
                # Mutação de pesos
                mutation = np.random.randn(*layer.weights.shape) * mutation_rate
                layer.weights += mutation
                
                # Atualizar bias
                if layer.bias.size > 0:
                    bias_mutation = np.random.randn(*layer.bias.shape) * mutation_rate * 0.1
                    layer.bias += bias_mutation
        
        # 2. Neuroplasticidade estrutural (crescimento)
        if self.state.plasticity > self.config.plasticity_threshold:
            # Chance de neurogênese baseada na plasticidade
            neurogenesis_prob = self.config.neurogenesis_probability * self.state.plasticity
            
            if random.random() < neurogenesis_prob:
                # Escolher camada para neurogênese
                candidate_layers = ['L3_Dense_Reasoning', 'H1_Holographic']
                selected_layer = random.choice(candidate_layers)
                self.neurogenesis(selected_layer)
        
        # 3. Expansão quântica
        if self.state.coherence > self.config.coherence_threshold:
            quantum_expansion_prob = 0.05 * self.state.coherence
            
            if random.random() < quantum_expansion_prob:
                self.neurogenesis('Q2_Entanglement')
        
        # 4. Atualizar estado do sistema
        self.state.plasticity = min(1.0, self.state.plasticity + 0.01)
        self.state.entropy = max(0.0, self.state.entropy - 0.005)
        self.state.evolution_epoch = self.evolution_epoch
        self.state.last_update = datetime.now()
        
        logger.debug(f"🔄 Evolução concluída. Época: {self.evolution_epoch} | "
                    f"Plasticidade: {self.state.plasticity:.3f}")
    
    async def train_online(self, features: List[float], target: float):
        """Treinamento online com uma amostra"""
        try:
            # Converter para numpy array
            features_array = np.array(features)
            
            # Fazer predição
            prediction = await self.predict(features_array)
            
            # Calcular erro
            error = target - prediction.prediction
            
            # Backpropagation simplificada
            learning_rate = self.config.learning_rate
            
            # Ajustar pesos da última camada (simplificado)
            if self.layers:
                last_layer = self.layers[-1]
                if last_layer.weights.size > 0 and features_array.size > 0:
                    # Gradiente simples
                    gradient = error * features_array[:last_layer.weights.shape[1]]
                    
                    # Atualizar pesos
                    last_layer.weights += learning_rate * np.outer(np.ones(last_layer.nodes), gradient)
                    
                    # Atualizar bias
                    last_layer.bias += learning_rate * error
            
            # Evoluir a rede
            self.evolve()
            
            # Registrar treinamento
            self.training_history.append({
                'timestamp': datetime.now().isoformat(),
                'features': features,
                'target': target,
                'prediction': prediction.prediction,
                'error': error,
                'epoch': self.evolution_epoch
            })
            
            if len(self.training_history) > 1000:
                self.training_history.pop(0)
            
            logger.debug(f"📚 Treinamento online: Erro={error:.4f} | "
                        f"Época={self.evolution_epoch}")
            
        except Exception as e:
            logger.error(f"❌ Erro no treinamento online: {e}")
    
    # --- UTILIDADES ---
    
    def _update_system_state(self, quantum_coherence: float, classical_confidence: float):
        """Atualiza o estado do sistema"""
        self.state.coherence = quantum_coherence
        self.state.entropy = 1 - classical_confidence
        
        # Atualizar estados das camadas
        self.state.layer_states = []
        for layer in self.layers:
            if layer.activation.size > 0:
                activity = float(np.mean(np.abs(layer.activation)))
                
                # Calcular coerência e entropia específicas da camada
                layer_coherence = 0.0
                layer_entropy = 0.0
                
                if self._is_quantum(layer.type):
                    layer_coherence = float(np.std(layer.activation))
                    layer_entropy = float(-np.sum(layer.activation * np.log(layer.activation + 1e-10)))
                else:
                    layer_coherence = activity
                    layer_entropy = 1 - activity
                
                self.state.layer_states.append(LayerState(
                    id=layer.id,
                    activity=activity,
                    coherence=layer_coherence,
                    entropy=layer_entropy
                ))
        
        # Atualizar caminhos ativos
        active_threshold = 0.3
        self.state.active_pathways = [
            f"{state.id}:{state.activity:.2f}" 
            for state in self.state.layer_states 
            if state.activity > active_threshold
        ]
        
        self.state.last_update = datetime.now()
    
    def _determine_time_horizon(self, prediction: float, coherence: float) -> TimeHorizon:
        """Determina o horizonte de tempo baseado na predição e coerência"""
        if coherence > 0.8 and abs(prediction - 0.5) > 0.4:
            return TimeHorizon.SCALP_IMEDIATO
        elif coherence > 0.6 and abs(prediction - 0.5) > 0.3:
            return TimeHorizon.INTRADAY_SWING
        elif coherence < 0.3:
            return TimeHorizon.WAIT_AND_SEE
        elif coherence > 0.5:
            return TimeHorizon.SHORT_TERM
        else:
            return TimeHorizon.MEDIUM_TERM
    
    def _determine_dominant_logic(self, quantum_coherence: float, 
                                 classical_confidence: float) -> LogicType:
        """Determina a lógica dominante"""
        if quantum_coherence > classical_confidence * 1.2:
            return LogicType.QUANTUM
        elif classical_confidence > quantum_coherence * 1.2:
            return LogicType.CLASSICAL
        else:
            return LogicType.HYBRID
import numpy as np
from typing import List, Dict, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from collections import defaultdict
import asyncio
import math
import random
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enums e Tipos
class LayerType(Enum):
    # Classical Layers
    DENSE_RELU = 'DENSE_RELU'
    CONV1D_FEATURE = 'CONV1D_FEATURE'
    LSTM_TEMPORAL = 'LSTM_TEMPORAL'
    DROPOUT_STOCHASTIC = 'DROPOUT_STOCHASTIC'
    
    # Quantum Layers
    QUANTUM_SUPERPOSITION = 'QUANTUM_SUPERPOSITION'
    QUANTUM_ENTANGLEMENT = 'QUANTUM_ENTANGLEMENT'
    QUANTUM_INTERFERENCE = 'QUANTUM_INTERFERENCE'
    QUANTUM_MEASUREMENT = 'QUANTUM_MEASUREMENT'
    
    # Hybrid Layers
    HOLOGRAPHIC_FUSION = 'HOLOGRAPHIC_FUSION'
    ASI_CONSCIOUSNESS_FIELD = 'ASI_CONSCIOUSNESS_FIELD'

class DominantLogic(Enum):
    CLASSICAL = 'CLASSICAL'
    QUANTUM = 'QUANTUM'
    HYBRID = 'HYBRID'

class TimeHorizon(Enum):
    SCALP_IMEDIATO = "SCALP_IMEDIATO"
    INTRADAY_SWING = "INTRADAY_SWING"
    WAIT_AND_SEE = "WAIT_AND_SEE"
    SHORT_TERM = "SHORT_TERM"
    MEDIUM_TERM = "MEDIUM_TERM"
    LONG_TERM = "LONG_TERM"

# Estruturas de dados
@dataclass
class NeuralLayer:
    id: str
    type: LayerType
    nodes: int  # Neurons or Qubits
    activation: List[float] = field(default_factory=list)  # Current state
    weights: List[List[float]] = field(default_factory=list)  # Synaptic connections
    bias: List[float] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = LayerType(self.type)
        
        # Inicializar listas se vazias
        if not self.activation:
            self.activation = [0.0] * self.nodes
        if not self.bias:
            self.bias = [0.01] * self.nodes

@dataclass
class LayerState:
    id: str
    activity: float

@dataclass
class NeuralState:
    coherence: float  # 0-1 Quantum Coherence
    plasticity: float  # 0-1 Synaptic Adaptability
    entropy: float  # System Uncertainty
    active_pathways: List[str] = field(default_factory=list)  # Active concepts
    layer_states: List[LayerState] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'coherence': self.coherence,
            'plasticity': self.plasticity,
            'entropy': self.entropy,
            'active_pathways': self.active_pathways,
            'layer_states': [{'id': ls.id, 'activity': ls.activity} for ls in self.layer_states]
        }

@dataclass
class PredictionOutput:
    prediction: float  # 0-1 Normalized Prediction
    confidence: float  # 0-1
    time_horizon: TimeHorizon
    dominant_logic: DominantLogic
    vector: List[float]  # Feature vector
    quantum_coherence: float = 0.0
    classical_confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'prediction': self.prediction,
            'confidence': self.confidence,
            'time_horizon': self.time_horizon.value,
            'dominant_logic': self.dominant_logic.value,
            'vector': self.vector,
            'quantum_coherence': self.quantum_coherence,
            'classical_confidence': self.classical_confidence
        }

# Operações Matemáticas
class MathOps:
    """Operações matemáticas para redes neurais"""
    
    @staticmethod
    def sigmoid(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Função sigmóide"""
        return 1 / (1 + np.exp(-x))
    
    @staticmethod
    def tanh(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Função tangente hiperbólica"""
        return np.tanh(x)
    
    @staticmethod
    def relu(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Função ReLU"""
        return np.maximum(0, x)
    
    @staticmethod
    def dot(vec: List[float], weights: List[List[float]]) -> List[float]:
        """Multiplicação matriz-vetor (simplificada)"""
        if not weights or len(weights) == 0:
            return vec
        
        result = []
        for row in weights:
            if len(row) != len(vec):
                # Preencher com zeros se necessário
                adjusted_vec = vec + [0] * (len(row) - len(vec))
                row_sum = sum(w * v for w, v in zip(row, adjusted_vec))
            else:
                row_sum = sum(w * v for w, v in zip(row, vec))
            result.append(row_sum)
        
        return result
    
    @staticmethod
    def rotate(state: float, theta: float) -> float:
        """Rotação quântica (simulação de porta Ry)"""
        # Simula mudança de amplitude de probabilidade
        cos_term = math.cos(theta / 2) * math.sqrt(state)
        sin_term = math.sin(theta / 2) * math.sqrt(1 - state)
        return (cos_term + sin_term) ** 2
    
    @staticmethod
    def xavier_init(prev_nodes: int, curr_nodes: int) -> List[List[float]]:
        """Inicialização Xavier para pesos"""
        std = math.sqrt(2.0 / (prev_nodes + curr_nodes))
        return [
            [random.uniform(-std, std) for _ in range(prev_nodes)]
            for _ in range(curr_nodes)
        ]
    
    @staticmethod
    def normalize_vector(vec: List[float]) -> List[float]:
        """Normaliza vetor para [-1, 1] usando tanh"""
        return [MathOps.tanh(x) for x in vec]
    
    @staticmethod
    def softmax(vec: List[float]) -> List[float]:
        """Função softmax"""
        exp_vec = [math.exp(x) for x in vec]
        sum_exp = sum(exp_vec)
        return [x / sum_exp for x in exp_vec]

# --- CLASSE PRINCIPAL ---

class QuantumNeuralNetwork:
    """LEXTRADER-IAG: Arquitetura Neural Híbrida Geral e Quântica
    Core Engine v4.0 (Omega)
    """
    
    def __init__(self):
        self.layers: List[NeuralLayer] = []
        self.memory_cell: List[float] = []  # Estado da célula LSTM
        self.evolution_epoch: int = 0
        self.learning_rate: float = 0.01
        self.mutation_rate: float = 0.01
        self.neurogenesis_probability: float = 0.1
        
        # Estado do Sistema
        self.state = NeuralState(
            coherence=1.0,
            plasticity=0.5,
            entropy=0.0,
            active_pathways=[],
            layer_states=[]
        )
        
        # Histórico
        self.prediction_history: List[PredictionOutput] = []
        self.evolution_history: List[Dict[str, Any]] = []
        self.layer_growth_history: Dict[str, int] = defaultdict(int)
        
        logger.info("🧠 LEXTRADER-IAG: Instância criada")
    
    async def initialize(self) -> None:
        """Inicializa a arquitetura híbrida"""
        logger.info("🧠 LEXTRADER-IAG: Inicializando Arquitetura Híbrida...")
        await self.initialize_architecture()
        logger.info("✅ Redes Neurais Gerais e Quânticas Sincronizadas.")
    
    # --- DEFINIÇÃO DA ARQUITETURA ---
    
    async def initialize_architecture(self) -> None:
        """Define a arquitetura da rede neural híbrida"""
        self.layers = []
        
        # 1. PROCESSAMENTO DE ENTRADA (CLÁSSICO)
        # CNN para reconhecimento de padrões locais (microestrutura)
        self.add_layer('L1_CNN_Visual', LayerType.CONV1D_FEATURE, 64, {'kernel': 3})
        
        # 2. MEMÓRIA TEMPORAL (CLÁSSICO)
        # LSTM para contexto de séries temporais
        self.add_layer('L2_LSTM_Memory', LayerType.LSTM_TEMPORAL, 32, {'lookback': 10})
        
        # 3. CODIFICAÇÃO QUÂNTICA
        # Mapeamento de características clássicas para estado quântico
        self.add_layer('Q1_Superposition', LayerType.QUANTUM_SUPERPOSITION, 32, {})
        
        # 4. PROCESSAMENTO QUÂNTICO
        # Entrelaçamento de qubits para encontrar correlações não-locais
        self.add_layer('Q2_Entanglement', LayerType.QUANTUM_ENTANGLEMENT, 32, {'topology': 'all-to-all'})
        self.add_layer('Q3_Interference', LayerType.QUANTUM_INTERFERENCE, 16, {})
        
        # 5. FUSÃO HÍBRIDA
        # Fusão de Lógica Clássica com Intuição Quântica
        self.add_layer('H1_Holographic', LayerType.HOLOGRAPHIC_FUSION, 64, {'integration_rate': 0.7})
        
        # 6. RACIOCÍNIO PROFUNDO (CLÁSSICO)
        self.add_layer('L3_Dense_Reasoning', LayerType.DENSE_RELU, 128, {})
        
        # 7. CAMPO DE CONSCIÊNCIA (ASI)
        # Moldagem final da decisão baseada em restrições éticas/risco
        self.add_layer('ASI_Core', LayerType.ASI_CONSCIOUSNESS_FIELD, 1, {})
        
        # Inicializar pesos
        self.initialize_weights()
        
        # Inicializar célula de memória LSTM
        self.memory_cell = [0.0] * 32
        
        logger.info(f"✅ Arquitetura inicializada com {len(self.layers)} camadas")
    
    def add_layer(self, layer_id: str, layer_type: LayerType, nodes: int, parameters: Dict[str, Any]) -> None:
        """Adiciona uma camada à rede"""
        layer = NeuralLayer(
            id=layer_id,
            type=layer_type,
            nodes=nodes,
            parameters=parameters
        )
        self.layers.append(layer)
        logger.debug(f"➕ Camada adicionada: {layer_id} ({layer_type.value}) com {nodes} nós")
    
    def initialize_weights(self) -> None:
        """Inicializa os pesos sinápticos de todas as camadas"""
        for i, layer in enumerate(self.layers):
            prev_nodes = 4 if i == 0 else self.layers[i - 1].nodes
            
            # Inicialização Xavier
            layer.weights = MathOps.xavier_init(prev_nodes, layer.nodes)
            
            # Inicializar bias
            layer.bias = [random.uniform(-0.05, 0.05) for _ in range(layer.nodes)]
            
            logger.debug(f"⚖️ Pesos inicializados para {layer.id}: {len(layer.weights)}x{len(layer.weights[0])}")
    
    # --- PROPAGAÇÃO DIRETA (INFERÊNCIA) ---
    
    async def predict(self, features: List[float]) -> PredictionOutput:
        """Executa uma predição através da rede neural híbrida"""
        logger.debug(f"🔮 Predição iniciada com {len(features)} features")
        
        signal = features.copy()
        quantum_signal: List[float] = []
        classical_signal: List[float] = []
        
        # 1. Normalizar entrada
        signal = MathOps.normalize_vector(signal)
        
        # Processar cada camada
        for layer in self.layers:
            # Processamento baseado no tipo de camada
            if self._is_classical(layer.type):
                signal = self._process_classical(layer, signal)
                if layer.id == 'L2_LSTM_Memory':
                    classical_signal = signal.copy()
                    
            elif self._is_quantum(layer.type):
                # Se entrando no reino quântico, codificar sinal clássico
                if layer.type == LayerType.QUANTUM_SUPERPOSITION:
                    # Codificar: Amplitude Clássica -> Probabilidade Quântica
                    signal = [
                        (math.sin(v * math.pi) + 1) / 2
                        for v in signal[:layer.nodes]
                    ]
                
                signal = self._process_quantum(layer, signal)
                if layer.type == LayerType.QUANTUM_INTERFERENCE:
                    quantum_signal = signal.copy()
                    
            elif layer.type == LayerType.HOLOGRAPHIC_FUSION:
                # FUSÃO DE SINAIS
                signal = self._process_fusion(layer, classical_signal, quantum_signal)
                
            elif layer.type == LayerType.ASI_CONSCIOUSNESS_FIELD:
                signal = self._process_asi(layer, signal)
            
            # Atualizar ativação da camada para visualização
            layer.activation = signal[:layer.nodes]  # Garantir tamanho correto
        
        # Calcular métricas
        output = signal[0] if signal else 0.5
        
        # Coerência quântica (média dos sinais quânticos)
        quantum_coherence = 0.0
        if quantum_signal:
            quantum_coherence = sum(quantum_signal) / len(quantum_signal)
        
        # Confiança clássica
        classical_confidence = abs(output - 0.5) * 2
        
        # Determinar lógica dominante
        dominant_logic = DominantLogic.QUANTUM if quantum_coherence > classical_confidence else DominantLogic.CLASSICAL
        
        # Determinar horizonte de tempo
        time_horizon = self._determine_time_horizon(output, quantum_coherence)
        
        # Calcular confiança geral
        overall_confidence = (classical_confidence + quantum_coherence) / 2
        
        # Atualizar estado do sistema
        self.state.coherence = quantum_coherence
        self.state.entropy = 1 - classical_confidence
        self.state.layer_states = [
            LayerState(
                id=layer.id,
                activity=sum(abs(a) for a in layer.activation) / max(len(layer.activation), 1)
            )
            for layer in self.layers
        ]
        
        # Atualizar vias ativas
        if output > 0.7:
            self.state.active_pathways = ["BULLISH_SIGNAL_STRONG"]
        elif output < 0.3:
            self.state.active_pathways = ["BEARISH_SIGNAL_STRONG"]
        else:
            self.state.active_pathways = ["NEUTRAL_UNCERTAINTY"]
        
        # Criar resultado da predição
        result = PredictionOutput(
            prediction=output,
            confidence=overall_confidence,
            time_horizon=time_horizon,
            dominant_logic=dominant_logic,
            vector=signal,
            quantum_coherence=quantum_coherence,
            classical_confidence=classical_confidence
        )
        
        # Adicionar ao histórico
        self.prediction_history.append(result)
        if len(self.prediction_history) > 1000:
            self.prediction_history.pop(0)
        
        logger.debug(f"✅ Predição concluída: {output:.4f} (Confiança: {overall_confidence:.2%})")
        
        return result
    
    # --- PROCESSADORES DE CAMADA ---
    
    def _is_classical(self, layer_type: LayerType) -> bool:
        """Verifica se a camada é clássica"""
        classical_types = {
            LayerType.DENSE_RELU,
            LayerType.CONV1D_FEATURE,
            LayerType.LSTM_TEMPORAL,
            LayerType.DROPOUT_STOCHASTIC
        }
        return layer_type in classical_types
    
    def _is_quantum(self, layer_type: LayerType) -> bool:
        """Verifica se a camada é quântica"""
        return layer_type.value.startswith('QUANTUM')
    
    def _process_classical(self, layer: NeuralLayer, input_signal: List[float]) -> List[float]:
        """Processa camada clássica"""
        # Multiplicação matriz-vetor
        output = MathOps.dot(input_signal, layer.weights)
        
        # Adicionar bias
        output = [o + b for o, b in zip(output, layer.bias)]
        
        # Aplicar funções de ativação
        if layer.type == LayerType.DENSE_RELU:
            return [MathOps.relu(x) for x in output]
            
        elif layer.type == LayerType.LSTM_TEMPORAL:
            # Lógica LSTM simplificada
            processed = []
            lookback = layer.parameters.get('lookback', 10)
            
            for i, val in enumerate(output):
                if i >= len(self.memory_cell):
                    break
                    
                # Portas LSTM simplificadas
                forget_gate = MathOps.sigmoid(val)
                input_gate = MathOps.sigmoid(val + 0.1)
                candidate = MathOps.tanh(val)
                
                # Atualizar célula de memória
                self.memory_cell[i] = (self.memory_cell[i] * forget_gate) + (input_gate * candidate)
                
                # Saída
                processed.append(MathOps.tanh(self.memory_cell[i]))
            
            # Preencher se necessário
            while len(processed) < layer.nodes:
                processed.append(0.0)
            
            return processed[:layer.nodes]
            
        elif layer.type == LayerType.CONV1D_FEATURE:
            # Simulação de convolução 1D
            kernel_size = layer.parameters.get('kernel', 3)
            convolved = []
            
            for i in range(layer.nodes):
                # Média ponderada do kernel
                kernel_sum = 0.0
                for k in range(kernel_size):
                    idx = (i + k) % len(output)
                    kernel_sum += output[idx] * (1.0 / (k + 1))
                convolved.append(MathOps.relu(kernel_sum / kernel_size))
            
            return convolved
            
        else:  # DROPOUT_STOCHASTIC ou padrão
            # Aplicar sigmóide como padrão
            return [MathOps.sigmoid(x) for x in output]
    
    def _process_quantum(self, layer: NeuralLayer, input_signal: List[float]) -> List[float]:
        """Processa camada quântica"""
        if layer.type == LayerType.QUANTUM_ENTANGLEMENT:
            # Simular Entrelaçamento: Média de estados através de vizinhos (propriedade holográfica)
            entangled = input_signal.copy()
            n = len(entangled)
            
            for i in range(n):
                neighbor = input_signal[(i + 1) % n]
                # Simulação de Estado de Bell
                entangled[i] = (input_signal[i] + neighbor) / math.sqrt(2)
            
            return entangled
            
        elif layer.type == LayerType.QUANTUM_INTERFERENCE:
            # Interferência Construtiva/Destrutiva
            # Pode amplificar bons sinais ou cancelar ruído
            interfered = []
            for val in input_signal:
                phase = val * 2 * math.pi
                # Colapsar para probabilidade
                interfered.append((math.cos(phase) + 1) / 2)
            
            return interfered
            
        elif layer.type == LayerType.QUANTUM_MEASUREMENT:
            # Colapso da função de onda
            return [1.0 if x > 0.5 else 0.0 for x in input_signal]
        
        else:  # SUPERPOSITION ou outros
            # Apenas passar adiante
            return input_signal[:layer.nodes]
    
    def _process_fusion(self, layer: NeuralLayer, classical: List[float], quantum: List[float]) -> List[float]:
        """Processa fusão holográfica"""
        # Fusão Holográfica
        # Redimensiona vetores para combinar número de nós e média ponderada
        size = layer.nodes
        fused: List[float] = []
        
        integration_rate = layer.parameters.get('integration_rate', 0.5)
        
        for i in range(size):
            # Usar valores circulares se necessário
            c_val = classical[i % len(classical)] if classical else 0.5
            q_val = quantum[i % len(quantum)] if quantum else 0.5
            
            # Taxa de integração determina confiança na intuição quântica vs lógica clássica
            # Fusão não-linear
            fused_value = (c_val * (1 - integration_rate)) + (q_val * integration_rate)
            fused.append(fused_value)
        
        return fused
    
    def _process_asi(self, layer: NeuralLayer, input_signal: List[float]) -> List[float]:
        """Processa campo de consciência ASI"""
        # Restrições ASI e ajustes "Modo Deus"
        # Garante que sinais não violem parâmetros de risco
        processed = []
        
        for val in input_signal:
            # Amplificador de Certeza: Empurra sinais fracos para 0.5 (neutro) ou fortes para 0/1
            if val > 0.8:
                processed.append(min(1.0, val * 1.1))  # Convicção
            elif val < 0.2:
                processed.append(max(0.0, val * 0.9))  # Convicção
            else:
                processed.append(val)  # Preserva incerteza
        
        return processed
    
    # --- NEUROGÊNESE ESTRUTURAL (NOVOS NEURÔNIOS) ---
    
    def neurogenesis(self, layer_id: str) -> bool:
        """Adiciona um novo neurônio/qubit à camada especificada"""
        layer_idx = self._find_layer_index(layer_id)
        if layer_idx == -1:
            logger.warning(f"❌ Camada não encontrada para neurogênese: {layer_id}")
            return False
        
        layer = self.layers[layer_idx]
        prev_layer = self.layers[layer_idx - 1] if layer_idx > 0 else None
        next_layer = self.layers[layer_idx + 1] if layer_idx < len(self.layers) - 1 else None
        
        logger.info(f"✨ Neurogênese: Adicionando nó à camada {layer.id}. Total: {layer.nodes + 1}")
        
        # 1. Aumentar contagem de nós
        layer.nodes += 1
        
        # 2. Adicionar bias e inicializar ativação
        new_bias = random.uniform(-0.05, 0.05)
        layer.bias.append(new_bias)
        layer.activation.append(0.0)
        
        # 3. Adicionar pesos sinápticos da camada anterior
        input_size = prev_layer.nodes if prev_layer else 4  # entradas padrão
        new_weights = [random.uniform(-0.1, 0.1) for _ in range(input_size)]
        layer.weights.append(new_weights)
        
        # 4. Atualizar pesos da próxima camada
        if next_layer:
            for neuron_weights in next_layer.weights:
                neuron_weights.append(random.uniform(-0.1, 0.1))
        
        # Atualizar histórico
        self.layer_growth_history[layer_id] += 1
        
        # Aumentar plasticidade
        self.state.plasticity = min(1.0, self.state.plasticity + 0.05)
        
        logger.debug(f"✅ Neurogênese concluída para {layer_id}")
        return True
    
    def _find_layer_index(self, layer_id: str) -> int:
        """Encontra índice da camada pelo ID"""
        for i, layer in enumerate(self.layers):
            if layer.id == layer_id:
                return i
        return -1
    
    # --- UTILIDADES ---
    
    def _determine_time_horizon(self, prediction: float, coherence: float) -> TimeHorizon:
        """Determina horizonte de tempo baseado na predição e coerência"""
        if coherence > 0.8 and abs(prediction - 0.5) > 0.4:
            return TimeHorizon.SCALP_IMEDIATO
        elif coherence < 0.5:
            return TimeHorizon.WAIT_AND_SEE
        elif coherence > 0.6 and abs(prediction - 0.5) > 0.2:
            return TimeHorizon.INTRADAY_SWING
        elif prediction > 0.7 or prediction < 0.3:
            return TimeHorizon.SHORT_TERM
        else:
            return TimeHorizon.MEDIUM_TERM
    
    # --- APRENDIZADO E EVOLUÇÃO ---
    
    def evolve(self) -> None:
        """Evolui a rede neural através de aprendizado e neurogênese"""
        self.evolution_epoch += 1
        logger.info(f"🔄 Evolução da rede: Época {self.evolution_epoch}")
        
        # 1. Ajuste de Pesos Sinápticos (Aprendizado)
        for layer in self.layers:
            # Mutação de pesos
            mutated_weights = []
            for row in layer.weights:
                mutated_row = [
                    w + random.uniform(-self.mutation_rate, self.mutation_rate)
                    for w in row
                ]
                mutated_weights.append(mutated_row)
            layer.weights = mutated_weights
        
        # 2. Neuroplasticidade Estrutural (Crescimento)
        # Se plasticidade está alta e temos sorte, criar novo neurônio
        if self.state.plasticity > 0.6 and random.random() < self.neurogenesis_probability:
            logger.debug("🎲 Tentando neurogênese em L3_Dense_Reasoning")
            self.neurogenesis('L3_Dense_Reasoning')
        
        # 3. Expansão Quântica
        if self.state.coherence > 0.9 and random.random() < self.neurogenesis_probability * 0.5:
            logger.debug("🎲 Tentando neurogênese quântica em Q2_Entanglement")
            self.neurogenesis('Q2_Entanglement')
        
        # 4. Ajustar plasticidade baseado na performance
        if len(self.prediction_history) > 10:
            recent_confidences = [p.confidence for p in self.prediction_history[-10:]]
            avg_confidence = sum(recent_confidences) / len(recent_confidences)
            
            if avg_confidence > 0.7:
                # Alta confiança: reduzir plasticidade para estabilizar
                self.state.plasticity = max(0.1, self.state.plasticity - 0.05)
            else:
                # Baixa confiança: aumentar plasticidade para aprender
                self.state.plasticity = min(0.9, self.state.plasticity + 0.05)
        
        # Registrar evolução
        evolution_record = {
            'epoch': self.evolution_epoch,
            'timestamp': datetime.now().isoformat(),
            'coherence': self.state.coherence,
            'plasticity': self.state.plasticity,
            'entropy': self.state.entropy,
            'total_nodes': sum(layer.nodes for layer in self.layers)
        }
        self.evolution_history.append(evolution_record)
        
        # Limitar histórico
        if len(self.evolution_history) > 1000:
            self.evolution_history.pop(0)
        
        logger.debug(f"✅ Evolução concluída. Plasticidade: {self.state.plasticity:.3f}")
    
    # --- TREINAMENTO ONLINE ---
    
    def train_online(self, features: List[float], target: float) -> float:
        """Treinamento online com gradiente descendente simplificado"""
        # Executar predição
        prediction = asyncio.run(self.predict(features))
        
        # Calcular erro
        error = target - prediction.prediction
        
        # Backpropagation simplificado (taxa de aprendizado fixa)
        learning_rate = self.learning_rate * (1 + self.state.plasticity)
        
        # Ajustar pesos da última camada
        if self.layers:
            last_layer = self.layers[-1]
            
            # Ajuste simplificado
            for i in range(len(last_layer.weights)):
                for j in range(len(last_layer.weights[i])):
                    last_layer.weights[i][j] += learning_rate * error * random.uniform(-1, 1)
            
            # Ajustar bias
            for i in range(len(last_layer.bias)):
                last_layer.bias[i] += learning_rate * error * 0.1
        
        # Retornar erro
        return abs(error)
    
    # --- MÉTODOS DE ANÁLISE E VISUALIZAÇÃO ---
    
    def get_architecture_summary(self) -> Dict[str, Any]:
        """Retorna resumo da arquitetura da rede"""
        summary = {
            'total_layers': len(self.layers),
            'total_nodes': sum(layer.nodes for layer in self.layers),
            'evolution_epoch': self.evolution_epoch,
            'layer_details': []
        }
        
        for layer in self.layers:
            layer_summary = {
                'id': layer.id,
                'type': layer.type.value,
                'nodes': layer.nodes,
                'weight_shape': f"{len(layer.weights)}x{len(layer.weights[0]) if layer.weights else 0}",
                'avg_activation': sum(abs(a) for a in layer.activation) / max(len(layer.activation), 1),
                'growth_count': self.layer_growth_history.get(layer.id, 0)
            }
            summary['layer_details'].append(layer_summary)
        
        return summary
    
    def get_performance_metrics(self, window: int = 100) -> Dict[str, Any]:
        """Retorna métricas de performance"""
        if len(self.prediction_history) < 2:
            return {'error': 'Histórico insuficiente'}
        
        recent_predictions = self.prediction_history[-window:]
        
        confidences = [p.confidence for p in recent_predictions]
        predictions = [p.prediction for p in recent_predictions]
        
        return {
            'window_size': len(recent_predictions),
            'avg_confidence': sum(confidences) / len(confidences),
            'min_confidence': min(confidences),
            'max_confidence': max(confidences),
            'avg_prediction': sum(predictions) / len(predictions),
            'dominant_logic_distribution': {
                logic.value: sum(1 for p in recent_predictions if p.dominant_logic == logic)
                for logic in DominantLogic
            },
            'time_horizon_distribution': {
                horizon.value: sum(1 for p in recent_predictions if p.time_horizon == horizon)
                for horizon in TimeHorizon
            }
        }
    
    def get_state_vector(self) -> Dict[str, Any]:
        """Retorna vetor de estado completo do sistema"""
        return {
            'neural_state': self.state.to_dict(),
            'architecture': self.get_architecture_summary(),
            'performance': self.get_performance_metrics(50),
            'evolution': {
                'epoch': self.evolution_epoch,
                'recent_evolutions': len(self.evolution_history)
            }
        }
    
    def reset(self) -> None:
        """Reinicia a rede neural (mas mantém arquitetura)"""
        logger.warning("🔄 Reiniciando Quantum Neural Network...")
        
        # Reinicializar pesos
        self.initialize_weights()
        
        # Resetar estado
        self.state = NeuralState(
            coherence=1.0,
            plasticity=0.5,
            entropy=0.0,
            active_pathways=[],
            layer_states=[]
        )
        
        # Resetar memória
        self.memory_cell = [0.0] * 32
        
        # Limpar histórico (opcional)
        # self.prediction_history.clear()
        # self.evolution_history.clear()
        
        logger.info("✅ Rede neural reinicializada")

# Interface CLI para demonstração
class NeuralNetworkCLI:
    """Interface de linha de comando para a rede neural quântica"""
    
    def __init__(self):
        self.network = QuantumNeuralNetwork()
        self.running = True
    
    async def run(self):
        """Executa a interface CLI"""
        print("=" * 60)
        print("🧠 LEXTRADER-IAG - Rede Neural Quântica Híbrida")
        print("=" * 60)
        
        # Inicializar rede
        await self.network.initialize()
        
        while self.running:
            print("\n" + "=" * 40)
            print("MENU PRINCIPAL")
            print("=" * 40)
            print("1. 🔮 Fazer Predição")
            print("2. 🧬 Evoluir Rede")
            print("3. 📊 Ver Arquitetura")
            print("4. 📈 Ver Métricas")
            print("5. ⚙️  Ver Estado do Sistema")
            print("6. 🧠 Neurogênese Manual")
            print("7. 🎯 Treinamento Online")
            print("8. 🔄 Reiniciar Rede")
            print("0. ❌ Sair")
            print("=" * 40)
            
            choice = input("\nEscolha uma opção: ").strip()
            
            try:
                if choice == "1":
                    await self.make_prediction()
                elif choice == "2":
                    self.evolve_network()
                elif choice == "3":
                    self.show_architecture()
                elif choice == "4":
                    self.show_metrics()
                elif choice == "5":
                    self.show_system_state()
                elif choice == "6":
                    self.manual_neurogenesis()
                elif choice == "7":
                    self.online_training()
                elif choice == "8":
                    self.reset_network()
                elif choice == "0":
                    self.running = False
                    print("\n👋 Até logo!")
                else:
                    print("❌ Opção inválida!")
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Operação interrompida")
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    async def make_prediction(self):
        """Faz uma predição com dados simulados"""
        print("\n🔮 Gerando features simuladas...")
        
        # Gerar features aleatórias (4 features normalizadas)
        features = [random.random() for _ in range(4)]
        print(f"Features: {[f'{f:.3f}' for f in features]}")
        
        # Executar predição na rede
        prediction = await self.network.predict(features)
        print(f"Predição: {prediction.prediction:.3f} | Confiança: {prediction.confidence:.2%}")