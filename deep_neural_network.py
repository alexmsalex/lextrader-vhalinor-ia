import importlib.util
import os
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import warnings
from enum import Enum
import threading
import time
from scipy import stats
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# CONFIGURAÇÕES E CONSTANTES AVANÇADAS
# =============================================================================

class AnalysisMode(Enum):
    REALTIME = "REALTIME"
    HISTORICAL = "HISTORICAL"
    BACKTEST = "BACKTEST"
    OPTIMIZATION = "OPTIMIZATION"

class MarketRegime(Enum):
    TRENDING_BULL = "TRENDING_BULL"
    TRENDING_BEAR = "TRENDING_BEAR"
    RANGING = "RANGING"
    VOLATILE = "VOLATILE"
    BREAKOUT = "BREAKOUT"
    REVERSAL = "REVERSAL"

class TimeFrame(Enum):
    TICK = "TICK"
    M1 = "1M"
    M5 = "5M"
    M15 = "15M"
    M30 = "30M"
    H1 = "1H"
    H4 = "4H"
    D1 = "1D"
    W1 = "1W"
    MN1 = "1MN"

# =============================================================================
# ESTRUTURAS DE DADOS AVANÇADAS
# =============================================================================

@dataclass
class MarketData:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: Optional[float] = None
    typical_price: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'vwap': self.vwap,
            'typical_price': self.typical_price
        }

@dataclass
class TechnicalIndicators:
    # Tendência
    sma_20: float
    sma_50: float
    sma_200: float
    ema_12: float
    ema_26: float
    macd: float
    macd_signal: float
    macd_histogram: float
    adx: float
    adx_di_plus: float
    adx_di_minus: float
    ichimoku_base: float
    ichimoku_conversion: float
    ichimoku_leading_a: float
    ichimoku_leading_b: float
    ichimoku_lagging: float
    
    # Momentum
    rsi: float
    stoch_k: float
    stoch_d: float
    cci: float
    williams_r: float
    momentum: float
    roc: float
    
    # Volatilidade
    bollinger_upper: float
    bollinger_lower: float
    bollinger_middle: float
    bollinger_bandwidth: float
    bollinger_position: float
    atr: float
    keltner_upper: float
    keltner_lower: float
    keltner_middle: float
    
    # Volume
    volume_sma: float
    volume_ratio: float
    obv: float
    cmf: float
    mfi: float
    vwap: float
    
    # Ciclos
    hull_ma: float
    dema: float
    tema: float
    
    # Análise Avançada
    fractal_dimension: float
    hurst_exponent: float
    lyapunov_exponent: float
    correlation_dimension: float

@dataclass
class PatternRecognitionResult:
    pattern_name: str
    pattern_type: str
    confidence: float
    timeframe: str
    strength: float
    duration_bars: int
    volume_confirmation: bool
    indicators: List[str]
    entry_price: float
    target_price: float
    stop_loss: float
    risk_reward: float
    probability: float
    quality_score: float
    market_context: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'pattern_name': self.pattern_name,
            'pattern_type': self.pattern_type,
            'confidence': self.confidence,
            'timeframe': self.timeframe,
            'strength': self.strength,
            'duration_bars': self.duration_bars,
            'volume_confirmation': self.volume_confirmation,
            'indicators': self.indicators,
            'entry_price': self.entry_price,
            'target_price': self.target_price,
            'stop_loss': self.stop_loss,
            'risk_reward': self.risk_reward,
            'probability': self.probability,
            'quality_score': self.quality_score,
            'market_context': self.market_context
        }

@dataclass
class MarketRegimeAnalysis:
    regime: MarketRegime
    confidence: float
    volatility: float
    trend_strength: float
    volume_profile: str
    support_levels: List[float]
    resistance_levels: List[float]
    key_levels: List[float]
    market_phase: str
    regime_duration: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'regime': self.regime.value,
            'confidence': self.confidence,
            'volatility': self.volatility,
            'trend_strength': self.trend_strength,
            'volume_profile': self.volume_profile,
            'support_levels': self.support_levels,
            'resistance_levels': self.resistance_levels,
            'key_levels': self.key_levels,
            'market_phase': self.market_phase,
            'regime_duration': self.regime_duration
        }

@dataclass
class RiskAnalysis:
    var_95: float
    var_99: float
    expected_shortfall: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    volatility: float
    beta: float
    alpha: float
    correlation_matrix: np.ndarray
    stress_scenarios: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'var_95': self.var_95,
            'var_99': self.var_99,
            'expected_shortfall': self.expected_shortfall,
            'max_drawdown': self.max_drawdown,
            'sharpe_ratio': self.sharpe_ratio,
            'sortino_ratio': self.sortino_ratio,
            'calmar_ratio': self.calmar_ratio,
            'volatility': self.volatility,
            'beta': self.beta,
            'alpha': self.alpha,
            'correlation_matrix': self.correlation_matrix.tolist(),
            'stress_scenarios': self.stress_scenarios
        }

@dataclass
class PortfolioAnalysis:
    total_value: float
    pnl: float
    pnl_percentage: float
    daily_returns: List[float]
    positions: Dict[str, float]
    allocation: Dict[str, float]
    risk_metrics: RiskAnalysis
    performance_metrics: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_value': self.total_value,
            'pnl': self.pnl,
            'pnl_percentage': self.pnl_percentage,
            'daily_returns': self.daily_returns,
            'positions': self.positions,
            'allocation': self.allocation,
            'risk_metrics': self.risk_metrics.to_dict(),
            'performance_metrics': self.performance_metrics
        }

# =============================================================================
# REDE NEURAL PROFUNDA AVANÇADA
# =============================================================================

