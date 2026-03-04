/**
 * Advanced Algorithmic Trading System Core
 * Enhanced definitions and enumerations for financial AI systems
 */

export const AlgorithmType = {
  // Primary Algorithm Categories
  ML: {
    code: "ML",
    name: "Machine Learning",
    description: "Traditional machine learning algorithms (SVM, Random Forest, XGBoost)",
    complexity: "MEDIUM",
    latency: "MODERATE",
    accuracy: "HIGH"
  },
  STATISTICAL: {
    code: "STATISTICAL",
    name: "Statistical",
    description: "Statistical models and time series analysis (ARIMA, GARCH, Kalman Filter)",
    complexity: "MEDIUM",
    latency: "LOW",
    accuracy: "MEDIUM"
  },
  HYBRID: {
    code: "HYBRID",
    name: "Hybrid",
    description: "Combination of multiple algorithm types for enhanced performance",
    complexity: "HIGH",
    latency: "MODERATE",
    accuracy: "VERY_HIGH"
  },
  QUANTUM: {
    code: "QUANTUM",
    name: "Quantum",
    description: "Quantum computing inspired algorithms and quantum machine learning",
    complexity: "VERY_HIGH",
    latency: "VARIABLE",
    accuracy: "EXPERIMENTAL"
  },
  ENSEMBLE: {
    code: "ENSEMBLE",
    name: "Ensemble",
    description: "Combination of multiple models with voting or stacking",
    complexity: "HIGH",
    latency: "HIGH",
    accuracy: "VERY_HIGH"
  },
  DEEP_LEARNING: {
    code: "DEEP_LEARNING",
    name: "Deep Learning",
    description: "Neural networks including CNNs, RNNs, LSTMs, and Transformers",
    complexity: "VERY_HIGH",
    latency: "HIGH",
    accuracy: "VERY_HIGH"
  },
  REINFORCEMENT_LEARNING: {
    code: "REINFORCEMENT_LEARNING",
    name: "Reinforcement Learning",
    description: "RL agents learning optimal trading strategies through environment interaction",
    complexity: "VERY_HIGH",
    latency: "HIGH",
    accuracy: "HIGH"
  },
  GENETIC: {
    code: "GENETIC",
    name: "Genetic Algorithms",
    description: "Evolutionary computing for strategy optimization",
    complexity: "HIGH",
    latency: "HIGH",
    accuracy: "MEDIUM_HIGH"
  },
  FUZZY_LOGIC: {
    code: "FUZZY_LOGIC",
    name: "Fuzzy Logic",
    description: "Fuzzy inference systems for uncertain market conditions",
    complexity: "MEDIUM",
    latency: "LOW",
    accuracy: "MEDIUM"
  },
  SWARM_INTELLIGENCE: {
    code: "SWARM_INTELLIGENCE",
    name: "Swarm Intelligence",
    description: "Particle swarm optimization and ant colony optimization",
    complexity: "HIGH",
    latency: "MODERATE",
    accuracy: "MEDIUM_HIGH"
  }
};

export const AlgorithmComplexity = {
  VERY_LOW: "VERY_LOW",
  LOW: "LOW",
  MEDIUM: "MEDIUM",
  HIGH: "HIGH",
  VERY_HIGH: "VERY_HIGH"
};

export const AlgorithmLatency = {
  ULTRA_LOW: "ULTRA_LOW",      // < 1ms
  VERY_LOW: "VERY_LOW",        // 1-10ms
  LOW: "LOW",                  // 10-100ms
  MODERATE: "MODERATE",        // 100ms-1s
  HIGH: "HIGH",                // 1-10s
  VERY_HIGH: "VERY_HIGH",      // 10s-1min
  BATCH: "BATCH"               // > 1min
};

export const AlgorithmAccuracy = {
  EXPERIMENTAL: "EXPERIMENTAL",  // < 50%
  LOW: "LOW",                    // 50-60%
  MEDIUM: "MEDIUM",              // 60-70%
  MEDIUM_HIGH: "MEDIUM_HIGH",    // 70-80%
  HIGH: "HIGH",                  // 80-90%
  VERY_HIGH: "VERY_HIGH",        // 90-95%
  EXCEPTIONAL: "EXCEPTIONAL"     // > 95%
};

