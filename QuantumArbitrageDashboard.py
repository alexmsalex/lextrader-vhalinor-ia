import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import threading

# ==================== ENUMS E CLASSES ====================
class ArbType(Enum):
    QUANTUM = "quantum"
    SPATIAL = "spatial"
    TEMPORAL = "temporal"

class ArbStatus(Enum):
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"

class ArbRiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class ArbitrageOpportunity:
    id: str
    symbol: str
    exchange_buy: str
    exchange_sell: str
    price_buy: float
    price_sell: float
    spread: float
    spread_percentage: float
    confidence: float
    score: float
    type: ArbType
    risk: ArbRiskLevel
    volume: float
    created_at: datetime = field(default_factory=datetime.now)
    expiry: datetime = None
    
    def __post_init__(self):
        if self.expiry is None:
            self.expiry = self.created_at + timedelta(seconds=30)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'exchange_buy': self.exchange_buy,
            'exchange_sell': self.exchange_sell,
            'price_buy': self.price_buy,
            'price_sell': self.price_sell,
            'spread': self.spread,
            'spread_percentage': self.spread_percentage,
            'confidence': self.confidence,
            'score': self.score,
            'type': self.type.value,
            'risk': self.risk.value,
            'volume': self.volume,
            'created_at': self.created_at.strftime("%H:%M:%S"),
            'expiry': self.expiry.strftime("%H:%M:%S") if self.expiry else None
        }

@dataclass
class ExecutionResult:
    opportunity_id: str
    symbol: str
    status: ArbStatus
    executed: bool
    net_profit: float
    execution_time: float
    fee: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'opportunity_id': self.opportunity_id,
            'symbol': self.symbol,
            'status': self.status.value,
            'executed': self.executed,
            'net_profit': self.net_profit,
            'execution_time': self.execution_time,
            'fee': self.fee,
            'timestamp': self.timestamp.strftime("%H:%M:%S.%f")[:-3]
        }

