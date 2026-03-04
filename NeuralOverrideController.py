import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass


# Configuração da página
st.set_page_config(
    page_title="Controlador de Override Neural",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Enums e Classes de Tipos
class OverrideStatus(str, Enum):
    APPROVED = "approved"
    AUTO_BLOCKED = "auto-blocked"
    PENDING = "pending"
    REJECTED = "rejected"


class DecisionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class ActiveTab(str, Enum):
    DECISIONS = "DECISIONS"
    ATTEMPTS = "ATTEMPTS"
    CONFIG = "CONFIG"


class SentientState(str, Enum):
    STABLE = "STABLE"
    DEFENSIVE = "DEFENSIVE"
    ANXIOUS = "ANXIOUS"
    CONFIDENT = "CONFIDENT"
    EUPHORIC = "EUPHORIC"
    MONITORING = "MONITORING"


@dataclass
class OverrideAttempt:
    """Tentativa de override humano"""

    id: str
    timestamp: datetime
    user_id: str
    action: str
    asset: str
    reason: str
    status: OverrideStatus
    risk_level: int
    neural_confidence: float


@dataclass
class NeuralDecision:
    """Decisão neural do sistema"""

    id: str
    asset: str
    decision: DecisionType
    confidence: float
    reasoning: List[str]
    technical_indicators: List[str]
    risk_assessment: int
    expected_return: float
    timeframe: str


@dataclass
class ControlSettings:
    """Configurações de controle"""

    max_overrides_per_day: int
    minimum_confidence_threshold: float
    auto_block_threshold: float
    requires_approval_above: float
    allow_user_override: bool


class SentientCore:
    """Serviço de Núcleo Sentiente (AGI)"""

    def __init__(self):
        self.thoughts: List[str] = []
        self.state: SentientState = SentientState.STABLE
        self.stability: float = 85.0
        self.emotion_vector: Dict[str, float] = {
            "stability": 85.0,
            "confidence": 92.0,
            "focus": 88.0,
        }

    def get_state(self) -> SentientState:
        return self.state

    def get_vector(self) -> Dict[str, float]:
        return self.emotion_vector.copy()

    def add_thought(self, thought: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.thoughts.append(f"[{timestamp}] {thought}")
        if len(self.thoughts) > 20:
            self.thoughts.pop(0)

        if "BLOQUEADO" in thought or "EMERGÊNCIA" in thought:
            self.state = SentientState.ANXIOUS
            self.stability = max(0, self.stability - 20)
        elif "DESBLOQUEADO" in thought or "NORMAL" in thought:
            self.state = SentientState.STABLE
            self.stability = min(100, self.stability + 10)

    def perceive_reality(self, value: float, level: int) -> None:
        if level > 0:
            self.emotion_vector["confidence"] = min(
                100, self.emotion_vector["confidence"] + value
            )
            self.state = SentientState.CONFIDENT
        else:
            self.emotion_vector["stability"] = max(
                0, self.emotion_vector["stability"] - abs(value)
            )
            self.state = SentientState.DEFENSIVE

        if value > 0:
            self.add_thought(f"Percepção positiva: Reforço recebido (nível {level})")
        else:
            self.add_thought(f"Percepção negativa: Ajuste necessário (nível {level})")


def init_override_attempts() -> List[OverrideAttempt]:
    """Inicializa tentativas de override"""
    return [
        OverrideAttempt(
            id="1",
            timestamp=datetime.now(),
            user_id="USER-ADMIN",
            action="Vender BTCUSDT",
            asset="BTCUSDT",
            reason="Necessidade de liquidez",
            status=OverrideStatus.AUTO_BLOCKED,
            risk_level=95,
            neural_confidence=92.0,
        ),
        OverrideAttempt(
            id="2",
            timestamp=datetime.now() - timedelta(hours=1),
            user_id="USER-ADMIN",
            action="Comprar AAPL",
            asset="AAPL",
            reason="Oportunidade percebida",
            status=OverrideStatus.REJECTED,
            risk_level=87,
            neural_confidence=89.0,
        ),
    ]


def init_neural_decisions() -> List[NeuralDecision]:
    """Inicializa decisões neurais"""
    return [
        NeuralDecision(
            id="1",
            asset="BTCUSDT",
            decision=DecisionType.HOLD,
            confidence=92.0,
            reasoning=[
                "Tendência de alta confirmada",
                "RSI sobrecompra controlada",
                "Volume crescente",
            ],
            technical_indicators=["RSI: 68", "MACD: Positivo", "BB: Breakout"],
            risk_assessment=25,
            expected_return=12.5,
            timeframe="1-2 semanas",
        ),
        NeuralDecision(
            id="2",
            asset="ETHUSDT",
            decision=DecisionType.BUY,
            confidence=89.0,
            reasoning=[
                "Padrão de reversão",
                "Suporte EMA200",
                "Fundamentals sólidos",
            ],
            technical_indicators=["EMA20: Suporte", "Volume: Alto", "Fibonacci: 38.2%"],
            risk_assessment=18,
            expected_return=8.7,
            timeframe="3-5 dias",
        ),
    ]


def init_settings() -> ControlSettings:
    """Inicializa configurações"""
    return ControlSettings(
        max_overrides_per_day=3,
        minimum_confidence_threshold=75,
        auto_block_threshold=90,
        requires_approval_above=85,
        allow_user_override=True,
    )


# Inicialização do estado
if "sentient_core" not in st.session_state:
    st.session_state.sentient_core = SentientCore()

if "override_attempts" not in st.session_state:
    st.session_state.override_attempts = init_override_attempts()

if "neural_decisions" not in st.session_state:
    st.session_state.neural_decisions = init_neural_decisions()

if "settings" not in st.session_state:
    st.session_state.settings = init_settings()

if "system_locked" not in st.session_state:
    st.session_state.system_locked = False

if "overrides_today" not in st.session_state:
    st.session_state.overrides_today = 0

if "active_tab" not in st.session_state:
    st.session_state.active_tab = ActiveTab.DECISIONS

if "toast" not in st.session_state:
    st.session_state.toast = None

if "agi_message" not in st.session_state:
    st.session_state.agi_message = "Monitorando..."

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()


# CSS Customizado
st.markdown(
    """
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
        background-color: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.5);
        border-radius: 0.25rem;
    }

    .pulse-icon {
        color: #ef4444;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .system-status {
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid;
        font-size: 0.75rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .system-locked {
        background-color: #ef4444;
        color: white;
        border-color: #ef4444;
        animation: pulse 1s infinite;
    }

    .system-unlocked {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border-color: #10b981;
    }

    .toast-container {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .toast {
        padding: 0.75rem 1rem;
        border-radius: 0.25rem;
        border: 1px solid;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: bold;
        font-size: 0.75rem;
        margin-bottom: 0.5rem;
    }

    .toast-success {
        background-color: rgba(16, 185, 129, 0.9);
        border-color: #10b981;
        color: #d1fae5;
    }

    .toast-error {
        background-color: rgba(239, 68, 68, 0.9);
        border-color: #ef4444;
        color: #fecaca;
    }

    .toast-warning {
        background-color: rgba(245, 158, 11, 0.9);
        border-color: #f59e0b;
        color: #fef3c7;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        padding: 1.5rem;
        padding-bottom: 0.5rem;
    }

    .metric-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
    }

    .metric-label {
        color: #9ca3af;
        font-size: 0.625rem;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }

    .metric-value {
        color: white;
        font-size: 1.5rem;
        font-family: monospace;
        font-weight: bold;
        margin-bottom: 0.25rem;
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
        border-radius: 0.125rem;
    }

    .tab-navigation {
        display: flex;
        padding: 0 1.5rem;
        border-bottom: 1px solid #374151;
    }

    .tab-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        font-size: 0.75rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        border-bottom: 2px solid transparent;
    }

    .tab-button.active {
        color: #3b82f6;
        border-bottom-color: #3b82f6;
    }

    .decision-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-left: 4px solid #3b82f6;
        border-radius: 0 0.5rem 0.5rem 0;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }

    .decision-card:hover {
        border-color: #374151;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .confidence-badge {
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid;
        font-size: 0.625rem;
        font-weight: bold;
    }

    .confidence-high {
        color: #10b981;
        background-color: rgba(16, 185, 129, 0.2);
        border-color: #10b981;
    }

    .confidence-medium {
        color: #f59e0b;
        background-color: rgba(245, 158, 11, 0.2);
        border-color: #f59e0b;
    }

    .confidence-low {
        color: #ef4444;
        background-color: rgba(239, 68, 68, 0.2);
        border-color: #ef4444;
    }

    .decision-badge {
        padding: 0.125rem 0.5rem;
        background-color: #1f2937;
        color: #9ca3af;
        border: 1px solid #374151;
        border-radius: 0.25rem;
        font-size: 0.625rem;
        font-weight: bold;
        text-transform: uppercase;
    }

    .attempts-table {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        overflow: hidden;
    }

    .table-header {
        background-color: rgba(0, 0, 0, 0.4);
        color: #9ca3af;
        font-family: monospace;
        text-transform: uppercase;
        font-size: 0.75rem;
    }

    .table-cell {
        padding: 0.75rem;
        font-size: 0.75rem;
    }

    .status-badge {
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.625rem;
        font-weight: bold;
        text-transform: uppercase;
    }

    .status-approved {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid #10b981;
    }

    .status-blocked {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
    }

    .status-pending {
        background-color: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid #f59e0b;
    }
</style>
""",
    unsafe_allow_html=True,
)


def get_confidence_color(confidence: float) -> str:
    if confidence >= 90:
        return "confidence-high"
    elif confidence >= 80:
        return "confidence-medium"
    else:
        return "confidence-low"


def show_toast(message: str, toast_type: str) -> None:
    st.session_state.toast = {
        "message": message,
        "type": toast_type,
        "timestamp": datetime.now(),
    }


def handle_emergency_lock(reason: str = "Bloqueio manual de emergência") -> None:
    st.session_state.system_locked = True
    show_toast(reason, "error")
    st.session_state.sentient_core.add_thought(f"SISTEMA BLOQUEADO: {reason}")
    st.session_state.sentient_core.perceive_reality(5.0, -10)


def request_override(decision_id: str) -> None:
    if st.session_state.system_locked:
        show_toast("Sistema bloqueado. Override não disponível.", "error")
        return

    decision = next(
        (d for d in st.session_state.neural_decisions if d.id == decision_id), None
    )
    if not decision:
        return

    if st.session_state.overrides_today >= st.session_state.settings.max_overrides_per_day:
        show_toast("Limite diário de overrides atingido.", "error")
        return

    if decision.confidence >= st.session_state.settings.auto_block_threshold:
        show_toast(
            f"Override bloqueado: Confiança IA ({decision.confidence:.1f}%) excede limite de segurança.",
            "error",
        )
        add_attempt(decision, OverrideStatus.AUTO_BLOCKED, "Confiança Neural Excessiva")
        return

    is_pending = decision.confidence >= st.session_state.settings.requires_approval_above
    status = OverrideStatus.PENDING if is_pending else OverrideStatus.APPROVED

    add_attempt(decision, status, "Divergência de Análise Humana")

    if status == OverrideStatus.APPROVED:
        st.session_state.overrides_today += 1
        show_toast("Override aprovado e executado.", "success")
        st.session_state.sentient_core.perceive_reality(2.0, 0)
    else:
        show_toast("Override pendente de aprovação superior.", "warning")


def add_attempt(
    decision: NeuralDecision, status: OverrideStatus, reason: str
) -> None:
    new_attempt = OverrideAttempt(
        id=f"ATT-{int(time.time())}",
        timestamp=datetime.now(),
        user_id="ADMIN",
        action=f"Override: {decision.decision.value} {decision.asset}",
        asset=decision.asset,
        reason=reason,
        status=status,
        risk_level=int(100 - decision.confidence),
        neural_confidence=decision.confidence,
    )
    st.session_state.override_attempts = [
        new_attempt,
        *st.session_state.override_attempts,
    ]


def simulate_agi_loop() -> None:
    if st.session_state.system_locked:
        return

    agi_state = st.session_state.sentient_core.get_state()
    emotion = st.session_state.sentient_core.get_vector()

    if emotion["stability"] < 20 and not st.session_state.system_locked:
        handle_emergency_lock(
            "Instabilidade Emocional da AGI detectada. Bloqueio preventivo."
        )

    if agi_state in [SentientState.DEFENSIVE, SentientState.ANXIOUS]:
        st.session_state.settings.auto_block_threshold = 85
        st.session_state.settings.requires_approval_above = 75
        st.session_state.agi_message = (
            f"AGI em estado {agi_state.value}. Limites de segurança aumentados."
        )
    elif agi_state in [SentientState.CONFIDENT, SentientState.EUPHORIC]:
        st.session_state.settings.auto_block_threshold = 95
        st.session_state.settings.requires_approval_above = 90
        st.session_state.agi_message = (
            f"AGI em estado {agi_state.value}. Limites relaxados para fluxo."
        )

    for decision in st.session_state.neural_decisions:
        decision.confidence = min(
            99.0,
            max(70.0, decision.confidence + (random.random() - 0.5) * 2),
        )

    st.session_state.last_update = datetime.now()


# Barra lateral
with st.sidebar:
    st.markdown("### ⚙️ Controles do Sistema")

    if st.button(
        "🚨 BLOQUEIO DE EMERGÊNCIA",
        disabled=st.session_state.system_locked,
        use_container_width=True,
    ):
        handle_emergency_lock()
        st.experimental_rerun()

    st.markdown("---")

    st.markdown("### 🛡️ Status do Sistema")

    col_status1, col_status2 = st.columns(2)
    with col_status1:
        system_status = "🔴 BLOQUEADO" if st.session_state.system_locked else "🟢 OPERACIONAL"
        st.metric("Status", system_status)
    with col_status2:
        st.metric("Overrides Hoje", st.session_state.overrides_today)

    st.markdown("---")

    st.markdown("### 🧠 Estado AGI")
    sentient_state = st.session_state.sentient_core.get_state()
    emotion_vector = st.session_state.sentient_core.get_vector()
    st.markdown(f"**Estado:** {sentient_state.value}")

    col_agi1, col_agi2, col_agi3 = st.columns(3)
    with col_agi1:
        st.markdown(f"**Estabilidade:** {emotion_vector['stability']:.0f}%")
    with col_agi2:
        st.markdown(f"**Confiança:** {emotion_vector['confidence']:.0f}%")
    with col_agi3:
        st.markdown(f"**Foco:** {emotion_vector['focus']:.0f}%")

    st.markdown("---")
    st.markdown("### 📝 Logs AGI")
    logs_container = st.container(height=200)
    with logs_container:
        for thought in reversed(st.session_state.sentient_core.thoughts[-5:]):
            st.markdown(
                f"""
            <div style="background-color: rgba(0, 0, 0, 0.3); padding: 0.5rem; border-radius: 0.25rem; 
                 margin-bottom: 0.25rem; border-left: 3px solid #ef4444;">
                <div style="color: #9ca3af; font-size: 0.75rem;">{thought}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )


if st.session_state.toast:
    toast_class = {
        "success": "toast-success",
        "error": "toast-error",
        "warning": "toast-warning",
    }.get(st.session_state.toast["type"], "toast-success")
    toast_icon = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
    }.get(st.session_state.toast["type"], "✅")
    st.markdown(
        f"""
    <div class="toast-container">
        <div class="toast {toast_class}">
            <span>{toast_icon}</span>
            <span>{st.session_state.toast['message']}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


st.markdown(
    f"""
<div class="neural-header">
    <div class="header-left">
        <div class="header-icon">
            <span class="pulse-icon" style="font-size: 1.25rem;">🧠</span>
        </div>
        <div>
            <h1 style="color: white; font-weight: bold; letter-spacing: 0.1em; margin: 0;">
                CONTROLADOR DE OVERRIDE NEURAL
            </h1>
            <div style="color: #ef4444; font-size: 0.625rem; font-family: monospace; margin-top: 0.25rem;">
                INTERVENÇÃO HUMANA • SUPERVISÃO AGI
            </div>
        </div>
    </div>
    <div class="header-right" style="display: flex; align-items: center; gap: 1rem;">
        <div class="system-status {'system-locked' if st.session_state.system_locked else 'system-unlocked'}">
            <span>{'🔒' if st.session_state.system_locked else '🔓'}</span>
            <span>{'SISTEMA BLOQUEADO' if st.session_state.system_locked else 'OPERACIONAL'}</span>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)

override_ratio = (
    st.session_state.overrides_today / st.session_state.settings.max_overrides_per_day
)
progress_color = "#ef4444" if override_ratio >= 1 else "#3b82f6"
st.markdown(
    f"""
<div class="metric-card">
    <div class="metric-label">Overrides Hoje</div>
    <div style="display: flex; justify-content: space-between; align-items: end;">
        <span class="metric-value">{st.session_state.overrides_today}</span>
        <span style="color: #6b7280; font-size: 0.75rem;">Limite: {st.session_state.settings.max_overrides_per_day}</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="background-color: {progress_color}; width: {min(100, override_ratio * 100)}%;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

avg_confidence = (
    sum(d.confidence for d in st.session_state.neural_decisions)
    / len(st.session_state.neural_decisions)
    if st.session_state.neural_decisions
    else 0
)
st.markdown(
    f"""
<div class="metric-card">
    <div class="metric-label">Confiança Média IA</div>
    <div class="metric-value" style="color: #a855f7;">{avg_confidence:.1f}%</div>
</div>
""",
    unsafe_allow_html=True,
)

auto_blocks = sum(
    1
    for a in st.session_state.override_attempts
    if a.status == OverrideStatus.AUTO_BLOCKED
)
st.markdown(
    f"""
<div class="metric-card">
    <div class="metric-label">Bloqueios Auto</div>
    <div class="metric-value" style="color: #ef4444;">{auto_blocks}</div>
</div>
""",
    unsafe_allow_html=True,
)

protection_rate = 94.2
st.markdown(
    f"""
<div class="metric-card">
    <div class="metric-label">Taxa de Proteção</div>
    <div class="metric-value" style="color: #10b981;">{protection_rate}%</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    f"""
<div class="tab-navigation">
    <div class="tab-button {'active' if st.session_state.active_tab == ActiveTab.DECISIONS else ''}">
        <span>🧠</span>
        <span>Decisões Neurais</span>
    </div>
    <div class="tab-button {'active' if st.session_state.active_tab == ActiveTab.ATTEMPTS else ''}">
        <span>📋</span>
        <span>Tentativas ({len(st.session_state.override_attempts)})</span>
    </div>
    <div class="tab-button {'active' if st.session_state.active_tab == ActiveTab.CONFIG else ''}">
        <span>⚙️</span>
        <span>Configuração</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


if st.session_state.active_tab == ActiveTab.DECISIONS:
    st.markdown("#### 🧠 Decisões Neurais")
    for decision in st.session_state.neural_decisions:
        confidence_class = get_confidence_color(decision.confidence)
        st.markdown(
            f"""
        <div class="decision-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.25rem;">
                        <span style="font-weight: bold; color: white; font-size: 1.125rem;">{decision.asset}</span>
                        <span class="decision-badge">{decision.decision.value}</span>
                        <span class="confidence-badge {confidence_class}">{decision.confidence:.1f}% CONFIANÇA</span>
                    </div>
                    <div style="color: #9ca3af; font-size: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                        <span>⏱️</span>
                        <span>Timeframe: {decision.timeframe}</span>
                    </div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