export const NodeStatus = {
  // Processing States
  INITIALIZING: {
    code: "INITIALIZING",
    description: "Node is initializing resources and dependencies",
    color: "#FFA500",
    priority: "LOW"
  },
  PROCESSING: {
    code: "PROCESSING",
    description: "Node is actively processing data",
    color: "#1E90FF",
    priority: "HIGH"
  },
  COMPLETED: {
    code: "COMPLETED",
    description: "Node has successfully completed processing",
    color: "#32CD32",
    priority: "MEDIUM"
  },
  ERROR: {
    code: "ERROR",
    description: "Node encountered an error during processing",
    color: "#FF4500",
    priority: "CRITICAL"
  },
  IDLE: {
    code: "IDLE",
    description: "Node is waiting for input or scheduled task",
    color: "#808080",
    priority: "LOW"
  },
  OPTIMIZING: {
    code: "OPTIMIZING",
    description: "Node is optimizing its internal parameters",
    color: "#9370DB",
    priority: "MEDIUM"
  },
  BACKTESTING: {
    code: "BACKTESTING",
    description: "Node is performing historical backtesting",
    color: "#FFD700",
    priority: "MEDIUM"
  },
  TRAINING: {
    code: "TRAINING",
    description: "Node is training its machine learning model",
    color: "#00CED1",
    priority: "HIGH"
  },
  VALIDATING: {
    code: "VALIDATING",
    description: "Node is validating results against test data",
    color: "#20B2AA",
    priority: "MEDIUM"
  },
  DEPLOYING: {
    code: "DEPLOYING",
    description: "Node is deploying new model version",
    color: "#8A2BE2",
    priority: "HIGH"
  },
  ROLLING_BACK: {
    code: "ROLLING_BACK",
    description: "Node is rolling back to previous version",
    color: "#DC143C",
    priority: "CRITICAL"
  },
  DRAINING: {
    code: "DRAINING",
    description: "Node is gracefully shutting down",
    color: "#696969",
    priority: "MEDIUM"
  },
  OFFLINE: {
    code: "OFFLINE",
    description: "Node is offline for maintenance",
    color: "#000000",
    priority: "LOW"
  }
};

export const NodePriority = {
  CRITICAL: "CRITICAL",  // Must process immediately
  HIGH: "HIGH",          // Process as soon as possible
  MEDIUM: "MEDIUM",      // Process during normal operations
  LOW: "LOW",            // Process during idle time
  BACKGROUND: "BACKGROUND" // Process only when system is idle
};

export const Decision = {
  // Primary Trading Decisions
  BUY: {
    code: "BUY",
    name: "Buy",
    description: "Enter long position or increase existing long position",
    action: "ENTER_LONG",
    sentiment: "BULLISH",
    intensity: 1.0
  },
  SELL: {
    code: "SELL",
    name: "Sell",
    description: "Enter short position or increase existing short position",
    action: "ENTER_SHORT",
    sentiment: "BEARISH",
    intensity: 1.0
  },
  HOLD: {
    code: "HOLD",
    name: "Hold",
    description: "Maintain current position with no changes",
    action: "MAINTAIN",
    sentiment: "NEUTRAL",
    intensity: 0.0
  },

  // Advanced Trading Actions
  CLOSE_LONG: {
    code: "CLOSE_LONG",
    name: "Close Long",
    description: "Exit existing long position",
    action: "EXIT_POSITION",
    sentiment: "NEUTRAL",
    intensity: 0.0
  },
  CLOSE_SHORT: {
    code: "CLOSE_SHORT",
    name: "Close Short",
    description: "Exit existing short position",
    action: "EXIT_POSITION",
    sentiment: "NEUTRAL",
    intensity: 0.0
  },
  SCALE_IN: {
    code: "SCALE_IN",
    name: "Scale In",
    description: "Gradually add to existing position",
    action: "INCREASE_POSITION",
    sentiment: "BULLISH",
    intensity: 0.5
  },
  SCALE_OUT: {
    code: "SCALE_OUT",
    name: "Scale Out",
    description: "Gradually reduce existing position",
    action: "REDUCE_POSITION",
    sentiment: "NEUTRAL_BEARISH",
    intensity: 0.3
  },
  REVERSE: {
    code: "REVERSE",
    name: "Reverse",
    description: "Close current position and open opposite position",
    action: "REVERSE_POSITION",
    sentiment: "CONTRARIAN",
    intensity: 1.0
  },
  HEDGE: {
    code: "HEDGE",
    name: "Hedge",
    description: "Open opposite position to reduce risk",
    action: "HEDGE_POSITION",
    sentiment: "NEUTRAL",
    intensity: 0.0
  },
  STOP_LOSS: {
    code: "STOP_LOSS",
    name: "Stop Loss",
    description: "Emergency exit at predetermined loss level",
    action: "EMERGENCY_EXIT",
    sentiment: "BEARISH",
    intensity: 0.8
  },
  TAKE_PROFIT: {
    code: "TAKE_PROFIT",
    name: "Take Profit",
    description: "Exit at predetermined profit level",
    action: "PROFIT_EXIT",
    sentiment: "BULLISH",
    intensity: 0.8
  },
  TRAILING_STOP: {
    code: "TRAILING_STOP",
    name: "Trailing Stop",
    description: "Dynamic stop loss that follows price",
    action: "DYNAMIC_EXIT",
    sentiment: "NEUTRAL",
    intensity: 0.6
  }
};

