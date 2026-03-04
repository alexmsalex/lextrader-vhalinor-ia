import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import random
from datetime import datetime, timedelta
import time
from enum import Enum
import threading

# ==================== ENUMS E CLASSES ====================
class CircuitType(Enum):
    MARKET_SIMULATION = "MARKET_SIMULATION"
    PRICE_PREDICTION = "PRICE_PREDICTION"
    RISK_ANALYSIS = "RISK_ANALYSIS"

class TradeAction(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

@dataclass
class QuantumSimResult:
    id: str
    circuit_type: CircuitType
    execution_time: float
    qubits_used: int
    quantum_advantage: float
    confidence: float
    output_data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'circuit_type': self.circuit_type.value,
            'execution_time': self.execution_time,
            'qubits_used': self.qubits_used,
            'quantum_advantage': self.quantum_advantage,
            'confidence': self.confidence,
            'output_data': self.output_data,
            'timestamp': self.timestamp.strftime("%H:%M:%S")
        }

@dataclass
class QuantumSimOpportunity:
    symbol: str
    current_price: float
    predicted_price: float
    discrepancy: float  # diferença percentual
    action: TradeAction
    risk_level: str  # LOW, MEDIUM, HIGH
    quantum_certainty: float
    detected_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'current_price': self.current_price,
            'predicted_price': self.predicted_price,
            'discrepancy': self.discrepancy,
            'action': self.action.value,
            'risk_level': self.risk_level,
            'quantum_certainty': self.quantum_certainty,
            'detected_at': self.detected_at.strftime("%H:%M:%S")
        }

@dataclass
class SimulatorStatus:
    total_executions: int
    system_fidelity: float
    active_qubits: int
    quantum_advantage: float
    last_update: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'total_executions': self.total_executions,
            'system_fidelity': self.system_fidelity,
            'active_qubits': self.active_qubits,
            'quantum_advantage': self.quantum_advantage,
            'last_update': self.last_update.strftime("%H:%M:%S")
        }

