/**
 * Decision Orchestrator v5.0 - Sistema Avançado de Orquestração de Decisões
 * Sistema neural de tomada de decisão multi-vetorial com aprendizado contínuo
 */

import { AdvancedTemporalNetwork } from './advanced_temporal_network.js';
import { aiSystemManager } from './ai_system_manager.js';
import { strategyManager } from './strategy_manager.js';
import {
    AlgorithmType,
    Decision,
    DecisionConfidence,
    MarketRegime,
    Timeframe,
    RiskLevel,
    NodeStatus,
    EnumUtils
} from './algorithm_constants.js';

export class DecisionVector {
    constructor(config = {}) {
        this.config = {
            weight: config.weight || 1.0,
            threshold: config.threshold || 0.5,
            enabled: config.enabled !== false,
            adaptive: config.adaptive !== false,
            priority: config.priority || 1,
            ...config
        };

        this.history = [];
        this.performance = {
            accuracy: 0.5,
            recall: 0.5,
            precision: 0.5,
            f1Score: 0.5,
            totalDecisions: 0,
            correctDecisions: 0
        };

        this.vectorType = config.type || 'GENERIC';
        this.lastDecision = null;
        this.adaptationRate = 0.01;
    }

    async analyze(input, context) {
        const startTime = Date.now();

        try {
            const analysis = await this.performAnalysis(input, context);
            const decision = this.generateDecision(analysis, context);
            const confidence = this.calculateConfidence(analysis, context);

            const result = {
                vectorType: this.vectorType,
                decision,
                confidence,
                analysis,
                metadata: {
                    processingTime: Date.now() - startTime,
                    timestamp: new Date(),
                    inputHash: this.hashInput(input),
                    context: this.sanitizeContext(context)
                }
            };

            this.recordDecision(result);
            return result;

        } catch (error) {
            console.error(`❌ Erro no vetor ${this.vectorType}:`, error);
            return this.getFallbackDecision();
        }
    }

    async performAnalysis(input, context) {
        // Método abstrato - implementado por subclasses
        throw new Error('Método performAnalysis deve ser implementado');
    }

    generateDecision(analysis, context) {
        // Método abstrato - implementado por subclasses
        throw new Error('Método generateDecision deve ser implementado');
    }

    calculateConfidence(analysis, context) {
        // Base confidence calculation
        let confidence = 0.5;

        // Adjust based on market conditions
        if (context.marketRegime) {
            const regime = EnumUtils.getMarketRegimeByCode(context.marketRegime);
            if (regime) {
                confidence *= regime.probability || 0.6;
            }
        }

        // Adjust based on volatility
        if (context.volatility) {
            if (context.volatility > 0.03) confidence *= 0.8;
            if (context.volatility < 0.01) confidence *= 1.2;
        }

        // Adjust based on data quality
        if (context.dataQuality) {
            confidence *= context.dataQuality;
        }

        return Math.max(0.1, Math.min(0.99, confidence));
    }

    recordDecision(result) {
        this.history.push(result);

        // Keep history limited
        if (this.history.length > 1000) {
            this.history = this.history.slice(-500);
        }

        this.lastDecision = result;
    }

    updatePerformance(actualOutcome) {
        if (!this.lastDecision) return;

        this.performance.totalDecisions++;

        const wasCorrect = this.evaluateDecisionCorrectness(
            this.lastDecision.decision,
            actualOutcome
        );

        if (wasCorrect) {
            this.performance.correctDecisions++;
        }

        // Update metrics
        this.performance.accuracy = this.performance.correctDecisions / this.performance.totalDecisions;

        // Adaptive weight adjustment
        if (this.config.adaptive) {
            this.adaptWeight(wasCorrect);
        }
    }

    evaluateDecisionCorrectness(predicted, actual) {
        // Simplified evaluation - extend based on decision type
        if (typeof predicted === 'object' && predicted.code) {
            return predicted.code === actual.code;
        }
        return predicted === actual;
    }

    adaptWeight(wasCorrect) {
        if (wasCorrect) {
            this.config.weight += this.adaptationRate;
        } else {
            this.config.weight -= this.adaptationRate * 2; // Penalize errors more
        }

        // Bound weight
        this.config.weight = Math.max(0.1, Math.min(2.0, this.config.weight));
    }

    hashInput(input) {
        // Simple hash for tracking
        return JSON.stringify(input).split('').reduce((a, b) => {
            a = ((a << 5) - a) + b.charCodeAt(0);
            return a & a;
        }, 0);
    }

    sanitizeContext(context) {
        // Remove sensitive or large data
        const sanitized = { ...context };
        delete sanitized.rawData;
        delete sanitized.internalState;
        delete sanitized.userData;
        return sanitized;
    }

    getFallbackDecision() {
        return {
            vectorType: this.vectorType,
            decision: Decision.HOLD,
            confidence: 0.1,
            analysis: { fallback: true, reason: 'vector_failure' },
            metadata: {
                processingTime: 0,
                timestamp: new Date(),
                error: true
            }
        };
    }

    getMetrics() {
        return {
            type: this.vectorType,
            weight: this.config.weight,
            performance: { ...this.performance },
            historySize: this.history.length,
            lastDecisionTime: this.lastDecision?.metadata.timestamp,
            enabled: this.config.enabled
        };
    }

    reset() {
        this.history = [];
        this.performance = {
            accuracy: 0.5,
            recall: 0.5,
            precision: 0.5,
            f1Score: 0.5,
            totalDecisions: 0,
            correctDecisions: 0
        };
        this.config.weight = 1.0;
    }
}

export class TemporalVector extends DecisionVector {
    constructor(config = {}) {
        super({
            type: 'TEMPORAL',
            weight: 1.2,
            threshold: 0.6,
            adaptive: true,
            ...config
        });

        this.temporalNetwork = new AdvancedTemporalNetwork({
            sequenceLength: 60,
            hiddenSize: 128,
            memorySize: 256
        });

        this.patterns = new Map();
        this.sequenceBuffer = [];
        this.maxSequenceLength = 100;
    }

    async performAnalysis(input, context) {
        const { marketData, historicalData } = input;

        // Update sequence buffer
        this.updateSequenceBuffer(marketData);

        // Analyze temporal patterns
        const temporalAnalysis = await this.analyzeTemporalPatterns();

        // Get predictions from temporal network
        const predictions = await this.temporalNetwork.process({
            sequence: this.sequenceBuffer,
            context: context.marketRegime
        });

        // Identify cyclic patterns
        const cycles = this.detectCycles();

        // Calculate momentum
        const momentum = this.calculateMomentum();

        // Analyze trend persistence
        const trendPersistence = this.analyzeTrendPersistence();

        return {
            predictions,
            temporalAnalysis,
            cycles,
            momentum,
            trendPersistence,
            sequenceLength: this.sequenceBuffer.length,
            volatility: this.calculateVolatility()
        };
    }

    generateDecision(analysis, context) {
        const { predictions, momentum, trendPersistence } = analysis;

        if (!predictions || !predictions.horizons) {
            return Decision.HOLD;
        }

        const shortTerm = predictions.horizons.intraday;
        const mediumTerm = predictions.horizons.short_term;

        // Decision logic based on temporal analysis
        if (trendPersistence.strength > 0.7 && momentum > 0) {
            if (shortTerm.prediction > 0.02 && shortTerm.confidence > 0.7) {
                return Decision.BUY;
            }
        } else if (trendPersistence.strength > 0.7 && momentum < 0) {
            if (shortTerm.prediction < -0.02 && shortTerm.confidence > 0.7) {
                return Decision.SELL;
            }
        }

        // Check for trend reversals
        if (trendPersistence.isReversing && Math.abs(momentum) > 0.03) {
            if (momentum > 0) {
                return Decision.BUY;
            } else {
                return Decision.SELL;
            }
        }

        // Check for consolidation breakout
        if (trendPersistence.consolidation && Math.abs(momentum) > 0.04) {
            return momentum > 0 ? Decision.BUY : Decision.SELL;
        }

        return Decision.HOLD;
    }

    updateSequenceBuffer(marketData) {
        const snapshot = {
            timestamp: new Date(),
            price: marketData.close,
            volume: marketData.volume,
            high: marketData.high,
            low: marketData.low,
            indicators: this.calculateIndicators(marketData)
        };

        this.sequenceBuffer.push(snapshot);

        // Keep buffer size limited
        if (this.sequenceBuffer.length > this.maxSequenceLength) {
            this.sequenceBuffer = this.sequenceBuffer.slice(-this.maxSequenceLength);
        }
    }

