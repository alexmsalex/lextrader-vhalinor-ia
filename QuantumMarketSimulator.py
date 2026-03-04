import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# --- TYPES ---
class CircuitType(str, Enum):
    PRICE_PREDICTION = "PRICE_PREDICTION"
    RISK_ANALYSIS = "RISK_ANALYSIS"
    PORTFOLIO_OPTIMIZATION = "PORTFOLIO_OPTIMIZATION"
    ARBITRAGE_DETECTION = "ARBITRAGE_DETECTION"
    MARKET_SIMULATION = "MARKET_SIMULATION"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TimeHorizon(str, Enum):
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"

@dataclass
class QuantumSimResult:
    circuit_type: CircuitType
    output_data: Dict[str, Any]
    confidence: float
    execution_time: float
    qubits_used: int
    quantum_advantage: float
    timestamp: datetime

@dataclass
class QuantumSimOpportunity:
    id: str
    symbol: str
    current_price: float
    predicted_price: float
    discrepancy: float
    confidence: float
    quantum_certainty: float
    time_horizon: TimeHorizon
    risk_level: RiskLevel
    action: str
    timestamp: datetime

# --- SIMULATED AGI CORE ---
class SentientCore:
    """Simulação do núcleo AGI para influenciar parâmetros quânticos"""
    def __init__(self):
        self.stability = 75.0
        self.confidence = 80.0
        self.focus = 85.0
        self.curiosity = 70.0
        self.creativity = 75.0
    
    def get_vector(self) -> Dict[str, float]:
        """Retorna vetor emocional atual"""
        # Simulate small variations
        self._update_emotions()
        return {
            "stability": self.stability,
            "confidence": self.confidence,
            "focus": self.focus,
            "curiosity": self.curiosity,
            "creativity": self.creativity
        }
    
    def _update_emotions(self):
        """Atualiza emoções com variação suave"""
        for attr in ['stability', 'confidence', 'focus', 'curiosity', 'creativity']:
            current = getattr(self, attr)
            change = random.uniform(-0.5, 0.5)
            new_value = max(0, min(100, current + change))
            setattr(self, attr, new_value)

# --- UTILS: Gaussian Random ---
def gaussian_random(mean: float = 0, stdev: float = 1) -> float:
    """Transformada Box-Muller para distribuição normal"""
    u = 1 - random.random()
    v = random.random()
    z = np.sqrt(-2.0 * np.log(u)) * np.cos(2.0 * np.pi * v)
    return z * stdev + mean

# --- CIRCUIT CONFIGS ---
CIRCUIT_CONFIGS = {
    CircuitType.PRICE_PREDICTION: {
        "qubits": 128,
        "depth": 50,
        "gates": ['H', 'CNOT', 'RX', 'RY', 'RZ', 'MEASURE'],
        "description": 'Predição de preços usando superposição quântica'
    },
    CircuitType.RISK_ANALYSIS: {
        "qubits": 64,
        "depth": 30,
        "gates": ['H', 'CNOT', 'CZ', 'TOFFOLI', 'MEASURE'],
        "description": 'Análise de risco com emaranhamento quântico'
    },
    CircuitType.PORTFOLIO_OPTIMIZATION: {
        "qubits": 256,
        "depth": 75,
        "gates": ['H', 'CNOT', 'SWAP', 'CRX', 'CRY', 'MEASURE'],
        "description": 'Otimização de portfólio com algoritmos quânticos'
    },
    CircuitType.ARBITRAGE_DETECTION: {
        "qubits": 192,
        "depth": 60,
        "gates": ['H', 'CNOT', 'CCNOT', 'MEASURE'],
        "description": 'Detecção de arbitragem com vantagem quântica'
    },
    CircuitType.MARKET_SIMULATION: {
        "qubits": 512,
        "depth": 100,
        "gates": ['H', 'CNOT', 'RX', 'RY', 'RZ', 'MEASURE'],
        "description": 'Simulação de mercado em superposição quântica'
    }
}