export const DecisionConfidence = {
  VERY_LOW: {
    code: "VERY_LOW",
    range: [0, 0.2],
    description: "Very low confidence - avoid trading",
    color: "#FF0000",
    action: "NO_TRADE"
  },
  LOW: {
    code: "LOW",
    range: [0.2, 0.4],
    description: "Low confidence - trade with caution",
    color: "#FFA500",
    action: "SMALL_POSITION"
  },
  MEDIUM: {
    code: "MEDIUM",
    range: [0.4, 0.6],
    description: "Medium confidence - normal trading",
    color: "#FFFF00",
    action: "NORMAL_POSITION"
  },
  HIGH: {
    code: "HIGH",
    range: [0.6, 0.8],
    description: "High confidence - increased position",
    color: "#90EE90",
    action: "INCREASED_POSITION"
  },
  VERY_HIGH: {
    code: "VERY_HIGH",
    range: [0.8, 0.95],
    description: "Very high confidence - maximum position",
    color: "#32CD32",
    action: "MAX_POSITION"
  },
  EXTREME: {
    code: "EXTREME",
    range: [0.95, 1.0],
    description: "Extreme confidence - consider leverage",
    color: "#006400",
    action: "LEVERAGED_POSITION"
  }
};

export const MarketRegime = {
  TRENDING_UP: {
    code: "TRENDING_UP",
    name: "Bullish Trend",
    description: "Sustained upward price movement",
    volatility: "MEDIUM",
    direction: "UP",
    probability: 0.6
  },
  TRENDING_DOWN: {
    code: "TRENDING_DOWN",
    name: "Bearish Trend",
    description: "Sustained downward price movement",
    volatility: "MEDIUM",
    direction: "DOWN",
    probability: 0.6
  },
  SIDEWAYS: {
    code: "SIDEWAYS",
    name: "Range Bound",
    description: "Price moving within a defined range",
    volatility: "LOW",
    direction: "NEUTRAL",
    probability: 0.7
  },
  HIGH_VOLATILITY: {
    code: "HIGH_VOLATILITY",
    name: "High Volatility",
    description: "Large price swings and uncertainty",
    volatility: "HIGH",
    direction: "UNCERTAIN",
    probability: 0.4
  },
  LOW_VOLATILITY: {
    code: "LOW_VOLATILITY",
    name: "Low Volatility",
    description: "Small price movements and stability",
    volatility: "LOW",
    direction: "NEUTRAL",
    probability: 0.8
  },
  BREAKOUT: {
    code: "BREAKOUT",
    name: "Breakout",
    description: "Price breaking through key levels",
    volatility: "HIGH",
    direction: "STRONG_DIRECTIONAL",
    probability: 0.5
  },
  REVERSAL: {
    code: "REVERSAL",
    name: "Trend Reversal",
    description: "Change in primary trend direction",
    volatility: "HIGH",
    direction: "CHANGING",
    probability: 0.3
  },
  ACCUMULATION: {
    code: "ACCUMULATION",
    name: "Accumulation",
    description: "Smart money accumulating positions",
    volatility: "LOW",
    direction: "PRE_BULLISH",
    probability: 0.6
  },
  DISTRIBUTION: {
    code: "DISTRIBUTION",
    name: "Distribution",
    description: "Smart money distributing positions",
    volatility: "LOW",
    direction: "PRE_BEARISH",
    probability: 0.6
  },
  CRASH: {
    code: "CRASH",
    name: "Market Crash",
    description: "Rapid and severe price decline",
    volatility: "EXTREME",
    direction: "STRONG_DOWN",
    probability: 0.1
  },
  RALLY: {
    code: "RALLY",
    name: "Market Rally",
    description: "Rapid and strong price increase",
    volatility: "HIGH",
    direction: "STRONG_UP",
    probability: 0.2
  },
  FLASH_CRASH: {
    code: "FLASH_CRASH",
    name: "Flash Crash",
    description: "Extremely rapid price decline and recovery",
    volatility: "EXTREME",
    direction: "VOLATILE",
    probability: 0.05
  }
};