    async analyzeTemporalPatterns() {
        if (this.sequenceBuffer.length < 20) {
            return { patterns: [], confidence: 0.1 };
        }

        const patterns = [];
        const recentPrices = this.sequenceBuffer.slice(-50).map(s => s.price);

        // Detect common patterns
        patterns.push(...this.detectHeadAndShoulders(recentPrices));
        patterns.push(...this.detectDoubleTopBottom(recentPrices));
        patterns.push(...this.detectTrianglePatterns(recentPrices));

        // Calculate pattern confidence
        const confidence = patterns.length > 0 ?
            patterns.reduce((sum, p) => sum + p.confidence, 0) / patterns.length : 0.1;

        return {
            patterns,
            confidence,
            dominantPattern: patterns.length > 0 ?
                patterns.sort((a, b) => b.confidence - a.confidence)[0] : null
        };
    }

    detectCycles() {
        if (this.sequenceBuffer.length < 100) {
            return { cycles: [], dominantCycle: null };
        }

        const prices = this.sequenceBuffer.map(s => s.price);

        // Simple cycle detection using FFT (simplified)
        const cycles = [];

        // Detect daily cycles
        if (prices.length >= 96) { // 4-hour candles for 24h
            const dailyCycle = this.calculateCycleStrength(prices, 24);
            if (dailyCycle.strength > 0.6) {
                cycles.push({ period: 'DAILY', ...dailyCycle });
            }
        }

        // Detect weekly cycles
        if (prices.length >= 168) { // Hourly candles for 7 days
            const weeklyCycle = this.calculateCycleStrength(prices, 168);
            if (weeklyCycle.strength > 0.6) {
                cycles.push({ period: 'WEEKLY', ...weeklyCycle });
            }
        }

        return {
            cycles,
            dominantCycle: cycles.length > 0 ?
                cycles.sort((a, b) => b.strength - a.strength)[0] : null
        };
    }

    calculateCycleStrength(prices, expectedPeriod) {
        // Simplified cycle strength calculation
        const chunks = [];
        for (let i = 0; i < prices.length - expectedPeriod; i += expectedPeriod) {
            chunks.push(prices.slice(i, i + expectedPeriod));
        }

        if (chunks.length < 2) return { strength: 0, phase: 0 };

        // Calculate correlation between chunks
        let totalCorrelation = 0;
        for (let i = 0; i < chunks.length - 1; i++) {
            for (let j = i + 1; j < chunks.length; j++) {
                totalCorrelation += this.calculateCorrelation(chunks[i], chunks[j]);
            }
        }

        const avgCorrelation = totalCorrelation / (chunks.length * (chunks.length - 1) / 2);

        return {
            strength: Math.max(0, avgCorrelation),
            phase: this.calculatePhase(prices, expectedPeriod)
        };
    }

    calculateCorrelation(arr1, arr2) {
        const n = Math.min(arr1.length, arr2.length);
        if (n < 2) return 0;

        const mean1 = arr1.reduce((a, b) => a + b, 0) / n;
        const mean2 = arr2.reduce((a, b) => a + b, 0) / n;

        let numerator = 0;
        let denom1 = 0;
        let denom2 = 0;

        for (let i = 0; i < n; i++) {
            const dev1 = arr1[i] - mean1;
            const dev2 = arr2[i] - mean2;
            numerator += dev1 * dev2;
            denom1 += dev1 * dev1;
            denom2 += dev2 * dev2;
        }

        return numerator / Math.sqrt(denom1 * denom2);
    }

    calculatePhase(prices, period) {
        if (prices.length < period) return 0;

        const recent = prices.slice(-period);
        const firstHalf = recent.slice(0, Math.floor(period / 2));
        const secondHalf = recent.slice(Math.floor(period / 2));

        const mean1 = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
        const mean2 = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;

        return mean2 > mean1 ? 1 : -1; // 1 = rising phase, -1 = falling phase
    }

    calculateMomentum() {
        if (this.sequenceBuffer.length < 10) return 0;

        const recent = this.sequenceBuffer.slice(-10);
        const first = recent[0].price;
        const last = recent[recent.length - 1].price;

        return (last - first) / first;
    }

    analyzeTrendPersistence() {
        if (this.sequenceBuffer.length < 30) {
            return {
                strength: 0,
                direction: 'NEUTRAL',
                isReversing: false,
                consolidation: false
            };
        }

        const prices = this.sequenceBuffer.map(s => s.price);
        const returns = [];

        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
        }

        // Calculate trend strength
        const positiveReturns = returns.filter(r => r > 0);
        const negativeReturns = returns.filter(r => r < 0);
        const trendStrength = Math.abs(positiveReturns.length - negativeReturns.length) / returns.length;

        // Determine direction
        const direction = positiveReturns.length > negativeReturns.length ? 'UP' :
            negativeReturns.length > positiveReturns.length ? 'DOWN' : 'NEUTRAL';

        // Check for reversal
        const recentReturns = returns.slice(-5);
        const earlyReturns = returns.slice(0, 5);
        const isReversing = Math.sign(recentReturns.reduce((a, b) => a + b, 0)) !==
            Math.sign(earlyReturns.reduce((a, b) => a + b, 0));

        // Check for consolidation
        const volatility = this.calculateVolatility();
        const consolidation = volatility < 0.01 && trendStrength < 0.3;

