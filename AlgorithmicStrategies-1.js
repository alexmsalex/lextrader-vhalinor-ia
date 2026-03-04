/**
 * Algorithmic Strategies Manager
 * Sistema avançado de gerenciamento de estratégias algorítmicas
 * com otimização adaptativa e gestão de risco integrada
 */

import { AdvancedTemporalNetwork } from './advanced_temporal_network.js';
import { aiSystemManager } from './ai_system_manager.js';

export const StrategyType = {
    TREND_FOLLOWING: 'trend_following',
    MEAN_REVERSION: 'mean_reversion',
    BREAKOUT: 'breakout',
    ARBITRAGE: 'arbitrage',
    MARKET_MAKING: 'market_making',
    SENTIMENT_DRIVEN: 'sentiment_driven',
    ML_DRIVEN: 'ml_driven',
    HYBRID: 'hybrid',
    SCALPING: 'scalping',
    SWING: 'swing',
    POSITION: 'position'
};

export const Timeframe = {
    TICK: 'tick',
    ONE_MINUTE: '1m',
    FIVE_MINUTE: '5m',
    FIFTEEN_MINUTE: '15m',
    ONE_HOUR: '1h',
    FOUR_HOUR: '4h',
    DAILY: '1d',
    WEEKLY: '1w'
};

export const SignalStrength = {
    VERY_STRONG: 'VERY_STRONG',    // > 0.8
    STRONG: 'STRONG',              // 0.6 - 0.8
    MODERATE: 'MODERATE',          // 0.4 - 0.6
    WEAK: 'WEAK',                  // 0.2 - 0.4
    VERY_WEAK: 'VERY_WEAK'         // < 0.2
};

export const StrategyStatus = {
    ACTIVE: 'ACTIVE',
    PAUSED: 'PAUSED',
    DISABLED: 'DISABLED',
    OPTIMIZING: 'OPTIMIZING',
    BACKTESTING: 'BACKTESTING',
    ERROR: 'ERROR'
};

export class PositionSizing {
    constructor(config = {}) {
        this.config = {
            maxPositionSize: config.maxPositionSize || 0.1, // 10% do capital
            riskPerTrade: config.riskPerTrade || 0.02, // 2% por trade
            kellyFraction: config.kellyFraction || 0.5,
            useVolatilityAdjustment: config.useVolatilityAdjustment !== false,
            useCorrelationAdjustment: config.useCorrelationAdjustment !== false,
            ...config
        };

        this.positionHistory = [];
        this.correlationMatrix = new Map();
    }

    calculateSize(entryPrice, stopLoss, accountBalance, volatility, winRate, profitLossRatio) {
        // Cálculo baseado no risco
        const riskAmount = accountBalance * this.config.riskPerTrade;
        const priceRisk = Math.abs(entryPrice - stopLoss);
        const baseSize = riskAmount / priceRisk;

        // Ajuste por volatilidade
        let adjustedSize = baseSize;
        if (this.config.useVolatilityAdjustment) {
            adjustedSize *= this.adjustForVolatility(volatility);
        }

        // Ajuste por correlação
        if (this.config.useCorrelationAdjustment) {
            adjustedSize *= this.adjustForCorrelation();
        }

        // Aplicar critério de Kelly fracionário
        const kellySize = this.calculateKellySize(winRate, profitLossRatio);
        const finalSize = adjustedSize * kellySize * this.config.kellyFraction;

        // Limitar ao máximo permitido
        const maxSize = accountBalance * this.config.maxPositionSize / entryPrice;
        const clampedSize = Math.min(finalSize, maxSize);

        // Registrar
        this.positionHistory.push({
            timestamp: new Date(),
            entryPrice,
            size: clampedSize,
            accountBalance,
            volatility,
            winRate,
            profitLossRatio
        });

        return clampedSize;
    }

    adjustForVolatility(volatility) {
        // Reduzir tamanho em alta volatilidade
        if (volatility > 0.03) return 0.5; // -50%
        if (volatility > 0.02) return 0.7; // -30%
        if (volatility > 0.01) return 0.9; // -10%
        return 1.0;
    }

    adjustForCorrelation() {
        // Reduzir tamanho se muitas posições correlacionadas
        const recentPositions = this.positionHistory.slice(-10);
        if (recentPositions.length < 3) return 1.0;

        // Simplificado - em produção usar matriz de correlação real
        const avgSize = recentPositions.reduce((sum, pos) => sum + pos.size, 0) / recentPositions.length;
        const currentAvg = avgSize / recentPositions.length;

        if (currentAvg > this.config.maxPositionSize * 0.8) {
            return 0.5; // Reduzir pela metade se muito concentrado
        }

        return 1.0;
    }

    calculateKellySize(winRate, profitLossRatio) {
        if (winRate <= 0 || profitLossRatio <= 0) return 0.1; // Fallback

        // Fórmula de Kelly: f* = p - q/b
        const p = winRate;
        const q = 1 - winRate;
        const b = profitLossRatio;

        const kelly = (p * b - q) / b;
        return Math.max(0, Math.min(kelly, 0.25)); // Limitar a 25%
    }

    updateCorrelationMatrix(symbols, correlations) {
        for (let i = 0; i < symbols.length; i++) {
            for (let j = 0; j < symbols.length; j++) {
                const key = `${symbols[i]}_${symbols[j]}`;
                this.correlationMatrix.set(key, correlations[i][j]);
            }
        }
    }

    getPortfolioRiskMetrics(positions) {
        if (!positions || positions.length === 0) {
            return {
                totalExposure: 0,
                weightedVolatility: 0,
                diversificationScore: 1.0,
                maxDrawdownPotential: 0,
                riskAdjustedSize: 1.0
            };
        }

        let totalExposure = 0;
        let weightedVolatility = 0;
        let correlationSum = 0;

        positions.forEach(pos => {
            totalExposure += pos.size * pos.entryPrice;
            weightedVolatility += pos.size * pos.volatility;

            // Calcular correlações (simplificado)
            positions.forEach(otherPos => {
                if (pos.symbol !== otherPos.symbol) {
                    const key = `${pos.symbol}_${otherPos.symbol}`;
                    correlationSum += this.correlationMatrix.get(key) || 0;
                }
            });
        });

        const avgCorrelation = correlationSum / (positions.length * (positions.length - 1)) || 0;
        const diversificationScore = 1 - Math.abs(avgCorrelation);

        return {
            totalExposure,
            weightedVolatility: weightedVolatility / positions.length,
            diversificationScore,
            maxDrawdownPotential: weightedVolatility * (1 + avgCorrelation),
            riskAdjustedSize: Math.min(1.0, 1 / (1 + weightedVolatility * (1 + avgCorrelation)))
        };
    }
}

export class StrategyBacktester {
    constructor() {
        this.results = new Map();
        this.metricsHistory = [];
        this.optimizationQueue = [];
    }

