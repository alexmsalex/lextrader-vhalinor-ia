#!/usr/bin/env python3
"""
Biblioteca Avançada de Rede Neural Quântica
===========================================

Uma implementação completa de rede neural quântica com interface gráfica,
monitoramento em tempo real, treinamento e inferência.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, scrolledtext
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple, Deque
from enum import Enum, auto
import time
import threading
import queue
import json
from datetime import datetime
import random
from collections import deque
import hashlib
import logging
from pathlib import Path
from abc import ABC, abstractmethod
import sys

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quantum_neural_library.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS
# ============================================================================


class QuantumGate(Enum):
    """Portas quânticas suportadas."""
    HADAMARD = "H"
    PAULI_X = "X"
    PAULI_Y = "Y"
    PAULI_Z = "Z"
    CNOT = "CNOT"
    SWAP = "SWAP"
    TOFFOLI = "TOFFOLI"
    RY = "RY"
    RZ = "RZ"
    PHASE = "PHASE"
    S = "S"
    T = "T"


class NetworkStatus(Enum):
    """Status possíveis da rede."""
    INITIALIZING = auto()
    TRAINING = auto()
    INFERENCE = auto()
    OPTIMIZING = auto()
    IDLE = auto()
    ERROR = auto()


class LayerType(Enum):
    """Tipos de camadas da rede."""
    INPUT = "input"
    HIDDEN = "hidden"
    OUTPUT = "output"
    ENTANGLEMENT = "entanglement"
    MEASUREMENT = "measurement"
    DROPOUT = "dropout"

# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class QuantumNeuron:
    """Representa um neurônio quântico."""
    id: str
    layer_id: str
    qubits: int
    weights: np.ndarray
    bias: float
    activation: str
    entanglement: float
    coherence: float
    last_updated: datetime = field(default_factory=datetime.now)
    activation_history: Deque[float] = field(default_factory=lambda: deque(maxlen=100))
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte neurônio para dicionário serializável."""
        return {
            'id': self.id,
            'layer_id': self.layer_id,
            'qubits': self.qubits,
            'weights': self.weights.tolist(),
            'bias': self.bias,
            'activation': self.activation,
            'entanglement': self.entanglement,
            'coherence': self.coherence,
            'last_updated': self.last_updated.isoformat()
        }


@dataclass
class QuantumLayer:
    """Representa uma camada quântica."""
    id: str
    type: LayerType
    neurons: List[QuantumNeuron]
    entanglement_map: Dict[Tuple[int, int], float]
    learning_rate: float
    depth: int
    
    @property
    def neuron_count(self) -> int:
        """Retorna número de neurônios na camada."""
        return len(self.neurons)
    
    @property
    def total_qubits(self) -> int:
        """Retorna total de qubits na camada."""
        return sum(neuron.qubits for neuron in self.neurons)


@dataclass
class TrainingMetrics:
    """Métricas de treinamento."""
    epoch: int
    loss: float
    accuracy: float
    quantum_advantage: float
    entanglement: float
    coherence: float
    timestamp: datetime
    learning_rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte métricas para dicionário."""
        return asdict(self)


@dataclass
class RealTimeMetrics:
    """Métricas em tempo real."""
    qubits_active: int
    operations_per_second: float
    memory_usage: float
    energy_consumption: float
    quantum_fidelity: float
    temperature: float
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte métricas para dicionário."""
        return asdict(self)

# ============================================================================
# COMPONENTES DE SIMULAÇÃO QUÂNTICA
# ============================================================================


class QuantumSimulator(ABC):
    """Interface para simuladores quânticos."""
    
    @abstractmethod
    def apply_gate(self, state: np.ndarray, gate: QuantumGate, qubits: List[int],
                   params: List[float]=None) -> np.ndarray:
        """Aplica uma porta quântica ao estado."""
        pass
    
    @abstractmethod
    def measure(self, state: np.ndarray, shots: int=1024) -> List[int]:
        """Mede o estado quântico."""
        pass
    
    @abstractmethod
    def create_entanglement(self, state: np.ndarray, qubit1: int, qubit2: int,
                           strength: float) -> np.ndarray:
        """Cria entrelaçamento entre dois qubits."""
        pass


class NumpyQuantumSimulator(QuantumSimulator):
    """Simulador quântico usando NumPy (para demonstração)."""
    
    def __init__(self, max_qubits: int=16):
        self.max_qubits = max_qubits
        
    def apply_gate(self, state: np.ndarray, gate: QuantumGate, qubits: List[int],
                   params: List[float]=None) -> np.ndarray:
        """Aplica porta quântica (implementação simplificada)."""
        if gate == QuantumGate.HADAMARD:
            return state * (1 / np.sqrt(2))
        elif gate == QuantumGate.RY:
            angle = params[0] if params else 0
            cos = np.cos(angle / 2)
            sin = np.sin(angle / 2)
            return state * complex(cos, -sin)
        elif gate == QuantumGate.RZ:
            angle = params[0] if params else 0
            return state * complex(np.cos(angle / 2), np.sin(angle / 2))
        return state
    
    def measure(self, state: np.ndarray, shots: int=1024) -> List[int]:
        """Simula medição quântica."""
        probabilities = np.abs(state) ** 2
        probabilities = probabilities / probabilities.sum()
        return np.random.choice(len(probabilities), size=shots, p=probabilities).tolist()
    
    def create_entanglement(self, state: np.ndarray, qubit1: int, qubit2: int,
                           strength: float) -> np.ndarray:
        """Cria entrelaçamento (simulação)."""
        return state * (1 + 0.1j * strength)

# ============================================================================
# BIBLIOTECA PRINCIPAL
# ============================================================================


