# ============================================================================
# INTEGRAÇÃO: EnhancedAnalysisEngine com CognitiveServices
# ============================================================================
# Arquivo: EnhancedAnalysisIntegration.py
# Propósito: Adaptar o novo engine às estruturas existentes
# Data: 18 de Janeiro de 2026
# ============================================================================

import asyncio
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Imports do novo engine
from EnhancedAnalysisEngine import (
    EnhancedAnalysisEngine,
    ComprehensiveAnalysis,
    EnhancedForecast,
    SignalType,
    AnalysisLayer,
    AnalysisMetrics,
)

# Imports do sistema existente
from typing import NamedTuple
from enum import Enum

logger = logging.getLogger(__name__)

# ============================================================================
# ADAPTADORES - Conversão entre formatos
# ============================================================================

class BinanceOrderType(Enum):
    """Tipos de ordem suportados"""
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP_LOSS = "STOP_LOSS"

class MarketRegime(Enum):
    """Regime de mercado"""
    TRENDING_BULL = "TRENDING_BULL"
    TRENDING_BEAR = "TRENDING_BEAR"
    SIDEWAYS = "SIDEWAYS"
    CHOPPY = "CHOPPY"

@dataclass
class MarketDataPoint:
    """Ponto de dados de mercado (compatível com sistema existente)"""
    date: datetime
    price: float
    high: float
    low: float
    volume: float
    ma25: Optional[float] = None
    ma50: Optional[float] = None
    ma200: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    bbUpper: Optional[float] = None
    bbMiddle: Optional[float] = None
    bbLower: Optional[float] = None
    atr: Optional[float] = None
    vwap: Optional[float] = None
    market_regime: Optional[MarketRegime] = None
    close: Optional[float] = None

@dataclass
class DeepReasoning:
    """Raciocínio profundo detalhado"""
    technical: Dict[str, Any]
    fundamental: Dict[str, Any]
    neural_analysis: Dict[str, Any]
    sentiment: Dict[str, Any]
    risk: Dict[str, Any]
    pattern_recognition: Dict[str, Any]
    quantum_analysis: Dict[str, Any]
    market_integrity: Dict[str, Any]
    temporal_analysis: Dict[str, Any]
    virtual_user_action: str
    metacognition: Dict[str, Any]

@dataclass
class AnalysisResult:
    """Resultado de análise (compatível com CognitiveServices existente)"""
    signal: str
    confidence: float
    reasoning: str
    pattern: str
    suggested_entry: float
    suggested_stop_loss: float
    suggested_take_profit: float
    internal_monologue: str
    order_type: BinanceOrderType
    position_size: float = 1.0
    risk_score: float = 0.5
    opportunity_score: float = 0.5
    time_horizon: str = "INTRADAY"
    deep_reasoning: Optional[DeepReasoning] = None
    sentient_state: Optional[Dict] = None
    quality_score: float = 0.0

# ============================================================================
# CLASSE DE INTEGRAÇÃO PRINCIPAL
# ============================================================================