        return {
            strength: trendStrength,
            direction,
            isReversing,
            consolidation,
            duration: prices.length
        };
    }

    calculateVolatility() {
        if (this.sequenceBuffer.length < 2) return 0;

        const prices = this.sequenceBuffer.map(s => s.price);
        const returns = [];

        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
        }

        const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - mean, 2), 0) / returns.length;

        return Math.sqrt(variance);
    }

    calculateIndicators(marketData) {
        return {
            rsi: this.calculateRSI(marketData.close),
            macd: this.calculateMACD(marketData.close),
            bollinger: this.calculateBollingerBands(marketData.close),
            atr: this.calculateATR(marketData)
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

    calculateATR(marketData, period = 14) {
        const highs = marketData.high || [];
        const lows = marketData.low || [];
        const closes = marketData.close || [];

        if (highs.length < period || lows.length < period || closes.length < period) {
            return 0.01;
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

    detectHeadAndShoulders(prices) {
        // Simplified pattern detection
        const patterns = [];

        if (prices.length < 100) return patterns;

        // Look for head and shoulders pattern
        const middle = Math.floor(prices.length / 2);
        const left = prices.slice(0, middle);
        const right = prices.slice(middle);

        if (left.length >= 40 && right.length >= 40) {
            const leftShoulder = Math.max(...left.slice(0, 20));
            const head = Math.max(...left.slice(20, 40));
            const rightShoulder = Math.max(...right.slice(0, 20));

            if (head > leftShoulder && head > rightShoulder &&
                Math.abs(leftShoulder - rightShoulder) / head < 0.05) {
                patterns.push({
                    type: 'HEAD_AND_SHOULDERS',
                    confidence: 0.7,
                    direction: 'BEARISH'
                });
            }
        }

        return patterns;
    }

    detectDoubleTopBottom(prices) {
        const patterns = [];

        if (prices.length < 80) return patterns;

        // Look for double top
        const firstHalf = prices.slice(0, 40);
        const secondHalf = prices.slice(40, 80);

        const firstTop = Math.max(...firstHalf);
        const secondTop = Math.max(...secondHalf);

        if (Math.abs(firstTop - secondTop) / firstTop < 0.02) {
            patterns.push({
                type: 'DOUBLE_TOP',
                confidence: 0.6,
                direction: 'BEARISH'
            });
        }

        // Look for double bottom
        const firstBottom = Math.min(...firstHalf);
        const secondBottom = Math.min(...secondHalf);

        if (Math.abs(firstBottom - secondBottom) / firstBottom < 0.02) {
            patterns.push({
                type: 'DOUBLE_BOTTOM',
                confidence: 0.6,
                direction: 'BULLISH'
            });
        }

        return patterns;
    }

    detectTrianglePatterns(prices) {
        const patterns = [];

        if (prices.length < 60) return patterns;

        // Simple triangle detection
        const highs = [];
        const lows = [];

        for (let i = 0; i < prices.length; i += 10) {
            const chunk = prices.slice(i, i + 10);
            highs.push(Math.max(...chunk));
            lows.push(Math.min(...chunk));
        }

        // Check for converging highs and lows
        const highDiff = Math.abs(highs[0] - highs[highs.length - 1]) / highs[0];
        const lowDiff = Math.abs(lows[0] - lows[lows.length - 1]) / lows[0];

        if (highDiff < 0.05 && lowDiff < 0.05) {
            patterns.push({
                type: 'SYMMETRICAL_TRIANGLE',
                confidence: 0.5,
                direction: 'NEUTRAL'
            });
        }

        return patterns;
    }
}

export class AIStrategyVector extends DecisionVector {
    constructor(config = {}) {
        super({
            type: 'AI_STRATEGY',
            weight: 1.5,
            threshold: 0.65,
            adaptive: true,
            priority: 2,
            ...config
        });

        this.aiManager = aiSystemManager;
        this.strategyManager = strategyManager;
        this.strategyCache = new Map();
        this.signalCache = new Map();
        this.cacheTTL = 30000; // 30 seconds
    }

    async performAnalysis(input, context) {
        const { symbol, marketData, strategies } = input;

        // Get AI predictions
        const aiPrediction = await this.getAIPrediction(symbol, marketData);

        // Get strategy signals
        const strategySignals = await this.getStrategySignals(symbol, marketData, strategies);

        // Analyze consensus
        const consensus = this.analyzeConsensus(strategySignals, aiPrediction);

        // Calculate market context
        const marketContext = await this.analyzeMarketContext(symbol, marketData);

        // Risk assessment
        const riskAssessment = this.assessRisk(strategySignals, marketContext);

        return {
            aiPrediction,
            strategySignals,
            consensus,
            marketContext,
            riskAssessment,
            timestamp: new Date()
        };
    }

    generateDecision(analysis, context) {
        const { aiPrediction, strategySignals, consensus, riskAssessment } = analysis;

        if (!aiPrediction || !strategySignals || strategySignals.length === 0) {
            return Decision.HOLD;
        }

        // Check for strong AI signal
        if (aiPrediction.confidence > 0.8) {
            if (aiPrediction.prediction > 0.03) {
                return Decision.BUY;
            } else if (aiPrediction.prediction < -0.03) {
                return Decision.SELL;
            }
        }

        // Check strategy consensus
        if (consensus.strength > 0.7) {
            if (consensus.direction === 'BULLISH') {
                return Decision.BUY;
            } else if (consensus.direction === 'BEARISH') {
                return Decision.SELL;
            }
        }

        // Check for high-probability setups
        const highProbabilitySignals = strategySignals.filter(s =>
            s.signal.confidence > 0.75 &&
            Math.abs(s.signal.strength) > 0.05
        );

        if (highProbabilitySignals.length > 0) {
            const strongestSignal = highProbabilitySignals.sort((a, b) =>
                b.signal.confidence - a.signal.confidence
            )[0];

            if (strongestSignal.signal.action === 'BUY') {
                return Decision.BUY;
            } else if (strongestSignal.signal.action === 'SELL') {
                return Decision.SELL;
            }
        }

        // Check risk assessment
        if (riskAssessment.overallRisk === 'LOW' && consensus.strength > 0.5) {
            if (consensus.direction === 'BULLISH') {
                return Decision.SCALE_IN;
            } else if (consensus.direction === 'BEARISH') {
                return Decision.SCALE_OUT;
            }
        }

        return Decision.HOLD;
    }

    async getAIPrediction(symbol, marketData) {
        const cacheKey = `ai_${symbol}_${Date.now() / 60000 | 0}`; // Cache per minute

        if (this.signalCache.has(cacheKey)) {
            const cached = this.signalCache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTTL) {
                return cached.data;
            }
        }

        try {
            const prediction = await this.aiManager.predict(symbol, marketData);

            this.signalCache.set(cacheKey, {
                data: prediction,
                timestamp: Date.now()
            });

            // Clean old cache entries
            this.cleanCache();

            return prediction;
        } catch (error) {
            console.error('❌ Erro ao obter predição de IA:', error);
            return {
                prediction: 0,
                confidence: 0.1,
                fallback: true
            };
        }
    }

    async getStrategySignals(symbol, marketData, strategies) {
        const cacheKey = `strategy_${symbol}_${strategies?.join('_') || 'all'}_${Date.now() / 30000 | 0}`;

        if (this.strategyCache.has(cacheKey)) {
            const cached = this.strategyCache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTTL) {
                return cached.data;
            }
        }

        try {
            const signals = await this.strategyManager.getExecutionSignals(symbol, marketData);

            this.strategyCache.set(cacheKey, {
                data: signals.signals || [],
                timestamp: Date.now()
            });

            return signals.signals || [];
        } catch (error) {
            console.error('❌ Erro ao obter sinais de estratégia:', error);
            return [];
        }
    }

    analyzeConsensus(strategySignals, aiPrediction) {
        if (strategySignals.length === 0) {
            return {
                strength: 0,
                direction: 'NEUTRAL',
                agreement: 0,
                signalsCount: 0
            };
        }

        let buyCount = 0;
        let sellCount = 0;
        let holdCount = 0;
        let totalConfidence = 0;

        strategySignals.forEach(signal => {
            if (signal.signal.action === 'BUY') {
                buyCount++;
            } else if (signal.signal.action === 'SELL') {
                sellCount++;
            } else {
                holdCount++;
            }
            totalConfidence += signal.signal.confidence || 0.5;
        });

        // Include AI prediction in consensus
        if (aiPrediction && !aiPrediction.fallback) {
            if (aiPrediction.prediction > 0.01) {
                buyCount += 2; // Weight AI more heavily
            } else if (aiPrediction.prediction < -0.01) {
                sellCount += 2;
            }
            totalConfidence += aiPrediction.confidence || 0.5;
        }

        const totalSignals = buyCount + sellCount + holdCount;
        const agreement = Math.max(buyCount, sellCount) / totalSignals;

        let direction = 'NEUTRAL';
        if (buyCount > sellCount * 1.5) {
            direction = 'BULLISH';
        } else if (sellCount > buyCount * 1.5) {
            direction = 'BEARISH';
        }

        const avgConfidence = totalConfidence / (strategySignals.length + (aiPrediction ? 1 : 0));

        return {
            strength: agreement * avgConfidence,
            direction,
            agreement,
            signalsCount: totalSignals,
            buyCount,
            sellCount,
            holdCount
        };
    }

    async analyzeMarketContext(symbol, marketData) {
        const volatility = this.calculateVolatility(marketData.close);
        const trend = this.calculateTrend(marketData.close);
        const volume = marketData.volume ?
            marketData.volume[marketData.volume.length - 1] : 0;

        // Get market regime from temporal analysis
        let regime = 'SIDEWAYS';
        if (trend.strength > 0.7) {
            regime = trend.direction === 'UP' ? 'TRENDING_UP' : 'TRENDING_DOWN';
        } else if (volatility > 0.03) {
            regime = 'HIGH_VOLATILITY';
        }

        return {
            symbol,
            volatility,
            trend,
            volume,
            regime,
            timestamp: new Date()
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
        if (prices.length < 20) return { strength: 0, direction: 'NEUTRAL' };

        const recent = prices.slice(-20);
        const first = recent[0];
        const last = recent[recent.length - 1];
        const change = (last - first) / first;

        const direction = change > 0.02 ? 'UP' : change < -0.02 ? 'DOWN' : 'NEUTRAL';
        const strength = Math.abs(change) / 0.05; // Normalize

        return {
            strength: Math.min(strength, 1),
            direction,
            change
        };
    }

    assessRisk(strategySignals, marketContext) {
        if (strategySignals.length === 0) {
            return {
                overallRisk: 'MEDIUM',
                reasons: ['NO_SIGNALS'],
                riskScore: 0.5
            };
        }

        let riskScore = 0.5;
        const reasons = [];

        // Adjust based on market volatility
        if (marketContext.volatility > 0.03) {
            riskScore += 0.3;
            reasons.push('HIGH_VOLATILITY');
        }

        // Adjust based on signal dispersion
        const signalDirections = strategySignals.map(s => s.signal.action);
        const uniqueDirections = new Set(signalDirections).size;

        if (uniqueDirections > 2) {
            riskScore += 0.2;
            reasons.push('CONFLICTING_SIGNALS');
        }

        // Adjust based on signal confidence
        const avgConfidence = strategySignals.reduce((sum, s) =>
            sum + (s.signal.confidence || 0.5), 0) / strategySignals.length;

        if (avgConfidence < 0.6) {
            riskScore += 0.2;
            reasons.push('LOW_CONFIDENCE');
        }

        // Determine risk level
        let overallRisk = 'MEDIUM';
        if (riskScore > 0.8) {
            overallRisk = 'VERY_HIGH';
        } else if (riskScore > 0.65) {
            overallRisk = 'HIGH';
        } else if (riskScore > 0.35) {
            overallRisk = 'MEDIUM';
        } else if (riskScore > 0.2) {
            overallRisk = 'LOW';
        } else {
            overallRisk = 'VERY_LOW';
        }

        return {
            overallRisk,
            reasons,
            riskScore,
            volatility: marketContext.volatility,
            signalCount: strategySignals.length,
            avgConfidence
        };
    }

    cleanCache() {
        const now = Date.now();
        for (const [key, value] of this.signalCache.entries()) {
            if (now - value.timestamp > this.cacheTTL * 2) {
                this.signalCache.delete(key);
            }
        }
        for (const [key, value] of this.strategyCache.entries()) {
            if (now - value.timestamp > this.cacheTTL * 2) {
                this.strategyCache.delete(key);
            }
        }
    }
}

export class RiskManagementVector extends DecisionVector {
    constructor(config = {}) {
        super({
            type: 'RISK_MANAGEMENT',
            weight: 2.0, // High weight for risk management
            threshold: 0.3, // Low threshold - always consider risk
            adaptive: true,
            priority: 3, // Highest priority
            ...config
        });

        this.positions = new Map();
        this.riskLimits = {
            maxDrawdown: 0.15,
            maxPositionSize: 0.1,
            maxDailyLoss: 0.05,
            maxConcurrentPositions: 5,
            maxCorrelation: 0.7
        };

        this.riskMetrics = {
            currentDrawdown: 0,
            dailyPnL: 0,
            winRate: 0.5,
            sharpeRatio: 1.0,
            volatility: 0.02
        };

        this.history = [];
    }

    async performAnalysis(input, context) {
        const { currentPositions, accountBalance, marketData, proposedDecision } = input;

        // Update positions
        this.updatePositions(currentPositions);

        // Calculate current risk metrics
        const currentRisk = this.calculateCurrentRisk(accountBalance);

        // Assess proposed decision risk
        const decisionRisk = this.assessDecisionRisk(proposedDecision, marketData, accountBalance);

        // Calculate portfolio risk
        const portfolioRisk = this.calculatePortfolioRisk();

        // Check risk limits
        const limitChecks = this.checkRiskLimits(currentRisk, decisionRisk);

        // Generate risk-adjusted decision
        const riskAdjusted = this.generateRiskAdjustedDecision(
            proposedDecision,
            decisionRisk,
            limitChecks
        );

        return {
            currentRisk,
            decisionRisk,
            portfolioRisk,
            limitChecks,
            riskAdjusted,
            positions: Array.from(this.positions.values()),
            timestamp: new Date()
        };
    }

    generateDecision(analysis, context) {
        const { riskAdjusted, limitChecks, decisionRisk } = analysis;

        // Override with risk management decision
        return riskAdjusted.decision;
    }

    calculateConfidence(analysis, context) {
        const { limitChecks } = analysis;

        // Start with high confidence
        let confidence = 0.9;

        // Reduce confidence for any risk limit violations
        if (limitChecks.violations.length > 0) {
            confidence *= 0.7;
        }

        // Reduce confidence for high risk decisions
        if (analysis.decisionRisk.level === 'HIGH') {
            confidence *= 0.8;
        } else if (analysis.decisionRisk.level === 'VERY_HIGH') {
            confidence *= 0.6;
        }

        // Increase confidence for risk-mitigated decisions
        if (analysis.riskAdjusted.mitigations.length > 0) {
            confidence *= 1.1;
        }

        return Math.max(0.1, Math.min(0.99, confidence));
    }

    updatePositions(positions) {
        this.positions.clear();

        positions.forEach(position => {
            this.positions.set(position.id, {
                ...position,
                timestamp: new Date(),
                currentValue: position.size * position.currentPrice,
                unrealizedPnl: (position.currentPrice - position.entryPrice) * position.size *
                    (position.direction === 'LONG' ? 1 : -1)
            });
        });
    }

    calculateCurrentRisk(accountBalance) {
        const positions = Array.from(this.positions.values());

        if (positions.length === 0) {
            return {
                exposure: 0,
                concentration: 0,
                drawdown: this.riskMetrics.currentDrawdown,
                dailyPnL: this.riskMetrics.dailyPnL,
                riskScore: 0.1
            };
        }

        // Calculate total exposure
        const totalExposure = positions.reduce((sum, pos) =>
            sum + Math.abs(pos.size * pos.currentPrice), 0);

        const exposureRatio = totalExposure / accountBalance;

        // Calculate concentration risk
        const largestPosition = Math.max(...positions.map(p =>
            Math.abs(p.size * p.currentPrice)));
        const concentration = largestPosition / totalExposure;

        // Calculate correlation risk (simplified)
        const correlationRisk = this.calculateCorrelationRisk(positions);

        // Calculate overall risk score
        const riskScore = Math.min(1,
            exposureRatio * 0.4 +
            concentration * 0.3 +
            correlationRisk * 0.2 +
            (this.riskMetrics.currentDrawdown / this.riskLimits.maxDrawdown) * 0.1
        );

        return {
            exposure: exposureRatio,
            concentration,
            correlationRisk,
            drawdown: this.riskMetrics.currentDrawdown,
            dailyPnL: this.riskMetrics.dailyPnL,
            riskScore,
            positions: positions.length
        };
    }

    calculateCorrelationRisk(positions) {
        if (positions.length < 2) return 0;

        // Simplified correlation calculation
        // In production, use actual correlation matrix
        let totalCorrelation = 0;
        let count = 0;

        for (let i = 0; i < positions.length; i++) {
            for (let j = i + 1; j < positions.length; j++) {
                // Assume same asset class = high correlation
                if (positions[i].symbol.split('/')[0] === positions[j].symbol.split('/')[0]) {
                    totalCorrelation += 0.8;
                } else {
                    totalCorrelation += 0.2;
                }
                count++;
            }
        }

        return count > 0 ? totalCorrelation / count : 0;
    }

    assessDecisionRisk(proposedDecision, marketData, accountBalance) {
        if (!proposedDecision || proposedDecision.code === 'HOLD') {
            return {
                level: 'VERY_LOW',
                reasons: ['NO_ACTION'],
                sizeMultiplier: 1.0,
                stopLossAdjustment: 0
            };
        }

        const decision = EnumUtils.getDecisionByCode(proposedDecision.code);
        let riskLevel = 'MEDIUM';
        const reasons = [];
        let sizeMultiplier = 1.0;
        let stopLossAdjustment = 0;

        // Adjust based on decision type
        switch (proposedDecision.code) {
            case 'BUY':
            case 'SELL':
                riskLevel = 'HIGH';
                reasons.push('NEW_POSITION');
                break;
            case 'SCALE_IN':
                riskLevel = 'MEDIUM';
                reasons.push('INCREASING_EXPOSURE');
                sizeMultiplier = 0.5;
                break;
            case 'SCALE_OUT':
                riskLevel = 'LOW';
                reasons.push('REDUCING_EXPOSURE');
                sizeMultiplier = 0.3;
                break;
            case 'REVERSE':
                riskLevel = 'VERY_HIGH';
                reasons.push('POSITION_REVERSAL');
                break;
        }

        // Adjust based on market volatility
        const volatility = this.calculateVolatility(marketData.close);
        if (volatility > 0.03) {
            riskLevel = this.escalateRisk(riskLevel);
            reasons.push('HIGH_VOLATILITY');
            sizeMultiplier *= 0.7;
            stopLossAdjustment = 0.005; // Widen stop loss
        }

        // Adjust based on current drawdown
        if (this.riskMetrics.currentDrawdown > this.riskLimits.maxDrawdown * 0.5) {
            riskLevel = this.escalateRisk(riskLevel);
            reasons.push('ELEVATED_DRAWDOWN');
            sizeMultiplier *= 0.6;
        }

        // Adjust based on daily PnL
        if (this.riskMetrics.dailyPnL < -this.riskLimits.maxDailyLoss * 0.5) {
            riskLevel = this.escalateRisk(riskLevel);
            reasons.push('DAILY_LOSS');
            sizeMultiplier *= 0.5;
        }

        return {
            level: riskLevel,
            reasons,
            sizeMultiplier: Math.max(0.1, sizeMultiplier),
            stopLossAdjustment,
            volatility
        };
    }

    escalateRisk(currentLevel) {
        const levels = ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'];
        const index = levels.indexOf(currentLevel);
        return index < levels.length - 1 ? levels[index + 1] : 'VERY_HIGH';
    }

    calculatePortfolioRisk() {
        const positions = Array.from(this.positions.values());

        if (positions.length === 0) {
            return {
                valueAtRisk: 0,
                expectedShortfall: 0,
                maxLoss: 0,
                diversification: 1.0
            };
        }

        // Simplified VaR calculation
        const totalValue = positions.reduce((sum, pos) => sum + pos.currentValue, 0);
        const volatility = this.riskMetrics.volatility;

        // 95% VaR over 1 day
        const valueAtRisk = totalValue * volatility * 1.645;

        // Expected shortfall (CVaR)
        const expectedShortfall = totalValue * volatility * 2.06;

        // Maximum theoretical loss
        const maxLoss = totalValue * 0.5; // Assume 50% max loss

        // Diversification score
        const uniqueAssets = new Set(positions.map(p => p.symbol)).size;
        const diversification = uniqueAssets / positions.length;

        return {
            valueAtRisk,
            expectedShortfall,
            maxLoss,
            diversification,
            totalValue,
            positionCount: positions.length
        };
    }

    checkRiskLimits(currentRisk, decisionRisk) {
        const violations = [];
        const warnings = [];

        // Check drawdown limit
        if (currentRisk.drawdown > this.riskLimits.maxDrawdown) {
            violations.push({
                limit: 'MAX_DRAWDOWN',
                current: currentRisk.drawdown,
                max: this.riskLimits.maxDrawdown,
                severity: 'CRITICAL'
            });
        } else if (currentRisk.drawdown > this.riskLimits.maxDrawdown * 0.8) {
            warnings.push({
                limit: 'MAX_DRAWDOWN',
                current: currentRisk.drawdown,
                threshold: this.riskLimits.maxDrawdown * 0.8,
                severity: 'WARNING'
            });
        }

        // Check exposure limit
        if (currentRisk.exposure > this.riskLimits.maxPositionSize) {
            violations.push({
                limit: 'MAX_EXPOSURE',
                current: currentRisk.exposure,
                max: this.riskLimits.maxPositionSize,
                severity: 'HIGH'
            });
        }

        // Check position count
        if (currentRisk.positions >= this.riskLimits.maxConcurrentPositions) {
            violations.push({
                limit: 'MAX_POSITIONS',
                current: currentRisk.positions,
                max: this.riskLimits.maxConcurrentPositions,
                severity: 'MEDIUM'
            });
        }

        // Check correlation risk
        if (currentRisk.correlationRisk > this.riskLimits.maxCorrelation) {
            warnings.push({
                limit: 'MAX_CORRELATION',
                current: currentRisk.correlationRisk,
                max: this.riskLimits.maxCorrelation,
                severity: 'MEDIUM'
            });
        }

        // Check decision risk level
        if (decisionRisk.level === 'VERY_HIGH') {
            warnings.push({
                limit: 'DECISION_RISK',
                level: decisionRisk.level,
                severity: 'HIGH'
            });
        }

        return {
            violations,
            warnings,
            passed: violations.length === 0,
            hasWarnings: warnings.length > 0
        };
    }

    generateRiskAdjustedDecision(proposedDecision, decisionRisk, limitChecks) {
        // Start with proposed decision
        let adjustedDecision = { ...proposedDecision };
        const mitigations = [];

        // If there are critical violations, override with HOLD
        if (limitChecks.violations.some(v => v.severity === 'CRITICAL')) {
            adjustedDecision = Decision.HOLD;
            mitigations.push('CRITICAL_RISK_LIMIT_VIOLATION');
            return {
                decision: adjustedDecision,
                mitigations,
                overridden: true,
                reason: 'risk_limit_violation'
            };
        }

        // Adjust position size based on risk
        if (decisionRisk.sizeMultiplier !== 1.0) {
            mitigations.push(`SIZE_ADJUSTMENT:${decisionRisk.sizeMultiplier.toFixed(2)}`);
        }

        // Adjust stop loss if needed
        if (decisionRisk.stopLossAdjustment > 0) {
            mitigations.push(`STOP_LOSS_WIDENED:${decisionRisk.stopLossAdjustment}`);
        }

        // If high risk, consider more conservative action
        if (decisionRisk.level === 'VERY_HIGH') {
            if (adjustedDecision.code === 'BUY' || adjustedDecision.code === 'SELL') {
                adjustedDecision = Decision.SCALE_IN;
                mitigations.push('DOWNGRADED_TO_SCALE_IN');
            }
        }

        // If warnings exist, add caution flag
        if (limitChecks.hasWarnings) {
            mitigations.push('CAUTION_ADVISED');
        }

        return {
            decision: adjustedDecision,
            mitigations,
            overridden: adjustedDecision.code !== proposedDecision.code,
            originalDecision: proposedDecision,
            riskLevel: decisionRisk.level
        };
    }

    calculateVolatility(prices) {
        if (prices.length < 2) return 0.02;

        const returns = [];
        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
        }

        const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - mean, 2), 0) / returns.length;

        return Math.sqrt(variance);
    }

    updateRiskMetrics(pnlUpdate) {
        // Update daily PnL
        this.riskMetrics.dailyPnL += pnlUpdate;

        // Update drawdown
        if (pnlUpdate < 0) {
            this.riskMetrics.currentDrawdown += Math.abs(pnlUpdate);
        } else {
            // Reduce drawdown with profits
            this.riskMetrics.currentDrawdown = Math.max(
                0,
                this.riskMetrics.currentDrawdown - pnlUpdate * 0.5
            );
        }

        // Update win rate (simplified)
        if (pnlUpdate !== 0) {
            const wasWin = pnlUpdate > 0;
            this.riskMetrics.winRate = (this.riskMetrics.winRate * 0.9) + (wasWin ? 0.1 : 0);
        }

        // Record in history
        this.history.push({
            timestamp: new Date(),
            pnl: pnlUpdate,
            drawdown: this.riskMetrics.currentDrawdown,
            dailyPnL: this.riskMetrics.dailyPnL
        });

        // Keep history limited
        if (this.history.length > 1000) {
            this.history = this.history.slice(-500);
        }
    }

    resetDailyMetrics() {
        this.riskMetrics.dailyPnL = 0;
        // Note: drawdown persists across days
    }
}

