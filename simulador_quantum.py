# quantum/simulador_quantum.py
import streamlit as st
import asyncio
import time
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging
import random
import math
from dataclasses import dataclass
from enum import Enum
import json

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('simulador_quantum.log')
    ]
)
logger = logging.getLogger(__name__)

class QuantumState(Enum):
    """Estados quânticos do sistema"""
    SUPERPOSITION = "superposition"
    ENTANGLEMENT = "entanglement"
    COHERENCE = "coherence"
    DECOHERENCE = "decoherence"
    MEASURED = "measured"

class CircuitType(Enum):
    """Tipos de circuitos quânticos"""
    PRICE_PREDICTION = "price_prediction"
    RISK_ANALYSIS = "risk_analysis"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"
    ARBITRAGE_DETECTION = "arbitrage_detection"
    MARKET_SIMULATION = "market_simulation"

@dataclass
class QuantumResult:
    """Resultado de uma computação quântica"""
    circuit_type: CircuitType
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    confidence: float
    execution_time: float
    qubits_used: int
    quantum_advantage: float
    timestamp: datetime

@dataclass
class QuantumOpportunity:
    """Oportunidade detectada pelo simulador quântico"""
    id: str
    symbol: str
    predicted_price: float
    current_price: float
    discrepancy: float
    confidence: float
    quantum_certainty: float
    time_horizon: str  # SHORT, MEDIUM, LONG
    risk_level: str
    action: str  # BUY, SELL, HOLD
    timestamp: datetime