# --- MAIN SIMULATOR ---
class QuantumMarketSimulator:
    """Simulador Quântico de Mercado"""
    
    def __init__(self, quantum_bits: int = 1024):
        self.quantum_bits = quantum_bits
        self.results_history: List[QuantumSimResult] = []
        self.active_circuits: List[CircuitType] = []
        
        # AGI Core
        self.sentient_core = SentientCore()
        
        # Internal Config (Influenced by AGI)
        self.config = {
            "max_parallel_circuits": 8,
            "quantum_noise_level": 0.05,
            "decoherence_time": 100,
            "error_correction": True,
            "quantum_volume": 16,
            "simulation_fidelity": 0.95
        }
        
        print(f"⚛️ Simulador Quântico de Mercado inicializado ({quantum_bits} Qubits)")
    
    def _update_agi_parameters(self):
        """Integra com o Sentient Core para modular física da simulação"""
        emotion = self.sentient_core.get_vector()
        
        # High Focus = Reduced Noise
        self.config["quantum_noise_level"] = max(0.001, 0.05 - (emotion["focus"] / 2000))
        
        # High Stability = Longer Coherence
        self.config["decoherence_time"] = 100 + (emotion["stability"] * 2)
        
        # High Curiosity = More Circuits
        self.config["max_parallel_circuits"] = 8 + int(emotion["curiosity"] / 20)
        
        # Confidence = Higher Fidelity
        self.config["simulation_fidelity"] = 0.9 + (emotion["confidence"] / 1000)
    
    # --- PUBLIC API ---
    
    async def analyze_market_quantum(self, market_data: Dict[str, Any]) -> QuantumSimResult:
        """Análise quântica completa do mercado"""
        self._update_agi_parameters()
        start_time = time.time()
        
        try:
            # Execute parallel simulations
            price_analysis = await self._quantum_price_analysis(market_data)
            risk_analysis = await self._quantum_risk_assessment(market_data)
            momentum_analysis = await self._quantum_momentum_detection(market_data)
            
            combined_result = {
                "price": price_analysis,
                "risk": risk_analysis,
                "momentum": momentum_analysis,
                "market_outlook": self._synthesize_outlook(price_analysis, risk_analysis)
            }
            
            execution_time = time.time() - start_time
            result = QuantumSimResult(
                circuit_type=CircuitType.MARKET_SIMULATION,
                output_data=combined_result,
                confidence=0.85 + (random.random() * 0.1),
                execution_time=execution_time,
                qubits_used=CIRCUIT_CONFIGS[CircuitType.MARKET_SIMULATION]["qubits"],
                quantum_advantage=self._calculate_quantum_advantage(execution_time),
                timestamp=datetime.now()
            )
            
            self.results_history.append(result)
            if len(self.results_history) > 50:
                self.results_history.pop(0)
            
            return result
            
        except Exception as error:
            print(f"Quantum Analysis Failed: {error}")
            raise error
    
    async def predict_price_quantum(self, symbol: str, history: List[float]) -> QuantumSimResult:
        """Predição de preço usando circuitos quânticos"""
        self._update_agi_parameters()
        start_time = time.time()
        
        prediction_data = await self._prepare_quantum_price_data(history)
        prediction_result = await self._execute_price_prediction_circuit(prediction_data)
        
        execution_time = time.time() - start_time
        
        result = QuantumSimResult(
            circuit_type=CircuitType.PRICE_PREDICTION,
            output_data={**prediction_result, "symbol": symbol},
            confidence=prediction_result["prediction_confidence"],
            execution_time=execution_time,
            qubits_used=CIRCUIT_CONFIGS[CircuitType.PRICE_PREDICTION]["qubits"],
            quantum_advantage=self._calculate_quantum_advantage(execution_time),
            timestamp=datetime.now()
        )
        
        self.results_history.append(result)
        return result
    
    async def detect_arbitrage_opportunities(self, market_data: Dict[str, Any]) -> List[QuantumSimOpportunity]:
        """Detecta oportunidades de arbitragem quântica"""
        analysis = await self.analyze_market_quantum(market_data)
        opportunities: List[QuantumSimOpportunity] = []
        
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'XRP/USDT']
        
        for symbol in symbols:
            if random.random() > 0.7:  # 30% chance of opportunity
                current_price = market_data.get("current_price", random.uniform(40000, 60000))
                predicted = current_price * (1 + (random.random() - 0.5) * 0.02)
                discrepancy = abs(predicted - current_price) / current_price
                
                if discrepancy > 0.005:  # 0.5% threshold
                    action = "BUY" if predicted > current_price else "SELL"
                    risk_level = RiskLevel.HIGH if discrepancy > 0.02 else RiskLevel.LOW
                    
                    opportunity = QuantumSimOpportunity(
                        id=f"QOPP-{int(time.time())}-{random.randint(1000, 9999)}",
                        symbol=symbol,
                        current_price=current_price,
                        predicted_price=predicted,
                        discrepancy=discrepancy,
                        confidence=analysis.confidence,
                        quantum_certainty=0.9 + (random.random() * 0.09),
                        time_horizon=TimeHorizon.SHORT,
                        risk_level=risk_level,
                        action=action,
                        timestamp=datetime.now()
                    )
                    opportunities.append(opportunity)
        
        return opportunities
    
    # --- INTERNAL SIMULATION LOGIC ---
    
    async def _quantum_price_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simula análise de preço por colapso de função de onda"""
        await asyncio.sleep(0.1)  # Processing time
        
        current_price = data.get("current_price", 100)
        volatility = data.get("volatility", 0.02)
        
        superposition = self._create_price_superposition(current_price, volatility)
        
        return {
            "estimated_price": superposition["expected_value"],
            "distribution": superposition["distribution"],
            "quantum_volatility": superposition["volatility"],
            "confidence_interval": superposition["confidence_interval"]
        }
    
    async def _quantum_risk_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Avaliação de risco quântica"""
        await asyncio.sleep(0.08)
        
        # Simulate correlation matrix
        size = 4
        correlation_matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == j:
                    row.append(1.0)
                else:
                    row.append(random.uniform(-0.5, 0.5))
            correlation_matrix.append(row)
        
        return {
            "quantum_var": random.random() * 0.05,
            "entanglement_correlation": correlation_matrix,
            "risk_state": "STABLE" if random.random() > 0.5 else "UNSTABLE"
        }
    
    async def _quantum_momentum_detection(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Detecção de momentum quântica"""
        await asyncio.sleep(0.06)
        
        wave_patterns = [
            "CONSTRUCTIVE_INTERFERENCE",
            "DESTRUCTIVE_INTERFERENCE",
            "QUANTUM_TUNNELING",
            "COHERENT_OSCILLATION"
        ]
        
        return {
            "momentum_vector": random.uniform(-0.5, 0.5),
            "phase_transition": random.random() > 0.8,
            "wave_pattern": random.choice(wave_patterns)
        }
    
    def _create_price_superposition(self, base_price: float, volatility: float) -> Dict[str, Any]:
        """Cria superposição quântica de preços"""
        states = 1000
        distribution = []
        
        for _ in range(states):
            distribution.append(gaussian_random(base_price, base_price * volatility))
        
        distribution.sort()
        expected_value = np.mean(distribution)
        
        # Calculate 5th and 95th percentiles
        lower_bound = np.percentile(distribution, 5)
        upper_bound = np.percentile(distribution, 95)
        
        # Sample for UI (every 10th value)
        sampled_distribution = distribution[::10]
        
        return {
            "expected_value": expected_value,
            "distribution": sampled_distribution,
            "volatility": volatility * (1 + (random.random() * 0.1)),
            "confidence_interval": [float(lower_bound), float(upper_bound)]
        }
    
    async def _prepare_quantum_price_data(self, history: List[float]) -> Dict[str, float]:
        """Prepara dados para análise quântica"""
        if not history or len(history) == 0:
            return {"current_price": 100, "volatility": 0.02}
        
        returns = []
        for i in range(1, len(history)):
            returns.append((history[i] - history[i-1]) / history[i-1])
        
        if len(returns) == 0:
            return {"current_price": history[-1], "volatility": 0.02}
        
        # Calculate volatility (standard deviation)
        mean_return = np.mean(returns)
        variance = np.mean([(r - mean_return) ** 2 for r in returns])
        
        return {
            "current_price": history[-1],
            "volatility": np.sqrt(variance)
        }
    
    async def _execute_price_prediction_circuit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa circuito quântico de predição de preços"""
        await asyncio.sleep(0.15)
        algo = await self._quantum_price_analysis(data)
        
        return {
            "predicted_price": algo["estimated_price"],
            "prediction_confidence": 0.7 + (random.random() * 0.25),
            "price_range": algo["confidence_interval"],
            "horizon": "MEDIUM"
        }
    
    def _calculate_quantum_advantage(self, exec_time: float) -> float:
        """Calcula vantagem quântica sobre computação clássica"""
        # Simulate classical time being much slower
        classical_time = exec_time * (10 + random.random() * 90)
        return min(1000, classical_time / exec_time)
    
    def _synthesize_outlook(self, price: Dict[str, Any], risk: Dict[str, Any]) -> str:
        """Sintetiza perspectiva de mercado"""
        if risk.get("risk_state") == "UNSTABLE":
            return "ALTA VOLATILIDADE - RISCO DE COLAPSO"
        
        if price.get("estimated_price", 0) > 100:  # Mock logic
            return "TENDÊNCIA DE ALTA (INTERFERÊNCIA CONSTRUTIVA)"
        
        return "NEUTRO - SUPERPOSIÇÃO EQUILIBRADA"
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do simulador"""
        if not self.results_history:
            avg_advantage = 0
        else:
            avg_advantage = sum(r.quantum_advantage for r in self.results_history) / len(self.results_history)
        
        return {
            "active_circuits": len(self.active_circuits),
            "total_executions": len(self.results_history),
            "system_fidelity": self.config["simulation_fidelity"],
            "avg_advantage": avg_advantage,
            "quantum_bits": self.quantum_bits,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_circuit_info(self, circuit_type: CircuitType) -> Dict[str, Any]:
        """Retorna informações sobre um tipo de circuito"""
        config = CIRCUIT_CONFIGS.get(circuit_type, {})
        return {
            "type": circuit_type.value,
            "qubits": config.get("qubits", 0),
            "depth": config.get("depth", 0),
            "gates": config.get("gates", []),
            "description": config.get("description", ""),
            "fidelity": self.config["simulation_fidelity"]
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance"""
        if not self.results_history:
            return {"error": "No executions yet"}
        
        exec_times = [r.execution_time for r in self.results_history]
        confidences = [r.confidence for r in self.results_history]
        
        return {
            "avg_execution_time": np.mean(exec_times),
            "max_execution_time": max(exec_times),
            "min_execution_time": min(exec_times),
            "avg_confidence": np.mean(confidences),
            "total_executions": len(self.results_history),
            "circuits_used": list(set(r.circuit_type.value for r in self.results_history))
        }

# --- INSTANCE ---
market_simulator = QuantumMarketSimulator()

# --- EXAMPLE USAGE ---
async def example_usage():
    """Exemplo de uso do simulador quântico"""
    print("=== Exemplo de Uso do Simulador Quântico ===\n")
    
    # 1. Criar dados de mercado simulados
    market_data = {
        "current_price": 45000.0,
        "volatility": 0.023,
        "volume": 1500000000,
        "symbol": "BTC/USDT"
    }
    
    # 2. Análise quântica completa
    print("1. Executando análise quântica do mercado...")
    analysis = await market_simulator.analyze_market_quantum(market_data)
    print(f"   ✓ Análise concluída em {analysis.execution_time:.3f}s")
    print(f"   ✓ Confiança: {analysis.confidence:.2%}")
    print(f"   ✓ Vantagem Quântica: {analysis.quantum_advantage:.1f}x\n")
    
    # 3. Predição de preço
    print("2. Predição quântica de preço...")
    price_history = [42000, 42500, 43000, 43500, 44000, 44500, 45000]
    prediction = await market_simulator.predict_price_quantum("BTC/USDT", price_history)
    predicted_price = prediction.output_data.get("predicted_price", 0)
    print(f"   ✓ Preço atual: {market_data['current_price']:.2f}")
    print(f"   ✓ Preço previsto: {predicted_price:.2f}")
    print(f"   ✓ Intervalo de confiança: {prediction.output_data.get('price_range', [0, 0])}\n")
    
    # 4. Detectar oportunidades de arbitragem
    print("3. Detectando oportunidades de arbitragem...")
    opportunities = await market_simulator.detect_arbitrage_opportunities(market_data)
    print(f"   ✓ {len(opportunities)} oportunidades detectadas")
    
    for opp in opportunities[:2]:  # Show first 2
        print(f"   • {opp.symbol}: {opp.action} (Discrepância: {opp.discrepancy:.2%})")
    
    # 5. Status do sistema
    print("\n4. Status do Simulador:")
    status = market_simulator.get_status()
    for key, value in status.items():
        print(f"   • {key}: {value}")
    
    return analysis, prediction, opportunities

# --- STREAMLIT INTERFACE ---
def create_streamlit_interface():
    """Cria interface Streamlit para o simulador quântico"""
    import streamlit as st
    
    st.set_page_config(
        page_title="Simulador Quântico de Mercado",
        page_icon="⚛️",
        layout="wide"
    )
    
    st.title("⚛️ Simulador Quântico de Mercado")
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Controles Quânticos")
        
        qubits = st.slider("Qubits Disponíveis", 256, 4096, 1024, 256)
        fidelity = st.slider("Fidelidade da Simulação", 0.8, 1.0, 0.95, 0.01)
        
        st.markdown("---")
        st.header("📊 Parâmetros de Mercado")
        
        current_price = st.number_input("Preço Atual (BTC/USDT)", 10000.0, 100000.0, 45000.0, 1000.0)
        volatility = st.slider("Volatilidade", 0.001, 0.1, 0.023, 0.001)
        
        if st.button("🔄 Reconfigurar Simulador", use_container_width=True):
            # Reinitialize with new settings
            global market_simulator
            market_simulator = QuantumMarketSimulator(qubits)
            market_simulator.config["simulation_fidelity"] = fidelity
    
    # Main interface
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Qubits Ativos", market_simulator.quantum_bits)
    
    with col2:
        status = market_simulator.get_status()
        st.metric("Vantagem Quântica Média", f"{status['avg_advantage']:.1f}x")
    
    with col3:
        st.metric("Execuções Totais", status["total_executions"])
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Análise de Mercado", 
        "🎯 Predição de Preço", 
        "💰 Arbitragem", 
        "📊 Estatísticas"
    ])
    
    with tab1:
        st.header("Análise Quântica do Mercado")
        
        if st.button("⚡ Executar Análise Completa", type="primary"):
            with st.spinner("Executando análise quântica..."):
                market_data = {
                    "current_price": current_price,
                    "volatility": volatility,
                    "symbol": "BTC/USDT"
                }
                
                # Run async function in sync context
                import asyncio
                
                async def run_analysis():
                    return await market_simulator.analyze_market_quantum(market_data)
                
                analysis = asyncio.run(run_analysis())
                
                st.success(f"Análise concluída em {analysis.execution_time:.3f}s")
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Resultados da Análise")
                    st.metric("Confiança", f"{analysis.confidence:.2%}")
                    st.metric("Vantagem Quântica", f"{analysis.quantum_advantage:.1f}x")
                    
                    outlook = analysis.output_data.get("market_outlook", "N/A")
                    st.markdown(f"**Perspectiva:** {outlook}")
                
                with col2:
                    st.subheader("📈 Dados de Preço")
                    price_data = analysis.output_data.get("price", {})
                    if price_data:
                        st.metric("Preço Estimado", f"${price_data.get('estimated_price', 0):.2f}")
                        st.metric("Volatilidade Quântica", f"{price_data.get('quantum_volatility', 0):.4f}")
                        
                        # Show confidence interval
                        ci = price_data.get("confidence_interval", [0, 0])
                        st.markdown(f"**Intervalo de Confiança 90%:** ${ci[0]:.2f} - ${ci[1]:.2f}")
    
    with tab2:
        st.header("Predição Quântica de Preço")
        
        # Generate sample price history
        base_price = current_price
        history = []
        for i in range(20):
            change = random.uniform(-0.02, 0.02)
            history.append(base_price * (1 + change))
            base_price = history[-1]
        
        st.line_chart(pd.DataFrame({"Preço": history}))
        
        if st.button("🔮 Executar Predição Quântica", type="primary"):
            with st.spinner("Executando circuito quântico de predição..."):
                
                async def run_prediction():
                    return await market_simulator.predict_price_quantum("BTC/USDT", history)
                
                prediction = asyncio.run(run_prediction())
                
                st.success(f"Predição concluída em {prediction.execution_time:.3f}s")
                
                # Display prediction
                pred_data = prediction.output_data
                current = history[-1] if history else current_price
                predicted = pred_data.get("predicted_price", current)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Preço Atual", f"${current:.2f}")
                    st.metric("Preço Previsto", f"${predicted:.2f}")
                    
                    change_pct = ((predicted - current) / current) * 100
                    st.metric("Mudança Prevista", f"{change_pct:.2f}%")
                
                with col2:
                    st.metric("Confiança da Predição", f"{prediction.confidence:.2%}")
                    st.metric("Qubits Utilizados", prediction.qubits_used)
                    
                    horizon = pred_data.get("horizon", "N/A")
                    st.markdown(f"**Horizonte:** {horizon}")
    
    with tab3:
        st.header("Detecção de Arbitragem Quântica")
        
        if st.button("🔍 Scan por Oportunidades", type="primary"):
            with st.spinner("Executando detecção quântica de arbitragem..."):
                market_data = {
                    "current_price": current_price,
                    "volatility": volatility
                }
                
                async def run_arbitrage():
                    return await market_simulator.detect_arbitrage_opportunities(market_data)
                
                opportunities = asyncio.run(run_arbitrage())
                
                if opportunities:
                    st.success(f"{len(opportunities)} oportunidades detectadas!")
                    
                    # Display opportunities
                    for opp in opportunities:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                action_color = "green" if opp.action == "BUY" else "red"
                                st.markdown(f"### {opp.symbol}")
                                st.markdown(f"**Ação:** :{action_color}[{opp.action}]")
                            
                            with col2:
                                st.metric("Preço Atual", f"${opp.current_price:.2f}")
                                st.metric("Preço Previsto", f"${opp.predicted_price:.2f}")
                            
                            with col3:
                                st.metric("Discrepância", f"{opp.discrepancy:.2%}")
                                certainty_color = "🟢" if opp.quantum_certainty > 0.95 else "🟡"
                                st.markdown(f"**Certeza Quântica:** {certainty_color} {opp.quantum_certainty:.2%}")
                            
                            st.markdown("---")
                else:
                    st.info("Nenhuma oportunidade de arbitragem detectada no momento.")
    
    with tab4:
        st.header("Estatísticas do Simulador")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Status do Sistema")
            status = market_simulator.get_status()
            for key, value in status.items():
                if key != "last_update":
                    st.metric(key.replace("_", " ").title(), value)
                else:
                    st.caption(f"Última atualização: {value}")
        
        with col2:
            st.subheader("🎯 Performance")
            perf_stats = market_simulator.get_performance_stats()
            if "error" not in perf_stats:
                for key, value in perf_stats.items():
                    if isinstance(value, list):
                        st.markdown(f"**{key.replace('_', ' ').title()}:** {', '.join(value)}")
                    else:
                        st.metric(key.replace("_", " ").title(), 
                                 f"{value:.3f}" if isinstance(value, float) else value)
        
        # Circuit information
        st.subheader("⚡ Circuitos Quânticos")
        circuits = st.selectbox(
            "Selecione um circuito",
            list(CIRCUIT_CONFIGS.keys()),
            format_func=lambda x: x.value
        )
        
        circuit_info = market_simulator.get_circuit_info(circuits)
        cols = st.columns(4)
        
        with cols[0]:
            st.metric("Qubits", circuit_info["qubits"])
        
        with cols[1]:
            st.metric("Profundidade", circuit_info["depth"])
        
        with cols[2]:
            st.metric("Fidelidade", f"{circuit_info['fidelity']:.3f}")
        
        with cols[3]:
            st.markdown(f"**Portas:** {', '.join(circuit_info['gates'])}")
        
        st.markdown(f"**Descrição:** {circuit_info['description']}")

if __name__ == "__main__":
    # Run example usage
    import asyncio
    asyncio.run(example_usage())
    
    # To run Streamlit interface:
    # streamlit run quantum_simulator.py
    # Uncomment the line below to run the Streamlit interface
    # create_streamlit_interface()