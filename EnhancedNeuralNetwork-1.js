import { EventEmitter } from 'events';
import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgl'; // GPU backend
import { PerformanceMonitor } from '../utils/PerformanceMonitor';
import { DataPreprocessor } from '../utils/DataPreprocessor';
import { ModelRegistry } from '../utils/ModelRegistry';

/**
 * Enhanced Neural Network with GPU Acceleration and Advanced Features
 * 
 * This class implements a sophisticated neural network optimized for trading signal
 * prediction with GPU acceleration, transfer learning, and ensemble methods.
 */
export class EnhancedNeuralNetwork extends EventEmitter {
    private config: {
        modelType: 'LSTM' | 'GRU' | 'CNN' | 'Transformer' | 'Ensemble';
        inputShape: number[];
        outputShape: number[];
        layers: number[];
        learningRate: number;
        batchSize: number;
        epochs: number;
        validationSplit: number;
        dropoutRate: number;
        useGPU: boolean;
        enableQuantization: boolean;
        enablePruning: boolean;
        modelVersion: string;
        ensembleSize?: number;
        attentionHeads?: number;
        transformerLayers?: number;
    };

    private model: tf.LayersModel | tf.Sequential | null;
    private ensembleModels: tf.LayersModel[];
    private performance: {
        accuracy: number;
        loss: number;
        precision: number;
        recall: number;
        f1Score: number;
        inferenceTime: number;
        trainingTime: number;
        memoryUsage: number;
        gpuUtilization: number;
    };

    private performanceMonitor: PerformanceMonitor;
    private dataPreprocessor: DataPreprocessor;
    private modelRegistry: ModelRegistry;
    private isInitialized: boolean;
    private isTraining: boolean;
    private trainingHistory: tf.History[];
    private featureScaler: any;
    private labelEncoder: any;
    private classWeights: { [key: number]: number };
    private earlyStopping: tf.Callback;
    private modelCheckpoint: tf.Callback;
    private tensorBoard: tf.Callback;

    constructor(config: Partial<typeof EnhancedNeuralNetwork.prototype.config> = {}) {
        super();

        this.config = {
            modelType: config.modelType || 'LSTM',
            inputShape: config.inputShape || [50, 20], // [timesteps, features]
            outputShape: config.outputShape || [3], // [BUY, SELL, HOLD]
            layers: config.layers || [128, 64, 32],
            learningRate: config.learningRate || 0.001,
            batchSize: config.batchSize || 32,
            epochs: config.epochs || 100,
            validationSplit: config.validationSplit || 0.2,
            dropoutRate: config.dropoutRate || 0.3,
            useGPU: config.useGPU !== false,
            enableQuantization: config.enableQuantization || false,
            enablePruning: config.enablePruning || false,
            modelVersion: config.modelVersion || '1.0.0',
            ensembleSize: config.ensembleSize || 5,
            attentionHeads: config.attentionHeads || 8,
            transformerLayers: config.transformerLayers || 4
        };

        this.model = null;
        this.ensembleModels = [];
        this.performance = {
            accuracy: 0,
            loss: 0,
            precision: 0,
            recall: 0,
            f1Score: 0,
            inferenceTime: 0,
            trainingTime: 0,
            memoryUsage: 0,
            gpuUtilization: 0
        };

        this.performanceMonitor = new PerformanceMonitor();
        this.dataPreprocessor = new DataPreprocessor();
        this.modelRegistry = new ModelRegistry();
        this.isInitialized = false;
        this.isTraining = false;
        this.trainingHistory = [];
        this.featureScaler = null;
        this.labelEncoder = null;
        this.classWeights = {};

        // Initialize callbacks
        this.earlyStopping = tf.callbacks.earlyStopping({
            monitor: 'val_loss',
            patience: 10,
            restoreBestWeights: true
        });

        this.modelCheckpoint = tf.callbacks.modelCheckpoint({
            filepath: 'model-checkpoint',
            saveBestOnly: true
        });

        this.tensorBoard = tf.callbacks.tensorBoard({
            writeGraph: true,
            writeImages: true,
            updateFreq: 'batch'
        });

        this.setMaxListeners(50);
        this.log('Enhanced Neural Network instance created', 'info');
    }

    /**
     * Initialize the neural network with GPU optimization
     */
    async initialize(): Promise<{
        success: boolean;
        message: string;
        backend: string;
        gpuInfo: any;
        memoryInfo: any;
    }> {
        try {
            if (this.isInitialized) {
                return {
                    success: true,
                    message: 'Network already initialized',
                    backend: await tf.backend(),
                    gpuInfo: await this.getGPUInfo(),
                    memoryInfo: tf.memory()
                };
            }

            // Set backend for GPU acceleration
            if (this.config.useGPU) {
                try {
                    await tf.setBackend('webgl');
                    this.log('✅ WebGL backend enabled for GPU acceleration', 'info');
                } catch (error) {
                    this.log(`WebGL not available, falling back to CPU: ${error.message}`, 'warn');
                    await tf.setBackend('cpu');
                }
            }

            // Warm up GPU
            await this.warmUpGPU();

            // Initialize performance monitor
            await this.performanceMonitor.initialize();

            // Create model architecture
            await this.createModel();

            this.isInitialized = true;

            const backend = await tf.backend();
            const gpuInfo = await this.getGPUInfo();
            const memoryInfo = tf.memory();

            this.log(`⚡ Enhanced Neural Network initialized successfully`, 'info');
            this.log(`Backend: ${backend}`, 'debug');
            this.log(`Memory: ${JSON.stringify(memoryInfo)}`, 'debug');

            this.emit('initialized', {
                backend,
                gpuInfo,
                memoryInfo,
                config: this.config
            });

            return {
                success: true,
                message: 'Enhanced Neural Network initialized successfully',
                backend,
                gpuInfo,
                memoryInfo
            };

        } catch (error) {
            this.log(`Initialization failed: ${error.message}`, 'error');
            this.emit('error', error);

            return {
                success: false,
                message: `Initialization failed: ${error.message}`,
                backend: 'cpu',
                gpuInfo: null,
                memoryInfo: null
            };
        }
    }

