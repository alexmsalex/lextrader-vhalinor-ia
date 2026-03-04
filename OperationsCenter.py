import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Centro de Operações",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enums e Classes de Tipos
class MarketType(str, Enum):
    SPOT = "spot"
    FUTURE = "future"

class Platform(str, Enum):
    BINANCE = "BINANCE"
    CTRADER = "CTRADER"

class ActiveTab(str, Enum):
    ORDERBOOK = "orderbook"
    FUTURES = "futures"
    MINING = "mining"

class MarginType(str, Enum):
    ISOLATED = "ISOLATED"
    CROSS = "CROSS"

class OrderBookEntry:
    def __init__(self, price: float, amount: float, total: float = 0):
        self.price = price
        self.amount = amount
        self.total = total

class OrderBook:
    def __init__(self, symbol: str, asks: List[OrderBookEntry], bids: List[OrderBookEntry]):
        self.symbol = symbol
        self.asks = asks
        self.bids = bids

class FuturesPosition:
    def __init__(self, symbol: str, entry_price: float, mark_price: float, 
                 liquidation_price: float, pnl: float, roe: float, 
                 leverage: float, margin_type: MarginType):
        self.symbol = symbol
        self.entry_price = entry_price
        self.mark_price = mark_price
        self.liquidation_price = liquidation_price
        self.pnl = pnl
        self.roe = roe
        self.leverage = leverage
        self.margin_type = margin_type

class LiquidityPool:
    def __init__(self, id: str, pair: str, apy: float, tvl: float, user_share: float):
        self.id = id
        self.pair = pair
        self.apy = apy
        self.tvl = tvl
        self.user_share = user_share

# Serviços simulados
class ExchangeService:
    def __init__(self):
        self.current_symbol = "BTCUSDT"
        self.current_price = 45000
    
    def fetch_order_book(self, symbol: str, depth: int = 15) -> OrderBook:
        """Simula obtenção do livro de ordens"""
        # Gerar asks (vendas)
        asks = []
        current_price = self.current_price * (1 + random.uniform(0.001, 0.01))
        for i in range(depth):
            price = current_price * (1 + (i + 1) * 0.001)
            amount = random.uniform(0.5, 3.0)
            asks.append(OrderBookEntry(price, amount))
        
        # Gerar bids (compras)
        bids = []
        for i in range(depth):
            price = current_price * (1 - (i + 1) * 0.001)
            amount = random.uniform(0.5, 3.0)
            bids.append(OrderBookEntry(price, amount))
        
        return OrderBook(symbol, asks, bids)
    
    def fetch_futures_positions(self, symbol: str) -> List[FuturesPosition]:
        """Simula obtenção de posições futuras"""
        positions = []
        
        for i in range(random.randint(1, 3)):
            entry_price = self.current_price * random.uniform(0.95, 1.05)
            mark_price = self.current_price * random.uniform(0.98, 1.02)
            pnl = random.uniform(-500, 1500)
            
            position = FuturesPosition(
                symbol=f"{symbol}_PERP",
                entry_price=entry_price,
                mark_price=mark_price,
                liquidation_price=entry_price * random.uniform(0.8, 0.95),
                pnl=pnl,
                roe=(pnl / 1000) * 100,  # ROE baseado no PnL
                leverage=random.choice([5, 10, 20]),
                margin_type=random.choice([MarginType.ISOLATED, MarginType.CROSS])
            )
            positions.append(position)
        
        return positions
    
    def fetch_liquidity_mining_pools(self) -> List[LiquidityPool]:
        """Simula obtenção de pools de mineração"""
        pools = [
            LiquidityPool(
                id="1",
                pair="BTC/USDT",
                apy=18.7,
                tvl=25000000,
                user_share=0
            ),
            LiquidityPool(
                id="2",
                pair="ETH/USDT",
                apy=12.3,
                tvl=18000000,
                user_share=0
            ),
            LiquidityPool(
                id="3",
                pair="BNB/USDT",
                apy=25.4,
                tvl=15000000,
                user_share=0
            ),
            LiquidityPool(
                id="4",
                pair="SOL/USDT",
                apy=45.8,
                tvl=8000000,
                user_share=0
            )
        ]
        return pools

