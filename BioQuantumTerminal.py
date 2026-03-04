import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any, Tuple, Callable
from enum import Enum, auto
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json
import csv
import pandas as pd
import hashlib
import pickle
import queue
import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


# --- Enums and Enhanced Types ---
class TradingPhase(Enum):
    IDLE = "AGUARDANDO"
    DATA_LOADING = "CARREGANDO DADOS"
    PREPROCESSING = "PRÉ-PROCESSAMENTO"
    TRAINING = "TREINAMENTO"
    INFERENCE = "GERANDO SINAIS"
    BACKTESTING = "BACKTESTING"
    COMPLETE = "COMPLETO"
    ERROR = "ERRO"


class SignalStrength(Enum):
    WEAK = 0.3
    MODERATE = 0.6
    STRONG = 0.85
    VERY_STRONG = 0.95


class AssetClass(Enum):
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"
    STOCKS = "AÇÕES"
    INDICES = "ÍNDICES"
    COMMODITIES = "COMMODITIES"
    FUTURES = "FUTUROS"


class RiskLevel(Enum):
    LOW = "BAIXO"
    MEDIUM = "MÉDIO"
    HIGH = "ALTO"
    EXTREME = "EXTREMO"


class TimeFrame(Enum):
    TICK = "TICK"
    M1 = "1MIN"
    M5 = "5MIN"
    M15 = "15MIN"
    M30 = "30MIN"
    H1 = "1HORA"
    H4 = "4HORAS"
    D1 = "DIÁRIO"
    W1 = "SEMANAL"
    MN1 = "MENSAL"


@dataclass
class EnhancedTrainingLog:
    epoch: int
    loss: float
    mae: float
    accuracy: float
    val_loss: Optional[float] = None
    val_mae: Optional[float] = None
    learning_rate: float = 0.001
    timestamp: str = ""
    quantum_entropy: float = 0.0
    bio_coherence: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EnhancedBioSignal:
    id: str
    date: datetime
    price: float
    predicted_price: float
    action: str  # BUY, SELL, HOLD
    confidence: float
    strength: SignalStrength
    risk_level: RiskLevel
    time_frame: TimeFrame
    asset_class: AssetClass
    expected_return: float = 0.0
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    position_size: float = 0.0
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    technical_indicators: Dict[str, float] = None
    quantum_probability: float = 0.0
    
    def __post_init__(self):
        if self.technical_indicators is None:
            self.technical_indicators = {}
    
    def calculate_risk_reward(self) -> Optional[float]:
        if self.stop_loss and self.take_profit:
            risk = abs(self.price - self.stop_loss)
            reward = abs(self.take_profit - self.price)
            return reward / risk if risk > 0 else None
        return None
    
    def to_csv_row(self) -> List:
        return [
            self.id,
            self.date.isoformat(),
            self.price,
            self.predicted_price,
            self.action,
            self.confidence,
            self.strength.name,
            self.risk_level.value,
            self.expected_return,
            self.stop_loss or "",
            self.take_profit or "",
            self.quantum_probability
        ]


@dataclass
class BioSystemConfig:
    symbol: str
    time_frame: TimeFrame = TimeFrame.H1
    lookback: int = 60
    epochs: int = 100
    trading_threshold: float = 0.002
    batch_size: int = 32
    learning_rate: float = 0.001
    dropout_rate: float = 0.2
    hidden_layers: List[int] = None
    enable_quantum: bool = True
    enable_bio: bool = True
    risk_tolerance: float = 0.05
    max_position_size: float = 0.1
    stop_loss_pct: float = 0.02
    take_profit_pct: float = 0.04
    
    def __post_init__(self):
        if self.hidden_layers is None:
            self.hidden_layers = [128, 64, 32]
    
    def to_dict(self) -> Dict:
        return {
            k: v.value if isinstance(v, Enum) else v
            for k, v in asdict(self).items()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BioSystemConfig':
        return cls(**data)


@dataclass
class EnhancedLearningStatus:
    phase: str
    knowledge_size: int
    total_experiences: int
    quantum_advantage: float
    success_rate: float
    bio_coherence: float
    neural_plasticity: float
    memory_consolidation: float
    active_patterns: int
    last_learning: datetime
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "Quantum Advantage": f"{self.quantum_advantage:.2f}x",
            "Success Rate": f"{self.success_rate:.1%}",
            "Bio Coherence": f"{self.bio_coherence:.2f}Hz",
            "Neural Plasticity": f"{self.neural_plasticity:.1%}",
            "Active Patterns": self.active_patterns,
            "Knowledge Base": f"{self.knowledge_size:,} patterns"
        }


# --- Available Assets with Metadata ---
AVAILABLE_ASSETS = [
    ('BTC/USDT', AssetClass.CRYPTO, 'Bitcoin'),
    ('ETH/USDT', AssetClass.CRYPTO, 'Ethereum'),
    ('SOL/USDT', AssetClass.CRYPTO, 'Solana'),
    ('EURUSD', AssetClass.FOREX, 'Euro/Dólar'),
    ('GBPUSD', AssetClass.FOREX, 'Libra/Dólar'),
    ('USDJPY', AssetClass.FOREX, 'Dólar/Yen'),
    ('EURJPY', AssetClass.FOREX, 'Euro/Yen'),
    ('XAUUSD', AssetClass.COMMODITIES, 'Ouro'),
    ('XAGUSD', AssetClass.COMMODITIES, 'Prata'),
    ('SPX500', AssetClass.INDICES, 'S&P 500'),
    ('NASDAQ', AssetClass.INDICES, 'NASDAQ'),
    ('AAPL', AssetClass.STOCKS, 'Apple'),
    ('TSLA', AssetClass.STOCKS, 'Tesla'),
    ('MSFT', AssetClass.STOCKS, 'Microsoft'),
    ('CL-OIL', AssetClass.COMMODITIES, 'Petróleo'),
    ('US10Y', AssetClass.FUTURES, 'Tesouro 10Y'),
]


