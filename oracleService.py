import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging
from abc import ABC, abstractmethod
import numpy as np
from collections import defaultdict
import json
import httpx
from dataclasses_json import dataclass_json
import aiohttp
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enums e Tipos
class OracleSourceType(Enum):
    TRADINGVIEW = "TRADINGVIEW"
    YFINANCE = "YFINANCE"
    GLASSNODE = "GLASSNODE"
    SANTIMENT = "SANTIMENT"
    COINGLASS = "COINGLASS"
    INTOTHEBLOCK = "INTOTHEBLOCK"
    MESSARI = "MESSARI"
    CRYPTOCOMPARE = "CRYPTOCOMPARE"
    COINMETRICS = "COINMETRICS"
    DEFIPULSE = "DEFIPULSE"
    BYBIT = "BYBIT"
    COINBASE = "COINBASE"

class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"

class SourceReliability(Enum):
    HIGH = "HIGH"      # Dados em tempo real, APIs confiáveis
    MEDIUM = "MEDIUM"  # Dados com pequeno atraso
    LOW = "LOW"        # Dados estimados/simulados

# Estruturas de dados
@dataclass_json
@dataclass
class OracleSignal:
    source: OracleSourceType
    signal: SignalType
    score: float  # 0-100
    metadata: Dict[str, Any]
    latency: int  # ms
    timestamp: datetime
    reliability: SourceReliability
    confidence: float = 1.0  # 0-1
    weight: float = 1.0  # Peso no consenso
    
    def __post_init__(self):
        if isinstance(self.source, str):
            self.source = OracleSourceType(self.source)
        if isinstance(self.signal, str):
            self.signal = SignalType(self.signal)
        if isinstance(self.reliability, str):
            self.reliability = SourceReliability(self.reliability)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source.value,
            'signal': self.signal.value,
            'score': self.score,
            'metadata': self.metadata,
            'latency': self.latency,
            'timestamp': self.timestamp.isoformat(),
            'reliability': self.reliability.value,
            'confidence': self.confidence,
            'weight': self.weight
        }

@dataclass_json
@dataclass
class OracleConsensus:
    overall_score: float  # 0-100
    bullish_count: int
    bearish_count: int
    neutral_count: int
    primary_driver: OracleSourceType
    signals: List[OracleSignal]
    timestamp: datetime
    sentiment: str  # "BULLISH", "BEARISH", "NEUTRAL"
    confidence_level: float  # 0-1
    weighted_score: float  # Score ponderado
    market_phase: str = "UNKNOWN"
    
    def __post_init__(self):
        if isinstance(self.primary_driver, str):
            self.primary_driver = OracleSourceType(self.primary_driver)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'overall_score': self.overall_score,
            'bullish_count': self.bullish_count,
            'bearish_count': self.bearish_count,
            'neutral_count': self.neutral_count,
            'primary_driver': self.primary_driver.value,
            'signals': [s.to_dict() for s in self.signals],
            'timestamp': self.timestamp.isoformat(),
            'sentiment': self.sentiment,
            'confidence_level': self.confidence_level,
            'weighted_score': self.weighted_score,
            'market_phase': self.market_phase
        }

@dataclass
class HistoricalConsensus:
    timestamp: datetime
    symbol: str
    consensus: OracleConsensus
    actual_price_change: Optional[float] = None
    prediction_accuracy: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'symbol': self.symbol,
            'consensus': self.consensus.to_dict(),
            'actual_price_change': self.actual_price_change,
            'prediction_accuracy': self.prediction_accuracy
        }

@dataclass
class OracleConfig:
    """Configuração dos oráculos"""
    # Tempos de cache (em segundos)
    cache_durations: Dict[OracleSourceType, int] = field(default_factory=lambda: {
        OracleSourceType.TRADINGVIEW: 60,
        OracleSourceType.YFINANCE: 300,
        OracleSourceType.GLASSNODE: 900,
        OracleSourceType.SANTIMENT: 300,
        OracleSourceType.COINGLASS: 120,
        OracleSourceType.INTOTHEBLOCK: 600,
        OracleSourceType.MESSARI: 1200
    })
    
    # Pesos por fonte (0-2)
    source_weights: Dict[OracleSourceType, float] = field(default_factory=lambda: {
        OracleSourceType.TRADINGVIEW: 1.2,
        OracleSourceType.YFINANCE: 1.0,
        OracleSourceType.GLASSNODE: 1.5,
        OracleSourceType.SANTIMENT: 1.0,
        OracleSourceType.COINGLASS: 1.3,
        OracleSourceType.INTOTHEBLOCK: 1.4,
        OracleSourceType.MESSARI: 1.1
    })
    
    # Confiabilidade padrão
    source_reliability: Dict[OracleSourceType, SourceReliability] = field(default_factory=lambda: {
        OracleSourceType.TRADINGVIEW: SourceReliability.HIGH,
        OracleSourceType.YFINANCE: SourceReliability.MEDIUM,
        OracleSourceType.GLASSNODE: SourceReliability.HIGH,
        OracleSourceType.SANTIMENT: SourceReliability.MEDIUM,
        OracleSourceType.COINGLASS: SourceReliability.HIGH,
        OracleSourceType.INTOTHEBLOCK: SourceReliability.HIGH,
        OracleSourceType.MESSARI: SourceReliability.HIGH
    })
    
    # Thresholds
    strong_buy_threshold: float = 70.0
    strong_sell_threshold: float = 30.0
    buy_threshold: float = 55.0
    sell_threshold: float = 45.0

