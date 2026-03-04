import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import threading
import asyncio
from enum import Enum

# --- TYPES ---
class PlatformType(str, Enum):
    BINANCE = "BINANCE"
    CTRADER = "CTRADER"

class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"

class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

@dataclass
class ExchangeLog:
    id: str
    timestamp: datetime
    level: LogLevel
    message: str

@dataclass
class BalanceInfo:
    estimated_total_value: float
    free_usdt: float
    free_btc: float

# --- SIMULATED SERVICES ---
class ExchangeService:
    def __init__(self):
        self.logs: List[ExchangeLog] = []
        self._balance = BalanceInfo(
            estimated_total_value=150000.0,
            free_usdt=75000.0,
            free_btc=1.2
        )
        self._orders = []
    
    def add_log(self, level: LogLevel, message: str):
        """Adiciona um log ao histórico"""
        log = ExchangeLog(
            id=f"LOG-{len(self.logs)}-{int(time.time())}",
            timestamp=datetime.now(),
            level=level,
            message=message
        )
        self.logs.insert(0, log)  # Add to beginning
        if len(self.logs) > 100:  # Keep last 100 logs
            self.logs = self.logs[:100]
    
    async def fetch_balance(self) -> BalanceInfo:
        """Simula fetch de saldo"""
        # Simulate small random changes
        change = random.uniform(-100, 100)
        self._balance.estimated_total_value += change
        
        # Simulate network delay
        await asyncio.sleep(0.1)
        
        self.add_log(LogLevel.INFO, f"Saldo atualizado: ${self._balance.estimated_total_value:,.2f}")
        return self._balance
    
    async def create_order(self, symbol: str, order_type: OrderType, side: OrderSide, 
                          amount: float, price: Optional[float] = None) -> bool:
        """Simula criação de ordem"""
        try:
            # Simulate order processing
            await asyncio.sleep(0.5)
            
            order_id = f"ORD-{int(time.time())}-{random.randint(1000, 9999)}"
            executed_price = price if price else random.uniform(60000, 70000)
            
            self.add_log(
                LogLevel.SUCCESS,
                f"Ordem {order_id} executada: {side.upper()} {amount} {symbol} "
                f"@{executed_price:.2f} (Tipo: {order_type})"
            )
            
            # Update balance
            if side == OrderSide.BUY:
                self._balance.free_btc += amount
                self._balance.free_usdt -= amount * executed_price
            else:
                self._balance.free_btc -= amount
                self._balance.free_usdt += amount * executed_price
            
            # Update total value
            self._balance.estimated_total_value = (
                self._balance.free_usdt + 
                self._balance.free_btc * executed_price
            )
            
            return True
            
        except Exception as e:
            self.add_log(LogLevel.ERROR, f"Falha na ordem: {str(e)}")
            return False
    
    async def cancel_all_orders(self, symbol: str) -> bool:
        """Simula cancelamento de todas as ordens"""
        try:
            await asyncio.sleep(0.3)
            count = random.randint(1, 5)
            self.add_log(
                LogLevel.WARNING,
                f"Canceladas {count} ordens pendentes para {symbol}"
            )
            return True
        except:
            self.add_log(LogLevel.ERROR, "Falha ao cancelar ordens")
            return False

class cTraderService:
    def __init__(self):
        self._connected = False
        self._balance = BalanceInfo(
            estimated_total_value=100000.0,
            free_usdt=50000.0,
            free_btc=0.5
        )
    
    @property
    def is_connected(self) -> bool:
        """Simula status de conexão"""
        # Randomly disconnect sometimes
        if random.random() < 0.05:  # 5% chance to disconnect
            self._connected = False
        return self._connected
    
    async def connect(self) -> bool:
        """Simula conexão com cTrader"""
        await asyncio.sleep(0.5)
        self._connected = random.random() > 0.2  # 80% success rate
        return self._connected
    
    async def place_order(self, symbol: str, side: str, amount: float, 
                         price: Optional[float] = None) -> Dict[str, Any]:
        """Simula colocação de ordem no cTrader"""
        await asyncio.sleep(0.7)  # cTrader is slower
        
        order_id = f"CT-{int(time.time())}-{random.randint(10000, 99999)}"
        executed_price = price if price else random.uniform(60000, 70000)
        
        return {
            "order_id": order_id,
            "price": executed_price,
            "status": "EXECUTED"
        }

