import streamlit as st
import plotly.graph_objects as go
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional
import random
from datetime import datetime, timedelta
import time
import math
from enum import Enum
import threading
import queue

# ==================== ENUMS E CLASSES ====================
class GateType(Enum):
    HADAMARD = "H"
    PAULI_X = "X"
    PAULI_Y = "Y"
    PAULI_Z = "Z"
    CNOT = "CNOT"
    SWAP = "SWAP"
    T = "T"
    S = "S"
    MEASURE = "M"
    RY = "RY"
    RX = "RX"
    RZ = "RZ"
    PHASE = "P"
    TOFFOLI = "CCNOT"
    FREDKIN = "CSWAP"

@dataclass
class QuantumGate:
    id: str
    type: GateType
    target_qubit: int
    control_qubit: Optional[int] = None
    control_qubit2: Optional[int] = None
    rotation: float = 0.0
    duration: float = 0.0
    fidelity: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type.value,
            'target_qubit': self.target_qubit,
            'control_qubit': self.control_qubit,
            'control_qubit2': self.control_qubit2,
            'rotation': self.rotation,
            'duration': self.duration,
            'fidelity': self.fidelity,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class Qubit:
    id: str
    state: Tuple[complex, complex] = (1+0j, 0+0j)  # |0⟩ state
    entangled_with: List[str] = field(default_factory=list)
    phase: float = 0.0
    last_gate: Optional[str] = None
    decoherence: float = 0.0
    temperature: float = 0.015  # Kelvin
    error_rate: float = 0.001
    coherence_time: float = 100.0  # μs
    last_interaction: datetime = field(default_factory=datetime.now)
    
    def amplitude_0(self) -> float:
        """Amplitude for |0⟩ state"""
        return abs(self.state[0]) ** 2
    
    def amplitude_1(self) -> float:
        """Amplitude for |1⟩ state"""
        return abs(self.state[1]) ** 2
    
    def probability_1(self) -> float:
        """Probability of measuring |1⟩"""
        return self.amplitude_1()
    
    def get_bloch_coordinates(self) -> Tuple[float, float, float]:
        """Retorna coordenadas na esfera de Bloch"""
        alpha, beta = self.state
        
        # Normalizar
        norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
        if norm == 0:
            return (0, 0, 1)  # |0⟩ state
        
        alpha /= norm
        beta /= norm
        
        # Calcular coordenadas esféricas
        theta = 2 * math.acos(abs(alpha))
        phi = np.angle(beta) - np.angle(alpha)
        
        # Converter para coordenadas cartesianas
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        
        return (x, y, z)
    
    def to_dict(self):
        x, y, z = self.get_bloch_coordinates()
        return {
            'id': self.id,
            'amplitude_0': self.amplitude_0(),
            'amplitude_1': self.amplitude_1(),
            'entangled_with': self.entangled_with,
            'phase': self.phase,
            'decoherence': self.decoherence,
            'temperature': self.temperature,
            'error_rate': self.error_rate,
            'coherence_time': self.coherence_time,
            'bloch_x': x,
            'bloch_y': y,
            'bloch_z': z,
            'last_interaction': self.last_interaction.isoformat()
        }

@dataclass
class QuantumCircuitSim:
    id: str
    name: str
    qubits: List[Qubit]
    gates: List[QuantumGate]
    depth: int
    total_fidelity: float
    description: str = ""
    complexity_score: float = 0.0
    estimated_runtime: float = 0.0
    success_probability: float = 0.95
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'qubits': [q.id for q in self.qubits],
            'num_qubits': len(self.qubits),
            'num_gates': len(self.gates),
            'depth': self.depth,
            'total_fidelity': self.total_fidelity,
            'complexity_score': self.complexity_score,
            'estimated_runtime': self.estimated_runtime,
            'success_probability': self.success_probability,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

@dataclass
class QuantumError:
    type: str
    qubit_id: str
    magnitude: float
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False

