import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional, Literal, Tuple
import json
import random
from dataclasses import dataclass
from enum import Enum

# --- ENUMS & TYPES ---
class Direction(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

class PatternStatus(str, Enum):
    KNOWN = "KNOWN"
    NEWLY_REGISTERED = "NEWLY_REGISTERED"

# --- DATACLASSES ---
@dataclass
class TechnicalIndicatorInput:
    rsi: float = 0.0
    macd: float = 0.0
    stochastic: float = 0.0
    williams_r: float = 0.0
    cci: float = 0.0
    adx: float = 0.0
    aroon: float = 0.0
    mfi: float = 0.0
    ultimate_osc: float = 0.0
    roc: float = 0.0
    bollinger_upper: float = 0.0
    bollinger_middle: float = 0.0
    bollinger_lower: float = 0.0
    sma10: float = 0.0
    sma20: float = 0.0
    sma50: float = 0.0
    sma200: float = 0.0
    ema12: float = 0.0
    ema26: float = 0.0
    volume: float = 0.0
    vwap: float = 0.0
    atr: float = 0.0
    momentum: float = 0.0
    obv: float = 0.0
    cmf: float = 0.0

@dataclass
class MarketInput:
    price: float = 0.0
    volatility: float = 0.0
    trend: float = 0.0
    momentum: float = 0.0
    volume: float = 0.0
    sentiment: float = 0.0
    correlation: float = 0.0
    divergence: float = 0.0

@dataclass
class NeuralOutput:
    direction: Direction = Direction.NEUTRAL
    confidence: float = 0.0
    target_price: float = 0.0
    timeframe: str = "4H"
    probability: float = 0.0
    buy_signal: float = 0.0
    sell_signal: float = 0.0
    hold_signal: float = 0.0
    risk_assessment: float = 0.0
    stop_loss: float = 0.0
    risk_reward: float = 0.0

@dataclass
class NeuralMetrics:
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    learning_rate: float = 0.0
    iterations: int = 0
    input_nodes: int = 0
    hidden_layers: int = 0
    output_nodes: int = 0
    training_data: int = 0

@dataclass
class LearningProgress:
    epoch: int = 0
    loss: float = 0.0
    accuracy: float = 0.0
    validation_loss: float = 0.0
    validation_accuracy: float = 0.0
    timestamp: str = ""

@dataclass
class ActivePattern:
    id: str = ""
    name: str = ""
    value: float = 0.0  # 0-100 match probability
    status: PatternStatus = PatternStatus.KNOWN

# --- AGI SIMULATION ---
class SentientCore:
    def __init__(self):
        self.stability = 75.0
        self.confidence = 80.0
        self.focus = 85.0
        self.thoughts = []
    
    def get_vector(self) -> Dict[str, float]:
        return {
            "stability": self.stability,
            "confidence": self.confidence,
            "focus": self.focus
        }
    
    def get_state(self) -> str:
        avg = (self.stability + self.confidence + self.focus) / 3
        if avg > 80:
            return "CONFIDENT"
        elif avg > 60:
            return "NEUTRAL"
        elif avg > 40:
            return "CAUTIOUS"
        else:
            return "STRESSED"
    
    def perceive_reality(self, factor: float, reward: float):
        if reward > 0:
            self.confidence = min(100.0, self.confidence + 1.0)
            self.stability = min(100.0, self.stability + 0.5)
        else:
            self.confidence = max(0.0, self.confidence - 2.0)
            self.stability = max(0.0, self.stability - 1.0)
    
    def add_thought(self, thought: str):
        self.thoughts.append(f"{datetime.now().strftime('%H:%M:%S')}: {thought}")
        if len(self.thoughts) > 10:
            self.thoughts.pop(0)

# --- STREAMLIT CONFIG ---
st.set_page_config(
    page_title="Integração Neural Total",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLES ---
st.markdown("""
<style>
    .matrix-bg {
        background-color: #0a0a0a;
        color: #d1d5db;
    }
    
    .matrix-panel {
        background-color: rgba(30, 41, 59, 0.4);
        border: 1px solid #1e293b;
        border-radius: 0.5rem;
    }
    
    .metric-card {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .tab-button {
        padding: 0.5rem 1rem;
        border: none;
        background: none;
        cursor: pointer;
        font-size: 0.75rem;
        font-weight: bold;
        color: #6b7280;
        border-bottom: 2px solid transparent;
        transition: all 0.3s;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .tab-button.active {
        color: #a855f7;
        border-bottom-color: #a855f7;
    }
    
    .tab-button:hover:not(.active) {
        color: #ffffff;
    }
    
    .direction-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 2px solid;
        transition: all 0.3s;
    }
    
    .direction-bullish {
        color: #10b981;
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .direction-bearish {
        color: #ef4444;
        border-color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }
    
    .direction-neutral {
        color: #9ca3af;
        border-color: #6b7280;
        background: rgba(107, 114, 128, 0.1);
    }
    
    .signal-card {
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid;
    }
    
    .signal-buy {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    .signal-sell {
        background: rgba(239, 68, 68, 0.1);
        border-color: rgba(239, 68, 68, 0.3);
    }
    
    .signal-hold {
        background: rgba(107, 114, 128, 0.1);
        border-color: rgba(107, 114, 128, 0.3);
    }
    
    .pattern-card {
        background-color: rgba(30, 41, 59, 0.4);
        border: 1px solid #1e293b;
        border-radius: 0.5rem;
        padding: 1rem;
        height: 8rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        transition: all 0.3s;
    }
    
    .pattern-new {
        border-color: rgba(34, 197, 94, 0.5);
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.1);
    }
    
    .alert-new-pattern {
        background: rgba(234, 179, 8, 0.1);
        border: 1px solid rgba(234, 179, 8, 0.5);
        border-radius: 0.5rem;
        padding: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'tech_input' not in st.session_state:
    st.session_state.tech_input = TechnicalIndicatorInput()

if 'active_patterns' not in st.session_state:
    st.session_state.active_patterns = [
        ActivePattern(id='p1', name='Double Tops', value=0.0, status=PatternStatus.KNOWN),
        ActivePattern(id='p2', name='Head & Shoulders', value=0.0, status=PatternStatus.KNOWN),
        ActivePattern(id='p3', name='Bullish Flag', value=0.0, status=PatternStatus.KNOWN),
        ActivePattern(id='p4', name='Elliott Wave 3', value=0.0, status=PatternStatus.KNOWN),
        ActivePattern(id='p5', name='Fibonacci Retracement', value=0.0, status=PatternStatus.KNOWN),
        ActivePattern(id='p6', name='Wyckoff Spring', value=0.0, status=PatternStatus.KNOWN),
        ActivePattern(id='p7', name='Liquidity Grab', value=0.0, status=PatternStatus.KNOWN),
        ActivePattern(id='p8', name='Harmonic Gartley', value=0.0, status=PatternStatus.KNOWN)
    ]

if 'detected_pattern' not in st.session_state:
    st.session_state.detected_pattern = None

if 'market_input' not in st.session_state:
    st.session_state.market_input = MarketInput()

if 'output' not in st.session_state:
    st.session_state.output = NeuralOutput()

if 'metrics' not in st.session_state:
    st.session_state.metrics = NeuralMetrics(
        accuracy=89.4,
        precision=87.2,
        recall=91.6,
        f1_score=89.3,
        learning_rate=0.001,
        iterations=125847,
        input_nodes=47,
        hidden_layers=8,
        output_nodes=12,
        training_data=2847953
    )

if 'history' not in st.session_state:
    st.session_state.history = []

if 'is_training' not in st.session_state:
    st.session_state.is_training = True

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'PREDICTION'

if 'sentient_core' not in st.session_state:
    st.session_state.sentient_core = SentientCore()

if 'agi_mood' not in st.session_state:
    st.session_state.agi_mood = "NEUTRAL"

if 'agi_influence' not in st.session_state:
    st.session_state.agi_influence = 0.0

# --- HELPER FUNCTIONS ---
def get_direction_color(direction: Direction) -> Tuple[str, str]:
    if direction == Direction.BULLISH:
        return ("#10b981", "rgba(16, 185, 129, 0.1)", "#10b981")
    elif direction == Direction.BEARISH:
        return ("#ef4444", "rgba(239, 68, 68, 0.1)", "#ef4444")
    else:
        return ("#9ca3af", "rgba(107, 114, 128, 0.1)", "#6b7280")

def update_operations():
    """Atualiza todas as operações em tempo real"""
    if not st.session_state.is_training:
        return
    
    # 1. AGI MODULATION
    sentient_vector = st.session_state.sentient_core.get_vector()
    st.session_state.agi_mood = st.session_state.sentient_core.get_state()
    mood_bias = (sentient_vector['confidence'] + sentient_vector['focus']) / 200  # 0.0 to 1.0
    st.session_state.agi_influence = mood_bias * 100
    
    # 2. DATA GENERATION
    base_price = 42500 + (random.random() - 0.5) * 2000
    volatility = 15 + random.random() * 25 + ((100 - sentient_vector['stability']) / 10)
    
    # Technical Indicators
    new_tech = TechnicalIndicatorInput(
        rsi=30 + random.random() * 40,
        macd=(random.random() - 0.5) * 6,
        stochastic=random.random() * 100,
        williams_r=-random.random() * 100,
        cci=(random.random() - 0.5) * 400,
        adx=20 + random.random() * 60,
        aroon=random.random() * 100,
        mfi=20 + random.random() * 60,
        ultimate_osc=30 + random.random() * 40,
        roc=(random.random() - 0.5) * 10,
        bollinger_upper=base_price + 800,
        bollinger_middle=base_price,
        bollinger_lower=base_price - 800,
        sma10=base_price, sma20=base_price, sma50=base_price, sma200=base_price,
        ema12=base_price, ema26=base_price,
        volume=float(random.randint(0, 100000000)),
        vwap=base_price,
        atr=base_price * 0.02,
        momentum=(random.random() - 0.5) * 20,
        obv=float(random.randint(0, 1000000)),
        cmf=(random.random() - 0.5) * 0.4
    )
    st.session_state.tech_input = new_tech
    
    # Update Active Patterns
    for pattern in st.session_state.active_patterns:
        pattern.value = random.random() * 100
    
    # Simulate New Pattern Detection
    if not st.session_state.detected_pattern and random.random() > 0.97:
        exotic_names = ["Quantum Wedge", "Neural Divergence B", "Fractal Spin 4", "Hyper-Liquid Zone", "Void Gap Fill"]
        new_name = random.choice(exotic_names) + f" v{random.randint(0, 8)}"
        st.session_state.detected_pattern = ActivePattern(
            id=f"new-{int(time.time())}",
            name=new_name,
            value=85 + random.random() * 14,
            status=PatternStatus.NEWLY_REGISTERED
        )
    
    # Market Input
    st.session_state.market_input = MarketInput(
        price=base_price,
        volatility=volatility,
        trend=(random.random() - 0.5) * 2,
        momentum=(random.random() - 0.5) * 100,
        volume=random.random() * 100,
        sentiment=(random.random() - 0.5) * 2 + (mood_bias - 0.5),
        correlation=random.random() * 2 - 1,
        divergence=(random.random() - 0.5) * 2
    )
    
    # Neural Processing
    avg_tech = (new_tech.rsi + new_tech.adx + new_tech.mfi) / 3
    avg_pat = sum(p.value for p in st.session_state.active_patterns) / len(st.session_state.active_patterns)
    market_str = (abs(st.session_state.market_input.trend) + 
                 st.session_state.market_input.momentum + 
                 st.session_state.market_input.sentiment) / 3
    overall_conf = (avg_tech + avg_pat + market_str) / 3 + (mood_bias * 10)
    
    direction = Direction.NEUTRAL
    if overall_conf > 65:
        direction = Direction.BULLISH if st.session_state.market_input.trend > 0 else Direction.BEARISH
    
    st.session_state.output = NeuralOutput(
        direction=direction,
        confidence=min(99, max(55, overall_conf)),
        target_price=base_price * (1 + (0.02 if direction == Direction.BULLISH else -0.02)),
        timeframe=random.choice(["1H", "4H", "1D"]),
        probability=min(98, max(60, overall_conf + random.random() * 10)),
        buy_signal=70 + random.random() * 25 if direction == Direction.BULLISH else random.random() * 30,
        sell_signal=70 + random.random() * 25 if direction == Direction.BEARISH else random.random() * 30,
        hold_signal=60 + random.random() * 30 if direction == Direction.NEUTRAL else random.random() * 40,
        risk_assessment=20 + random.random() * 60 - (mood_bias * 10),
        stop_loss=base_price * 0.98,
        risk_reward=1.5 + random.random() * 2.5
    )
    
    # Update Metrics
    st.session_state.metrics.accuracy = min(99, st.session_state.metrics.accuracy + (random.random() - 0.4) * 0.1)
    st.session_state.metrics.iterations += random.randint(0, 100)
    st.session_state.metrics.training_data += random.randint(0, 1000)
    
    # Update History
    new_point = LearningProgress(
        epoch=len(st.session_state.history) + 1,
        loss=max(0.001, random.random() * 0.2),
        accuracy=85 + random.random() * 14,
        validation_loss=max(0.002, random.random() * 0.25),
        validation_accuracy=83 + random.random() * 15,
        timestamp=datetime.now().strftime("%H:%M:%S")
    )
    st.session_state.history = [*st.session_state.history[-49:], new_point]
    
    # AGI Feedback
    if random.random() > 0.9:
        reward = 1 if st.session_state.output.confidence > 80 else 0
        st.session_state.sentient_core.perceive_reality(st.session_state.market_input.volatility, reward)

def register_new_pattern():
    """Registra novo padrão detectado"""
    if st.session_state.detected_pattern:
        st.session_state.active_patterns.insert(0, st.session_state.detected_pattern)
        st.session_state.sentient_core.add_thought(
            f"Novo padrão neural assimilado: {st.session_state.detected_pattern.name}. Expandindo matriz de reconhecimento."
        )
        st.session_state.sentient_core.perceive_reality(0.5, 5)
        st.session_state.detected_pattern = None

def discard_pattern():
    """Descarta padrão detectado"""
    st.session_state.detected_pattern = None

# --- UI COMPONENTS ---
def render_header():
    """Renderiza o cabeçalho"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🧠 INTEGRAÇÃO NEURAL TOTAL")
        col1a, col1b = st.columns([2, 3])
        with col1a:
            st.markdown(f"**{len(st.session_state.active_patterns)} PADRÕES ATIVOS**")
        with col1b:
            st.markdown(f"SINTONIA AGI: **{st.session_state.agi_mood}** ({st.session_state.agi_influence:.0f}%)")
    
    with col2:
        if st.button(
            "⏸️ TREINANDO..." if st.session_state.is_training else "▶️ INICIAR",
            use_container_width=True
        ):
            st.session_state.is_training = not st.session_state.is_training

def render_tabs():
    """Renderiza as abas de navegação"""
    tabs = {
        'PREDICTION': '🎯 Previsão',
        'INDICATORS': '📊 Indicadores', 
        'PATTERNS': '🔍 Padrões',
        'LEARNING': '⚡ Aprendizado',
        'METRICS': '📈 Métricas'
    }
    
    selected_tab = st.session_state.active_tab
    
    # Criar tabs com radio buttons estilizados
    cols = st.columns(len(tabs))
    for idx, (tab_id, tab_label) in enumerate(tabs.items()):
        with cols[idx]:
            is_active = (selected_tab == tab_id)
            badge = ""
            if tab_id == 'PATTERNS' and st.session_state.detected_pattern:
                badge = "🔴"
            
            if st.button(
                f"{badge} {tab_label}",
                key=f"tab_{tab_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.active_tab = tab_id

def render_prediction_tab():
    """Renderiza aba de Previsão"""
    output = st.session_state.output
    color, bg_color, border_color = get_direction_color(output.direction)
    
    # Card de Direção
    st.markdown(f"""
    <div class="direction-card" style="border-color: {border_color}; background: {bg_color}; color: {color};">
        <div style="font-size: 0.75rem; font-weight: bold; opacity: 0.7; text-transform: uppercase; margin-bottom: 0.5rem;">
            Direção Neural Predita
        </div>
        <div style="font-size: 2.5rem; font-weight: 900; display: flex; justify-content: center; align-items: center; gap: 1rem;">
            {'📈' if output.direction == Direction.BULLISH else '📉' if output.direction == Direction.BEARISH else '⚡'}
            {output.direction}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas
    st.markdown("### Métricas de Previsão")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Confiança & Probabilidade")
        st.progress(output.confidence / 100, text=f"Confiança: {output.confidence:.1f}%")
        st.progress(output.probability / 100, text=f"Probabilidade: {output.probability:.1f}%")
    
    with col2:
        st.markdown(f"#### Alvos de Preço ({output.timeframe})")
        st.metric("Preço Alvo", f"${output.target_price:,.2f}")
        st.metric("Stop Loss", f"${output.stop_loss:,.2f}")
        st.metric("Risco / Retorno", f"1:{output.risk_reward:.2f}")
    
    with col3:
        st.markdown("#### Sinais de Saída")
        
        col3a, col3b = st.columns(2)
        with col3a:
            st.markdown(f"""
            <div class="signal-card signal-buy">
                <div style="font-size: 0.75rem; color: #10b981; font-weight: bold;">COMPRA</div>
                <div style="font-size: 1.25rem; font-family: monospace; text-align: right;">{output.buy_signal:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3b:
            st.markdown(f"""
            <div class="signal-card signal-sell">
                <div style="font-size: 0.75rem; color: #ef4444; font-weight: bold;">VENDA</div>
                <div style="font-size: 1.25rem; font-family: monospace; text-align: right;">{output.sell_signal:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="signal-card signal-hold">
            <div style="font-size: 0.75rem; color: #9ca3af; font-weight: bold;">AGUARDAR</div>
            <div style="font-size: 1.25rem; font-family: monospace; text-align: right;">{output.hold_signal:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

def render_indicators_tab():
    """Renderiza aba de Indicadores"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Radar Técnico")
        
        # Preparar dados para radar chart
        tech = st.session_state.tech_input
        radar_data = pd.DataFrame({
            'Métrica': ['RSI', 'MACD', 'Stoch', 'ADX', 'MFI', 'ROC'],
            'Valor': [
                tech.rsi,
                abs(tech.macd) * 10,
                tech.stochastic,
                tech.adx,
                tech.mfi,
                abs(tech.roc) * 10
            ]
        })
        
        fig = go.Figure(data=go.Scatterpolar(
            r=radar_data['Valor'],
            theta=radar_data['Métrica'],
            fill='toself',
            fillcolor='rgba(139, 92, 246, 0.3)',
            line_color='rgb(139, 92, 246)',
            name='Indicadores'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📋 Lista de Indicadores (RAW)")
        
        # Converter tech_input para dict
        tech_dict = {k: v for k, v in st.session_state.tech_input.__dict__.items()}
        
        # Mostrar em duas colunas
        cols = st.columns(2)
        for idx, (key, value) in enumerate(tech_dict.items()):
            with cols[idx % 2]:
                st.metric(
                    label=key.replace('_', ' ').upper(),
                    value=f"{value:.2f}" if isinstance(value, float) else value
                )

def render_patterns_tab():
    """Renderiza aba de Padrões"""
    # Alerta de novo padrão
    if st.session_state.detected_pattern:
        st.markdown(f"""
        <div class="alert-new-pattern">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                <div style="padding: 0.5rem; background: rgba(234, 179, 8, 0.2); border-radius: 50%; border: 1px solid rgba(234, 179, 8, 0.5);">
                    🔍
                </div>
                <div>
                    <h3 style="margin: 0; color: white; font-weight: bold;">
                        ANOMALIA DETECTADA: {st.session_state.detected_pattern.name}
                    </h3>
                    <p style="margin: 0; color: rgba(234, 179, 8, 0.8); font-size: 0.875rem;">
                        Probabilidade de Correspondência: {st.session_state.detected_pattern.value:.1f}%
                    </p>
                </div>
            </div>
            <div style="display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 1rem;">
                <button onclick="discardPattern()" style="padding: 0.5rem 1rem; border: 1px solid #4b5563; background: transparent; color: #9ca3af; border-radius: 0.25rem; cursor: pointer;">
                    IGNORAR
                </button>
                <button onclick="registerNewPattern()" style="padding: 0.5rem 1rem; background: #eab308; color: black; border: none; border-radius: 0.25rem; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 0.25rem;">
                    ➕ REGISTRAR PADRÃO
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botões reais
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ IGNORAR", use_container_width=True):
                discard_pattern()
                st.rerun()
        with col2:
            if st.button("✅ REGISTRAR PADRÃO", type="primary", use_container_width=True):
                register_new_pattern()
                st.rerun()
    
    st.markdown("### Padrões Ativos")
    
    # Mostrar padrões em grid
    cols = st.columns(5)
    for idx, pattern in enumerate(st.session_state.active_patterns):
        with cols[idx % 5]:
            is_new = (pattern.status == PatternStatus.NEWLY_REGISTERED)
            border_color = "#22c55e" if is_new else "#1e293b"
            progress_color = "#22c55e" if is_new else "#8b5cf6"
            
            st.markdown(f"""
            <div class="pattern-card {'pattern-new' if is_new else ''}" style="border-color: {border_color};">
                {('✅' if is_new else '')}
                <div style="font-size: 0.625rem; color: #9ca3af; text-align: center; margin-bottom: 0.5rem; text-transform: uppercase;">
                    {pattern.name}
                </div>
                <div style="font-size: 1.25rem; font-weight: bold; color: white; margin-bottom: 0.5rem;">
                    {pattern.value:.1f}%
                </div>
                <div style="width: 100%; height: 0.375rem; background: #1f2937; border-radius: 0.1875rem; overflow: hidden;">
                    <div style="height: 100%; background: {progress_color}; width: {pattern.value}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_learning_tab():
    """Renderiza aba de Aprendizado"""
    st.markdown("#### 📈 Evolução de Aprendizado (Precisão vs Perda)")
    
    if st.session_state.history:
        # Converter histórico para DataFrame
        history_df = pd.DataFrame([{
            'epoch': h.epoch,
            'timestamp': h.timestamp,
            'accuracy': h.accuracy,
            'validation_accuracy': h.validation_accuracy,
            'loss': h.loss
        } for h in st.session_state.history])
        
        # Criar gráfico com área
        fig = go.Figure()
        
        # Área de precisão (verde)
        fig.add_trace(go.Scatter(
            x=history_df['timestamp'],
            y=history_df['accuracy'],
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.2)',
            line_color='#10b981',
            name='Precisão',
            yaxis='y1'
        ))
        
        # Linha de precisão de validação (amarela)
        fig.add_trace(go.Scatter(
            x=history_df['timestamp'],
            y=history_df['validation_accuracy'],
            line_color='#eab308',
            name='Neutra',
            yaxis='y1'
        ))
        
        # Linha de perda (vermelha)
        fig.add_trace(go.Scatter(
            x=history_df['timestamp'],
            y=history_df['loss'],
            line_color='#ef4444',
            name='Perda',
            yaxis='y2'
        ))
        
        fig.update_layout(
            yaxis=dict(
                title="Precisão (%)",
                range=[0, 100],
                titlefont=dict(color="#10b981"),
                tickfont=dict(color="#666")
            ),
            yaxis2=dict(
                title="Perda",
                overlaying="y",
                side="right",
                titlefont=dict(color="#ef4444"),
                tickfont=dict(color="#666")
            ),
            xaxis=dict(showgrid=True, gridcolor="#222"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aguardando dados de treinamento...")

def render_metrics_tab():
    """Renderiza aba de Métricas"""
    metrics = st.session_state.metrics
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Precisão Geral", f"{metrics.accuracy:.1f}%")
        st.progress(metrics.accuracy / 100)
    
    with col2:
        st.metric("Iterações de Treino", f"{metrics.iterations:,}")
    
    with col3:
        st.metric("Pontos de Dados", f"{metrics.training_data / 1e6:.2f}M")
    
    with col4:
        st.metric("Score F1", f"{metrics.f1_score:.1f}")
    
    st.markdown("---")
    
    # Informações adicionais
    col5, col6 = st.columns(2)
    
    with col5:
        st.metric("Taxa de Aprendizado", f"{metrics.learning_rate:.4f}")
        st.metric("Precisão", f"{metrics.precision:.1f}%")
    
    with col6:
        st.metric("Recall", f"{metrics.recall:.1f}%")
        st.metric("Input Nodes", metrics.input_nodes)
    
    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 0.5rem; border: 1px solid #374151; text-align: center; color: #9ca3af; font-size: 0.75rem;">
        Estrutura Neural: {metrics.input_nodes} Input Nodes → {metrics.hidden_layers} Hidden Layers → {metrics.output_nodes} Output Nodes
    </div>
    """, unsafe_allow_html=True)

# --- MAIN APP ---
def main():
    # Atualizar operações se estiver treinando
    update_operations()
    
    # Renderizar interface
    render_header()
    st.markdown("---")
    render_tabs()
    st.markdown("---")
    
    # Renderizar aba ativa
    if st.session_state.active_tab == 'PREDICTION':
        render_prediction_tab()
    elif st.session_state.active_tab == 'INDICATORS':
        render_indicators_tab()
    elif st.session_state.active_tab == 'PATTERNS':
        render_patterns_tab()
    elif st.session_state.active_tab == 'LEARNING':
        render_learning_tab()
    elif st.session_state.active_tab == 'METRICS':
        render_metrics_tab()
    
    # Auto-refresh se estiver treinando
    if st.session_state.is_training:
        time.sleep(1)  # Atualizar a cada 1 segundo
        st.rerun()

if __name__ == "__main__":
    main()