    async backtest(strategy, marketData, config = {}) {
        const startTime = Date.now();
        const {
            initialCapital = 10000,
            commission = 0.001,
            slippage = 0.0005,
            startDate = null,
            endDate = null,
            timeframe = Timeframe.ONE_HOUR
        } = config;

        console.log(`🔍 Iniciando backtest da estratégia ${strategy.name}...`);

        try {
            const results = await this.executeBacktest(strategy, marketData, {
                initialCapital,
                commission,
                slippage,
                startDate,
                endDate,
                timeframe
            });

            const metrics = this.calculatePerformanceMetrics(results);
            const optimization = this.analyzeForOptimization(strategy, results, marketData);

            const backtestResult = {
                strategyId: strategy.id,
                name: strategy.name,
                timeframe,
                duration: Date.now() - startTime,
                results,
                metrics,
                optimization,
                timestamp: new Date()
            };

            this.results.set(strategy.id, backtestResult);
            this.metricsHistory.push({
                strategyId: strategy.id,
                timestamp: new Date(),
                metrics
            });

            console.log(`✅ Backtest concluído para ${strategy.name}`);
            console.log(`📊 Retorno total: ${metrics.totalReturn.toFixed(2)}%`);

            return backtestResult;

        } catch (error) {
            console.error(`❌ Erro no backtest da estratégia ${strategy.name}:`, error);
            throw error;
        }
    }

    async executeBacktest(strategy, marketData, config) {
        const trades = [];
        let capital = config.initialCapital;
        let position = null;
        let equityCurve = [capital];

        const dataPoints = marketData.length;
        let currentIndex = 0;

        while (currentIndex < dataPoints) {
            const currentData = marketData[currentIndex];
            const signal = await strategy.generateSignal(currentData, position);

            if (signal.action !== 'HOLD') {
                // Executar trade
                const trade = this.executeTrade(signal, currentData, capital, position, config);

                if (trade) {
                    trades.push(trade);
                    capital = trade.balanceAfter;
                    position = trade.positionAfter;
                    equityCurve.push(capital);
                }
            }

            currentIndex++;

            // Atualizar posição em aberto
            if (position) {
                position.currentValue = position.size * currentData.close;
                position.unrealizedPnl = position.currentValue - position.costBasis;
            }
        }

        // Fechar posição aberta no final
        if (position) {
            const closeTrade = this.closePosition(position, marketData[dataPoints - 1], capital, config);
            trades.push(closeTrade);
            capital = closeTrade.balanceAfter;
            equityCurve.push(capital);
        }

        return {
            trades,
            finalCapital: capital,
            equityCurve,
            initialCapital: config.initialCapital,
            totalTrades: trades.length
        };
    }

    executeTrade(signal, marketData, capital, currentPosition, config) {
        const entryPrice = marketData.close * (1 + (signal.action === 'BUY' ? config.slippage : -config.slippage));
        const exitPrice = marketData.close * (1 + (signal.action === 'SELL' ? config.slippage : -config.slippage));

        let trade = null;

        if (signal.action === 'BUY' && !currentPosition) {
            // Nova posição long
            const size = signal.size || (capital * 0.1 / entryPrice);
            const cost = size * entryPrice;
            const commissionCost = cost * config.commission;
            const totalCost = cost + commissionCost;

            if (totalCost > capital) {
                console.warn('⚠️ Capital insuficiente para executar trade');
                return null;
            }

            trade = {
                id: `trade_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                timestamp: marketData.timestamp,
                action: 'BUY',
                symbol: signal.symbol,
                size,
                entryPrice,
                costBasis: totalCost / size,
                commission: commissionCost,
                balanceBefore: capital,
                balanceAfter: capital - totalCost,
                positionAfter: {
                    symbol: signal.symbol,
                    size,
                    entryPrice,
                    costBasis: totalCost / size,
                    direction: 'LONG',
                    openedAt: marketData.timestamp
                }
            };

        } else if (signal.action === 'SELL' && currentPosition) {
            // Fechar posição
            const exitValue = currentPosition.size * exitPrice;
            const commissionCost = exitValue * config.commission;
            const netProceeds = exitValue - commissionCost;
            const pnl = netProceeds - (currentPosition.size * currentPosition.costBasis);

            trade = {
                id: `trade_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                timestamp: marketData.timestamp,
                action: 'SELL',
                symbol: signal.symbol,
                size: currentPosition.size,
                exitPrice,
                entryPrice: currentPosition.entryPrice,
                pnl,
                pnlPercent: (pnl / (currentPosition.size * currentPosition.costBasis)) * 100,
                commission: commissionCost,
                balanceBefore: capital,
                balanceAfter: capital + netProceeds,
                positionAfter: null,
                holdDuration: marketData.timestamp - currentPosition.openedAt
            };
        }

        return trade;
    }