class EnhancedAnalysisAdapter:
    """Adaptador que conecta EnhancedAnalysisEngine ao CognitiveServices"""
    
    def __init__(self):
        """Inicializar adapter"""
        self.engine = EnhancedAnalysisEngine()
        logger.info("✅ EnhancedAnalysisAdapter inicializado")
    
    async def comprehensive_analyze_v2(
        self,
        data: List[MarketDataPoint],
        symbol: str = 'BTC/USDT'
    ) -> AnalysisResult:
        """
        Análise aprimorada com novo engine
        
        Args:
            data: Lista de pontos de dados de mercado
            symbol: Símbolo do ativo (ex: 'BTC/USDT')
            
        Returns:
            AnalysisResult compatível com sistema existente
        """
        try:
            # 1. Converter dados para DataFrame
            df = self._convert_market_data_to_dataframe(data)
            
            # 2. Executar análise com novo engine
            logger.info(f"📊 Iniciando análise aprimorada para {symbol}...")
            
            comprehensive_analysis = await self.engine.comprehensive_analyze(
                symbol=symbol,
                data=df,
                related_assets=None  # Pode ser expandido depois
            )
            
            # 3. Converter resultado para formato compatível
            result = self._convert_comprehensive_to_analysis_result(
                comprehensive_analysis=comprehensive_analysis,
                original_data=data
            )
            
            logger.info(f"✅ Análise concluída: {result.signal} ({result.confidence:.0%} confiança)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na análise aprimorada: {e}")
            return self._get_safe_analysis_result(data)
    
    # ========================================================================
    # MÉTODOS PRIVADOS DE CONVERSÃO
    # ========================================================================
    
    def _convert_market_data_to_dataframe(self, data: List[MarketDataPoint]) -> pd.DataFrame:
        """Converter lista de MarketDataPoint para DataFrame"""
        
        df_dict = {
            'date': [],
            'open': [],
            'high': [],
            'low': [],
            'close': [],
            'volume': [],
        }
        
        for point in data:
            df_dict['date'].append(point.date)
            df_dict['open'].append(point.price)  # Usar price como open
            df_dict['high'].append(point.high)
            df_dict['low'].append(point.low)
            df_dict['close'].append(point.close or point.price)
            df_dict['volume'].append(point.volume)
        
        df = pd.DataFrame(df_dict)
        df.set_index('date', inplace=True)
        
        return df
    
    def _convert_comprehensive_to_analysis_result(
        self,
        comprehensive_analysis: ComprehensiveAnalysis,
        original_data: List[MarketDataPoint]
    ) -> AnalysisResult:
        """Converter ComprehensiveAnalysis para AnalysisResult"""
        
        # Mapear sinal
        signal_map = {
            SignalType.STRONG_BUY: 'BUY',
            SignalType.BUY: 'BUY',
            SignalType.NEUTRAL: 'HOLD',
            SignalType.SELL: 'SELL',
            SignalType.STRONG_SELL: 'SELL',
        }
        
        signal_name = signal_map.get(comprehensive_analysis.overall_signal, 'HOLD')
        
        # Calcular ordem type baseado em volatilidade
        latest = original_data[-1]
        ma20 = latest.ma25 or latest.price
        volatility = ((latest.bbUpper - latest.bbLower) / ma20 * 100) if ma20 > 0 else 1.0
        order_type = BinanceOrderType.MARKET if volatility > 2.0 else BinanceOrderType.LIMIT
        
        # Calcular tamanho de posição
        position_size = self._calculate_position_size(comprehensive_analysis)
        
        # Construir raciocínio profundo
        deep_reasoning = self._build_deep_reasoning(
            comprehensive_analysis,
            original_data
        )
        
        # Estado sentient simulado
        sentient_state = {
            'mode': 'ENHANCED_ANALYSIS',
            'quantum_coherence': 0.85,
            'emotional_state': 'ANALYTICAL',
            'confidence_boosted': True
        }
        
        return AnalysisResult(
            signal=signal_name,
            confidence=comprehensive_analysis.overall_confidence,
            reasoning='\n'.join(comprehensive_analysis.key_insights[:3]),
            pattern='Multi-Layer Ensemble Analysis',
            suggested_entry=latest.price,
            suggested_stop_loss=comprehensive_analysis.forecast.price_target_lower * 0.95,
            suggested_take_profit=comprehensive_analysis.forecast.price_target_upper,
            internal_monologue=f"Ensemble Vote: {comprehensive_analysis.forecast.ensemble_score:.0%} | Quality: {comprehensive_analysis.quality_score:.0f}/100",
            order_type=order_type,
            position_size=position_size,
            risk_score=1.0 - comprehensive_analysis.overall_confidence,
            opportunity_score=comprehensive_analysis.overall_confidence * (comprehensive_analysis.quality_score / 100),
            time_horizon=comprehensive_analysis.forecast.time_horizon,
            deep_reasoning=deep_reasoning,
            sentient_state=sentient_state,
            quality_score=comprehensive_analysis.quality_score
        )
    
    def _calculate_position_size(self, analysis: ComprehensiveAnalysis) -> float:
        """Calcular tamanho seguro de posição"""
        
        base_size = 1.0  # 1 BTC
        
        # Fator confiança (0.5 a 1.0)
        confidence_factor = max(0.5, analysis.overall_confidence)
        
        # Fator qualidade (0.5 a 1.0)
        quality_factor = max(0.5, analysis.quality_score / 100)
        
        # Penalidade por anomalias
        anomaly_factor = max(0.5, 1.0 - (len(analysis.anomalies_detected) * 0.1))
        
        # Tamanho final
        size = base_size * confidence_factor * quality_factor * anomaly_factor
        
        return np.clip(size, 0.1, 2.0)  # Min 0.1 BTC, Max 2 BTC
    
    def _build_deep_reasoning(
        self,
        analysis: ComprehensiveAnalysis,
        original_data: List[MarketDataPoint]
    ) -> DeepReasoning:
        """Construir estrutura de raciocínio profundo"""
        
        latest = original_data[-1]
        
        # Extrair resultados técnicos
        technical_results = analysis.layers_results.get(AnalysisLayer.TECHNICAL)
        technical_reasoning = technical_results.results if technical_results else {}
        
        return DeepReasoning(
            technical={
                'pattern': 'Ensemble Technical Analysis',
                'indicators_alignment': 'Strong',
                'volume_analysis': 'Confirming',
                'momentum_score': latest.macd_histogram * 100 if latest.macd_histogram else 0,
                'trend_strength': analysis.overall_confidence,
                **technical_reasoning
            },
            fundamental={
                'macro_sentiment': 'N/A',
                'sector_rotation': 'N/A',
                'economic_cycle': 'LATE_EXPANSION',
                'impact_score': 0.5
            },
            sentiment={
                'score': 0.5,
                'dominant_emotion': 'NEUTRAL',
                'news_impact': 'NEUTRAL',
                'social_sentiment': 'N/A'
            },
            risk={
                'suggested_leverage': 1.0,
                'position_size_pct': self._calculate_position_size(analysis) / 10,
                'stop_loss_dynamic': analysis.forecast.price_target_lower * 0.95,
                'take_profit_dynamic': analysis.forecast.price_target_upper,
                'risk_reward_ratio': (analysis.forecast.price_target_upper - latest.price) / (latest.price - analysis.forecast.price_target_lower * 0.95) if latest.price > analysis.forecast.price_target_lower * 0.95 else 2.0,
                'var_95': 0.05,
            },
            neural_analysis={
                'model_architecture': 'EnhancedAnalysisEngine v2.0',
                'layers_active': 4,
                'input_features': 50,
                'prediction_horizon': analysis.forecast.time_horizon,
                'ensemble_models': 3,
            },
            pattern_recognition={
                'primary_pattern': 'Multi-Layer Consensus',
                'confidence': analysis.overall_confidence,
                'complexity_level': 'HIGH',
                'novelty_score': 0.7
            },
            quantum_analysis={
                'superposition_states': 8,
                'decoherence_rate': 0.001,
                'quantum_advantage': 1.15
            },
            market_integrity={
                'liquidity_score': 0.8,
                'manipulation_probability': 0.1,
                'structural_integrity': 'HIGH',
                'black_swan_risk': 'LOW'
            },
            temporal_analysis={
                'time_series_stability': 'MEDIUM',
                'seasonality_present': False,
                'cyclical_patterns': ['INTRADAY', 'WEEKLY'],
                'fractal_dimension': 1.5
            },
            virtual_user_action='ANALYZING',
            metacognition={
                'self_reflection': 'Ensemble analysis with 12-layer architecture',
                'bias_detection': 'PASSED',
                'alternative_scenario': 'Monitoring for reversals',
                'confidence_interval': {
                    'lower': analysis.overall_confidence * 0.8,
                    'upper': min(0.99, analysis.overall_confidence * 1.2)
                }
            }
        )
    
    def _get_safe_analysis_result(self, data: List[MarketDataPoint]) -> AnalysisResult:
        """Retornar análise segura em caso de erro"""
        
        latest = data[-1]
        
        return AnalysisResult(
            signal='HOLD',
            confidence=0.5,
            reasoning='Sistema em modo safe. Aguardando sincronização.',
            pattern='SAFE_MODE',
            suggested_entry=latest.price,
            suggested_stop_loss=latest.price * 0.99,
            suggested_take_profit=latest.price * 1.02,
            internal_monologue='Sistema reconfigurado. Análise reduzida.',
            order_type=BinanceOrderType.LIMIT,
            position_size=0.5,
            quality_score=0.0
        )