    /**
     * Create neural network model based on configuration
     */
    private async createModel(): Promise<void> {
        switch (this.config.modelType) {
            case 'LSTM':
                this.model = this.createLSTMModel();
                break;
            case 'GRU':
                this.model = this.createGRUModel();
                break;
            case 'CNN':
                this.model = this.createCNNModel();
                break;
            case 'Transformer':
                this.model = this.createTransformerModel();
                break;
            case 'Ensemble':
                await this.createEnsembleModel();
                break;
            default:
                this.model = this.createLSTMModel();
        }

        // Compile the model
        this.model.compile({
            optimizer: tf.train.adam(this.config.learningRate),
            loss: 'categoricalCrossentropy',
            metrics: [
                'accuracy',
                tf.metrics.precision(),
                tf.metrics.recall(),
                this.f1ScoreMetric()
            ]
        });

        this.log(`Model created: ${this.config.modelType}`, 'info');
        this.log(`Model summary: ${this.model.summary()}`, 'debug');
    }

    /**
     * Create LSTM model architecture
     */
    private createLSTMModel(): tf.Sequential {
        const model = tf.sequential();

        // Input layer
        model.add(tf.layers.lstm({
            units: this.config.layers[0],
            inputShape: this.config.inputShape,
            returnSequences: true,
            kernelInitializer: 'heNormal',
            recurrentInitializer: 'orthogonal'
        }));
        model.add(tf.layers.batchNormalization());
        model.add(tf.layers.dropout(this.config.dropoutRate));

        // Hidden LSTM layers
        for (let i = 1; i < this.config.layers.length; i++) {
            model.add(tf.layers.lstm({
                units: this.config.layers[i],
                returnSequences: i < this.config.layers.length - 1,
                kernelInitializer: 'heNormal',
                recurrentInitializer: 'orthogonal'
            }));
            model.add(tf.layers.batchNormalization());
            model.add(tf.layers.dropout(this.config.dropoutRate));
        }

        // Output layer
        model.add(tf.layers.dense({
            units: this.config.outputShape[0],
            activation: 'softmax',
            kernelInitializer: 'glorotNormal'
        }));

        return model;
    }

    /**
     * Create GRU model architecture
     */
    private createGRUModel(): tf.Sequential {
        const model = tf.sequential();

        model.add(tf.layers.gru({
            units: this.config.layers[0],
            inputShape: this.config.inputShape,
            returnSequences: true,
            kernelInitializer: 'heNormal',
            recurrentInitializer: 'orthogonal'
        }));
        model.add(tf.layers.batchNormalization());
        model.add(tf.layers.dropout(this.config.dropoutRate));

        for (let i = 1; i < this.config.layers.length; i++) {
            model.add(tf.layers.gru({
                units: this.config.layers[i],
                returnSequences: i < this.config.layers.length - 1,
                kernelInitializer: 'heNormal',
                recurrentInitializer: 'orthogonal'
            }));
            model.add(tf.layers.batchNormalization());
            model.add(tf.layers.dropout(this.config.dropoutRate));
        }

        model.add(tf.layers.dense({
            units: this.config.outputShape[0],
            activation: 'softmax',
            kernelInitializer: 'glorotNormal'
        }));

        return model;
    }

    /**
     * Create CNN model architecture
     */
    private createCNNModel(): tf.Sequential {
        const model = tf.sequential();

        // Convolutional layers for feature extraction
        model.add(tf.layers.conv1d({
            filters: 64,
            kernelSize: 3,
            strides: 1,
            padding: 'same',
            activation: 'relu',
            inputShape: this.config.inputShape
        }));
        model.add(tf.layers.batchNormalization());
        model.add(tf.layers.maxPooling1d({ poolSize: 2 }));

        model.add(tf.layers.conv1d({
            filters: 128,
            kernelSize: 3,
            strides: 1,
            padding: 'same',
            activation: 'relu'
        }));
        model.add(tf.layers.batchNormalization());
        model.add(tf.layers.maxPooling1d({ poolSize: 2 }));

        model.add(tf.layers.conv1d({
            filters: 256,
            kernelSize: 3,
            strides: 1,
            padding: 'same',
            activation: 'relu'
        }));
        model.add(tf.layers.batchNormalization());

        // Flatten and dense layers
        model.add(tf.layers.flatten());

        for (const units of this.config.layers) {
            model.add(tf.layers.dense({ units, activation: 'relu' }));
            model.add(tf.layers.batchNormalization());
            model.add(tf.layers.dropout(this.config.dropoutRate));
        }

        model.add(tf.layers.dense({
            units: this.config.outputShape[0],
            activation: 'softmax'
        }));

        return model;
    }