# Base para oráculos
class BaseOracle(ABC):
    """Classe base para todos os oráculos"""
    
    def __init__(self, source_type: OracleSourceType, config: OracleConfig):
        self.source_type = source_type
        self.config = config
        self.cache: Dict[str, Tuple[OracleSignal, float]] = {}
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = datetime.min
    
    @abstractmethod
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Busca sinal da fonte"""
        pass
    
    async def get_signal(self, symbol: str) -> OracleSignal:
        """Obtém sinal com cache"""
        cache_key = f"{symbol}_{self.source_type.value}"
        current_time = time.time()
        
        # Verificar cache
        if cache_key in self.cache:
            signal, cache_time = self.cache[cache_key]
            cache_duration = self.config.cache_durations.get(self.source_type, 300)
            
            if current_time - cache_time < cache_duration:
                logger.debug(f"Usando cache para {self.source_type.value}: {symbol}")
                return signal
        
        try:
            # Buscar novo sinal
            self.request_count += 1
            signal = await self.fetch_signal(symbol)
            signal.timestamp = datetime.now()
            
            # Atualizar cache
            self.cache[cache_key] = (signal, current_time)
            self.last_request_time = datetime.now()
            
            return signal
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Erro em {self.source_type.value} para {symbol}: {e}")
            
            # Fallback para dados simulados
            return await self._get_fallback_signal(symbol)
    
    async def _get_fallback_signal(self, symbol: str) -> OracleSignal:
        """Sinal de fallback quando a API falha"""
        return OracleSignal(
            source=self.source_type,
            signal=SignalType.NEUTRAL,
            score=50.0,
            metadata={"error": "API offline", "fallback": True},
            latency=1000,
            timestamp=datetime.now(),
            reliability=SourceReliability.LOW,
            confidence=0.3,
            weight=0.5
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do oráculo"""
        return {
            'source': self.source_type.value,
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.request_count, 1),
            'last_request': self.last_request_time.isoformat() if self.last_request_time > datetime.min else None,
            'cache_size': len(self.cache)
        }

# Implementações dos oráculos
class TradingViewOracle(BaseOracle):
    """Oracle do TradingView (Análise Técnica)"""
    
    def __init__(self, config: OracleConfig):
        super().__init__(OracleSourceType.TRADINGVIEW, config)
    
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Simula o widget de Análise Técnica do TradingView"""
        # Simular latência
        await asyncio.sleep(random.uniform(0.05, 0.2))
        
        # Gerar scores para diferentes indicadores
        rsi_score = random.uniform(0, 100)
        macd_score = random.uniform(0, 100)
        ma_score = random.uniform(0, 100)
        
        # Calcular score composto
        composite_score = (rsi_score * 0.4 + macd_score * 0.3 + ma_score * 0.3)
        
        # Determinar sinal
        if composite_score > 60:
            signal = SignalType.BUY
        elif composite_score < 40:
            signal = SignalType.SELL
        else:
            signal = SignalType.NEUTRAL
        
        # Determinar força do sinal
        if composite_score > 80:
            signal = SignalType.STRONG_BUY
        elif composite_score < 20:
            signal = SignalType.STRONG_SELL
        
        return OracleSignal(
            source=self.source_type,
            signal=signal,
            score=composite_score,
            metadata={
                "rsi": round(rsi_score, 1),
                "macd": round(macd_score, 1),
                "moving_averages": round(ma_score, 1),
                "composite_score": round(composite_score, 1),
                "timeframe": "4H",
                "indicators": ["RSI", "MACD", "MA50", "MA200"]
            },
            latency=random.randint(80, 200),
            timestamp=datetime.now(),
            reliability=self.config.source_reliability[self.source_type],
            confidence=min(0.9, composite_score / 100),
            weight=self.config.source_weights.get(self.source_type, 1.0)
        )

class YFinanceOracle(BaseOracle):
    """Oracle do Yahoo Finance (Correlações Tradicionais)"""
    
    def __init__(self, config: OracleConfig):
        super().__init__(OracleSourceType.YFINANCE, config)
    
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Simula dados do Yahoo Finance"""
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Correlação com S&P 500
        spy_correlation = random.uniform(0.3, 0.9)
        
        # Tendência do DXY (Índice Dólar)
        dxy_trend = random.choice(['UP', 'DOWN'])
        dxy_strength = random.uniform(0.1, 0.5)
        
        # Tendência do VIX (Medo)
        vix_trend = random.choice(['UP', 'DOWN'])
        
        # Lógica de sinal
        score = 50.0
        signal = SignalType.NEUTRAL
        
        # Se DXY caindo (bom para crypto) e correlação com SPY alta
        if dxy_trend == 'DOWN' and spy_correlation > 0.6:
            score = 65 + random.uniform(0, 15)
            signal = SignalType.BUY
        # Se DXY subindo (ruim para crypto)
        elif dxy_trend == 'UP':
            score = 35 - random.uniform(0, 15)
            signal = SignalType.SELL
        # Se VIX subindo (medo no mercado tradicional)
        elif vix_trend == 'UP':
            score = 40 - random.uniform(0, 10)
            signal = SignalType.SELL
        
        # Ajustar score baseado na correlação
        score = min(100, max(0, score + (spy_correlation - 0.5) * 20))
        
        return OracleSignal(
            source=self.source_type,
            signal=signal,
            score=score,
            metadata={
                "sp500_correlation": round(spy_correlation, 3),
                "dxy_trend": dxy_trend,
                "dxy_strength": round(dxy_strength, 3),
                "vix_trend": vix_trend,
                "analysis": "Correlação com mercados tradicionais",
                "market_regime": "RISK_ON" if spy_correlation > 0.7 else "RISK_OFF"
            },
            latency=random.randint(300, 600),
            timestamp=datetime.now(),
            reliability=self.config.source_reliability[self.source_type],
            confidence=abs(spy_correlation - 0.5) * 2,  # Mais confiança em correlações extremas
            weight=self.config.source_weights.get(self.source_type, 1.0)
        )

