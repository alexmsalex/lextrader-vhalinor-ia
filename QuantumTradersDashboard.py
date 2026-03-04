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
class TradeAction(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class TradingSignal:
    id: str
    symbol: str
    action: TradeAction
    confidence: float
    price_target: float
    stop_loss: float
    risk_level: RiskLevel
    quantity: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'action': self.action.value,
            'confidence': self.confidence,
            'price_target': self.price_target,
            'stop_loss': self.stop_loss,
            'risk_level': self.risk_level.value,
            'quantity': self.quantity,
            'timestamp': self.timestamp.strftime("%H:%M:%S")
        }

@dataclass
class ArbitrageOpportunity:
    id: str
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread: float
    spread_percentage: float
    confidence: float
    volume: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'buy_exchange': self.buy_exchange,
            'sell_exchange': self.sell_exchange,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'spread': self.spread,
            'spread_percentage': self.spread_percentage,
            'confidence': self.confidence,
            'volume': self.volume,
            'timestamp': self.timestamp.strftime("%H:%M:%S")
        }

@dataclass
class PortfolioAllocation:
    symbol: str
    value: float
    weight: float
    score: float
    allocation: float
    
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'value': self.value,
            'weight': self.weight,
            'score': self.score,
            'allocation': self.allocation
        }

