import streamlit as st
import plotly.graph_objects as go
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
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

@dataclass
class QuantumGate:
    id: str
    type: GateType
    target_qubit: int
    control_qubit: int = None
    rotation: float = 0.0
    duration: float = 0.0
    fidelity: float = 1.0
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type.value,
            'target_qubit': self.target_qubit,
            'control_qubit': self.control_qubit,
            'rotation': self.rotation,
            'duration': self.duration,
            'fidelity': self.fidelity
        }

@dataclass
class Qubit:
    id: str
    state: Tuple[complex, complex] = (1+0j, 0+0j)  # |0⟩ state
    entangled_with: List[str] = field(default_factory=list)
    phase: float = 0.0
    last_gate: str = None
    decoherence: float = 0.0
    
    def amplitude_0(self) -> float:
        """Amplitude for |0⟩ state"""
        return abs(self.state[0]) ** 2
    
    def amplitude_1(self) -> float:
        """Amplitude for |1⟩ state"""
        return abs(self.state[1]) ** 2
    
    def probability_1(self) -> float:
        """Probability of measuring |1⟩"""
        return self.amplitude_1()
    
    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'amplitude_0': self.amplitude_0(),
            'amplitude_1': self.amplitude_1(),
            'entangled_with': self.entangled_with,
            'phase': self.phase,
            'decoherence': self.decoherence
        }

@dataclass
class QuantumCircuitSim:
    id: str
    name: str
    qubits: List[Qubit]
    gates: List[QuantumGate]
    depth: int
    total_fidelity: float
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
            'created_at': self.created_at.strftime("%H:%M:%S")
        }