class CTraderService:
    def __init__(self):
        self.connected = True
        self.current_symbol = "EURUSD"
        self.current_price = 1.0850
    
    def get_order_book(self, symbol: str) -> OrderBook:
        """Simula obtenção do livro de ordens do cTrader"""
        # Gerar asks (vendas) com mais casas decimais
        asks = []
        current_price = self.current_price * (1 + random.uniform(0.0001, 0.0005))
        for i in range(15):
            price = current_price + (i + 1) * 0.0001
            amount = random.uniform(10000, 50000)
            asks.append(OrderBookEntry(price, amount))
        
        # Gerar bids (compras)
        bids = []
        for i in range(15):
            price = current_price - (i + 1) * 0.0001
            amount = random.uniform(10000, 50000)
            bids.append(OrderBookEntry(price, amount))
        
        return OrderBook(symbol, asks, bids)
    
    def get_open_positions(self) -> List[FuturesPosition]:
        """Simula obtenção de posições abertas do cTrader"""
        positions = []
        
        pairs = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        
        for pair in random.sample(pairs, random.randint(1, 2)):
            entry_price = random.uniform(1.0, 1.2) if pair != "XAUUSD" else random.uniform(1800, 2000)
            mark_price = entry_price * random.uniform(0.998, 1.002)
            pnl = random.uniform(-100, 300)
            
            position = FuturesPosition(
                symbol=pair,
                entry_price=entry_price,
                mark_price=mark_price,
                liquidation_price=entry_price * random.uniform(0.95, 0.99),
                pnl=pnl,
                roe=(pnl / 500) * 100,  # ROE baseado no PnL
                leverage=random.choice([10, 20, 30]),
                margin_type=MarginType.ISOLATED
            )
            positions.append(position)
        
        return positions

# Inicialização dos serviços
if 'exchange_service' not in st.session_state:
    st.session_state.exchange_service = ExchangeService()

if 'ctrader_service' not in st.session_state:
    st.session_state.ctrader_service = CTraderService()

if 'platform' not in st.session_state:
    st.session_state.platform = Platform.BINANCE

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = ActiveTab.ORDERBOOK

if 'market_type' not in st.session_state:
    st.session_state.market_type = MarketType.FUTURE

if 'symbol' not in st.session_state:
    st.session_state.symbol = "BTCUSDT"

if 'current_price' not in st.session_state:
    st.session_state.current_price = 45000

if 'order_book' not in st.session_state:
    st.session_state.order_book = None

if 'positions' not in st.session_state:
    st.session_state.positions = []

if 'pools' not in st.session_state:
    st.session_state.pools = []