class SentientCore:
    """Simulação do núcleo AGI para validação de ordens"""
    def __init__(self):
        self.approval_rate = 0.95  # 95% de aprovação
        
    def should_approve_order(self, symbol: str, side: str, amount: float) -> bool:
        """Decide se aprova uma ordem baseado em lógica simulada"""
        # Simulate AI decision making
        volatility_factor = random.uniform(0.8, 1.2)
        
        # Risk assessment logic
        risk_score = random.random()
        if side == "buy" and "BTC" in symbol:
            risk_score *= 0.7  # Less risky for BTC buys
        
        return risk_score < self.approval_rate

# --- STREAMLIT COMPONENT ---
def init_session_state():
    """Inicializa o estado da sessão"""
    if 'exchange_service' not in st.session_state:
        st.session_state.exchange_service = ExchangeService()
    
    if 'ctrader_service' not in st.session_state:
        st.session_state.ctrader_service = cTraderService()
    
    if 'sentient_core' not in st.session_state:
        st.session_state.sentient_core = SentientCore()
    
    if 'platform' not in st.session_state:
        st.session_state.platform = PlatformType.BINANCE
    
    if 'symbol' not in st.session_state:
        st.session_state.symbol = "BTC/USDT"
    
    if 'side' not in st.session_state:
        st.session_state.side = OrderSide.BUY
    
    if 'order_type' not in st.session_state:
        st.session_state.order_type = OrderType.MARKET
    
    if 'amount' not in st.session_state:
        st.session_state.amount = "0.001"
    
    if 'price' not in st.session_state:
        st.session_state.price = "65000"
    
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    
    if 'is_connected' not in st.session_state:
        st.session_state.is_connected = False
    
    if 'balance' not in st.session_state:
        st.session_state.balance = None
    
    if 'connection_checked' not in st.session_state:
        st.session_state.connection_checked = False
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()

def get_log_color(level: LogLevel) -> str:
    """Retorna cor baseada no nível do log"""
    colors = {
        LogLevel.INFO: "#60a5fa",        # Blue
        LogLevel.WARNING: "#fbbf24",     # Yellow
        LogLevel.ERROR: "#ef4444",       # Red
        LogLevel.SUCCESS: "#10b981"      # Green
    }
    return colors.get(level, "#9ca3af")

async def update_connection_status():
    """Atualiza status de conexão"""
    if st.session_state.platform == PlatformType.BINANCE:
        # For Binance, we're always "connected" in simulation
        st.session_state.is_connected = True
        # Fetch balance
        balance = await st.session_state.exchange_service.fetch_balance()
        st.session_state.balance = balance
    else:
        # For cTrader, check connection
        if not st.session_state.connection_checked:
            await st.session_state.ctrader_service.connect()
            st.session_state.connection_checked = True
        
        st.session_state.is_connected = st.session_state.ctrader_service.is_connected
        if st.session_state.is_connected:
            st.session_state.balance = st.session_state.ctrader_service._balance
    
    st.session_state.last_update = datetime.now()

