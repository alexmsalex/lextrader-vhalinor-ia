import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random
from typing import List, Dict, Any, Optional
from enum import Enum
import math

# Configuração da página
st.set_page_config(
    page_title="Análise Quântica Avançada",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enums e Classes de Tipos
class SignificanceLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class MarketPhase(str, Enum):
    ACCUMULATION = "ACCUMULATION"
    TRENDING = "TRENDING"
    DISTRIBUTION = "DISTRIBUTION"
    CORRECTION = "CORRECTION"

class AttractorType(str, Enum):
    LORENZ = "LORENZ"
    ROSSLER = "ROSSLER"
    HENON = "HENON"
    CHUA = "CHUA"

class QuantumStateMetric:
    def __init__(self, dimension: str, probability: float, coherence: float, 
                 entanglement: float, prediction: str, confidence: float):
        self.dimension = dimension
        self.probability = probability
        self.coherence = coherence
        self.entanglement = entanglement
        self.prediction = prediction
        self.confidence = confidence

class FractalPattern:
    def __init__(self, pattern: str, level: int, dimension: float, 
                 self_similarity: float, significance: SignificanceLevel, 
                 market_phase: MarketPhase):
        self.pattern = pattern
        self.level = level
        self.dimension = dimension
        self.self_similarity = self_similarity
        self.significance = significance
        self.market_phase = market_phase

class ChaosMetric:
    def __init__(self, name: str, value: float, stability: float, 
                 lyapunov: float, entropy: float, attractor_type: AttractorType):
        self.name = name
        self.value = value
        self.stability = stability
        self.lyapunov = lyapunov
        self.entropy = entropy
        self.attractor_type = attractor_type

# Serviço de Análise Quântica
class QuantumAnalysisService:
    def __init__(self):
        self.dimensions = ["TIME", "PRICE", "VOLUME", "VOLATILITY", "MOMENTUM", "SENTIMENT"]
        self.fractal_patterns = [
            "MANDELBROT",
            "JULIA", 
            "SIERPINSKI",
            "KOCH",
            "CANTOR",
            "DRAGON"
        ]
        self.chaos_names = [
            "BUTTERFLY EFFECT",
            "SENSITIVE DEPENDENCE",
            "STRANGE ATTRACTOR",
            "BIFURCATION",
            "PERIOD DOUBLING",
            "INTERMITTENCY"
        ]
    
    def generate_quantum_states(self) -> List[QuantumStateMetric]:
        """Gera estados quânticos simulados"""
        states = []
        
        for dimension in self.dimensions:
            states.append(QuantumStateMetric(
                dimension=dimension,
                probability=random.uniform(30, 90),
                coherence=random.uniform(40, 95),
                entanglement=random.uniform(20, 85),
                prediction=random.choice(["POSITIVA", "NEGATIVA", "NEUTRA"]),
                confidence=random.uniform(70, 98)
            ))
        
        return states
    
    def generate_fractal_patterns(self) -> List[FractalPattern]:
        """Gera padrões fractais simulados"""
        patterns = []
        
        for i, pattern_name in enumerate(self.fractal_patterns):
            significance = random.choice(list(SignificanceLevel))
            market_phase = random.choice(list(MarketPhase))
            
            patterns.append(FractalPattern(
                pattern=pattern_name,
                level=i + 1,
                dimension=random.uniform(1.5, 2.5),
                self_similarity=random.uniform(0.6, 0.95),
                significance=significance,
                market_phase=market_phase
            ))
        
        return patterns
    
    def generate_chaos_metrics(self) -> List[ChaosMetric]:
        """Gera métricas de teoria do caos"""
        metrics = []
        
        for name in self.chaos_names:
            attractor = random.choice(list(AttractorType))
            
            metrics.append(ChaosMetric(
                name=name,
                value=random.uniform(40, 90),
                stability=random.uniform(30, 85),
                lyapunov=random.uniform(-0.1, 0.3),
                entropy=random.uniform(2.5, 6.5),
                attractor_type=attractor
            ))
        
        return metrics
    
    def calculate_fractal_dimension(self, patterns: List[FractalPattern]) -> float:
        """Calcula a dimensão fractal média"""
        if not patterns:
            return 0
        return sum(p.dimension for p in patterns) / len(patterns)
    
    def calculate_global_coherence(self, states: List[QuantumStateMetric]) -> float:
        """Calcula a coerência global"""
        if not states:
            return 0
        return sum(s.coherence for s in states) / len(states)

# Inicialização
if 'quantum_service' not in st.session_state:
    st.session_state.quantum_service = QuantumAnalysisService()

if 'quantum_states' not in st.session_state:
    st.session_state.quantum_states = []

if 'fractal_patterns' not in st.session_state:
    st.session_state.fractal_patterns = []

if 'chaos_metrics' not in st.session_state:
    st.session_state.chaos_metrics = []

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# CSS Customizado
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #d1d5db;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .quantum-panel {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .matrix-border {
        border-color: #374151;
    }
    
    .pink-glow {
        color: #ec4899;
        text-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
    }
    
    .spinning {
        animation: spin 4s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .significance-critical {
        color: #ef4444;
        background-color: rgba(239, 68, 68, 0.2);
        border: 1px solid #ef4444;
    }
    
    .significance-high {
        color: #f59e0b;
        background-color: rgba(245, 158, 11, 0.2);
        border: 1px solid #f59e0b;
    }
    
    .significance-medium {
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.2);
        border: 1px solid #3b82f6;
    }
    
    .significance-low {
        color: #9ca3af;
        background-color: rgba(156, 163, 175, 0.2);
        border: 1px solid #9ca3af;
    }
    
    .progress-bar {
        width: 100%;
        height: 0.25rem;
        background-color: #1f2937;
        border-radius: 0.125rem;
        overflow: hidden;
        margin-top: 0.25rem;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 0.125rem;
    }
    
    .card-hover {
        transition: all 0.3s;
    }
    
    .card-hover:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Função para atualizar dados