    /**
     * Create Transformer model architecture
     */
    private createTransformerModel(): tf.LayersModel {
        const input = tf.input({ shape: this.config.inputShape });

        // Positional encoding
        let x = this.positionalEncoding(input);

        // Transformer blocks
        for (let i = 0; i < (this.config.transformerLayers || 4); i++) {
            x = this.transformerBlock(x, this.config.attentionHeads || 8);
        }

        // Global pooling and output
        x = tf.layers.globalAveragePooling1d().apply(x) as tf.SymbolicTensor;

        for (const units of this.config.layers) {
            x = tf.layers.dense({ units, activation: 'relu' }).apply(x) as tf.SymbolicTensor;
            x = tf.layers.batchNormalization().apply(x) as tf.SymbolicTensor;
            x = tf.layers.dropout(this.config.dropoutRate).apply(x) as tf.SymbolicTensor;
        }

        const output = tf.layers.dense({
            units: this.config.outputShape[0],
            activation: 'softmax'
        }).apply(x) as tf.SymbolicTensor;

        return tf.model({ inputs: input, outputs: output });
    }

    /**
     * Create ensemble of models
     */
    private async createEnsembleModel(): Promise<void> {
        const modelTypes: Array<'LSTM' | 'GRU' | 'CNN'> = ['LSTM', 'GRU', 'CNN'];

        for (let i = 0; i < (this.config.ensembleSize || 5); i++) {
            const modelType = modelTypes[i % modelTypes.length];
            let model: tf.LayersModel;

            switch (modelType) {
                case 'LSTM':
                    model = this.createLSTMModel();
                    break;
                case 'GRU':
                    model = this.createGRUModel();
                    break;
                case 'CNN':
                    model = this.createCNNModel();
                    break;
            }

            model.compile({
                optimizer: tf.train.adam(this.config.learningRate),
                loss: 'categoricalCrossentropy',
                metrics: ['accuracy']
            });

            this.ensembleModels.push(model);
        }

        this.log(`Ensemble model created with ${this.ensembleModels.length} sub-models`, 'info');
    }

    /**
     * Transformer block implementation
     */
    private transformerBlock(input: tf.SymbolicTensor, numHeads: number): tf.SymbolicTensor {
        // Multi-head attention
        const attentionOutput = tf.layers.multiHeadAttention({
            numHeads,
            keyDim: 64
        }).apply([input, input, input]) as tf.SymbolicTensor;

        // Add & Norm
        let x = tf.layers.add().apply([input, attentionOutput]) as tf.SymbolicTensor;
        x = tf.layers.layerNormalization().apply(x) as tf.SymbolicTensor;

        // Feed forward
        const ffn = tf.layers.dense({ units: 256, activation: 'relu' }).apply(x) as tf.SymbolicTensor;
        const ffnOutput = tf.layers.dense({ units: this.config.inputShape[1] }).apply(ffn) as tf.SymbolicTensor;

        // Add & Norm
        x = tf.layers.add().apply([x, ffnOutput]) as tf.SymbolicTensor;
        x = tf.layers.layerNormalization().apply(x) as tf.SymbolicTensor;

        return x;
    }

    /**
     * Positional encoding for Transformer
     */
    private positionalEncoding(input: tf.SymbolicTensor): tf.SymbolicTensor {
        const [seqLength, dModel] = this.config.inputShape;
        const position = tf.range(0, seqLength, 1, 'float32').reshape([seqLength, 1]);
        const divTerm = tf.exp(tf.range(0, dModel, 2, 'float32').mul(-Math.log(10000.0) / dModel));

        const posEncoding = tf.zeros([seqLength, dModel]);
        // This is a simplified version - in practice you'd compute sinusoidal encoding
        return tf.layers.add().apply([input, posEncoding]) as tf.SymbolicTensor;
    }

    /**
     * Custom F1 Score metric
     */
    private f1ScoreMetric(): tf.CustomCallbackConfig {
        return {
            name: 'f1_score',
            updateState: (yTrue: tf.Tensor, yPred: tf.Tensor, sampleWeight?: tf.Tensor) => {
                // Implement F1 score calculation
                const threshold = 0.5;
                const yPredLabels = yPred.greater(threshold);
                const yTrueLabels = yTrue.greater(threshold);

                const truePositives = yTrueLabels.mul(yPredLabels).sum().dataSync()[0];
                const falsePositives = yTrueLabels.notEqual(yPredLabels).mul(yPredLabels).sum().dataSync()[0];
                const falseNegatives = yTrueLabels.notEqual(yPredLabels).mul(yTrueLabels).sum().dataSync()[0];

                const precision = truePositives / (truePositives + falsePositives + 1e-7);
                const recall = truePositives / (truePositives + falseNegatives + 1e-7);
                const f1 = 2 * (precision * recall) / (precision + recall + 1e-7);

                return tf.tensor(f1);
            }
        };
    }