    closePosition(position, marketData, capital, config) {
        const exitPrice = marketData.close;
        const exitValue = position.size * exitPrice;
        const commissionCost = exitValue * config.commission;
        const netProceeds = exitValue - commissionCost;
        const pnl = netProceeds - (position.size * position.costBasis);

        return {
            id: `close_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            timestamp: marketData.timestamp,
            action: 'CLOSE',
            symbol: position.symbol,
            size: position.size,
            exitPrice,
            entryPrice: position.entryPrice,
            pnl,
            pnlPercent: (pnl / (position.size * position.costBasis)) * 100,
            commission: commissionCost,
            balanceBefore: capital,
            balanceAfter: capital + netProceeds,
            holdDuration: marketData.timestamp - position.openedAt
        };
    }

    calculatePerformanceMetrics(results) {
        const { trades, equityCurve, initialCapital, finalCapital } = results;

        if (trades.length === 0) {
            return this.getEmptyMetrics();
        }

        // Métricas básicas
        const totalReturn = ((finalCapital - initialCapital) / initialCapital) * 100;
        const winningTrades = trades.filter(t => t.pnl > 0);
        const losingTrades = trades.filter(t => t.pnl < 0);
        const winRate = winningTrades.length / trades.length;

        // Calcular retorno médio por trade
        const avgWin = winningTrades.length > 0 ?
            winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length : 0;
        const avgLoss = losingTrades.length > 0 ?
            Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length) : 0;
        const profitFactor = avgLoss > 0 ? (avgWin * winRate) / (avgLoss * (1 - winRate)) : Infinity;

        // Drawdown
        const drawdown = this.calculateDrawdown(equityCurve);

        // Sharpe Ratio (simplificado)
        const returns = this.calculateReturns(equityCurve);
        const sharpeRatio = this.calculateSharpeRatio(returns);

        // Calmar Ratio
        const calmarRatio = totalReturn / (drawdown.maxDrawdownPercent || 1);

        // Expectancy
        const expectancy = (winRate * avgWin) - ((1 - winRate) * avgLoss);

        return {
            totalReturn,
            annualizedReturn: this.annualizeReturn(totalReturn, results.durationDays),
            winRate: winRate * 100,
            profitFactor,
            sharpeRatio,
            calmarRatio,
            maxDrawdown: drawdown.maxDrawdown,
            maxDrawdownPercent: drawdown.maxDrawdownPercent,
            avgWin: avgWin,
            avgLoss: avgLoss,
            expectancy,
            totalTrades: trades.length,
            winningTrades: winningTrades.length,
            losingTrades: losingTrades.length,
            avgTradeDuration: this.calculateAvgTradeDuration(trades),
            bestTrade: this.getBestTrade(trades),
            worstTrade: this.getWorstTrade(trades),
            recoveryFactor: totalReturn / drawdown.maxDrawdown,
            sortinoRatio: this.calculateSortinoRatio(returns)
        };
    }

    calculateDrawdown(equityCurve) {
        let peak = equityCurve[0];
        let maxDrawdown = 0;
        let maxDrawdownPercent = 0;

        for (const equity of equityCurve) {
            if (equity > peak) {
                peak = equity;
            }

            const drawdown = peak - equity;
            const drawdownPercent = (drawdown / peak) * 100;

            if (drawdown > maxDrawdown) {
                maxDrawdown = drawdown;
                maxDrawdownPercent = drawdownPercent;
            }
        }

        return { maxDrawdown, maxDrawdownPercent };
    }

    calculateReturns(equityCurve) {
        const returns = [];
        for (let i = 1; i < equityCurve.length; i++) {
            const ret = (equityCurve[i] - equityCurve[i - 1]) / equityCurve[i - 1];
            returns.push(ret);
        }
        return returns;
    }

    calculateSharpeRatio(returns, riskFreeRate = 0.02) {
        if (returns.length === 0) return 0;

        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const stdDev = Math.sqrt(
            returns.reduce((sum, ret) => sum + Math.pow(ret - avgReturn, 2), 0) / returns.length
        );

        if (stdDev === 0) return 0;

        return (avgReturn - riskFreeRate) / stdDev * Math.sqrt(252); // Anualizado
    }

    calculateSortinoRatio(returns, riskFreeRate = 0.02) {
        if (returns.length === 0) return 0;

        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const negativeReturns = returns.filter(r => r < 0);
        const downsideDeviation = Math.sqrt(
            negativeReturns.reduce((sum, ret) => sum + Math.pow(ret, 2), 0) / returns.length
        );

        if (downsideDeviation === 0) return 0;

        return (avgReturn - riskFreeRate) / downsideDeviation * Math.sqrt(252);
    }

    calculateAvgTradeDuration(trades) {
        const closedTrades = trades.filter(t => t.holdDuration);
        if (closedTrades.length === 0) return 0;

        const totalDuration = closedTrades.reduce((sum, t) => sum + t.holdDuration, 0);
        return totalDuration / closedTrades.length;
    }

    getBestTrade(trades) {
        if (trades.length === 0) return null;
        return trades.reduce((best, trade) => trade.pnl > best.pnl ? trade : best);
    }

    getWorstTrade(trades) {
        if (trades.length === 0) return null;
        return trades.reduce((worst, trade) => trade.pnl < worst.pnl ? trade : worst);
    }

    annualizeReturn(totalReturn, days) {
        if (!days || days <= 0) return totalReturn;
        const years = days / 365;
        return ((1 + totalReturn / 100) ** (1 / years) - 1) * 100;
    }

    getEmptyMetrics() {
        return {
            totalReturn: 0,
            annualizedReturn: 0,
            winRate: 0,
            profitFactor: 0,
            sharpeRatio: 0,
            calmarRatio: 0,
            maxDrawdown: 0,
            maxDrawdownPercent: 0,
            avgWin: 0,
            avgLoss: 0,
            expectancy: 0,
            totalTrades: 0,
            winningTrades: 0,
            losingTrades: 0,
            avgTradeDuration: 0,
            recoveryFactor: 0,
            sortinoRatio: 0
        };
    }

    analyzeForOptimization(strategy, results, marketData) {
        const suggestions = [];

        // Análise de parâmetros
        if (results.metrics.winRate < 40) {
            suggestions.push({
                type: 'PARAMETER_ADJUSTMENT',
                message: 'Baixa taxa de acerto. Considere ajustar parâmetros de entrada.',
                parameter: 'entryThreshold',
                currentValue: strategy.config?.entryThreshold,
                suggestedValue: strategy.config?.entryThreshold ? strategy.config.entryThreshold * 1.2 : 0.02
            });
        }

        if (results.metrics.profitFactor < 1.5) {
            suggestions.push({
                type: 'RISK_MANAGEMENT',
                message: 'Fator de lucro baixo. Melhore relação risco/retorno.',
                suggestion: 'Ajustar stop-loss e take-profit'
            });
        }

        if (results.metrics.maxDrawdownPercent > 20) {
            suggestions.push({
                type: 'DRAWDOWN_CONTROL',
                message: 'Drawdown excessivo. Reduza tamanho de posição.',
                parameter: 'riskPerTrade',
                suggestedReduction: '30%'
            });
        }

        return {
            suggestions,
            optimizedParameters: this.suggestOptimizedParameters(strategy, results),
            recommendedActions: this.generateRecommendedActions(results.metrics)
        };
    }

    suggestOptimizedParameters(strategy, results) {
        const baseConfig = strategy.config || {};
        const optimized = { ...baseConfig };

        // Ajustes baseados em métricas
        if (results.metrics.winRate > 60 && results.metrics.profitFactor > 2) {
            // Estratégia performando bem - aumentar agressividade
            optimized.riskPerTrade = (baseConfig.riskPerTrade || 0.02) * 1.2;
            optimized.positionSizeMultiplier = (baseConfig.positionSizeMultiplier || 1) * 1.1;
        } else if (results.metrics.winRate < 40 || results.metrics.profitFactor < 1) {
            // Estratégia performando mal - reduzir risco
            optimized.riskPerTrade = (baseConfig.riskPerTrade || 0.02) * 0.8;
            optimized.positionSizeMultiplier = (baseConfig.positionSizeMultiplier || 1) * 0.9;
        }

        return optimized;
    }

    generateRecommendedActions(metrics) {
        const actions = [];

        if (metrics.sharpeRatio > 2) {
            actions.push('AUMENTAR_ALOCAÇÃO');
        }

        if (metrics.maxDrawdownPercent > 15) {
            actions.push('REDUZIR_EXPOSIÇÃO');
        }

        if (metrics.winRate > 55 && metrics.profitFactor > 1.8) {
            actions.push('MANTER_ESTRATÉGIA');
        }

        if (metrics.totalReturn < -5) {
            actions.push('REAVALIAR_ESTRATÉGIA');
        }

        return actions;
    }

    async optimizeStrategy(strategy, marketData, paramSpace) {
        console.log(`⚙️  Otimizando estratégia ${strategy.name}...`);

        const optimizationResults = [];
        const bestResults = {
            sharpeRatio: -Infinity,
            metrics: null,
            parameters: null
        };

        // Busca em grade (grid search) simplificada
        for (const params of this.generateParameterCombinations(paramSpace)) {
            const optimizedStrategy = { ...strategy, config: { ...strategy.config, ...params } };

            const result = await this.backtest(optimizedStrategy, marketData, {
                timeframe: strategy.timeframe
            });

            optimizationResults.push({
                parameters: params,
                metrics: result.metrics
            });

            if (result.metrics.sharpeRatio > bestResults.sharpeRatio) {
                bestResults.sharpeRatio = result.metrics.sharpeRatio;
                bestResults.metrics = result.metrics;
                bestResults.parameters = params;
            }
        }

        return {
            bestParameters: bestResults.parameters,
            bestMetrics: bestResults.metrics,
            allResults: optimizationResults,
            optimizationSurface: this.createOptimizationSurface(optimizationResults)
        };
    }

    generateParameterCombinations(paramSpace) {
        const combinations = [];
        const keys = Object.keys(paramSpace);

        function generate(index, current) {
            if (index === keys.length) {
                combinations.push({ ...current });
                return;
            }

            const key = keys[index];
            const values = paramSpace[key];

            for (const value of values) {
                current[key] = value;
                generate(index + 1, current);
            }
        }

        generate(0, {});
        return combinations;
    }

    createOptimizationSurface(optimizationResults) {
        // Criar superfície de otimização para visualização
        return optimizationResults.map(result => ({
            parameters: result.parameters,
            sharpeRatio: result.metrics.sharpeRatio,
            totalReturn: result.metrics.totalReturn,
            maxDrawdown: result.metrics.maxDrawdownPercent
        }));
    }
}

export class StrategySignal {
    constructor(config = {}) {
        this.config = {
            entryThreshold: config.entryThreshold || 0.02,
            exitThreshold: config.exitThreshold || 0.01,
            stopLoss: config.stopLoss || 0.03,
            takeProfit: config.takeProfit || 0.05,
            timeExit: config.timeExit || 24 * 60 * 60 * 1000, // 24h em ms
            useTrailingStop: config.useTrailingStop !== false,
            usePyramiding: config.usePyramiding || false,
            maxPositions: config.maxPositions || 1,
            ...config
        };

        this.signals = [];
        this.confirmationIndicators = [];
    }

    async generate(symbol, marketData, aiPrediction, context) {
        const baseSignal = await this.calculateBaseSignal(marketData);
        const aiEnhanced = await this.enhanceWithAI(baseSignal, aiPrediction);
        const contextAdjusted = await this.adjustForContext(aiEnhanced, context);
        const riskAdjusted = await this.applyRiskManagement(contextAdjusted, marketData);

        const finalSignal = {
            ...riskAdjusted,
            symbol,
            timestamp: new Date(),
            signalId: `signal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            strength: this.calculateSignalStrength(riskAdjusted),
            confidence: this.calculateSignalConfidence(riskAdjusted, aiPrediction),
            metadata: {
                marketData: this.extractMetadata(marketData),
                aiPrediction,
                context
            }
        };

        this.signals.push(finalSignal);
        return finalSignal;
    }

