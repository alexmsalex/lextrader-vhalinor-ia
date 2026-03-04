// advanced_temporal_network.js - Rede Temporal Avançada para Mercados Financeiros
// Versão expandida com arquitetura híbrida de memória e mecanismos de atenção temporal
import * as tf from 'https://esm.sh/@tensorflow/tfjs@^4.22.0';
import { TSMixerLayer } from './temporal_mixer.js'; // Importação da camada TSMixer

export const MarketRegime = {
    TRENDING_UP: 'TRENDING_UP',
    TRENDING_DOWN: 'TRENDING_DOWN',
    SIDEWAYS: 'SIDEWAYS',
    HIGH_VOLATILITY: 'HIGH_VOLATILITY',
    LOW_VOLATILITY: 'LOW_VOLATILITY',
    BREAKOUT: 'BREAKOUT',
    REVERSAL: 'REVERSAL',
    ACCUMULATION: 'ACCUMULATION',
    DISTRIBUTION: 'DISTRIBUTION'
};

export const TimeHorizon = {
    INTRADAY: 'INTRADAY',      // 1-60 minutos
    SHORT_TERM: 'SHORT_TERM',  // 1-5 dias
    MEDIUM_TERM: 'MEDIUM_TERM', // 1-4 semanas
    LONG_TERM: 'LONG_TERM'     // 1-3 meses
};

export class TemporalMemoryCell extends tf.layers.Layer {
    constructor(config) {
        super(config);
        this.hiddenSize = config.hiddenSize;
        this.memorySize = config.memorySize;
        this.returnSequences = config.returnSequences || false;

        // Gates para controle de memória
        this.inputGate = tf.layers.dense({
            units: this.hiddenSize,
            activation: 'sigmoid',
            kernelInitializer: 'glorotNormal'
        });

        this.forgetGate = tf.layers.dense({
            units: this.memorySize,
            activation: 'sigmoid',
            kernelInitializer: 'glorotNormal'
        });

        this.outputGate = tf.layers.dense({
            units: this.hiddenSize,
            activation: 'sigmoid',
            kernelInitializer: 'glorotNormal'
        });

        this.memoryUpdate = tf.layers.dense({
            units: this.memorySize,
            activation: 'tanh',
            kernelInitializer: 'glorotNormal'
        });

        this.hiddenUpdate = tf.layers.dense({
            units: this.hiddenSize,
            activation: 'tanh',
            kernelInitializer: 'glorotNormal'
        });
    }

    call(inputs, kwargs) {
        const [x, states] = inputs;
        const [hPrev, mPrev] = states || [null, null];

        // Processamento de gates
        const inputGate = this.inputGate.apply([x, hPrev].filter(Boolean));
        const forgetGate = this.forgetGate.apply([x, hPrev].filter(Boolean));
        const outputGate = this.outputGate.apply([x, hPrev].filter(Boolean));

        // Atualização de memória
        const memoryUpdate = this.memoryUpdate.apply([x, hPrev].filter(Boolean));
        const mNew = mPrev ?
            tf.add(tf.mul(forgetGate, mPrev), tf.mul(inputGate, memoryUpdate)) :
            memoryUpdate;

        // Atualização do estado oculto
        const hiddenUpdate = this.hiddenUpdate.apply([x, mNew]);
        const hNew = tf.mul(outputGate, tf.tanh(mNew));

        return [hNew, mNew];
    }

    static get className() {
        return 'TemporalMemoryCell';
    }
}

export class MultiHorizonAttention {
    constructor(config) {
        this.horizons = config.horizons || [1, 5, 20, 60];
        this.attentionHeads = config.attentionHeads || 4;
        this.dropoutRate = config.dropoutRate || 0.1;

        this.attentionLayers = this.horizons.map(horizon =>
            tf.layers.multiHeadAttention({
                headSize: config.hiddenSize / this.attentionHeads,
                numHeads: this.attentionHeads,
                dropout: this.dropoutRate
            })
        );
    }

