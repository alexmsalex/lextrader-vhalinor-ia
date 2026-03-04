import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum
import random
import time

# Configuração da página
st.set_page_config(
    page_title="Análise de Preço Quântica",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enums e Classes de Tipos
class TimeHorizon(str, Enum):
    ULTRA_SHORT = "ULTRA_SHORT"
    SHORT_TERM = "SHORT_TERM"
    MEDIUM_TERM = "MEDIUM_TERM"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class MarketRegime(str, Enum):
    TRENDING = "TRENDING"
    MEAN_REVERSION = "MEAN_REVERSION"
    RANGING = "RANGING"
    VOLATILE = "VOLATILE"

class MarketDataPoint:
    def __init__(self, timestamp: datetime, price: float, volume: float):
        self.timestamp = timestamp
        self.price = price
        self.volume = volume

class WavefunctionState:
    def __init__(self, amplitude: List[float], phase: List[float]):
        self.amplitude = amplitude
        self.phase = phase

class PricePrediction:
    def __init__(self, time_horizon: TimeHorizon, predicted_price: float, 
                 current_price: float, confidence: float, 
                 wavefunction_state: WavefunctionState, 
                 probability_distribution: List[float]):
        self.time_horizon = time_horizon
        self.predicted_price = predicted_price
        self.current_price = current_price
        self.confidence = confidence
        self.wavefunction_state = wavefunction_state
        self.probability_distribution = probability_distribution

class QuantumMetrics:
    def __init__(self, coherence: float, entropy: float):
        self.coherence = coherence
        self.entropy = entropy

class RiskAssessment:
    def __init__(self, risk_level: RiskLevel, score: float, factors: List[str]):
        self.risk_level = risk_level
        self.score = score
        self.factors = factors

class PriceAnalysisResult:
    def __init__(self, symbol: str, market_regime: MarketRegime, 
                 volatility_estimate: float, quantum_metrics: QuantumMetrics,
                 risk_assessment: RiskAssessment, predictions: List[PricePrediction]):
        self.symbol = symbol
        self.market_regime = market_regime
        self.volatility_estimate = volatility_estimate
        self.quantum_metrics = quantum_metrics
        self.risk_assessment = risk_assessment
        self.predictions = predictions

# Analisador de Preço Quântico
class QuantumPriceAnalyzer:
    def __init__(self):
        self.results_history: List[PriceAnalysisResult] = []
    
    def analyze_price_quantum(self, symbol: str, prices: List[float]) -> PriceAnalysisResult:
        """Analisa os preços usando simulação quântica"""
        
        current_price = prices[-1] if prices else 0
        
        # Simular estados da função de onda
        num_points = 100
        amplitude = []
        phase = []
        
        for i in range(num_points):
            # Simular padrões de onda quântica
            x = i / num_points * 2 * np.pi
            amp_val = np.abs(np.sin(x) * np.cos(x * 2) * np.random.normal(1, 0.1))
            phase_val = np.angle(np.exp(1j * x) * np.random.normal(1, 0.1))
            amplitude.append(amp_val)
            phase.append(phase_val)
        
        # Normalizar amplitude
        max_amp = max(amplitude) if amplitude else 1
        amplitude = [a / max_amp for a in amplitude]
        
        # Gerar distribuição de probabilidade (normal)
        prob_dist = []
        for i in range(num_points):
            mu = current_price * (1 + 0.05 * np.sin(i/10))
            sigma = current_price * 0.02
            prob = np.exp(-0.5 * ((i - mu/current_price*10) / sigma)**2)
            prob_dist.append(prob)
        
        # Normalizar distribuição de probabilidade
        total_prob = sum(prob_dist)
        prob_dist = [p / total_prob for p in prob_dist]
        
        # Criar previsões para diferentes horizontes temporais
        predictions = []
        horizons = [TimeHorizon.ULTRA_SHORT, TimeHorizon.SHORT_TERM, TimeHorizon.MEDIUM_TERM]
        
        for horizon in horizons:
            # Calcular preço previsto baseado no horizonte
            if horizon == TimeHorizon.ULTRA_SHORT:
                price_mult = 1 + random.uniform(-0.01, 0.01)
                confidence = random.uniform(0.85, 0.95)
            elif horizon == TimeHorizon.SHORT_TERM:
                price_mult = 1 + random.uniform(-0.03, 0.03)
                confidence = random.uniform(0.75, 0.85)
            else:  # MEDIUM_TERM
                price_mult = 1 + random.uniform(-0.08, 0.08)
                confidence = random.uniform(0.65, 0.75)
            
            predicted_price = current_price * price_mult
            
            # Criar função de onda para esta previsão
            wave_state = WavefunctionState(
                amplitude=amplitude.copy(),
                phase=phase.copy()
            )
            
            predictions.append(PricePrediction(
                time_horizon=horizon,
                predicted_price=predicted_price,
                current_price=current_price,
                confidence=confidence,
                wavefunction_state=wave_state,
                probability_distribution=prob_dist.copy()
            ))
        
        # Criar métricas quânticas
        quantum_metrics = QuantumMetrics(
            coherence=random.uniform(0.7, 0.95),
            entropy=random.uniform(0.3, 0.7)
        )
        
        # Avaliação de risco
        volatility = np.std(prices[-20:]) / np.mean(prices[-20:]) if len(prices) >= 20 else 0.02
        risk_score = volatility * 100
        
        if risk_score < 1.5:
            risk_level = RiskLevel.LOW
        elif risk_score < 3.0:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.HIGH
        
        risk_assessment = RiskAssessment(
            risk_level=risk_level,
            score=risk_score,
            factors=[
                f"Volatilidade: {volatility*100:.2f}%",
                "Correlação de mercado",
                "Liquidez atual",
                "Eventos macroeconômicos"
            ]
        )
        
        # Determinar regime de mercado
        if volatility > 0.03:
            market_regime = MarketRegime.VOLATILE
        elif len(prices) > 10 and all(prices[i] > prices[i-1] for i in range(1, len(prices))):
            market_regime = MarketRegime.TRENDING
        else:
            market_regime = random.choice([MarketRegime.MEAN_REVERSION, MarketRegime.RANGING])
        
        result = PriceAnalysisResult(
            symbol=symbol,
            market_regime=market_regime,
            volatility_estimate=volatility,
            quantum_metrics=quantum_metrics,
            risk_assessment=risk_assessment,
            predictions=predictions
        )
        
        self.results_history.append(result)
        return result

# Inicialização
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = QuantumPriceAnalyzer()

if 'selected_horizon' not in st.session_state:
    st.session_state.selected_horizon = 0

if 'market_data' not in st.session_state:
    # Gerar dados de mercado de exemplo
    base_price = 45000
    st.session_state.market_data = []
    for i in range(100):
        price = base_price + np.sin(i/10) * 1000 + random.random() * 500
        st.session_state.market_data.append(
            MarketDataPoint(
                timestamp=datetime.now() - timedelta(minutes=100-i),
                price=price,
                volume=random.uniform(100, 1000)
            )
        )

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
    
    .purple-glow {
        color: #a855f7;
        text-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
    }
    
    .metric-value {
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .horizon-btn {
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: 1px solid #374151;
        background: transparent;
        color: #9ca3af;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 0.75rem;
    }
    
    .horizon-btn:hover {
        background-color: rgba(255, 255, 255, 0.05);
    }
    
    .horizon-btn.active {
        background-color: rgba(168, 85, 247, 0.2);
        border-color: #a855f7;
        color: white;
    }
    
    .confidence-bar {
        height: 0.5rem;
        background-color: #1f2937;
        border-radius: 0.25rem;
        overflow: hidden;
    }
    
    .confidence-fill {
        height: 100%;
        background-color: #a855f7;
        border-radius: 0.25rem;
    }
    
    .risk-high { color: #ef4444; }
    .risk-medium { color: #f59e0b; }
    .risk-low { color: #10b981; }
</style>
""", unsafe_allow_html=True)

# Parâmetros da aplicação
symbol = st.sidebar.text_input("Símbolo", value="BTC/USD")
auto_refresh = st.sidebar.checkbox("Atualização Automática", value=True)
refresh_interval = st.sidebar.slider("Intervalo (segundos)", 1, 60, 5)

# Header
st.markdown("""
<div style="padding: 1rem; border-bottom: 1px solid #374151; background-color: #111827; display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
        <div style="padding: 0.5rem; background-color: rgba(168, 85, 247, 0.2); border: 1px solid rgba(168, 85, 247, 0.5); border-radius: 0.25rem;">
            <span class="purple-glow" style="font-size: 1.25rem;">⚛️</span>
        </div>
        <div>
            <h2 style="color: white; font-weight: bold; letter-spacing: 0.1em; margin: 0;">ANÁLISE DE PREÇO QUÂNTICA</h2>
            <div style="color: #a855f7; font-size: 0.625rem; font-family: monospace;">
                COLAPSO DA FUNÇÃO DE ONDA
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Analisar dados
if st.session_state.market_data:
    prices = [d.price for d in st.session_state.market_data]
    
    if len(prices) >= 10:
        result = st.session_state.analyzer.analyze_price_quantum(symbol, prices)
        
        # Botões de horizonte temporal
        col_horizons = st.columns(3)
        horizons = [TimeHorizon.ULTRA_SHORT, TimeHorizon.SHORT_TERM, TimeHorizon.MEDIUM_TERM]
        
        for i, horizon in enumerate(horizons):
            with col_horizons[i]:
                is_active = st.session_state.selected_horizon == i
                btn_class = "active" if is_active else ""
                if st.button(
                    horizon.value,
                    key=f"horizon_{i}",
                    use_container_width=True
                ):
                    st.session_state.selected_horizon = i
                    st.rerun()
        
        current_pred = result.predictions[st.session_state.selected_horizon]
        
        # Layout principal
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            # Painel de Predição
            st.markdown('<div class="quantum-panel">', unsafe_allow_html=True)
            st.markdown("#### 🎯 PREDIÇÃO")
            st.markdown(f'<div class="metric-value" style="color: white;">${current_pred.predicted_price:,.2f}</div>', unsafe_allow_html=True)
            
            # Indicador de tendência
            trend_diff = ((current_pred.predicted_price - current_pred.current_price) / current_pred.current_price * 100)
            trend_icon = "📈" if trend_diff > 0 else "📉"
            trend_color = "#10b981" if trend_diff > 0 else "#ef4444"
            
            st.markdown(f"""
            <div style="color: {trend_color}; display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                {trend_icon} {abs(trend_diff):.2f}% Previsto
            </div>
            """, unsafe_allow_html=True)
            
            # Barra de confiança
            st.markdown("**Confiança**")
            confidence_pct = current_pred.confidence * 100
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5rem 0;">
                <span>{confidence_pct:.1f}%</span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: {confidence_pct}%"></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Painel de Métricas
            st.markdown('<div class="quantum-panel" style="margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown("#### 🧠 Métricas de Estado")
            
            col_metrics1, col_metrics2 = st.columns(2)
            
            with col_metrics1:
                st.metric("Coerência", f"{result.quantum_metrics.coherence:.4f}")
                st.metric("Volatilidade", f"{result.volatility_estimate*100:.2f}%")
            
            with col_metrics2:
                st.metric("Entropia", f"{result.quantum_metrics.entropy:.4f}")
                
                # Risco
                risk_color = {
                    RiskLevel.LOW: "#10b981",
                    RiskLevel.MEDIUM: "#f59e0b",
                    RiskLevel.HIGH: "#ef4444"
                }.get(result.risk_assessment.risk_level, "#9ca3af")
                
                st.markdown(f"""
                <div style="margin-top: 0.5rem;">
                    <div style="font-size: 0.875rem; color: #9ca3af;">Risco</div>
                    <div style="color: {risk_color}; font-weight: bold; font-size: 1rem;">
                        {result.risk_assessment.risk_level.value}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Informações adicionais
            st.markdown('<div class="quantum-panel" style="margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown("#### 📊 Informações")
            st.markdown(f"**Símbolo:** {result.symbol}")
            st.markdown(f"**Regime de Mercado:** {result.market_regime.value}")
            st.markdown(f"**Horizonte:** {current_pred.time_horizon.value}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            # Gráfico da Função de Onda
            st.markdown('<div class="quantum-panel">', unsafe_allow_html=True)
            st.markdown("#### 📊 Função de Onda de Preço (Amplitude)")
            
            # Preparar dados da função de onda
            wave_data = []
            for i in range(min(50, len(current_pred.wavefunction_state.amplitude))):
                wave_data.append({
                    'idx': i,
                    'amplitude': current_pred.wavefunction_state.amplitude[i],
                    'phase': current_pred.wavefunction_state.phase[i]
                })
            
            wave_df = pd.DataFrame(wave_data)
            
            fig_wave = go.Figure()
            
            # Adicionar amplitude (área)
            fig_wave.add_trace(go.Scatter(
                x=wave_df['idx'],
                y=wave_df['amplitude'],
                fill='tozeroy',
                mode='lines',
                name='Amplitude',
                line=dict(color='#a855f7', width=2),
                fillcolor='rgba(168, 85, 247, 0.3)'
            ))
            
            # Adicionar fase (linha tracejada)
            fig_wave.add_trace(go.Scatter(
                x=wave_df['idx'],
                y=wave_df['phase'],
                mode='lines',
                name='Fase',
                line=dict(color='#3b82f6', width=1, dash='dash')
            ))
            
            fig_wave.update_layout(
                height=250,
                margin=dict(l=0, r=0, t=30, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#222222',
                    zeroline=False,
                    showticklabels=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#222222',
                    zeroline=False
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_wave, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Gráfico de Distribuição de Probabilidade
            st.markdown('<div class="quantum-panel" style="margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown("#### 📈 Distribuição de Probabilidade (Previsão)")
            
            # Preparar dados de probabilidade
            prob_data = []
            for i, prob in enumerate(current_pred.probability_distribution):
                prob_data.append({
                    'idx': i,
                    'probability': prob
                })
            
            prob_df = pd.DataFrame(prob_data)
            
            fig_prob = go.Figure()
            
            fig_prob.add_trace(go.Scatter(
                x=prob_df['idx'],
                y=prob_df['probability'],
                fill='tozeroy',
                mode='lines',
                name='Probabilidade',
                line=dict(color='#22c55e', width=2),
                fillcolor='rgba(34, 197, 94, 0.3)'
            ))
            
            fig_prob.update_layout(
                height=250,
                margin=dict(l=0, r=0, t=30, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#222222',
                    zeroline=False,
                    showticklabels=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#222222',
                    zeroline=False,
                    title='Densidade de Probabilidade'
                ),
                showlegend=False
            )
            
            st.plotly_chart(fig_prob, use_container_width=True)
            st.markdown('<div style="text-align: center; color: #9ca3af; font-size: 0.75rem; margin-top: 0.5rem;">Densidade de Probabilidade do Preço Futuro</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Fatores de Risco
            st.markdown('<div class="quantum-panel" style="margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Fatores de Risco")
            
            for factor in result.risk_assessment.factors:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="width: 6px; height: 6px; border-radius: 50%; background-color: #ef4444;"></div>
                    <span>{factor}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.warning("Dados insuficientes para análise")
else:
    st.info("Aguardando dados de mercado...")

# Atualização automática
if auto_refresh:
    time.sleep(refresh_interval)
    # Atualizar dados de mercado
    last_price = st.session_state.market_data[-1].price if st.session_state.market_data else 45000
    new_price = last_price * (1 + random.uniform(-0.01, 0.01))
    
    st.session_state.market_data.append(
        MarketDataPoint(
            timestamp=datetime.now(),
            price=new_price,
            volume=random.uniform(100, 1000)
        )
    )
    
    # Manter apenas os últimos 100 pontos
    if len(st.session_state.market_data) > 100:
        st.session_state.market_data = st.session_state.market_data[-100:]
    
    st.rerun()

# Rodapé com estatísticas
st.markdown("---")
col_stats1, col_stats2, col_stats3 = st.columns(3)

with col_stats1:
    st.metric("Preço Atual", f"${st.session_state.market_data[-1].price:,.2f}" if st.session_state.market_data else "$0.00")

with col_stats2:
    if len(st.session_state.market_data) > 1:
        change = ((st.session_state.market_data[-1].price - st.session_state.market_data[-2].price) / 
                 st.session_state.market_data[-2].price * 100)
        st.metric("Variação 24h", f"{change:.2f}%")

with col_stats3:
    st.metric("Análises Realizadas", len(st.session_state.analyzer.results_history))