"""
Coletor de Dados de Criptomoedas - Top 20
==========================================
Coleta dados históricos e em tempo real das 20 principais criptomoedas
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List

import ccxt
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoDataCollector:
    """Coletor de dados de criptomoedas"""

    # Top 20 criptomoedas por market cap
    TOP_20_CRYPTOS = [
        'BTC/USDT',   # Bitcoin
        'ETH/USDT',   # Ethereum
        'BNB/USDT',   # Binance Coin
        'XRP/USDT',   # Ripple
        'ADA/USDT',   # Cardano
        'DOGE/USDT',  # Dogecoin
        'SOL/USDT',   # Solana
        'TRX/USDT',   # Tron
        'DOT/USDT',   # Polkadot
        'MATIC/USDT', # Polygon
        'LTC/USDT',   # Litecoin
        'SHIB/USDT',  # Shiba Inu
        'AVAX/USDT',  # Avalanche
        'UNI/USDT',   # Uniswap
        'LINK/USDT',  # Chainlink
        'ATOM/USDT',  # Cosmos
        'XLM/USDT',   # Stellar
        'ETC/USDT',   # Ethereum Classic
        'BCH/USDT',   # Bitcoin Cash
        'ALGO/USDT'   # Algorand
    ]

    def __init__(self, exchange_id='binance'):
        """Inicializa o coletor"""
        self.exchange_id = exchange_id
        self.exchange = getattr(ccxt, exchange_id)({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        self.data_path = 'neural_layers/01_sensorial/crypto_data'

    def fetch_historical_data(self, symbol: str, timeframe: str = '1d',
                             days: int = 1095) -> pd.DataFrame:
        """
        Busca dados históricos (3 anos = 1095 dias)

        Args:
            symbol: Par de trading (ex: 'BTC/USDT')
            timeframe: Timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
            days: Número de dias de histórico
        """
        try:
            logger.info(f"Buscando dados históricos de {symbol}...")

            # Calcular timestamp de início (3 anos atrás)
            since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)

            # Buscar dados (CCXT síncrono)
            ohlcv = self.exchange.fetch_ohlcv(
                symbol,
                timeframe=timeframe,
                since=since,
                limit=1000
            )

            # Converter para DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )

            # Converter timestamp para datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            logger.info(f"✅ {symbol}: {len(df)} registros coletados")
            return df

        except Exception as e:
            logger.error(f"❌ Erro ao buscar {symbol}: {e}")
            return pd.DataFrame()

    def fetch_realtime_data(self, symbol: str) -> Dict:
        """Busca dados em tempo real"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)

            return {
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'last': ticker.get('last'),
                'bid': ticker.get('bid'),
                'ask': ticker.get('ask'),
                'high': ticker.get('high'),
                'low': ticker.get('low'),
                'volume': ticker.get('volume'),
                'change': ticker.get('change'),
                'percentage': ticker.get('percentage')
            }
        except Exception as e:
            logger.error(f"❌ Erro ao buscar dados em tempo real de {symbol}: {e}")
            return {}

    def collect_all_historical(self, timeframe: str = '1d'):
        """Coleta dados históricos de todas as 20 criptomoedas"""
        logger.info("="*70)
        logger.info("📊 COLETANDO DADOS HISTÓRICOS DAS TOP 20 CRIPTOMOEDAS")
        logger.info("="*70)

        all_data = {}

        for symbol in self.TOP_20_CRYPTOS:
            df = self.fetch_historical_data(symbol, timeframe)

            if not df.empty:
                all_data[symbol] = df

                # Salvar em CSV
                filename = f"{self.data_path}/{symbol.replace('/', '_')}_{timeframe}_3years.csv"
                df.to_csv(filename)
                logger.info(f"💾 Salvo: {filename}")

            # Aguardar para respeitar rate limit
            time.sleep(1)

        logger.info(f"\n✅ Coleta concluída: {len(all_data)} criptomoedas")
        return all_data

    def collect_all_realtime(self) -> Dict:
        """Coleta dados em tempo real de todas as 20 criptomoedas"""
        logger.info("📡 Coletando dados em tempo real...")

        realtime_data = {}

        for symbol in self.TOP_20_CRYPTOS:
            data = self.fetch_realtime_data(symbol)
            if data:
                realtime_data[symbol] = data
            time.sleep(0.5)

        # Salvar em JSON
        filename = f"{self.data_path}/realtime_data.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(realtime_data, f, indent=2)

        logger.info(f"✅ Dados em tempo real salvos: {filename}")
        return realtime_data

    def get_crypto_info(self) -> List[Dict]:
        """Retorna informações das 20 principais criptomoedas"""
        return [
            {'symbol': 'BTC/USDT', 'name': 'Bitcoin', 'rank': 1},
            {'symbol': 'ETH/USDT', 'name': 'Ethereum', 'rank': 2},
            {'symbol': 'BNB/USDT', 'name': 'Binance Coin', 'rank': 3},
            {'symbol': 'XRP/USDT', 'name': 'Ripple', 'rank': 4},
            {'symbol': 'ADA/USDT', 'name': 'Cardano', 'rank': 5},
            {'symbol': 'DOGE/USDT', 'name': 'Dogecoin', 'rank': 6},
            {'symbol': 'SOL/USDT', 'name': 'Solana', 'rank': 7},
            {'symbol': 'TRX/USDT', 'name': 'Tron', 'rank': 8},
            {'symbol': 'DOT/USDT', 'name': 'Polkadot', 'rank': 9},
            {'symbol': 'MATIC/USDT', 'name': 'Polygon', 'rank': 10},
            {'symbol': 'LTC/USDT', 'name': 'Litecoin', 'rank': 11},
            {'symbol': 'SHIB/USDT', 'name': 'Shiba Inu', 'rank': 12},
            {'symbol': 'AVAX/USDT', 'name': 'Avalanche', 'rank': 13},
            {'symbol': 'UNI/USDT', 'name': 'Uniswap', 'rank': 14},
            {'symbol': 'LINK/USDT', 'name': 'Chainlink', 'rank': 15},
            {'symbol': 'ATOM/USDT', 'name': 'Cosmos', 'rank': 16},
            {'symbol': 'XLM/USDT', 'name': 'Stellar', 'rank': 17},
            {'symbol': 'ETC/USDT', 'name': 'Ethereum Classic', 'rank': 18},
            {'symbol': 'BCH/USDT', 'name': 'Bitcoin Cash', 'rank': 19},
            {'symbol': 'ALGO/USDT', 'name': 'Algorand', 'rank': 20}
        ]

def main():
    """Função principal"""
    collector = CryptoDataCollector()

    # Coletar dados históricos
    historical = collector.collect_all_historical(timeframe='1d')

    # Coletar dados em tempo real
    realtime = collector.collect_all_realtime()

    print("\n" + "="*70)
    print("✅ COLETA COMPLETA!")
    print("="*70)
    print(f"Dados históricos: {len(historical)} criptomoedas")
    print(f"Dados em tempo real: {len(realtime)} criptomoedas")
    print("="*70)

if __name__ == "__main__":
    main()