export class DecisionOrchestrator {
    constructor(config = {}) {
        this.config = {
            enableAllVectors: config.enableAllVectors !== false,
            decisionThreshold: config.decisionThreshold || 0.7,
            confidenceThreshold: config.confidenceThreshold || 0.65,
            maxProcessingTime: config.maxProcessingTime || 5000,
            enableLearning: config.enableLearning !== false,
            vectorWeights: config.vectorWeights || {
                TEMPORAL: 1.0,
                AI_STRATEGY: 1.2,
                RISK_MANAGEMENT: 1.5,
                MARKET_SENTIMENT: 1.0,
                QUANTITATIVE: 1.1
            },
            ...config
        };

        // Initialize decision vectors
        this.vectors = new Map();
        this.initializeVectors();

        // Decision history and learning
        this.decisionHistory = [];
        this.performanceMetrics = {
            totalDecisions: 0,
            correctDecisions: 0,
            totalPnL: 0,
            winRate: 0,
            avgConfidence: 0,
            vectorPerformance: new Map()
        };

        // Consensus engine
        this.consensusEngine = new ConsensusEngine();

        // Risk overlay
        this.riskOverlay = new RiskOverlay();

        // Learning system
        this.learningSystem = this.config.enableLearning ?
            new DecisionLearningSystem() : null;

        console.log('🧠 Decision Orchestrator v5.0 inicializado');
    }

