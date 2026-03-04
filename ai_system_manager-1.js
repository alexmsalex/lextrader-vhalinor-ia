/**
 * Sistema Avançado de IA para Previsão Financeira
 * Gerenciador central de modelos com orquestração inteligente
 */

import { AdvancedTemporalNetwork, MarketRegime } from './advanced_temporal_network.js';
import { NeuroEvolutionController } from './neuro_evolution_controller.js';
import { QuantumHybridPredictor } from './quantum_hybrid_predictor.js';
import { MetaStrategyOptimizer } from './meta_strategy_optimizer.js';

export const ModelType = {
    TEMPORAL_NETWORK: 'temporal_network',
    NEURO_EVOLUTION: 'neuro_evolution',
    QUANTUM_HYBRID: 'quantum_hybrid',
    ENSEMBLE: 'ensemble',
    TRANSFORMER: 'transformer',
    LIGHTGBM: 'lightgbm'
};

export const PredictionConfidence = {
    VERY_HIGH: 'VERY_HIGH',    // > 90%
    HIGH: 'HIGH',              // 80-90%
    MEDIUM: 'MEDIUM',          // 70-80%
    LOW: 'LOW',                // 60-70%
    VERY_LOW: 'VERY_LOW'       // < 60%
};

export class ModelPerformanceMetrics {
    constructor() {
        this.predictions = [];
        this.accuracyHistory = [];
        this.latencyHistory = [];
        this.confidenceHistory = [];
        this.regimeAccuracy = new Map();
        this.startTime = Date.now();
    }

    addPrediction(modelId, prediction, actual, latency, regime) {
        const timestamp = Date.now();
        const error = Math.abs(prediction - actual);
        const accuracy = 1 - error;
        const isCorrectDirection = Math.sign(prediction) === Math.sign(actual);

        const entry = {
            modelId,
            timestamp,
            prediction,
            actual,
            error,
            accuracy,
            latency,
            regime,
            isCorrectDirection,
            confidence: this.calculateConfidence(accuracy, latency, regime)
        };

        this.predictions.push(entry);
        this.accuracyHistory.push(accuracy);
        this.latencyHistory.push(latency);
        this.confidenceHistory.push(entry.confidence);

        // Atualizar precisão por regime
        if (regime) {
            if (!this.regimeAccuracy.has(regime)) {
                this.regimeAccuracy.set(regime, []);
            }
            this.regimeAccuracy.get(regime).push(accuracy);
        }

        return entry;
    }

    calculateConfidence(accuracy, latency, regime) {
        let confidence = accuracy * 100;

        // Penalizar alta latência
        if (latency > 100) confidence *= 0.95;
        if (latency > 500) confidence *= 0.90;

        // Ajustar por regime
        if (regime === MarketRegime.HIGH_VOLATILITY) confidence *= 0.85;
        if (regime === MarketRegime.LOW_VOLATILITY) confidence *= 1.1;

        return Math.min(Math.max(confidence, 0), 100);
    }

    getModelMetrics(modelId, lookback = 100) {
        const modelPredictions = this.predictions
            .filter(p => p.modelId === modelId)
            .slice(-lookback);

        if (modelPredictions.length === 0) return null;

        const avgAccuracy = modelPredictions.reduce((sum, p) => sum + p.accuracy, 0) / modelPredictions.length;
        const avgLatency = modelPredictions.reduce((sum, p) => sum + p.latency, 0) / modelPredictions.length;
        const directionAccuracy = modelPredictions.filter(p => p.isCorrectDirection).length / modelPredictions.length;
        const winRate = modelPredictions.filter(p => p.prediction * p.actual > 0).length / modelPredictions.length;

        return {
            modelId,
            predictionsCount: modelPredictions.length,
            avgAccuracy: avgAccuracy * 100,
            avgLatency,
            directionAccuracy: directionAccuracy * 100,
            winRate: winRate * 100,
            recentConfidence: modelPredictions.slice(-10).reduce((sum, p) => sum + p.confidence, 0) / Math.min(10, modelPredictions.length),
            regimePerformance: this.getRegimePerformance(modelId)
        };
    }

    getRegimePerformance(modelId) {
        const performance = {};
        for (const [regime, accuracies] of this.regimeAccuracy.entries()) {
            const modelAccuracies = this.predictions
                .filter(p => p.modelId === modelId && p.regime === regime)
                .map(p => p.accuracy);

            if (modelAccuracies.length > 0) {
                performance[regime] = {
                    count: modelAccuracies.length,
                    avgAccuracy: modelAccuracies.reduce((a, b) => a + b, 0) / modelAccuracies.length * 100,
                    stdDev: this.calculateStdDev(modelAccuracies) * 100
                };
            }
        }
        return performance;
    }