class SimuladorQuantum:
    """
    Simulador Quântico Avançado para análise de mercados financeiros
    Integra com o sistema de arbitragem quântica
    """
    
    def __init__(self, quantum_bits: int = 1024):
        self.quantum_bits = quantum_bits
        self.circuits = {}
        self.results_history: List[QuantumResult] = []
        self.quantum_state = QuantumState.COHERENCE
        self.entanglement_networks = {}
        
        # Configurações do simulador
        self.config = {
            'max_parallel_circuits': 8,
            'quantum_noise_level': 0.05,
            'decoherence_time': 100,  # ms
            'error_correction': True,
            'quantum_volume': 16,
            'simulation_fidelity': 0.95
        }
        
        # Inicializar circuitos quânticos
        self._initialize_quantum_circuits()
        
        logger.info(f"⚛️ Simulador Quântico inicializado com {quantum_bits} qbits")

    def _initialize_quantum_circuits(self):
        """Inicializa os circuitos quânticos principais"""
        self.circuits = {
            CircuitType.PRICE_PREDICTION: {
                'qubits': 128,
                'depth': 50,
                'gates': ['H', 'CNOT', 'RX', 'RY', 'RZ', 'MEASURE'],
                'description': 'Predição de preços usando superposição quântica'
            },
            CircuitType.RISK_ANALYSIS: {
                'qubits': 64,
                'depth': 30,
                'gates': ['H', 'CNOT', 'CZ', 'TOFFOLI', 'MEASURE'],
                'description': 'Análise de risco com emaranhamento quântico'
            },
            CircuitType.PORTFOLIO_OPTIMIZATION: {
                'qubits': 256,
                'depth': 75,
                'gates': ['H', 'CNOT', 'SWAP', 'CRX', 'CRY', 'MEASURE'],
                'description': 'Otimização de portfólio com algoritmos quânticos'
            },
            CircuitType.ARBITRAGE_DETECTION: {
                'qubits': 192,
                'depth': 60,
                'gates': ['H', 'CNOT', 'CCNOT', 'MEASURE'],
                'description': 'Detecção de arbitragem com vantagem quântica'
            },
            CircuitType.MARKET_SIMULATION: {
                'qubits': 512,
                'depth': 100,
                'gates': ['H', 'CNOT', 'RX', 'RY', 'RZ', 'MEASURE'],
                'description': 'Simulação de mercado em superposição quântica'
            }
        }

    async def analyze_market_quantum(self, market_data: Dict[str, Any]) -> QuantumResult:
        """
        Análise quântica completa do mercado
        Integra com o sistema de arbitragem
        """
        logger.info("🔮 Iniciando análise quântica do mercado...")
        
        start_time = time.time()
        
        try:
            # Executar múltiplas análises quânticas em paralelo
            analyses = await asyncio.gather(
                self._quantum_price_analysis(market_data),
                self._quantum_risk_assessment(market_data),
                self._quantum_momentum_detection(market_data),
                self._quantum_volatility_prediction(market_data),
                return_exceptions=True
            )
            
            # Combinar resultados
            combined_result = await self._combine_quantum_analyses(analyses)
            
            execution_time = time.time() - start_time
            
            result = QuantumResult(
                circuit_type=CircuitType.MARKET_SIMULATION,
                input_data=market_data,
                output_data=combined_result,
                confidence=combined_result.get('overall_confidence', 0.7),
                execution_time=execution_time,
                qubits_used=self.circuits[CircuitType.MARKET_SIMULATION]['qubits'],
                quantum_advantage=await self._calculate_quantum_advantage(execution_time),
                timestamp=datetime.now()
            )
            
            self.results_history.append(result)
            logger.info(f"✅ Análise quântica concluída em {execution_time:.3f}s")
            
            return result
            
        except Exception as error:
            logger.error(f"❌ Erro na análise quântica: {error}")
            raise error

    async def predict_price_quantum(self, symbol: str, historical_data: List[float]) -> QuantumResult:
        """
        Predição de preço usando algoritmos quânticos
        """
        logger.info(f"📈 Predição quântica de preço para {symbol}...")
        
        start_time = time.time()
        
        try:
            # Preparar dados para o circuito quântico
            quantum_data = await self._prepare_quantum_price_data(historical_data)
            
            # Executar circuito de predição
            prediction_result = await self._execute_price_prediction_circuit(quantum_data)
            
            execution_time = time.time() - start_time
            
            result = QuantumResult(
                circuit_type=CircuitType.PRICE_PREDICTION,
                input_data={'symbol': symbol, 'historical_data': historical_data},
                output_data=prediction_result,
                confidence=prediction_result.get('prediction_confidence', 0.75),
                execution_time=execution_time,
                qubits_used=self.circuits[CircuitType.PRICE_PREDICTION]['qubits'],
                quantum_advantage=await self._calculate_quantum_advantage(execution_time),
                timestamp=datetime.now()
            )
            
            self.results_history.append(result)
            logger.info(f"🎯 Predição quântica: {prediction_result.get('predicted_price', 0):.2f}")
            
            return result
            
        except Exception as error:
            logger.error(f"❌ Erro na predição quântica: {error}")
            raise error

    async def detect_arbitrage_opportunities(self, market_data: Dict[str, Any]) -> List[QuantumOpportunity]:
        """
        Detecta oportunidades de arbitragem usando computação quântica
        Integra diretamente com o QuantumArbitrage
        """
        logger.info("🎯 Detectando oportunidades de arbitragem quântica...")
        
        try:
            # Análise quântica do mercado
            quantum_analysis = await self.analyze_market_quantum(market_data)
            
            # Detectar discrepâncias quânticas
            opportunities = await self._find_quantum_discrepancies(quantum_analysis, market_data)
            
            # Aplicar otimização quântica
            optimized_opportunities = await self._quantum_optimize_opportunities(opportunities)
            
            logger.info(f"✅ {len(optimized_opportunities)} oportunidades quânticas detectadas")
            return optimized_opportunities
            
        except Exception as error:
            logger.error(f"❌ Erro na detecção de oportunidades: {error}")
            return []

    async def optimize_portfolio_quantum(self, portfolio: Dict[str, Any], market_data: Dict[str, Any]) -> QuantumResult:
        """
        Otimização de portfólio usando algoritmos quânticos
        """
        logger.info("💼 Otimizando portfólio com computação quântica...")
        
        start_time = time.time()
        
        try:
            # Executar algoritmo quântico de otimização
            optimization_result = await self._execute_portfolio_optimization_circuit(portfolio, market_data)
            
            execution_time = time.time() - start_time
            
            result = QuantumResult(
                circuit_type=CircuitType.PORTFOLIO_OPTIMIZATION,
                input_data={'portfolio': portfolio, 'market_data': market_data},
                output_data=optimization_result,
                confidence=optimization_result.get('optimization_confidence', 0.8),
                execution_time=execution_time,
                qubits_used=self.circuits[CircuitType.PORTFOLIO_OPTIMIZATION]['qubits'],
                quantum_advantage=await self._calculate_quantum_advantage(execution_time),
                timestamp=datetime.now()
            )
            
            self.results_history.append(result)
            logger.info("✅ Portfólio otimizado com vantagem quântica")
            
            return result
            
        except Exception as error:
            logger.error(f"❌ Erro na otimização de portfólio: {error}")
            raise error

    async def assess_risk_quantum(self, positions: Dict[str, Any], market_conditions: Dict[str, Any]) -> QuantumResult:
        """
        Avaliação de risco usando algoritmos quânticos
        """
        logger.info("🛡️ Avaliando risco com computação quântica...")
        
        start_time = time.time()
        
        try:
            # Executar análise de risco quântica
            risk_assessment = await self._execute_risk_analysis_circuit(positions, market_conditions)
            
            execution_time = time.time() - start_time
            
            result = QuantumResult(
                circuit_type=CircuitType.RISK_ANALYSIS,
                input_data={'positions': positions, 'market_conditions': market_conditions},
                output_data=risk_assessment,
                confidence=risk_assessment.get('risk_confidence', 0.85),
                execution_time=execution_time,
                qubits_used=self.circuits[CircuitType.RISK_ANALYSIS]['qubits'],
                quantum_advantage=await self._calculate_quantum_advantage(execution_time),
                timestamp=datetime.now()
            )
            
            self.results_history.append(result)
            logger.info(f"✅ Risco avaliado: {risk_assessment.get('overall_risk', 'MEDIUM')}")
            
            return result
            
        except Exception as error:
            logger.error(f"❌ Erro na avaliação de risco: {error}")
            raise error

    # Métodos internos de simulação quântica
    async def _quantum_price_analysis(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise quântica de preços"""
        await asyncio.sleep(0.1)  # Simulação de processamento quântico
        
        # Simular algoritmo quântico de análise de preços
        current_price = market_data.get('current_price', 100)
        volatility = market_data.get('volatility', 0.02)
        
        # Usar superposição quântica para explorar múltiplos cenários
        quantum_superposition = await self._create_price_superposition(current_price, volatility)
        
        return {
            'quantum_price_estimate': quantum_superposition['expected_value'],
            'price_probability_distribution': quantum_superposition['distribution'],
            'quantum_volatility': quantum_superposition['volatility'],
            'confidence_interval': quantum_superposition['confidence_interval'],
            'quantum_metrics': {
                'wave_function_collapse': random.uniform(0.7, 0.95),
                'quantum_interference': random.uniform(0.6, 0.9),
                'probability_amplitude': random.uniform(0.5, 0.85)
            }
        }

    async def _quantum_risk_assessment(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Avaliação de risco quântica"""
        await asyncio.sleep(0.08)
        
        # Simular avaliação de risco com emaranhamento quântico
        risk_factors = await self._entangle_risk_factors(market_data)
        
        return {
            'quantum_var': risk_factors['value_at_risk'],
            'risk_superposition': risk_factors['risk_states'],
            'quantum_hedge_ratios': risk_factors['hedge_ratios'],
            'entanglement_correlation': risk_factors['correlation_matrix'],
            'risk_metrics': {
                'quantum_beta': random.uniform(0.8, 1.2),
                'coherence_risk': random.uniform(0.1, 0.4),
                'decoherence_probability': random.uniform(0.05, 0.2)
            }
        }

    async def _quantum_momentum_detection(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detecção de momentum quântico"""
        await asyncio.sleep(0.06)
        
        # Simular detecção de momentum com algoritmos quânticos
        momentum_states = await self._analyze_quantum_momentum(market_data)
        
        return {
            'quantum_momentum': momentum_states['momentum_vector'],
            'wave_pattern': momentum_states['wave_analysis'],
            'phase_transition': momentum_states['phase_detection'],
            'momentum_confidence': momentum_states['certainty'],
            'momentum_metrics': {
                'quantum_velocity': random.uniform(-0.1, 0.1),
                'probability_current': random.uniform(0.1, 0.5),
                'wave_packet_spread': random.uniform(0.01, 0.1)
            }
        }

    async def _quantum_volatility_prediction(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predição de volatilidade quântica"""
        await asyncio.sleep(0.07)
        
        # Simular predição de volatilidade com métodos quânticos
        volatility_forecast = await self._forecast_quantum_volatility(market_data)
        
        return {
            'quantum_volatility_forecast': volatility_forecast['volatility_prediction'],
            'uncertainty_principle': volatility_forecast['uncertainty'],
            'volatility_superposition': volatility_forecast['volatility_states'],
            'prediction_horizon': volatility_forecast['time_horizon'],
            'volatility_metrics': {
                'quantum_fluctuations': random.uniform(0.01, 0.05),
                'coherence_length': random.uniform(10, 50),
                'tunneling_probability': random.uniform(0.001, 0.01)
            }
        }

    async def _combine_quantum_analyses(self, analyses: List[Any]) -> Dict[str, Any]:
        """Combina múltiplas análises quânticas"""
        valid_analyses = [a for a in analyses if not isinstance(a, Exception)]
        
        if not valid_analyses:
            return {'error': 'No valid analyses'}
        
        # Combinar resultados usando superposição quântica
        combined = {
            'overall_confidence': np.mean([a.get('confidence', 0.5) for a in valid_analyses if 'confidence' in a]),
            'market_outlook': await this._synthesize_quantum_outlook(valid_analyses),
            'trading_signals': await this._extract_quantum_signals(valid_analyses),
            'risk_assessment': await this._combine_quantum_risks(valid_analyses),
            'quantum_metrics': {
                'superposition_coherence': random.uniform(0.8, 0.98),
                'entanglement_strength': random.uniform(0.7, 0.95),
                'measurement_certainty': random.uniform(0.6, 0.9)
            }
        }
        
        return combined

    async def _execute_price_prediction_circuit(self, quantum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa circuito quântico de predição de preços"""
        await asyncio.sleep(0.15)
        
        # Simular execução de circuito quântico
        base_price = quantum_data.get('current_price', 100)
        historical_volatility = quantum_data.get('volatility', 0.02)
        
        # Aplicar algoritmo quântico de predição
        quantum_prediction = await this._quantum_forecast_algorithm(base_price, historical_volatility)
        
        return {
            'predicted_price': quantum_prediction['price'],
            'prediction_confidence': quantum_prediction['confidence'],
            'price_range': quantum_prediction['range'],
            'quantum_factors': quantum_prediction['factors'],
            'time_horizon': quantum_prediction['horizon']
        }

    async def _find_quantum_discrepancies(self, quantum_analysis: QuantumResult, market_data: Dict[str, Any]) -> List[QuantumOpportunity]:
        """Encontra discrepâncias usando análise quântica"""
        opportunities = []
        
        # Simular detecção de discrepâncias quânticas
        symbols = market_data.get('symbols', ['BTC/USD', 'ETH/USD', 'ADA/USD'])
        
        for symbol in symbols:
            current_price = self._simulate_market_price(symbol)
            quantum_price = current_price * random.uniform(0.98, 1.02)  # Discrepância simulada
            
            discrepancy = abs(quantum_price - current_price) / current_price
            
            if discrepancy > 0.005:  # 0.5% de discrepância mínima
                opportunity = QuantumOpportunity(
                    id=f"QUANTUM_OPP_{symbol}_{int(time.time())}",
                    symbol=symbol,
                    predicted_price=quantum_price,
                    current_price=current_price,
                    discrepancy=discrepancy,
                    confidence=random.uniform(0.7, 0.95),
                    quantum_certainty=random.uniform(0.8, 0.98),
                    time_horizon=random.choice(['SHORT', 'MEDIUM', 'LONG']),
                    risk_level=random.choice(['LOW', 'MEDIUM', 'HIGH']),
                    action='BUY' if quantum_price > current_price else 'SELL',
                    timestamp=datetime.now()
                )
                opportunities.append(opportunity)
        
        return opportunities

    # Métodos de simulação quântica
    async def _create_price_superposition(self, base_price: float, volatility: float) -> Dict[str, Any]:
        """Cria superposição quântica de preços"""
        # Simular superposição de estados de preço
        states = 1000  # Número de estados na superposição
        price_states = np.random.normal(base_price, base_price * volatility, states)
        
        return {
            'expected_value': float(np.mean(price_states)),
            'distribution': price_states.tolist(),
            'volatility': float(np.std(price_states)),
            'confidence_interval': [
                float(np.percentile(price_states, 5)),
                float(np.percentile(price_states, 95))
            ]
        }

    async def _entangle_risk_factors(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria emaranhamento quântico entre fatores de risco"""
        factors = ['price_risk', 'volatility_risk', 'liquidity_risk', 'correlation_risk']
        
        # Simular matriz de correlação emaranhada
        correlation_matrix = np.random.uniform(0.3, 0.9, (len(factors), len(factors)))
        np.fill_diagonal(correlation_matrix, 1.0)
        
        return {
            'value_at_risk': random.uniform(0.01, 0.05),
            'risk_states': factors,
            'hedge_ratios': {factor: random.uniform(0.1, 0.9) for factor in factors},
            'correlation_matrix': correlation_matrix.tolist()
        }

    async def _calculate_quantum_advantage(self, execution_time: float) -> float:
        """Calcula vantagem quântica sobre métodos clássicos"""
        # Simular vantagem quântica (2x a 1000x mais rápido)
        classical_time_estimate = execution_time * random.uniform(10, 1000)
        quantum_advantage = classical_time_estimate / execution_time
        
        return min(quantum_advantage, 1000)  # Limitar a 1000x

    async def _prepare_quantum_price_data(self, historical_data: List[float]) -> Dict[str, Any]:
        """Prepara dados para processamento quântico"""
        if not historical_data:
            historical_data = [100 + random.uniform(-10, 10) for _ in range(100)]
        
        returns = np.diff(historical_data) / historical_data[:-1]
        
        return {
            'current_price': historical_data[-1] if historical_data else 100,
            'volatility': float(np.std(returns)) if len(returns) > 1 else 0.02,
            'trend': np.polyfit(range(len(historical_data)), historical_data, 1)[0] if historical_data else 0,
            'data_points': len(historical_data)
        }

    # Métodos de integração com o sistema de arbitragem
    async def get_quantum_arbitrage_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera sinais de arbitragem baseados em computação quântica
        Para integração com o QuantumArbitrage
        """
        try:
            # Análise quântica do mercado
            quantum_analysis = await self.analyze_market_quantum(market_data)
            
            # Detectar oportunidades
            opportunities = await self.detect_arbitrage_opportunities(market_data)
            
            # Gerar sinais de trading
            signals = await this._generate_quantum_trading_signals(quantum_analysis, opportunities)
            
            return {
                'signals': signals,
                'quantum_confidence': quantum_analysis.confidence,
                'opportunities_count': len(opportunities),
                'timestamp': datetime.now(),
                'quantum_metrics': quantum_analysis.output_data.get('quantum_metrics', {})
            }
            
        except Exception as error:
            logger.error(f"❌ Erro na geração de sinais quânticos: {error}")
            return {'error': str(error)}

    async def optimize_arbitrage_execution(self, opportunity: Any) -> Dict[str, Any]:
        """
        Otimiza execução de arbitragem usando algoritmos quânticos
        Para integração com o QuantumArbitrage
        """
        try:
            # Simular otimização quântica da execução
            optimization = await this._quantum_execution_optimization(opportunity)
            
            return {
                'optimized_execution_plan': optimization['plan'],
                'quantum_speedup': optimization['speedup'],
                'risk_reduction': optimization['risk_reduction'],
                'profit_enhancement': optimization['profit_boost'],
                'timestamp': datetime.now()
            }
            
        except Exception as error:
            logger.error(f"❌ Erro na otimização de execução: {error}")
            return {'error': str(error)}

    # Métodos auxiliares
    def _simulate_market_price(self, symbol: str) -> float:
        """Simula preço de mercado para um símbolo"""
        base_prices = {
            'BTC/USD': 45000,
            'ETH/USD': 3000,
            'ADA/USD': 0.5,
            'DOT/USD': 7.0,
            'LINK/USD': 15.0
        }
        
        base_price = base_prices.get(symbol, 100)
        return base_price * (1 + random.uniform(-0.02, 0.02))

    async def _quantum_optimize_opportunities(self, opportunities: List[QuantumOpportunity]) -> List[QuantumOpportunity]:
        """Otimiza oportunidades usando algoritmos quânticos"""
        if not opportunities:
            return []
        
        # Ordenar por confiança quântica
        opportunities.sort(key=lambda x: x.quantum_certainty, reverse=True)
        
        # Aplicar filtro quântico
        filtered_opportunities = [
            opp for opp in opportunities 
            if opp.discrepancy > 0.005 and opp.confidence > 0.7
        ]
        
        return filtered_opportunities[:10]  # Limitar a 10 melhores oportunidades

    # Métodos de monitoramento e relatórios
    def get_quantum_metrics(self) -> Dict[str, Any]:
        """Retorna métricas do simulador quântico"""
        total_executions = len(self.results_history)
        avg_confidence = np.mean([r.confidence for r in self.results_history]) if self.results_history else 0
        avg_advantage = np.mean([r.quantum_advantage for r in self.results_history]) if self.results_history else 0
        
        return {
            'total_quantum_executions': total_executions,
            'average_confidence': avg_confidence,
            'average_quantum_advantage': avg_advantage,
            'quantum_bits_available': self.quantum_bits,
            'active_circuits': len(self.circuits),
            'quantum_state': self.quantum_state.value,
            'system_fidelity': self.config['simulation_fidelity'],
            'timestamp': datetime.now()
        }

    def get_circuit_status(self) -> Dict[str, Any]:
        """Retorna status dos circuitos quânticos"""
        return {
            circuit_type.value: {
                'qubits': config['qubits'],
                'depth': config['depth'],
                'gates': config['gates'],
                'description': config['description']
            }
            for circuit_type, config in self.circuits.items()
        }

# Função de demonstração e integração
async def main():
    """Demonstração do Simulador Quântico e integração com arbitragem"""
    simulador = SimuladorQuantum()
    
    print("⚛️ SIMULADOR QUÂNTICO - DEMONSTRAÇÃO")
    print("=" * 50)
    
    # Dados de mercado simulados
    market_data = {
        'symbols': ['BTC/USD', 'ETH/USD', 'ADA/USD'],
        'current_price': 45000,
        'volatility': 0.02,
        'volume': 1000000,
        'timestamp': datetime.now()
    }
    
    # 1. Análise quântica do mercado
    print("\n1. Executando análise quântica do mercado...")
    quantum_analysis = await simulador.analyze_market_quantum(market_data)
    print(f"   ✅ Confiança: {quantum_analysis.confidence:.1%}")
    print(f"   ⚛️ Vantagem quântica: {quantum_analysis.quantum_advantage:.1f}x")
    
    # 2. Predição de preços
    print("\n2. Predição quântica de preços...")
    historical_data = [45000 + random.uniform(-1000, 1000) for _ in range(100)]
    price_prediction = await simulador.predict_price_quantum('BTC/USD', historical_data)
    print(f"   📈 Preço predito: ${price_prediction.output_data.get('predicted_price', 0):.2f}")
    
    # 3. Detecção de oportunidades
    print("\n3. Detectando oportunidades de arbitragem...")
    opportunities = await simulador.detect_arbitrage_opportunities(market_data)
    print(f"   🎯 {len(opportunities)} oportunidades detectadas")
    
    if opportunities:
        best_opp = opportunities[0]
        print(f"   💰 Melhor oportunidade: {best_opp.symbol}")
        print(f"   📊 Discrepância: {best_opp.discrepancy:.3%}")
        print(f"   🎯 Ação: {best_opp.action}")
    
    # 4. Métricas do sistema
    print("\n4. Métricas do simulador quântico:")
    metrics = simulador.get_quantum_metrics()
    for key, value in metrics.items():
        if key != 'timestamp':
            print(f"   {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())