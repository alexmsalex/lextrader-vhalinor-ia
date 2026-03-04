/**
 * autonomous_risk_manager.js - Sistema Avançado de Gestão de Risco Autônomo AGI
 * Sistema neural de detecção e mitigação de riscos em tempo real com aprendizado adaptativo
 */

import {
    RiskLevel,
    MarketRegime,
    Decision,
    Timeframe,
    EnumUtils
} from './algorithm_constants.js';
import { AdvancedTemporalNetwork } from './advanced_temporal_network.js';

export class AnomalyType {
    static VOLATILITY_SPIKE = {
        code: 'VOLATILITY_SPIKE',
        severity: 'HIGH',
        description: 'Aumento súbito na volatilidade do mercado',
        mitigation: 'REDUCE_POSITION_SIZE'
    };

    static LIQUIDITY_DROP = {
        code: 'LIQUIDITY_DROP',
        severity: 'CRITICAL',
        description: 'Queda significativa na liquidez do mercado',
        mitigation: 'EXIT_POSITIONS'
    };

    static CORRELATION_BREAKDOWN = {
        code: 'CORRELATION_BREAKDOWN',
        severity: 'MEDIUM',
        description: 'Ruptura em correlações históricas',
        mitigation: 'REBALANCE_PORTFOLIO'
    };

    static VOLUME_ANOMALY = {
        code: 'VOLUME_ANOMALY',
        severity: 'MEDIUM',
        description: 'Volume anormal em relação à média histórica',
        mitigation: 'INVESTIGATE_FURTHER'
    };

    static PRICE_GAP = {
        code: 'PRICE_GAP',
        severity: 'HIGH',
        description: 'Gap de preço significativo',
        mitigation: 'ADJUST_STOPS'
    };

    static NEWS_IMPACT = {
        code: 'NEWS_IMPACT',
        severity: 'VARIABLE',
        description: 'Impacto de notícias macroeconômicas',
        mitigation: 'PAUSE_TRADING'
    };

    static SENTIMENT_SHIFT = {
        code: 'SENTIMENT_SHIFT',
        severity: 'MEDIUM',
        description: 'Mudança brusca no sentimento de mercado',
        mitigation: 'REASSESS_STRATEGY'
    };

    static TECHNICAL_BREAKDOWN = {
        code: 'TECHNICAL_BREAKDOWN',
        severity: 'MEDIUM',
        description: 'Falha técnica no sistema ou conectividade',
        mitigation: 'ENTER_SAFE_MODE'
    };
}

export class AnomalyDetector {
    constructor(config = {}) {
        this.config = {
            historySize: config.historySize || 1000,
            detectionThreshold: config.detectionThreshold || 3.0,
            adaptiveThreshold: config.adaptiveThreshold !== false,
            enableMultivariate: config.enableMultivariate !== false,
            realTimeMonitoring: config.realTimeMonitoring !== false,
            anomalyWindow: config.anomalyWindow || 60, // minutos
            ...config
        };

        this.history = [];
        this.anomalyHistory = [];
        this.statisticalModels = new Map();
        this.machineLearningModel = null;
        this.temporalNetwork = new AdvancedTemporalNetwork({
            sequenceLength: 60,
            hiddenSize: 64,
            memorySize: 128
        });

        this.thresholds = {
            volatility: 3.0,
            volume: 2.5,
            correlation: 2.8,
            spread: 3.2,
            momentum: 2.7
        };

        this.initializeModels();
        console.log('🔍 Anomaly Detector inicializado');
    }

    initializeModels() {
        // Inicializar modelos estatísticos para diferentes métricas
        const metrics = ['volatility', 'volume', 'spread', 'momentum', 'liquidity'];

        metrics.forEach(metric => {
            this.statisticalModels.set(metric, {
                history: [],
                mean: 0,
                std: 0,
                lastUpdate: null,
                modelType: 'EXPONENTIAL_SMOOTHING'
            });
        });

        // Inicializar modelo de aprendizado de máquina
        this.initializeMLModel();

        // Iniciar monitoramento em tempo real se habilitado
        if (this.config.realTimeMonitoring) {
            this.startRealTimeMonitoring();
        }
    }

    initializeMLModel() {
        // Modelo simplificado de detecção de anomalias
        // Em produção, usar Isolation Forest, One-Class SVM, ou Autoencoder
        this.machineLearningModel = {
            features: ['volatility', 'volume', 'spread', 'rsi', 'momentum'],
            threshold: 0.95,
            trained: false,
            trainingData: [],

            predict: (features) => {
                if (!this.machineLearningModel.trained || features.length < 5) {
                    return { score: 0.5, isAnomaly: false };
                }

                // Simulação de predição - em produção usar modelo real
                const volatilityScore = Math.abs(features[0] - 0.02) / 0.02;
                const volumeScore = Math.abs(features[1] - 1.0) / 0.5;
                const spreadScore = Math.abs(features[2] - 0.0001) / 0.0001;

                const anomalyScore = (volatilityScore + volumeScore + spreadScore) / 3;
                const isAnomaly = anomalyScore > this.machineLearningModel.threshold;

                return { score: anomalyScore, isAnomaly };
            },

            train: (data) => {
                if (data.length < 100) return;

                // Treinamento simplificado
                this.machineLearningModel.trainingData = data;
                this.machineLearningModel.trained = true;
                console.log('🤖 Modelo ML de anomalias treinado');
            }
        };
    }

    startRealTimeMonitoring() {
        setInterval(() => {
            this.performHealthCheck();
        }, 30000); // A cada 30 segundos

        console.log('📊 Monitoramento em tempo real iniciado');
    }

    async detect(marketData, context = {}) {
        const startTime = Date.now();

        try {
            // Coletar métricas
            const metrics = this.collectMetrics(marketData, context);

            // Detecção multivariada
            const multivariateDetection = await this.multivariateDetection(metrics, context);

            // Detecção estatística univariada
            const statisticalDetection = this.statisticalDetection(metrics);

            // Detecção baseada em ML
            const mlDetection = this.mlDetection(metrics);

            // Detecção temporal
            const temporalDetection = await this.temporalDetection(marketData);

            // Combinação de detecções
            const combinedDetection = this.combineDetections([
                multivariateDetection,
                statisticalDetection,
                mlDetection,
                temporalDetection
            ], context);

            // Atualizar histórico
            this.updateHistory(metrics, combinedDetection);

            // Atualizar modelos
            this.updateModels(metrics, combinedDetection);

            // Gerar relatório
            const report = this.generateReport(combinedDetection, {
                processingTime: Date.now() - startTime,
                metrics,
                context
            });

            return report;

        } catch (error) {
            console.error('❌ Erro na detecção de anomalias:', error);
            return this.getFallbackDetection();
        }
    }