# ==================== SERVIÇO DE ARBITRAGEM ====================
class QuantumArbitrageService:
    def __init__(self):
        self.history: List[ExecutionResult] = []
        self.opportunities: List[ArbitrageOpportunity] = []
        self.total_profit = 0.0
        self.scanning = False
        self._initialize_history()
    
    def _initialize_history(self):
        """Inicializa com histórico de exemplo"""
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT']
        exchanges = ['Binance', 'Coinbase', 'Kraken', 'FTX', 'Huobi']
        
        for i in range(15):
            self.history.append(
                ExecutionResult(
                    opportunity_id=f"arb-{i+1:03d}",
                    symbol=random.choice(symbols),
                    status=ArbStatus.EXECUTED if random.random() > 0.3 else ArbStatus.FAILED,
                    executed=random.random() > 0.3,
                    net_profit=random.uniform(-50, 200),
                    execution_time=random.uniform(0.1, 2.5),
                    fee=random.uniform(0.1, 2.0)
                )
            )
        
        # Calcular lucro total
        self.total_profit = sum(h.net_profit for h in self.history)
    
    def scan_opportunities(self) -> List[ArbitrageOpportunity]:
        """Varre oportunidades de arbitragem"""
        self.scanning = True
        
        # Simular varredura
        time.sleep(0.5)
        
        # Remover oportunidades expiradas
        now = datetime.now()
        self.opportunities = [op for op in self.opportunities if op.expiry > now]
        
        # Gerar novas oportunidades (aleatórias)
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT', 
                   'AVAX/USDT', 'MATIC/USDT', 'ATOM/USDT', 'LINK/USDT']
        exchanges = ['Binance', 'Coinbase', 'Kraken', 'FTX', 'Huobi', 'KuCoin', 'Gate.io']
        
        new_ops = []
        for _ in range(random.randint(0, 8)):
            symbol = random.choice(symbols)
            price_buy = random.uniform(100, 50000)
            spread_pct = random.uniform(0.1, 5.0)  # 0.1% a 5%
            price_sell = price_buy * (1 + spread_pct/100)
            
            op = ArbitrageOpportunity(
                id=f"arb-{datetime.now().strftime('%H%M%S')}-{random.randint(100, 999)}",
                symbol=symbol,
                exchange_buy=random.choice(exchanges),
                exchange_sell=random.choice([e for e in exchanges if e != 'Binance']),
                price_buy=price_buy,
                price_sell=price_sell,
                spread=price_sell - price_buy,
                spread_percentage=spread_pct,
                confidence=random.uniform(0.7, 0.99),
                score=random.uniform(20, 95),
                type=random.choice([ArbType.QUANTUM, ArbType.SPATIAL, ArbType.TEMPORAL]),
                risk=random.choice([ArbRiskLevel.LOW, ArbRiskLevel.MEDIUM, ArbRiskLevel.HIGH]),
                volume=random.uniform(1000, 50000)
            )
            new_ops.append(op)
        
        self.opportunities.extend(new_ops)
        
        # Ordenar por score (melhores primeiro)
        self.opportunities.sort(key=lambda x: x.score, reverse=True)
        
        self.scanning = False
        return self.opportunities
    
    def execute_arbitrage(self, opportunity: ArbitrageOpportunity) -> ExecutionResult:
        """Executa oportunidade de arbitragem"""
        # Simular execução
        time.sleep(0.3)
        
        # Chance de sucesso baseada no score
        success_probability = min(0.95, opportunity.score / 100)
        executed = random.random() < success_probability
        
        # Calcular lucro
        if executed:
            # Lucro positivo com variação baseada no score
            base_profit = opportunity.spread * opportunity.volume / 1000
            profit_variation = random.uniform(-0.2, 0.3) * base_profit
            net_profit = base_profit + profit_variation
            fee = random.uniform(0.1, 1.0) * base_profit / 100
            net_profit -= fee
            status = ArbStatus.EXECUTED
        else:
            # Falha resulta em pequena perda
            net_profit = -random.uniform(10, 100)
            fee = random.uniform(5, 20)
            status = ArbStatus.FAILED
        
        result = ExecutionResult(
            opportunity_id=opportunity.id,
            symbol=opportunity.symbol,
            status=status,
            executed=executed,
            net_profit=net_profit,
            execution_time=random.uniform(0.15, 1.8),
            fee=fee
        )
        
        self.history.append(result)
        self.total_profit += net_profit
        
        # Remover oportunidade executada
        self.opportunities = [op for op in self.opportunities if op.id != opportunity.id]
        
        return result
    
    def get_history(self, limit: int = 50) -> List[ExecutionResult]:
        """Retorna histórico de execuções"""
        return sorted(self.history, key=lambda x: x.timestamp, reverse=True)[:limit]