    calculateStdDev(values) {
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const variance = values.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / values.length;
        return Math.sqrt(variance);
    }

    getUptime() {
        return Date.now() - this.startTime;
    }

    reset() {
        this.predictions = [];
        this.accuracyHistory = [];
        this.latencyHistory = [];
        this.confidenceHistory = [];
        this.regimeAccuracy.clear();
        this.startTime = Date.now();
    }
}

export class ModelEnsemble {
    constructor() {
        this.models = new Map();
        this.weights = new Map();
        this.diversityMatrix = new Map();
    }

    addModel(modelId, model, initialWeight = 1.0) {
        this.models.set(modelId, model);
        this.weights.set(modelId, initialWeight);
        this.updateDiversity();
    }

    async predict(inputs) {
        const predictions = new Map();
        const startTime = Date.now();

        // Coletar previsões de todos os modelos
        for (const [modelId, model] of this.models) {
            try {
                const predictionStart = Date.now();
                const prediction = await model.predict(inputs);
                const latency = Date.now() - predictionStart;

                predictions.set(modelId, {
                    prediction: prediction.value || prediction,
                    confidence: prediction.confidence || 0.8,
                    latency,
                    metadata: prediction.metadata || {}
                });
            } catch (error) {
                console.error(`❌ Erro no modelo ${modelId}:`, error);
                predictions.set(modelId, null);
            }
        }

        // Calcular previsão ponderada
        const weightedPrediction = this.calculateWeightedPrediction(predictions);
        const ensembleLatency = Date.now() - startTime;

        return {
            value: weightedPrediction,
            predictions: Object.fromEntries(predictions),
            weights: Object.fromEntries(this.weights),
            confidence: this.calculateEnsembleConfidence(predictions),
            latency: ensembleLatency,
            timestamp: new Date()
        };
    }

    calculateWeightedPrediction(predictions) {
        let totalWeight = 0;
        let weightedSum = 0;

        for (const [modelId, prediction] of predictions) {
            if (prediction && !isNaN(prediction.prediction)) {
                const weight = this.weights.get(modelId) || 1;
                weightedSum += prediction.prediction * weight;
                totalWeight += weight;
            }
        }

        return totalWeight > 0 ? weightedSum / totalWeight : 0;
    }

    calculateEnsembleConfidence(predictions) {
        const validPredictions = Array.from(predictions.values())
            .filter(p => p && !isNaN(p.confidence));

        if (validPredictions.length === 0) return 0;

        // Média ponderada das confianças
        const avgConfidence = validPredictions.reduce((sum, p) => sum + p.confidence, 0) / validPredictions.length;

        // Ajustar pela diversidade
        const diversityScore = this.calculateDiversityScore(predictions);
        const adjustedConfidence = avgConfidence * (0.7 + 0.3 * diversityScore);

        return Math.min(adjustedConfidence, 1);
    }

    calculateDiversityScore(predictions) {
        const values = Array.from(predictions.values())
            .filter(p => p)
            .map(p => p.prediction);

        if (values.length < 2) return 1;

        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
        const stdDev = Math.sqrt(variance);

        // Normalizar para 0-1
        return Math.min(stdDev * 10, 1);
    }

    updateWeights(performanceMetrics) {
        for (const [modelId] of this.models) {
            const metrics = performanceMetrics.getModelMetrics(modelId, 50);
            if (metrics) {
                // Novo peso baseado em desempenho recente
                const newWeight = Math.max(0.1, Math.min(2.0,
                    metrics.recentConfidence / 100 *
                    (metrics.directionAccuracy / 100) *
                    (1 / (metrics.avgLatency / 1000 + 0.1))
                ));

                this.weights.set(modelId, newWeight);
            }
        }

        // Normalizar pesos
        this.normalizeWeights();
    }

    normalizeWeights() {
        const totalWeight = Array.from(this.weights.values()).reduce((a, b) => a + b, 0);
        if (totalWeight > 0) {
            for (const [modelId, weight] of this.weights) {
                this.weights.set(modelId, weight / totalWeight * this.weights.size);
            }
        }
    }

    updateDiversity() {
        // Atualizar matriz de diversidade entre modelos
        const modelIds = Array.from(this.models.keys());

        for (let i = 0; i < modelIds.length; i++) {
            for (let j = i + 1; j < modelIds.length; j++) {
                const key = `${modelIds[i]}_${modelIds[j]}`;
                const model1 = this.models.get(modelIds[i]);
                const model2 = this.models.get(modelIds[j]);

                // Calcular similaridade (simplificado)
                const similarity = this.estimateModelSimilarity(model1, model2);
                this.diversityMatrix.set(key, 1 - similarity);
            }
        }
    }

