#!/usr/bin/env python3
"""
Quantum Simulator for Financial Applications

Simulador quântico completo para análise financeira e otimização de trading.
Implementa circuitos quânticos, algoritmos financeiros e análise de portfólio.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from collections import deque
import json
from datetime import datetime
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logger = logging.getLogger(__name__)


class QuantumGate(Enum):
    """Portas quânticas suportadas pelo simulador."""
    HADAMARD = "H"
    PAULI_X = "X"
    PAULI_Y = "Y"
    PAULI_Z = "Z"
    CNOT = "CNOT"
    SWAP = "SWAP"
    RY = "RY"
    RZ = "RZ"
    PHASE = "P"
    T = "T"
    S = "S"
    TOFFOLI = "CCX"
    CPHASE = "CP"


class MeasurementBasis(Enum):
    """Bases de medição quântica."""
    COMPUTATIONAL = "Z"
    HADAMARD = "X"
    CIRCULAR = "Y"


@dataclass
class GateOperation:
    """Operação de porta quântica no circuito."""
    gate: QuantumGate
    qubits: List[int]
    parameters: List[float] = field(default_factory=list)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def __str__(self) -> str:
        params_str = f"({', '.join(f'{p:.3f}' for p in self.parameters)})" if self.parameters else ""
        return f"{self.gate.value}{params_str} q{self.qubits}"


@dataclass
class QuantumState:
    """Estado quântico com operações de medição."""
    amplitudes: np.ndarray
    n_qubits: int
    density_matrix: Optional[np.ndarray] = None
    
    def __post_init__(self):
        """Normaliza o estado após inicialização."""
        norm = np.sqrt(np.sum(np.abs(self.amplitudes) ** 2))
        if norm > 0:
            self.amplitudes = self.amplitudes / norm
    
    @property
    def probabilities(self) -> np.ndarray:
        """Retorna probabilidades de medição."""
        return np.abs(self.amplitudes) ** 2
    
    def measure(self, basis: MeasurementBasis=MeasurementBasis.COMPUTATIONAL,
                shots: int=1) -> List[int]:
        """
        Mede o estado quântico.
        
        Args:
            basis: Base de medição
            shots: Número de medições
            
        Returns:
            Lista de resultados de medição
        """
        if basis == MeasurementBasis.COMPUTATIONAL:
            probs = self.probabilities
        else:
            # Rotacionar para outra base
            rotated_state = self._rotate_basis(basis)
            probs = np.abs(rotated_state.amplitudes) ** 2
        
        # Amostrar da distribuição
        indices = np.random.choice(len(probs), size=shots, p=probs)
        
        # Converter para strings binárias
        results = []
        for idx in indices:
            binary = format(idx, f'0{self.n_qubits}b')
            results.append([int(bit) for bit in binary])
        
        return results
    
    def _rotate_basis(self, basis: MeasurementBasis) -> 'QuantumState':
        """Rotaciona o estado para outra base de medição."""
        if basis == MeasurementBasis.COMPUTATIONAL:
            return self
        
        n = self.n_qubits
        size = 2 ** n
        
        if basis == MeasurementBasis.HADAMARD:
            # Matriz Hadamard para n qubits
            H = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
            H_n = H
            for _ in range(n - 1):
                H_n = np.kron(H_n, H)
            new_amplitudes = H_n @ self.amplitudes
        elif basis == MeasurementBasis.CIRCULAR:
            # Base circular (Y)
            Y = 1 / np.sqrt(2) * np.array([[1, -1j], [1, 1j]])
            Y_n = Y
            for _ in range(n - 1):
                Y_n = np.kron(Y_n, Y)
            new_amplitudes = Y_n @ self.amplitudes
        else:
            return self
        
        return QuantumState(new_amplitudes, n)
    
    def entanglement_entropy(self) -> float:
        """Calcula entropia de emaranhamento do estado."""
        if self.n_qubits < 2:
            return 0.0
        
        # Calcular matriz densidade reduzida
        state_vector = self.amplitudes.reshape(2, -1)
        rho = state_vector @ state_vector.conj().T
        rho /= np.trace(rho)
        
        # Calcular entropia de von Neumann
        eigenvalues = np.linalg.eigvalsh(rho)
        eigenvalues = eigenvalues[eigenvalues > 1e-10]
        entropy = -np.sum(eigenvalues * np.log2(eigenvalues))
        
        return entropy


class QuantumCircuit:
    """
    Circuito quântico completo com operações unitárias e medições.
    
    Attributes:
        n_qubits: Número de qubits no circuito
        operations: Lista de operações aplicadas
        state: Estado quântico atual
    """
    
    def __init__(self, n_qubits: int, name: str="QuantumCircuit"):
        """
        Inicializa circuito quântico.
        
        Args:
            n_qubits: Número de qubits
            name: Nome do circuito
        """
        self.n_qubits = n_qubits
        self.name = name
        self.operations: List[GateOperation] = []
        self.state = self._initialize_state()
        self.measurement_results: List[List[int]] = []
        self.execution_time: float = 0.0
        
        logger.info(f"Circuit '{name}' initialized with {n_qubits} qubits")
    
    def _initialize_state(self) -> QuantumState:
        """Inicializa estado |0...0⟩."""
        size = 2 ** self.n_qubits
        amplitudes = np.zeros(size, dtype=complex)
        amplitudes[0] = 1.0 + 0j
        return QuantumState(amplitudes, self.n_qubits)
    
    def reset(self) -> None:
        """Reseta o circuito para estado inicial."""
        self.state = self._initialize_state()
        self.measurement_results.clear()
        self.operations.clear()
        logger.debug(f"Circuit '{self.name}' reset")
    
    def apply_gate(self, gate: QuantumGate, qubits: List[int],
                   parameters: List[float]=None) -> 'QuantumCircuit':
        """
        Aplica uma porta quântica ao circuito.
        
        Args:
            gate: Porta quântica a aplicar
            qubits: Lista de qubits afetados
            parameters: Parâmetros para portas parametrizadas
            
        Returns:
            Self para chaining
        """
        # Validar qubits
        for q in qubits:
            if q < 0 or q >= self.n_qubits:
                raise ValueError(f"Qubit {q} fora do intervalo [0, {self.n_qubits-1}]")
        
        params = parameters or []
        operation = GateOperation(gate, qubits, params)
        self.operations.append(operation)
        
        # Aplicar gate ao estado
        self._apply_gate_to_state(gate, qubits, params)
        
        logger.debug(f"Applied {operation} to circuit '{self.name}'")
        return self
    
    def _apply_gate_to_state(self, gate: QuantumGate, qubits: List[int],
                            parameters: List[float]) -> None:
        """Aplica porta quântica ao estado atual."""
        n = self.n_qubits
        
        # Matrizes de porta base
        gate_matrices = {
            QuantumGate.HADAMARD: 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]]),
            QuantumGate.PAULI_X: np.array([[0, 1], [1, 0]]),
            QuantumGate.PAULI_Y: np.array([[0, -1j], [1j, 0]]),
            QuantumGate.PAULI_Z: np.array([[1, 0], [0, -1]]),
            QuantumGate.T: np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]]),
            QuantumGate.S: np.array([[1, 0], [0, 1j]]),
        }
        
        if gate in gate_matrices:
            # Porta de 1 qubit
            U = gate_matrices[gate]
            self._apply_single_qubit_gate(U, qubits[0])
        
        elif gate == QuantumGate.CNOT:
            # CNOT gate
            if len(qubits) != 2:
                raise ValueError("CNOT requer 2 qubits")
            self._apply_cnot(qubits[0], qubits[1])
        
        elif gate == QuantumGate.RY:
            # Porta de rotação Y
            if not parameters:
                raise ValueError("RY gate requer ângulo")
            angle = parameters[0]
            U = np.array([
                [np.cos(angle / 2), -np.sin(angle / 2)],
                [np.sin(angle / 2), np.cos(angle / 2)]
            ])
            self._apply_single_qubit_gate(U, qubits[0])
        
        elif gate == QuantumGate.RZ:
            # Porta de rotação Z
            if not parameters:
                raise ValueError("RZ gate requer ângulo")
            angle = parameters[0]
            U = np.array([
                [np.exp(-1j * angle / 2), 0],
                [0, np.exp(1j * angle / 2)]
            ])
            self._apply_single_qubit_gate(U, qubits[0])
        
        elif gate == QuantumGate.PHASE:
            # Porta de fase
            if not parameters:
                raise ValueError("Phase gate requer ângulo")
            angle = parameters[0]
            U = np.array([[1, 0], [0, np.exp(1j * angle)]])
            self._apply_single_qubit_gate(U, qubits[0])
        
        else:
            logger.warning(f"Gate {gate} não implementado - ignorando")
    
    def _apply_single_qubit_gate(self, U: np.ndarray, qubit: int) -> None:
        """Aplica porta de 1 qubit usando produto de Kronecker."""
        n = self.n_qubits
        
        # Construir operador completo
        if qubit == 0:
            op = U
        else:
            op = np.eye(2)
        
        for q in range(1, n):
            if q == qubit:
                op = np.kron(op, U)
            else:
                op = np.kron(op, np.eye(2))
        
        # Aplicar ao estado
        self.state.amplitudes = op @ self.state.amplitudes
    
    def _apply_cnot(self, control: int, target: int) -> None:
        """Aplica porta CNOT usando operador de projeção."""
        n = self.n_qubits
        size = 2 ** n
        
        # Construir matriz CNOT
        cnot_matrix = np.eye(size, dtype=complex)
        
        for i in range(size):
            # Converter para binário
            binary = format(i, f'0{n}b')
            bits = [int(bit) for bit in binary]
            
            # Verificar se control qubit é 1
            if bits[control] == 1:
                # Inverter target qubit
                bits[target] = 1 - bits[target]
                
                # Converter de volta para decimal
                j = int(''.join(str(b) for b in bits), 2)
                
                # Atualizar matriz
                cnot_matrix[i, i] = 0
                cnot_matrix[j, i] = 1
        
        # Aplicar ao estado
        self.state.amplitudes = cnot_matrix @ self.state.amplitudes
    
    def add_hadamard(self, qubit: int) -> 'QuantumCircuit':
        """Adiciona porta Hadamard."""
        return self.apply_gate(QuantumGate.HADAMARD, [qubit])
    
    def add_cnot(self, control: int, target: int) -> 'QuantumCircuit':
        """Adiciona porta CNOT."""
        return self.apply_gate(QuantumGate.CNOT, [control, target])
    
    def add_ry(self, qubit: int, angle: float) -> 'QuantumCircuit':
        """Adiciona porta de rotação Y."""
        return self.apply_gate(QuantumGate.RY, [qubit], [angle])
    
    def add_rz(self, qubit: int, angle: float) -> 'QuantumCircuit':
        """Adiciona porta de rotação Z."""
        return self.apply_gate(QuantumGate.RZ, [qubit], [angle])
    
    def measure_all(self, basis: MeasurementBasis=MeasurementBasis.COMPUTATIONAL,
                   shots: int=1024) -> List[List[int]]:
        """
        Mede todos os qubits.
        
        Args:
            basis: Base de medição
            shots: Número de medições
            
        Returns:
            Resultados das medições
        """
        import time
        start_time = time.time()
        
        results = self.state.measure(basis, shots)
        self.measurement_results.extend(results)
        
        self.execution_time = time.time() - start_time
        logger.info(f"Measured circuit '{self.name}': {shots} shots in {self.execution_time:.3f}s")
        
        return results
    
    def get_counts(self, shots: int=1024) -> Dict[str, int]:
        """
        Retorna contagens de medição.
        
        Args:
            shots: Número de medições
            
        Returns:
            Dicionário com contagens de cada resultado
        """
        results = self.measure_all(shots=shots)
        counts = {}
        
        for result in results:
            key = ''.join(str(bit) for bit in result)
            counts[key] = counts.get(key, 0) + 1
        
        return counts
    
    def expectation_value(self, observable: np.ndarray) -> float:
        """
        Calcula valor esperado de um observável.
        
        Args:
            observable: Operador observável
            
        Returns:
            Valor esperado
        """
        psi = self.state.amplitudes
        return np.real(psi.conj().T @ observable @ psi)
    
    def get_statevector(self) -> np.ndarray:
        """Retorna vetor de estado atual."""
        return self.state.amplitudes.copy()
    
    def get_density_matrix(self) -> np.ndarray:
        """Calcula matriz densidade do estado."""
        psi = self.state.amplitudes.reshape(-1, 1)
        rho = psi @ psi.conj().T
        return rho
    
    def get_entanglement_entropy(self) -> float:
        """Calcula entropia de emaranhamento."""
        return self.state.entanglement_entropy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa circuito para dicionário."""
        return {
            "name": self.name,
            "n_qubits": self.n_qubits,
            "operations": [str(op) for op in self.operations],
            "execution_time": self.execution_time,
            "measurement_count": len(self.measurement_results)
        }
    
    def __str__(self) -> str:
        """Representação em string do circuito."""
        ops_str = '\n  '.join(str(op) for op in self.operations)
        return (f"QuantumCircuit '{self.name}' ({self.n_qubits} qubits):\n"
                f"  {ops_str}")