# ==================== SERVIÇO DE TRADING QUÂNTICO ====================
class QuantumAlgorithmsTrader:
    def __init__(self):
        self.capital = 100000.0
        self.trading_signals: List[TradingSignal] = []
        self.arbitrage_opportunities: List[ArbitrageOpportunity] = []
        self.portfolio_allocations: List[PortfolioAllocation] = []
        self.risk_metrics = {
            'total_pnl': 0.0,
            'success_rate': 0.75,
            'sharpe_ratio': 2.1,
            'max_drawdown': -5.2,
            'volatility': 12.4,
            'win_rate': 62.3,
            'avg_profit': 245.7,
            'avg_loss': -123.4
        }
        self._initialize_data()
        self._running = False
        self._thread = None
    
    def _initialize_data(self):
        """Inicializa dados de exemplo"""
        # Sinais de trading
        symbols = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'ADA/USD', 'DOT/USD', 
                   'AVAX/USD', 'MATIC/USD', 'ATOM/USD', 'LINK/USD', 'UNI/USD']
        
        for i in range(8):
            symbol = random.choice(symbols)
            base_price = random.uniform(10, 50000)
            
            signal = TradingSignal(
                id=f"sig_{i:03d}",
                symbol=symbol,
                action=random.choice([TradeAction.BUY, TradeAction.SELL]),
                confidence=random.uniform(0.65, 0.95),
                price_target=base_price * (1 + random.uniform(0.02, 0.15)),
                stop_loss=base_price * (1 - random.uniform(0.02, 0.1)),
                risk_level=random.choice([RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]),
                quantity=random.randint(1, 100)
            )
            self.trading_signals.append(signal)
        
        # Oportunidades de arbitragem
        exchanges = ['Binance', 'Coinbase', 'Kraken', 'FTX', 'Huobi', 'KuCoin', 'Gate.io']
        
        for i in range(5):
            symbol = random.choice(symbols)
            buy_price = random.uniform(100, 50000)
            spread_pct = random.uniform(0.5, 3.0)
            sell_price = buy_price * (1 + spread_pct/100)
            
            arb = ArbitrageOpportunity(
                id=f"arb_{i:03d}",
                symbol=symbol,
                buy_exchange=random.choice(exchanges),
                sell_exchange=random.choice([e for e in exchanges if e != exchanges[0]]),
                buy_price=buy_price,
                sell_price=sell_price,
                spread=sell_price - buy_price,
                spread_percentage=spread_pct,
                confidence=random.uniform(0.7, 0.98),
                volume=random.uniform(1000, 50000)
            )
            self.arbitrage_opportunities.append(arb)
        
        # Alocações de portfólio
        portfolio_symbols = random.sample(symbols, 5)
        total_value = sum(random.uniform(10000, 50000) for _ in range(5))
        
        for i, symbol in enumerate(portfolio_symbols):
            value = random.uniform(10000, 50000)
            allocation = PortfolioAllocation(
                symbol=symbol,
                value=value,
                weight=value / total_value,
                score=random.uniform(0.6, 0.95),
                allocation=(value / total_value) * 100
            )
            self.portfolio_allocations.append(allocation)
    
    def initialize(self):
        """Inicializa o trader"""
        self._running = True
        self._thread = threading.Thread(target=self._run_trading_cycle, daemon=True)
        self._thread.start()
    
    def _run_trading_cycle(self):
        """Executa ciclo de trading em background"""
        while self._running:
            try:
                self.execute_trading_cycle()
                time.sleep(5)  # Ciclo a cada 5 segundos
            except Exception as e:
                st.error(f"Erro no ciclo de trading: {e}")
                time.sleep(1)
    
    def execute_trading_cycle(self):
        """Executa um ciclo completo de trading"""
        # Simular PnL
        pnl_change = random.uniform(-500, 1000)
        self.risk_metrics['total_pnl'] += pnl_change
        
        # Atualizar taxa de sucesso
        self.risk_metrics['success_rate'] += random.uniform(-0.02, 0.03)
        self.risk_metrics['success_rate'] = max(0.5, min(0.95, self.risk_metrics['success_rate']))
        
        # Atualizar capital
        self.capital += pnl_change
        
        # Rotacionar sinais (remover alguns, adicionar novos)
        if random.random() > 0.7 and self.trading_signals:
            self.trading_signals.pop(random.randint(0, len(self.trading_signals)-1))
        
        if random.random() > 0.6:
            symbols = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'ADA/USD', 'DOT/USD']
            base_price = random.uniform(10, 50000)
            
            new_signal = TradingSignal(
                id=f"sig_{datetime.now().strftime('%H%M%S')}",
                symbol=random.choice(symbols),
                action=random.choice([TradeAction.BUY, TradeAction.SELL]),
                confidence=random.uniform(0.65, 0.95),
                price_target=base_price * (1 + random.uniform(0.02, 0.15)),
                stop_loss=base_price * (1 - random.uniform(0.02, 0.1)),
                risk_level=random.choice([RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]),
                quantity=random.randint(1, 100)
            )
            self.trading_signals.append(new_signal)
        
        # Atualizar oportunidades de arbitragem
        if random.random() > 0.8 and self.arbitrage_opportunities:
            self.arbitrage_opportunities.pop(random.randint(0, len(self.arbitrage_opportunities)-1))
        
        if random.random() > 0.7:
            symbols = ['BTC/USD', 'ETH/USD', 'SOL/USD']
            exchanges = ['Binance', 'Coinbase', 'Kraken', 'FTX', 'Huobi']
            buy_price = random.uniform(100, 50000)
            spread_pct = random.uniform(0.5, 3.0)
            
            new_arb = ArbitrageOpportunity(
                id=f"arb_{datetime.now().strftime('%H%M%S')}",
                symbol=random.choice(symbols),
                buy_exchange=random.choice(exchanges),
                sell_exchange=random.choice([e for e in exchanges if e != exchanges[0]]),
                buy_price=buy_price,
                sell_price=buy_price * (1 + spread_pct/100),
                spread=buy_price * (spread_pct/100),
                spread_percentage=spread_pct,
                confidence=random.uniform(0.7, 0.98),
                volume=random.uniform(1000, 50000)
            )
            self.arbitrage_opportunities.append(new_arb)
        
        # Atualizar alocações de portfólio
        if random.random() > 0.6:
            for allocation in self.portfolio_allocations:
                allocation.value *= (1 + random.uniform(-0.05, 0.08))
                allocation.score += random.uniform(-0.05, 0.05)
                allocation.score = max(0.3, min(1.0, allocation.score))
    
    def stop(self):
        """Para o trader"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
    
    @property
    def riskMetrics(self):
        return self.risk_metrics
    
    @property
    def tradingSignals(self):
        return self.trading_signals
    
    @property
    def arbitrageOpportunities(self):
        return self.arbitrage_opportunities

# ==================== APLICAÇÃO STREAMLIT ====================
def main():
    st.set_page_config(
        page_title="Quantum Traders Dashboard",
        page_icon="⚡",
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
        .stats-card {
            background-color: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            transition: all 0.3s ease;
        }
        .stats-card:hover {
            border-color: rgba(6, 182, 212, 0.3);
            transform: translateY(-2px);
        }
        .signal-card {
            background-color: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 1rem;
            transition: all 0.3s ease;
        }
        .signal-card:hover {
            border-color: rgba(6, 182, 212, 0.5);
            transform: translateY(-2px);
        }
        .arbitrage-card {
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(234, 179, 8, 0.3);
            border-radius: 0.5rem;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }
        .arbitrage-card:hover {
            background-color: rgba(234, 179, 8, 0.1);
            border-color: rgba(234, 179, 8, 0.5);
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
        .risk-low {
            color: #10b981;
        }
        .risk-medium {
            color: #f59e0b;
        }
        .risk-high {
            color: #ef4444;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar trader
    if 'trader' not in st.session_state:
        st.session_state.trader = QuantumAlgorithmsTrader()
        st.session_state.trader.initialize()
    
    trader = st.session_state.trader
    metrics = trader.riskMetrics
    signals = trader.tradingSignals
    arbitrage = trader.arbitrageOpportunities
    capital = trader.capital
    
    # Header stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stats-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; font-weight: bold;">
                        Capital Total
                    </span>
                    <span style="color: #06b6d4; font-size: 1rem;">💰</span>
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: white;">
                    ${capital:,.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pnl = metrics['total_pnl']
        pnl_color = "#10b981" if pnl >= 0 else "#ef4444"
        pnl_icon = "📈" if pnl >= 0 else "📉"
        
        st.markdown(f"""
            <div class="stats-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; font-weight: bold;">
                        PnL Ciclo
                    </span>
                    <span style="color: {pnl_color}; font-size: 1rem;">{pnl_icon}</span>
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: {pnl_color};">
                    ${pnl:+.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        success_rate = metrics['success_rate'] * 100
        st.markdown(f"""
            <div class="stats-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; font-weight: bold;">
                        Taxa de Sucesso
                    </span>
                    <span style="color: #3b82f6; font-size: 1rem;">🛡️</span>
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: white;">
                    {success_rate:.1f}%
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stats-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; font-weight: bold;">
                        Oportunidades Arb.
                    </span>
                    <span style="color: #eab308; font-size: 1rem;">⚖️</span>
                </div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: white;">
                    {len(arbitrage)}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Conteúdo principal
    col1, col2 = st.columns(2)
    
    with col1:
        # Scanner de Arbitragem
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="color: #eab308; font-size: 1rem;">⚖️</span>
                <h3 style="color: #eab308; font-size: 0.9rem; font-weight: bold; margin: 0;">
                    SCANNER DE ARBITRAGEM QUÂNTICA
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if not arbitrage:
            st.info("Buscando divergências de preço...", icon="🔍")
        else:
            for arb in arbitrage:
                arb_dict = arb.to_dict()
                
                st.markdown(f"""
                    <div class="arbitrage-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 0.8rem; font-weight: bold; color: white;">
                                    {arb.symbol}
                                </div>
                                <div style="font-size: 0.6rem; color: #9ca3af; display: flex; gap: 0.25rem;">
                                    <span>{arb.buy_exchange}</span>
                                    <span style="color: #6b7280;">→</span>
                                    <span>{arb.sell_exchange}</span>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="color: #10b981; font-family: monospace; font-size: 0.9rem; font-weight: bold;">
                                    +{arb.spread_percentage:.2f}%
                                </div>
                                <div style="font-size: 0.6rem; color: #9ca3af;">
                                    Confiança: {(arb.confidence * 100):.0f}%
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Alocação de Portfólio
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="color: #3b82f6; font-size: 1rem;">💼</span>
                <h3 style="color: #3b82f6; font-size: 0.9rem; font-weight: bold; margin: 0;">
                    ALOCAÇÃO OTIMIZADA (Q-ANNEALING)
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Preparar dados para o gráfico
        if trader.portfolio_allocations:
            portfolio_data = []
            for allocation in trader.portfolio_allocations:
                portfolio_data.append({
                    'symbol': allocation.symbol,
                    'value': allocation.value,
                    'score': allocation.score,
                    'allocation': allocation.allocation
                })
            
            df = pd.DataFrame(portfolio_data)
            
            # Criar gráfico de barras
            fig = px.bar(
                df,
                y='symbol',
                x='value',
                orientation='h',
                color='score',
                color_continuous_scale='blues',
                hover_data=['allocation'],
                labels={'value': 'Valor ($)', 'symbol': 'Ativo', 'score': 'Score'}
            )
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                yaxis_title="",
                xaxis_title="",
                showlegend=False,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Gerando alocações de portfólio...", icon="⏳")
    
    st.divider()
    
    # Sinais de Trading Ativos
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <span style="color: #06b6d4; font-size: 1rem;">🎯</span>
            <h3 style="color: #06b6d4; font-size: 0.9rem; font-weight: bold; margin: 0;">
                SINAIS DE TRADING ATIVOS
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if not signals:
        st.info("Aguardando sinais de trading...", icon="📊")
    else:
        # Criar colunas responsivas
        cols_per_row = 3
        num_signals = len(signals)
        num_rows = (num_signals + cols_per_row - 1) // cols_per_row
        
        for row in range(num_rows):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                signal_idx = row * cols_per_row + col_idx
                if signal_idx < num_signals:
                    sig = signals[signal_idx]
                    sig_dict = sig.to_dict()
                    
                    with cols[col_idx]:
                        action_class = "buy-badge" if sig.action == TradeAction.BUY else "sell-badge"
                        risk_class = f"risk-{sig.risk_level.value.lower()}"
                        
                        st.markdown(f"""
                            <div class="signal-card">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                                    <div>
                                        <div style="font-size: 0.9rem; font-weight: bold; color: white;">
                                            {sig.symbol}
                                        </div>
                                        <div class="{action_class}" style="margin-top: 0.25rem;">
                                            {sig.action.value}
                                        </div>
                                    </div>
                                    <div style="text-align: right;">
                                        <div style="font-family: monospace; font-size: 1.2rem; font-weight: bold; color: white;">
                                            {(sig.confidence * 100):.0f}%
                                        </div>
                                        <div style="font-size: 0.6rem; color: #9ca3af; text-transform: uppercase;">
                                            Score Quântico
                                        </div>
                                    </div>
                                </div>
                                
                                <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(55, 65, 81, 0.5); font-size: 0.7rem;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                        <span style="color: #9ca3af;">Alvo</span>
                                        <span style="color: #10b981; font-family: monospace;">${sig.price_target:.2f}</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                        <span style="color: #9ca3af;">Stop</span>
                                        <span style="color: #ef4444; font-family: monospace;">${sig.stop_loss:.2f}</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                                        <span style="color: #9ca3af;">Risco</span>
                                        <span class="{risk_class}" style="font-weight: bold;">
                                            {sig.risk_level.value}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
    
    # Atualizar periodicamente
    time.sleep(0.1)
    st.rerun()

if __name__ == "__main__":
    main()