    estimateModelSimilarity(model1, model2) {
        // Estimativa simplificada de similaridade
        // Em produção, usar técnicas mais avançadas
        return 0.5;
    }

    getTopModels(count = 3) {
        const modelWeights = Array.from(this.weights.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, count);

        return modelWeights.map(([modelId, weight]) => ({
            modelId,
            weight,
            model: this.models.get(modelId)
        }));
    }
}

export class MarketContextAnalyzer {
    constructor() {
        this.contextHistory = [];
        this.contextPatterns = new Map();
        this.macroIndicators = {
            vix: null,
            usdIndex: null,
            bondYields: null,
            commodityPrices: new Map()
        };
    }

    async analyze(symbol, marketData, timeframe = '1h') {
        const context = {
            timestamp: new Date(),
            symbol,
            timeframe,

            // Indicadores técnicos
            volatility: this.calculateVolatility(marketData.prices),
            trendStrength: this.calculateTrendStrength(marketData.prices),
            volumeProfile: this.analyzeVolumeProfile(marketData),
            supportResistance: this.identifySupportResistance(marketData.prices),

            // Sentimento
            sentiment: await this.fetchMarketSentiment(symbol),
            newsImpact: this.analyzeNewsImpact(symbol),

            // Macro
            macroContext: this.getMacroContext(),

            // Liquidez
            liquidity: this.assessLiquidity(marketData),

            // Ciclos temporais
            temporalCycle: this.identifyTemporalCycle(),

            // Score de contexto
            contextScore: 0
        };

        context.contextScore = this.calculateContextScore(context);
        this.contextHistory.push(context);

        // Manter histórico limitado
        if (this.contextHistory.length > 1000) {
            this.contextHistory.shift();
        }

        return context;
    }

    calculateVolatility(prices) {
        if (prices.length < 2) return 0;

        const returns = [];
        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
        }

