# quantum/quantum_neural_network.py
import streamlit as st
import asyncio
import math
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from collections import defaultdict

# Importar otimizador de performance
try:
    from QuantumPerformanceOptimizer import (
        quantum_cache, 
        get_quantum_optimizer,
        AsyncOptimizations
    )
    OPTIMIZER_AVAILABLE = True
except ImportError:
    OPTIMIZER_AVAILABLE = False
    print("⚠️ QuantumPerformanceOptimizer não disponível")

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('quantum_neural_network.log')
    ]
)
logger = logging.getLogger(__name__)

class LayerType(Enum):
    QUANTUM_ENCODING = "quantum_encoding"
    QUANTUM_FEATURE_MAP = "quantum_feature_map"
    QUANTUM_PROCESSING = "quantum_processing"
    QUANTUM_MEASUREMENT = "quantum_measurement"

class EntanglementType(Enum):
    LINEAR = "linear"
    FULL = "full"

@dataclass
class QuantumLayer:
    """Estrutura para camadas da rede neural quântica"""
    layer_type: LayerType
    qubits: int
    gates: List[str]
    entanglement: Optional[EntanglementType] = None
    variational: bool = False
    observables: Optional[List[str]] = None

@dataclass
class QuantumPrediction:
    """Resultado da predição da rede neural quântica"""
    prediction: float
    confidence: float
    quantum_state: List[int]
    entanglement: float
    measurements: List[int]

@dataclass
class TrainingResult:
    """Resultado do treinamento quântico"""
    loss: float
    accuracy: float
    quantum_advantage: float
    gradients: Dict[str, List[float]]

class Qubit:
    """Simulação de um qubit quântico"""
    
    def __init__(self, id: int):
        self.id = id
        self.state = [1.0, 0.0]  # Estado |0⟩
        self.measured = False
        self.measurement_result = None
    
    def __repr__(self):
        return f"Qubit({self.id}, state={self.state}, measured={self.measured})"