    collectMetrics(marketData, context) {
        const { close, high, low, volume, spread } = marketData;

        // Métricas básicas
        const volatility = this.calculateVolatility(close);
        const avgVolume = volume ? volume.reduce((a, b) => a + b, 0) / volume.length : 0;
        const currentVolume = volume ? volume[volume.length - 1] : 0;
        const volumeRatio = avgVolume > 0 ? currentVolume / avgVolume : 1;

        // Métricas de preço
        const momentum = this.calculateMomentum(close);
        const priceRange = (Math.max(...high) - Math.min(...low)) / Math.min(...low);

        // Métricas de liquidez
        const avgSpread = spread ? spread.reduce((a, b) => a + b, 0) / spread.length : 0.0001;
        const currentSpread = spread ? spread[spread.length - 1] : 0.0001;
        const spreadRatio = currentSpread / avgSpread;

        // Métricas técnicas
        const rsi = this.calculateRSI(close);
        const atr = this.calculateATR(high, low, close);

        // Métricas de contexto
        const marketRegime = context.marketRegime || 'SIDEWAYS';
        const session = context.tradingSession || 'REGULAR';

        return {
            timestamp: new Date(),
            volatility,
            volume: volumeRatio,
            spread: spreadRatio,
            momentum,
            priceRange,
            rsi,
            atr,
            marketRegime,
            session,
            raw: {
                close: close[close.length - 1],
                volume: currentVolume,
                spread: currentSpread
            }
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

        return Math.sqrt(variance) * Math.sqrt(252); // Anualizado
    }

    calculateMomentum(prices, period = 10) {
        if (prices.length < period) return 0;

        const recent = prices.slice(-period);
        const first = recent[0];
        const last = recent[recent.length - 1];

        return (last - first) / first;
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

    calculateATR(high, low, close, period = 14) {
        if (high.length < period || low.length < period || close.length < period) {
            return 0.01;
        }

        let trueRanges = [];
        for (let i = 1; i < period; i++) {
            const tr1 = high[i] - low[i];
            const tr2 = Math.abs(high[i] - close[i - 1]);
            const tr3 = Math.abs(low[i] - close[i - 1]);

            trueRanges.push(Math.max(tr1, tr2, tr3));
        }

        return trueRanges.reduce((a, b) => a + b, 0) / trueRanges.length;
    }

    async multivariateDetection(metrics, context) {
        if (!this.config.enableMultivariate) {
            return { anomalies: [], score: 0 };
        }

        const anomalies = [];
        let overallScore = 0;

        // Detecção de spike de volatilidade
        const volatilityAnomaly = this.detectVolatilitySpike(metrics, context);
        if (volatilityAnomaly.isAnomaly) {
            anomalies.push(volatilityAnomaly);
            overallScore += volatilityAnomaly.severityWeight;
        }

        // Detecção de anomalia de volume
        const volumeAnomaly = this.detectVolumeAnomaly(metrics, context);
        if (volumeAnomaly.isAnomaly) {
            anomalies.push(volumeAnomaly);
            overallScore += volumeAnomaly.severityWeight;
        }

        // Detecção de anomalia de spread
        const spreadAnomaly = this.detectSpreadAnomaly(metrics, context);
        if (spreadAnomaly.isAnomaly) {
            anomalies.push(spreadAnomaly);
            overallScore += spreadAnomaly.severityWeight;
        }

        // Detecção de quebra de correlação
        const correlationAnomaly = await this.detectCorrelationBreakdown(context);
        if (correlationAnomaly.isAnomaly) {
            anomalies.push(correlationAnomaly);
            overallScore += correlationAnomaly.severityWeight;
        }

        return {
            anomalies,
            score: overallScore / (anomalies.length || 1),
            isAnomaly: anomalies.length > 0,
            method: 'MULTIVARIATE'
        };
    }

    detectVolatilitySpike(metrics, context) {
        const model = this.statisticalModels.get('volatility');
        const zScore = this.calculateZScore(metrics.volatility, model);

        const isAnomaly = zScore > this.thresholds.volatility;
        const severity = this.calculateSeverity(zScore, this.thresholds.volatility);

        return {
            type: AnomalyType.VOLATILITY_SPIKE,
            isAnomaly,
            score: zScore,
            severity,
            severityWeight: severity === 'CRITICAL' ? 2.0 : severity === 'HIGH' ? 1.5 : 1.0,
            metrics: {
                current: metrics.volatility,
                mean: model.mean,
                std: model.std,
                zScore
            },
            context: {
                marketRegime: metrics.marketRegime,
                session: metrics.session
            }
        };
    }

    detectVolumeAnomaly(metrics, context) {
        const model = this.statisticalModels.get('volume');
        const zScore = this.calculateZScore(metrics.volume, model);

        const isAnomaly = zScore > this.thresholds.volume;
        const severity = this.calculateSeverity(zScore, this.thresholds.volume);

        return {
            type: AnomalyType.VOLUME_ANOMALY,
            isAnomaly,
            score: zScore,
            severity,
            severityWeight: severity === 'CRITICAL' ? 2.0 : severity === 'HIGH' ? 1.5 : 1.0,
            metrics: {
                current: metrics.volume,
                mean: model.mean,
                std: model.std,
                zScore
            }
        };
    }

    detectSpreadAnomaly(metrics, context) {
        const model = this.statisticalModels.get('spread');
        const zScore = this.calculateZScore(metrics.spread, model);

        const isAnomaly = zScore > this.thresholds.spread;
        const severity = this.calculateSeverity(zScore, this.thresholds.spread);

        return {
            type: AnomalyType.LIQUIDITY_DROP,
            isAnomaly,
            score: zScore,
            severity,
            severityWeight: severity === 'CRITICAL' ? 2.0 : severity === 'HIGH' ? 1.5 : 1.0,
            metrics: {
                current: metrics.spread,
                mean: model.mean,
                std: model.std,
                zScore
            }
        };
    }

    async detectCorrelationBreakdown(context) {
        // Em produção, calcular correlações entre ativos
        // Aqui é uma implementação simplificada
        const correlationScore = 0.2; // Placeholder

        const isAnomaly = correlationScore < 0.3; // Correlação muito baixa
        const severity = isAnomaly ? 'MEDIUM' : 'LOW';

        return {
            type: AnomalyType.CORRELATION_BREAKDOWN,
            isAnomaly,
            score: correlationScore,
            severity,
            severityWeight: 1.0,
            metrics: {
                correlationScore
            }
        };
    }

    statisticalDetection(metrics) {
        const anomalies = [];
        let overallScore = 0;

        // Verificar cada métrica com seu modelo estatístico
        for (const [metricName, model] of this.statisticalModels) {
            const metricValue = metrics[metricName];
            if (metricValue === undefined) continue;

            const zScore = this.calculateZScore(metricValue, model);
            const threshold = this.thresholds[metricName] || 3.0;

            if (zScore > threshold) {
                const severity = this.calculateSeverity(zScore, threshold);

                anomalies.push({
                    metric: metricName,
                    value: metricValue,
                    zScore,
                    threshold,
                    severity,
                    modelStats: {
                        mean: model.mean,
                        std: model.std,
                        sampleSize: model.history.length
                    }
                });

                overallScore += zScore;
            }
        }

        return {
            anomalies,
            score: anomalies.length > 0 ? overallScore / anomalies.length : 0,
            isAnomaly: anomalies.length > 0,
            method: 'STATISTICAL'
        };
    }

    mlDetection(metrics) {
        if (!this.machineLearningModel || !this.machineLearningModel.trained) {
            return { isAnomaly: false, score: 0, method: 'ML' };
        }

        const features = [
            metrics.volatility,
            metrics.volume,
            metrics.spread,
            metrics.rsi / 100, // Normalizar RSI
            metrics.momentum
        ];

        const prediction = this.machineLearningModel.predict(features);

        return {
            isAnomaly: prediction.isAnomaly,
            score: prediction.score,
            confidence: Math.abs(prediction.score - 0.5) * 2,
            method: 'ML',
            features
        };
    }

    async temporalDetection(marketData) {
        try {
            // Usar a rede temporal para detectar padrões anômalos
            const sequence = this.prepareTemporalSequence(marketData);
            const prediction = await this.temporalNetwork.process(sequence);

            // Análise da previsão da rede temporal
            const confidence = prediction.confidence || 0.5;
            const regime = prediction.regime;

            // Detectar anomalias baseadas na confiança da rede
            const isAnomaly = confidence < 0.3; // Baixa confiança = possível anomalia
            const score = 1 - confidence; // Inverter confiança para score de anomalia

            return {
                isAnomaly,
                score,
                confidence,
                regime,
                method: 'TEMPORAL',
                temporalFeatures: {
                    sequenceLength: sequence.length,
                    prediction: prediction.horizons
                }
            };

        } catch (error) {
            console.error('❌ Erro na detecção temporal:', error);
            return { isAnomaly: false, score: 0, method: 'TEMPORAL' };
        }
    }

    prepareTemporalSequence(marketData) {
        const { close, high, low, volume } = marketData;
        const sequenceLength = Math.min(60, close.length);

        const sequence = [];
        for (let i = close.length - sequenceLength; i < close.length; i++) {
            sequence.push({
                close: close[i] || 0,
                high: high[i] || 0,
                low: low[i] || 0,
                volume: volume ? volume[i] || 0 : 0,
                returns: i > 0 ? (close[i] - close[i - 1]) / close[i - 1] : 0
            });
        }

        return sequence;
    }

    combineDetections(detections, context) {
        if (detections.length === 0) {
            return {
                isAnomaly: false,
                overallScore: 0,
                confidence: 1.0,
                details: []
            };
        }

        // Pesos para diferentes métodos de detecção
        const methodWeights = {
            MULTIVARIATE: 1.5,
            STATISTICAL: 1.2,
            ML: 1.8,
            TEMPORAL: 1.3
        };

        let weightedSum = 0;
        let totalWeight = 0;
        const details = [];
        let anyAnomaly = false;

        detections.forEach(detection => {
            const weight = methodWeights[detection.method] || 1.0;
            const weightedScore = detection.score * weight;

            weightedSum += weightedScore;
            totalWeight += weight;

            if (detection.isAnomaly) {
                anyAnomaly = true;
            }

            details.push({
                method: detection.method,
                score: detection.score,
                weightedScore,
                isAnomaly: detection.isAnomaly,
                details: detection.anomalies || detection
            });
        });

        const overallScore = totalWeight > 0 ? weightedSum / totalWeight : 0;

        // Ajustar baseado no contexto
        const contextAdjustment = this.calculateContextAdjustment(context);
        const adjustedScore = overallScore * contextAdjustment;

        // Determinar se é anomalia baseado no score ajustado
        const isAnomaly = anyAnomaly && adjustedScore > 0.7;

        return {
            isAnomaly,
            overallScore: adjustedScore,
            confidence: this.calculateConfidence(detections),
            details,
            context: {
                adjustment: contextAdjustment,
                marketConditions: context.marketRegime
            }
        };
    }

    calculateContextAdjustment(context) {
        let adjustment = 1.0;

        // Ajustar baseado no regime de mercado
        const regime = context.marketRegime;
        if (regime === 'HIGH_VOLATILITY') {
            adjustment *= 0.8; // Menos sensível em alta volatilidade
        } else if (regime === 'LOW_VOLATILITY') {
            adjustment *= 1.2; // Mais sensível em baixa volatilidade
        }

        // Ajustar baseado na sessão
        const session = context.tradingSession;
        if (session === 'ASIA' || session === 'PACIFIC') {
            adjustment *= 0.9; // Menos liquidez
        } else if (session === 'OVERLAP_LONDON_NY') {
            adjustment *= 1.1; // Mais atividade
        }

        return Math.max(0.5, Math.min(2.0, adjustment));
    }

    calculateConfidence(detections) {
        if (detections.length === 0) return 0.5;

        const agreeingDetections = detections.filter(d => d.isAnomaly).length;
        const agreement = agreeingDetections / detections.length;

        // Média ponderada das confianças
        let totalConfidence = 0;
        detections.forEach(d => {
            totalConfidence += d.confidence || 0.5;
        });

        const avgConfidence = totalConfidence / detections.length;

        return (agreement + avgConfidence) / 2;
    }

    calculateZScore(value, model) {
        if (model.history.length < 10 || model.std === 0) {
            return 0;
        }

        return Math.abs((value - model.mean) / model.std);
    }

    calculateSeverity(zScore, threshold) {
        if (zScore > threshold * 2) return 'CRITICAL';
        if (zScore > threshold * 1.5) return 'HIGH';
        if (zScore > threshold) return 'MEDIUM';
        return 'LOW';
    }

    updateHistory(metrics, detection) {
        const entry = {
            timestamp: metrics.timestamp,
            metrics,
            detection,
            isAnomaly: detection.isAnomaly
        };

        this.history.push(entry);

        // Manter histórico limitado
        if (this.history.length > this.config.historySize) {
            this.history = this.history.slice(-this.config.historySize);
        }

        // Atualizar histórico de anomalias
        if (detection.isAnomaly) {
            this.anomalyHistory.push({
                ...entry,
                severity: this.calculateOverallSeverity(detection)
            });

            if (this.anomalyHistory.length > 1000) {
                this.anomalyHistory = this.anomalyHistory.slice(-500);
            }
        }
    }

    calculateOverallSeverity(detection) {
        const score = detection.overallScore;

        if (score > 0.9) return 'CRITICAL';
        if (score > 0.7) return 'HIGH';
        if (score > 0.5) return 'MEDIUM';
        return 'LOW';
    }

    updateModels(metrics, detection) {
        // Atualizar modelos estatísticos
        for (const [metricName, model] of this.statisticalModels) {
            const value = metrics[metricName];
            if (value !== undefined) {
                model.history.push(value);

                if (model.history.length > 100) {
                    model.history = model.history.slice(-100);
                }

                // Recalcular estatísticas
                model.mean = model.history.reduce((a, b) => a + b, 0) / model.history.length;
                model.std = Math.sqrt(
                    model.history.reduce((sum, val) => sum + Math.pow(val - model.mean, 2), 0) /
                    model.history.length
                );

                model.lastUpdate = new Date();
            }
        }

        // Atualizar modelo ML
        if (this.machineLearningModel && !detection.isAnomaly) {
            // Apenas adicionar exemplos normais para treinamento
            const features = [
                metrics.volatility,
                metrics.volume,
                metrics.spread,
                metrics.rsi / 100,
                metrics.momentum
            ];

            this.machineLearningModel.trainingData.push({
                features,
                label: 'NORMAL',
                timestamp: metrics.timestamp
            });

            // Treinar periodicamente
            if (this.machineLearningModel.trainingData.length % 100 === 0) {
                this.machineLearningModel.train(this.machineLearningModel.trainingData);
            }
        }

        // Ajustar thresholds adaptativamente
        if (this.config.adaptiveThreshold) {
            this.adaptThresholds(detection);
        }
    }

    adaptThresholds(detection) {
        // Ajustar thresholds baseado na taxa de detecção
        const recentHistory = this.history.slice(-100);
        const anomalyRate = recentHistory.filter(h => h.isAnomaly).length / recentHistory.length;

        // Se detectando muitas anomalias, aumentar thresholds
        if (anomalyRate > 0.1) { // > 10% de anomalias
            Object.keys(this.thresholds).forEach(key => {
                this.thresholds[key] *= 1.05; // Aumentar 5%
            });
        }
        // Se detectando poucas anomalias, diminuir thresholds
        else if (anomalyRate < 0.02) { // < 2% de anomalias
            Object.keys(this.thresholds).forEach(key => {
                this.thresholds[key] *= 0.95; // Diminuir 5%
            });
        }

        // Limitar thresholds
        Object.keys(this.thresholds).forEach(key => {
            this.thresholds[key] = Math.max(2.0, Math.min(5.0, this.thresholds[key]));
        });
    }

    generateReport(detection, metadata) {
        const report = {
            timestamp: new Date(),
            isAnomaly: detection.isAnomaly,
            overallScore: detection.overallScore,
            confidence: detection.confidence,
            severity: this.calculateOverallSeverity(detection),
            details: detection.details,
            metadata: {
                processingTime: metadata.processingTime,
                metrics: metadata.metrics,
                context: metadata.context
            },
            recommendations: this.generateRecommendations(detection),
            systemStatus: this.getSystemStatus()
        };

        return report;
    }

    generateRecommendations(detection) {
        if (!detection.isAnomaly) {
            return [{
                action: 'CONTINUE_NORMAL',
                priority: 'LOW',
                description: 'Nenhuma anomalia detectada - operação normal'
            }];
        }

        const recommendations = [];
        const severity = this.calculateOverallSeverity(detection);

        // Recomendações baseadas na severidade
        if (severity === 'CRITICAL') {
            recommendations.push({
                action: 'IMMEDIATE_SHUTDOWN',
                priority: 'CRITICAL',
                description: 'Anomalia crítica detectada - encerrar todas as operações',
                steps: [
                    'Close all positions',
                    'Cancel all pending orders',
                    'Enter safe mode',
                    'Notify administrators'
                ]
            });
        } else if (severity === 'HIGH') {
            recommendations.push({
                action: 'REDUCE_EXPOSURE',
                priority: 'HIGH',
                description: 'Anomalia alta detectada - reduzir exposição',
                steps: [
                    'Reduce position sizes by 50%',
                    'Widen stop losses',
                    'Avoid new positions',
                    'Monitor closely'
                ]
            });
        } else if (severity === 'MEDIUM') {
            recommendations.push({
                action: 'INCREASE_CAUTION',
                priority: 'MEDIUM',
                description: 'Anomalia média detectada - aumentar cautela',
                steps: [
                    'Reduce position sizes by 25%',
                    'Review risk parameters',
                    'Monitor for escalation'
                ]
            });
        } else {
            recommendations.push({
                action: 'MONITOR_CLOSELY',
                priority: 'LOW',
                description: 'Anomalia baixa detectada - monitorar situação',
                steps: [
                    'Continue with caution',
                    'Review anomaly details',
                    'Prepare contingency plans'
                ]
            });
        }

        // Recomendações específicas baseadas no tipo de anomalia
        detection.details.forEach(detail => {
            if (detail.details && detail.details.anomalies) {
                detail.details.anomalies.forEach(anomaly => {
                    if (anomaly.type && anomaly.type.mitigation) {
                        recommendations.push({
                            action: anomaly.type.mitigation,
                            priority: anomaly.severity || 'MEDIUM',
                            description: `Mitigar ${anomaly.type.code}: ${anomaly.type.description}`,
                            anomalyType: anomaly.type.code
                        });
                    }
                });
            }
        });

        return recommendations;
    }

    getFallbackDetection() {
        return {
            isAnomaly: false,
            overallScore: 0,
            confidence: 0.5,
            severity: 'LOW',
            details: [],
            recommendations: [{
                action: 'SYSTEM_ERROR',
                priority: 'MEDIUM',
                description: 'Sistema de detecção com erro - usar precaução'
            }],
            fallback: true
        };
    }

    performHealthCheck() {
        const health = {
            timestamp: new Date(),
            systemStatus: 'HEALTHY',
            metrics: {}
        };

        // Verificar modelos estatísticos
        for (const [metric, model] of this.statisticalModels) {
            health.metrics[metric] = {
                sampleSize: model.history.length,
                lastUpdate: model.lastUpdate,
                mean: model.mean,
                std: model.std
            };
        }

        // Verificar histórico
        health.historySize = this.history.length;
        health.anomalyHistorySize = this.anomalyHistory.length;

        // Verificar thresholds
        health.thresholds = { ...this.thresholds };

        // Verificar performance recente
        const recentAnomalies = this.history.slice(-100).filter(h => h.isAnomaly).length;
        health.anomalyRate = recentAnomalies / 100;

        // Determinar status
        if (health.anomalyRate > 0.3) {
            health.systemStatus = 'HIGH_ALERT';
        } else if (health.anomalyRate > 0.15) {
            health.systemStatus = 'WARNING';
        } else if (this.history.length < 50) {
            health.systemStatus = 'INITIALIZING';
        }

        console.log('🏥 Health Check:', health.systemStatus, `Anomaly Rate: ${(health.anomalyRate * 100).toFixed(1)}%`);

        return health;
    }

    getSystemStatus() {
        return {
            historySize: this.history.length,
            anomalyHistorySize: this.anomalyHistory.length,
            statisticalModels: Array.from(this.statisticalModels.keys()),
            mlModelTrained: this.machineLearningModel?.trained || false,
            adaptiveThresholds: this.config.adaptiveThreshold,
            realTimeMonitoring: this.config.realTimeMonitoring,
            thresholds: { ...this.thresholds },
            recentAnomalyRate: this.calculateRecentAnomalyRate(),
            systemUptime: Date.now() - this.startTime
        };
    }

    calculateRecentAnomalyRate() {
        if (this.history.length < 10) return 0;

        const recent = this.history.slice(-100);
        const anomalies = recent.filter(h => h.isAnomaly).length;
        return anomalies / recent.length;
    }

    getAnomalyStatistics(timeframe = '24h') {
        const now = Date.now();
        let cutoff = now - (24 * 60 * 60 * 1000); // 24 horas padrão

        if (timeframe === '1h') cutoff = now - (60 * 60 * 1000);
        if (timeframe === '7d') cutoff = now - (7 * 24 * 60 * 60 * 1000);
        if (timeframe === '30d') cutoff = now - (30 * 24 * 60 * 60 * 1000);

        const recentAnomalies = this.anomalyHistory.filter(a =>
            a.timestamp.getTime() > cutoff
        );

        const statistics = {
            total: recentAnomalies.length,
            bySeverity: {},
            byType: {},
            timeline: []
        };

        // Agrupar por severidade
        recentAnomalies.forEach(anomaly => {
            const severity = anomaly.severity || 'LOW';
            statistics.bySeverity[severity] = (statistics.bySeverity[severity] || 0) + 1;

            // Agrupar por tipo se disponível
            if (anomaly.detection?.details) {
                anomaly.detection.details.forEach(detail => {
                    if (detail.details?.anomalies) {
                        detail.details.anomalies.forEach(a => {
                            if (a.type) {
                                const type = a.type.code;
                                statistics.byType[type] = (statistics.byType[type] || 0) + 1;
                            }
                        });
                    }
                });
            }
        });

        // Criar timeline (últimas 24 horas por hora)
        for (let i = 23; i >= 0; i--) {
            const hourStart = now - (i * 60 * 60 * 1000);
            const hourEnd = hourStart + (60 * 60 * 1000);

            const hourAnomalies = recentAnomalies.filter(a =>
                a.timestamp.getTime() >= hourStart && a.timestamp.getTime() < hourEnd
            );

            statistics.timeline.push({
                hour: new Date(hourStart).toISOString(),
                count: hourAnomalies.length,
                averageScore: hourAnomalies.length > 0 ?
                    hourAnomalies.reduce((sum, a) => sum + (a.detection?.overallScore || 0), 0) / hourAnomalies.length : 0
            });
        }

        return statistics;
    }

    reset() {
        this.history = [];
        this.anomalyHistory = [];

        // Resetar modelos estatísticos
        for (const [metric, model] of this.statisticalModels) {
            model.history = [];
            model.mean = 0;
            model.std = 0;
            model.lastUpdate = null;
        }

        // Resetar modelo ML
        if (this.machineLearningModel) {
            this.machineLearningModel.trainingData = [];
            this.machineLearningModel.trained = false;
        }

        // Resetar thresholds
        this.thresholds = {
            volatility: 3.0,
            volume: 2.5,
            correlation: 2.8,
            spread: 3.2,
            momentum: 2.7
        };

        console.log('🔄 Anomaly Detector resetado');
    }

    exportData() {
        return {
            config: { ...this.config },
            history: this.history.slice(-1000),
            anomalyHistory: this.anomalyHistory.slice(-500),
            thresholds: { ...this.thresholds },
            statisticalModels: Object.fromEntries(
                Array.from(this.statisticalModels.entries()).map(([key, model]) => [
                    key,
                    {
                        mean: model.mean,
                        std: model.std,
                        sampleSize: model.history.length
                    }
                ])
            ),
            systemStatus: this.getSystemStatus(),
            exportTimestamp: new Date()
        };
    }

    importData(data) {
        if (!data) return;

        if (data.config) {
            this.config = { ...this.config, ...data.config };
        }

        if (data.history) {
            this.history = data.history;
        }

        if (data.anomalyHistory) {
            this.anomalyHistory = data.anomalyHistory;
        }

        if (data.thresholds) {
            this.thresholds = { ...this.thresholds, ...data.thresholds };
        }

        if (data.statisticalModels) {
            Object.keys(data.statisticalModels).forEach(key => {
                const modelData = data.statisticalModels[key];
                if (this.statisticalModels.has(key)) {
                    const model = this.statisticalModels.get(key);
                    model.mean = modelData.mean || 0;
                    model.std = modelData.std || 0;
                }
            });
        }

        console.log('📥 Dados do Anomaly Detector importados');
    }
}

export class AutonomousRiskManager {
    constructor(config = {}) {
        this.config = {
            riskAppetite: config.riskAppetite || 'MODERATE',
            maxDrawdown: config.maxDrawdown || 0.15,
            maxPositionSize: config.maxPositionSize || 0.1,
            maxDailyLoss: config.maxDailyLoss || 0.05,
            enableAutoHedge: config.enableAutoHedge !== false,
            anomalyResponse: config.anomalyResponse || 'ADAPTIVE',
            circuitBreakers: config.circuitBreakers !== false,
            ...config
        };

        this.anomalyDetector = new AnomalyDetector({
            realTimeMonitoring: true,
            adaptiveThreshold: true,
            enableMultivariate: true
        });

        this.riskMetrics = {
            currentDrawdown: 0,
            dailyPnL: 0,
            totalExposure: 0,
            winRate: 0.5,
            sharpeRatio: 1.0,
            maxConsecutiveLosses: 0,
            currentConsecutiveLosses: 0
        };

        this.positions = new Map();
        this.riskLimits = this.calculateRiskLimits();
        this.circuitBreakers = new Map();
        this.hedgingStrategies = new Map();
        this.riskHistory = [];

        this.startTime = Date.now();

        this.initializeCircuitBreakers();
        this.initializeHedgingStrategies();

        console.log('🛡️  Autonomous Risk Manager inicializado');
    }

    calculateRiskLimits() {
        const baseLimits = {
            maxDrawdown: this.config.maxDrawdown,
            maxPositionSize: this.config.maxPositionSize,
            maxDailyLoss: this.config.maxDailyLoss,
            maxConcurrentPositions: 5,
            maxCorrelation: 0.7,
            minLiquidity: 1000000 // Volume mínimo em USD
        };

        // Ajustar baseado no apetite ao risco
        switch (this.config.riskAppetite) {
            case 'VERY_LOW':
                baseLimits.maxDrawdown *= 0.5;
                baseLimits.maxPositionSize *= 0.5;
                baseLimits.maxDailyLoss *= 0.5;
                break;
            case 'LOW':
                baseLimits.maxDrawdown *= 0.7;
                baseLimits.maxPositionSize *= 0.7;
                baseLimits.maxDailyLoss *= 0.7;
                break;
            case 'HIGH':
                baseLimits.maxDrawdown *= 1.5;
                baseLimits.maxPositionSize *= 1.5;
                baseLimits.maxDailyLoss *= 1.5;
                break;
            case 'VERY_HIGH':
                baseLimits.maxDrawdown *= 2.0;
                baseLimits.maxPositionSize *= 2.0;
                baseLimits.maxDailyLoss *= 2.0;
                break;
        }

        return baseLimits;
    }

    initializeCircuitBreakers() {
        // Circuit breakers para diferentes níveis de risco
        this.circuitBreakers.set('LEVEL_1', {
            threshold: 0.05, // 5% drawdown
            action: 'REDUCE_LEVERAGE',
            description: 'Reduzir alavancagem em 50%'
        });

        this.circuitBreakers.set('LEVEL_2', {
            threshold: 0.10, // 10% drawdown
            action: 'HALF_POSITIONS',
            description: 'Reduzir posições pela metade'
        });

        this.circuitBreakers.set('LEVEL_3', {
            threshold: this.riskLimits.maxDrawdown * 0.8, // 80% do máximo
            action: 'CLOSE_ALL',
            description: 'Fechar todas as posições'
        });

        this.circuitBreakers.set('LEVEL_4', {
            threshold: this.riskLimits.maxDrawdown, // Drawdown máximo
            action: 'FULL_SHUTDOWN',
            description: 'Desligamento completo do sistema'
        });
    }

    initializeHedgingStrategies() {
        // Estratégias de hedge para diferentes cenários
        this.hedgingStrategies.set('VOLATILITY_HEDGE', {
            condition: (metrics) => metrics.volatility > 0.03,
            action: 'BUY_VXX', // ETF de volatilidade
            description: 'Hedge contra aumento de volatilidade'
        });

        this.hedgingStrategies.set('MARKET_DOWNTURN_HEDGE', {
            condition: (metrics) => metrics.marketRegime === 'TRENDING_DOWN',
            action: 'BUY_PUTS',
            description: 'Hedge contra tendência de baixa'
        });

        this.hedgingStrategies.set('CORRELATION_HEDGE', {
            condition: (metrics) => metrics.correlation > 0.8,
            action: 'DIVERSIFY',
            description: 'Hedge contra alta correlação'
        });

        this.hedgingStrategies.set('LIQUIDITY_HEDGE', {
            condition: (metrics) => metrics.liquidity < this.riskLimits.minLiquidity,
            action: 'REDUCE_SIZE',
            description: 'Hedge contra baixa liquidez'
        });
    }

    async assessRisk(positions, marketData, context = {}) {
        const startTime = Date.now();

        try {
            // Atualizar posições
            this.updatePositions(positions);

            // Calcular métricas de risco atuais
            const currentRisk = this.calculateCurrentRisk();

            // Detectar anomalias de mercado
            const anomalyReport = await this.anomalyDetector.detect(marketData, context);

            // Verificar circuit breakers
            const circuitBreakerCheck = this.checkCircuitBreakers(currentRisk);

            // Avaliar necessidade de hedge
            const hedgeAssessment = this.assessHedgingNeeds(currentRisk, marketData, context);

            // Gerar recomendações de risco
            const recommendations = this.generateRiskRecommendations(
                currentRisk,
                anomalyReport,
                circuitBreakerCheck,
                hedgeAssessment
            );

            // Calcular limites de posição ajustados
            const adjustedLimits = this.calculateAdjustedLimits(
                currentRisk,
                anomalyReport,
                recommendations
            );

            // Gerar relatório completo
            const report = this.generateRiskReport({
                currentRisk,
                anomalyReport,
                circuitBreakerCheck,
                hedgeAssessment,
                recommendations,
                adjustedLimits,
                processingTime: Date.now() - startTime,
                context
            });

            // Atualizar histórico
            this.updateRiskHistory(report);

            return report;

        } catch (error) {
            console.error('❌ Erro na avaliação de risco:', error);
            return this.getFallbackRiskAssessment();
        }
    }

    updatePositions(positions) {
        this.positions.clear();

        positions.forEach(position => {
            this.positions.set(position.id, {
                ...position,
                timestamp: new Date(),
                currentValue: position.size * position.currentPrice,
                unrealizedPnl: (position.currentPrice - position.entryPrice) * position.size *
                    (position.direction === 'LONG' ? 1 : -1),
                riskMetrics: this.calculatePositionRisk(position)
            });
        });
    }

    calculatePositionRisk(position) {
        const risk = {
            exposure: position.size * position.currentPrice,
            stopDistance: Math.abs(position.currentPrice - position.stopLoss) / position.currentPrice,
            profitDistance: Math.abs(position.takeProfit - position.currentPrice) / position.currentPrice,
            riskRewardRatio: 0
        };

        if (risk.stopDistance > 0) {
            risk.riskRewardRatio = risk.profitDistance / risk.stopDistance;
        }

        return risk;
    }

    calculateCurrentRisk() {
        const positions = Array.from(this.positions.values());

        if (positions.length === 0) {
            return {
                exposure: 0,
                drawdown: this.riskMetrics.currentDrawdown,
                dailyPnL: this.riskMetrics.dailyPnL,
                positionCount: 0,
                concentration: 0,
                correlationRisk: 0,
                overallScore: 0.1
            };
        }

        // Calcular exposição total
        const totalExposure = positions.reduce((sum, pos) =>
            sum + Math.abs(pos.currentValue), 0);

        // Calcular PnL total
        const totalPnL = positions.reduce((sum, pos) => sum + pos.unrealizedPnl, 0);

        // Calcular drawdown
        const drawdown = totalPnL < 0 ? Math.abs(totalPnL / totalExposure) : 0;

        // Calcular concentração
        const largestPosition = Math.max(...positions.map(p => Math.abs(p.currentValue)));
        const concentration = largestPosition / totalExposure;

        // Calcular risco de correlação (simplificado)
        const correlationRisk = this.calculatePortfolioCorrelation(positions);

        // Calcular score geral de risco
        const riskScore = this.calculateRiskScore({
            exposure: totalExposure,
            drawdown,
            concentration,
            correlationRisk,
            positionCount: positions.length,
            dailyPnL: this.riskMetrics.dailyPnL
        });

        return {
            exposure: totalExposure,
            drawdown,
            dailyPnL: this.riskMetrics.dailyPnL,
            totalPnL,
            positionCount: positions.length,
            concentration,
            correlationRisk,
            overallScore: riskScore,
            positions: positions.map(p => ({
                id: p.id,
                symbol: p.symbol,
                exposure: p.currentValue,
                pnl: p.unrealizedPnl,
                risk: p.riskMetrics
            }))
        };
    }

    calculatePortfolioCorrelation(positions) {
        if (positions.length < 2) return 0;

        // Implementação simplificada
        // Em produção, usar matriz de correlação real
        let totalCorrelation = 0;
        let count = 0;

        for (let i = 0; i < positions.length; i++) {
            for (let j = i + 1; j < positions.length; j++) {
                const pos1 = positions[i];
                const pos2 = positions[j];

                // Correlação simplificada baseada no símbolo
                let correlation = 0.2; // Baixa por padrão

                if (pos1.symbol.split('/')[0] === pos2.symbol.split('/')[0]) {
                    correlation = 0.8; // Alta se mesma moeda base
                } else if (pos1.symbol.split('/')[1] === pos2.symbol.split('/')[1]) {
                    correlation = 0.6; // Média se mesma moeda de cotação
                }

                totalCorrelation += correlation;
                count++;
            }
        }

        return count > 0 ? totalCorrelation / count : 0;
    }

    calculateRiskScore(riskMetrics) {
        const weights = {
            drawdown: 0.4,
            exposure: 0.2,
            concentration: 0.15,
            correlation: 0.15,
            dailyPnL: 0.1
        };

        // Normalizar métricas
        const normalizedDrawdown = Math.min(riskMetrics.drawdown / this.riskLimits.maxDrawdown, 1);
        const normalizedExposure = Math.min(riskMetrics.exposure / 100000, 1); // Assumindo $100k como referência
        const normalizedConcentration = riskMetrics.concentration;
        const normalizedCorrelation = riskMetrics.correlationRisk;
        const normalizedDailyPnL = Math.min(Math.abs(riskMetrics.dailyPnL) / this.riskLimits.maxDailyLoss, 1);

        // Calcular score ponderado
        const score =
            normalizedDrawdown * weights.drawdown +
            normalizedExposure * weights.exposure +
            normalizedConcentration * weights.concentration +
            normalizedCorrelation * weights.correlation +
            normalizedDailyPnL * weights.dailyPnL;

        return Math.min(1, Math.max(0, score));
    }

    checkCircuitBreakers(currentRisk) {
        const triggeredBreakers = [];
        const warnings = [];

        for (const [level, breaker] of this.circuitBreakers) {
            if (currentRisk.drawdown >= breaker.threshold) {
                triggeredBreakers.push({
                    level,
                    threshold: breaker.threshold,
                    action: breaker.action,
                    description: breaker.description,
                    currentDrawdown: currentRisk.drawdown
                });
            } else if (currentRisk.drawdown >= breaker.threshold * 0.8) {
                warnings.push({
                    level,
                    threshold: breaker.threshold,
                    warningThreshold: breaker.threshold * 0.8,
                    description: `Aproximando-se do circuit breaker ${level}`,
                    currentDrawdown: currentRisk.drawdown
                });
            }
        }

        return {
            triggeredBreakers,
            warnings,
            hasTriggered: triggeredBreakers.length > 0,
            hasWarnings: warnings.length > 0
        };
    }

    assessHedgingNeeds(currentRisk, marketData, context) {
        if (!this.config.enableAutoHedge) {
            return {
                needsHedge: false,
                strategies: [],
                reason: 'Auto-hedge desabilitado'
            };
        }

        const strategies = [];

        // Avaliar cada estratégia de hedge
        for (const [strategyName, strategy] of this.hedgingStrategies) {
            try {
                const shouldHedge = strategy.condition({
                    ...currentRisk,
                    ...marketData,
                    ...context
                });

                if (shouldHedge) {
                    strategies.push({
                        name: strategyName,
                        action: strategy.action,
                        description: strategy.description,
                        condition: 'TRIGGERED'
                    });
                }
            } catch (error) {
                console.error(`❌ Erro na avaliação da estratégia ${strategyName}:`, error);
            }
        }

        return {
            needsHedge: strategies.length > 0,
            strategies,
            marketConditions: context.marketRegime || 'UNKNOWN'
        };
    }

    generateRiskRecommendations(currentRisk, anomalyReport, circuitBreakerCheck, hedgeAssessment) {
        const recommendations = [];
        const priority = {
            CRITICAL: 4,
            HIGH: 3,
            MEDIUM: 2,
            LOW: 1
        };

        // Recomendações baseadas em circuit breakers
        circuitBreakerCheck.triggeredBreakers.forEach(breaker => {
            recommendations.push({
                type: 'CIRCUIT_BREAKER',
                action: breaker.action,
                priority: 'CRITICAL',
                description: `Circuit breaker ${breaker.level} acionado: ${breaker.description}`,
                details: {
                    currentDrawdown: currentRisk.drawdown,
                    threshold: breaker.threshold
                }
            });
        });

        // Recomendações baseadas em anomalias
        if (anomalyReport.isAnomaly) {
            anomalyReport.recommendations.forEach(rec => {
                recommendations.push({
                    type: 'ANOMALY_RESPONSE',
                    action: rec.action,
                    priority: rec.priority || 'HIGH',
                    description: `Resposta a anomalia: ${rec.description}`,
                    details: {
                        anomalyScore: anomalyReport.overallScore,
                        severity: anomalyReport.severity
                    }
                });
            });
        }

        // Recomendações baseadas em hedge
        if (hedgeAssessment.needsHedge) {
            hedgeAssessment.strategies.forEach(strategy => {
                recommendations.push({
                    type: 'HEDGING',
                    action: strategy.action,
                    priority: 'MEDIUM',
                    description: `Estratégia de hedge: ${strategy.description}`,
                    details: {
                        strategy: strategy.name,
                        condition: strategy.condition
                    }
                });
            });
        }

        // Recomendações baseadas em métricas de risco
        if (currentRisk.drawdown > this.riskLimits.maxDrawdown * 0.5) {
            recommendations.push({
                type: 'RISK_METRIC',
                action: 'REDUCE_POSITION_SIZE',
                priority: 'HIGH',
                description: `Drawdown elevado: ${(currentRisk.drawdown * 100).toFixed(1)}%`,
                details: {
                    current: currentRisk.drawdown,
                    limit: this.riskLimits.maxDrawdown
                }
            });
        }

        if (currentRisk.concentration > 0.5) {
            recommendations.push({
                type: 'CONCENTRATION',
                action: 'DIVERSIFY',
                priority: 'MEDIUM',
                description: `Concentração elevada: ${(currentRisk.concentration * 100).toFixed(1)}%`,
                details: {
                    concentration: currentRisk.concentration
                }
            });
        }

        // Ordenar por prioridade
        recommendations.sort((a, b) =>
            (priority[b.priority] || 0) - (priority[a.priority] || 0)
        );

        return recommendations;
    }

    calculateAdjustedLimits(currentRisk, anomalyReport, recommendations) {
        const adjusted = { ...this.riskLimits };
        let adjustmentFactor = 1.0;

        // Ajustar baseado em anomalias
        if (anomalyReport.isAnomaly) {
            const anomalySeverity = anomalyReport.severity;
            switch (anomalySeverity) {
                case 'CRITICAL':
                    adjustmentFactor *= 0.3;
                    break;
                case 'HIGH':
                    adjustmentFactor *= 0.5;
                    break;
                case 'MEDIUM':
                    adjustmentFactor *= 0.7;
                    break;
                case 'LOW':
                    adjustmentFactor *= 0.9;
                    break;
            }
        }

        // Ajustar baseado em circuit breakers
        if (recommendations.some(r => r.type === 'CIRCUIT_BREAKER')) {
            adjustmentFactor *= 0.5;
        }

        // Ajustar baseado no drawdown atual
        const drawdownRatio = currentRisk.drawdown / this.riskLimits.maxDrawdown;
        if (drawdownRatio > 0.5) {
            adjustmentFactor *= (1 - drawdownRatio * 0.5);
        }

        // Aplicar ajustes
        Object.keys(adjusted).forEach(key => {
            if (typeof adjusted[key] === 'number') {
                adjusted[key] *= adjustmentFactor;
            }
        });

        // Garantir limites mínimos
        adjusted.maxPositionSize = Math.max(0.01, adjusted.maxPositionSize);
        adjusted.maxDailyLoss = Math.max(0.01, adjusted.maxDailyLoss);

        return {
            original: this.riskLimits,
            adjusted,
            adjustmentFactor,
            reason: anomalyReport.isAnomaly ? 'ANOMALY_DETECTED' : 'RISK_ADJUSTMENT'
        };
    }

    generateRiskReport(data) {
        return {
            timestamp: new Date(),
            riskAssessment: {
                currentRisk: data.currentRisk,
                anomalyReport: data.anomalyReport,
                circuitBreakerCheck: data.circuitBreakerCheck,
                hedgeAssessment: data.hedgeAssessment
            },
            recommendations: data.recommendations,
            adjustedLimits: data.adjustedLimits,
            actions: this.determineActions(data.recommendations, data.adjustedLimits),
            metadata: {
                processingTime: data.processingTime,
                context: data.context,
                systemStatus: this.getSystemStatus()
            }
        };
    }

    determineActions(recommendations, adjustedLimits) {
        const actions = [];
        const actionMap = new Map();

        // Agrupar ações similares
        recommendations.forEach(rec => {
            if (!actionMap.has(rec.action)) {
                actionMap.set(rec.action, {
                    action: rec.action,
                    priorities: [],
                    descriptions: [],
                    types: []
                });
            }

            const action = actionMap.get(rec.action);
            action.priorities.push(rec.priority);
            action.descriptions.push(rec.description);
            action.types.push(rec.type);
        });

        // Converter para array e ordenar
        for (const [action, details] of actionMap) {
            const maxPriority = details.priorities.reduce((max, p) =>
                ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].indexOf(p) <
                    ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].indexOf(max) ? p : max,
                'LOW'
            );

            actions.push({
                action,
                priority: maxPriority,
                descriptions: details.descriptions,
                types: details.types,
                timestamp: new Date()
            });
        }

        // Ordenar por prioridade
        const priorityOrder = { CRITICAL: 4, HIGH: 3, MEDIUM: 2, LOW: 1 };
        actions.sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);