        const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - mean, 2), 0) / returns.length;

        return Math.sqrt(variance) * Math.sqrt(252); // Anualizado
    }

    calculateTrendStrength(prices) {
        if (prices.length < 20) return 0;

        const period = 20;
        const recentPrices = prices.slice(-period);
        const x = Array.from({ length: period }, (_, i) => i);
        const y = recentPrices;

        // Regressão linear simples
        const n = period;
        const sumX = x.reduce((a, b) => a + b, 0);
        const sumY = y.reduce((a, b) => a + b, 0);
        const sumXY = x.reduce((sum, val, idx) => sum + val * y[idx], 0);
        const sumX2 = x.reduce((sum, val) => sum + val * val, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const rSquared = this.calculateRSquared(x, y, slope);

        return {
            slope,
            strength: Math.abs(slope) * rSquared,
            direction: slope > 0 ? 'up' : 'down'
        };
    }

    calculateRSquared(x, y, slope) {
        const meanY = y.reduce((a, b) => a + b, 0) / y.length;

        let ssTotal = 0;
        let ssResidual = 0;

        for (let i = 0; i < x.length; i++) {
            ssTotal += Math.pow(y[i] - meanY, 2);
            const predicted = slope * x[i];
            ssResidual += Math.pow(y[i] - predicted, 2);
        }

        return 1 - (ssResidual / ssTotal);
    }

    analyzeVolumeProfile(marketData) {
        const volumes = marketData.volumes || [];
        const prices = marketData.prices || [];

        if (volumes.length === 0 || prices.length === 0) {
            return { profile: 'unknown', concentration: 0 };
        }

        const avgVolume = volumes.reduce((a, b) => a + b, 0) / volumes.length;
        const volumeRatio = volumes[volumes.length - 1] / avgVolume;

        return {
            profile: volumeRatio > 1.5 ? 'high' : volumeRatio < 0.5 ? 'low' : 'normal',
            concentration: this.calculateVolumeConcentration(volumes, prices),
            ratio: volumeRatio
        };
    }

    calculateVolumeConcentration(volumes, prices) {
        // Simular cálculo de concentração (POC, etc.)
        return 0.5;
    }

    identifySupportResistance(prices) {
        if (prices.length < 50) return { supports: [], resistances: [] };

        const recentPrices = prices.slice(-50);
        const supports = [];
        const resistances = [];

        // Identificar mínimos locais (suportes)
        for (let i = 5; i < recentPrices.length - 5; i++) {
            const window = recentPrices.slice(i - 5, i + 6);
            if (recentPrices[i] === Math.min(...window)) {
                supports.push(recentPrices[i]);
            }
        }

        // Identificar máximos locais (resistências)
        for (let i = 5; i < recentPrices.length - 5; i++) {
            const window = recentPrices.slice(i - 5, i + 6);
            if (recentPrices[i] === Math.max(...window)) {
                resistances.push(recentPrices[i]);
            }
        }

        return {
            supports: [...new Set(supports)].slice(-3),
            resistances: [...new Set(resistances)].slice(-3)
        };
    }

    async fetchMarketSentiment(symbol) {
        // Integrar com API de sentimento
        return {
            overall: 0.5,
            social: 0.5,
            news: 0.5,
            lastUpdated: new Date()
        };
    }

    analyzeNewsImpact(symbol) {
        // Análise de impacto de notícias
        return {
            hasNews: false,
            impact: 0,
            sentiment: 'neutral'
        };
    }

    getMacroContext() {
        return {
            vix: this.macroIndicators.vix,
            usdIndex: this.macroIndicators.usdIndex,
            bondYields: this.macroIndicators.bondYields,
            riskOn: this.isRiskOnEnvironment()
        };
    }

    isRiskOnEnvironment() {
        // Determinar se é ambiente risk-on ou risk-off
        return true;
    }

    assessLiquidity(marketData) {
        const spreads = marketData.spreads || [];
        const depths = marketData.depths || [];

        if (spreads.length === 0) return 'unknown';

        const avgSpread = spreads.reduce((a, b) => a + b, 0) / spreads.length;

        if (avgSpread < 0.0001) return 'high';
        if (avgSpread < 0.001) return 'medium';
        return 'low';
    }

    identifyTemporalCycle() {
        const now = new Date();
        const hour = now.getUTCHours();
        const day = now.getUTCDay();

        // Identificar ciclos de mercado
        if (day >= 1 && day <= 5) {
            if (hour >= 13 && hour <= 17) return 'london_ny_overlap';
            if (hour >= 8 && hour <= 12) return 'london_session';
            if (hour >= 13 && hour <= 21) return 'ny_session';
            if (hour >= 22 || hour <= 7) return 'asia_session';
        }

        return 'weekend';
    }

    calculateContextScore(context) {
        let score = 50;

        // Ajustes baseados em fatores
        if (context.volatility < 0.1) score += 10;
        if (context.volatility > 0.3) score -= 15;

        if (context.trendStrength.strength > 0.7) score += 15;
        if (context.trendStrength.strength < 0.3) score -= 10;

        if (context.volumeProfile.profile === 'high') score += 10;
        if (context.volumeProfile.profile === 'low') score -= 10;

        if (context.liquidity === 'high') score += 15;
        if (context.liquidity === 'low') score -= 20;

        return Math.max(0, Math.min(100, score));
    }

    getOptimalModelType(context) {
        if (context.volatility > 0.25) return ModelType.QUANTUM_HYBRID;
        if (context.trendStrength.strength > 0.7) return ModelType.TEMPORAL_NETWORK;
        if (context.contextScore > 70) return ModelType.ENSEMBLE;
        return ModelType.NEURO_EVOLUTION;
    }
}

export class AISystemManager {
    constructor(config = {}) {
        this.config = {
            autoOptimize: config.autoOptimize !== false,
            realTimeLearning: config.realTimeLearning !== false,
            maxParallelModels: config.maxParallelModels || 5,
            telemetryEnabled: config.telemetryEnabled !== false,
            ...config
        };

        this.models = new Map();
        this.modelRegistry = new Map();
        this.ensemble = new ModelEnsemble();
        this.performanceMetrics = new ModelPerformanceMetrics();
        this.contextAnalyzer = new MarketContextAnalyzer();
        this.telemetry = [];
        this.symbolModels = new Map();
        this.modelConfigs = new Map();
        this.isInitialized = false;

        this.initDefaultModels();
    }

    initDefaultModels() {
        // Configurações padrão para diferentes símbolos
        this.modelConfigs.set('default', {
            primary: ModelType.TEMPORAL_NETWORK,
            fallback: ModelType.NEURO_EVOLUTION,
            ensemble: true,
            minConfidence: 0.65
        });

        this.modelConfigs.set('forex', {
            primary: ModelType.TEMPORAL_NETWORK,
            fallback: ModelType.QUANTUM_HYBRID,
            ensemble: true,
            minConfidence: 0.7
        });

        this.modelConfigs.set('crypto', {
            primary: ModelType.QUANTUM_HYBRID,
            fallback: ModelType.NEURO_EVOLUTION,
            ensemble: true,
            minConfidence: 0.6
        });

        this.modelConfigs.set('stocks', {
            primary: ModelType.ENSEMBLE,
            fallback: ModelType.TEMPORAL_NETWORK,
            ensemble: true,
            minConfidence: 0.75
        });
    }