class GlassnodeOracle(BaseOracle):
    """Oracle do Glassnode (Dados On-Chain)"""
    
    def __init__(self, config: OracleConfig):
        super().__init__(OracleSourceType.GLASSNODE, config)
    
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Simula métricas on-chain do Glassnode"""
        await asyncio.sleep(random.uniform(0.2, 0.8))
        
        # NUPL (Net Unrealized Profit/Loss)
        nupl = random.uniform(0, 1)
        
        # Exchange Net Flow (positivo = entrada, negativo = saída)
        exchange_flow = random.uniform(-1000, 1000)
        
        # Supply in Profit
        supply_in_profit = random.uniform(0.5, 1.0)
        
        # MVRV Ratio
        mvrv_ratio = random.uniform(0.8, 3.0)
        
        # Determinar sinal baseado em múltiplas métricas
        score = 50.0
        signal = SignalType.NEUTRAL
        
        # Lógica NUPL (Capitulation -> Buy, Euphoria -> Sell)
        if nupl < 0.3:  # Capitulação
            score = 75 + random.uniform(0, 15)
            signal = SignalType.BUY
        elif nupl > 0.7:  # Euforia
            score = 25 - random.uniform(0, 15)
            signal = SignalType.SELL
        
        # Ajustar baseado no flow
        if exchange_flow < -500:  # Forte saída de exchanges (bullish)
            score = min(100, score + 10)
            if signal == SignalType.NEUTRAL:
                signal = SignalType.BUY
        elif exchange_flow > 500:  # Forte entrada (bearish)
            score = max(0, score - 10)
            if signal == SignalType.NEUTRAL:
                signal = SignalType.SELL
        
        # Ajustar baseado no MVRV
        if mvrv_ratio < 1.0:  # Subvalorizado
            score = min(100, score + 5)
        elif mvrv_ratio > 2.5:  # Sobrevalorizado
            score = max(0, score - 5)
        
        return OracleSignal(
            source=self.source_type,
            signal=signal,
            score=score,
            metadata={
                "nupl": round(nupl, 3),
                "exchange_net_flow": round(exchange_flow, 1),
                "supply_in_profit": round(supply_in_profit * 100, 1),
                "mvrv_ratio": round(mvrv_ratio, 2),
                "sopr": round(random.uniform(0.8, 1.2), 3),
                "entity_adjusted": True,
                "data_freshness": "1h"
            },
            latency=random.randint(700, 1000),
            timestamp=datetime.now(),
            reliability=self.config.source_reliability[self.source_type],
            confidence=0.85,  # Dados on-chain são geralmente confiáveis
            weight=self.config.source_weights.get(self.source_type, 1.0)
        )

class SantimentOracle(BaseOracle):
    """Oracle do Santiment (Sentimento Social)"""
    
    def __init__(self, config: OracleConfig):
        super().__init__(OracleSourceType.SANTIMENT, config)
    
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Simula dados de sentimento social"""
        await asyncio.sleep(random.uniform(0.15, 0.6))
        
        # Volume Social
        social_volume = random.randint(1000, 10000)
        
        # Score de Sentimento (ponderado)
        sentiment_score = random.uniform(-2, 2)
        
        # Dominância no Reddit/Twitter
        reddit_dominance = random.uniform(0.3, 0.7)
        twitter_dominance = 1 - reddit_dominance
        
        # Mentions Growth
        mentions_growth = random.uniform(-0.3, 0.5)
        
        # Lógica contrarian
        score = 50.0
        signal = SignalType.NEUTRAL
        
        # Extremo de otimismo -> vender (contrarian)
        if sentiment_score > 1.5:
            score = 30 - random.uniform(0, 10)
            signal = SignalType.SELL
        # Extremo de pessimismo -> comprar (contrarian)
        elif sentiment_score < -1.5:
            score = 70 + random.uniform(0, 10)
            signal = SignalType.BUY
        # Crescimento moderado de menções -> bullish
        elif mentions_growth > 0.2:
            score = 60 + random.uniform(0, 10)
            signal = SignalType.BUY
        
        # Ajustar baseado no volume social
        if social_volume > 7000 and signal == SignalType.NEUTRAL:
            score = 55 + random.uniform(0, 5)
            signal = SignalType.BUY
        
        return OracleSignal(
            source=self.source_type,
            signal=signal,
            score=score,
            metadata={
                "social_volume": social_volume,
                "sentiment_score": round(sentiment_score, 3),
                "reddit_dominance": round(reddit_dominance * 100, 1),
                "twitter_dominance": round(twitter_dominance * 100, 1),
                "mentions_growth": round(mentions_growth * 100, 1),
                "top_keywords": ["bullish", "buy", "rally"] if sentiment_score > 0 else ["bearish", "sell", "crash"],
                "data_sources": ["Twitter", "Reddit", "Telegram", "4chan"]
            },
            latency=random.randint(500, 800),
            timestamp=datetime.now(),
            reliability=self.config.source_reliability[self.source_type],
            confidence=0.7 - abs(sentiment_score) * 0.1,  # Menos confiança em extremos
            weight=self.config.source_weights.get(self.source_type, 1.0)
        )