    async calculateBaseSignal(marketData) {
        // Lógica base de sinal (exemplo: crossover de médias móveis)
        const maShort = this.calculateMA(marketData.close, 9);
        const maLong = this.calculateMA(marketData.close, 21);

        const lastPrice = marketData.close[marketData.close.length - 1];
        const diff = (maShort - maLong) / lastPrice;

        let action = 'HOLD';
        if (diff > this.config.entryThreshold) {
            action = 'BUY';
        } else if (diff < -this.config.entryThreshold) {
            action = 'SELL';
        }

        return {
            action,
            strength: Math.abs(diff),
            priceLevels: {
                entry: lastPrice,
                stopLoss: action === 'BUY' ?
                    lastPrice * (1 - this.config.stopLoss) :
                    lastPrice * (1 + this.config.stopLoss),
                takeProfit: action === 'BUY' ?
                    lastPrice * (1 + this.config.takeProfit) :
                    lastPrice * (1 - this.config.takeProfit)
            },
            rationale: `MA Crossover: ${maShort.toFixed(4)} vs ${maLong.toFixed(4)}`
        };
    }

    calculateMA(prices, period) {
        if (prices.length < period) return prices[prices.length - 1] || 0;
        const slice = prices.slice(-period);
        return slice.reduce((a, b) => a + b, 0) / period;
    }

    async enhanceWithAI(baseSignal, aiPrediction) {
        if (!aiPrediction || baseSignal.action === 'HOLD') {
            return baseSignal;
        }

        // Ajustar sinal baseado na previsão de IA
        const aiDirection = Math.sign(aiPrediction.prediction || 0);
        const signalDirection = baseSignal.action === 'BUY' ? 1 : -1;

        let enhancedAction = baseSignal.action;
        let enhancedStrength = baseSignal.strength;

        if (aiDirection === signalDirection) {
            // Confirmação da IA - fortalecer sinal
            enhancedStrength *= 1.5;
        } else if (Math.abs(aiPrediction.prediction) > 0.03) {
            // Conflito forte com IA - enfraquecer sinal
            enhancedStrength *= 0.5;
            if (enhancedStrength < this.config.entryThreshold * 0.5) {
                enhancedAction = 'HOLD';
            }
        }

        return {
            ...baseSignal,
            action: enhancedAction,
            strength: enhancedStrength,
            aiConfirmation: aiDirection === signalDirection ? 'CONFIRMED' : 'CONFLICT',
            aiWeight: Math.abs(aiPrediction.prediction) * (aiPrediction.confidence || 0.5)
        };
    }

    async adjustForContext(signal, context) {
        if (signal.action === 'HOLD') return signal;

        let adjustedStrength = signal.strength;

        // Ajustar por volatilidade
        if (context.volatility > 0.03) {
            adjustedStrength *= 0.7; // Reduzir força em alta volatilidade
        }

        // Ajustar por liquidez
        if (context.liquidity === 'low') {
            adjustedStrength *= 0.8;
        }

        // Ajustar por regime de mercado
        if (context.regime === MarketRegime.TRENDING_UP && signal.action === 'BUY') {
            adjustedStrength *= 1.2;
        } else if (context.regime === MarketRegime.TRENDING_DOWN && signal.action === 'SELL') {
            adjustedStrength *= 1.2;
        }

        return {
            ...signal,
            strength: adjustedStrength,
            contextAdjustments: {
                volatility: context.volatility,
                liquidity: context.liquidity,
                regime: context.regime
            }
        };
    }

    async applyRiskManagement(signal, marketData) {
        if (signal.action === 'HOLD') return signal;

        // Ajustar stop-loss baseado em ATR
        const atr = this.calculateATR(marketData);
        const dynamicStopLoss = atr * 2;

        // Ajustar take-profit baseado em relação risco/retorno
        const riskRewardRatio = 2; // Alvo 2:1
        const dynamicTakeProfit = dynamicStopLoss * riskRewardRatio;

        return {
            ...signal,
            priceLevels: {
                ...signal.priceLevels,
                stopLoss: signal.action === 'BUY' ?
                    marketData.close * (1 - dynamicStopLoss) :
                    marketData.close * (1 + dynamicStopLoss),
                takeProfit: signal.action === 'BUY' ?
                    marketData.close * (1 + dynamicTakeProfit) :
                    marketData.close * (1 - dynamicTakeProfit)
            },
            riskMetrics: {
                atr,
                riskRewardRatio,
                volatility: this.calculateVolatility(marketData.close)
            }
        };
    }

    calculateATR(marketData, period = 14) {
        const highs = marketData.high || [];
        const lows = marketData.low || [];
        const closes = marketData.close || [];

        if (highs.length < period || lows.length < period || closes.length < period) {
            return 0.01; // Valor padrão
        }

        let trueRanges = [];
        for (let i = 1; i < period; i++) {
            const high = highs[i];
            const low = lows[i];
            const prevClose = closes[i - 1];

            const tr1 = high - low;
            const tr2 = Math.abs(high - prevClose);
            const tr3 = Math.abs(low - prevClose);

            trueRanges.push(Math.max(tr1, tr2, tr3));
        }

        return trueRanges.reduce((a, b) => a + b, 0) / trueRanges.length;
    }

