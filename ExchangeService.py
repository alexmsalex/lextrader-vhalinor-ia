import ccxt
import asyncio
import websockets
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import time
import logging
from decimal import Decimal
import os
import sys
from pathlib import Path
import threading
import queue

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tipos e estruturas de dados
class MarketType(Enum):
    SPOT = "spot"
    FUTURE = "future"
    MARGIN = "margin"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(Enum):
    LIMIT = "limit"
    MARKET = "market"

class LogLevel(Enum):
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
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'level': self.level.value,
            'message': self.message
        }

@dataclass
class WalletBalance:
    total_usdt: float = 0.0
    free_usdt: float = 0.0
    total_btc: float = 0.0
    free_btc: float = 0.0
    estimated_total_value: float = 0.0

@dataclass
class FuturesPosition:
    symbol: str
    amount: float
    entry_price: float
    mark_price: float
    pnl: float
    roe: float
    leverage: float
    margin_type: str
    liquidation_price: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'symbol': self.symbol,
            'amount': self.amount,
            'entry_price': self.entry_price,
            'mark_price': self.mark_price,
            'pnl': self.pnl,
            'roe': self.roe,
            'leverage': self.leverage,
            'margin_type': self.margin_type,
            'liquidation_price': self.liquidation_price
        }

@dataclass
class OrderBookLevel:
    price: float
    amount: float
    total: float

@dataclass
class OrderBook:
    bids: List[OrderBookLevel]
    asks: List[OrderBookLevel]
    timestamp: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'bids': [{'price': b.price, 'amount': b.amount, 'total': b.total} for b in self.bids],
            'asks': [{'price': a.price, 'amount': a.amount, 'total': a.total} for a in self.asks],
            'timestamp': self.timestamp
        }

@dataclass
class LiquidityPool:
    id: str
    pair: str
    apy: float
    tvl: float
    user_share: float

@dataclass
class SymbolInfo:
    symbol: str
    base: str
    quote: str
    precision: Dict[str, int]
    limits: Dict[str, Any]
    active: bool
    margin: bool
    futures: bool

@dataclass
class Candle:
    time: str
    timestamp: int
    price: float
    open: float
    high: float
    low: float
    volume: float
    is_final: bool

# Simulação do núcleo sentiente (para compatibilidade)
class SentientCore:
    def __init__(self):
        self.thoughts = []
        self.state = "STABLE"
        self.emotion_stability = 100.0
    
    def add_thought(self, thought: str):
        self.thoughts.append(f"{datetime.now().isoformat()}: {thought}")
        if len(self.thoughts) > 100:
            self.thoughts.pop(0)
    
    def get_state(self) -> str:
        return self.state
    
    def get_vector(self) -> Dict[str, float]:
        return {"stability": self.emotion_stability}
    
    def perceive_reality(self, intensity: float, feedback: float):
        # Simula percepção do núcleo AGI
        if feedback < -50:
            self.state = "STRESSED"
            self.emotion_stability = max(0, self.emotion_stability - 10)
        elif feedback > 0:
            self.state = "EXCITED"
            self.emotion_stability = min(100, self.emotion_stability + 5)
        else:
            self.state = "STABLE"
    
    def get_thoughts(self) -> List[str]:
        return self.thoughts

# Inicializar núcleo sentiente
sentient_core = SentientCore()

# Configurações de chaves
class ExchangeKeys:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY", "")
        self.api_secret = os.getenv("BINANCE_API_SECRET", "")

keys = ExchangeKeys()

# Sistema de logs
logs: List[ExchangeLog] = []
logs_lock = threading.Lock()

def add_log(message: str, level: LogLevel = LogLevel.INFO):
    """Adiciona entrada ao log"""
    with logs_lock:
        log_entry = ExchangeLog(
            id=f"LOG-{int(time.time()*1000)}-{len(logs)}",
            timestamp=datetime.now(),
            level=level,
            message=message
        )
        logs.insert(0, log_entry)
        if len(logs) > 200:
            logs.pop()
    
    # Também loga no console
    log_method = {
        LogLevel.INFO: logger.info,
        LogLevel.WARNING: logger.warning,
        LogLevel.ERROR: logger.error,
        LogLevel.SUCCESS: logger.info
    }
    log_method[level](f"[EXCHANGE] {message}")