if 'loading' not in st.session_state:
    st.session_state.loading = False

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
    
    .operations-center {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    .operations-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #374151;
    }
    
    .platform-selector {
        display: flex;
        background-color: #000;
        border: 1px solid #374151;
        border-radius: 0.25rem;
        padding: 0.125rem;
        margin-left: 1rem;
    }
    
    .platform-btn {
        padding: 0.25rem 0.5rem;
        font-size: 0.5625rem;
        font-weight: bold;
        border-radius: 0.125rem;
        border: none;
        background: transparent;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .platform-btn:hover {
        color: white;
    }
    
    .platform-btn.active {
        color: white;
    }
    
    .platform-binance.active {
        background-color: #f59e0b;
    }
    
    .platform-ctrader.active {
        background-color: #3b82f6;
    }
    
    .tab-selector {
        display: flex;
        gap: 0.5rem;
    }
    
    .tab-btn {
        padding: 0.25rem 0.75rem;
        font-size: 0.625rem;
        border-radius: 0.25rem;
        border: 1px solid;
        background: transparent;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .tab-btn:hover {
        color: white;
    }
    
    .tab-btn.active {
        color: white;
    }
    
    .tab-orderbook.active {
        background-color: rgba(14, 165, 233, 0.3);
        border-color: #0ea5e9;
    }
    
    .tab-futures.active {
        background-color: rgba(168, 85, 247, 0.3);
        border-color: #a855f7;
    }
    
    .tab-mining.active {
        background-color: rgba(245, 158, 11, 0.3);
        border-color: #f59e0b;
    }
    
    .orderbook-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        height: 100%;
        font-family: monospace;
        font-size: 0.625rem;
    }
    
    .orderbook-side {
        display: flex;
        flex-direction: column;
    }
    
    .orderbook-header {
        color: #9ca3af;
        margin-bottom: 0.5rem;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid #374151;
        display: flex;
        justify-content: space-between;
    }
    
    .asks-side .orderbook-header {
        color: #ef4444;
    }
    
    .bids-side .orderbook-header {
        color: #10b981;
    }
    
    .orderbook-row {
        display: flex;
        justify-content: space-between;
        position: relative;
        padding: 0.125rem 0;
    }
    
    .orderbook-ask {
        color: #f87171;
    }
    
    .orderbook-bid {
        color: #4ade80;
    }
    
    .volume-bar {
        position: absolute;
        right: 0;
        top: 0;
        height: 100%;
        opacity: 0.2;
        z-index: 0;
    }
    
    .position-card {
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        border: 1px solid;
    }
    
    .position-card-binance {
        border-color: rgba(168, 85, 247, 0.3);
    }
    
    .position-card-ctrader {
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .position-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .position-symbol {
        color: white;
        font-weight: bold;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .leverage-badge {
        font-size: 0.625rem;
        padding: 0.125rem 0.5rem;
        border-radius: 0.125rem;
    }
    
    .leverage-profit {
        background-color: rgba(22, 163, 74, 0.5);
        color: #4ade80;
    }
    
    .leverage-loss {
        background-color: rgba(220, 38, 38, 0.5);
        color: #f87171;
    }
    
    .position-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        font-size: 0.625rem;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }
    
    .position-pnl {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 0.5rem;
        border-top: 1px solid #374151;
        font-size: 0.625rem;
    }
    
    .pool-card {
        background-color: rgba(0, 0, 0, 0.3);
        border: 1px solid #374151;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .pool-card:hover {
        border-color: rgba(245, 158, 11, 0.5);
    }
    
    .pool-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .pool-icon {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        background-color: #1f2937;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: bold;
        color: #6b7280;
    }
    
    .pool-name {
        color: white;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .pool-tvl {
        color: #9ca3af;
        font-size: 0.5625rem;
    }
    
    .pool-apy {
        color: #10b981;
        font-size: 0.875rem;
        font-weight: bold;
        font-family: monospace;
        text-align: right;
    }
    
    .pool-btn {
        margin-top: 0.25rem;
        font-size: 0.5625rem;
        background-color: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        padding: 0.125rem 0.5rem;
        border-radius: 0.125rem;
        border: 1px solid rgba(245, 158, 11, 0.5);
        cursor: pointer;
    }
    
    .pool-btn:hover {
        background-color: rgba(245, 158, 11, 0.4);
    }
    
    .alert-yellow {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 0.25rem;
        padding: 0.5rem;
        font-size: 0.625rem;
        color: #f59e0b;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #6b7280;
        gap: 0.5rem;
    }
    
    .scroll-container {
        flex: 1;
        overflow-y: auto;
        padding-right: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Função para buscar dados
def fetch_data():
    st.session_state.loading = True
    
    try:
        if st.session_state.platform == Platform.BINANCE:
            # Lógica Binance
            if st.session_state.active_tab == ActiveTab.ORDERBOOK:
                book = st.session_state.exchange_service.fetch_order_book(st.session_state.symbol, 15)
                st.session_state.order_book = book
            elif st.session_state.active_tab == ActiveTab.FUTURES and st.session_state.market_type == MarketType.FUTURE:
                positions = st.session_state.exchange_service.fetch_futures_positions(st.session_state.symbol)
                st.session_state.positions = positions
            elif st.session_state.active_tab == ActiveTab.MINING:
                pools = st.session_state.exchange_service.fetch_liquidity_mining_pools()
                st.session_state.pools = pools
        else:
            # Lógica cTrader
            if st.session_state.active_tab == ActiveTab.ORDERBOOK:
                book = st.session_state.ctrader_service.get_order_book(st.session_state.symbol)
                st.session_state.order_book = book
            elif st.session_state.active_tab == ActiveTab.FUTURES:
                positions = st.session_state.ctrader_service.get_open_positions()
                st.session_state.positions = positions
            elif st.session_state.active_tab == ActiveTab.MINING:
                # cTrader Copy Trading Mock
                st.session_state.pools = [
                    LiquidityPool(
                        id="1",
                        pair="Copy: AlphaBot",
                        apy=125.5,
                        tvl=5000000,
                        user_share=0
                    ),
                    LiquidityPool(
                        id="2",
                        pair="Copy: QuantumGrid",
                        apy=45.2,
                        tvl=1200000,
                        user_share=0
                    )
                ]
                
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
    finally:
        st.session_state.loading = False
        st.session_state.last_update = datetime.now()

# Inicializar dados
if st.session_state.order_book is None:
    fetch_data()

# Barra lateral com configurações
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    # Seletor de mercado
    market_type = st.selectbox(
        "Tipo de Mercado",
        ["FUTURE", "SPOT"],
        index=0 if st.session_state.market_type == MarketType.FUTURE else 1
    )
    if market_type == "FUTURE":
        st.session_state.market_type = MarketType.FUTURE
    else:
        st.session_state.market_type = MarketType.SPOT
    
    # Seletor de símbolo
    if st.session_state.platform == Platform.BINANCE:
        symbol = st.selectbox(
            "Símbolo",
            ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT"],
            index=0
        )
    else:
        symbol = st.selectbox(
            "Símbolo",
            ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
            index=0
        )
    st.session_state.symbol = symbol
    
    # Preço atual
    if st.session_state.platform == Platform.BINANCE:
        st.session_state.current_price = st.number_input(
            "Preço Atual (USDT)",
            min_value=0.0,
            value=45000.0,
            step=1000.0
        )
    else:
        st.session_state.current_price = st.number_input(
            "Preço Atual",
            min_value=0.0,
            value=1.0850,
            step=0.0010,
            format="%.4f"
        )
    
    st.markdown("---")
    st.markdown("### 📊 Controles")
    
    if st.button("🔄 Atualizar Dados"):
        fetch_data()
        st.success("Dados atualizados!")
    
    auto_refresh = st.checkbox("Atualização Automática", value=True)
    refresh_interval = st.slider("Intervalo (segundos)", 1, 10, 3)
    
    st.markdown("---")
    st.markdown("### 📈 Estatísticas")
    
    if st.session_state.platform == Platform.BINANCE:
        st.metric("Preço Atual", f"${st.session_state.current_price:,.2f}")
    else:
        st.metric("Preço Atual", f"{st.session_state.current_price:.4f}")
    
    if st.session_state.active_tab == ActiveTab.ORDERBOOK and st.session_state.order_book:
        st.metric("Profundidade", f"{len(st.session_state.order_book.asks)} níveis")
    elif st.session_state.active_tab == ActiveTab.FUTURES:
        st.metric("Posições Ativas", len(st.session_state.positions))
    elif st.session_state.active_tab == ActiveTab.MINING:
        st.metric("Pools Disponíveis", len(st.session_state.pools))
    
    st.markdown(f"*Última atualização:* {st.session_state.last_update.strftime('%H:%M:%S')}")

# Componente principal
st.markdown("""
<div class="operations-center">
    <div class="operations-header">
        <div style="display: flex; align-items: center;">
            <h3 style="color: white; font-weight: bold; font-size: 0.875rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="color: #0ea5e9;">⚙️</span>
                CENTRO DE OPERAÇÕES
            </h3>
            
            <!-- Platform Selector -->
            <div class="platform-selector">
                <button class="platform-btn platform-binance {'active' if platform == 'BINANCE' else ''}" onclick="window.location.href='?platform=BINANCE'">
                    BINANCE
                </button>
                <button class="platform-btn platform-ctrader {'active' if platform == 'CTRADER' else ''}" onclick="window.location.href='?platform=CTRADER'">
                    cTRADER
                </button>
            </div>
        </div>
        
        <!-- Tab Selector -->
        <div class="tab-selector">
            <button class="tab-btn tab-orderbook {'active' if active_tab == 'ORDERBOOK' else ''}" onclick="window.location.href='?tab=ORDERBOOK'">
                BOOK (L2)
            </button>
            <button class="tab-btn tab-futures {'active' if active_tab == 'FUTURES' else ''}" onclick="window.location.href='?tab=FUTURES'">
                POSIÇÕES
            </button>
            <button class="tab-btn tab-mining {'active' if active_tab == 'MINING' else ''}" onclick="window.location.href='?tab=MINING'">
                {'MINING / EARN' if platform == 'BINANCE' else 'COPY TRADING'}
            </button>
        </div>
    </div>
    
    <div class="scroll-container">
""".format(
    platform=st.session_state.platform.value,
    active_tab=st.session_state.active_tab.value
), unsafe_allow_html=True)

# Conteúdo baseado na aba ativa
if st.session_state.active_tab == ActiveTab.ORDERBOOK:
    if st.session_state.order_book:
        st.markdown('<div class="orderbook-container">', unsafe_allow_html=True)
        
        # ASKS (Vendas)
        st.markdown('<div class="orderbook-side asks-side">', unsafe_allow_html=True)
        st.markdown('<div class="orderbook-header"><span>VENDAS (ASKS)</span><span>QTD</span></div>', unsafe_allow_html=True)
        
        asks = st.session_state.order_book.asks[::-1]  # Inverter para mostrar do maior para menor
        max_ask_amount = max(ask.amount for ask in asks) if asks else 1
        
        for ask in asks:
            width_percent = min(100, (ask.amount / max_ask_amount) * 100)
            price_format = f"{ask.price:.5f}" if st.session_state.platform == Platform.CTRADER else f"{ask.price:.2f}"
            
            st.markdown(f"""
            <div class="orderbook-row">
                <div class="volume-bar" style="background-color: #ef4444; width: {width_percent}%;"></div>
                <span class="orderbook-ask">{price_format}</span>
                <span style="color: #9ca3af;">{ask.amount:.4f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # BIDS (Compras)
        st.markdown('<div class="orderbook-side bids-side">', unsafe_allow_html=True)
        st.markdown('<div class="orderbook-header"><span>COMPRAS (BIDS)</span><span>QTD</span></div>', unsafe_allow_html=True)
        
        bids = st.session_state.order_book.bids
        max_bid_amount = max(bid.amount for bid in bids) if bids else 1
        
        for bid in bids:
            width_percent = min(100, (bid.amount / max_bid_amount) * 100)
            price_format = f"{bid.price:.5f}" if st.session_state.platform == Platform.CTRADER else f"{bid.price:.2f}"
            
            st.markdown(f"""
            <div class="orderbook-row">
                <div class="volume-bar" style="background-color: #10b981; width: {width_percent}%;"></div>
                <span class="orderbook-bid">{price_format}</span>
                <span style="color: #9ca3af;">{bid.amount:.4f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div style="font-size: 1.5rem;">⏳</div>
            <p>Conectando ao Feed L2 ({st.session_state.platform.value})...</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.active_tab == ActiveTab.FUTURES:
    if st.session_state.platform == Platform.BINANCE and st.session_state.market_type == MarketType.SPOT:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size: 1.5rem;">🔒</div>
            <p style="text-align: center;">
                Binance: Terminal configurado para SPOT.<br/>
                <span style="font-size: 0.625rem;">Alterne para MODO FUTUROS no cabeçalho para acessar derivativos.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    elif not st.session_state.positions:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size: 1.5rem;">⚡</div>
            <p>Nenhuma posição aberta.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for position in st.session_state.positions:
            position_class = "position-card-ctrader" if st.session_state.platform == Platform.CTRADER else "position-card-binance"
            leverage_class = "leverage-profit" if position.pnl >= 0 else "leverage-loss"
            pnl_color = "#4ade80" if position.pnl >= 0 else "#f87171"
            pnl_sign = "+" if position.pnl >= 0 else ""
            currency = "EUR" if st.session_state.platform == Platform.CTRADER else "USDT"
            
            st.markdown(f"""
            <div class="position-card {position_class}">
                <div class="position-header">
                    <div class="position-symbol">
                        {'🌍' if st.session_state.platform == Platform.CTRADER else ''}
                        {position.symbol}
                    </div>
                    <span class="leverage-badge {leverage_class}">
                        {position.leverage}x {position.margin_type.value}
                    </span>
                </div>
                
                <div class="position-grid">
                    <div>Entrada: <span style="color: white;">${position.entry_price:.2f}</span></div>
                    <div>Mark: <span style="color: white;">${position.mark_price:.2f}</span></div>
                    <div>Liq: <span style="color: #f97316;">${position.liquidation_price:.2f}</span></div>
                    <div>ROE: <span style="color: {'#4ade80' if position.roe >= 0 else '#f87171'}">{position.roe:.2f}%</span></div>
                </div>
                
                <div class="position-pnl">
                    <span style="color: #9ca3af;">PnL Não Realizado</span>
                    <span style="color: {pnl_color}; font-weight: bold; font-family: monospace; font-size: 0.875rem;">
                        {pnl_sign}{position.pnl:.2f} {currency}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.active_tab == ActiveTab.MINING:
    tab_label = "Liquidez Neural & Mineração DeFi" if st.session_state.platform == Platform.BINANCE else "cTrader Copy Strategy"
    btn_label = "MINERAR" if st.session_state.platform == Platform.BINANCE else "COPIAR"
    
    st.markdown(f"""
    <div class="alert-yellow">
        <span>⚡</span>
        <span>{tab_label}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.pools:
        st.markdown("""
        <div class="empty-state">
            <p>Nenhum pool disponível.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for pool in st.session_state.pools:
            first_char = pool.pair.split(':')[0][0] if ':' in pool.pair else pool.pair.split('/')[0][0]
            tvl_formatted = f"${pool.tvl/1000000:.1f}M"
            
            st.markdown(f"""
            <div class="pool-card">
                <div class="pool-info">
                    <div class="pool-icon">{first_char}</div>
                    <div>
                        <div class="pool-name">{pool.pair}</div>
                        <div class="pool-tvl">Liquidez/AUM: {tvl_formatted}</div>
                    </div>
                </div>
                <div>
                    <div class="pool-apy">{pool.apy}% {'APY' if st.session_state.platform == Platform.BINANCE else 'ROI'}</div>
                    <button class="pool-btn">{btn_label}</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    if st.session_state.platform == Platform.BINANCE:
        st.markdown(f"**Símbolo:** {st.session_state.symbol}")
    else:
        st.markdown(f"**Par:** {st.session_state.symbol}")

with col_footer2:
    st.markdown(f"**Plataforma:** {st.session_state.platform.value}")

with col_footer3:
    st.markdown(f"**Modo:** {st.session_state.market_type.value.upper()}")

# Atualização automática
if auto_refresh:
    time.sleep(refresh_interval)
    fetch_data()
    st.rerun()

# URLs para mudar estado (simulado)
platform = st.query_params.get("platform", [st.session_state.platform.value])[0]
if platform in ["BINANCE", "CTRADER"]:
    st.session_state.platform = Platform(platform)

tab = st.query_params.get("tab", [st.session_state.active_tab.value])[0]
if tab in ["ORDERBOOK", "FUTURES", "MINING"]:
    st.session_state.active_tab = ActiveTab(tab)