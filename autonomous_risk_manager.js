/**
 * autonomous_risk_manager.js - Sistema de Gestão de Risco Autônomo AGI
 */
class AnomalyDetector {
    constructor() {
        this.history = [];
        this.threshold = 3.0;
    }

    detectByZScore(metrics) {
        if (this.history.length < 10) return { isAnomaly: false };
        const values = this.history.map(h => h.volatility || 0);
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const std = Math.sqrt(values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length);
        const zscore = Math.abs((metrics.volatility - mean) / (std || 0.001));
        return { isAnomaly: zscore > this.threshold, score: zscore };
    }
}

export { AnomalyDetector };