# ==================== SIMULADOR DE MERCADO QUÂNTICO ====================
class QuantumMarketSimulator:
    def __init__(self):
        self.results_history: List[QuantumSimResult] = []
        self.opportunities: List[QuantumSimOpportunity] = []
        self.status = SimulatorStatus(
            total_executions=0,
            system_fidelity=0.95,
            active_qubits=32,
            quantum_advantage=3.7
        )
        self._is_simulating = False
        self._initialize_history()
    
    def _initialize_history(self):
        """Inicializa histórico de simulações"""
        base_time = datetime.now() - timedelta(minutes=30)
        
        for i in range(8):
            result = QuantumSimResult(
                id=f"sim_{i:03d}",
                circuit_type=random.choice(list(CircuitType)),
                execution_time=random.uniform(0.001, 0.005),
                qubits_used=random.randint(16, 32),
                quantum_advantage=random.uniform(2.5, 4.5),
                confidence=random.uniform(0.7, 0.95),
                output_data={
                    'market_outlook': random.choice(['BULLISH', 'BEARISH', 'NEUTRAL', 'VOLATILE']),
                    'price': {
                        'distribution': [random.random() for _ in range(20)]
                    }
                }
            )
            self.results_history.append(result)
        
        # Inicializar status
        self.status.total_executions = len(self.results_history)
    
    def get_status(self) -> SimulatorStatus:
        """Retorna status atual do simulador"""
        # Atualizar status dinamicamente
        self.status.last_update = datetime.now()
        self.status.system_fidelity += random.uniform(-0.001, 0.001)
        self.status.system_fidelity = max(0.9, min(0.99, self.status.system_fidelity))
        self.status.quantum_advantage += random.uniform(-0.05, 0.05)
        self.status.quantum_advantage = max(2.0, min(5.0, self.status.quantum_advantage))
        
        return self.status
    
    async def analyze_market_quantum(self, market_data: Dict[str, float]) -> QuantumSimResult:
        """Analisa mercado usando simulação quântica"""
        self._is_simulating = True
        
        # Simular processamento quântico
        time.sleep(0.5)  # Simular latência
        
        current_price = market_data.get('current_price', 45000)
        volatility = market_data.get('volatility', 0.02)
        
        # Gerar distribuição de probabilidade
        distribution = []
        for i in range(20):
            # Distribuição normal centrada no preço atual
            base = np.exp(-((i - 10) ** 2) / (2 * volatility * 100))
            noise = random.uniform(-0.1, 0.1)
            distribution.append(max(0, base + noise))
        
        # Normalizar distribuição
        total = sum(distribution)
        if total > 0:
            distribution = [d/total for d in distribution]
        
        # Criar resultado
        result = QuantumSimResult(
            id=f"sim_{datetime.now().strftime('%H%M%S')}",
            circuit_type=CircuitType.MARKET_SIMULATION,
            execution_time=random.uniform(0.001, 0.005),
            qubits_used=random.randint(24, 32),
            quantum_advantage=random.uniform(3.0, 4.5),
            confidence=0.8 + random.random() * 0.15,
            output_data={
                'market_outlook': random.choice(['BULLISH', 'BEARISH', 'NEUTRAL', 'VOLATILE']),
                'price': {
                    'distribution': distribution,
                    'current': current_price,
                    'predicted': current_price * (1 + random.uniform(-0.05, 0.05))
                }
            }
        )
        
        self.results_history.append(result)
        self.status.total_executions += 1
        
        # Manter apenas últimos 20 resultados
        if len(self.results_history) > 20:
            self.results_history = self.results_history[-20:]
        
        self._is_simulating = False
        return result
    
    async def detect_arbitrage_opportunities(self, market_data: Dict[str, float]) -> List[QuantumSimOpportunity]:
        """Detecta oportunidades de arbitragem usando simulação quântica"""
        symbols = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'ADA/USD', 'DOT/USD', 
                  'AVAX/USD', 'MATIC/USD', 'ATOM/USD', 'LINK/USD']
        
        opportunities = []
        
        for symbol in symbols[:5]:  # Limitar a 5 símbolos
            current_price = 45000 + random.uniform(-5000, 5000)
            predicted_price = current_price * (1 + random.uniform(-0.08, 0.08))
            discrepancy = abs(predicted_price - current_price) / current_price
            
            # Determinar ação baseada na discrepância
            if predicted_price > current_price:
                action = TradeAction.BUY
            else:
                action = TradeAction.SELL
            
            # Determinar nível de risco
            if discrepancy > 0.05:
                risk_level = 'HIGH'
            elif discrepancy > 0.02:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            opportunity = QuantumSimOpportunity(
                symbol=symbol,
                current_price=current_price,
                predicted_price=predicted_price,
                discrepancy=discrepancy,
                action=action,
                risk_level=risk_level,
                quantum_certainty=0.7 + random.random() * 0.25
            )
            
            opportunities.append(opportunity)
        
        # Ordenar por discrepância (maiores primeiro)
        opportunities.sort(key=lambda x: x.discrepancy, reverse=True)
        
        self.opportunities = opportunities
        return opportunities
    
    async def predict_price_quantum(self, symbol: str, price_history: List[float]) -> QuantumSimResult:
        """Prediz preços usando simulação quântica"""
        self._is_simulating = True
        time.sleep(0.3)  # Simular processamento
        
        # Gerar distribuição preditiva
        distribution = []
        for i in range(20):
            base = np.sin(i/3) * 0.5 + 0.5
            noise = random.uniform(-0.2, 0.2)
            distribution.append(max(0, base + noise))
        
        # Normalizar
        total = sum(distribution)
        if total > 0:
            distribution = [d/total for d in distribution]
        
        result = QuantumSimResult(
            id=f"pred_{datetime.now().strftime('%H%M%S')}",
            circuit_type=CircuitType.PRICE_PREDICTION,
            execution_time=random.uniform(0.002, 0.006),
            qubits_used=random.randint(20, 28),
            quantum_advantage=random.uniform(3.2, 4.8),
            confidence=0.75 + random.random() * 0.2,
            output_data={
                'symbol': symbol,
                'price': {
                    'distribution': distribution,
                    'current': price_history[-1] if price_history else 45000,
                    'predicted_range': {
                        'min': (price_history[-1] if price_history else 45000) * 0.95,
                        'max': (price_history[-1] if price_history else 45000) * 1.05
                    }
                }
            }
        )
        
        self.results_history.append(result)
        self.status.total_executions += 1
        
        self._is_simulating = False
        return result
    
    @property
    def is_simulating(self) -> bool:
        return self._is_simulating