    apply(inputs) {
        const horizonOutputs = this.horizons.map((horizon, idx) => {
            // Aplicar atenção específica para cada horizonte temporal
            const attentionLayer = this.attentionLayers[idx];
            return attentionLayer.apply([inputs, inputs]);
        });

        // Combinar saídas ponderadas por horizonte
        const weights = tf.softmax(tf.ones([this.horizons.length, 1]));
        const combined = tf.addN(
            horizonOutputs.map((output, idx) =>
                tf.mul(output, weights.slice([idx, 0], [1, 1]))
            )
        );

        return combined;
    }
}

export class AdvancedTemporalNetwork {
    constructor(config = {}) {
        this.config = {
            sequenceLength: config.sequenceLength || 60,
            hiddenSize: config.hiddenSize || 128,
            memorySize: config.memorySize || 256,
            numFeatures: config.numFeatures || 20,
            dropoutRate: config.dropoutRate || 0.2,
            learningRate: config.learningRate || 0.001,
            useAttention: config.useAttention !== false,
            useTSMixer: config.useTSMixer !== false,
            ...config
        };

        this.model = null;
        this.memoryBank = [];
        this.maxMemorySize = 1000;
        this.regimeClassifier = this.buildRegimeClassifier();

        console.log('✅ Advanced Temporal Network initialized with config:', this.config);
    }

    buildModel() {
        const input = tf.input({
            shape: [this.config.sequenceLength, this.config.numFeatures]
        });

        // Normalização por instância temporal
        let x = tf.layers.layerNormalization().apply(input);

        // Camada TSMixer (se habilitada)
        if (this.config.useTSMixer) {
            x = new TSMixerLayer({
                kernelSize: 3,
                dropoutRate: this.config.dropoutRate
            }).apply(x);
        }

        // Camada de memória temporal
        const memoryCell = new TemporalMemoryCell({
            hiddenSize: this.config.hiddenSize,
            memorySize: this.config.memorySize
        });

        const rnnLayer = tf.layers.rnn({
            cell: memoryCell,
            returnSequences: true,
            dropout: this.config.dropoutRate
        });

        x = rnnLayer.apply(x);

        // Mecanismo de atenção multi-horizonte
        if (this.config.useAttention) {
            const attention = new MultiHorizonAttention({
                horizons: [5, 20, 60],
                hiddenSize: this.config.hiddenSize,
                attentionHeads: 4
            });
            x = attention.apply(x);
        }

        // Camadas específicas por horizonte temporal
        const horizonOutputs = {};

        [TimeHorizon.INTRADAY, TimeHorizon.SHORT_TERM, TimeHorizon.MEDIUM_TERM].forEach(horizon => {
            let horizonPath = x;

            // Processamento específico para cada horizonte
            horizonPath = tf.layers.dense({
                units: this.config.hiddenSize / 2,
                activation: 'relu'
            }).apply(horizonPath);

            horizonPath = tf.layers.dropout({
                rate: this.config.dropoutRate
            }).apply(horizonPath);

            // Saída para o horizonte
            const horizonOut = tf.layers.dense({
                units: 1,
                activation: 'linear',
                name: `output_${horizon}`
            }).apply(horizonPath);

            horizonOutputs[horizon] = horizonOut;
        });

        // Saída do regime de mercado
        const regimePath = tf.layers.globalAveragePooling1d().apply(x);
        const regimeOut = tf.layers.dense({
            units: Object.keys(MarketRegime).length,
            activation: 'softmax',
            name: 'regime_output'
        }).apply(regimePath);

        // Saída de confiança
        const confidencePath = tf.layers.globalMaxPooling1d().apply(x);
        const confidenceOut = tf.layers.dense({
            units: 1,
            activation: 'sigmoid',
            name: 'confidence_output'
        }).apply(confidencePath);

        this.model = tf.model({
            inputs: input,
            outputs: [horizonOutputs.INTRADAY, horizonOutputs.SHORT_TERM,
            horizonOutputs.MEDIUM_TERM, regimeOut, confidenceOut]
        });

        const optimizer = tf.train.adam(this.config.learningRate);
        this.model.compile({
            optimizer: optimizer,
            loss: {
                'output_INTRADAY': 'meanSquaredError',
                'output_SHORT_TERM': 'meanSquaredError',
                'output_MEDIUM_TERM': 'meanSquaredError',
                'regime_output': 'categoricalCrossentropy',
                'confidence_output': 'binaryCrossentropy'
            },
            lossWeights: [0.3, 0.3, 0.2, 0.1, 0.1],
            metrics: ['mae', 'accuracy']
        });

        console.log('✅ Model architecture built successfully');
        return this.model;
    }

