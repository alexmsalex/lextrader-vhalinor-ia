import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Tuple, Dict, Any
import logging
from dataclasses import dataclass
import warnings

# Configurações iniciais
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

@dataclass
class AnalysisConfig:
    """Configurações para análise técnica"""
    sma_short: int = 50
    sma_long: int = 200
    rsi_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9

class FinancialDataAnalyzer:
    """Classe principal para análise de dados financeiros"""
    
    def __init__(self, config: Optional[AnalysisConfig] = None):
        self.config = config or AnalysisConfig()
        self.data = None
        
    def get_historical_data(self, ticker: str, start_date: str, end_date: str, 
                          progress: bool = False) -> pd.DataFrame:
        """
        Obtém dados históricos do Yahoo Finance com tratamento de erros
        
        Args:
            ticker: Símbolo do ativo
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            progress: Mostrar barra de progresso
            
        Returns:
            DataFrame com dados históricos
        """
        try:
            logger.info(f"Baixando dados para {ticker} de {start_date} até {end_date}")
            df = yf.download(ticker, start=start_date, end=end_date, progress=progress)
            
            if df.empty:
                raise ValueError(f"Nenhum dado encontrado para {ticker}")
                
            logger.info(f"Dados baixados com sucesso: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao baixar dados: {e}")
            raise
    
    def clean_historical_data(self, df: pd.DataFrame, 
                            keep_columns: Optional[list] = None) -> pd.DataFrame:
        """
        Limpa e formata os dados históricos
        
        Args:
            df: DataFrame com dados brutos
            keep_columns: Colunas a manter (None para padrão)
            
        Returns:
            DataFrame limpo
        """
        df_clean = df.copy()
        
        # Colunas padrão a manter
        if keep_columns is None:
            keep_columns = ['Close']
        
        # Mantém apenas colunas especificadas
        columns_to_drop = [col for col in df_clean.columns if col not in keep_columns]
        df_clean = df_clean.drop(columns=columns_to_drop, errors='ignore')
        
        # Renomeia colunas
        column_mapping = {'Close': 'price'}
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Reseta índice e formata data
        df_clean = df_clean.reset_index()
        df_clean['date'] = pd.to_datetime(df_clean['Date'])
        df_clean = df_clean.drop('Date', axis=1)
        
        # Remove duplicatas e valores NaN
        df_clean = df_clean.drop_duplicates(subset=['date']).sort_values('date')
        df_clean = df_clean.dropna()
        
        logger.info(f"Dados limpos: {len(df_clean)} registros válidos")
        return df_clean
    
    def compute_rsi(self, series: pd.Series, period: Optional[int] = None) -> pd.Series:
        """
        Calcula o Índice de Força Relativa (RSI) de forma otimizada
        
        Args:
            series: Série de preços
            period: Período do RSI
            
        Returns:
            Série com valores RSI
        """
        period = period or self.config.rsi_period
        
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        
        # EMA para suavização
        avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
        avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def compute_macd(self, series: pd.Series, 
                    fast_period: Optional[int] = None,
                    slow_period: Optional[int] = None,
                    signal_period: Optional[int] = None) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calcula o MACD (Moving Average Convergence Divergence)
        
        Args:
            series: Série de preços
            fast_period: Período rápido
            slow_period: Período lento
            signal_period: Período do sinal
            
        Returns:
            Tuple (MACD, Signal, Histogram)
        """
        fast_period = fast_period or self.config.macd_fast
        slow_period = slow_period or self.config.macd_slow
        signal_period = signal_period or self.config.macd_signal
        
        fast_ema = series.ewm(span=fast_period, min_periods=fast_period).mean()
        slow_ema = series.ewm(span=slow_period, min_periods=slow_period).mean()
        
        macd = fast_ema - slow_ema
        signal = macd.ewm(span=signal_period, min_periods=signal_period).mean()
        histogram = macd - signal
        
        return macd, signal, histogram
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula múltiplos indicadores técnicos de forma eficiente
        
        Args:
            df: DataFrame com dados de preço
            
        Returns:
            DataFrame com indicadores técnicos
        """
        df_indicators = df.copy()
        price_series = df_indicators['price']
        
        # Médias Móveis
        df_indicators['sma_50'] = price_series.rolling(window=self.config.sma_short).mean()
        df_indicators['sma_200'] = price_series.rolling(window=self.config.sma_long).mean()
        
        # RSI
        df_indicators['rsi'] = self.compute_rsi(price_series)
        
        # MACD
        macd, signal, hist = self.compute_macd(price_series)
        df_indicators['macd'] = macd
        df_indicators['macd_signal'] = signal
        df_indicators['macd_hist'] = hist
        
        # Bollinger Bands (adicional)
        df_indicators['bb_middle'] = price_series.rolling(window=20).mean()
        bb_std = price_series.rolling(window=20).std()
        df_indicators['bb_upper'] = df_indicators['bb_middle'] + (bb_std * 2)
        df_indicators['bb_lower'] = df_indicators['bb_middle'] - (bb_std * 2)
        
        logger.info("Indicadores técnicos calculados")
        return df_indicators
    
    def generate_trading_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera sinais de trading baseados em múltiplos indicadores
        
        Args:
            df: DataFrame com indicadores técnicos
            
        Returns:
            DataFrame com sinais
        """
        df_signals = df.copy()
        
        # Sinais baseados em cruzamento de médias
        df_signals['sma_signal'] = np.where(
            df_signals['sma_50'] > df_signals['sma_200'], 1, -1
        )
        
        # Sinais RSI (sobrecomprado/sobrevendido)
        df_signals['rsi_signal'] = 0
        df_signals.loc[df_signals['rsi'] < 30, 'rsi_signal'] = 1  # Sobrevendido
        df_signals.loc[df_signals['rsi'] > 70, 'rsi_signal'] = -1  # Sobrecomprado
        
        # Sinais MACD
        df_signals['macd_signal'] = np.where(
            df_signals['macd'] > df_signals['macd_signal'], 1, -1
        )
        
        # Sinal consolidado
        df_signals['final_signal'] = (
            df_signals['sma_signal'] + df_signals['rsi_signal'] + df_signals['macd_signal']
        )
        
        logger.info("Sinais de trading gerados")
        return df_signals
    
    def calculate_performance_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Calcula métricas de performance do ativo
        
        Args:
            df: DataFrame com dados completos
            
        Returns:
            Dicionário com métricas de performance
        """
        returns = df['price'].pct_change().dropna()
        
        metrics = {
            'total_return': (df['price'].iloc[-1] / df['price'].iloc[0] - 1) * 100,
            'annual_return': (df['price'].iloc[-1] / df['price'].iloc[0]) ** (252/len(df)) - 1,
            'volatility': returns.std() * np.sqrt(252),
            'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0,
            'max_drawdown': (df['price'] / df['price'].cummax() - 1).min() * 100,
            'win_rate': (returns > 0).mean() * 100
        }
        
        logger.info("Métricas de performance calculadas")
        return metrics
    
    def create_comprehensive_plot(self, df: pd.DataFrame, ticker: str):
        """
        Cria visualização completa dos dados e indicadores
        
        Args:
            df: DataFrame com dados completos
            ticker: Símbolo do ativo para título
        """
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        fig.suptitle(f'Análise Técnica - {ticker}', fontsize=16, fontweight='bold')
        
        # Subplot 1: Preço e Médias Móveis
        axes[0].plot(df['date'], df['price'], label='Preço', linewidth=2, color='black')
        axes[0].plot(df['date'], df['sma_50'], label='SMA 50', alpha=0.7)
        axes[0].plot(df['date'], df['sma_200'], label='SMA 200', alpha=0.7)
        axes[0].fill_between(df['date'], df['bb_upper'], df['bb_lower'], 
                           alpha=0.2, label='Bollinger Bands')
        axes[0].set_title('Preço e Tendência')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Subplot 2: RSI
        axes[1].plot(df['date'], df['rsi'], label='RSI', color='purple')
        axes[1].axhline(70, linestyle='--', alpha=0.7, color='red')
        axes[1].axhline(30, linestyle='--', alpha=0.7, color='green')
        axes[1].fill_between(df['date'], 70, 30, alpha=0.1, color='gray')
        axes[1].set_title('RSI - Indicador de Momentum')
        axes[1].set_ylim(0, 100)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Subplot 3: MACD
        axes[2].plot(df['date'], df['macd'], label='MACD', color='blue')
        axes[2].plot(df['date'], df['macd_signal'], label='Signal', color='red')
        axes[2].bar(df['date'], df['macd_hist'], label='Histograma', 
                   color=np.where(df['macd_hist'] > 0, 'green', 'red'), alpha=0.6)
        axes[2].set_title('MACD')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        # Subplot 4: Sinais
        axes[3].plot(df['date'], df['price'], label='Preço', color='black', alpha=0.7)
        buy_signals = df[df['final_signal'] > 1]
        sell_signals = df[df['final_signal'] < -1]
        axes[3].scatter(buy_signals['date'], buy_signals['price'], 
                       color='green', marker='^', s=100, label='Compra')
        axes[3].scatter(sell_signals['date'], sell_signals['price'], 
                       color='red', marker='v', s=100, label='Venda')
        axes[3].set_title('Sinais de Trading')
        axes[3].legend()
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def export_data(self, df: pd.DataFrame, filename: str, format_type: str = 'csv'):
        """
        Exporta dados em múltiplos formatos
        
        Args:
            df: DataFrame para exportar
            filename: Nome do arquivo (sem extensão)
            format_type: Tipo de arquivo ('csv', 'excel', 'json', etc.)
        """
        export_methods = {
            'csv': lambda: df.to_csv(f'{filename}.csv', index=False),
            'excel': lambda: df.to_excel(f'{filename}.xlsx', index=False),
            'json': lambda: df.to_json(f'{filename}.json', orient='records', indent=2),
            'parquet': lambda: df.to_parquet(f'{filename}.parquet'),
            'feather': lambda: df.to_feather(f'{filename}.feather')
        }
        
        if format_type in export_methods:
            try:
                export_methods[format_type]()
                logger.info(f"Dados exportados como {format_type}: {filename}.{format_type}")
            except Exception as e:
                logger.error(f"Erro ao exportar como {format_type}: {e}")
        else:
            logger.warning(f"Formato {format_type} não suportado")