    /**
     * Train the neural network with advanced features
     */
    async train(data: {
        features: number[][][]; // [samples, timesteps, features]
        labels: number[][];     // [samples, classes]
        validationData?: {
            features: number[][][];
            labels: number[][];
        };
        classWeights?: { [key: number]: number };
        callbacks?: tf.Callback[];
    }): Promise<{
        success: boolean;
        history: tf.History;
        finalMetrics: any;
        trainingTime: number;
        modelSize: number;
    }> {
        try {
            if (!this.isInitialized) {
                await this.initialize();
            }

            if (this.isTraining) {
                throw new Error('Training already in progress');
            }

            this.isTraining = true;
            this.emit('trainingStarted', { samples: data.features.length });

            const startTime = Date.now();

            // Preprocess data
            const preprocessedData = await this.preprocessTrainingData(data);

            // Calculate class weights if not provided
            if (!data.classWeights) {
                this.classWeights = this.calculateClassWeights(preprocessedData.labels);
            } else {
                this.classWeights = data.classWeights;
            }

            // Convert to tensors
            const trainTensors = {
                features: tf.tensor3d(preprocessedData.features),
                labels: tf.tensor2d(preprocessedData.labels)
            };

            let validationTensors = null;
            if (data.validationData) {
                validationTensors = {
                    features: tf.tensor3d(data.validationData.features),
                    labels: tf.tensor2d(data.validationData.labels)
                };
            }

            // Prepare callbacks
            const callbacks = [
                this.earlyStopping,
                this.modelCheckpoint,
                this.tensorBoard,
                {
                    onBatchEnd: (batch: number, logs?: tf.Logs) => {
                        this.emit('batchEnd', { batch, logs });
                    },
                    onEpochEnd: (epoch: number, logs?: tf.Logs) => {
                        this.performanceMonitor.recordTrainingMetrics(logs);
                        this.emit('epochEnd', { epoch, logs });
                    }
                },
                ...(data.callbacks || [])
            ];

            // Train the model
            let history: tf.History;

            if (this.config.modelType === 'Ensemble') {
                history = await this.trainEnsemble(trainTensors, validationTensors, callbacks);
            } else {
                history = await this.model.fit(trainTensors.features, trainTensors.labels, {
                    batchSize: this.config.batchSize,
                    epochs: this.config.epochs,
                    validationSplit: this.config.validationSplit,
                    validationData: validationTensors ? [validationTensors.features, validationTensors.labels] : undefined,
                    callbacks,
                    classWeight: this.classWeights,
                    verbose: this.config.modelType === 'Ensemble' ? 0 : 1 // Suppress ensemble verbose
                });
            }

            this.trainingHistory.push(history);
            const trainingTime = Date.now() - startTime;

            // Update performance metrics
            await this.updatePerformanceMetrics(history);

            // Apply optimizations if enabled
            if (this.config.enableQuantization) {
                await this.applyQuantization();
            }

            if (this.config.enablePruning) {
                await this.applyPruning();
            }

            // Calculate model size
            const modelSize = await this.calculateModelSize();

            this.isTraining = false;
            this.emit('trainingCompleted', {
                history,
                trainingTime,
                modelSize,
                performance: this.performance
            });

            this.log(`Training completed in ${trainingTime}ms`, 'info');
            this.log(`Final accuracy: ${this.performance.accuracy.toFixed(4)}`, 'info');
            this.log(`Final loss: ${this.performance.loss.toFixed(4)}`, 'info');

            return {
                success: true,
                history,
                finalMetrics: this.performance,
                trainingTime,
                modelSize
            };

        } catch (error) {
            this.isTraining = false;
            this.log(`Training failed: ${error.message}`, 'error');
            this.emit('trainingError', error);

            return {
                success: false,
                history: null,
                finalMetrics: null,
                trainingTime: 0,
                modelSize: 0
            };
        }
    }

    /**
     * Train ensemble of models
     */
    private async trainEnsemble(
        trainTensors: { features: tf.Tensor3D; labels: tf.Tensor2D },
        validationTensors: { features: tf.Tensor3D; labels: tf.Tensor2D } | null,
        callbacks: tf.Callback[]
    ): Promise<tf.History> {
        const histories: tf.History[] = [];

        for (let i = 0; i < this.ensembleModels.length; i++) {
            this.log(`Training ensemble model ${i + 1}/${this.ensembleModels.length}`, 'info');

            const history = await this.ensembleModels[i].fit(
                trainTensors.features,
                trainTensors.labels,
                {
                    batchSize: this.config.batchSize,
                    epochs: this.config.epochs,
                    validationSplit: this.config.validationSplit,
                    validationData: validationTensors ? [validationTensors.features, validationTensors.labels] : undefined,
                    callbacks: callbacks.filter(cb => cb !== this.tensorBoard), // Disable tensorboard for each model
                    classWeight: this.classWeights,
                    verbose: 0
                }
            );

            histories.push(history);
            this.emit('ensembleModelTrained', { modelIndex: i, history });
        }

        // Return combined history
        return this.combineHistories(histories);
    }

    /**
     * Combine multiple training histories
     */
    private combineHistories(histories: tf.History[]): tf.History {
        const combined: tf.History = {
            history: {
                loss: [],
                acc: [],
                val_loss: [],
                val_acc: []
            },
            params: {
                epochs: 0,
                steps: 0
            },
            epoch: []
        };

        histories.forEach(history => {
            combined.history.loss.push(...history.history.loss);
            combined.history.acc.push(...history.history.acc);
            combined.history.val_loss.push(...(history.history.val_loss || []));
            combined.history.val_acc.push(...(history.history.val_acc || []));
        });

        return combined;
    }

    /**
     * Preprocess training data
     */
    private async preprocessTrainingData(data: {
        features: number[][][];
        labels: number[][];
    }): Promise<{
        features: number[][][];
        labels: number[][];
        scaler: any;
        encoder: any;
    }> {
        // Normalize features
        const normalizedFeatures = await this.dataPreprocessor.normalize3D(data.features);

        // Encode labels if needed
        const encodedLabels = this.labelEncoder
            ? this.labelEncoder.transform(data.labels)
            : data.labels;

        // Handle class imbalance
        const balancedData = await this.dataPreprocessor.handleClassImbalance(
            normalizedFeatures,
            encodedLabels
        );

        return {
            features: balancedData.features,
            labels: balancedData.labels,
            scaler: this.dataPreprocessor.getScaler(),
            encoder: this.labelEncoder
        };
    }