export const Timeframe = {
  TICK: {
    code: "TICK",
    name: "Tick",
    milliseconds: 1,
    description: "Individual trade data",
    usage: "HIGH_FREQUENCY"
  },
  ONE_SECOND: {
    code: "ONE_SECOND",
    name: "1 Second",
    milliseconds: 1000,
    description: "One second intervals",
    usage: "ULTRA_HIGH_FREQUENCY"
  },
  FIVE_SECOND: {
    code: "FIVE_SECOND",
    name: "5 Seconds",
    milliseconds: 5000,
    description: "Five second intervals",
    usage: "HIGH_FREQUENCY"
  },
  THIRTY_SECOND: {
    code: "THIRTY_SECOND",
    name: "30 Seconds",
    milliseconds: 30000,
    description: "Thirty second intervals",
    usage: "HIGH_FREQUENCY"
  },
  ONE_MINUTE: {
    code: "ONE_MINUTE",
    name: "1 Minute",
    milliseconds: 60000,
    description: "One minute candlesticks",
    usage: "MEDIUM_FREQUENCY"
  },
  FIVE_MINUTE: {
    code: "FIVE_MINUTE",
    name: "5 Minutes",
    milliseconds: 300000,
    description: "Five minute candlesticks",
    usage: "SWING_TRADING"
  },
  FIFTEEN_MINUTE: {
    code: "FIFTEEN_MINUTE",
    name: "15 Minutes",
    milliseconds: 900000,
    description: "Fifteen minute candlesticks",
    usage: "SWING_TRADING"
  },
  ONE_HOUR: {
    code: "ONE_HOUR",
    name: "1 Hour",
    milliseconds: 3600000,
    description: "Hourly candlesticks",
    usage: "DAY_TRADING"
  },
  FOUR_HOUR: {
    code: "FOUR_HOUR",
    name: "4 Hours",
    milliseconds: 14400000,
    description: "Four hour candlesticks",
    usage: "SWING_TRADING"
  },
  DAILY: {
    code: "DAILY",
    name: "Daily",
    milliseconds: 86400000,
    description: "Daily candlesticks",
    usage: "POSITION_TRADING"
  },
  WEEKLY: {
    code: "WEEKLY",
    name: "Weekly",
    milliseconds: 604800000,
    description: "Weekly candlesticks",
    usage: "INVESTING"
  },
  MONTHLY: {
    code: "MONTHLY",
    name: "Monthly",
    milliseconds: 2592000000,
    description: "Monthly candlesticks",
    usage: "INVESTING"
  }
};

