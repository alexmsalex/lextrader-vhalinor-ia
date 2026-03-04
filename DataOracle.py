import asyncio
import random
from typing import List, Dict, Any, Literal, Optional
from dataclasses import dataclass
from enum import Enum

# Tipos
OracleSignalType = Literal['BUY', 'SELL', 'NEUTRAL']

class OracleSourceType(Enum):
    TRADINGVIEW = "TRADINGVIEW"
    YFINANCE = "YFINANCE"
    GLASSNODE = "GLASSNODE"
    SANTIMENT = "SANTIMENT"
    COINGLASS = "COINGLASS"
    INTOTHEBLOCK = "INTOTHEBLOCK"
    MESSARI = "MESSARI"
    COINGLASS = "COINGLASS"
    INTOTHEBLOCK = "INTOTHEBLOCK"
    MESSARI = "MESSARI"

@dataclass
class OracleSignal:
    source: str
    signal: OracleSignalType
    score: float
    metadata: str
    latency: int

@dataclass
class OracleConsensus:
    overallScore: float
    bullishCount: int
    bearishCount: int
    primaryDriver: str
    signals: List[OracleSignal]

class DataOracle:
    def __init__(self):
        """Inicializa o serviço de oráculo de dados."""
        pass
    
    async def get_tradingview_signal(self, symbol: str) -> OracleSignal:
        """Obtém sinal do TradingView."""
        score = random.random() * 100
        signal: OracleSignalType = 'NEUTRAL'
        
        if score > 60:
            signal = 'BUY'
        elif score < 40:
            signal = 'SELL'
        
        signal_text = "Strong Buy" if signal == 'BUY' else signal
        
        return OracleSignal(
            source=OracleSourceType.TRADINGVIEW.value,
            signal=signal,
            score=score,
            metadata=f"Oscillators: {signal_text} | MA: Mixed",
            latency=120
        )
    
    async def get_yfinance_data(self, symbol: str) -> OracleSignal:
        """Obtém dados do Yahoo Finance."""
        spy_correlation = random.random()
        dxy_trend = 'UP' if random.random() > 0.5 else 'DOWN'
        signal: OracleSignalType = 'NEUTRAL'
        
        if dxy_trend == 'DOWN' and spy_correlation > 0.5:
            signal = 'BUY'
        elif dxy_trend == 'UP':
            signal = 'SELL'
        
        return OracleSignal(
            source=OracleSourceType.YFINANCE.value,
            signal=signal,
            score=random.random() * 100,
            metadata=f"SP500 Corr: {(spy_correlation*100):.0f}% | DXY: {dxy_trend}",
            latency=450
        )
    
    async def get_glassnode_metrics(self, symbol: str) -> OracleSignal:
        """Obtém métricas da Glassnode."""
        nupl = random.random()
        exchange_flow = 'OUTFLOW' if random.random() > 0.5 else 'INFLOW'
        signal: OracleSignalType = 'NEUTRAL'
        
        if nupl < 0.3:
            signal = 'BUY'
        elif nupl > 0.7:
            signal = 'SELL'
        
        if exchange_flow == 'OUTFLOW' and signal != 'SELL':
            signal = 'BUY'
        
        return OracleSignal(
            source=OracleSourceType.GLASSNODE.value,
            signal=signal,
            score=nupl * 100,
            metadata=f"NUPL: {nupl:.2f} | NetFlow: {exchange_flow}",
            latency=800
        )
    
    async def get_santiment_data(self, symbol: str) -> OracleSignal:
        """Obtém dados da Santiment."""
        social_volume = random.randint(0, 10000)
        sentiment_score = (random.random() * 4) - 2  # -2 a 2
        signal: OracleSignalType = 'NEUTRAL'
        
        if sentiment_score > 1:
            signal = 'SELL'
        elif sentiment_score < -1:
            signal = 'BUY'
        
        return OracleSignal(
            source=OracleSourceType.SANTIMENT.value,
            signal=signal,
            score=50 + (sentiment_score * 25),
            metadata=f"Social Vol: {social_volume} | Sentiment: {sentiment_score:.2f}",
            latency=600
        )
    
    async def get_coinglass_data(self, symbol: str) -> OracleSignal:
        """Obtém dados do Coinglass."""
        ls_ratio = 0.5 + random.random()  # 0.5 a 1.5
        funding_rate = (random.random() * 0.04) - 0.02  # -2% a 2%
        signal: OracleSignalType = 'NEUTRAL'
        
        if ls_ratio > 1.2:
            signal = 'SELL'
        elif funding_rate < -0.01:
            signal = 'BUY'
        
        return OracleSignal(
            source=OracleSourceType.COINGLASS.value,
            signal=signal,
            score=50,
            metadata=f"L/S Ratio: {ls_ratio:.2f} | Funding: {funding_rate:.4f}%",
            latency=300
        )
    
    async def get_intotheblock_data(self, symbol: str) -> OracleSignal:
        """Obtém dados do IntoTheBlock."""
        in_money = random.random() * 100  # 0 a 100%
        signal: OracleSignalType = 'NEUTRAL'
        
        if in_money > 90:
            signal = 'SELL'
        elif in_money < 40:
            signal = 'BUY'
        
        return OracleSignal(
            source=OracleSourceType.INTOTHEBLOCK.value,
            signal=signal,
            score=in_money,
            metadata=f"In Money: {in_money:.0f}% | Whales: Stable",
            latency=550
        )
    
    async def get_messari_data(self, symbol: str) -> OracleSignal:
        """Obtém dados do Messari."""
        real_vol_profile = random.random()  # 0 a 1
        signal: OracleSignalType = 'NEUTRAL'
        
        if real_vol_profile > 0.8:
            signal = 'BUY'
        
        return OracleSignal(
            source=OracleSourceType.MESSARI.value,
            signal=signal,
            score=real_vol_profile * 100,
            metadata=f"Real Vol: {(real_vol_profile*100):.0f}% | Dev Activity: High",
            latency=700
        )
    
    async def get_market_consensus(self, symbol: str = 'BTC/USDT') -> OracleConsensus:
        """
        Obtém consenso de mercado de múltiplas fontes.
        
        Args:
            symbol: Par de trading (padrão: 'BTC/USDT')
            
        Returns:
            OracleConsensus: Consenso agregado de todas as fontes
        """
        # Coletar sinais de todas as fontes
        signals = await asyncio.gather(
            self.get_tradingview_signal(symbol),
            self.get_yfinance_data(symbol),
            self.get_glassnode_metrics(symbol),
            self.get_santiment_data(symbol),
            self.get_coinglass_data(symbol),
            self.get_intotheblock_data(symbol),
            self.get_messari_data(symbol)
        )
        
        # Calcular estatísticas agregadas
        bullish_count = 0
        bearish_count = 0
        total_score = 0.0
        
        for signal in signals:
            if signal.signal == 'BUY':
                bullish_count += 1
                total_score += signal.score
            elif signal.signal == 'SELL':
                bearish_count += 1
                total_score += (100 - signal.score)
            else:  # NEUTRAL
                total_score += 50
        
        # Calcular pontuação geral
        overall_score = total_score / len(signals)
        
        # Encontrar principal driver (fonte com maior desvio da neutralidade)
        primary_driver = max(
            signals,
            key=lambda s: abs(s.score - 50)
        ).source
        
        return OracleConsensus(
            overallScore=overall_score,
            bullishCount=bullish_count,
            bearishCount=bearish_count,
            primaryDriver=primary_driver,
            signals=signals
        )
    
    async def get_signal_from_source(self, source: OracleSourceType, symbol: str) -> OracleSignal:
        """
        Obtém sinal de uma fonte específica.
        
        Args:
            source: Fonte de dados
            symbol: Par de trading
            
        Returns:
            OracleSignal: Sinal da fonte especificada
        """
        source_methods = {
            OracleSourceType.TRADINGVIEW: self.get_tradingview_signal,
            OracleSourceType.YFINANCE: self.get_yfinance_data,
            OracleSourceType.GLASSNODE: self.get_glassnode_metrics,
            OracleSourceType.SANTIMENT: self.get_santiment_data,
            OracleSourceType.COINGLASS: self.get_coinglass_data,
            OracleSourceType.INTOTHEBLOCK: self.get_intotheblock_data,
            OracleSourceType.MESSARI: self.get_messari_data,
        }
        
        if source not in source_methods:
            raise ValueError(f"Fonte não suportada: {source}")
        
        return await source_methods[source](symbol)