async def execute_order():
    """Executa uma ordem"""
    st.session_state.is_processing = True
    
    try:
        # Parse inputs
        amount = float(st.session_state.amount)
        price = float(st.session_state.price) if st.session_state.order_type == OrderType.LIMIT else None
        
        # AGI Validation
        approved = st.session_state.sentient_core.should_approve_order(
            st.session_state.symbol,
            st.session_state.side,
            amount
        )
        
        if not approved:
            st.session_state.exchange_service.add_log(
                LogLevel.WARNING,
                f"Ordem REJEITADA pelo Núcleo Senciente: {st.session_state.side.upper()} "
                f"{amount} {st.session_state.symbol}"
            )
            st.session_state.is_processing = False
            return
        
        # Execute based on platform
        if st.session_state.platform == PlatformType.BINANCE:
            success = await st.session_state.exchange_service.create_order(
                st.session_state.symbol,
                st.session_state.order_type,
                st.session_state.side,
                amount,
                price
            )
            
            if success:
                # Update balance after successful order
                await st.session_state.exchange_service.fetch_balance()
        
        else:  # cTrader
            if not st.session_state.ctrader_service.is_connected:
                st.session_state.exchange_service.add_log(
                    LogLevel.ERROR,
                    "cTrader desconectado. Reconectando..."
                )
                await st.session_state.ctrader_service.connect()
            
            if st.session_state.ctrader_service.is_connected:
                result = await st.session_state.ctrader_service.place_order(
                    st.session_state.symbol,
                    st.session_state.side,
                    amount,
                    price
                )
                
                st.session_state.exchange_service.add_log(
                    LogLevel.SUCCESS,
                    f"cTrader: Ordem {result['order_id']} enviada. "
                    f"Preço: {result['price']:.2f}"
                )
            else:
                st.session_state.exchange_service.add_log(
                    LogLevel.ERROR,
                    "Falha ao conectar com cTrader"
                )
    
    except ValueError as e:
        st.session_state.exchange_service.add_log(
            LogLevel.ERROR,
            f"Valor inválido: {str(e)}"
        )
    except Exception as e:
        st.session_state.exchange_service.add_log(
            LogLevel.ERROR,
            f"Erro na execução: {str(e)}"
        )
    
    finally:
        st.session_state.is_processing = False

async def cancel_all_orders():
    """Cancela todas as ordens"""
    if st.session_state.platform == PlatformType.BINANCE:
        success = await st.session_state.exchange_service.cancel_all_orders(
            st.session_state.symbol
        )
        if success:
            st.session_state.exchange_service.add_log(
                LogLevel.SUCCESS,
                "Todas as ordens canceladas com sucesso"
            )
    else:
        st.session_state.exchange_service.add_log(
            LogLevel.WARNING,
            "Cancelamento em massa não suportado no simulador cTrader"
        )