export const TradingSession = {
  ASIA: {
    code: "ASIA",
    name: "Asian Session",
    open: "00:00 UTC",
    close: "09:00 UTC",
    activePairs: ["USD/JPY", "AUD/USD", "NZD/USD"],
    volatility: "LOW"
  },
  LONDON: {
    code: "LONDON",
    name: "London Session",
    open: "08:00 UTC",
    close: "16:00 UTC",
    activePairs: ["EUR/USD", "GBP/USD", "EUR/GBP"],
    volatility: "HIGH"
  },
  NEW_YORK: {
    code: "NEW_YORK",
    name: "New York Session",
    open: "13:00 UTC",
    close: "21:00 UTC",
    activePairs: ["USD/CAD", "USD/CHF", "EUR/USD"],
    volatility: "HIGH"
  },
  OVERLAP_LONDON_NY: {
    code: "OVERLAP_LONDON_NY",
    name: "London-NY Overlap",
    open: "13:00 UTC",
    close: "16:00 UTC",
    activePairs: ["EUR/USD", "GBP/USD", "USD/JPY"],
    volatility: "VERY_HIGH"
  },
  PACIFIC: {
    code: "PACIFIC",
    name: "Pacific Session",
    open: "21:00 UTC",
    close: "06:00 UTC",
    activePairs: ["AUD/USD", "NZD/USD", "AUD/JPY"],
    volatility: "MEDIUM"
  },
  WEEKEND: {
    code: "WEEKEND",
    name: "Weekend",
    open: "21:00 UTC Friday",
    close: "00:00 UTC Monday",
    activePairs: ["BTC/USD", "ETH/USD"],
    volatility: "LOW"
  }
};

export const RiskLevel = {
  VERY_LOW: {
    code: "VERY_LOW",
    maxDrawdown: 0.02,  // 2%
    positionSize: 0.01,  // 1% of capital
    description: "Very conservative risk profile"
  },
  LOW: {
    code: "LOW",
    maxDrawdown: 0.05,  // 5%
    positionSize: 0.02,  // 2% of capital
    description: "Conservative risk profile"
  },
  MODERATE: {
    code: "MODERATE",
    maxDrawdown: 0.10,  // 10%
    positionSize: 0.05,  // 5% of capital
    description: "Balanced risk profile"
  },
  HIGH: {
    code: "HIGH",
    maxDrawdown: 0.20,  // 20%
    positionSize: 0.10,  // 10% of capital
    description: "Aggressive risk profile"
  },
  VERY_HIGH: {
    code: "VERY_HIGH",
    maxDrawdown: 0.35,  // 35%
    positionSize: 0.20,  // 20% of capital
    description: "Very aggressive risk profile"
  },
  EXTREME: {
    code: "EXTREME",
    maxDrawdown: 0.50,  // 50%
    positionSize: 0.35,  // 35% of capital
    description: "Extreme risk profile - professional only"
  }
};

export const AssetClass = {
  FOREX: {
    code: "FOREX",
    name: "Foreign Exchange",
    description: "Currency pairs trading",
    leverage: "HIGH",
    volatility: "MEDIUM"
  },
  STOCKS: {
    code: "STOCKS",
    name: "Equities",
    description: "Company shares trading",
    leverage: "MEDIUM",
    volatility: "MEDIUM_HIGH"
  },
  CRYPTO: {
    code: "CRYPTO",
    name: "Cryptocurrency",
    description: "Digital currency trading",
    leverage: "HIGH",
    volatility: "VERY_HIGH"
  },
  COMMODITIES: {
    code: "COMMODITIES",
    name: "Commodities",
    description: "Raw materials trading",
    leverage: "MEDIUM",
    volatility: "HIGH"
  },
  INDICES: {
    code: "INDICES",
    name: "Indices",
    description: "Market index trading",
    leverage: "HIGH",
    volatility: "MEDIUM"
  },
  BONDS: {
    code: "BONDS",
    name: "Bonds",
    description: "Fixed income securities",
    leverage: "LOW",
    volatility: "LOW"
  },
  FUTURES: {
    code: "FUTURES",
    name: "Futures",
    description: "Derivative contracts",
    leverage: "VERY_HIGH",
    volatility: "HIGH"
  },
  OPTIONS: {
    code: "OPTIONS",
    name: "Options",
    description: "Derivative options contracts",
    leverage: "EXTREME",
    volatility: "VERY_HIGH"
  },
  ETFs: {
    code: "ETFs",
    name: "Exchange Traded Funds",
    description: "Basket securities trading",
    leverage: "MEDIUM",
    volatility: "MEDIUM"
  }
};