    buildRegimeClassifier() {
        // Classificador base para regimes de mercado
        const model = tf.sequential();

        model.add(tf.layers.dense({
            units: 64,
            activation: 'relu',
            inputShape: [this.config.numFeatures]
        }));

        model.add(tf.layers.dropout({ rate: 0.3 }));

        model.add(tf.layers.dense({
            units: 32,
            activation: 'relu'
        }));

        model.add(tf.layers.dense({
            units: Object.keys(MarketRegime).length,
            activation: 'softmax'
        }));

        model.compile({
            optimizer: 'adam',
            loss: 'categoricalCrossentropy',
            metrics: ['accuracy']
        });

        return model;
    }

    async detectMarketRegime(data) {
        const features = this.extractRegimeFeatures(data);
        const prediction = this.regimeClassifier.predict(features);
        const regimeIdx = prediction.argMax(-1).dataSync()[0];
        const confidence = prediction.max().dataSync()[0];

        const regimes = Object.values(MarketRegime);
        return {
            regime: regimes[regimeIdx],
            confidence: confidence,
            probabilities: prediction.dataSync()
        };
    }

    extractRegimeFeatures(data) {
        // Extrai características para classificação de regime
        const returns = tf.tensor1d(data.close).diff();
        const volatility = returns.std();
        const trend = tf.tensor1d(data.close).sub(tf.mean(data.close)).abs().mean();
        const volumeRatio = tf.tensor1d(data.volume).mean().div(tf.max(data.volume));

        return tf.concat([
            returns.mean().reshape([1]),
            volatility.reshape([1]),
            trend.reshape([1]),
            volumeRatio.reshape([1]),
            tf.tensor1d([data.rsi || 50, data.macd || 0, data.atr || 0])
        ]);
    }

    async train(data, labels, epochs = 50, validationSplit = 0.2) {
        console.log('🚀 Starting model training...');

        if (!this.model) {
            this.buildModel();
        }

        const history = await this.model.fit(data, labels, {
            epochs: epochs,
            validationSplit: validationSplit,
            batchSize: 32,
            callbacks: {
                onEpochEnd: (epoch, logs) => {
                    console.log(`Epoch ${epoch + 1}: loss = ${logs.loss.toFixed(4)}, val_loss = ${logs.val_loss.toFixed(4)}`);
                }
            }
        });

        console.log('✅ Training completed');
        return history;
    }