# ==================== SIMULADOR QUÂNTICO ====================
class QuantumCircuitSimulator:
    def __init__(self):
        self.qubits: List[Qubit] = []
        self.circuits: List[QuantumCircuitSim] = []
        self.errors: List[QuantumError] = []
        self.metrics = {
            'total_qubits': 64,
            'quantum_supremacy': 3.7,
            'processing_power': 17500,  # QFLOPS
            'coherence_time': 12.5,  # μs
            'entanglement_ratio': 0.42,
            'gate_fidelity': 0.9987,
            'circuit_depth_avg': 8.3,
            'error_rate': 0.0012,
            'quantum_volume': 512,
            'active_gates': 0,
            'quantum_noise': 0.05
        }
        self._initialize_qubits()
        self._initialize_circuits()
        self._animation_queue = queue.Queue()
        self._stop_animation = False
        self._metrics_history = {
            'quantum_supremacy': [],
            'processing_power': [],
            'coherence_time': [],
            'gate_fidelity': [],
            'timestamps': []
        }
        
    def _initialize_qubits(self):
        """Inicializa qubits com estados aleatórios"""
        self.qubits = []
        for i in range(64):  # 64 qubits total
            # Criar estado quântico aleatório
            angle = random.uniform(0, math.pi/2)
            state_0 = math.cos(angle)
            state_1 = math.sin(angle) * np.exp(1j * random.uniform(0, 2*math.pi))
            
            # Criar emaranhamentos aleatórios
            entangled_with = []
            if random.random() < 0.3:  # 30% chance de estar emaranhado
                partner = random.randint(0, 63)
                if partner != i:
                    entangled_with.append(f"q_{partner}")
            
            qubit = Qubit(
                id=f"q_{i}",
                state=(state_0, state_1),
                entangled_with=entangled_with,
                phase=random.uniform(0, 2*math.pi),
                decoherence=random.uniform(0, 0.2),
                temperature=random.uniform(0.01, 0.02),
                error_rate=random.uniform(0.0005, 0.002),
                coherence_time=random.uniform(50, 150)
            )
            self.qubits.append(qubit)
    
    def _initialize_circuits(self):
        """Inicializa circuitos quânticos de exemplo"""
        circuit_data = [
            ("Grover's Search", "Algoritmo de busca quântica", 8, 32),
            ("Quantum Fourier Transform", "Transformada de Fourier quântica", 10, 45),
            ("VQE Optimization", "Otimização variacional quântica", 6, 28),
            ("Shor's Algorithm", "Fatoração de números grandes", 12, 60),
            ("QAOA Max-Cut", "Otimização combinatória", 8, 35),
            ("Quantum Neural Network", "Rede neural quântica", 7, 40),
            ("Quantum Walk", "Passeio quântico", 5, 25),
            ("Error Correction", "Correção de erros quânticos", 9, 50)
        ]
        
        for i, (name, desc, num_qubits, num_gates) in enumerate(circuit_data):
            qubits = random.sample(self.qubits, min(num_qubits, len(self.qubits)))
            
            gates = []
            for j in range(num_gates):
                gate_type = random.choice(list(GateType))
                gate = QuantumGate(
                    id=f"g_{i}_{j}",
                    type=gate_type,
                    target_qubit=random.randint(0, num_qubits-1),
                    control_qubit=random.randint(0, num_qubits-1) if random.random() > 0.7 else None,
                    control_qubit2=random.randint(0, num_qubits-1) if gate_type == GateType.TOFFOLI and random.random() > 0.5 else None,
                    rotation=random.uniform(0, 2*math.pi),
                    duration=random.uniform(0.1, 2.0),
                    fidelity=random.uniform(0.98, 0.999)
                )
                gates.append(gate)
            
            complexity = num_qubits * num_gates / 10.0
            circuit = QuantumCircuitSim(
                id=f"circuit_{i}",
                name=name,
                qubits=qubits,
                gates=gates,
                depth=random.randint(5, 15),
                total_fidelity=random.uniform(0.92, 0.99),
                description=desc,
                complexity_score=complexity,
                estimated_runtime=num_gates * 0.1,
                success_probability=random.uniform(0.88, 0.98)
            )
            self.circuits.append(circuit)
    
    def _update_metrics_history(self):
        """Atualiza histórico de métricas"""
        timestamp = datetime.now()
        self._metrics_history['timestamps'].append(timestamp)
        self._metrics_history['quantum_supremacy'].append(self.metrics['quantum_supremacy'])
        self._metrics_history['processing_power'].append(self.metrics['processing_power'])
        self._metrics_history['coherence_time'].append(self.metrics['coherence_time'])
        self._metrics_history['gate_fidelity'].append(self.metrics['gate_fidelity'])
        
        # Manter apenas últimos 100 pontos
        if len(self._metrics_history['timestamps']) > 100:
            for key in self._metrics_history:
                self._metrics_history[key] = self._metrics_history[key][-100:]
    
    def generate_error(self):
        """Gera erro quântico aleatório"""
        error_types = ['Decoherence', 'Phase Error', 'Amplitude Damping', 'Bit Flip', 'Phase Flip']
        qubit = random.choice(self.qubits)
        
        error = QuantumError(
            type=random.choice(error_types),
            qubit_id=qubit.id,
            magnitude=random.uniform(0.01, 0.1)
        )
        self.errors.append(error)
        
        # Aplicar efeito do erro no qubit
        qubit.decoherence += error.magnitude
        qubit.error_rate += error.magnitude * 0.01
        
        return error
    
    def update_animation(self):
        """Atualiza animação dos qubits"""
        while not self._stop_animation:
            # Atualizar fases dos qubits
            for qubit in self.qubits:
                # Evolução temporal (rotação de fase)
                phase_change = random.uniform(-0.08, 0.08) * (1 - qubit.decoherence)
                qubit.phase += phase_change
                qubit.phase %= (2 * math.pi)
                
                # Aumento gradual de descoerência
                decoherence_change = random.uniform(-0.005, 0.015)
                qubit.decoherence += decoherence_change
                qubit.decoherence = max(0, min(0.5, qubit.decoherence))
                
                # Oscilação aleatória de emaranhamento
                if random.random() < 0.03:  # 3% chance de alterar emaranhamento
                    if qubit.entangled_with and random.random() < 0.4:
                        qubit.entangled_with = []
                    elif not qubit.entangled_with and random.random() < 0.15:
                        partner = random.randint(0, 63)
                        if partner != int(qubit.id.split('_')[1]):
                            qubit.entangled_with = [f"q_{partner}"]
                
                # Atualizar tempo desde última interação
                time_since_interaction = (datetime.now() - qubit.last_interaction).total_seconds()
                if time_since_interaction > 1.0 and random.random() < 0.01:
                    qubit.last_interaction = datetime.now()
            
            # Atualizar métricas com variações mais realistas
            self.metrics['total_qubits'] = len(self.qubits)
            
            # Quantum supremacy com drift positivo
            supremacy_change = random.uniform(-0.05, 0.08)
            self.metrics['quantum_supremacy'] += supremacy_change
            self.metrics['quantum_supremacy'] = max(1.0, min(8.0, self.metrics['quantum_supremacy']))
            
            # Processing power com crescimento geral
            power_change = random.uniform(-80, 120)
            self.metrics['processing_power'] += power_change
            self.metrics['processing_power'] = max(15000, min(25000, self.metrics['processing_power']))
            
            # Coherence time com decaimento gradual
            coherence_change = random.uniform(-0.15, 0.1)
            self.metrics['coherence_time'] += coherence_change
            self.metrics['coherence_time'] = max(5.0, min(25.0, self.metrics['coherence_time']))
            
            # Gate fidelity com pequenas oscilações
            fidelity_change = random.uniform(-0.0001, 0.0001)
            self.metrics['gate_fidelity'] += fidelity_change
            self.metrics['gate_fidelity'] = max(0.99, min(0.9999, self.metrics['gate_fidelity']))
            
            # Quantum noise varia dinamicamente
            self.metrics['quantum_noise'] = 0.03 + random.uniform(-0.01, 0.01)
            
            # Atualizar gates ativos
            self.metrics['active_gates'] = sum(len(circuit.gates) for circuit in self.circuits)
            
            # Gerar erro aleatório ocasionalmente
            if random.random() < 0.02:  # 2% chance por ciclo
                self.generate_error()
            
            # Atualizar histórico
            self._update_metrics_history()
            
            time.sleep(0.05)  # 20 FPS
    
    def get_qubit_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos qubits"""
        decoherence_values = [q.decoherence for q in self.qubits]
        entanglement_counts = [len(q.entangled_with) for q in self.qubits]
        
        return {
            'avg_decoherence': np.mean(decoherence_values),
            'max_decoherence': np.max(decoherence_values),
            'entangled_qubits': sum(1 for q in self.qubits if q.entangled_with),
            'avg_entanglement': np.mean(entanglement_counts),
            'total_errors': len(self.errors),
            'unresolved_errors': sum(1 for e in self.errors if not e.resolved)
        }
    
    def start_animation(self):
        """Inicia thread de animação"""
        self._stop_animation = False
        animation_thread = threading.Thread(target=self.update_animation, daemon=True)
        animation_thread.start()
    
    def stop_animation(self):
        """Para a animação"""
        self._stop_animation = True

# ==================== VISUALIZADOR STREAMLIT ====================
def main():
    st.set_page_config(
        page_title="Visualizador Quântico",
        page_icon="⚛️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS personalizado melhorado
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #0f172a 100%);
        }
        .main {
            color: #e5e5e5;
        }
        
        /* Cartões de métricas */
        .metric-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        .metric-card:hover {
            border-color: rgba(6, 182, 212, 0.4);
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 25px -5px rgba(6, 182, 212, 0.2);
        }
        
        /* Cartões de circuito */
        .circuit-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.7), rgba(30, 41, 59, 0.8));
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            transition: all 0.3s ease;
        }
        .circuit-card:hover {
            border-color: rgba(139, 92, 246, 0.5);
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.95));
            transform: translateX(4px);
        }
        
        /* Barras de fidelidade */
        .fidelity-bar {
            width: 100%;
            height: 8px;
            background: rgba(30, 41, 59, 0.8);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
            position: relative;
        }
        .fidelity-fill {
            height: 100%;
            background: linear-gradient(90deg, 
                #3b82f6 0%, 
                #8b5cf6 50%, 
                #ec4899 100%);
            border-radius: 4px;
            position: relative;
            transition: width 0.5s ease;
        }
        .fidelity-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg,
                transparent 0%,
                rgba(255, 255, 255, 0.1) 50%,
                transparent 100%);
            animation: shine 2s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        /* Canvas quântico */
        .quantum-canvas {
            background: rgba(5, 5, 5, 0.9);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            backdrop-filter: blur(10px);
        }
        
        .canvas-header {
            position: absolute;
            top: 0.75rem;
            left: 0.75rem;
            background: rgba(0, 0, 0, 0.7);
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            border: 1px solid rgba(55, 65, 81, 0.5);
            font-size: 0.75rem;
            font-weight: 600;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            z-index: 100;
            backdrop-filter: blur(5px);
        }
        
        /* Badges */
        .status-badge {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: 0.5rem;
        }
        .status-running { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
        .status-paused { background: rgba(251, 191, 36, 0.2); color: #fbbf24; }
        .status-error { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(30, 41, 59, 0.5);
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1rem;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(15, 23, 42, 0.9);
            border-bottom: 2px solid #06b6d4;
        }
        
        /* Tooltips */
        .tooltip {
            position: relative;
            cursor: help;
        }
        .tooltip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            white-space: nowrap;
            z-index: 1000;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar simulador
    if 'simulator' not in st.session_state:
        st.session_state.simulator = QuantumCircuitSimulator()
        st.session_state.simulator.start_animation()
        st.session_state.animation_running = True
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    simulator = st.session_state.simulator
    metrics = simulator.metrics
    circuits = simulator.circuits
    qubits = simulator.qubits
    errors = simulator.errors
    
    # Header com controles
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("""
            <h1 style="margin: 0; color: white; font-size: 2.2rem;">
                ⚛️ Quantum Circuit Dashboard
                <span class="status-badge status-running">LIVE</span>
            </h1>
            <p style="color: #94a3b8; margin: 0.25rem 0 1rem 0; font-size: 0.9rem;">
                Visualização em tempo real de estados quânticos e métricas do sistema
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("⏸️ Pausar" if st.session_state.animation_running else "▶️ Retomar", 
                    use_container_width=True, type="secondary"):
            if st.session_state.animation_running:
                simulator.stop_animation()
                st.session_state.animation_running = False
            else:
                simulator.start_animation()
                st.session_state.animation_running = True
            st.rerun()
    
    with col3:
        if st.button("🔄 Resetar", use_container_width=True, type="secondary"):
            st.session_state.simulator = QuantumCircuitSimulator()
            st.session_state.simulator.start_animation()
            st.session_state.animation_running = True
            st.session_state.last_update = datetime.now()
            st.rerun()
    
    st.divider()
    
    # Seção de métricas expandida
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card tooltip" data-tooltip="Total de qubits no sistema">
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">
                    QUBITS TOTAIS
                </div>
                <div style="font-family: 'SF Mono', monospace; font-size: 2rem; font-weight: bold; color: white;">
                    {metrics['total_qubits']}
                </div>
                <div style="font-size: 0.7rem; color: #4ade80; margin-top: 0.25rem;">
                    ↑ {random.randint(1, 5)}% desde ontem
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card tooltip" data-tooltip="Fator de supremacia quântica">
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">
                    SUPREMACIA Q
                </div>
                <div style="font-family: 'SF Mono', monospace; font-size: 2rem; font-weight: bold; color: #10b981;">
                    {metrics['quantum_supremacy']:.1f}x
                </div>
                <div style="font-size: 0.7rem; color: #fbbf24; margin-top: 0.25rem;">
                    {random.choice(['Estável', 'Crescendo', 'Ótimo'])}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card tooltip" data-tooltip="Poder de processamento quântico">
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">
                    QFLOPS
                </div>
                <div style="font-family: 'SF Mono', monospace; font-size: 2rem; font-weight: bold; color: #3b82f6;">
                    {(metrics['processing_power'] / 1000):.1f}K
                </div>
                <div style="font-size: 0.7rem; color: #60a5fa; margin-top: 0.25rem;">
                    {random.randint(80, 120)}% da capacidade
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card tooltip" data-tooltip="Tempo de coerência quântica">
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">
                    COERÊNCIA (T₂)
                </div>
                <div style="font-family: 'SF Mono', monospace; font-size: 2rem; font-weight: bold; color: #8b5cf6;">
                    {metrics['coherence_time']:.1f}μs
                </div>
                <div style="font-size: 0.7rem; color: #a78bfa; margin-top: 0.25rem;">
                    Alvo: 20μs
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        qubit_stats = simulator.get_qubit_statistics()
        st.markdown(f"""
            <div class="metric-card tooltip" data-tooltip="Taxa de emaranhamento do sistema">
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">
                    EMARANHAMENTO
                </div>
                <div style="font-family: 'SF Mono', monospace; font-size: 2rem; font-weight: bold; color: #ec4899;">
                    {qubit_stats['entangled_qubits']}
                </div>
                <div style="font-size: 0.7rem; color: #f472b6; margin-top: 0.25rem;">
                    {qubit_stats['avg_entanglement']:.1f} conexões/qubit
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Área principal com abas
    tab1, tab2, tab3 = st.tabs(["🌌 Visualização Quântica", "📊 Circuitos Ativos", "⚡ Estatísticas"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
                <div class="quantum-canvas" style="height: 500px;">
                    <div class="canvas-header">
                        <span>🌀</span> ESTADO QUÂNTICO EM TEMPO REAL
                        <span style="color: #06b6d4; margin-left: auto; font-size: 0.65rem;">
                            {timestamp}
                        </span>
                    </div>
                </div>
            """.format(timestamp=datetime.now().strftime("%H:%M:%S")), unsafe_allow_html=True)
            
            # Criar visualização quântica com Plotly
            fig = create_quantum_visualization(qubits)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Gráfico de métricas históricas
            if simulator._metrics_history['timestamps']:
                fig_history = create_metrics_history_chart(simulator._metrics_history)
                st.plotly_chart(fig_history, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Seção de circuitos ativos
            st.markdown("""
                <div style="font-size: 0.85rem; font-weight: bold; color: white; margin-bottom: 0.75rem; 
                          display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #06b6d4;">📡</span> CIRCUITOS ATIVOS
                    <span style="color: #94a3b8; font-size: 0.7rem; margin-left: auto;">
                        {count}
                    </span>
                </div>
            """.format(count=len(circuits)), unsafe_allow_html=True)
            
            for circuit in circuits:
                circuit_dict = circuit.to_dict()
                success_color = "#10b981" if circuit.success_probability > 0.9 else "#fbbf24"
                
                st.markdown(f"""
                    <div class="circuit-card">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                            <div style="font-size: 0.8rem; font-weight: bold; color: white;">
                                {circuit.name}
                            </div>
                            <span style="font-size: 0.6rem; color: {success_color};">
                                {circuit.success_probability:.0%}
                            </span>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; font-size: 0.65rem; color: #94a3b8; margin-bottom: 0.4rem;">
                            <span>🧮 {circuit_dict['num_qubits']}Q</span>
                            <span>⚡ {circuit_dict['num_gates']}G</span>
                            <span>📏 {circuit.depth}D</span>
                        </div>
                        
                        <div style="font-size: 0.6rem; color: #6b7280; margin-bottom: 0.4rem; line-height: 1.2;">
                            {circuit.description}
                        </div>
                        
                        <div class="fidelity-bar">
                            <div class="fidelity-fill" style="width: {circuit.total_fidelity * 100}%;"></div>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; font-size: 0.55rem; margin-top: 0.4rem;">
                            <span style="color: #8b5cf6;">Fidelidade: {(circuit.total_fidelity * 100):.1f}%</span>
                            <span style="color: #94a3b8;">Complexidade: {circuit.complexity_score:.1f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # Visualização detalhada dos circuitos
        st.markdown("### 📋 Detalhes dos Circuitos")
        
        for circuit in circuits:
            with st.expander(f"{circuit.name} - {len(circuit.qubits)} Qubits, {len(circuit.gates)} Gates"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 Estatísticas**")
                    stats_data = {
                        "Profundidade": circuit.depth,
                        "Fidelidade Total": f"{circuit.total_fidelity * 100:.2f}%",
                        "Probabilidade de Sucesso": f"{circuit.success_probability * 100:.1f}%",
                        "Tempo Estimado": f"{circuit.estimated_runtime:.2f}s",
                        "Score de Complexidade": f"{circuit.complexity_score:.1f}"
                    }
                    
                    for key, value in stats_data.items():
                        st.markdown(f"• **{key}:** {value}")
                
                with col2:
                    st.markdown("**🎯 Últimas Operações**")
                    recent_gates = circuit.gates[-5:] if len(circuit.gates) > 5 else circuit.gates
                    for gate in recent_gates:
                        control_info = ""
                        if gate.control_qubit is not None:
                            control_info = f" (C{gate.control_qubit})"
                        st.markdown(f"• `{gate.type.value}` → Q{gate.target_qubit}{control_info}")
                
                st.markdown(f"**📝 Descrição:** {circuit.description}")
    
    with tab3:
        # Estatísticas do sistema
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Estatísticas dos Qubits")
            qubit_stats = simulator.get_qubit_statistics()
            
            stats_fig = go.Figure()
            
            # Gráfico de pizza para estados de emaranhamento
            entangled = qubit_stats['entangled_qubits']
            not_entangled = len(qubits) - entangled
            
            stats_fig.add_trace(go.Pie(
                labels=['Emaranhados', 'Isolados'],
                values=[entangled, not_entangled],
                hole=0.4,
                marker_colors=['#8b5cf6', '#3b82f6'],
                textinfo='percent+label'
            ))
            
            stats_fig.update_layout(
                template='plotly_dark',
                height=300,
                margin=dict(l=20, r=20, t=30, b=20),
                showlegend=True
            )
            
            st.plotly_chart(stats_fig, use_container_width=True)
            
            # Métricas numéricas
            st.metric("Descoerência Média", f"{qubit_stats['avg_decoherence']:.3f}")
            st.metric("Descoerência Máxima", f"{qubit_stats['max_decoherence']:.3f}")
            st.metric("Erros Ativos", f"{qubit_stats['unresolved_errors']}/{qubit_stats['total_errors']}")
        
        with col2:
            st.markdown("### ⚡ Status do Sistema")
            
            # Status das métricas
            metric_status = [
                ("Gate Fidelity", metrics['gate_fidelity'], 0.995, "gate_fidelity"),
                ("Quantum Volume", metrics['quantum_volume'], 512, "quantum_volume"),
                ("Noise Level", metrics['quantum_noise'], 0.05, "quantum_noise"),
                ("Error Rate", metrics['error_rate'], 0.001, "error_rate")
            ]
            
            for name, value, target, key in metric_status:
                percentage = (value / target * 100) if target > 0 else 0
                color = "#10b981" if percentage >= 90 else "#fbbf24" if percentage >= 75 else "#ef4444"
                
                st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span style="font-size: 0.85rem; color: #94a3b8;">{name}</span>
                            <span style="font-size: 0.85rem; color: {color}; font-weight: bold;">
                                {percentage:.1f}%
                            </span>
                        </div>
                        <div style="width: 100%; height: 6px; background: rgba(30, 41, 59, 0.5); border-radius: 3px; overflow: hidden;">
                            <div style="width: {min(percentage, 100)}%; height: 100%; background: {color}; border-radius: 3px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Lista de erros recentes
            if errors:
                st.markdown("### ⚠️ Erros Recentes")
                recent_errors = errors[-3:] if len(errors) > 3 else errors
                for error in recent_errors:
                    status_color = "#ef4444" if not error.resolved else "#10b981"
                    status_text = "Pendente" if not error.resolved else "Resolvido"
                    st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.1); padding: 0.5rem; border-radius: 6px; margin-bottom: 0.5rem;">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="font-size: 0.8rem; font-weight: bold; color: #ef4444;">{error.type}</span>
                                <span style="font-size: 0.7rem; color: {status_color};">{status_text}</span>
                            </div>
                            <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 0.25rem;">
                                Qubit: {error.qubit_id} | Magnitude: {error.magnitude:.3f}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Rodapé
    st.divider()
    st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.75rem; padding: 1rem;">
            ⚛️ Quantum Dashboard v2.0 • Última atualização: {timestamp} • {fps:.0f} FPS
        </div>
    """.format(
        timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3],
        fps=1 / max(0.001, (datetime.now() - st.session_state.last_update).total_seconds())
    ), unsafe_allow_html=True)
    
    # Atualizar periodicamente
    now = datetime.now()
    if (now - st.session_state.last_update).total_seconds() > 0.05 and st.session_state.animation_running:  # ~20 FPS
        st.session_state.last_update = now
        st.rerun()

