import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
import json

# Configuração da página
st.set_page_config(
    page_title="Otimizador de Precisão Neural",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enums e Classes de Tipos
class ModelType(str, Enum):
    LSTM = "LSTM"
    GRU = "GRU"
    CNN = "CNN"
    TRANSFORMER = "TRANSFORMER"
    HYBRID = "HYBRID"
    QUANTUM = "QUANTUM"
    NEUROMORPHIC = "NEUROMORPHIC"

class ParamStatus(str, Enum):
    OPTIMIZING = "OPTIMIZING"
    STABLE = "STABLE"
    TESTING = "TESTING"

class ActiveTab(str, Enum):
    ENSEMBLE = "ENSEMBLE"
    PARAMS = "PARAMS"
    METRICS = "METRICS"
    TECHNIQUES = "TECHNIQUES"

@dataclass
class EnsembleModel:
    """Representa um modelo no ensemble"""
    id: str
    name: str
    model_type: ModelType
    accuracy: float
    weight: float
    confidence: float
    predictions: int
    is_active: bool
    learning_rate: float
    layers: int
    parameters: int

@dataclass
class HyperparameterConfig:
    """Configuração de hiperparâmetro"""
    parameter: str
    current_value: float
    optimal_value: float
    impact: float
    status: ParamStatus

@dataclass
class PrecisionMetric:
    """Métrica de precisão temporal"""
    timestamp: datetime
    time_label: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    mse: float
    mae: float
    technique: str

# Serviço de Núcleo Sentiente Simulado
class SentientCore:
    def __init__(self):
        self.thoughts = []
        self.state = "NEUTRAL"
        self.focus = 85.0
        self.confidence = 92.0
        self.vector = {"focus": 85.0, "confidence": 92.0}
    
    def get_vector(self) -> Dict[str, float]:
        """Retorna o vetor de estado atual"""
        return self.vector.copy()
    
    def get_state(self) -> str:
        """Retorna o estado atual"""
        return self.state
    
    def add_thought(self, thought: str):
        """Adiciona um pensamento ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.thoughts.append(f"[{timestamp}] {thought}")
        
        # Manter apenas os últimos 20 pensamentos
        if len(self.thoughts) > 20:
            self.thoughts.pop(0)
        
        # Atualizar estado baseado no pensamento
        if any(word in thought.lower() for word in ["otimizando", "melhorando", "avançando"]):
            self.state = "OPTIMIZING"
            self.confidence = min(100, self.confidence + 0.5)
        elif any(word in thought.lower() for word in ["pausa", "consolidando", "estável"]):
            self.state = "STABLE"
            self.focus = max(70, self.focus - 5)
    
    def perceive_reality(self, value: float, level: int):
        """Simula percepção da realidade"""
        # Atualizar métricas baseado na percepção
        self.confidence = min(100, max(0, self.confidence + value * 10))
        self.focus = min(100, max(0, self.focus + value * 5))
        self.vector = {"focus": self.focus, "confidence": self.confidence}
        
        # Log da percepção
        if value > 0:
            self.add_thought(f"Percepção positiva: Reforço recebido (nível {level})")
        else:
            self.add_thought(f"Percepção negativa: Ajuste necessário (nível {level})")

# Inicialização de dados
def init_ensemble_models() -> List[EnsembleModel]:
    """Inicializa os modelos do ensemble"""
    return [
        EnsembleModel(
            id='lstm_primary',
            name='LSTM Primário',
            model_type=ModelType.LSTM,
            accuracy=87.4,
            weight=0.12,
            confidence=0.92,
            predictions=15420,
            is_active=True,
            learning_rate=0.0001,
            layers=4,
            parameters=2400000
        ),
        EnsembleModel(
            id='lstm_secondary',
            name='LSTM Secundário',
            model_type=ModelType.LSTM,
            accuracy=89.2,
            weight=0.13,
            confidence=0.94,
            predictions=14200,
            is_active=True,
            learning_rate=0.00008,
            layers=6,
            parameters=3200000
        ),
        EnsembleModel(
            id='gru_momentum',
            name='GRU Momentum',
            model_type=ModelType.GRU,
            accuracy=84.7,
            weight=0.10,
            confidence=0.89,
            predictions=12350,
            is_active=True,
            learning_rate=0.00015,
            layers=3,
            parameters=1800000
        ),
        EnsembleModel(
            id='cnn_pattern',
            name='CNN Padrões',
            model_type=ModelType.CNN,
            accuracy=91.2,
            weight=0.12,
            confidence=0.95,
            predictions=8940,
            is_active=True,
            learning_rate=0.0002,
            layers=8,
            parameters=4500000
        ),
        EnsembleModel(
            id='transformer_trend',
            name='Transformer Trends',
            model_type=ModelType.TRANSFORMER,
            accuracy=93.8,
            weight=0.12,
            confidence=0.97,
            predictions=6780,
            is_active=True,
            learning_rate=0.00008,
            layers=16,
            parameters=8500000
        ),
        EnsembleModel(
            id='hybrid_advanced',
            name='Híbrido Avançado',
            model_type=ModelType.HYBRID,
            accuracy=95.2,
            weight=0.08,
            confidence=0.99,
            predictions=10500,
            is_active=True,
            learning_rate=0.00005,
            layers=18,
            parameters=9800000
        ),
        EnsembleModel(
            id='quantum_ent',
            name='Entrelaçamento Q',
            model_type=ModelType.QUANTUM,
            accuracy=96.5,
            weight=0.15,
            confidence=0.88,
            predictions=4200,
            is_active=True,
            learning_rate=0.01,
            layers=32,
            parameters=1024
        ),
        EnsembleModel(
            id='neuromorphic_spike',
            name='Spiking Neural Net',
            model_type=ModelType.NEUROMORPHIC,
            accuracy=92.1,
            weight=0.10,
            confidence=0.91,
            predictions=5600,
            is_active=False,
            learning_rate=0.001,
            layers=128,
            parameters=5000000
        )
    ]

def init_hyperparameters() -> List[HyperparameterConfig]:
    """Inicializa os hiperparâmetros"""
    return [
        HyperparameterConfig(
            parameter='Learning Rate',
            current_value=0.0001,
            optimal_value=0.00012,
            impact=87,
            status=ParamStatus.OPTIMIZING
        ),
        HyperparameterConfig(
            parameter='Batch Size',
            current_value=64,
            optimal_value=128,
            impact=63,
            status=ParamStatus.OPTIMIZING
        ),
        HyperparameterConfig(
            parameter='Dropout Rate',
            current_value=0.15,
            optimal_value=0.12,
            impact=44,
            status=ParamStatus.STABLE
        ),
        HyperparameterConfig(
            parameter='Hidden Units',
            current_value=256,
            optimal_value=512,
            impact=78,
            status=ParamStatus.OPTIMIZING
        ),
        HyperparameterConfig(
            parameter='Attention Heads',
            current_value=8,
            optimal_value=16,
            impact=94,
            status=ParamStatus.OPTIMIZING
        ),
        HyperparameterConfig(
            parameter='Quantum Depth',
            current_value=10,
            optimal_value=15,
            impact=89,
            status=ParamStatus.TESTING
        )
    ]

# Técnicas de otimização
TECHNIQUES = [
    "Ensemble Learning: Combinação ponderada de múltiplos modelos",
    "Transfer Learning: Adaptação de pré-treino financeiro",
    "Data Augmentation: Geração sintética via GANs",
    "Bayesian Optimization: Ajuste fino de hiperparâmetros",
    "Quantum Annealing: Busca de mínimo global de erro",
    "Neuro-Evolution: Mutação de topologia de rede"
]

# Inicialização do estado
if 'sentient_core' not in st.session_state:
    st.session_state.sentient_core = SentientCore()

if 'ensemble_models' not in st.session_state:
    st.session_state.ensemble_models = init_ensemble_models()

if 'hyperparams' not in st.session_state:
    st.session_state.hyperparams = init_hyperparameters()

if 'metrics' not in st.session_state:
    # Gerar métricas iniciais
    initial_metrics = []
    for i in range(20):
        timestamp = datetime.now() - timedelta(seconds=(20 - i))
        initial_metrics.append(PrecisionMetric(
            timestamp=timestamp,
            time_label=timestamp.strftime("%H:%M:%S"),
            accuracy=85 + random.random() * 5,
            precision=84 + random.random() * 6,
            recall=86 + random.random() * 4,
            f1_score=85 + random.random() * 5,
            mse=0.02 + random.random() * 0.01,
            mae=0.015 + random.random() * 0.005,
            technique='Init'
        ))
    st.session_state.metrics = initial_metrics

if 'overall_accuracy' not in st.session_state:
    st.session_state.overall_accuracy = 88.4

if 'ensemble_accuracy' not in st.session_state:
    st.session_state.ensemble_accuracy = 90.0

if 'is_optimizing' not in st.session_state:
    st.session_state.is_optimizing = True

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = ActiveTab.ENSEMBLE

if 'agi_mood' not in st.session_state:
    st.session_state.agi_mood = "NEUTRAL"

if 'iteration_count' not in st.session_state:
    st.session_state.iteration_count = 4829

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
    
    .neural-header {
        padding: 1rem;
        border-bottom: 1px solid #374151;
        background-color: #111827;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .header-icon {
        padding: 0.5rem;
        background-color: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.5);
        border-radius: 0.25rem;
    }
    
    .pulse-icon {
        color: #6366f1;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .agi-mood {
        background-color: rgba(0, 0, 0, 0.4);
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #374151;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .ensemble-score {
        background-color: rgba(168, 85, 247, 0.2);
        border: 1px solid rgba(168, 85, 247, 0.5);
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .optimize-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: 1px solid;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .optimize-active {
        background-color: rgba(245, 158, 11, 0.3);
        border-color: #f59e0b;
        color: #f59e0b;
    }
    
    .optimize-active:hover {
        background-color: rgba(245, 158, 11, 0.5);
    }
    
    .optimize-inactive {
        background-color: rgba(16, 185, 129, 0.3);
        border-color: #10b981;
        color: #10b981;
    }
    
    .optimize-inactive:hover {
        background-color: rgba(16, 185, 129, 0.5);
    }
    
    .tab-navigation {
        display: flex;
        border-bottom: 1px solid #374151;
        background-color: rgba(0, 0, 0, 0.2);
    }
    
    .tab-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
        border-right: 1px solid #374151;
    }
    
    .tab-button:hover {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
    }
    
    .tab-button.active {
        background-color: rgba(99, 102, 241, 0.2);
        color: #6366f1;
        border-bottom: 2px solid #6366f1;
    }
    
    .model-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        transition: all 0.3s;
    }
    
    .model-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-2px);
    }
    
    .model-card.inactive {
        opacity: 0.6;
    }
    
    .model-type-badge {
        font-size: 0.625rem;
        background-color: #1f2937;
        padding: 0.125rem 0.5rem;
        border-radius: 0.125rem;
        border: 1px solid #374151;
        color: #9ca3af;
    }
    
    .param-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .status-badge {
        font-size: 0.5625rem;
        padding: 0.125rem 0.5rem;
        border-radius: 0.125rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .status-optimizing {
        background-color: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.5);
    }
    
    .status-stable {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
    
    .status-testing {
        background-color: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.5);
    }
    
    .tech-card {
        background-color: rgba(0, 0, 0, 0.3);
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        display: flex;
        align-items: start;
        gap: 0.75rem;
    }
    
    .metric-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.875rem;
        font-family: monospace;
        font-weight: bold;
        margin-top: 0.25rem;
    }
    
    .metric-label {
        color: #9ca3af;
        font-size: 0.625rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .bayesian-panel {
        background-color: rgba(0, 0, 0, 0.4);
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    .progress-bar {
        width: 100%;
        height: 0.25rem;
        background-color: #1f2937;
        border-radius: 0.125rem;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .progress-fill {
        height: 100%;
        background-color: #f59e0b;
        border-radius: 0.125rem;
        animation: pulse 1s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
def get_model_color(model_type: ModelType) -> str:
    """Retorna a cor para o tipo de modelo"""
    color_map = {
        ModelType.LSTM: "#10b981",
        ModelType.GRU: "#f59e0b",
        ModelType.CNN: "#3b82f6",
        ModelType.TRANSFORMER: "#6366f1",
        ModelType.HYBRID: "#ef4444",
        ModelType.QUANTUM: "#a855f7",
        ModelType.NEUROMORPHIC: "#ec4899"
    }
    return color_map.get(model_type, "#6b7280")

def toggle_optimization():
    """Alterna o estado de otimização"""
    new_state = not st.session_state.is_optimizing
    st.session_state.is_optimizing = new_state
    
    if new_state:
        st.session_state.sentient_core.add_thought(
            "Retomando otimização neural. Focando em minimizar a função de perda global."
        )
    else:
        st.session_state.sentient_core.add_thought(
            "Otimização pausada. Consolidando pesos sinápticos atuais."
        )

def simulate_optimization():
    """Simula um ciclo de otimização"""
    if not st.session_state.is_optimizing:
        return
    
    # Obter estado do AGI para influenciar a simulação
    sentient = st.session_state.sentient_core.get_vector()
    st.session_state.agi_mood = st.session_state.sentient_core.get_state()
    
    # Fator de influência do AGI
    agi_factor = (sentient["focus"] + sentient["confidence"]) / 200  # 0.0 - 1.0
    random_noise = (random.random() - 0.3) * 0.5
    improvement = (random_noise + (agi_factor * 0.1)) * 0.5
    
    # 1. Atualizar modelos
    updated_models = []
    for model in st.session_state.ensemble_models:
        if not model.is_active:
            updated_models.append(model)
            continue
        
        new_accuracy = min(99.9, max(70, model.accuracy + improvement))
        updated_models.append(EnsembleModel(
            id=model.id,
            name=model.name,
            model_type=model.model_type,
            accuracy=new_accuracy,
            weight=model.weight,
            confidence=model.confidence,
            predictions=model.predictions + random.randint(0, 10),
            is_active=model.is_active,
            learning_rate=model.learning_rate,
            layers=model.layers,
            parameters=model.parameters
        ))
    st.session_state.ensemble_models = updated_models
    
    # 2. Atualizar hiperparâmetros
    updated_params = []
    for param in st.session_state.hyperparams:
        new_impact = min(100, max(0, param.impact + (random.random() - 0.5) * 2))
        updated_params.append(HyperparameterConfig(
            parameter=param.parameter,
            current_value=param.current_value,
            optimal_value=param.optimal_value,
            impact=new_impact,
            status=param.status
        ))
    st.session_state.hyperparams = updated_params
    
    # 3. Atualizar métricas gerais
    new_overall_accuracy = min(99.9, st.session_state.overall_accuracy + (improvement * 0.2))
    
    # Feedback do AGI: se a precisão melhorar significativamente
    if new_overall_accuracy > st.session_state.overall_accuracy + 0.1:
        st.session_state.sentient_core.perceive_reality(0.5, 1)
    
    st.session_state.overall_accuracy = new_overall_accuracy
    st.session_state.ensemble_accuracy = min(99.9, st.session_state.ensemble_accuracy + (improvement * 0.3))
    
    # 4. Adicionar novo ponto de métrica
    last_metric = st.session_state.metrics[-1]
    new_metric = PrecisionMetric(
        timestamp=datetime.now(),
        time_label=datetime.now().strftime("%H:%M:%S"),
        accuracy=min(99.9, last_metric.accuracy + improvement),
        precision=min(99.9, last_metric.precision + (improvement * 0.8)),
        recall=min(99.9, last_metric.recall + (improvement * 0.9)),
        f1_score=min(99.9, last_metric.f1_score + (improvement * 0.85)),
        mse=max(0.001, last_metric.mse - (improvement * 0.001)),
        mae=max(0.001, last_metric.mae - (improvement * 0.001)),
        technique='Hybrid Opt'
    )
    
    # Atualizar lista de métricas
    st.session_state.metrics = st.session_state.metrics[1:] + [new_metric]
    
    # Incrementar contador de iterações
    st.session_state.iteration_count += 1
    st.session_state.last_update = datetime.now()

# Barra lateral com controles
with st.sidebar:
    st.markdown("### ⚙️ Controles de Otimização")
    
    # Botão de otimização
    button_text = "⏸️ Pausar Otimização" if st.session_state.is_optimizing else "▶️ Iniciar Otimização"
    button_class = "optimize-active" if st.session_state.is_optimizing else "optimize-inactive"
    
    if st.button(button_text, use_container_width=True):
        toggle_optimization()
        st.rerun()
    
    st.markdown("---")
    
    # Configurações de simulação
    st.markdown("### 🔧 Configurações")
    
    simulation_speed = st.slider(
        "Velocidade de Simulação",
        min_value=1,
        max_value=10,
        value=2,
        help="Segundos entre atualizações"
    )
    
    noise_level = st.slider(
        "Nível de Ruído",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Variabilidade nas simulações"
    )
    
    st.markdown("---")
    
    # Estatísticas do AGI
    st.markdown("### 🧠 Estado do AGI")
    
    sentient_vector = st.session_state.sentient_core.get_vector()
    
    col_agi1, col_agi2 = st.columns(2)
    
    with col_agi1:
        st.metric("Foco", f"{sentient_vector['focus']:.1f}%")
    
    with col_agi2:
        st.metric("Confiança", f"{sentient_vector['confidence']:.1f}%")
    
    st.markdown(f"**Estado:** {st.session_state.agi_mood}")
    
    st.markdown("---")
    
    # Logs do AGI
    st.markdown("### 💭 Pensamentos do AGI")
    
    thoughts_container = st.container(height=200)
    with thoughts_container:
        for thought in reversed(st.session_state.sentient_core.thoughts[-5:]):
            st.markdown(f"""
            <div style="background-color: rgba(0, 0, 0, 0.3); padding: 0.5rem; border-radius: 0.25rem; margin-bottom: 0.25rem; 
                 border-left: 3px solid #6366f1;">
                <div style="color: #9ca3af; font-size: 0.75rem;">{thought}</div>
            </div>
            """, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="neural-header">
    <div class="header-left">
        <div class="header-icon">
            <span class="pulse-icon" style="font-size: 1.25rem;">🎯</span>
        </div>
        <div>
            <h1 style="color: white; font-weight: bold; letter-spacing: 0.1em; margin: 0;">OTIMIZADOR DE PRECISÃO NEURAL</h1>
            <div style="color: #6366f1; font-size: 0.625rem; font-family: monospace; margin-top: 0.25rem;">
                ENSEMBLE TUNING • HYPERPARAMETER SEARCH
            </div>
        </div>
    </div>
    
    <div class="header-right">
        <div class="agi-mood">
            <span style="color: #3b82f6; font-size: 1rem;">⚡</span>
            <span style="font-size: 0.75rem; font-family: monospace; color: #9ca3af;">AGI MOOD:</span>
            <span style="font-weight: bold; color: white;">{agi_mood}</span>
        </div>
        
        <div class="ensemble-score">
            <span style="color: #a855f7; font-size: 1rem;">🧩</span>
            <span style="font-weight: bold; color: white;">ENSEMBLE: {ensemble_accuracy:.2f}%</span>
        </div>
    </div>
</div>
""".format(
    agi_mood=st.session_state.agi_mood,
    ensemble_accuracy=st.session_state.ensemble_accuracy
), unsafe_allow_html=True)

