import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import random
from datetime import datetime, timedelta
import time
from enum import Enum
import threading
import queue
import math

# ==================== ENUMS E CLASSES ====================
class NetworkStatus(Enum):
    INITIALIZING = "INITIALIZING"
    TRAINING = "TRAINING"
    IDLE = "IDLE"
    ERROR = "ERROR"
    COMPLETE = "COMPLETE"

@dataclass
class MetricData:
    timestamp: datetime
    qubits_active: int
    temperature: float  # Kelvin
    quantum_fidelity: float
    ops_per_second: float
    entanglement_ratio: float
    coherence_time: float
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.strftime("%H:%M:%S"),
            'qubitsActive': self.qubits_active,
            'temperature': self.temperature,
            'quantumFidelity': self.quantum_fidelity,
            'opsPerSecond': self.ops_per_second,
            'entanglementRatio': self.entanglement_ratio,
            'coherenceTime': self.coherence_time
        }

@dataclass
class NetworkInfo:
    total_neurons: int
    total_layers: int
    quantum_advantage: float
    current_epoch: int
    memory_usage: float
    learning_rate: float
    model_size: float
    
    def to_dict(self):
        return {
            'totalNeurons': self.total_neurons,
            'totalLayers': self.total_layers,
            'quantumAdvantage': self.quantum_advantage,
            'currentEpoch': self.current_epoch,
            'memoryUsage': self.memory_usage,
            'learningRate': self.learning_rate,
            'modelSize': self.model_size
        }