# ==================== SIMULADOR QUÂNTICO ====================
class QuantumCircuitSimulator:
    def __init__(self):
        self.qubits: List[Qubit] = []
        self.circuits: List[QuantumCircuitSim] = []
        self.metrics = {
            'total_qubits': 64,
            'quantum_supremacy': 3.7,
            'processing_power': 17500,  # QFLOPS
            'coherence_time': 12.5,  # μs
            'entanglement_ratio': 0.42,
            'gate_fidelity': 0.9987,
            'circuit_depth_avg': 8.3
        }
        self._initialize_qubits()
        self._initialize_circuits()
        self._animation_queue = queue.Queue()
        self._stop_animation = False
        
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
                decoherence=random.uniform(0, 0.2)
            )
            self.qubits.append(qubit)
    
    def _initialize_circuits(self):
        """Inicializa circuitos quânticos de exemplo"""
        circuit_names = [
            "Grover's Search",
            "Quantum Fourier Transform",
            "VQE Optimization",
            "Shor's Algorithm",
            "QAOA Max-Cut",
            "Quantum Neural Network",
            "Quantum Walk",
            "Error Correction"
        ]
        
        for i, name in enumerate(circuit_names):
            num_qubits = random.randint(4, 12)
            qubits = random.sample(self.qubits, min(num_qubits, len(self.qubits)))
            
            num_gates = random.randint(8, 25)
            gates = []
            for j in range(num_gates):
                gate = QuantumGate(
                    id=f"g_{i}_{j}",
                    type=random.choice(list(GateType)),
                    target_qubit=random.randint(0, num_qubits-1),
                    control_qubit=random.randint(0, num_qubits-1) if random.random() > 0.7 else None,
                    rotation=random.uniform(0, 2*math.pi),
                    duration=random.uniform(0.1, 2.0),
                    fidelity=random.uniform(0.95, 0.999)
                )
                gates.append(gate)
            
            circuit = QuantumCircuitSim(
                id=f"circuit_{i}",
                name=name,
                qubits=qubits,
                gates=gates,
                depth=random.randint(5, 15),
                total_fidelity=random.uniform(0.85, 0.99)
            )
            self.circuits.append(circuit)
    
    def update_animation(self):
        """Atualiza animação dos qubits"""
        while not self._stop_animation:
            # Atualizar fases dos qubits
            for qubit in self.qubits:
                # Evolução temporal (rotação de fase)
                qubit.phase += random.uniform(-0.1, 0.1)
                qubit.phase %= (2 * math.pi)
                
                # Aumento gradual de descoerência
                qubit.decoherence += random.uniform(-0.01, 0.02)
                qubit.decoherence = max(0, min(1, qubit.decoherence))
                
                # Oscilação aleatória de emaranhamento
                if random.random() < 0.05:  # 5% chance de alterar emaranhamento
                    if qubit.entangled_with and random.random() < 0.3:
                        qubit.entangled_with = []
                    elif not qubit.entangled_with and random.random() < 0.2:
                        partner = random.randint(0, 63)
                        if partner != int(qubit.id.split('_')[1]):
                            qubit.entangled_with = [f"q_{partner}"]
            
            # Atualizar métricas
            self.metrics['total_qubits'] = len(self.qubits)
            self.metrics['quantum_supremacy'] += random.uniform(-0.1, 0.1)
            self.metrics['quantum_supremacy'] = max(1.0, min(5.0, self.metrics['quantum_supremacy']))
            
            self.metrics['processing_power'] += random.uniform(-100, 200)
            self.metrics['processing_power'] = max(10000, min(30000, self.metrics['processing_power']))
            
            self.metrics['coherence_time'] += random.uniform(-0.2, 0.2)
            self.metrics['coherence_time'] = max(5.0, min(20.0, self.metrics['coherence_time']))
            
            time.sleep(0.05)  # 20 FPS
    
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
    
    # CSS personalizado
    st.markdown("""
        <style>
        .main {
            background-color: #0a0a0a;
            color: #e5e5e5;
        }
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #111827 100%);
        }
        .metric-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            border-color: rgba(6, 182, 212, 0.3);
            transform: translateY(-2px);
        }
        .circuit-card {
            background-color: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 0.75rem;
            margin-bottom: 0.75rem;
            transition: all 0.3s ease;
        }
        .circuit-card:hover {
            border-color: rgba(6, 182, 212, 0.5);
            background-color: rgba(0, 0, 0, 0.6);
        }
        .fidelity-bar {
            width: 100%;
            height: 6px;
            background-color: #1f2937;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        .fidelity-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            border-radius: 3px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .quantum-canvas {
            background-color: #050505;
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            overflow: hidden;
            position: relative;
        }
        .canvas-header {
            position: absolute;
            top: 0.5rem;
            left: 0.5rem;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            border: 1px solid rgba(55, 65, 81, 0.5);
            font-size: 0.7rem;
            font-weight: bold;
            color: #9ca3af;
            display: flex;
            align-items: center;
            gap: 0.25rem;
            z-index: 100;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar simulador
    if 'simulator' not in st.session_state:
        st.session_state.simulator = QuantumCircuitSimulator()
        st.session_state.simulator.start_animation()
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    simulator = st.session_state.simulator
    metrics = simulator.metrics
    circuits = simulator.circuits
    qubits = simulator.qubits
    
    # Barra superior de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; margin-bottom: 0.25rem;">
                    Qubits Totais
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: white;">
                    {metrics['total_qubits']}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; margin-bottom: 0.25rem;">
                    Supremacia Q
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: #10b981;">
                    {metrics['quantum_supremacy']:.1f}x
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; margin-bottom: 0.25rem;">
                    QFLOPS
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: #3b82f6;">
                    {(metrics['processing_power'] / 1000):.1f}K
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; margin-bottom: 0.25rem;">
                    Coerência (T₂)
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: #8b5cf6;">
                    {metrics['coherence_time']:.1f}μs
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Área principal de visualização
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
            <div class="quantum-canvas" style="height: 500px;">
                <div class="canvas-header">
                    <span>⚛️</span> MATRIZ DE ESTADO QUÂNTICO (REAL-TIME)
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Criar visualização quântica com Plotly
        fig = create_quantum_visualization(qubits)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
            <div style="font-size: 0.8rem; font-weight: bold; color: white; margin-bottom: 0.5rem; 
                      display: flex; align-items: center; gap: 0.25rem;">
                <span style="color: #06b6d4;">🔗</span> CIRCUITOS ATIVOS
            </div>
        """, unsafe_allow_html=True)
        
        for circuit in circuits:
            circuit_dict = circuit.to_dict()
            
            st.markdown(f"""
                <div class="circuit-card">
                    <div style="font-size: 0.7rem; font-weight: bold; color: white; margin-bottom: 0.25rem;">
                        {circuit.name}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.6rem; color: #9ca3af; margin-bottom: 0.25rem;">
                        <span>Qubits: {circuit_dict['num_qubits']}</span>
                        <span>Gates: {circuit_dict['num_gates']}</span>
                    </div>
                    <div style="font-size: 0.6rem; color: #6b7280; margin-bottom: 0.25rem;">
                        Profundidade: {circuit.depth}
                    </div>
                    <div class="fidelity-bar">
                        <div class="fidelity-fill" style="width: {circuit.total_fidelity * 100}%;"></div>
                    </div>
                    <div style="font-size: 0.5rem; text-align: right; color: #8b5cf6; margin-top: 0.25rem;">
                        Fidelidade: {(circuit.total_fidelity * 100):.1f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Atualizar periodicamente
    now = datetime.now()
    if (now - st.session_state.last_update).total_seconds() > 0.05:  # ~20 FPS
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
        if i >= cols * rows:  # Limitar ao grid
            break
            
        col = i % cols
        row = i // cols
        
        x = col * cell_size + cell_size / 2
        y = row * cell_size + cell_size / 2
        
        # Tamanho baseado na probabilidade de |1⟩
        prob_1 = qubit.probability_1()
        size = 5 + (prob_1 * 15)
        
        # Cor baseada na fase
        phase_hue = (qubit.phase / (2 * math.pi)) * 360
        color = f'hsl({phase_hue}, 70%, 60%)'
        
        # Texto hover
        hover_text = f"""
        Qubit: {qubit.id}<br>
        |0⟩: {qubit.amplitude_0():.3f}<br>
        |1⟩: {qubit.amplitude_1():.3f}<br>
        Phase: {qubit.phase:.2f} rad<br>
        Decoherence: {qubit.decoherence:.2%}<br>
        Entangled with: {', '.join(qubit.entangled_with) if qubit.entangled_with else 'None'}
        """
        
        x_positions.append(x)
        y_positions.append(y)
        sizes.append(size)
        colors.append(color)
        hover_texts.append(hover_text)
    
    # Criar figura
    fig = go.Figure()
    
    # Adicionar grade de fundo
    for col in range(cols + 1):
        fig.add_shape(
            type="line",
            x0=col * cell_size,
            y0=0,
            x1=col * cell_size,
            y1=rows * cell_size,
            line=dict(color="rgba(255, 255, 255, 0.05)", width=1)
        )
    
    for row in range(rows + 1):
        fig.add_shape(
            type="line",
            x0=0,
            y0=row * cell_size,
            x1=cols * cell_size,
            y1=row * cell_size,
            line=dict(color="rgba(255, 255, 255, 0.05)", width=1)
        )
    
    # Adicionar linhas de emaranhamento
    entanglement_added = set()
    for i, qubit in enumerate(qubits[:cols*rows]):
        for partner_id in qubit.entangled_with:
            try:
                partner_idx = int(partner_id.split('_')[1])
                if partner_idx < i:  # Evitar duplicatas
                    key = frozenset([i, partner_idx])
                    if key not in entanglement_added:
                        # Obter posições
                        col_i = i % cols
                        row_i = i // cols
                        col_p = partner_idx % cols
                        row_p = partner_idx // cols
                        
                        x_i = col_i * cell_size + cell_size / 2
                        y_i = row_i * cell_size + cell_size / 2
                        x_p = col_p * cell_size + cell_size / 2
                        y_p = row_p * cell_size + cell_size / 2
                        
                        # Adicionar linha
                        fig.add_trace(go.Scatter(
                            x=[x_i, x_p],
                            y=[y_i, y_p],
                            mode='lines',
                            line=dict(
                                color=f'rgba(139, 92, 246, {0.1 + random.random() * 0.2})',
                                width=1
                            ),
                            hoverinfo='skip',
                            showlegend=False
                        ))
                        
                        entanglement_added.add(key)
            except (ValueError, IndexError):
                continue
    
    # Adicionar qubits
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(color='white', width=1),
            opacity=0.8
        ),
        text=hover_texts,
        hoverinfo='text',
        name='Qubits'
    ))
    
    # Adicionar núcleos (pontos brancos)
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers',
        marker=dict(
            size=3,
            color='white',
            opacity=1.0
        ),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Configurar layout
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(5, 5, 5, 1)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, cols * cell_size]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, rows * cell_size],
            scaleanchor="x",
            scaleratio=1
        ),
        showlegend=False,
        hovermode='closest'
    )
    
    return fig

if __name__ == "__main__":
    main()