# Navegação por tabs
st.markdown("""
<div class="tab-navigation">
    <div class="tab-button {'active' if active_tab == 'ENSEMBLE' else ''}" onclick="window.location.href='?tab=ENSEMBLE'">
        <span>🧩</span>
        <span>Ensemble Models</span>
    </div>
    <div class="tab-button {'active' if active_tab == 'PARAMS' else ''}" onclick="window.location.href='?tab=PARAMS'">
        <span>⚙️</span>
        <span>Hiperparâmetros</span>
    </div>
    <div class="tab-button {'active' if active_tab == 'METRICS' else ''}" onclick="window.location.href='?tab=METRICS'">
        <span>📊</span>
        <span>Métricas</span>
    </div>
    <div class="tab-button {'active' if active_tab == 'TECHNIQUES' else ''}" onclick="window.location.href='?tab=TECHNIQUES'">
        <span>🔬</span>
        <span>Técnicas</span>
    </div>
</div>
""".format(active_tab=st.session_state.active_tab.value), unsafe_allow_html=True)

# Conteúdo baseado na aba ativa
if st.session_state.active_tab == ActiveTab.ENSEMBLE:
    st.markdown("#### 🧩 Ensemble de Modelos")
    
    # Criar grade de modelos
    col_models = st.columns(3)
    
    for i, model in enumerate(st.session_state.ensemble_models):
        col_idx = i % 3
        with col_models[col_idx]:
            model_class = "model-card" if model.is_active else "model-card inactive"
            model_color = get_model_color(model.model_type)
            
            st.markdown(f"""
            <div class="{model_class}">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 0.5rem; height: 0.5rem; border-radius: 50%; background-color: {model_color};"></div>
                        <span style="font-weight: bold; color: white; font-size: 0.875rem;">{model.name}</span>
                    </div>
                    <span class="model-type-badge">{model.model_type.value}</span>
                </div>
                
                <div style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 0.25rem;">
                        <span style="color: #9ca3af;">Precisão</span>
                        <span style="color: white; font-family: monospace;">{model.accuracy:.2f}%</span>
                    </div>
                    <div style="width: 100%; background-color: #1f2937; height: 0.375rem; border-radius: 0.1875rem; overflow: hidden;">
                        <div style="height: 100%; background-color: {model_color}; width: {model.accuracy}%; 
                             transition: width 1s;"></div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.625rem; color: #9ca3af; font-family: monospace;">
                    <div style="background-color: rgba(0, 0, 0, 0.3); padding: 0.375rem; border-radius: 0.25rem;">
                        <div>PESO</div>
                        <div style="color: white;">{model.weight:.2f}</div>
                    </div>
                    <div style="background-color: rgba(0, 0, 0, 0.3); padding: 0.375rem; border-radius: 0.25rem;">
                        <div>CONFIANÇA</div>
                        <div style="color: white;">{(model.confidence * 100):.0f}%</div>
                    </div>
                    <div style="background-color: rgba(0, 0, 0, 0.3); padding: 0.375rem; border-radius: 0.25rem;">
                        <div>PREDIÇÕES</div>
                        <div style="color: white;">{model.predictions:,}</div>
                    </div>
                    <div style="background-color: rgba(0, 0, 0, 0.3); padding: 0.375rem; border-radius: 0.25rem;">
                        <div>PARAMS</div>
                        <div style="color: white;">{(model.parameters / 1e6):.1f}M</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.active_tab == ActiveTab.PARAMS:
    col_params1, col_params2 = st.columns([2, 1])
    
    with col_params1:
        st.markdown("#### ⚙️ Hiperparâmetros")
        
        for param in st.session_state.hyperparams:
            # Determinar classe de status
            status_class = {
                ParamStatus.OPTIMIZING: "status-optimizing",
                ParamStatus.STABLE: "status-stable",
                ParamStatus.TESTING: "status-testing"
            }.get(param.status, "status-optimizing")
            
            st.markdown(f"""
            <div class="param-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-weight: bold; color: white; font-size: 0.875rem;">{param.parameter}</span>
                    <span class="status-badge {status_class}">{param.status.value}</span>
                </div>
                
                <div style="display: flex; align-items: center; gap: 1rem; font-size: 0.75rem; font-family: monospace; 
                     color: #9ca3af; margin-bottom: 0.5rem;">
                    <span style="background-color: rgba(0, 0, 0, 0.4); padding: 0.25rem 0.5rem; border-radius: 0.25rem;">
                        Atual: <span style="color: white;">{param.current_value}</span>
                    </span>
                    <span style="color: #6366f1;">→</span>
                    <span style="background-color: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); 
                         padding: 0.25rem 0.5rem; border-radius: 0.25rem; color: #6366f1;">
                        Alvo: {param.optimal_value}
                    </span>
                </div>
                
                <div style="position: relative;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.5625rem; color: #6b7280; 
                         margin-bottom: 0.25rem;">
                        <span>Impacto no Modelo</span>
                        <span>{param.impact:.0f}%</span>
                    </div>
                    <div style="width: 100%; background-color: #1f2937; height: 0.5rem; border-radius: 0.25rem; overflow: hidden;">
                        <div style="height: 100%; background: linear-gradient(to right, #374151, #6366f1); 
                             width: {param.impact}%; transition: width 0.5s;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_params2:
        st.markdown("#### ⚡ Otimização Bayesiana")
        
        st.markdown("""
        <div class="bayesian-panel">
            <div style="color: #f59e0b; font-size: 3rem; animation: pulse 1s infinite;">⚡</div>
            <h3 style="color: white; font-size: 1.25rem; margin: 0.5rem 0;">Otimização Bayesiana Ativa</h3>
            <p style="color: #9ca3af; font-size: 0.875rem; max-width: 300px; line-height: 1.4; margin-bottom: 1rem;">
                O núcleo AGI está explorando o espaço de hiperparâmetros usando inferência probabilística para minimizar a função de perda global.
            </p>
            
            <div style="width: 100%; max-width: 300px; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #9ca3af; margin-bottom: 0.25rem;">
                    <span>Iteração Atual</span>
                    <span>#{iteration_count}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 67%;"></div>
                </div>
            </div>
        </div>
        """.format(iteration_count=st.session_state.iteration_count), unsafe_allow_html=True)

elif st.session_state.active_tab == ActiveTab.METRICS:
    st.markdown("#### 📊 Métricas de Performance")
    
    # Métricas principais
    col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
    
    with col_metrics1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Precisão Geral</div>
            <div class="metric-value" style="color: #6366f1;">{st.session_state.overall_accuracy:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metrics2:
        last_metric = st.session_state.metrics[-1]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">F1-Score</div>
            <div class="metric-value" style="color: white;">{last_metric.f1_score:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metrics3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Erro Médio (MSE)</div>
            <div class="metric-value" style="color: #ef4444;">{last_metric.mse:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metrics4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Ensemble Score</div>
            <div class="metric-value" style="color: #a855f7;">{st.session_state.ensemble_accuracy:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de evolução
    st.markdown("#### 📈 Evolução de Precisão (Tempo Real)")
    
    if st.session_state.metrics:
        metrics_df = pd.DataFrame([
            {
                'timestamp': m.timestamp,
                'time_label': m.time_label,
                'accuracy': m.accuracy,
                'f1_score': m.f1_score,
                'mse': m.mse
            }
            for m in st.session_state.metrics
        ])
        
        fig = go.Figure()
        
        # Adicionar linha de precisão
        fig.add_trace(go.Scatter(
            x=metrics_df['time_label'],
            y=metrics_df['accuracy'],
            mode='lines',
            name='Accuracy',
            line=dict(color='#6366f1', width=3),
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.1)'
        ))
        
        # Adicionar linha de F1-Score
        fig.add_trace(go.Scatter(
            x=metrics_df['time_label'],
            y=metrics_df['f1_score'],
            mode='lines',
            name='F1-Score',
            line=dict(color='#10b981', width=2, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.05)'
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                zeroline=False,
                showticklabels=True,
                tickfont=dict(color='#9ca3af', size=10)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                zeroline=False,
                range=[80, 100],
                tickfont=dict(color='#9ca3af', size=10)
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#9ca3af')
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

else:  # TECHNIQUES
    st.markdown("#### 🔬 Técnicas de Otimização")
    
    # Grade de técnicas
    col_techs = st.columns(2)
    
    for i, technique in enumerate(TECHNIQUES):
        col_idx = i % 2
        with col_techs[col_idx]:
            technique_name = technique.split(":")[0]
            technique_desc = technique.split(":")[1]
            
            st.markdown(f"""
            <div class="tech-card">
                <div style="color: #10b981; font-size: 1rem;">✅</div>
                <div>
                    <div style="font-weight: bold; color: white; font-size: 0.875rem; margin-bottom: 0.25rem;">
                        {technique_name}
                    </div>
                    <div style="color: #9ca3af; font-size: 0.75rem;">
                        {technique_desc}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Painel de próxima implementação
    st.markdown("""
    <div style="background-color: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); 
         border-radius: 0.5rem; padding: 1rem; margin-top: 1rem; display: flex; align-items: center; gap: 1rem;">
        <div style="color: #6366f1; font-size: 1.5rem;">⚙️</div>
        <div style="color: #c7d2fe; font-size: 0.875rem;">
            Próxima implementação: <span style="font-weight: bold;">Meta-Learning Adaptativo</span> agendada pelo núcleo.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    active_models = sum(1 for m in st.session_state.ensemble_models if m.is_active)
    total_models = len(st.session_state.ensemble_models)
    st.markdown(f"**Modelos Ativos:** {active_models}/{total_models}")

with col_footer2:
    st.markdown(f"**Última Atualização:** {st.session_state.last_update.strftime('%H:%M:%S')}")

with col_footer3:
    optimization_status = "🟢 Ativa" if st.session_state.is_optimizing else "🟡 Pausada"
    st.markdown(f"**Otimização:** {optimization_status}")

# Atualização automática
auto_refresh = st.sidebar.checkbox("Atualização Automática", value=True)

if auto_refresh:
    time.sleep(simulation_speed)
    simulate_optimization()
    st.rerun()

# URLs para mudança de tab (simulado)
tab = st.query_params.get("tab", [st.session_state.active_tab.value])[0]
if tab in ["ENSEMBLE", "PARAMS", "METRICS", "TECHNIQUES"]:
    st.session_state.active_tab = ActiveTab(tab)