    async start() {
        console.log('🚀 AI System Manager: Iniciando coordenação de modelos...');

        try {
            // Inicializar modelos base
            await this.initializeBaseModels();

            // Iniciar otimização contínua
            if (this.config.autoOptimize) {
                this.startContinuousOptimization();
            }

            // Iniciar coleta de telemetria
            if (this.config.telemetryEnabled) {
                this.startTelemetryCollection();
            }

            this.isInitialized = true;
            console.log('✅ AI System Manager: Inicialização completa');

            return this.getSystemStatus();
        } catch (error) {
            console.error('❌ Erro na inicialização do AI System Manager:', error);
            throw error;
        }
    }

    async initializeBaseModels() {
        console.log('🔄 Inicializando modelos base...');

        // Temporal Network
        const temporalNet = new AdvancedTemporalNetwork({
            sequenceLength: 60,
            hiddenSize: 128,
            memorySize: 256
        });
        await temporalNet.buildModel();
        this.registerModel('temporal_net_v1', temporalNet, ModelType.TEMPORAL_NETWORK);

        // Neuro Evolution Controller
        const neuroEvo = new NeuroEvolutionController({
            populationSize: 50,
            mutationRate: 0.1,
            eliteSize: 10
        });
        await neuroEvo.initialize();
        this.registerModel('neuro_evo_v1', neuroEvo, ModelType.NEURO_EVOLUTION);

        // Adicionar ao ensemble
        this.ensemble.addModel('temporal_net_v1', temporalNet, 1.2);
        this.ensemble.addModel('neuro_evo_v1', neuroEvo, 0.9);

        console.log(`✅ ${this.models.size} modelos inicializados`);
    }

    registerModel(id, model, type, metadata = {}) {
        const modelInfo = {
            id,
            model,
            type,
            metadata: {
                created: new Date(),
                version: '1.0.0',
                performance: { accuracy: 0, latency: 0 },
                ...metadata
            },
            isActive: true,
            predictionsCount: 0
        };

        this.models.set(id, modelInfo);
        this.modelRegistry.set(id, type);

        console.log(`📝 Modelo registrado: ${id} (${type})`);
        return modelInfo;
    }

    async predict(symbol, data, options = {}) {
        const startTime = Date.now();

        if (!this.isInitialized) {
            console.warn('⚠️  Sistema não inicializado, usando fallback');
            return this.getFallbackPrediction(symbol, data);
        }

        try {
            // Analisar contexto de mercado
            const context = await this.contextAnalyzer.analyze(symbol, data);

            // Determinar modelo ótimo para o contexto
            const optimalModelType = this.contextAnalyzer.getOptimalModelType(context);
            const symbolConfig = this.modelConfigs.get(this.getSymbolType(symbol)) ||
                this.modelConfigs.get('default');

            // Coletar previsões
            const predictions = [];

            // Previsão do modelo primário
            const primaryModel = this.getBestModelForType(optimalModelType);
            if (primaryModel) {
                const primaryPred = await this.getModelPrediction(
                    primaryModel.id,
                    primaryModel.model,
                    data,
                    context
                );
                predictions.push(primaryPred);
            }

            // Previsão do ensemble
            if (symbolConfig.ensemble) {
                const ensemblePred = await this.ensemble.predict(data);
                predictions.push({
                    modelId: 'ensemble',
                    ...ensemblePred,
                    latency: Date.now() - startTime
                });
            }

            // Combinar previsões
            const finalPrediction = this.combinePredictions(predictions, context);

            // Coletar telemetria
            this.collectTelemetry({
                symbol,
                timestamp: new Date(),
                predictions,
                finalPrediction,
                context,
                latency: Date.now() - startTime
            });

            // Atualizar métricas de desempenho
            if (options.actualValue !== undefined) {
                predictions.forEach(pred => {
                    this.performanceMetrics.addPrediction(
                        pred.modelId,
                        pred.value,
                        options.actualValue,
                        pred.latency,
                        context.regime
                    );
                });
            }

            // Otimização em tempo real
            if (this.config.realTimeLearning && options.actualValue !== undefined) {
                this.performRealTimeOptimization(predictions, options.actualValue);
            }

            return {
                symbol,
                prediction: finalPrediction.value,
                confidence: finalPrediction.confidence,
                confidenceLevel: this.getConfidenceLevel(finalPrediction.confidence),
                timestamp: new Date(),
                context,
                modelBreakdown: predictions.map(p => ({
                    modelId: p.modelId,
                    prediction: p.value,
                    confidence: p.confidence,
                    weight: p.weight || 1
                })),
                systemMetrics: this.getSystemMetrics(),
                recommendations: this.generateRecommendations(finalPrediction, context)
            };

        } catch (error) {
            console.error(`❌ Erro na previsão para ${symbol}:`, error);
            return this.getFallbackPrediction(symbol, data, error);
        }
    }

