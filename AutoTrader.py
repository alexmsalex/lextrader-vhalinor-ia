"""
AutoTrader - Sistema Avançado de Trading Automatizado
Sistema completo de trading com suporte a múltiplas estratégias,
gerenciamento de risco e backtesting.
"""

# Imports padrão
import os
import sys
import csv
import uuid
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any

# Imports de terceiros
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Imports condicionais (com tratamento de erro)
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("⚠️ python-dotenv não instalado. Use: pip install python-dotenv")

try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    import logging
    logger = logging.getLogger(__name__)
    print("⚠️ loguru não instalado. Use: pip install loguru")

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance não instalado. Use: pip install yfinance")

try:
    from binance.client import Client as BinanceClient
    BINANCE_AVAILABLE = True
except ImportError:
    BINANCE_AVAILABLE = False
    print("⚠️ python-binance não instalado. Use: pip install python-binance")

try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    print("⚠️ ccxt não instalado. Use: pip install ccxt")

try:
    import ta
    TA_AVAILABLE = True
except ImportError:
    TA_AVAILABLE = False
    print("⚠️ ta não instalado. Use: pip install ta")

try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    print("⚠️ schedule não instalado. Use: pip install schedule")

# Carregar variáveis de ambiente
if DOTENV_AVAILABLE:
    load_dotenv()


# ============================================================================
# CONFIGURAÇÕES E ENUMS
# ============================================================================

class TradingMode(Enum):
    """Modos de operação do trader"""
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"


class TimeFrame(Enum):
    """Timeframes disponíveis"""
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"


@dataclass
class BrokerConfig:
    """Configuração de broker"""
    name: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    testnet: bool = True


@dataclass
class TradingConfig:
    """Configuração de trading"""
    initial_balance: float = 10000
    risk_per_trade: float = 0.02  # 2%
    max_positions: int = 5
    stop_loss_pct: float = 0.02  # 2%
    take_profit_pct: float = 0.04  # 4%
    trailing_stop: bool = True
    trailing_distance: float = 0.01  # 1%
    use_pyramiding: bool = False
    max_daily_trades: int = 10


@dataclass
class Position:
    """Representa uma posição de trading"""
    symbol: str
    entry_price: float
    size: float
    side: str  # 'BUY' or 'SELL'
    stop_loss: float
    take_profit: float
    timestamp: datetime
    position_id: str


# ============================================================================
# LOGGER
# ============================================================================

class TradingLogger:
    """Sistema de logging para trading"""

    def __init__(self, log_level: str = "INFO"):
        if LOGURU_AVAILABLE:
            logger.remove()

            # Console output
            logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                       "<level>{level: <8}</level> | "
                       "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
                       "<cyan>{line}</cyan> - <level>{message}</level>",
                level=log_level
            )

            # File output
            log_file = f"logs/trading_{datetime.now().strftime('%Y%m%d')}.log"
            os.makedirs("logs", exist_ok=True)
            logger.add(
                log_file,
                rotation="500 MB",
                retention="30 days",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                       "{name}:{function}:{line} - {message}",
                level="INFO"
            )

            self.logger = logger
        else:
            # Fallback para logging padrão
            logging.basicConfig(
                level=getattr(logging, log_level),
                format='%(asctime)s | %(levelname)-8s | %(message)s'
            )
            self.logger = logging.getLogger(__name__)

    def get_logger(self):
        """Retorna instância do logger"""
        return self.logger


# ============================================================================
# DATA FEEDS
# ============================================================================

class DataFeed(ABC):
    """Classe abstrata para diferentes fontes de dados"""

    @abstractmethod
    def get_historical_data(self, symbol: str, timeframe: str,
                          limit: int) -> pd.DataFrame:
        """Obtém dados históricos"""

    @abstractmethod
    def get_realtime_data(self, symbol: str, callback):
        """Obtém dados em tempo real"""


