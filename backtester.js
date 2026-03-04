const { SMA, EMA, RSI, MACD } = require('technicalindicators');
const math = require('mathjs');

class Backtester {
    constructor(strategy, config = {}) {
        this.strategy = strategy;
        this.config = {
            initialCapital: config.initialCapital || 10000,
            commission: config.commission || 0.001, // 0.1%
            slippage: config.slippage || 0.0005, // 0.05%
            startDate: config.startDate,
            endDate: config.endDate,
            timeframe: config.timeframe || '1d',
            ...config
        };

        this.results = null;
        this.trades = [];
        this.equityCurve = [];
        this.metrics = {};
    }

    async run(historicalData) {
        console.log('🚀 Iniciando backtest...');

        try {
            // Preparar dados
            const preparedData = this.prepareData(historicalData);

            // Executar estratégia
            const results = await this.executeStrategy(preparedData);

            // Calcular métricas
            this.calculateMetrics(results);

            // Gerar relatório
            this.generateReport();

            console.log('✅ Backtest concluído!');
            return this.results;

        } catch (error) {
            console.error('Erro no backtest:', error);
            throw error;
        }
    }

    prepareData(historicalData) {
        console.log('Preparando dados...');

        const data = {
            timestamps: [],
            opens: [],
            highs: [],
            lows: [],
            closes: [],
            volumes: []
        };

        // Ordenar por timestamp
        historicalData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        // Filtrar por período
        let filteredData = historicalData;
        if (this.config.startDate || this.config.endDate) {
            filteredData = historicalData.filter(item => {
                const date = new Date(item.timestamp);
                const startOk = !this.config.startDate || date >= new Date(this.config.startDate);
                const endOk = !this.config.endDate || date <= new Date(this.config.endDate);
                return startOk && endOk;
            });
        }

        // Extrair arrays
        filteredData.forEach(item => {
            data.timestamps.push(new Date(item.timestamp));
            data.opens.push(item.open);
            data.highs.push(item.high);
            data.lows.push(item.low);
            data.closes.push(item.close);
            data.volumes.push(item.volume || 0);
        });

        console.log(`Dados preparados: ${data.timestamps.length} períodos`);
        return data;
    }

    async executeStrategy(data) {
        console.log('Executando estratégia...');

        const results = {
            trades: [],
            equity: [this.config.initialCapital],
            maxDrawdown: 0,
            sharpeRatio: 0,
            totalReturn: 0
        };

        let capital = this.config.initialCapital;
        let position = null;
        let equityPeak = capital;

        // Calcular indicadores
        const indicators = this.calculateIndicators(data);

        // Executar em cada ponto de dados
        for (let i = 50; i < data.closes.length; i++) { // Começar depois de ter dados suficientes
            const currentData = {
                timestamp: data.timestamps[i],
                open: data.opens[i],
                high: data.highs[i],
                low: data.lows[i],
                close: data.closes[i],
                volume: data.volumes[i],
                indicators: this.getCurrentIndicators(indicators, i)
            };

            // Obter sinal da estratégia
            const signal = await this.strategy.getSignal(currentData, position);

            // Executar trade se houver sinal
            if (signal && signal.action !== 'HOLD') {
                const tradeResult = this.executeTrade(
                    signal,
                    currentData,
                    capital,
                    position,
                    i === data.closes.length - 1 // última barra?
                );

                if (tradeResult) {
                    results.trades.push(tradeResult);
                    capital = tradeResult.capitalAfter;
                    position = tradeResult.position;

                    // Atualizar curva de equity
                    results.equity.push(capital);

                    // Atualizar drawdown
                    if (capital > equityPeak) {
                        equityPeak = capital;
                    }
                    const drawdown = (equityPeak - capital) / equityPeak;
                    results.maxDrawdown = Math.max(results.maxDrawdown, drawdown);
                }
            } else if (position) {
                // Atualizar PnL da posição atual
                const unrealizedPnl = this.calculateUnrealizedPnl(position, currentData.close);
                results.equity[results.equity.length - 1] = capital + unrealizedPnl;
            }
        }

        // Fechar posição aberta no final
        if (position) {
            const closeTrade = this.closePosition(position, data.closes[data.closes.length - 1]);
            results.trades.push(closeTrade);
            capital = closeTrade.capitalAfter;
            results.equity.push(capital);
        }

        results.finalCapital = capital;
        results.totalReturn = (capital - this.config.initialCapital) / this.config.initialCapital;

        this.trades = results.trades;
        this.equityCurve = results.equity;

        return results;
    }