export const ModelType = {
  PREDICTIVE: {
    code: "PREDICTIVE",
    name: "Predictive Model",
    description: "Predicts future price movements",
    horizon: "FUTURE"
  },
  CLASSIFICATION: {
    code: "CLASSIFICATION",
    name: "Classification Model",
    description: "Classifies market regimes or patterns",
    horizon: "CURRENT"
  },
  REGRESSION: {
    code: "REGRESSION",
    name: "Regression Model",
    description: "Predicts continuous values",
    horizon: "FUTURE"
  },
  CLUSTERING: {
    code: "CLUSTERING",
    name: "Clustering Model",
    description: "Groups similar market conditions",
    horizon: "CURRENT"
  },
  REINFORCEMENT: {
    code: "REINFORCEMENT",
    name: "Reinforcement Model",
    description: "Learns optimal trading strategies",
    horizon: "FUTURE"
  },
  ANOMALY_DETECTION: {
    code: "ANOMALY_DETECTION",
    name: "Anomaly Detection",
    description: "Detects unusual market behavior",
    horizon: "CURRENT"
  },
  SENTIMENT_ANALYSIS: {
    code: "SENTIMENT_ANALYSIS",
    name: "Sentiment Analysis",
    description: "Analyzes market sentiment from text",
    horizon: "CURRENT"
  }
};

export const ExecutionMode = {
  PAPER: {
    code: "PAPER",
    name: "Paper Trading",
    description: "Simulated trading with no real money",
    risk: "NONE"
  },
  LIVE: {
    code: "LIVE",
    name: "Live Trading",
    description: "Real money trading",
    risk: "ACTUAL"
  },
  BACKTEST: {
    code: "BACKTEST",
    name: "Backtesting",
    description: "Historical data testing",
    risk: "NONE"
  },
  FORWARD_TEST: {
    code: "FORWARD_TEST",
    name: "Forward Testing",
    description: "Real-time testing with simulated execution",
    risk: "SIMULATED"
  },
  HYBRID: {
    code: "HYBRID",
    name: "Hybrid Mode",
    description: "Combination of paper and live trading",
    risk: "PARTIAL"
  }
};

export const SignalSource = {
  TECHNICAL: {
    code: "TECHNICAL",
    name: "Technical Analysis",
    description: "Based on price patterns and indicators"
  },
  FUNDAMENTAL: {
    code: "FUNDAMENTAL",
    name: "Fundamental Analysis",
    description: "Based on economic and financial data"
  },
  QUANTITATIVE: {
    code: "QUANTITATIVE",
    name: "Quantitative Models",
    description: "Based on mathematical and statistical models"
  },
  SENTIMENT: {
    code: "SENTIMENT",
    name: "Market Sentiment",
    description: "Based on news, social media, and sentiment analysis"
  },
  MACHINE_LEARNING: {
    code: "MACHINE_LEARNING",
    name: "Machine Learning",
    description: "Based on AI/ML model predictions"
  },
  ENSEMBLE: {
    code: "ENSEMBLE",
    name: "Ensemble",
    description: "Combination of multiple signal sources"
  }
};

export const OptimizationMethod = {
  GRID_SEARCH: {
    code: "GRID_SEARCH",
    name: "Grid Search",
    description: "Exhaustive search over parameter grid"
  },
  RANDOM_SEARCH: {
    code: "RANDOM_SEARCH",
    name: "Random Search",
    description: "Random sampling of parameter space"
  },
  BAYESIAN: {
    code: "BAYESIAN",
    name: "Bayesian Optimization",
    description: "Probabilistic model-based optimization"
  },
  GENETIC_ALGORITHM: {
    code: "GENETIC_ALGORITHM",
    name: "Genetic Algorithm",
    description: "Evolutionary optimization approach"
  },
  GRADIENT_BASED: {
    code: "GRADIENT_BASED",
    name: "Gradient Based",
    description: "Optimization using gradient information"
  },
  REINFORCEMENT_LEARNING: {
    code: "REINFORCEMENT_LEARNING",
    name: "Reinforcement Learning",
    description: "Learning optimal parameters through trial and error"
  }
};

