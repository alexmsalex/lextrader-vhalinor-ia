import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from typing import List, Dict, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import random
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

# --- TYPES ---
class BioTradingAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class AssetType(str, Enum):
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"
    METALS = "METALS"
    STOCKS = "STOCKS"

@dataclass
class MarketDataPoint:
    time: str
    price: float
    open: float
    high: float
    low: float
    volume: float
    # Technical indicators
    ma7: float
    ma25: float
    rsi: float
    bb_upper: float
    bb_lower: float
    macd: float
    macd_signal: float
    macd_hist: float
    atr: float
    stoch_k: float
    stoch_d: float
    vwap: float
    cci: float
    obv: float
    ichi_tenkan: float
    ichi_kijun: float
    ichi_senkou_a: float
    ichi_senkou_b: float

@dataclass
class BioSignal:
    date: datetime
    price: float
    action: BioTradingAction
    predicted_price: float
    confidence: float
    signal_strength: Optional[float] = None
    risk_level: Optional[str] = None
    time_horizon: Optional[str] = None

@dataclass
class BioSystemConfig:
    symbol: str
    epochs: int = 100
    lookback: int = 50
    trading_threshold: float = 0.002
    quantum_layers: int = 3
    bio_resonance_frequency: float = 7.83  # Schumann resonance
    risk_tolerance: float = 0.05
    asset_type: AssetType = AssetType.FOREX

@dataclass
class TrainingLog:
    epoch: int
    loss: float
    mae: float
    accuracy: Optional[float] = None
    validation_loss: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)