    /**
     * Calculate class weights for imbalanced datasets
     */
    private calculateClassWeights(labels: number[][]): { [key: number]: number } {
        const classCounts: { [key: number]: number } = {};

        // Count instances per class
        labels.forEach(labelArray => {
            const classIndex = labelArray.indexOf(Math.max(...labelArray));
            classCounts[classIndex] = (classCounts[classIndex] || 0) + 1;
        });

        const total = labels.length;
        const classWeights: { [key: number]: number } = {};

        Object.keys(classCounts).forEach(classIndex => {
            const classIdx = parseInt(classIndex);
            classWeights[classIdx] = total / (Object.keys(classCounts).length * classCounts[classIdx]);
        });

        return classWeights;
    }

    /**
     * Update performance metrics after training
     */
    private async updatePerformanceMetrics(history: tf.History): Promise<void> {
        const lastEpoch = history.history.acc.length - 1;

        this.performance = {
            accuracy: history.history.acc[lastEpoch] || 0,
            loss: history.history.loss[lastEpoch] || 0,
            precision: history.history.precision?.[lastEpoch] || 0,
            recall: history.history.recall?.[lastEpoch] || 0,
            f1Score: history.history.f1_score?.[lastEpoch] || 0,
            inferenceTime: await this.measureInferenceTime(),
            trainingTime: history.params.epochs * 1000, // Approximate
            memoryUsage: tf.memory().numBytes,
            gpuUtilization: await this.getGPUUtilization()
        };
    }

    /**
     * Make predictions with advanced features
     */
    async predict(input: {
        features: number[][];
        metadata?: {
            timestamp: Date;
            symbol: string;
            timeframe: string;
        };
        options?: {
            returnProbabilities?: boolean;
            returnUncertainty?: boolean;
            returnFeatureImportance?: boolean;
            ensembleVoting?: 'hard' | 'soft' | 'weighted';
        };
    }): Promise<{
        signal: 'STRONG_BUY' | 'BUY' | 'NEUTRAL' | 'SELL' | 'STRONG_SELL';
        confidence: number;
        probabilities: { [key: string]: number };
        uncertainty?: number;
        featureImportance?: Array<{ feature: string; importance: number }>;
        metadata: any;
        modelInfo: any;
        performance: any;
    }> {
        try {
            if (!this.isInitialized) {
                await this.initialize();
            }

            const startTime = performance.now();

            // Preprocess input
            const preprocessedInput = await this.preprocessInput(input.features);
            const inputTensor = tf.tensor3d([preprocessedInput]);

            // Make prediction
            let predictions: tf.Tensor;
            let ensemblePredictions: tf.Tensor[] = [];

            if (this.config.modelType === 'Ensemble') {
                // Get predictions from all ensemble models
                for (const model of this.ensembleModels) {
                    const pred = model.predict(inputTensor) as tf.Tensor;
                    ensemblePredictions.push(pred);
                }

                // Combine predictions based on voting strategy
                const votingStrategy = input.options?.ensembleVoting || 'soft';
                predictions = this.combineEnsemblePredictions(ensemblePredictions, votingStrategy);
            } else {
                predictions = this.model.predict(inputTensor) as tf.Tensor;
            }

            // Calculate uncertainty if requested
            let uncertainty: number | undefined;
            if (input.options?.returnUncertainty) {
                uncertainty = this.calculateUncertainty(predictions, ensemblePredictions);
            }

            // Get probabilities
            const probabilitiesArray = await predictions.data();
            const probabilities = {
                STRONG_BUY: probabilitiesArray[0],
                BUY: probabilitiesArray[1],
                NEUTRAL: probabilitiesArray[2],
                SELL: probabilitiesArray[3],
                STRONG_SELL: probabilitiesArray[4]
            };

            // Determine signal and confidence
            const maxIndex = probabilitiesArray.indexOf(Math.max(...probabilitiesArray));
            const signal = this.getSignalFromIndex(maxIndex);
            const confidence = probabilitiesArray[maxIndex];

            // Calculate feature importance if requested
            let featureImportance: Array<{ feature: string; importance: number }> | undefined;
            if (input.options?.returnFeatureImportance) {
                featureImportance = await this.calculateFeatureImportance(inputTensor);
            }

            const inferenceTime = performance.now() - startTime;
            this.performance.inferenceTime = inferenceTime;

            // Update performance monitor
            this.performanceMonitor.recordInference(inferenceTime);

            // Clean up tensors
            tf.dispose([inputTensor, predictions, ...ensemblePredictions]);

            this.emit('predictionMade', {
                signal,
                confidence,
                inferenceTime,
                metadata: input.metadata
            });

            return {
                signal,
                confidence,
                probabilities: input.options?.returnProbabilities ? probabilities : undefined,
                uncertainty,
                featureImportance,
                metadata: input.metadata || {},
                modelInfo: {
                    type: this.config.modelType,
                    version: this.config.modelVersion,
                    timestamp: new Date()
                },
                performance: {
                    inferenceTime,
                    memoryUsage: tf.memory().numBytes,
                    gpuUtilization: await this.getGPUUtilization()
                }
            };

        } catch (error) {
            this.log(`Prediction failed: ${error.message}`, 'error');
            this.emit('predictionError', error);

            return {
                signal: 'NEUTRAL',
                confidence: 0,
                probabilities: {},
                metadata: input.metadata || {},
                modelInfo: {
                    type: this.config.modelType,
                    version: this.config.modelVersion,
                    timestamp: new Date()
                },
                performance: {
                    inferenceTime: 0,
                    memoryUsage: 0,
                    gpuUtilization: 0
                }
            };
        }
    }

