"""
LEXTRADER-IAG 4.0 - Analisador Unificado de Mercados
====================================================
Sistema integrado que combina análises de criptomoedas, forex e arbitragem
com IA avançada e tomada de decisão automatizada.

Versão: 1.0.0
Data: Janeiro 2026
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging
from enum import Enum

# Imports dos analisadores específicos
from crypto_analysis_advanced import AdvancedCryptoAnalyzer, CryptoAnalysisResult
from forex_analysis_advanced import AdvancedForexAnalyzer, ForexAnalysisResult
from arbitrage_analysis_advanced import AdvancedArbitrageAnalyzer, ArbitrageAnalysisResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketType(Enum):
    """Tipos de mercado"""
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    ARBITRAGE = "ARBITRAGE"


class OverallSignal(Enum):
    """Sinal geral do mercado"""
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"
    ARBITRAGE = "ARBITRAGE"


@dataclass
class UnifiedAnalysisResult:
    """Resultado da análise unificada"""
    timestamp: datetime
    overall_signal: OverallSignal
    confidence: float
    crypto_analysis: Optional[CryptoAnalysisResult]
    forex_analysis: Optional[ForexAnalysisResult]
    arbitrage_analysis: Optional[ArbitrageAnalysisResult]
    market_correlation: Dict[str, float]
    risk_assessment: Dict[str, Any]
    portfolio_recommendations: List[str]
    execution_priority: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


class MarketCorrelationAnalyzer:
    """Analisador de correlações entre mercados"""

    def __init__(self):
        self.correlation_history = []
        logger.info("✅ Analisador de Correlações de Mercado inicializado")

    def calculate_cross_market_correlations(self, crypto_data: pd.DataFrame,
                                          forex_data: pd.DataFrame) -> Dict[str, float]:
        """Calcula correlações entre mercados"""
        correlations = {}

        try:
            # Correlação BTC vs USD Index
            if len(crypto_data) > 0 and len(forex_data) > 0:
                btc_returns = crypto_data['close'].pct_change().dropna()
                usd_returns = forex_data['close'].pct_change().dropna()

                # Alinha os dados
                min_len = min(len(btc_returns), len(usd_returns))
                if min_len > 10:
                    corr = btc_returns.tail(min_len).corr(usd_returns.tail(min_len))
                    correlations['BTC_USD'] = corr

            # Correlações adicionais (simuladas)
            correlations.update({
                'CRYPTO_FOREX': np.random.uniform(-0.5, 0.5),
                'RISK_ON_OFF': np.random.uniform(-0.8, 0.8),
                'VOLATILITY_CORRELATION': np.random.uniform(0.3, 0.9)
            })

        except Exception as e:
            logger.error(f"Erro ao calcular correlações: {e}")

        return correlations

    def analyze_market_regime(self, correlations: Dict[str, float]) -> str:
        """Analisa regime de mercado baseado em correlações"""
        btc_usd_corr = correlations.get('BTC_USD', 0)
        risk_corr = correlations.get('RISK_ON_OFF', 0)

        if btc_usd_corr < -0.5 and risk_corr > 0.5:
            return "RISK_OFF"
        elif btc_usd_corr > 0.3 and risk_corr > 0.3:
            return "RISK_ON"
        elif abs(btc_usd_corr) < 0.2:
            return "DECOUPLED"
        else:
            return "TRANSITIONAL"


class RiskAssessmentEngine:
    """Engine de avaliação de risco unificado"""

    def __init__(self):
        logger.info("✅ Engine de Avaliação de Risco inicializado")

    def assess_unified_risk(self, crypto_result: Optional[CryptoAnalysisResult],
                           forex_result: Optional[ForexAnalysisResult],
                           arbitrage_result: Optional[ArbitrageAnalysisResult]) -> Dict[str, Any]:
        """Avalia risco unificado"""
        risk_factors = {
            'market_risk': 0,
            'liquidity_risk': 0,
            'execution_risk': 0,
            'correlation_risk': 0,
            'overall_risk': 0
        }

        # Risco de mercado
        market_risks = []
        if crypto_result:
            market_risks.append(crypto_result.risk_score)
        if forex_result:
            # Forex geralmente tem menor risco
            market_risks.append(30)

        if market_risks:
            risk_factors['market_risk'] = np.mean(market_risks)

        # Risco de liquidez
        if arbitrage_result and arbitrage_result.opportunities_found > 0:
            risk_factors['liquidity_risk'] = 20  # Arbitragem indica boa liquidez
        else:
            risk_factors['liquidity_risk'] = 50

        # Risco de execução
        execution_risks = []
        if crypto_result:
            # Crypto tem maior risco de execução
            execution_risks.append(40)
        if forex_result:
            # Forex tem menor risco de execução
            execution_risks.append(20)

        risk_factors['execution_risk'] = np.mean(execution_risks) if execution_risks else 30

        # Risco de correlação
        risk_factors['correlation_risk'] = 30  # Placeholder

        # Risco geral
        risk_factors['overall_risk'] = np.mean([
            risk_factors['market_risk'],
            risk_factors['liquidity_risk'],
            risk_factors['execution_risk'],
            risk_factors['correlation_risk']
        ])

        return risk_factors


class PortfolioOptimizer:
    """Otimizador de portfólio multi-mercado"""

    def __init__(self):
        logger.info("✅ Otimizador de Portfólio inicializado")

    def generate_portfolio_allocation(self, crypto_result: Optional[CryptoAnalysisResult],
                                    forex_result: Optional[ForexAnalysisResult],
                                    arbitrage_result: Optional[ArbitrageAnalysisResult],
                                    risk_tolerance: str = "moderate") -> Dict[str, float]:
        """Gera alocação de portfólio otimizada"""
        allocation = {
            'crypto': 0.0,
            'forex': 0.0,
            'arbitrage': 0.0,
            'cash': 0.0
        }

        total_score = 0
        scores = {}

        # Score para crypto
        if crypto_result:
            crypto_score = (crypto_result.technical_score + crypto_result.fundamental_score + crypto_result.sentiment_score) / 3
            scores['crypto'] = crypto_score
            total_score += crypto_score

        # Score para forex
        if forex_result:
            forex_score = (forex_result.technical_score + forex_result.fundamental_score) / 2
            scores['forex'] = forex_score
            total_score += forex_score

        # Score para arbitragem
        if arbitrage_result and arbitrage_result.best_opportunity:
            arb_score = arbitrage_result.best_opportunity.confidence
            scores['arbitrage'] = arb_score
            total_score += arb_score

        # Calcula alocações baseadas em scores
        if total_score > 0:
            for market, score in scores.items():
                base_allocation = score / total_score

                # Ajusta baseado na tolerância ao risco
                if risk_tolerance == "conservative":
                    if market == 'crypto':
                        base_allocation *= 0.5
                    elif market == 'forex':
                        base_allocation *= 1.2
                elif risk_tolerance == "aggressive":
                    if market == 'crypto':
                        base_allocation *= 1.5
                    elif market == 'arbitrage':
                        base_allocation *= 1.3

                allocation[market] = min(base_allocation, 0.6)  # Max 60% em qualquer mercado

        # Normaliza para somar 100%
        total_allocated = sum(allocation.values())
        if total_allocated > 0:
            for market in allocation:
                allocation[market] = allocation[market] / total_allocated
        else:
            allocation['cash'] = 1.0

        return allocation


class UnifiedMarketAnalyzer:
    """Analisador unificado de todos os mercados"""

    def __init__(self):
        self.crypto_analyzer = AdvancedCryptoAnalyzer()
        self.forex_analyzer = AdvancedForexAnalyzer()
        self.arbitrage_analyzer = AdvancedArbitrageAnalyzer()
        self.correlation_analyzer = MarketCorrelationAnalyzer()
        self.risk_engine = RiskAssessmentEngine()
        self.portfolio_optimizer = PortfolioOptimizer()

        logger.info("🚀 Analisador Unificado de Mercados inicializado")

    async def analyze_all_markets(self, crypto_symbols: List[str] = None,
                                 forex_pairs: List[str] = None,
                                 arbitrage_assets: List[str] = None,
                                 exchanges: List[str] = None) -> UnifiedAnalysisResult:
        """Análise completa de todos os mercados"""
        logger.info("🌐 Iniciando análise unificada de mercados...")

        # Valores padrão
        crypto_symbols = crypto_symbols or ['BTC/USDT']
        forex_pairs = forex_pairs or ['EUR/USD']
        arbitrage_assets = arbitrage_assets or ['BTC/USDT', 'ETH/USDT']
        exchanges = exchanges or ['binance', 'coinbase']

        # Executa análises em paralelo
        tasks = []

        # Análise de crypto
        if crypto_symbols:
            tasks.append(self.crypto_analyzer.analyze(crypto_symbols[0]))

        # Análise de forex
        if forex_pairs:
            tasks.append(self.forex_analyzer.analyze(forex_pairs[0]))

        # Análise de arbitragem
        if arbitrage_assets and exchanges:
            tasks.append(self.arbitrage_analyzer.scan_all_opportunities(arbitrage_assets, exchanges))

        # Executa todas as análises
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Processa resultados
        crypto_result = results[0] if len(results) > 0 and not isinstance(results[0], Exception) else None
        forex_result = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else None
        arbitrage_result = results[2] if len(results) > 2 and not isinstance(results[2], Exception) else None

        # Análise de correlações
        correlations = {}
        if crypto_result and forex_result:
            # Busca dados para correlação
            crypto_data = await self.crypto_analyzer.fetch_ohlcv(crypto_symbols[0])
            forex_data = await self.forex_analyzer.fetch_forex_data(forex_pairs[0])
            correlations = self.correlation_analyzer.calculate_cross_market_correlations(crypto_data, forex_data)

        # Avaliação de risco
        risk_assessment = self.risk_engine.assess_unified_risk(crypto_result, forex_result, arbitrage_result)

        # Determina sinal geral
        overall_signal, confidence = self._determine_overall_signal(crypto_result, forex_result, arbitrage_result)

        # Gera recomendações de portfólio
        portfolio_recommendations = self._generate_portfolio_recommendations(
            crypto_result, forex_result, arbitrage_result, risk_assessment
        )

        # Prioridade de execução
        execution_priority = self._determine_execution_priority(crypto_result, forex_result, arbitrage_result)

        return UnifiedAnalysisResult(
            timestamp=datetime.now(),
            overall_signal=overall_signal,
            confidence=confidence,
            crypto_analysis=crypto_result,
            forex_analysis=forex_result,
            arbitrage_analysis=arbitrage_result,
            market_correlation=correlations,
            risk_assessment=risk_assessment,
            portfolio_recommendations=portfolio_recommendations,
            execution_priority=execution_priority,
            metadata={
                'analysis_duration': 0,
                'markets_analyzed': len([r for r in [crypto_result, forex_result, arbitrage_result] if r]),
                'correlation_regime': self.correlation_analyzer.analyze_market_regime(correlations)
            }
        )

    def _determine_overall_signal(self, crypto_result, forex_result, arbitrage_result) -> Tuple[OverallSignal, float]:
        """Determina sinal geral do mercado"""
        signals = []
        confidences = []

        # Arbitragem tem prioridade
        if arbitrage_result and arbitrage_result.best_opportunity and arbitrage_result.best_opportunity.net_profit > 0.5:
            return OverallSignal.ARBITRAGE, arbitrage_result.best_opportunity.confidence

        # Combina sinais de crypto e forex
        if crypto_result:
            if crypto_result.signal.value in ['STRONG_BUY', 'BUY']:
                signals.append(1)
            elif crypto_result.signal.value in ['STRONG_SELL', 'SELL']:
                signals.append(-1)
            else:
                signals.append(0)
            confidences.append(crypto_result.confidence)

        if forex_result:
            if forex_result.signal.value in ['STRONG_BUY', 'BUY']:
                signals.append(1)
            elif forex_result.signal.value in ['STRONG_SELL', 'SELL']:
                signals.append(-1)
            else:
                signals.append(0)
            confidences.append(forex_result.confidence)

        if not signals:
            return OverallSignal.HOLD, 50.0

        avg_signal = np.mean(signals)
        avg_confidence = np.mean(confidences)

        if avg_signal >= 0.7:
            return OverallSignal.STRONG_BUY, avg_confidence
        elif avg_signal >= 0.3:
            return OverallSignal.BUY, avg_confidence
        elif avg_signal <= -0.7:
            return OverallSignal.STRONG_SELL, avg_confidence
        elif avg_signal <= -0.3:
            return OverallSignal.SELL, avg_confidence
        else:
            return OverallSignal.HOLD, avg_confidence

    def _generate_portfolio_recommendations(self, crypto_result, forex_result, arbitrage_result, risk_assessment) -> List[str]:
        """Gera recomendações de portfólio"""
        recommendations = []

        # Alocação otimizada
        allocation = self.portfolio_optimizer.generate_portfolio_allocation(
            crypto_result, forex_result, arbitrage_result
        )

        recommendations.append("📊 Alocação Recomendada:")
        for market, percentage in allocation.items():
            if percentage > 0.05:  # Apenas alocações > 5%
                recommendations.append(f"  • {market.upper()}: {percentage:.1%}")

        # Recomendações baseadas em risco
        overall_risk = risk_assessment.get('overall_risk', 50)
        if overall_risk > 70:
            recommendations.append("⚠️ Alto risco detectado: Reduza exposição")
        elif overall_risk < 30:
            recommendations.append("✅ Baixo risco: Considere aumentar exposição")

        # Recomendações específicas por mercado
        if crypto_result and crypto_result.signal.value in ['STRONG_BUY', 'BUY']:
            recommendations.append(f"🚀 Crypto: {crypto_result.signal.value} em {crypto_result.symbol}")

        if forex_result and forex_result.signal.value in ['STRONG_BUY', 'BUY']:
            recommendations.append(f"💱 Forex: {forex_result.signal.value} em {forex_result.pair}")

        if arbitrage_result and arbitrage_result.best_opportunity:
            best = arbitrage_result.best_opportunity
            recommendations.append(f"⚡ Arbitragem: {best.type.value} - Lucro {best.net_profit:.2f}%")

        return recommendations

    def _determine_execution_priority(self, crypto_result, forex_result, arbitrage_result) -> List[Dict[str, Any]]:
        """Determina prioridade de execução"""
        priorities = []

        # Arbitragem sempre tem prioridade máxima
        if arbitrage_result and arbitrage_result.best_opportunity:
            best = arbitrage_result.best_opportunity
            priorities.append({
                'market': 'arbitrage',
                'priority': 1,
                'action': f"Execute {best.type.value}",
                'profit_potential': best.net_profit,
                'time_sensitive': True
            })

        # Crypto e Forex baseado em confiança
        market_priorities = []

        if crypto_result:
            market_priorities.append({
                'market': 'crypto',
                'confidence': crypto_result.confidence,
                'signal': crypto_result.signal.value,
                'action': f"{crypto_result.signal.value} {crypto_result.symbol}"
            })

        if forex_result:
            market_priorities.append({
                'market': 'forex',
                'confidence': forex_result.confidence,
                'signal': forex_result.signal.value,
                'action': f"{forex_result.signal.value} {forex_result.pair}"
            })

        # Ordena por confiança
        market_priorities.sort(key=lambda x: x['confidence'], reverse=True)

        # Adiciona às prioridades
        for i, market_priority in enumerate(market_priorities):
            priorities.append({
                'market': market_priority['market'],
                'priority': i + 2,  # Após arbitragem
                'action': market_priority['action'],
                'confidence': market_priority['confidence'],
                'time_sensitive': False
            })

        return priorities


async def main():
    """Demonstração do sistema unificado"""
    print("=" * 80)
    print("🌐 LEXTRADER-IAG 4.0 - Analisador Unificado de Mercados")
    print("=" * 80)
    print()

    analyzer = UnifiedMarketAnalyzer()

    # Análise completa
    result = await analyzer.analyze_all_markets(
        crypto_symbols=['BTC/USDT'],
        forex_pairs=['EUR/USD'],
        arbitrage_assets=['BTC/USDT', 'ETH/USDT'],
        exchanges=['binance', 'coinbase']
    )

    print(f"🎯 Sinal Geral: {result.overall_signal.value}")
    print(f"🎯 Confiança: {result.confidence:.1f}%")
    print(f"📊 Mercados Analisados: {result.metadata['markets_analyzed']}")
    print(f"🔗 Regime de Correlação: {result.metadata['correlation_regime']}")
    print()

    print("📈 Análises por Mercado:")
    if result.crypto_analysis:
        print(f"  🪙 Crypto ({result.crypto_analysis.symbol}): {result.crypto_analysis.signal.value}")
    if result.forex_analysis:
        print(f"  💱 Forex ({result.forex_analysis.pair}): {result.forex_analysis.signal.value}")
    if result.arbitrage_analysis:
        print(f"  ⚡ Arbitragem: {result.arbitrage_analysis.opportunities_found} oportunidades")
    print()

    print("⚠️ Avaliação de Risco:")
    for risk_type, score in result.risk_assessment.items():
        print(f"  • {risk_type.replace('_', ' ').title()}: {score:.1f}/100")
    print()

    print("🎯 Prioridade de Execução:")
    for priority in result.execution_priority:
        print(f"  {priority['priority']}. {priority['action']} ({'⏰ Urgente' if priority.get('time_sensitive') else '📅 Normal'})")
    print()

    print("💡 Recomendações de Portfólio:")
    for rec in result.portfolio_recommendations:
        print(f"  {rec}")


if __name__ == "__main__":
    asyncio.run(main())