def render_left_panel():
    """Renderiza painel esquerdo de controles"""
    with st.container():
        # Header
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); 
                    background: rgba(30, 41, 59, 0.5);">
            <div style="display: flex; align-items: center; gap: 0.5rem; color: white; 
                        font-weight: bold; letter-spacing: 0.1em;">
                <span style="color: #818cf8;">💻</span> CMD_NEXUS
            </div>
            <div style="font-size: 0.625rem; display: flex; align-items: center; gap: 0.5rem;">
        """, unsafe_allow_html=True)
        
        if st.session_state.is_connected:
            st.markdown('<span style="color: #10b981; display: flex; align-items: center; gap: 0.25rem;">📶 LINK_OK</span>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<span style="color: #ef4444; display: flex; align-items: center; gap: 0.25rem;">🔌 OFFLINE</span>', 
                       unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Content
        with st.container():
            st.markdown("<div style='padding: 1rem;'>", unsafe_allow_html=True)
            
            # Platform Selection
            st.markdown("""
            <div style="font-size: 0.625rem; text-transform: uppercase; color: #6b7280; margin-bottom: 0.25rem;">
                Target Platform
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("BINANCE", 
                           key="btn_binance",
                           use_container_width=True,
                           type="primary" if st.session_state.platform == PlatformType.BINANCE else "secondary"):
                    st.session_state.platform = PlatformType.BINANCE
                    st.rerun()
            
            with col2:
                if st.button("cTRADER", 
                           key="btn_ctrader",
                           use_container_width=True,
                           type="primary" if st.session_state.platform == PlatformType.CTRADER else "secondary"):
                    st.session_state.platform = PlatformType.CTRADER
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Balance Info
            st.markdown("""
            <div style="background: rgba(0, 0, 0, 0.4); border: 1px solid #374151; 
                        border-radius: 0.25rem; padding: 0.75rem; margin-bottom: 1.5rem;">
                <div style="font-size: 0.625rem; text-transform: uppercase; color: #6b7280; margin-bottom: 0.25rem;">
                    Saldo Estimado ({})
                </div>
                <div style="font-size: 1.5rem; color: white; font-weight: bold; display: flex; align-items: center; gap: 0.25rem;">
                    <span style="color: #818cf8;">{}</span>
                    {}
                </div>
            </div>
            """.format(
                st.session_state.platform.value,
                "$" if st.session_state.platform == PlatformType.BINANCE else "€",
                f"{st.session_state.balance.estimated_total_value:,.2f}" if st.session_state.balance else "---"
            ), unsafe_allow_html=True)
            
            # Order Form
            st.markdown("### 📊 Formulário de Ordem")
            
            # Symbol
            symbol = st.text_input(
                "Par de Trading",
                value=st.session_state.symbol,
                key="input_symbol",
                help="Ex: BTC/USDT, ETH/USDT"
            )
            if symbol != st.session_state.symbol:
                st.session_state.symbol = symbol.upper()
            
            # Side Selection
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "🟢 COMPRAR",
                    use_container_width=True,
                    type="primary" if st.session_state.side == OrderSide.BUY else "secondary"
                ):
                    st.session_state.side = OrderSide.BUY
            
            with col2:
                if st.button(
                    "🔴 VENDER",
                    use_container_width=True,
                    type="primary" if st.session_state.side == OrderSide.SELL else "secondary"
                ):
                    st.session_state.side = OrderSide.SELL
            
            # Order Type
            order_type = st.radio(
                "Tipo de Ordem",
                [OrderType.MARKET.value, OrderType.LIMIT.value],
                horizontal=True,
                key="radio_order_type"
            )
            st.session_state.order_type = OrderType(order_type)
            
            # Amount
            amount = st.text_input(
                "Quantidade",
                value=st.session_state.amount,
                key="input_amount"
            )
            st.session_state.amount = amount
            
            # Price (only for limit orders)
            if st.session_state.order_type == OrderType.LIMIT:
                price = st.text_input(
                    "Preço Limite",
                    value=st.session_state.price,
                    key="input_price"
                )
                st.session_state.price = price
            
            # Execute Button
            button_color = "green" if st.session_state.side == OrderSide.BUY else "red"
            button_text = "⚡ EXECUTAR COMPRA" if st.session_state.side == OrderSide.BUY else "⚡ EXECUTAR VENDA"
            
            if st.button(
                button_text,
                use_container_width=True,
                type="primary",
                disabled=st.session_state.is_processing,
                key="btn_execute"
            ):
                asyncio.run(execute_order())
                st.rerun()
            
            # Cancel All Button
            if st.button(
                "🗑️ CANCELAR TODAS",
                use_container_width=True,
                type="secondary",
                disabled=st.session_state.is_processing,
                key="btn_cancel_all"
            ):
                if st.session_state.platform == PlatformType.BINANCE:
                    asyncio.run(cancel_all_orders())
                else:
                    st.warning("Cancelamento em massa não suportado no cTrader")
                st.rerun()
            
            # AGI Validation Notice
            st.markdown("""
            <div style="background: rgba(37, 99, 235, 0.1); border: 1px solid rgba(37, 99, 235, 0.3); 
                        border-radius: 0.25rem; padding: 0.75rem; margin-top: 1rem; font-size: 0.625rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; 
                            font-weight: bold; color: #60a5fa;">
                    <span>🛡️</span> VALIDAÇÃO AGI ATIVA
                </div>
                <div style="color: #93c5fd;">
                    Ordens para {} sujeitas à aprovação do Núcleo Senciente.
                </div>
            </div>
            """.format(st.session_state.platform.value), unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

def render_right_panel():
    """Renderiza painel direito de logs"""
    with st.container():
        # Header
        st.markdown("""
        <div style="padding: 0.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); 
                    background: rgba(0, 0, 0, 0.3); font-size: 0.625rem; color: #6b7280;
                    display: flex; justify-content: space-between;">
            <span>OUTPUT STREAM ({})</span>
            <span>PROTOCOL: {}</span>
        </div>
        """.format(
            st.session_state.platform.value,
            "REST/WSS" if st.session_state.platform == PlatformType.BINANCE else "FIX 4.4"
        ), unsafe_allow_html=True)
        
        # Logs Container
        logs_html = """
        <div style="flex: 1; overflow-y: auto; padding: 1rem; background: black; 
                    font-family: monospace; font-size: 0.75rem; height: 600px;">
        """
        
        logs = st.session_state.exchange_service.logs
        
        if not logs:
            logs_html += """
            <div style="color: #4b5563; font-style: italic; text-align: center; margin-top: 5rem;">
                Terminal pronto. Aguardando comandos...
            </div>
            """
        else:
            for log in logs[:50]:  # Show last 50 logs
                color = get_log_color(log.level)
                time_str = log.timestamp.strftime("%H:%M:%S")
                
                logs_html += f"""
                <div style="display: flex; gap: 0.75rem; padding: 0.125rem 0; 
                            border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
                    <span style="color: #6b7280; width: 5rem; flex-shrink: 0;">
                        {time_str}
                    </span>
                    <span style="color: {color}; width: 4rem; flex-shrink: 0; font-weight: bold;">
                        [{log.level}]
                    </span>
                    <span style="color: #d1d5db; flex: 1;">
                        {log.message}
                    </span>
                </div>
                """
        
        logs_html += "</div>"
        
        st.markdown(logs_html, unsafe_allow_html=True)
        
        # Input Simulation
        st.markdown("""
        <div style="padding: 0.5rem; background: #1f2937; display: flex; align-items: center; 
                    gap: 0.5rem; border-top: 1px solid #374151;">
            <span style="color: #10b981; font-weight: bold;">></span>
            <div style="width: 0.5rem; height: 1rem; background: #10b981; animation: pulse 1s infinite;"></div>
        </div>
        
        <style>
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.2; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Exchange Command Terminal",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS Styles
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #d1d5db;
        }
        
        .css-1d391kg {
            background: transparent;
        }
        
        .stButton > button {
            font-family: monospace;
            transition: all 0.3s;
        }
        
        .stButton > button[type="primary"] {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            border: none;
        }
        
        .stButton > button[type="secondary"] {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        input {
            background: rgba(0, 0, 0, 0.5) !important;
            border: 1px solid #374151 !important;
            color: white !important;
            font-family: monospace !important;
        }
        
        input:focus {
            border-color: #818cf8 !important;
            box-shadow: 0 0 0 1px #818cf8 !important;
        }
        
        .stRadio > div {
            background: #1f2937;
            padding: 0.25rem;
            border-radius: 0.25rem;
            border: 1px solid #374151;
        }
        
        .stRadio > div > label {
            color: #9ca3af;
        }
        
        .stRadio > div > label:hover {
            color: white;
        }
        
        [data-testid="stRadio"] > div > label > div:first-child {
            background-color: #374151;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Update connection status periodically
    current_time = datetime.now()
    if (current_time - st.session_state.last_update).seconds >= 2:  # Update every 2 seconds
        asyncio.run(update_connection_status())
    
    # Main layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_left_panel()
    
    with col2:
        render_right_panel()
    
    # Auto-refresh
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())