export const ValidationMethod = {
  TRAIN_TEST: {
    code: "TRAIN_TEST",
    name: "Train-Test Split",
    description: "Simple split of data into training and testing sets"
  },
  CROSS_VALIDATION: {
    code: "CROSS_VALIDATION",
    name: "Cross Validation",
    description: "K-fold cross validation"
  },
  WALK_FORWARD: {
    code: "WALK_FORWARD",
    name: "Walk Forward",
    description: "Time-series aware validation method"
  },
  OUT_OF_SAMPLE: {
    code: "OUT_OF_SAMPLE",
    name: "Out of Sample",
    description: "Validation on completely unseen data"
  },
  MONTE_CARLO: {
    code: "MONTE_CARLO",
    name: "Monte Carlo",
    description: "Statistical validation through random sampling"
  }
};

// Utility functions for working with enums
export const EnumUtils = {
  getAlgorithmByCode: (code) => {
    return Object.values(AlgorithmType).find(algo => algo.code === code);
  },

  getDecisionByCode: (code) => {
    return Object.values(Decision).find(decision => decision.code === code);
  },

  getNodeStatusByCode: (code) => {
    return Object.values(NodeStatus).find(status => status.code === code);
  },

  getConfidenceForValue: (value) => {
    for (const confidence of Object.values(DecisionConfidence)) {
      if (value >= confidence.range[0] && value <= confidence.range[1]) {
        return confidence;
      }
    }
    return DecisionConfidence.VERY_LOW;
  },

  getRiskLevelByCode: (code) => {
    return Object.values(RiskLevel).find(risk => risk.code === code);
  },

  getMarketRegimeByCode: (code) => {
    return Object.values(MarketRegime).find(regime => regime.code === code);
  },

  getTimeframeByCode: (code) => {
    return Object.values(Timeframe).find(tf => tf.code === code);
  },

  getAllAlgorithms: () => {
    return Object.values(AlgorithmType);
  },

  getAllDecisions: () => {
    return Object.values(Decision);
  },

  getAllMarketRegimes: () => {
    return Object.values(MarketRegime);
  },

  getAlgorithmComplexity: (algorithmCode) => {
    const algo = EnumUtils.getAlgorithmByCode(algorithmCode);
    return algo ? algo.complexity : AlgorithmComplexity.MEDIUM;
  },

  getAlgorithmAccuracy: (algorithmCode) => {
    const algo = EnumUtils.getAlgorithmByCode(algorithmCode);
    return algo ? algo.accuracy : AlgorithmAccuracy.MEDIUM;
  },

  getAlgorithmLatency: (algorithmCode) => {
    const algo = EnumUtils.getAlgorithmByCode(algorithmCode);
    return algo ? algo.latency : AlgorithmLatency.MODERATE;
  },

  isTrendFollowingDecision: (decisionCode) => {
    const decision = EnumUtils.getDecisionByCode(decisionCode);
    return decision && ['BUY', 'SELL', 'REVERSE'].includes(decision.code);
  },

  isExitDecision: (decisionCode) => {
    const decision = EnumUtils.getDecisionByCode(decisionCode);
    return decision && ['CLOSE_LONG', 'CLOSE_SHORT', 'STOP_LOSS', 'TAKE_PROFIT'].includes(decision.code);
  },

  isPositionAdjustmentDecision: (decisionCode) => {
    const decision = EnumUtils.getDecisionByCode(decisionCode);
    return decision && ['SCALE_IN', 'SCALE_OUT', 'HEDGE'].includes(decision.code);
  },

  getActiveSession: () => {
    const now = new Date();
    const utcHours = now.getUTCHours();

    if (utcHours >= 0 && utcHours < 9) return TradingSession.ASIA;
    if (utcHours >= 8 && utcHours < 16) return TradingSession.LONDON;
    if (utcHours >= 13 && utcHours < 21) return TradingSession.NEW_YORK;
    if (utcHours >= 13 && utcHours < 16) return TradingSession.OVERLAP_LONDON_NY;
    if (utcHours >= 21 || utcHours < 6) return TradingSession.PACIFIC;

    return TradingSession.WEEKEND;
  },

  getRecommendedAlgorithm: (marketRegimeCode, timeframeCode) => {
    const regime = EnumUtils.getMarketRegimeByCode(marketRegimeCode);
    const tf = EnumUtils.getTimeframeByCode(timeframeCode);

    if (!regime || !tf) return AlgorithmType.HYBRID;

    if (regime.code === 'HIGH_VOLATILITY') {
      return AlgorithmType.QUANTUM;
    }

    if (regime.code === 'TRENDING_UP' || regime.code === 'TRENDING_DOWN') {
      return AlgorithmType.DEEP_LEARNING;
    }

    if (tf.usage === 'HIGH_FREQUENCY') {
      return AlgorithmType.STATISTICAL;
    }

    return AlgorithmType.ENSEMBLE;
  },

  getOptimalTimeframe: (algorithmCode, assetClassCode) => {
    const algo = EnumUtils.getAlgorithmByCode(algorithmCode);

    if (!algo) return Timeframe.ONE_HOUR;

    switch (algo.code) {
      case 'DEEP_LEARNING':
      case 'REINFORCEMENT_LEARNING':
        return Timeframe.ONE_HOUR;
      case 'ML':
      case 'ENSEMBLE':
        return Timeframe.FOUR_HOUR;
      case 'STATISTICAL':
        return Timeframe.FIFTEEN_MINUTE;
      case 'QUANTUM':
        return Timeframe.ONE_MINUTE;
      default:
        return Timeframe.ONE_HOUR;
    }
  },

  calculatePositionSize: (riskLevelCode, confidenceValue, accountBalance) => {
    const risk = EnumUtils.getRiskLevelByCode(riskLevelCode);
    const confidence = EnumUtils.getConfidenceForValue(confidenceValue);

    if (!risk || !confidence) return 0;

    // Base position size from risk level
    let size = risk.positionSize * accountBalance;

    // Adjust based on confidence
    const confidenceMultiplier = (confidenceValue - 0.5) * 2; // Map 0.5-1.0 to 0-1
    size *= (1 + confidenceMultiplier);

    // Apply confidence-based limits
    switch (confidence.code) {
      case 'VERY_LOW':
        size *= 0.1;
        break;
      case 'LOW':
        size *= 0.3;
        break;
      case 'MEDIUM':
        size *= 0.6;
        break;
      case 'HIGH':
        size *= 0.9;
        break;
      case 'VERY_HIGH':
        size *= 1.2;
        break;
      case 'EXTREME':
        size *= 1.5;
        break;
    }

    // Cap at risk limit
    const maxSize = risk.positionSize * accountBalance * 2;
    return Math.min(size, maxSize);
  }
};