    async getModelPrediction(modelId, model, data, context) {
        const startTime = Date.now();

        try {
            const prediction = await model.process ?
                await model.process(data) :
                await model.predict(data);

            const latency = Date.now() - startTime;

            return {
                modelId,
                value: prediction.prediction || prediction.value || prediction,
                confidence: prediction.confidence || 0.7,
                latency,
                metadata: {
                    ...prediction,
                    regime: prediction.regime || context.regime,
                    timestamp: new Date()
                }
            };
        } catch (error) {
            console.error(`❌ Erro no modelo ${modelId}:`, error);
            return {
                modelId,
                value: 0,
                confidence: 0.1,
                latency: Date.now() - startTime,
                error: error.message
            };
        }
    }

    combinePredictions(predictions, context) {
        if (predictions.length === 0) {
            return { value: 0, confidence: 0 };
        }

        if (predictions.length === 1) {
            return {
                value: predictions[0].value,
                confidence: predictions[0].confidence
            };
        }

        // Média ponderada por confiança e desempenho histórico
        let totalWeight = 0;
        let weightedSum = 0;
        let maxConfidence = 0;

        for (const pred of predictions) {
            if (pred.error) continue;

            const modelMetrics = this.performanceMetrics.getModelMetrics(pred.modelId, 20);
            const historicalWeight = modelMetrics ? modelMetrics.recentConfidence / 100 : 0.5;

            const currentConfidence = pred.confidence || 0.5;
            const latencyPenalty = pred.latency > 100 ? 0.9 : 1.0;

            const weight = currentConfidence * historicalWeight * latencyPenalty;

            weightedSum += pred.value * weight;
            totalWeight += weight;
            maxConfidence = Math.max(maxConfidence, currentConfidence);
        }

        const finalValue = totalWeight > 0 ? weightedSum / totalWeight : 0;
        const avgConfidence = predictions.reduce((sum, p) => sum + (p.confidence || 0), 0) / predictions.length;

        // Ajustar confiança baseado no consenso
        const consensus = this.calculatePredictionConsensus(predictions);
        const adjustedConfidence = avgConfidence * (0.3 + 0.7 * consensus);

        return {
            value: finalValue,
            confidence: Math.min(adjustedConfidence, maxConfidence),
            consensus
        };
    }

    calculatePredictionConsensus(predictions) {
        if (predictions.length < 2) return 1;

        const signs = predictions.map(p => Math.sign(p.value || 0));
        const positiveCount = signs.filter(s => s > 0).length;
        const negativeCount = signs.filter(s => s < 0).length;
        const neutralCount = signs.filter(s => s === 0).length;

        const maxCount = Math.max(positiveCount, negativeCount, neutralCount);
        return maxCount / predictions.length;
    }

    getBestModelForType(type) {
        const modelsOfType = Array.from(this.models.values())
            .filter(m => m.type === type && m.isActive)
            .sort((a, b) => {
                const metricsA = this.performanceMetrics.getModelMetrics(a.id, 20);
                const metricsB = this.performanceMetrics.getModelMetrics(b.id, 20);
                const scoreA = metricsA ? metricsA.recentConfidence : 0;
                const scoreB = metricsB ? metricsB.recentConfidence : 0;
                return scoreB - scoreA;
            });

        return modelsOfType.length > 0 ? modelsOfType[0] : null;
    }

    getSymbolType(symbol) {
        if (symbol.includes('USDT') || symbol.includes('BTC')) return 'crypto';
        if (symbol.includes('/') && symbol.length === 7) return 'forex';
        return 'stocks';
    }

    getFallbackPrediction(symbol, data, error = null) {
        console.log(`🔄 Usando fallback para ${symbol}`);

        // Fallback simples baseado em média móvel
        const prices = data.prices || data.close || [];
        const recentPrices = prices.slice(-20);
        const avg = recentPrices.reduce((a, b) => a + b, 0) / recentPrices.length;
        const lastPrice = recentPrices[recentPrices.length - 1] || 0;

        const prediction = lastPrice > avg ? 0.02 : -0.02;

        return {
            symbol,
            prediction,
            confidence: 0.5,
            confidenceLevel: PredictionConfidence.LOW,
            timestamp: new Date(),
            fallback: true,
            error: error?.message,
            recommendation: 'Use with caution - fallback prediction'
        };
    }