# ==================== BIBLIOTECA QUÂNTICA ====================
class QuantumLibrary:
    def __init__(self):
        self.status = NetworkStatus.INITIALIZING
        self.real_time_metrics: List[MetricData] = []
        self.log_messages: List[str] = []
        self.network_info = NetworkInfo(
            total_neurons=2048,
            total_layers=12,
            quantum_advantage=3.7,
            current_epoch=42,
            memory_usage=2.3,  # GB
            learning_rate=0.001,
            model_size=45.6  # MB
        )
        self._training = False
        self._training_thread = None
        self._init_time = datetime.now()
        
        # Inicializar logs
        self.log_messages = [
            "[INFO] Quantum Core v6.1 inicializado",
            "[INFO] Carregando arquitetura híbrida",
            "[INFO] 2048 neurônios quânticos detectados",
            "[INFO] Sistema de resfriamento: 0.015K",
            "[INFO] Fidelidade inicial: 0.9987",
            "[INFO] Preparando camadas convolucionais",
            "[INFO] Emaranhamento quântico estabelecido"
        ]
        
        # Inicializar métricas
        self._generate_initial_metrics()
    
    def _generate_initial_metrics(self):
        """Gera métricas iniciais"""
        base_time = self._init_time
        for i in range(100):
            metric = MetricData(
                timestamp=base_time - timedelta(seconds=(100-i)*5),
                qubits_active=random.randint(1900, 2048),
                temperature=0.015 + random.random() * 0.002,
                quantum_fidelity=0.995 + random.random() * 0.005,
                ops_per_second=random.uniform(1.5e6, 2.5e6),
                entanglement_ratio=random.uniform(0.3, 0.5),
                coherence_time=random.uniform(8, 15)
            )
            self.real_time_metrics.append(metric)
    
    def start_training(self):
        """Inicia treinamento da rede neural quântica"""
        if self._training:
            return
        
        self.status = NetworkStatus.TRAINING
        self._training = True
        
        # Adicionar log
        self.log_messages.append(f"[TRAINING] Iniciando treinamento em {datetime.now().strftime('%H:%M:%S')}")
        self.log_messages.append("[TRAINING] Otimizando pesos quânticos")
        
        # Iniciar thread de treinamento
        self._training_thread = threading.Thread(target=self._training_loop, daemon=True)
        self._training_thread.start()
    
    def stop_training(self):
        """Para o treinamento"""
        self._training = False
        self.status = NetworkStatus.IDLE
        self.log_messages.append(f"[TRAINING] Treinamento interrompido em {datetime.now().strftime('%H:%M:%S')}")
    
    def _training_loop(self):
        """Loop de treinamento em background"""
        epoch = self.network_info.current_epoch
        
        while self._training:
            try:
                # Atualizar métricas durante treinamento
                self._update_training_metrics()
                
                # Atualizar informações da rede
                self.network_info.current_epoch += 1
                self.network_info.quantum_advantage += random.uniform(-0.01, 0.03)
                self.network_info.quantum_advantage = max(1.0, min(5.0, self.network_info.quantum_advantage))
                
                # Adicionar logs ocasionais
                if random.random() > 0.7:
                    messages = [
                        "[TRAINING] Backpropagation quântica concluída",
                        "[TRAINING] Gradientes estabilizados",
                        "[TRAINING] Camada convolucional otimizada",
                        "[TRAINING] Emaranhamento reforçado",
                        "[TRAINING] Ruído quântico reduzido"
                    ]
                    self.log_messages.append(random.choice(messages))
                
                time.sleep(2)  # Simular processamento
                
            except Exception as e:
                self.log_messages.append(f"[ERROR] Erro no treinamento: {str(e)}")
                break
    
    def _update_training_metrics(self):
        """Atualiza métricas durante treinamento"""
        last_metric = self.real_time_metrics[-1] if self.real_time_metrics else None
        
        if last_metric:
            new_metric = MetricData(
                timestamp=datetime.now(),
                qubits_active=last_metric.qubits_active + random.randint(-5, 10),
                temperature=last_metric.temperature + random.uniform(-0.0005, 0.001),
                quantum_fidelity=last_metric.quantum_fidelity + random.uniform(-0.0001, 0.0003),
                ops_per_second=last_metric.ops_per_second + random.uniform(-100000, 200000),
                entanglement_ratio=last_metric.entanglement_ratio + random.uniform(-0.01, 0.02),
                coherence_time=last_metric.coherence_time + random.uniform(-0.1, 0.2)
            )
            
            # Garantir limites físicos
            new_metric.qubits_active = max(1800, min(2048, new_metric.qubits_active))
            new_metric.temperature = max(0.010, min(0.030, new_metric.temperature))
            new_metric.quantum_fidelity = max(0.95, min(1.0, new_metric.quantum_fidelity))
            new_metric.entanglement_ratio = max(0.1, min(0.8, new_metric.entanglement_ratio))
            new_metric.coherence_time = max(5.0, min(20.0, new_metric.coherence_time))
            
            self.real_time_metrics.append(new_metric)
            
            # Manter apenas últimos 100 pontos
            if len(self.real_time_metrics) > 100:
                self.real_time_metrics = self.real_time_metrics[-100:]
    
    def save_model(self):
        """Simula salvamento do modelo"""
        self.log_messages.append(f"[SAVE] Modelo salvo em {datetime.now().strftime('%H:%M:%S')}")
        self.log_messages.append("[SAVE] 45.6MB armazenados no sistema de arquivos quânticos")
    
    def get_network_info(self) -> NetworkInfo:
        """Retorna informações da rede"""
        return self.network_info
    
    @property
    def logMessages(self):
        return self.log_messages

