
import { OracleConsensus, OracleSignal, OracleSourceType } from "../types";

class DataOracle {
    async getTradingViewSignal(symbol: string): Promise<OracleSignal> {
        const score = Math.random() * 100;
        let signal: 'BUY' | 'SELL' | 'NEUTRAL' = 'NEUTRAL';
        if (score > 60) signal = 'BUY';
        if (score < 40) signal = 'SELL';

        return {
            source: 'TRADINGVIEW',
            signal,
            score,
            metadata: `Oscillators: ${signal === 'BUY' ? 'Strong Buy' : signal} | MA: Mixed`,
            latency: 120
        };
    }

    async getYFinanceData(symbol: string): Promise<OracleSignal> {
        const spyCorrelation = Math.random(); 
        const dxyTrend = Math.random() > 0.5 ? 'UP' : 'DOWN';
        let signal: 'BUY' | 'SELL' | 'NEUTRAL' = 'NEUTRAL';
        if (dxyTrend === 'DOWN' && spyCorrelation > 0.5) signal = 'BUY';
        else if (dxyTrend === 'UP') signal = 'SELL';

        return {
            source: 'YFINANCE',
            signal,
            score: Math.random() * 100,
            metadata: `SP500 Corr: ${(spyCorrelation*100).toFixed(0)}% | DXY: ${dxyTrend}`,
            latency: 450
        };
    }

    async getGlassnodeMetrics(symbol: string): Promise<OracleSignal> {
        const nupl = Math.random(); 
        const exchangeFlow = Math.random() > 0.5 ? 'OUTFLOW' : 'INFLOW'; 
        let signal: 'BUY' | 'SELL' | 'NEUTRAL' = 'NEUTRAL';
        if (nupl < 0.3) signal = 'BUY'; 
        if (nupl > 0.7) signal = 'SELL'; 
        if (exchangeFlow === 'OUTFLOW' && signal !== 'SELL') signal = 'BUY';

        return {
            source: 'GLASSNODE',
            signal,
            score: nupl * 100,
            metadata: `NUPL: ${nupl.toFixed(2)} | NetFlow: ${exchangeFlow}`,
            latency: 800
        };
    }

    async getSantimentData(symbol: string): Promise<OracleSignal> {
        const socialVolume = Math.floor(Math.random() * 10000);
        const sentimentScore = (Math.random() * 4) - 2; 
        let signal: 'BUY' | 'SELL' | 'NEUTRAL' = 'NEUTRAL';
        if (sentimentScore > 1) signal = 'SELL'; 
        if (sentimentScore < -1) signal = 'BUY'; 

        return {
            source: 'SANTIMENT',
            signal,
            score: 50 + (sentimentScore * 25),
            metadata: `Social Vol: ${socialVolume} | Sentiment: ${sentimentScore.toFixed(2)}`,
            latency: 600
        };
    }

    async getCoinglassData(symbol: string): Promise<OracleSignal> {
        const lsRatio = 0.5 + Math.random(); 
        const fundingRate = (Math.random() * 0.04) - 0.02; 
        let signal: 'BUY' | 'SELL' | 'NEUTRAL' = 'NEUTRAL';
        if (lsRatio > 1.2) signal = 'SELL'; 
        if (fundingRate < -0.01) signal = 'BUY'; 

        return {
            source: 'COINGLASS',
            signal,
            score: 50,
            metadata: `L/S Ratio: ${lsRatio.toFixed(2)} | Funding: ${fundingRate.toFixed(4)}%`,
            latency: 300
        };
    }

    async getIntoTheBlockData(symbol: string): Promise<OracleSignal> {
        const inMoney = Math.random() * 100;
        let signal: 'BUY' | 'SELL' | 'NEUTRAL' = 'NEUTRAL';
        if (inMoney > 90) signal = 'SELL'; 
        if (inMoney < 40) signal = 'BUY'; 

        return {
            source: 'INTOTHEBLOCK',
            signal,
            score: inMoney,
            metadata: `In Money: ${inMoney.toFixed(0)}% | Whales: Stable`,
            latency: 550
        };
    }

    async getMessariData(symbol: string): Promise<OracleSignal> {
        const realVolProfile = Math.random();
        let signal: 'BUY' | 'SELL' | 'NEUTRAL' = 'NEUTRAL';
        if (realVolProfile > 0.8) signal = 'BUY'; 

        return {
            source: 'MESSARI',
            signal,
            score: realVolProfile * 100,
            metadata: `Real Vol: ${(realVolProfile*100).toFixed(0)}% | Dev Activity: High`,
            latency: 700
        };
    }

    async getMarketConsensus(symbol: string = 'BTC/USDT'): Promise<OracleConsensus> {
        const signals = await Promise.all([
            this.getTradingViewSignal(symbol),
            this.getYFinanceData(symbol),
            this.getGlassnodeMetrics(symbol),
            this.getSantimentData(symbol),
            this.getCoinglassData(symbol),
            this.getIntoTheBlockData(symbol),
            this.getMessariData(symbol)
        ]);

        let bullishCount = 0;
        let bearishCount = 0;
        let totalScore = 0;

        signals.forEach(s => {
            if (s.signal === 'BUY') bullishCount++;
            if (s.signal === 'SELL') bearishCount++;
            totalScore += s.signal === 'BUY' ? s.score : s.signal === 'SELL' ? (100 - s.score) : 50;
        });

        const overallScore = totalScore / signals.length;
        
        const primaryDriver = signals.reduce((prev, current) => {
            const prevDev = Math.abs(prev.score - 50);
            const currDev = Math.abs(current.score - 50);
            return currDev > prevDev ? current : prev;
        }).source;

        return {
            overallScore,
            bullishCount,
            bearishCount,
            primaryDriver,
            signals
        };
    }
}

export const oracleService = new DataOracle();
