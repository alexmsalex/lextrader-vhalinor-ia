"""
Analisador de Dados de Criptomoedas
====================================
Gera estatísticas e análises dos dados coletados
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoDataAnalyzer:
    """Analisador de dados de criptomoedas"""

    def __init__(self):
        self.data_path = 'neural_layers/01_sensorial/crypto_data'
        self.cryptos = [
            'BTC_USDT', 'ETH_USDT', 'BNB_USDT', 'XRP_USDT', 'ADA_USDT',
            'DOGE_USDT', 'SOL_USDT', 'TRX_USDT', 'DOT_USDT', 'MATIC_USDT',
            'LTC_USDT', 'SHIB_USDT', 'AVAX_USDT', 'UNI_USDT', 'LINK_USDT',
            'ATOM_USDT', 'XLM_USDT', 'ETC_USDT', 'BCH_USDT', 'ALGO_USDT'
        ]

    def load_historical_data(self, symbol: str) -> pd.DataFrame:
        """Carrega dados históricos de uma criptomoeda"""
        filename = f"{self.data_path}/{symbol}_1d_3years.csv"

        if not os.path.exists(filename):
            logger.warning(f"⚠️  Arquivo não encontrado: {filename}")
            return pd.DataFrame()

        df = pd.read_csv(filename, index_col='timestamp', parse_dates=True)
        return df

    def calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """Calcula estatísticas de um DataFrame"""
        if df.empty:
            return {}

        stats = {
            'total_records': len(df),
            'date_range': {
                'start': df.index.min().isoformat(),
                'end': df.index.max().isoformat()
            },
            'price': {
                'current': float(df['close'].iloc[-1]),
                'min': float(df['low'].min()),
                'max': float(df['high'].max()),
                'mean': float(df['close'].mean()),
                'std': float(df['close'].std())
            },
            'volume': {
                'total': float(df['volume'].sum()),
                'mean': float(df['volume'].mean()),
                'max': float(df['volume'].max())
            },
            'returns': {
                'total': float((df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100),
                'daily_mean': float(df['close'].pct_change().mean() * 100),
                'daily_std': float(df['close'].pct_change().std() * 100)
            }
        }

        return stats

    def analyze_all_cryptos(self) -> Dict:
        """Analisa todas as criptomoedas"""
        logger.info("="*70)
        logger.info("📊 ANALISANDO DADOS DE CRIPTOMOEDAS")
        logger.info("="*70)

        results = {}

        for symbol in self.cryptos:
            logger.info(f"Analisando {symbol}...")

            df = self.load_historical_data(symbol)

            if not df.empty:
                stats = self.calculate_statistics(df)
                results[symbol] = stats
                logger.info(f"✅ {symbol}: {stats['total_records']} registros")
            else:
                logger.warning(f"⚠️  {symbol}: Sem dados")

        logger.info(f"\n✅ Análise concluída: {len(results)} criptomoedas")
        return results

    def generate_report(self) -> str:
        """Gera relatório completo de análise"""
        results = self.analyze_all_cryptos()

        report = []
        report.append("="*70)
        report.append("📊 RELATÓRIO DE ANÁLISE DE CRIPTOMOEDAS")
        report.append("="*70)
        report.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total de criptomoedas: {len(results)}")
        report.append("="*70)
        report.append("")

        # Ranking por retorno total
        sorted_by_return = sorted(
            results.items(),
            key=lambda x: x[1].get('returns', {}).get('total', 0),
            reverse=True
        )

        report.append("🏆 TOP 10 - MAIOR RETORNO (3 ANOS)")
        report.append("-"*70)
        for i, (symbol, stats) in enumerate(sorted_by_return[:10], 1):
            ret = stats.get('returns', {}).get('total', 0)
            price = stats.get('price', {}).get('current', 0)
            report.append(f"{i:2d}. {symbol:15s} | Retorno: {ret:+10.2f}% | Preço: ${price:,.2f}")
        report.append("")

        # Ranking por volatilidade
        sorted_by_volatility = sorted(
            results.items(),
            key=lambda x: x[1].get('returns', {}).get('daily_std', 0),
            reverse=True
        )

        report.append("📈 TOP 10 - MAIOR VOLATILIDADE")
        report.append("-"*70)
        for i, (symbol, stats) in enumerate(sorted_by_volatility[:10], 1):
            vol = stats.get('returns', {}).get('daily_std', 0)
            report.append(f"{i:2d}. {symbol:15s} | Volatilidade: {vol:.2f}%")
        report.append("")

        # Estatísticas gerais
        report.append("📊 ESTATÍSTICAS GERAIS")
        report.append("-"*70)

        total_records = sum(s.get('total_records', 0) for s in results.values())
        avg_return = sum(s.get('returns', {}).get('total', 0) for s in results.values()) / len(results)
        avg_volatility = sum(s.get('returns', {}).get('daily_std', 0) for s in results.values()) / len(results)

        report.append(f"Total de registros: {total_records:,}")
        report.append(f"Retorno médio (3 anos): {avg_return:+.2f}%")
        report.append(f"Volatilidade média: {avg_volatility:.2f}%")
        report.append("")

        report.append("="*70)
        report.append("✅ ANÁLISE CONCLUÍDA")
        report.append("="*70)

        return "\n".join(report)

    def save_analysis(self):
        """Salva análise em arquivos"""
        # Gerar análise
        results = self.analyze_all_cryptos()

        # Salvar JSON
        json_file = f"{self.data_path}/analysis_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        logger.info(f"💾 Análise salva: {json_file}")

        # Gerar e salvar relatório
        report = self.generate_report()
        report_file = f"{self.data_path}/analysis_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"💾 Relatório salvo: {report_file}")

        # Exibir relatório
        print("\n" + report)

def main():
    """Função principal"""
    analyzer = CryptoDataAnalyzer()
    analyzer.save_analysis()

if __name__ == "__main__":
    main()