    getConfidenceLevel(confidence) {
        if (confidence >= 0.9) return PredictionConfidence.VERY_HIGH;
        if (confidence >= 0.8) return PredictionConfidence.HIGH;
        if (confidence >= 0.7) return PredictionConfidence.MEDIUM;
        if (confidence >= 0.6) return PredictionConfidence.LOW;
        return PredictionConfidence.VERY_LOW;
    }

    collectTelemetry(data) {
        if (!this.config.telemetryEnabled) return;

        const telemetryEntry = {
            ...data,
            systemLoad: this.getSystemLoad(),
            memoryUsage: process.memoryUsage ? process.memoryUsage().heapUsed : 0
        };

        this.telemetry.push(telemetryEntry);

        // Manter telemetria limitada
        if (this.telemetry.length > 10000) {
            this.telemetry = this.telemetry.slice(-5000);
        }
    }

    getSystemMetrics() {
        return {
            totalModels: this.models.size,
            activeModels: Array.from(this.models.values()).filter(m => m.isActive).length,
            ensembleSize: this.ensemble.models.size,
            uptime: this.performanceMetrics.getUptime(),
            totalPredictions: this.performanceMetrics.predictions.length,
            avgLatency: this.performanceMetrics.latencyHistory.length > 0 ?
                this.performanceMetrics.latencyHistory.reduce((a, b) => a + b, 0) /
                this.performanceMetrics.latencyHistory.length : 0,
            systemLoad: this.getSystemLoad()
        };
    }

    getSystemLoad() {
        // Simulação de carga do sistema
        return {
            cpu: Math.random() * 0.5,
            memory: process.memoryUsage ? process.memoryUsage().heapUsed / (1024 * 1024) : 0,
            queueSize: this.telemetry.length
        };
    }

    generateRecommendations(prediction, context) {
        const recommendations = [];

        if (prediction.confidence < 0.6) {
            recommendations.push({
                type: 'warning',
                message: 'Low confidence prediction - consider manual verification',
                priority: 'high'
            });
        }

        if (context.volatility > 0.3) {
            recommendations.push({
                type: 'risk',
                message: 'High volatility environment - reduce position size',
                priority: 'medium'
            });
        }

        if (context.liquidity === 'low') {
            recommendations.push({
                type: 'liquidity',
                message: 'Low liquidity - wider spreads expected',
                priority: 'medium'
            });
        }

        return recommendations;
    }

    performRealTimeOptimization(predictions, actualValue) {
        // Atualizar pesos do ensemble
        this.ensemble.updateWeights(this.performanceMetrics);

        // Ajustar modelos individuais
        predictions.forEach(pred => {
            const modelInfo = this.models.get(pred.modelId);
            if (modelInfo && modelInfo.model.adapt) {
                try {
                    modelInfo.model.adapt(pred, actualValue);
                } catch (error) {
                    console.error(`❌ Erro na adaptação do modelo ${pred.modelId}:`, error);
                }
            }
        });
    }

    startContinuousOptimization() {
        setInterval(() => {
            this.optimizeModels();
        }, 300000); // A cada 5 minutos

        console.log('🔄 Otimização contínua iniciada');
    }

    async optimizeModels() {
        console.log('⚙️  Executando otimização de modelos...');

        try {
            // Reavaliar modelos com baixo desempenho
            for (const [modelId, modelInfo] of this.models) {
                const metrics = this.performanceMetrics.getModelMetrics(modelId, 50);

                if (metrics && metrics.avgAccuracy < 60) {
                    console.log(`⚠️  Modelo ${modelId} com baixa precisão: ${metrics.avgAccuracy.toFixed(1)}%`);

                    if (modelInfo.model.retrain) {
                        await modelInfo.model.retrain();
                        console.log(`🔄 Modelo ${modelId} retreinado`);
                    }
                }
            }

            // Otimizar ensemble
            this.ensemble.updateWeights(this.performanceMetrics);

            console.log('✅ Otimização concluída');
        } catch (error) {
            console.error('❌ Erro na otimização:', error);
        }
    }

    startTelemetryCollection() {
        setInterval(() => {
            this.saveTelemetrySnapshot();
        }, 60000); // A cada minuto
    }

    saveTelemetrySnapshot() {
        const snapshot = {
            timestamp: new Date(),
            metrics: this.getSystemMetrics(),
            performance: this.getPerformanceSummary(),
            models: Array.from(this.models.values()).map(m => ({
                id: m.id,
                type: m.type,
                isActive: m.isActive,
                predictionsCount: m.predictionsCount
            }))
        };

        // Em produção, salvar em banco de dados ou arquivo
        console.log('📊 Snapshot de telemetria:', snapshot.timestamp);
    }

