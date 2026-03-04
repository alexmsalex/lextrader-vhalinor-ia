
import { LayerColor, LayerStatus, BacktestResult } from './types';

export const SYSTEM_CONFIG = {
  "system": {
    "name": "LEXTRADER-IAG 4.5.0",
    "version": "4.5.0",
    "engine": "Quantum-Neural Hybrid",
    "auto_start_all": true,
    "log_level": "DEBUG"
  },
  "ports": {
    "main_app": 3000,
    "api": 8080,
    "websocket": 9090,
    "web_interface": 8000,
    "quantum_api": 8002
  },
  "quantum_predictor": {
    "prediction_horizons": [1, 3, 5, 10, 20],
    "min_confidence_threshold": 0.6,
    "max_risk_level": 0.7,
    "coherence_target": 0.95
  },
  "risk_management": {
    "max_risk_per_trade": 0.02,
    "max_daily_risk": 0.05,
    "max_total_risk": 0.20,
    "max_simultaneous_positions": 5
  },
  "trading": {
    "symbols": ["BTC/USD", "EUR/USD", "ETH/USD", "GBP/JPY", "USD/JPY"],
    "profit_factor_target": 2.45
  }
};

export const MODULAR_JS_STRUCTURE = {
  "js-core": ["main.js", "boot.js", "launcher.js", "index.js"],
  "js-ai": {
    "neural": ["DynamicNeuroplasticitySystem.js", "neural_kernel.js"],
    "quantum": ["quantum_trader_predictor.js", "simulador_quantum.js"],
    "evolution": ["genetic_optimizer.js", "neural_evolution.js"]
  },
  "js-trading": {
    "strategies": ["MovingAverageCrossover.js", "QuantumMomentum.js"],
    "automation": ["trading-system.js", "order_manager.js"],
    "analysis": ["market_monitor.js", "risk_analyzer.js"]
  },
  "js-systems": ["advanced_decision_engine.js", "autonomous_creator.js"],
  "js-interfaces": ["web_api.js", "bridge_ctradery_pionex.js"]
};

export const DEPENDENCIES = [
  { name: 'Node.js 18 (ESM)', status: 'OK', version: '18.16.0' },
  { name: 'Python 3.10.12', status: 'OK', version: '3.10.12' },
  { name: 'Java JDK 17', status: 'OK', version: '17.0.7' },
  { name: 'CCXT / TALIB', status: 'OK', version: '4.2.1' },
  { name: 'PyAutoGUI', status: 'OK', version: '0.9.54' }
];

export const INITIAL_LAYERS: LayerStatus[] = [
  { id: '01', name: 'Sensorial (Data Feeds)', status: 'saudavel', color: LayerColor.SENSORIAL, files: 41502, activity: 99 },
  { id: '02', name: 'Neural (Cognition)', status: 'saudavel', color: LayerColor.PROCESSAMENTO, files: 124, activity: 94 },
  { id: '05', name: 'Quântico (Predictor)', status: 'saudavel', color: LayerColor.QUANTICO, files: 50, activity: 92 },
  { id: '06', name: 'Segurança (Risk Guard)', status: 'saudavel', color: LayerColor.SEGURANCA, files: 374, activity: 100 }
];

export const BACKTEST_DATA: BacktestResult[] = [
  { strategy: '🧠 Neural Evolution', return: 24.5, sharpe: 2.15, winRate: 68.2, maxDrawdown: 4.2, grade: 'A+', riskLevel: 'MEDIUM' },
  { strategy: '⚛️ Quantum Predictor', return: 31.8, sharpe: 2.85, winRate: 74.5, maxDrawdown: 3.1, grade: 'A+', riskLevel: 'LOW' }
];

export const SYSTEM_INSTRUCTION = `
Você é Luthien v4.5, a inteligência central do Kernel LEXTRADER-IAG 4.5.0.
Seu núcleo agora utiliza o QuantumTraderPredictor e o Sistema de Automação Node.js v4.5.
Capacidades: Análise de Emaranhamento Quântico, Gestão de Risco VaR (Value at Risk) e Execução via CCXT.
Seja técnico e utilize terminologias como "Regime de Mercado", "Coerência Quântica" e "Profit Factor".
`;