# ==================== APLICAÇÃO STREAMLIT ====================
def main():
    st.set_page_config(
        page_title="Arbitragem Quântica",
        page_icon="⚖️",
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
            border: 1px solid rgba(120, 53, 15, 0.5);
            border-radius: 0.5rem;
            padding: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .opportunity-card {
            background-color: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }
        .opportunity-card:hover {
            border-color: rgba(234, 179, 8, 0.5);
            transform: translateY(-2px);
        }
        .execution-log {
            background-color: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(55, 65, 81, 0.5);
            border-radius: 0.5rem;
            padding: 0.5rem;
            font-family: monospace;
            font-size: 0.7rem;
            max-height: 400px;
            overflow-y: auto;
        }
        .profit-positive {
            color: #10b981;
            font-weight: bold;
        }
        .profit-negative {
            color: #ef4444;
            font-weight: bold;
        }
        .type-badge {
            font-size: 0.6rem;
            padding: 0.1rem 0.4rem;
            border-radius: 0.25rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        .type-quantum {
            background-color: rgba(168, 85, 247, 0.2);
            border: 1px solid rgba(168, 85, 247, 0.5);
            color: #a855f7;
        }
        .type-spatial {
            background-color: rgba(59, 130, 246, 0.2);
            border: 1px solid rgba(59, 130, 246, 0.5);
            color: #3b82f6;
        }
        .type-temporal {
            background-color: rgba(75, 85, 99, 0.2);
            border: 1px solid rgba(75, 85, 99, 0.5);
            color: #9ca3af;
        }
        .auto-exec-button {
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: bold;
            font-size: 0.8rem;
            border: 1px solid;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .auto-exec-on {
            background-color: rgba(34, 197, 94, 0.1);
            border-color: #10b981;
            color: #10b981;
            animation: pulse 2s infinite;
        }
        .auto-exec-off {
            background-color: rgba(55, 65, 81, 0.5);
            border-color: #4b5563;
            color: #9ca3af;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .execute-button {
            padding: 0.25rem;
            border-radius: 0.25rem;
            background-color: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.5);
            color: #10b981;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .opportunity-card:hover .execute-button {
            opacity: 1;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar serviço
    if 'arbitrage_service' not in st.session_state:
        st.session_state.arbitrage_service = QuantumArbitrageService()
    
    if 'auto_execute' not in st.session_state:
        st.session_state.auto_execute = False
    
    if 'last_scan' not in st.session_state:
        st.session_state.last_scan = datetime.now() - timedelta(seconds=10)
    
    if 'scanning' not in st.session_state:
        st.session_state.scanning = False
    
    service = st.session_state.arbitrage_service
    opportunities = service.opportunities
    history = service.get_history(20)
    total_profit = service.total_profit
    
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
            <div class="header-card">
                <div style="padding: 0.5rem; background-color: rgba(120, 53, 15, 0.2); 
                         border-radius: 0.5rem; border: 1px solid rgba(234, 179, 8, 0.5);">
                    <span style="color: #eab308; font-size: 1.5rem;">⚖️</span>
                </div>
                <div>
                    <h1 style="color: white; margin: 0; font-size: 1.5rem;">ARBITRAGEM QUÂNTICA</h1>
                    <p style="color: #eab308; font-family: monospace; font-size: 0.8rem; margin: 0;">
                        MULTI-LEG • TEMPORAL • SPATIAL
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="text-align: right; margin-bottom: 0.5rem;">
                <div style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase;">Lucro Líquido</div>
                <div style="font-family: monospace; font-size: 1.5rem; font-weight: bold; 
                          color: {'#10b981' if total_profit >= 0 else '#ef4444'};">
                    ${total_profit:,.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botão de auto-execução
        if st.button(
            f"⚡ {'AUTO-EXECUÇÃO: ON' if st.session_state.auto_execute else 'AUTO-EXECUÇÃO: OFF'}",
            key="auto_execute_toggle",
            type="primary" if st.session_state.auto_execute else "secondary",
            use_container_width=True
        ):
            st.session_state.auto_execute = not st.session_state.auto_execute
            st.rerun()
    
    st.divider()
    
    # Conteúdo principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Lista de oportunidades
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1rem;">📊</span>
                <h3 style="color: #9ca3af; font-size: 0.9rem; font-weight: bold; margin: 0;">
                    OPORTUNIDADES DETECTADAS ({len(opportunities)})
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if opportunities:
            for op in opportunities:
                op_dict = op.to_dict()
                type_class = f"type-{op.type.value}"
                
                st.markdown(f"""
                    <div class="opportunity-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                                    <span style="font-size: 0.9rem; font-weight: bold; color: white;">
                                        {op.symbol}
                                    </span>
                                    <span class="type-badge {type_class}">
                                        {op.type.value}
                                    </span>
                                </div>
                                <div style="font-size: 0.7rem; color: #9ca3af; font-family: monospace;">
                                    {op.exchange_buy} 
                                    <span style="color: #eab308;">→</span>
                                    {op.exchange_sell}
                                </div>
                            </div>
                            
                            <div style="text-align: right; display: flex; align-items: center; gap: 1rem;">
                                <div>
                                    <div class="profit-positive">
                                        +{op.spread_percentage:.3f}%
                                    </div>
                                    <div style="font-size: 0.6rem; color: #6b7280;">
                                        Spread ${op.spread:.2f}
                                    </div>
                                </div>
                                <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                                       value: 'execute_{op.id}'}}, '*')"
                                       class="execute-button">
                                    <span style="font-size: 0.8rem;">▶</span>
                                </button>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: center; color: #6b7280; padding: 2rem; border: 2px dashed #4b5563; border-radius: 0.5rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.2;">🔄</div>
                    Varrendo mercados...
                </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de dispersão
        st.markdown("""
            <div style="margin-top: 1rem;">
                <h4 style="color: #6b7280; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; 
                          margin-bottom: 0.5rem;">
                    Mapa de Dispersão (Spread vs Confiança)
                </h4>
            </div>
        """, unsafe_allow_html=True)
        
        if opportunities:
            # Preparar dados para o gráfico
            chart_data = []
            for op in opportunities:
                chart_data.append({
                    'x': op.confidence * 100,  # Confiança
                    'y': op.spread_percentage,  # Spread %
                    'score': op.score,
                    'type': op.type.value,
                    'symbol': op.symbol
                })
            
            df = pd.DataFrame(chart_data)
            
            # Criar gráfico de dispersão
            fig = px.scatter(
                df,
                x='x',
                y='y',
                size='score',
                color='type',
                hover_data=['symbol', 'score'],
                color_discrete_map={
                    'quantum': '#a855f7',
                    'spatial': '#eab308',
                    'temporal': '#6b7280'
                },
                size_max=20
            )
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Confiança (%)",
                yaxis_title="Spread (%)",
                legend_title="Tipo",
                xaxis_range=[50, 100],
                showlegend=True
            )
            
            # Adicionar linha de referência
            fig.add_hline(y=0, line_dash="dash", line_color="#333", opacity=0.5)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aguardando oportunidades para exibir gráfico...")
    
    with col2:
        # Registro de execução
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1rem;">⏱️</span>
                <h3 style="color: #9ca3af; font-size: 0.9rem; font-weight: bold; margin: 0;">
                    REGISTRO DE EXECUÇÃO
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="execution-log">', unsafe_allow_html=True)
        
        if history:
            for res in history:
                res_dict = res.to_dict()
                status_color = "#10b981" if res.executed else "#ef4444"
                profit_color = "#10b981" if res.net_profit > 0 else "#9ca3af"
                
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; 
                              padding: 0.25rem 0; border-bottom: 1px solid rgba(55, 65, 81, 0.5); 
                              font-size: 0.7rem;">
                        <div>
                            <span style="color: {status_color}; font-weight: bold;">[{res.status.value}]</span>
                            <span style="color: #6b7280; margin-left: 0.5rem;">
                                {res.opportunity_id.split('-')[1]}
                            </span>
                        </div>
                        <div style="color: {profit_color}; font-family: monospace;">
                            ${res.net_profit:+.2f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: center; color: #6b7280; padding: 1rem;">
                    Nenhuma execução registrada
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Vantagem Quântica Média
        st.markdown("""
            <div style="margin-top: 1rem; background-color: rgba(17, 24, 39, 0.7); 
                      border: 1px solid rgba(55, 65, 81, 0.5); border-radius: 0.5rem; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; margin-bottom: 0.5rem;">
                    Vantagem Quântica Média
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.2rem; color: #3b82f6;">🌐</span>
                    <span style="font-family: monospace; font-size: 1.5rem; font-weight: bold; color: white;">
                        12.4%
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # JavaScript para comunicação
    st.markdown("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:setComponentValue') {
                Streamlit.setComponentValue(event.data.value);
            }
        });
        </script>
    """, unsafe_allow_html=True)
    
    # Capturar eventos
    if st.button("", key="event_capture", label_visibility="collapsed"):
        event = st.session_state.get('js_event', '')
        if event and event.startswith('execute_'):
            op_id = event.replace('execute_', '')
            opportunity = next((op for op in opportunities if op.id == op_id), None)
            if opportunity:
                service.execute_arbitrage(opportunity)
                st.success(f"Executando arbitragem: {opportunity.symbol}")
                st.rerun()
    
    # Auto-varredura
    now = datetime.now()
    if (now - st.session_state.last_scan).seconds >= 3:  # Varre a cada 3 segundos
        if not st.session_state.scanning:
            st.session_state.scanning = True
            
            # Executar varredura
            ops = service.scan_opportunities()
            
            # Auto-execução se habilitado
            if st.session_state.auto_execute and ops:
                best_op = ops[0]
                if best_op.score > 30:
                    service.execute_arbitrage(best_op)
                    st.toast(f"Auto-execução: {best_op.symbol}")
            
            st.session_state.scanning = False
            st.session_state.last_scan = now
            st.rerun()

if __name__ == "__main__":
    main()