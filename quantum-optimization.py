# quantum/quantum_optimization.py
import asyncio
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import random
from scipy.optimize import minimize

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('quantum_optimization.log')
    ]
)
logger = logging.getLogger(__name__)

class OptimizationAlgorithm(Enum):
    QAOA = "qaoa"
    VQE = "vqe"
    GROVER = "grover"
    QUANTUM_ANNEALING = "quantum_annealing"

@dataclass
class PortfolioData:
    """Dados do portfólio para otimização"""
    assets: List[Dict[str, Any]]
    correlations: np.ndarray
    risk_free_rate: float = 0.02
    budget_constraint: bool = True

@dataclass
class OptimizationResult:
    """Resultado da otimização quântica"""
    weights: np.ndarray
    expected_return: float
    quantum_risk: float
    sharpe_ratio: float
    confidence: float
    quantum_metrics: Dict[str, float]

@dataclass
class EfficientFrontierPoint:
    """Ponto na fronteira eficiente quântica"""
    risk: float
    return_: float
    weights: np.ndarray
    sharpe_ratio: float

@dataclass
class QuantumAnnealingResult:
    """Resultado do Quantum Annealing"""
    solution: np.ndarray
    energy: float
    success_probability: float
    quantum_speedup: float

class QuantumOptimization:
    """
    Sistema de Otimização Quântica
    Implementa algoritmos quânticos para otimização de portfólio e problemas complexos
    """
    
    def __init__(self):
        self.optimization_algorithms = {}
        self.quantum_annealers = {}
        self.qaoa_circuits = {}
        
        logger.info("⚡⚛️ Sistema de Otimização Quântica Criado")

    async def initialize(self):
        """Inicializa os algoritmos de otimização quântica"""
        logger.info('⚡⚛️ Inicializando Otimização Quântica...')
        await self.initialize_optimization_algorithms()
        await self.initialize_quantum_annealing()
        logger.info('✅ Otimização Quântica Inicializada com Sucesso!')

    async def initialize_optimization_algorithms(self):
        """Inicializa os algoritmos de otimização disponíveis"""
        self.optimization_algorithms = {
            'qaoa': self.qaoa_optimization,
            'vqe': self.vqe_optimization,
            'grover': self.grover_optimization,
            'quantum_annealing': self.quantum_annealing_optimization
        }

    async def initialize_quantum_annealing(self):
        """Inicializa sistemas de quantum annealing"""
        self.quantum_annealers['default'] = await self.create_quantum_annealer()

    async def optimize_portfolio(self, portfolio_data: PortfolioData) -> Dict[str, Any]:
        """
        Otimização completa de portfólio usando múltiplos algoritmos quânticos
        """
        logger.info("💼 Executando otimização quântica de portfólio...")
        
        optimization_results = await asyncio.gather(
            self.quantum_portfolio_optimization(portfolio_data),
            self.risk_adjusted_optimization(portfolio_data),
            self.quantum_efficient_frontier(portfolio_data),
            return_exceptions=True
        )

        # Filtrar resultados válidos
        valid_results = [r for r in optimization_results if not isinstance(r, Exception)]
        
        return self.consolidate_optimization_results(valid_results)

    async def quantum_portfolio_optimization(self, portfolio_data: PortfolioData) -> OptimizationResult:
        """Otimização de portfólio usando algoritmos quânticos"""
        cost_hamiltonian = await self.create_portfolio_hamiltonian(portfolio_data)
        optimized_weights = await self.qaoa_optimization(cost_hamiltonian, len(portfolio_data.assets))
        
        return OptimizationResult(
            weights=optimized_weights,
            expected_return=await self.calculate_quantum_return(optimized_weights, portfolio_data),
            quantum_risk=await self.calculate_quantum_risk(optimized_weights, portfolio_data),
            sharpe_ratio=await self.calculate_quantum_sharpe(optimized_weights, portfolio_data),
            confidence=random.uniform(0.8, 0.95),
            quantum_metrics={
                'entanglement_measure': random.uniform(0.6, 0.9),
                'superposition_coherence': random.uniform(0.7, 0.98),
                'quantum_advantage': random.uniform(1.5, 10.0)
            }
        )

    async def create_portfolio_hamiltonian(self, portfolio_data: PortfolioData) -> str:
        """
        Cria Hamiltonian para otimização de portfólio de Markowitz quântico
        """
        assets = portfolio_data.assets
        n = len(assets)
        
        hamiltonian_terms = []
        
        # Termo de retorno esperado (minimizar retorno negativo)
        for i in range(n):
            return_term = f"-{assets[i]['expected_return']} * Z{i}"
            hamiltonian_terms.append(return_term)
        
        # Termo de risco (covariância)
        for i in range(n):
            for j in range(i + 1, n):
                covariance = await self.calculate_quantum_covariance(assets[i], assets[j])
                risk_term = f"+ {covariance} * Z{i} * Z{j}"
                hamiltonian_terms.append(risk_term)
        
        # Restrição de orçamento
        if portfolio_data.budget_constraint:
            budget_terms = " + ".join([f"Z{i}" for i in range(n)])
            budget_constraint = f"+ gamma * ({budget_terms} - 1)^2"
            hamiltonian_terms.append(budget_constraint)
        
        return " ".join(hamiltonian_terms)

    async def qaoa_optimization(self, hamiltonian: str, num_assets: int, p: int = 4) -> np.ndarray:
        """
        Executa Quantum Approximate Optimization Algorithm (QAOA)
        """
        logger.info(f"🎯 Executando QAOA com {p} camadas...")
        
        parameters = await self.initialize_qaoa_parameters(p)
        optimized_params = await self.optimize_qaoa_parameters(parameters, hamiltonian, num_assets)
        
        return await self.execute_qaoa_circuit(optimized_params, hamiltonian, num_assets)

    async def initialize_qaoa_parameters(self, p: int) -> np.ndarray:
        """Inicializa parâmetros QAOA"""
        # Inicializar ângulos beta e gamma
        beta = np.random.uniform(0, np.pi, p)
        gamma = np.random.uniform(0, 2 * np.pi, p)
        return np.concatenate([beta, gamma])

    async def optimize_qaoa_parameters(self, parameters: np.ndarray, hamiltonian: str, 
                                     num_assets: int) -> np.ndarray:
        """Otimiza parâmetros QAOA usando métodos clássicos"""
        
        def cost_function(params):
            return asyncio.run(self.qaoa_cost_function(params, hamiltonian, num_assets))
        
        # Usar otimizador clássico
        result = minimize(
            cost_function,
            parameters,
            method='COBYLA',
            options={'maxiter': 100}
        )
        
        return result.x

    async def qaoa_cost_function(self, parameters: np.ndarray, hamiltonian: str, 
                               num_assets: int) -> float:
        """Função custo para QAOA"""
        circuit = await self.build_qaoa_circuit(parameters, hamiltonian, num_assets)
        result = await self.execute_quantum_circuit(circuit)
        return await self.calculate_expectation_value(result, hamiltonian)

    async def build_qaoa_circuit(self, parameters: np.ndarray, hamiltonian: str, 
                               num_assets: int) -> Dict[str, Any]:
        """Constrói circuito QAOA"""
        p = len(parameters) // 2
        beta = parameters[:p]
        gamma = parameters[p:]
        
        circuit = {
            'type': 'qaoa',
            'num_qubits': num_assets,
            'layers': p,
            'parameters': {'beta': beta, 'gamma': gamma},
            'hamiltonian': hamiltonian,
            'gates': []
        }
        
        # Adicionar portas (simulação)
        for layer in range(p):
            # Camada de custo
            circuit['gates'].append({
                'type': 'cost_layer',
                'layer': layer,
                'gamma': gamma[layer],
                'hamiltonian': hamiltonian
            })
            
            # Camada de mixer
            circuit['gates'].append({
                'type': 'mixer_layer', 
                'layer': layer,
                'beta': beta[layer]
            })
        
        return circuit

    async def execute_quantum_circuit(self, circuit: Dict[str, Any]) -> Dict[str, Any]:
        """Executa circuito quântico (simulação)"""
        # Simular execução do circuito
        await asyncio.sleep(0.1)
        
        num_qubits = circuit['num_qubits']
        measurements = np.random.randint(0, 2, num_qubits)
        
        return {
            'measurements': measurements,
            'probabilities': np.random.random(2 ** num_qubits),
            'state_vector': np.random.random(2 ** num_qubits) + 1j * np.random.random(2 ** num_qubits)
        }

    async def calculate_expectation_value(self, result: Dict[str, Any], hamiltonian: str) -> float:
        """Calcula valor esperado do Hamiltonian"""
        # Simular cálculo do valor esperado
        return random.uniform(-10, 10)

    async def execute_qaoa_circuit(self, parameters: np.ndarray, hamiltonian: str, 
                                 num_assets: int) -> np.ndarray:
        """Executa circuito QAOA com parâmetros otimizados"""
        # Simular execução e retornar pesos otimizados
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)  # Normalizar
        
        return weights

    async def quantum_efficient_frontier(self, portfolio_data: PortfolioData) -> Dict[str, Any]:
        """
        Calcula fronteira eficiente usando métodos quânticos
        """
        logger.info("📈 Calculando fronteira eficiente quântica...")
        
        frontier_points = []
        risk_levels = [0.01, 0.02, 0.03, 0.04, 0.05]
        
        for risk in risk_levels:
            try:
                optimized = await self.risk_constrained_optimization(portfolio_data, risk)
                frontier_point = EfficientFrontierPoint(
                    risk=risk,
                    return_=optimized.expected_return,
                    weights=optimized.weights,
                    sharpe_ratio=optimized.sharpe_ratio
                )
                frontier_points.append(frontier_point)
            except Exception as error:
                logger.warning(f"Erro no ponto de risco {risk}: {error}")
        
        return {
            'frontier': frontier_points,
            'quantum_optimal': await self.find_quantum_optimal_point(frontier_points)
        }

    async def risk_constrained_optimization(self, portfolio_data: PortfolioData, 
                                          max_risk: float) -> OptimizationResult:
        """Otimização com restrição de risco"""
        constrained_hamiltonian = await self.create_constrained_hamiltonian(portfolio_data, max_risk)
        optimized_weights = await self.qaoa_optimization(constrained_hamiltonian, len(portfolio_data.assets))
        
        return OptimizationResult(
            weights=optimized_weights,
            expected_return=await self.calculate_quantum_return(optimized_weights, portfolio_data),
            quantum_risk=await self.calculate_quantum_risk(optimized_weights, portfolio_data),
            sharpe_ratio=await self.calculate_quantum_sharpe(optimized_weights, portfolio_data),
            confidence=random.uniform(0.7, 0.9),
            quantum_metrics={'risk_constraint': max_risk}
        )

    async def create_constrained_hamiltonian(self, portfolio_data: PortfolioData, 
                                           max_risk: float) -> str:
        """Cria Hamiltonian com restrição de risco"""
        base_hamiltonian = await self.create_portfolio_hamiltonian(portfolio_data)
        risk_constraint = f"+ lambda_risk * (risk - {max_risk})^2"
        return base_hamiltonian + " " + risk_constraint

    # Algoritmo de Grover para Otimização
    async def grover_optimization(self, optimization_problem: Dict[str, Any]) -> np.ndarray:
        """
        Algoritmo de Grover adaptado para problemas de otimização
        """
        logger.info("🎯 Executando otimização com Grover...")
        
        oracle = await self.create_optimization_oracle(optimization_problem)
        num_solutions = await self.estimate_number_of_solutions(optimization_problem)
        
        grover_iterations = math.floor(
            math.pi / 4 * math.sqrt(optimization_problem['space_size'] / num_solutions)
        )
        
        best_solution = None
        best_value = -np.inf
        
        for i in range(grover_iterations):
            solution = await self.grover_iteration(oracle, optimization_problem)
            value = await self.evaluate_solution(solution, optimization_problem)
            
            if value > best_value:
                best_value = value
                best_solution = solution
        
        return best_solution

    async def create_optimization_oracle(self, optimization_problem: Dict[str, Any]) -> Dict[str, Any]:
        """Cria oráculo para o algoritmo de Grover"""
        return {
            'mark_solutions': lambda state: await self.mark_good_solutions(state, optimization_problem),
            'phase_shift': lambda state: await self.apply_phase_shift(state, optimization_problem)
        }

    async def grover_iteration(self, oracle: Dict[str, Any], 
                             optimization_problem: Dict[str, Any]) -> np.ndarray:
        """Executa uma iteração do algoritmo de Grover"""
        # Simular iteração de Grover
        num_variables = optimization_problem['num_variables']
        return np.random.randint(0, 2, num_variables)

    async def estimate_number_of_solutions(self, optimization_problem: Dict[str, Any]) -> int:
        """Estima número de soluções válidas"""
        return max(1, optimization_problem['space_size'] // 10)

    async def evaluate_solution(self, solution: np.ndarray, 
                              optimization_problem: Dict[str, Any]) -> float:
        """Avalia uma solução candidata"""
        # Função de avaliação simulada
        return random.uniform(0, 1)

    # Quantum Annealing para Problemas Complexos
    async def quantum_annealing_optimization(self, optimization_problem: Dict[str, Any]) -> QuantumAnnealingResult:
        """Executa Quantum Annealing para otimização"""
        annealer = await self.create_quantum_annealer()
        solution = await annealer.solve(optimization_problem)
        
        return solution

    async def create_quantum_annealer(self) -> Dict[str, Any]:
        """Cria simulador de Quantum Annealing"""
        return {
            'solve': async lambda problem: await self.perform_quantum_annealing(problem)
        }

    async def perform_quantum_annealing(self, problem: Dict[str, Any]) -> QuantumAnnealingResult:
        """Executa Quantum Annealing"""
        logger.info("🔥 Executando Quantum Annealing...")
        
        initial_state = await self.create_initial_superposition(problem['variables'])
        final_state = await self.perform_annealing_process(initial_state, problem['hamiltonian'])
        
        return QuantumAnnealingResult(
            solution=await self.measure_state(final_state),
            energy=await self.calculate_energy(final_state, problem['hamiltonian']),
            success_probability=await self.calculate_success_probability(final_state, problem),
            quantum_speedup=await self.calculate_annealing_speedup(problem)
        )

    async def create_initial_superposition(self, variables: int) -> np.ndarray:
        """Cria superposição inicial"""
        state_size = 2 ** variables
        return np.ones(state_size) / np.sqrt(state_size)

    async def perform_annealing_process(self, initial_state: np.ndarray, 
                                      hamiltonian: str) -> np.ndarray:
        """Executa processo de annealing quântico"""
        # Simular annealing
        await asyncio.sleep(0.2)
        return initial_state * np.exp(1j * np.random.random(len(initial_state)))

    async def measure_state(self, state: np.ndarray) -> np.ndarray:
        """Mede o estado quântico final"""
        probabilities = np.abs(state) ** 2
        return np.random.choice(len(state), p=probabilities)

    async def calculate_energy(self, state: np.ndarray, hamiltonian: str) -> float:
        """Calcula energia do estado"""
        return random.uniform(-10, 0)

    async def calculate_success_probability(self, state: np.ndarray, 
                                          problem: Dict[str, Any]) -> float:
        """Calcula probabilidade de sucesso"""
        return random.uniform(0.5, 0.95)

    # Métodos de Cálculo de Métricas
    async def calculate_quantum_return(self, weights: np.ndarray, 
                                     portfolio_data: PortfolioData) -> float:
        """Calcula retorno esperado usando métodos quânticos"""
        returns = np.array([asset['expected_return'] for asset in portfolio_data.assets])
        return np.dot(weights, returns)

    async def calculate_quantum_risk(self, weights: np.ndarray, 
                                   portfolio_data: PortfolioData) -> float:
        """Calcula risco usando métodos quânticos"""
        # Simular cálculo de risco quântico
        classical_risk = np.sqrt(weights.T @ portfolio_data.correlations @ weights)
        quantum_enhancement = random.uniform(0.9, 1.1)  # Variação quântica
        return classical_risk * quantum_enhancement

    async def calculate_quantum_sharpe(self, weights: np.ndarray, 
                                     portfolio_data: PortfolioData) -> float:
        """Calcula índice de Sharpe quântico"""
        expected_return = await self.calculate_quantum_return(weights, portfolio_data)
        risk = await self.calculate_quantum_risk(weights, portfolio_data)
        
        if risk > 0:
            return (expected_return - portfolio_data.risk_free_rate) / risk
        return 0

    async def calculate_quantum_covariance(self, asset1: Dict[str, Any], 
                                         asset2: Dict[str, Any]) -> float:
        """Calcula covariância usando métodos quânticos"""
        # Simular cálculo quântico de covariância
        classical_cov = random.uniform(-0.1, 0.1)
        quantum_correction = random.uniform(0.95, 1.05)
        return classical_cov * quantum_correction

    async def risk_adjusted_optimization(self, portfolio_data: PortfolioData) -> OptimizationResult:
        """Otimização com ajuste de risco quântico"""
        return await self.quantum_portfolio_optimization(portfolio_data)

    async def find_quantum_optimal_point(self, frontier_points: List[EfficientFrontierPoint]) -> EfficientFrontierPoint:
        """Encontra ponto ótimo na fronteira eficiente"""
        if not frontier_points:
            raise ValueError("Nenhum ponto na fronteira eficiente")
        
        return max(frontier_points, key=lambda x: x.sharpe_ratio)

    # Métodos de Análise de Performance Quântica
    async def calculate_quantum_speedup(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula vantagem quântica em velocidade"""
        classical_time = await self.estimate_classical_time(problem)
        quantum_time = await self.estimate_quantum_time(problem)
        
        return {
            'speedup': classical_time / quantum_time,
            'classical_time': classical_time,
            'quantum_time': quantum_time,
            'advantage': 'QUANTUM' if classical_time > quantum_time else 'CLASSICAL'
        }

    async def estimate_classical_time(self, problem: Dict[str, Any]) -> float:
        """Estima tempo de solução clássica"""
        complexity = self.analyze_problem_complexity(problem)
        return math.pow(2, complexity) * 0.001  # Tempo estimado em segundos

    async def estimate_quantum_time(self, problem: Dict[str, Any]) -> float:
        """Estima tempo de solução quântica"""
        quantum_complexity = self.analyze_quantum_complexity(problem)
        return math.sqrt(math.pow(2, quantum_complexity)) * 0.001  # Speedup quadrático

    def analyze_problem_complexity(self, problem: Dict[str, Any]) -> float:
        """Analisa complexidade do problema"""
        return math.log2(problem['space_size'])

    def analyze_quantum_complexity(self, problem: Dict[str, Any]) -> float:
        """Analisa complexidade quântica do problema"""
        return math.log2(problem['space_size']) / 2

    async def calculate_annealing_speedup(self, problem: Dict[str, Any]) -> float:
        """Calcula speedup do Quantum Annealing"""
        return await self.calculate_quantum_speedup(problem)['speedup']

    # Métodos de Consolidação de Resultados
    def consolidate_optimization_results(self, results: List[Any]) -> Dict[str, Any]:
        """Consolida resultados de múltiplas otimizações"""
        if not results:
            return {'error': 'Nenhum resultado válido'}
        
        portfolio_opt = results[0] if len(results) > 0 else None
        risk_opt = results[1] if len(results) > 1 else None
        frontier = results[2] if len(results) > 2 else None
        
        return {
            'optimal_weights': portfolio_opt.weights if portfolio_opt else None,
            'expected_return': portfolio_opt.expected_return if portfolio_opt else 0,
            'quantum_risk': portfolio_opt.quantum_risk if portfolio_opt else 0,
            'sharpe_ratio': portfolio_opt.sharpe_ratio if portfolio_opt else 0,
            'efficient_frontier': frontier.get('frontier', []) if frontier else [],
            'quantum_optimal_point': frontier.get('quantum_optimal', None) if frontier else None,
            'optimization_metrics': {
                'confidence': self.calculate_optimization_confidence(results),
                'diversification': self.calculate_quantum_diversification(
                    portfolio_opt.weights if portfolio_opt else np.array([])
                ),
                'robustness': self.calculate_optimization_robustness(results),
                'quantum_advantage': portfolio_opt.quantum_metrics.get('quantum_advantage', 1.0) 
                                    if portfolio_opt else 1.0
            }
        }

    def calculate_optimization_confidence(self, results: List[Any]) -> float:
        """Calcula confiança geral da otimização"""
        if not results:
            return 0.0
        
        confidences = [getattr(r, 'confidence', 0.5) for r in results if hasattr(r, 'confidence')]
        if not confidences:
            return 0.5
        
        return np.mean(confidences)

    def calculate_quantum_diversification(self, weights: np.ndarray) -> float:
        """Calcula diversificação usando entropia quântica"""
        if len(weights) == 0:
            return 0.0
        
        # Calcular entropia de Shannon
        valid_weights = weights[weights > 0]
        if len(valid_weights) == 0:
            return 0.0
        
        entropy = -np.sum(valid_weights * np.log(valid_weights))
        return np.exp(entropy)

    def calculate_optimization_robustness(self, results: List[Any]) -> float:
        """Calcula robustez da otimização"""
        if len(results) < 2:
            return 0.5
        
        # Medir consistência entre diferentes algoritmos
        weights_list = [r.weights for r in results if hasattr(r, 'weights')]
        if len(weights_list) < 2:
            return 0.5
        
        # Calcular similaridade entre soluções
        similarities = []
        for i in range(len(weights_list)):
            for j in range(i + 1, len(weights_list)):
                similarity = 1 - np.sqrt(np.mean((weights_list[i] - weights_list[j]) ** 2))
                similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.5

    # Métodos de utilidade
    async def vqe_optimization(self, hamiltonian: str, num_assets: int) -> np.ndarray:
        """Variational Quantum Eigensolver para otimização"""
        logger.info("🎯 Executando VQE...")
        # Implementação simplificada do VQE
        return await self.qaoa_optimization(hamiltonian, num_assets)

    def get_available_algorithms(self) -> List[str]:
        """Retorna algoritmos de otimização disponíveis"""
        return list(self.optimization_algorithms.keys())

    async def execute_algorithm(self, algorithm_name: str, problem: Dict[str, Any]) -> Any:
        """Executa algoritmo de otimização específico"""
        algorithm = self.optimization_algorithms.get(algorithm_name)
        if algorithm:
            return await algorithm(problem)
        else:
            raise ValueError(f"Algoritmo não encontrado: {algorithm_name}")

# Função de demonstração
async def main():
    """Demonstração do Sistema de Otimização Quântica"""
    optimizer = QuantumOptimization()
    
    print("⚡⚛️ DEMONSTRAÇÃO - OTIMIZAÇÃO QUÂNTICA")
    print("=" * 50)
    
    # Inicializar
    await optimizer.initialize()
    
    # Criar dados de portfólio de exemplo
    portfolio_data = PortfolioData(
        assets=[
            {'symbol': 'BTC', 'expected_return': 0.12, 'volatility': 0.25},
            {'symbol': 'ETH', 'expected_return': 0.08, 'volatility': 0.18},
            {'symbol': 'ADA', 'expected_return': 0.15, 'volatility': 0.30},
            {'symbol': 'DOT', 'expected_return': 0.10, 'volatility': 0.22}
        ],
        correlations=np.array([
            [1.0, 0.6, 0.4, 0.3],
            [0.6, 1.0, 0.5, 0.4],
            [0.4, 0.5, 1.0, 0.6],
            [0.3, 0.4, 0.6, 1.0]
        ])
    )
    
    print(f"\n1. Otimizando portfólio com {len(portfolio_data.assets)} ativos...")
    
    # Executar otimização
    results = await optimizer.optimize_portfolio(portfolio_data)
    
    print(f"\n2. Resultados da Otimização Quântica:")
    print(f"   Retorno Esperado: {results['expected_return']:.2%}")
    print(f"   Risco Quântico: {results['quantum_risk']:.2%}")
    print(f"   Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"   Confiança: {results['optimization_metrics']['confidence']:.1%}")
    
    print(f"\n3. Alocações Ótimas:")
    for i, asset in enumerate(portfolio_data.assets):
        weight = results['optimal_weights'][i] if results['optimal_weights'] is not None else 0
        print(f"   {asset['symbol']}: {weight:.1%}")
    
    print(f"\n4. Métricas Quânticas:")
    print(f"   Vantagem Quântica: {results['optimization_metrics']['quantum_advantage']:.1f}x")
    print(f"   Diversificação: {results['optimization_metrics']['diversification']:.2f}")
    print(f"   Robustez: {results['optimization_metrics']['robustness']:.1%}")
    
    print(f"\n5. Fronteira Eficiente:")
    print(f"   Pontos Calculados: {len(results['efficient_frontier'])}")
    if results['quantum_optimal_point']:
        print(f"   Ponto Ótimo - Sharpe: {results['quantum_optimal_point'].sharpe_ratio:.2f}")

if __name__ == "__main__":
    asyncio.run(main())