    calculateVolatility(prices) {
        if (prices.length < 2) return 0;
        const returns = [];
        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
        }
        const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - mean, 2), 0) / returns.length;
        return Math.sqrt(variance);
    }

    calculateSignalStrength(signal) {
        if (signal.action === 'HOLD') return SignalStrength.VERY_WEAK;

        const baseStrength = signal.strength || 0;
        const aiWeight = signal.aiWeight || 0.5;
        const contextFactor = signal.contextAdjustments ? 0.8 : 1.0;

        const combinedStrength = baseStrength * aiWeight * contextFactor;

        if (combinedStrength > 0.08) return SignalStrength.VERY_STRONG;
        if (combinedStrength > 0.06) return SignalStrength.STRONG;
        if (combinedStrength > 0.04) return SignalStrength.MODERATE;
        if (combinedStrength > 0.02) return SignalStrength.WEAK;
        return SignalStrength.VERY_WEAK;
    }

    calculateSignalConfidence(signal, aiPrediction) {
        let confidence = 0.5; // Base

        // Fatores de confiança
        if (signal.aiConfirmation === 'CONFIRMED') confidence += 0.2;
        if (signal.strength > 0.05) confidence += 0.15;
        if (aiPrediction?.confidence > 0.7) confidence += 0.1;

        // Penalidades
        if (signal.contextAdjustments?.volatility > 0.03) confidence -= 0.1;
        if (signal.contextAdjustments?.liquidity === 'low') confidence -= 0.05;

        return Math.max(0.1, Math.min(0.95, confidence));
    }

    extractMetadata(marketData) {
        return {
            price: marketData.close,
            volume: marketData.volume,
            rsi: this.calculateRSI(marketData.close),
            macd: this.calculateMACD(marketData.close),
            bollingerBands: this.calculateBollingerBands(marketData.close)
        };
    }

    calculateRSI(prices, period = 14) {
        if (prices.length < period + 1) return 50;

        let gains = 0;
        let losses = 0;

        for (let i = 1; i <= period; i++) {
            const change = prices[i] - prices[i - 1];
            if (change > 0) gains += change;
            else losses -= change;
        }

        const avgGain = gains / period;
        const avgLoss = losses / period;
        const rs = avgGain / (avgLoss || 1);

        return 100 - (100 / (1 + rs));
    }

    calculateMACD(prices) {
        // Implementação simplificada do MACD
        const ema12 = this.calculateEMA(prices, 12);
        const ema26 = this.calculateEMA(prices, 26);
        const macdLine = ema12 - ema26;
        const signalLine = this.calculateEMA(prices.map((_, i) => macdLine), 9);

        return {
            macdLine,
            signalLine,
            histogram: macdLine - signalLine
        };
    }

    calculateEMA(prices, period) {
        if (prices.length < period) return prices[prices.length - 1] || 0;

        const multiplier = 2 / (period + 1);
        let ema = prices[0];

        for (let i = 1; i < prices.length; i++) {
            ema = (prices[i] - ema) * multiplier + ema;
        }

        return ema;
    }

    calculateBollingerBands(prices, period = 20, stdDev = 2) {
        if (prices.length < period) {
            const lastPrice = prices[prices.length - 1] || 0;
            return {
                upper: lastPrice,
                middle: lastPrice,
                lower: lastPrice
            };
        }

        const slice = prices.slice(-period);
        const middle = slice.reduce((a, b) => a + b, 0) / period;
        const variance = slice.reduce((sum, price) => sum + Math.pow(price - middle, 2), 0) / period;
        const std = Math.sqrt(variance);

        return {
            upper: middle + (std * stdDev),
            middle,
            lower: middle - (std * stdDev)
        };
    }
}

export class StrategyManager {
    constructor(config = {}) {
        this.config = {
            maxActiveStrategies: config.maxActiveStrategies || 10,
            autoOptimization: config.autoOptimization !== false,
            riskManagement: config.riskManagement !== false,
            performanceMonitoring: config.performanceMonitoring !== false,
            ...config
        };

        this.activeStrategies = new Map();
        this.strategyRegistry = new Map();
        this.strategyPerformance = new Map();
        this.positionSizing = new PositionSizing();
        this.backtester = new StrategyBacktester();
        this.strategySignals = new Map();
        this.strategyQueue = [];
        this.riskLimits = new Map();

        this.performanceHistory = [];
        this.signalHistory = [];
        this.positionHistory = [];

        console.log('📈 Strategy Manager inicializado');
    }

    async initialize() {
        console.log('🚀 Inicializando Strategy Manager...');

        // Inicializar estratégias padrão
        await this.initializeDefaultStrategies();

        // Iniciar monitoramento de performance
        if (this.config.performanceMonitoring) {
            this.startPerformanceMonitoring();
        }

        // Iniciar otimização automática
        if (this.config.autoOptimization) {
            this.startAutoOptimization();
        }

        console.log('✅ Strategy Manager inicializado');
    }

    async initializeDefaultStrategies() {
        // Estratégia de Trend Following
        const trendFollowing = await this.createTrendFollowingStrategy();
        this.registerStrategy(trendFollowing);

        // Estratégia de Mean Reversion
        const meanReversion = await this.createMeanReversionStrategy();
        this.registerStrategy(meanReversion);

        // Estratégia de Breakout
        const breakout = await this.createBreakoutStrategy();
        this.registerStrategy(breakout);

        console.log(`✅ ${this.strategyRegistry.size} estratégias padrão inicializadas`);
    }

    async createTrendFollowingStrategy() {
        const strategy = {
            id: `trend_following_${Date.now()}`,
            name: 'Trend Following v1.0',
            type: StrategyType.TREND_FOLLOWING,
            timeframe: Timeframe.ONE_HOUR,
            status: StrategyStatus.ACTIVE,
            config: {
                maShortPeriod: 9,
                maLongPeriod: 21,
                entryThreshold: 0.015,
                stopLoss: 0.02,
                takeProfit: 0.04,
                useTrailingStop: true,
                trailingStopDistance: 0.01,
                riskPerTrade: 0.02
            },
            symbols: ['EUR/USD', 'GBP/USD', 'USD/JPY'],

            async generateSignal(marketData, currentPosition) {
                const maShort = this.calculateMA(marketData.close, this.config.maShortPeriod);
                const maLong = this.calculateMA(marketData.close, this.config.maLongPeriod);
                const lastPrice = marketData.close[marketData.close.length - 1];

                let action = 'HOLD';
                let strength = 0;

                if (maShort > maLong * (1 + this.config.entryThreshold)) {
                    action = 'BUY';
                    strength = (maShort - maLong) / lastPrice;
                } else if (maShort < maLong * (1 - this.config.entryThreshold)) {
                    action = 'SELL';
                    strength = (maLong - maShort) / lastPrice;
                }

                // Verificar se já temos posição
                if (currentPosition) {
                    if (currentPosition.direction === 'LONG' && action === 'SELL') {
                        action = 'CLOSE_LONG';
                    } else if (currentPosition.direction === 'SHORT' && action === 'BUY') {
                        action = 'CLOSE_SHORT';
                    }
                }

                return {
                    action,
                    strength,
                    price: lastPrice,
                    rationale: `MA Crossover: ${maShort.toFixed(4)} vs ${maLong.toFixed(4)}`,
                    confidence: Math.min(strength * 10, 0.9)
                };
            },

            calculateMA(prices, period) {
                if (prices.length < period) return prices[prices.length - 1] || 0;
                const slice = prices.slice(-period);
                return slice.reduce((a, b) => a + b, 0) / period;
            }
        };

        return strategy;
    }