class BinanceDataFeed(DataFeed):
    """Data feed para Binance"""

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        if not BINANCE_AVAILABLE:
            raise ImportError("python-binance não está instalado")

        self.client = BinanceClient(api_key, api_secret, testnet=testnet)

    def get_historical_data(self, symbol: str, timeframe: str,
                          limit: int = 500) -> pd.DataFrame:
        """Obtém dados históricos da Binance"""
        klines = self.client.get_klines(
            symbol=symbol,
            interval=timeframe,
            limit=limit
        )

        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].astype(float)

        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    def get_realtime_data(self, symbol: str, callback):
        """Implementar WebSocket para dados em tempo real"""
        # TODO: Implementar WebSocket
        pass


class YahooDataFeed(DataFeed):
    """Data feed para Yahoo Finance"""

    def __init__(self):
        if not YFINANCE_AVAILABLE:
            raise ImportError("yfinance não está instalado")

    def get_historical_data(self, symbol: str, timeframe: str,
                          limit: int = 500) -> pd.DataFrame:
        """Obtém dados históricos do Yahoo Finance"""
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=f"{limit}d", interval=timeframe)
        df.reset_index(inplace=True)
        return df

    def get_realtime_data(self, symbol: str, callback):
        """Yahoo Finance não suporta dados em tempo real"""
        raise NotImplementedError("Yahoo Finance não suporta dados em tempo real")


# ============================================================================
# INDICADORES TÉCNICOS
# ============================================================================

class TechnicalIndicators:
    """Calculadora de indicadores técnicos"""

    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Calcula todos os indicadores técnicos"""
        if not TA_AVAILABLE:
            logger.warning("Biblioteca 'ta' não disponível. "
                         "Indicadores não serão calculados.")
            return df

        df = df.copy()

        # RSI
        df['rsi'] = ta.momentum.RSIIndicator(
            df['close'], window=14
        ).rsi()

        # Médias móveis
        df['sma_20'] = ta.trend.SMAIndicator(
            df['close'], window=20
        ).sma_indicator()
        df['sma_50'] = ta.trend.SMAIndicator(
            df['close'], window=50
        ).sma_indicator()
        df['ema_12'] = ta.trend.EMAIndicator(
            df['close'], window=12
        ).ema_indicator()
        df['ema_26'] = ta.trend.EMAIndicator(
            df['close'], window=26
        ).ema_indicator()

        # MACD
        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_width'] = bb.bollinger_wband()

        # ATR para volatilidade
        df['atr'] = ta.volatility.AverageTrueRange(
            df['high'], df['low'], df['close'], window=14
        ).average_true_range()

        # Volume
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']

        # Suporte e Resistência
        support, resistance = TechnicalIndicators.calculate_support_resistance(df)
        df['support'] = support
        df['resistance'] = resistance

        return df

    @staticmethod
    def calculate_support_resistance(df: pd.DataFrame,
                                   window: int = 20) -> Tuple[pd.Series, pd.Series]:
        """Calcula níveis de suporte e resistência"""
        support = df['low'].rolling(window=window, center=True).min()
        resistance = df['high'].rolling(window=window, center=True).max()
        return support, resistance


# ============================================================================
# GERENCIAMENTO DE RISCO
# ============================================================================

class RiskManager:
    """Gerenciador de risco"""

    def __init__(self, config: TradingConfig):
        self.config = config
        self.open_positions: List[Position] = []
        self.daily_trades = 0
        self.daily_pnl = 0

    def calculate_position_size(self, balance: float, entry_price: float,
                              stop_loss_price: float) -> float:
        """Calcula tamanho da posição baseado no risco"""
        risk_amount = balance * self.config.risk_per_trade
        risk_per_share = abs(entry_price - stop_loss_price)

        if risk_per_share == 0:
            return 0

        position_size = risk_amount / risk_per_share
        return round(position_size, 8)  # Para cripto

    def validate_trade(self, symbol: str, side: str, size: float) -> bool:
        """Valida se o trade pode ser executado"""
        # Verificar número máximo de posições
        if len(self.open_positions) >= self.config.max_positions:
            return False

        # Verificar trades diários
        if self.daily_trades >= self.config.max_daily_trades:
            return False

        # Verificar se já existe posição no mesmo símbolo
        existing_positions = [p for p in self.open_positions if p.symbol == symbol]
        if existing_positions and not self.config.use_pyramiding:
            return False

        return True

    def calculate_stop_loss(self, entry_price: float, side: str) -> float:
        """Calcula stop loss dinâmico"""
        if side == 'BUY':
            return entry_price * (1 - self.config.stop_loss_pct)
        return entry_price * (1 + self.config.stop_loss_pct)

    def calculate_take_profit(self, entry_price: float, side: str) -> float:
        """Calcula take profit dinâmico"""
        if side == 'BUY':
            return entry_price * (1 + self.config.take_profit_pct)
        return entry_price * (1 - self.config.take_profit_pct)


# ============================================================================
# ESTRATÉGIAS DE TRADING
# ============================================================================

class TradingStrategy(ABC):
    """Classe abstrata para estratégias de trading"""

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Gera sinal de trading"""