// Default configurations
export const DefaultConfigs = {
  ALGORITHM: AlgorithmType.ENSEMBLE,
  RISK_LEVEL: RiskLevel.MODERATE,
  TIMEFRAME: Timeframe.ONE_HOUR,
  MARKET_REGIME: MarketRegime.SIDEWAYS,
  EXECUTION_MODE: ExecutionMode.PAPER,
  CONFIDENCE_THRESHOLD: 0.7,
  MAX_POSITIONS: 5,
  MAX_DRAWDOWN: 0.15,
  MIN_WIN_RATE: 0.55,
  MAX_LEVERAGE: 3.0
};

// Export types for TypeScript (if used)
export const Types = {
  AlgorithmType: Object.keys(AlgorithmType),
  NodeStatus: Object.keys(NodeStatus),
  Decision: Object.keys(Decision),
  MarketRegime: Object.keys(MarketRegime),
  Timeframe: Object.keys(Timeframe),
  RiskLevel: Object.keys(RiskLevel),
  AssetClass: Object.keys(AssetClass),
  ExecutionMode: Object.keys(ExecutionMode)
};

export default {
  AlgorithmType,
  NodeStatus,
  Decision,
  MarketRegime,
  Timeframe,
  TradingSession,
  RiskLevel,
  AssetClass,
  ModelType,
  ExecutionMode,
  SignalSource,
  OptimizationMethod,
  ValidationMethod,
  EnumUtils,
  DefaultConfigs,
  Types
};