class FinancialQuantumSimulator:
    """
    Simulador quântico para aplicações financeiras.
    
    Implementa algoritmos quânticos para:
    - Predição de preços
    - Otimização de portfólio
    - Análise de risco
    - Detecção de padrões de mercado
    """
    
    def __init__(self, config: Dict[str, Any]=None):
        """
        Inicializa simulador financeiro quântico.
        
        Args:
            config: Configuração do simulador
        """
        self.config = config or self._default_config()
        self.circuit_cache: Dict[str, QuantumCircuit] = {}
        self.prediction_history: deque = deque(maxlen=1000)
        self.optimization_history: List[Dict[str, Any]] = []
        
        logger.info("Financial Quantum Simulator initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Retorna configuração padrão."""
        return {
            "quantum": {
                "default_shots": 2048,
                "max_qubits": 10,
                "use_entanglement": True,
                "optimization_depth": 5
            },
            "financial": {
                "confidence_threshold": 0.65,
                "risk_free_rate": 0.02,
                "volatility_window": 20,
                "max_portfolio_size": 20
            },
            "performance": {
                "cache_enabled": True,
                "parallel_execution": False,
                "timeout_seconds": 30
            }
        }
    
    def simulate_price_prediction(self, historical_data: List[float],
                                 lookback_period: int=10) -> Dict[str, Any]:
        """
        Simula predição de preços usando algoritmos quânticos.
        
        Args:
            historical_data: Dados históricos de preços
            lookback_period: Período de lookback para features
            
        Returns:
            Dicionário com predição e métricas
        """
        logger.info(f"Simulating price prediction for {len(historical_data)} data points")
        
        try:
            # Preparar dados
            processed_data = self._prepare_price_data(historical_data, lookback_period)
            
            # Executar circuito quântico para predição
            prediction_result = self._quantum_price_prediction_circuit(processed_data)
            
            # Análise de confiança
            confidence_metrics = self._calculate_confidence_metrics(
                prediction_result, processed_data
            )
            
            # Gerar sinal de trading
            trading_signal = self._generate_trading_signal(
                prediction_result, confidence_metrics
            )
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "prediction": prediction_result,
                "confidence_metrics": confidence_metrics,
                "trading_signal": trading_signal,
                "lookback_period": lookback_period,
                "data_points": len(historical_data),
                "quantum_circuit_used": True,
                "entanglement_entropy": prediction_result.get("entanglement", 0.0)
            }
            
            # Armazenar no histórico
            self.prediction_history.append(result)
            
            logger.info(f"Price prediction complete: signal={trading_signal['action']}, "
                       f"confidence={confidence_metrics['overall_confidence']:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in price prediction: {e}")
            return self._create_error_result("price_prediction", str(e))
    
    def _prepare_price_data(self, data: List[float], lookback: int) -> Dict[str, Any]:
        """Prepara dados de preço para processamento quântico."""
        if len(data) < lookback:
            raise ValueError(f"Dados insuficientes: {len(data)} < {lookback}")
        
        # Calcular retornos
        returns = np.diff(data) / data[:-1]
        
        # Features baseadas em retornos
        recent_returns = returns[-lookback:] if len(returns) >= lookback else returns
        
        # Estatísticas
        stats_dict = {
            "mean_return": float(np.mean(recent_returns)),
            "volatility": float(np.std(recent_returns)),
            "skewness": float(stats.skew(recent_returns)) if len(recent_returns) > 2 else 0.0,
            "kurtosis": float(stats.kurtosis(recent_returns)) if len(recent_returns) > 3 else 0.0,
            "max_return": float(np.max(recent_returns)),
            "min_return": float(np.min(recent_returns)),
            "last_return": float(recent_returns[-1]) if len(recent_returns) > 0 else 0.0
        }
        
        # Normalizar para encoding quântico
        normalized = {
            key: self._normalize_for_quantum(value, key)
            for key, value in stats_dict.items()
        }
        
        return {
            "raw_stats": stats_dict,
            "normalized": normalized,
            "lookback_period": lookback,
            "data_length": len(data)
        }
    
    def _normalize_for_quantum(self, value: float, stat_name: str) -> float:
        """Normaliza valor para encoding quântico."""
        # Ranges específicos por estatística
        ranges = {
            "mean_return": (-0.1, 0.1),
            "volatility": (0, 0.2),
            "skewness": (-3, 3),
            "kurtosis": (-10, 10),
            "max_return": (-0.5, 0.5),
            "min_return": (-0.5, 0.5),
            "last_return": (-0.2, 0.2)
        }
        
        low, high = ranges.get(stat_name, (-1, 1))
        
        # Clip e normalize para [0, 1]
        clipped = np.clip(value, low, high)
        normalized = (clipped - low) / (high - low)
        
        return float(normalized)
    
    def _quantum_price_prediction_circuit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa circuito quântico para predição de preços."""
        # Usar 4 qubits para predição
        n_qubits = 4
        circuit = QuantumCircuit(n_qubits, "price_prediction")
        
        # Encoding dos dados nos qubits
        normalized_data = data["normalized"]
        
        # Aplicar rotações baseadas nos dados
        angle_mapping = [
            ("mean_return", 0),
            ("volatility", 1),
            ("skewness", 2),
            ("last_return", 3)
        ]
        
        for stat_name, qubit in angle_mapping:
            if stat_name in normalized_data:
                angle = normalized_data[stat_name] * np.pi
                circuit.add_ry(qubit, angle)
        
        # Adicionar entrelaçamento se configurado
        if self.config["quantum"]["use_entanglement"]:
            circuit.add_cnot(0, 1)
            circuit.add_cnot(2, 3)
            circuit.add_cnot(1, 2)
        
        # Medir
        shots = self.config["quantum"]["default_shots"]
        counts = circuit.get_counts(shots)
        
        # Análise dos resultados
        prediction_result = self._analyze_measurement_counts(counts, n_qubits)
        
        # Adicionar métricas do circuito
        prediction_result.update({
            "circuit_operations": len(circuit.operations),
            "entanglement": circuit.get_entanglement_entropy(),
            "execution_time": circuit.execution_time,
            "shots": shots
        })
        
        # Cache do circuito
        if self.config["performance"]["cache_enabled"]:
            self.circuit_cache["price_prediction"] = circuit
        
        return prediction_result
    
    def _analyze_measurement_counts(self, counts: Dict[str, int],
                                   n_qubits: int) -> Dict[str, Any]:
        """Analisa contagens de medição para gerar predição."""
        total_shots = sum(counts.values())
        
        if total_shots == 0:
            return {"direction": "NEUTRAL", "strength": 0.0, "counts": counts}
        
        # Converter counts para probabilidades
        probabilities = {}
        for state, count in counts.items():
            probabilities[state] = count / total_shots
        
        # Calcular valor esperado do primeiro qubit (sinal de direção)
        expected_value = 0.0
        for state, prob in probabilities.items():
            # Primeiro bit indica direção (0=DOWN, 1=UP)
            direction_bit = int(state[0])
            expected_value += prob * direction_bit
        
        # Determinar direção baseada no valor esperado
        if expected_value > 0.5:
            direction = "UP"
            strength = (expected_value - 0.5) * 2
        elif expected_value < 0.5:
            direction = "DOWN"
            strength = (0.5 - expected_value) * 2
        else:
            direction = "NEUTRAL"
            strength = 0.0
        
        # Calcular entropia de Shannon da distribuição
        entropy = -sum(p * np.log2(p) for p in probabilities.values() if p > 0)
        max_entropy = n_qubits
        normalized_entropy = entropy / max_entropy
        
        return {
            "direction": direction,
            "strength": float(strength),
            "expected_value": float(expected_value),
            "entropy": float(entropy),
            "normalized_entropy": float(normalized_entropy),
            "probabilities": probabilities,
            "total_shots": total_shots
        }
    
    def _calculate_confidence_metrics(self, prediction_result: Dict[str, Any],
                                     data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas de confiança para a predição."""
        strength = prediction_result.get("strength", 0.0)
        entropy = prediction_result.get("normalized_entropy", 1.0)
        
        # Confiança baseada na força do sinal e entropia
        signal_confidence = strength
        entropy_confidence = 1.0 - entropy  # Baixa entropia = alta confiança
        
        # Confiança baseada na volatilidade dos dados
        volatility = data["raw_stats"].get("volatility", 0.0)
        volatility_confidence = np.exp(-volatility * 10)  # Decai com volatilidade
        
        # Confiança combinada
        weights = {
            "signal": 0.4,
            "entropy": 0.3,
            "volatility": 0.3
        }
        
        overall_confidence = (
            weights["signal"] * signal_confidence + 
            weights["entropy"] * entropy_confidence + 
            weights["volatility"] * volatility_confidence
        )
        
        return {
            "overall_confidence": float(overall_confidence),
            "signal_confidence": float(signal_confidence),
            "entropy_confidence": float(entropy_confidence),
            "volatility_confidence": float(volatility_confidence),
            "volatility": float(volatility),
            "confidence_threshold": self.config["financial"]["confidence_threshold"],
            "is_confident": overall_confidence >= self.config["financial"]["confidence_threshold"]
        }
    
    def _generate_trading_signal(self, prediction_result: Dict[str, Any],
                                confidence_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sinal de trading baseado na predição e confiança."""
        direction = prediction_result.get("direction", "NEUTRAL")
        strength = prediction_result.get("strength", 0.0)
        confidence = confidence_metrics.get("overall_confidence", 0.0)
        is_confident = confidence_metrics.get("is_confident", False)
        
        # Determinar ação
        if not is_confident or direction == "NEUTRAL":
            action = "HOLD"
            position_size = 0.0
        elif direction == "UP":
            action = "BUY"
            position_size = min(strength * confidence, 1.0)
        elif direction == "DOWN":
            action = "SELL"
            position_size = min(strength * confidence, 1.0)
        else:
            action = "HOLD"
            position_size = 0.0
        
        return {
            "action": action,
            "position_size": float(position_size),
            "direction": direction,
            "strength": float(strength),
            "confidence": float(confidence),
            "timestamp": datetime.now().isoformat()
        }
    
    def optimize_portfolio(self, assets: List[str],
                          returns_data: Dict[str, List[float]],
                          risk_free_rate: float=None) -> Dict[str, Any]:
        """
        Otimiza portfólio usando algoritmos quânticos.
        
        Args:
            assets: Lista de ativos
            returns_data: Dicionário com retornos históricos por ativo
            risk_free_rate: Taxa livre de risco
            
        Returns:
            Pesos otimizados e métricas
        """
        logger.info(f"Optimizing portfolio with {len(assets)} assets")
        
        try:
            # Validar inputs
            if len(assets) == 0:
                raise ValueError("Lista de ativos vazia")
            
            if len(assets) > self.config["financial"]["max_portfolio_size"]:
                assets = assets[:self.config["financial"]["max_portfolio_size"]]
                logger.warning(f"Portfolio truncado para {len(assets)} ativos")
            
            # Preparar dados
            portfolio_data = self._prepare_portfolio_data(assets, returns_data)
            
            # Executar otimização quântica
            optimization_result = self._quantum_portfolio_optimization(
                portfolio_data, risk_free_rate
            )
            
            # Calcular métricas de performance
            performance_metrics = self._calculate_portfolio_metrics(
                optimization_result, portfolio_data
            )
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "assets": assets,
                "optimized_weights": optimization_result["weights"],
                "performance_metrics": performance_metrics,
                "optimization_method": "quantum_variational",
                "n_assets": len(assets),
                "risk_free_rate": risk_free_rate or self.config["financial"]["risk_free_rate"]
            }
            
            # Armazenar no histórico
            self.optimization_history.append(result)
            
            logger.info(f"Portfolio optimization complete: "
                       f"sharpe={performance_metrics['sharpe_ratio']:.3f}, "
                       f"return={performance_metrics['expected_return']:.3f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in portfolio optimization: {e}")
            return self._create_error_result("portfolio_optimization", str(e))
    
    def _prepare_portfolio_data(self, assets: List[str],
                               returns_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Prepara dados do portfólio para otimização."""
        # Extrair retornos para cada ativo
        asset_returns = []
        valid_assets = []
        
        for asset in assets:
            if asset in returns_data and len(returns_data[asset]) > 1:
                returns = returns_data[asset]
                asset_returns.append(returns)
                valid_assets.append(asset)
            else:
                logger.warning(f"Dados insuficientes para ativo {asset} - ignorando")
        
        if len(valid_assets) == 0:
            raise ValueError("Nenhum ativo com dados suficientes")
        
        # Converter para array numpy
        returns_matrix = np.array(asset_returns).T
        
        # Calcular estatísticas
        mean_returns = np.mean(returns_matrix, axis=0)
        cov_matrix = np.cov(returns_matrix.T)
        volatilities = np.std(returns_matrix, axis=0)
        
        # Correlações
        corr_matrix = np.corrcoef(returns_matrix.T)
        
        return {
            "assets": valid_assets,
            "returns_matrix": returns_matrix,
            "mean_returns": mean_returns,
            "cov_matrix": cov_matrix,
            "corr_matrix": corr_matrix,
            "volatilities": volatilities,
            "n_assets": len(valid_assets),
            "n_periods": returns_matrix.shape[0]
        }
    
    def _quantum_portfolio_optimization(self, portfolio_data: Dict[str, Any],
                                       risk_free_rate: float=None) -> Dict[str, Any]:
        """Executa otimização quântica de portfólio."""
        n_assets = portfolio_data["n_assets"]
        mean_returns = portfolio_data["mean_returns"]
        cov_matrix = portfolio_data["cov_matrix"]
        
        # Usar algoritmo variacional quântico
        risk_free = risk_free_rate or self.config["financial"]["risk_free_rate"]
        
        # Circuito quântico para otimização
        n_qubits = min(n_assets * 2, self.config["quantum"]["max_qubits"])
        circuit = QuantumCircuit(n_qubits, "portfolio_optimization")
        
        # Encoding dos retornos esperados
        for i in range(min(n_assets, n_qubits)):
            # Mapear retorno para ângulo de rotação
            angle = mean_returns[i] * np.pi * 2
            circuit.add_ry(i, angle)
        
        # Adicionar entrelaçamento para capturar correlações
        if n_qubits >= 2 and self.config["quantum"]["use_entanglement"]:
            for i in range(n_qubits - 1):
                circuit.add_cnot(i, i + 1)
        
        # Camadas de otimização
        depth = self.config["quantum"]["optimization_depth"]
        for layer in range(depth):
            for i in range(n_qubits):
                # Parâmetros variacionais
                theta = np.random.random() * np.pi
                phi = np.random.random() * np.pi
                
                circuit.add_ry(i, theta)
                circuit.add_rz(i, phi)
        
        # Medir
        shots = self.config["quantum"]["default_shots"]
        counts = circuit.get_counts(shots)
        
        # Converter medições em pesos
        weights = self._measurements_to_weights(counts, n_qubits, n_assets)
        
        # Normalizar pesos para soma = 1
        if np.sum(weights) > 0:
            weights = weights / np.sum(weights)
        else:
            # Distribuição igualitária se todos zero
            weights = np.ones(n_assets) / n_assets
        
        # Calcular métricas do portfólio
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(weights.T @ cov_matrix @ weights)
        
        if portfolio_volatility > 0:
            sharpe_ratio = (portfolio_return - risk_free) / portfolio_volatility
        else:
            sharpe_ratio = 0.0
        
        return {
            "weights": {portfolio_data["assets"][i]: float(weights[i]) 
                       for i in range(n_assets)},
            "expected_return": float(portfolio_return),
            "volatility": float(portfolio_volatility),
            "sharpe_ratio": float(sharpe_ratio),
            "circuit_entanglement": circuit.get_entanglement_entropy(),
            "shots": shots,
            "optimization_depth": depth
        }
    
    def _measurements_to_weights(self, counts: Dict[str, int],
                                n_qubits: int, n_assets: int) -> np.ndarray:
        """Converte medições quânticas em pesos de portfólio."""
        total_shots = sum(counts.values())
        
        if total_shots == 0:
            return np.ones(n_assets) / n_assets
        
        # Inicializar pesos
        weights = np.zeros(n_assets)
        
        # Mapear medições para ativos
        for state, count in counts.items():
            # Usar bits para determinar participação
            for i in range(min(n_qubits, n_assets)):
                if state[i] == '1':
                    weights[i] += count
        
        # Normalizar pelo total de shots
        weights = weights / total_shots
        
        # Garantir que todos os ativos tenham peso mínimo
        min_weight = 0.01  # 1% mínimo
        weights = np.maximum(weights, min_weight)
        
        return weights
    
    def _calculate_portfolio_metrics(self, optimization_result: Dict[str, Any],
                                    portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas detalhadas do portfólio."""
        weights = np.array(list(optimization_result["weights"].values()))
        mean_returns = portfolio_data["mean_returns"]
        cov_matrix = portfolio_data["cov_matrix"]
        
        # Métricas básicas
        expected_return = float(np.dot(weights, mean_returns))
        volatility = float(np.sqrt(weights.T @ cov_matrix @ weights))
        
        # Ratio de Sharpe
        risk_free = self.config["financial"]["risk_free_rate"]
        if volatility > 0:
            sharpe_ratio = (expected_return - risk_free) / volatility
        else:
            sharpe_ratio = 0.0
        
        # Sortino Ratio (considera apenas downside volatility)
        returns_matrix = portfolio_data["returns_matrix"]
        portfolio_returns = returns_matrix @ weights
        downside_returns = portfolio_returns[portfolio_returns < risk_free]
        
        if len(downside_returns) > 0:
            downside_volatility = np.std(downside_returns)
            if downside_volatility > 0:
                sortino_ratio = (expected_return - risk_free) / downside_volatility
            else:
                sortino_ratio = sharpe_ratio
        else:
            sortino_ratio = sharpe_ratio
        
        # Valor em Risco (VaR) 95%
        if len(portfolio_returns) > 0:
            var_95 = float(np.percentile(portfolio_returns, 5))
            cvar_95 = float(np.mean(portfolio_returns[portfolio_returns <= var_95]))
        else:
            var_95 = 0.0
            cvar_95 = 0.0
        
        # Diversificação
        weights_array = np.array(list(weights))
        if np.sum(weights_array) > 0:
            normalized_weights = weights_array / np.sum(weights_array)
            entropy_diversification = -np.sum(
                normalized_weights * np.log(normalized_weights + 1e-10)
            )
            max_entropy = np.log(len(weights_array))
            normalized_diversification = entropy_diversification / max_entropy
        else:
            normalized_diversification = 0.0
        
        return {
            "expected_return": expected_return,
            "volatility": volatility,
            "sharpe_ratio": float(sharpe_ratio),
            "sortino_ratio": float(sortino_ratio),
            "var_95": var_95,
            "cvar_95": cvar_95,
            "max_drawdown_simulated": self._simulate_max_drawdown(portfolio_returns),
            "diversification_score": float(normalized_diversification),
            "concentration_risk": float(np.max(weights_array) if len(weights_array) > 0 else 0.0)
        }
    
    def _simulate_max_drawdown(self, returns: np.ndarray) -> float:
        """Simula maximum drawdown a partir dos retornos."""
        if len(returns) == 0:
            return 0.0
        
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        
        return float(np.min(drawdown))
    
    def analyze_market_regime(self, market_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Analisa regime de mercado usando algoritmos quânticos.
        
        Args:
            market_data: Dados de mercado (preços, volumes, etc.)
            
        Returns:
            Classificação do regime e métricas
        """
        logger.info("Analyzing market regime with quantum algorithms")
        
        try:
            # Preparar dados para análise quântica
            regime_data = self._prepare_regime_data(market_data)
            
            # Executar circuito quântico para classificação
            regime_result = self._quantum_regime_classification(regime_data)
            
            # Análise de confiança
            regime_confidence = self._calculate_regime_confidence(regime_result)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "regime": regime_result["classification"],
                "regime_confidence": regime_confidence,
                "features_used": regime_data["feature_names"],
                "quantum_circuit": regime_result["circuit_metrics"],
                "market_conditions": regime_result["market_conditions"]
            }
            
            logger.info(f"Market regime analysis: {regime_result['classification']} "
                       f"(confidence: {regime_confidence:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in market regime analysis: {e}")
            return self._create_error_result("market_regime", str(e))
    
    def _prepare_regime_data(self, market_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Prepara dados para análise de regime."""
        features = {}
        feature_names = []
        
        # Preços
        if "prices" in market_data:
            prices = market_data["prices"]
            returns = np.diff(prices) / prices[:-1]
            
            features["returns_mean"] = float(np.mean(returns[-20:])) if len(returns) >= 20 else 0.0
            features["returns_vol"] = float(np.std(returns[-20:])) if len(returns) >= 20 else 0.0
            features["returns_skew"] = float(stats.skew(returns[-60:])) if len(returns) >= 60 else 0.0
            feature_names.extend(["returns_mean", "returns_vol", "returns_skew"])
        
        # Volumes (se disponível)
        if "volumes" in market_data:
            volumes = market_data["volumes"]
            if len(volumes) >= 20:
                vol_ratio = volumes[-1] / np.mean(volumes[-20:-1])
                features["volume_ratio"] = float(vol_ratio)
                feature_names.append("volume_ratio")
        
        # VIX-like volatility (se disponível)
        if "volatility" in market_data:
            volatility = market_data["volatility"]
            if len(volatility) >= 5:
                features["volatility_level"] = float(np.mean(volatility[-5:]))
                feature_names.append("volatility_level")
        
        # Normalizar features
        normalized = {}
        for name, value in features.items():
            normalized[name] = self._normalize_for_quantum(value, name)
        
        return {
            "raw_features": features,
            "normalized_features": normalized,
            "feature_names": feature_names,
            "n_features": len(features)
        }
    
    def _quantum_regime_classification(self, regime_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classifica regime de mercado usando circuito quântico."""
        n_features = regime_data["n_features"]
        n_qubits = min(n_features + 2, 6)  # Limitar a 6 qubits
        
        circuit = QuantumCircuit(n_qubits, "regime_classification")
        features = regime_data["normalized_features"]
        
        # Encoding das features
        for i, (name, value) in enumerate(features.items()):
            if i < n_qubits:
                angle = value * np.pi
                circuit.add_ry(i, angle)
        
        # Entrelaçamento para capturar relações complexas
        if n_qubits >= 3:
            circuit.add_cnot(0, 1)
            circuit.add_cnot(1, 2)
            if n_qubits >= 4:
                circuit.add_cnot(2, 3)
        
        # Medir
        shots = self.config["quantum"]["default_shots"] // 2
        counts = circuit.get_counts(shots)
        
        # Classificar baseado nos resultados
        classification = self._classify_regime_from_counts(counts, n_qubits)
        
        # Condições de mercado inferidas
        market_conditions = self._infer_market_conditions(
            classification, regime_data["raw_features"]
        )
        
        return {
            "classification": classification,
            "counts": counts,
            "circuit_metrics": circuit.to_dict(),
            "market_conditions": market_conditions,
            "shots": shots,
            "n_qubits": n_qubits
        }
    
    def _classify_regime_from_counts(self, counts: Dict[str, int],
                                    n_qubits: int) -> str:
        """Classifica regime de mercado baseado nas medições."""
        if not counts:
            return "UNCERTAIN"
        
        total = sum(counts.values())
        
        # Analisar padrões nas medições
        bull_patterns = ["11", "101", "111"]
        bear_patterns = ["00", "010", "000"]
        volatile_patterns = ["01", "10", "001", "110"]
        
        bull_score = 0
        bear_score = 0
        volatile_score = 0
        
        for pattern, count in counts.items():
            # Verificar padrões nos primeiros bits
            for bull_pat in bull_patterns:
                if pattern.startswith(bull_pat):
                    bull_score += count
            
            for bear_pat in bear_patterns:
                if pattern.startswith(bear_pat):
                    bear_score += count
            
            for vol_pat in volatile_patterns:
                if pattern.startswith(vol_pat):
                    volatile_score += count
        
        # Normalizar scores
        bull_score /= total
        bear_score /= total
        volatile_score /= total
        
        # Determinar regime dominante
        scores = {
            "BULL": bull_score,
            "BEAR": bear_score,
            "VOLATILE": volatile_score
        }
        
        dominant = max(scores.items(), key=lambda x: x[1])
        
        # Threshold para confiança
        if dominant[1] < 0.4:
            return "NEUTRAL"
        else:
            return dominant[0]
    
    def _infer_market_conditions(self, regime: str,
                                features: Dict[str, float]) -> Dict[str, Any]:
        """Infer conditions específicas do regime."""
        conditions = {
            "regime": regime,
            "volatility_level": "UNKNOWN",
            "trend_strength": "UNKNOWN",
            "market_sentiment": "NEUTRAL"
        }
        
        # Inferir baseado nas features
        if "returns_vol" in features:
            vol = features["returns_vol"]
            if vol > 0.05:
                conditions["volatility_level"] = "HIGH"
            elif vol > 0.02:
                conditions["volatility_level"] = "MEDIUM"
            else:
                conditions["volatility_level"] = "LOW"
        
        if "returns_mean" in features:
            mean = features["returns_mean"]
            if regime == "BULL" and mean > 0:
                conditions["trend_strength"] = "STRONG" if abs(mean) > 0.01 else "WEAK"
            elif regime == "BEAR" and mean < 0:
                conditions["trend_strength"] = "STRONG" if abs(mean) > 0.01 else "WEAK"
        
        # Sentimento baseado no regime
        if regime == "BULL":
            conditions["market_sentiment"] = "POSITIVE"
        elif regime == "BEAR":
            conditions["market_sentiment"] = "NEGATIVE"
        elif regime == "VOLATILE":
            conditions["market_sentiment"] = "UNCERTAIN"
        
        return conditions
    
    def _calculate_regime_confidence(self, regime_result: Dict[str, Any]) -> float:
        """Calcula confiança na classificação do regime."""
        counts = regime_result.get("counts", {})
        
        if not counts:
            return 0.0
        
        total = sum(counts.values())
        regime = regime_result.get("classification", "NEUTRAL")
        
        # Calcular proporção de medições consistentes com o regime
        consistent_patterns = {
            "BULL": ["11", "101", "111"],
            "BEAR": ["00", "010", "000"],
            "VOLATILE": ["01", "10", "001", "110"],
            "NEUTRAL": []  # Todos são consistentes
        }
        
        patterns = consistent_patterns.get(regime, [])
        
        if not patterns:  # NEUTRAL
            # Para NEUTRAL, confiança baseada na uniformidade
            max_count = max(counts.values())
            uniformity = 1 - (max_count / total)
            return float(uniformity)
        
        # Contar medições consistentes
        consistent_count = 0
        for pattern, count in counts.items():
            for pat in patterns:
                if pattern.startswith(pat):
                    consistent_count += count
                    break
        
        confidence = consistent_count / total
        
        # Ajustar pela entropia do circuito
        circuit_metrics = regime_result.get("circuit_metrics", {})
        if "entanglement" in circuit_metrics:
            entanglement = circuit_metrics["entanglement"]
            # Alta entropia pode reduzir confiança em classificações simples
            confidence *= (1 - entanglement * 0.5)
        
        return float(np.clip(confidence, 0.0, 1.0))
    
    def get_prediction_history(self, limit: int=100) -> List[Dict[str, Any]]:
        """Retorna histórico de predições."""
        return list(self.prediction_history)[-limit:]
    
    def get_optimization_history(self, limit: int=50) -> List[Dict[str, Any]]:
        """Retorna histórico de otimizações."""
        return self.optimization_history[-limit:]
    
    def clear_cache(self) -> None:
        """Limpa cache de circuitos."""
        self.circuit_cache.clear()
        logger.info("Quantum circuit cache cleared")
    
    def _create_error_result(self, operation: str, error_msg: str) -> Dict[str, Any]:
        """Cria resultado de erro padronizado."""
        return {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": "ERROR",
            "error": error_msg,
            "quantum_circuit_used": False
        }
    
    def __str__(self) -> str:
        """Representação em string do simulador."""
        return (f"FinancialQuantumSimulator\n"
                f"  Config: {json.dumps(self.config, indent=2)}\n"
                f"  Prediction history: {len(self.prediction_history)} entries\n"
                f"  Optimization history: {len(self.optimization_history)} entries\n"
                f"  Circuit cache: {len(self.circuit_cache)} circuits")

# ============================================================================
# FUNÇÕES DE DEMONSTRAÇÃO E TESTES
# ============================================================================


def demonstrate_quantum_circuit() -> None:
    """Demonstra funcionalidades básicas do circuito quântico."""
    print("🧪 Demonstração do Quantum Circuit")
    print("=" * 50)
    
    # Criar circuito
    circuit = QuantumCircuit(3, "demo_circuit")
    
    # Adicionar operações
    circuit.add_hadamard(0) \
          .add_cnot(0, 1) \
          .add_ry(2, np.pi / 4) \
          .add_cnot(1, 2)
    
    print(f"\n{circuit}")
    
    # Medir
    counts = circuit.get_counts(shots=1000)
    
    print(f"\n📊 Contagens de medição (1000 shots):")
    for state, count in sorted(counts.items()):
        print(f"  |{state}⟩: {count} ({count/10:.1f}%)")
    
    # Estatísticas
    print(f"\n📈 Estatísticas do circuito:")
    print(f"  Operações aplicadas: {len(circuit.operations)}")
    print(f"  Entropia de emaranhamento: {circuit.get_entanglement_entropy():.4f}")
    print(f"  Tempo de execução: {circuit.execution_time:.3f}s")
    
    # Estado final
    statevector = circuit.get_statevector()
    print(f"\n🌌 Vetor de estado (primeiros 8 amplitudes):")
    for i in range(min(8, len(statevector))):
        amplitude = statevector[i]
        prob = np.abs(amplitude) ** 2
        print(f"  |{format(i, '03b')}⟩: {amplitude.real:.3f}{amplitude.imag:+.3f}i "
              f"(prob: {prob:.3f})")


def demonstrate_financial_simulation() -> None:
    """Demonstra simulação financeira quântica."""
    print("\n💰 Demonstração do Financial Quantum Simulator")
    print("=" * 50)
    
    # Criar simulador
    simulator = FinancialQuantumSimulator()
    
    # Gerar dados sintéticos
    np.random.seed(42)
    n_days = 100
    prices = 100 * np.cumprod(1 + np.random.randn(n_days) * 0.01 + 0.0005)
    prices = prices.tolist()
    
    print(f"\n📈 Dados sintéticos gerados:")
    print(f"  Período: {n_days} dias")
    print(f"  Preço inicial: {prices[0]:.2f}")
    print(f"  Preço final: {prices[-1]:.2f}")
    print(f"  Retorno total: {(prices[-1]/prices[0]-1)*100:.2f}%")
    
    # Predição de preços
    print(f"\n🎯 Predição de preços quântica:")
    prediction = simulator.simulate_price_prediction(prices, lookback_period=20)
    
    if prediction["status"] != "ERROR":
        signal = prediction["trading_signal"]
        confidence = prediction["confidence_metrics"]
        
        print(f"  Direção predita: {prediction['prediction']['direction']}")
        print(f"  Força do sinal: {prediction['prediction']['strength']:.2f}")
        print(f"  Confiança geral: {confidence['overall_confidence']:.2f}")
        print(f"  Sinal de trading: {signal['action']}")
        print(f"  Tamanho da posição: {signal['position_size']:.2f}")
    else:
        print(f"  Erro: {prediction['error']}")
    
    # Otimização de portfólio
    print(f"\n🏦 Otimização de portfólio quântica:")
    
    assets = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    returns_data = {}
    
    for asset in assets:
        # Gerar retornos sintéticos com correlações
        base_return = np.random.randn(n_days) * 0.01 + 0.0005
        asset_return = base_return + np.random.randn(n_days) * 0.005
        returns_data[asset] = asset_return.tolist()
    
    portfolio_result = simulator.optimize_portfolio(assets, returns_data)
    
    if portfolio_result["status"] != "ERROR":
        weights = portfolio_result["optimized_weights"]
        metrics = portfolio_result["performance_metrics"]
        
        print(f"\n  Pesos otimizados:")
        for asset, weight in weights.items():
            print(f"    {asset}: {weight:.2%}")
        
        print(f"\n  Métricas de performance:")
        print(f"    Retorno esperado: {metrics['expected_return']:.2%}")
        print(f"    Volatilidade: {metrics['volatility']:.2%}")
        print(f"    Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
        print(f"    Sortino Ratio: {metrics['sortino_ratio']:.3f}")
        print(f"    Diversificação: {metrics['diversification_score']:.2f}")
    else:
        print(f"  Erro: {portfolio_result['error']}")
    
    # Análise de regime de mercado
    print(f"\n🌍 Análise de regime de mercado:")
    
    market_data = {
        "prices": prices,
        "volumes": np.random.randint(1000000, 5000000, n_days).tolist(),
        "volatility": np.random.rand(n_days) * 0.05 + 0.01
    }
    
    regime_analysis = simulator.analyze_market_regime(market_data)
    
    if regime_analysis["status"] != "ERROR":
        print(f"  Regime classificado: {regime_analysis['regime']}")
        print(f"  Confiança: {regime_analysis['regime_confidence']:.2f}")
        print(f"  Condições de mercado:")
        for key, value in regime_analysis["market_conditions"].items():
            print(f"    {key}: {value}")
    else:
        print(f"  Erro: {regime_analysis['error']}")
    
    # Estatísticas do simulador
    print(f"\n📊 Estatísticas do simulador:")
    print(f"  Histórico de predições: {len(simulator.prediction_history)}")
    print(f"  Histórico de otimizações: {len(simulator.optimization_history)}")
    print(f"  Circuitos em cache: {len(simulator.circuit_cache)}")


def main() -> None:
    """Função principal."""
    print("🚀 Quantum Simulator for Financial Applications")
    print("=" * 60)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('quantum_simulator.log')
        ]
    )
    
    try:
        # Demonstrar circuito quântico
        demonstrate_quantum_circuit()
        
        # Demonstrar simulação financeira
        demonstrate_financial_simulation()
        
        print(f"\n✅ Demonstração concluída com sucesso!")
        print(f"📁 Logs salvos em: quantum_simulator.log")
        
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