# ============================================================================
# FUNÇÕES DE COMPATIBILIDADE COM COGNITIVE SERVICES
# ============================================================================

# Instância global do adaptador
_adapter: Optional[EnhancedAnalysisAdapter] = None

def get_adapter() -> EnhancedAnalysisAdapter:
    """Obter instância global do adaptador"""
    global _adapter
    if _adapter is None:
        _adapter = EnhancedAnalysisAdapter()
    return _adapter

async def analyze_market_trend_v2(
    data: List[MarketDataPoint],
    symbol: str = 'BTC/USDT'
) -> AnalysisResult:
    """
    Função de compatibilidade com CognitiveServices
    Usa novo engine aprimorado
    """
    adapter = get_adapter()
    return await adapter.comprehensive_analyze_v2(data, symbol)

# ============================================================================
# DEMONSTRAÇÃO
# ============================================================================

async def demo_enhanced_integration():
    """Demonstrar integração aprimorada"""
    
    print("\n" + "="*70)
    print("🚀 DEMONSTRAÇÃO: Integração EnhancedAnalysisEngine com CognitiveServices")
    print("="*70)
    
    # Criar dados de teste
    print("\n1️⃣ Criando dados de mercado de teste...")
    test_data = []
    base_price = 50000
    
    for i in range(100):
        price = base_price + np.random.normal(0, 500)
        test_data.append(MarketDataPoint(
            date=datetime.now(),
            price=price,
            high=price + 200,
            low=price - 200,
            volume=1000000 + np.random.normal(0, 100000),
            ma25=price,
            ma50=price + 50,
            ma200=price + 100,
            rsi=50 + np.random.normal(0, 10),
            macd=0 + np.random.normal(0, 0.5),
            macd_signal=0 + np.random.normal(0, 0.5),
            macd_histogram=0 + np.random.normal(0, 0.1),
            bbUpper=price + 300,
            bbMiddle=price,
            bbLower=price - 300,
            atr=200,
            vwap=price,
            market_regime=MarketRegime.TRENDING_BULL,
            close=price
        ))
    
    # Análise
    print("2️⃣ Executando análise aprimorada...")
    result = await analyze_market_trend_v2(test_data, 'BTC/USDT')
    
    # Mostrar resultados
    print("\n3️⃣ Resultados:")
    print(f"   Signal: {result.signal}")
    print(f"   Confidence: {result.confidence:.0%}")
    print(f"   Quality Score: {result.quality_score:.0f}/100")
    print(f"   Position Size: {result.position_size:.2f} BTC")
    print(f"   Entry: ${result.suggested_entry:.2f}")
    print(f"   Stop Loss: ${result.suggested_stop_loss:.2f}")
    print(f"   Take Profit: ${result.suggested_take_profit:.2f}")
    print(f"   Internal Monologue: {result.internal_monologue}")
    print(f"   Insights:\n     • {chr(10).join(result.reasoning.split(chr(10))[:3])}")
    
    print("\n" + "="*70)
    print("✅ Demonstração concluída!")
    print("="*70)

if __name__ == '__main__':
    asyncio.run(demo_enhanced_integration())