class CoinglassOracle(BaseOracle):
    """Oracle do Coinglass (Dados de Derivativos)"""
    
    def __init__(self, config: OracleConfig):
        super().__init__(OracleSourceType.COINGLASS, config)
    
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Simula dados de derivativos e liquidações"""
        await asyncio.sleep(random.uniform(0.05, 0.3))
        
        # Long/Short Ratio
        long_short_ratio = random.uniform(0.5, 1.5)
        
        # Funding Rate
        funding_rate = random.uniform(-0.02, 0.03)
        
        # Open Interest
        open_interest = random.uniform(10000, 50000)
        oi_change = random.uniform(-0.1, 0.2)
        
        # Liquidations (em milhões)
        long_liquidations = random.uniform(1, 50)
        short_liquidations = random.uniform(1, 50)
        
        # Lógica baseada em squeezes
        score = 50.0
        signal = SignalType.NEUTRAL
        
        # Funding rate negativo -> potencial squeeze de shorts
        if funding_rate < -0.01:
            score = 65 + random.uniform(0, 15)
            signal = SignalType.BUY
        # Muitos longs -> bearish
        elif long_short_ratio > 1.3:
            score = 35 - random.uniform(0, 15)
            signal = SignalType.SELL
        # Aumento significativo no Open Interest
        elif oi_change > 0.15:
            score = 60 + random.uniform(0, 10)
            signal = SignalType.BUY
        
        # Ajustar baseado em liquidações
        if short_liquidations > long_liquidations * 2:
            score = min(100, score + 8)
        elif long_liquidations > short_liquidations * 2:
            score = max(0, score - 8)
        
        return OracleSignal(
            source=self.source_type,
            signal=signal,
            score=score,
            metadata={
                "long_short_ratio": round(long_short_ratio, 3),
                "funding_rate": round(funding_rate * 100, 4),
                "open_interest": round(open_interest, 1),
                "oi_change": round(oi_change * 100, 1),
                "long_liquidations": round(long_liquidations, 2),
                "short_liquidations": round(short_liquidations, 2),
                "total_liquidations": round(long_liquidations + short_liquidations, 2),
                "exchanges": ["Binance", "Bybit", "OKX", "Deribit"]
            },
            latency=random.randint(200, 400),
            timestamp=datetime.now(),
            reliability=self.config.source_reliability[self.source_type],
            confidence=0.8,
            weight=self.config.source_weights.get(self.source_type, 1.0)
        )

class IntoTheBlockOracle(BaseOracle):
    """Oracle do IntoTheBlock (Análise On-Chain Avançada)"""
    
    def __init__(self, config: OracleConfig):
        super().__init__(OracleSourceType.INTOTHEBLOCK, config)
    
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Simula análise on-chain avançada"""
        await asyncio.sleep(random.uniform(0.3, 0.7))
        
        # In/Out of the Money
        in_money = random.uniform(30, 95)
        
        # Concentration por whales
        whale_concentration = random.uniform(0.4, 0.8)
        
        # Network Value
        network_value = random.uniform(1000000, 5000000)
        nvt_signal = random.choice(['BULLISH', 'BEARISH', 'NEUTRAL'])
        
        # Holders Distribution
        holders_distribution = {
            "whales": random.uniform(0.05, 0.3),
            "sharks": random.uniform(0.1, 0.4),
            "fish": random.uniform(0.3, 0.6),
            "shrimp": random.uniform(0.1, 0.3)
        }
        
        # Lógica baseada em valorização
        score = in_money  # Usar % in money como base
        signal = SignalType.NEUTRAL
        
        # Muitos in money -> risco de profit taking
        if in_money > 85:
            score = 30 + random.uniform(0, 10)
            signal = SignalType.SELL
        # Poucos in money -> oportunidade de compra
        elif in_money < 50:
            score = 70 + random.uniform(0, 10)
            signal = SignalType.BUY
        
        # Ajustar baseado na concentração de whales
        if whale_concentration > 0.7 and signal == SignalType.BUY:
            score = max(0, score - 10)  # Menos bullish se muito concentrado
        
        # Ajustar baseado no NVT
        if nvt_signal == 'BULLISH':
            score = min(100, score + 5)
        elif nvt_signal == 'BEARISH':
            score = max(0, score - 5)
        
        return OracleSignal(
            source=self.source_type,
            signal=signal,
            score=score,
            metadata={
                "in_the_money": round(in_money, 1),
                "whale_concentration": round(whale_concentration * 100, 1),
                "network_value": round(network_value, 1),
                "nvt_signal": nvt_signal,
                "holders_distribution": {k: round(v * 100, 1) for k, v in holders_distribution.items()},
                "large_transactions": random.randint(50, 300),
                "smart_price": random.uniform(0.8, 1.2)
            },
            latency=random.randint(500, 700),
            timestamp=datetime.now(),
            reliability=self.config.source_reliability[self.source_type],
            confidence=0.75 + (abs(50 - score) / 100) * 0.25,  # Mais confiança em sinais fortes
            weight=self.config.source_weights.get(self.source_type, 1.0)
        )

class MessariOracle(BaseOracle):
    """Oracle do Messari (Fundamentais de Cripto)"""
    
    def __init__(self, config: OracleConfig):
        super().__init__(OracleSourceType.MESSARI, config)
    
    async def fetch_signal(self, symbol: str) -> OracleSignal:
        """Simula dados fundamentais do Messari"""
        await asyncio.sleep(random.uniform(0.4, 0.9))
        
        # Real Volume vs Reported
        real_volume_ratio = random.uniform(0.6, 1.0)
        
        # Developer Activity
        developer_activity = random.uniform(0, 100)
        
        # Treasury Health
        treasury_health = random.uniform(0.5, 1.0)
        
        # Adoption Metrics
        adoption_score = random.uniform(0, 100)
        
        # Regulatory Score
        regulatory_score = random.uniform(0, 100)
        
        # Lógica baseada em fundamentos
        score = 50.0
        signal = SignalType.NEUTRAL
        
        # Volume real alto -> qualidade de volume
        if real_volume_ratio > 0.9:
            score = 70 + random.uniform(0, 15)
            signal = SignalType.BUY
        
        # Atividade de desenvolvedores forte
        if developer_activity > 80:
            score = min(100, score + 10)
            if signal == SignalType.NEUTRAL:
                signal = SignalType.BUY
        
        # Saúde do tesouro boa
        if treasury_health > 0.8:
            score = min(100, score + 5)
        
        # Adoção crescente
        if adoption_score > 70:
            score = min(100, score + 8)
            if signal == SignalType.NEUTRAL:
                signal = SignalType.BUY
        
        # Score regulatório ruim
        if regulatory_score < 30:
            score = max(0, score - 15)
            if signal == SignalType.NEUTRAL:
                signal = SignalType.SELL
        
        # Calcular score composto
        composite_score = (
            real_volume_ratio * 0.3 +
            (developer_activity / 100) * 0.25 +
            treasury_health * 0.2 +
            (adoption_score / 100) * 0.15 +
            (regulatory_score / 100) * 0.1
        ) * 100
        
        score = max(0, min(100, composite_score))
        
        return OracleSignal(
            source=self.source_type,
            signal=signal,
            score=score,
            metadata={
                "real_volume_ratio": round(real_volume_ratio, 3),
                "developer_activity": round(developer_activity, 1),
                "treasury_health": round(treasury_health, 3),
                "adoption_score": round(adoption_score, 1),
                "regulatory_score": round(regulatory_score, 1),
                "institutional_grade": random.choice(["A", "B", "C", "D"]),
                "research_reports": random.randint(1, 10),
                "data_quality": "HIGH" if real_volume_ratio > 0.85 else "MEDIUM"
            },
            latency=random.randint(600, 900),
            timestamp=datetime.now(),
            reliability=self.config.source_reliability[self.source_type],
            confidence=0.8,
            weight=self.config.source_weights.get(self.source_type, 1.0)
        )