class EMACrossoverStrategy(TradingStrategy):
    """Estratégia de cruzamento de EMAs"""

    def __init__(self, fast_period: int = 12, slow_period: int = 26):
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signal(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Gera sinal baseado em cruzamento de EMAs"""
        if len(df) < self.slow_period:
            return {'signal': 'HOLD', 'strength': 0}

        # Calcular EMAs
        fast_ema = df['close'].ewm(span=self.fast_period).mean()
        slow_ema = df['close'].ewm(span=self.slow_period).mean()

        current_fast = fast_ema.iloc[-1]
        current_slow = slow_ema.iloc[-1]
        previous_fast = fast_ema.iloc[-2]
        previous_slow = slow_ema.iloc[-2]

        # Gerar sinal
        if current_fast > current_slow and previous_fast <= previous_slow:
            return {'signal': 'BUY', 'strength': 1.0}
        if current_fast < current_slow and previous_fast >= previous_slow:
            return {'signal': 'SELL', 'strength': 1.0}
        return {'signal': 'HOLD', 'strength': 0}


class RSIStrategy(TradingStrategy):
    """Estratégia baseada em RSI"""

    def __init__(self, oversold: int = 30, overbought: int = 70):
        self.oversold = oversold
        self.overbought = overbought

    def generate_signal(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Gera sinal baseado em RSI"""
        if 'rsi' not in df.columns:
            return {'signal': 'HOLD', 'strength': 0}

        rsi = df['rsi'].iloc[-1]

        if rsi < self.oversold:
            strength = (self.oversold - rsi) / self.oversold
            return {'signal': 'BUY', 'strength': strength}
        if rsi > self.overbought:
            strength = (rsi - self.overbought) / (100 - self.overbought)
            return {'signal': 'SELL', 'strength': strength}
        return {'signal': 'HOLD', 'strength': 0}


# ============================================================================
# AUTO TRADER PRINCIPAL
# ============================================================================

class EnhancedAutoTrader:
    """Sistema principal de trading automatizado"""

    def __init__(self, config: TradingConfig, data_feed: DataFeed,
                 strategy: TradingStrategy, mode: TradingMode = TradingMode.PAPER):

        self.config = config
        self.data_feed = data_feed
        self.strategy = strategy
        self.mode = mode

        # Inicializar componentes
        self.logger = TradingLogger().get_logger()
        self.risk_manager = RiskManager(config)
        self.indicators = TechnicalIndicators()

        # Estado do trader
        self.balance = config.initial_balance
        self.equity = config.initial_balance
        self.portfolio = {}
        self.trade_history = []
        self.symbols = ['BTCUSDT', 'ETHUSDT']  # Símbolos para monitorar

        self.logger.info(f"AutoTrader inicializado em modo {mode.value}")
        self.logger.info(f"Saldo inicial: ${self.balance:.2f}")

    def run(self):
        """Executa o trader"""
        if self.mode == TradingMode.BACKTEST:
            self.run_backtest()
        else:
            self.run_live()

    def run_live(self):
        """Executa trading em tempo real"""
        if not SCHEDULE_AVAILABLE:
            self.logger.error("Biblioteca 'schedule' não disponível")
            return

        self.logger.info("Iniciando trading em tempo real...")

        # Agendar execução periódica
        schedule.every(5).minutes.do(self.trading_cycle)

        # Loop principal
        while True:
            schedule.run_pending()
            time.sleep(1)

    def trading_cycle(self):
        """Ciclo completo de trading"""
        try:
            self.logger.info("Executando ciclo de trading...")

            # 1. Coletar dados
            for symbol in self.symbols:
                df = self.data_feed.get_historical_data(symbol, '1h', 100)

                if df.empty:
                    continue

                # 2. Calcular indicadores
                df = self.indicators.calculate_all_indicators(df)

                # 3. Gerar sinal
                signal = self.strategy.generate_signal(df)

                # 4. Executar trade se houver sinal
                if signal['signal'] != 'HOLD':
                    self.execute_trade(symbol, df, signal)

                # 5. Gerenciar posições abertas
                self.manage_positions(symbol, df)

            # 6. Atualizar equity
            self.update_equity()

            # 7. Log de desempenho
            self.log_performance()

        except Exception as e:
            self.logger.error(f"Erro no ciclo de trading: {e}")

    def execute_trade(self, symbol: str, df: pd.DataFrame, signal: Dict):
        """Executa um trade"""
        current_price = df['close'].iloc[-1]
        side = signal['signal']

        # Validar trade
        if not self.risk_manager.validate_trade(symbol, side, 1):
            return

        # Calcular parâmetros do trade
        stop_loss = self.risk_manager.calculate_stop_loss(current_price, side)
        take_profit = self.risk_manager.calculate_take_profit(current_price, side)
        position_size = self.risk_manager.calculate_position_size(
            self.balance, current_price, stop_loss
        )

        if position_size <= 0:
            return

        # Criar posição
        position = Position(
            symbol=symbol,
            entry_price=current_price,
            size=position_size,
            side=side,
            stop_loss=stop_loss,
            take_profit=take_profit,
            timestamp=datetime.now(),
            position_id=str(uuid.uuid4())
        )

        # Adicionar ao gerenciador de risco
        self.risk_manager.open_positions.append(position)

        # Atualizar saldo (modo paper)
        if side == 'BUY':
            self.balance -= position_size * current_price
        else:
            self.balance += position_size * current_price

        # Registrar trade
        trade_record = {
            'timestamp': datetime.now(),
            'symbol': symbol,
            'side': side,
            'price': current_price,
            'size': position_size,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'balance': self.balance
        }

        self.trade_history.append(trade_record)
        self.logger.info(f"Trade executado: {side} {symbol} @ ${current_price:.2f}")

    def manage_positions(self, symbol: str, df: pd.DataFrame):
        """Gerencia posições abertas"""
        current_price = df['close'].iloc[-1]

        for position in self.risk_manager.open_positions[:]:
            if position.symbol != symbol:
                continue

            # Verificar stop loss
            if ((position.side == 'BUY' and current_price <= position.stop_loss) or
                (position.side == 'SELL' and current_price >= position.stop_loss)):
                self.close_position(position, current_price, 'STOP_LOSS')

            # Verificar take profit
            elif ((position.side == 'BUY' and current_price >= position.take_profit) or
                  (position.side == 'SELL' and current_price <= position.take_profit)):
                self.close_position(position, current_price, 'TAKE_PROFIT')

            # Atualizar trailing stop
            elif self.config.trailing_stop:
                self.update_trailing_stop(position, current_price)

    def close_position(self, position: Position, exit_price: float, reason: str):
        """Fecha uma posição"""
        # Calcular P&L
        if position.side == 'BUY':
            pnl = (exit_price - position.entry_price) * position.size
        else:
            pnl = (position.entry_price - exit_price) * position.size

        # Atualizar saldo
        self.balance += position.size * exit_price

        # Remover posição
        if position in self.risk_manager.open_positions:
            self.risk_manager.open_positions.remove(position)

        # Registrar fechamento
        self.logger.info(f"Posição fechada: {position.symbol} | "
                        f"P&L: ${pnl:.2f} | Motivo: {reason}")

    def update_trailing_stop(self, position: Position, current_price: float):
        """Atualiza trailing stop"""
        if position.side == 'BUY':
            new_stop = current_price * (1 - self.config.trailing_distance)
            if new_stop > position.stop_loss:
                position.stop_loss = new_stop
        else:
            new_stop = current_price * (1 + self.config.trailing_distance)
            if new_stop < position.stop_loss:
                position.stop_loss = new_stop

    def update_equity(self):
        """Atualiza equity total"""
        open_positions_value = 0

        for position in self.risk_manager.open_positions:
            # Em um sistema real, buscar preço atual de cada posição
            open_positions_value += position.size * position.entry_price

        self.equity = self.balance + open_positions_value

    def log_performance(self):
        """Registra desempenho atual"""
        performance = {
            'timestamp': datetime.now(),
            'balance': self.balance,
            'equity': self.equity,
            'open_positions': len(self.risk_manager.open_positions),
            'total_trades': len(self.trade_history)
        }

        self.logger.info(f"Performance: Balance=${self.balance:.2f}, "
                        f"Equity=${self.equity:.2f}, "
                        f"Positions={len(self.risk_manager.open_positions)}")

        # Salvar em arquivo
        self.save_performance_log(performance)

    def save_performance_log(self, performance: Dict):
        """Salva log de desempenho em CSV"""
        file_path = f"performance_{datetime.now().strftime('%Y%m%d')}.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=performance.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(performance)

    def run_backtest(self, start_date: str = None, end_date: str = None):
        """Executa backtesting"""
        self.logger.info(f"Iniciando backtest de {start_date} a {end_date}")

        # TODO: Implementar lógica de backtesting completa

        self.generate_backtest_report()

    def generate_backtest_report(self):
        """Gera relatório de backtesting"""
        if not self.trade_history:
            return

        # Calcular métricas
        total_trades = len(self.trade_history)
        winning_trades = len([
            t for t in self.trade_history if
            (t['side'] == 'BUY' and t.get('exit_price', 0) > t['price']) or
            (t['side'] == 'SELL' and t.get('exit_price', 0) < t['price'])
        ])

        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        total_pnl = self.equity - self.config.initial_balance
        roi = (total_pnl / self.config.initial_balance * 100)

        # Gerar gráficos
        self.plot_performance()

        self.logger.info("Backtest Report:")
        self.logger.info(f"Total Trades: {total_trades}")
        self.logger.info(f"Win Rate: {win_rate:.2f}%")
        self.logger.info(f"Total P&L: ${total_pnl:.2f}")
        self.logger.info(f"ROI: {roi:.2f}%")

    def plot_performance(self):
        """Gera gráficos de desempenho"""
        sns.set_style("whitegrid")

        # Gráfico de equity curve
        if len(self.trade_history) > 0:
            dates = [t['timestamp'] for t in self.trade_history]
            balances = [t['balance'] for t in self.trade_history]

            plt.figure(figsize=(12, 6))
            plt.plot(dates, balances, linewidth=2)
            plt.title('Equity Curve', fontsize=14)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Balance ($)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('equity_curve.png', dpi=300)
            plt.close()


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal para executar o trader"""

    # Configuração
    config = TradingConfig(
        initial_balance=10000,
        risk_per_trade=0.02,
        max_positions=3,
        stop_loss_pct=0.015,
        take_profit_pct=0.03,
        trailing_stop=True
    )

    # Configurar fonte de dados (usar variáveis de ambiente)
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        print("⚠️ Configure as variáveis de ambiente:")
        print("   BINANCE_API_KEY")
        print("   BINANCE_API_SECRET")
        return

    # Criar data feed
    try:
        data_feed = BinanceDataFeed(api_key, api_secret, testnet=True)
    except ImportError as e:
        print(f"❌ Erro ao criar data feed: {e}")
        return

    # Criar estratégia
    strategy = EMACrossoverStrategy(fast_period=12, slow_period=26)

    # Criar e executar trader
    trader = EnhancedAutoTrader(
        config=config,
        data_feed=data_feed,
        strategy=strategy,
        mode=TradingMode.PAPER
    )

    # Executar
    try:
        trader.run()
    except KeyboardInterrupt:
        print("\n⏹️ Trader interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
