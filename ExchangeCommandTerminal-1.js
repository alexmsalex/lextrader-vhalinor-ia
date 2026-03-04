import { EventEmitter } from 'events';
import * as blessed from 'blessed';
import * as contrib from 'blessed-contrib';
import chalk from 'chalk';
import { format, formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { table } from 'table';
import boxen from 'boxen';
import cliProgress from 'cli-progress';
import ora from 'ora';
import inquirer from 'inquirer';
import autocomplete from 'inquirer-autocomplete-prompt';
import { v4 as uuidv4 } from 'uuid';
import { RiskManager } from '../risk/RiskManager';
import { PortfolioManager } from '../portfolio/PortfolioManager';
import { MarketDataStream } from '../market/MarketDataStream';
import { EnhancedNeuralNetwork } from '../ai/EnhancedNeuralNetwork';
import { AlertSystem } from '../alerts/AlertSystem';
import { OrderValidator } from '../utils/OrderValidator';
import { PerformanceMonitor } from '../utils/PerformanceMonitor';
import { CircuitBreaker } from '../utils/CircuitBreaker';
import { OrderRouter } from '../exchange/OrderRouter';
import { ExecutionEngine } from '../exchange/ExecutionEngine';
import { OrderBookManager } from '../exchange/OrderBookManager';

/**
 * Exchange Command Terminal - Sistema Avançado de Execução de Ordens
 * 
 * Terminal de comandos para execução de ordens com validação em tempo real,
 * múltiplas estratégias de execução, circuit breakers, e integração completa
 * com todos os módulos do sistema.
 */
export class CommandTerminal extends EventEmitter {
    private config: {
        mode: 'LIVE' | 'PAPER' | 'BACKTEST';
        defaultExchange: string;
        executionStrategies: {
            market: boolean;
            limit: boolean;
            stop: boolean;
            twap: boolean;
            vwap: boolean;
            iceberg: boolean;
        };
        validationLevel: 'BASIC' | 'STRICT' | 'PARANOID';
        maxOrderSize: number;
        minOrderSize: number;
        requireConfirmation: boolean;
        autoHedge: boolean;
        slippageTolerance: number;
        maxOpenOrders: number;
        circuitBreakerThreshold: number;
        enableSmartRouting: boolean;
        enablePartialFills: boolean;
        defaultLeverage: number;
        riskPerTrade: number;
    };

    private riskManager: RiskManager;
    private portfolioManager: PortfolioManager;
    private marketData: MarketDataStream;
    private aiEngine: EnhancedNeuralNetwork;
    private alertSystem: AlertSystem;
    private orderValidator: OrderValidator;
    private performanceMonitor: PerformanceMonitor;
    private circuitBreaker: CircuitBreaker;
    private orderRouter: OrderRouter;
    private executionEngine: ExecutionEngine;
    private orderBookManager: OrderBookManager;

    private terminalScreen: blessed.Widgets.Screen | null;
    private terminalGrid: blessed.Widgets.GridElement | null;
    private orderHistory: OrderRecord[];
    private pendingOrders: PendingOrder[];
    private executionQueue: ExecutionQueueItem[];
    private activeConnections: ExchangeConnection[];
    private orderCounters: OrderCounters;
    private sessionMetrics: SessionMetrics;
    private isInitialized: boolean;
    private isExecuting: boolean;
    private circuitBreakerState: CircuitBreakerState;
    private smartOrderCache: SmartOrderCache;
    private uiComponents: TerminalUIComponents;

    constructor(config: Partial<typeof CommandTerminal.prototype.config> = {}) {
        super();

        this.config = {
            mode: config.mode || 'PAPER',
            defaultExchange: config.defaultExchange || 'BINANCE',
            executionStrategies: {
                market: config.executionStrategies?.market !== false,
                limit: config.executionStrategies?.limit !== false,
                stop: config.executionStrategies?.stop !== false,
                twap: config.executionStrategies?.twap || false,
                vwap: config.executionStrategies?.vwap || false,
                iceberg: config.executionStrategies?.iceberg || false,
                ...config.executionStrategies
            },
            validationLevel: config.validationLevel || 'STRICT',
            maxOrderSize: config.maxOrderSize || 1000000,
            minOrderSize: config.minOrderSize || 10,
            requireConfirmation: config.requireConfirmation !== false,
            autoHedge: config.autoHedge || false,
            slippageTolerance: config.slippageTolerance || 0.1,
            maxOpenOrders: config.maxOpenOrders || 50,
            circuitBreakerThreshold: config.circuitBreakerThreshold || 5,
            enableSmartRouting: config.enableSmartRouting !== false,
            enablePartialFills: config.enablePartialFills || true,
            defaultLeverage: config.defaultLeverage || 1,
            riskPerTrade: config.riskPerTrade || 2
        };

        // Inicializa módulos
        this.riskManager = new RiskManager();
        this.portfolioManager = new PortfolioManager();
        this.marketData = new MarketDataStream();
        this.aiEngine = new EnhancedNeuralNetwork();
        this.alertSystem = new AlertSystem();
        this.orderValidator = new OrderValidator();
        this.performanceMonitor = new PerformanceMonitor();
        this.circuitBreaker = new CircuitBreaker();
        this.orderRouter = new OrderRouter();
        this.executionEngine = new ExecutionEngine();
        this.orderBookManager = new OrderBookManager();

        // Estado interno
        this.terminalScreen = null;
        this.terminalGrid = null;
        this.orderHistory = [];
        this.pendingOrders = [];
        this.executionQueue = [];
        this.activeConnections = [];
        this.orderCounters = {
            total: 0,
            successful: 0,
            failed: 0,
            pending: 0,
            cancelled: 0,
            partial: 0
        };
        this.sessionMetrics = {
            startTime: new Date(),
            totalVolume: 0,
            totalFees: 0,
            avgExecutionTime: 0,
            successRate: 0,
            maxDrawdown: 0,
            sharpeRatio: 0
        };
        this.isInitialized = false;
        this.isExecuting = false;
        this.circuitBreakerState = 'CLOSED';
        this.smartOrderCache = new Map();
        this.uiComponents = {};

        // Configura eventos
        this.setupEventHandlers();

        this.setMaxListeners(100);
        this.log('Command Terminal initialized', 'info');
    }

    /**
     * Inicializa o terminal
     */
    async initialize(): Promise<{
        success: boolean;
        message: string;
        mode: string;
        exchanges: string[];
    }> {
        try {
            if (this.isInitialized) {
                return {
                    success: true,
                    message: 'Terminal already initialized',
                    mode: this.config.mode,
                    exchanges: this.activeConnections.map(c => c.exchange)
                };
            }

            // Inicializa módulos
            const initPromises = [
                this.riskManager.initialize(),
                this.portfolioManager.initialize(),
                this.marketData.initialize(),
                this.aiEngine.initialize(),
                this.orderValidator.initialize(this.config),
                this.performanceMonitor.initialize(),
                this.circuitBreaker.initialize(this.config.circuitBreakerThreshold),
                this.orderRouter.initialize(),
                this.executionEngine.initialize(),
                this.orderBookManager.initialize()
            ];

            await Promise.all(initPromises);

            // Conecta às exchanges
            await this.connectToExchanges();

            // Configura alertas
            await this.setupAlerts();

            // Inicia monitoramento de performance
            this.startPerformanceMonitoring();

            this.isInitialized = true;

            this.log(`✅ Command Terminal initialized in ${this.config.mode} mode`, 'success');
            this.log(`Active exchanges: ${this.activeConnections.map(c => c.exchange).join(', ')}`, 'info');
            this.log(`Execution strategies: ${Object.keys(this.config.executionStrategies).filter(k => this.config.executionStrategies[k]).join(', ')}`, 'info');

            this.emit('terminalInitialized', {
                mode: this.config.mode,
                config: this.config,
                connections: this.activeConnections,
                timestamp: new Date()
            });

            return {
                success: true,
                message: 'Command Terminal initialized successfully',
                mode: this.config.mode,
                exchanges: this.activeConnections.map(c => c.exchange)
            };

        } catch (error) {
            this.log(`Initialization failed: ${error.message}`, 'error');
            this.emit('initializationFailed', error);

            return {
                success: false,
                message: `Initialization failed: ${error.message}`,
                mode: this.config.mode,
                exchanges: []
            };
        }
    }

    /**
     * Executa uma ordem com validação completa
     */
    async execute(order: OrderRequest, options: ExecutionOptions = {}): Promise<OrderExecutionResult> {
        const orderId = uuidv4();
        const startTime = Date.now();

        try {
            if (!this.isInitialized) {
                throw new Error('Terminal not initialized');
            }

            if (this.circuitBreakerState === 'OPEN') {
                throw new Error('Circuit breaker is OPEN - trading suspended');
            }

            if (this.isExecuting) {
                throw new Error('Another order is being executed');
            }

            this.isExecuting = true;

            this.log(`⚡ CMD_NEXUS: Processing order ${orderId}`, 'info');
            this.emit('orderProcessingStarted', { orderId, order });

            // 1. Validação básica
            const validationResult = await this.validateOrder(order);
            if (!validationResult.valid) {
                throw new Error(`Order validation failed: ${validationResult.errors.join(', ')}`);
            }

            // 2. Análise de risco
            const riskAnalysis = await this.analyzeRisk(order);
            if (!riskAnalysis.approved) {
                throw new Error(`Risk analysis failed: ${riskAnalysis.reasons.join(', ')}`);
            }

            // 3. Obter melhor preço/rota
            const routingResult = await this.routeOrder(order, options);

            // 4. Confirmação (se necessário)
            if (this.config.requireConfirmation && !options.skipConfirmation) {
                const confirmed = await this.requestConfirmation(order, routingResult);
                if (!confirmed) {
                    throw new Error('Order cancelled by user');
                }
            }

            // 5. Execução
            const executionResult = await this.executeOrder(orderId, order, routingResult, options);

            // 6. Pós-execução
            await this.postExecutionProcessing(orderId, order, executionResult);

            // 7. Atualizar métricas
            this.updateMetrics(order, executionResult, Date.now() - startTime);

            this.isExecuting = false;

            this.log(`✅ Order ${orderId} executed successfully`, 'success');
            this.emit('orderExecuted', { orderId, order, result: executionResult });

            return {
                success: true,
                orderId,
                executionResult,
                timestamp: new Date(),
                metrics: this.getOrderMetrics(orderId)
            };

        } catch (error) {
            this.isExecuting = false;

            const errorResult: OrderExecutionResult = {
                success: false,
                orderId,
                error: error.message,
                timestamp: new Date(),
                metrics: null
            };

            this.log(`❌ Order ${orderId} failed: ${error.message}`, 'error');
            this.emit('orderFailed', { orderId, order, error: error.message });

            // Verifica se precisa abrir circuit breaker
            await this.checkCircuitBreaker();

            return errorResult;
        }
    }

    /**
     * Executa múltiplas ordens em lote
     */
    async executeBatch(orders: OrderRequest[], options: BatchExecutionOptions = {}): Promise<BatchExecutionResult> {
        const batchId = uuidv4();
        const startTime = Date.now();
        const results: OrderExecutionResult[] = [];
        const errors: BatchError[] = [];

        this.log(`📦 Executing batch ${batchId} with ${orders.length} orders`, 'info');
        this.emit('batchExecutionStarted', { batchId, orderCount: orders.length });

        // Cria barra de progresso para batch
        const progressBar = new cliProgress.SingleBar({
            format: `${chalk.cyan('{bar}')} {percentage}% | {value}/{total} orders | ETA: {eta}s`,
            barCompleteChar: '█',
            barIncompleteChar: '░',
            hideCursor: true
        }, cliProgress.Presets.shades_classic);

        progressBar.start(orders.length, 0);

        try {
            const executionMode = options.executionMode || 'SEQUENTIAL';
            const maxConcurrent = options.maxConcurrent || 3;

            switch (executionMode) {
                case 'SEQUENTIAL':
                    // Execução sequencial
                    for (let i = 0; i < orders.length; i++) {
                        try {
                            const result = await this.execute(orders[i], {
                                ...options,
                                skipConfirmation: true
                            });
                            results.push(result);
                        } catch (error) {
                            errors.push({
                                orderIndex: i,
                                error: error.message,
                                order: orders[i]
                            });
                        }
                        progressBar.update(i + 1);
                    }
                    break;

                case 'PARALLEL':
                    // Execução paralela limitada
                    const chunks = this.chunkArray(orders, maxConcurrent);
                    for (let chunkIndex = 0; chunkIndex < chunks.length; chunkIndex++) {
                        const chunk = chunks[chunkIndex];
                        const chunkPromises = chunk.map((order, index) =>
                            this.execute(order, { ...options, skipConfirmation: true })
                                .then(result => ({ success: true, result }))
                                .catch(error => ({ success: false, error, order }))
                        );

                        const chunkResults = await Promise.allSettled(chunkPromises);

                        chunkResults.forEach((result, index) => {
                            if (result.status === 'fulfilled') {
                                const value = result.value;
                                if (value.success) {
                                    results.push(value.result);
                                } else {
                                    errors.push({
                                        orderIndex: chunkIndex * maxConcurrent + index,
                                        error: value.error.message,
                                        order: value.order
                                    });
                                }
                            }
                        });

                        progressBar.update((chunkIndex + 1) * maxConcurrent);
                    }
                    break;

                case 'TWAP':
                    // Execução TWAP (Time Weighted Average Price)
                    await this.executeTWAPBatch(orders, options, progressBar, results, errors);
                    break;

                case 'VWAP':
                    // Execução VWAP (Volume Weighted Average Price)
                    await this.executeVWAPBatch(orders, options, progressBar, results, errors);
                    break;
            }

            progressBar.stop();

            const batchResult: BatchExecutionResult = {
                batchId,
                success: errors.length === 0,
                totalOrders: orders.length,
                successfulOrders: results.length,
                failedOrders: errors.length,
                results,
                errors,
                executionTime: Date.now() - startTime,
                averageExecutionTime: results.length > 0
                    ? results.reduce((sum, r) => sum + (r.metrics?.executionTime || 0), 0) / results.length
                    : 0,
                timestamp: new Date()
            };

            this.log(`📦 Batch ${batchId} completed: ${results.length} successful, ${errors.length} failed`,
                errors.length === 0 ? 'success' : 'warning');

            this.emit('batchExecutionCompleted', batchResult);

            return batchResult;

        } catch (error) {
            progressBar.stop();
            this.log(`❌ Batch ${batchId} failed: ${error.message}`, 'error');

            return {
                batchId,
                success: false,
                totalOrders: orders.length,
                successfulOrders: results.length,
                failedOrders: errors.length + 1,
                results,
                errors: [...errors, {
                    orderIndex: -1,
                    error: error.message,
                    order: null
                }],
                executionTime: Date.now() - startTime,
                averageExecutionTime: 0,
                timestamp: new Date()
            };
        }
    }

    /**
     * Executa ordem com estratégia TWAP
     */
    private async executeTWAPBatch(
        orders: OrderRequest[],
        options: BatchExecutionOptions,
        progressBar: cliProgress.SingleBar,
        results: OrderExecutionResult[],
        errors: BatchError[]
    ): Promise<void> {
        const totalDuration = options.twapDuration || 300000; // 5 minutos padrão
        const slices = options.twapSlices || 10;
        const sliceDuration = totalDuration / slices;

        const totalAmount = orders.reduce((sum, order) => sum + order.amount, 0);
        const sliceAmount = totalAmount / slices;

        for (let slice = 0; slice < slices; slice++) {
            // Distribui ordens proporcionalmente para cada slice
            const sliceOrders = orders.map(order => ({
                ...order,
                amount: order.amount * (sliceAmount / totalAmount)
            }));

            // Executa slice atual
            for (let i = 0; i < sliceOrders.length; i++) {
                try {
                    const result = await this.execute(sliceOrders[i], {
                        ...options,
                        skipConfirmation: true,
                        strategy: 'TWAP',
                        slice: slice + 1,
                        totalSlices: slices
                    });
                    results.push(result);
                } catch (error) {
                    errors.push({
                        orderIndex: slice * sliceOrders.length + i,
                        error: error.message,
                        order: sliceOrders[i]
                    });
                }
            }

            progressBar.update((slice + 1) * (orders.length / slices));

            // Aguarda intervalo entre slices (exceto no último)
            if (slice < slices - 1) {
                await new Promise(resolve => setTimeout(resolve, sliceDuration));
            }
        }
    }

    /**
     * Executa ordem com estratégia VWAP
     */
    private async executeVWAPBatch(
        orders: OrderRequest[],
        options: BatchExecutionOptions,
        progressBar: cliProgress.SingleBar,
        results: OrderExecutionResult[],
        errors: BatchError[]
    ): Promise<void> {
        // Obter dados de volume do mercado
        const volumeData = await this.marketData.getVolumeProfile(
            orders[0].symbol,
            options.vwapPeriod || '1h'
        );

        // Calcular distribuição baseada em volume
        const volumeSlices = this.calculateVolumeSlices(volumeData, orders.length);

        for (let i = 0; i < orders.length; i++) {
            const order = orders[i];
            const slice = volumeSlices[i];

            try {
                const result = await this.execute({
                    ...order,
                    amount: order.amount * slice.percentage
                }, {
                    ...options,
                    skipConfirmation: true,
                    strategy: 'VWAP',
                    volumeSlice: slice
                });
                results.push(result);
            } catch (error) {
                errors.push({
                    orderIndex: i,
                    error: error.message,
                    order
                });
            }

            progressBar.update(i + 1);

            // Aguarda baseado no perfil de volume
            if (i < orders.length - 1) {
                const waitTime = slice.duration * 1000; // converter para ms
                await new Promise(resolve => setTimeout(resolve, waitTime));
            }
        }
    }

    /**
     * Valida ordem completa
     */
    private async validateOrder(order: OrderRequest): Promise<ValidationResult> {
        const errors: string[] = [];
        const warnings: string[] = [];

        // Validação básica
        if (!order.symbol || !order.side || !order.amount) {
            errors.push('Missing required fields');
        }

        if (order.amount <= 0) {
            errors.push('Amount must be positive');
        }

        if (order.amount < this.config.minOrderSize) {
            errors.push(`Amount below minimum (${this.config.minOrderSize})`);
        }

        if (order.amount > this.config.maxOrderSize) {
            errors.push(`Amount exceeds maximum (${this.config.maxOrderSize})`);
        }

        // Validação de símbolo
        const validSymbols = await this.marketData.getAvailableSymbols();
        if (!validSymbols.includes(order.symbol)) {
            errors.push(`Invalid symbol: ${order.symbol}`);
        }

        // Validação de tipo de ordem
        if (order.type && !this.config.executionStrategies[order.type.toLowerCase()]) {
            errors.push(`Order type not supported: ${order.type}`);
        }

        // Validação de preço para ordens limit
        if (order.type === 'LIMIT' && (!order.price || order.price <= 0)) {
            errors.push('Limit orders require a valid price');
        }

        // Validação de stop para ordens stop
        if (order.type === 'STOP' && (!order.stopPrice || order.stopPrice <= 0)) {
            errors.push('Stop orders require a valid stop price');
        }

        // Validação de leverage
        if (order.leverage && order.leverage > 100) {
            warnings.push('High leverage detected');
        }

        // Verifica se mercado está aberto
        const marketStatus = await this.marketData.getMarketStatus(order.symbol);
        if (!marketStatus.trading) {
            warnings.push('Market is not currently trading');
        }

        return {
            valid: errors.length === 0,
            errors,
            warnings,
            timestamp: new Date()
        };
    }

    /**
     * Análise de risco para ordem
     */
    private async analyzeRisk(order: OrderRequest): Promise<RiskAnalysis> {
        const reasons: string[] = [];
        const riskFactors: RiskFactor[] = [];
        let riskScore = 0;

        // 1. Análise de posição atual
        const currentPosition = await this.portfolioManager.getPosition(order.symbol);
        if (currentPosition) {
            const exposure = Math.abs(currentPosition.size * currentPosition.entryPrice);
            if (exposure > this.config.maxOrderSize * 0.5) {
                riskScore += 30;
                riskFactors.push({
                    factor: 'High existing exposure',
                    score: 30,
                    details: `Current exposure: ${exposure}`
                });
            }
        }

        // 2. Análise de volatilidade
        const volatility = await this.marketData.getVolatility(order.symbol);
        if (volatility > 0.05) { // 5% de volatilidade
            riskScore += 20;
            riskFactors.push({
                factor: 'High volatility',
                score: 20,
                details: `Volatility: ${(volatility * 100).toFixed(2)}%`
            });
        }

        // 3. Análise de liquidez
        const liquidity = await this.marketData.getLiquidity(order.symbol);
        const orderValue = order.amount * (order.price || await this.marketData.getCurrentPrice(order.symbol));
        if (orderValue > liquidity * 0.1) { // Ordem > 10% da liquidez
            riskScore += 25;
            riskFactors.push({
                factor: 'Low liquidity for order size',
                score: 25,
                details: `Order size: ${orderValue.toFixed(2)}, Liquidity: ${liquidity.toFixed(2)}`
            });
        }

        // 4. Análise de correlação
        const correlation = await this.riskManager.getPortfolioCorrelation(order.symbol);
        if (correlation > 0.8) {
            riskScore += 15;
            riskFactors.push({
                factor: 'High portfolio correlation',
                score: 15,
                details: `Correlation: ${correlation.toFixed(2)}`
            });
        }

        // 5. Análise de drawdown recente
        const recentDrawdown = await this.portfolioManager.getRecentDrawdown();
        if (recentDrawdown < -0.05) { // -5% drawdown
            riskScore += 10;
            riskFactors.push({
                factor: 'Recent drawdown',
                score: 10,
                details: `Drawdown: ${(recentDrawdown * 100).toFixed(2)}%`
            });
        }

        // Verifica limites de risco
        if (riskScore > 50) {
            reasons.push(`Risk score too high: ${riskScore}/100`);
        }

        // Verifica limite de perda por trade
        const maxLoss = this.config.riskPerTrade / 100 * (await this.portfolioManager.getTotalValue());
        const potentialLoss = await this.riskManager.calculatePotentialLoss(order);
        if (potentialLoss > maxLoss) {
            reasons.push(`Potential loss (${potentialLoss.toFixed(2)}) exceeds risk limit (${maxLoss.toFixed(2)})`);
        }

        // Verifica concentração
        const concentration = await this.riskManager.getConcentrationRisk(order.symbol);
        if (concentration > 0.3) { // 30% concentração
            reasons.push(`High concentration risk: ${(concentration * 100).toFixed(1)}%`);
        }

        return {
            approved: reasons.length === 0,
            reasons,
            riskScore,
            riskFactors,
            timestamp: new Date()
        };
    }

    /**
     * Roteamento inteligente de ordem
     */
    private async routeOrder(order: OrderRequest, options: ExecutionOptions): Promise<RoutingResult> {
        const startTime = Date.now();

        // Verifica cache primeiro
        const cacheKey = this.getRoutingCacheKey(order);
        const cached = this.smartOrderCache.get(cacheKey);
        if (cached && Date.now() - cached.timestamp < 5000) { // Cache de 5 segundos
            this.log(`Using cached routing for ${order.symbol}`, 'debug');
            return cached.result;
        }

        let routingResult: RoutingResult;

        if (this.config.enableSmartRouting) {
            // Roteamento inteligente multi-exchange
            routingResult = await this.orderRouter.findBestRoute(order);
        } else {
            // Roteamento simples para exchange padrão
            routingResult = {
                exchange: this.config.defaultExchange,
                price: await this.getBestPrice(order),
                estimatedFees: await this.calculateFees(order),
                estimatedSlippage: await this.estimateSlippage(order),
                routeScore: 85,
                alternatives: []
            };
        }

        // Adiciona predição da IA se disponível
        if (options.useAI !== false) {
            const aiPrediction = await this.getAIPrediction(order);
            routingResult.aiPrediction = aiPrediction;
        }

        // Cache do resultado
        this.smartOrderCache.set(cacheKey, {
            result: routingResult,
            timestamp: Date.now()
        });

        // Limpa cache antigo
        this.cleanSmartOrderCache();

        const routingTime = Date.now() - startTime;
        this.log(`Routing completed in ${routingTime}ms for ${order.symbol}`, 'debug');

        return routingResult;
    }

    /**
     * Obtém melhor preço para ordem
     */
    private async getBestPrice(order: OrderRequest): Promise<number> {
        const orderBook = await this.orderBookManager.getOrderBook(order.symbol);

        if (order.type === 'MARKET') {
            return order.side === 'BUY'
                ? orderBook.asks[0]?.price || 0
                : orderBook.bids[0]?.price || 0;
        } else if (order.type === 'LIMIT') {
            return order.price!;
        } else if (order.type === 'STOP') {
            return order.stopPrice!;
        }

        return await this.marketData.getCurrentPrice(order.symbol);
    }

    /**
     * Calcula taxas estimadas
     */
    private async calculateFees(order: OrderRequest): Promise<number> {
        const exchange = this.config.defaultExchange;
        const feeRates = {
            'BINANCE': 0.001, // 0.1%
            'COINBASE': 0.005, // 0.5%
            'KRAKEN': 0.0026, // 0.26%
            'FTX': 0.0007 // 0.07%
        };

        const orderValue = order.amount * (order.price || await this.marketData.getCurrentPrice(order.symbol));
        const baseFee = orderValue * (feeRates[exchange] || 0.002);

        // Desconto por volume (se aplicável)
        const volumeDiscount = await this.getVolumeDiscount(exchange);
        const finalFee = baseFee * (1 - volumeDiscount);

        return finalFee;
    }

    /**
     * Estima slippage
     */
    private async estimateSlippage(order: OrderRequest): Promise<number> {
        const orderBook = await this.orderBookManager.getOrderBook(order.symbol);
        const orderValue = order.amount * (order.price || await this.marketData.getCurrentPrice(order.symbol));

        if (order.side === 'BUY') {
            const availableLiquidity = orderBook.asks.reduce((sum, ask) => sum + ask.quantity * ask.price, 0);
            if (orderValue > availableLiquidity * 0.1) {
                return 0.02; // 2% de slippage estimado
            }
        } else {
            const availableLiquidity = orderBook.bids.reduce((sum, bid) => sum + bid.quantity * bid.price, 0);
            if (orderValue > availableLiquidity * 0.1) {
                return 0.02;
            }
        }

        return 0.001; // 0.1% slippage para ordens pequenas
    }

    /**
     * Obtém predição da IA para ordem
     */
    private async getAIPrediction(order: OrderRequest): Promise<AIPrediction> {
        try {
            const marketData = await this.marketData.getMarketData(order.symbol, '1h');
            const prediction = await this.aiEngine.predict({
                features: [marketData.features],
                options: {
                    returnProbabilities: true,
                    returnUncertainty: true
                }
            });

            return {
                signal: prediction.signal,
                confidence: prediction.confidence,
                probabilities: prediction.probabilities,
                uncertainty: prediction.uncertainty,
                recommendation: this.getAIRecoommendation(prediction, order)
            };
        } catch (error) {
            this.log(`AI prediction failed: ${error.message}`, 'debug');
            return null;
        }
    }

    /**
     * Gera recomendação baseada na predição da IA
     */
    private getAIRecoommendation(prediction: any, order: OrderRequest): string {
        const { signal, confidence } = prediction;

        if (confidence < 0.6) {
            return 'Low confidence - consider waiting';
        }

        if (order.side === 'BUY') {
            if (signal === 'STRONG_BUY' || signal === 'BUY') {
                return 'AI confirms BUY signal';
            } else if (signal === 'STRONG_SELL' || signal === 'SELL') {
                return 'AI suggests SELL - reconsider order';
            }
        } else {
            if (signal === 'STRONG_SELL' || signal === 'SELL') {
                return 'AI confirms SELL signal';
            } else if (signal === 'STRONG_BUY' || signal === 'BUY') {
                return 'AI suggests BUY - reconsider order';
            }
        }

        return 'AI neutral - proceed with caution';
    }

    /**
     * Solicita confirmação do usuário
     */
    private async requestConfirmation(order: OrderRequest, routing: RoutingResult): Promise<boolean> {
        if (this.config.mode === 'BACKTEST') {
            return true; // Sem confirmação em backtest
        }

        const orderValue = order.amount * (routing.price || 0);

        const confirmationMessage = boxen(
            `${chalk.bold('📝 Order Confirmation')}\n\n` +
            `${chalk.cyan('Symbol:')} ${order.symbol}\n` +
            `${chalk.cyan('Side:')} ${chalk[order.side === 'BUY' ? 'green' : 'red'](order.side)}\n` +
            `${chalk.cyan('Amount:')} ${order.amount}\n` +
            `${chalk.cyan('Price:')} ${routing.price ? this.formatCurrency(routing.price) : 'MARKET'}\n` +
            `${chalk.cyan('Type:')} ${order.type || 'MARKET'}\n` +
            `${chalk.cyan('Value:')} ${this.formatCurrency(orderValue)}\n` +
            `${chalk.cyan('Fees:')} ${this.formatCurrency(routing.estimatedFees)}\n` +
            `${chalk.cyan('Slippage:')} ${(routing.estimatedSlippage * 100).toFixed(2)}%\n` +
            `${chalk.cyan('Exchange:')} ${routing.exchange}\n\n` +
            `${routing.aiPrediction ? `${chalk.cyan('AI Prediction:')} ${routing.aiPrediction.recommendation}\n\n` : ''}` +
            `${chalk.bold('Proceed with order?')}`,
            {
                padding: 1,
                borderStyle: 'double',
                borderColor: order.side === 'BUY' ? 'green' : 'red',
                backgroundColor: '#111'
            }
        );

        console.log(confirmationMessage);

        const answers = await inquirer.prompt([
            {
                type: 'confirm',
                name: 'confirm',
                message: 'Confirm order execution?',
                default: false
            }
        ]);

        return answers.confirm;
    }

    /**
     * Executa a ordem na exchange
     */
    private async executeOrder(
        orderId: string,
        order: OrderRequest,
        routing: RoutingResult,
        options: ExecutionOptions
    ): Promise<ExecutionResult> {
        const startTime = Date.now();
        const executionId = uuidv4();

        this.log(`🚀 Executing order ${orderId} on ${routing.exchange}`, 'info');
        this.emit('orderExecutionStarted', { orderId, executionId, order, routing });

        // Adiciona à fila de execução
        this.executionQueue.push({
            orderId,
            executionId,
            order,
            routing,
            status: 'PENDING',
            timestamp: new Date()
        });

        let executionResult: ExecutionResult;

        try {
            // Escolhe estratégia de execução
            const executionStrategy = options.strategy || this.getExecutionStrategy(order, routing);

            switch (executionStrategy) {
                case 'IMMEDIATE':
                    executionResult = await this.executeImmediate(order, routing);
                    break;
                case 'TWAP':
                    executionResult = await this.executeTWAP(order, routing, options);
                    break;
                case 'VWAP':
                    executionResult = await this.executeVWAP(order, routing, options);
                    break;
                case 'ICEBERG':
                    executionResult = await this.executeIceberg(order, routing, options);
                    break;
                default:
                    executionResult = await this.executeImmediate(order, routing);
            }

            const executionTime = Date.now() - startTime;

            // Atualiza fila de execução
            const queueItem = this.executionQueue.find(item => item.executionId === executionId);
            if (queueItem) {
                queueItem.status = 'COMPLETED';
                queueItem.executionTime = executionTime;
                queueItem.result = executionResult;
            }

            this.log(`✅ Execution ${executionId} completed in ${executionTime}ms`, 'success');

            return executionResult;

        } catch (error) {
            const executionTime = Date.now() - startTime;

            // Atualiza fila de execução
            const queueItem = this.executionQueue.find(item => item.executionId === executionId);
            if (queueItem) {
                queueItem.status = 'FAILED';
                queueItem.executionTime = executionTime;
                queueItem.error = error.message;
            }

            this.log(`❌ Execution ${executionId} failed in ${executionTime}ms: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * Execução imediata (market/limit)
     */
    private async executeImmediate(order: OrderRequest, routing: RoutingResult): Promise<ExecutionResult> {
        const executionParams = {
            symbol: order.symbol,
            side: order.side,
            quantity: order.amount,
            type: order.type || 'MARKET',
            price: order.type === 'LIMIT' ? order.price : undefined,
            stopPrice: order.type === 'STOP' ? order.stopPrice : undefined
        };

        const result = await this.executionEngine.execute(executionParams, routing.exchange);

        return {
            success: result.success,
            executedPrice: result.price,
            executedAmount: result.quantity,
            fees: result.fees,
            orderId: result.orderId,
            exchangeOrderId: result.exchangeOrderId,
            timestamp: new Date(),
            fills: result.fills || [],
            averagePrice: result.averagePrice || result.price
        };
    }

    /**
     * Execução TWAP
     */
    private async executeTWAP(
        order: OrderRequest,
        routing: RoutingResult,
        options: ExecutionOptions
    ): Promise<ExecutionResult> {
        const slices = options.twapSlices || 10;
        const sliceAmount = order.amount / slices;
        const sliceInterval = (options.twapDuration || 300000) / slices; // 5 minutos padrão

        const fills: Fill[] = [];
        let totalExecuted = 0;
        let totalFees = 0;
        let weightedPrice = 0;

        for (let i = 0; i < slices; i++) {
            try {
                const sliceOrder = {
                    ...order,
                    amount: sliceAmount,
                    type: 'MARKET' // Cada slice como market order
                };

                const sliceResult = await this.executeImmediate(sliceOrder, routing);

                fills.push(...sliceResult.fills);
                totalExecuted += sliceResult.executedAmount;
                totalFees += sliceResult.fees;
                weightedPrice += sliceResult.averagePrice * sliceResult.executedAmount;

                this.log(`TWAP slice ${i + 1}/${slices} executed`, 'info');

                // Aguarda intervalo (exceto no último slice)
                if (i < slices - 1) {
                    await new Promise(resolve => setTimeout(resolve, sliceInterval));
                }

            } catch (error) {
                this.log(`TWAP slice ${i + 1} failed: ${error.message}`, 'warning');
                // Continua com próximo slice
            }
        }

        const averagePrice = totalExecuted > 0 ? weightedPrice / totalExecuted : 0;

        return {
            success: totalExecuted > 0,
            executedPrice: averagePrice,
            executedAmount: totalExecuted,
            fees: totalFees,
            orderId: uuidv4(),
            exchangeOrderId: 'TWAP_COMPOSITE',
            timestamp: new Date(),
            fills,
            averagePrice,
            strategy: 'TWAP'
        };
    }

    /**
     * Execução Iceberg
     */
    private async executeIceberg(
        order: OrderRequest,
        routing: RoutingResult,
        options: ExecutionOptions
    ): Promise<ExecutionResult> {
        const peakSize = options.icebergPeak || order.amount * 0.1; // 10% padrão
        const restSize = order.amount - peakSize;

        // Executa pico inicial
        const peakOrder = {
            ...order,
            amount: peakSize,
            type: 'LIMIT',
            price: routing.price
        };

        const peakResult = await this.executeImmediate(peakOrder, routing);

        // Executa resto como ordem oculta
        const restOrder = {
            ...order,
            amount: restSize,
            type: 'LIMIT',
            price: routing.price,
            hidden: true
        };

        const restResult = await this.executeImmediate(restOrder, routing);

        // Combina resultados
        const combinedFills = [...peakResult.fills, ...restResult.fills];
        const totalExecuted = peakResult.executedAmount + restResult.executedAmount;
        const totalFees = peakResult.fees + restResult.fees;
        const weightedPrice = (peakResult.averagePrice * peakResult.executedAmount +
            restResult.averagePrice * restResult.executedAmount) / totalExecuted;

        return {
            success: peakResult.success && restResult.success,
            executedPrice: weightedPrice,
            executedAmount: totalExecuted,
            fees: totalFees,
            orderId: uuidv4(),
            exchangeOrderId: 'ICEBERG_COMPOSITE',
            timestamp: new Date(),
            fills: combinedFills,
            averagePrice: weightedPrice,
            strategy: 'ICEBERG'
        };
    }

    /**
     * Processamento pós-execução
     */
    private async postExecutionProcessing(
        orderId: string,
        order: OrderRequest,
        executionResult: ExecutionResult
    ): Promise<void> {
        // 1. Atualiza portfólio
        await this.portfolioManager.updatePosition({
            symbol: order.symbol,
            side: order.side,
            size: executionResult.executedAmount,
            entryPrice: executionResult.averagePrice,
            timestamp: new Date(),
            orderId
        });

        // 2. Atualiza histórico
        const orderRecord: OrderRecord = {
            orderId,
            ...order,
            executionResult,
            status: executionResult.success ? 'FILLED' : 'FAILED',
            timestamp: new Date(),
            metrics: this.getOrderMetrics(orderId)
        };

        this.orderHistory.push(orderRecord);

        // 3. Limita histórico
        if (this.orderHistory.length > 1000) {
            this.orderHistory = this.orderHistory.slice(-1000);
        }

        // 4. Hedge automático (se configurado)
        if (this.config.autoHedge && executionResult.success) {
            await this.autoHedgePosition(order, executionResult);
        }

        // 5. Emite eventos
        this.emit('orderRecorded', orderRecord);

        // 6. Log detalhado
        this.logOrderExecution(orderRecord);
    }

    /**
     * Hedge automático de posição
     */
    private async autoHedgePosition(order: OrderRequest, executionResult: ExecutionResult): Promise<void> {
        try {
            const riskExposure = await this.riskManager.calculateExposure(order.symbol);
            if (riskExposure > this.config.riskPerTrade) {
                const hedgeAmount = executionResult.executedAmount * 0.1; // Hedge 10%
                const hedgeSide = order.side === 'BUY' ? 'SELL' : 'BUY';

                const hedgeOrder: OrderRequest = {
                    symbol: order.symbol,
                    side: hedgeSide,
                    amount: hedgeAmount,
                    type: 'MARKET'
                };

                this.log(`Auto-hedging ${hedgeAmount} ${order.symbol}`, 'info');
                await this.execute(hedgeOrder, { skipConfirmation: true });

                this.emit('positionHedged', {
                    symbol: order.symbol,
                    amount: hedgeAmount,
                    side: hedgeSide,
                    reason: 'Risk exposure limit'
                });
            }
        } catch (error) {
            this.log(`Auto-hedge failed: ${error.message}`, 'warning');
        }
    }

    /**
     * Log de execução de ordem
     */
    private logOrderExecution(orderRecord: OrderRecord): void {
        const { orderId, symbol, side, amount, executionResult, status } = orderRecord;

        const logBox = boxen(
            `${chalk.bold('📊 Order Execution Report')}\n\n` +
            `${chalk.cyan('Order ID:')} ${orderId}\n` +
            `${chalk.cyan('Symbol:')} ${symbol}\n` +
            `${chalk.cyan('Side:')} ${chalk[side === 'BUY' ? 'green' : 'red'](side)}\n` +
            `${chalk.cyan('Requested:')} ${amount}\n` +
            `${chalk.cyan('Executed:')} ${executionResult.executedAmount}\n` +
            `${chalk.cyan('Average Price:')} ${this.formatCurrency(executionResult.averagePrice)}\n` +
            `${chalk.cyan('Fees:')} ${this.formatCurrency(executionResult.fees)}\n` +
            `${chalk.cyan('Status:')} ${chalk[status === 'FILLED' ? 'green' : 'red'](status)}\n` +
            `${chalk.cyan('Execution Time:')} ${orderRecord.metrics?.executionTime || 0}ms\n` +
            `${chalk.cyan('Fill Rate:')} ${((executionResult.executedAmount / amount) * 100).toFixed(1)}%`,
            {
                padding: 1,
                borderStyle: 'single',
                borderColor: status === 'FILLED' ? 'green' : 'red',
                backgroundColor: '#111'
            }
        );

        console.log(logBox);
    }

    /**
     * Atualiza métricas da sessão
     */
    private updateMetrics(order: OrderRequest, executionResult: ExecutionResult, executionTime: number): void {
        this.orderCounters.total++;

        if (executionResult.success) {
            this.orderCounters.successful++;
            this.sessionMetrics.totalVolume += executionResult.executedAmount * executionResult.averagePrice;
            this.sessionMetrics.totalFees += executionResult.fees;

            // Atualiza tempo médio de execução
            const totalTime = this.sessionMetrics.avgExecutionTime * (this.orderCounters.successful - 1);
            this.sessionMetrics.avgExecutionTime = (totalTime + executionTime) / this.orderCounters.successful;
        } else {
            this.orderCounters.failed++;
        }

        // Atualiza taxa de sucesso
        this.sessionMetrics.successRate = this.orderCounters.successful / this.orderCounters.total;

        // Atualiza métricas de performance
        this.updatePerformanceMetrics();
    }

    /**
     * Atualiza métricas de performance
     */
    private updatePerformanceMetrics(): void {
        // Atualiza drawdown máximo
        const currentDrawdown = this.portfolioManager.getCurrentDrawdown();
        if (currentDrawdown < this.sessionMetrics.maxDrawdown) {
            this.sessionMetrics.maxDrawdown = currentDrawdown;
        }

        // Atualiza Sharpe ratio
        this.sessionMetrics.sharpeRatio = this.portfolioManager.getSharpeRatio();
    }

    /**
     * Obtém métricas da ordem
     */
    private getOrderMetrics(orderId: string): OrderMetrics | null {
        const orderRecord = this.orderHistory.find(o => o.orderId === orderId);
        if (!orderRecord) return null;

        const execution = orderRecord.executionResult;

        return {
            orderId,
            executionTime: orderRecord.metrics?.executionTime || 0,
            fillRate: execution.executedAmount / orderRecord.amount,
            slippage: execution.averagePrice ?
                Math.abs((execution.averagePrice - (orderRecord.price || 0)) / (orderRecord.price || 1)) : 0,
            costPercentage: execution.fees / (execution.executedAmount * execution.averagePrice),
            latency: orderRecord.metrics?.latency || 0,
            queueTime: orderRecord.metrics?.queueTime || 0,
            exchangeLatency: orderRecord.metrics?.exchangeLatency || 0
        };
    }

    /**
     * Verifica circuit breaker
     */
    private async checkCircuitBreaker(): Promise<void> {
        const recentFailures = this.orderHistory
            .slice(-10)
            .filter(o => o.status === 'FAILED').length;

        if (recentFailures >= this.config.circuitBreakerThreshold) {
            this.circuitBreakerState = 'OPEN';
            this.log(`⚠️ Circuit breaker OPENED - ${recentFailures} recent failures`, 'error');

            this.emit('circuitBreakerOpened', {
                reason: `${recentFailures} consecutive failures`,
                timestamp: new Date()
            });

            // Tenta resetar após 60 segundos
            setTimeout(() => {
                this.circuitBreakerState = 'HALF_OPEN';
                this.log('Circuit breaker HALF-OPEN - testing recovery', 'warning');
            }, 60000);
        }
    }

    /**
     * Conecta às exchanges
     */
    private async connectToExchanges(): Promise<void> {
        const exchanges = ['BINANCE', 'COINBASE', 'KRAKEN', 'FTX'];

        for (const exchange of exchanges) {
            try {
                const connection = await this.executionEngine.connect(exchange);
                this.activeConnections.push({
                    exchange,
                    connected: true,
                    latency: connection.latency,
                    lastChecked: new Date()
                });

                this.log(`✅ Connected to ${exchange} (${connection.latency}ms)`, 'success');
            } catch (error) {
                this.activeConnections.push({
                    exchange,
                    connected: false,
                    latency: 0,
                    lastChecked: new Date()
                });

                this.log(`❌ Failed to connect to ${exchange}: ${error.message}`, 'error');
            }
        }
    }

    /**
     * Configura alertas
     */
    private async setupAlerts(): Promise<void> {
        this.alertSystem.on('alert', (alert) => {
            this.displayTerminalAlert(alert);
        });

        // Configura alertas padrão
        await this.alertSystem.addAlert({
            type: 'ORDER_FAILURE',
            condition: () => this.orderCounters.failed > 5,
            message: 'Multiple order failures detected',
            severity: 'HIGH'
        });

        await this.alertSystem.addAlert({
            type: 'HIGH_SLIPPAGE',
            condition: async () => {
                const recentOrders = this.orderHistory.slice(-5);
                const avgSlippage = recentOrders.reduce((sum, o) =>
                    sum + (o.metrics?.slippage || 0), 0) / recentOrders.length;
                return avgSlippage > 0.02; // 2% slippage
            },
            message: 'High slippage detected',
            severity: 'MEDIUM'
        });
    }

    /**
     * Inicia monitoramento de performance
     */
    private startPerformanceMonitoring(): void {
        setInterval(() => {
            this.performanceMonitor.recordMetrics({
                orderCount: this.orderCounters.total,
                successRate: this.sessionMetrics.successRate,
                avgExecutionTime: this.sessionMetrics.avgExecutionTime,
                circuitBreakerState: this.circuitBreakerState,
                activeConnections: this.activeConnections.filter(c => c.connected).length
            });
        }, 30000); // A cada 30 segundos
    }

    /**
     * Mostra terminal interativo
     */
    async showTerminal(): Promise<void> {
        if (this.terminalScreen) {
            return; // Já está aberto
        }

        try {
            // Cria tela blessed
            this.terminalScreen = blessed.screen({
                smartCSR: true,
                title: 'LEXTRADER Command Terminal',
                cursor: {
                    artificial: true,
                    shape: 'line',
                    blink: true
                }
            });

            // Cria grid
            this.terminalGrid = contrib.grid({
                rows: 12,
                cols: 12,
                screen: this.terminalScreen
            });

            // Adiciona widgets
            this.addTerminalWidgets();

            // Configura teclas de atalho
            this.setupTerminalKeybindings();

            // Renderiza
            this.terminalScreen.render();

            // Atualiza periódicamente
            setInterval(() => this.updateTerminalWidgets(), 2000);

            this.log('Terminal interface started', 'info');

        } catch (error) {
            this.log(`Failed to start terminal: ${error.message}`, 'error');
        }
    }

    /**
     * Adiciona widgets ao terminal
     */
    private addTerminalWidgets(): void {
        if (!this.terminalGrid || !this.terminalScreen) return;

        // Widget de status
        this.uiComponents.statusBox = this.terminalGrid.set(0, 0, 3, 12, contrib.donut, {
            label: ' Terminal Status ',
            radius: 8,
            arcWidth: 3,
            data: [
                { label: 'Success', percent: 0, color: ['green'] },
                { label: 'Failed', percent: 0, color: ['red'] },
                { label: 'Pending', percent: 0, color: ['yellow'] }
            ]
        });

        // Widget de execuções recentes
        this.uiComponents.orderTable = this.terminalGrid.set(3, 0, 4, 12, contrib.table, {
            keys: true,
            fg: 'white',
            selectedFg: 'white',
            selectedBg: 'blue',
            label: ' Recent Executions ',
            columnSpacing: 2,
            columnWidth: [12, 8, 8, 10, 10]
        });

        // Widget de métricas
        this.uiComponents.metricsBox = this.terminalGrid.set(7, 0, 3, 12, blessed.box, {
            label: ' Session Metrics ',
            border: { type: 'line' },
            style: {
                border: { fg: 'cyan' },
                label: { fg: 'white' }
            },
            content: 'Loading...'
        });

        // Widget de comando
        this.uiComponents.commandBox = this.terminalGrid.set(10, 0, 2, 12, blessed.textbox, {
            label: ' Command Input ',
            border: { type: 'line' },
            style: {
                border: { fg: 'magenta' },
                label: { fg: 'white' }
            },
            inputOnFocus: true,
            keys: true
        });

        // Configura handler de comandos no terminal
        this.uiComponents.commandBox.on('submit', (text: string) => {
            this.handleTerminalCommand(text);
            this.uiComponents.commandBox.clearValue();
            this.terminalScreen?.render();
        });
    }

    /**
     * Atualiza widgets do terminal
     */
    private async updateTerminalWidgets(): Promise<void> {
        if (!this.terminalScreen) return;

        try {
            // Atualiza status
            const successRate = this.orderCounters.total > 0
                ? (this.orderCounters.successful / this.orderCounters.total) * 100
                : 0;
            const failRate = this.orderCounters.total > 0
                ? (this.orderCounters.failed / this.orderCounters.total) * 100
                : 0;
            const pendingRate = 100 - successRate - failRate;

            this.uiComponents.statusBox.setData([
                { label: 'Success', percent: successRate, color: ['green'] },
                { label: 'Failed', percent: failRate, color: ['red'] },
                { label: 'Pending', percent: pendingRate, color: ['yellow'] }
            ]);

            // Atualiza tabela de execuções
            const recentOrders = this.orderHistory.slice(-10).reverse();
            const tableData = [
                ['Time', 'Symbol', 'Side', 'Amount', 'Status', 'Price']
            ];

            recentOrders.forEach(order => {
                tableData.push([
                    format(order.timestamp, 'HH:mm:ss'),
                    order.symbol,
                    order.side,
                    order.amount.toString(),
                    order.status,
                    order.executionResult?.averagePrice?.toFixed(2) || 'N/A'
                ]);
            });

            this.uiComponents.orderTable.setData(tableData);

            // Atualiza métricas
            const metricsContent =
                `Total Orders: ${this.orderCounters.total}\n` +
                `Success Rate: ${(this.sessionMetrics.successRate * 100).toFixed(1)}%\n` +
                `Avg Exec Time: ${this.sessionMetrics.avgExecutionTime.toFixed(0)}ms\n` +
                `Total Volume: ${this.formatCurrency(this.sessionMetrics.totalVolume)}\n` +
                `Circuit Breaker: ${this.circuitBreakerState}\n` +
                `Active Connections: ${this.activeConnections.filter(c => c.connected).length}`;

            this.uiComponents.metricsBox.setContent(metricsContent);

            this.terminalScreen.render();
        } catch (error) {
            // Ignora erros de atualização
        }
    }

    /**
     * Configura teclas de atalho do terminal
     */
    private setupTerminalKeybindings(): void {
        if (!this.terminalScreen) return;

        this.terminalScreen.key(['escape', 'q', 'C-c'], () => {
            this.terminalScreen?.destroy();
            this.terminalScreen = null;
            this.terminalGrid = null;
            this.uiComponents = {};
            this.log('Terminal interface closed', 'info');
        });

        this.terminalScreen.key(['C-r'], () => {
            this.updateTerminalWidgets();
        });

        this.terminalScreen.key(['C-l'], () => {
            this.clearTerminal();
        });

        this.terminalScreen.key(['C-h'], () => {
            this.showTerminalHelp();
        });
    }

    /**
     * Limpa terminal
     */
    private clearTerminal(): void {
        if (this.terminalScreen) {
            this.terminalScreen.clearRegion(0, 0, this.terminalScreen.width, this.terminalScreen.height);
            this.terminalScreen.render();
        }
    }

    /**
     * Mostra ajuda no terminal
     */
    private showTerminalHelp(): void {
        const helpBox = blessed.box({
            top: 'center',
            left: 'center',
            width: '80%',
            height: '80%',
            content: [
                'LEXTRADER Command Terminal - Help',
                '',
                'Commands:',
                '  buy <symbol> <amount> [price]  - Buy order',
                '  sell <symbol> <amount> [price] - Sell order',
                '  status                         - Show terminal status',
                '  history                        - Show order history',
                '  metrics                        - Show session metrics',
                '  clear                          - Clear terminal',
                '  help                           - Show this help',
                '  exit                           - Exit terminal',
                '',
                'Shortcuts:',
                '  Ctrl+R - Refresh',
                '  Ctrl+L - Clear',
                '  Ctrl+H - Help',
                '  Esc/Q  - Exit',
                '',
                'Press any key to continue...'
            ].join('\n'),
            border: { type: 'line' },
            style: {
                border: { fg: 'cyan' },
                content: { fg: 'white' }
            }
        });

        if (this.terminalScreen) {
            this.terminalScreen.append(helpBox);
            helpBox.focus();

            helpBox.on('keypress', () => {
                this.terminalScreen?.remove(helpBox);
                this.terminalScreen?.render();
            });

            this.terminalScreen.render();
        }
    }

    /**
     * Handler de comandos do terminal
     */
    private async handleTerminalCommand(command: string): Promise<void> {
        const parts = command.trim().split(' ');
        const cmd = parts[0].toLowerCase();
        const args = parts.slice(1);

        try {
            switch (cmd) {
                case 'buy':
                case 'sell':
                    if (args.length < 2) {
                        this.showTerminalMessage('Usage: <buy|sell> <symbol> <amount> [price]', 'error');
                        return;
                    }

                    const order: OrderRequest = {
                        symbol: args[0].toUpperCase(),
                        side: cmd.toUpperCase() as 'BUY' | 'SELL',
                        amount: parseFloat(args[1]),
                        type: args[2] ? 'LIMIT' : 'MARKET',
                        price: args[2] ? parseFloat(args[2]) : undefined
                    };

                    this.showTerminalMessage(`Processing ${cmd.toUpperCase()} order for ${order.symbol}...`, 'info');

                    const result = await this.execute(order);

                    if (result.success) {
                        this.showTerminalMessage(`Order ${result.orderId} executed successfully`, 'success');
                    } else {
                        this.showTerminalMessage(`Order failed: ${result.error}`, 'error');
                    }
                    break;

                case 'status':
                    this.showTerminalStatus();
                    break;

                case 'history':
                    this.showTerminalHistory(args[0] || '10');
                    break;

                case 'metrics':
                    this.showTerminalMetrics();
                    break;

                case 'clear':
                    this.clearTerminal();
                    break;

                case 'help':
                    this.showTerminalHelp();
                    break;

                case 'exit':
                    if (this.terminalScreen) {
                        this.terminalScreen.destroy();
                        this.terminalScreen = null;
                    }
                    break;

                default:
                    this.showTerminalMessage(`Unknown command: ${cmd}`, 'warning');
                    break;
            }
        } catch (error) {
            this.showTerminalMessage(`Command error: ${error.message}`, 'error');
        }
    }

    /**
     * Mostra mensagem no terminal
     */
    private showTerminalMessage(message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info'): void {
        if (!this.terminalScreen) return;

        const colors = {
            info: 'blue',
            success: 'green',
            warning: 'yellow',
            error: 'red'
        };

        const messageBox = blessed.box({
            top: 'center',
            left: 'center',
            width: '50%',
            height: 5,
            content: message,
            border: { type: 'line' },
            style: {
                border: { fg: colors[type] },
                content: { fg: 'white' }
            }
        });

        this.terminalScreen.append(messageBox);
        this.terminalScreen.render();

        // Remove após 3 segundos
        setTimeout(() => {
            this.terminalScreen?.remove(messageBox);
            this.terminalScreen?.render();
        }, 3000);
    }

    /**
     * Mostra status no terminal
     */
    private showTerminalStatus(): void {
        if (!this.terminalScreen) return;

        const statusContent =
            `Command Terminal Status\n\n` +
            `Mode: ${this.config.mode}\n` +
            `Circuit Breaker: ${this.circuitBreakerState}\n` +
            `Active Orders: ${this.pendingOrders.length}\n` +
            `Queue Length: ${this.executionQueue.length}\n` +
            `Connected Exchanges: ${this.activeConnections.filter(c => c.connected).length}\n` +
            `Session Uptime: ${formatDistanceToNow(this.sessionMetrics.startTime)}`;

        const statusBox = blessed.box({
            top: 'center',
            left: 'center',
            width: '60%',
            height: 12,
            content: statusContent,
            border: { type: 'line' },
            style: {
                border: { fg: 'cyan' },
                content: { fg: 'white' }
            }
        });

        this.terminalScreen.append(statusBox);
        statusBox.focus();

        statusBox.on('keypress', () => {
            this.terminalScreen?.remove(statusBox);
            this.terminalScreen?.render();
        });

        this.terminalScreen.render();
    }

    /**
     * Mostra histórico no terminal
     */
    private showTerminalHistory(count: string): void {
        const limit = parseInt(count) || 10;
        const recentOrders = this.orderHistory.slice(-limit).reverse();

        let historyContent = `Last ${limit} Orders\n\n`;

        if (recentOrders.length === 0) {
            historyContent += 'No orders found';
        } else {
            recentOrders.forEach((order, i) => {
                historyContent +=
                    `${i + 1}. ${format(order.timestamp, 'HH:mm:ss')} ` +
                    `${order.symbol} ${order.side} ${order.amount} ` +
                    `@ ${order.executionResult?.averagePrice?.toFixed(2) || 'N/A'} ` +
                    `[${order.status}]\n`;
            });
        }

        const historyBox = blessed.box({
            top: 'center',
            left: 'center',
            width: '80%',
            height: Math.min(limit + 4, 20),
            content: historyContent,
            border: { type: 'line' },
            style: {
                border: { fg: 'magenta' },
                content: { fg: 'white' }
            },
            scrollable: true,
            alwaysScroll: true,
            scrollbar: {
                ch: ' ',
                style: {
                    bg: 'blue'
                }
            }
        });

        if (this.terminalScreen) {
            this.terminalScreen.append(historyBox);
            historyBox.focus();

            historyBox.on('keypress', () => {
                this.terminalScreen?.remove(historyBox);
                this.terminalScreen?.render();
            });

            this.terminalScreen.render();
        }
    }

    /**
     * Mostra métricas no terminal
     */
    private showTerminalMetrics(): void {
        const metricsContent =
            `Session Metrics\n\n` +
            `Total Orders: ${this.orderCounters.total}\n` +
            `Successful: ${this.orderCounters.successful}\n` +
            `Failed: ${this.orderCounters.failed}\n` +
            `Success Rate: ${(this.sessionMetrics.successRate * 100).toFixed(1)}%\n` +
            `Total Volume: ${this.formatCurrency(this.sessionMetrics.totalVolume)}\n` +
            `Total Fees: ${this.formatCurrency(this.sessionMetrics.totalFees)}\n` +
            `Avg Execution Time: ${this.sessionMetrics.avgExecutionTime.toFixed(0)}ms\n` +
            `Max Drawdown: ${(this.sessionMetrics.maxDrawdown * 100).toFixed(2)}%\n` +
            `Sharpe Ratio: ${this.sessionMetrics.sharpeRatio.toFixed(2)}\n` +
            `Session Duration: ${formatDistanceToNow(this.sessionMetrics.startTime)}`;

        const metricsBox = blessed.box({
            top: 'center',
            left: 'center',
            width: '60%',
            height: 16,
            content: metricsContent,
            border: { type: 'line' },
            style: {
                border: { fg: 'green' },
                content: { fg: 'white' }
            }
        });

        if (this.terminalScreen) {
            this.terminalScreen.append(metricsBox);
            metricsBox.focus();

            metricsBox.on('keypress', () => {
                this.terminalScreen?.remove(metricsBox);
                this.terminalScreen?.render();
            });

            this.terminalScreen.render();
        }
    }

    /**
     * Configura handlers de eventos
     */
    private setupEventHandlers(): void {
        // Eventos do execution engine
        this.executionEngine.on('orderUpdate', (update) => {
            this.emit('orderUpdate', update);
        });

        this.executionEngine.on('fill', (fill) => {
            this.emit('fill', fill);
        });

        this.executionEngine.on('error', (error) => {
            this.log(`Execution engine error: ${error.message}`, 'error');
        });

        // Eventos do risk manager
        this.riskManager.on('limitExceeded', (limit) => {
            this.emit('riskLimitExceeded', limit);
        });

        // Eventos do market data
        this.marketData.on('priceUpdate', (update) => {
            this.emit('priceUpdate', update);
        });
    }

    /**
     * Utilitários
     */
    private log(message: string, level: 'info' | 'success' | 'warning' | 'error' = 'info'): void {
        const timestamp = chalk.gray(`[${format(new Date(), 'HH:mm:ss')}]`);
        const levelMap = {
            info: { icon: 'ℹ️', color: 'cyan' },
            success: { icon: '✅', color: 'green' },
            warning: { icon: '⚠️', color: 'yellow' },
            error: { icon: '❌', color: 'red' }
        };

        const { icon, color } = levelMap[level];
        console.log(`${timestamp} ${icon} ${chalk[color](message)}`);
        this.emit('log', { level, message, timestamp: new Date() });
    }

    private formatCurrency(value: number): string {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }

    private chunkArray<T>(array: T[], size: number): T[][] {
        const chunks: T[][] = [];
        for (let i = 0; i < array.length; i += size) {
            chunks.push(array.slice(i, i + size));
        }
        return chunks;
    }

    private getRoutingCacheKey(order: OrderRequest): string {
        return `${order.symbol}_${order.side}_${order.type}_${order.amount}`;
    }

    private cleanSmartOrderCache(): void {
        const now = Date.now();
        for (const [key, value] of this.smartOrderCache.entries()) {
            if (now - value.timestamp > 30000) { // 30 segundos
                this.smartOrderCache.delete(key);
            }
        }
    }

    private getExecutionStrategy(order: OrderRequest, routing: RoutingResult): string {
        if (order.amount > routing.estimatedSlippage * 100) { // Alta slippage estimada
            return 'TWAP';
        }
        return 'IMMEDIATE';
    }

    private calculateVolumeSlices(volumeData: any, orderCount: number): any[] {
        // Implementação simplificada
        return Array.from({ length: orderCount }, (_, i) => ({
            percentage: 1 / orderCount,
            duration: 1 // segundo
        }));
    }

    private async getVolumeDiscount(exchange: string): Promise<number> {
        // Implementação simplificada
        return 0.2; // 20% de desconto
    }

    /**
     * Métodos públicos adicionais
     */

    getOrderHistory(limit: number = 100): OrderRecord[] {
        return this.orderHistory.slice(-limit);
    }

    getSessionMetrics(): SessionMetrics {
        return { ...this.sessionMetrics };
    }

    getActiveConnections(): ExchangeConnection[] {
        return [...this.activeConnections];
    }

    getCircuitBreakerState(): CircuitBreakerState {
        return this.circuitBreakerState;
    }

    resetSession(): void {
        this.orderHistory = [];
        this.pendingOrders = [];
        this.executionQueue = [];
        this.orderCounters = {
            total: 0,
            successful: 0,
            failed: 0,
            pending: 0,
            cancelled: 0,
            partial: 0
        };
        this.sessionMetrics = {
            startTime: new Date(),
            totalVolume: 0,
            totalFees: 0,
            avgExecutionTime: 0,
            successRate: 0,
            maxDrawdown: 0,
            sharpeRatio: 0
        };
        this.circuitBreakerState = 'CLOSED';
        this.smartOrderCache.clear();

        this.log('Session reset', 'info');
        this.emit('sessionReset');
    }

    async shutdown(): Promise<void> {
        this.log('Shutting down Command Terminal...', 'info');

        // Cancela ordens pendentes
        for (const order of this.pendingOrders) {
            try {
                await this.executionEngine.cancelOrder(order.orderId, order.exchange);
            } catch (error) {
                this.log(`Failed to cancel order ${order.orderId}: ${error.message}`, 'warning');
            }
        }

        // Fecha conexões
        for (const connection of this.activeConnections) {
            if (connection.connected) {
                await this.executionEngine.disconnect(connection.exchange);
            }
        }

        // Fecha terminal
        if (this.terminalScreen) {
            this.terminalScreen.destroy();
            this.terminalScreen = null;
        }

        this.log('Command Terminal shutdown complete', 'success');
        this.emit('shutdown');
    }
}

// Interfaces e Tipos

interface OrderRequest {
    symbol: string;
    side: 'BUY' | 'SELL';
    amount: number;
    type?: 'MARKET' | 'LIMIT' | 'STOP' | 'STOP_LIMIT';
    price?: number;
    stopPrice?: number;
    leverage?: number;
    hidden?: boolean;
    postOnly?: boolean;
    timeInForce?: 'GTC' | 'IOC' | 'FOK';
    clientOrderId?: string;
}

interface ExecutionOptions {
    strategy?: 'IMMEDIATE' | 'TWAP' | 'VWAP' | 'ICEBERG';
    useAI?: boolean;
    skipConfirmation?: boolean;
    twapDuration?: number;
    twapSlices?: number;
    vwapPeriod?: string;
    icebergPeak?: number;
    maxConcurrent?: number;
    executionMode?: 'SEQUENTIAL' | 'PARALLEL' | 'TWAP' | 'VWAP';
}

interface BatchExecutionOptions extends ExecutionOptions {
    executionMode?: 'SEQUENTIAL' | 'PARALLEL' | 'TWAP' | 'VWAP';
    maxConcurrent?: number;
}

interface OrderExecutionResult {
    success: boolean;
    orderId: string;
    executionResult?: ExecutionResult;
    error?: string;
    timestamp: Date;
    metrics?: OrderMetrics | null;
}

interface BatchExecutionResult {
    batchId: string;
    success: boolean;
    totalOrders: number;
    successfulOrders: number;
    failedOrders: number;
    results: OrderExecutionResult[];
    errors: BatchError[];
    executionTime: number;
    averageExecutionTime: number;
    timestamp: Date;
}

interface BatchError {
    orderIndex: number;
    error: string;
    order: OrderRequest | null;
}

interface ValidationResult {
    valid: boolean;
    errors: string[];
    warnings: string[];
    timestamp: Date;
}

interface RiskAnalysis {
    approved: boolean;
    reasons: string[];
    riskScore: number;
    riskFactors: RiskFactor[];
    timestamp: Date;
}

interface RiskFactor {
    factor: string;
    score: number;
    details: string;
}

interface RoutingResult {
    exchange: string;
    price: number;
    estimatedFees: number;
    estimatedSlippage: number;
    routeScore: number;
    alternatives: RoutingAlternative[];
    aiPrediction?: AIPrediction | null;
}

interface RoutingAlternative {
    exchange: string;
    price: number;
    fees: number;
    score: number;
}

interface AIPrediction {
    signal: string;
    confidence: number;
    probabilities: { [key: string]: number };
    uncertainty?: number;
    recommendation: string;
}

interface ExecutionResult {
    success: boolean;
    executedPrice: number;
    executedAmount: number;
    fees: number;
    orderId: string;
    exchangeOrderId: string;
    timestamp: Date;
    fills: Fill[];
    averagePrice: number;
    strategy?: string;
}

interface Fill {
    price: number;
    amount: number;
    fee: number;
    timestamp: Date;
    exchangeOrderId: string;
}

interface OrderRecord extends OrderRequest {
    orderId: string;
    executionResult: ExecutionResult;
    status: 'PENDING' | 'FILLED' | 'PARTIAL' | 'CANCELLED' | 'FAILED';
    timestamp: Date;
    metrics?: OrderMetrics;
}

interface OrderMetrics {
    orderId: string;
    executionTime: number;
    fillRate: number;
    slippage: number;
    costPercentage: number;
    latency: number;
    queueTime: number;
    exchangeLatency: number;
}

interface PendingOrder {
    orderId: string;
    exchange: string;
    symbol: string;
    side: string;
    amount: number;
    timestamp: Date;
}

interface ExecutionQueueItem {
    orderId: string;
    executionId: string;
    order: OrderRequest;
    routing: RoutingResult;
    status: 'PENDING' | 'EXECUTING' | 'COMPLETED' | 'FAILED';
    timestamp: Date;
    executionTime?: number;
    result?: ExecutionResult;
    error?: string;
}

interface ExchangeConnection {
    exchange: string;
    connected: boolean;
    latency: number;
    lastChecked: Date;
}

interface OrderCounters {
    total: number;
    successful: number;
    failed: number;
    pending: number;
    cancelled: number;
    partial: number;
}

interface SessionMetrics {
    startTime: Date;
    totalVolume: number;
    totalFees: number;
    avgExecutionTime: number;
    successRate: number;
    maxDrawdown: number;
    sharpeRatio: number;
}

type CircuitBreakerState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

interface SmartOrderCache {
    timestamp: number;
    result: RoutingResult;
}

type SmartOrderCacheMap = Map<string, SmartOrderCache>;

interface TerminalUIComponents {
    statusBox?: any;
    orderTable?: any;
    metricsBox?: any;
    commandBox?: any;
}

export default CommandTerminal;