    getPerformanceSummary() {
        const summary = {
            overall: {
                totalPredictions: this.performanceMetrics.predictions.length,
                avgAccuracy: this.performanceMetrics.accuracyHistory.length > 0 ?
                    this.performanceMetrics.accuracyHistory.reduce((a, b) => a + b, 0) /
                    this.performanceMetrics.accuracyHistory.length * 100 : 0,
                avgLatency: this.performanceMetrics.latencyHistory.length > 0 ?
                    this.performanceMetrics.latencyHistory.reduce((a, b) => a + b, 0) /
                    this.performanceMetrics.latencyHistory.length : 0
            },
            byModel: {}
        };

        for (const [modelId] of this.models) {
            const metrics = this.performanceMetrics.getModelMetrics(modelId, 100);
            if (metrics) {
                summary.byModel[modelId] = metrics;
            }
        }

        return summary;
    }

    getSystemStatus() {
        return {
            initialized: this.isInitialized,
            totalModels: this.models.size,
            ensembleSize: this.ensemble.models.size,
            uptime: this.performanceMetrics.getUptime(),
            performance: this.getPerformanceSummary().overall,
            config: this.config
        };
    }

    async addModel(model, id = null, type = ModelType.ENSEMBLE) {
        const modelId = id || `model_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        try {
            const modelInfo = this.registerModel(modelId, model, type);
            this.ensemble.addModel(modelId, model, 1.0);

            console.log(`✅ Modelo ${modelId} adicionado com sucesso`);
            return modelInfo;
        } catch (error) {
            console.error(`❌ Erro ao adicionar modelo ${modelId}:`, error);
            throw error;
        }
    }

    async removeModel(modelId) {
        if (this.models.has(modelId)) {
            this.models.delete(modelId);
            this.modelRegistry.delete(modelId);

            // Remover do ensemble
            this.ensemble.models.delete(modelId);
            this.ensemble.weights.delete(modelId);

            console.log(`🗑️  Modelo ${modelId} removido`);
            return true;
        }

        return false;
    }

    disableModel(modelId) {
        const modelInfo = this.models.get(modelId);
        if (modelInfo) {
            modelInfo.isActive = false;
            console.log(`⏸️  Modelo ${modelId} desativado`);
            return true;
        }
        return false;
    }

    enableModel(modelId) {
        const modelInfo = this.models.get(modelId);
        if (modelInfo) {
            modelInfo.isActive = true;
            console.log(`▶️  Modelo ${modelId} ativado`);
            return true;
        }
        return false;
    }

    getModelInfo(modelId) {
        const modelInfo = this.models.get(modelId);
        if (!modelInfo) return null;

        const metrics = this.performanceMetrics.getModelMetrics(modelId, 100);

        return {
            ...modelInfo,
            metrics,
            ensembleWeight: this.ensemble.weights.get(modelId) || 0
        };
    }

    listModels() {
        return Array.from(this.models.values()).map(modelInfo => ({
            id: modelInfo.id,
            type: modelInfo.type,
            isActive: modelInfo.isActive,
            predictionsCount: modelInfo.predictionsCount,
            metrics: this.performanceMetrics.getModelMetrics(modelInfo.id, 50)
        }));
    }

    resetSystem() {
        console.log('🔄 Resetando sistema...');

        this.performanceMetrics.reset();
        this.telemetry = [];

        // Manter modelos ativos
        Array.from(this.models.values()).forEach(modelInfo => {
            modelInfo.predictionsCount = 0;
        });

        console.log('✅ Sistema resetado');
        return this.getSystemStatus();
    }

    async shutdown() {
        console.log('🛑 Desligando AI System Manager...');

        // Salvar estado dos modelos
        await this.saveModelStates();

        // Limpar recursos
        this.models.clear();
        this.ensemble.models.clear();
        this.telemetry = [];

        console.log('✅ AI System Manager desligado');
    }

    async saveModelStates() {
        // Salvar estados dos modelos para persistência
        for (const [modelId, modelInfo] of this.models) {
            if (modelInfo.model.save) {
                try {
                    await modelInfo.model.save(`./models/${modelId}_state`);
                    console.log(`💾 Estado do modelo ${modelId} salvo`);
                } catch (error) {
                    console.error(`❌ Erro ao salvar estado do modelo ${modelId}:`, error);
                }
            }
        }
    }
}

// Exportar instância singleton
const aiSystemManager = new AISystemManager();

export default aiSystemManager;