    async createMeanReversionStrategy() {
        const strategy = {
            id: `mean_reversion_${Date.now()}`,
            name: 'Mean Reversion v1.0',
            type: StrategyType.MEAN_REVERSION,
            timeframe: Timeframe.ONE_HOUR,
            status: StrategyStatus.ACTIVE,
            config: {
                lookbackPeriod: 20,
                entryZScore: 2.0,
                exitZScore: 0.5,
                stopLoss: 0.03,
                takeProfit: 0.02,
                maxHoldPeriod: 24 // horas
            },
            symbols: ['EUR/USD', 'GBP/USD', 'USD/CHF'],

            async generateSignal(marketData, currentPosition) {
                const prices = marketData.close;
                if (prices.length < this.config.lookbackPeriod) {
                    return { action: 'HOLD', strength: 0 };
                }

                const recentPrices = prices.slice(-this.config.lookbackPeriod);
                const mean = recentPrices.reduce((a, b) => a + b, 0) / recentPrices.length;
                const std = Math.sqrt(
                    recentPrices.reduce((sum, price) => sum + Math.pow(price - mean, 2), 0) / recentPrices.length
                );

                const lastPrice = prices[prices.length - 1];
                const zScore = (lastPrice - mean) / (std || 1);

                let action = 'HOLD';
                let strength = 0;

                if (zScore > this.config.entryZScore) {
                    action = 'SELL'; // Sobrecomprado
                    strength = zScore;
                } else if (zScore < -this.config.entryZScore) {
                    action = 'BUY'; // Sobreventido
                    strength = -zScore;
                }

                // Verificar saída
                if (currentPosition) {
                    const entryZScore = currentPosition.metadata?.entryZScore || 0;
                    if (Math.abs(zScore) < this.config.exitZScore) {
                        action = currentPosition.direction === 'LONG' ? 'CLOSE_LONG' : 'CLOSE_SHORT';
                    }
                }

                return {
                    action,
                    strength: Math.min(strength / 3, 1),
                    price: lastPrice,
                    rationale: `Z-Score: ${zScore.toFixed(2)} (Mean: ${mean.toFixed(4)}, Std: ${std.toFixed(4)})`,
                    confidence: Math.min(Math.abs(zScore) / 4, 0.9)
                };
            }
        };

        return strategy;
    }

    async createBreakoutStrategy() {
        const strategy = {
            id: `breakout_${Date.now()}`,
            name: 'Breakout v1.0',
            type: StrategyType.BREAKOUT,
            timeframe: Timeframe.FOUR_HOUR,
            status: StrategyStatus.ACTIVE,
            config: {
                consolidationPeriod: 20,
                breakoutThreshold: 0.01,
                stopLoss: 0.015,
                takeProfit: 0.03,
                confirmationBars: 2
            },
            symbols: ['BTC/USD', 'ETH/USD', 'XRP/USD'],

            async generateSignal(marketData, currentPosition) {
                const prices = marketData.close;
                const highs = marketData.high || prices;
                const lows = marketData.low || prices;

                if (prices.length < this.config.consolidationPeriod) {
                    return { action: 'HOLD', strength: 0 };
                }

                // Identificar período de consolidação
                const consolidationPrices = prices.slice(-this.config.consolidationPeriod);
                const consolidationHigh = Math.max(...consolidationPrices);
                const consolidationLow = Math.min(...consolidationPrices);
                const consolidationRange = consolidationHigh - consolidationLow;

                const lastPrice = prices[prices.length - 1];
                const isBreakingOut = lastPrice > consolidationHigh * (1 + this.config.breakoutThreshold);
                const isBreakingDown = lastPrice < consolidationLow * (1 - this.config.breakoutThreshold);

                let action = 'HOLD';
                let strength = 0;

                if (isBreakingOut) {
                    action = 'BUY';
                    strength = (lastPrice - consolidationHigh) / consolidationHigh;
                } else if (isBreakingDown) {
                    action = 'SELL';
                    strength = (consolidationLow - lastPrice) / consolidationLow;
                }

                return {
                    action,
                    strength,
                    price: lastPrice,
                    rationale: `Breakout: ${lastPrice.toFixed(4)} (Range: ${consolidationLow.toFixed(4)}-${consolidationHigh.toFixed(4)})`,
                    confidence: Math.min(strength * 20, 0.9)
                };
            }
        };

        return strategy;
    }

    registerStrategy(strategy) {
        if (this.activeStrategies.size >= this.config.maxActiveStrategies) {
            console.warn(`⚠️ Limite de estratégias ativas atingido (${this.config.maxActiveStrategies})`);
            return false;
        }

        const strategyId = strategy.id || `strategy_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const strategyWithId = { ...strategy, id: strategyId };

        this.activeStrategies.set(strategyId, strategyWithId);
        this.strategyRegistry.set(strategyId, strategy.type);

        // Inicializar performance tracker
        this.strategyPerformance.set(strategyId, {
            totalTrades: 0,
            winningTrades: 0,
            totalPnl: 0,
            currentWinStreak: 0,
            currentLossStreak: 0,
            maxDrawdown: 0,
            sharpeRatio: 0,
            lastSignal: null,
            lastTrade: null
        });

        // Inicializar signal generator
        const signalGenerator = new StrategySignal(strategy.config);
        this.strategySignals.set(strategyId, signalGenerator);

        console.log(`📈 Estratégia ${strategy.name} (${strategyId}) registrada`);
        return strategyId;
    }

    async addStrategy(name, logic, type = StrategyType.HYBRID, config = {}) {
        const strategy = {
            id: `strategy_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            name,
            type,
            timeframe: config.timeframe || Timeframe.ONE_HOUR,
            status: StrategyStatus.ACTIVE,
            config: {
                riskPerTrade: 0.02,
                stopLoss: 0.03,
                takeProfit: 0.05,
                ...config
            },
            symbols: config.symbols || ['EUR/USD'],
            generateSignal: logic
        };