    async process(inputData) {
        try {
            if (!this.model) {
                await this.buildModel();
            }

            // Pré-processamento dos dados
            const processedData = await this.preprocessData(inputData);

            // Detecção de regime de mercado
            const regimeAnalysis = await this.detectMarketRegime(inputData);

            // Predição do modelo principal
            const predictions = this.model.predict(processedData);

            // Processamento das saídas
            const horizonPredictions = {};
            const horizonNames = [TimeHorizon.INTRADAY, TimeHorizon.SHORT_TERM, TimeHorizon.MEDIUM_TERM];

            horizonNames.forEach((horizon, idx) => {
                const pred = predictions[idx].dataSync()[0];
                const confidence = predictions[4].dataSync()[0]; // Confiança geral

                horizonPredictions[horizon.toLowerCase()] = {
                    prediction: pred,
                    confidence: confidence * (1 - idx * 0.1), // Decaimento de confiança por horizonte
                    volatility_adjusted: this.adjustForVolatility(pred, regimeAnalysis)
                };
            });

            // Adicionar memória ao banco de memória
            this.updateMemoryBank({
                timestamp: new Date().toISOString(),
                input: inputData,
                predictions: horizonPredictions,
                regime: regimeAnalysis
            });

            // Análise de consistência temporal
            const temporalConsistency = this.analyzeTemporalConsistency(horizonPredictions);

            return {
                horizons: horizonPredictions,
                regime: regimeAnalysis.regime,
                regime_confidence: regimeAnalysis.confidence,
                regime_probabilities: regimeAnalysis.probabilities,
                confidence: predictions[4].dataSync()[0],
                temporal_consistency: temporalConsistency,
                market_context: this.analyzeMarketContext(inputData),
                memory_patterns: this.identifyMemoryPatterns(),
                recommendation: this.generateRecommendation(horizonPredictions, regimeAnalysis),
                risk_metrics: this.calculateRiskMetrics(inputData)
            };

        } catch (error) {
            console.error('❌ Error processing data:', error);
            return this.getFallbackPrediction(inputData);
        }
    }

    preprocessData(data) {
        // Normalização e preparação dos dados
        const features = [
            'open', 'high', 'low', 'close', 'volume',
            'returns', 'volatility', 'rsi', 'macd', 'bollinger_upper',
            'bollinger_lower', 'atr', 'obv', 'vwap', 'momentum',
            'volume_ratio', 'price_acceleration', 'trend_strength',
            'support_level', 'resistance_level'
        ];

        const sequence = [];
        for (let i = 0; i < this.config.sequenceLength; i++) {
            const timestep = features.map(feature => {
                return data[feature] ? data[feature][i] || 0 : 0;
            });
            sequence.push(timestep);
        }

        return tf.tensor3d([sequence]);
    }

    updateMemoryBank(entry) {
        this.memoryBank.push(entry);

        // Limitar tamanho do banco de memória
        if (this.memoryBank.length > this.maxMemorySize) {
            this.memoryBank.shift();
        }

        // Atualizar pesos baseado em padrões de memória
        if (this.memoryBank.length % 100 === 0) {
            this.adaptFromMemoryPatterns();
        }
    }

    identifyMemoryPatterns() {
        if (this.memoryBank.length < 10) return [];

        const recentPatterns = this.memoryBank.slice(-10);
        const patterns = [];

        // Identificar padrões recorrentes
        for (let i = 0; i < recentPatterns.length - 1; i++) {
            const current = recentPatterns[i];
            const next = recentPatterns[i + 1];

            if (current.regime.regime === next.regime.regime &&
                Math.abs(current.predictions.intraday.prediction -
                    next.predictions.intraday.prediction) < 0.02) {
                patterns.push({
                    pattern: 'stability',
                    regime: current.regime.regime,
                    strength: 0.8
                });
            }
        }

        return patterns;
    }

    analyzeTemporalConsistency(predictions) {
        const horizons = ['intraday', 'short_term', 'medium_term'];
        let consistencyScore = 0;

        for (let i = 0; i < horizons.length - 1; i++) {
            const current = predictions[horizons[i]];
            const next = predictions[horizons[i + 1]];

            // Verificar se as previsões seguem uma direção consistente
            if (Math.sign(current.prediction) === Math.sign(next.prediction)) {
                consistencyScore += 0.3;
            }
        }

        return {
            score: consistencyScore,
            level: consistencyScore > 0.6 ? 'high' :
                consistencyScore > 0.3 ? 'medium' : 'low',
            recommendation: consistencyScore > 0.6 ?
                'Strong directional consistency across time horizons' :
                'Mixed signals across time horizons'
        };
    }

    analyzeMarketContext(data) {
        const context = {
            volatility_regime: data.volatility > 0.02 ? 'high' : 'low',
            trend_strength: Math.abs(data.trend_strength || 0),
            volume_profile: data.volume > data.volume_ma ? 'above_average' : 'below_average',
            market_hours: this.isMarketHours(),
            news_sentiment: data.news_sentiment || 'neutral'
        };

        return context;
    }