# --- Enhanced Quantum System with Realistic Simulation ---
class EnhancedBioQuantumSystem:
    """Sistema Bio-Quântico Avançado com múltiplas funcionalidades"""
    
    def __init__(self, config: BioSystemConfig):
        self.config = config
        self.is_training = False
        self.current_epoch = 0
        self.training_logs: List[EnhancedTrainingLog] = []
        self.signals: List[EnhancedBioSignal] = []
        self.model_weights = None
        self.quantum_state = None
        self.bio_rhythm = 0.0
        self.performance_metrics = {}
        self.backtest_results = {}
        self.asset_metadata = {}
        
        # Thread safety
        self._lock = threading.Lock()
        self._training_queue = queue.Queue()
        
        # Initialize with asset metadata
        self._initialize_asset_metadata()
        
        print(f"🧬 Bio-Quantum System v3.0 initialized for {config.symbol}")
    
    def _initialize_asset_metadata(self):
        """Initialize metadata for available assets"""
        for symbol, asset_class, description in AVAILABLE_ASSETS:
            self.asset_metadata[symbol] = {
                'class': asset_class,
                'description': description,
                'volatility': random.uniform(0.1, 0.3),
                'correlation': {},
                'optimal_params': {
                    'lookback': random.choice([30, 50, 100]),
                    'threshold': random.uniform(0.001, 0.005),
                    'risk_level': random.choice(['LOW', 'MEDIUM', 'HIGH'])
                }
            }
    
    def initialize(self) -> None:
        """Initialize the bio-quantum system with quantum state preparation"""
        print("⚛️ Preparing quantum state...")
        
        # Initialize quantum state (simulated)
        self.quantum_state = {
            'amplitude': np.random.randn(8) + 1j * np.random.randn(8),
            'entanglement': np.random.rand(8, 8),
            'coherence': random.uniform(0.5, 1.0)
        }
        
        # Initialize bio-rhythm
        self.bio_rhythm = 7.83  # Schumann resonance
        
        # Initialize neural network weights (simulated)
        self.model_weights = {
            'encoder': np.random.randn(64, 32),
            'lstm': np.random.randn(128, 64),
            'attention': np.random.randn(32, 16),
            'output': np.random.randn(16, 1)
        }
        
        print("✅ Bio-Quantum system fully initialized")
    
    def load_realistic_data(self, symbol: str) -> List[Dict]:
        """Load realistic simulated data with market patterns"""
        print(f"📊 Loading realistic data for {symbol}...")
        
        # Get asset metadata
        metadata = self.asset_metadata.get(symbol, {})
        asset_class = metadata.get('class', AssetClass.FOREX)
        
        # Base parameters based on asset class
        if asset_class == AssetClass.CRYPTO:
            base_price = random.uniform(1000, 100000)
            volatility = random.uniform(0.02, 0.05)
            trend_strength = random.uniform(-0.001, 0.001)
        elif asset_class == AssetClass.FOREX:
            base_price = random.uniform(0.5, 200)
            volatility = random.uniform(0.0005, 0.002)
            trend_strength = random.uniform(-0.0001, 0.0001)
        else:
            base_price = random.uniform(10, 1000)
            volatility = random.uniform(0.005, 0.015)
            trend_strength = random.uniform(-0.0005, 0.0005)
        
        data = []
        current_price = base_price
        time = datetime.now() - timedelta(days=30)
        
        # Market regime simulation
        regimes = ['trending_up', 'trending_down', 'ranging', 'volatile']
        current_regime = random.choice(regimes)
        regime_duration = 0
        
        for i in range(1000):
            # Change regime occasionally
            regime_duration += 1
            if regime_duration > random.randint(100, 300):
                current_regime = random.choice([r for r in regimes if r != current_regime])
                regime_duration = 0
            
            # Price movement based on regime
            if current_regime == 'trending_up':
                drift = trend_strength * 2
                vol_multiplier = 0.8
            elif current_regime == 'trending_down':
                drift = -trend_strength * 2
                vol_multiplier = 0.8
            elif current_regime == 'volatile':
                drift = 0
                vol_multiplier = 2.0
            else:  # ranging
                drift = 0
                vol_multiplier = 0.5
            
            # Calculate price change with drift and noise
            change = drift + random.gauss(0, volatility * vol_multiplier)
            current_price *= (1 + change)
            
            # Ensure positive price
            current_price = max(current_price, 0.01)
            
            # Add periodic patterns (weekly, monthly effects)
            if i % 168 == 0:  # Weekly pattern
                current_price *= (1 + random.uniform(-0.02, 0.02))
            
            # Generate OHLC data
            open_price = current_price
            high_price = current_price * (1 + abs(random.gauss(0, volatility * 0.5)))
            low_price = current_price * (1 - abs(random.gauss(0, volatility * 0.5)))
            close_price = current_price
            
            # Calculate volume with some correlation to volatility
            volume = random.uniform(1000, 10000) * (1 + abs(change) * 100)
            
            # Calculate technical indicators
            if i >= 20:
                recent_prices = [d['close'] for d in data[-20:]] + [close_price]
                sma_20 = sum(recent_prices) / len(recent_prices)
                
                # RSI calculation
                gains = []
                losses = []
                for j in range(1, min(15, len(recent_prices))):
                    change_j = recent_prices[j] - recent_prices[j - 1]
                    if change_j > 0:
                        gains.append(change_j)
                    else:
                        losses.append(-change_j)
                
                avg_gain = sum(gains) / len(gains) if gains else 0
                avg_loss = sum(losses) / len(losses) if losses else 0.001
                rsi = 100 - (100 / (1 + avg_gain / avg_loss))
            else:
                sma_20 = close_price
                rsi = 50
            
            data_point = {
                'timestamp': time + timedelta(hours=i),
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume,
                'sma_20': sma_20,
                'rsi': rsi,
                'regime': current_regime,
                'volatility': volatility * vol_multiplier
            }
            
            data.append(data_point)
        
        print(f"✅ Loaded {len(data)} realistic data points")
        return data
    
    def train_enhanced_model(self, progress_callback: Optional[Callable]=None,
                            status_callback: Optional[Callable]=None) -> None:
        """Enhanced training with realistic metrics and quantum effects"""
        
        def training_process():
            self.is_training = True
            self.training_logs.clear()
            
            # Initial quantum state
            quantum_entropy = 1.0
            bio_coherence = self.bio_rhythm
            
            for epoch in range(1, self.config.epochs + 1):
                if not self.is_training:
                    break
                
                self.current_epoch = epoch
                
                # Simulate realistic training metrics with convergence
                base_loss = 0.5 * np.exp(-epoch / 50)
                loss_variation = random.uniform(-0.01, 0.01)
                loss = max(0.001, base_loss + loss_variation)
                
                # MAE follows similar pattern
                mae = loss * 0.7 + random.uniform(0, 0.005)
                
                # Accuracy improves with training
                accuracy = min(0.95, 0.6 + epoch / self.config.epochs * 0.35)
                
                # Validation metrics (slightly worse)
                val_loss = loss * 1.1 + random.uniform(0, 0.01)
                val_mae = mae * 1.05 + random.uniform(0, 0.005)
                
                # Simulate quantum effects
                quantum_entropy *= 0.99  # Decreasing entropy (increasing order)
                quantum_entropy += random.uniform(-0.02, 0.02)
                quantum_entropy = max(0.1, min(1.0, quantum_entropy))
                
                # Bio-coherence oscillation
                bio_coherence = 7.83 + 0.5 * np.sin(epoch * 0.1)
                
                # Learning rate decay
                learning_rate = self.config.learning_rate * (1 / (1 + 0.01 * epoch))
                
                log = EnhancedTrainingLog(
                    epoch=epoch,
                    loss=loss,
                    mae=mae,
                    accuracy=accuracy,
                    val_loss=val_loss,
                    val_mae=val_mae,
                    learning_rate=learning_rate,
                    timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3],
                    quantum_entropy=quantum_entropy,
                    bio_coherence=bio_coherence
                )
                
                with self._lock:
                    self.training_logs.append(log)
                
                # Call progress callback
                if progress_callback:
                    progress_callback(log)
                
                # Call status callback for detailed updates
                if status_callback:
                    status_data = {
                        'epoch': epoch,
                        'total_epochs': self.config.epochs,
                        'loss': loss,
                        'accuracy': accuracy,
                        'quantum_entropy': quantum_entropy,
                        'learning_rate': learning_rate,
                        'phase': 'TRAINING' if epoch < self.config.epochs else 'FINALIZING'
                    }
                    status_callback(status_data)
                
                # Simulate training time with variability
                sleep_time = 0.05 + random.uniform(-0.02, 0.02)
                time.sleep(max(0.01, sleep_time))
            
            self.is_training = False
            
            # Final model optimization
            if status_callback:
                status_callback({'phase': 'QUANTUM_OPTIMIZATION', 'message': 'Optimizing quantum states...'})
            
            time.sleep(0.5)  # Simulate final optimization
            
            if status_callback:
                status_callback({'phase': 'COMPLETE', 'message': 'Training completed successfully'})
        
        # Start training in separate thread
        thread = threading.Thread(target=training_process, daemon=True)
        thread.start()
    
    def generate_enhanced_signals(self, data: Optional[List[Dict]]=None) -> List[EnhancedBioSignal]:
        """Generate enhanced trading signals with risk management"""
        
        if data is None:
            # Generate simulated data if none provided
            data = self.load_realistic_data(self.config.symbol)
        
        signals = []
        base_price = data[0]['close'] if data else 100.0
        
        for i in range(100, len(data)):
            if i >= len(data):
                break
            
            current_point = data[i]
            historical_points = data[max(0, i - 50):i]
            
            # Current price
            current_price = current_point['close']
            
            # Analyze market regime
            market_regime = self._analyze_market_regime(historical_points)
            
            # Calculate technical indicators
            indicators = self._calculate_technical_indicators(historical_points, current_point)
            
            # Generate prediction with uncertainty
            predicted_price = self._generate_prediction(current_price, historical_points, market_regime)
            
            # Calculate expected return
            expected_return = (predicted_price - current_price) / current_price
            
            # Determine signal strength
            signal_strength = self._calculate_signal_strength(expected_return, indicators, market_regime)
            
            # Determine risk level
            risk_level = self._assess_risk_level(indicators, market_regime)
            
            # Generate trading action
            action = self._generate_trading_action(
                expected_return,
                signal_strength,
                risk_level,
                current_price,
                indicators
            )
            
            # Calculate confidence
            confidence = self._calculate_confidence(expected_return, indicators, market_regime)
            
            # Quantum probability
            quantum_probability = self._calculate_quantum_probability(action, confidence)
            
            # Calculate position sizing
            position_size = self._calculate_position_size(
                current_price,
                risk_level,
                confidence,
                self.config.max_position_size
            )
            
            # Calculate stop loss and take profit
            stop_loss, take_profit = self._calculate_risk_levels(
                current_price,
                action,
                indicators['atr'] if 'atr' in indicators else current_price * 0.01,
                risk_level
            )
            
            # Calculate performance metrics
            sharpe_ratio = random.uniform(0.5, 2.0)
            max_drawdown = random.uniform(0.01, 0.05)
            
            signal = EnhancedBioSignal(
                id=f"SIG_{hashlib.md5(f'{current_point['timestamp']}_{current_price}'.encode()).hexdigest()[:8]}",
                date=current_point['timestamp'],
                price=current_price,
                predicted_price=predicted_price,
                action=action,
                confidence=confidence,
                strength=signal_strength,
                risk_level=risk_level,
                time_frame=self.config.time_frame,
                asset_class=self.asset_metadata.get(self.config.symbol, {}).get('class', AssetClass.FOREX),
                expected_return=expected_return,
                stop_loss=stop_loss,
                take_profit=take_profit,
                position_size=position_size,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                technical_indicators=indicators,
                quantum_probability=quantum_probability
            )
            
            signals.append(signal)
        
        self.signals = signals
        print(f"📡 Generated {len(signals)} enhanced trading signals")
        return signals
    
    def _analyze_market_regime(self, data: List[Dict]) -> str:
        """Analyze current market regime"""
        if len(data) < 20:
            return "NEUTRAL"
        
        closes = [d['close'] for d in data]
        returns = np.diff(closes) / closes[:-1]
        
        # Calculate trend
        x = np.arange(len(closes))
        slope, _ = np.polyfit(x, closes, 1)
        slope_pct = slope / np.mean(closes)
        
        # Calculate volatility
        volatility = np.std(returns)
        
        # Determine regime
        if abs(slope_pct) > 0.001:
            return "TRENDING_UP" if slope_pct > 0 else "TRENDING_DOWN"
        elif volatility > np.percentile([0.01, 0.02, 0.03], 75):
            return "VOLATILE"
        else:
            return "RANGING"
    
    def _calculate_technical_indicators(self, historical: List[Dict], current: Dict) -> Dict[str, float]:
        """Calculate technical indicators"""
        closes = [d['close'] for d in historical] + [current['close']]
        
        indicators = {
            'rsi': current.get('rsi', 50),
            'sma_20': current.get('sma_20', current['close']),
            'atr': abs(current['high'] - current['low']) * 0.1,
            'volume_ratio': current['volume'] / (sum(d['volume'] for d in historical[-5:]) / 5) if len(historical) >= 5 else 1.0
        }
        
        # Calculate momentum
        if len(closes) >= 10:
            indicators['momentum'] = (closes[-1] - closes[-10]) / closes[-10]
        
        # Calculate volatility
        if len(closes) >= 20:
            returns = np.diff(closes[-20:]) / closes[-21:-1]
            indicators['volatility'] = np.std(returns)
        
        return indicators
    
    def _generate_prediction(self, current_price: float, historical: List[Dict], regime: str) -> float:
        """Generate price prediction based on multiple factors"""
        
        # Base prediction from trend
        if len(historical) >= 10:
            recent_prices = [d['close'] for d in historical[-10:]]
            trend = np.polyfit(range(10), recent_prices, 1)[0]
        else:
            trend = 0
        
        # Regime-based adjustment
        regime_factors = {
            "TRENDING_UP": 1.002,
            "TRENDING_DOWN": 0.998,
            "VOLATILE": 1.000,
            "RANGING": 1.000,
            "NEUTRAL": 1.000
        }
        
        regime_factor = regime_factors.get(regime, 1.000)
        
        # Add some noise
        noise = random.gauss(0, current_price * 0.001)
        
        # Calculate prediction
        prediction = current_price * regime_factor + trend * 0.1 + noise
        
        return prediction
    
    def _calculate_signal_strength(self, expected_return: float, indicators: Dict, regime: str) -> SignalStrength:
        """Calculate signal strength"""
        
        strength_score = 0.0
        
        # Expected return component
        strength_score += min(abs(expected_return) * 100, 0.4)
        
        # RSI component
        rsi = indicators.get('rsi', 50)
        if rsi < 30 or rsi > 70:
            strength_score += 0.2
        
        # Volume component
        volume_ratio = indicators.get('volume_ratio', 1.0)
        if volume_ratio > 1.5:
            strength_score += 0.1
        
        # Momentum component
        momentum = indicators.get('momentum', 0)
        strength_score += abs(momentum) * 10
        
        # Regime component
        if regime in ["TRENDING_UP", "TRENDING_DOWN"]:
            strength_score += 0.1
        
        # Determine strength level
        if strength_score >= 0.8:
            return SignalStrength.VERY_STRONG
        elif strength_score >= 0.6:
            return SignalStrength.STRONG
        elif strength_score >= 0.4:
            return SignalStrength.MODERATE
        else:
            return SignalStrength.WEAK
    
    def _assess_risk_level(self, indicators: Dict, regime: str) -> RiskLevel:
        """Assess risk level for the signal"""
        
        risk_score = 0.0
        
        # Volatility component
        volatility = indicators.get('volatility', 0.01)
        risk_score += min(volatility * 100, 0.4)
        
        # RSI extremes
        rsi = indicators.get('rsi', 50)
        if rsi > 80 or rsi < 20:
            risk_score += 0.3
        
        # Regime risk
        if regime == "VOLATILE":
            risk_score += 0.3
        
        # Determine risk level
        if risk_score >= 0.8:
            return RiskLevel.EXTREME
        elif risk_score >= 0.6:
            return RiskLevel.HIGH
        elif risk_score >= 0.4:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_trading_action(self, expected_return: float, strength: SignalStrength,
                                risk: RiskLevel, current_price: float, indicators: Dict) -> str:
        """Generate trading action based on multiple factors"""
        
        # Base action from expected return
        threshold = self.config.trading_threshold
        
        # Adjust threshold based on risk
        risk_multipliers = {
            RiskLevel.LOW: 0.8,
            RiskLevel.MEDIUM: 1.0,
            RiskLevel.HIGH: 1.2,
            RiskLevel.EXTREME: 1.5
        }
        
        adjusted_threshold = threshold * risk_multipliers.get(risk, 1.0)
        
        # Generate action
        if expected_return > adjusted_threshold:
            return "BUY"
        elif expected_return < -adjusted_threshold:
            return "SELL"
        else:
            return "HOLD"
    
    def _calculate_confidence(self, expected_return: float, indicators: Dict, regime: str) -> float:
        """Calculate confidence level for the signal"""
        
        confidence_score = 0.0
        
        # Expected return magnitude
        confidence_score += min(abs(expected_return) * 500, 0.3)
        
        # Indicator agreement
        rsi = indicators.get('rsi', 50)
        if (expected_return > 0 and rsi < 70) or (expected_return < 0 and rsi > 30):
            confidence_score += 0.2
        
        # Volume confirmation
        volume_ratio = indicators.get('volume_ratio', 1.0)
        if volume_ratio > 1.2:
            confidence_score += 0.1
        
        # Regime stability
        if regime in ["TRENDING_UP", "TRENDING_DOWN"]:
            confidence_score += 0.2
        elif regime == "RANGING":
            confidence_score += 0.1
        
        # Momentum confirmation
        momentum = indicators.get('momentum', 0)
        if momentum * expected_return > 0:  # Same direction
            confidence_score += 0.2
        
        return min(1.0, confidence_score)
    
    def _calculate_quantum_probability(self, action: str, confidence: float) -> float:
        """Calculate quantum probability for the signal"""
        
        # Simulate quantum superposition
        if action == "BUY":
            base_prob = 0.6
        elif action == "SELL":
            base_prob = 0.6
        else:
            base_prob = 0.8
        
        # Adjust with confidence
        quantum_prob = base_prob * confidence + random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, quantum_prob))
    
    def _calculate_position_size(self, price: float, risk: RiskLevel, confidence: float,
                                max_size: float) -> float:
        """Calculate optimal position size"""
        
        # Risk-based sizing
        risk_multipliers = {
            RiskLevel.LOW: 1.0,
            RiskLevel.MEDIUM: 0.7,
            RiskLevel.HIGH: 0.4,
            RiskLevel.EXTREME: 0.2
        }
        
        base_size = max_size * risk_multipliers.get(risk, 0.5)
        
        # Adjust with confidence
        position_size = base_size * confidence
        
        return position_size
    
    def _calculate_risk_levels(self, price: float, action: str, atr: float, risk: RiskLevel) -> Tuple[float, float]:
        """Calculate stop loss and take profit levels"""
        
        # Risk multiplier based on risk level
        risk_multipliers = {
            RiskLevel.LOW: 1.0,
            RiskLevel.MEDIUM: 1.5,
            RiskLevel.HIGH: 2.0,
            RiskLevel.EXTREME: 3.0
        }
        
        multiplier = risk_multipliers.get(risk, 1.5)
        
        # Calculate stop loss
        if action == "BUY":
            stop_loss = price * (1 - self.config.stop_loss_pct * multiplier)
            take_profit = price * (1 + self.config.take_profit_pct * multiplier)
        elif action == "SELL":
            stop_loss = price * (1 + self.config.stop_loss_pct * multiplier)
            take_profit = price * (1 - self.config.take_profit_pct * multiplier)
        else:
            stop_loss = None
            take_profit = None
        
        # Adjust with ATR if available
        if atr and stop_loss and take_profit:
            if action == "BUY":
                stop_loss = min(stop_loss, price - atr * multiplier)
                take_profit = max(take_profit, price + atr * multiplier * 2)
            elif action == "SELL":
                stop_loss = max(stop_loss, price + atr * multiplier)
                take_profit = min(take_profit, price - atr * multiplier * 2)
        
        return stop_loss, take_profit
    
    def run_backtest(self, signals: List[EnhancedBioSignal], initial_capital: float=10000.0) -> Dict:
        """Run backtest on generated signals"""
        
        print("📊 Running backtest...")
        
        capital = initial_capital
        positions = []
        trades = []
        equity_curve = [capital]
        
        for signal in signals:
            if signal.action == "BUY" and capital > 0:
                # Execute buy
                position_value = capital * signal.position_size
                shares = position_value / signal.price
                
                position = {
                    'entry_price': signal.price,
                    'shares': shares,
                    'entry_time': signal.date,
                    'stop_loss': signal.stop_loss,
                    'take_profit': signal.take_profit
                }
                
                positions.append(position)
                capital -= position_value
                
                trades.append({
                    'type': 'BUY',
                    'price': signal.price,
                    'size': position_value,
                    'time': signal.date,
                    'signal_id': signal.id
                })
            
            elif signal.action == "SELL" and positions:
                # Close positions
                for position in positions[:]:
                    exit_price = signal.price
                    pnl = (exit_price - position['entry_price']) * position['shares']
                    
                    capital += position['entry_price'] * position['shares'] + pnl
                    
                    trades.append({
                        'type': 'SELL',
                        'price': exit_price,
                        'size': position['entry_price'] * position['shares'],
                        'pnl': pnl,
                        'time': signal.date,
                        'signal_id': signal.id
                    })
                    
                    positions.remove(position)
            
            # Check stop losses and take profits
            for position in positions[:]:
                current_price = signal.price
                
                # Check stop loss
                if position['stop_loss'] and (
                    (position['entry_price'] > position['stop_loss'] and current_price <= position['stop_loss']) or
                    (position['entry_price'] < position['stop_loss'] and current_price >= position['stop_loss'])
                ):
                    pnl = (position['stop_loss'] - position['entry_price']) * position['shares']
                    capital += position['entry_price'] * position['shares'] + pnl
                    
                    trades.append({
                        'type': 'STOP_LOSS',
                        'price': position['stop_loss'],
                        'size': position['entry_price'] * position['shares'],
                        'pnl': pnl,
                        'time': signal.date
                    })
                    
                    positions.remove(position)
                
                # Check take profit
                elif position['take_profit'] and (
                    (position['entry_price'] < position['take_profit'] and current_price >= position['take_profit']) or
                    (position['entry_price'] > position['take_profit'] and current_price <= position['take_profit'])
                ):
                    pnl = (position['take_profit'] - position['entry_price']) * position['shares']
                    capital += position['entry_price'] * position['shares'] + pnl
                    
                    trades.append({
                        'type': 'TAKE_PROFIT',
                        'price': position['take_profit'],
                        'size': position['entry_price'] * position['shares'],
                        'pnl': pnl,
                        'time': signal.date
                    })
                    
                    positions.remove(position)
            
            # Calculate current equity
            current_equity = capital
            for position in positions:
                current_equity += signal.price * position['shares']
            
            equity_curve.append(current_equity)
        
        # Close any remaining positions
        for position in positions:
            exit_price = signals[-1].price if signals else position['entry_price']
            pnl = (exit_price - position['entry_price']) * position['shares']
            capital += position['entry_price'] * position['shares'] + pnl
        
        # Calculate metrics
        returns = np.diff(equity_curve) / equity_curve[:-1]
        
        if len(returns) > 0:
            total_return = (equity_curve[-1] - initial_capital) / initial_capital
            sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
            max_drawdown = self._calculate_max_drawdown(equity_curve)
            win_rate = len([t for t in trades if t.get('pnl', 0) > 0]) / len(trades) if trades else 0
            avg_win = np.mean([t['pnl'] for t in trades if t.get('pnl', 0) > 0]) if any(t.get('pnl', 0) > 0 for t in trades) else 0
            avg_loss = np.mean([abs(t['pnl']) for t in trades if t.get('pnl', 0) < 0]) if any(t.get('pnl', 0) < 0 for t in trades) else 0
            profit_factor = abs(sum(t['pnl'] for t in trades if t.get('pnl', 0) > 0) / 
                              sum(t['pnl'] for t in trades if t.get('pnl', 0) < 0)) if any(t.get('pnl', 0) < 0 for t in trades) else float('inf')
        else:
            total_return = 0
            sharpe_ratio = 0
            max_drawdown = 0
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            profit_factor = 0
        
        results = {
            'initial_capital': initial_capital,
            'final_capital': equity_curve[-1],
            'total_return': total_return,
            'total_trades': len(trades),
            'winning_trades': len([t for t in trades if t.get('pnl', 0) > 0]),
            'losing_trades': len([t for t in trades if t.get('pnl', 0) < 0]),
            'win_rate': win_rate,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'equity_curve': equity_curve,
            'trades': trades
        }
        
        self.backtest_results = results
        print(f"✅ Backtest completed: {total_return:.2%} return, {len(trades)} trades")
        
        return results
    
    def _calculate_max_drawdown(self, equity_curve: List[float]) -> float:
        """Calculate maximum drawdown from equity curve"""
        if not equity_curve:
            return 0.0
        
        peak = equity_curve[0]
        max_dd = 0.0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
        
        return max_dd
    
    def stop_training(self) -> None:
        """Stop the training process"""
        self.is_training = False
        print("⏹️ Training stopped by user")
    
    def save_model(self, filepath: str) -> None:
        """Save the model to a file"""
        model_data = {
            'config': self.config.to_dict(),
            'weights': self.model_weights,
            'quantum_state': self.quantum_state,
            'training_logs': [log.to_dict() for log in self.training_logs],
            'performance_metrics': self.performance_metrics
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """Load a model from a file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.config = BioSystemConfig.from_dict(model_data['config'])
        self.model_weights = model_data['weights']
        self.quantum_state = model_data['quantum_state']
        self.training_logs = [EnhancedTrainingLog(**log) for log in model_data['training_logs']]
        self.performance_metrics = model_data.get('performance_metrics', {})
        
        print(f"📂 Model loaded from {filepath}")


# --- Enhanced Continuous Learning Service ---
class EnhancedContinuousLearningService:
    """Enhanced continuous learning service with adaptive capabilities"""
    
    def __init__(self):
        self.phases = ["COLLECTING", "PROCESSING", "LEARNING", "OPTIMIZING", "CONSOLIDATING"]
        self.current_phase_index = 0
        self.knowledge_base = random.randint(1000, 5000)
        self.total_experiences = random.randint(5000, 20000)
        self.quantum_advantage = random.uniform(1.5, 4.0)
        self.success_rate = random.uniform(0.7, 0.98)
        self.bio_coherence = random.uniform(7.0, 8.5)
        self.neural_plasticity = random.uniform(0.3, 0.9)
        self.memory_consolidation = random.uniform(0.5, 0.95)
        self.active_patterns = random.randint(50, 200)
        self.last_learning = datetime.now()
        
        self.learning_cycles = 0
        self.phase_durations = [3, 2, 5, 3, 2]  # Duration in seconds per phase
    
    def get_status(self) -> EnhancedLearningStatus:
        """Get current learning status with adaptive improvements"""
        
        # Cycle through phases
        current_time = time.time()
        phase_duration = self.phase_durations[self.current_phase_index]
        
        if current_time - self.last_learning.timestamp() > phase_duration:
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phases)
            self.learning_cycles += 1
            self.last_learning = datetime.now()
            
            # Simulate learning improvements
            self._simulate_learning_improvements()
        
        return EnhancedLearningStatus(
            phase=self.phases[self.current_phase_index],
            knowledge_size=self.knowledge_base,
            total_experiences=self.total_experiences,
            quantum_advantage=self.quantum_advantage,
            success_rate=self.success_rate,
            bio_coherence=self.bio_coherence,
            neural_plasticity=self.neural_plasticity,
            memory_consolidation=self.memory_consolidation,
            active_patterns=self.active_patterns,
            last_learning=self.last_learning
        )
    
    def _simulate_learning_improvements(self):
        """Simulate continuous learning improvements"""
        
        # Knowledge grows with experiences
        self.knowledge_base += random.randint(1, 10)
        self.total_experiences += random.randint(5, 20)
        
        # Quantum advantage fluctuates but trends upward
        self.quantum_advantage += random.uniform(-0.05, 0.1)
        self.quantum_advantage = max(1.0, min(10.0, self.quantum_advantage))
        
        # Success rate improves with experience
        self.success_rate += random.uniform(-0.005, 0.01)
        self.success_rate = max(0.5, min(0.995, self.success_rate))
        
        # Bio-coherence oscillates naturally
        self.bio_coherence = 7.83 + random.uniform(-0.5, 0.5)
        
        # Neural plasticity decreases with consolidation
        self.neural_plasticity -= random.uniform(0.001, 0.005)
        self.neural_plasticity = max(0.1, self.neural_plasticity)
        
        # Memory consolidation improves
        self.memory_consolidation += random.uniform(0.001, 0.01)
        self.memory_consolidation = min(0.99, self.memory_consolidation)
        
        # Active patterns fluctuate
        self.active_patterns += random.randint(-5, 10)
        self.active_patterns = max(10, self.active_patterns)
    
    def reset_learning(self):
        """Reset the learning process"""
        self.current_phase_index = 0
        self.learning_cycles = 0
        print("🔄 Learning process reset")


# --- Main Bio-Quantum Terminal Application ---
class EnhancedBioQuantumTerminal:
    """Enhanced Bio-Quantum Terminal with advanced features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🧬 SISTEMA BIO-QUANTUM v3.0")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#0a0a0a")
        
        # Set window icon
        try:
            self.root.iconbitmap("brain.ico")  # You can create this icon file
        except:
            pass
        
        # State management
        self.config = BioSystemConfig(symbol='BTC/USDT')
        self.logs: List[EnhancedTrainingLog] = []
        self.signals: List[EnhancedBioSignal] = []
        self.is_training = False
        self.training_progress = 0
        self.learning_status: Optional[EnhancedLearningStatus] = None
        self.backtest_results: Optional[Dict] = None
        self.current_data: Optional[List[Dict]] = None
        
        # Services
        self.system: Optional[EnhancedBioQuantumSystem] = None
        self.continuous_learner = EnhancedContinuousLearningService()
        
        # Thread pool
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Initialize
        self.initialize_system()
        
        # Setup UI
        self.setup_ui()
        
        # Start updates
        self.start_status_updates()
        self.start_real_time_updates()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def initialize_system(self):
        """Initialize the bio-quantum system"""
        self.system = EnhancedBioQuantumSystem(self.config)
        self.system.initialize()
        
        # Load initial data
        self.load_initial_data()
        
        self.add_log("🧬 Bio-Quantum Kernel v3.0 initialized", "SYSTEM")
        self.add_log(f"📊 Asset loaded: {self.config.symbol}", "SYSTEM")
        self.add_log("⚡ System ready for quantum analysis", "SYSTEM")
    
    def load_initial_data(self):
        """Load initial market data"""
        if self.system:
            self.current_data = self.system.load_realistic_data(self.config.symbol)
            self.add_log(f"📈 Loaded {len(self.current_data)} data points", "DATA")
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container
        self.main_container = tk.Frame(self.root, bg="#0a0a0a")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create tabs
        self.setup_dashboard_tab()
        self.setup_training_tab()
        self.setup_signals_tab()
        self.setup_backtest_tab()
        self.setup_analytics_tab()
        self.setup_settings_tab()
        
        # Status bar
        self.setup_status_bar()
    
    def setup_dashboard_tab(self):
        """Setup the main dashboard tab"""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="📊 DASHBOARD")
        
        # Dashboard layout
        dashboard_frame = tk.Frame(self.dashboard_tab, bg="#0a0a0a")
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - System status
        self.setup_system_status(dashboard_frame)
        
        # Middle section - Quick actions and metrics
        self.setup_quick_actions(dashboard_frame)
        
        # Bottom section - Real-time charts
        self.setup_dashboard_charts(dashboard_frame)
    
    def setup_system_status(self, parent):
        """Setup system status panel"""
        status_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=2)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Header
        header_frame = tk.Frame(status_frame, bg="#1a1a2e")
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(header_frame, text="🚀 SISTEMA BIO-QUANTUM v3.0",
                font=("Arial", 14, "bold"), fg="#10b981", bg="#1a1a2e").pack(side=tk.LEFT)
        
        # System indicators
        indicators_frame = tk.Frame(status_frame, bg="#1a1a2e")
        indicators_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # System health indicators
        indicators = [
            ("⚛️ Quantum Core", "OPERATIONAL", "#3b82f6"),
            ("🧬 Bio-Interface", "SYNCHRONIZED", "#10b981"),
            ("🧠 Neural Network", "OPTIMIZED", "#8b5cf6"),
            ("📊 Data Pipeline", "FLOWING", "#f59e0b"),
            ("🎯 Signal Engine", "READY", "#ef4444"),
            ("🛡️ Risk Manager", "ACTIVE", "#06b6d4")
        ]
        
        for i, (label, status, color) in enumerate(indicators):
            frame = tk.Frame(indicators_frame, bg="#1a1a2e")
            frame.grid(row=i // 3, column=i % 3, sticky="w", padx=10, pady=5)
            
            tk.Label(frame, text=label, font=("Arial", 9),
                    fg="#cccccc", bg="#1a1a2e").pack(side=tk.LEFT)
            tk.Label(frame, text="●", font=("Arial", 12),
                    fg=color, bg="#1a1a2e").pack(side=tk.LEFT, padx=(5, 0))
            tk.Label(frame, text=status, font=("Courier", 9, "bold"),
                    fg=color, bg="#1a1a2e").pack(side=tk.LEFT, padx=(2, 0))
    
    def setup_quick_actions(self, parent):
        """Setup quick actions panel"""
        actions_frame = tk.Frame(parent, bg="#0a0a0a")
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Quick actions title
        tk.Label(actions_frame, text="⚡ AÇÕES RÁPIDAS",
                font=("Arial", 11, "bold"), fg="#f59e0b", bg="#0a0a0a").pack(anchor=tk.W, pady=(0, 10))
        
        # Action buttons
        buttons_frame = tk.Frame(actions_frame, bg="#0a0a0a")
        buttons_frame.pack(fill=tk.X)
        
        actions = [
            ("🚀 Treinar Modelo", self.start_training, "#166534"),
            ("📡 Gerar Sinais", self.generate_signals, "#1d4ed8"),
            ("📊 Executar Backtest", self.run_backtest, "#7c3aed"),
            ("💾 Salvar Modelo", self.save_model, "#0f766e"),
            ("📂 Carregar Modelo", self.load_model, "#be185d"),
            ("🔄 Atualizar Dados", self.refresh_data, "#ea580c")
        ]
        
        for i, (text, command, color) in enumerate(actions):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                padx=20,
                pady=10,
                borderwidth=0,
                relief=tk.FLAT
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")
            buttons_frame.grid_columnconfigure(i % 3, weight=1)
    
    def setup_dashboard_charts(self, parent):
        """Setup dashboard mini-charts"""
        charts_frame = tk.Frame(parent, bg="#0a0a0a")
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Two column layout
        left_frame = tk.Frame(charts_frame, bg="#0a0a0a")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_frame = tk.Frame(charts_frame, bg="#0a0a0a")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Performance metrics chart
        self.setup_performance_chart(left_frame)
        
        # Learning progress chart
        self.setup_learning_chart(right_frame)
    
    def setup_performance_chart(self, parent):
        """Setup performance metrics mini-chart"""
        chart_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(chart_frame, text="📈 DESEMPENHO DO MODELO",
                font=("Arial", 10, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=10)
        
        # Create simple matplotlib figure
        self.performance_fig = Figure(figsize=(6, 3), dpi=80, facecolor='#1a1a2e')
        self.performance_ax = self.performance_fig.add_subplot(111)
        self.performance_ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.performance_ax.set_xlabel('Época', color='#666666', fontsize=8)
        self.performance_ax.set_ylabel('Loss / Acurácia', color='#666666', fontsize=8)
        self.performance_ax.tick_params(colors='#666666', labelsize=7)
        self.performance_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Add to Tkinter
        self.performance_canvas = FigureCanvasTkAgg(self.performance_fig, chart_frame)
        self.performance_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def setup_learning_chart(self, parent):
        """Setup learning progress mini-chart"""
        chart_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(chart_frame, text="🧠 APRENDIZADO CONTÍNUO",
                font=("Arial", 10, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=10)
        
        # Create simple matplotlib figure
        self.learning_fig = Figure(figsize=(6, 3), dpi=80, facecolor='#1a1a2e')
        self.learning_ax = self.learning_fig.add_subplot(111)
        self.learning_ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.learning_ax.set_xlabel('Tempo', color='#666666', fontsize=8)
        self.learning_ax.set_ylabel('Taxa de Sucesso', color='#666666', fontsize=8)
        self.learning_ax.tick_params(colors='#666666', labelsize=7)
        self.learning_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Add to Tkinter
        self.learning_canvas = FigureCanvasTkAgg(self.learning_fig, chart_frame)
        self.learning_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def setup_training_tab(self):
        """Setup the training tab"""
        self.training_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.training_tab, text="🏋️‍♂️ TREINAMENTO")
        
        # Training tab layout
        training_frame = tk.Frame(self.training_tab, bg="#0a0a0a")
        training_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Configuration
        left_panel = tk.Frame(training_frame, bg="#0a0a0a")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Configuration panel
        self.setup_configuration_panel(left_panel)
        
        # Training controls
        self.setup_training_controls(left_panel)
        
        # Terminal logs
        self.setup_terminal_logs(left_panel)
        
        # Right panel - Training charts
        right_panel = tk.Frame(training_frame, bg="#0a0a0a")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Training metrics chart
        self.setup_training_chart(right_panel)
        
        # Quantum metrics chart
        self.setup_quantum_chart(right_panel)
    
    def setup_configuration_panel(self, parent):
        """Setup configuration panel with advanced options"""
        config_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(config_frame, text="⚙️ CONFIGURAÇÃO AVANÇADA",
                font=("Arial", 11, "bold"), fg="#f59e0b", bg="#1a1a2e").pack(pady=15)
        
        # Configuration grid
        grid_frame = tk.Frame(config_frame, bg="#1a1a2e")
        grid_frame.pack(padx=15, pady=(0, 15))
        
        # Asset selection with enhanced combobox
        row = 0
        tk.Label(grid_frame, text="Ativo", font=("Arial", 9),
                fg="#cccccc", bg="#1a1a2e").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        self.asset_var = tk.StringVar(value=self.config.symbol)
        self.asset_combo = ttk.Combobox(
            grid_frame,
            textvariable=self.asset_var,
            values=[asset[0] for asset in AVAILABLE_ASSETS],
            state="readonly",
            width=20,
            font=("Courier", 10)
        )
        self.asset_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.asset_combo.bind("<<ComboboxSelected>>", self.on_asset_changed)
        
        # Time frame
        row += 1
        tk.Label(grid_frame, text="Time Frame", font=("Arial", 9),
                fg="#cccccc", bg="#1a1a2e").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        self.timeframe_var = tk.StringVar(value=self.config.time_frame.value)
        self.timeframe_combo = ttk.Combobox(
            grid_frame,
            textvariable=self.timeframe_var,
            values=[tf.value for tf in TimeFrame],
            state="readonly",
            width=20,
            font=("Courier", 10)
        )
        self.timeframe_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        # Lookback
        row += 1
        tk.Label(grid_frame, text="Lookback", font=("Arial", 9),
                fg="#cccccc", bg="#1a1a2e").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        self.lookback_var = tk.IntVar(value=self.config.lookback)
        tk.Scale(
            grid_frame,
            variable=self.lookback_var,
            from_=10,
            to=200,
            orient=tk.HORIZONTAL,
            length=150,
            bg="#1a1a2e",
            fg="#cccccc",
            highlightbackground="#1a1a2e"
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        # Epochs
        row += 1
        tk.Label(grid_frame, text="Épocas", font=("Arial", 9),
                fg="#cccccc", bg="#1a1a2e").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        self.epochs_var = tk.IntVar(value=self.config.epochs)
        tk.Scale(
            grid_frame,
            variable=self.epochs_var,
            from_=10,
            to=500,
            orient=tk.HORIZONTAL,
            length=150,
            bg="#1a1a2e",
            fg="#cccccc",
            highlightbackground="#1a1a2e"
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        # Threshold
        row += 1
        tk.Label(grid_frame, text="Threshold", font=("Arial", 9),
                fg="#cccccc", bg="#1a1a2e").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        self.threshold_var = tk.DoubleVar(value=self.config.trading_threshold)
        tk.Scale(
            grid_frame,
            variable=self.threshold_var,
            from_=0.0001,
            to=0.01,
            resolution=0.0001,
            orient=tk.HORIZONTAL,
            length=150,
            bg="#1a1a2e",
            fg="#cccccc",
            highlightbackground="#1a1a2e"
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        # Risk tolerance
        row += 1
        tk.Label(grid_frame, text="Tolerância Risco", font=("Arial", 9),
                fg="#cccccc", bg="#1a1a2e").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        self.risk_var = tk.DoubleVar(value=self.config.risk_tolerance)
        tk.Scale(
            grid_frame,
            variable=self.risk_var,
            from_=0.01,
            to=0.2,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=150,
            bg="#1a1a2e",
            fg="#cccccc",
            highlightbackground="#1a1a2e"
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
    
    def setup_training_controls(self, parent):
        """Setup training controls panel"""
        controls_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(controls_frame, text="🎯 CONTROLES DE TREINAMENTO",
                font=("Arial", 11, "bold"), fg="#10b981", bg="#1a1a2e").pack(pady=15)
        
        # Control buttons
        buttons_frame = tk.Frame(controls_frame, bg="#1a1a2e")
        buttons_frame.pack(padx=15, pady=(0, 15))
        
        self.train_button = tk.Button(
            buttons_frame,
            text="🚀 INICIAR TREINAMENTO",
            command=self.toggle_training,
            font=("Arial", 10, "bold"),
            bg="#166534",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            padx=30,
            pady=12,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.train_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            buttons_frame,
            text="⏹️ PARAR",
            command=self.stop_training,
            font=("Arial", 10, "bold"),
            bg="#991b1b",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            padx=30,
            pady=12,
            borderwidth=0,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = tk.Frame(controls_frame, bg="#1a1a2e")
        progress_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Progresso: 0%",
            font=("Courier", 10),
            fg="#f59e0b",
            bg="#1a1a2e"
        )
        self.progress_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Status label
        self.training_status_label = tk.Label(
            progress_frame,
            text="Status: AGUARDANDO",
            font=("Courier", 9),
            fg="#cccccc",
            bg="#1a1a2e"
        )
        self.training_status_label.pack(anchor=tk.W)
    
    def setup_terminal_logs(self, parent):
        """Setup terminal logs display"""
        terminal_frame = tk.Frame(parent, bg="black", relief=tk.RAISED, borderwidth=1)
        terminal_frame.pack(fill=tk.BOTH, expand=True)
        
        # Terminal header
        header_frame = tk.Frame(terminal_frame, bg="black")
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(header_frame, text="💻 TERMINAL BIO-QUÂNTICO",
                font=("Courier", 11, "bold"), fg="#10b981", bg="black").pack(side=tk.LEFT)
        
        # Clear button
        tk.Button(
            header_frame,
            text="🧹 Limpar",
            command=self.clear_logs,
            font=("Arial", 8),
            bg="#374151",
            fg="white",
            padx=10,
            pady=2,
            borderwidth=0
        ).pack(side=tk.RIGHT)
        
        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            terminal_frame,
            bg="black",
            fg="#cccccc",
            font=("Consolas", 9),
            insertbackground="#ffffff",
            wrap=tk.WORD,
            borderwidth=0,
            highlightthickness=0
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Configure tags for different log types
        self.logs_text.tag_config("SYSTEM", foreground="#666666")
        self.logs_text.tag_config("TRAINING", foreground="#f59e0b")
        self.logs_text.tag_config("SIGNAL", foreground="#10b981")
        self.logs_text.tag_config("ERROR", foreground="#ef4444")
        self.logs_text.tag_config("WARNING", foreground="#fbbf24")
        self.logs_text.tag_config("INFO", foreground="#3b82f6")
        self.logs_text.tag_config("SUCCESS", foreground="#22c55e")
        
        # Add initial logs
        self.add_log("Sistema Bio-Quantum v3.0 inicializado", "SYSTEM")
        self.add_log("Pronto para análise quântica", "SUCCESS")
    
    def setup_training_chart(self, parent):
        """Setup training metrics chart"""
        chart_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(chart_frame, text="📈 MÉTRICAS DE TREINAMENTO",
                font=("Arial", 11, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=15)
        
        # Create matplotlib figure with multiple subplots
        self.training_fig = Figure(figsize=(10, 6), dpi=80, facecolor='#1a1a2e')
        gs = self.training_fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Loss subplot
        self.loss_ax = self.training_fig.add_subplot(gs[0, 0])
        self.loss_ax.set_facecolor('#1a1a2e')
        self.loss_ax.set_title('Loss vs Val Loss', color='#cccccc', fontsize=10)
        self.loss_ax.set_xlabel('Época', color='#666666', fontsize=8)
        self.loss_ax.set_ylabel('Loss', color='#666666', fontsize=8)
        self.loss_ax.tick_params(colors='#666666', labelsize=7)
        self.loss_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # MAE subplot
        self.mae_ax = self.training_fig.add_subplot(gs[0, 1])
        self.mae_ax.set_facecolor('#1a1a2e')
        self.mae_ax.set_title('MAE vs Val MAE', color='#cccccc', fontsize=10)
        self.mae_ax.set_xlabel('Época', color='#666666', fontsize=8)
        self.mae_ax.set_ylabel('MAE', color='#666666', fontsize=8)
        self.mae_ax.tick_params(colors='#666666', labelsize=7)
        self.mae_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Accuracy subplot
        self.acc_ax = self.training_fig.add_subplot(gs[1, 0])
        self.acc_ax.set_facecolor('#1a1a2e')
        self.acc_ax.set_title('Acurácia', color='#cccccc', fontsize=10)
        self.acc_ax.set_xlabel('Época', color='#666666', fontsize=8)
        self.acc_ax.set_ylabel('Acurácia', color='#666666', fontsize=8)
        self.acc_ax.tick_params(colors='#666666', labelsize=7)
        self.acc_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Learning rate subplot
        self.lr_ax = self.training_fig.add_subplot(gs[1, 1])
        self.lr_ax.set_facecolor('#1a1a2e')
        self.lr_ax.set_title('Taxa de Aprendizado', color='#cccccc', fontsize=10)
        self.lr_ax.set_xlabel('Época', color='#666666', fontsize=8)
        self.lr_ax.set_ylabel('Learning Rate', color='#666666', fontsize=8)
        self.lr_ax.tick_params(colors='#666666', labelsize=7)
        self.lr_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Add to Tkinter
        self.training_canvas = FigureCanvasTkAgg(self.training_fig, chart_frame)
        self.training_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.training_canvas, chart_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_quantum_chart(self, parent):
        """Setup quantum metrics chart"""
        chart_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(chart_frame, text="⚛️ MÉTRICAS QUÂNTICAS",
                font=("Arial", 11, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=15)
        
        # Create matplotlib figure
        self.quantum_fig = Figure(figsize=(10, 4), dpi=80, facecolor='#1a1a2e')
        self.quantum_ax = self.quantum_fig.add_subplot(111)
        self.quantum_ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.quantum_ax.set_xlabel('Época', color='#666666', fontsize=8)
        self.quantum_ax.set_ylabel('Entropia / Coerência', color='#666666', fontsize=8)
        self.quantum_ax.tick_params(colors='#666666', labelsize=7)
        self.quantum_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Add to Tkinter
        self.quantum_canvas = FigureCanvasTkAgg(self.quantum_fig, chart_frame)
        self.quantum_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def setup_signals_tab(self):
        """Setup the signals tab"""
        self.signals_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.signals_tab, text="📡 SINAIS")
        
        # Signals tab layout
        signals_frame = tk.Frame(self.signals_tab, bg="#0a0a0a")
        signals_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top controls
        controls_frame = tk.Frame(signals_frame, bg="#0a0a0a")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(controls_frame, text="🎯 GERADOR DE SINAIS",
                font=("Arial", 12, "bold"), fg="#10b981", bg="#0a0a0a").pack(side=tk.LEFT)
        
        tk.Button(
            controls_frame,
            text="📡 Gerar Sinais",
            command=self.generate_signals,
            font=("Arial", 10, "bold"),
            bg="#1d4ed8",
            fg="white",
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT, padx=(0, 10))
        
        tk.Button(
            controls_frame,
            text="💾 Exportar CSV",
            command=self.export_signals_csv,
            font=("Arial", 10),
            bg="#0f766e",
            fg="white",
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Split pane for signals list and chart
        paned_window = tk.PanedWindow(signals_frame, orient=tk.HORIZONTAL, bg="#0a0a0a")
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left pane - Signals list
        left_pane = tk.Frame(paned_window, bg="#0a0a0a")
        paned_window.add(left_pane, width=600)
        
        # Signals treeview
        self.setup_signals_treeview(left_pane)
        
        # Right pane - Signals chart
        right_pane = tk.Frame(paned_window, bg="#0a0a0a")
        paned_window.add(right_pane)
        
        # Signals chart
        self.setup_signals_chart(right_pane)
    
    def setup_signals_treeview(self, parent):
        """Setup signals treeview with scrollable table"""
        # Frame for treeview
        tree_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ('ID', 'Data', 'Preço', 'Ação', 'Confiança', 'Força', 'Risco', 'Retorno', 'SL', 'TP')
        self.signals_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=20
        )
        
        # Configure columns
        col_widths = [80, 120, 80, 60, 80, 80, 80, 80, 80, 80]
        for col, width in zip(columns, col_widths):
            self.signals_tree.heading(col, text=col)
            self.signals_tree.column(col, width=width, anchor=tk.CENTER)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.signals_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.signals_tree.xview)
        self.signals_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.signals_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Double-click event for signal details
        self.signals_tree.bind('<Double-Button-1>', self.show_signal_details)
    
    def setup_signals_chart(self, parent):
        """Setup signals visualization chart"""
        chart_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(chart_frame, text=f"📊 SINAIS: {self.config.symbol}",
                font=("Arial", 11, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=10)
        
        # Create matplotlib figure
        self.signals_fig = Figure(figsize=(10, 6), dpi=80, facecolor='#1a1a2e')
        self.signals_ax = self.signals_fig.add_subplot(111)
        self.signals_ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.signals_ax.set_xlabel('Tempo', color='#666666', fontsize=9)
        self.signals_ax.set_ylabel('Preço', color='#666666', fontsize=9)
        self.signals_ax.tick_params(colors='#666666', labelsize=8)
        self.signals_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Placeholder text
        self.signals_placeholder = self.signals_ax.text(
            0.5, 0.5,
            'Aguardando geração de sinais...',
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.signals_ax.transAxes,
            fontsize=12,
            color='#666666'
        )
        
        # Add to Tkinter
        self.signals_canvas = FigureCanvasTkAgg(self.signals_fig, chart_frame)
        self.signals_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.signals_canvas, chart_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_backtest_tab(self):
        """Setup the backtest tab"""
        self.backtest_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.backtest_tab, text="📊 BACKTEST")
        
        # Backtest tab layout
        backtest_frame = tk.Frame(self.backtest_tab, bg="#0a0a0a")
        backtest_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top controls
        controls_frame = tk.Frame(backtest_frame, bg="#0a0a0a")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(controls_frame, text="🧪 BACKTEST AUTOMÁTICO",
                font=("Arial", 12, "bold"), fg="#f59e0b", bg="#0a0a0a").pack(side=tk.LEFT)
        
        tk.Button(
            controls_frame,
            text="📊 Executar Backtest",
            command=self.run_backtest,
            font=("Arial", 10, "bold"),
            bg="#7c3aed",
            fg="white",
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Backtest parameters
        params_frame = tk.Frame(backtest_frame, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        params_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(params_frame, text="PARÂMETROS DO BACKTEST",
                font=("Arial", 10, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=10)
        
        param_grid = tk.Frame(params_frame, bg="#1a1a2e")
        param_grid.pack(padx=15, pady=(0, 15))
        
        # Initial capital
        tk.Label(param_grid, text="Capital Inicial ($):",
                font=("Arial", 9), fg="#cccccc", bg="#1a1a2e").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.capital_var = tk.DoubleVar(value=10000.0)
        tk.Entry(
            param_grid,
            textvariable=self.capital_var,
            font=("Courier", 10),
            bg="black",
            fg="white",
            width=15
        ).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Commission
        tk.Label(param_grid, text="Comissão (%):",
                font=("Arial", 9), fg="#cccccc", bg="#1a1a2e").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.commission_var = tk.DoubleVar(value=0.1)
        tk.Entry(
            param_grid,
            textvariable=self.commission_var,
            font=("Courier", 10),
            bg="black",
            fg="white",
            width=15
        ).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Results display
        results_frame = tk.Frame(backtest_frame, bg="#0a0a0a")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left - Metrics
        metrics_frame = tk.Frame(results_frame, bg="#0a0a0a")
        metrics_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.setup_backtest_metrics(metrics_frame)
        
        # Right - Equity curve
        chart_frame = tk.Frame(results_frame, bg="#0a0a0a")
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.setup_equity_chart(chart_frame)
    
    def setup_backtest_metrics(self, parent):
        """Setup backtest metrics display"""
        metrics_container = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        metrics_container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(metrics_container, text="📈 MÉTRICAS DE PERFORMANCE",
                font=("Arial", 11, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=15)
        
        # Metrics grid
        self.metrics_frame = tk.Frame(metrics_container, bg="#1a1a2e")
        self.metrics_frame.pack(padx=15, pady=(0, 15), fill=tk.BOTH, expand=True)
        
        # Placeholder for metrics
        tk.Label(self.metrics_frame, text="Execute um backtest para ver as métricas...",
                font=("Arial", 10), fg="#666666", bg="#1a1a2e").pack(pady=50)
    
    def setup_equity_chart(self, parent):
        """Setup equity curve chart"""
        chart_frame = tk.Frame(parent, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(chart_frame, text="📊 CURVA DE EQUITY",
                font=("Arial", 11, "bold"), fg="#cccccc", bg="#1a1a2e").pack(pady=15)
        
        # Create matplotlib figure
        self.equity_fig = Figure(figsize=(8, 5), dpi=80, facecolor='#1a1a2e')
        self.equity_ax = self.equity_fig.add_subplot(111)
        self.equity_ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.equity_ax.set_xlabel('Tempo', color='#666666', fontsize=9)
        self.equity_ax.set_ylabel('Equity ($)', color='#666666', fontsize=9)
        self.equity_ax.tick_params(colors='#666666', labelsize=8)
        self.equity_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Placeholder
        self.equity_ax.text(
            0.5, 0.5,
            'Aguardando dados de backtest...',
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.equity_ax.transAxes,
            fontsize=12,
            color='#666666'
        )
        
        # Add to Tkinter
        self.equity_canvas = FigureCanvasTkAgg(self.equity_fig, chart_frame)
        self.equity_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def setup_analytics_tab(self):
        """Setup the analytics tab"""
        self.analytics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analytics_tab, text="📈 ANALYTICS")
        
        # Analytics tab would contain advanced analytics
        # For now, add a placeholder
        placeholder = tk.Label(
            self.analytics_tab,
            text="📈 Advanced Analytics Dashboard\n\nComing in v4.0...",
            font=("Arial", 16),
            fg="#666666",
            bg="#0a0a0a"
        )
        placeholder.pack(expand=True)
    
    def setup_settings_tab(self):
        """Setup the settings tab"""
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="⚙️ SETTINGS")
        
        # Settings tab would contain system settings
        # For now, add a placeholder
        placeholder = tk.Label(
            self.settings_tab,
            text="⚙️ System Settings\n\nConfigure system preferences...",
            font=("Arial", 16),
            fg="#666666",
            bg="#0a0a0a"
        )
        placeholder.pack(expand=True)
    
    def setup_status_bar(self):
        """Setup the status bar at the bottom"""
        self.status_bar = tk.Frame(self.main_container, bg="#1a1a2e", height=30)
        self.status_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_bar.grid_propagate(False)
        
        # Left status
        self.system_status_label = tk.Label(
            self.status_bar,
            text="Sistema: ✅ Operacional",
            font=("Courier", 9),
            fg="#10b981",
            bg="#1a1a2e"
        )
        self.system_status_label.pack(side=tk.LEFT, padx=15)
        
        # Middle status
        self.memory_status_label = tk.Label(
            self.status_bar,
            text="Memória: 45%",
            font=("Courier", 9),
            fg="#f59e0b",
            bg="#1a1a2e"
        )
        self.memory_status_label.pack(side=tk.LEFT, padx=15)
        
        # Right status
        self.time_status_label = tk.Label(
            self.status_bar,
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            font=("Courier", 9),
            fg="#3b82f6",
            bg="#1a1a2e"
        )
        self.time_status_label.pack(side=tk.RIGHT, padx=15)
    
    def start_status_updates(self):
        """Start periodic status updates"""

        def update_loop():
            while True:
                # Update learning status
                status = self.continuous_learner.get_status()
                self.learning_status = status
                
                # Update status bar
                self.root.after(0, self.update_status_bar)
                
                # Update learning chart if exists
                if hasattr(self, 'learning_ax'):
                    self.root.after(0, self.update_learning_chart, status)
                
                time.sleep(2)
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
    
    def start_real_time_updates(self):
        """Start real-time updates for charts and status"""

        def update_time():
            while True:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.root.after(0, lambda: self.time_status_label.config(text=current_time))
                time.sleep(1)
        
        thread = threading.Thread(target=update_time, daemon=True)
        thread.start()
    
    def update_status_bar(self):
        """Update the status bar with current information"""
        if self.learning_status:
            metrics = self.learning_status.get_metrics()
            status_text = f"Quantum: {metrics['Quantum Advantage']} | "
            status_text += f"Sucesso: {metrics['Success Rate']} | "
            status_text += f"Padrões: {metrics['Active Patterns']}"
            
            # Update a label if we have one for learning status
            if hasattr(self, 'learning_status_label'):
                self.learning_status_label.config(text=status_text)
    
    def update_learning_chart(self, status: EnhancedLearningStatus):
        """Update the learning chart with new data"""
        if not hasattr(self, 'learning_data'):
            self.learning_data = {'time': [], 'success': []}
        
        # Add new data point
        self.learning_data['time'].append(datetime.now())
        self.learning_data['success'].append(status.success_rate)
        
        # Keep only last 50 points
        if len(self.learning_data['time']) > 50:
            self.learning_data['time'] = self.learning_data['time'][-50:]
            self.learning_data['success'] = self.learning_data['success'][-50:]
        
        # Update plot
        self.learning_ax.clear()
        
        if self.learning_data['time']:
            times = [t.strftime('%H:%M:%S') for t in self.learning_data['time']]
            self.learning_ax.plot(times, self.learning_data['success'], color='#10b981', linewidth=2)
            self.learning_ax.fill_between(times, 0, self.learning_data['success'], alpha=0.3, color='#10b981')
        
        # Configure axes
        self.learning_ax.set_facecolor('#1a1a2e')
        self.learning_ax.set_xlabel('Tempo', color='#666666', fontsize=8)
        self.learning_ax.set_ylabel('Taxa de Sucesso', color='#666666', fontsize=8)
        self.learning_ax.tick_params(colors='#666666', labelsize=7)
        self.learning_ax.set_ylim(0, 1)
        self.learning_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Rotate x-axis labels for readability
        plt.setp(self.learning_ax.get_xticklabels(), rotation=45, ha='right')
        
        # Redraw canvas
        self.learning_canvas.draw()
    
    def on_asset_changed(self, event):
        """Handle asset selection change"""
        new_symbol = self.asset_var.get()
        
        # Update config
        self.config.symbol = new_symbol
        self.config.time_frame = TimeFrame(self.timeframe_var.get())
        self.config.lookback = self.lookback_var.get()
        self.config.epochs = self.epochs_var.get()
        self.config.trading_threshold = self.threshold_var.get()
        self.config.risk_tolerance = self.risk_var.get()
        
        # Reinitialize system
        self.system = EnhancedBioQuantumSystem(self.config)
        self.system.initialize()
        
        # Load new data
        self.load_initial_data()
        
        # Clear previous data
        self.signals = []
        self.logs = []
        self.backtest_results = None
        
        # Update UI
        self.clear_signals_tree()
        self.clear_charts()
        
        self.add_log(f"Ativo alterado para: {new_symbol}", "SYSTEM")
        self.add_log(f"Configuração atualizada", "INFO")
    
    def toggle_training(self):
        """Start or stop the training process"""
        if self.is_training:
            self.stop_training()
        else:
            self.start_training()
    
    def start_training(self):
        """Start the training process"""
        if not self.system:
            messagebox.showerror("Erro", "Sistema não inicializado")
            return
        
        # Update config from UI
        self.config.lookback = self.lookback_var.get()
        self.config.epochs = self.epochs_var.get()
        self.config.trading_threshold = self.threshold_var.get()
        
        # Update state
        self.is_training = True
        self.training_progress = 0
        
        # Update UI
        self.train_button.config(
            text="⏹️ PARAR TREINAMENTO",
            bg="#991b1b",
            activebackground="#dc2626"
        )
        self.stop_button.config(state=tk.NORMAL)
        self.training_status_label.config(
            text="Status: INICIANDO TREINAMENTO...",
            fg="#f59e0b"
        )
        
        # Clear previous logs
        self.logs = []
        self.logs_text.delete(1.0, tk.END)
        
        self.add_log("Iniciando treinamento do modelo Bio-Quântico...", "TRAINING")
        self.add_log(f"Configuração: {self.config.epochs} épocas, lookback={self.config.lookback}", "INFO")
        
        # Start training in separate thread
        def training_wrapper():
            try:
                self.system.train_enhanced_model(
                    progress_callback=self.on_training_progress,
                    status_callback=self.on_training_status
                )
                
                # Training complete
                self.root.after(0, self.on_training_complete)
                
            except Exception as e:
                self.root.after(0, lambda: self.on_training_error(str(e)))
        
        thread = threading.Thread(target=training_wrapper, daemon=True)
        thread.start()
    
    def stop_training(self):
        """Stop the training process"""
        if self.system:
            self.system.stop_training()
        
        self.is_training = False
        
        # Update UI
        self.train_button.config(
            text="🚀 INICIAR TREINAMENTO",
            bg="#166534",
            activebackground="#15803d"
        )
        self.stop_button.config(state=tk.DISABLED)
        self.training_status_label.config(
            text="Status: TREINAMENTO INTERROMPIDO",
            fg="#ef4444"
        )
        
        self.add_log("Treinamento interrompido pelo usuário.", "WARNING")
    
    def on_training_progress(self, log: EnhancedTrainingLog):
        """Handle training progress updates"""
        self.logs.append(log)
        self.training_progress = (log.epoch / self.config.epochs) * 100
        
        # Update UI in main thread
        self.root.after(0, self.update_training_ui, log)
    
    def on_training_status(self, status_data: Dict):
        """Handle training status updates"""
        self.root.after(0, self.update_training_status_ui, status_data)
    
    def update_training_ui(self, log: EnhancedTrainingLog):
        """Update training UI elements"""
        # Update progress
        self.progress_bar['value'] = self.training_progress
        self.progress_label.config(text=f"Progresso: {self.training_progress:.1f}%")
        
        # Add log to terminal
        log_entry = f"[{log.timestamp}] Epoch {log.epoch}/{self.config.epochs}: "
        log_entry += f"loss={log.loss:.5f} mae={log.mae:.5f} acc={log.accuracy:.3f}"
        
        if log.val_loss:
            log_entry += f" val_loss={log.val_loss:.5f}"
        
        self.add_log(log_entry, "TRAINING")
        
        # Update training charts
        self.update_training_charts()
        
        # Update quantum chart
        self.update_quantum_chart(log)
    
    def update_training_status_ui(self, status_data: Dict):
        """Update training status UI"""
        phase = status_data.get('phase', '')
        message = status_data.get('message', '')
        
        if phase:
            status_text = f"Status: {phase}"
            if message:
                status_text += f" - {message}"
            
            self.training_status_label.config(text=status_text)
            
            # Color coding based on phase
            if phase == 'TRAINING':
                self.training_status_label.config(fg="#f59e0b")
            elif phase == 'QUANTUM_OPTIMIZATION':
                self.training_status_label.config(fg="#8b5cf6")
            elif phase == 'COMPLETE':
                self.training_status_label.config(fg="#10b981")
    
    def on_training_complete(self):
        """Handle training completion"""
        self.is_training = False
        
        # Update UI
        self.train_button.config(
            text="🚀 INICIAR TREINAMENTO",
            bg="#166534",
            activebackground="#15803d"
        )
        self.stop_button.config(state=tk.DISABLED)
        self.training_status_label.config(
            text="Status: TREINAMENTO COMPLETO",
            fg="#10b981"
        )
        
        self.add_log(">> Treinamento concluído com sucesso!", "SUCCESS")
        self.add_log(f"Total de épocas: {len(self.logs)}", "INFO")
        
        # Show performance summary
        if self.logs:
            last_log = self.logs[-1]
            summary = f"Performance final: Loss={last_log.loss:.5f}, MAE={last_log.mae:.5f}, Acc={last_log.accuracy:.3f}"
            self.add_log(summary, "SUCCESS")
    
    def on_training_error(self, error_msg: str):
        """Handle training errors"""
        self.is_training = False
        
        # Update UI
        self.train_button.config(
            text="🚀 INICIAR TREINAMENTO",
            bg="#166534",
            activebackground="#15803d"
        )
        self.stop_button.config(state=tk.DISABLED)
        self.training_status_label.config(
            text="Status: ERRO NO TREINAMENTO",
            fg="#ef4444"
        )
        
        self.add_log(f"ERRO: {error_msg}", "ERROR")
    
    def update_training_charts(self):
        """Update all training charts"""
        if not self.logs:
            return
        
        epochs = [log.epoch for log in self.logs]
        losses = [log.loss for log in self.logs]
        maes = [log.mae for log in self.logs]
        accuracies = [log.accuracy for log in self.logs]
        val_losses = [log.val_loss for log in self.logs if log.val_loss]
        val_maes = [log.val_mae for log in self.logs if log.val_mae]
        learning_rates = [log.learning_rate for log in self.logs]
        
        # Update loss chart
        self.loss_ax.clear()
        self.loss_ax.plot(epochs, losses, color='#ef4444', linewidth=2, label='Loss')
        if val_losses:
            self.loss_ax.plot(epochs[:len(val_losses)], val_losses, color='#fca5a5', linewidth=1.5, label='Val Loss')
        self.loss_ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
        self.loss_ax.set_facecolor('#1a1a2e')
        self.loss_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Update MAE chart
        self.mae_ax.clear()
        self.mae_ax.plot(epochs, maes, color='#3b82f6', linewidth=2, label='MAE')
        if val_maes:
            self.mae_ax.plot(epochs[:len(val_maes)], val_maes, color='#93c5fd', linewidth=1.5, label='Val MAE')
        self.mae_ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
        self.mae_ax.set_facecolor('#1a1a2e')
        self.mae_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Update accuracy chart
        self.acc_ax.clear()
        self.acc_ax.plot(epochs, accuracies, color='#10b981', linewidth=2)
        self.acc_ax.set_facecolor('#1a1a2e')
        self.acc_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Update learning rate chart
        self.lr_ax.clear()
        self.lr_ax.plot(epochs, learning_rates, color='#f59e0b', linewidth=2)
        self.lr_ax.set_facecolor('#1a1a2e')
        self.lr_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Redraw all canvases
        self.training_canvas.draw()
    
    def update_quantum_chart(self, log: EnhancedTrainingLog):
        """Update quantum metrics chart"""
        if not hasattr(self, 'quantum_data'):
            self.quantum_data = {'epoch': [], 'entropy': [], 'coherence': []}
        
        self.quantum_data['epoch'].append(log.epoch)
        self.quantum_data['entropy'].append(log.quantum_entropy)
        self.quantum_data['coherence'].append(log.bio_coherence)
        
        # Update plot
        self.quantum_ax.clear()
        
        if self.quantum_data['epoch']:
            self.quantum_ax.plot(self.quantum_data['epoch'], self.quantum_data['entropy'],
                                color='#8b5cf6', linewidth=2, label='Entropia Quântica')
            self.quantum_ax.plot(self.quantum_data['epoch'], self.quantum_data['coherence'],
                                color='#06b6d4', linewidth=2, label='Coerência Bio', linestyle='--')
        
        self.quantum_ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
        self.quantum_ax.set_facecolor('#1a1a2e')
        self.quantum_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        self.quantum_canvas.draw()
    
    def generate_signals(self):
        """Generate trading signals"""
        if not self.system:
            messagebox.showerror("Erro", "Sistema não inicializado")
            return
        
        if not self.current_data:
            messagebox.showwarning("Aviso", "Nenhum dado carregado")
            return
        
        self.add_log("Iniciando geração de sinais...", "SIGNAL")
        
        # Run in separate thread
        def generate_wrapper():
            try:
                signals = self.system.generate_enhanced_signals(self.current_data)
                self.root.after(0, lambda: self.on_signals_generated(signals))
            except Exception as e:
                self.root.after(0, lambda: self.on_signals_error(str(e)))
        
        thread = threading.Thread(target=generate_wrapper, daemon=True)
        thread.start()
    
    def on_signals_generated(self, signals: List[EnhancedBioSignal]):
        """Handle signals generation completion"""
        self.signals = signals
        
        # Update signals treeview
        self.update_signals_tree()
        
        # Update signals chart
        self.update_signals_chart_visualization()
        
        self.add_log(f"✅ {len(signals)} sinais gerados com sucesso!", "SUCCESS")
        
        # Show statistics
        buy_count = sum(1 for s in signals if s.action == "BUY")
        sell_count = sum(1 for s in signals if s.action == "SELL")
        hold_count = sum(1 for s in signals if s.action == "HOLD")
        
        stats = f"Estatísticas: BUY={buy_count} | SELL={sell_count} | HOLD={hold_count}"
        self.add_log(stats, "INFO")
    
    def on_signals_error(self, error_msg: str):
        """Handle signals generation errors"""
        self.add_log(f"ERRO na geração de sinais: {error_msg}", "ERROR")
    
    def update_signals_tree(self):
        """Update the signals treeview"""
        # Clear existing items
        self.clear_signals_tree()
        
        # Add new items
        for signal in self.signals[-50:]:  # Show last 50 signals
            values = (
                signal.id,
                signal.date.strftime('%Y-%m-%d %H:%M'),
                f"{signal.price:.4f}",
                signal.action,
                f"{signal.confidence:.1%}",
                signal.strength.name,
                signal.risk_level.value,
                f"{signal.expected_return:.2%}",
                f"{signal.stop_loss:.4f}" if signal.stop_loss else "",
                f"{signal.take_profit:.4f}" if signal.take_profit else ""
            )
            
            # Color coding for actions
            tags = ()
            if signal.action == "BUY":
                tags = ('buy',)
            elif signal.action == "SELL":
                tags = ('sell',)
            else:
                tags = ('hold',)
            
            self.signals_tree.insert('', tk.END, values=values, tags=tags)
        
        # Configure tag colors
        self.signals_tree.tag_configure('buy', foreground='#10b981')
        self.signals_tree.tag_configure('sell', foreground='#ef4444')
        self.signals_tree.tag_configure('hold', foreground='#6b7280')
    
    def clear_signals_tree(self):
        """Clear the signals treeview"""
        for item in self.signals_tree.get_children():
            self.signals_tree.delete(item)
    
    def update_signals_chart_visualization(self):
        """Update the signals visualization chart"""
        if not self.signals:
            return
        
        # Remove placeholder
        if hasattr(self, 'signals_placeholder'):
            self.signals_placeholder.remove()
        
        # Prepare data
        dates = [s.date for s in self.signals]
        prices = [s.price for s in self.signals]
        predicted = [s.predicted_price for s in self.signals]
        
        # Clear and update plot
        self.signals_ax.clear()
        
        # Plot price line
        self.signals_ax.plot(dates, prices, color='#4ade80', linewidth=1, label='Preço Real', alpha=0.7)
        
        # Plot predicted prices
        self.signals_ax.plot(dates, predicted, color='#facc15', linewidth=1, label='Previsão', linestyle='--', alpha=0.7)
        
        # Add buy/sell markers
        buy_dates = [s.date for s in self.signals if s.action == "BUY"]
        buy_prices = [s.price for s in self.signals if s.action == "BUY"]
        self.signals_ax.scatter(buy_dates, buy_prices, color='#10b981', s=50, marker='^', label='Compra', zorder=5)
        
        sell_dates = [s.date for s in self.signals if s.action == "SELL"]
        sell_prices = [s.price for s in self.signals if s.action == "SELL"]
        self.signals_ax.scatter(sell_dates, sell_prices, color='#ef4444', s=50, marker='v', label='Venda', zorder=5)
        
        # Configure axes
        self.signals_ax.set_facecolor('#1a1a2e')
        self.signals_ax.set_xlabel('Data', color='#666666', fontsize=9)
        self.signals_ax.set_ylabel('Preço', color='#666666', fontsize=9)
        self.signals_ax.tick_params(colors='#666666', labelsize=8)
        self.signals_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        self.signals_ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
        
        # Format x-axis dates
        plt.setp(self.signals_ax.get_xticklabels(), rotation=45, ha='right')
        
        # Redraw canvas
        self.signals_canvas.draw()
    
    def run_backtest(self):
        """Run backtest on generated signals"""
        if not self.signals:
            messagebox.showwarning("Aviso", "Gere sinais primeiro")
            return
        
        self.add_log("Iniciando backtest...", "INFO")
        
        # Run in separate thread
        def backtest_wrapper():
            try:
                initial_capital = self.capital_var.get()
                results = self.system.run_backtest(self.signals, initial_capital)
                self.root.after(0, lambda: self.on_backtest_complete(results))
            except Exception as e:
                self.root.after(0, lambda: self.on_backtest_error(str(e)))
        
        thread = threading.Thread(target=backtest_wrapper, daemon=True)
        thread.start()
    
    def on_backtest_complete(self, results: Dict):
        """Handle backtest completion"""
        self.backtest_results = results
        
        # Update metrics display
        self.update_backtest_metrics(results)
        
        # Update equity chart
        self.update_equity_chart(results)
        
        self.add_log(f"✅ Backtest concluído!", "SUCCESS")
        self.add_log(f"Retorno total: {results['total_return']:.2%}", "INFO")
        self.add_log(f"Win Rate: {results['win_rate']:.1%}", "INFO")
    
    def on_backtest_error(self, error_msg: str):
        """Handle backtest errors"""
        self.add_log(f"ERRO no backtest: {error_msg}", "ERROR")
    
    def update_backtest_metrics(self, results: Dict):
        """Update backtest metrics display"""
        # Clear existing widgets
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        
        # Create metrics display
        metrics = [
            ("💰 Capital Final", f"${results['final_capital']:,.2f}", "#10b981"),
            ("📈 Retorno Total", f"{results['total_return']:.2%}", "#10b981" if results['total_return'] >= 0 else "#ef4444"),
            ("🎯 Total Trades", f"{results['total_trades']}", "#3b82f6"),
            ("✅ Trades Vencedores", f"{results['winning_trades']}", "#10b981"),
            ("❌ Trades Perdedores", f"{results['losing_trades']}", "#ef4444"),
            ("📊 Win Rate", f"{results['win_rate']:.1%}", "#10b981" if results['win_rate'] >= 0.5 else "#f59e0b"),
            ("⚡ Sharpe Ratio", f"{results['sharpe_ratio']:.2f}", "#10b981" if results['sharpe_ratio'] >= 1 else "#f59e0b"),
            ("📉 Max Drawdown", f"{results['max_drawdown']:.2%}", "#ef4444" if results['max_drawdown'] > 0.1 else "#f59e0b"),
            ("💰 Profit Factor", f"{results['profit_factor']:.2f}", "#10b981" if results['profit_factor'] >= 1.5 else "#f59e0b"),
            ("📈 Média Ganho", f"${results['avg_win']:,.2f}", "#10b981"),
            ("📉 Média Perda", f"${results['avg_loss']:,.2f}", "#ef4444")
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            # Label
            tk.Label(self.metrics_frame, text=label, font=("Arial", 9),
                    fg="#cccccc", bg="#1a1a2e").grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            
            # Value
            tk.Label(self.metrics_frame, text=value, font=("Courier", 10, "bold"),
                    fg=color, bg="#1a1a2e").grid(row=i, column=1, sticky=tk.W, pady=5)
    
    def update_equity_chart(self, results: Dict):
        """Update equity curve chart"""
        if 'equity_curve' not in results:
            return
        
        equity_curve = results['equity_curve']
        
        # Clear plot
        self.equity_ax.clear()
        
        # Plot equity curve
        self.equity_ax.plot(equity_curve, color='#10b981', linewidth=2)
        
        # Fill under curve
        self.equity_ax.fill_between(range(len(equity_curve)), equity_curve, alpha=0.3, color='#10b981')
        
        # Add horizontal line for initial capital
        if equity_curve:
            self.equity_ax.axhline(y=equity_curve[0], color='#6b7280', linestyle='--', alpha=0.5)
        
        # Configure axes
        self.equity_ax.set_facecolor('#1a1a2e')
        self.equity_ax.set_xlabel('Trade #', color='#666666', fontsize=9)
        self.equity_ax.set_ylabel('Equity ($)', color='#666666', fontsize=9)
        self.equity_ax.tick_params(colors='#666666', labelsize=8)
        self.equity_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Add title
        total_return = results['total_return']
        title_color = '#10b981' if total_return >= 0 else '#ef4444'
        self.equity_ax.set_title(f'Equity Curve - Return: {total_return:.2%}', color=title_color, fontsize=11)
        
        # Redraw canvas
        self.equity_canvas.draw()
    
    def refresh_data(self):
        """Refresh market data"""
        if not self.system:
            return
        
        self.add_log("Atualizando dados de mercado...", "INFO")
        
        # Load fresh data
        self.current_data = self.system.load_realistic_data(self.config.symbol)
        
        self.add_log(f"✅ Dados atualizados: {len(self.current_data)} pontos", "SUCCESS")
    
    def save_model(self):
        """Save the current model to a file"""
        if not self.system:
            messagebox.showerror("Erro", "Nenhum modelo para salvar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".bqm",
            filetypes=[("Bio-Quantum Model", "*.bqm"), ("All Files", "*.*")],
            initialfile=f"model_{self.config.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bqm"
        )
        
        if filename:
            try:
                self.system.save_model(filename)
                self.add_log(f"Modelo salvo em: {filename}", "SUCCESS")
            except Exception as e:
                self.add_log(f"Erro ao salvar modelo: {e}", "ERROR")
    
    def load_model(self):
        """Load a model from a file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Bio-Quantum Model", "*.bqm"), ("All Files", "*.*")]
        )
        
        if filename and self.system:
            try:
                self.system.load_model(filename)
                self.add_log(f"Modelo carregado de: {filename}", "SUCCESS")
                
                # Update UI with loaded model info
                self.add_log(f"Modelo treinado com {len(self.system.training_logs)} épocas", "INFO")
                
                # Update training charts
                self.logs = self.system.training_logs
                self.update_training_charts()
                
            except Exception as e:
                self.add_log(f"Erro ao carregar modelo: {e}", "ERROR")
    
    def export_signals_csv(self):
        """Export signals to CSV file"""
        if not self.signals:
            messagebox.showwarning("Aviso", "Nenhum sinal para exportar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile=f"signals_{self.config.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Write header
                    writer.writerow([
                        'ID', 'Date', 'Price', 'Predicted', 'Action',
                        'Confidence', 'Strength', 'Risk', 'Expected_Return',
                        'Stop_Loss', 'Take_Profit', 'Quantum_Probability'
                    ])
                    
                    # Write data
                    for signal in self.signals:
                        writer.writerow(signal.to_csv_row())
                
                self.add_log(f"Sinais exportados para: {filename}", "SUCCESS")
                
            except Exception as e:
                self.add_log(f"Erro ao exportar sinais: {e}", "ERROR")
    
    def show_signal_details(self, event):
        """Show detailed information for a selected signal"""
        selection = self.signals_tree.selection()
        if not selection:
            return
        
        item = self.signals_tree.item(selection[0])
        signal_id = item['values'][0]
        
        # Find the signal
        signal = next((s for s in self.signals if s.id == signal_id), None)
        if not signal:
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Detalhes do Sinal: {signal_id}")
        details_window.geometry("500x600")
        details_window.configure(bg="#0a0a0a")
        
        # Signal details
        details_frame = tk.Frame(details_window, bg="#1a1a2e", relief=tk.RAISED, borderwidth=1)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(details_frame, text=f"📊 DETALHES DO SINAL",
                font=("Arial", 12, "bold"), fg="#10b981", bg="#1a1a2e").pack(pady=15)
        
        # Details grid
        grid_frame = tk.Frame(details_frame, bg="#1a1a2e")
        grid_frame.pack(padx=15, pady=(0, 15))
        
        details = [
            ("ID", signal.id),
            ("Data", signal.date.strftime('%Y-%m-%d %H:%M:%S')),
            ("Ativo", self.config.symbol),
            ("Preço", f"${signal.price:.4f}"),
            ("Previsão", f"${signal.predicted_price:.4f}"),
            ("Ação", signal.action),
            ("Confiança", f"{signal.confidence:.1%}"),
            ("Força", signal.strength.name),
            ("Risco", signal.risk_level.value),
            ("Retorno Esperado", f"{signal.expected_return:.2%}"),
            ("Stop Loss", f"${signal.stop_loss:.4f}" if signal.stop_loss else "N/A"),
            ("Take Profit", f"${signal.take_profit:.4f}" if signal.take_profit else "N/A"),
            ("Probabilidade Quântica", f"{signal.quantum_probability:.1%}")
        ]
        
        for i, (label, value) in enumerate(details):
            # Label
            tk.Label(grid_frame, text=label + ":", font=("Arial", 9),
                    fg="#cccccc", bg="#1a1a2e").grid(row=i, column=0, sticky=tk.W, pady=5)
            
            # Value
            tk.Label(grid_frame, text=value, font=("Courier", 9),
                    fg="#ffffff", bg="#1a1a2e").grid(row=i, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Technical indicators section
        if signal.technical_indicators:
            tk.Label(grid_frame, text="--- Indicadores Técnicos ---",
                    font=("Arial", 10, "bold"), fg="#f59e0b", bg="#1a1a2e").grid(row=len(details), column=0, columnspan=2, pady=(15, 5))
            
            row = len(details) + 1
            for idx, (indicator, value) in enumerate(signal.technical_indicators.items()):
                tk.Label(grid_frame, text=indicator + ":", font=("Arial", 8),
                        fg="#cccccc", bg="#1a1a2e").grid(row=row + idx, column=0, sticky=tk.W, pady=2)
                
                tk.Label(grid_frame, text=f"{value:.4f}", font=("Courier", 8),
                        fg="#ffffff", bg="#1a1a2e").grid(row=row + idx, column=1, sticky=tk.W, pady=2, padx=(10, 0))
    
    def clear_logs(self):
        """Clear the terminal logs"""
        self.logs_text.delete(1.0, tk.END)
        self.add_log("Terminal limpo", "SYSTEM")
    
    def clear_charts(self):
        """Clear all charts"""
        # Clear training charts
        for ax in [self.loss_ax, self.mae_ax, self.acc_ax, self.lr_ax]:
            ax.clear()
            ax.set_facecolor('#1a1a2e')
            ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Clear signals chart
        self.signals_ax.clear()
        self.signals_ax.set_facecolor('#1a1a2e')
        self.signals_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Clear equity chart
        self.equity_ax.clear()
        self.equity_ax.set_facecolor('#1a1a2e')
        self.equity_ax.grid(True, color='#222222', linestyle='--', alpha=0.3)
        
        # Redraw canvases
        self.training_canvas.draw()
        self.signals_canvas.draw()
        self.equity_canvas.draw()
    
    def add_log(self, message: str, log_type: str="INFO"):
        """Add a log message to the terminal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.logs_text.insert(tk.END, formatted_message, log_type)
        self.logs_text.see(tk.END)
        
        # Also print to console for debugging
        print(f"[{log_type}] {message}")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_training:
            if messagebox.askyesno("Confirmar", "O treinamento está em andamento. Deseja realmente sair?"):
                self.system.stop_training()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    # Create main window
    root = tk.Tk()
    
    # Set style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles
    style.configure("TNotebook", background="#0a0a0a", borderwidth=0)
    style.configure("TNotebook.Tab", background="#1a1a2e", foreground="#cccccc", padding=[10, 5])
    style.map("TNotebook.Tab", background=[("selected", "#3b82f6")], foreground=[("selected", "white")])
    
    # Create application
    app = EnhancedBioQuantumTerminal(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()            times = self.learning_data['time']
        self.learning_ax.clear()
            if self.learning_data['success']:
                self.learning_ax.plot(times, self.learning_data['success'], color='#10b981
', linewidth=2)
        self.learning_ax.set_title('Taxa de Sucesso ao Longo do Tempo', color='#ffffff', fontsize=10)
        self.learning_ax.set_xlabel('Tempo', color='#666666', fontsize=8)
        self.learning_ax.set_ylabel('Sucesso', color='#666666', fontsize=8)
        self.learning_ax.tick_params(colors='#666666', labelsize=7)