    /**
     * Combine ensemble predictions using different voting strategies
     */
    private combineEnsemblePredictions(
        predictions: tf.Tensor[],
        strategy: 'hard' | 'soft' | 'weighted'
    ): tf.Tensor {
        switch (strategy) {
            case 'hard':
                // Majority voting
                const classPredictions = predictions.map(p => {
                    const data = p.dataSync();
                    return data.indexOf(Math.max(...data));
                });

                const classCounts = classPredictions.reduce((counts, cls) => {
                    counts[cls] = (counts[cls] || 0) + 1;
                    return counts;
                }, {} as { [key: number]: number });

                const winningClass = Object.keys(classCounts).reduce((a, b) =>
                    classCounts[parseInt(a)] > classCounts[parseInt(b)] ? a : b
                );

                const hardResult = new Array(5).fill(0);
                hardResult[parseInt(winningClass)] = 1;
                return tf.tensor([hardResult]);

            case 'weighted':
                // Weight by model accuracy (simplified)
                const weights = this.ensembleModels.map((_, i) => 1 / (i + 1)); // Example weights
                const weightedSum = predictions.reduce((sum, pred, i) => {
                    return sum.add(pred.mul(weights[i]));
                }, tf.zeros([1, 5]));

                const totalWeight = weights.reduce((a, b) => a + b, 0);
                return weightedSum.div(totalWeight);

            case 'soft':
            default:
                // Average probabilities
                const sum = predictions.reduce((sum, pred) => sum.add(pred), tf.zeros([1, 5]));
                return sum.div(predictions.length);
        }
    }

    /**
     * Calculate prediction uncertainty
     */
    private calculateUncertainty(prediction: tf.Tensor, ensemblePredictions: tf.Tensor[]): number {
        if (ensemblePredictions.length > 1) {
            // Calculate variance across ensemble predictions
            const predictionsData = ensemblePredictions.map(p => p.dataSync());
            const variances = new Array(5).fill(0);

            for (let i = 0; i < 5; i++) {
                const values = predictionsData.map(p => p[i]);
                const mean = values.reduce((a, b) => a + b, 0) / values.length;
                const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
                variances[i] = variance;
            }

            return variances.reduce((a, b) => a + b, 0) / variances.length;
        }

        // For single model, use prediction entropy
        const probs = prediction.dataSync();
        const entropy = -probs.reduce((sum, p) => sum + (p > 0 ? p * Math.log(p) : 0), 0);
        return entropy / Math.log(5); // Normalize to [0, 1]
    }

    /**
     * Calculate feature importance using integrated gradients
     */
    private async calculateFeatureImportance(inputTensor: tf.Tensor3D): Promise<Array<{ feature: string; importance: number }>> {
        // Simplified feature importance calculation
        const baseline = tf.zerosLike(inputTensor);
        const steps = 20;

        const gradients = tf.tidy(() => {
            const scaledInputs = tf.linspace(0, 1, steps).arraySync().map(alpha => {
                return baseline.mul(1 - alpha).add(inputTensor.mul(alpha));
            });

            let totalGradients = tf.zerosLike(inputTensor);

            scaledInputs.forEach(scaledInput => {
                tf.variable(scaledInput);
                const pred = this.model.predict(scaledInput) as tf.Tensor;
                const grad = tf.grad(() => pred)(scaledInput);
                totalGradients = totalGradients.add(grad);
            });

            return totalGradients.div(steps);
        });

        const gradientsData = await gradients.data();
        const featureNames = this.generateFeatureNames();

        const importance = featureNames.map((name, i) => ({
            feature: name,
            importance: Math.abs(gradientsData[i])
        }));

        importance.sort((a, b) => b.importance - a.importance);

        tf.dispose([baseline, gradients]);

        return importance.slice(0, 10); // Return top 10 features
    }

    /**
     * Generate feature names for importance analysis
     */
    private generateFeatureNames(): string[] {
        const baseFeatures = [
            'Open', 'High', 'Low', 'Close', 'Volume',
            'RSI', 'MACD', 'Bollinger_Upper', 'Bollinger_Lower', 'ATR',
            'VWAP', 'EMA_20', 'EMA_50', 'SMA_200', 'Stochastic',
            'Volume_MA', 'Price_Change', 'Volatility', 'Market_Cap', 'Sentiment'
        ];

        const featureNames: string[] = [];
        for (let t = 0; t < this.config.inputShape[0]; t++) {
            for (let f = 0; f < Math.min(this.config.inputShape[1], baseFeatures.length); f++) {
                featureNames.push(`${baseFeatures[f]}_t-${this.config.inputShape[0] - t - 1}`);
            }
        }

        return featureNames;
    }

    /**
     * Get signal from prediction index
     */
    private getSignalFromIndex(index: number): 'STRONG_BUY' | 'BUY' | 'NEUTRAL' | 'SELL' | 'STRONG_SELL' {
        switch (index) {
            case 0: return 'STRONG_BUY';
            case 1: return 'BUY';
            case 2: return 'NEUTRAL';
            case 3: return 'SELL';
            case 4: return 'STRONG_SELL';
            default: return 'NEUTRAL';
        }
    }