# ==================== COMPONENTE DE VISUALIZAÇÃO NEURAL ====================
class NodeVisualizer:
    def __init__(self):
        self.layers = [
            {'count': 8, 'name': "INPUT"},
            {'count': 16, 'name': "HIDDEN_1"},
            {'count': 16, 'name': "HIDDEN_2"},
            {'count': 12, 'name': "QUANTUM_PROC"},
            {'count': 8, 'name': "FUSION"},
            {'count': 4, 'name': "OUTPUT"}
        ]
    
    def create_visualization(self, is_training: bool):
        """Cria visualização da rede neural"""
        fig = go.Figure()
        
        # Adicionar grade de fundo
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,1)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[0, 100]
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[0, 100]
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            showlegend=False
        )
        
        # Adicionar grade CSS-style
        for x in range(0, 101, 5):
            fig.add_shape(
                type="line",
                x0=x, y0=0,
                x1=x, y1=100,
                line=dict(color="rgba(51, 51, 51, 0.1)", width=1)
            )
        
        for y in range(0, 101, 5):
            fig.add_shape(
                type="line",
                x0=0, y0=y,
                x1=100, y1=y,
                line=dict(color="rgba(51, 51, 51, 0.1)", width=1)
            )
        
        # Posicionar camadas
        num_layers = len(self.layers)
        x_positions = np.linspace(10, 90, num_layers)
        
        # Desenhar conexões (simplificado)
        for layer_idx, (layer, x) in enumerate(zip(self.layers[:-1], x_positions[:-1])):
            next_x = x_positions[layer_idx + 1]
            
            # Algumas conexões aleatórias
            for _ in range(min(layer['count'], 5)):
                y1 = random.uniform(10, 90)
                y2 = random.uniform(10, 90)
                
                fig.add_trace(go.Scatter(
                    x=[x, next_x],
                    y=[y1, y2],
                    mode='lines',
                    line=dict(color='rgba(55, 65, 81, 0.2)', width=0.5),
                    hoverinfo='skip'
                ))
        
        # Desenhar nós
        for layer_idx, (layer, x) in enumerate(zip(self.layers, x_positions)):
            is_quantum = "QUANTUM" in layer['name']
            
            # Distribuir nós verticalmente
            y_positions = np.linspace(10, 90, layer['count'])
            
            for y in y_positions:
                is_active = is_training and random.random() > 0.5
                
                if is_quantum:
                    color = 'rgba(168, 85, 247, 0.8)' if is_active else 'rgba(168, 85, 247, 0.3)'
                    border_color = 'rgba(168, 85, 247, 1)' if is_active else 'rgba(168, 85, 247, 0.5)'
                    size = 12 if is_active else 8
                else:
                    color = 'rgba(59, 130, 246, 0.8)' if is_active else 'rgba(59, 130, 246, 0.3)'
                    border_color = 'rgba(59, 130, 246, 1)' if is_active else 'rgba(59, 130, 246, 0.5)'
                    size = 12 if is_active else 8
                
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    marker=dict(
                        size=size,
                        color=color,
                        line=dict(color=border_color, width=2)
                    ),
                    hoverinfo='skip'
                ))
                
                # Efeito de brilho para nós ativos
                if is_active:
                    fig.add_trace(go.Scatter(
                        x=[x],
                        y=[y],
                        mode='markers',
                        marker=dict(
                            size=size * 2,
                            color=color,
                            opacity=0.3,
                            line=dict(width=0)
                        ),
                        hoverinfo='skip'
                    ))
        
        return fig