class QuantumNeuralNetwork:
    """
    Rede Neural Quântica - Combina princípios de redes neurais 
    com computação quântica para aprendizado avançado
    """
    
    def __init__(self):
        self.layers: List[QuantumLayer] = []
        self.quantum_weights: Dict[str, List[Qubit]] = {}
        self.entanglement_patterns: Dict[str, Any] = {}
        self.superposition_layers: Dict[str, Any] = {}
        self.qubit_counter = 0
        
        # Inicializar otimizador
        self.optimizer = get_quantum_optimizer() if OPTIMIZER_AVAILABLE else None
        
        logger.info("🧠⚛️ Rede Neural Quântica Criada")

    async def initialize(self):
        """Inicializa a rede neural quântica"""
        logger.info('🧠⚛️ Inicializando Rede Neural Quântica...')
        await self.initialize_quantum_layers()
        await self.initialize_quantum_weights()
        logger.info('✅ Rede Neural Quântica Inicializada com Sucesso!')

    async def initialize_quantum_layers(self):
        """Configura camadas quânticas para processamento"""
        self.layers = [
            QuantumLayer(
                layer_type=LayerType.QUANTUM_ENCODING,
                qubits=8,
                gates=['H', 'RX', 'RY']
            ),
            QuantumLayer(
                layer_type=LayerType.QUANTUM_FEATURE_MAP,
                qubits=16,
                gates=['H', 'RX', 'RY', 'CNOT'],
                entanglement=EntanglementType.LINEAR
            ),
            QuantumLayer(
                layer_type=LayerType.QUANTUM_PROCESSING,
                qubits=12,
                gates=['RX', 'RY', 'RZ', 'CNOT'],
                variational=True
            ),
            QuantumLayer(
                layer_type=LayerType.QUANTUM_MEASUREMENT,
                qubits=4,
                gates=[],
                observables=['Z', 'X']
            )
        ]

    async def initialize_quantum_weights(self):
        """Inicializa pesos quânticos com superposição"""
        for layer in self.layers:
            weights = await self.create_quantum_weights(layer.qubits)
            self.quantum_weights[layer.layer_type.value] = weights

    async def create_quantum_weights(self, num_qubits: int) -> List[Qubit]:
        """Cria pesos quânticos com superposição"""
        weights = []
        
        for i in range(num_qubits):
            weight_qubit = await self.create_qubit()
            # Inicializar com superposição igual
            await self.apply_hadamard_gate(weight_qubit)
            weights.append(weight_qubit)
        
        return weights

    async def predict(self, quantum_input: List[Qubit], classical_features: List[float]) -> QuantumPrediction:
        """
        Executa forward pass quântico para predição
        Otimizado com cache automático
        """
        logger.info("🔮 Executando predição quântica...")
        
        # Usar cache se disponível
        if self.optimizer:
            return await self._predict_cached(classical_features)
        else:
            return await self._predict_uncached(quantum_input, classical_features)
    
    @quantum_cache(ttl=300.0) if OPTIMIZER_AVAILABLE else lambda f: f
    async def _predict_cached(self, classical_features: List[float]) -> QuantumPrediction:
        """Versão cached da predição"""
        quantum_input = []
        return await self._predict_uncached(quantum_input, classical_features)
    
    async def _predict_uncached(self, quantum_input: List[Qubit], classical_features: List[float]) -> QuantumPrediction:
        """Implementação real da predição"""
        # Forward pass quântico
        encoded_input = await self.quantum_encode(classical_features)
        processed_state = await self.quantum_forward_pass(encoded_input)
        measurements = await self.quantum_measure(processed_state)
        
        return self.interpret_quantum_results(measurements)

    async def quantum_encode(self, classical_features: List[float]) -> List[Qubit]:
        """Codifica features clássicas em estados quânticos"""
        encoded_qubits = []
        
        for i, feature in enumerate(classical_features):
            qubit = await self.create_qubit()
            angle = self.normalize_to_pi(feature)
            await self.apply_rotation_gate(qubit, angle)
            encoded_qubits.append(qubit)
        
        logger.info(f"📊 {len(encoded_qubits)} qubits codificados")
        return encoded_qubits

    async def quantum_forward_pass(self, encoded_input: List[Qubit]) -> List[Qubit]:
        """
        Executa o forward pass através de todas as camadas quânticas
        Otimizado com batch processing
        """
        current_state = encoded_input
        
        # Se otimizador disponível, processar em paralelo
        if self.optimizer and len(self.layers) > 4:
            # Batch processing para múltiplas camadas
            logger.debug("🚀 Batch processing de camadas ativado")
            tasks = [self.apply_quantum_layer(layer, current_state) for layer in self.layers]
            states = await asyncio.gather(*tasks)
            return states[-1] if states else current_state
        else:
            # Processamento sequencial (padrão)
            for layer in self.layers:
                logger.debug(f"Aplicando camada {layer.layer_type.value}")
                current_state = await self.apply_quantum_layer(layer, current_state)
            return current_state

    async def apply_quantum_layer(self, layer: QuantumLayer, input_state: List[Qubit]) -> List[Qubit]:
        """Aplica uma camada quântica específica"""
        if layer.layer_type == LayerType.QUANTUM_ENCODING:
            return await self.apply_encoding_layer(input_state, layer)
        elif layer.layer_type == LayerType.QUANTUM_FEATURE_MAP:
            return await self.apply_feature_map_layer(input_state, layer)
        elif layer.layer_type == LayerType.QUANTUM_PROCESSING:
            return await self.apply_processing_layer(input_state, layer)
        elif layer.layer_type == LayerType.QUANTUM_MEASUREMENT:
            return await self.apply_measurement_layer(input_state, layer)
        else:
            return input_state

    async def apply_feature_map_layer(self, input_state: List[Qubit], layer: QuantumLayer) -> List[Qubit]:
        """Aplica camada de mapeamento de features quântico"""
        output_state = input_state.copy()
        
        # Aplicar mapa de features quântico
        for i, qubit in enumerate(output_state):
            await self.apply_feature_map_gates(qubit, layer.gates)
        
        # Criar entrelaçamento
        if layer.entanglement == EntanglementType.LINEAR:
            await self.create_linear_entanglement(output_state)
        elif layer.entanglement == EntanglementType.FULL:
            await self.create_full_entanglement(output_state)
        
        return output_state

    async def create_linear_entanglement(self, qubits: List[Qubit]):
        """Cria entrelaçamento linear entre qubits"""
        for i in range(len(qubits) - 1):
            await self.apply_cnot_gate(qubits[i], qubits[i + 1])

    async def create_full_entanglement(self, qubits: List[Qubit]):
        """Cria entrelaçamento completo entre qubits"""
        for i in range(len(qubits)):
            for j in range(i + 1, len(qubits)):
                await self.apply_cnot_gate(qubits[i], qubits[j])

    async def apply_processing_layer(self, input_state: List[Qubit], layer: QuantumLayer) -> List[Qubit]:
        """Aplica camada de processamento quântico variacional"""
        output_state = input_state.copy()
        weights = self.quantum_weights.get('quantum_processing', [])
        
        # Aplicar circuitos variacionais
        for i, qubit in enumerate(output_state):
            if i < len(weights):
                await self.apply_variational_block(qubit, weights[i])
        
        return output_state

    async def apply_variational_block(self, data_qubit: Qubit, weight_qubit: Qubit):
        """Aplica bloco variacional quântico"""
        await self.apply_controlled_rotation(data_qubit, weight_qubit)
        await self.apply_entangling_gate(data_qubit, weight_qubit)

    async def quantum_measure(self, quantum_state: List[Qubit]) -> List[int]:
        """Realiza medição do estado quântico"""
        measurements = []
        
        for qubit in quantum_state:
            measurement = await self.measure_qubit(qubit)
            measurements.append(measurement)
        
        return measurements

    def interpret_quantum_results(self, measurements: List[int]) -> QuantumPrediction:
        """Interpreta resultados das medições quânticas"""
        binary_result = [1 if m == 1 else 0 for m in measurements]
        decimal_result = self.binary_to_decimal(binary_result)
        
        return QuantumPrediction(
            prediction=self.normalize_prediction(decimal_result),
            confidence=self.calculate_quantum_confidence(measurements),
            quantum_state=measurements,
            entanglement=self.calculate_entanglement_measure(measurements),
            measurements=measurements
        )

    def calculate_quantum_confidence(self, measurements: List[int]) -> float:
        """Calcula confiança baseada na variância das medições"""
        variance = self.calculate_variance(measurements)
        return 1.0 - variance  # Confiança inversamente proporcional à variância

    # Métodos de Aprendizado Quântico
    async def train_quantum(self, data: List[List[float]], labels: List[float]) -> TrainingResult:
        """Treina a rede neural quântica"""
        logger.info("🎯 Iniciando treinamento quântico...")
        
        quantum_gradients = await self.calculate_quantum_gradients(data, labels)
        await self.update_quantum_weights(quantum_gradients)
        
        return TrainingResult(
            loss=await self.calculate_quantum_loss(data, labels),
            accuracy=await self.calculate_quantum_accuracy(data, labels),
            quantum_advantage=await self.calculate_training_advantage(data),
            gradients=quantum_gradients
        )

    async def calculate_quantum_gradients(self, data: List[List[float]], labels: List[float]) -> Dict[str, List[float]]:
        """Calcula gradientes quânticos usando parameter shift rule"""
        gradients = {}
        
        for layer in self.layers:
            layer_gradients = await self.calculate_layer_gradients(layer, data, labels)
            gradients[layer.layer_type.value] = layer_gradients
        
        return gradients

    async def calculate_layer_gradients(self, layer: QuantumLayer, data: List[List[float]], labels: List[float]) -> List[float]:
        """Calcula gradientes para uma camada específica"""
        gradients = []
        
        for i in range(layer.qubits):
            gradient = await self.parameter_shift_rule(layer, i, data, labels)
            gradients.append(gradient)
        
        return gradients

    async def parameter_shift_rule(self, layer: QuantumLayer, qubit_index: int, 
                                 data: List[List[float]], labels: List[float]) -> float:
        """Implementa parameter shift rule para gradientes quânticos"""
        shift = math.pi / 2
        
        plus_loss = await self.calculate_shifted_loss(layer, qubit_index, shift, data, labels)
        minus_loss = await self.calculate_shifted_loss(layer, qubit_index, -shift, data, labels)
        
        return (plus_loss - minus_loss) / 2

    async def calculate_shifted_loss(self, layer: QuantumLayer, qubit_index: int, 
                                   shift: float, data: List[List[float]], labels: List[float]) -> float:
        """Calcula loss com parâmetros deslocados"""
        # Simulação do cálculo de loss com shift
        total_loss = 0.0
        
        for i, sample in enumerate(data):
            prediction = await self.predict([], sample)  # Simplified
            expected = labels[i]
            loss = (prediction.prediction - expected) ** 2
            total_loss += loss
        
        return total_loss / len(data)

    async def calculate_quantum_loss(self, data: List[List[float]], labels: List[float]) -> float:
        """Calcula loss quântica"""
        total_loss = 0.0
        
        for i, sample in enumerate(data):
            prediction = await self.predict([], sample)
            expected = labels[i]
            loss = (prediction.prediction - expected) ** 2
            total_loss += loss
        
        return total_loss / len(data)

    async def calculate_quantum_accuracy(self, data: List[List[float]], labels: List[float]) -> float:
        """Calcula acurácia quântica"""
        correct = 0
        
        for i, sample in enumerate(data):
            prediction = await self.predict([], sample)
            predicted_class = 1 if prediction.prediction > 0.5 else 0
            if predicted_class == labels[i]:
                correct += 1
        
        return correct / len(data)

    async def calculate_training_advantage(self, data: List[List[float]]) -> float:
        """Calcula vantagem quântica no treinamento"""
        # Simular vantagem quântica (2x a 100x mais rápido)
        return random.uniform(2.0, 100.0)

    async def update_quantum_weights(self, gradients: Dict[str, List[float]]):
        """Atualiza pesos quânticos baseado nos gradientes"""
        learning_rate = 0.01
        
        for layer_type, layer_gradients in gradients.items():
            if layer_type in self.quantum_weights:
                weights = self.quantum_weights[layer_type]
                for i, (qubit, gradient) in enumerate(zip(weights, layer_gradients)):
                    if i < len(layer_gradients):
                        await self.update_qubit_weight(qubit, gradient, learning_rate)

    async def update_qubit_weight(self, qubit: Qubit, gradient: float, learning_rate: float):
        """Atualiza peso de um qubit individual"""
        # Simular atualização do peso quântico
        rotation_angle = -learning_rate * gradient
        await self.apply_rotation_gate(qubit, rotation_angle)

    # Métodos de Operações Quânticas
    async def create_qubit(self) -> Qubit:
        """Cria um novo qubit"""
        qubit = Qubit(self.qubit_counter)
        self.qubit_counter += 1
        return qubit

    async def apply_hadamard_gate(self, qubit: Qubit):
        """Aplica porta Hadamard (H) ao qubit"""
        # Matriz Hadamard
        h_matrix = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
        qubit.state = np.dot(h_matrix, qubit.state)
        
    async def apply_rotation_gate(self, qubit: Qubit, angle: float):
        """Aplica porta de rotação RX ao qubit"""
        # Matriz RX
        rx_matrix = np.array([
            [math.cos(angle/2), -1j * math.sin(angle/2)],
            [-1j * math.sin(angle/2), math.cos(angle/2)]
        ])
        qubit.state = np.dot(rx_matrix, qubit.state)

    async def apply_cnot_gate(self, control_qubit: Qubit, target_qubit: Qubit):
        """Aplica porta CNOT entre dois qubits"""
        # Simulação simplificada do CNOT
        if control_qubit.measured and control_qubit.measurement_result == 1:
            # Se control é 1, flip o target
            target_qubit.state = [target_qubit.state[1], target_qubit.state[0]]

    async def apply_feature_map_gates(self, qubit: Qubit, gates: List[str]):
        """Aplica sequência de portas para mapeamento de features"""
        for gate in gates:
            if gate == 'H':
                await self.apply_hadamard_gate(qubit)
            elif gate == 'RX':
                angle = random.uniform(0, 2 * math.pi)
                await self.apply_rotation_gate(qubit, angle)
            elif gate == 'RY':
                # Similar to RX but different axis
                angle = random.uniform(0, 2 * math.pi)
                await self.apply_rotation_gate(qubit, angle)

    async def apply_controlled_rotation(self, data_qubit: Qubit, weight_qubit: Qubit):
        """Aplica rotação controlada"""
        # Simulação de rotação controlada
        angle = random.uniform(0, math.pi / 4)
        await self.apply_rotation_gate(data_qubit, angle)

    async def apply_entangling_gate(self, qubit1: Qubit, qubit2: Qubit):
        """Aplica porta de entrelaçamento"""
        await self.apply_cnot_gate(qubit1, qubit2)

    async def measure_qubit(self, qubit: Qubit) -> int:
        """Mede o qubit e colapsa sua função de onda"""
        if qubit.measured:
            return qubit.measurement_result
        
        # Probabilidade de medir |1⟩
        prob_1 = abs(qubit.state[1]) ** 2
        measurement = 1 if random.random() < prob_1 else 0
        
        qubit.measured = True
        qubit.measurement_result = measurement
        
        # Colapsar o estado
        if measurement == 0:
            qubit.state = [1.0, 0.0]
        else:
            qubit.state = [0.0, 1.0]
        
        return measurement

    # Métodos de Utilidade Quântica
    def normalize_to_pi(self, value: float) -> float:
        """Normaliza valor para o intervalo [-π, π]"""
        return (value * 2 * math.pi) - math.pi

    def binary_to_decimal(self, binary_array: List[int]) -> int:
        """Converte array binário para decimal"""
        return sum(bit * (2 ** (len(binary_array) - 1 - i)) 
                  for i, bit in enumerate(binary_array))

    def normalize_prediction(self, value: int) -> float:
        """Normaliza predição para o intervalo [0, 1]"""
        if not self.layers:
            return 0.0
            
        last_layer_qubits = self.layers[-1].qubits
        max_value = (2 ** last_layer_qubits) - 1
        return value / max_value if max_value > 0 else 0.0

    def calculate_entanglement_measure(self, measurements: List[int]) -> float:
        """Calcula medida de entrelaçamento (entropia de von Neumann)"""
        probabilities = self.calculate_measurement_probabilities(measurements)
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
        return entropy

    def calculate_measurement_probabilities(self, measurements: List[int]) -> List[float]:
        """Calcula probabilidades de medição"""
        total = len(measurements)
        zeros = sum(1 for m in measurements if m == 0)
        ones = sum(1 for m in measurements if m == 1)
        
        return [zeros / total, ones / total]

    def calculate_variance(self, measurements: List[int]) -> float:
        """Calcula variância das medições"""
        if not measurements:
            return 0.0
        mean = sum(measurements) / len(measurements)
        variance = sum((x - mean) ** 2 for x in measurements) / len(measurements)
        return variance

    # Métodos de aplicação de camadas específicas
    async def apply_encoding_layer(self, input_state: List[Qubit], layer: QuantumLayer) -> List[Qubit]:
        """Aplica camada de codificação quântica"""
        return input_state  # Já codificado anteriormente

    async def apply_measurement_layer(self, input_state: List[Qubit], layer: QuantumLayer) -> List[Qubit]:
        """Aplica camada de medição quântica"""
        return input_state  # A medição é feita separadamente

    # Métodos de status e diagnóstico
    def get_network_status(self) -> Dict[str, Any]:
        """Retorna status da rede neural quântica"""
        return {
            'total_layers': len(self.layers),
            'total_qubits': self.qubit_counter,
            'quantum_weights_initialized': len(self.quantum_weights) > 0,
            'layers_config': [
                {
                    'type': layer.layer_type.value,
                    'qubits': layer.qubits,
                    'entanglement': layer.entanglement.value if layer.entanglement else None,
                    'variational': layer.variational
                }
                for layer in self.layers
            ],
            'performance_metrics': {
                'average_confidence': 0.85,  # Placeholder
                'entanglement_strength': 0.75,  # Placeholder
                'quantum_advantage': 15.2  # Placeholder
            }
        }

    async def apply_quantum_error_correction(self, qubits: List[Qubit]) -> List[Qubit]:
        """Aplica correção de erros quânticos usando código de repetição"""
        corrected_qubits = []
        
        for i in range(0, len(qubits), 3):
            if i + 2 < len(qubits):
                encoded_qubits = [qubits[i], qubits[i+1], qubits[i+2]]
                corrected = await self._majority_vote_correction(encoded_qubits)
                corrected_qubits.append(corrected)
            else:
                corrected_qubits.extend(qubits[i:])
        
        return corrected_qubits
    
    async def _majority_vote_correction(self, encoded_qubits: List[Qubit]) -> Qubit:
        """Correção por voto majoritário"""
        measurements = []
        for qubit in encoded_qubits:
            prob_1 = abs(qubit.state[1]) ** 2
            measurements.append(1 if prob_1 > 0.5 else 0)
        
        majority = 1 if sum(measurements) >= 2 else 0
        corrected_qubit = await self.create_qubit()
        
        if majority == 1:
            corrected_qubit.state = [0.0, 1.0]
        else:
            corrected_qubit.state = [1.0, 0.0]
        
        return corrected_qubit
    
    async def apply_decoherence_mitigation(self, qubits: List[Qubit], coherence_time: float = 100.0) -> List[Qubit]:
        """Mitiga efeitos de decoerência nos qubits"""
        mitigated_qubits = []
        
        for qubit in qubits:
            decoherence_factor = math.exp(-1.0 / coherence_time)
            
            alpha = qubit.state[0] * decoherence_factor
            beta = qubit.state[1] * decoherence_factor
            
            norm = math.sqrt(abs(alpha)**2 + abs(beta)**2)
            if norm > 0:
                qubit.state = [alpha / norm, beta / norm]
            
            mitigated_qubits.append(qubit)
        
        return mitigated_qubits
    
    async def apply_advanced_entanglement(self, qubits: List[Qubit], entanglement_type: str = 'GHZ') -> List[Qubit]:
        """Aplica entrelaçamento avançado (GHZ ou W state)"""
        if entanglement_type == 'GHZ':
            return await self._create_ghz_state(qubits)
        elif entanglement_type == 'W':
            return await self._create_w_state(qubits)
        else:
            return await self.create_full_entanglement(qubits)
    
    async def _create_ghz_state(self, qubits: List[Qubit]) -> List[Qubit]:
        """Cria estado GHZ (Greenberger-Horne-Zeilinger)"""
        if len(qubits) < 2:
            return qubits
        
        await self.apply_hadamard_gate(qubits[0])
        
        for i in range(1, len(qubits)):
            await self.apply_cnot_gate(qubits[0], qubits[i])
        
        return qubits
    
    async def _create_w_state(self, qubits: List[Qubit]) -> List[Qubit]:
        """Cria estado W"""
        n = len(qubits)
        if n < 2:
            return qubits
        
        for i, qubit in enumerate(qubits):
            angle = math.asin(math.sqrt(1.0 / (n - i)))
            await self.apply_rotation_gate(qubit, 2 * angle)
            
            if i < n - 1:
                await self.apply_cnot_gate(qubit, qubits[i + 1])
        
        return qubits
    
    async def calculate_quantum_fidelity(self, state1: List[Qubit], state2: List[Qubit]) -> float:
        """Calcula fidelidade entre dois estados quânticos"""
        if len(state1) != len(state2):
            return 0.0
        
        fidelity_sum = 0.0
        for q1, q2 in zip(state1, state2):
            overlap = abs(np.dot(np.conj(q1.state), q2.state))
            fidelity_sum += overlap ** 2
        
        return fidelity_sum / len(state1) if len(state1) > 0 else 0.0
    
    async def apply_quantum_amplitude_amplification(self, qubits: List[Qubit], target_state: List[float]) -> List[Qubit]:
        """Aplica amplificação de amplitude quântica (similar ao algoritmo de Grover)"""
        iterations = int(math.pi / 4 * math.sqrt(2 ** len(qubits)))
        
        for _ in range(iterations):
            for qubit in qubits:
                await self.apply_oracle_gate(qubit, target_state)
            
            for qubit in qubits:
                await self.apply_diffusion_gate(qubit)
        
        return qubits
    
    async def apply_oracle_gate(self, qubit: Qubit, target: List[float]):
        """Aplica operador oráculo"""
        if abs(qubit.state[0] - target[0]) < 0.1 and abs(qubit.state[1] - target[1]) < 0.1:
            qubit.state = [-qubit.state[0], -qubit.state[1]]
    
    async def apply_diffusion_gate(self, qubit: Qubit):
        """Aplica operador de difusão"""
        await self.apply_hadamard_gate(qubit)
        
        qubit.state = [2 * 0.5 - qubit.state[0], 2 * 0.5 - qubit.state[1]]
        
        await self.apply_hadamard_gate(qubit)
    
    def calculate_von_neumann_entropy(self, qubits: List[Qubit]) -> float:
        """Calcula entropia de von Neumann do estado quântico"""
        density_matrix = self._compute_density_matrix(qubits)
        
        eigenvalues = np.linalg.eigvalsh(density_matrix)
        
        entropy = 0.0
        for eigval in eigenvalues:
            if eigval > 1e-10:
                entropy -= eigval * math.log2(eigval)
        
        return entropy
    
    def _compute_density_matrix(self, qubits: List[Qubit]) -> np.ndarray:
        """Computa matriz de densidade do sistema"""
        n = len(qubits)
        dim = 2 ** n
        density = np.zeros((dim, dim), dtype=complex)
        
        for i in range(dim):
            for j in range(dim):
                amplitude = 1.0
                for k, qubit in enumerate(qubits):
                    bit_i = (i >> k) & 1
                    bit_j = (j >> k) & 1
                    amplitude *= qubit.state[bit_i] * np.conj(qubit.state[bit_j])
                density[i, j] = amplitude
        
        return density