# ==================== APLICAÇÃO STREAMLIT ====================
def main():
    st.set_page_config(
        page_title="Simulador Quântico",
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
            border: 1px solid rgba(79, 70, 229, 0.5);
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
        .opportunity-card {
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }
        .opportunity-card:hover {
            border-color: rgba(79, 70, 229, 0.3);
            transform: translateY(-2px);
        }
        .sim-button {
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: bold;
            font-size: 0.8rem;
            border: 1px solid;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .sim-active {
            background-color: rgba(79, 70, 229, 0.1);
            border-color: #4f46e5;
            color: #4f46e5;
        }
        .sim-inactive {
            background-color: rgba(79, 70, 229, 0.3);
            border-color: #4f46e5;
            color: #4f46e5;
        }
        .sim-disabled {
            background-color: rgba(79, 70, 229, 0.1);
            border-color: #4f46e5;
            color: #4f46e5;
            opacity: 0.5;
            cursor: not-allowed;
        }
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .spin {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .buy-badge {
            background-color: rgba(34, 197, 94, 0.2);
            border: 1px solid rgba(34, 197, 94, 0.5);
            color: #10b981;
            padding: 0.1rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.7rem;
            font-weight: bold;
        }
        .sell-badge {
            background-color: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.5);
            color: #ef4444;
            padding: 0.1rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.7rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar simulador
    if 'simulator' not in st.session_state:
        st.session_state.simulator = QuantumMarketSimulator()
    
    if 'selected_circuit' not in st.session_state:
        st.session_state.selected_circuit = 'MARKET_SIMULATION'
    
    if 'is_simulating' not in st.session_state:
        st.session_state.is_simulating = False
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    simulator = st.session_state.simulator
    status = simulator.get_status()
    results = simulator.results_history
    opportunities = simulator.opportunities
    is_simulating = simulator.is_simulating
    
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
            <div class="header-card">
                <div style="padding: 0.5rem; background-color: rgba(79, 70, 229, 0.2); 
                         border-radius: 0.5rem; border: 1px solid rgba(79, 70, 229, 0.5);">
                    <span style="color: #4f46e5; font-size: 1.5rem;" class="pulse">⚛️</span>
                </div>
                <div>
                    <h1 style="color: white; margin: 0; font-size: 1.5rem;">SIMULADOR DE MERCADO QUÂNTICO</h1>
                    <p style="color: #4f46e5; font-family: monospace; font-size: 0.8rem; margin: 0;">
                        {status.total_executions} EXECUÇÕES • FIDELIDADE {(status.system_fidelity * 100):.1f}%
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Seletor de circuito
        circuit_options = {
            'MARKET_SIMULATION': 'SIMULAÇÃO DE MERCADO',
            'PRICE_PREDICTION': 'PREDIÇÃO DE PREÇO',
            'RISK_ANALYSIS': 'ANÁLISE DE RISCO'
        }
        
        selected_circuit = st.selectbox(
            "Selecionar Circuito",
            options=list(circuit_options.keys()),
            format_func=lambda x: circuit_options[x],
            key="circuit_select",
            label_visibility="collapsed"
        )
        
        # Botão de execução
        button_text = "SIMULANDO..." if is_simulating else "EXECUTAR CIRCUITO"
        button_icon = "⚡" if is_simulating else "▶️"
        button_class = "sim-disabled" if is_simulating else "sim-inactive"
        
        if st.button(f"{button_icon} {button_text}", 
                    key="run_simulation",
                    disabled=is_simulating,
                    use_container_width=True):
            st.session_state.is_simulating = True
            st.session_state.selected_circuit = selected_circuit
            st.rerun()
    
    st.divider()
    
    # Conteúdo principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Painel de métricas
        st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <h3 style="color: #9ca3af; font-size: 0.8rem; font-weight: bold; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #4f46e5;">⚡</span> RESULTADOS DA EXECUÇÃO
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if results:
            latest_result = results[-1]
            result_dict = latest_result.to_dict()
            
            # Grid de métricas
            col_met1, col_met2 = st.columns(2)
            
            with col_met1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Tempo Exec.</div>
                        <div style="font-family: monospace; font-size: 1rem; color: white;">
                            {latest_result.execution_time:.4f}s
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Vantagem</div>
                        <div style="font-family: monospace; font-size: 1rem; color: #10b981;">
                            {latest_result.quantum_advantage:.1f}x
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_met2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Qubits</div>
                        <div style="font-family: monospace; font-size: 1rem; color: white;">
                            {latest_result.qubits_used}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #9ca3af;">Confiança</div>
                        <div style="font-family: monospace; font-size: 1rem; color: #4f46e5;">
                            {(latest_result.confidence * 100):.1f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Outlook do mercado
            outlook = latest_result.output_data.get('market_outlook', 'N/A')
            st.markdown(f"""
                <div style="margin-top: 0.5rem; font-size: 0.7rem; color: #9ca3af; padding-top: 0.5rem; border-top: 1px solid rgba(55, 65, 81, 0.5);">
                    OUTLOOK: <span style="color: white; font-weight: bold;">{outlook}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma simulação recente.", icon="ℹ️")
        
        # Gráfico de superposição de preços
        st.markdown("""
            <div style="margin-top: 1rem; margin-bottom: 0.5rem;">
                <h3 style="color: #9ca3af; font-size: 0.8rem; font-weight: bold; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #4f46e5;">📊</span> SUPERPOSIÇÃO DE PREÇOS
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if results:
            latest_result = results[-1]
            distribution = latest_result.output_data.get('price', {}).get('distribution', [])
            
            if distribution:
                # Criar dataframe para o gráfico
                prob_data = []
                for i, val in enumerate(distribution):
                    prob_data.append({
                        'idx': i,
                        'value': val
                    })
                
                df = pd.DataFrame(prob_data)
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df['idx'],
                    y=df['value'],
                    mode='lines',
                    fill='tozeroy',
                    fillcolor='rgba(99, 102, 241, 0.3)',
                    line=dict(color='#6366f1', width=2),
                    name='Probabilidade'
                ))
                
                fig.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=200,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=False, showticklabels=False),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Sem dados de distribuição", icon="📈")
        else:
            st.info("Aguardando simulação...", icon="⏳")
    
    with col2:
        # Painel de oportunidades
        st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <h3 style="color: #9ca3af; font-size: 0.8rem; font-weight: bold; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #4f46e5;">🌐</span> OPORTUNIDADES DETECTADAS (QUANTUM SCAN)
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if not opportunities:
            st.markdown("""
                <div style="text-align: center; color: #6b7280; padding: 3rem; border: 2px dashed #4b5563; border-radius: 0.5rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.2;">⚛️</div>
                    Aguardando varredura quântica...
                </div>
            """, unsafe_allow_html=True)
        else:
            for opp in opportunities:
                opp_dict = opp.to_dict()
                badge_class = "buy-badge" if opp.action == TradeAction.BUY else "sell-badge"
                badge_text = "BUY" if opp.action == TradeAction.BUY else "SELL"
                
                st.markdown(f"""
                    <div class="opportunity-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                                    <span style="font-size: 0.9rem; font-weight: bold; color: white;">
                                        {opp.symbol}
                                    </span>
                                    <span class="{badge_class}">
                                        {badge_text}
                                    </span>
                                </div>
                                <div style="font-size: 0.7rem; color: #9ca3af; display: flex; gap: 0.75rem;">
                                    <span>Atual: ${opp.current_price:.2f}</span>
                                    <span>
                                        Previsto: <span style="color: #a5b4fc;">${opp.predicted_price:.2f}</span>
                                    </span>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-family: monospace; font-size: 0.9rem; font-weight: bold; color: white;">
                                    {(opp.discrepancy * 100):.2f}% Diff
                                </div>
                                <div style="font-size: 0.65rem; color: #9ca3af; display: flex; align-items: center; justify-content: flex-end; gap: 0.25rem;">
                                    {'⚠️' if opp.risk_level == 'HIGH' else ''}
                                    Certeza: {(opp.quantum_certainty * 100):.1f}%
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    # Executar simulação se solicitado
    if st.session_state.is_simulating:
        import asyncio
        
        # Criar dados de mercado simulados
        mock_data = {
            'current_price': 45000 + (random.random() * 1000),
            'volatility': 0.02 + (random.random() * 0.01)
        }
        
        if st.session_state.selected_circuit == 'MARKET_SIMULATION':
            # Executar simulação assíncrona
            result = asyncio.run(simulator.analyze_market_quantum(mock_data))
            opportunities = asyncio.run(simulator.detect_arbitrage_opportunities(mock_data))
        elif st.session_state.selected_circuit == 'PRICE_PREDICTION':
            # Gerar histórico falso
            history = [45000 + np.sin(i/10)*1000 + random.random()*500 for i in range(100)]
            result = asyncio.run(simulator.predict_price_quantum('BTC/USD', history))
        
        st.session_state.is_simulating = False
        st.rerun()
    
    # Atualizar periodicamente
    now = datetime.now()
    if (now - st.session_state.last_update).total_seconds() > 1:  # Atualizar a cada 1s
        st.session_state.last_update = now
        st.rerun()

if __name__ == "__main__":
    main()