def main():
    """Função principal de exemplo"""
    # Configuração
    config = AnalysisConfig(
        sma_short=50,
        sma_long=200,
        rsi_period=14,
        macd_fast=12,
        macd_slow=26,
        macd_signal=9
    )
    
    # Inicializar analisador
    analyzer = FinancialDataAnalyzer(config)
    
    # Parâmetros
    ticker = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2024-12-01'
    
    try:
        # Obter e processar dados
        raw_data = analyzer.get_historical_data(ticker, start_date, end_date)
        clean_data = analyzer.clean_historical_data(raw_data)
        data_with_indicators = analyzer.calculate_technical_indicators(clean_data)
        final_data = analyzer.generate_trading_signals(data_with_indicators)
        
        # Calcular métricas
        metrics = analyzer.calculate_performance_metrics(final_data)
        
        # Exibir resultados
        print("\n" + "="*50)
        print(f"ANÁLISE - {ticker}")
        print("="*50)
        print(f"Retorno Total: {metrics['total_return']:.2f}%")
        print(f"Retorno Anual: {metrics['annual_return']:.2%}")
        print(f"Volatilidade: {metrics['volatility']:.2%}")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
        print(f"Win Rate: {metrics['win_rate']:.2f}%")
        
        # Plotar gráficos
        analyzer.create_comprehensive_plot(final_data, ticker)
        
        # Exportar dados
        analyzer.export_data(final_data, f'{ticker}_analysis', 'csv')
        analyzer.export_data(final_data, f'{ticker}_analysis', 'excel')
        
        return final_data, metrics
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return None, None

if __name__ == "__main__":
    data, performance_metrics = main()