def update_data():
    st.session_state.quantum_states = st.session_state.quantum_service.generate_quantum_states()
    st.session_state.fractal_patterns = st.session_state.quantum_service.generate_fractal_patterns()
    st.session_state.chaos_metrics = st.session_state.quantum_service.generate_chaos_metrics()
    st.session_state.last_update = datetime.now()

# Atualizar dados inicialmente
if not st.session_state.quantum_states:
    update_data()

# Configuração da barra lateral
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    auto_refresh = st.checkbox("Atualização Automática", value=True)
    refresh_interval = st.slider("Intervalo (segundos)", 1, 10, 4)
    
    if st.button("🔄 Atualizar Agora"):
        update_data()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Estatísticas")
    coherence = st.session_state.quantum_service.calculate_global_coherence(st.session_state.quantum_states)
    dimensionality = st.session_state.quantum_service.calculate_fractal_dimension(st.session_state.fractal_patterns)
    
    st.metric("Coerência Global", f"{coherence:.1f}%")
    st.metric("Dimensão Fractal", f"{dimensionality:.3f}D")
    
    st.markdown(f"*Última atualização:* {st.session_state.last_update.strftime('%H:%M:%S')}")

# Header
col_header1, col_header2 = st.columns([3, 2])

with col_header1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="padding: 0.5rem; background-color: rgba(236, 72, 153, 0.2); border: 1px solid rgba(236, 72, 153, 0.5); border-radius: 0.5rem;">
            <span class="pink-glow spinning" style="font-size: 1.5rem;">⚛️</span>
        </div>
        <div>
            <h1 style="color: white; font-weight: bold; letter-spacing: 0.1em; margin: 0;">ANÁLISE QUÂNTICA AVANÇADA</h1>
            <div style="color: #ec4899; font-size: 0.75rem; font-family: monospace; margin-top: 0.25rem;">
                CHAOS THEORY • FRACTAL GEOMETRY
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    st.markdown("""
    <div style="display: flex; justify-content: flex-end; gap: 2rem; font-family: monospace;">
        <div style="text-align: right;">
            <div style="color: #9ca3af; font-size: 0.75rem; margin-bottom: 0.25rem;">COERÊNCIA GLOBAL</div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 6rem; height: 0.5rem; background-color: #1f2937; border-radius: 0.25rem; overflow: hidden;">
                    <div style="height: 100%; background-color: #ec4899; width: """ + f"{coherence}%" + """;"></div>
                </div>
                <span style="color: white; font-weight: bold; font-size: 1.125rem;">""" + f"{coherence:.1f}%" + """</span>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="color: #9ca3af; font-size: 0.75rem; margin-bottom: 0.25rem;">DIMENSÃO FRACTAL</div>
            <span style="color: #3b82f6; font-weight: bold; font-size: 1.125rem;">""" + f"{dimensionality:.3f}D" + """</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Layout principal com 3 colunas
col1, col2, col3 = st.columns(3)

with col1:
    # Coluna 1: Estados Quânticos
    st.markdown("#### 📊 Estados Quânticos")
    
    # Gráfico Radar
    if st.session_state.quantum_states:
        radar_data = []
        for state in st.session_state.quantum_states:
            radar_data.append({
                'dimension': state.dimension,
                'coherence': state.coherence
            })
        
        radar_df = pd.DataFrame(radar_data)
        
        fig = go.Figure(data=go.Scatterpolar(
            r=radar_df['coherence'],
            theta=radar_df['dimension'],
            fill='toself',
            line=dict(color='#f472b6', width=2),
            fillcolor='rgba(244, 114, 182, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='#333',
                    linecolor='#333'
                ),
                angularaxis=dict(
                    gridcolor='#333',
                    linecolor='#333',
                    tickfont=dict(color='#666', size=9)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=False,
            height=250,
            margin=dict(l=50, r=50, t=30, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Cards dos Estados Quânticos
    for i, state in enumerate(st.session_state.quantum_states):
        with st.container():
            st.markdown(f"""
            <div class="quantum-panel card-hover" style="margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-weight: bold; color: white; font-size: 0.875rem;">{state.dimension}</span>
                    <span style="color: #ec4899; font-size: 0.625rem; border: 1px solid rgba(236, 72, 153, 0.5); padding: 0.125rem 0.5rem; border-radius: 0.25rem;">
                        {state.confidence:.0f}% CONF
                    </span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div>
                        <div style="color: #9ca3af; font-size: 0.625rem; margin-bottom: 0.125rem;">PROB</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="background-color: #3b82f6; width: {state.probability}%;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="color: #9ca3af; font-size: 0.625rem; margin-bottom: 0.125rem;">ENTANG</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="background-color: #8b5cf6; width: {state.entanglement}%;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="color: #9ca3af; font-size: 0.625rem; margin-bottom: 0.125rem;">COHER</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="background-color: #ec4899; width: {state.coherence}%;"></div>
                        </div>
                    </div>
                </div>
                
                <div style="background-color: rgba(31, 41, 55, 0.5); padding: 0.5rem; border-radius: 0.25rem; display: flex; justify-content: space-between;">
                    <span style="color: #9ca3af; font-size: 0.625rem;">Previsão:</span>
                    <span style="color: {'#10b981' if 'POSITIVA' in state.prediction else '#ef4444' if 'NEGATIVA' in state.prediction else '#f59e0b'}; 
                          font-size: 0.625rem; font-weight: bold;">
                        {state.prediction}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    # Coluna 2: Padrões Fractais
    st.markdown("#### ❄️ Padrões Fractais")
    
    for fractal in st.session_state.fractal_patterns:
        significance_class = {
            SignificanceLevel.CRITICAL: "significance-critical",
            SignificanceLevel.HIGH: "significance-high",
            SignificanceLevel.MEDIUM: "significance-medium",
            SignificanceLevel.LOW: "significance-low"
        }.get(fractal.significance, "significance-low")
        
        with st.container():
            st.markdown(f"""
            <div class="quantum-panel card-hover" style="margin-bottom: 0.75rem; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0.5rem; right: 0.5rem; opacity: 0.1; font-size: 1.5rem;">❄️</div>
                
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 1.5rem; height: 1.5rem; border-radius: 50%; background-color: #1f2937; 
                              display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">
                            {fractal.level}
                        </div>
                        <span style="font-weight: bold; color: white; font-size: 0.875rem;">{fractal.pattern}</span>
                    </div>
                    <span class="{significance_class}" style="font-size: 0.625rem; padding: 0.125rem 0.5rem; border-radius: 0.25rem;">
                        {fractal.significance.value}
                    </span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.5rem;">
                    <div>
                        <span style="color: #9ca3af; font-size: 0.625rem; display: block;">Auto-Similaridade</span>
                        <span style="color: #3b82f6; font-family: monospace; font-size: 0.875rem;">{fractal.self_similarity:.3f}</span>
                        <div class="progress-bar">
                            <div class="progress-fill" style="background-color: #3b82f6; width: {fractal.self_similarity * 100}%;"></div>
                        </div>
                    </div>
                    <div>
                        <span style="color: #9ca3af; font-size: 0.625rem; display: block;">Dimensão</span>
                        <span style="color: #8b5cf6; font-family: monospace; font-size: 0.875rem;">{fractal.dimension:.3f}D</span>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; 
                      border-top: 1px solid #374151; padding-top: 0.5rem; margin-top: 0.5rem;">
                    <span style="color: #9ca3af; font-size: 0.625rem;">Fase de Mercado</span>
                    <span style="color: white; font-weight: bold; font-size: 0.75rem;">{fractal.market_phase.value}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col3:
    # Coluna 3: Teoria do Caos
    st.markdown("#### 🔥 Teoria do Caos")
    
    for chaos in st.session_state.chaos_metrics:
        # Determinar cor baseada no expoente de Lyapunov
        if chaos.lyapunov > 0.15:
            lyapunov_color = "#ef4444"  # vermelho
        elif chaos.lyapunov > 0:
            lyapunov_color = "#f59e0b"  # amarelo
        else:
            lyapunov_color = "#10b981"  # verde
        
        with st.container():
            st.markdown(f"""
            <div class="quantum-panel card-hover" style="margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="font-weight: bold; color: #d1d5db; font-size: 0.875rem;">{chaos.name}</span>
                    <span style="color: #9ca3af; font-size: 0.625rem; background-color: #1f2937; 
                          padding: 0.125rem 0.5rem; border-radius: 0.25rem; border: 1px solid #374151;">
                        {chaos.attractor_type.value}
                    </span>
                </div>
                
                <div style="margin-bottom: 0.75rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <div style="color: #9ca3af; font-size: 0.625rem; width: 4rem;">Valor</div>
                        <div style="flex: 1; background-color: #1f2937; height: 0.5rem; border-radius: 0.25rem; overflow: hidden;">
                            <div style="height: 100%; background-color: #f97316; width: {chaos.value}%;"></div>
                        </div>
                        <div style="color: #f97316; font-size: 0.75rem; width: 2rem; text-align: right;">{chaos.value:.0f}</div>
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="color: #9ca3af; font-size: 0.625rem; width: 4rem;">Estabilidade</div>
                        <div style="flex: 1; background-color: #1f2937; height: 0.5rem; border-radius: 0.25rem; overflow: hidden;">
                            <div style="height: 100%; background-color: #10b981; width: {chaos.stability}%;"></div>
                        </div>
                        <div style="color: #10b981; font-size: 0.75rem; width: 2rem; text-align: right;">{chaos.stability:.0f}</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 0.75rem; 
                      border-top: 1px solid #374151; padding-top: 0.75rem;">
                    <div style="background-color: rgba(31, 41, 55, 0.5); padding: 0.5rem; border-radius: 0.25rem; text-align: center;">
                        <div style="color: #9ca3af; font-size: 0.5rem; text-transform: uppercase; margin-bottom: 0.25rem;">Lyapunov Exp</div>
                        <div style="color: {lyapunov_color}; font-family: monospace; font-weight: bold; font-size: 0.875rem;">
                            {chaos.lyapunov:.3f}
                        </div>
                    </div>
                    <div style="background-color: rgba(31, 41, 55, 0.5); padding: 0.5rem; border-radius: 0.25rem; text-align: center;">
                        <div style="color: #9ca3af; font-size: 0.5rem; text-transform: uppercase; margin-bottom: 0.25rem;">Entropia</div>
                        <div style="color: #3b82f6; font-family: monospace; font-weight: bold; font-size: 0.875rem;">
                            {chaos.entropy:.2f} bits
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; color: #9ca3af; font-size: 0.75rem;">
    <div>⚛️ Sistema de Análise Quântica • CHAOS THEORY IMPLEMENTATION</div>
    <div>Atualização: """ + f"{st.session_state.last_update.strftime('%H:%M:%S')}" + """</div>
</div>
""", unsafe_allow_html=True)

# Atualização automática
if auto_refresh:
    time.sleep(refresh_interval)
    update_data()
    st.rerun()