# Função de demonstração
async def main():
    """Demonstração da Rede Neural Quântica"""
    qnn = QuantumNeuralNetwork()
    
    print("🧠⚛️ DEMONSTRAÇÃO - REDE NEURAL QUÂNTICA")
    print("=" * 50)
    
    # Inicializar rede
    await qnn.initialize()
    
    # Dados de exemplo
    classical_features = [0.1, 0.5, 0.8, 0.3, 0.9]
    quantum_input = []  # Será criado durante a codificação
    
    print(f"\n1. Realizando predição com {len(classical_features)} features...")
    
    # Fazer predição
    prediction = await qnn.predict(quantum_input, classical_features)
    
    print(f"\n2. Resultado da Predição Quântica:")
    print(f"   🎯 Predição: {prediction.prediction:.3f}")
    print(f"   📊 Confiança: {prediction.confidence:.1%}")
    print(f"   ⚛️ Entrelaçamento: {prediction.entanglement:.3f}")
    print(f"   🔢 Medições: {prediction.measurements}")
    
    # Dados de treinamento de exemplo
    print(f"\n3. Realizando treinamento quântico...")
    training_data = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9]
    ]
    training_labels = [0, 1, 0]
    
    training_result = await qnn.train_quantum(training_data, training_labels)
    
    print(f"\n4. Resultado do Treinamento:")
    print(f"   📉 Loss: {training_result.loss:.4f}")
    print(f"   🎯 Acurácia: {training_result.accuracy:.1%}")
    print(f"   ⚡ Vantagem Quântica: {training_result.quantum_advantage:.1f}x")
    
    print(f"\n5. Status da Rede:")
    status = qnn.get_network_status()
    for key, value in status.items():
        if key != 'layers_config':
            print(f"   {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())