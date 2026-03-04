"""
Market Monitor - Sistema de Monitoramento Contínuo do Mercado
=============================================================
Monitora múltiplos mercados em tempo real, detecta oportunidades,
gera alertas e sinais de trading automaticamente
"""

import threading
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from loguru import logger
except ImportError:
    import logging as logger_module
    logger = logger_module.getLogger(__name__)


class AlertSeverity(Enum):
    """Severidade de alertas"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class MarketCondition(Enum):
    """Condições de mercado"""
    TRENDING_UP = "TRENDING_UP"
    TRENDING_DOWN = "TRENDING_DOWN"
    RANGING = "RANGING"
    BREAKOUT = "BREAKOUT"
    BREAKDOWN = "BREAKDOWN"
    CONSOLIDATION = "CONSOLIDATION"
    VOLATILE = "VOLATILE"
    CALM = "CALM"


@dataclass
class MarketAlert:
    """Alerta de mercado"""
    timestamp: datetime
    symbol: str
    severity: AlertSeverity
    alert_type: str
    message: str
    price: float
    condition: MarketCondition
    data: Dict


@dataclass
class PriceLevel:
    """Nível de preço importante"""
    symbol: str
    level_type: str  # 'SUPPORT', 'RESISTANCE'
    price: float
    strength: float  # 0-100
    touches: int
    first_touch: datetime
    last_touch: datetime


@dataclass
class MarketMetrics:
    """Métricas de mercado"""
    symbol: str
    timestamp: datetime
    current_price: float
    high_24h: float
    low_24h: float
    volume_24h: float
    volatility: float
    trend_strength: float
    momentum: float
    rsi: float
    macd: float


class MarketMonitor:
    """
    Monitor de mercado que executa análise contínua e detecta oportunidades
    """

    def __init__(self, symbols: List[str], update_frequency: int = 60):
        """
        Args:
            symbols: Lista de símbolos para monitorar
            update_frequency: Frequência de atualização em segundos
        """
        self.symbols = symbols
        self.update_frequency = update_frequency
        self.is_running = False
        self._stop_event = threading.Event()
        self._monitor_thread = None
        
        # Dados monitorados
        self.current_prices: Dict[str, float] = {}
        self.price_history: Dict[str, List[float]] = {s: [] for s in symbols}
        self.alerts: List[MarketAlert] = []
        self.price_levels: Dict[str, List[PriceLevel]] = {}
        self.metrics: Dict[str, MarketMetrics] = {}
        
        # Callbacks
        self._callbacks = {
            'on_price_update': [],
            'on_alert': [],
            'on_opportunity': [],
            'on_level_break': [],
        }
        
        # Configurações
        self.price_change_threshold = 0.02  # 2%
        self.volatility_threshold = 0.03  # 3%
        self.volume_threshold = 1.5  # 150% da média
        
        logger.info(f"✅ Market Monitor inicializado para {len(symbols)} símbolos")

    def register_callback(self, event_type: str, callback: Callable):
        """Registra callback para eventos"""
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)

    def _trigger_callbacks(self, event_type: str, data: Dict = None):
        """Dispara callbacks registrados"""
        if event_type in self._callbacks:
            for callback in self._callbacks[event_type]:
                try:
                    callback(data or {})
                except Exception as e:
                    logger.error(f"❌ Erro em callback {event_type}: {e}")

    def start(self):
        """Inicia o monitor"""
        if self.is_running:
            logger.warning("⚠️  Monitor já está em execução")
            return
        
        self.is_running = True
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("🔍 Market Monitor iniciado")

    def stop(self):
        """Para o monitor"""
        self.is_running = False
        self._stop_event.set()
        logger.info("🔍 Market Monitor parado")

    def _monitoring_loop(self):
        """Loop principal de monitoramento"""
        while not self._stop_event.is_set():
            try:
                for symbol in self.symbols:
                    try:
                        # Coletar dados de mercado
                        market_data = self._fetch_market_data(symbol)
                        if market_data:
                            self._process_market_data(symbol, market_data)
                            self._detect_opportunities(symbol, market_data)
                            self._detect_alerts(symbol, market_data)
                    
                    except Exception as e:
                        logger.error(f"❌ Erro ao monitorar {symbol}: {e}")
                
                time.sleep(self.update_frequency)
            
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}")
                time.sleep(5)

    def _fetch_market_data(self, symbol: str) -> Optional[Dict]:
        """Busca dados de mercado (implementar com API real)"""
        # Placeholder - implementar com API real
        try:
            # Exemplo com yfinance
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1h')
            
            if data.empty:
                return None
            
            last_row = data.iloc[-1]
            return {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'price': float(last_row['Close']),
                'high': float(last_row['High']),
                'low': float(last_row['Low']),
                'volume': float(last_row['Volume']),
                'open': float(last_row['Open']),
            }
        except Exception as e:
            logger.debug(f"⚠️  Não foi possível buscar dados para {symbol}: {e}")
            return None

    def _process_market_data(self, symbol: str, data: Dict):
        """Processa dados de mercado recebidos"""
        price = data.get('price', 0)
        
        # Atualizar preço atual
        old_price = self.current_prices.get(symbol, price)
        self.current_prices[symbol] = price
        
        # Atualizar histórico
        self.price_history[symbol].append(price)
        if len(self.price_history[symbol]) > 1000:
            self.price_history[symbol].pop(0)
        
        # Calcular métricas
        metrics = self._calculate_metrics(symbol, data)
        self.metrics[symbol] = metrics
        
        # Disparar callback
        self._trigger_callbacks('on_price_update', {
            'symbol': symbol,
            'price': price,
            'change': price - old_price,
            'change_pct': ((price - old_price) / old_price * 100) if old_price else 0,
        })

    def _calculate_metrics(self, symbol: str, data: Dict) -> MarketMetrics:
        """Calcula métricas de mercado"""
        history = self.price_history.get(symbol, [])
        
        # Volatilidade simples
        if len(history) > 1:
            returns = [(history[i] - history[i-1]) / history[i-1] for i in range(1, len(history))]
            volatility = sum(r**2 for r in returns) ** 0.5 / len(returns) if returns else 0
        else:
            volatility = 0
        
        # Tendência
        if len(history) > 20:
            recent_avg = sum(history[-10:]) / 10
            old_avg = sum(history[-20:-10]) / 10
            trend_strength = abs(recent_avg - old_avg) / old_avg if old_avg else 0
        else:
            trend_strength = 0
        
        return MarketMetrics(
            symbol=symbol,
            timestamp=datetime.now(),
            current_price=data.get('price', 0),
            high_24h=data.get('high', 0),
            low_24h=data.get('low', 0),
            volume_24h=data.get('volume', 0),
            volatility=volatility,
            trend_strength=trend_strength,
            momentum=0,  # Implementar cálculo
            rsi=0,  # Implementar cálculo
            macd=0,  # Implementar cálculo
        )

    def _detect_opportunities(self, symbol: str, data: Dict):
        """Detecta oportunidades de trading"""
        metrics = self.metrics.get(symbol)
        if not metrics:
            return
        
        opportunities = []
        
        # Opportunity 1: Quebra de resistência
        if metrics.trend_strength > 0.05 and metrics.volatility < 0.02:
            opportunities.append({
                'type': 'BREAKOUT',
                'confidence': 0.8,
                'suggestion': 'BUY',
                'reason': 'Forte tendência de alta com volatilidade baixa'
            })
        
        # Opportunity 2: Volatilidade extrema
        if metrics.volatility > self.volatility_threshold:
            opportunities.append({
                'type': 'HIGH_VOLATILITY',
                'confidence': 0.7,
                'suggestion': 'CAUTION',
                'reason': 'Volatilidade anormalmente alta'
            })
        
        # Opportunity 3: Volume alto
        if data.get('volume', 0) > self.volume_threshold:
            opportunities.append({
                'type': 'HIGH_VOLUME',
                'confidence': 0.7,
                'suggestion': 'WATCH',
                'reason': 'Volume acima da média'
            })
        
        if opportunities:
            self._trigger_callbacks('on_opportunity', {
                'symbol': symbol,
                'opportunities': opportunities,
                'timestamp': datetime.now(),
            })

    def _detect_alerts(self, symbol: str, data: Dict):
        """Detecta e gera alertas"""
        price = data.get('price', 0)
        old_price = self.current_prices.get(symbol, price)
        
        # Alerta 1: Mudança de preço significativa
        if old_price and abs(price - old_price) / old_price > self.price_change_threshold:
            alert = MarketAlert(
                timestamp=datetime.now(),
                symbol=symbol,
                severity=AlertSeverity.WARNING,
                alert_type='PRICE_JUMP',
                message=f"Salto de preço: {abs((price-old_price)/old_price*100):.2f}%",
                price=price,
                condition=MarketCondition.VOLATILE,
                data={'old_price': old_price, 'new_price': price}
            )
            self.alerts.append(alert)
            self._trigger_callbacks('on_alert', asdict(alert))
            logger.warning(f"⚠️  ALERTA {symbol}: {alert.message}")

    def get_summary(self, symbol: str) -> Dict:
        """Retorna resumo do mercado para um símbolo"""
        metrics = self.metrics.get(symbol)
        if not metrics:
            return {}
        
        return {
            'symbol': symbol,
            'price': metrics.current_price,
            'volatility': f"{metrics.volatility*100:.2f}%",
            'trend_strength': f"{metrics.trend_strength*100:.2f}%",
            'volume_24h': metrics.volume_24h,
            'high_24h': metrics.high_24h,
            'low_24h': metrics.low_24h,
        }

    def get_all_summaries(self) -> Dict[str, Dict]:
        """Retorna resumos de todos os símbolos"""
        return {symbol: self.get_summary(symbol) for symbol in self.symbols}

    def export_alerts(self, filepath: str):
        """Exporta alertas para arquivo"""
        try:
            alerts_data = [asdict(a) for a in self.alerts]
            with open(filepath, 'w') as f:
                json.dump(alerts_data, f, indent=2, default=str)
            logger.info(f"💾 {len(self.alerts)} alertas exportados para {filepath}")
        except Exception as e:
            logger.error(f"❌ Erro ao exportar alertas: {e}")