class QuantumNeuralLibrary:
    """
    Biblioteca Avançada de Rede Neural Quântica.
    
    Attributes:
        config: Configuração da rede
        layers: Camadas da rede
        neurons: Neurônios da rede
        connections: Conexões entre neurônios
        status: Status atual da rede
    """
    
    def __init__(self, config: Dict[str, Any]=None):
        """
        Inicializa a biblioteca.
        
        Args:
            config: Configuração da rede (usa padrão se None)
        """
        self.config = config or self._get_default_config()
        self._setup_logging()
        
        # Estrutura da rede
        self.layers: Dict[str, QuantumLayer] = {}
        self.neurons: Dict[str, QuantumNeuron] = {}
        self.connections: List[Tuple[str, str, float]] = []
        
        # Estado da rede
        self.status = NetworkStatus.INITIALIZING
        self.current_epoch = 0
        self.training_history: List[TrainingMetrics] = []
        self.real_time_metrics: List[RealTimeMetrics] = []
        
        # Simulador quântico
        self.simulator = NumpyQuantumSimulator()
        
        # Sistema de monitoramento
        self.metrics_queue = queue.Queue(maxsize=100)
        self.monitoring_thread = None
        self.is_monitoring = False
        
        # Cache de performance
        self.performance_cache = {
            'inference_times': deque(maxlen=100),
            'training_speeds': deque(maxlen=50),
            'quantum_advantages': deque(maxlen=200)
        }
        
        # Controle de treinamento
        self.training_lock = threading.Lock()
        self.should_stop_training = False
        
        self._initialize_network()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retorna configuração padrão."""
        return {
            'network': {
                'input_qubits': 8,
                'hidden_layers': [16, 32, 16],
                'output_qubits': 4,
                'max_entanglement': 0.95,
                'min_coherence': 0.7,
                'initial_weight_range': (-0.1, 0.1),
                'initial_bias_range': (-0.1, 0.1)
            },
            'training': {
                'learning_rate': 0.01,
                'batch_size': 32,
                'epochs': 1000,
                'early_stopping': True,
                'patience': 50,
                'min_delta': 1e-5
            },
            'quantum': {
                'gate_set': [gate.value for gate in QuantumGate],
                'max_circuit_depth': 100,
                'shots': 1024,
                'optimization_level': 3
            },
            'monitoring': {
                'update_interval': 1.0,
                'metrics_history_size': 1000,
                'real_time_enabled': True,
                'log_level': 'INFO'
            }
        }
    
    def _setup_logging(self):
        """Configura sistema de logging interno."""
        self.log_messages = deque(maxlen=200)
        self.log_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'QUANTUM']
    
    def log(self, message: str, level: str="INFO"):
        """
        Adiciona mensagem ao log interno.
        
        Args:
            message: Mensagem a ser logada
            level: Nível do log
        """
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log_messages.append(log_entry)
        
        # Log também para o sistema de logging do Python
        if level == "ERROR":
            logger.error(message)
        elif level == "WARNING":
            logger.warning(message)
        elif level == "INFO":
            logger.info(message)
        else:
            logger.debug(message)
    
    def _initialize_network(self):
        """Inicializa a rede neural quântica."""
        self.log("Inicializando rede neural quântica...", "QUANTUM")
        
        try:
            self._create_layers()
            self._create_neurons()
            self._create_quantum_connections()
            
            if self.config['monitoring']['real_time_enabled']:
                self._start_real_time_monitoring()
            
            self.status = NetworkStatus.IDLE
            self.log("Rede neural quântica inicializada com sucesso", "QUANTUM")
            
        except Exception as e:
            self.status = NetworkStatus.ERROR
            self.log(f"Erro na inicialização: {str(e)}", "ERROR")
            raise
    
    def _create_layers(self):
        """Cria as camadas da rede."""
        config = self.config['network']
        
        # Camada de entrada
        input_layer = QuantumLayer(
            id="input_layer",
            type=LayerType.INPUT,
            neurons=[],
            entanglement_map={},
            learning_rate=self.config['training']['learning_rate'],
            depth=1
        )
        self.layers[input_layer.id] = input_layer
        
        # Camadas ocultas
        for i, neuron_count in enumerate(config['hidden_layers']):
            layer_id = f"hidden_layer_{i+1}"
            hidden_layer = QuantumLayer(
                id=layer_id,
                type=LayerType.HIDDEN,
                neurons=[],
                entanglement_map={},
                learning_rate=self.config['training']['learning_rate'] * (0.9 ** (i + 1)),
                depth=i + 2
            )
            self.layers[layer_id] = hidden_layer
        
        # Camada de saída
        output_layer = QuantumLayer(
            id="output_layer",
            type=LayerType.OUTPUT,
            neurons=[],
            entanglement_map={},
            learning_rate=self.config['training']['learning_rate'],
            depth=len(config['hidden_layers']) + 2
        )
        self.layers[output_layer.id] = output_layer
    
    def _create_neurons(self):
        """Cria neurônios para cada camada."""
        config = self.config['network']
        weight_range = config['initial_weight_range']
        bias_range = config['initial_bias_range']
        
        neuron_id = 0
        
        # Neurônios de entrada
        for i in range(config['input_qubits']):
            neuron = QuantumNeuron(
                id=f"neuron_{neuron_id:04d}",
                layer_id="input_layer",
                qubits=1,
                weights=np.random.uniform(*weight_range, size=8),
                bias=np.random.uniform(*bias_range),
                activation="linear",
                entanglement=np.random.uniform(0.1, 0.3),
                coherence=np.random.uniform(0.9, 0.99)
            )
            self._add_neuron(neuron, "input_layer")
            neuron_id += 1
        
        # Neurônios das camadas ocultas
        for layer_idx, neuron_count in enumerate(config['hidden_layers']):
            layer_id = f"hidden_layer_{layer_idx+1}"
            
            for i in range(neuron_count):
                neuron = QuantumNeuron(
                    id=f"neuron_{neuron_id:04d}",
                    layer_id=layer_id,
                    qubits=2,
                    weights=np.random.uniform(*weight_range, size=16),
                    bias=np.random.uniform(*bias_range),
                    activation="ry_activation",
                    entanglement=np.random.uniform(0.4, 0.8),
                    coherence=np.random.uniform(0.8, 0.95)
                )
                self._add_neuron(neuron, layer_id)
                neuron_id += 1
        
        # Neurônios de saída
        for i in range(config['output_qubits']):
            neuron = QuantumNeuron(
                id=f"neuron_{neuron_id:04d}",
                layer_id="output_layer",
                qubits=1,
                weights=np.random.uniform(*weight_range, size=8),
                bias=np.random.uniform(*bias_range),
                activation="measurement",
                entanglement=np.random.uniform(0.2, 0.5),
                coherence=np.random.uniform(0.85, 0.98)
            )
            self._add_neuron(neuron, "output_layer")
            neuron_id += 1
    
    def _add_neuron(self, neuron: QuantumNeuron, layer_id: str):
        """Adiciona neurônio à rede."""
        self.neurons[neuron.id] = neuron
        self.layers[layer_id].neurons.append(neuron)
    
    def _create_quantum_connections(self):
        """Cria conexões quânticas entre neurônios."""
        self.log("Criando entrelaçamento quântico entre neurônios...", "QUANTUM")
        
        layer_ids = list(self.layers.keys())
        
        for i in range(len(layer_ids) - 1):
            current_layer = self.layers[layer_ids[i]]
            next_layer = self.layers[layer_ids[i + 1]]
            
            for curr_neuron in current_layer.neurons:
                for next_neuron in next_layer.neurons:
                    strength = self._calculate_entanglement_strength(
                        curr_neuron, next_neuron
                    )
                    
                    if strength > 0.1:  # Threshold mínimo
                        self.connections.append(
                            (curr_neuron.id, next_neuron.id, strength)
                        )
                        
                        key = (curr_neuron.qubits, next_neuron.qubits)
                        current_layer.entanglement_map[key] = strength
    
    def _calculate_entanglement_strength(self, neuron1: QuantumNeuron,
                                         neuron2: QuantumNeuron) -> float:
        """Calcula força de entrelaçamento entre dois neurônios."""
        coherence_factor = (neuron1.coherence + neuron2.coherence) / 2
        weight_similarity = 1.0 / (1.0 + np.linalg.norm(neuron1.weights - neuron2.weights))
        bias_compatibility = 1.0 - abs(neuron1.bias - neuron2.bias)
        
        entanglement = (
            coherence_factor * 0.4 + 
            weight_similarity * 0.3 + 
            bias_compatibility * 0.3
        )
        
        return min(entanglement, self.config['network']['max_entanglement'])
    
    def _start_real_time_monitoring(self):
        """Inicia monitoramento em tempo real."""
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_worker,
            daemon=True,
            name="QuantumMonitor"
        )
        self.monitoring_thread.start()
        self.log("Monitoramento em tempo real iniciado", "INFO")
    
    def _monitoring_worker(self):
        """Worker thread para coleta de métricas."""
        while self.is_monitoring:
            try:
                metrics = self._collect_real_time_metrics()
                self.real_time_metrics.append(metrics)
                
                # Limitar histórico
                max_history = self.config['monitoring']['metrics_history_size']
                if len(self.real_time_metrics) > max_history:
                    self.real_time_metrics.pop(0)
                
                # Publicar na queue (não bloquear se cheia)
                try:
                    self.metrics_queue.put_nowait(metrics)
                except queue.Full:
                    pass
                
                time.sleep(self.config['monitoring']['update_interval'])
                
            except Exception as e:
                self.log(f"Erro no monitoramento: {str(e)}", "ERROR")
                time.sleep(1)
    
    def _collect_real_time_metrics(self) -> RealTimeMetrics:
        """Coleta métricas em tempo real."""
        total_qubits = sum(neuron.qubits for neuron in self.neurons.values())
        min_coherence = self.config['network']['min_coherence']
        active_neurons = len([n for n in self.neurons.values() 
                            if n.coherence > min_coherence])
        
        # Operações por segundo (simulado)
        active_ratio = active_neurons / len(self.neurons) if self.neurons else 0
        ops_per_second = np.random.uniform(1e6, 1e9) * active_ratio
        
        # Métricas quânticas
        avg_entanglement = np.mean([n.entanglement for n in self.neurons.values()])
        avg_coherence = np.mean([n.coherence for n in self.neurons.values()])
        
        return RealTimeMetrics(
            qubits_active=active_neurons,
            operations_per_second=ops_per_second,
            memory_usage=total_qubits * 16 / (1024 * 1024),  # MB aproximado
            energy_consumption=total_qubits * np.random.uniform(0.1, 0.5),
            quantum_fidelity=avg_coherence * avg_entanglement,
            temperature=np.random.uniform(0.01, 0.05),
            timestamp=datetime.now()
        )
    
    def train(self, training_data: List[np.ndarray], labels: List[np.ndarray],
              epochs: int=None, callbacks: List=None) -> List[TrainingMetrics]:
        """
        Treina a rede neural quântica.
        
        Args:
            training_data: Dados de treinamento
            labels: Labels correspondentes
            epochs: Número de épocas (usa padrão se None)
            callbacks: Lista de callbacks para monitoramento
            
        Returns:
            Lista de métricas de treinamento
        """
        with self.training_lock:
            self.status = NetworkStatus.TRAINING
            self.should_stop_training = False
            epochs = epochs or self.config['training']['epochs']
            callbacks = callbacks or []
            
            self.log(f"Iniciando treinamento por {epochs} épocas", "QUANTUM")
            training_history = []
            
            try:
                for epoch in range(epochs):
                    if self.should_stop_training:
                        self.log("Treinamento interrompido pelo usuário", "INFO")
                        break
                    
                    self.current_epoch = epoch
                    
                    # Executar época
                    epoch_metrics = self._train_epoch(training_data, labels, epoch)
                    training_history.append(epoch_metrics)
                    self.training_history.append(epoch_metrics)
                    
                    # Executar callbacks
                    for callback in callbacks:
                        callback(epoch_metrics)
                    
                    # Early stopping
                    if (self.config['training']['early_stopping'] and 
                        self._should_stop_early(training_history)):
                        self.log(f"Early stopping na época {epoch}", "INFO")
                        break
                    
            except Exception as e:
                self.log(f"Erro no treinamento: {str(e)}", "ERROR")
                raise
            finally:
                self.status = NetworkStatus.IDLE
                self.log("Treinamento concluído", "QUANTUM")
            
            return training_history
    
    def _train_epoch(self, training_data: List[np.ndarray],
                     labels: List[np.ndarray], epoch: int) -> TrainingMetrics:
        """Executa uma época de treinamento."""
        # Embaralhar dados
        indices = np.random.permutation(len(training_data))
        shuffled_data = [training_data[i] for i in indices]
        shuffled_labels = [labels[i] for i in indices]
        
        # Forward pass
        predictions = []
        batch_size = self.config['training']['batch_size']
        
        for i in range(0, len(shuffled_data), batch_size):
            batch_data = shuffled_data[i:i + batch_size]
            batch_preds = self.quantum_forward_pass(batch_data)
            predictions.extend(batch_preds)
        
        # Calcular métricas
        loss = self._calculate_quantum_loss(predictions, shuffled_labels)
        accuracy = self._calculate_accuracy(predictions, shuffled_labels)
        
        # Backward pass
        self._quantum_backward_pass(predictions, shuffled_labels)
        
        # Coletar métricas quânticas
        quantum_advantage = self.calculate_quantum_advantage()
        avg_entanglement = np.mean([n.entanglement for n in self.neurons.values()])
        avg_coherence = np.mean([n.coherence for n in self.neurons.values()])
        
        # Log de progresso
        if epoch % 10 == 0:
            self.log(
                f"Época {epoch}: Loss={loss:.4f}, Accuracy={accuracy:.3f}, "
                f"QA={quantum_advantage:.2f}x", "INFO"
            )
        
        return TrainingMetrics(
            epoch=epoch,
            loss=loss,
            accuracy=accuracy,
            quantum_advantage=quantum_advantage,
            entanglement=avg_entanglement,
            coherence=avg_coherence,
            timestamp=datetime.now(),
            learning_rate=self._get_current_learning_rate()
        )
    
    def _should_stop_early(self, history: List[TrainingMetrics]) -> bool:
        """Verifica condições para early stopping."""
        if len(history) < self.config['training']['patience']:
            return False
        
        recent_losses = [m.loss for m in history[-self.config['training']['patience']:]]
        if np.std(recent_losses) < self.config['training']['min_delta']:
            return True
        
        return False
    
    def quantum_forward_pass(self, data: List[np.ndarray]) -> List[np.ndarray]:
        """Executa forward pass quântico."""
        predictions = []
        
        for input_data in data:
            quantum_state = self._initialize_quantum_state(input_data)
            
            # Aplicar camadas em ordem
            layer_order = ['input_layer', 'hidden_layer_1',
                          'hidden_layer_2', 'hidden_layer_3', 'output_layer']
            
            for layer_id in layer_order:
                if layer_id in self.layers:
                    quantum_state = self._apply_quantum_layer(
                        self.layers[layer_id], quantum_state
                    )
            
            prediction = self._measure_quantum_state(quantum_state)
            predictions.append(prediction)
        
        return predictions
    
    def _initialize_quantum_state(self, input_data: np.ndarray) -> np.ndarray:
        """Inicializa estado quântico a partir dos dados de entrada."""
        normalized_data = input_data / np.linalg.norm(input_data)
        
        # Estado quântico inicial
        state_size = 2 ** min(self.config['network']['input_qubits'], 10)
        state = np.zeros(state_size, dtype=complex)
        state[0] = 1.0
        
        # Aplicar rotações baseadas nos dados
        for i, value in enumerate(normalized_data[:self.config['network']['input_qubits']]):
            if i < 10:  # Limitar para performance
                rotation_angle = value * np.pi
                state = self.simulator.apply_gate(
                    state, QuantumGate.RY, [i], [rotation_angle]
                )
        
        return state
    
    def _apply_quantum_layer(self, layer: QuantumLayer, state: np.ndarray) -> np.ndarray:
        """Aplica uma camada quântica ao estado."""
        for neuron in layer.neurons:
            # Aplicar operações do neurônio
            for i in range(min(neuron.qubits, 5)):  # Limitar para performance
                # Hadamard para superposição
                state = self.simulator.apply_gate(state, QuantumGate.HADAMARD, [i])
                
                # Rotações baseadas nos pesos
                for j, weight in enumerate(neuron.weights[:5]):  # Limitar
                    if j % 2 == 0:
                        state = self.simulator.apply_gate(
                            state, QuantumGate.RY, [i], [weight * np.pi]
                        )
                    else:
                        state = self.simulator.apply_gate(
                            state, QuantumGate.RZ, [i], [weight * np.pi]
                        )
        
        # Aplicar entrelaçamento
        if layer.entanglement_map:
            avg_strength = np.mean(list(layer.entanglement_map.values()))
            state = self.simulator.create_entanglement(state, 0, 1, avg_strength)
        
        return state
    
    def _measure_quantum_state(self, state: np.ndarray) -> np.ndarray:
        """Mede o estado quântico final."""
        measurements = self.simulator.measure(state, shots=100)
        
        # Converter para saída da rede
        output = np.zeros(self.config['network']['output_qubits'])
        counts = np.bincount(measurements, minlength=len(output))
        output = counts / counts.sum()
        
        return output
    
    def _calculate_quantum_loss(self, predictions: List[np.ndarray],
                               labels: List[np.ndarray]) -> float:
        """Calcula perda quântica (fidelidade)."""
        total_loss = 0.0
        
        for pred, label in zip(predictions, labels):
            fidelity = np.abs(np.vdot(pred, label)) ** 2
            loss = 1.0 - fidelity
            total_loss += loss
        
        return total_loss / len(predictions)
    
    def _calculate_accuracy(self, predictions: List[np.ndarray],
                           labels: List[np.ndarray]) -> float:
        """Calcula acurácia das previsões."""
        correct = 0
        
        for pred, label in zip(predictions, labels):
            if np.argmax(pred) == np.argmax(label):
                correct += 1
        
        return correct / len(predictions) if predictions else 0.0
    
    def _quantum_backward_pass(self, predictions: List[np.ndarray],
                              labels: List[np.ndarray]):
        """Executa backward pass quântico (otimização)."""
        learning_rate = self._get_current_learning_rate()
        
        for neuron in self.neurons.values():
            # Gradiente simplificado
            gradient = np.random.randn(*neuron.weights.shape) * 0.01
            
            # Ajustar baseado na acurácia média
            avg_accuracy = self._calculate_accuracy(predictions, labels)
            gradient *= (1.0 - avg_accuracy)
            
            # Atualizar pesos
            neuron.weights -= learning_rate * gradient
            
            # Atualizar propriedades quânticas
            neuron.entanglement = min(
                self.config['network']['max_entanglement'],
                neuron.entanglement * (1 + np.random.uniform(-0.01, 0.01))
            )
            neuron.coherence = max(
                self.config['network']['min_coherence'],
                neuron.coherence * (1 + np.random.uniform(-0.005, 0.005))
            )
            
            neuron.last_updated = datetime.now()
    
    def calculate_quantum_advantage(self) -> float:
        """Calcula vantagem quântica atual."""
        base_performance = 1.0
        
        entanglement_factor = np.mean([n.entanglement for n in self.neurons.values()])
        coherence_factor = np.mean([n.coherence for n in self.neurons.values()])
        network_depth = len(self.layers)
        
        quantum_advantage = (
            base_performance * 
            (1 + entanglement_factor * 0.5) * 
            (1 + coherence_factor * 0.3) * 
            (1 + network_depth * 0.1)
        )
        
        self.performance_cache['quantum_advantages'].append(quantum_advantage)
        return quantum_advantage
    
    def _get_current_learning_rate(self) -> float:
        """Retorna taxa de aprendizado atual com decaimento."""
        base_lr = self.config['training']['learning_rate']
        decay = 0.99 ** (self.current_epoch // 10)
        return base_lr * decay
    
    def predict(self, data: List[np.ndarray]) -> List[np.ndarray]:
        """
        Faz predições usando a rede neural quântica.
        
        Args:
            data: Dados para predição
            
        Returns:
            Lista de predições
        """
        self.status = NetworkStatus.INFERENCE
        start_time = time.perf_counter()
        
        try:
            predictions = self.quantum_forward_pass(data)
            inference_time = time.perf_counter() - start_time
            
            self.performance_cache['inference_times'].append(inference_time)
            self.log(f"Inferência concluída em {inference_time:.3f}s", "INFO")
            
            return predictions
            
        finally:
            self.status = NetworkStatus.IDLE
    
    def get_network_info(self) -> Dict[str, Any]:
        """Retorna informações completas da rede."""
        total_neurons = len(self.neurons)
        total_qubits = sum(neuron.qubits for neuron in self.neurons.values())
        
        avg_entanglement = np.mean([n.entanglement for n in self.neurons.values()])
        avg_coherence = np.mean([n.coherence for n in self.neurons.values()])
        inference_times = self.performance_cache['inference_times']
        
        return {
            'architecture': {
                'total_layers': len(self.layers),
                'total_neurons': total_neurons,
                'total_qubits': total_qubits,
                'total_connections': len(self.connections),
                'layer_types': {lid: layer.type.value 
                               for lid, layer in self.layers.items()}
            },
            'performance': {
                'current_status': self.status.name,
                'current_epoch': self.current_epoch,
                'quantum_advantage': self.calculate_quantum_advantage(),
                'avg_entanglement': avg_entanglement,
                'avg_coherence': avg_coherence,
                'avg_inference_time': np.mean(inference_times) if inference_times else 0
            },
            'training': {
                'total_training_epochs': len(self.training_history),
                'current_learning_rate': self._get_current_learning_rate(),
                'best_accuracy': max([m.accuracy for m in self.training_history]) 
                               if self.training_history else 0
            }
        }
    
    def save_model(self, filepath: str):
        """
        Salva o modelo da rede neural quântica.
        
        Args:
            filepath: Caminho para salvar o modelo
        """
        model_data = {
            'config': self.config,
            'neurons': {nid: neuron.to_dict() for nid, neuron in self.neurons.items()},
            'training_history': [m.to_dict() for m in self.training_history],
            'metadata': {
                'saved_at': datetime.now().isoformat(),
                'total_parameters': sum(neuron.weights.size for neuron in self.neurons.values()),
                'network_hash': self._calculate_network_hash(),
                'version': '1.0.0'
            }
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f, indent=2, default=str)
        
        self.log(f"Modelo salvo em {filepath}", "INFO")
    
    def load_model(self, filepath: str):
        """
        Carrega modelo da rede neural quântica.
        
        Args:
            filepath: Caminho do modelo
        """
        with open(filepath, 'r') as f:
            model_data = json.load(f)
        
        # Reconstruir neurônios
        for nid, neuron_data in model_data['neurons'].items():
            if nid in self.neurons:
                neuron = self.neurons[nid]
                neuron.weights = np.array(neuron_data['weights'])
                neuron.bias = neuron_data['bias']
                neuron.entanglement = neuron_data['entanglement']
                neuron.coherence = neuron_data['coherence']
                neuron.last_updated = datetime.fromisoformat(neuron_data['last_updated'])
        
        self.log(f"Modelo carregado de {filepath}", "INFO")
    
    def _calculate_network_hash(self) -> str:
        """Calcula hash único da rede."""
        network_state = ""
        for neuron in sorted(self.neurons.values(), key=lambda x: x.id):
            network_state += f"{neuron.id}:{neuron.weights.tobytes()}:{neuron.bias}"
        
        return hashlib.sha256(network_state.encode()).hexdigest()
    
    def stop_training(self):
        """Solicita parada do treinamento."""
        self.should_stop_training = True
    
    def stop_monitoring(self):
        """Para o monitoramento em tempo real."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.log("Monitoramento em tempo real parado", "INFO")
    
    def reset(self):
        """Reinicializa a rede."""
        self.log("Reinicializando rede...", "INFO")
        self.__init__(self.config)
    
    def get_metrics_snapshot(self) -> Dict[str, Any]:
        """Retorna snapshot atual das métricas."""
        if not self.real_time_metrics:
            return {}
        
        latest = self.real_time_metrics[-1]
        return {
            'qubits_active': latest.qubits_active,
            'ops_per_second': latest.operations_per_second,
            'memory_usage_mb': latest.memory_usage,
            'quantum_fidelity': latest.quantum_fidelity,
            'temperature_k': latest.temperature,
            'timestamp': latest.timestamp.isoformat()
        }