# Instância global do serviço
oracle_service = DataOracle()

# Funções auxiliares para uso síncrono (opcional)
async def get_consensus_async(symbol: str = 'BTC/USDT') -> OracleConsensus:
    """Versão assíncrona para obter consenso."""
    return await oracle_service.get_market_consensus(symbol)

def get_consensus(symbol: str = 'BTC/USDT') -> OracleConsensus:
    """Versão síncrona para obter consenso."""
    return asyncio.run(oracle_service.get_market_consensus(symbol))

# Exemplo de uso
async def example_usage():
    """Exemplo de uso do serviço de oráculo."""
    print("🔮 Serviço de Oráculo de Dados")
    print("=" * 50)
    
    # Obter consenso de mercado
    consensus = await oracle_service.get_market_consensus()
    
    print(f"Consenso de Mercado para BTC/USDT:")
    print(f"Pontuação Geral: {consensus.overallScore:.2f}/100")
    print(f"Bullish: {consensus.bullishCount} fontes")
    print(f"Bearish: {consensus.bearishCount} fontes")
    print(f"Principal Driver: {consensus.primaryDriver}")
    print()
    
    print("Sinais Individuais:")
    print("-" * 80)
    
    for signal in consensus.signals:
        emoji = "🟢" if signal.signal == 'BUY' else "🔴" if signal.signal == 'SELL' else "🟡"
        print(f"{emoji} {signal.source:<15} | {signal.signal:<6} | "
              f"Score: {signal.score:6.2f} | Latency: {signal.latency:4}ms")
        print(f"   {signal.metadata}")
        print()

if __name__ == "__main__":
    # Configurar seed para reprodutibilidade
    random.seed(42)
    
    # Executar exemplo
    asyncio.run(example_usage())