# Classe principal de Exchange
class BinanceExchange:
    def __init__(self):
        self.exchange: Optional[ccxt.binance] = None
        self.current_market_type: MarketType = MarketType.SPOT
        self.ws_connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.ws_listeners: Dict[str, List[Callable]] = {}
        self.price_streams: Dict[str, bool] = {}
        self.markets_loaded = False
        
    def set_credentials(self, api_key: str, api_secret: str):
        """Define credenciais da API"""
        keys.api_key = api_key
        keys.api_secret = api_secret
        self.exchange = None  # Forçar recriação
        add_log("Credenciais de API atualizadas em memória.", LogLevel.INFO)
    
    def set_market_type(self, market_type: MarketType):
        """Define o tipo de mercado"""
        if market_type != self.current_market_type:
            self.current_market_type = market_type
            self.exchange = None  # Forçar recriação com novo tipo
            add_log(f"Contexto de mercado alterado para: {market_type.value.upper()}", LogLevel.INFO)
    
    def ensure_exchange(self) -> ccxt.binance:
        """Garante que a exchange está inicializada"""
        if self.exchange is not None:
            return self.exchange
        
        try:
            options = {
                'defaultType': self.current_market_type.value,
                'adjustForTimeDifference': True,
                'recvWindow': 60000
            }
            
            self.exchange = ccxt.binance({
                'apiKey': keys.api_key,
                'secret': keys.api_secret,
                'enableRateLimit': True,
                'options': options
            })
            
            # Tentar carregar mercados apenas se tivermos chaves
            if keys.api_key:
                try:
                    self.exchange.load_markets()
                    self.markets_loaded = True
                    add_log(f"Mercados carregados para {self.current_market_type.value}", LogLevel.SUCCESS)
                except Exception as e:
                    logger.warning(f"Não foi possível carregar mercados: {e}")
            
            add_log(f"Exchange Binance ({self.current_market_type.value}) inicializada com sucesso.", LogLevel.SUCCESS)
            return self.exchange
            
        except Exception as e:
            error_msg = f"Erro ao inicializar exchange: {str(e)}"
            add_log(error_msg, LogLevel.ERROR)
            raise RuntimeError(error_msg)
    
    async def fetch_ticker(self, symbol: str = "BTC/USDT") -> Optional[Dict[str, Any]]:
        """Busca ticker do símbolo"""
        ex = self.ensure_exchange()
        try:
            ticker = ex.fetch_ticker(symbol)
            add_log(f"Ticker obtido: {symbol} - Preço: {ticker.get('last')}", LogLevel.INFO)
            return ticker
        except Exception as e:
            error_msg = f"Erro ao obter ticker {symbol}: {str(e)}"
            add_log(error_msg, LogLevel.ERROR)
            return None
    
    async def fetch_ohlcv(
        self, 
        symbol: str = "BTC/USDT", 
        timeframe: str = "1h", 
        limit: int = 100
    ) -> List[List[float]]:
        """Busca dados OHLCV"""
        ex = self.ensure_exchange()
        try:
            ohlcv = ex.fetch_ohlcv(symbol, timeframe, limit=limit)
            add_log(f"OHLCV obtido: {symbol} - {len(ohlcv)} candles", LogLevel.INFO)
            return ohlcv
        except Exception as e:
            error_msg = f"Falha ao buscar OHLCV: {str(e)}"
            add_log(error_msg, LogLevel.ERROR)
            return []
    
    async def fetch_order_book(self, symbol: str, limit: int = 20) -> Optional[OrderBook]:
        """Busca livro de ordens"""
        ex = self.ensure_exchange()
        try:
            book = ex.fetch_order_book(symbol, limit)
            
            def process_levels(levels: List[List[float]]) -> List[OrderBookLevel]:
                total = 0.0
                processed = []
                for level in levels:
                    price, amount = level[0], level[1]
                    total += amount
                    processed.append(OrderBookLevel(price=price, amount=amount, total=total))
                return processed
            
            order_book = OrderBook(
                bids=process_levels(book['bids']),
                asks=process_levels(book['asks']),
                timestamp=book.get('timestamp', int(time.time() * 1000))
            )
            
            return order_book
            
        except Exception as e:
            add_log(f"Erro no Order Book: {str(e)}", LogLevel.WARNING)
            return None
    
    async def create_order(
        self,
        symbol: str,
        order_type: OrderType,
        side: OrderSide,
        amount: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Cria uma ordem na exchange"""
        ex = self.ensure_exchange()
        
        # 1. Verificação de segurança AGI
        agi_state = sentient_core.get_state()
        emotion = sentient_core.get_vector()
        
        if agi_state in ["DORMANT", "FRACTURED"]:
            msg = f"AGI REJEITOU A ORDEM: Estado {agi_state} instável. Risco de falha cognitiva."
            add_log(msg, LogLevel.ERROR)
            sentient_core.add_thought(msg)
            raise RuntimeError(msg)
        
        if emotion.get("stability", 100) < 20:
            msg = "ALERTA DE SEGURANÇA: Instabilidade emocional detectada. Ordem bloqueada pelo núcleo."
            add_log(msg, LogLevel.WARNING)
            sentient_core.add_thought(msg)
            raise RuntimeError(msg)
        
        add_log(
            f"Iniciando ordem: {side.value.upper()} {amount} {symbol} @ "
            f"{price if price else 'MARKET'}",
            LogLevel.INFO
        )
        
        # Modo de simulação
        if not keys.api_key:
            await asyncio.sleep(0.8)  # Simular latência
            result = self._simulate_order(symbol, order_type.value, side.value, amount, price or 0)
            add_log(f"Ordem SIMULADA executada: {result['id']}", LogLevel.SUCCESS)
            sentient_core.perceive_reality(0.5, 0 if order_type == OrderType.MARKET else 0.1)
            return result
        
        try:
            params = {}
            order: Dict[str, Any]
            
            if order_type == OrderType.LIMIT and price is not None:
                order = ex.create_limit_order(
                    symbol=symbol,
                    side=side.value,
                    amount=amount,
                    price=price,
                    params=params
                )
            else:
                order = ex.create_market_order(
                    symbol=symbol,
                    side=side.value,
                    amount=amount,
                    params=params
                )
            
            add_log(f"Ordem executada na Binance: {order.get('id', 'N/A')}", LogLevel.SUCCESS)
            sentient_core.perceive_reality(1.0, 0)
            return order
            
        except Exception as e:
            error_msg = f"FALHA CRÍTICA NA ORDEM: {str(e)}"
            add_log(error_msg, LogLevel.ERROR)
            sentient_core.add_thought(f"Erro na matrix financeira: {str(e)}")
            sentient_core.perceive_reality(5.0, -100)
            raise
    
    async def cancel_all_orders(self, symbol: str) -> List[str]:
        """Cancela todas as ordens do símbolo"""
        ex = self.ensure_exchange()
        
        if not keys.api_key:
            add_log(f"Cancelamento simulado de todas as ordens para {symbol}", LogLevel.INFO)
            return []
        
        try:
            orders = ex.fetch_open_orders(symbol)
            results = []
            for order in orders:
                try:
                    ex.cancel_order(order['id'], symbol)
                    add_log(f"Ordem {order['id']} cancelada", LogLevel.INFO)
                    results.append(order['id'])
                except Exception as e:
                    add_log(f"Erro ao cancelar ordem {order['id']}: {str(e)}", LogLevel.WARNING)
            return results
        except Exception as e:
            error_msg = f"Erro ao cancelar ordens: {str(e)}"
            add_log(error_msg, LogLevel.ERROR)
            raise
    
    async def fetch_balance(self) -> Optional[WalletBalance]:
        """Busca saldo da conta"""
        ex = self.ensure_exchange()
        
        # Modo de simulação
        if not keys.api_key:
            # Retorna dados simulados
            return WalletBalance(
                total_usdt=10000.0,
                free_usdt=8000.0,
                total_btc=0.1,
                free_btc=0.08,
                estimated_total_value=15000.0
            )
        
        try:
            balance = ex.fetch_balance()
            
            usdt = balance.get('USDT', {'total': 0.0, 'free': 0.0})
            btc = balance.get('BTC', {'total': 0.0, 'free': 0.0})
            
            # Converter para float se for Decimal
            def to_float(value):
                if isinstance(value, Decimal):
                    return float(value)
                return float(value or 0.0)
            
            total_usdt = to_float(usdt.get('total'))
            free_usdt = to_float(usdt.get('free'))
            total_btc = to_float(btc.get('total'))
            free_btc = to_float(btc.get('free'))
            
            estimated_value = total_usdt
            
            if self.current_market_type == MarketType.SPOT and total_btc > 0:
                try:
                    ticker = await self.fetch_ticker("BTC/USDT")
                    if ticker and ticker.get('last'):
                        estimated_value = total_usdt + (total_btc * float(ticker['last']))
                except:
                    pass
            
            return WalletBalance(
                total_usdt=total_usdt,
                free_usdt=free_usdt,
                total_btc=total_btc,
                free_btc=free_btc,
                estimated_total_value=estimated_value
            )
            
        except Exception as e:
            add_log(f"Erro ao buscar saldo: {str(e)}", LogLevel.ERROR)
            return None
    
    async def fetch_futures_positions(self, symbol: Optional[str] = None) -> List[FuturesPosition]:
        """Busca posições futuros"""
        if self.current_market_type != MarketType.FUTURE or not keys.api_key:
            return []
        
        ex = self.ensure_exchange()
        try:
            positions = ex.fetch_positions(symbols=[symbol] if symbol else None)
            result = []
            for pos in positions:
                try:
                    position = FuturesPosition(
                        symbol=pos['symbol'],
                        amount=float(pos.get('contracts', pos.get('amount', 0))),
                        entry_price=float(pos.get('entryPrice', 0)),
                        mark_price=float(pos.get('markPrice', 0)),
                        pnl=float(pos.get('unrealizedPnl', 0)),
                        roe=float(pos.get('percentage', 0)),
                        leverage=float(pos.get('leverage', 1)),
                        margin_type=pos.get('marginType', 'cross'),
                        liquidation_price=float(pos.get('liquidationPrice', 0))
                    )
                    result.append(position)
                except (KeyError, TypeError) as e:
                    logger.warning(f"Erro ao processar posição: {e}")
            return result
        except Exception as e:
            add_log(f"Erro ao buscar posições futuros: {str(e)}", LogLevel.WARNING)
            return []
    
    async def fetch_liquidity_mining_pools(self) -> List[LiquidityPool]:
        """Busca pools de liquidez (simulado)"""
        # Em um cenário real, isso viria da API da Binance
        return [
            LiquidityPool(id='1', pair='BTC/USDT', apy=3.45, tvl=125000000.0, user_share=0.0),
            LiquidityPool(id='2', pair='ETH/USDT', apy=4.12, tvl=89000000.0, user_share=0.0),
        ]
    
    async def check_order_details(self, order_id: str, symbol: str) -> Optional[Dict[str, Any]]:
        """Verifica detalhes de uma ordem"""
        if not keys.api_key:
            return None
        
        ex = self.ensure_exchange()
        try:
            return ex.fetch_order(order_id, symbol)
        except Exception:
            return None
    
    async def cancel_order(self, order_id: str, symbol: str) -> bool:
        """Cancela uma ordem específica"""
        if not keys.api_key:
            return True
        
        ex = self.ensure_exchange()
        try:
            ex.cancel_order(order_id, symbol)
            return True
        except Exception:
            return False
    
    def _simulate_order(self, symbol: str, order_type: str, side: str, amount: float, price: float) -> Dict[str, Any]:
        """Simula uma ordem (para modo sem API)"""
        return {
            'id': f'SIM-{int(time.time()*1000)}',
            'symbol': symbol,
            'type': order_type,
            'side': side,
            'amount': amount,
            'price': price,
            'status': 'closed',
            'timestamp': int(time.time() * 1000),
            'datetime': datetime.now().isoformat(),
            'filled': amount,
            'remaining': 0,
            'cost': amount * price,
            'trades': [],
            'fee': {'currency': 'USDT', 'cost': 0.0}
        }
    
    async def start_price_stream(
        self, 
        symbol: str, 
        timeframe: str = "15m",
        on_update: Optional[Callable[[Candle], None]] = None
    ) -> str:
        """Inicia stream de preços WebSocket"""
        ws_symbol = symbol.replace("/", "").lower()
        stream_id = f"{ws_symbol}_{timeframe}"
        
        if stream_id in self.price_streams:
            return stream_id
        
        async def ws_listener():
            url = f"wss://stream.binance.com:9443/ws/{ws_symbol}@kline_{timeframe}"
            
            while stream_id in self.price_streams:
                try:
                    async with websockets.connect(url) as websocket:
                        self.ws_connections[stream_id] = websocket
                        add_log(f"WebSocket conectado para {symbol} ({timeframe})", LogLevel.INFO)
                        
                        while stream_id in self.price_streams:
                            message = await websocket.recv()
                            data = json.loads(message)
                            
                            if data.get('e') == 'kline':
                                k = data['k']
                                candle = Candle(
                                    time=datetime.fromtimestamp(k['t'] / 1000).strftime('%H:%M:%S'),
                                    timestamp=k['t'],
                                    price=float(k['c']),
                                    open=float(k['o']),
                                    high=float(k['h']),
                                    low=float(k['l']),
                                    volume=float(k['v']),
                                    is_final=k['x']
                                )
                                
                                if on_update:
                                    on_update(candle)
                                
                                # Notificar listeners registrados
                                if stream_id in self.ws_listeners:
                                    for listener in self.ws_listeners[stream_id]:
                                        try:
                                            listener(candle)
                                        except Exception as e:
                                            logger.error(f"Erro no listener: {e}")
                
                except websockets.exceptions.ConnectionClosed:
                    add_log(f"Conexão WebSocket fechada para {symbol}", LogLevel.WARNING)
                    await asyncio.sleep(5)
                except Exception as e:
                    add_log(f"Erro no WebSocket {symbol}: {str(e)}", LogLevel.ERROR)
                    await asyncio.sleep(10)
        
        self.price_streams[stream_id] = True
        asyncio.create_task(ws_listener())
        
        return stream_id
    
    def stop_price_stream(self, stream_id: str):
        """Para um stream de preços"""
        if stream_id in self.price_streams:
            del self.price_streams[stream_id]
        
        if stream_id in self.ws_connections:
            # O loop WebSocket se encerrará naturalmente na próxima iteração
            pass
    
    def add_price_listener(self, stream_id: str, listener: Callable[[Candle], None]):
        """Adiciona um listener para stream de preços"""
        if stream_id not in self.ws_listeners:
            self.ws_listeners[stream_id] = []
        self.ws_listeners[stream_id].append(listener)
    
    def remove_price_listener(self, stream_id: str, listener: Callable[[Candle], None]):
        """Remove um listener de stream de preços"""
        if stream_id in self.ws_listeners:
            if listener in self.ws_listeners[stream_id]:
                self.ws_listeners[stream_id].remove(listener)
    
    # Métodos de conveniência (aliases)
    async def get_ticker(self, symbol: str = "BTC/USDT") -> Optional[Dict[str, Any]]:
        return await self.fetch_ticker(symbol)
    
    async def get_ohlcv(self, symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 100):
        return await self.fetch_ohlcv(symbol, timeframe, limit)
    
    async def get_order_book(self, symbol: str, limit: int = 20):
        return await self.fetch_order_book(symbol, limit)
    
    async def send_market_order(self, symbol: str, side: OrderSide, amount: float):
        return await self.create_order(symbol, OrderType.MARKET, side, amount)
    
    async def send_limit_order(self, symbol: str, side: OrderSide, amount: float, price: float):
        return await self.create_order(symbol, OrderType.LIMIT, side, amount, price)
    
    async def get_balance(self):
        return await self.fetch_balance()

# Instância global da exchange
exchange = BinanceExchange()

# Funções de conveniência para compatibilidade
def set_credentials(api_key: str, api_secret: str):
    exchange.set_credentials(api_key, api_secret)

def set_market_type(market_type: str):
    exchange.set_market_type(MarketType(market_type))

async def fetch_ticker(symbol: str = "BTC/USDT") -> Optional[Dict[str, Any]]:
    return await exchange.fetch_ticker(symbol)

async def fetch_ohlcv(symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 100):
    return await exchange.fetch_ohlcv(symbol, timeframe, limit)

async def fetch_order_book(symbol: str, limit: int = 20):
    return await exchange.fetch_order_book(symbol, limit)

async def create_order(symbol: str, order_type: str, side: str, amount: float, price: Optional[float] = None):
    return await exchange.create_order(
        symbol,
        OrderType(order_type),
        OrderSide(side),
        amount,
        price
    )

async def cancel_all_orders(symbol: str):
    return await exchange.cancel_all_orders(symbol)

async def fetch_balance():
    return await exchange.fetch_balance()

async def fetch_futures_positions(symbol: Optional[str] = None):
    return await exchange.fetch_futures_positions(symbol)

async def fetch_liquidity_mining_pools():
    return await exchange.fetch_liquidity_mining_pools()

async def check_order_details(order_id: str, symbol: str):
    return await exchange.check_order_details(order_id, symbol)

async def cancel_order(order_id: str, symbol: str):
    return await exchange.cancel_order(order_id, symbol)

def start_price_stream(symbol: str, timeframe: str = "15m", on_update: Optional[Callable] = None):
    return exchange.start_price_stream(symbol, timeframe, on_update)

def stop_price_stream(stream_id: str):
    exchange.stop_price_stream(stream_id)

# Aliases para compatibilidade com Python
def get_exchange():
    return exchange.ensure_exchange()

async def pegar_ohlcv(symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 100):
    return await fetch_ohlcv(symbol, timeframe, limit)

async def obter_ticker(symbol: str = "BTC/USDT"):
    return await fetch_ticker(symbol)

async def enviar_ordem_market(symbol: str, side: str, amount: float):
    return await create_order(symbol, "market", side, amount)

async def enviar_ordem_limit(symbol: str, side: str, amount: float, price: float):
    return await create_order(symbol, "limit", side, amount, price)

async def obter_saldo():
    return await fetch_balance()

# Aliases para compatibilidade com TypeScript
pegarOhlcv = fetch_ohlcv
enviarOrdemMarket = enviar_ordem_market
enviarOrdemLimit = enviar_ordem_limit
fetchHistoricalData = fetch_ohlcv

# Interface CLI para interação
class ExchangeCLI:
    def __init__(self):
        self.running = True
        self.current_streams = []
    
    async def run(self):
        """Executa a interface CLI"""
        print("=" * 60)
        print("🔗 BINANCE EXCHANGE INTERFACE - Python Edition")
        print("=" * 60)
        
        while self.running:
            print("\n" + "=" * 40)
            print("MENU PRINCIPAL")
            print("=" * 40)
            print("1. 🔑 Configurar Credenciais")
            print("2. 📊 Ver Ticker")
            print("3. 📈 Ver OHLCV")
            print("4. 📖 Ver Order Book")
            print("5. 💰 Ver Saldo")
            print("6. 🛒 Criar Ordem")
            print("7. ❌ Cancelar Ordem")
            print("8. 📡 Stream de Preços")
            print("9. 📝 Ver Logs")
            print("10. 🧠 Estado do Núcleo AGI")
            print("0. ❌ Sair")
            print("=" * 40)
            
            choice = input("\nEscolha uma opção: ").strip()
            
            try:
                if choice == "1":
                    await self.configure_credentials()
                elif choice == "2":
                    await self.show_ticker()
                elif choice == "3":
                    await self.show_ohlcv()
                elif choice == "4":
                    await self.show_order_book()
                elif choice == "5":
                    await self.show_balance()
                elif choice == "6":
                    await self.create_order_menu()
                elif choice == "7":
                    await self.cancel_order_menu()
                elif choice == "8":
                    await self.price_stream_menu()
                elif choice == "9":
                    self.show_logs()
                elif choice == "10":
                    self.show_agi_state()
                elif choice == "0":
                    self.running = False
                    # Parar todos os streams
                    for stream_id in self.current_streams:
                        stop_price_stream(stream_id)
                    print("\n👋 Até logo!")
                else:
                    print("❌ Opção inválida!")
            
            except Exception as e:
                print(f"❌ Erro: {e}")
                logger.error(f"Erro na CLI: {e}", exc_info=True)
    
    async def configure_credentials(self):
        """Configura credenciais da API"""
        print("\n" + "=" * 40)
        print("🔑 CONFIGURAR CREDENCIAIS")
        print("=" * 40)
        
        use_env = input("Usar variáveis de ambiente? (s/n): ").strip().lower()
        
        if use_env == 's':
            api_key = os.getenv("BINANCE_API_KEY", "")
            api_secret = os.getenv("BINANCE_API_SECRET", "")
            
            if api_key and api_secret:
                set_credentials(api_key, api_secret)
                print("✅ Credenciais carregadas do ambiente")
            else:
                print("❌ Variáveis de ambiente não configuradas")
        else:
            api_key = input("API Key: ").strip()
            api_secret = input("API Secret: ").strip()
            
            if api_key and api_secret:
                set_credentials(api_key, api_secret)
                print("✅ Credenciais configuradas")
            else:
                print("⚠️ Credenciais não fornecidas - Modo simulação ativado")
    
    async def show_ticker(self):
        """Mostra ticker de um símbolo"""
        symbol = input("Símbolo (ex: BTC/USDT): ").strip() or "BTC/USDT"
        
        print(f"\n📊 Buscando ticker para {symbol}...")
        ticker = await fetch_ticker(symbol)
        
        if ticker:
            print(f"\n📈 {symbol.upper()}")
            print(f"  Último preço: ${ticker.get('last', 'N/A'):,.2f}")
            print(f"  Variação 24h: {ticker.get('percentage', 0):.2f}%")
            print(f"  Volume 24h: {ticker.get('quoteVolume', 0):,.0f} USDT")
            print(f"  Alta 24h: ${ticker.get('high', 0):,.2f}")
            print(f"  Baixa 24h: ${ticker.get('low', 0):,.2f}")
        else:
            print("❌ Não foi possível obter ticker")
    
    async def show_ohlcv(self):
        """Mostra dados OHLCV"""
        symbol = input("Símbolo (ex: BTC/USDT): ").strip() or "BTC/USDT"
        timeframe = input("Timeframe (1m, 5m, 1h, 1d): ").strip() or "1h"
        limit = int(input("Quantidade de candles: ").strip() or "10")
        
        print(f"\n📈 Buscando OHLCV para {symbol} ({timeframe})...")
        ohlcv_data = await fetch_ohlcv(symbol, timeframe, limit)
        
        if ohlcv_data:
            print(f"\n🕯️ Últimos {len(ohlcv_data)} candles:")
            for candle in ohlcv_data[-5:]:  # Mostrar últimos 5
                timestamp = datetime.fromtimestamp(candle[0] / 1000).strftime('%H:%M %d/%m')
                print(f"  {timestamp} | O:{candle[1]:.2f} H:{candle[2]:.2f} L:{candle[3]:.2f} C:{candle[4]:.2f} V:{candle[5]:.0f}")
        else:
            print("❌ Não foi possível obter dados OHLCV")
    
    async def show_order_book(self):
        """Mostra livro de ordens"""
        symbol = input("Símbolo (ex: BTC/USDT): ").strip() or "BTC/USDT"
        
        print(f"\n📖 Buscando order book para {symbol}...")
        order_book = await fetch_order_book(symbol)
        
        if order_book:
            print(f"\n🔴 ASKS (Venda):")
            for ask in order_book.asks[:5]:
                print(f"  ${ask.price:,.2f} | {ask.amount:.4f} | Total: {ask.total:,.4f}")
            
            print(f"\n🟢 BIDS (Compra):")
            for bid in reversed(order_book.bids[-5:]):
                print(f"  ${bid.price:,.2f} | {bid.amount:.4f} | Total: {bid.total:,.4f}")
        else:
            print("❌ Não foi possível obter order book")
    
    async def show_balance(self):
        """Mostra saldo da conta"""
        print("\n💰 Buscando saldo...")
        balance = await fetch_balance()
        
        if balance:
            print(f"\n💵 SALDO")
            print(f"  USDT Total: ${balance.total_usdt:,.2f}")
            print(f"  USDT Disponível: ${balance.free_usdt:,.2f}")
            print(f"  BTC Total: {balance.total_btc:.6f}")
            print(f"  BTC Disponível: {balance.free_btc:.6f}")
            print(f"  Valor Estimado Total: ${balance.estimated_total_value:,.2f}")
        else:
            print("❌ Não foi possível obter saldo")
    
    async def create_order_menu(self):
        """Menu para criar ordem"""
        print("\n" + "=" * 40)
        print("🛒 CRIAR ORDEM")
        print("=" * 40)
        
        symbol = input("Símbolo (ex: BTC/USDT): ").strip() or "BTC/USDT"
        side = input("Lado (buy/sell): ").strip().lower()
        order_type = input("Tipo (market/limit): ").strip().lower()
        amount = float(input("Quantidade: ").strip() or "0.001")
        
        price = None
        if order_type == "limit":
            price = float(input("Preço: ").strip() or "0")
        
        if side not in ["buy", "sell"]:
            print("❌ Lado inválido")
            return
        
        if order_type not in ["market", "limit"]:
            print("❌ Tipo de ordem inválido")
            return
        
        confirm = input(f"\nConfirmar ordem {side.upper()} {amount} {symbol}? (s/n): ").strip().lower()
        if confirm != 's':
            print("❌ Ordem cancelada")
            return
        
        print("\n🚀 Enviando ordem...")
        try:
            order = await create_order(symbol, order_type, side, amount, price)
            print(f"✅ Ordem executada!")
            print(f"  ID: {order.get('id')}")
            print(f"  Status: {order.get('status')}")
            print(f"  Preço: {order.get('price', 'N/A')}")
            print(f"  Quantidade: {order.get('amount')}")
        except Exception as e:
            print(f"❌ Erro na ordem: {e}")
    
    async def cancel_order_menu(self):
        """Menu para cancelar ordem"""
        print("\n" + "=" * 40)
        print("❌ CANCELAR ORDEM")
        print("=" * 40)
        
        print("1. Cancelar ordem específica")
        print("2. Cancelar todas as ordens de um símbolo")
        print("3. Voltar")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            order_id = input("ID da ordem: ").strip()
            symbol = input("Símbolo: ").strip() or "BTC/USDT"
            
            success = await cancel_order(order_id, symbol)
            if success:
                print("✅ Ordem cancelada")
            else:
                print("❌ Falha ao cancelar ordem")
        
        elif choice == "2":
            symbol = input("Símbolo: ").strip() or "BTC/USDT"
            
            confirm = input(f"Cancelar TODAS as ordens de {symbol}? (s/n): ").strip().lower()
            if confirm != 's':
                print("❌ Operação cancelada")
                return
            
            canceled = await cancel_all_orders(symbol)
            print(f"✅ {len(canceled)} ordens canceladas")
    
    async def price_stream_menu(self):
        """Menu para stream de preços"""
        print("\n" + "=" * 40)
        print("📡 STREAM DE PREÇOS")
        print("=" * 40)
        
        symbol = input("Símbolo (ex: BTC/USDT): ").strip() or "BTC/USDT"
        timeframe = input("Timeframe (ex: 15m): ").strip() or "15m"
        
        print(f"\n🎯 Iniciando stream para {symbol} ({timeframe})...")
        print("Pressione Ctrl+C para parar\n")
        
        def on_candle_update(candle: Candle):
            status = "🟢" if candle.is_final else "🟡"
            print(f"{status} {candle.time} | {candle.price:.2f} | "
                  f"O:{candle.open:.2f} H:{candle.high:.2f} L:{candle.low:.2f} V:{candle.volume:.0f}")
        
        try:
            stream_id = await exchange.start_price_stream(symbol, timeframe, on_candle_update)
            self.current_streams.append(stream_id)
            
            # Manter o stream rodando
            while stream_id in exchange.price_streams:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️ Parando stream...")
            exchange.stop_price_stream(stream_id)
            if stream_id in self.current_streams:
                self.current_streams.remove(stream_id)
    
    def show_logs(self):
        """Mostra logs recentes"""
        print("\n" + "=" * 40)
        print("📝 LOGS RECENTES")
        print("=" * 40)
        
        with logs_lock:
            recent_logs = logs[:20]  # Últimos 20 logs
        
        if not recent_logs:
            print("Nenhum log disponível")
            return
        
        for log_entry in recent_logs:
            level_emoji = {
                LogLevel.INFO: "ℹ️",
                LogLevel.WARNING: "⚠️",
                LogLevel.ERROR: "❌",
                LogLevel.SUCCESS: "✅"
            }
            time_str = log_entry.timestamp.strftime("%H:%M:%S")
            print(f"{level_emoji.get(log_entry.level, '📝')} [{time_str}] {log_entry.message}")
    
    def show_agi_state(self):
        """Mostra estado do núcleo AGI"""
        print("\n" + "=" * 40)
        print("🧠 ESTADO DO NÚCLEO AGI")
        print("=" * 40)
        
        state = sentient_core.get_state()
        emotion = sentient_core.get_vector()
        thoughts = sentient_core.get_thoughts()
        
        state_emoji = {
            "STABLE": "🟢",
            "EXCITED": "🎉",
            "STRESSED": "😰",
            "DORMANT": "💤",
            "FRACTURED": "💔"
        }
        
        print(f"Estado: {state_emoji.get(state, '❓')} {state}")
        print(f"Estabilidade emocional: {emotion.get('stability', 100)}/100")
        
        print(f"\n💭 Últimos pensamentos:")
        for thought in thoughts[-5:]:  # Últimos 5 pensamentos
            print(f"  {thought}")

# Função principal assíncrona
async def main():
    """Função principal"""
    print("Inicializando Interface Binance...")
    
    # Criar e executar CLI
    cli = ExchangeCLI()
    await cli.run()

# Executar se este arquivo for o principal
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        logger.error(f"Erro fatal: {e}", exc_info=True)