    initializeVectors() {
        // Core vectors
        this.addVector(new TemporalVector({
            weight: this.config.vectorWeights.TEMPORAL,
            priority: 1
        }));

        this.addVector(new AIStrategyVector({
            weight: this.config.vectorWeights.AI_STRATEGY,
            priority: 2
        }));

        this.addVector(new RiskManagementVector({
            weight: this.config.vectorWeights.RISK_MANAGEMENT,
            priority: 3
        }));

        console.log(`✅ ${this.vectors.size} vetores de decisão inicializados`);
    }

    addVector(vector) {
        this.vectors.set(vector.vectorType, vector);
        console.log(`📊 Vetor ${vector.vectorType} adicionado com peso ${vector.config.weight}`);
    }

    removeVector(vectorType) {
        if (this.vectors.has(vectorType)) {
            this.vectors.delete(vectorType);
            console.log(`🗑️ Vetor ${vectorType} removido`);
            return true;
        }
        return false;
    }

    async execute(input, context = {}) {
        const executionId = `exec_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        console.log(`🧠 Orquestrando decisão multi-vetorial [${executionId}]...`);

        const startTime = Date.now();

        try {
            // Validate input
            if (!this.validateInput(input)) {
                console.warn('⚠️ Entrada inválida para orquestração');
                return this.getFallbackDecision(executionId);
            }

            // Enrich context
            const enrichedContext = await this.enrichContext(context);

            // Execute all vectors in parallel
            const vectorResults = await this.executeVectors(input, enrichedContext);

            // Build consensus
            const consensus = await this.buildConsensus(vectorResults, enrichedContext);

            // Apply risk overlay
            const riskAdjusted = await this.applyRiskOverlay(consensus, input, enrichedContext);

            // Make final decision
            const finalDecision = await this.makeFinalDecision(riskAdjusted, enrichedContext);

            // Apply learning
            if (this.learningSystem) {
                await this.learningSystem.recordDecision({
                    executionId,
                    input,
                    context: enrichedContext,
                    vectorResults,
                    consensus,
                    riskAdjusted,
                    finalDecision,
                    timestamp: new Date()
                });
            }

            // Update performance metrics
            this.updatePerformanceMetrics(finalDecision);

            // Record in history
            this.recordDecision(executionId, {
                input,
                context: enrichedContext,
                vectorResults,
                consensus,
                riskAdjusted,
                finalDecision,
                processingTime: Date.now() - startTime
            });

            console.log(`✅ Decisão orquestrada em ${Date.now() - startTime}ms`);
            console.log(`📊 Decisão final: ${finalDecision.decision.name} (${finalDecision.confidence.toFixed(2)})`);

            return finalDecision;

        } catch (error) {
            console.error('❌ Erro na orquestração de decisão:', error);
            return this.getFallbackDecision(executionId, error);
        }
    }

    validateInput(input) {
        if (!input) return false;

        // Check for required fields based on input type
        if (input.type === 'TRADING_DECISION') {
            return input.symbol && input.marketData;
        }

        return true;
    }

    async enrichContext(context) {
        const enriched = {
            timestamp: new Date(),
            orchestratorVersion: '5.0',
            systemLoad: this.getSystemLoad(),
            ...context
        };

        // Add market context if not provided
        if (!enriched.marketContext && context.symbol) {
            enriched.marketContext = await this.fetchMarketContext(context.symbol);
        }

        // Add risk context
        if (!enriched.riskContext) {
            enriched.riskContext = {
                riskLevel: 'MODERATE',
                maxDrawdown: 0.15,
                positionLimit: 5
            };
        }

        return enriched;
    }

    async executeVectors(input, context) {
        const vectorPromises = [];
        const results = new Map();

        // Execute enabled vectors
        for (const [vectorType, vector] of this.vectors) {
            if (vector.config.enabled) {
                vectorPromises.push(
                    vector.analyze(input, context)
                        .then(result => {
                            results.set(vectorType, result);
                            return result;
                        })
                        .catch(error => {
                            console.error(`❌ Erro no vetor ${vectorType}:`, error);
                            results.set(vectorType, vector.getFallbackDecision());
                            return null;
                        })
                );
            }
        }

        // Wait for all vectors with timeout
        await Promise.race([
            Promise.all(vectorPromises),
            new Promise(resolve => setTimeout(resolve, this.config.maxProcessingTime))
        ]);

        return results;
    }

    async buildConsensus(vectorResults, context) {
        return await this.consensusEngine.buildConsensus(
            Array.from(vectorResults.entries()).map(([type, result]) => ({
                vectorType: type,
                decision: result.decision,
                confidence: result.confidence,
                weight: this.vectors.get(type)?.config.weight || 1.0,
                analysis: result.analysis,
                metadata: result.metadata
            })),
            context
        );
    }

    async applyRiskOverlay(consensus, input, context) {
        return await this.riskOverlay.apply(
            consensus,
            {
                ...input,
                currentPositions: context.currentPositions || [],
                accountBalance: context.accountBalance || 10000,
                riskProfile: context.riskContext
            },
            context
        );
    }

    async makeFinalDecision(riskAdjusted, context) {
        const { consensus, riskAssessment } = riskAdjusted;

        // Check confidence threshold
        if (consensus.confidence < this.config.confidenceThreshold) {
            return {
                decision: Decision.HOLD,
                confidence: consensus.confidence,
                reason: 'LOW_CONFIDENCE',
                consensus,
                riskAssessment,
                timestamp: new Date(),
                orchestrator: 'v5.0'
            };
        }

        // Check if we should proceed
        if (!riskAdjusted.proceed) {
            return {
                decision: Decision.HOLD,
                confidence: consensus.confidence,
                reason: 'RISK_BLOCKED',
                consensus,
                riskAssessment,
                timestamp: new Date(),
                orchestrator: 'v5.0'
            };
        }

        // Make the final decision
        const finalDecision = {
            decision: consensus.decision,
            confidence: consensus.confidence * riskAdjusted.confidenceMultiplier,
            sizeMultiplier: riskAdjusted.sizeMultiplier,
            riskLevel: riskAssessment.level,
            consensus: {
                strength: consensus.strength,
                agreement: consensus.agreement,
                vectorCount: consensus.vectorCount
            },
            riskAssessment,
            metadata: {
                processingTime: context.processingTime,
                timestamp: new Date(),
                orchestratorVersion: '5.0',
                vectorContributions: riskAdjusted.vectorContributions
            }
        };

        return finalDecision;
    }

    async fetchMarketContext(symbol) {
        // In production, fetch real market context
        return {
            symbol,
            volatility: 0.02,
            trend: 'NEUTRAL',
            volume: 'NORMAL',
            regime: 'SIDEWAYS',
            session: EnumUtils.getActiveSession().name
        };
    }

    getSystemLoad() {
        return {
            vectorCount: this.vectors.size,
            activeVectors: Array.from(this.vectors.values()).filter(v => v.config.enabled).length,
            decisionHistorySize: this.decisionHistory.length,
            memoryUsage: process.memoryUsage ? process.memoryUsage().heapUsed / (1024 * 1024) : 0
        };
    }

    updatePerformanceMetrics(decision) {
        this.performanceMetrics.totalDecisions++;
        this.performanceMetrics.avgConfidence =
            (this.performanceMetrics.avgConfidence * (this.performanceMetrics.totalDecisions - 1) +
                decision.confidence) / this.performanceMetrics.totalDecisions;

        // Note: Actual performance (correct/incorrect) would be updated
        // when trade outcomes are known
    }

    recordDecision(executionId, data) {
        const record = {
            id: executionId,
            ...data,
            timestamp: new Date()
        };

        this.decisionHistory.push(record);

        // Keep history limited
        if (this.decisionHistory.length > 10000) {
            this.decisionHistory = this.decisionHistory.slice(-5000);
        }
    }

    getFallbackDecision(executionId, error = null) {
        return {
            decision: Decision.HOLD,
            confidence: 0.1,
            reason: error ? 'ORCHESTRATION_ERROR' : 'FALLBACK',
            error: error?.message,
            executionId,
            timestamp: new Date(),
            orchestrator: 'v5.0_fallback'
        };
    }

    async learnFromOutcome(executionId, outcome) {
        if (!this.learningSystem) return;

        const decisionRecord = this.decisionHistory.find(d => d.id === executionId);
        if (decisionRecord) {
            await this.learningSystem.learnFromOutcome(decisionRecord, outcome);

            // Update vector weights based on learning
            this.adjustVectorWeights(decisionRecord, outcome);
        }
    }

    adjustVectorWeights(decisionRecord, outcome) {
        const { vectorResults } = decisionRecord;

        for (const [vectorType, result] of vectorResults) {
            const vector = this.vectors.get(vectorType);
            if (vector && vector.config.adaptive) {
                vector.updatePerformance(outcome);
            }
        }
    }

    getVectorMetrics() {
        const metrics = {};
        for (const [vectorType, vector] of this.vectors) {
            metrics[vectorType] = vector.getMetrics();
        }
        return metrics;
    }

    getSystemMetrics() {
        return {
            totalDecisions: this.performanceMetrics.totalDecisions,
            avgConfidence: this.performanceMetrics.avgConfidence,
            winRate: this.performanceMetrics.winRate,
            vectorCount: this.vectors.size,
            decisionHistorySize: this.decisionHistory.length,
            learningEnabled: !!this.learningSystem
        };
    }

    reset() {
        this.decisionHistory = [];
        this.performanceMetrics = {
            totalDecisions: 0,
            correctDecisions: 0,
            totalPnL: 0,
            winRate: 0,
            avgConfidence: 0,
            vectorPerformance: new Map()
        };

        for (const vector of this.vectors.values()) {
            vector.reset();
        }

        console.log('🔄 Decision Orchestrator resetado');
    }

    setVectorWeight(vectorType, weight) {
        const vector = this.vectors.get(vectorType);
        if (vector) {
            const oldWeight = vector.config.weight;
            vector.config.weight = Math.max(0.1, Math.min(3.0, weight));
            console.log(`⚖️  Peso do vetor ${vectorType} alterado: ${oldWeight} → ${vector.config.weight}`);
            return true;
        }
        return false;
    }

    enableVector(vectorType) {
        const vector = this.vectors.get(vectorType);
        if (vector) {
            vector.config.enabled = true;
            console.log(`✅ Vetor ${vectorType} ativado`);
            return true;
        }
        return false;
    }

    disableVector(vectorType) {
        const vector = this.vectors.get(vectorType);
        if (vector) {
            vector.config.enabled = false;
            console.log(`⏸️  Vetor ${vectorType} desativado`);
            return true;
        }
        return false;
    }
}

class ConsensusEngine {
    constructor() {
        this.consensusMethods = {
            WEIGHTED_AVERAGE: 'weighted_average',
            MAJORITY_VOTE: 'majority_vote',
            CONFIDENCE_WEIGHTED: 'confidence_weighted',
            BAYESIAN: 'bayesian'
        };

        this.activeMethod = this.consensusMethods.CONFIDENCE_WEIGHTED;
    }

    async buildConsensus(vectorDecisions, context) {
        if (!vectorDecisions || vectorDecisions.length === 0) {
            return this.getDefaultConsensus();
        }

        // Filter out invalid decisions
        const validDecisions = vectorDecisions.filter(d =>
            d && d.decision && d.confidence > 0.1
        );

        if (validDecisions.length === 0) {
            return this.getDefaultConsensus();
        }

        // Build consensus based on selected method
        switch (this.activeMethod) {
            case this.consensusMethods.WEIGHTED_AVERAGE:
                return this.weightedAverageConsensus(validDecisions, context);
            case this.consensusMethods.MAJORITY_VOTE:
                return this.majorityVoteConsensus(validDecisions, context);
            case this.consensusMethods.CONFIDENCE_WEIGHTED:
                return this.confidenceWeightedConsensus(validDecisions, context);
            case this.consensusMethods.BAYESIAN:
                return this.bayesianConsensus(validDecisions, context);
            default:
                return this.confidenceWeightedConsensus(validDecisions, context);
        }
    }

    confidenceWeightedConsensus(decisions, context) {
        // Group decisions by type
        const decisionGroups = new Map();

        decisions.forEach(decision => {
            const key = decision.decision.code;
            if (!decisionGroups.has(key)) {
                decisionGroups.set(key, []);
            }
            decisionGroups.get(key).push(decision);
        });

        // Calculate weighted score for each decision type
        const scores = new Map();
        for (const [decisionCode, groupDecisions] of decisionGroups) {
            let totalWeight = 0;
            let weightedConfidence = 0;

            groupDecisions.forEach(d => {
                const weight = d.weight || 1.0;
                totalWeight += weight;
                weightedConfidence += d.confidence * weight;
            });

            scores.set(decisionCode, {
                score: weightedConfidence / totalWeight,
                weight: totalWeight,
                count: groupDecisions.length
            });
        }

        // Find best decision
        let bestDecision = null;
        let bestScore = -Infinity;

        for (const [decisionCode, scoreData] of scores) {
            if (scoreData.score > bestScore) {
                bestScore = scoreData.score;
                bestDecision = EnumUtils.getDecisionByCode(decisionCode);
            }
        }

        // Calculate agreement
        const totalVectors = decisions.length;
        const winningGroup = decisionGroups.get(bestDecision.code) || [];
        const agreement = winningGroup.length / totalVectors;

        // Calculate overall confidence
        const avgConfidence = decisions.reduce((sum, d) => sum + d.confidence, 0) / totalVectors;
        const consensusConfidence = (bestScore + avgConfidence) / 2;

        return {
            decision: bestDecision,
            confidence: consensusConfidence,
            strength: bestScore,
            agreement,
            vectorCount: totalVectors,
            scores: Object.fromEntries(scores),
            method: this.activeMethod
        };
    }

    weightedAverageConsensus(decisions, context) {
        // Convert decisions to numerical scores
        const decisionScores = decisions.map(d => ({
            score: this.decisionToScore(d.decision),
            weight: d.weight || 1.0,
            confidence: d.confidence
        }));

        // Calculate weighted average
        let totalWeight = 0;
        let weightedSum = 0;
        let totalConfidence = 0;

        decisionScores.forEach(ds => {
            const effectiveWeight = ds.weight * ds.confidence;
            totalWeight += effectiveWeight;
            weightedSum += ds.score * effectiveWeight;
            totalConfidence += ds.confidence;
        });

        const avgScore = weightedSum / totalWeight;
        const avgConfidence = totalConfidence / decisions.length;

        // Convert back to decision
        const decision = this.scoreToDecision(avgScore);

        return {
            decision,
            confidence: avgConfidence,
            strength: Math.abs(avgScore),
            agreement: this.calculateAgreement(decisions, decision),
            vectorCount: decisions.length,
            method: this.activeMethod
        };
    }

    majorityVoteConsensus(decisions, context) {
        const voteCounts = new Map();

        decisions.forEach(d => {
            const key = d.decision.code;
            voteCounts.set(key, (voteCounts.get(key) || 0) + 1);
        });

        // Find majority
        let majorityDecision = null;
        let maxVotes = 0;

        for (const [decisionCode, count] of voteCounts) {
            if (count > maxVotes) {
                maxVotes = count;
                majorityDecision = EnumUtils.getDecisionByCode(decisionCode);
            }
        }

        const agreement = maxVotes / decisions.length;

        // Average confidence of majority voters
        const majorityVoters = decisions.filter(d => d.decision.code === majorityDecision.code);
        const avgConfidence = majorityVoters.reduce((sum, d) => sum + d.confidence, 0) / majorityVoters.length;

        return {
            decision: majorityDecision,
            confidence: avgConfidence,
            strength: agreement,
            agreement,
            vectorCount: decisions.length,
            voteCounts: Object.fromEntries(voteCounts),
            method: this.activeMethod
        };
    }

    bayesianConsensus(decisions, context) {
        // Simplified Bayesian consensus
        // In production, implement full Bayesian model

        return this.confidenceWeightedConsensus(decisions, context);
    }

    decisionToScore(decision) {
        const scores = {
            'BUY': 1.0,
            'SELL': -1.0,
            'HOLD': 0.0,
            'CLOSE_LONG': -0.5,
            'CLOSE_SHORT': 0.5,
            'SCALE_IN': 0.7,
            'SCALE_OUT': -0.3,
            'REVERSE': 0.0, // Depends on current position
            'HEDGE': 0.0,
            'STOP_LOSS': -0.8,
            'TAKE_PROFIT': 0.8,
            'TRAILING_STOP': 0.0
        };

        return scores[decision.code] || 0.0;
    }

    scoreToDecision(score) {
        if (score > 0.3) return Decision.BUY;
        if (score > 0.1) return Decision.SCALE_IN;
        if (score < -0.3) return Decision.SELL;
        if (score < -0.1) return Decision.SCALE_OUT;
        return Decision.HOLD;
    }

    calculateAgreement(decisions, consensusDecision) {
        if (!consensusDecision) return 0;

        const agreeing = decisions.filter(d =>
            d.decision.code === consensusDecision.code
        ).length;

        return agreeing / decisions.length;
    }

    getDefaultConsensus() {
        return {
            decision: Decision.HOLD,
            confidence: 0.1,
            strength: 0,
            agreement: 0,
            vectorCount: 0,
            method: this.activeMethod
        };
    }

    setConsensusMethod(method) {
        if (Object.values(this.consensusMethods).includes(method)) {
            this.activeMethod = method;
            return true;
        }
        return false;
    }
}

class RiskOverlay {
    constructor() {
        this.riskRules = [
            this.maxDrawdownRule.bind(this),
            this.positionLimitRule.bind(this),
            this.volatilityRule.bind(this),
            this.correlationRule.bind(this),
            this.timeOfDayRule.bind(this)
        ];
    }

    async apply(consensus, input, context) {
        const riskAssessment = await this.assessRisk(consensus, input, context);

        // Apply risk rules
        const ruleResults = this.applyRiskRules(consensus, input, context, riskAssessment);

        // Determine if we should proceed
        const shouldProceed = this.shouldProceed(ruleResults);

        // Calculate adjustments
        const adjustments = this.calculateAdjustments(ruleResults, consensus, riskAssessment);

        return {
            consensus,
            riskAssessment,
            ruleResults,
            proceed: shouldProceed,
            confidenceMultiplier: adjustments.confidenceMultiplier,
            sizeMultiplier: adjustments.sizeMultiplier,
            vectorContributions: this.calculateVectorContributions(consensus, adjustments)
        };
    }

    async assessRisk(consensus, input, context) {
        const { currentPositions = [], accountBalance = 10000, riskProfile = {} } = input;

        // Calculate current exposure
        const totalExposure = currentPositions.reduce((sum, pos) =>
            sum + Math.abs(pos.size * pos.currentPrice), 0);

        const exposureRatio = totalExposure / accountBalance;

        // Calculate drawdown (simplified)
        const drawdown = this.calculateDrawdown(currentPositions);

        // Assess decision risk
        const decisionRisk = this.assessDecisionRisk(consensus.decision, exposureRatio);

        return {
            exposure: exposureRatio,
            drawdown,
            positionCount: currentPositions.length,
            decisionRisk: decisionRisk.level,
            riskScore: this.calculateRiskScore(exposureRatio, drawdown, decisionRisk.score),
            limits: {
                maxExposure: riskProfile.maxPositionSize || 0.1,
                maxDrawdown: riskProfile.maxDrawdown || 0.15,
                maxPositions: riskProfile.positionLimit || 5
            }
        };
    }

    calculateDrawdown(positions) {
        if (positions.length === 0) return 0;

        // Simplified drawdown calculation
        const totalPnl = positions.reduce((sum, pos) => sum + (pos.unrealizedPnl || 0), 0);
        const totalValue = positions.reduce((sum, pos) => sum + pos.currentValue, 0);

        return totalPnl < 0 ? Math.abs(totalPnl / totalValue) : 0;
    }

    assessDecisionRisk(decision, currentExposure) {
        let level = 'LOW';
        let score = 0.3;

        switch (decision.code) {
            case 'BUY':
            case 'SELL':
                level = currentExposure > 0.3 ? 'HIGH' : 'MEDIUM';
                score = 0.6 + currentExposure;
                break;
            case 'SCALE_IN':
                level = 'MEDIUM';
                score = 0.5;
                break;
            case 'REVERSE':
                level = 'VERY_HIGH';
                score = 0.8;
                break;
            default:
                level = 'LOW';
                score = 0.3;
        }

        return { level, score };
    }

    calculateRiskScore(exposure, drawdown, decisionRisk) {
        return Math.min(1, exposure * 0.4 + drawdown * 0.3 + decisionRisk * 0.3);
    }

    applyRiskRules(consensus, input, context, riskAssessment) {
        const results = [];

        for (const rule of this.riskRules) {
            try {
                const result = rule(consensus, input, context, riskAssessment);
                results.push(result);
            } catch (error) {
                console.error('❌ Erro na regra de risco:', error);
                results.push({
                    rule: 'ERROR',
                    passed: true,
                    severity: 'LOW',
                    message: 'Rule error'
                });
            }
        }

        return results;
    }

    maxDrawdownRule(consensus, input, context, riskAssessment) {
        const { drawdown, limits } = riskAssessment;
        const maxDrawdown = limits.maxDrawdown || 0.15;

        if (drawdown > maxDrawdown) {
            return {
                rule: 'MAX_DRAWDOWN',
                passed: false,
                severity: 'CRITICAL',
                message: `Drawdown ${(drawdown * 100).toFixed(1)}% exceeds limit ${(maxDrawdown * 100).toFixed(1)}%`,
                block: true
            };
        } else if (drawdown > maxDrawdown * 0.8) {
            return {
                rule: 'MAX_DRAWDOWN',
                passed: true,
                severity: 'WARNING',
                message: `Drawdown ${(drawdown * 100).toFixed(1)}% approaching limit`,
                adjustment: 0.5
            };
        }

        return {
            rule: 'MAX_DRAWDOWN',
            passed: true,
            severity: 'LOW',
            message: `Drawdown ${(drawdown * 100).toFixed(1)}% within limits`
        };
    }

    positionLimitRule(consensus, input, context, riskAssessment) {
        const { positionCount, limits } = riskAssessment;
        const maxPositions = limits.maxPositions || 5;

        if (positionCount >= maxPositions) {
            return {
                rule: 'POSITION_LIMIT',
                passed: false,
                severity: 'HIGH',
                message: `Position count ${positionCount} at limit ${maxPositions}`,
                block: consensus.decision.code === 'BUY' || consensus.decision.code === 'SELL'
            };
        }

        return {
            rule: 'POSITION_LIMIT',
            passed: true,
            severity: 'LOW',
            message: `Position count ${positionCount} within limits`
        };
    }

    volatilityRule(consensus, input, context, riskAssessment) {
        const volatility = context.marketContext?.volatility || 0.02;

        if (volatility > 0.04) {
            return {
                rule: 'VOLATILITY',
                passed: false,
                severity: 'HIGH',
                message: `High volatility ${(volatility * 100).toFixed(1)}%`,
                adjustment: 0.3,
                block: consensus.decision.code === 'REVERSE'
            };
        } else if (volatility > 0.025) {
            return {
                rule: 'VOLATILITY',
                passed: true,
                severity: 'MEDIUM',
                message: `Elevated volatility ${(volatility * 100).toFixed(1)}%`,
                adjustment: 0.7
            };
        }

        return {
            rule: 'VOLATILITY',
            passed: true,
            severity: 'LOW',
            message: `Volatility ${(volatility * 100).toFixed(1)}% normal`
        };
    }

    correlationRule(consensus, input, context, riskAssessment) {
        // Simplified correlation check
        // In production, check correlation matrix

        return {
            rule: 'CORRELATION',
            passed: true,
            severity: 'LOW',
            message: 'Correlation check passed'
        };
    }

    timeOfDayRule(consensus, input, context, riskAssessment) {
        const hour = new Date().getUTCHours();

        // Avoid trading during low liquidity periods
        if (hour >= 22 || hour <= 6) {
            return {
                rule: 'TIME_OF_DAY',
                passed: true,
                severity: 'MEDIUM',
                message: 'Low liquidity period',
                adjustment: 0.8
            };
        }

        return {
            rule: 'TIME_OF_DAY',
            passed: true,
            severity: 'LOW',
            message: 'Normal trading hours'
        };
    }

    shouldProceed(ruleResults) {
        // Check for critical blocks
        const criticalBlocks = ruleResults.filter(r =>
            r.block && (r.severity === 'CRITICAL' || r.severity === 'HIGH')
        );

        return criticalBlocks.length === 0;
    }

    calculateAdjustments(ruleResults, consensus, riskAssessment) {
        let confidenceMultiplier = 1.0;
        let sizeMultiplier = 1.0;

        // Apply adjustments from rules
        ruleResults.forEach(rule => {
            if (rule.adjustment) {
                confidenceMultiplier *= rule.adjustment;
                sizeMultiplier *= rule.adjustment;
            }
        });

        // Adjust based on risk score
        const riskScore = riskAssessment.riskScore || 0.5;
        const riskAdjustment = 1 - (riskScore * 0.5); // Reduce up to 50% for high risk

        confidenceMultiplier *= riskAdjustment;
        sizeMultiplier *= riskAdjustment;

        // Ensure minimum values
        confidenceMultiplier = Math.max(0.1, Math.min(1.0, confidenceMultiplier));
        sizeMultiplier = Math.max(0.1, Math.min(1.0, sizeMultiplier));

        return { confidenceMultiplier, sizeMultiplier };
    }

    calculateVectorContributions(consensus, adjustments) {
        return {
            confidenceMultiplier: adjustments.confidenceMultiplier,
            sizeMultiplier: adjustments.sizeMultiplier,
            riskAdjustedConfidence: consensus.confidence * adjustments.confidenceMultiplier
        };
    }
}

class DecisionLearningSystem {
    constructor() {
        this.trainingData = [];
        this.model = null;
        this.learningRate = 0.01;
        this.batchSize = 100;
    }

    async recordDecision(decisionRecord) {
        this.trainingData.push(decisionRecord);

        // Keep training data limited
        if (this.trainingData.length > 10000) {
            this.trainingData = this.trainingData.slice(-5000);
        }

        // Train periodically
        if (this.trainingData.length % this.batchSize === 0) {
            await this.train();
        }
    }

    async learnFromOutcome(decisionRecord, outcome) {
        // Add outcome to training data
        const enhancedRecord = {
            ...decisionRecord,
            outcome,
            learnedAt: new Date()
        };

        this.trainingData.push(enhancedRecord);

        // Update learning model
        await this.updateModel(enhancedRecord);
    }

    async train() {
        if (this.trainingData.length < this.batchSize) return;

        console.log('🧠 Treinando sistema de aprendizagem...');

        try {
            // Simplified training - in production, use proper ML
            this.updateLearningRates();

            console.log('✅ Sistema de aprendizagem atualizado');
        } catch (error) {
            console.error('❌ Erro no treinamento:', error);
        }
    }

    updateModel(trainingExample) {
        // Update internal model based on example
        // This would be a proper ML model in production
    }

    updateLearningRates() {
        // Adjust learning rates based on recent performance
        if (this.trainingData.length < 100) return;

        const recent = this.trainingData.slice(-100);
        const successful = recent.filter(r =>
            r.outcome && r.outcome.success === true
        ).length;

        const successRate = successful / recent.length;

        // Adjust learning rate based on success rate
        if (successRate > 0.6) {
            this.learningRate *= 1.1; // Increase if doing well
        } else if (successRate < 0.4) {
            this.learningRate *= 0.9; // Decrease if doing poorly
        }

        this.learningRate = Math.max(0.001, Math.min(0.1, this.learningRate));
    }

    predictOptimalDecision(context) {
        // Use learned model to predict optimal decision
        // Simplified for now
        return {
            decision: Decision.HOLD,
            confidence: 0.5,
            learned: true
        };
    }
}

// Export singleton instance
const decisionOrchestrator = new DecisionOrchestrator();

export default decisionOrchestrator;