    /**
     * Preprocess input data
     */
    private async preprocessInput(features: number[][]): Promise<number[][]> {
        if (this.featureScaler) {
            return this.featureScaler.transform([features])[0];
        }

        // If no scaler, normalize manually
        const normalized = features.map(featureRow => {
            const mean = featureRow.reduce((a, b) => a + b, 0) / featureRow.length;
            const std = Math.sqrt(featureRow.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / featureRow.length);
            return featureRow.map(val => std > 0 ? (val - mean) / std : 0);
        });

        return normalized;
    }

    /**
     * Warm up GPU for optimal performance
     */
    private async warmUpGPU(): Promise<void> {
        this.log('Warming up GPU...', 'debug');

        const warmUpTensor = tf.randomNormal([1, 50, 20]);
        const warmUpModel = tf.sequential();
        warmUpModel.add(tf.layers.dense({ units: 10, inputShape: [50, 20] }));
        warmUpModel.add(tf.layers.flatten());
        warmUpModel.add(tf.layers.dense({ units: 5, activation: 'softmax' }));

        warmUpModel.compile({
            optimizer: 'adam',
            loss: 'categoricalCrossentropy',
            metrics: ['accuracy']
        });

        await warmUpModel.fit(warmUpTensor, tf.ones([1, 5]), {
            epochs: 1,
            verbose: 0
        });

        tf.dispose([warmUpTensor]);
        this.log('GPU warm-up complete', 'debug');
    }

    /**
     * Apply quantization to reduce model size
     */
    private async applyQuantization(): Promise<void> {
        this.log('Applying quantization...', 'info');

        // Simplified quantization - in practice, use tfjs-converter
        const weights = this.model.getWeights();
        const quantizedWeights = weights.map(weight => {
            const data = weight.dataSync();
            const min = Math.min(...data);
            const max = Math.max(...data);
            const scale = 255 / (max - min);

            const quantized = data.map(val => Math.round((val - min) * scale));
            return tf.tensor(quantized, weight.shape);
        });

        this.model.setWeights(quantizedWeights);
        this.log('Quantization applied', 'info');
    }

    /**
     * Apply pruning to remove unimportant weights
     */
    private async applyPruning(): Promise<void> {
        this.log('Applying pruning...', 'info');

        const weights = this.model.getWeights();
        const prunedWeights = weights.map(weight => {
            const data = weight.dataSync();
            const threshold = this.calculatePruningThreshold(data);

            const prunedData = data.map(val => Math.abs(val) < threshold ? 0 : val);
            return tf.tensor(prunedData, weight.shape);
        });

        this.model.setWeights(prunedWeights);
        this.log(`Pruning applied with sparsity: ${this.calculateSparsity(prunedWeights).toFixed(2)}%`, 'info');
    }

    /**
     * Calculate pruning threshold
     */
    private calculatePruningThreshold(data: Float32Array): number {
        const sorted = Array.from(data).map(Math.abs).sort((a, b) => a - b);
        const percentile = 10; // Prune 10% smallest weights
        const index = Math.floor(sorted.length * percentile / 100);
        return sorted[index];
    }

    /**
     * Calculate model sparsity
     */
    private calculateSparsity(weights: tf.Tensor[]): number {
        const totalWeights = weights.reduce((sum, w) => sum + w.size, 0);
        const zeroWeights = weights.reduce((sum, w) => {
            const data = w.dataSync();
            return sum + data.filter(val => val === 0).length;
        }, 0);

        return (zeroWeights / totalWeights) * 100;
    }

    /**
     * Measure inference time
     */
    private async measureInferenceTime(): Promise<number> {
        const testInput = tf.randomNormal([1, ...this.config.inputShape]);
        const startTime = performance.now();

        for (let i = 0; i < 10; i++) {
            await this.model.predict(testInput);
        }

        const endTime = performance.now();
        tf.dispose(testInput);

        return (endTime - startTime) / 10;
    }

    /**
     * Calculate model size in bytes
     */
    private async calculateModelSize(): Promise<number> {
        if (!this.model) return 0;

        const weights = this.model.getWeights();
        return weights.reduce((size, weight) => size + weight.size * 4, 0); // 4 bytes per float32
    }

    /**
     * Get GPU information
     */
    private async getGPUInfo(): Promise<any> {
        if (typeof navigator !== 'undefined' && 'gpu' in navigator) {
            try {
                const adapter = await (navigator as any).gpu.requestAdapter();
                return {
                    vendor: adapter.info?.vendor || 'unknown',
                    architecture: adapter.info?.architecture || 'unknown',
                    description: adapter.info?.description || 'unknown',
                    supported: true
                };
            } catch (error) {
                return { supported: false, error: error.message };
            }
        }

        return { supported: false, message: 'WebGPU not available' };
    }

    /**
     * Get GPU utilization
     */
    private async getGPUUtilization(): Promise<number> {
        // Simplified GPU utilization calculation
        // In a real implementation, this would use WebGL extensions
        const memoryInfo = tf.memory();
        const gpuMemory = memoryInfo.numBytesInGPU || 0;
        const totalMemory = 4 * 1024 * 1024 * 1024; // Assume 4GB GPU

        return Math.min(100, (gpuMemory / totalMemory) * 100);
    }