    calculateIndicators(data) {
        const indicators = {};

        // SMA
        indicators.sma20 = SMA.calculate({ period: 20, values: data.closes });
        indicators.sma50 = SMA.calculate({ period: 50, values: data.closes });
        indicators.sma200 = SMA.calculate({ period: 200, values: data.closes });

        // EMA
        indicators.ema12 = EMA.calculate({ period: 12, values: data.closes });
        indicators.ema26 = EMA.calculate({ period: 26, values: data.closes });

        // RSI
        indicators.rsi = RSI.calculate({ period: 14, values: data.closes });

        // MACD
        indicators.macd = MACD.calculate({
            values: data.closes,
            fastPeriod: 12,
            slowPeriod: 26,
            signalPeriod: 9
        });

        // Volume SMA
        if (data.volumes.some(v => v > 0)) {
            indicators.volumeSMA20 = SMA.calculate({ period: 20, values: data.volumes });
        }

        return indicators;
    }

    getCurrentIndicators(indicators, index) {
        const current = {};

        Object.keys(indicators).forEach(key => {
            if (indicators[key] && indicators[key][index]) {
                current[key] = indicators[key][index];
            }
        });

        return current;
    }

    executeTrade(signal, data, capital, currentPosition, isLastBar = false) {
        const price = data.close;
        let adjustedPrice = price;

        // Aplicar slippage
        if (signal.action === 'BUY') {
            adjustedPrice = price * (1 + this.config.slippage);
        } else if (signal.action === 'SELL') {
            adjustedPrice = price * (1 - this.config.slippage);
        }

        // Fechar posição existente se necessário
        let tradeResult = null;

        if (currentPosition) {
            // Fechar posição oposta ou se for o último candle
            if (currentPosition.side !== signal.action || isLastBar) {
                tradeResult = this.closePosition(currentPosition, adjustedPrice);
                capital = tradeResult.capitalAfter;
            }
        }

        // Abrir nova posição
        if (signal.action !== 'HOLD' && (!currentPosition || currentPosition.side !== signal.action)) {
            const newTrade = this.openPosition(signal, adjustedPrice, capital, data.timestamp);

            if (newTrade) {
                if (tradeResult) {
                    // Combinar resultados
                    tradeResult = {
                        ...tradeResult,
                        nextPosition: newTrade.position,
                        capitalAfter: newTrade.capitalAfter
                    };
                } else {
                    tradeResult = newTrade;
                }
            }
        }

        return tradeResult;
    }

    openPosition(signal, price, capital, timestamp) {
        // Calcular tamanho da posição
        const positionSize = this.calculatePositionSize(capital, signal);

        if (positionSize.quantity <= 0) {
            return null;
        }

        // Verificar se há capital suficiente
        const cost = positionSize.quantity * price;
        const commission = cost * this.config.commission;
        const totalCost = cost + commission;

        if (totalCost > capital) {
            console.warn('Capital insuficiente para abrir posição');
            return null;
        }

        const position = {
            side: signal.action,
            entryPrice: price,
            quantity: positionSize.quantity,
            entryTime: timestamp,
            stopLoss: signal.stopLoss || price * (signal.action === 'BUY' ? 0.98 : 1.02),
            takeProfit: signal.takeProfit || price * (signal.action === 'BUY' ? 1.04 : 0.96),
            metadata: signal.metadata || {}
        };

        const capitalAfter = capital - totalCost;

        return {
            type: 'OPEN',
            timestamp,
            side: signal.action,
            price,
            quantity: positionSize.quantity,
            cost: totalCost,
            commission,
            position,
            capitalBefore: capital,
            capitalAfter
        };
    }

    closePosition(position, price) {
        const value = position.quantity * price;
        const commission = value * this.config.commission;

        let pnl;
        if (position.side === 'BUY') {
            pnl = (price - position.entryPrice) * position.quantity - commission;
        } else {
            pnl = (position.entryPrice - price) * position.quantity - commission;
        }

        const capitalBefore = this.equityCurve[this.equityCurve.length - 1] || this.config.initialCapital;
        const capitalAfter = capitalBefore + pnl;

        const tradeResult = {
            type: 'CLOSE',
            timestamp: new Date(),
            side: position.side === 'BUY' ? 'SELL' : 'BUY',
            price,
            quantity: position.quantity,
            pnl,
            returnPercent: pnl / (position.entryPrice * position.quantity),
            commission,
            position,
            capitalBefore,
            capitalAfter,
            holdingPeriod: (new Date() - new Date(position.entryTime)) / (1000 * 60 * 60 * 24) // dias
        };

        return tradeResult;
    }

