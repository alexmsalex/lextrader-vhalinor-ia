"""
Analisador de Dados de Forex
=============================
Gera estatísticas e análises dos dados coletados
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ForexDataAnalyzer:
    """Analisador de dados de forex"""

    def __init__(self):
        self.data_path = 'neural_layers/01_sensorial/forex_data'
        self.forex_pairs = [
            'EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF', 'AUD_USD',
            'USD_CAD', 'NZD_USD', 'EUR_GBP', 'EUR_JPY', 'GBP_JPY',
            'EUR_CHF', 'EUR_AUD', 'EUR_CAD', 'GBP_CHF', 'GBP_AUD',
            'AUD_JPY', 'AUD_CAD', 'NZD_JPY', 'CHF_JPY', 'CAD_JPY'
        ]

    def load_historical_data(self, symbol: str) -> pd.DataFrame:
        """Carrega dados históricos de um par forex"""
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

        # Calcular pips (para forex, 1 pip = 0.0001 para a maioria dos pares)
        price_change = df['close'].iloc[-1] - df['close'].iloc[0]
        pips_change = price_change * 10000  # Conversão para pips

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
                'pips': float(pips_change),
                'daily_mean': float(df['close'].pct_change().mean() * 100),
                'daily_std': float(df['close'].pct_change().std() * 100)
            }
        }

        return stats

    def analyze_all_forex(self) -> Dict:
        """Analisa todos os pares forex"""
        logger.info("="*70)
        logger.info("📊 ANALISANDO DADOS DE FOREX")
        logger.info("="*70)

        results = {}

        for symbol in self.forex_pairs:
            logger.info(f"Analisando {symbol}...")

            df = self.load_historical_data(symbol)

            if not df.empty:
                stats = self.calculate_statistics(df)
                results[symbol] = stats
                logger.info(f"✅ {symbol}: {stats['total_records']} registros")
            else:
                logger.warning(f"⚠️  {symbol}: Sem dados")

        logger.info(f"\n✅ Análise concluída: {len(results)} pares forex")
        return results

    def generate_report(self) -> str:
        """Gera relatório completo de análise"""
        results = self.analyze_all_forex()

        report = []
        report.append("="*70)
        report.append("📊 RELATÓRIO DE ANÁLISE DE FOREX")
        report.append("="*70)
        report.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total de pares: {len(results)}")
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
            pips = stats.get('returns', {}).get('pips', 0)
            price = stats.get('price', {}).get('current', 0)
            report.append(f"{i:2d}. {symbol:15s} | Retorno: {ret:+8.2f}% | Pips: {pips:+8.0f} | Preço: {price:.4f}")
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
            report.append(f"{i:2d}. {symbol:15s} | Volatilidade: {vol:.3f}%")
        report.append("")

        # Pares Majors vs Cross
        report.append("📊 ANÁLISE POR CATEGORIA")
        report.append("-"*70)

        majors = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF', 'AUD_USD', 'USD_CAD', 'NZD_USD']
        crosses = [p for p in self.forex_pairs if p not in majors]

        majors_return = sum(results.get(p, {}).get('returns', {}).get('total', 0) for p in majors) / len(majors)
        crosses_return = sum(results.get(p, {}).get('returns', {}).get('total', 0) for p in crosses) / len(crosses)

        report.append(f"Pares Majors (7):  Retorno médio: {majors_return:+.2f}%")
        report.append(f"Pares Cross (13):  Retorno médio: {crosses_return:+.2f}%")
        report.append("")

        # Estatísticas gerais
        report.append("📊 ESTATÍSTICAS GERAIS")
        report.append("-"*70)

        total_records = sum(s.get('total_records', 0) for s in results.values())
        avg_return = sum(s.get('returns', {}).get('total', 0) for s in results.values()) / len(results)
        avg_volatility = sum(s.get('returns', {}).get('daily_std', 0) for s in results.values()) / len(results)

        report.append(f"Total de registros: {total_records:,}")
        report.append(f"Retorno médio (3 anos): {avg_return:+.2f}%")
        report.append(f"Volatilidade média: {avg_volatility:.3f}%")
        report.append("")

        report.append("="*70)
        report.append("✅ ANÁLISE CONCLUÍDA")
        report.append("="*70)

        return "\n".join(report)

    def save_analysis(self):
        """Salva análise em arquivos"""
        # Gerar análise
        results = self.analyze_all_forex()

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
    analyzer = ForexDataAnalyzer()
    analyzer.save_analysis()

if __name__ == "__main__":
    main()