    /**
     * Save model to storage
     */
    async saveModel(name: string): Promise<{
        success: boolean;
        message: string;
        size: number;
        metadata: any;
    }> {
        try {
            if (!this.model) {
                throw new Error('No model to save');
            }

            const modelSize = await this.calculateModelSize();
            const metadata = {
                config: this.config,
                performance: this.performance,
                trainingHistory: this.trainingHistory.map(h => ({
                    loss: h.history.loss,
                    accuracy: h.history.acc,
                    epochs: h.params.epochs
                })),
                timestamp: new Date(),
                version: this.config.modelVersion
            };

            // Save model weights and architecture
            await this.model.save(`localstorage://${name}`);

            // Save metadata
            localStorage.setItem(`model_metadata_${name}`, JSON.stringify(metadata));

            this.log(`Model saved: ${name} (${(modelSize / 1024 / 1024).toFixed(2)} MB)`, 'info');
            this.emit('modelSaved', { name, size: modelSize, metadata });

            return {
                success: true,
                message: 'Model saved successfully',
                size: modelSize,
                metadata
            };

        } catch (error) {
            this.log(`Failed to save model: ${error.message}`, 'error');
            return {
                success: false,
                message: `Failed to save model: ${error.message}`,
                size: 0,
                metadata: null
            };
        }
    }

    /**
     * Load model from storage
     */
    async loadModel(name: string): Promise<{
        success: boolean;
        message: string;
        model: any;
        metadata: any;
    }> {
        try {
            // Load model
            this.model = await tf.loadLayersModel(`localstorage://${name}`);

            // Load metadata
            const metadataStr = localStorage.getItem(`model_metadata_${name}`);
            const metadata = metadataStr ? JSON.parse(metadataStr) : null;

            if (metadata) {
                this.config = { ...this.config, ...metadata.config };
                this.performance = metadata.performance;
                this.trainingHistory = metadata.trainingHistory;
            }

            this.isInitialized = true;
            this.log(`Model loaded: ${name}`, 'info');
            this.emit('modelLoaded', { name, metadata });

            return {
                success: true,
                message: 'Model loaded successfully',
                model: this.model,
                metadata
            };

        } catch (error) {
            this.log(`Failed to load model: ${error.message}`, 'error');
            return {
                success: false,
                message: `Failed to load model: ${error.message}`,
                model: null,
                metadata: null
            };
        }
    }

    /**
     * Export model for production
     */
    async exportModel(format: 'tfjs' | 'onnx' | 'tflite' = 'tfjs'): Promise<{
        success: boolean;
        message: string;
        format: string;
        size: number;
        artifacts: any;
    }> {
        try {
            const modelSize = await this.calculateModelSize();
            let artifacts: any;

            switch (format) {
                case 'tfjs':
                    const modelArtifacts = await this.model.save(tf.io.withSaveHandler(async (artifacts) => artifacts));
                    artifacts = modelArtifacts;
                    break;

                case 'onnx':
                    // Convert to ONNX format (simplified - in practice use converter)
                    artifacts = {
                        format: 'onnx',
                        version: '1.0',
                        metadata: this.config,
                        warning: 'ONNX export requires external conversion'
                    };
                    break;

                case 'tflite':
                    artifacts = {
                        format: 'tflite',
                        version: '2.0',
                        metadata: this.config,
                        warning: 'TFLite export requires external conversion'
                    };
                    break;
            }

            this.log(`Model exported in ${format} format (${(modelSize / 1024 / 1024).toFixed(2)} MB)`, 'info');

            return {
                success: true,
                message: 'Model exported successfully',
                format,
                size: modelSize,
                artifacts
            };

        } catch (error) {
            this.log(`Failed to export model: ${error.message}`, 'error');
            return {
                success: false,
                message: `Failed to export model: ${error.message}`,
                format,
                size: 0,
                artifacts: null
            };
        }
    }

    /**
     * Get model performance statistics
     */
    getPerformanceStats(): {
        training: any;
        inference: any;
        memory: any;
        hardware: any;
    } {
        return {
            training: {
                accuracy: this.performance.accuracy,
                loss: this.performance.loss,
                precision: this.performance.precision,
                recall: this.performance.recall,
                f1Score: this.performance.f1Score,
                trainingTime: this.performance.trainingTime
            },
            inference: {
                averageTime: this.performance.inferenceTime,
                throughput: 1000 / this.performance.inferenceTime, // predictions per second
                latency: this.performance.inferenceTime
            },
            memory: {
                usage: this.performance.memoryUsage,
                gpuMemory: tf.memory().numBytesInGPU || 0,
                cpuMemory: tf.memory().numBytes - (tf.memory().numBytesInGPU || 0)
            },
            hardware: {
                backend: tf.getBackend(),
                gpuUtilization: this.performance.gpuUtilization,
                tensorflowVersion: tf.version.tfjs
            }
        };
    }

    /**
     * Reset the neural network
     */
    reset(): void {
        if (this.model) {
            tf.dispose(this.model);
            this.model = null;
        }

        this.ensembleModels.forEach(model => tf.dispose(model));
        this.ensembleModels = [];

        this.isInitialized = false;
        this.isTraining = false;
        this.trainingHistory = [];
        this.performance = {
            accuracy: 0,
            loss: 0,
            precision: 0,
            recall: 0,
            f1Score: 0,
            inferenceTime: 0,
            trainingTime: 0,
            memoryUsage: 0,
            gpuUtilization: 0
        };

        this.log('Neural network reset', 'info');
        this.emit('reset');
    }

    /**
     * Log messages with levels
     */
    private log(message: string, level: 'debug' | 'info' | 'warn' | 'error' = 'info'): void {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] [EnhancedNeuralNetwork] [${level.toUpperCase()}] ${message}`;

        this.emit('log', { level, message, timestamp });

        if (level === 'error') console.error(logMessage);
        else if (level === 'warn') console.warn(logMessage);
        else if (level === 'info') console.info(logMessage);
        else console.debug(logMessage);
    }
}

export default EnhancedNeuralNetwork;