# ==================== APLICAÇÃO STREAMLIT ====================
def main():
    st.set_page_config(
        page_title="Quantum Neural Library",
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
        .header-card {
            background-color: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(107, 33, 168, 0.5);
            border-radius: 0.5rem;
            padding: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .metric-card {
            background-color: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
        }
        .info-card {
            background-color: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
        }
        .log-panel {
            background-color: black;
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            font-family: monospace;
            font-size: 0.7rem;
            max-height: 200px;
            overflow-y: auto;
        }
        .tab-button {
            padding: 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.7rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        .tab-active {
            background-color: rgba(107, 33, 168, 0.5);
            color: white;
            border: 1px solid rgba(168, 85, 247, 0.5);
        }
        .tab-inactive {
            background-color: rgba(55, 65, 81, 0.5);
            color: #9ca3af;
            border: 1px solid rgba(55, 65, 81, 0.5);
        }
        .tab-inactive:hover {
            color: white;
            background-color: rgba(55, 65, 81, 0.7);
        }
        .training-button {
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: bold;
            border: 1px solid;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .training-active {
            background-color: rgba(239, 68, 68, 0.1);
            border-color: #ef4444;
            color: #ef4444;
        }
        .training-inactive {
            background-color: rgba(34, 197, 94, 0.1);
            border-color: #10b981;
            color: #10b981;
        }
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .spin-slow {
            animation: spin 3s linear infinite;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar biblioteca quântica
    if 'quantum_library' not in st.session_state:
        st.session_state.quantum_library = QuantumLibrary()
    
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'NEURAL'  # 'NEURAL' or 'CIRCUIT'
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    library = st.session_state.quantum_library
    status = library.status
    metrics = library.real_time_metrics
    logs = library.logMessages
    info = library.get_network_info()
    
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
            <div class="header-card">
                <div style="padding: 0.5rem; background-color: rgba(107, 33, 168, 0.2); 
                         border-radius: 0.5rem; border: 1px solid rgba(168, 85, 247, 0.5);">
                    <span style="color: #a855f7; font-size: 1.5rem;" class="spin-slow">⚛️</span>
                </div>
                <div>
                    <h1 style="color: white; margin: 0; font-size: 1.5rem;">QUANTUM NEURAL LIBRARY</h1>
                    <p style="color: #a855f7; font-family: monospace; font-size: 0.8rem; margin: 0;">
                        CORE V6.1 • {'ARQUITETURA HÍBRIDA' if st.session_state.view_mode == 'NEURAL' else 'SIMULAÇÃO DE CIRCUITOS'}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Tabs de visualização
        tab_col1, tab_col2 = st.columns(2)
        
        with tab_col1:
            if st.button("🧠 NEURAL", key="tab_neural", use_container_width=True,
                        type="primary" if st.session_state.view_mode == 'NEURAL' else "secondary"):
                st.session_state.view_mode = 'NEURAL'
                st.rerun()
        
        with tab_col2:
            if st.button("⚡ CIRCUITS", key="tab_circuit", use_container_width=True,
                        type="primary" if st.session_state.view_mode == 'CIRCUIT' else "secondary"):
                st.session_state.view_mode = 'CIRCUIT'
                st.rerun()
        
        # Status
        st.markdown(f"""
            <div style="text-align: right; margin-top: 0.5rem;">
                <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase;">Status</div>
                <div style="font-size: 0.8rem; font-weight: bold; 
                          color: {'#10b981' if status == NetworkStatus.TRAINING else '#9ca3af'};
                          {'class="pulse"' if status == NetworkStatus.TRAINING else ''};">
                    {status.value}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botões de controle
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button(
                f"⏸️ PARAR" if status == NetworkStatus.TRAINING else "▶️ TREINAR",
                key="toggle_training",
                type="primary" if status == NetworkStatus.TRAINING else "secondary",
                use_container_width=True
            ):
                if status == NetworkStatus.TRAINING:
                    library.stop_training()
                else:
                    library.start_training()
                st.rerun()
        
        with col_btn2:
            if st.button("💾 SALVAR", key="save_model", type="secondary", use_container_width=True):
                library.save_model()
                st.rerun()
    
    st.divider()
    
    # Conteúdo principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Telemetria Híbrida
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="color: #9ca3af; font-size: 1rem;">📊</span>
                <h3 style="color: #9ca3af; font-size: 0.8rem; font-weight: bold; margin: 0;">
                    TELEMETRIA HÍBRIDA
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if metrics:
            latest = metrics[-1].to_dict()
            
            # Métricas rápidas
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Qubits Neurais</div>
                        <div style="font-family: monospace; font-size: 1.2rem; font-weight: bold; color: white;">
                            {latest['qubitsActive']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Temp. Sistema</div>
                        <div style="font-family: monospace; font-size: 1.2rem; font-weight: bold; color: #3b82f6;">
                            {latest['temperature']:.3f}K
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_m2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Fidelidade</div>
                        <div style="font-family: monospace; font-size: 1.2rem; font-weight: bold; color: #10b981;">
                            {latest['quantumFidelity']:.4f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Ops/Sec</div>
                        <div style="font-family: monospace; font-size: 1.2rem; font-weight: bold; color: #a855f7;">
                            {(latest['opsPerSecond'] / 1e6):.1f}M
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de fidelidade
            st.markdown("""
                <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 1rem;">Evolução de Fidelidade</div>
            """, unsafe_allow_html=True)
            
            # Preparar dados para gráfico
            chart_data = []
            for metric in metrics[-50:]:
                chart_data.append({
                    'timestamp': metric.timestamp,
                    'fidelity': metric.quantum_fidelity
                })
            
            df = pd.DataFrame(chart_data)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['fidelity'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(168, 85, 247, 0.3)',
                line=dict(color='#a855f7', width=2),
                name='Fidelidade'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(range=[0.8, 1.0], showgrid=False, showticklabels=False),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Aguardando telemetria...", icon="⏳")
        
        # Estrutura
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem; margin-bottom: 0.5rem;">
                <span style="color: #9ca3af; font-size: 1rem;">🧬</span>
                <h3 style="color: #9ca3af; font-size: 0.8rem; font-weight: bold; margin: 0;">
                    ESTRUTURA
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        info_dict = info.to_dict()
        
        st.markdown(f"""
            <div class="info-card">
                <div style="font-family: monospace; font-size: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; padding: 0.25rem 0; border-bottom: 1px solid rgba(55, 65, 81, 0.5);">
                        <span style="color: #9ca3af;">Neurônios Totais</span>
                        <span style="color: white;">{info_dict['totalNeurons']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.25rem 0; border-bottom: 1px solid rgba(55, 65, 81, 0.5);">
                        <span style="color: #9ca3af;">Camadas Profundas</span>
                        <span style="color: white;">{info_dict['totalLayers']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.25rem 0; border-bottom: 1px solid rgba(55, 65, 81, 0.5);">
                        <span style="color: #9ca3af;">Vantagem Quântica</span>
                        <span style="color: #10b981;">{info_dict['quantumAdvantage']:.2f}x</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 0.25rem 0;">
                        <span style="color: #9ca3af;">Época Atual</span>
                        <span style="color: #3b82f6;">{info_dict['currentEpoch']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Visualização principal
        st.markdown("""
            <div style="position: relative; background-color: rgba(0, 0, 0, 0.4); 
                      border: 1px solid rgba(55, 65, 81, 0.5); border-radius: 0.5rem; 
                      padding: 0.5rem; height: 500px; margin-bottom: 1rem;">
                <div style="position: absolute; top: 1rem; left: 1rem; z-index: 100; 
                          background-color: rgba(0, 0, 0, 0.8); padding: 0.25rem 0.5rem; 
                          border-radius: 0.25rem; border: 1px solid rgba(55, 65, 81, 0.5); 
                          font-size: 0.7rem; color: #9ca3af;">
                    TOPOLOGIA HÍBRIDA EM TEMPO REAL
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.view_mode == 'NEURAL':
            # Visualização neural
            visualizer = NodeVisualizer()
            fig = visualizer.create_visualization(status == NetworkStatus.TRAINING)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            # Placeholder para visualização de circuitos
            st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; height: 450px; color: #6b7280;">
                    <div style="text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                        <div>Visualização de Circuitos Quânticos</div>
                        <div style="font-size: 0.8rem; margin-top: 0.5rem;">(Integração com QuantumCircuitVisualizer)</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Painel de logs
        st.markdown("""
            <div style="margin-top: 1rem;">
                <div style="color: #10b981; font-weight: bold; font-size: 0.8rem; 
                          display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span>🖥️</span> SYSTEM_LOGS
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="log-panel">', unsafe_allow_html=True)
        
        # Mostrar logs em ordem reversa (mais recentes primeiro)
        for log in reversed(logs[-20:]):
            st.markdown(f"""
                <div style="border-bottom: 1px solid rgba(55, 65, 81, 0.5); padding: 0.25rem 0; color: #9ca3af;">
                    {log}
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Atualizar periodicamente
    now = datetime.now()
    if (now - st.session_state.last_update).total_seconds() > 0.5:  # Atualizar a cada 0.5s
        st.session_state.last_update = now
        st.rerun()

if __name__ == "__main__":
    main()