    adjustForVolatility(prediction, regimeAnalysis) {
        // Ajustar previsão baseado na volatilidade
        if (regimeAnalysis.regime === MarketRegime.HIGH_VOLATILITY) {
            return prediction * 0.8; // Reduzir magnitude em alta volatilidade
        } else if (regimeAnalysis.regime === MarketRegime.LOW_VOLATILITY) {
            return prediction * 1.2; // Aumentar confiança em baixa volatilidade
        }
        return prediction;
    }

    calculateRiskMetrics(data) {
        const returns = tf.tensor1d(data.close).diff();
        const volatility = returns.std().dataSync()[0];
        const maxDrawdown = this.calculateMaxDrawdown(data.close);
        const sharpeRatio = returns.mean().dataSync()[0] / (volatility + 1e-6);

        return {
            volatility: volatility,
            max_drawdown: maxDrawdown,
            sharpe_ratio: sharpeRatio,
            var_95: this.calculateVaR(returns.dataSync(), 0.95),
            expected_shortfall: this.calculateExpectedShortfall(returns.dataSync(), 0.95)
        };
    }

    calculateMaxDrawdown(prices) {
        let peak = prices[0];
        let maxDrawdown = 0;

        for (let price of prices) {
            if (price > peak) peak = price;
            const drawdown = (peak - price) / peak;
            if (drawdown > maxDrawdown) maxDrawdown = drawdown;
        }

        return maxDrawdown;
    }

    calculateVaR(returns, confidence) {
        const sortedReturns = [...returns].sort((a, b) => a - b);
        const index = Math.floor(sortedReturns.length * (1 - confidence));
        return sortedReturns[index];
    }

    calculateExpectedShortfall(returns, confidence) {
        const varLevel = this.calculateVaR(returns, confidence);
        const tailReturns = returns.filter(r => r <= varLevel);
        return tailReturns.reduce((a, b) => a + b, 0) / tailReturns.length;
    }

    generateRecommendation(predictions, regime) {
        const intraday = predictions.intraday;
        const shortTerm = predictions.short_term;

        let action = 'HOLD';
        let confidence = (intraday.confidence + shortTerm.confidence) / 2;

        if (intraday.prediction > 0.03 && shortTerm.prediction > 0.02) {
            action = regime.regime === MarketRegime.TRENDING_UP ? 'STRONG_BUY' : 'BUY';
        } else if (intraday.prediction < -0.03 && shortTerm.prediction < -0.02) {
            action = regime.regime === MarketRegime.TRENDING_DOWN ? 'STRONG_SELL' : 'SELL';
        } else if (Math.abs(intraday.prediction) < 0.01 && regime.regime === MarketRegime.SIDEWAYS) {
            action = 'RANGE_TRADE';
        }

        return {
            action: action,
            confidence: confidence,
            timeframe: intraday.confidence > shortTerm.confidence ? 'INTRADAY' : 'SHORT_TERM',
            stop_loss: intraday.prediction * 0.8,
            take_profit: intraday.prediction * 1.5
        };
    }

    adaptFromMemoryPatterns() {
        // Adaptar pesos do modelo baseado em padrões da memória
        console.log('🔄 Adapting model weights from memory patterns');

        // Implementar lógica de adaptação incremental
        // (e.g., ajustar learning rate, fine-tune específico)
    }

    isMarketHours() {
        const now = new Date();
        const hours = now.getUTCHours();
        const day = now.getUTCDay();

        // Mercado Forex 24/5
        if (hours >= 0 && hours < 24 && day >= 1 && day <= 5) {
            return 'market_hours';
        }
        return 'after_hours';
    }