# Serviço principal de oráculos
class OracleService:
    """Serviço de agregação de múltiplos oráculos"""
    
    def __init__(self, config: Optional[OracleConfig] = None):
        self.config = config or OracleConfig()
        self.oracles: Dict[OracleSourceType, BaseOracle] = {}
        self.history: List[HistoricalConsensus] = []
        self.max_history_size = 1000
        
        # Inicializar oráculos
        self._initialize_oracles()
        
        logger.info("✅ OracleService inicializado com sucesso")
    
    def _initialize_oracles(self):
        """Inicializa todos os oráculos disponíveis"""
        self.oracles = {
            OracleSourceType.TRADINGVIEW: TradingViewOracle(self.config),
            OracleSourceType.YFINANCE: YFinanceOracle(self.config),
            OracleSourceType.GLASSNODE: GlassnodeOracle(self.config),
            OracleSourceType.SANTIMENT: SantimentOracle(self.config),
            OracleSourceType.COINGLASS: CoinglassOracle(self.config),
            OracleSourceType.INTOTHEBLOCK: IntoTheBlockOracle(self.config),
            OracleSourceType.MESSARI: MessariOracle(self.config)
        }
        
        logger.info(f"📊 {len(self.oracles)} oráculos inicializados")
    
    async def get_market_consensus(self, symbol: str = 'BTC/USDT') -> OracleConsensus:
        """Obtém consenso de mercado de todos os oráculos"""
        logger.info(f"🔄 Buscando consenso para {symbol}")
        
        start_time = datetime.now()
        
        try:
            # Buscar sinais de todos os oráculos em paralelo
            signals = await asyncio.gather(
                *[oracle.get_signal(symbol) for oracle in self.oracles.values()],
                return_exceptions=True
            )
            
            # Filtrar sinais válidos
            valid_signals: List[OracleSignal] = []
            for i, signal in enumerate(signals):
                source_type = list(self.oracles.keys())[i]
                
                if isinstance(signal, Exception):
                    logger.warning(f"Erro em {source_type.value}: {signal}")
                    continue
                
                if not isinstance(signal, OracleSignal):
                    logger.warning(f"Tipo inválido de {source_type.value}: {type(signal)}")
                    continue
                
                valid_signals.append(signal)
            
            if not valid_signals:
                raise ValueError("Nenhum sinal válido recebido")
            
            # Calcular consenso
            consensus = self._calculate_consensus(valid_signals, symbol)
            
            # Adicionar ao histórico
            self._add_to_history(symbol, consensus)
            
            # Log do resultado
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"✅ Consenso calculado para {symbol}: "
                f"Score={consensus.overall_score:.1f} | "
                f"Sentimento={consensus.sentiment} | "
                f"Tempo={elapsed:.2f}s"
            )
            
            return consensus
            
        except Exception as e:
            logger.error(f"❌ Erro ao calcular consenso: {e}")
            
            # Retornar consenso de erro
            return self._create_error_consensus(symbol, str(e))
    
    def _calculate_consensus(self, signals: List[OracleSignal], symbol: str) -> OracleConsensus:
        """Calcula consenso a partir dos sinais"""
        # Contadores
        bullish_count = 0
        bearish_count = 0
        neutral_count = 0
        
        # Scores ponderados
        weighted_scores = []
        total_weight = 0
        
        for signal in signals:
            # Contar sinais
            if signal.signal in [SignalType.BUY, SignalType.STRONG_BUY]:
                bullish_count += 1
            elif signal.signal in [SignalType.SELL, SignalType.STRONG_SELL]:
                bearish_count += 1
            else:
                neutral_count += 1
            
            # Converter score para escala 0-100 com viés direcional
            if signal.signal in [SignalType.BUY, SignalType.STRONG_BUY]:
                directional_score = signal.score
            elif signal.signal in [SignalType.SELL, SignalType.STRONG_SELL]:
                directional_score = 100 - signal.score
            else:
                directional_score = 50  # Neutro
            
            # Aplicar peso e confiança
            effective_score = directional_score * signal.weight * signal.confidence
            effective_weight = signal.weight * signal.confidence
            
            weighted_scores.append(effective_score)
            total_weight += effective_weight
        
        # Calcular scores
        if total_weight > 0:
            weighted_score = sum(weighted_scores) / total_weight
            overall_score = weighted_score
        else:
            weighted_score = 50.0
            overall_score = 50.0
        
        # Determinar primary driver (maior desvio da média)
        primary_driver = max(
            signals,
            key=lambda s: abs((s.score if s.signal in [SignalType.BUY, SignalType.STRONG_BUY] else 100 - s.score) - 50)
        ).source
        
        # Determinar sentimento
        if overall_score > self.config.strong_buy_threshold:
            sentiment = "STRONG_BULLISH"
        elif overall_score > self.config.buy_threshold:
            sentiment = "BULLISH"
        elif overall_score < self.config.strong_sell_threshold:
            sentiment = "STRONG_BEARISH"
        elif overall_score < self.config.sell_threshold:
            sentiment = "BEARISH"
        else:
            sentiment = "NEUTRAL"
        
        # Calcular nível de confiança
        confidence_level = min(1.0, total_weight / len(signals))
        
        # Determinar fase do mercado
        market_phase = self._determine_market_phase(signals)
        
        return OracleConsensus(
            overall_score=overall_score,
            bullish_count=bullish_count,
            bearish_count=bearish_count,
            neutral_count=neutral_count,
            primary_driver=primary_driver,
            signals=signals,
            timestamp=datetime.now(),
            sentiment=sentiment,
            confidence_level=confidence_level,
            weighted_score=weighted_score,
            market_phase=market_phase
        )
    
    def _determine_market_phase(self, signals: List[OracleSignal]) -> str:
        """Determina a fase do mercado baseado nos sinais"""
        # Extrair métricas relevantes
        metrics = {
            'volatility': 0,
            'sentiment_extreme': 0,
            'on_chain_health': 0,
            'derivatives_risk': 0
        }
        
        for signal in signals:
            if signal.source == OracleSourceType.TRADINGVIEW:
                if 'composite_score' in signal.metadata:
                    score = signal.metadata['composite_score']
                    metrics['volatility'] = abs(score - 50) / 50
            
            elif signal.source == OracleSourceType.SANTIMENT:
                if 'sentiment_score' in signal.metadata:
                    metrics['sentiment_extreme'] = abs(signal.metadata['sentiment_score']) / 2
            
            elif signal.source == OracleSourceType.GLASSNODE:
                if 'nupl' in signal.metadata:
                    nupl = signal.metadata['nupl']
                    metrics['on_chain_health'] = 1.0 if nupl > 0.7 else 0.5 if nupl > 0.3 else 0.0
            
            elif signal.source == OracleSourceType.COINGLASS:
                if 'long_short_ratio' in signal.metadata:
                    ratio = signal.metadata['long_short_ratio']
                    metrics['derivatives_risk'] = abs(ratio - 1.0)
        
        # Determinar fase
        if metrics['volatility'] > 0.7 and metrics['sentiment_extreme'] > 0.8:
            return "PANIC" if metrics['sentiment_extreme'] > 0 else "FOMO"
        elif metrics['on_chain_health'] > 0.8 and metrics['derivatives_risk'] < 0.3:
            return "ACCUMULATION"
        elif metrics['volatility'] < 0.3 and metrics['sentiment_extreme'] < 0.3:
            return "RANGING"
        elif metrics['derivatives_risk'] > 0.5:
            return "LEVERAGED"
        else:
            return "TRANSITION"
    
    def _add_to_history(self, symbol: str, consensus: OracleConsensus):
        """Adiciona consenso ao histórico"""
        historical = HistoricalConsensus(
            timestamp=consensus.timestamp,
            symbol=symbol,
            consensus=consensus
        )
        
        self.history.append(historical)
        
        # Manter histórico limitado
        if len(self.history) > self.max_history_size:
            self.history = self.history[-self.max_history_size:]
    
    def _create_error_consensus(self, symbol: str, error: str) -> OracleConsensus:
        """Cria consenso de erro"""
        return OracleConsensus(
            overall_score=50.0,
            bullish_count=0,
            bearish_count=0,
            neutral_count=0,
            primary_driver=OracleSourceType.TRADINGVIEW,
            signals=[],
            timestamp=datetime.now(),
            sentiment="ERROR",
            confidence_level=0.0,
            weighted_score=50.0,
            market_phase="ERROR"
        )
    
    async def get_signal_from_source(self, source: OracleSourceType, symbol: str) -> OracleSignal:
        """Obtém sinal de uma fonte específica"""
        if source not in self.oracles:
            raise ValueError(f"Fonte não suportada: {source}")
        
        return await self.oracles[source].get_signal(symbol)
    
    def get_oracle_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de todos os oráculos"""
        stats = {}
        for source_type, oracle in self.oracles.items():
            stats[source_type.value] = oracle.get_stats()
        
        stats['history_size'] = len(self.history)
        stats['consensus_count'] = len(self.history)
        
        if self.history:
            latest = self.history[-1]
            stats['latest_consensus'] = {
                'symbol': latest.symbol,
                'score': latest.consensus.overall_score,
                'sentiment': latest.consensus.sentiment,
                'timestamp': latest.timestamp.isoformat()
            }
        
        return stats
    
    def get_historical_consensus(self, symbol: Optional[str] = None, limit: int = 100) -> List[HistoricalConsensus]:
        """Retorna histórico de consensos"""
        filtered = self.history
        
        if symbol:
            filtered = [h for h in filtered if h.symbol == symbol]
        
        return filtered[-limit:] if filtered else []
    
    def analyze_accuracy(self, symbol: str, lookback_days: int = 30) -> Dict[str, Any]:
        """Analisa precisão histórica (simulação)"""
        # Em produção, compararia com dados reais de preço
        # Por enquanto, retorna análise simulada
        
        historical = self.get_historical_consensus(symbol, 100)
        
        if len(historical) < 10:
            return {"error": "Dados insuficientes"}
        
        # Simular análise
        correct_predictions = 0
        total_predictions = 0
        
        for i in range(len(historical) - 1):
            current = historical[i]
            next_data = historical[i + 1] if i + 1 < len(historical) else None
            
            if next_data:
                # Simplificação: considerar correto se sentimento se manteve
                current_sentiment = current.consensus.sentiment
                next_sentiment = next_data.consensus.sentiment
                
                if current_sentiment == next_sentiment:
                    correct_predictions += 1
                
                total_predictions += 1
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        return {
            'symbol': symbol,
            'lookback_days': lookback_days,
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
            'accuracy': round(accuracy * 100, 1),
            'analysis_period': {
                'start': historical[0].timestamp.isoformat() if historical else None,
                'end': historical[-1].timestamp.isoformat() if historical else None
            }
        }
    
    def save_state(self, filepath: str = "oracle_state.json"):
        """Salva estado do serviço"""
        try:
            state = {
                'config': asdict(self.config),
                'history': [h.to_dict() for h in self.history],
                'oracle_stats': self.get_oracle_stats(),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Estado salvo em {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar estado: {e}")
            return False
    
    def load_state(self, filepath: str = "oracle_state.json") -> bool:
        """Carrega estado do serviço"""
        try:
            if not os.path.exists(filepath):
                logger.warning(f"Arquivo de estado não encontrado: {filepath}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # Carregar histórico
            self.history = []
            for item in state.get('history', []):
                # Converter strings de volta para objetos
                consensus_dict = item['consensus']
                signals = []
                
                for sig_dict in consensus_dict['signals']:
                    signal = OracleSignal(
                        source=OracleSourceType(sig_dict['source']),
                        signal=SignalType(sig_dict['signal']),
                        score=sig_dict['score'],
                        metadata=sig_dict['metadata'],
                        latency=sig_dict['latency'],
                        timestamp=datetime.fromisoformat(sig_dict['timestamp']),
                        reliability=SourceReliability(sig_dict['reliability']),
                        confidence=sig_dict.get('confidence', 1.0),
                        weight=sig_dict.get('weight', 1.0)
                    )
                    signals.append(signal)
                
                consensus = OracleConsensus(
                    overall_score=consensus_dict['overall_score'],
                    bullish_count=consensus_dict['bullish_count'],
                    bearish_count=consensus_dict['bearish_count'],
                    neutral_count=consensus_dict['neutral_count'],
                    primary_driver=OracleSourceType(consensus_dict['primary_driver']),
                    signals=signals,
                    timestamp=datetime.fromisoformat(consensus_dict['timestamp']),
                    sentiment=consensus_dict['sentiment'],
                    confidence_level=consensus_dict['confidence_level'],
                    weighted_score=consensus_dict['weighted_score'],
                    market_phase=consensus_dict.get('market_phase', 'UNKNOWN')
                )
                
                historical = HistoricalConsensus(
                    timestamp=datetime.fromisoformat(item['timestamp']),
                    symbol=item['symbol'],
                    consensus=consensus,
                    actual_price_change=item.get('actual_price_change'),
                    prediction_accuracy=item.get('prediction_accuracy')
                )
                
                self.history.append(historical)
            
            logger.info(f"✅ Estado carregado de {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar estado: {e}")
            return False

# Instância global
oracle_service = OracleService()

# Interface CLI para demonstração
class OracleCLI:
    """Interface de linha de comando para o OracleService"""
    
    def __init__(self, service: OracleService):
        self.service = service
        self.running = True
    
    async def run(self):
        """Executa a interface CLI"""
        print("=" * 60)
        print("🔮 ORACLE SERVICE - Agregação de Sinais de Mercado")
        print("=" * 60)
        
        while self.running:
            print("\n" + "=" * 40)
            print("MENU PRINCIPAL")
            print("=" * 40)
            print("1. 📊 Obter Consenso de Mercado")
            print("2. 🎯 Obter Sinal de Fonte Específica")
            print("3. 📈 Ver Estatísticas dos Oráculos")
            print("4. 📜 Ver Histórico de Consensos")
            print("5. 🎯 Analisar Precisão Histórica")
            print("6. 💾 Salvar Estado")
            print("7. 📂 Carregar Estado")
            print("8. ⚙️  Configurar Pesos")
            print("0. ❌ Sair")
            print("=" * 40)
            
            choice = input("\nEscolha uma opção: ").strip()
            
            try:
                if choice == "1":
                    await self.get_market_consensus()
                elif choice == "2":
                    await self.get_single_source()
                elif choice == "3":
                    self.show_oracle_stats()
                elif choice == "4":
                    self.show_history()
                elif choice == "5":
                    self.analyze_accuracy()
                elif choice == "6":
                    self.save_state()
                elif choice == "7":
                    self.load_state()
                elif choice == "8":
                    self.configure_weights()
                elif choice == "0":
                    self.running = False
                    print("\n👋 Até logo!")
                else:
                    print("❌ Opção inválida!")
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Operação interrompida")
            except Exception as e:
                print(f"❌ Erro: {e}")
                logger.error(f"Erro na CLI: {e}", exc_info=True)
    
    async def get_market_consensus(self):
        """Obtém consenso de mercado"""
        symbol = input("Símbolo (ex: BTC/USDT): ").strip() or "BTC/USDT"
        
        print(f"\n🔄 Buscando consenso para {symbol}...")
        
        consensus = await self.service.get_market_consensus(symbol)
        
        print(f"\n" + "=" * 50)
        print(f"📊 CONSENSO DE MERCADO: {symbol}")
        print("=" * 50)
        
        # Score e sentimento
        score_color = "🟢" if consensus.overall_score > 55 else "🔴" if consensus.overall_score < 45 else "🟡"
        print(f"\n{score_color} Score Geral: {consensus.overall_score:.1f}/100")
        print(f"📈 Sentimento: {consensus.sentiment}")
        print(f"🎯 Confiança: {consensus.confidence_level:.1%}")
        print(f"🔄 Fase do Mercado: {consensus.market_phase}")
        print(f"🏆 Driver Principal: {consensus.primary_driver.value}")
        
        # Contadores
        print(f"\n📊 Distribuição:")
        print(f"  🟢 Bullish: {consensus.bullish_count}")
        print(f"  🔴 Bearish: {consensus.bearish_count}")
        print(f"  🟡 Neutral: {consensus.neutral_count}")
        
        # Sinais individuais
        print(f"\n🎯 Sinais por Fonte:")
        for signal in consensus.signals:
            signal_emoji = {
                SignalType.STRONG_BUY: "🟢✨",
                SignalType.BUY: "🟢",
                SignalType.NEUTRAL: "🟡",
                SignalType.SELL: "🔴",
                SignalType.STRONG_SELL: "🔴✨"
            }.get(signal.signal, "⚪")
            
            print(f"  {signal_emoji} {signal.source.value}:")
            print(f"     Sinal: {signal.signal.value}")
            print(f"     Score: {signal.score:.1f}")
            print(f"     Confiança: {signal.confidence:.1%}")
            if signal.metadata:
                key = list(signal.metadata.keys())[0]
                print(f"     {key}: {signal.metadata[key]}")
    
    async def get_single_source(self):
        """Obtém sinal de uma fonte específica"""
        print("\n📡 Fontes disponíveis:")
        for i, source in enumerate(OracleSourceType, 1):
            print(f"{i}. {source.value}")
        
        try:
            choice = int(input("\nSelecione a fonte: ").strip()) - 1
            if 0 <= choice < len(OracleSourceType):
                source = list(OracleSourceType)[choice]
                symbol = input("Símbolo: ").strip() or "BTC/USDT"
                
                print(f"\n🔄 Buscando {source.value} para {symbol}...")
                signal = await self.service.get_signal_from_source(source, symbol)
                
                print(f"\n🎯 {source.value}:")
                print(f"  Sinal: {signal.signal.value}")
                print(f"  Score: {signal.score:.1f}")
                print(f"  Latência: {signal.latency}ms")
                print(f"  Confiabilidade: {signal.reliability.value}")
                
                if signal.metadata:
                    print(f"\n  📊 Metadados:")
                    for key, value in signal.metadata.items():
                        print(f"    {key}: {value}")
            else:
                print("❌ Opção inválida!")
                
        except (ValueError, IndexError):
            print("❌ Seleção inválida!")
    
    def show_oracle_stats(self):
        """Mostra estatísticas dos oráculos"""
        stats = self.service.get_oracle_stats()
        
        print("\n" + "=" * 40)
        print("📈 ESTATÍSTICAS DOS ORÁCULOS")
        print("=" * 40)
        
        total_requests = 0
        total_errors = 0
        
        for source, data in stats.items():
            if source not in ['history_size', 'consensus_count', 'latest_consensus']:
                print(f"\n📡 {source}:")
                print(f"  Requisições: {data.get('request_count', 0)}")
                print(f"  Erros: {data.get('error_count', 0)}")
                print(f"  Taxa de Erro: {data.get('error_rate', 0):.1%}")
                
                total_requests += data.get('request_count', 0)
                total_errors += data.get('error_count', 0)
        
        print(f"\n📊 Totais:")
        print(f"  Requisições Totais: {total_requests}")
        print(f"  Erros Totais: {total_errors}")
        print(f"  Taxa de Erro Geral: {total_errors/max(total_requests,1):.1%}")
        print(f"  Consensos no Histórico: {stats.get('consensus_count', 0)}")
        
        if 'latest_consensus' in stats:
            latest = stats['latest_consensus']
            print(f"\n⏱️  Último Consenso:")
            print(f"  Símbolo: {latest.get('symbol')}")
            print(f"  Score: {latest.get('score', 0):.1f}")
            print(f"  Sentimento: {latest.get('sentiment')}")
    
    def show_history(self):
        """Mostra histórico de consensos"""
        symbol = input("Símbolo (opcional): ").strip() or None
        limit = int(input("Quantidade (padrão: 10): ").strip() or "10")
        
        history = self.service.get_historical_consensus(symbol, limit)
        
        if not history:
            print("📭 Nenhum consenso no histórico")
            return
        
        print(f"\n" + "=" * 50)
        print(f"📜 HISTÓRICO DE CONSENSOS ({len(history)})")
        print("=" * 50)
        
        for i, item in enumerate(reversed(history[-limit:]), 1):
            cons = item.consensus
            
            sentiment_emoji = {
                "STRONG_BULLISH": "🟢✨",
                "BULLISH": "🟢",
                "NEUTRAL": "🟡",
                "BEARISH": "🔴",
                "STRONG_BEARISH": "🔴✨",
                "ERROR": "❌"
            }.get(cons.sentiment, "⚪")
            
            time_str = item.timestamp.strftime("%H:%M")
            
            print(f"\n{i}. {time_str} {sentiment_emoji} {item.symbol}")
            print(f"   Score: {cons.overall_score:.1f} | {cons.sentiment}")
            print(f"   Bull/Bear: {cons.bullish_count}/{cons.bearish_count}")
            print(f"   Driver: {cons.primary_driver.value}")
    
    def analyze_accuracy(self):
        """Analisa precisão histórica"""
        symbol = input("Símbolo (ex: BTC/USDT): ").strip() or "BTC/USDT"
        
        print(f"\n📊 Analisando precisão para {symbol}...")
        
        analysis = self.service.analyze_accuracy(symbol)
        
        if 'error' in analysis:
            print(f"❌ {analysis['error']}")
            return
        
        print(f"\n🎯 ANÁLISE DE PRECISÃO:")
        print(f"  Símbolo: {analysis['symbol']}")
        print(f"  Período: {analysis['lookback_days']} dias")
        print(f"  Previsões: {analysis['total_predictions']}")
        print(f"  Corretas: {analysis['correct_predictions']}")
        
        accuracy = analysis['accuracy']
        accuracy_color = "🟢" if accuracy > 60 else "🔴" if accuracy < 40 else "🟡"
        print(f"  {accuracy_color} Precisão: {accuracy}%")
        
        if 'analysis_period' in analysis:
            period = analysis['analysis_period']
            print(f"  Início: {period.get('start', 'N/A')}")
            print(f"  Fim: {period.get('end', 'N/A')}")
    
    def save_state(self):
        """Salva estado do serviço"""
        filename = input("Nome do arquivo (padrão: oracle_state.json): ").strip() or "oracle_state.json"
        
        success = self.service.save_state(filename)
        
        if success:
            print(f"✅ Estado salvo em {filename}")
        else:
            print("❌ Falha ao salvar estado")
    
    def load_state(self):
        """Carrega estado do serviço"""
        filename = input("Nome do arquivo (padrão: oracle_state.json): ").strip() or "oracle_state.json"
        
        success = self.service.load_state(filename)
        
        if success:
            print(f"✅ Estado carregado de {filename}")
        else:
            print("❌ Falha ao carregar estado")
    
    def configure_weights(self):
        """Configura pesos das fontes"""
        print("\n⚖️  CONFIGURAR PESOS DAS FONTES")
        print("Peso atual: 1.0 = normal, 1.5 = mais importante, 0.5 = menos importante")
        
        for source_type in self.service.oracles.keys():
            current_weight = self.service.config.source_weights.get(source_type, 1.0)
            new_weight = input(f"{source_type.value} (atual: {current_weight}): ").strip()
            
            if new_weight:
                try:
                    weight = float(new_weight)
                    if 0 <= weight <= 2:
                        self.service.config.source_weights[source_type] = weight
                        print(f"✅ {source_type.value} alterado para {weight}")
                    else:
                        print(f"❌ Peso deve estar entre 0 e 2")
                except ValueError:
                    print(f"❌ Valor inválido")
        
        print("\n✅ Pesos atualizados!")

# Função principal
async def main():
    """Função principal"""
    print("Inicializando OracleService...")
    
    # Criar serviço
    service = OracleService()
    
    # Criar e executar CLI
    cli = OracleCLI(service)
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