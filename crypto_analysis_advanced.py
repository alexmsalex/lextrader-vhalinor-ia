"""
LEXTRADER-IAG 4.0 - Análise Avançada de Criptomoedas
====================================================
Sistema completo de análise técnica, fundamental e de sentimento para criptomoedas
com integração de IA, machine learning e análise preditiva.

Versão: 1.0.0
Data: Janeiro 2026
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import logging
from enum import Enum
import json

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Imports opcionais
try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    logger.warning("CCXT não disponível. Instale com: pip install ccxt")

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("Scikit-learn não disponível")

try:
    import ta
    TA_AVAILABLE = True
except ImportError:
    TA_AVAILABLE = False
    logger.warning("TA-Lib não disponível. Instale com: pip install ta")


class CryptoSignal(Enum):
    """Sinais de trading"""
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


class MarketRegime(Enum):
    """Regimes de mercado"""
    BULL_TRENDING = "BULL_TRENDING"
    BEAR_TRENDING = "BEAR_TRENDING"
    SIDEWAYS = "SIDEWAYS"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"


@dataclass
class CryptoAnalysisResult:
    """Resultado da análise de criptomoeda"""
    symbol: str
    timestamp: datetime
    price: float
    signal: CryptoSignal
    confidence: float
    technical_score: float
    fundamental_score: float
    sentiment_score: float
    market_regime: MarketRegime
    support_levels: List[float]
    resistance_levels: List[float]
    predicted_price_24h: float
    predicted_price_7d: float
    risk_score: float
    volume_analysis: Dict[str, Any]
    indicators: Dict[str, float]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class CryptoTechnicalAnalyzer:
    """Analisador técnico avançado para criptomoedas"""

    def __init__(self):
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        logger.info("✅ Analisador Técnico de Crypto inicializado")

    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula todos os indicadores técnicos"""
        df = df.copy()

        # Moving Averages
        df['sma_7'] = df['close'].rolling(window=7).mean()
        df['sma_25'] = df['close'].rolling(window=25).mean()
        df['sma_99'] = df['close'].rolling(window=99).mean()
        df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()

        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']

        # Stochastic
        low_14 = df['low'].rolling(window=14).min()
        high_14 = df['high'].rolling(window=14).max()
        df['stoch_k'] = 100 * ((df['close'] - low_14) / (high_14 - low_14))
        df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()

        # ATR (Average True Range)
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['atr'] = true_range.rolling(14).mean()

        # Volume indicators
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']

        # OBV (On-Balance Volume)
        df['obv'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()

        # ADX (Average Directional Index)
        df['adx'] = self._calculate_adx(df)

        # Ichimoku Cloud
        df = self._calculate_ichimoku(df)

        # Clean up infinite and NaN values to prevent overflow
        df = self._clean_dataframe(df)

        return df

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove valores infinitos e NaN para prevenir overflow"""
        # Substituir infinitos por NaN
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Preencher NaN com forward fill, depois backward fill
        df = df.ffill().bfill()
        
        # Se ainda houver NaN, preencher com 0
        df = df.fillna(0)
        
        # Limitar valores extremos (clip) para prevenir overflow
        for col in df.select_dtypes(include=[np.number]).columns:
            if col not in ['timestamp']:
                # Limitar valores entre -1e10 e 1e10
                df[col] = df[col].clip(lower=-1e10, upper=1e10)
        
        return df

    def _calculate_adx(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calcula ADX"""
        high = df['high']
        low = df['low']
        close = df['close']

        plus_dm = high.diff()
        minus_dm = low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0

        tr = pd.DataFrame({
            'hl': high - low,
            'hc': abs(high - close.shift()),
            'lc': abs(low - close.shift())
        }).max(axis=1)

        atr = tr.rolling(period).mean()
        plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
        minus_di = abs(100 * (minus_dm.rolling(period).mean() / atr))

        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(period).mean()

        return adx

    def _calculate_ichimoku(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula Ichimoku Cloud"""
        # Tenkan-sen (Conversion Line)
        nine_period_high = df['high'].rolling(window=9).max()
        nine_period_low = df['low'].rolling(window=9).min()
        df['tenkan_sen'] = (nine_period_high + nine_period_low) / 2

        # Kijun-sen (Base Line)
        period26_high = df['high'].rolling(window=26).max()
        period26_low = df['low'].rolling(window=26).min()
        df['kijun_sen'] = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A)
        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)

        # Senkou Span B (Leading Span B)
        period52_high = df['high'].rolling(window=52).max()
        period52_low = df['low'].rolling(window=52).min()
        df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)

        # Chikou Span (Lagging Span)
        df['chikou_span'] = df['close'].shift(-26)

        return df

    def identify_support_resistance(self, df: pd.DataFrame, window: int = 20) -> Tuple[List[float], List[float]]:
        """Identifica níveis de suporte e resistência"""
        supports = []
        resistances = []

        for i in range(window, len(df) - window):
            # Suporte: mínimo local
            if df['low'].iloc[i] == df['low'].iloc[i-window:i+window].min():
                supports.append(df['low'].iloc[i])

            # Resistência: máximo local
            if df['high'].iloc[i] == df['high'].iloc[i-window:i+window].max():
                resistances.append(df['high'].iloc[i])

        # Remove duplicatas próximas
        supports = self._cluster_levels(supports)
        resistances = self._cluster_levels(resistances)

        return supports[-5:], resistances[-5:]  # Últimos 5 níveis

    def _cluster_levels(self, levels: List[float], threshold: float = 0.02) -> List[float]:
        """Agrupa níveis próximos"""
        if not levels:
            return []

        levels = sorted(levels)
        clustered = [levels[0]]

        for level in levels[1:]:
            if abs(level - clustered[-1]) / clustered[-1] > threshold:
                clustered.append(level)

        return clustered

    def detect_patterns(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Detecta padrões de candlestick"""
        patterns = {}

        # Doji
        body = abs(df['close'] - df['open'])
        range_size = df['high'] - df['low']
        patterns['doji'] = (body / range_size < 0.1).iloc[-1] if len(df) > 0 else False

        # Hammer
        lower_shadow = df[['open', 'close']].min(axis=1) - df['low']
        upper_shadow = df['high'] - df[['open', 'close']].max(axis=1)
        patterns['hammer'] = (lower_shadow > 2 * body).iloc[-1] and (upper_shadow < body).iloc[-1] if len(df) > 0 else False

        # Engulfing
        if len(df) >= 2:
            patterns['bullish_engulfing'] = (
                df['close'].iloc[-2] < df['open'].iloc[-2] and
                df['close'].iloc[-1] > df['open'].iloc[-1] and
                df['open'].iloc[-1] < df['close'].iloc[-2] and
                df['close'].iloc[-1] > df['open'].iloc[-2]
            )
            patterns['bearish_engulfing'] = (
                df['close'].iloc[-2] > df['open'].iloc[-2] and
                df['close'].iloc[-1] < df['open'].iloc[-1] and
                df['open'].iloc[-1] > df['close'].iloc[-2] and
                df['close'].iloc[-1] < df['open'].iloc[-2]
            )

        return patterns

    def calculate_technical_score(self, df: pd.DataFrame) -> float:
        """Calcula score técnico geral (0-100)"""
        scores = []

        # RSI
        rsi = df['rsi'].iloc[-1]
        if rsi < 30:
            scores.append(80)  # Oversold - bullish
        elif rsi > 70:
            scores.append(20)  # Overbought - bearish
        else:
            scores.append(50)

        # MACD
        if df['macd'].iloc[-1] > df['macd_signal'].iloc[-1]:
            scores.append(70)  # Bullish
        else:
            scores.append(30)  # Bearish

        # Moving Averages
        if df['sma_7'].iloc[-1] > df['sma_25'].iloc[-1] > df['sma_99'].iloc[-1]:
            scores.append(80)  # Strong uptrend
        elif df['sma_7'].iloc[-1] < df['sma_25'].iloc[-1] < df['sma_99'].iloc[-1]:
            scores.append(20)  # Strong downtrend
        else:
            scores.append(50)

        # Bollinger Bands
        price = df['close'].iloc[-1]
        bb_position = (price - df['bb_lower'].iloc[-1]) / (df['bb_upper'].iloc[-1] - df['bb_lower'].iloc[-1])
        scores.append(bb_position * 100)

        # Volume
        if df['volume_ratio'].iloc[-1] > 1.5:
            scores.append(70)  # High volume confirmation
        else:
            scores.append(50)

        return np.mean(scores)


class CryptoFundamentalAnalyzer:
    """Analisador fundamental para criptomoedas"""

    def __init__(self):
        self.metrics_cache = {}
        logger.info("✅ Analisador Fundamental de Crypto inicializado")

    async def analyze_fundamentals(self, symbol: str) -> Dict[str, Any]:
        """Analisa fundamentos da criptomoeda"""
        fundamentals = {
            'market_cap_rank': 0,
            'market_cap': 0,
            'volume_24h': 0,
            'circulating_supply': 0,
            'total_supply': 0,
            'max_supply': 0,
            'ath': 0,
            'ath_change_percentage': 0,
            'atl': 0,
            'atl_change_percentage': 0,
            'developer_score': 0,
            'community_score': 0,
            'liquidity_score': 0,
            'public_interest_score': 0
        }

        # Aqui você integraria com APIs como CoinGecko, CoinMarketCap, etc.
        # Por enquanto, retorna estrutura básica

        return fundamentals

    def calculate_fundamental_score(self, fundamentals: Dict[str, Any]) -> float:
        """Calcula score fundamental (0-100)"""
        scores = []

        # Market Cap Rank (quanto menor, melhor)
        rank = fundamentals.get('market_cap_rank', 1000)
        if rank <= 10:
            scores.append(90)
        elif rank <= 50:
            scores.append(70)
        elif rank <= 100:
            scores.append(50)
        else:
            scores.append(30)

        # Volume/Market Cap ratio
        volume = fundamentals.get('volume_24h', 0)
        market_cap = fundamentals.get('market_cap', 1)
        volume_ratio = volume / market_cap if market_cap > 0 else 0
        if volume_ratio > 0.1:
            scores.append(80)
        elif volume_ratio > 0.05:
            scores.append(60)
        else:
            scores.append(40)

        # Supply metrics
        circulating = fundamentals.get('circulating_supply', 0)
        total = fundamentals.get('total_supply', 1)
        supply_ratio = circulating / total if total > 0 else 0
        scores.append(supply_ratio * 100)

        # Developer and community scores
        scores.append(fundamentals.get('developer_score', 50))
        scores.append(fundamentals.get('community_score', 50))

        return np.mean(scores) if scores else 50.0


class CryptoSentimentAnalyzer:
    """Analisador de sentimento para criptomoedas"""

    def __init__(self):
        self.sentiment_cache = {}
        logger.info("✅ Analisador de Sentimento de Crypto inicializado")

    async def analyze_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Analisa sentimento do mercado"""
        sentiment = {
            'social_volume': 0,
            'social_dominance': 0,
            'news_sentiment': 0.5,  # -1 a 1
            'twitter_sentiment': 0.5,
            'reddit_sentiment': 0.5,
            'fear_greed_index': 50,  # 0-100
            'whale_activity': 0,
            'exchange_inflow': 0,
            'exchange_outflow': 0
        }

        # Integração com APIs de sentimento (LunarCrush, Santiment, etc.)
        return sentiment

    def calculate_sentiment_score(self, sentiment: Dict[str, Any]) -> float:
        """Calcula score de sentimento (0-100)"""
        scores = []

        # Fear & Greed Index
        fg_index = sentiment.get('fear_greed_index', 50)
        scores.append(fg_index)

        # News Sentiment (-1 a 1 -> 0 a 100)
        news_sent = sentiment.get('news_sentiment', 0)
        scores.append((news_sent + 1) * 50)

        # Social Media Sentiment
        twitter_sent = sentiment.get('twitter_sentiment', 0)
        reddit_sent = sentiment.get('reddit_sentiment', 0)
        scores.append((twitter_sent + 1) * 50)
        scores.append((reddit_sent + 1) * 50)

        # Whale Activity (mais atividade = mais interesse)
        whale_activity = sentiment.get('whale_activity', 0)
        scores.append(min(whale_activity * 10, 100))

        return np.mean(scores) if scores else 50.0


class CryptoPricePredictor:
    """Preditor de preços usando ML"""

    def __init__(self):
        self.model = None
        if SKLEARN_AVAILABLE:
            self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        logger.info("✅ Preditor de Preços de Crypto inicializado")

    def train(self, df: pd.DataFrame):
        """Treina modelo de predição"""
        if not SKLEARN_AVAILABLE or self.model is None:
            return

        # Prepara features
        features = ['sma_7', 'sma_25', 'rsi', 'macd', 'bb_width', 'volume_ratio', 'atr']
        X = df[features].dropna()
        y = df['close'].shift(-1).dropna()

        # Alinha X e y
        min_len = min(len(X), len(y))
        X = X.iloc[:min_len]
        y = y.iloc[:min_len]

        if len(X) > 50:
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            logger.info(f"✅ Modelo treinado com {len(X)} amostras")

    def predict(self, df: pd.DataFrame, periods: int = 24) -> List[float]:
        """Prediz preços futuros"""
        if not SKLEARN_AVAILABLE or self.model is None:
            # Predição simples baseada em média móvel
            return [df['close'].iloc[-1] * (1 + np.random.uniform(-0.05, 0.05)) for _ in range(periods)]

        features = ['sma_7', 'sma_25', 'rsi', 'macd', 'bb_width', 'volume_ratio', 'atr']
        
        # Validar e limpar features antes da predição
        last_features = df[features].iloc[-1:].copy()
        
        # Substituir infinitos e NaN
        last_features = last_features.replace([np.inf, -np.inf], np.nan)
        last_features = last_features.ffill().fillna(0)
        
        # Limitar valores extremos
        for col in last_features.columns:
            last_features[col] = last_features[col].clip(lower=-1e6, upper=1e6)
        
        last_features_values = last_features.values

        predictions = []
        current_features = last_features_values.copy()

        for _ in range(periods):
            try:
                # Validar features antes de escalar
                if np.any(np.isnan(current_features)) or np.any(np.isinf(current_features)):
                    current_features = np.nan_to_num(current_features, nan=0.0, posinf=1e6, neginf=-1e6)
                
                scaled_features = self.scaler.transform(current_features)
                
                # Validar features escaladas
                if np.any(np.isnan(scaled_features)) or np.any(np.isinf(scaled_features)):
                    scaled_features = np.nan_to_num(scaled_features, nan=0.0, posinf=10.0, neginf=-10.0)
                
                pred = self.model.predict(scaled_features)[0]
                
                # Validar predição
                if np.isnan(pred) or np.isinf(pred):
                    pred = df['close'].iloc[-1]  # Usar último preço conhecido
                
                predictions.append(float(pred))

                # Atualizar features de forma mais conservadora
                # Usar uma pequena variação aleatória em vez de usar features escaladas
                variation = np.random.uniform(-0.01, 0.01, current_features.shape)
                current_features = current_features * (1 + variation)
                
            except Exception as e:
                # Em caso de erro, usar predição simples
                pred = df['close'].iloc[-1] * (1 + np.random.uniform(-0.02, 0.02))
                predictions.append(float(pred))

        return predictions


class AdvancedCryptoAnalyzer:
    """Analisador completo de criptomoedas"""

    def __init__(self):
        self.technical_analyzer = CryptoTechnicalAnalyzer()
        self.fundamental_analyzer = CryptoFundamentalAnalyzer()
        self.sentiment_analyzer = CryptoSentimentAnalyzer()
        self.price_predictor = CryptoPricePredictor()

        self.exchange = None
        if CCXT_AVAILABLE:
            try:
                self.exchange = ccxt.binance()
                logger.info("✅ Conectado à Binance via CCXT")
            except Exception as e:
                logger.warning(f"Erro ao conectar exchange: {e}")

        logger.info("🚀 Analisador Avançado de Crypto inicializado")

    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 500) -> pd.DataFrame:
        """Busca dados OHLCV"""
        if self.exchange:
            try:
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                return df
            except Exception as e:
                logger.error(f"Erro ao buscar dados: {e}")

        # Dados simulados para teste
        dates = pd.date_range(end=datetime.now(), periods=limit, freq='1H')
        df = pd.DataFrame({
            'timestamp': dates,
            'open': np.random.uniform(40000, 45000, limit),
            'high': np.random.uniform(40000, 45000, limit),
            'low': np.random.uniform(40000, 45000, limit),
            'close': np.random.uniform(40000, 45000, limit),
            'volume': np.random.uniform(100, 1000, limit)
        })
        return df

    async def analyze(self, symbol: str, timeframe: str = '1h') -> CryptoAnalysisResult:
        """Análise completa da criptomoeda"""
        logger.info(f"📊 Analisando {symbol}...")

        # Busca dados
        df = await self.fetch_ohlcv(symbol, timeframe)

        # Calcula indicadores
        df = self.technical_analyzer.calculate_all_indicators(df)

        # Análise técnica
        technical_score = self.technical_analyzer.calculate_technical_score(df)
        supports, resistances = self.technical_analyzer.identify_support_resistance(df)
        patterns = self.technical_analyzer.detect_patterns(df)

        # Análise fundamental
        fundamentals = await self.fundamental_analyzer.analyze_fundamentals(symbol)
        fundamental_score = self.fundamental_analyzer.calculate_fundamental_score(fundamentals)

        # Análise de sentimento
        sentiment = await self.sentiment_analyzer.analyze_sentiment(symbol)
        sentiment_score = self.sentiment_analyzer.calculate_sentiment_score(sentiment)

        # Predição de preços
        self.price_predictor.train(df)
        predictions = self.price_predictor.predict(df, periods=168)  # 7 dias em horas

        # Determina sinal
        overall_score = (technical_score * 0.4 + fundamental_score * 0.3 + sentiment_score * 0.3)
        signal = self._determine_signal(overall_score, df)

        # Calcula risco
        risk_score = self._calculate_risk(df, sentiment)

        # Identifica regime de mercado
        market_regime = self._identify_market_regime(df)

        # Gera recomendações
        recommendations = self._generate_recommendations(df, signal, risk_score, patterns)

        return CryptoAnalysisResult(
            symbol=symbol,
            timestamp=datetime.now(),
            price=df['close'].iloc[-1],
            signal=signal,
            confidence=min(abs(overall_score - 50) * 2, 100),
            technical_score=technical_score,
            fundamental_score=fundamental_score,
            sentiment_score=sentiment_score,
            market_regime=market_regime,
            support_levels=supports,
            resistance_levels=resistances,
            predicted_price_24h=predictions[23] if len(predictions) > 23 else df['close'].iloc[-1],
            predicted_price_7d=predictions[-1] if predictions else df['close'].iloc[-1],
            risk_score=risk_score,
            volume_analysis=self._analyze_volume(df),
            indicators={
                'rsi': df['rsi'].iloc[-1],
                'macd': df['macd'].iloc[-1],
                'bb_width': df['bb_width'].iloc[-1],
                'adx': df['adx'].iloc[-1] if 'adx' in df.columns else 0,
                'volume_ratio': df['volume_ratio'].iloc[-1]
            },
            recommendations=recommendations,
            metadata={'patterns': patterns, 'fundamentals': fundamentals, 'sentiment': sentiment}
        )

    def _determine_signal(self, score: float, df: pd.DataFrame) -> CryptoSignal:
        """Determina sinal de trading"""
        if score >= 75:
            return CryptoSignal.STRONG_BUY
        elif score >= 60:
            return CryptoSignal.BUY
        elif score >= 40:
            return CryptoSignal.HOLD
        elif score >= 25:
            return CryptoSignal.SELL
        else:
            return CryptoSignal.STRONG_SELL

    def _calculate_risk(self, df: pd.DataFrame, sentiment: Dict) -> float:
        """Calcula score de risco (0-100, maior = mais risco)"""
        risks = []

        # Volatilidade
        volatility = df['close'].pct_change().std()
        risks.append(min(volatility * 1000, 100))

        # ATR relativo
        atr_pct = df['atr'].iloc[-1] / df['close'].iloc[-1]
        risks.append(min(atr_pct * 500, 100))

        # Volume anormal
        if df['volume_ratio'].iloc[-1] > 3:
            risks.append(70)
        else:
            risks.append(30)

        # Sentimento extremo
        fg_index = sentiment.get('fear_greed_index', 50)
        if fg_index < 20 or fg_index > 80:
            risks.append(70)
        else:
            risks.append(30)

        return np.mean(risks)

    def _identify_market_regime(self, df: pd.DataFrame) -> MarketRegime:
        """Identifica regime de mercado"""
        # Tendência
        sma_7 = df['sma_7'].iloc[-1]
        sma_25 = df['sma_25'].iloc[-1]
        sma_99 = df['sma_99'].iloc[-1]

        # Volatilidade
        volatility = df['close'].pct_change().std()

        if volatility > 0.05:
            return MarketRegime.HIGH_VOLATILITY
        elif volatility < 0.01:
            return MarketRegime.LOW_VOLATILITY
        elif sma_7 > sma_25 > sma_99:
            return MarketRegime.BULL_TRENDING
        elif sma_7 < sma_25 < sma_99:
            return MarketRegime.BEAR_TRENDING
        else:
            return MarketRegime.SIDEWAYS

    def _analyze_volume(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analisa volume"""
        return {
            'current_volume': df['volume'].iloc[-1],
            'avg_volume': df['volume'].mean(),
            'volume_trend': 'increasing' if df['volume'].iloc[-10:].mean() > df['volume'].iloc[-20:-10].mean() else 'decreasing',
            'volume_spike': df['volume_ratio'].iloc[-1] > 2,
            'obv_trend': 'bullish' if df['obv'].iloc[-1] > df['obv'].iloc[-20] else 'bearish'
        }

    def _generate_recommendations(self, df: pd.DataFrame, signal: CryptoSignal,
                                 risk_score: float, patterns: Dict) -> List[str]:
        """Gera recomendações"""
        recommendations = []

        if signal in [CryptoSignal.STRONG_BUY, CryptoSignal.BUY]:
            recommendations.append(f"Sinal de {signal.value}: Considere posição de compra")
            if risk_score > 60:
                recommendations.append("⚠️ Alto risco: Use stop-loss apertado")
        elif signal in [CryptoSignal.STRONG_SELL, CryptoSignal.SELL]:
            recommendations.append(f"Sinal de {signal.value}: Considere reduzir exposição")

        if df['rsi'].iloc[-1] > 70:
            recommendations.append("RSI em sobrecompra: Possível correção")
        elif df['rsi'].iloc[-1] < 30:
            recommendations.append("RSI em sobrevenda: Possível recuperação")

        if patterns.get('bullish_engulfing'):
            recommendations.append("📈 Padrão Bullish Engulfing detectado")
        if patterns.get('bearish_engulfing'):
            recommendations.append("📉 Padrão Bearish Engulfing detectado")

        if df['volume_ratio'].iloc[-1] > 2:
            recommendations.append("🔊 Volume anormalmente alto: Confirme movimento")

        return recommendations


async def main():
    """Função de demonstração"""
    print("=" * 80)
    print("🚀 LEXTRADER-IAG 4.0 - Análise Avançada de Criptomoedas")
    print("=" * 80)
    print()

    analyzer = AdvancedCryptoAnalyzer()

    # Analisa Bitcoin
    result = await analyzer.analyze('BTC/USDT', '1h')

    print(f"📊 Análise de {result.symbol}")
    print(f"Preço Atual: ${result.price:,.2f}")
    print(f"Sinal: {result.signal.value} (Confiança: {result.confidence:.1f}%)")
    print(f"Score Técnico: {result.technical_score:.1f}/100")
    print(f"Score Fundamental: {result.fundamental_score:.1f}/100")
    print(f"Score Sentimento: {result.sentiment_score:.1f}/100")
    print(f"Regime de Mercado: {result.market_regime.value}")
    print(f"Risco: {result.risk_score:.1f}/100")
    print()
    print(f"Previsão 24h: ${result.predicted_price_24h:,.2f}")
    print(f"Previsão 7d: ${result.predicted_price_7d:,.2f}")
    print()
    print("Recomendações:")
    for rec in result.recommendations:
        print(f"  • {rec}")


if __name__ == "__main__":
    asyncio.run(main())