        return actions;
    }

    updateRiskHistory(report) {
        this.riskHistory.push(report);

        if (this.riskHistory.length > 10000) {
            this.riskHistory = this.riskHistory.slice(-5000);
        }

        // Atualizar métricas de risco
        this.updateRiskMetrics(report);
    }

    updateRiskMetrics(report) {
        const { currentRisk } = report.riskAssessment;

        // Atualizar drawdown
        this.riskMetrics.currentDrawdown = currentRisk.drawdown;

        // Atualizar PnL diário
        this.riskMetrics.dailyPnL = currentRisk.dailyPnL;

        // Atualizar exposição
        this.riskMetrics.totalExposure = currentRisk.exposure;

        // Atualizar sequência de perdas
        if (currentRisk.dailyPnL < 0) {
            this.riskMetrics.currentConsecutiveLosses++;
            this.riskMetrics.maxConsecutiveLosses = Math.max(
                this.riskMetrics.maxConsecutiveLosses,
                this.riskMetrics.currentConsecutiveLosses
            );
        } else {
            this.riskMetrics.currentConsecutiveLosses = 0;
        }
    }

    getFallbackRiskAssessment() {
        return {
            timestamp: new Date(),
            riskAssessment: {
                currentRisk: {
                    exposure: 0,
                    drawdown: 0,
                    dailyPnL: 0,
                    positionCount: 0,
                    overallScore: 0.1
                },
                anomalyReport: this.anomalyDetector.getFallbackDetection(),
                circuitBreakerCheck: { triggeredBreakers: [], warnings: [], hasTriggered: false },
                hedgeAssessment: { needsHedge: false, strategies: [] }
            },
            recommendations: [{
                type: 'SYSTEM_ERROR',
                action: 'USE_CAUTION',
                priority: 'HIGH',
                description: 'Erro no sistema de risco - usar máxima cautela'
            }],
            adjustedLimits: {
                original: this.riskLimits,
                adjusted: this.riskLimits,
                adjustmentFactor: 0.5,
                reason: 'SYSTEM_ERROR'
            },
            actions: [],
            metadata: {
                processingTime: 0,
                context: {},
                systemStatus: this.getSystemStatus(),
                fallback: true
            }
        };
    }

    getSystemStatus() {
        return {
            positions: this.positions.size,
            currentDrawdown: this.riskMetrics.currentDrawdown,
            dailyPnL: this.riskMetrics.dailyPnL,
            totalExposure: this.riskMetrics.totalExposure,
            consecutiveLosses: this.riskMetrics.currentConsecutiveLosses,
            maxConsecutiveLosses: this.riskMetrics.maxConsecutiveLosses,
            riskHistorySize: this.riskHistory.length,
            anomalyDetectorStatus: this.anomalyDetector.getSystemStatus(),
            circuitBreakers: Array.from(this.circuitBreakers.keys()),
            hedgingStrategies: Array.from(this.hedgingStrategies.keys()),
            systemUptime: Date.now() - this.startTime
        };
    }

    async executeRiskAction(action, parameters = {}) {
        console.log(`⚡ Executando ação de risco: ${action}`);

        try {
            switch (action) {
                case 'REDUCE_POSITION_SIZE':
                    return await this.reducePositionSize(parameters.percentage || 0.5);

                case 'CLOSE_ALL_POSITIONS':
                    return await this.closeAllPositions();

                case 'ENTER_SAFE_MODE':
                    return await this.enterSafeMode();

                case 'HEDGE_PORTFOLIO':
                    return await this.hedgePortfolio(parameters.strategy);

                case 'DIVERSIFY':
                    return await this.diversifyPortfolio();

                default:
                    console.warn(`⚠️ Ação de risco desconhecida: ${action}`);
                    return { success: false, error: 'Unknown action' };
            }
        } catch (error) {
            console.error(`❌ Erro ao executar ação ${action}:`, error);
            return { success: false, error: error.message };
        }
    }

    async reducePositionSize(percentage) {
        const positions = Array.from(this.positions.values());
        const actions = [];

        positions.forEach(position => {
            const newSize = position.size * (1 - percentage);
            actions.push({
                positionId: position.id,
                symbol: position.symbol,
                action: 'REDUCE',
                currentSize: position.size,
                newSize,
                reduction: percentage * 100
            });
        });

        // Em produção, executar ordens reais
        console.log(`📉 Reduzindo tamanho de posições em ${(percentage * 100).toFixed(1)}%`);

        return {
            success: true,
            actions,
            message: `Positions reduced by ${(percentage * 100).toFixed(1)}%`
        };
    }

    async closeAllPositions() {
        const positions = Array.from(this.positions.values());
        const actions = [];

        positions.forEach(position => {
            actions.push({
                positionId: position.id,
                symbol: position.symbol,
                action: 'CLOSE',
                size: position.size,
                price: position.currentPrice
            });
        });

        // Limpar posições locais
        this.positions.clear();

        console.log('🚫 Fechando todas as posições');

        return {
            success: true,
            actions,
            message: 'All positions closed'
        };
    }

    async enterSafeMode() {
        // Fechar todas as posições
        await this.closeAllPositions();

        // Reduzir limites de risco
        this.riskLimits.maxPositionSize *= 0.1;
        this.riskLimits.maxDailyLoss *= 0.1;

        // Desabilitar trading agressivo
        this.config.riskAppetite = 'VERY_LOW';

        console.log('🛡️  Entrando em modo de segurança');

        return {
            success: true,
            actions: ['CLOSED_ALL_POSITIONS', 'REDUCED_RISK_LIMITS', 'ENTERED_SAFE_MODE'],
            message: 'System entered safe mode'
        };
    }

    async hedgePortfolio(strategy) {
        console.log(`🛡️  Aplicando hedge: ${strategy}`);

        // Em produção, implementar lógica de hedge real
        return {
            success: true,
            strategy,
            message: 'Hedge applied'
        };
    }

    async diversifyPortfolio() {
        const positions = Array.from(this.positions.values());

        // Analisar concentração atual
        const symbols = positions.map(p => p.symbol);
        const uniqueSymbols = new Set(symbols);

        if (uniqueSymbols.size <= 1) {
            // Portfolio muito concentrado - recomendar diversificação
            return {
                success: false,
                message: 'Portfolio too concentrated',
                recommendation: 'Add uncorrelated assets'
            };
        }

        // Em produção, calcular e executar rebalanceamento
        return {
            success: true,
            currentDiversification: uniqueSymbols.size / positions.length,
            message: 'Diversification analysis complete'
        };
    }

    getRiskStatistics(timeframe = '24h') {
        const anomalyStats = this.anomalyDetector.getAnomalyStatistics(timeframe);

        // Calcular estatísticas de risco
        const recentAssessments = this.riskHistory.filter(r => {
            const cutoff = Date.now() - (24 * 60 * 60 * 1000);
            return r.timestamp.getTime() > cutoff;
        });

        const riskStats = {
            totalAssessments: recentAssessments.length,
            highRiskEvents: recentAssessments.filter(r =>
                r.riskAssessment.currentRisk.overallScore > 0.7
            ).length,
            circuitBreakerTriggers: recentAssessments.filter(r =>
                r.riskAssessment.circuitBreakerCheck.hasTriggered
            ).length,
            averageRiskScore: recentAssessments.length > 0 ?
                recentAssessments.reduce((sum, r) => sum + r.riskAssessment.currentRisk.overallScore, 0) /
                recentAssessments.length : 0,
            actionsTaken: recentAssessments.reduce((count, r) =>
                count + r.actions.length, 0
            )
        };

        return {
            anomalyStats,
            riskStats,
            timeframe,
            generatedAt: new Date()
        };
    }

    reset() {
        this.positions.clear();
        this.riskHistory = [];
        this.riskMetrics = {
            currentDrawdown: 0,
            dailyPnL: 0,
            totalExposure: 0,
            winRate: 0.5,
            sharpeRatio: 1.0,
            maxConsecutiveLosses: 0,
            currentConsecutiveLosses: 0
        };

        this.anomalyDetector.reset();

        console.log('🔄 Autonomous Risk Manager resetado');
    }

    exportData() {
        return {
            config: { ...this.config },
            riskMetrics: { ...this.riskMetrics },
            riskLimits: { ...this.riskLimits },
            positions: Array.from(this.positions.values()),
            riskHistory: this.riskHistory.slice(-1000),
            anomalyDetectorData: this.anomalyDetector.exportData(),
            exportTimestamp: new Date()
        };
    }

    importData(data) {
        if (!data) return;

        if (data.config) {
            this.config = { ...this.config, ...data.config };
        }

        if (data.riskMetrics) {
            this.riskMetrics = { ...this.riskMetrics, ...data.riskMetrics };
        }

        if (data.riskLimits) {
            this.riskLimits = { ...this.riskLimits, ...data.riskLimits };
        }

        if (data.positions) {
            data.positions.forEach(position => {
                this.positions.set(position.id, position);
            });
        }

        if (data.riskHistory) {
            this.riskHistory = data.riskHistory;
        }

        if (data.anomalyDetectorData) {
            this.anomalyDetector.importData(data.anomalyDetectorData);
        }

        console.log('📥 Dados do Risk Manager importados');
    }
}

// Exportar instâncias singleton
const anomalyDetector = new AnomalyDetector();
const autonomousRiskManager = new AutonomousRiskManager();

export {
    AnomalyDetector,
    AutonomousRiskManager,
    AnomalyType,
    anomalyDetector,
    autonomousRiskManager as default
};