    calculateUnrealizedPnl(position, currentPrice) {
        if (position.side === 'BUY') {
            return (currentPrice - position.entryPrice) * position.quantity;
        } else {
            return (position.entryPrice - currentPrice) * position.quantity;
        }
    }

    calculatePositionSize(capital, signal) {
        // Método baseado no risco
        const riskPercent = signal.riskPercent || 0.02; // 2% por trade
        const riskAmount = capital * riskPercent;

        // Distância para stop loss
        const stopDistance = Math.abs(signal.entryPrice - signal.stopLoss);

        if (stopDistance === 0) {
            return { quantity: 0, risk: 0 };
        }

        // Quantidade baseada no risco
        const quantity = riskAmount / stopDistance;

        // Limitar pelo máximo configurado
        const maxPosition = capital * 0.1; // 10% do capital
        const maxQuantity = maxPosition / signal.entryPrice;

        return {
            quantity: Math.min(quantity, maxQuantity),
            risk: riskAmount
        };
    }

    calculateMetrics(results) {
        console.log('Calculando métricas...');

        if (results.trades.length === 0) {
            this.metrics = {
                totalTrades: 0,
                winningTrades: 0,
                losingTrades: 0,
                winRate: 0,
                totalReturn: 0,
                annualizedReturn: 0,
                sharpeRatio: 0,
                maxDrawdown: 0,
                profitFactor: 0,
                averageWin: 0,
                averageLoss: 0,
                largestWin: 0,
                largestLoss: 0,
                averageHoldingPeriod: 0
            };
            return;
        }

        const trades = results.trades.filter(t => t.type === 'CLOSE');

        // Métricas básicas
        const winningTrades = trades.filter(t => t.pnl > 0);
        const losingTrades = trades.filter(t => t.pnl < 0);

        const totalProfit = winningTrades.reduce((sum, t) => sum + t.pnl, 0);
        const totalLoss = Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0));

        // Período do backtest
        const startDate = new Date(results.trades[0].timestamp);
        const endDate = new Date(results.trades[results.trades.length - 1].timestamp);
        const years = (endDate - startDate) / (1000 * 60 * 60 * 24 * 365.25);

        this.metrics = {
            totalTrades: trades.length,
            winningTrades: winningTrades.length,
            losingTrades: losingTrades.length,
            winRate: winningTrades.length / trades.length,

            totalReturn: results.totalReturn,
            annualizedReturn: years > 0 ? Math.pow(1 + results.totalReturn, 1 / years) - 1 : 0,

            sharpeRatio: this.calculateSharpeRatio(trades, years),
            sortinoRatio: this.calculateSortinoRatio(trades, years),

            maxDrawdown: results.maxDrawdown,
            profitFactor: totalLoss > 0 ? totalProfit / totalLoss : Infinity,

            averageWin: winningTrades.length > 0 ? totalProfit / winningTrades.length : 0,
            averageLoss: losingTrades.length > 0 ? totalLoss / losingTrades.length : 0,

            largestWin: winningTrades.length > 0 ? Math.max(...winningTrades.map(t => t.pnl)) : 0,
            largestLoss: losingTrades.length > 0 ? Math.min(...losingTrades.map(t => t.pnl)) : 0,

            averageHoldingPeriod: trades.length > 0 ?
                trades.reduce((sum, t) => sum + t.holdingPeriod, 0) / trades.length : 0,

            expectancy: this.calculateExpectancy(trades),
            kellyCriterion: this.calculateKellyCriterion(trades)
        };
    }

    calculateSharpeRatio(trades, years, riskFreeRate = 0.02) {
        if (trades.length < 2 || years === 0) return 0;

        const returns = trades.map(t => t.returnPercent);
        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const excessReturn = avgReturn - riskFreeRate / 252; // Taxa diária

        const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
        const stdDev = Math.sqrt(variance);

        return stdDev > 0 ? (excessReturn / stdDev) * Math.sqrt(252) : 0;
    }

    calculateSortinoRatio(trades, years, riskFreeRate = 0.02) {
        if (trades.length < 2 || years === 0) return 0;

        const returns = trades.map(t => t.returnPercent);
        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const excessReturn = avgReturn - riskFreeRate / 252;

        const negativeReturns = returns.filter(r => r < 0);
        if (negativeReturns.length === 0) return Infinity;

        const avgNegative = negativeReturns.reduce((a, b) => a + b, 0) / negativeReturns.length;
        const downsideVariance = negativeReturns.reduce((sum, r) => sum + Math.pow(r - avgNegative, 2), 0) / negativeReturns.length;
        const downsideDev = Math.sqrt(downsideVariance);

        return downsideDev > 0 ? (excessReturn / downsideDev) * Math.sqrt(252) : 0;
    }

    calculateExpectancy(trades) {
        const winRate = this.metrics.winRate;
        const avgWin = this.metrics.averageWin;
        const avgLoss = this.metrics.averageLoss;

        return (winRate * avgWin) - ((1 - winRate) * Math.abs(avgLoss));
    }

    calculateKellyCriterion(trades) {
        const winRate = this.metrics.winRate;
        const winLossRatio = this.metrics.averageWin / Math.abs(this.metrics.averageLoss);

        if (winLossRatio <= 0) return 0;

        const kelly = (winRate * winLossRatio - (1 - winRate)) / winLossRatio;
        return Math.max(0, kelly);
    }

    generateReport() {
        this.results = {
            summary: {
                initialCapital: this.config.initialCapital,
                finalCapital: this.equityCurve[this.equityCurve.length - 1] || this.config.initialCapital,
                netProfit: (this.equityCurve[this.equityCurve.length - 1] || this.config.initialCapital) - this.config.initialCapital,
                totalReturn: this.metrics.totalReturn,
                annualizedReturn: this.metrics.annualizedReturn
            },
            metrics: this.metrics,
            trades: this.trades,
            equityCurve: this.equityCurve,
            drawdown: this.calculateDrawdownCurve(),
            monthlyReturns: this.calculateMonthlyReturns(),
            config: this.config
        };
    }

    calculateDrawdownCurve() {
        const drawdowns = [];
        let peak = this.equityCurve[0];

        for (const equity of this.equityCurve) {
            if (equity > peak) {
                peak = equity;
            }
            const drawdown = (peak - equity) / peak;
            drawdowns.push(drawdown);
        }

        return drawdowns;
    }

    calculateMonthlyReturns() {
        const monthly = {};

        this.trades.forEach(trade => {
            if (trade.type === 'CLOSE') {
                const date = new Date(trade.timestamp);
                const monthKey = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`;

                if (!monthly[monthKey]) {
                    monthly[monthKey] = {
                        trades: 0,
                        profit: 0,
                        loss: 0,
                        net: 0
                    };
                }

                monthly[monthKey].trades++;
                monthly[monthKey].net += trade.pnl;

                if (trade.pnl > 0) {
                    monthly[monthKey].profit += trade.pnl;
                } else {
                    monthly[monthKey].loss += Math.abs(trade.pnl);
                }
            }
        });

        return monthly;
    }

    getPerformanceReport() {
        return {
            ...this.results,
            analysis: this.analyzePerformance(),
            recommendations: this.generateTradingRecommendations()
        };
    }

    analyzePerformance() {
        const analysis = {
            strengths: [],
            weaknesses: [],
            opportunities: [],
            threats: []
        };

        // Análise de força
        if (this.metrics.winRate > 0.6) {
            analysis.strengths.push(`Alta taxa de acerto (${(this.metrics.winRate * 100).toFixed(1)}%)`);
        }

        if (this.metrics.profitFactor > 2) {
            analysis.strengths.push(`Excelente profit factor (${this.metrics.profitFactor.toFixed(2)})`);
        }

        if (this.metrics.maxDrawdown < 0.1) {
            analysis.strengths.push(`Baixo drawdown máximo (${(this.metrics.maxDrawdown * 100).toFixed(1)}%)`);
        }

        // Análise de fraquezas
        if (this.metrics.winRate < 0.4) {
            analysis.weaknesses.push(`Baixa taxa de acerto (${(this.metrics.winRate * 100).toFixed(1)}%)`);
        }

        if (this.metrics.averageLoss > Math.abs(this.metrics.averageWin)) {
            analysis.weaknesses.push('Perdas médias maiores que ganhos médios');
        }

        if (this.metrics.maxDrawdown > 0.2) {
            analysis.weaknesses.push(`Drawdown muito alto (${(this.metrics.maxDrawdown * 100).toFixed(1)}%)`);
        }

        // Oportunidades
        if (this.metrics.expectancy > 0) {
            analysis.opportunities.push(`Expectativa positiva (${this.metrics.expectancy.toFixed(4)})`);
        }

        // Ameaças
        if (this.metrics.sharpeRatio < 1) {
            analysis.threats.push(`Baixo Sharpe ratio (${this.metrics.sharpeRatio.toFixed(2)})`);
        }

        return analysis;
    }

    generateTradingRecommendations() {
        const recommendations = [];

        if (this.metrics.winRate < 0.4) {
            recommendations.push('Melhorar filtros de entrada para aumentar taxa de acerto');
        }

        if (this.metrics.averageLoss > Math.abs(this.metrics.averageWin) * 1.5) {
            recommendations.push('Ajustar stop loss para reduzir tamanho das perdas');
        }

        if (this.metrics.maxDrawdown > 0.15) {
            recommendations.push('Implementar gestão de risco mais conservadora');
        }

        if (this.metrics.kellyCriterion > 0.2) {
            recommendations.push(`Pode aumentar tamanho das posições (Kelly: ${(this.metrics.kellyCriterion * 100).toFixed(1)}%)`);
        } else if (this.metrics.kellyCriterion <= 0) {
            recommendations.push('Evitar trading - estratégia não lucrativa');
        }

        return recommendations;
    }

    optimizeParameters(paramRanges) {
        console.log('Otimizando parâmetros...');

        const results = [];

        // Busca em grid simplificada
        for (const param in paramRanges) {
            const values = paramRanges[param];

            for (const value of values) {
                // Atualizar estratégia com novo parâmetro
                this.strategy.updateParam(param, value);

                // Rerun backtest
                const result = this.run(this.historicalData); // Precisa armazenar historicalData

                results.push({
                    param,
                    value,
                    metrics: this.metrics,
                    totalReturn: this.metrics.totalReturn
                });
            }
        }

        // Encontrar melhor combinação
        const bestResult = results.reduce((best, current) => {
            return current.metrics.totalReturn > best.metrics.totalReturn ? current : best;
        });

        console.log('Melhor parâmetro encontrado:', bestResult);
        return bestResult;
    }

    plotResults() {
        // Geração de gráficos simples no console
        console.log('\n📊 CURVA DE EQUITY:');
        console.log('═'.repeat(50));

        const maxEquity = Math.max(...this.equityCurve);
        const minEquity = Math.min(...this.equityCurve);
        const range = maxEquity - minEquity;
        const height = 10;

        for (let h = height; h >= 0; h--) {
            let line = '';
            const threshold = minEquity + (range * h / height);

            this.equityCurve.forEach((equity, i) => {
                if (i % Math.floor(this.equityCurve.length / 50) === 0) {
                    line += equity >= threshold ? '█' : ' ';
                }
            });

            console.log(line);
        }

        console.log('═'.repeat(50));
        console.log(`Início: ${this.config.initialCapital.toFixed(2)} | Fim: ${this.equityCurve[this.equityCurve.length - 1].toFixed(2)}`);
    }
}

// Estratégia de exemplo
class SampleStrategy {
    constructor() {
        this.params = {
            rsiOverbought: 70,
            rsiOversold: 30,
            smaShort: 20,
            smaLong: 50
        };
    }

    async getSignal(data, currentPosition) {
        const { rsi, sma20, sma50 } = data.indicators;

        if (!rsi || !sma20 || !sma50) {
            return { action: 'HOLD' };
        }

        // Sinal de compra
        if (rsi < this.params.rsiOversold && sma20 > sma50) {
            return {
                action: 'BUY',
                entryPrice: data.close,
                stopLoss: data.close * 0.98,
                takeProfit: data.close * 1.04,
                confidence: 0.7,
                metadata: { reason: 'RSI oversold + SMA bullish crossover' }
            };
        }

        // Sinal de venda
        if (rsi > this.params.rsiOverbought && sma20 < sma50) {
            return {
                action: 'SELL',
                entryPrice: data.close,
                stopLoss: data.close * 1.02,
                takeProfit: data.close * 0.96,
                confidence: 0.7,
                metadata: { reason: 'RSI overbought + SMA bearish crossover' }
            };
        }

        return { action: 'HOLD' };
    }

    updateParam(param, value) {
        this.params[param] = value;
    }
}

module.exports = { Backtester, SampleStrategy };