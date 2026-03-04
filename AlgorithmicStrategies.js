/**
 * Algorithmic Strategies Manager
 */
export class StrategyManager {
    constructor() {
        this.activeStrategies = new Set();
    }

    addStrategy(name, logic) {
        this.activeStrategies.add({ name, logic, status: 'ACTIVE' });
        console.log(`📈 Estratégia ${name} integrada ao pool.`);
    }

    getExecutionSignals() {
        return Array.from(this.activeStrategies).map(s => s.name);
    }
}