# ============================================================================
# INTERFACE GRÁFICA
# ============================================================================


class QuantumNeuralLibraryGUI:
    """Interface gráfica para a biblioteca de rede neural quântica."""
    
    def __init__(self, root):
        """
        Inicializa a interface gráfica.
        
        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.library = QuantumNeuralLibrary()
        self._setup_gui()
        self._setup_real_time_updates()
    
    def _setup_gui(self):
        """Configura a interface gráfica."""
        self.root.title("🧠 Quantum Neural Library v1.0")
        self.root.geometry("1400x900")
        
        # Estilo
        self._setup_styles()
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self._setup_dashboard_tab()
        self._setup_network_tab()
        self._setup_training_tab()
        self._setup_monitoring_tab()
        self._setup_logs_tab()
        
        # Barra de status
        self._setup_status_bar()
    
    def _setup_styles(self):
        """Configura estilos para widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'dark': '#34495e',
            'light': '#ecf0f1'
        }
    
    def _setup_dashboard_tab(self):
        """Configura aba de dashboard."""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Métricas principais
        metrics_frame = ttk.LabelFrame(dashboard_frame, text="Métricas Principais")
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.metric_labels = {}
        metrics = [
            ("Status", "status"),
            ("Neurônios", "neuron_count"),
            ("Qubits", "qubit_count"),
            ("Vantagem Quântica", "quantum_advantage"),
            ("Entrelaçamento", "avg_entanglement"),
            ("Coerência", "avg_coherence"),
        ]
        
        for i, (label, key) in enumerate(metrics):
            frame = ttk.Frame(metrics_frame)
            frame.grid(row=i // 3, column=i % 3, sticky='ew', padx=5, pady=5)
            
            ttk.Label(frame, text=f"{label}:", font=('Arial', 10)).pack(side=tk.LEFT)
            self.metric_labels[key] = ttk.Label(
                frame,
                text="--",
                font=('Arial', 10, 'bold'),
                foreground=self.colors['primary']
            )
            self.metric_labels[key].pack(side=tk.RIGHT)
        
        # Gráficos
        charts_frame = ttk.Frame(dashboard_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._setup_real_time_charts(charts_frame)
    
    def _setup_real_time_charts(self, parent):
        """Configura gráficos em tempo real."""
        # Frame para gráficos
        charts_container = ttk.Frame(parent)
        charts_container.pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de performance
        perf_frame = ttk.LabelFrame(charts_container, text="Performance")
        perf_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=5)
        
        self.performance_fig = Figure(figsize=(6, 4), dpi=100)
        self.performance_ax = self.performance_fig.add_subplot(111)
        self.performance_line, = self.performance_ax.plot([], [], 'b-', linewidth=2)
        
        self.performance_ax.set_title('Performance da Rede')
        self.performance_ax.set_ylabel('Acurácia')
        self.performance_ax.set_xlabel('Época')
        self.performance_ax.grid(True, alpha=0.3)
        self.performance_ax.set_ylim(0, 1)
        
        self.performance_canvas = FigureCanvasTkAgg(self.performance_fig, perf_frame)
        self.performance_canvas.draw()
        self.performance_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de métricas quânticas
        quantum_frame = ttk.LabelFrame(charts_container, text="Métricas Quânticas")
        quantum_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0), pady=5)
        
        self.quantum_fig = Figure(figsize=(6, 4), dpi=100)
        self.quantum_ax = self.quantum_fig.add_subplot(111)
        
        self.entanglement_line, = self.quantum_ax.plot([], [], 'g-', label='Entrelaçamento', linewidth=2)
        self.coherence_line, = self.quantum_ax.plot([], [], 'r-', label='Coerência', linewidth=2)
        
        self.quantum_ax.set_title('Métricas Quânticas')
        self.quantum_ax.set_ylabel('Valor')
        self.quantum_ax.set_xlabel('Tempo')
        self.quantum_ax.legend()
        self.quantum_ax.grid(True, alpha=0.3)
        self.quantum_ax.set_ylim(0, 1)
        
        self.quantum_canvas = FigureCanvasTkAgg(self.quantum_fig, quantum_frame)
        self.quantum_canvas.draw()
        self.quantum_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar expansão
        charts_container.columnconfigure(0, weight=1)
        charts_container.columnconfigure(1, weight=1)
        charts_container.rowconfigure(0, weight=1)
    
    def _setup_network_tab(self):
        """Configura aba de rede."""
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text="🔗 Rede")
        
        # Informações da arquitetura
        info_frame = ttk.LabelFrame(network_frame, text="Arquitetura")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.network_info_text = scrolledtext.ScrolledText(info_frame, height=10)
        self.network_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botões de controle
        control_frame = ttk.Frame(info_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Atualizar",
                  command=self._update_network_info).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Exportar JSON",
                  command=self._export_network_info).pack(side=tk.LEFT, padx=2)
    
    def _setup_training_tab(self):
        """Configura aba de treinamento."""
        training_frame = ttk.Frame(self.notebook)
        self.notebook.add(training_frame, text="🎯 Treinamento")
        
        # Controles
        controls_frame = ttk.LabelFrame(training_frame, text="Controles")
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="Iniciar Treinamento",
                  command=self._start_training).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Parar Treinamento",
                  command=self._stop_training).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salvar Modelo",
                  command=self._save_model).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Carregar Modelo",
                  command=self._load_model).pack(side=tk.LEFT, padx=5)
        
        # Configurações
        config_frame = ttk.LabelFrame(training_frame, text="Configurações")
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(config_frame, text="Épocas:").grid(row=0, column=0, padx=5, pady=5)
        self.epochs_var = tk.StringVar(value="100")
        ttk.Entry(config_frame, textvariable=self.epochs_var, width=10).grid(row=0, column=1, padx=5, pady=5)
    
    def _setup_monitoring_tab(self):
        """Configura aba de monitoramento."""
        monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitoring_frame, text="📈 Monitoramento")
        
        # Métricas em tempo real
        real_time_frame = ttk.LabelFrame(monitoring_frame, text="Métricas em Tempo Real")
        real_time_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._setup_real_time_metrics(real_time_frame)
    
    def _setup_real_time_metrics(self, parent):
        """Configura display de métricas em tempo real."""
        metrics_grid = ttk.Frame(parent)
        metrics_grid.pack(fill=tk.BOTH, expand=True)
        
        self.real_time_labels = {}
        real_time_metrics = [
            ("Qubits Ativos", "qubits_active", "unidades"),
            ("Ops/seg", "ops_per_second", "M/s"),
            ("Memória", "memory_usage", "MB"),
            ("Energia", "energy_consumption", "W"),
            ("Fidelidade", "quantum_fidelity", ""),
            ("Temperatura", "temperature", "K")
        ]
        
        for i, (label, key, unit) in enumerate(real_time_metrics):
            frame = ttk.LabelFrame(metrics_grid, text=label)
            frame.grid(row=i // 3, column=i % 3, sticky='nsew', padx=5, pady=5)
            
            value_label = ttk.Label(frame, text="--", font=('Arial', 16, 'bold'))
            value_label.pack(pady=5)
            
            unit_label = ttk.Label(frame, text=unit, font=('Arial', 10))
            unit_label.pack()
            
            self.real_time_labels[key] = (value_label, unit_label)
        
        # Configurar expansão
        for i in range(3):
            metrics_grid.columnconfigure(i, weight=1)
        for i in range(2):
            metrics_grid.rowconfigure(i, weight=1)
    
    def _setup_logs_tab(self):
        """Configura aba de logs."""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📝 Logs")
        
        # Controles de log
        log_controls = ttk.Frame(logs_frame)
        log_controls.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        ttk.Button(log_controls, text="Limpar Logs",
                  command=self._clear_logs).pack(side=tk.LEFT, padx=2)
        ttk.Button(log_controls, text="Exportar Logs",
                  command=self._export_logs).pack(side=tk.LEFT, padx=2)
        
        # Área de texto para logs
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=20)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.logs_text.config(state=tk.DISABLED)
    
    def _setup_status_bar(self):
        """Configura barra de status."""
        self.status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Pronto")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.time_label = ttk.Label(self.status_bar, text="")
        self.time_label.pack(side=tk.RIGHT, padx=5)
    
    def _setup_real_time_updates(self):
        """Configura atualizações em tempo real."""
        self.update_interval = 1000  # ms
        self._schedule_updates()
    
    def _schedule_updates(self):
        """Agenda próxima atualização."""
        self._update_display()
        self._update_time()
        self.root.after(self.update_interval, self._schedule_updates)
    
    def _update_time(self):
        """Atualiza hora na barra de status."""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"🕒 {current_time}")
    
    def _update_display(self):
        """Atualiza toda a exibição."""
        try:
            # Atualizar métricas principais
            network_info = self.library.get_network_info()
            if network_info:
                self.metric_labels['status'].config(
                    text=network_info['performance']['current_status']
                )
                self.metric_labels['neuron_count'].config(
                    text=str(network_info['architecture']['total_neurons'])
                )
                self.metric_labels['qubit_count'].config(
                    text=str(network_info['architecture']['total_qubits'])
                )
                self.metric_labels['quantum_advantage'].config(
                    text=f"{network_info['performance']['quantum_advantage']:.2f}x"
                )
                self.metric_labels['avg_entanglement'].config(
                    text=f"{network_info['performance']['avg_entanglement']:.3f}"
                )
                self.metric_labels['avg_coherence'].config(
                    text=f"{network_info['performance']['avg_coherence']:.3f}"
                )
            
            # Atualizar métricas em tempo real
            metrics_snapshot = self.library.get_metrics_snapshot()
            if metrics_snapshot:
                for key, (value_label, unit_label) in self.real_time_labels.items():
                    if key in metrics_snapshot:
                        value = metrics_snapshot[key]
                        if key == 'ops_per_second':
                            display_value = f"{value/1e6:.1f}"
                        elif key == 'memory_usage_mb':
                            display_value = f"{value:.1f}"
                        else:
                            display_value = f"{value:.3f}"
                        value_label.config(text=display_value)
            
            # Atualizar gráficos
            self._update_charts()
            
            # Atualizar informações da rede
            self._update_network_info()
            
            # Atualizar logs
            self._update_logs()
            
        except Exception as e:
            logger.error(f"Erro ao atualizar display: {e}")
    
    def _update_charts(self):
        """Atualiza gráficos em tempo real."""
        if self.library.training_history:
            # Performance
            epochs = [m.epoch for m in self.library.training_history]
            accuracies = [m.accuracy for m in self.library.training_history]
            
            self.performance_line.set_data(epochs, accuracies)
            self.performance_ax.relim()
            self.performance_ax.autoscale_view()
            self.performance_canvas.draw()
            
            # Métricas quânticas
            time_points = list(range(len(self.library.training_history)))
            entanglements = [m.entanglement for m in self.library.training_history]
            coherences = [m.coherence for m in self.library.training_history]
            
            self.entanglement_line.set_data(time_points, entanglements)
            self.coherence_line.set_data(time_points, coherences)
            
            self.quantum_ax.relim()
            self.quantum_ax.autoscale_view()
            self.quantum_canvas.draw()
    
    def _update_network_info(self):
        """Atualiza informações da rede."""
        try:
            network_info = self.library.get_network_info()
            info_text = json.dumps(network_info, indent=2, default=str)
            
            self.network_info_text.config(state=tk.NORMAL)
            self.network_info_text.delete(1.0, tk.END)
            self.network_info_text.insert(1.0, info_text)
            self.network_info_text.config(state=tk.DISABLED)
        except Exception as e:
            logger.error(f"Erro ao atualizar info da rede: {e}")
    
    def _update_logs(self):
        """Atualiza display de logs."""
        try:
            if self.library.log_messages:
                self.logs_text.config(state=tk.NORMAL)
                
                # Adicionar apenas novas mensagens
                current_content = set(self.logs_text.get(1.0, tk.END).strip().split('\n'))
                new_messages = [msg for msg in self.library.log_messages 
                              if msg not in current_content]
                
                for message in new_messages[-20:]:
                    self.logs_text.insert(tk.END, message + '\n')
                
                # Scroll automático
                self.logs_text.see(tk.END)
                self.logs_text.config(state=tk.DISABLED)
        except Exception as e:
            logger.error(f"Erro ao atualizar logs: {e}")
    
    def _start_training(self):
        """Inicia treinamento em thread separada."""

        def training_worker():
            try:
                epochs = int(self.epochs_var.get())
                
                # Dados de treinamento simulados
                training_data = [np.random.randn(8) for _ in range(100)]
                labels = [np.eye(4)[random.randint(0, 3)] for _ in range(100)]
                
                self.library.train(training_data, labels, epochs=epochs)
                
            except ValueError:
                self.status_label.config(text="Erro: número de épocas inválido")
            except Exception as e:
                logger.error(f"Erro no treinamento: {e}")
                self.status_label.config(text=f"Erro: {str(e)}")
        
        training_thread = threading.Thread(target=training_worker, daemon=True)
        training_thread.start()
        self.status_label.config(text="Treinamento iniciado...")
    
    def _stop_training(self):
        """Para o treinamento."""
        self.library.stop_training()
        self.status_label.config(text="Treinamento parado")
    
    def _save_model(self):
        """Salva o modelo atual."""
        filename = f"quantum_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            self.library.save_model(filename)
            self.status_label.config(text=f"Modelo salvo: {filename}")
        except Exception as e:
            self.status_label.config(text=f"Erro ao salvar: {str(e)}")
    
    def _load_model(self):
        """Carrega modelo de arquivo."""
        from tkinter import filedialog
        
        filepath = filedialog.askopenfilename(
            title="Selecionar modelo",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                self.library.load_model(filepath)
                self.status_label.config(text=f"Modelo carregado: {Path(filepath).name}")
            except Exception as e:
                self.status_label.config(text=f"Erro ao carregar: {str(e)}")
    
    def _export_network_info(self):
        """Exporta informações da rede para JSON."""
        from tkinter import filedialog
        
        filepath = filedialog.asksaveasfilename(
            title="Exportar informações da rede",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filepath:
            try:
                network_info = self.library.get_network_info()
                with open(filepath, 'w') as f:
                    json.dump(network_info, f, indent=2, default=str)
                self.status_label.config(text=f"Informações exportadas: {Path(filepath).name}")
            except Exception as e:
                self.status_label.config(text=f"Erro ao exportar: {str(e)}")
    
    def _clear_logs(self):
        """Limpa os logs exibidos."""
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.delete(1.0, tk.END)
        self.logs_text.config(state=tk.DISABLED)
        self.status_label.config(text="Logs limpos")
    
    def _export_logs(self):
        """Exporta logs para arquivo de texto."""
        from tkinter import filedialog
        
        filepath = filedialog.asksaveasfilename(
            title="Exportar logs",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    for log_entry in self.library.log_messages:
                        f.write(log_entry + '\n')
                self.status_label.config(text=f"Logs exportados: {Path(filepath).name}")
            except Exception as e:
                self.status_label.config(text=f"Erro ao exportar logs: {str(e)}")
    
    def on_closing(self):
        """Executado ao fechar a aplicação."""
        self.library.stop_monitoring()
        self.root.destroy()

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================


def main():
    """Função principal."""
    try:
        root = tk.Tk()
        app = QuantumNeuralLibraryGUI(root)
        
        # Configurar fechamento seguro
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Centralizar janela
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.mainloop()
        
    except Exception as e:
        logger.critical(f"Erro fatal na aplicação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