class AdvancedDeepNeuralNetwork:
    """Rede Neural Profunda Avançada para Análise de Mercado"""
    
    def __init__(self, input_dim: int = 100, hidden_layers: List[int] = None):
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers or [512, 256, 128, 64, 32]
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.training_history = None
        
        self._build_model()
    
    def _build_model(self) -> None:
        """Construir arquitetura da rede neural"""
        inputs = keras.Input(shape=(self.input_dim,))
        
        # Camadas ocultas
        x = inputs
        for units in self.hidden_layers:
            x = layers.Dense(units, activation='relu')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Dropout(0.3)(x)
        
        # Múltiplas saídas para diferentes análises
        pattern_output = layers.Dense(50, activation='softmax', name='pattern_recognition')(x)
        regime_output = layers.Dense(6, activation='softmax', name='regime_classification')(x)
        price_output = layers.Dense(3, activation='linear', name='price_prediction')(x)
        risk_output = layers.Dense(5, activation='linear', name='risk_assessment')(x)
        
        self.model = keras.Model(
            inputs=inputs,
            outputs=[pattern_output, regime_output, price_output, risk_output]
        )
        
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss={
                'pattern_recognition': 'categorical_crossentropy',
                'regime_classification': 'categorical_crossentropy',
                'price_prediction': 'mse',
                'risk_assessment': 'mse'
            },
            metrics={
                'pattern_recognition': 'accuracy',
                'regime_classification': 'accuracy',
                'price_prediction': 'mae',
                'risk_assessment': 'mae'
            }
        )
    
    def prepare_features(self, market_data: List[MarketData], 
                        technical_indicators: List[TechnicalIndicators]) -> np.ndarray:
        """Preparar features para a rede neural"""
        features = []
        
        for data, indicators in zip(market_data, technical_indicators):
            feature_vector = [
                data.open, data.high, data.low, data.close, data.volume,
                indicators.sma_20, indicators.sma_50, indicators.sma_200,
                indicators.ema_12, indicators.ema_26, indicators.macd,
                indicators.macd_signal, indicators.macd_histogram,
                indicators.adx, indicators.adx_di_plus, indicators.adx_di_minus,
                indicators.rsi, indicators.stoch_k, indicators.stoch_d,
                indicators.cci, indicators.williams_r, indicators.momentum,
                indicators.bollinger_upper, indicators.bollinger_lower,
                indicators.bollinger_middle, indicators.atr,
                indicators.volume_sma, indicators.volume_ratio,
                indicators.obv, indicators.cmf, indicators.mfi,
                indicators.fractal_dimension, indicators.hurst_exponent
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def train(self, features: np.ndarray, 
              targets: Dict[str, np.ndarray],
              epochs: int = 100,
              batch_size: int = 32,
              validation_split: float = 0.2) -> None:
        """Treinar a rede neural"""
        # Normalizar features
        features_scaled = self.scaler.fit_transform(features)
        
        # Treinar modelo
        self.training_history = self.model.fit(
            features_scaled,
            targets,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1,
            callbacks=[
                keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
            ]
        )
        
        self.is_trained = True
    
    def predict(self, features: np.ndarray) -> Dict[str, np.ndarray]:
        """Fazer previsões"""
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado")
        
        features_scaled = self.scaler.transform(features)
        return self.model.predict(features_scaled)
    
    def analyze_market(self, market_data: List[MarketData],
                      technical_indicators: List[TechnicalIndicators]) -> Dict[str, Any]:
        """Análise completa do mercado"""
        features = self.prepare_features(market_data, technical_indicators)
        predictions = self.predict(features)
        
        return {
            'pattern_probabilities': predictions[0],
            'regime_probabilities': predictions[1],
            'price_predictions': predictions[2],
            'risk_metrics': predictions[3],
            'confidence_scores': np.max(predictions[0], axis=1)
        }

# =============================================================================
# ANALISADOR TÉCNICO AVANÇADO
# =============================================================================

class AdvancedTechnicalAnalyzer:
    """Analisador Técnico Avançado com múltiplos indicadores"""
    
    def __init__(self):
        self.indicators_cache = {}
    
    def calculate_sma(self, prices: List[float], period: int) -> List[float]:
        """Média Móvel Simples"""
        return pd.Series(prices).rolling(window=period).mean().tolist()
    
    def calculate_ema(self, prices: List[float], period: int) -> List[float]:
        """Média Móvel Exponencial"""
        return pd.Series(prices).ewm(span=period).mean().tolist()
    
    def calculate_macd(self, prices: List[float]) -> Tuple[List[float], List[float], List[float]]:
        """MACD"""
        exp1 = pd.Series(prices).ewm(span=12).mean()
        exp2 = pd.Series(prices).ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        return macd.tolist(), signal.tolist(), histogram.tolist()
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """RSI"""
        delta = pd.Series(prices).diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.tolist()
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20) -> Tuple[List[float], List[float], List[float]]:
        """Bandas de Bollinger"""
        sma = pd.Series(prices).rolling(window=period).mean()
        std = pd.Series(prices).rolling(window=period).std()
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        return upper.tolist(), sma.tolist(), lower.tolist()
    
    def calculate_atr(self, high: List[float], low: List[float], close: List[float], period: int = 14) -> List[float]:
        """Average True Range"""
        high = pd.Series(high)
        low = pd.Series(low)
        close = pd.Series(close)
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr.tolist()
    
    def calculate_adx(self, high: List[float], low: List[float], close: List[float], period: int = 14) -> Tuple[List[float], List[float], List[float]]:
        """Average Directional Index"""
        high = pd.Series(high)
        low = pd.Series(low)
        close = pd.Series(close)
        
        plus_dm = high.diff()
        minus_dm = low.diff().abs()
        
        plus_dm[plus_dm < minus_dm] = 0
        minus_dm[minus_dm < plus_dm] = 0
        
        tr = self.calculate_atr(high.tolist(), low.tolist(), close.tolist(), period)
        tr_series = pd.Series(tr)
        
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / tr_series)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / tr_series)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        
        return adx.tolist(), plus_di.tolist(), minus_di.tolist()
    
    def calculate_ichimoku(self, high: List[float], low: List[float], close: List[float]) -> Tuple[List[float], List[float], List[float], List[float], List[float]]:
        """Ichimoku Cloud"""
        high = pd.Series(high)
        low = pd.Series(low)
        close = pd.Series(close)
        
        # Conversion Line
        conversion = (high.rolling(window=9).max() + low.rolling(window=9).min()) / 2
        
        # Base Line
        base = (high.rolling(window=26).max() + low.rolling(window=26).min()) / 2
        
        # Leading Span A
        leading_span_a = ((conversion + base) / 2).shift(26)
        
        # Leading Span B
        leading_span_b = ((high.rolling(window=52).max() + low.rolling(window=52).min()) / 2).shift(26)
        
        # Lagging Span
        lagging_span = close.shift(-26)
        
        return (conversion.tolist(), base.tolist(), leading_span_a.tolist(), 
                leading_span_b.tolist(), lagging_span.tolist())
    
    def calculate_fractal_dimension(self, prices: List[float]) -> float:
        """Dimensão Fractal para análise de complexidade"""
        n = len(prices)
        if n < 10:
            return 1.0
        
        # Método de Higuchi para dimensão fractal
        k_max = 10
        L = []
        
        for k in range(1, k_max + 1):
            Lk = 0
            for m in range(k):
                series = prices[m::k]
                if len(series) > 1:
                    Lk += (np.sum(np.abs(np.diff(series))) * (n - 1) / (k * len(series) * k))
            L.append(Lk)
        
        x = np.log(range(1, k_max + 1))
        y = np.log(L)
        
        if len(x) > 1 and len(y) > 1:
            slope, _, _, _, _ = stats.linregress(x, y)
            return abs(slope)
        else:
            return 1.0
    
    def calculate_hurst_exponent(self, prices: List[float]) -> float:
        """Expoente de Hurst para análise de persistência"""
        n = len(prices)
        if n < 100:
            return 0.5
        
        max_lag = min(20, n // 4)
        lags = range(2, max_lag)
        
        tau = []
        for lag in lags:
            pp = np.subtract(prices[lag:], prices[:-lag])
            tau.append(np.sqrt(np.std(pp)))
        
        if len(lags) > 1 and len(tau) > 1:
            hurst = np.polyfit(np.log(lags), np.log(tau), 1)[0]
            return hurst
        else:
            return 0.5
    
    def calculate_all_indicators(self, market_data: List[MarketData]) -> List[TechnicalIndicators]:
        """Calcular todos os indicadores técnicos"""
        indicators_list = []
        
        closes = [data.close for data in market_data]
        highs = [data.high for data in market_data]
        lows = [data.low for data in market_data]
        volumes = [data.volume for data in market_data]
        
        for i in range(len(market_data)):
            if i < 200:  # Precisa de dados suficientes
                continue
                
            # Calcular indicadores
            sma_20 = self.calculate_sma(closes[:i+1], 20)[-1]
            sma_50 = self.calculate_sma(closes[:i+1], 50)[-1]
            sma_200 = self.calculate_sma(closes[:i+1], 200)[-1]
            ema_12 = self.calculate_ema(closes[:i+1], 12)[-1]
            ema_26 = self.calculate_ema(closes[:i+1], 26)[-1]
            
            macd, macd_signal, macd_histogram = self.calculate_macd(closes[:i+1])
            macd_val = macd[-1] if macd else 0
            macd_sig = macd_signal[-1] if macd_signal else 0
            macd_hist = macd_histogram[-1] if macd_histogram else 0
            
            rsi = self.calculate_rsi(closes[:i+1])[-1]
            stoch = self.calculate_stochastic(highs[:i+1], lows[:i+1], closes[:i+1])
            stoch_k = stoch[0][-1] if stoch[0] else 50
            stoch_d = stoch[1][-1] if stoch[1] else 50
            
            bollinger_upper, bollinger_middle, bollinger_lower = self.calculate_bollinger_bands(closes[:i+1])
            boll_upper = bollinger_upper[-1] if bollinger_upper else closes[i]
            boll_middle = bollinger_middle[-1] if bollinger_middle else closes[i]
            boll_lower = bollinger_lower[-1] if bollinger_lower else closes[i]
            
            atr = self.calculate_atr(highs[:i+1], lows[:i+1], closes[:i+1])[-1]
            
            volume_sma = self.calculate_sma(volumes[:i+1], 20)[-1]
            volume_ratio = volumes[i] / volume_sma if volume_sma > 0 else 1
            
            fractal_dim = self.calculate_fractal_dimension(closes[max(0, i-100):i+1])
            hurst_exp = self.calculate_hurst_exponent(closes[max(0, i-200):i+1])
            
            indicators = TechnicalIndicators(
                sma_20=sma_20, sma_50=sma_50, sma_200=sma_200,
                ema_12=ema_12, ema_26=ema_26,
                macd=macd_val, macd_signal=macd_sig, macd_histogram=macd_hist,
                adx=50, adx_di_plus=50, adx_di_minus=50,  # Simplificado
                ichimoku_base=0, ichimoku_conversion=0, ichimoku_leading_a=0,
                ichimoku_leading_b=0, ichimoku_lagging=0,
                rsi=rsi, stoch_k=stoch_k, stoch_d=stoch_d,
                cci=0, williams_r=0, momentum=0, roc=0,
                bollinger_upper=boll_upper, bollinger_lower=boll_lower,
                bollinger_middle=boll_middle, bollinger_bandwidth=0,
                bollinger_position=0, atr=atr,
                keltner_upper=0, keltner_lower=0, keltner_middle=0,
                volume_sma=volume_sma, volume_ratio=volume_ratio,
                obv=0, cmf=0, mfi=0, vwap=market_data[i].vwap or 0,
                hull_ma=0, dema=0, tema=0,
                fractal_dimension=fractal_dim, hurst_exponent=hurst_exp,
                lyapunov_exponent=0, correlation_dimension=0
            )
            
            indicators_list.append(indicators)
        
        return indicators_list
    
    def calculate_stochastic(self, high: List[float], low: List[float], close: List[float], 
                           k_period: int = 14, d_period: int = 3) -> Tuple[List[float], List[float]]:
        """Indicador Estocástico"""
        high_series = pd.Series(high)
        low_series = pd.Series(low)
        close_series = pd.Series(close)
        
        lowest_low = low_series.rolling(window=k_period).min()
        highest_high = high_series.rolling(window=k_period).max()
        
        k = 100 * (close_series - lowest_low) / (highest_high - lowest_low)
        d = k.rolling(window=d_period).mean()
        
        return k.tolist(), d.tolist()

# =============================================================================
# SISTEMA DE RECONHECIMENTO DE PADRÕES AVANÇADO
# =============================================================================

class AdvancedPatternRecognizer:
    """Sistema Avançado de Reconhecimento de Padrões"""
    
    def __init__(self):
        self.patterns_database = self._initialize_patterns_database()
        self.neural_network = AdvancedDeepNeuralNetwork()
    
    def _initialize_patterns_database(self) -> Dict[str, Dict]:
        """Inicializar banco de dados de padrões"""
        return {
            # Padrões de Reversão
            'head_shoulders': {
                'type': 'REVERSAL_BEARISH',
                'complexity': 'HIGH',
                'reliability': 0.85,
                'duration_bars': 40,
                'volume_confirmation': True
            },
            'inverse_head_shoulders': {
                'type': 'REVERSAL_BULLISH',
                'complexity': 'HIGH',
                'reliability': 0.83,
                'duration_bars': 40,
                'volume_confirmation': True
            },
            'double_top': {
                'type': 'REVERSAL_BEARISH',
                'complexity': 'MEDIUM',
                'reliability': 0.78,
                'duration_bars': 25,
                'volume_confirmation': True
            },
            'double_bottom': {
                'type': 'REVERSAL_BULLISH',
                'complexity': 'MEDIUM',
                'reliability': 0.76,
                'duration_bars': 25,
                'volume_confirmation': True
            },
            'triple_top': {
                'type': 'REVERSAL_BEARISH',
                'complexity': 'HIGH',
                'reliability': 0.82,
                'duration_bars': 50,
                'volume_confirmation': True
            },
            'triple_bottom': {
                'type': 'REVERSAL_BULLISH',
                'complexity': 'HIGH',
                'reliability': 0.80,
                'duration_bars': 50,
                'volume_confirmation': True
            },
            
            # Padrões de Continuação
            'flag_bullish': {
                'type': 'CONTINUATION_BULLISH',
                'complexity': 'LOW',
                'reliability': 0.75,
                'duration_bars': 15,
                'volume_confirmation': True
            },
            'flag_bearish': {
                'type': 'CONTINUATION_BEARISH',
                'complexity': 'LOW',
                'reliability': 0.73,
                'duration_bars': 15,
                'volume_confirmation': True
            },
            'pennant': {
                'type': 'CONTINUATION',
                'complexity': 'MEDIUM',
                'reliability': 0.70,
                'duration_bars': 20,
                'volume_confirmation': True
            },
            'wedge_rising': {
                'type': 'REVERSAL_BEARISH',
                'complexity': 'MEDIUM',
                'reliability': 0.68,
                'duration_bars': 30,
                'volume_confirmation': True
            },
            'wedge_falling': {
                'type': 'REVERSAL_BULLISH',
                'complexity': 'MEDIUM',
                'reliability': 0.67,
                'duration_bars': 30,
                'volume_confirmation': True
            },
            
            # Padrões de Breakout
            'triangle_ascending': {
                'type': 'BULLISH_BREAKOUT',
                'complexity': 'MEDIUM',
                'reliability': 0.72,
                'duration_bars': 35,
                'volume_confirmation': True
            },
            'triangle_descending': {
                'type': 'BEARISH_BREAKOUT',
                'complexity': 'MEDIUM',
                'reliability': 0.71,
                'duration_bars': 35,
                'volume_confirmation': True
            },
            'triangle_symmetrical': {
                'type': 'BREAKOUT',
                'complexity': 'HIGH',
                'reliability': 0.65,
                'duration_bars': 40,
                'volume_confirmation': True
            },
            'rectangle': {
                'type': 'BREAKOUT',
                'complexity': 'LOW',
                'reliability': 0.74,
                'duration_bars': 25,
                'volume_confirmation': True
            },
            
            # Padrões Complexos
            'cup_handle': {
                'type': 'BULLISH_BREAKOUT',
                'complexity': 'HIGH',
                'reliability': 0.79,
                'duration_bars': 60,
                'volume_confirmation': True
            },
            'rounding_bottom': {
                'type': 'REVERSAL_BULLISH',
                'complexity': 'HIGH',
                'reliability': 0.77,
                'duration_bars': 55,
                'volume_confirmation': True
            },
            'diamond': {
                'type': 'REVERSAL',
                'complexity': 'VERY_HIGH',
                'reliability': 0.69,
                'duration_bars': 45,
                'volume_confirmation': True
            }
        }
    
    def detect_patterns(self, market_data: List[MarketData],
                       technical_indicators: List[TechnicalIndicators]) -> List[PatternRecognitionResult]:
        """Detectar múltiplos padrões nos dados de mercado"""
        results = []
        
        # Análise neural
        neural_analysis = self.neural_network.analyze_market(market_data, technical_indicators)
        
        # Detecção de padrões específicos
        for pattern_name, pattern_info in self.patterns_database.items():
            confidence = self._calculate_pattern_confidence(
                pattern_name, market_data, technical_indicators, neural_analysis
            )
            
            if confidence > 0.6:  # Threshold de confiança
                result = self._create_pattern_result(
                    pattern_name, pattern_info, confidence, market_data, technical_indicators
                )
                results.append(result)
        
        # Ordenar por confiança
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results
    
    def _calculate_pattern_confidence(self, pattern_name: str,
                                    market_data: List[MarketData],
                                    technical_indicators: List[TechnicalIndicators],
                                    neural_analysis: Dict[str, Any]) -> float:
        """Calcular confiança do padrão"""
        base_confidence = neural_analysis['confidence_scores'][-1] if len(neural_analysis['confidence_scores']) > 0 else 0.5
        
        # Fatores de ajuste baseados no padrão específico
        pattern_factors = {
            'volume_confirmation': self._check_volume_confirmation(market_data),
            'trend_alignment': self._check_trend_alignment(technical_indicators),
            'support_resistance': self._check_support_resistance(market_data),
            'timeframe_consistency': self._check_timeframe_consistency(),
            'market_context': self._check_market_context(technical_indicators)
        }
        
        adjustment = sum(pattern_factors.values()) / len(pattern_factors)
        final_confidence = base_confidence * adjustment
        
        return min(1.0, max(0.0, final_confidence))
    
    def _create_pattern_result(self, pattern_name: str, pattern_info: Dict,
                             confidence: float, market_data: List[MarketData],
                             technical_indicators: List[TechnicalIndicators]) -> PatternRecognitionResult:
        """Criar resultado de reconhecimento de padrão"""
        current_price = market_data[-1].close
        pattern_data = self.patterns_database[pattern_name]
        
        # Calcular alvos e stops
        target, stop_loss = self._calculate_targets_stops(
            pattern_name, market_data, technical_indicators
        )
        
        risk_reward = abs(target - current_price) / abs(stop_loss - current_price) if stop_loss != current_price else 1.0
        
        return PatternRecognitionResult(
            pattern_name=pattern_name.replace('_', ' ').title(),
            pattern_type=pattern_info['type'],
            confidence=confidence,
            timeframe='1H',  # Poderia ser dinâmico
            strength=pattern_info['reliability'],
            duration_bars=pattern_info['duration_bars'],
            volume_confirmation=pattern_info['volume_confirmation'],
            indicators=self._get_relevant_indicators(pattern_name),
            entry_price=current_price,
            target_price=target,
            stop_loss=stop_loss,
            risk_reward=risk_reward,
            probability=confidence * pattern_info['reliability'],
            quality_score=self._calculate_quality_score(pattern_name, market_data),
            market_context=self._analyze_market_context(technical_indicators)
        )
    
    def _calculate_targets_stops(self, pattern_name: str,
                               market_data: List[MarketData],
                               technical_indicators: List[TechnicalIndicators]) -> Tuple[float, float]:
        """Calcular alvos e stops baseados no padrão"""
        current_price = market_data[-1].close
        atr = technical_indicators[-1].atr if technical_indicators else current_price * 0.02
        
        # Lógica simplificada para cálculo de alvos
        if 'BULLISH' in pattern_name:
            target = current_price * 1.03  # 3% de alvo
            stop_loss = current_price * 0.98  # 2% de stop
        elif 'BEARISH' in pattern_name:
            target = current_price * 0.97  # 3% de alvo
            stop_loss = current_price * 1.02  # 2% de stop
        else:
            target = current_price * 1.02  # 2% de alvo padrão
            stop_loss = current_price * 0.98  # 2% de stop padrão
        
        return target, stop_loss
    
    def _get_relevant_indicators(self, pattern_name: str) -> List[str]:
        """Obter indicadores relevantes para o padrão"""
        indicator_map = {
            'head_shoulders': ['Volume', 'RSI Divergence', 'Neckline Break'],
            'double_top': ['Volume Confirmation', 'RSI', 'Support Break'],
            'cup_handle': ['Volume U-shape', 'Handle Formation', 'Breakout Volume'],
            'flag_bullish': ['Volume Decline', 'Flag Breakout', 'Trend Continuation']
        }
        return indicator_map.get(pattern_name, ['Volume', 'Price Action', 'Trend'])
    
    def _calculate_quality_score(self, pattern_name: str, market_data: List[MarketData]) -> float:
        """Calcular score de qualidade do padrão"""
        # Lógica simplificada - implementação real seria mais complexa
        volatility = np.std([data.close for data in market_data[-20:]]) / market_data[-1].close
        volume_trend = np.mean([data.volume for data in market_data[-5:]]) / np.mean([data.volume for data in market_data[-20:-5]])
        
        quality_factors = [
            1.0 - min(volatility, 0.1),  # Baixa volatilidade é melhor
            min(volume_trend, 2.0) / 2.0,  # Volume consistente ou crescente
            0.8  # Fator base
        ]
        
        return np.mean(quality_factors)
    
    def _analyze_market_context(self, technical_indicators: List[TechnicalIndicators]) -> str:
        """Analisar contexto de mercado"""
        if not technical_indicators:
            return "NEUTRAL"
        
        latest = technical_indicators[-1]
        
        if latest.rsi > 70:
            return "OVERBOUGHT"
        elif latest.rsi < 30:
            return "OVERSOLD"
        elif latest.macd > latest.macd_signal:
            return "BULLISH_MOMENTUM"
        elif latest.macd < latest.macd_signal:
            return "BEARISH_MOMENTUM"
        else:
            return "NEUTRAL"

    # Métodos auxiliares para cálculo de confiança
    def _check_volume_confirmation(self, market_data: List[MarketData]) -> float:
        """Verificar confirmação de volume"""
        if len(market_data) < 10:
            return 0.5
        
        recent_volume = np.mean([data.volume for data in market_data[-5:]])
        historical_volume = np.mean([data.volume for data in market_data[-20:-5]])
        
        if recent_volume > historical_volume * 1.2:
            return 1.0
        elif recent_volume > historical_volume:
            return 0.8
        else:
            return 0.6
    
    def _check_trend_alignment(self, technical_indicators: List[TechnicalIndicators]) -> float:
        """Verificar alinhamento com tendência"""
        if not technical_indicators:
            return 0.5
        
        latest = technical_indicators[-1]
        
        if latest.sma_20 > latest.sma_50 > latest.sma_200:
            return 1.0  # Tendência de alta forte
        elif latest.sma_20 < latest.sma_50 < latest.sma_200:
            return 1.0  # Tendência de baixa forte
        else:
            return 0.7  # Mercado em range
    
    def _check_support_resistance(self, market_data: List[MarketData]) -> float:
        """Verificar níveis de suporte e resistência"""
        if len(market_data) < 50:
            return 0.5
        
        prices = [data.close for data in market_data[-50:]]
        resistance = max(prices)
        support = min(prices)
        current = prices[-1]
        
        distance_to_resistance = abs(resistance - current) / current
        distance_to_support = abs(support - current) / current
        
        if distance_to_resistance < 0.02 or distance_to_support < 0.02:
            return 0.9  # Próximo de nível chave
        else:
            return 0.7
    
    def _check_timeframe_consistency(self) -> float:
        """Verificar consistência entre timeframes"""
        # Implementação simplificada
        return 0.8
    
    def _check_market_context(self, technical_indicators: List[TechnicalIndicators]) -> float:
        """Verificar contexto de mercado"""
        if not technical_indicators:
            return 0.5
        
        latest = technical_indicators[-1]
        
        # Verificar múltiplas condições
        conditions = [
            latest.rsi > 30 and latest.rsi < 70,  # RSI não em extremos
            latest.macd_histogram > -0.001,       # MACD não muito negativo
            latest.adx > 25,                      # ADX indica tendência
        ]
        
        score = sum(conditions) / len(conditions)
        return score

# =============================================================================
# ANALISADOR DE REGIME DE MERCADO
# =============================================================================

class MarketRegimeAnalyzer:
    """Analisador Avançado de Regime de Mercado"""
    
    def __init__(self):
        self.regime_history = []
        self.volatility_threshold = 0.02
        self.trend_threshold = 0.005
    
    def analyze_regime(self, market_data: List[MarketData],
                      technical_indicators: List[TechnicalIndicators]) -> MarketRegimeAnalysis:
        """Analisar regime atual do mercado"""
        if len(market_data) < 50:
            return self._get_default_regime()
        
        # Calcular métricas de regime
        volatility = self._calculate_volatility(market_data)
        trend_strength = self._calculate_trend_strength(technical_indicators)
        volume_profile = self._analyze_volume_profile(market_data)
        support_levels = self._identify_support_levels(market_data)
        resistance_levels = self._identify_resistance_levels(market_data)
        
        # Determinar regime
        regime, confidence = self._determine_regime(
            volatility, trend_strength, volume_profile, technical_indicators
        )
        
        return MarketRegimeAnalysis(
            regime=regime,
            confidence=confidence,
            volatility=volatility,
            trend_strength=trend_strength,
            volume_profile=volume_profile,
            support_levels=support_levels,
            resistance_levels=resistance_levels,
            key_levels=support_levels + resistance_levels,
            market_phase=self._determine_market_phase(technical_indicators),
            regime_duration=self._calculate_regime_duration(regime)
        )
    
    def _calculate_volatility(self, market_data: List[MarketData]) -> float:
        """Calcular volatilidade do mercado"""
        returns = []
        for i in range(1, len(market_data)):
            ret = (market_data[i].close - market_data[i-1].close) / market_data[i-1].close
            returns.append(ret)
        
        return np.std(returns) if returns else 0.0
    
    def _calculate_trend_strength(self, technical_indicators: List[TechnicalIndicators]) -> float:
        """Calcular força da tendência"""
        if not technical_indicators:
            return 0.5
        
        latest = technical_indicators[-1]
        
        # Usar ADX como medida principal de força da tendência
        adx_strength = min(latest.adx / 100.0, 1.0) if hasattr(latest, 'adx') else 0.5
        
        # Fatores adicionais
        sma_alignment = 1.0 if (latest.sma_20 > latest.sma_50 > latest.sma_200 or 
                               latest.sma_20 < latest.sma_50 < latest.sma_200) else 0.7
        
        return (adx_strength + sma_alignment) / 2.0
    
    def _analyze_volume_profile(self, market_data: List[MarketData]) -> str:
        """Analisar perfil de volume"""
        if len(market_data) < 20:
            return "NORMAL"
        
        recent_volume = np.mean([data.volume for data in market_data[-5:]])
        historical_volume = np.mean([data.volume for data in market_data[-20:]])
        
        ratio = recent_volume / historical_volume
        
        if ratio > 1.5:
            return "HIGH"
        elif ratio > 1.2:
            return "ABOVE_AVERAGE"
        elif ratio < 0.8:
            return "LOW"
        else:
            return "NORMAL"
    
    def _identify_support_levels(self, market_data: List[MarketData]) -> List[float]:
        """Identificar níveis de suporte"""
        if len(market_data) < 30:
            return []
        
        prices = [data.low for data in market_data[-30:]]
        return self._find_significant_levels(prices, 'support')
    
    def _identify_resistance_levels(self, market_data: List[MarketData]) -> List[float]:
        """Identificar níveis de resistência"""
        if len(market_data) < 30:
            return []
        
        prices = [data.high for data in market_data[-30:]]
        return self._find_significant_levels(prices, 'resistance')
    
    def _find_significant_levels(self, prices: List[float], level_type: str) -> List[float]:
        """Encontrar níveis significativos de suporte/resistência"""
        if len(prices) < 10:
            return []
        
        # Implementação simplificada - usar approach mais sofisticado na versão real
        sorted_prices = sorted(prices)
        quartile_size = len(sorted_prices) // 4
        
        if level_type == 'support':
            return sorted_prices[:quartile_size:max(1, quartile_size//3)]
        else:
            return sorted_prices[-quartile_size::max(1, quartile_size//3)]
    
    def _determine_regime(self, volatility: float, trend_strength: float,
                         volume_profile: str, technical_indicators: List[TechnicalIndicators]) -> Tuple[MarketRegime, float]:
        """Determinar regime de mercado"""
        if not technical_indicators:
            return MarketRegime.RANGING, 0.5
        
        latest = technical_indicators[-1]
        
        # Lógica de decisão baseada em múltiplos fatores
        factors = []
        
        # Fator de volatilidade
        if volatility > self.volatility_threshold * 2:
            factors.append(('VOLATILE', 0.9))
        elif volatility < self.volatility_threshold * 0.5:
            factors.append(('RANGING', 0.8))
        
        # Fator de tendência
        if trend_strength > 0.7:
            if latest.sma_20 > latest.sma_50:
                factors.append(('TRENDING_BULL', 0.85))
            else:
                factors.append(('TRENDING_BEAR', 0.85))
        
        # Fator de volume
        if volume_profile == 'HIGH':
            factors.append(('BREAKOUT', 0.75))
        
        # Se não há fatores fortes, assume ranging
        if not factors:
            return MarketRegime.RANGING, 0.6
        
        # Escolher o regime com maior confiança
        best_regime = max(factors, key=lambda x: x[1])
        regime_map = {
            'VOLATILE': MarketRegime.VOLATILE,
            'RANGING': MarketRegime.RANGING,
            'TRENDING_BULL': MarketRegime.TRENDING_BULL,
            'TRENDING_BEAR': MarketRegime.TRENDING_BEAR,
            'BREAKOUT': MarketRegime.BREAKOUT
        }
        
        return regime_map.get(best_regime[0], MarketRegime.RANGING), best_regime[1]
    
    def _determine_market_phase(self, technical_indicators: List[TechnicalIndicators]) -> str:
        """Determinar fase do mercado"""
        if not technical_indicators:
            return "UNCERTAIN"
        
        latest = technical_indicators[-1]
        
        if latest.rsi < 30:
            return "OVERSOLD"
        elif latest.rsi > 70:
            return "OVERBOUGHT"
        elif latest.macd > latest.macd_signal:
            return "ACCUMULATION"
        elif latest.macd < latest.macd_signal:
            return "DISTRIBUTION"
        else:
            return "CONSOLIDATION"
    
    def _calculate_regime_duration(self, current_regime: MarketRegime) -> int:
        """Calcular duração do regime atual"""
        # Implementação simplificada
        return len([r for r in self.regime_history[-10:] if r == current_regime])
    
    def _get_default_regime(self) -> MarketRegimeAnalysis:
        """Obter análise de regime padrão"""
        return MarketRegimeAnalysis(
            regime=MarketRegime.RANGING,
            confidence=0.5,
            volatility=0.0,
            trend_strength=0.5,
            volume_profile="NORMAL",
            support_levels=[],
            resistance_levels=[],
            key_levels=[],
            market_phase="UNCERTAIN",
            regime_duration=0
        )

# =============================================================================
# ANALISADOR DE RISCO AVANÇADO
# =============================================================================

class AdvancedRiskAnalyzer:
    """Analisador de Risco Avançado"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.risk_free_rate = 0.02  # Taxa livre de risco anual
    
    def analyze_portfolio_risk(self, returns: List[float],
                              positions: Dict[str, float],
                              market_data: Dict[str, List[MarketData]]) -> RiskAnalysis:
        """Analisar risco da carteira"""
        if not returns:
            return self._get_default_risk_analysis()
        
        returns_array = np.array(returns)
        
        # Métricas de risco básicas
        var_95 = self._calculate_var(returns_array, 0.95)
        var_99 = self._calculate_var(returns_array, 0.99)
        expected_shortfall = self._calculate_expected_shortfall(returns_array, 0.95)
        max_drawdown = self._calculate_max_drawdown(returns_array)
        
        # Métricas de performance ajustadas ao risco
        sharpe_ratio = self._calculate_sharpe_ratio(returns_array)
        sortino_ratio = self._calculate_sortino_ratio(returns_array)
        calmar_ratio = self._calculate_calmar_ratio(returns_array, max_drawdown)
        
        # Volatilidade e correlações
        volatility = np.std(returns_array)
        correlation_matrix = self._calculate_correlation_matrix(market_data)
        
        # Cenários de stress
        stress_scenarios = self._calculate_stress_scenarios(returns_array, market_data)
        
        return RiskAnalysis(
            var_95=var_95,
            var_99=var_99,
            expected_shortfall=expected_shortfall,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            volatility=volatility,
            beta=0.0,  # Seria calculado vs benchmark
            alpha=0.0,  # Seria calculado vs benchmark
            correlation_matrix=correlation_matrix,
            stress_scenarios=stress_scenarios
        )
    
    def _calculate_var(self, returns: np.ndarray, confidence: float) -> float:
        """Calcular Value at Risk"""
        return np.percentile(returns, (1 - confidence) * 100)
    
    def _calculate_expected_shortfall(self, returns: np.ndarray, confidence: float) -> float:
        """Calcular Expected Shortfall (CVaR)"""
        var = self._calculate_var(returns, confidence)
        tail_returns = returns[returns <= var]
        return np.mean(tail_returns) if len(tail_returns) > 0 else var
    
    def _calculate_max_drawdown(self, returns: np.ndarray) -> float:
        """Calcular Maximum Drawdown"""
        cumulative = np.cumprod(1 + returns)
        peak = np.maximum.accumulate(cumulative)
        drawdown = (peak - cumulative) / peak
        return np.max(drawdown) if len(drawdown) > 0 else 0.0
    
    def _calculate_sharpe_ratio(self, returns: np.ndarray) -> float:
        """Calcular Sharpe Ratio"""
        excess_returns = returns - self.risk_free_rate / 252  # Diário
        return np.mean(excess_returns) / np.std(excess_returns) if np.std(excess_returns) > 0 else 0.0
    
    def _calculate_sortino_ratio(self, returns: np.ndarray) -> float:
        """Calcular Sortino Ratio"""
        excess_returns = returns - self.risk_free_rate / 252
        negative_returns = returns[returns < 0]
        downside_std = np.std(negative_returns) if len(negative_returns) > 0 else 0.0
        return np.mean(excess_returns) / downside_std if downside_std > 0 else 0.0
    
    def _calculate_calmar_ratio(self, returns: np.ndarray, max_drawdown: float) -> float:
        """Calcular Calmar Ratio"""
        annual_return = np.mean(returns) * 252
        return annual_return / max_drawdown if max_drawdown > 0 else 0.0
    
    def _calculate_correlation_matrix(self, market_data: Dict[str, List[MarketData]]) -> np.ndarray:
        """Calcular matriz de correlação entre ativos"""
        symbols = list(market_data.keys())
        n = len(symbols)
        
        if n == 0:
            return np.array([])
        
        # Extrair returns de cada símbolo
        returns_data = {}
        for symbol, data in market_data.items():
            if len(data) > 1:
                prices = [d.close for d in data]
                returns = np.diff(prices) / prices[:-1]
                returns_data[symbol] = returns
        
        # Criar matriz de correlação
        correlation_matrix = np.eye(n)
        
        for i, sym1 in enumerate(symbols):
            for j, sym2 in enumerate(symbols):
                if i != j and sym1 in returns_data and sym2 in returns_data:
                    # Encontrar tamanho comum
                    min_len = min(len(returns_data[sym1]), len(returns_data[sym2]))
                    if min_len > 5:
                        corr = np.corrcoef(returns_data[sym1][-min_len:], 
                                         returns_data[sym2][-min_len:])[0, 1]
                        correlation_matrix[i, j] = corr if not np.isnan(corr) else 0.0
        
        return correlation_matrix
    
    def _calculate_stress_scenarios(self, returns: np.ndarray, 
                                  market_data: Dict[str, List[MarketData]]) -> Dict[str, float]:
        """Calcular cenários de stress"""
        scenarios = {}
        
        if len(returns) > 0:
            # Cenário de crash (pior 1% dos returns)
            crash_scenario = np.percentile(returns, 1)
            scenarios['MARKET_CRASH'] = crash_scenario
            
            # Cenário de alta volatilidade
            high_vol_scenario = np.mean(returns) - 2 * np.std(returns)
            scenarios['HIGH_VOLATILITY'] = high_vol_scenario
            
            # Cenário de liquidez
            liquidity_scenario = np.percentile(returns, 5)
            scenarios['LIQUIDITY_CRISIS'] = liquidity_scenario
        
        return scenarios
    
    def _get_default_risk_analysis(self) -> RiskAnalysis:
        """Obter análise de risco padrão"""
        return RiskAnalysis(
            var_95=0.0,
            var_99=0.0,
            expected_shortfall=0.0,
            max_drawdown=0.0,
            sharpe_ratio=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
            volatility=0.0,
            beta=0.0,
            alpha=0.0,
            correlation_matrix=np.array([]),
            stress_scenarios={}
        )

# =============================================================================
# SISTEMA PRINCIPAL DE ANÁLISE
# =============================================================================

class AdvancedMarketAnalysisSystem:
    """Sistema Completo de Análise de Mercado"""
    
    def __init__(self):
        self.technical_analyzer = AdvancedTechnicalAnalyzer()
        self.pattern_recognizer = AdvancedPatternRecognizer()
        self.regime_analyzer = MarketRegimeAnalyzer()
        self.risk_analyzer = AdvancedRiskAnalyzer()
        
        self.analysis_history = []
        self.portfolio_data = {}
    
    def comprehensive_analysis(self, market_data: List[MarketData],
                             portfolio_positions: Dict[str, float] = None) -> Dict[str, Any]:
        """Executar análise completa do mercado"""
        
        # 1. Análise Técnica
        technical_indicators = self.technical_analyzer.calculate_all_indicators(market_data)
        
        # 2. Reconhecimento de Padrões
        patterns = self.pattern_recognizer.detect_patterns(market_data, technical_indicators)
        
        # 3. Análise de Regime
        regime_analysis = self.regime_analyzer.analyze_regime(market_data, technical_indicators)
        
        # 4. Análise de Risco (se houver dados de portfolio)
        risk_analysis = None
        if portfolio_positions:
            returns = self._calculate_portfolio_returns(portfolio_positions, market_data)
            risk_analysis = self.risk_analyzer.analyze_portfolio_risk(
                returns, portfolio_positions, {'current': market_data}
            )
        
        # 5. Síntese e Recomendações
        synthesis = self._create_analysis_synthesis(
            patterns, regime_analysis, risk_analysis, technical_indicators
        )
        
        # Armazenar no histórico
        analysis_result = {
            'timestamp': datetime.now(),
            'technical_indicators': technical_indicators,
            'patterns': patterns,
            'regime_analysis': regime_analysis,
            'risk_analysis': risk_analysis,
            'synthesis': synthesis,
            'market_data': market_data
        }
        
        self.analysis_history.append(analysis_result)
        
        return analysis_result
    
    def _calculate_portfolio_returns(self, positions: Dict[str, float],
                                   market_data: List[MarketData]) -> List[float]:
        """Calcular returns da carteira"""
        # Implementação simplificada
        if len(market_data) < 2:
            return []
        
        returns = []
        for i in range(1, len(market_data)):
            ret = (market_data[i].close - market_data[i-1].close) / market_data[i-1].close
            returns.append(ret)
        
        return returns
    
    def _create_analysis_synthesis(self, patterns: List[PatternRecognitionResult],
                                 regime_analysis: MarketRegimeAnalysis,
                                 risk_analysis: Optional[RiskAnalysis],
                                 technical_indicators: List[TechnicalIndicators]) -> Dict[str, Any]:
        """Criar síntese da análise"""
        
        # Análise de Confiança Geral
        overall_confidence = self._calculate_overall_confidence(patterns, regime_analysis)
        
        # Recomendações Baseadas em Múltiplos Fatores
        recommendations = self._generate_recommendations(patterns, regime_analysis, technical_indicators)
        
        # Alertas de Risco
        risk_alerts = self._generate_risk_alerts(risk_analysis, regime_analysis)
        
        return {
            'overall_confidence': overall_confidence,
            'market_outlook': self._determine_market_outlook(regime_analysis, patterns),
            'trading_recommendations': recommendations,
            'risk_alerts': risk_alerts,
            'key_levels': regime_analysis.key_levels,
            'optimal_timeframe': self._determine_optimal_timeframe(patterns, regime_analysis),
            'market_sentiment': self._calculate_market_sentiment(technical_indicators)
        }
    
    def _calculate_overall_confidence(self, patterns: List[PatternRecognitionResult],
                                   regime_analysis: MarketRegimeAnalysis) -> float:
        """Calcular confiança geral da análise"""
        if not patterns:
            return regime_analysis.confidence * 0.7
        
        pattern_confidence = np.mean([p.confidence for p in patterns])
        regime_confidence = regime_analysis.confidence
        
        return (pattern_confidence + regime_confidence) / 2.0
    
    def _generate_recommendations(self, patterns: List[PatternRecognitionResult],
                                regime_analysis: MarketRegimeAnalysis,
                                technical_indicators: List[TechnicalIndicators]) -> List[Dict[str, Any]]:
        """Gerar recomendações de trading"""
        recommendations = []
        
        if not patterns or not technical_indicators:
            return recommendations
        
        latest_indicators = technical_indicators[-1]
        
        for pattern in patterns[:3]:  # Top 3 padrões
            if pattern.confidence > 0.7:
                recommendation = {
                    'pattern': pattern.pattern_name,
                    'action': 'BUY' if 'BULLISH' in pattern.pattern_type else 'SELL',
                    'confidence': pattern.confidence,
                    'entry': pattern.entry_price,
                    'target': pattern.target_price,
                    'stop_loss': pattern.stop_loss,
                    'risk_reward': pattern.risk_reward,
                    'timeframe': pattern.timeframe,
                    'rationale': f"Padrão {pattern.pattern_name} detectado com {pattern.confidence:.1%} de confiança"
                }
                recommendations.append(recommendation)
        
        # Recomendação baseada em regime
        if regime_analysis.regime == MarketRegime.TRENDING_BULL:
            recommendations.append({
                'pattern': 'TREND_FOLLOWING',
                'action': 'BUY_ON_DIPS',
                'confidence': regime_analysis.confidence,
                'rationale': 'Mercado em tendência de alta forte'
            })
        elif regime_analysis.regime == MarketRegime.TRENDING_BEAR:
            recommendations.append({
                'pattern': 'TREND_FOLLOWING',
                'action': 'SELL_ON_RALLIES',
                'confidence': regime_analysis.confidence,
                'rationale': 'Mercado em tendência de baixa forte'
            })
        
        return recommendations
    
    def _generate_risk_alerts(self, risk_analysis: Optional[RiskAnalysis],
                            regime_analysis: MarketRegimeAnalysis) -> List[Dict[str, Any]]:
        """Gerar alertas de risco"""
        alerts = []
        
        # Alertas baseados em regime
        if regime_analysis.volatility > 0.05:
            alerts.append({
                'level': 'HIGH',
                'type': 'VOLATILITY',
                'message': f'Alta volatilidade detectada: {regime_analysis.volatility:.2%}',
                'suggestion': 'Reduzir tamanho de posição'
            })
        
        if regime_analysis.regime == MarketRegime.VOLATILE:
            alerts.append({
                'level': 'MEDIUM',
                'type': 'MARKET_REGIME',
                'message': 'Mercado em regime volátil',
                'suggestion': 'Considerar hedging ou reduzir exposição'
            })
        
        # Alertas baseados em análise de risco
        if risk_analysis:
            if risk_analysis.max_drawdown > 0.1:
                alerts.append({
                    'level': 'HIGH',
                    'type': 'DRAWDOWN',
                    'message': f'Drawdown máximo elevado: {risk_analysis.max_drawdown:.2%}',
                    'suggestion': 'Revisar estratégia e gestão de risco'
                })
            
            if risk_analysis.var_95 < -0.03:
                alerts.append({
                    'level': 'MEDIUM',
                    'type': 'VAR',
                    'message': f'VaR 95% elevado: {risk_analysis.var_95:.2%}',
                    'suggestion': 'Aumentar capital de risco ou reduzir alavancagem'
                })
        
        return alerts
    
    def _determine_market_outlook(self, regime_analysis: MarketRegimeAnalysis,
                                patterns: List[PatternRecognitionResult]) -> str:
        """Determinar perspectiva geral do mercado"""
        bull_patterns = len([p for p in patterns if 'BULLISH' in p.pattern_type])
        bear_patterns = len([p for p in patterns if 'BEARISH' in p.pattern_type])
        
        if regime_analysis.regime == MarketRegime.TRENDING_BULL and bull_patterns > bear_patterns:
            return "STRONGLY_BULLISH"
        elif regime_analysis.regime == MarketRegime.TRENDING_BEAR and bear_patterns > bull_patterns:
            return "STRONGLY_BEARISH"
        elif bull_patterns > bear_patterns:
            return "CAUTIOUSLY_BULLISH"
        elif bear_patterns > bull_patterns:
            return "CAUTIOUSLY_BEARISH"
        else:
            return "NEUTRAL"
    
    def _determine_optimal_timeframe(self, patterns: List[PatternRecognitionResult],
                                   regime_analysis: MarketRegimeAnalysis) -> str:
        """Determinar timeframe ótimo para trading"""
        if not patterns:
            return "1H"
        
        # Lógica simplificada para determinar melhor timeframe
        timeframes = [p.timeframe for p in patterns if hasattr(p, 'timeframe')]
        if timeframes:
            return max(set(timeframes), key=timeframes.count)
        
        return "1H"
    
    def _calculate_market_sentiment(self, technical_indicators: List[TechnicalIndicators]) -> Dict[str, float]:
        """Calcular sentimento de mercado"""
        if not technical_indicators:
            return {'bullish': 0.5, 'bearish': 0.5, 'neutral': 0.5}
        
        latest = technical_indicators[-1]
        
        # Fatores para sentimento bullish
        bullish_factors = []
        if latest.rsi > 50:
            bullish_factors.append(0.7)
        if latest.macd > latest.macd_signal:
            bullish_factors.append(0.8)
        if latest.sma_20 > latest.sma_50:
            bullish_factors.append(0.6)
        
        # Fatores para sentimento bearish
        bearish_factors = []
        if latest.rsi < 50:
            bearish_factors.append(0.7)
        if latest.macd < latest.macd_signal:
            bearish_factors.append(0.8)
        if latest.sma_20 < latest.sma_50:
            bearish_factors.append(0.6)
        
        bullish_score = np.mean(bullish_factors) if bullish_factors else 0.3
        bearish_score = np.mean(bearish_factors) if bearish_factors else 0.3
        neutral_score = 1.0 - abs(bullish_score - bearish_score)
        
        # Normalizar
        total = bullish_score + bearish_score + neutral_score
        return {
            'bullish': bullish_score / total,
            'bearish': bearish_score / total,
            'neutral': neutral_score / total
        }

# =============================================================================
# CLASSE PRINCIPAL EXPANDIDA
# =============================================================================

ORIG = r"c:\Users\alexm\Desktop\LEX.I.A\.venv\neural\DeepNeuralNetwork.py"

if os.path.exists(ORIG):
    spec = importlib.util.spec_from_file_location("deep_neural_network_orig", ORIG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    DeepNeuralNetwork = getattr(mod, "DeepNeuralNetwork")
else:
    class DeepNeuralNetwork:
        """Rede Neural Profunda com capacidades expandidas"""
        
        def __init__(self):
            self.analysis_system = AdvancedMarketAnalysisSystem()
            self.is_initialized = False
            self.last_analysis = None
        
        def initialize(self) -> None:
            """Inicializar sistema de análise"""
            self.is_initialized = True
            print("Sistema de Análise de Mercado Inicializado")
        
        def comprehensive_market_analysis(self, market_data: List[Dict]) -> Dict[str, Any]:
            """Executar análise completa de mercado"""
            if not self.is_initialized:
                self.initialize()
            
            # Converter dados de mercado
            converted_data = self._convert_market_data(market_data)
            
            # Executar análise
            analysis_result = self.analysis_system.comprehensive_analysis(converted_data)
            self.last_analysis = analysis_result
            
            return analysis_result
        
        def real_time_monitoring(self, market_data: List[Dict]) -> Dict[str, Any]:
            """Monitoramento em tempo real"""
            analysis = self.comprehensive_market_analysis(market_data)
            
            # Extrair informações críticas para monitoramento
            critical_info = {
                'timestamp': datetime.now(),
                'market_regime': analysis['regime_analysis'].regime.value,
                'regime_confidence': analysis['regime_analysis'].confidence,
                'detected_patterns': len(analysis['patterns']),
                'top_pattern': analysis['patterns'][0].pattern_name if analysis['patterns'] else 'None',
                'overall_confidence': analysis['synthesis']['overall_confidence'],
                'market_outlook': analysis['synthesis']['market_outlook'],
                'risk_alerts': len(analysis['synthesis']['risk_alerts']),
                'recommendations': len(analysis['synthesis']['trading_recommendations'])
            }
            
            return critical_info
        
        def render_html(self) -> str:
            """Renderizar análise em HTML"""
            if not self.last_analysis:
                return "<div class='card'>Nenhuma análise disponível</div>"
            
            analysis = self.last_analysis
            
            html = f"""
            <div class="advanced-analysis-container">
                <div class="header">
                    <h2>🧠 ANÁLISE AVANÇADA DE MERCADO</h2>
                    <p class="timestamp">Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="summary-grid">
                    <div class="summary-card regime">
                        <h3>📊 REGIME DE MERCADO</h3>
                        <p class="regime-value">{analysis['regime_analysis'].regime.value}</p>
                        <p class="confidence">Confiança: {analysis['regime_analysis'].confidence:.1%}</p>
                    </div>
                    
                    <div class="summary-card patterns">
                        <h3>🎯 PADRÕES DETECTADOS</h3>
                        <p class="pattern-count">{len(analysis['patterns'])} padrões</p>
                        <p class="top-pattern">Top: {analysis['patterns'][0].pattern_name if analysis['patterns'] else 'Nenhum'}</p>
                    </div>
                    
                    <div class="summary-card outlook">
                        <h3>🔮 PERSPECTIVA</h3>
                        <p class="outlook-value">{analysis['synthesis']['market_outlook']}</p>
                        <p class="confidence">Confiança Geral: {analysis['synthesis']['overall_confidence']:.1%}</p>
                    </div>
                    
                    <div class="summary-card risk">
                        <h3>⚠️ ALERTAS DE RISCO</h3>
                        <p class="alert-count">{len(analysis['synthesis']['risk_alerts'])} alertas</p>
                        <p class="sentiment">Sentimento: {analysis['synthesis']['market_sentiment']['bullish']:.1%} Bullish</p>
                    </div>
                </div>
                
                <div class="recommendations-section">
                    <h3>💡 RECOMENDAÇÕES</h3>
                    <div class="recommendations-grid">
            """
            
            for rec in analysis['synthesis']['trading_recommendations'][:5]:
                html += f"""
                        <div class="recommendation-card">
                            <h4>{rec['action']} - {rec['pattern']}</h4>
                            <p>Confiança: {rec['confidence']:.1%}</p>
                            <p>RR: 1:{rec['risk_reward']:.2f}</p>
                            <p class="rationale">{rec['rationale']}</p>
                        </div>
                """
            
            html += """
                    </div>
                </div>
                
                <div class="patterns-section">
                    <h3>📈 PADRÕES IDENTIFICADOS</h3>
                    <div class="patterns-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Padrão</th>
                                    <th>Tipo</th>
                                    <th>Confiança</th>
                                    <th>Alvo</th>
                                    <th>Stop</th>
                                    <th>R:R</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            for pattern in analysis['patterns'][:10]:
                html += f"""
                                <tr>
                                    <td>{pattern.pattern_name}</td>
                                    <td>{pattern.pattern_type}</td>
                                    <td>{pattern.confidence:.1%}</td>
                                    <td>{pattern.target_price:.4f}</td>
                                    <td>{pattern.stop_loss:.4f}</td>
                                    <td>1:{pattern.risk_reward:.2f}</td>
                                </tr>
                """
            
            html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <style>
            .advanced-analysis-container { 
                font-family: Arial, sans-serif; 
                background: #1e293b; 
                color: white; 
                padding: 20px; 
                border-radius: 10px; 
            }
            .header { text-align: center; margin-bottom: 30px; }
            .summary-grid { 
                display: grid; 
                grid-template-columns: repeat(4, 1fr); 
                gap: 15px; 
                margin-bottom: 30px; 
            }
            .summary-card { 
                background: #334155; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center; 
            }
            .recommendations-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 15px; 
            }
            .recommendation-card { 
                background: #475569; 
                padding: 15px; 
                border-radius: 6px; 
                border-left: 4px solid #3b82f6; 
            }
            .patterns-table table { 
                width: 100%; 
                border-collapse: collapse; 
            }
            .patterns-table th, .patterns-table td { 
                padding: 10px; 
                text-align: left; 
                border-bottom: 1px solid #475569; 
            }
            .patterns-table th { 
                background: #334155; 
            }
            </style>
            """
            
            return html
        
        def _convert_market_data(self, market_data: List[Dict]) -> List[MarketData]:
            """Converter dados de mercado para formato interno"""
            converted = []
            
            for data in market_data:
                converted.append(MarketData(
                    timestamp=datetime.fromisoformat(data['timestamp']),
                    open=float(data['open']),
                    high=float(data['high']),
                    low=float(data['low']),
                    close=float(data['close']),
                    volume=float(data['volume']),
                    vwap=float(data.get('vwap', data['close'])),
                    typical_price=(float(data['high']) + float(data['low']) + float(data['close'])) / 3
                ))
            
            return converted
        
        def get_technical_indicators(self, market_data: List[Dict]) -> List[TechnicalIndicators]:
            """Obter indicadores técnicos para dados de mercado"""
            converted_data = self._convert_market_data(market_data)
            return self.analysis_system.technical_analyzer.calculate_all_indicators(converted_data)
        
        def backtest_strategy(self, market_data: List[Dict], strategy_rules: Dict) -> Dict[str, Any]:
            """Backtest de estratégia de trading"""
            # Implementação simplificada do backtest
            converted_data = self._convert_market_data(market_data)
            technical_indicators = self.analysis_system.technical_analyzer.calculate_all_indicators(converted_data)
            
            results = {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'win_rate': 0.0,
                'profit_factor': 0.0
            }
            
            # Lógica de backtest seria implementada aqui
            # ...
            
            return results

# =============================================================================
# EXEMPLO DE USO
# =============================================================================

def example_usage():
    """Exemplo de uso do sistema avançado"""
    
    # Criar instância
    dnn = DeepNeuralNetwork()
    
    # Gerar dados de exemplo
    sample_data = []
    base_price = 100.0
    
    for i in range(500):
        timestamp = datetime.now() - timedelta(minutes=500-i)
        price_change = np.random.normal(0, 0.5)
        close_price = base_price * (1 + price_change/100)
        
        sample_data.append({
            'timestamp': timestamp.isoformat(),
            'open': close_price * 0.999,
            'high': close_price * 1.005,
            'low': close_price * 0.995,
            'close': close_price,
            'volume': np.random.uniform(1000, 10000),
            'vwap': close_price
        })
    
    # Executar análise
    analysis = dnn.comprehensive_market_analysis(sample_data)
    
    print("=== ANÁLISE COMPLETA DE MERCADO ===")
    print(f"Regime: {analysis['regime_analysis'].regime.value}")
    print(f"Confiança do Regime: {analysis['regime_analysis'].confidence:.1%}")
    print(f"Padrões Detectados: {len(analysis['patterns'])}")
    print(f"Perspectiva: {analysis['synthesis']['market_outlook']}")
    print(f"Confiança Geral: {analysis['synthesis']['overall_confidence']:.1%}")
    
    # Mostrar recomendações
    print("\n=== RECOMENDAÇÕES ===")
    for rec in analysis['synthesis']['trading_recommendations'][:3]:
        print(f"{rec['action']} - {rec['pattern']} (Conf: {rec['confidence']:.1%}, R:R: 1:{rec['risk_reward']:.2f})")
    
    # Gerar HTML
    html_output = dnn.render_html()
    print(f"\nHTML gerado: {len(html_output)} caracteres")

if __name__ == "__main__":
    example_usage()