def create_quantum_visualization(qubits: List[Qubit]) -> go.Figure:
    """Cria visualização quântica interativa"""
    
    # Configurar layout da grade
    cols = 8
    rows = 8
    cell_size = 1.0
    
    # Preparar dados para scatter plot
    x_positions = []
    y_positions = []
    sizes = []
    colors = []
    hover_texts = []
    
    for i, qubit in enumerate(qubits):
        if i >= cols * rows:
            break
            
        col = i % cols
        row = i // cols
        
        x = col * cell_size + cell_size / 2
        y = row * cell_size + cell_size / 2
        
        # Tamanho baseado na probabilidade de |1⟩
        prob_1 = qubit.probability_1()
        size = 8 + (prob_1 * 20)
        
        # Cor baseada na fase com variação de saturação baseada na descoerência
        phase_hue = (qubit.phase / (2 * math.pi)) * 360
        saturation = max(30, 100 - qubit.decoherence * 200)
        lightness = 50 + qubit.probability_1() * 20
        color = f'hsl({phase_hue}, {saturation}%, {lightness}%)'
        
        # Texto hover melhorado
        hover_text = f"""
        <b>Qubit {qubit.id}</b><br>
        ───────────<br>
        |0⟩ Amplitude: {qubit.amplitude_0():.4f}<br>
        |1⟩ Amplitude: {qubit.amplitude_1():.4f}<br>
        |1⟩ Probability: {qubit.probability_1():.2%}<br>
        Phase: {qubit.phase:.3f} rad<br>
        Decoherence: {qubit.decoherence:.2%}<br>
        Temperature: {qubit.temperature:.3f} K<br>
        Error Rate: {qubit.error_rate:.4%}<br>
        Coherence Time: {qubit.coherence_time:.1f} μs<br>
        Entangled with: {', '.join(qubit.entangled_with) if qubit.entangled_with else 'None'}
        """
        
        x_positions.append(x)
        y_positions.append(y)
        sizes.append(size)
        colors.append(color)
        hover_texts.append(hover_text)
    
    # Criar figura
    fig = go.Figure()
    
    # Adicionar grade de fundo com gradiente
    for col in range(cols + 1):
        fig.add_shape(
            type="line",
            x0=col * cell_size,
            y0=0,
            x1=col * cell_size,
            y1=rows * cell_size,
            line=dict(color="rgba(255, 255, 255, 0.03)", width=1, dash="dot")
        )
    
    for row in range(rows + 1):
        fig.add_shape(
            type="line",
            x0=0,
            y0=row * cell_size,
            x1=cols * cell_size,
            y1=row * cell_size,
            line=dict(color="rgba(255, 255, 255, 0.03)", width=1, dash="dot")
        )
    
    # Adicionar linhas de emaranhamento com gradiente
    entanglement_added = set()
    for i, qubit in enumerate(qubits[:cols*rows]):
        for partner_id in qubit.entangled_with:
            try:
                partner_idx = int(partner_id.split('_')[1])
                if partner_idx < i:
                    key = frozenset([i, partner_idx])
                    if key not in entanglement_added:
                        col_i = i % cols
                        row_i = i // cols
                        col_p = partner_idx % cols
                        row_p = partner_idx // cols
                        
                        x_i = col_i * cell_size + cell_size / 2
                        y_i = row_i * cell_size + cell_size / 2
                        x_p = col_p * cell_size + cell_size / 2
                        y_p = row_p * cell_size + cell_size / 2
                        
                        # Calcular força do emaranhamento
                        strength = random.uniform(0.2, 0.4)
                        
                        fig.add_trace(go.Scatter(
                            x=[x_i, x_p],
                            y=[y_i, y_p],
                            mode='lines',
                            line=dict(
                                color=f'rgba(139, 92, 246, {strength})',
                                width=1 + strength * 2,
                                dash='dash'
                            ),
                            hoverinfo='skip',
                            showlegend=False
                        ))
                        
                        entanglement_added.add(key)
            except (ValueError, IndexError):
                continue
    
    # Adicionar qubits com efeito de brilho
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(color='rgba(255, 255, 255, 0.8)', width=1.5),
            opacity=0.9,
            symbol='circle'
        ),
        text=hover_texts,
        hoverinfo='text',
        name='Qubits',
        hovertemplate='%{text}<extra></extra>'
    ))
    
    # Adicionar núcleos com brilho
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers',
        marker=dict(
            size=[s/3 for s in sizes],
            color='white',
            opacity=0.6
        ),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Configurar layout avançado
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(5, 5, 5, 0.95)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.5, cols * cell_size + 0.5],
            constrain="domain"
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.5, rows * cell_size + 0.5],
            scaleanchor="x",
            scaleratio=1,
            constrain="domain"
        ),
        showlegend=False,
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="rgba(0, 0, 0, 0.8)",
            font_size=12,
            font_family="monospace"
        )
    )
    
    return fig

def create_metrics_history_chart(metrics_history: Dict[str, List]) -> go.Figure:
    """Cria gráfico de histórico de métricas"""
    
    if not metrics_history['timestamps']:
        return go.Figure()
    
    fig = go.Figure()
    
    # Adicionar linhas para cada métrica
    colors = {
        'quantum_supremacy': '#10b981',
        'processing_power': '#3b82f6',
        'coherence_time': '#8b5cf6',
        'gate_fidelity': '#ec4899'
    }
    
    for metric_name, color in colors.items():
        if metric_name in metrics_history and metrics_history[metric_name]:
            fig.add_trace(go.Scatter(
                x=metrics_history['timestamps'],
                y=metrics_history[metric_name],
                mode='lines',
                name=metric_name.replace('_', ' ').title(),
                line=dict(color=color, width=2),
                opacity=0.8
            ))
    
    fig.update_layout(
        template='plotly_dark',
        height=250,
        margin=dict(l=40, r=20, t=30, b=40),
        xaxis_title="Tempo",
        yaxis_title="Valor",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    return fig

if __name__ == "__main__":
    main()