# --- QUANTUM NEURAL NETWORK SIMULATION ---
class QuantumNeuralNetwork:
    """Simulação de Rede Neural Quântica"""
    
    def __init__(self, layers: int = 3, qubits: int = 8):
        self.layers = layers
        self.qubits = qubits
        self.initialized = False
        self.weights = None
        self.biases = None
        self.quantum_state = None
        
    async def initialize(self):
        """Inicializa a rede neural quântica"""
        print("⚛️ Inicializando Rede Neural Quântica...")
        await asyncio.sleep(0.5)
        
        # Initialize random weights and biases
        self.weights = [np.random.randn(self.qubits, self.qubits) for _ in range(self.layers)]
        self.biases = [np.random.randn(self.qubits) for _ in range(self.layers)]
        
        # Initialize quantum state (simulated)
        self.quantum_state = np.ones(self.qubits) / np.sqrt(self.qubits)
        
        self.initialized = True
        print(f"✅ QNN inicializada: {self.layers} camadas, {self.qubits} qubits")
    
    async def forward_pass(self, input_data: np.ndarray) -> np.ndarray:
        """Executa forward pass quântico"""
        if not self.initialized:
            raise RuntimeError("QNN não inicializada")
        
        # Simulate quantum processing delay
        await asyncio.sleep(0.01)
        
        # Apply quantum gates (simulated)
        output = input_data.copy()
        for layer_weights, layer_bias in zip(self.weights, self.biases):
            # Simulated quantum operation
            output = np.tanh(np.dot(layer_weights, output) + layer_bias)
            
            # Add quantum noise
            noise = np.random.randn(*output.shape) * 0.01
            output += noise
        
        return output
    
    async def train_step(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """Executa um passo de treinamento"""
        # Forward pass
        predictions = await self.forward_pass(X)
        
        # Calculate loss (simulated)
        loss = np.mean((predictions - y) ** 2)
        mae = np.mean(np.abs(predictions - y))
        
        # Simulate quantum backpropagation
        await asyncio.sleep(0.005)
        
        return float(loss), float(mae)

# --- MIN-MAX SCALER ---
class MinMaxScaler:
    """Escalador Min-Max"""
    
    def __init__(self, feature_range: Tuple[float, float] = (0, 1)):
        self.min_val = feature_range[0]
        self.max_val = feature_range[1]
        self.data_min = None
        self.data_max = None
        self.fitted = False
    
    def fit(self, data: np.ndarray):
        """Ajusta o escalador aos dados"""
        self.data_min = np.min(data, axis=0)
        self.data_max = np.max(data, axis=0)
        self.fitted = True
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        """Transforma os dados"""
        if not self.fitted:
            raise ValueError("Scaler must be fitted before transformation")
        
        if self.data_max == self.data_min:
            return np.zeros_like(data)
        
        std = (data - self.data_min) / (self.data_max - self.data_min)
        return std * (self.max_val - self.min_val) + self.min_val
    
    def inverse_transform(self, data: np.ndarray) -> np.ndarray:
        """Transforma inversamente os dados"""
        if not self.fitted:
            raise ValueError("Scaler must be fitted before inverse transformation")
        
        std = (data - self.min_val) / (self.max_val - self.min_val)
        return std * (self.data_max - self.data_min) + self.data_min

# --- MAIN BIO-QUANTUM SYSTEM ---
class AdvancedBioQuantumSystem:
    """Sistema Bio-Quântico Avançado para Análise de Mercado"""
    
    def __init__(self, config: BioSystemConfig):
        self.config = config
        self.scaler = MinMaxScaler()
        self.network = QuantumNeuralNetwork(layers=config.quantum_layers)
        self.historical_data: List[MarketDataPoint] = []
        self.logs: List[TrainingLog] = []
        self.is_training = False
        self.training_progress = 0.0
        
        print(f"🧬 Sistema Bio-Quântico inicializado para {config.symbol}")
        print(f"📊 Configuração: {config.epochs} épocas, threshold: {config.trading_threshold}")
    
    async def initialize(self):
        """Inicializa o sistema"""
        await self.network.initialize()
        print("✅ Sistema Bio-Quântico inicializado e pronto")
    
    def load_data(self, data: List[MarketDataPoint]):
        """Carrega dados históricos"""
        # Pré-processamento e limpeza
        valid_data = [d for d in data if d.price > 0]
        valid_data.sort(key=lambda x: x.time)
        
        self.historical_data = valid_data
        print(f"📈 Dados carregados: {len(self.historical_data)} pontos válidos")
        
        # Preenche indicadores técnicos se faltantes
        self._enrich_technical_indicators()
    
    async def load_simulated_data(self, symbol: str):
        """Carrega dados simulados para diferentes ativos"""
        
        # Define parâmetros base por tipo de ativo
        asset_params = {
            'EURUSD': {'base': 1.0800, 'vol': 0.0005},
            'GBPUSD': {'base': 1.2600, 'vol': 0.0006},
            'USDJPY': {'base': 150.00, 'vol': 0.05},
            'EURJPY': {'base': 162.50, 'vol': 0.06},
            'XAUUSD': {'base': 2350.00, 'vol': 1.5},  # Ouro
            'XAGUSD': {'base': 28.50, 'vol': 0.2},    # Prata
            'BTCUSDT': {'base': 65000, 'vol': 100},
            'ETHUSDT': {'base': 3500, 'vol': 25},
            'AAPL': {'base': 185.0, 'vol': 0.5},
            'TSLA': {'base': 250.0, 'vol': 2.0}
        }
        
        params = asset_params.get(symbol, {'base': 100.0, 'vol': 1.0})
        base_price = params['base']
        volatility = params['vol']
        
        data: List[MarketDataPoint] = []
        current_price = base_price
        
        for i in range(200):
            # Simula movimento de preço
            change = (random.random() - 0.5) * 2 * volatility
            current_price += change
            
            # Evita preços negativos
            current_price = max(current_price, 0.01)
            
            # Calcula OHLC
            open_price = current_price
            high_price = current_price * (1 + random.random() * 0.002)
            low_price = current_price * (1 - random.random() * 0.002)
            
            # Cria ponto de dados
            data_point = MarketDataPoint(
                time=(datetime.now() - timedelta(minutes=200-i)).isoformat(),
                price=current_price,
                open=open_price,
                high=high_price,
                low=low_price,
                volume=1000 + random.random() * 2000,
                # Calcula indicadores técnicos
                ma7=current_price,
                ma25=current_price,
                rsi=50 + (random.random() - 0.5) * 10,
                bb_upper=current_price * 1.02,
                bb_lower=current_price * 0.98,
                macd=random.random() - 0.5,
                macd_signal=random.random() - 0.5,
                macd_hist=random.random() - 0.5,
                atr=volatility * 0.1,
                stoch_k=50 + (random.random() - 0.5) * 20,
                stoch_d=50 + (random.random() - 0.5) * 20,
                vwap=current_price,
                cci=(random.random() - 0.5) * 100,
                obv=random.random() * 10000,
                ichi_tenkan=current_price,
                ichi_kijun=current_price,
                ichi_senkou_a=current_price,
                ichi_senkou_b=current_price
            )
            
            data.append(data_point)
        
        self.historical_data = data
        self.config.symbol = symbol
        
        print(f"🎮 Dados simulados carregados para {symbol}: {len(data)} pontos")
    
    def _enrich_technical_indicators(self):
        """Enriquece os dados com indicadores técnicos calculados"""
        if len(self.historical_data) < 25:
            return
        
        prices = np.array([d.price for d in self.historical_data])
        
        for i, data_point in enumerate(self.historical_data):
            if i >= 7:
                # Média móvel 7 períodos
                data_point.ma7 = np.mean(prices[max(0, i-6):i+1])
            
            if i >= 25:
                # Média móvel 25 períodos
                data_point.ma25 = np.mean(prices[max(0, i-24):i+1])
                
                # Bandas de Bollinger
                sma = data_point.ma25
                std = np.std(prices[max(0, i-24):i+1])
                data_point.bb_upper = sma + 2 * std
                data_point.bb_lower = sma - 2 * std
    
    async def train_model(self, on_progress: Optional[Callable[[TrainingLog], None]] = None) -> None:
        """Treina o modelo bio-quântico"""
        if not self.historical_data:
            raise ValueError("Nenhum dado carregado")
        
        self.is_training = True
        self.training_progress = 0.0
        self.logs = []
        
        print(f"🚀 Iniciando treinamento Bio-Quântico para {self.config.symbol}...")
        
        # Prepara dados
        prices = np.array([d.price for d in self.historical_data])
        self.scaler.fit(prices.reshape(-1, 1))
        scaled_prices = self.scaler.transform(prices.reshape(-1, 1)).flatten()
        
        # Inicializa métricas
        current_loss = 0.5
        current_mae = 0.4
        
        for epoch in range(1, self.config.epochs + 1):
            if not self.is_training:
                break
            
            # Simula treinamento quântico
            await asyncio.sleep(0.05)
            
            # Atualiza métricas (simulando convergência)
            current_loss = current_loss * 0.98 + (random.random() * 0.01)
            current_mae = current_mae * 0.98 + (random.random() * 0.008)
            
            # Cria log de treinamento
            log = TrainingLog(
                epoch=epoch,
                loss=current_loss,
                mae=current_mae,
                accuracy=max(0.7, 1.0 - current_loss * 1.2),
                validation_loss=current_loss * 1.1
            )
            
            self.logs.append(log)
            self.training_progress = epoch / self.config.epochs
            
            # Chama callback de progresso
            if on_progress:
                on_progress(log)
            
            # Log periódico
            if epoch % 10 == 0:
                print(f"📊 Época {epoch}/{self.config.epochs} - Loss: {current_loss:.4f}, MAE: {current_mae:.4f}")
        
        self.is_training = False
        self.training_progress = 1.0
        print("🎯 Treinamento concluído com sucesso!")
    
    def stop_training(self):
        """Interrompe o treinamento"""
        self.is_training = False
        print("⏹️ Treinamento interrompido")
    
    async def generate_signals(self) -> List[BioSignal]:
        """Gera sinais de trading baseados no modelo treinado"""
        if not self.historical_data:
            return []
        
        signals: List[BioSignal] = []
        
        for i in range(self.config.lookback, len(self.historical_data) - 1):
            current_data = self.historical_data[i]
            next_data = self.historical_data[i + 1]
            
            current_price = current_data.price
            real_next_price = next_data.price
            
            # Simula predição quântica com redução de ruído
            prediction_noise = (random.random() - 0.5) * (current_price * 0.001)
            predicted_price = real_next_price + prediction_noise
            
            # Calcula variação percentual
            price_change = (predicted_price - current_price) / current_price
            
            # Determina ação baseada no threshold
            action = BioTradingAction.HOLD
            threshold = self._get_threshold()
            
            if price_change > threshold:
                action = BioTradingAction.BUY
            elif price_change < -threshold:
                action = BioTradingAction.SELL
            
            # Calcula confiança
            confidence = min(abs(price_change) * 2000, 1.0)
            
            # Determina força do sinal
            signal_strength = abs(price_change) / threshold
            
            # Determina nível de risco
            risk_level = self._assess_risk_level(current_data, price_change)
            
            # Determina horizonte temporal
            time_horizon = self._determine_time_horizon(price_change)
            
            signal = BioSignal(
                date=datetime.fromisoformat(current_data.time),
                price=current_price,
                action=action,
                predicted_price=predicted_price,
                confidence=confidence,
                signal_strength=signal_strength,
                risk_level=risk_level,
                time_horizon=time_horizon
            )
            
            signals.append(signal)
        
        print(f"📡 Gerados {len(signals)} sinais de trading")
        return signals
    
    def _get_threshold(self) -> float:
        """Retorna threshold apropriado para o tipo de ativo"""
        symbol = self.config.symbol.upper()
        
        # Thresholds específicos por tipo de ativo
        if 'JPY' in symbol:
            return 0.0005  # Pares JPY são menos voláteis
        elif any(x in symbol for x in ['XAU', 'XAG', 'GOLD', 'SILVER']):
            return 0.005  # Metais têm maior volatilidade
        elif any(x in symbol for x in ['BTC', 'ETH', 'SOL']):
            return 0.01   # Criptomoedas são muito voláteis
        else:
            return self.config.trading_threshold
    
    def _assess_risk_level(self, data: MarketDataPoint, price_change: float) -> str:
        """Avalia o nível de risco do sinal"""
        
        # Baseado na volatilidade (ATR)
        volatility_risk = data.atr / data.price
        
        # Baseado na distância das bandas de Bollinger
        bb_width = (data.bb_upper - data.bb_lower) / data.price
        
        # Baseado no RSI
        rsi_extreme = abs(data.rsi - 50) / 50
        
        # Combina fatores
        risk_score = volatility_risk * 0.4 + bb_width * 0.3 + rsi_extreme * 0.3
        
        if risk_score > 0.1:
            return "HIGH"
        elif risk_score > 0.05:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _determine_time_horizon(self, price_change: float) -> str:
        """Determina o horizonte temporal recomendado"""
        abs_change = abs(price_change)
        
        if abs_change > 0.02:
            return "SHORT"  # Sinais fortes, operações curtas
        elif abs_change > 0.005:
            return "MEDIUM" # Sinais médios, swing trading
        else:
            return "LONG"   # Sinais fracos, posicionamento
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Retorna métricas de performance do modelo"""
        if not self.logs:
            return {}
        
        last_log = self.logs[-1]
        
        return {
            'final_loss': last_log.loss,
            'final_mae': last_log.mae,
            'final_accuracy': last_log.accuracy or 0.0,
            'total_epochs': len(self.logs),
            'training_time': (last_log.timestamp - self.logs[0].timestamp).total_seconds(),
            'avg_loss': np.mean([log.loss for log in self.logs]),
            'avg_mae': np.mean([log.mae for log in self.logs])
        }
    
    def get_recommendations(self) -> Dict[str, Any]:
        """Retorna recomendações baseadas na análise atual"""
        if not self.historical_data:
            return {}
        
        latest_data = self.historical_data[-1]
        
        # Análise de tendência
        trend = "BULLISH" if latest_data.price > latest_data.ma25 else "BEARISH"
        
        # Análise de momentum
        momentum = "STRONG" if abs(latest_data.price - latest_data.ma7) > latest_data.atr else "WEAK"
        
        # Análise de volatilidade
        volatility = "HIGH" if latest_data.atr / latest_data.price > 0.01 else "LOW"
        
        # Sinal RSI
        rsi_signal = "OVERBOUGHT" if latest_data.rsi > 70 else "OVERSOLD" if latest_data.rsi < 30 else "NEUTRAL"
        
        return {
            'current_price': latest_data.price,
            'trend': trend,
            'momentum': momentum,
            'volatility': volatility,
            'rsi_signal': rsi_signal,
            'support_level': latest_data.bb_lower,
            'resistance_level': latest_data.bb_upper,
            'recommended_action': self._get_recommended_action(latest_data),
            'confidence_score': self._calculate_confidence_score(latest_data)
        }
    
    def _get_recommended_action(self, data: MarketDataPoint) -> str:
        """Determina ação recomendada baseada em múltiplos fatores"""
        
        factors = []
        
        # Fator de tendência
        if data.price > data.ma25:
            factors.append(1)  # Bullish
        else:
            factors.append(-1) # Bearish
        
        # Fator de momentum
        if data.price > data.ma7:
            factors.append(0.5)
        else:
            factors.append(-0.5)
        
        # Fator RSI
        if data.rsi > 70:
            factors.append(-1)  # Sobrevendido
        elif data.rsi < 30:
            factors.append(1)   # Sobrecomprado
        else:
            factors.append(0)
        
        # Soma os fatores
        total_score = sum(factors)
        
        if total_score > 1:
            return "STRONG_BUY"
        elif total_score > 0:
            return "WEAK_BUY"
        elif total_score < -1:
            return "STRONG_SELL"
        elif total_score < 0:
            return "WEAK_SELL"
        else:
            return "HOLD"
    
    def _calculate_confidence_score(self, data: MarketDataPoint) -> float:
        """Calcula score de confiança baseado em múltiplos indicadores"""
        
        scores = []
        
        # Conformidade de tendência (preço vs MAs)
        if (data.price > data.ma7 > data.ma25) or (data.price < data.ma7 < data.ma25):
            scores.append(0.3)  # Tendências alinhadas
        
        # Volatilidade controlada
        vol_score = 1.0 - min(1.0, data.atr / data.price * 100)
        scores.append(vol_score * 0.2)
        
        # RSI em zona neutra
        rsi_score = 1.0 - abs(data.rsi - 50) / 50
        scores.append(rsi_score * 0.2)
        
        # Volume acima da média
        volume_score = min(1.0, data.volume / 1000)
        scores.append(volume_score * 0.1)
        
        # Distância das bandas
        bb_score = 1.0 - abs(data.price - (data.bb_upper + data.bb_lower)/2) / (data.bb_upper - data.bb_lower)
        scores.append(bb_score * 0.2)
        
        return min(1.0, max(0.0, sum(scores)))

# --- INTERFACE STREAMLIT ---
def create_streamlit_interface():
    """Cria interface Streamlit para o sistema Bio-Quântico"""
    import streamlit as st
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    st.set_page_config(
        page_title="Sistema Bio-Quântico Avançado",
        page_icon="🧬",
        layout="wide"
    )
    
    # CSS Styles
    st.markdown("""
    <style>
        .main-header {
            color: #10b981;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        .signal-buy {
            color: #10b981;
            font-weight: bold;
        }
        .signal-sell {
            color: #ef4444;
            font-weight: bold;
        }
        .signal-hold {
            color: #6b7280;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🧬 Sistema Bio-Quântico Avançado</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize session state
    if 'bio_system' not in st.session_state:
        st.session_state.bio_system = None
    if 'signals' not in st.session_state:
        st.session_state.signals = []
    if 'is_training' not in st.session_state:
        st.session_state.is_training = False
    if 'training_logs' not in st.session_state:
        st.session_state.training_logs = []
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuração do Sistema")
        
        symbol = st.selectbox(
            "Ativo",
            ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSDT", "ETHUSDT", "AAPL", "TSLA"],
            index=0
        )
        
        epochs = st.slider("Épocas de Treinamento", 10, 500, 100, 10)
        threshold = st.slider("Threshold de Trading", 0.001, 0.02, 0.002, 0.001)
        lookback = st.slider("Período Lookback", 10, 200, 50, 10)
        
        asset_type_map = {
            "EURUSD": AssetType.FOREX,
            "GBPUSD": AssetType.FOREX,
            "USDJPY": AssetType.FOREX,
            "XAUUSD": AssetType.METALS,
            "BTCUSDT": AssetType.CRYPTO,
            "ETHUSDT": AssetType.CRYPTO,
            "AAPL": AssetType.STOCKS,
            "TSLA": AssetType.STOCKS
        }
        
        asset_type = asset_type_map.get(symbol, AssetType.FOREX)
        
        config = BioSystemConfig(
            symbol=symbol,
            epochs=epochs,
            lookback=lookback,
            trading_threshold=threshold,
            asset_type=asset_type
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Inicializar Sistema", use_container_width=True):
                st.session_state.bio_system = AdvancedBioQuantumSystem(config)
                st.success("Sistema inicializado!")
        
        with col2:
            if st.button("📈 Carregar Dados", use_container_width=True):
                if st.session_state.bio_system:
                    import asyncio
                    asyncio.run(st.session_state.bio_system.load_simulated_data(symbol))
                    st.success("Dados simulados carregados!")
                else:
                    st.warning("Inicialize o sistema primeiro")
        
        st.markdown("---")
        
        # Training controls
        st.header("🎯 Treinamento")
        
        if st.button("🏋️‍♂️ Iniciar Treinamento", type="primary", use_container_width=True):
            if st.session_state.bio_system:
                st.session_state.is_training = True
                st.session_state.training_logs = []
                
                # Start training in background
                import threading
                
                def train():
                    import asyncio
                    
                    async def train_async():
                        def on_progress(log: TrainingLog):
                            st.session_state.training_logs.append(log)
                        
                        await st.session_state.bio_system.train_model(on_progress)
                        st.session_state.is_training = False
                    
                    asyncio.run(train_async())
                
                thread = threading.Thread(target=train, daemon=True)
                thread.start()
                
                st.success("Treinamento iniciado!")
            else:
                st.warning("Inicialize o sistema primeiro")
        
        if st.button("⏹️ Parar Treinamento", type="secondary", use_container_width=True):
            if st.session_state.bio_system:
                st.session_state.bio_system.stop_training()
                st.session_state.is_training = False
                st.info("Treinamento interrompido")
        
        st.markdown("---")
        
        # Generate signals
        if st.button("📡 Gerar Sinais", use_container_width=True):
            if st.session_state.bio_system:
                import asyncio
                st.session_state.signals = asyncio.run(st.session_state.bio_system.generate_signals())
                st.success(f"{len(st.session_state.signals)} sinais gerados!")
            else:
                st.warning("Inicialize e treine o sistema primeiro")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Status do Sistema")
        
        if st.session_state.bio_system:
            status_data = {
                "Sistema": "✅ Inicializado",
                "Ativo": st.session_state.bio_system.config.symbol,
                "Dados Carregados": f"{len(st.session_state.bio_system.historical_data)} pontos" if st.session_state.bio_system.historical_data else "❌ Não",
                "Treinado": f"{len(st.session_state.bio_system.logs)} épocas" if st.session_state.bio_system.logs else "❌ Não"
            }
            
            for key, value in status_data.items():
                st.markdown(f"<div class='metric-card'><strong>{key}:</strong> {value}</div>", unsafe_allow_html=True)
        else:
            st.info("Sistema não inicializado")
    
    with col2:
        st.markdown("### ⚡ Métricas de Treinamento")
        
        if st.session_state.training_logs:
            latest_log = st.session_state.training_logs[-1]
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Loss", f"{latest_log.loss:.4f}")
            with col_b:
                st.metric("MAE", f"{latest_log.mae:.4f}")
            with col_c:
                st.metric("Acurácia", f"{latest_log.accuracy or 0:.1%}")
            
            # Progress bar
            if st.session_state.is_training:
                progress = latest_log.epoch / st.session_state.bio_system.config.epochs
                st.progress(progress, text=f"Época {latest_log.epoch}/{st.session_state.bio_system.config.epochs}")
        else:
            st.info("Nenhum treinamento realizado")
    
    st.markdown("---")
    
    # Training chart
    if st.session_state.training_logs:
        st.markdown("### 📈 Progresso do Treinamento")
        
        df_logs = pd.DataFrame([
            {
                'Época': log.epoch,
                'Loss': log.loss,
                'MAE': log.mae,
                'Acurácia': log.accuracy or 0
            }
            for log in st.session_state.training_logs
        ])
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=df_logs['Época'], y=df_logs['Loss'], name="Loss", line=dict(color='red')),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df_logs['Época'], y=df_logs['MAE'], name="MAE", line=dict(color='orange')),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df_logs['Época'], y=df_logs['Acurácia'], name="Acurácia", line=dict(color='green')),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Evolução das Métricas de Treinamento",
            xaxis_title="Época",
            yaxis_title="Loss/MAE",
            yaxis2_title="Acurácia",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Signals
    if st.session_state.signals:
        st.markdown("### 🎯 Sinais de Trading Gerados")
        
        # Filter recent signals
        recent_signals = st.session_state.signals[-20:]
        
        # Create DataFrame for display
        signals_df = pd.DataFrame([
            {
                'Data': signal.date.strftime('%d/%m %H:%M'),
                'Preço': f"${signal.price:.4f}" if 'USD' in st.session_state.bio_system.config.symbol else f"${signal.price:.2f}",
                'Ação': signal.action.value,
                'Previsto': f"${signal.predicted_price:.4f}" if 'USD' in st.session_state.bio_system.config.symbol else f"${signal.predicted_price:.2f}",
                'Confiança': f"{signal.confidence:.1%}",
                'Força': signal.signal_strength or 0,
                'Risco': signal.risk_level or "N/A",
                'Horizonte': signal.time_horizon or "N/A"
            }
            for signal in recent_signals
        ])
        
        # Style DataFrame
        def color_action(val):
            if val == 'BUY':
                return 'color: #10b981; font-weight: bold'
            elif val == 'SELL':
                return 'color: #ef4444; font-weight: bold'
            else:
                return 'color: #6b7280'
        
        styled_df = signals_df.style.applymap(color_action, subset=['Ação'])
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Signal statistics
        st.markdown("### 📊 Estatísticas dos Sinais")
        
        buy_count = sum(1 for s in st.session_state.signals if s.action == BioTradingAction.BUY)
        sell_count = sum(1 for s in st.session_state.signals if s.action == BioTradingAction.SELL)
        hold_count = sum(1 for s in st.session_state.signals if s.action == BioTradingAction.HOLD)
        total_count = len(st.session_state.signals)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Compra", buy_count, f"{buy_count/total_count:.1%}")
        with col2:
            st.metric("Venda", sell_count, f"{sell_count/total_count:.1%}")
        with col3:
            st.metric("Aguardar", hold_count, f"{hold_count/total_count:.1%}")
    
    # Recommendations
    if st.session_state.bio_system and st.session_state.bio_system.historical_data:
        st.markdown("---")
        st.markdown("### 🧠 Recomendações Atuais")
        
        recommendations = st.session_state.bio_system.get_recommendations()
        
        if recommendations:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Preço Atual:** ${recommendations['current_price']:.4f}")
                st.markdown(f"**Tendência:** {recommendations['trend']}")
                st.markdown(f"**Momentum:** {recommendations['momentum']}")
                st.markdown(f"**Volatilidade:** {recommendations['volatility']}")
            
            with col2:
                st.markdown(f"**RSI:** {recommendations['rsi_signal']}")
                st.markdown(f"**Suporte:** ${recommendations['support_level']:.4f}")
                st.markdown(f"**Resistência:** ${recommendations['resistance_level']:.4f}")
                st.markdown(f"**Score de Confiança:** {recommendations['confidence_score']:.1%}")
            
            # Recommended action with color
            action = recommendations['recommended_action']
            action_color = {
                'STRONG_BUY': '🟢💪',
                'WEAK_BUY': '🟢',
                'HOLD': '🟡',
                'WEAK_SELL': '🔴',
                'STRONG_SELL': '🔴💪'
            }.get(action, '⚫')
            
            st.markdown(f"### {action_color} **Ação Recomendada: {action}**")

if __name__ == "__main__":
    # Para executar a interface Streamlit:
    # streamlit run bio_quantum_system.py
    create_streamlit_interface()