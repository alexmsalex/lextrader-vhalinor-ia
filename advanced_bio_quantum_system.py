import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import asyncio
import aiofiles
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('BioQuantumSystem')

class TradingAction(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

@dataclass
class SystemConfig:
    data_path: str
    model_path: str
    api_key: str
    api_secret: str
    symbol: str
    interval: str = "1m"
    lookback: int = 60
    epochs: int = 100
    thread_pool_size: int = 4
    trading_threshold: float = 0.02
    batch_size: int = 32
    validation_split: float = 0.2

    @classmethod
    def create(cls, data_path: str, model_path: str, api_key: str, api_secret: str, 
               symbol: str, **kwargs) -> 'SystemConfig':
        return cls(
            data_path=data_path,
            model_path=model_path,
            api_key=api_key,
            api_secret=api_secret,
            symbol=symbol,
            **kwargs
        )

@dataclass
class DataPoint:
    date: datetime
    close: float
    volume: float = 0.0
    high: float = 0.0
    low: float = 0.0
    open: float = 0.0

@dataclass
class EnhancedDataPoint(DataPoint):
    technical_features: Dict[str, float] = field(default_factory=dict)
    
    def add_feature(self, name: str, value: float):
        self.technical_features[name] = value

@dataclass
class MACD:
    macd: float
    signal: float
    histogram: float

@dataclass
class Signal:
    date: datetime
    price: float
    action: TradingAction
    predicted_price: Optional[float] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        if self.predicted_price is not None:
            error = abs(self.price - self.predicted_price) / self.price
            self.confidence = max(0.0, 1.0 - error)
    
    def to_csv_string(self) -> str:
        pred_price = self.predicted_price if self.predicted_price is not None else 0.0
        return f"{self.date},{self.price:.4f},{self.action.value},{pred_price:.4f},{self.confidence:.4f}"
    
    def has_prediction(self) -> bool:
        return self.predicted_price is not None

@dataclass
class TrainingDataset:
    sequences: np.ndarray
    targets: np.ndarray
    metadata: List[EnhancedDataPoint]
    
    def save(self, filepath: str):
        np.savez(filepath, 
                 sequences=self.sequences, 
                 targets=self.targets,
                 metadata_timestamps=[point.date.timestamp() for point in self.metadata])
    
    @classmethod
    def load(cls, filepath: str) -> 'TrainingDataset':
        data = np.load(filepath, allow_pickle=True)
        metadata = [
            EnhancedDataPoint(datetime.fromtimestamp(ts)) 
            for ts in data['metadata_timestamps']
        ]
        return cls(
            sequences=data['sequences'],
            targets=data['targets'],
            metadata=metadata
        )

@dataclass
class EvaluationResult:
    mse: float
    mae: float
    rmse: float
    predictions: np.ndarray
    actuals: np.ndarray

class MinMaxScaler:
    def __init__(self, feature_range: Tuple[float, float] = (0, 1)):
        self.min_val, self.max_val = feature_range
        self.data_min = None
        self.data_max = None
        self.fitted = False
    
    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        self.data_min = np.min(data)
        self.data_max = np.max(data)
        self.fitted = True
        return self.transform(data)
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        if not self.fitted:
            raise ValueError("Scaler must be fitted before transformation")
        
        data_std = (data - self.data_min) / (self.data_max - self.data_min)
        return data_std * (self.max_val - self.min_val) + self.min_val
    
    def inverse_transform(self, data: np.ndarray) -> np.ndarray:
        if not self.fitted:
            raise ValueError("Scaler must be fitted before inverse transformation")
        
        data_std = (data - self.min_val) / (self.max_val - self.min_val)
        return data_std * (self.data_max - self.data_min) + self.data_min

class TechnicalAnalysis:
    @staticmethod
    def calculate_sma(data: List[DataPoint], index: int, period: int) -> float:
        if index < period - 1:
            return 0.0
        prices = [point.close for point in data[index-period+1:index+1]]
        return np.mean(prices)
    
    @staticmethod
    def calculate_ema(data: List[DataPoint], index: int, period: int) -> float:
        if index < period - 1:
            return 0.0
        
        prices = [point.close for point in data[index-period+1:index+1]]
        multiplier = 2.0 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    @staticmethod
    def calculate_rsi(data: List[DataPoint], index: int, period: int = 14) -> float:
        if index < period:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(index-period+1, index+1):
            change = data[i].close - data[i-1].close
            if change > 0:
                gains.append(change)
            else:
                losses.append(-change)
        
        if not gains and not losses:
            return 50.0
        
        avg_gain = np.mean(gains) if gains else 0
        avg_loss = np.mean(losses) if losses else 0.001  # Evitar divisão por zero
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        return 100.0 - (100.0 / (1.0 + rs))
    
    @staticmethod
    def calculate_macd(data: List[DataPoint], index: int) -> MACD:
        if index < 26:
            return MACD(0.0, 0.0, 0.0)
        
        ema_12 = TechnicalAnalysis.calculate_ema(data, index, 12)
        ema_26 = TechnicalAnalysis.calculate_ema(data, index, 26)
        macd = ema_12 - ema_26
        
        # Calcular sinal (EMA 9 do MACD)
        macd_values = []
        for i in range(index-8, index+1):
            ema_12_i = TechnicalAnalysis.calculate_ema(data, i, 12)
            ema_26_i = TechnicalAnalysis.calculate_ema(data, i, 26)
            macd_values.append(ema_12_i - ema_26_i)
        
        signal = np.mean(macd_values)  # Simplificado
        histogram = macd - signal
        
        return MACD(macd, signal, histogram)

class AdvancedBioQuantumSystem:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.scaler = MinMaxScaler()
        self.model: Optional[keras.Model] = None
        self.historical_data: List[DataPoint] = []
        self.trading_signals: List[Signal] = []
        self.loop = asyncio.get_event_loop()
        self._initialize_system()
    
    def _initialize_system(self):
        """Inicializa o sistema carregando o modelo se existir"""
        try:
            self.load_model()
            logger.info("Sistema Bio-Quantum inicializado com sucesso")
        except Exception as e:
            logger.warning(f"Modelo não encontrado, será criado novo modelo: {e}")
    
    async def load_and_preprocess_data(self) -> TrainingDataset:
        """Carrega e pré-processa os dados de forma assíncrona"""
        logger.info("Carregando e pré-processando dados...")
        
        try:
            # Carregar dados do CSV
            raw_data = await self._load_csv_data()
            
            # Aplicar limpeza de dados
            cleaned_data = self._apply_data_cleaning(raw_data)
            
            # Adicionar features técnicas
            enhanced_data = self._add_technical_features(cleaned_data)
            
            # Normalizar dados
            close_prices = np.array([point.close for point in enhanced_data])
            scaled_data = self.scaler.fit_transform(close_prices)
            
            # Criar sequências para treinamento
            dataset = self._create_sequences(scaled_data, enhanced_data)
            
            # Salvar dataset processado
            await self._save_processed_dataset(dataset)
            
            self.historical_data = cleaned_data
            logger.info(f"Dados carregados e pré-processados: {len(self.historical_data)} pontos")
            
            return dataset
            
        except Exception as e:
            logger.error(f"Erro no carregamento de dados: {e}")
            raise
    
    async def _load_csv_data(self) -> List[DataPoint]:
        """Carrega dados do arquivo CSV"""
        data = []
        async with aiofiles.open(self.config.data_path, 'r') as file:
            lines = await file.readlines()
            
            # Pular header e processar linhas
            for line in lines[1:]:
                values = line.strip().split(',')
                if len(values) >= 2:
                    try:
                        date = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S')
                        close = float(values[1])
                        data_point = DataPoint(date=date, close=close)
                        
                        # Adicionar dados adicionais se disponíveis
                        if len(values) >= 5:
                            data_point.open = float(values[1])
                            data_point.high = float(values[2])
                            data_point.low = float(values[3])
                            data_point.close = float(values[4])
                            if len(values) >= 6:
                                data_point.volume = float(values[5])
                        
                        data.append(data_point)
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Erro ao processar linha: {line}. Erro: {e}")
                        continue
        
        return data
    
    def _apply_data_cleaning(self, raw_data: List[DataPoint]) -> List[DataPoint]:
        """Aplica limpeza e filtros nos dados"""
        return sorted(
            [point for point in raw_data if point.close > 0],
            key=lambda x: x.date
        )
    
    def _add_technical_features(self, data: List[DataPoint]) -> List[EnhancedDataPoint]:
        """Adiciona indicadores técnicos aos dados"""
        enhanced_data = []
        
        for i, point in enumerate(data):
            enhanced_point = EnhancedDataPoint(
                date=point.date,
                close=point.close,
                volume=point.volume,
                high=point.high,
                low=point.low,
                open=point.open
            )
            
            # SMA 20
            if i >= 19:
                sma_20 = TechnicalAnalysis.calculate_sma(data, i, 20)
                enhanced_point.add_feature("SMA_20", sma_20)
            
            # RSI 14
            if i >= 14:
                rsi_14 = TechnicalAnalysis.calculate_rsi(data, i, 14)
                enhanced_point.add_feature("RSI_14", rsi_14)
            
            # MACD
            if i >= 26:
                macd = TechnicalAnalysis.calculate_macd(data, i)
                enhanced_point.add_feature("MACD", macd.macd)
                enhanced_point.add_feature("MACD_Signal", macd.signal)
                enhanced_point.add_feature("MACD_Histogram", macd.histogram)
            
            enhanced_data.append(enhanced_point)
        
        return enhanced_data
    
    def _create_sequences(self, scaled_data: np.ndarray, enhanced_data: List[EnhancedDataPoint]) -> TrainingDataset:
        """Cria sequências para treinamento do modelo LSTM"""
        sequences = []
        targets = []
        metadata = []
        
        for i in range(self.config.lookback, len(scaled_data)):
            sequence = scaled_data[i-self.config.lookback:i]
            target = scaled_data[i]
            
            sequences.append(sequence)
            targets.append(target)
            metadata.append(enhanced_data[i])
        
        sequences_array = np.array(sequences).reshape(-1, self.config.lookback, 1)
        targets_array = np.array(targets)
        
        return TrainingDataset(sequences_array, targets_array, metadata)
    
    async def _save_processed_dataset(self, dataset: TrainingDataset):
        """Salva dataset processado de forma assíncrona"""
        def save():
            dataset.save("processed_dataset.npz")
        
        await self.loop.run_in_executor(None, save)
    
    def build_model(self):
        """Constrói o modelo LSTM avançado"""
        logger.info("Construindo modelo LSTM avançado...")
        
        self.model = keras.Sequential([
            layers.LSTM(50, return_sequences=True, input_shape=(self.config.lookback, 1)),
            layers.Dropout(0.2),
            layers.LSTM(50, return_sequences=False),
            layers.Dropout(0.2),
            layers.Dense(20, activation='relu'),
            layers.Dense(1, activation='linear')
        ])
        
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        logger.info("Modelo LSTM construído com sucesso")
        logger.info(self.model.summary())
    
    async def train_model(self, dataset: TrainingDataset):
        """Treina o modelo de forma assíncrona"""
        logger.info("Iniciando treinamento do modelo...")
        
        def train():
            # Callbacks para monitoramento
            callbacks = [
                keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5),
                keras.callbacks.ModelCheckpoint(
                    f"{self.config.model_path}.checkpoint",
                    save_best_only=True,
                    save_weights_only=True
                ),
                keras.callbacks.CSVLogger('training_log.csv')
            ]
            
            history = self.model.fit(
                dataset.sequences,
                dataset.targets,
                batch_size=self.config.batch_size,
                epochs=self.config.epochs,
                validation_split=self.config.validation_split,
                callbacks=callbacks,
                verbose=1
            )
            
            return history
        
        history = await self.loop.run_in_executor(None, train)
        await self.save_model()
        logger.info("Treinamento concluído com sucesso")
        
        return history
    
    async def evaluate_model(self, dataset: TrainingDataset) -> EvaluationResult:
        """Avalia o modelo treinado"""
        logger.info("Avaliando modelo...")
        
        def evaluate():
            predictions = self.model.predict(dataset.sequences)
            actuals = dataset.targets
            
            mse = np.mean((predictions.flatten() - actuals) ** 2)
            mae = np.mean(np.abs(predictions.flatten() - actuals))
            rmse = np.sqrt(mse)
            
            return EvaluationResult(mse, mae, rmse, predictions.flatten(), actuals)
        
        result = await self.loop.run_in_executor(None, evaluate)
        logger.info(f"Avaliação concluída: RMSE = {result.rmse:.6f}")
        
        return result
    
    async def generate_signals(self) -> List[Signal]:
        """Gera sinais de trading baseados nas previsões do modelo"""
        logger.info("Gerando sinais de trading...")
        
        if not self.historical_data:
            raise ValueError("Dados históricos não carregados")
        
        close_prices = np.array([point.close for point in self.historical_data])
        scaled_data = self.scaler.transform(close_prices)
        
        signals = []
        
        for i in range(self.config.lookback, len(scaled_data)):
            sequence = scaled_data[i-self.config.lookback:i].reshape(1, self.config.lookback, 1)
            
            # Fazer previsão
            prediction_scaled = self.model.predict(sequence, verbose=0)
            predicted_price = self.scaler.inverse_transform(prediction_scaled.flatten())[0]
            
            current_price = self.historical_data[i].close
            action = self._generate_trading_signal(current_price, predicted_price)
            
            signal = Signal(
                date=self.historical_data[i].date,
                price=current_price,
                action=action,
                predicted_price=predicted_price
            )
            
            signals.append(signal)
        
        self.trading_signals = signals
        logger.info(f"{len(signals)} sinais gerados com sucesso")
        
        return signals
    
    def _generate_trading_signal(self, current_price: float, predicted_price: float) -> TradingAction:
        """Gera sinal de trading baseado na previsão"""
        price_change = (predicted_price - current_price) / current_price
        
        if price_change > self.config.trading_threshold:
            return TradingAction.BUY
        elif price_change < -self.config.trading_threshold:
            return TradingAction.SELL
        else:
            return TradingAction.HOLD
    
    async def export_signals_to_csv(self, filepath: str, signals: List[Signal]):
        """Exporta sinais para arquivo CSV"""
        async with aiofiles.open(filepath, 'w') as file:
            await file.write("Date,Price,Action,Predicted_Price,Confidence\n")
            
            for signal in signals:
                await file.write(signal.to_csv_string() + "\n")
        
        logger.info(f"Sinais exportados para: {filepath}")
    
    def plot_signals(self, signals: List[Signal]):
        """Gera gráfico dos sinais de trading"""
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
            
            # Gráfico de preços e sinais
            dates = [signal.date for signal in signals]
            prices = [signal.price for signal in signals]
            predicted_prices = [signal.predicted_price for signal in signals if signal.has_prediction()]
            predicted_dates = [signal.date for signal in signals if signal.has_prediction()]
            
            buy_signals = [signal for signal in signals if signal.action == TradingAction.BUY]
            sell_signals = [signal for signal in signals if signal.action == TradingAction.SELL]
            
            ax1.plot(dates, prices, label='Preço Real', linewidth=1, alpha=0.7)
            if predicted_prices:
                ax1.plot(predicted_dates, predicted_prices, label='Preço Previsto', linewidth=1, alpha=0.7)
            
            if buy_signals:
                buy_dates = [signal.date for signal in buy_signals]
                buy_prices = [signal.price for signal in buy_signals]
                ax1.scatter(buy_dates, buy_prices, color='green', marker='^', s=50, label='Compra', alpha=0.8)
            
            if sell_signals:
                sell_dates = [signal.date for signal in sell_signals]
                sell_prices = [signal.price for signal in sell_signals]
                ax1.scatter(sell_dates, sell_prices, color='red', marker='v', s=50, label='Venda', alpha=0.8)
            
            ax1.set_title('Sinais de Trading Bio-Quantum')
            ax1.set_ylabel('Preço')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Formatar eixos de data
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # Gráfico de confiança
            confidences = [signal.confidence for signal in signals if signal.has_prediction()]
            confidence_dates = [signal.date for signal in signals if signal.has_prediction()]
            
            ax2.plot(confidence_dates, confidences, label='Confiança da Previsão', color='orange', linewidth=1)
            ax2.set_xlabel('Data')
            ax2.set_ylabel('Confiança')
            ax2.set_ylim(0, 1)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Formatar eixos de data
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            plt.tight_layout()
            plt.savefig('trading_signals.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráfico gerado e salvo como 'trading_signals.png'")
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico: {e}")
    
    async def execute_trading_strategy(self):
        """Executa a estratégia de trading"""
        signals = await self.generate_signals()
        
        trading_tasks = []
        for signal in signals:
            if signal.action != TradingAction.HOLD:
                trading_tasks.append(self._execute_order(signal))
        
        if trading_tasks:
            await asyncio.gather(*trading_tasks)
            logger.info(f"Executadas {len(trading_tasks)} ordens de trading")
        else:
            logger.info("Nenhuma ordem de trading para executar")
    
    async def _execute_order(self, signal: Signal):
        """Executa uma ordem de trading individual"""
        try:
            logger.info(f"Executando ordem {signal.action.value} para {self.config.symbol} em {signal.date}")
            
            # Simular execução (substituir por API real)
            await asyncio.sleep(0.1)
            logger.info(f"Ordem {signal.action.value} executada com sucesso")
            
        except Exception as e:
            logger.error(f"Erro na execução da ordem: {e}")
    
    async def save_model(self):
        """Salva o modelo treinado"""
        if self.model:
            self.model.save(self.config.model_path)
            logger.info(f"Modelo salvo em: {self.config.model_path}")
    
    def load_model(self):
        """Carrega um modelo salvo"""
        self.model = keras.models.load_model(self.config.model_path)
        logger.info(f"Modelo carregado de: {self.config.model_path}")
    
    async def run(self):
        """Executa o pipeline completo do sistema"""
        logger.info("Iniciando sistema Bio-Quantum...")
        
        try:
            # Pipeline principal
            dataset = await self.load_and_preprocess_data()
            
            if not self.model:
                self.build_model()
                history = await self.train_model(dataset)
            else:
                logger.info("Usando modelo pré-existente")
            
            # Avaliar modelo
            evaluation = await self.evaluate_model(dataset)
            
            # Gerar e exportar sinais
            signals = await self.generate_signals()
            await self.export_signals_to_csv("trading_signals.csv", signals)
            
            # Executar estratégia
            await self.execute_trading_strategy()
            
            # Gerar visualização
            self.plot_signals(signals)
            
            logger.info("Pipeline de trading concluído com sucesso")
            
        except Exception as e:
            logger.error(f"Erro no pipeline de trading: {e}")
            raise
    
    async def shutdown(self):
        """Finaliza o sistema adequadamente"""
        logger.info("Sistema Bio-Quantum finalizado")

# Exemplo de uso
async def main():
    """Função principal de exemplo"""
    
    # Configuração do sistema
    config = SystemConfig.create(
        data_path="financial_data.csv",
        model_path="bio_quantum_model.h5",
        api_key="your_api_key",
        api_secret="your_api_secret",
        symbol="BTCUSDT",
        lookback=60,
        epochs=50,
        trading_threshold=0.015
    )
    
    # Criar e executar sistema
    system = AdvancedBioQuantumSystem(config)
    
    try:
        await system.run()
        
        # Manter sistema ativo por um tempo
        await asyncio.sleep(10)
        
    finally:
        await system.shutdown()

if __name__ == "__main__":
    # Executar sistema
    asyncio.run(main())

# Código para gerar dados de exemplo se necessário
def generate_sample_data(filename: str = "financial_data.csv", num_points: int = 1000):
    """Gera dados de exemplo para teste"""
    start_date = datetime(2023, 1, 1)
    prices = [100.0]
    
    for i in range(1, num_points):
        # Simular movimento de preço com tendência e ruído
        change = np.random.normal(0.001, 0.02)
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 1.0))  # Preço mínimo de 1.0
    
    with open(filename, 'w') as f:
        f.write("Date,Open,High,Low,Close,Volume\n")
        for i, price in enumerate(prices):
            date = start_date + timedelta(hours=i)
            open_price = price * (1 + np.random.normal(0, 0.005))
            high = max(open_price, price) * (1 + abs(np.random.normal(0, 0.01)))
            low = min(open_price, price) * (1 - abs(np.random.normal(0, 0.01)))
            volume = np.random.uniform(1000, 10000)
            
            f.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')},{open_price:.4f},{high:.4f},{low:.4f},{price:.4f},{volume:.2f}\n")
    
    print(f"Dados de exemplo gerados em: {filename}")

# Gerar dados de exemplo se o arquivo não existir
import os
if not os.path.exists("financial_data.csv"):
    generate_sample_data()