    getFallbackPrediction(data) {
        // Método de fallback baseado em média móvel simples
        const prices = data.close || [];
        const ma5 = prices.slice(-5).reduce((a, b) => a + b, 0) / 5;
        const ma20 = prices.slice(-20).reduce((a, b) => a + b, 0) / 20;
        const trend = ma5 > ma20 ? 0.02 : -0.02;

        return {
            horizons: {
                intraday: { prediction: trend, confidence: 0.65 },
                short_term: { prediction: trend * 1.5, confidence: 0.6 },
                medium_term: { prediction: trend * 2, confidence: 0.55 }
            },
            regime: ma5 > ma20 ? MarketRegime.TRENDING_UP : MarketRegime.TRENDING_DOWN,
            confidence: 0.7,
            fallback: true
        };
    }

    async saveModel(path = './models/temporal_network') {
        if (this.model) {
            await this.model.save(`localstorage://${path}`);
            console.log(`💾 Model saved to: ${path}`);
        }
    }

    async loadModel(path = './models/temporal_network') {
        try {
            this.model = await tf.loadLayersModel(`localstorage://${path}`);
            console.log(`📂 Model loaded from: ${path}`);
        } catch (error) {
            console.log('📝 No saved model found, building new model');
            this.buildModel();
        }
    }

    getModelSummary() {
        if (this.model) {
            this.model.summary();
        }
    }

    resetMemoryBank() {
        this.memoryBank = [];
        console.log('🔄 Memory bank reset');
    }

    getPerformanceMetrics() {
        return {
            memory_size: this.memoryBank.length,
            avg_confidence: this.calculateAverageConfidence(),
            regime_distribution: this.calculateRegimeDistribution(),
            prediction_accuracy: this.estimatePredictionAccuracy()
        };
    }

    calculateAverageConfidence() {
        if (this.memoryBank.length === 0) return 0;

        const total = this.memoryBank.reduce((sum, entry) =>
            sum + (entry.predictions?.intraday?.confidence || 0), 0);
        return total / this.memoryBank.length;
    }

    calculateRegimeDistribution() {
        const distribution = {};
        Object.values(MarketRegime).forEach(regime => {
            distribution[regime] = 0;
        });

        this.memoryBank.forEach(entry => {
            if (entry.regime?.regime) {
                distribution[entry.regime.regime] =
                    (distribution[entry.regime.regime] || 0) + 1;
            }
        });

        return distribution;
    }

    estimatePredictionAccuracy() {
        // Estimativa simples baseada em consistência temporal
        if (this.memoryBank.length < 2) return 0.5;

        let correct = 0;
        for (let i = 0; i < this.memoryBank.length - 1; i++) {
            const pred1 = this.memoryBank[i].predictions.intraday.prediction;
            const pred2 = this.memoryBank[i + 1].predictions.intraday.prediction;

            if (Math.sign(pred1) === Math.sign(pred2)) {
                correct++;
            }
        }

        return correct / (this.memoryBank.length - 1);
    }
}

// Exportar utilitários auxiliares
export const TemporalUtils = {
    calculateBollingerBands: (prices, period = 20, stdDev = 2) => {
        const sma = prices.slice(-period).reduce((a, b) => a + b, 0) / period;
        const variance = prices.slice(-period).reduce((sum, price) =>
            sum + Math.pow(price - sma, 2), 0) / period;
        const std = Math.sqrt(variance);

        return {
            upper: sma + (std * stdDev),
            middle: sma,
            lower: sma - (std * stdDev)
        };
    },

    calculateRSI: (prices, period = 14) => {
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
        const rs = avgGain / (avgLoss || 1e-6);

        return 100 - (100 / (1 + rs));
    },

    createSequences: (data, sequenceLength) => {
        const sequences = [];
        const labels = [];

        for (let i = sequenceLength; i < data.length; i++) {
            sequences.push(data.slice(i - sequenceLength, i));
            labels.push(data[i]); // Próximo valor
        }

        return { sequences, labels };
    },

    normalizeBatch: (tensor, axis = 0) => {
        const mean = tensor.mean(axis);
        const std = tensor.std(axis);
        return tensor.sub(mean).div(std.add(1e-6));
    }
};

// Exportação padrão
export default AdvancedTemporalNetwork;