        return this.registerStrategy(strategy);
    }

    async removeStrategy(strategyId) {
        if (this.activeStrategies.has(strategyId)) {
            const strategy = this.activeStrategies.get(strategyId);
            this.activeStrategies.delete(strategyId);
            this.strategyRegistry.delete(strategyId);
            this.strategyPerformance.delete(strategyId);
            this.strategySignals.delete(strategyId);

            console.log(`🗑️  Estratégia ${strategy.name} removida`);
            return true;
        }

        return false;
    }

    disableStrategy(strategyId) {
        const strategy = this.activeStrategies.get(strategyId);
        if (strategy) {
            strategy.status = StrategyStatus.PAUSED;
            console.log(`⏸️  Estratégia ${strategy.name} desativada`);
            return true;
        }
        return false;
    }

    enableStrategy(strategyId) {
        const strategy = this.activeStrategies.get(strategyId);
        if (strategy) {
            strategy.status = StrategyStatus.ACTIVE;
            console.log(`▶️  Estratégia ${strategy.name} ativada`);
            return true;
        }
        return false;
    }

    async getExecutionSignals(symbol, marketData) {
        const signals = [];
        const aiPrediction = await aiSystemManager.predict(symbol, marketData);
        const context = await this.analyzeMarketContext(symbol, marketData);

        for (const [strategyId, strategy] of this.activeStrategies) {
            if (strategy.status !== StrategyStatus.ACTIVE) continue;

            // Verificar se estratégia aplica ao símbolo
            if (!strategy.symbols.includes(symbol)) continue;

            try {
                const signalGenerator = this.strategySignals.get(strategyId);
                const signal = await signalGenerator.generate(symbol, marketData, aiPrediction, context);

                // Aplicar filtro de força mínima
                if (signal.strength !== SignalStrength.VERY_WEAK) {
                    signals.push({
                        strategyId,
                        strategyName: strategy.name,
                        strategyType: strategy.type,
                        ...signal
                    });

                    // Atualizar histórico
                    this.signalHistory.push({
                        timestamp: new Date(),
                        strategyId,
                        symbol,
                        signal,
                        context
                    });
                }
            } catch (error) {
                console.error(`❌ Erro ao gerar sinal para estratégia ${strategy.name}:`, error);
            }
        }

        // Ordenar por força e confiança
        signals.sort((a, b) => {
            const strengthOrder = {
                [SignalStrength.VERY_STRONG]: 5,
                [SignalStrength.STRONG]: 4,
                [SignalStrength.MODERATE]: 3,
                [SignalStrength.WEAK]: 2,
                [SignalStrength.VERY_WEAK]: 1
            };

            const strengthDiff = strengthOrder[b.strength] - strengthOrder[a.strength];
            if (strengthDiff !== 0) return strengthDiff;

            return b.confidence - a.confidence;
        });

        return {
            symbol,
            timestamp: new Date(),
            signals,
            topSignal: signals.length > 0 ? signals[0] : null,
            consensus: this.calculateSignalConsensus(signals),
            marketContext: context
        };
    }

    async analyzeMarketContext(symbol, marketData) {
        return {
            volatility: this.calculateVolatility(marketData.close),
            trend: this.calculateTrend(marketData.close),
            volume: marketData.volume ? marketData.volume[marketData.volume.length - 1] : 0,
            marketHours: this.getMarketHours(),
            economicEvents: await this.checkEconomicEvents(),
            sentiment: await this.getMarketSentiment(symbol)
        };
    }

    calculateVolatility(prices) {
        if (prices.length < 2) return 0;
        const returns = [];
        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
        }
        const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - mean, 2), 0) / returns.length;
        return Math.sqrt(variance);
    }

    calculateTrend(prices) {
        if (prices.length < 20) return 'neutral';
        const recent = prices.slice(-20);
        const first = recent[0];
        const last = recent[recent.length - 1];
        const change = (last - first) / first;

        if (change > 0.02) return 'up';
        if (change < -0.02) return 'down';
        return 'neutral';
    }

    getMarketHours() {
        const now = new Date();
        const hour = now.getUTCHours();

        if (hour >= 13 && hour <= 17) return 'london_ny_overlap';
        if (hour >= 8 && hour <= 12) return 'london_session';
        if (hour >= 13 && hour <= 21) return 'ny_session';
        if (hour >= 22 || hour <= 7) return 'asia_session';
        return 'off_hours';
    }

    async checkEconomicEvents() {
        // Em produção, integrar com API de calendário econômico
        return {
            hasEvents: false,
            impact: 'low'
        };
    }

    async getMarketSentiment(symbol) {
        // Em produção, integrar com API de sentimento
        return {
            overall: 0.5,
            lastUpdated: new Date()
        };
    }

    calculateSignalConsensus(signals) {
        if (signals.length === 0) return 'NEUTRAL';

        const buySignals = signals.filter(s => s.action === 'BUY').length;
        const sellSignals = signals.filter(s => s.action === 'SELL').length;

        if (buySignals > sellSignals * 2) return 'STRONG_BUY';
        if (buySignals > sellSignals) return 'BUY';
        if (sellSignals > buySignals * 2) return 'STRONG_SELL';
        if (sellSignals > buySignals) return 'SELL';
        return 'NEUTRAL';
    }

    async executeTrade(signal, accountBalance, currentPositions) {
        const strategy = this.activeStrategies.get(signal.strategyId);
        if (!strategy) {
            throw new Error(`Estratégia ${signal.strategyId} não encontrada`);
        }

        // Calcular tamanho da posição
        const positionSize = this.positionSizing.calculateSize(
            signal.priceLevels.entry,
            signal.priceLevels.stopLoss,
            accountBalance,
            signal.riskMetrics?.volatility || 0.02,
            this.getStrategyWinRate(signal.strategyId),
            2 // profitLossRatio
        );

        // Verificar limites de risco
        if (!this.checkRiskLimits(signal, positionSize, currentPositions)) {
            throw new Error('Limite de risco excedido');
        }

        // Criar ordem de trade
        const trade = {
            id: `trade_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            timestamp: new Date(),
            strategyId: signal.strategyId,
            strategyName: strategy.name,
            symbol: signal.symbol,
            action: signal.action,
            size: positionSize,
            entryPrice: signal.priceLevels.entry,
            stopLoss: signal.priceLevels.stopLoss,
            takeProfit: signal.priceLevels.takeProfit,
            signalStrength: signal.strength,
            signalConfidence: signal.confidence,
            status: 'PENDING',
            metadata: {
                signalId: signal.signalId,
                rationale: signal.rationale,
                aiConfirmation: signal.aiConfirmation
            }
        };

        // Adicionar à fila de execução
        this.strategyQueue.push(trade);

        // Atualizar histórico
        this.positionHistory.push(trade);

        console.log(`📊 Trade gerado: ${signal.action} ${signal.symbol} @ ${signal.priceLevels.entry}`);

        return trade;
    }

    getStrategyWinRate(strategyId) {
        const performance = this.strategyPerformance.get(strategyId);
        if (!performance || performance.totalTrades === 0) return 0.5;
        return performance.winningTrades / performance.totalTrades;
    }

    checkRiskLimits(signal, positionSize, currentPositions) {
        // Verificar limite por estratégia
        const strategyLimit = this.riskLimits.get(signal.strategyId) || {
            maxPositions: 3,
            maxExposure: 0.3 // 30% do capital
        };

        const currentStrategyPositions = currentPositions.filter(p => p.strategyId === signal.strategyId);
        if (currentStrategyPositions.length >= strategyLimit.maxPositions) {
            return false;
        }

        // Verificar exposição total
        const totalExposure = currentPositions.reduce((sum, pos) => sum + pos.size * pos.entryPrice, 0);
        const newExposure = positionSize * signal.priceLevels.entry;

        if ((totalExposure + newExposure) > strategyLimit.maxExposure) {
            return false;
        }

        return true;
    }

    updateStrategyPerformance(strategyId, tradeResult) {
        const performance = this.strategyPerformance.get(strategyId);
        if (!performance) return;

        performance.totalTrades++;
        performance.totalPnl += tradeResult.pnl || 0;

        if (tradeResult.pnl > 0) {
            performance.winningTrades++;
            performance.currentWinStreak++;
            performance.currentLossStreak = 0;
        } else if (tradeResult.pnl < 0) {
            performance.currentLossStreak++;
            performance.currentWinStreak = 0;
        }

        performance.lastTrade = tradeResult;

        // Atualizar drawdown
        if (tradeResult.pnl < 0 && Math.abs(tradeResult.pnl) > performance.maxDrawdown) {
            performance.maxDrawdown = Math.abs(tradeResult.pnl);
        }

        this.strategyPerformance.set(strategyId, performance);

        // Adicionar ao histórico de performance
        this.performanceHistory.push({
            timestamp: new Date(),
            strategyId,
            tradeResult,
            performance: { ...performance }
        });
    }

    startPerformanceMonitoring() {
        setInterval(() => {
            this.monitorStrategies();
        }, 60000); // A cada minuto
    }

    async monitorStrategies() {
        console.log('📊 Monitorando desempenho das estratégias...');

        for (const [strategyId, strategy] of this.activeStrategies) {
            if (strategy.status !== StrategyStatus.ACTIVE) continue;

            const performance = this.strategyPerformance.get(strategyId);
            if (!performance || performance.totalTrades < 10) continue;

            // Verificar desempenho
            const winRate = performance.winningTrades / performance.totalTrades;
            const avgPnl = performance.totalPnl / performance.totalTrades;

            if (winRate < 0.4 && avgPnl < 0) {
                console.warn(`⚠️  Estratégia ${strategy.name} com desempenho ruim: Win Rate ${(winRate * 100).toFixed(1)}%, PnL Médio ${avgPnl.toFixed(4)}`);

                // Desativar estratégia temporariamente
                if (this.config.autoOptimization) {
                    strategy.status = StrategyStatus.OPTIMIZING;
                    this.optimizeStrategy(strategyId);
                }
            }
        }
    }

    startAutoOptimization() {
        setInterval(() => {
            this.runPeriodicOptimization();
        }, 3600000); // A cada hora
    }

    async runPeriodicOptimization() {
        console.log('⚙️  Executando otimização periódica...');

        for (const [strategyId, strategy] of this.activeStrategies) {
            if (strategy.status === StrategyStatus.ACTIVE) {
                await this.optimizeStrategy(strategyId);
            }
        }
    }

    async optimizeStrategy(strategyId) {
        const strategy = this.activeStrategies.get(strategyId);
        if (!strategy) return;

        console.log(`⚙️  Otimizando estratégia ${strategy.name}...`);

        try {
            // Coletar dados históricos para otimização
            const marketData = await this.fetchHistoricalData(strategy.symbols[0], strategy.timeframe);

            // Espaço de parâmetros para otimização
            const paramSpace = {
                entryThreshold: [0.01, 0.015, 0.02, 0.025],
                stopLoss: [0.02, 0.025, 0.03],
                takeProfit: [0.03, 0.04, 0.05],
                maShortPeriod: [7, 9, 12],
                maLongPeriod: [20, 21, 25]
            };

            const optimizationResult = await this.backtester.optimizeStrategy(
                strategy,
                marketData,
                paramSpace
            );

            // Aplicar parâmetros otimizados
            if (optimizationResult.bestParameters) {
                strategy.config = { ...strategy.config, ...optimizationResult.bestParameters };
                strategy.status = StrategyStatus.ACTIVE;

                console.log(`✅ Estratégia ${strategy.name} otimizada. Novos parâmetros:`, optimizationResult.bestParameters);
            }

        } catch (error) {
            console.error(`❌ Erro ao otimizar estratégia ${strategy.name}:`, error);
            strategy.status = StrategyStatus.ERROR;
        }
    }

    async fetchHistoricalData(symbol, timeframe, limit = 1000) {
        // Em produção, integrar com API de dados históricos
        return {
            timestamp: Array.from({ length: limit }, (_, i) => Date.now() - i * 3600000),
            open: Array.from({ length: limit }, () => 1 + Math.random() * 0.1),
            high: Array.from({ length: limit }, () => 1 + Math.random() * 0.12),
            low: Array.from({ length: limit }, () => 0.9 + Math.random() * 0.1),
            close: Array.from({ length: limit }, () => 1 + Math.random() * 0.1),
            volume: Array.from({ length: limit }, () => Math.random() * 1000000)
        };
    }

    async backtestStrategy(strategyId, marketData, config = {}) {
        const strategy = this.activeStrategies.get(strategyId);
        if (!strategy) {
            throw new Error(`Estratégia ${strategyId} não encontrada`);
        }

        return await this.backtester.backtest(strategy, marketData, config);
    }

    getStrategyMetrics(strategyId) {
        const strategy = this.activeStrategies.get(strategyId);
        if (!strategy) return null;

        const performance = this.strategyPerformance.get(strategyId);
        const signals = this.signalHistory.filter(s => s.strategyId === strategyId);

        return {
            strategyInfo: {
                id: strategy.id,
                name: strategy.name,
                type: strategy.type,
                timeframe: strategy.timeframe,
                status: strategy.status,
                symbols: strategy.symbols
            },
            performance: performance || {
                totalTrades: 0,
                winningTrades: 0,
                totalPnl: 0,
                currentWinStreak: 0,
                currentLossStreak: 0,
                maxDrawdown: 0
            },
            signals: {
                total: signals.length,
                recent: signals.slice(-10),
                distribution: this.getSignalDistribution(signals)
            },
            configuration: strategy.config
        };
    }

    getSignalDistribution(signals) {
        const distribution = {
            BUY: 0,
            SELL: 0,
            HOLD: 0
        };

        signals.forEach(signal => {
            distribution[signal.signal.action] = (distribution[signal.signal.action] || 0) + 1;
        });

        return distribution;
    }

    listStrategies() {
        return Array.from(this.activeStrategies.values()).map(strategy => ({
            id: strategy.id,
            name: strategy.name,
            type: strategy.type,
            timeframe: strategy.timeframe,
            status: strategy.status,
            symbols: strategy.symbols,
            performance: this.strategyPerformance.get(strategy.id) || {},
            config: strategy.config
        }));
    }

    getSystemStatus() {
        return {
            totalStrategies: this.activeStrategies.size,
            activeStrategies: Array.from(this.activeStrategies.values()).filter(s => s.status === StrategyStatus.ACTIVE).length,
            totalSignals: this.signalHistory.length,
            totalTrades: this.positionHistory.length,
            performanceMetrics: this.calculateOverallPerformance(),
            riskMetrics: this.calculateSystemRiskMetrics()
        };
    }

    calculateOverallPerformance() {
        let totalTrades = 0;
        let totalPnl = 0;
        let winningTrades = 0;

        for (const performance of this.strategyPerformance.values()) {
            totalTrades += performance.totalTrades;
            totalPnl += performance.totalPnl;
            winningTrades += performance.winningTrades;
        }

        return {
            totalTrades,
            totalPnl,
            winRate: totalTrades > 0 ? winningTrades / totalTrades : 0,
            avgPnl: totalTrades > 0 ? totalPnl / totalTrades : 0,
            sharpeRatio: this.calculateSharpeRatio()
        };
    }

    calculateSharpeRatio() {
        // Cálculo simplificado do Sharpe Ratio
        return 1.5; // Placeholder
    }

    calculateSystemRiskMetrics() {
        const positions = this.positionHistory.filter(p => p.status === 'OPEN');

        return {
            totalExposure: positions.reduce((sum, pos) => sum + pos.size * pos.entryPrice, 0),
            maxPositionSize: Math.max(...positions.map(p => p.size * p.entryPrice), 0),
            openPositions: positions.length,
            avgStopLossDistance: positions.reduce((sum, pos) => {
                const distance = Math.abs(pos.entryPrice - pos.stopLoss) / pos.entryPrice;
                return sum + distance;
            }, 0) / (positions.length || 1),
            concentrationRisk: this.calculateConcentrationRisk(positions)
        };
    }

    calculateConcentrationRisk(positions) {
        if (positions.length === 0) return 0;

        const symbols = positions.map(p => p.symbol);
        const uniqueSymbols = new Set(symbols).size;

        return positions.length / uniqueSymbols; // Quanto maior, mais concentrado
    }

    async resetSystem() {
        console.log('🔄 Resetando Strategy Manager...');

        this.activeStrategies.clear();
        this.strategyRegistry.clear();
        this.strategyPerformance.clear();
        this.strategySignals.clear();
        this.strategyQueue = [];
        this.performanceHistory = [];
        this.signalHistory = [];
        this.positionHistory = [];

        // Reinicializar estratégias padrão
        await this.initializeDefaultStrategies();

        console.log('✅ Strategy Manager resetado');
        return this.getSystemStatus();
    }
}

// Exportar instância singleton
const strategyManager = new StrategyManager();

export default strategyManager;