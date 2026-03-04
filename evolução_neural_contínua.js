/**
 * SISTEMA DE EVOLUÇÃO NEURAL CONTÍNUA EM JAVASCRIPT
 * Motor de Evolução Neural com aprendizado contínuo
 * Melhorias: Web Workers, IndexedDB, Visualização em tempo real, APIs REST
 */

// ============================================================================
// ENUMS E CONSTANTES
// ============================================================================

const EvolutionStrategy = Object.freeze({
    GENETIC_ALGORITHM: 'GENETIC_ALGORITHM',
    GRADIENT_EVOLUTION: 'GRADIENT_EVOLUTION',
    NEUROEVOLUTION: 'NEUROEVOLUTION',
    LAMARCKIAN: 'LAMARCKIAN',
    COEVOLUTION: 'COEVOLUTION',
    SYMBIOTIC: 'SYMBIOTIC',
    QUANTUM_EVOLUTION: 'QUANTUM_EVOLUTION',
    MULTI_OBJECTIVE: 'MULTI_OBJECTIVE'
});

const MutationType = Object.freeze({
    WEIGHT_PERTURBATION: 'WEIGHT_PERTURBATION',
    NODE_ADDITION: 'NODE_ADDITION',
    CONNECTION_ADDITION: 'CONNECTION_ADDITION',
    CONNECTION_REMOVAL: 'CONNECTION_REMOVAL',
    ACTIVATION_MUTATION: 'ACTIVATION_MUTATION',
    TOPOLOGY_MUTATION: 'TOPOLOGY_MUTATION',
    QUANTUM_MUTATION: 'QUANTUM_MUTATION',
    EPIGENETIC: 'EPIGENETIC'
});

const FitnessMetric = Object.freeze({
    PERFORMANCE: 'PERFORMANCE',
    ADAPTABILITY: 'ADAPTABILITY',
    EFFICIENCY: 'EFFICIENCY',
    ROBUSTNESS: 'ROBUSTNESS',
    GENERALIZATION: 'GENERALIZATION',
    INNOVATION: 'INNOVATION',
    ENERGY_EFFICIENCY: 'ENERGY_EFFICIENCY',
    LEARNING_SPEED: 'LEARNING_SPEED'
});

const EvolutionPhase = Object.freeze({
    INITIALIZATION: 'INITIALIZATION',
    EVALUATION: 'EVALUATION',
    SELECTION: 'SELECTION',
    REPRODUCTION: 'REPRODUCTION',
    MUTATION: 'MUTATION',
    INTEGRATION: 'INTEGRATION',
    VALIDATION: 'VALIDATION',
    DEPLOYMENT: 'DEPLOYMENT'
});

// ============================================================================
// UTILITÁRIOS
// ============================================================================

class MathUtils {
    static mean(arr) {
        if (!arr || arr.length === 0) return 0;
        return arr.reduce((a, b) => a + b, 0) / arr.length;
    }

    static median(arr) {
        if (!arr || arr.length === 0) return 0;
        const sorted = [...arr].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
    }

    static std(arr) {
        if (!arr || arr.length < 2) return 0;
        const mean = this.mean(arr);
        const variance = arr.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / arr.length;
        return Math.sqrt(variance);
    }

    static gaussianRandom(mean = 0, std = 1) {
        let u = 0, v = 0;
        while (u === 0) u = Math.random();
        while (v === 0) v = Math.random();
        return mean + std * Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    }

    static percentile(arr, p) {
        if (!arr || arr.length === 0) return 0;
        const sorted = [...arr].sort((a, b) => a - b);
        const index = Math.ceil((p / 100) * sorted.length) - 1;
        return sorted[Math.max(0, index)];
    }

    static linregress(x, y) {
        if (x.length !== y.length || x.length < 2) return { slope: 0, intercept: 0 };
        
        const n = x.length;
        let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
        
        for (let i = 0; i < n; i++) {
            sumX += x[i];
            sumY += y[i];
            sumXY += x[i] * y[i];
            sumX2 += x[i] * x[i];
        }
        
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;
        
        return { slope, intercept };
    }

    static correlation(x, y) {
        if (x.length !== y.length || x.length < 2) return 0;
        
        const n = x.length;
        let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
        
        for (let i = 0; i < n; i++) {
            sumX += x[i];
            sumY += y[i];
            sumXY += x[i] * y[i];
            sumX2 += x[i] * x[i];
            sumY2 += y[i] * y[i];
        }
        
        const numerator = n * sumXY - sumX * sumY;
        const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
        
        return denominator === 0 ? 0 : numerator / denominator;
    }
}

class IDGenerator {
    static generateId(prefix = 'id') {
        return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    static generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
}

class Logger {
    constructor(name = 'NeuralEvolution') {
        this.name = name;
        this.levels = {
            DEBUG: 0,
            INFO: 1,
            WARN: 2,
            ERROR: 3
        };
        this.currentLevel = this.levels.INFO;
    }

    log(level, message, ...args) {
        if (this.levels[level] >= this.currentLevel) {
            const timestamp = new Date().toISOString();
            console.log(`[${timestamp}] [${level}] [${this.name}] ${message}`, ...args);
        }
    }

    debug(message, ...args) {
        this.log('DEBUG', message, ...args);
    }

    info(message, ...args) {
        this.log('INFO', message, ...args);
    }

    warn(message, ...args) {
        this.log('WARN', message, ...args);
    }

    error(message, ...args) {
        this.log('ERROR', message, ...args);
    }
}

// ============================================================================
// ESTRUTURAS DE DADOS AVANÇADAS
// ============================================================================

class NeuralGenome {
    constructor({
        id = IDGenerator.generateId('genome'),
        generation = 0,
        created_at = new Date(),
        node_genes = [],
        connection_genes = [],
        mutation_rate = 0.1,
        crossover_rate = 0.7,
        learning_rate = 0.01,
        parent_ids = [],
        mutation_history = [],
        fitness_scores = {},
        evaluation_count = 0,
        last_evaluated = null,
        metadata = {},
        tags = new Set()
    } = {}) {
        this.id = id;
        this.generation = generation;
        this.created_at = new Date(created_at);
        this.node_genes = node_genes;
        this.connection_genes = connection_genes;
        this.mutation_rate = mutation_rate;
        this.crossover_rate = crossover_rate;
        this.learning_rate = learning_rate;
        this.parent_ids = parent_ids;
        this.mutation_history = mutation_history;
        this.fitness_scores = fitness_scores;
        this.evaluation_count = evaluation_count;
        this.last_evaluated = last_evaluated ? new Date(last_evaluated) : null;
        this.metadata = metadata;
        this.tags = new Set(tags);
    }

    get overall_fitness() {
        if (!this.fitness_scores || Object.keys(this.fitness_scores).length === 0) {
            return 0.0;
        }

        const weights = {
            [FitnessMetric.PERFORMANCE]: 0.35,
            [FitnessMetric.ADAPTABILITY]: 0.25,
            [FitnessMetric.EFFICIENCY]: 0.15,
            [FitnessMetric.ROBUSTNESS]: 0.15,
            [FitnessMetric.GENERALIZATION]: 0.10
        };

        let total = 0.0;
        for (const [metric, weight] of Object.entries(weights)) {
            const score = this.fitness_scores[metric] || 0.0;
            total += score * weight;
        }

        return total;
    }

    get complexity() {
        const nodes = this.node_genes.length;
        const connections = this.connection_genes.length;

        if (nodes > 0 && connections > 0) {
            return Math.log(nodes * connections + 1);
        }
        return 0.0;
    }

    get novelty_score() {
        if (!this.mutation_history || this.mutation_history.length === 0) {
            return 0.0;
        }

        const recent_mutations = this.mutation_history.slice(-10);
        const unique_types = new Set(recent_mutations.map(m => m.type)).size;
        const total_types = Object.keys(MutationType).length;

        return unique_types / total_types;
    }

    add_node_gene(node_type, activation, kwargs = {}) {
        const node_id = `node_${this.node_genes.length + 1}`;

        const node_gene = {
            id: node_id,
            type: node_type,
            activation: activation,
            bias: Math.random() * 2 - 1, // -1 to 1
            created_at: new Date().toISOString(),
            ...kwargs
        };

        this.node_genes.push(node_gene);
        return node_id;
    }

    add_connection_gene(source_id, target_id, weight, enabled = true, innovation_id = null) {
        if (innovation_id === null) {
            innovation_id = `innov_${source_id}_${target_id}_${Date.now()}`;
        }

        const connection_gene = {
            id: innovation_id,
            source: source_id,
            target: target_id,
            weight: weight,
            enabled: enabled,
            created_at: new Date().toISOString()
        };

        this.connection_genes.push(connection_gene);
        return innovation_id;
    }

    record_mutation(mutation_type, details) {
        const mutation_record = {
            type: mutation_type,
            timestamp: new Date().toISOString(),
            generation: this.generation,
            details: details
        };

        this.mutation_history.push(mutation_record);
    }

    toJSON() {
        return {
            id: this.id,
            generation: this.generation,
            created_at: this.created_at.toISOString(),
            node_genes: this.node_genes,
            connection_genes: this.connection_genes,
            mutation_rate: this.mutation_rate,
            crossover_rate: this.crossover_rate,
            learning_rate: this.learning_rate,
            parent_ids: this.parent_ids,
            mutation_history: this.mutation_history,
            fitness_scores: this.fitness_scores,
            evaluation_count: this.evaluation_count,
            last_evaluated: this.last_evaluated ? this.last_evaluated.toISOString() : null,
            metadata: this.metadata,
            tags: Array.from(this.tags)
        };
    }

    static fromJSON(data) {
        return new NeuralGenome({
            ...data,
            created_at: new Date(data.created_at),
            last_evaluated: data.last_evaluated ? new Date(data.last_evaluated) : null,
            tags: new Set(data.tags || [])
        });
    }

    async saveToFile(filename) {
        const data = JSON.stringify(this.toJSON(), null, 2);
        if (typeof window !== 'undefined' && window.showSaveFilePicker) {
            // Browser File System Access API
            try {
                const handle = await window.showSaveFilePicker({
                    suggestedName: filename,
                    types: [{
                        description: 'JSON files',
                        accept: { 'application/json': ['.json'] }
                    }]
                });
                const writable = await handle.createWritable();
                await writable.write(data);
                await writable.close();
                return true;
            } catch (err) {
                console.warn('File System Access API not available:', err);
            }
        }
        
        // Fallback for Node.js or older browsers
        if (typeof process !== 'undefined' && process.versions && process.versions.node) {
            const fs = require('fs');
            fs.writeFileSync(filename, data);
            return true;
        } else {
            // Download as file in browser
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
            return true;
        }
    }

    static async loadFromFile(filename) {
        if (typeof process !== 'undefined' && process.versions && process.versions.node) {
            const fs = require('fs');
            const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
            return NeuralGenome.fromJSON(data);
        } else {
            const response = await fetch(filename);
            const data = await response.json();
            return NeuralGenome.fromJSON(data);
        }
    }
}

class EvolutionaryPopulation {
    constructor({
        id = IDGenerator.generateId('pop'),
        generation = 0,
        created_at = new Date(),
        genomes = {},
        population_size = 100,
        elitism_count = 5,
        selection_pressure = 0.3,
        mutation_rate = 0.1,
        crossover_rate = 0.7,
        fitness_stats = {},
        diversity_score = 0.0,
        convergence_rate = 0.0,
        best_genome_history = [],
        average_fitness_history = [],
        environment_id = null,
        evolutionary_pressure = {}
    } = {}) {
        this.id = id;
        this.generation = generation;
        this.created_at = new Date(created_at);
        this.genomes = genomes;
        this.population_size = population_size;
        this.elitism_count = elitism_count;
        this.selection_pressure = selection_pressure;
        this.mutation_rate = mutation_rate;
        this.crossover_rate = crossover_rate;
        this.fitness_stats = fitness_stats;
        this.diversity_score = diversity_score;
        this.convergence_rate = convergence_rate;
        this.best_genome_history = best_genome_history;
        this.average_fitness_history = average_fitness_history;
        this.environment_id = environment_id;
        this.evolutionary_pressure = evolutionary_pressure;

        // Inicializar população se vazia
        if (Object.keys(this.genomes).length === 0 && this.population_size > 0) {
            this._initializeRandomPopulation();
        }
    }

    _initializeRandomPopulation() {
        for (let i = 0; i < this.population_size; i++) {
            const genome = new NeuralGenome({
                id: `genome_init_${i}`,
                generation: 0,
                mutation_rate: this.mutation_rate,
                crossover_rate: this.crossover_rate
            });

            this._createBasicTopology(genome);
            this.genomes[genome.id] = genome;
        }
    }

    _createBasicTopology(genome) {
        // Adicionar nós de entrada
        const input_nodes = [];
        for (let i = 0; i < 3; i++) {
            const node_id = genome.add_node_gene(
                'input',
                'linear',
                { position: `input_${i}` }
            );
            input_nodes.push(node_id);
        }

        // Adicionar nós ocultos
        const hidden_nodes = [];
        for (let i = 0; i < 5; i++) {
            const node_id = genome.add_node_gene(
                'hidden',
                'relu',
                { layer: 1 }
            );
            hidden_nodes.push(node_id);
        }

        // Adicionar nós de saída
        const output_node = genome.add_node_gene(
            'output',
            'sigmoid',
            { position: 'output' }
        );

        // Criar conexões aleatórias
        for (const input_node of input_nodes) {
            for (const hidden_node of hidden_nodes) {
                if (Math.random() > 0.3) { // 70% de chance de conexão
                    genome.add_connection_gene(
                        input_node,
                        hidden_node,
                        Math.random() * 2 - 1 // -1 to 1
                    );
                }
            }
        }

        for (const hidden_node of hidden_nodes) {
            if (Math.random() > 0.2) { // 80% de chance
                genome.add_connection_gene(
                    hidden_node,
                    output_node,
                    Math.random() * 2 - 1
                );
            }
        }
    }

    get size() {
        return Object.keys(this.genomes).length;
    }

    get best_genome() {
        if (this.size === 0) return null;

        let best = null;
        let bestFitness = -Infinity;

        for (const genome of Object.values(this.genomes)) {
            const fitness = genome.overall_fitness;
            if (fitness > bestFitness) {
                bestFitness = fitness;
                best = genome;
            }
        }

        return best;
    }

    get average_fitness() {
        if (this.size === 0) return 0.0;

        const fitnesses = Object.values(this.genomes).map(g => g.overall_fitness);
        return MathUtils.mean(fitnesses);
    }

    get fitness_std() {
        if (this.size < 2) return 0.0;

        const fitnesses = Object.values(this.genomes).map(g => g.overall_fitness);
        return MathUtils.std(fitnesses);
    }

    updateStatistics() {
        if (this.size === 0) return;

        const fitnesses = Object.values(this.genomes).map(g => g.overall_fitness);

        this.fitness_stats = {
            min: Math.min(...fitnesses),
            max: Math.max(...fitnesses),
            mean: MathUtils.mean(fitnesses),
            median: MathUtils.median(fitnesses),
            std: MathUtils.std(fitnesses),
            q1: MathUtils.percentile(fitnesses, 25),
            q3: MathUtils.percentile(fitnesses, 75)
        };

        this.diversity_score = this._calculateDiversity();
        this.convergence_rate = this._calculateConvergenceRate();
        this.average_fitness_history.push(this.average_fitness);

        if (this.best_genome) {
            this.best_genome_history.push({
                generation: this.generation,
                genome_id: this.best_genome.id,
                fitness: this.best_genome.overall_fitness,
                complexity: this.best_genome.complexity,
                timestamp: new Date().toISOString()
            });
        }
    }

    _calculateDiversity() {
        if (this.size < 2) return 0.0;

        const fitnesses = Object.values(this.genomes).map(g => g.overall_fitness);
        const mean_fitness = MathUtils.mean(fitnesses);

        if (mean_fitness > 0) {
            const cv = this.fitness_stats.std / mean_fitness;
            return Math.min(1.0, cv);
        }
        return 0.0;
    }

    _calculateConvergenceRate() {
        if (this.average_fitness_history.length < 10) return 0.0;

        const recent_history = this.average_fitness_history.slice(-10);
        const x = Array.from({ length: recent_history.length }, (_, i) => i);
        const regression = MathUtils.linregress(x, recent_history);
        
        const max_fitness = Math.max(...recent_history);
        return Math.abs(regression.slope) / (max_fitness + 1e-10);
    }

    evolveGeneration(strategy = EvolutionStrategy.GENETIC_ALGORITHM) {
        // 1. Avaliar fitness (se necessário)
        for (const genome of Object.values(this.genomes)) {
            if (genome.evaluation_count === 0) {
                this._evaluateGenome(genome);
            }
        }

        // 2. Atualizar estatísticas
        this.updateStatistics();

        // 3. Selecionar pais
        const parents = this._selectParents(strategy);

        // 4. Criar nova geração
        const newGenomes = this._createNewGeneration(parents, strategy);

        // 5. Aplicar mutações
        const mutatedGenomes = this._applyMutations(newGenomes, strategy);

        // 6. Atualizar população
        this.genomes = mutatedGenomes;
        this.generation += 1;

        return this;
    }

    _evaluateGenome(genome) {
        // Simulação de avaliação (em implementação real, isso treinaria a rede)
        const base_score = Math.random() * 0.4 + 0.3; // 0.3-0.7
        const complexity_factor = genome.complexity * 0.1;
        const novelty_bonus = genome.novelty_score * 0.2;

        genome.fitness_scores = {
            [FitnessMetric.PERFORMANCE]: base_score + complexity_factor,
            [FitnessMetric.ADAPTABILITY]: Math.random() * 0.4 + 0.4, // 0.4-0.8
            [FitnessMetric.EFFICIENCY]: Math.max(0.1, 0.6 - complexity_factor * 0.2),
            [FitnessMetric.ROBUSTNESS]: Math.random() * 0.4 + 0.5, // 0.5-0.9
            [FitnessMetric.GENERALIZATION]: Math.random() * 0.4 + 0.3 + novelty_bonus, // 0.3-0.7 + bônus
            [FitnessMetric.INNOVATION]: genome.novelty_score,
            [FitnessMetric.LEARNING_SPEED]: Math.random() * 0.4 + 0.4 // 0.4-0.8
        };

        genome.evaluation_count += 1;
        genome.last_evaluated = new Date();
    }

    _selectParents(strategy) {
        const genomesList = Object.values(this.genomes);

        if (strategy === EvolutionStrategy.GENETIC_ALGORITHM) {
            // Seleção por torneio
            const parents = [];
            const tournament_size = Math.max(2, Math.floor(genomesList.length * this.selection_pressure));

            while (parents.length < genomesList.length) {
                const tournament = [];
                const available = [...genomesList];
                
                for (let i = 0; i < Math.min(tournament_size, available.length); i++) {
                    const idx = Math.floor(Math.random() * available.length);
                    tournament.push(available.splice(idx, 1)[0]);
                }

                const winner = tournament.reduce((best, current) => 
                    current.overall_fitness > best.overall_fitness ? current : best
                );
                parents.push(winner);
            }

            return parents;
        } else if (strategy === EvolutionStrategy.NEUROEVOLUTION) {
            // NEAT: seleção por espécies (simplificado)
            const species = this._speciatePopulation(genomesList);
            const parents = [];

            for (const specieGenomes of Object.values(species)) {
                if (specieGenomes.length > 0) {
                    const weights = specieGenomes.map(g => g.overall_fitness + 0.1);
                    const specieParents = this._weightedRandomSelection(specieGenomes, weights, Math.floor(specieGenomes.length / 2));
                    parents.push(...specieParents);
                }
            }

            return parents.length > 0 ? parents : genomesList;
        } else {
            // Seleção aleatória com viés de fitness
            const weights = genomesList.map(g => g.overall_fitness + 0.1);
            return this._weightedRandomSelection(genomesList, weights, genomesList.length);
        }
    }

    _weightedRandomSelection(items, weights, count) {
        const selected = [];
        const totalWeight = weights.reduce((a, b) => a + b, 0);

        for (let i = 0; i < count; i++) {
            let random = Math.random() * totalWeight;
            for (let j = 0; j < items.length; j++) {
                random -= weights[j];
                if (random <= 0) {
                    selected.push(items[j]);
                    break;
                }
            }
        }

        return selected;
    }

    _speciatePopulation(genomes, compatibility_threshold = 3.0) {
        if (genomes.length === 0) return {};

        const species = {};

        for (const genome of genomes) {
            let placed = false;

            for (const [specieId, specieGenomes] of Object.entries(species)) {
                if (specieGenomes.length > 0) {
                    const representative = specieGenomes[0];
                    const distance = this._genomicDistance(genome, representative);

                    if (distance < compatibility_threshold) {
                        specieGenomes.push(genome);
                        placed = true;
                        break;
                    }
                }
            }

            if (!placed) {
                const specieId = `specie_${Object.keys(species).length + 1}`;
                species[specieId] = [genome];
            }
        }

        return species;
    }

    _genomicDistance(genome1, genome2) {
        const excess_genes = Math.abs(genome1.connection_genes.length - genome2.connection_genes.length);
        const disjoint_genes = this._countDisjointGenes(genome1, genome2);
        const weight_diff = this._averageWeightDifference(genome1, genome2);

        const c1 = 1.0, c2 = 1.0, c3 = 0.4;
        const N = Math.max(genome1.connection_genes.length, genome2.connection_genes.length, 1);

        return (c1 * excess_genes / N) + (c2 * disjoint_genes / N) + (c3 * weight_diff);
    }

    _countDisjointGenes(genome1, genome2) {
        const ids1 = new Set(genome1.connection_genes.map(conn => conn.id));
        const ids2 = new Set(genome2.connection_genes.map(conn => conn.id));

        const disjoint = new Set([...ids1].filter(x => !ids2.has(x)));
        disjoint.forEach(x => ids2.has(x) || disjoint.delete(x));

        return disjoint.size;
    }

    _averageWeightDifference(genome1, genome2) {
        const connections1 = {};
        const connections2 = {};

        for (const conn of genome1.connection_genes) connections1[conn.id] = conn;
        for (const conn of genome2.connection_genes) connections2[conn.id] = conn;

        const commonIds = Object.keys(connections1).filter(id => id in connections2);

        if (commonIds.length === 0) return 0.0;

        const weight_diffs = commonIds.map(id => 
            Math.abs(connections1[id].weight - connections2[id].weight)
        );

        return MathUtils.mean(weight_diffs);
    }

    _createNewGeneration(parents, strategy) {
        const newGenomes = {};

        // Preservar elite
        const elite = this._selectElite(parents);
        for (const genome of elite) {
            newGenomes[genome.id] = genome;
        }

        // Preencher restante com crossover/mutação
        while (Object.keys(newGenomes).length < this.population_size) {
            let child;

            if (Math.random() < this.crossover_rate && parents.length >= 2) {
                // Crossover
                const [parent1, parent2] = this._randomSample(parents, 2);
                child = this._crossoverGenomes(parent1, parent2, strategy);
            } else {
                // Clonagem com mutação
                const parent = parents[Math.floor(Math.random() * parents.length)];
                child = this._cloneGenome(parent);
            }

            child.id = `genome_gen${this.generation + 1}_${Object.keys(newGenomes).length}`;
            child.generation = this.generation + 1;
            
            newGenomes[child.id] = child;
        }

        return newGenomes;
    }

    _randomSample(array, n) {
        const shuffled = [...array].sort(() => 0.5 - Math.random());
        return shuffled.slice(0, n);
    }

    _selectElite(genomes) {
        const sorted = [...genomes].sort((a, b) => b.overall_fitness - a.overall_fitness);
        return sorted.slice(0, this.elitism_count);
    }

    _crossoverGenomes(parent1, parent2, strategy) {
        if (strategy === EvolutionStrategy.NEUROEVOLUTION) {
            return this._neatCrossover(parent1, parent2);
        } else {
            return this._uniformCrossover(parent1, parent2);
        }
    }

    _neatCrossover(parent1, parent2) {
        // Assumir parent1 é mais fit
        let fitParent = parent1.overall_fitness >= parent2.overall_fitness ? parent1 : parent2;
        let otherParent = fitParent === parent1 ? parent2 : parent1;

        const child = new NeuralGenome({
            mutation_rate: (parent1.mutation_rate + parent2.mutation_rate) / 2,
            crossover_rate: (parent1.crossover_rate + parent2.crossover_rate) / 2,
            learning_rate: (parent1.learning_rate + parent2.learning_rate) / 2
        });

        const connMap1 = {};
        const connMap2 = {};

        for (const conn of parent1.connection_genes) connMap1[conn.id] = conn;
        for (const conn of parent2.connection_genes) connMap2[conn.id] = conn;

        const allInnovations = new Set([
            ...Object.keys(connMap1),
            ...Object.keys(connMap2)
        ]);

        for (const innovId of allInnovations) {
            if (innovId in connMap1 && innovId in connMap2) {
                // Gene correspondente
                let inheritedGene;
                if (parent1.overall_fitness > parent2.overall_fitness) {
                    inheritedGene = connMap1[innovId];
                } else if (parent2.overall_fitness > parent1.overall_fitness) {
                    inheritedGene = connMap2[innovId];
                } else {
                    inheritedGene = Math.random() > 0.5 ? connMap1[innovId] : connMap2[innovId];
                }

                // Possibilidade de desabilitar gene
                if (!connMap1[innovId].enabled || !connMap2[innovId].enabled) {
                    if (Math.random() < 0.25) {
                        inheritedGene = { ...inheritedGene, enabled: false };
                    }
                }

                child.connection_genes.push({ ...inheritedGene });
            } else if (innovId in connMap1) {
                // Gene excedente/disjunto
                if (parent1.overall_fitness >= parent2.overall_fitness) {
                    child.connection_genes.push({ ...connMap1[innovId] });
                }
            } else {
                // Gene excedente/disjunto do parent2
                if (parent2.overall_fitness > parent1.overall_fitness) {
                    child.connection_genes.push({ ...connMap2[innovId] });
                }
            }
        }

        // Herdar nós (simplificado)
        child.node_genes = [...fitParent.node_genes];

        return child;
    }

    _uniformCrossover(parent1, parent2) {
        const child = new NeuralGenome();

        // Crossover de nós (simplificado)
        const maxNodes = Math.max(parent1.node_genes.length, parent2.node_genes.length);
        for (let i = 0; i < maxNodes; i++) {
            const node1 = parent1.node_genes[i];
            const node2 = parent2.node_genes[i];

            if (!node1 && !node2) continue;
            
            const chosenNode = !node1 ? node2 : 
                              !node2 ? node1 :
                              Math.random() > 0.5 ? node1 : node2;
            
            child.node_genes.push({ ...chosenNode });
        }

        // Crossover de conexões
        const connMap1 = {};
        const connMap2 = {};

        for (const conn of parent1.connection_genes) connMap1[conn.id] = conn;
        for (const conn of parent2.connection_genes) connMap2[conn.id] = conn;

        const allInnovations = new Set([
            ...Object.keys(connMap1),
            ...Object.keys(connMap2)
        ]);

        for (const innovId of allInnovations) {
            if (innovId in connMap1 && innovId in connMap2) {
                const chosenParent = Math.random() > 0.5 ? connMap1 : connMap2;
                child.connection_genes.push({ ...chosenParent[innovId] });
            } else if (innovId in connMap1) {
                child.connection_genes.push({ ...connMap1[innovId] });
            } else {
                child.connection_genes.push({ ...connMap2[innovId] });
            }
        }

        return child;
    }

    _cloneGenome(genome) {
        return NeuralGenome.fromJSON(genome.toJSON());
    }

    _applyMutations(genomes, strategy) {
        const mutatedGenomes = {};

        for (const [genomeId, genome] of Object.entries(genomes)) {
            mutatedGenomes[genomeId] = this._mutateGenome(genome, strategy);
        }

        return mutatedGenomes;
    }

    _mutateGenome(genome, strategy) {
        const mutations_applied = [];

        // Mutação de pesos
        if (Math.random() < genome.mutation_rate * 0.8) {
            this._mutateWeights(genome);
            mutations_applied.push(MutationType.WEIGHT_PERTURBATION);
        }

        // Mutação estrutural
        if (Math.random() < genome.mutation_rate * 0.3) {
            const mutation_type = this._applyStructuralMutation(genome);
            if (mutation_type) {
                mutations_applied.push(mutation_type);
            }
        }

        // Mutação de parâmetros
        if (Math.random() < genome.mutation_rate * 0.2) {
            this._mutateParameters(genome);
            mutations_applied.push(MutationType.EPIGENETIC);
        }

        // Registrar mutações
        for (const mutation_type of mutations_applied) {
            genome.record_mutation(mutation_type, {
                strategy: strategy,
                new_mutation_rate: genome.mutation_rate
            });
        }

        // Meta-mutação: ajustar taxa de mutação
        if (Math.random() < 0.1) {
            genome.mutation_rate *= Math.random() * 0.4 + 0.8; // 0.8-1.2
            genome.mutation_rate = Math.max(0.01, Math.min(0.5, genome.mutation_rate));
        }

        return genome;
    }

    _mutateWeights(genome) {
        for (const connection of genome.connection_genes) {
            if (connection.enabled && Math.random() < 0.8) {
                const perturbation = MathUtils.gaussianRandom(0, 0.1);
                connection.weight += perturbation;
                connection.weight = Math.max(-3.0, Math.min(3.0, connection.weight));
            }
        }
    }

    _applyStructuralMutation(genome) {
        const mutation_types = [
            MutationType.NODE_ADDITION,
            MutationType.CONNECTION_ADDITION,
            MutationType.CONNECTION_REMOVAL,
            MutationType.TOPOLOGY_MUTATION
        ];

        const mutation_type = mutation_types[Math.floor(Math.random() * mutation_types.length)];

        try {
            switch (mutation_type) {
                case MutationType.NODE_ADDITION:
                    this._addNodeMutation(genome);
                    break;
                case MutationType.CONNECTION_ADDITION:
                    this._addConnectionMutation(genome);
                    break;
                case MutationType.CONNECTION_REMOVAL:
                    this._removeConnectionMutation(genome);
                    break;
                case MutationType.TOPOLOGY_MUTATION:
                    this._topologyMutation(genome);
                    break;
            }
            return mutation_type;
        } catch (error) {
            console.warn('Falha na mutação estrutural:', error);
            return null;
        }
    }

    _addNodeMutation(genome) {
        const enabled_connections = genome.connection_genes.filter(c => c.enabled);
        if (enabled_connections.length === 0) return;

        const connection = enabled_connections[Math.floor(Math.random() * enabled_connections.length)];
        connection.enabled = false;

        const new_node_id = genome.add_node_gene(
            'hidden',
            ['relu', 'sigmoid', 'tanh'][Math.floor(Math.random() * 3)]
        );

        genome.add_connection_gene(
            connection.source,
            new_node_id,
            1.0
        );

        genome.add_connection_gene(
            new_node_id,
            connection.target,
            connection.weight
        );
    }

    _addConnectionMutation(genome) {
        if (genome.node_genes.length < 2) return;

        const existing_connections = new Set(
            genome.connection_genes.map(c => `${c.source}_${c.target}`)
        );

        const possible_connections = [];

        for (let i = 0; i < genome.node_genes.length; i++) {
            for (let j = i + 1; j < genome.node_genes.length; j++) {
                const source = genome.node_genes[i].id;
                const target = genome.node_genes[j].id;
                const connection_key = `${source}_${target}`;

                if (!existing_connections.has(connection_key)) {
                    possible_connections.push([source, target]);
                }
            }
        }

        if (possible_connections.length > 0) {
            const [source_id, target_id] = possible_connections[
                Math.floor(Math.random() * possible_connections.length)
            ];
            genome.add_connection_gene(
                source_id,
                target_id,
                Math.random() * 2 - 1
            );
        }
    }

    _removeConnectionMutation(genome) {
        const enabled_connections = genome.connection_genes.filter(c => c.enabled);
        if (enabled_connections.length > 0) {
            const connection = enabled_connections[
                Math.floor(Math.random() * enabled_connections.length)
            ];
            connection.enabled = false;
        }
    }

    _topologyMutation(genome) {
        if (genome.node_genes.length === 0) return;

        const node = genome.node_genes[Math.floor(Math.random() * genome.node_genes.length)];
        if (node.type === 'hidden') {
            const activations = ['relu', 'sigmoid', 'tanh', 'leaky_relu'];
            node.activation = activations[Math.floor(Math.random() * activations.length)];
        }
    }

    _mutateParameters(genome) {
        if (Math.random() < 0.3) {
            genome.learning_rate *= Math.random() * 1.5 + 0.5; // 0.5-2.0
            genome.learning_rate = Math.max(0.0001, Math.min(0.1, genome.learning_rate));
        }
    }

    getStatistics() {
        this.updateStatistics();

        return {
            population_id: this.id,
            generation: this.generation,
            size: this.size,
            average_fitness: this.average_fitness,
            best_fitness: this.best_genome ? this.best_genome.overall_fitness : 0.0,
            fitness_std: this.fitness_std,
            diversity_score: this.diversity_score,
            convergence_rate: this.convergence_rate,
            fitness_stats: this.fitness_stats,
            environment: this.environment_id,
            evolutionary_pressure: this.evolutionary_pressure,
            timestamp: new Date().toISOString()
        };
    }

    toJSON() {
        return {
            id: this.id,
            generation: this.generation,
            created_at: this.created_at.toISOString(),
            genomes: Object.fromEntries(
                Object.entries(this.genomes).map(([id, genome]) => [id, genome.toJSON()])
            ),
            population_size: this.population_size,
            elitism_count: this.elitism_count,
            selection_pressure: this.selection_pressure,
            mutation_rate: this.mutation_rate,
            crossover_rate: this.crossover_rate,
            fitness_stats: this.fitness_stats,
            diversity_score: this.diversity_score,
            convergence_rate: this.convergence_rate,
            best_genome_history: this.best_genome_history,
            average_fitness_history: this.average_fitness_history,
            environment_id: this.environment_id,
            evolutionary_pressure: this.evolutionary_pressure
        };
    }

    static fromJSON(data) {
        const genomes = {};
        for (const [id, genomeData] of Object.entries(data.genomes || {})) {
            genomes[id] = NeuralGenome.fromJSON(genomeData);
        }

        return new EvolutionaryPopulation({
            ...data,
            created_at: new Date(data.created_at),
            genomes: genomes
        });
    }
}

// ============================================================================
// AMBIENTE EVOLUTIVO
// ============================================================================

class EvolutionaryEnvironment {
    constructor({
        id = IDGenerator.generateId('env'),
        name = 'Default Environment',
        created_at = new Date(),
        population_config = {
            size: 100,
            elitism: 5,
            mutation_rate: 0.1,
            crossover_rate: 0.7
        },
        evolutionary_strategy = EvolutionStrategy.GENETIC_ALGORITHM,
        fitness_metrics = [
            FitnessMetric.PERFORMANCE,
            FitnessMetric.ADAPTABILITY,
            FitnessMetric.EFFICIENCY
        ],
        selection_pressure = 0.3,
        novelty_weight = 0.1,
        complexity_penalty = 0.05,
        max_generations = 1000,
        target_fitness = 0.95,
        stagnation_limit = 50,
        current_generation = 0,
        populations = {},
        active_population_id = null,
        evolution_history = [],
        best_solutions = [],
        environment_metrics = {},
        adaptive_parameters = {
            mutation_rate_adjustment: 0.1,
            selection_pressure_adjustment: 0.05,
            novelty_exploration_rate: 0.2
        }
    } = {}) {
        this.id = id;
        this.name = name;
        this.created_at = new Date(created_at);
        this.population_config = population_config;
        this.evolutionary_strategy = evolutionary_strategy;
        this.fitness_metrics = fitness_metrics;
        this.selection_pressure = selection_pressure;
        this.novelty_weight = novelty_weight;
        this.complexity_penalty = complexity_penalty;
        this.max_generations = max_generations;
        this.target_fitness = target_fitness;
        this.stagnation_limit = stagnation_limit;
        this.current_generation = current_generation;
        this.populations = populations;
        this.active_population_id = active_population_id;
        this.evolution_history = evolution_history;
        this.best_solutions = best_solutions;
        this.environment_metrics = environment_metrics;
        this.adaptive_parameters = adaptive_parameters;

        if (!this.active_population_id) {
            this.createNewPopulation();
        }
    }

    createNewPopulation(name = 'Main Population') {
        const population = new EvolutionaryPopulation({
            population_size: this.population_config.size,
            elitism_count: this.population_config.elitism,
            mutation_rate: this.population_config.mutation_rate,
            crossover_rate: this.population_config.crossover_rate,
            environment_id: this.id
        });

        this.populations[population.id] = population;
        this.active_population_id = population.id;

        return population.id;
    }

    async runEvolutionCycle(generations = 10) {
        console.log(`Iniciando ciclo evolutivo de ${generations} gerações`);

        const start_time = Date.now();

        for (let gen = 0; gen < generations; gen++) {
            if (this.current_generation >= this.max_generations) {
                console.log(`Limite máximo de gerações (${this.max_generations}) atingido`);
                break;
            }

            await this._evolveGeneration();

            // Verificar estagnação
            if (this._checkStagnation()) {
                console.log('Estagnação detectada, ajustando parâmetros...');
                this._adjustEvolutionaryParameters();
            }

            // Verificar se atingiu fitness alvo
            if (this._checkTargetAchieved()) {
                console.log(`Fitness alvo (${this.target_fitness}) atingido!`);
                break;
            }
        }

        const elapsed = (Date.now() - start_time) / 1000;
        console.log(`Ciclo evolutivo concluído em ${elapsed.toFixed(2)}s`);
    }

    async _evolveGeneration() {
        if (!this.active_population_id) {
            console.warn('Nenhuma população ativa');
            return;
        }

        const population = this.populations[this.active_population_id];

        // 1. Fase de avaliação
        await this._evaluatePopulation(population);

        // 2. Evoluir população
        population.evolveGeneration(this.evolutionary_strategy);

        // 3. Atualizar ambiente
        this.current_generation += 1;
        this._updateEnvironmentMetrics(population);
        this._recordGenerationHistory(population);

        // 4. Verificar e salvar melhores soluções
        this._updateBestSolutions(population);

        console.log(
            `Geração ${this.current_generation} evoluída. ` +
            `Melhor fitness: ${population.best_genome ? population.best_genome.overall_fitness.toFixed(4) : 0}`
        );
    }

    async _evaluatePopulation(population) {
        const evaluationPromises = [];

        for (const genome of Object.values(population.genomes)) {
            if (genome.evaluation_count === 0) {
                evaluationPromises.push(this._evaluateGenomeTask(genome));
            }
        }

        if (evaluationPromises.length > 0) {
            await Promise.all(evaluationPromises);
        }
    }

    async _evaluateGenomeTask(genome) {
        // Simular processamento assíncrono
        await new Promise(resolve => 
            setTimeout(resolve, Math.random() * 90 + 10) // 10-100ms
        );

        // Avaliação simulada
        const base_performance = Math.random() * 0.4 + 0.4; // 0.4-0.8
        const innovation_bonus = genome.novelty_score * 0.3;
        const complexity_penalty = Math.min(0.3, genome.complexity * this.complexity_penalty);

        genome.fitness_scores = {
            [FitnessMetric.PERFORMANCE]: base_performance - complexity_penalty + innovation_bonus,
            [FitnessMetric.ADAPTABILITY]: Math.random() * 0.4 + 0.5, // 0.5-0.9
            [FitnessMetric.EFFICIENCY]: Math.max(0.1, 0.7 - genome.complexity * 0.1),
            [FitnessMetric.ROBUSTNESS]: Math.random() * 0.35 + 0.6, // 0.6-0.95
            [FitnessMetric.GENERALIZATION]: Math.random() * 0.4 + 0.4 + innovation_bonus * 0.5,
            [FitnessMetric.INNOVATION]: genome.novelty_score,
            [FitnessMetric.ENERGY_EFFICIENCY]: Math.random() * 0.4 + 0.5, // 0.5-0.9
            [FitnessMetric.LEARNING_SPEED]: Math.random() * 0.45 + 0.4 // 0.4-0.85
        };

        genome.evaluation_count += 1;
        genome.last_evaluated = new Date();
    }

    _updateEnvironmentMetrics(population) {
        const stats = population.getStatistics();

        this.environment_metrics = {
            current_generation: this.current_generation,
            active_population: population.id,
            population_size: population.size,
            average_fitness: stats.average_fitness,
            best_fitness: stats.best_fitness,
            diversity: stats.diversity_score,
            convergence: stats.convergence_rate,
            stagnation_count: this._calculateStagnationCount(),
            innovation_rate: this._calculateInnovationRate(population),
            environmental_pressure: this._calculateEnvironmentalPressure()
        };
    }

    _calculateStagnationCount() {
        if (this.evolution_history.length < 10) return 0;

        const recent_history = this.evolution_history.slice(-10);
        const fitness_values = recent_history.map(h => h.best_fitness);

        let improvements = 0;
        for (let i = 1; i < fitness_values.length; i++) {
            if (fitness_values[i] > fitness_values[i - 1] * 1.001) { // 0.1% de melhoria
                improvements += 1;
            }
        }

        return 10 - improvements;
    }

    _calculateInnovationRate(population) {
        if (Object.keys(population.genomes).length === 0) return 0.0;

        const novelty_scores = Object.values(population.genomes).map(g => g.novelty_score);
        return MathUtils.mean(novelty_scores);
    }

    _calculateEnvironmentalPressure() {
        return {
            selection: this.selection_pressure,
            novelty: this.novelty_weight,
            complexity: this.complexity_penalty,
            adaptation_rate: this.adaptive_parameters.mutation_rate_adjustment
        };
    }

    _recordGenerationHistory(population) {
        const history_entry = {
            generation: this.current_generation,
            timestamp: new Date().toISOString(),
            population_id: population.id,
            best_genome_id: population.best_genome ? population.best_genome.id : null,
            best_fitness: population.best_genome ? population.best_genome.overall_fitness : 0.0,
            average_fitness: population.average_fitness,
            diversity: population.diversity_score,
            environment_metrics: { ...this.environment_metrics }
        };

        this.evolution_history.push(history_entry);
    }

    _updateBestSolutions(population) {
        if (!population.best_genome) return;

        const current_best = population.best_genome;
        const current_fitness = current_best.overall_fitness;

        if (this.best_solutions.length === 0 || current_fitness > this.best_solutions[0].fitness) {
            const solution_entry = {
                genome_id: current_best.id,
                fitness: current_fitness,
                generation: this.current_generation,
                complexity: current_best.complexity,
                novelty: current_best.novelty_score,
                timestamp: new Date().toISOString(),
                metadata: current_best.metadata
            };

            this.best_solutions.unshift(solution_entry);

            // Manter apenas as top 20 soluções
            if (this.best_solutions.length > 20) {
                this.best_solutions = this.best_solutions.slice(0, 20);
            }
        }
    }

    _checkStagnation() {
        const stagnation_count = this.environment_metrics.stagnation_count || 0;
        return stagnation_count >= this.stagnation_limit;
    }

    _checkTargetAchieved() {
        if (this.best_solutions.length === 0) return false;
        return this.best_solutions[0].fitness >= this.target_fitness;
    }

    _adjustEvolutionaryParameters() {
        // Aumentar taxa de mutação para explorar mais
        this.population_config.mutation_rate = Math.min(
            0.5, this.population_config.mutation_rate * 1.5
        );

        // Aumentar peso da novidade
        this.novelty_weight = Math.min(0.5, this.novelty_weight * 1.3);

        // Reduzir pressão seletiva temporariamente
        this.selection_pressure = Math.max(0.1, this.selection_pressure * 0.7);

        console.log(
            `Parâmetros ajustados: mutation_rate=${this.population_config.mutation_rate.toFixed(3)}, ` +
            `novelty_weight=${this.novelty_weight.toFixed(3)}`
        );
    }

    getEvolutionReport() {
        if (this.best_solutions.length === 0) {
            return { status: 'NO_EVOLUTION_YET' };
        }

        const best = this.best_solutions[0];

        return {
            environment_id: this.id,
            environment_name: this.name,
            current_generation: this.current_generation,
            total_generations: this.evolution_history.length,
            best_solution: best,
            evolution_stats: {
                average_fitness_trend: this._getFitnessTrend(),
                diversity_trend: this._getDiversityTrend(),
                innovation_rate_trend: this._getInnovationTrend(),
                convergence_speed: this._calculateConvergenceSpeed()
            },
            environment_status: {
                stagnation: this._checkStagnation(),
                target_achieved: this._checkTargetAchieved(),
                evolutionary_pressure: this._calculateEnvironmentalPressure()
            },
            recommendations: this._generateRecommendations()
        };
    }

    _getFitnessTrend() {
        if (this.evolution_history.length === 0) return [];
        return this.evolution_history.slice(-20).map(h => h.average_fitness);
    }

    _getDiversityTrend() {
        if (this.evolution_history.length === 0) return [];
        return this.evolution_history.slice(-20).map(h => h.environment_metrics.diversity || 0);
    }

    _getInnovationTrend() {
        if (this.evolution_history.length === 0) return [];
        return this.evolution_history.slice(-20).map(h => h.environment_metrics.innovation_rate || 0);
    }

    _calculateConvergenceSpeed() {
        if (this.evolution_history.length < 10) return 0.0;

        const fitness_values = this.evolution_history.map(h => h.average_fitness);
        if (fitness_values.length >= 10) {
            // Calcular autocorrelação com lag 1
            const x = fitness_values.slice(0, -1);
            const y = fitness_values.slice(1);
            const correlation = MathUtils.correlation(x, y);
            return Math.abs(correlation);
        }

        return 0.0;
    }

    _generateRecommendations() {
        const recommendations = [];

        if (this._checkStagnation()) {
            recommendations.push(
                'Aumentar taxa de mutação para explorar novo espaço de busca',
                'Introduzir mais diversidade genética',
                'Considerar mudança de estratégia evolutiva',
                'Reduzir pressão seletiva temporariamente'
            );
        }

        if (this.environment_metrics.diversity < 0.1) {
            recommendations.push('Diversidade genética muito baixa - risco de convergência prematura');
        }

        if (this.environment_metrics.innovation_rate < 0.05) {
            recommendations.push('Taxa de inovação baixa - considerar aumentar peso da novidade');
        }

        if (this.current_generation > 100 && !this._checkTargetAchieved()) {
            recommendations.push('Progresso lento - considerar ajustar critérios de fitness');
        }

        return recommendations;
    }

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            created_at: this.created_at.toISOString(),
            population_config: this.population_config,
            evolutionary_strategy: this.evolutionary_strategy,
            fitness_metrics: this.fitness_metrics,
            selection_pressure: this.selection_pressure,
            novelty_weight: this.novelty_weight,
            complexity_penalty: this.complexity_penalty,
            max_generations: this.max_generations,
            target_fitness: this.target_fitness,
            stagnation_limit: this.stagnation_limit,
            current_generation: this.current_generation,
            populations: Object.fromEntries(
                Object.entries(this.populations).map(([id, pop]) => [id, pop.toJSON()])
            ),
            active_population_id: this.active_population_id,
            evolution_history: this.evolution_history,
            best_solutions: this.best_solutions,
            environment_metrics: this.environment_metrics,
            adaptive_parameters: this.adaptive_parameters
        };
    }

    static fromJSON(data) {
        const populations = {};
        for (const [id, popData] of Object.entries(data.populations || {})) {
            populations[id] = EvolutionaryPopulation.fromJSON(popData);
        }

        return new EvolutionaryEnvironment({
            ...data,
            created_at: new Date(data.created_at),
            populations: populations
        });
    }
}

// ============================================================================
// SISTEMA DE EVOLUÇÃO NEURAL CONTÍNUA
// ============================================================================

class EvolutionWorker {
    constructor() {
        this.workers = [];
        this.taskQueue = [];
        this.running = false;
        this.maxWorkers = navigator.hardwareConcurrency || 4;
    }

    async initialize() {
        for (let i = 0; i < this.maxWorkers; i++) {
            const worker = this._createWorker();
            this.workers.push({ worker, busy: false });
        }
        this.running = true;
        this._processQueue();
    }

    _createWorker() {
        const workerCode = `
            self.onmessage = async function(e) {
                const { id, task, data } = e.data;
                
                try {
                    let result;
                    switch (task) {
                        case 'evaluate_genome':
                            result = simulateGenomeEvaluation(data);
                            break;
                        case 'crossover':
                            result = simulateCrossover(data.parent1, data.parent2);
                            break;
                        case 'mutate':
                            result = simulateMutation(data.genome);
                            break;
                        default:
                            throw new Error('Unknown task: ' + task);
                    }
                    
                    self.postMessage({ id, result });
                } catch (error) {
                    self.postMessage({ id, error: error.message });
                }
            };
            
            function simulateGenomeEvaluation(genome) {
                // Simulação de avaliação
                const base = Math.random() * 0.4 + 0.3;
                const complexity = genome.complexity * 0.1;
                return {
                    performance: base + complexity,
                    adaptability: Math.random() * 0.4 + 0.4,
                    efficiency: Math.max(0.1, 0.6 - genome.complexity * 0.2)
                };
            }
            
            function simulateCrossover(parent1, parent2) {
                // Simulação de crossover
                return {
                    id: 'child_' + Date.now(),
                    fitness: (parent1.fitness + parent2.fitness) / 2
                };
            }
            
            function simulateMutation(genome) {
                // Simulação de mutação
                return {
                    ...genome,
                    mutation_rate: genome.mutation_rate * (Math.random() * 0.4 + 0.8)
                };
            }
        `;

        const blob = new Blob([workerCode], { type: 'application/javascript' });
        return new Worker(URL.createObjectURL(blob));
    }

    submitTask(task, data) {
        return new Promise((resolve, reject) => {
            const taskId = IDGenerator.generateId('task');
            this.taskQueue.push({
                id: taskId,
                task,
                data,
                resolve,
                reject
            });
        });
    }

    _processQueue() {
        if (!this.running) return;

        for (const workerInfo of this.workers) {
            if (!workerInfo.busy && this.taskQueue.length > 0) {
                const task = this.taskQueue.shift();
                workerInfo.busy = true;

                workerInfo.worker.onmessage = (e) => {
                    const { id, result, error } = e.data;
                    if (error) {
                        task.reject(new Error(error));
                    } else {
                        task.resolve(result);
                    }
                    workerInfo.busy = false;
                    this._processQueue();
                };

                workerInfo.worker.postMessage({
                    id: task.id,
                    task: task.task,
                    data: task.data
                });
            }
        }

        setTimeout(() => this._processQueue(), 10);
    }

    async terminate() {
        this.running = false;
        for (const workerInfo of this.workers) {
            workerInfo.worker.terminate();
        }
        this.workers = [];
    }
}

class ContinuousNeuralEvolution {
    constructor(config = null) {
        this.config = config || this._defaultConfig();
        this.environments = new Map();
        this.evolutionTasks = new Map();
        this.isRunning = false;
        this.workerPool = new EvolutionWorker();
        this.metricsCollector = new EvolutionMetricsCollector();
        this.eventBus = new EvolutionEventBus();
        this.logger = new Logger('ContinuousNeuralEvolution');

        // Inicializar worker pool
        this.workerPool.initialize();

        this.logger.info('Sistema de Evolução Neural Contínua inicializado');
    }

    _defaultConfig() {
        return {
            max_concurrent_environments: 5,
            default_generations_per_cycle: 50,
            checkpoint_interval: 10,
            auto_save: true,
            log_level: 'INFO',
            evolution_strategies: [
                EvolutionStrategy.GENETIC_ALGORITHM,
                EvolutionStrategy.NEUROEVOLUTION,
                EvolutionStrategy.MULTI_OBJECTIVE
            ]
        };
    }

    createEnvironment(name, kwargs = {}) {
        const env_config = {
            name: name,
            population_config: kwargs.population_config || {
                size: kwargs.population_size || 100,
                elitism: kwargs.elitism || 5,
                mutation_rate: kwargs.mutation_rate || 0.1,
                crossover_rate: kwargs.crossover_rate || 0.7
            },
            evolutionary_strategy: kwargs.strategy || EvolutionStrategy.GENETIC_ALGORITHM,
            max_generations: kwargs.max_generations || 1000,
            target_fitness: kwargs.target_fitness || 0.95
        };

        const environment = new EvolutionaryEnvironment(env_config);
        this.environments.set(environment.id, environment);

        this.eventBus.publish({
            type: 'environment_created',
            environment_id: environment.id,
            name: name,
            timestamp: new Date().toISOString()
        });

        this.logger.info(`Ambiente criado: ${environment.id} (${name})`);
        return environment.id;
    }

    async startEvolution(environment_id, generations = null) {
        if (!this.environments.has(environment_id)) {
            throw new Error(`Ambiente ${environment_id} não encontrado`);
        }

        if (this.evolutionTasks.has(environment_id)) {
            this.logger.warn(`Evolução já em execução para ambiente ${environment_id}`);
            return;
        }

        const env = this.environments.get(environment_id);
        const gen_count = generations || this.config.default_generations_per_cycle;

        const task = this._runEvolutionLoop(env, gen_count);
        this.evolutionTasks.set(environment_id, task);

        this.eventBus.publish({
            type: 'evolution_started',
            environment_id: environment_id,
            generations: gen_count,
            timestamp: new Date().toISOString()
        });

        this.logger.info(`Evolução iniciada para ambiente ${environment_id} (${gen_count} gerações)`);
    }

    async _runEvolutionLoop(environment, generations) {
        try {
            await environment.runEvolutionCycle(generations);

            // Coletar métricas
            this.metricsCollector.recordEvolution(environment);

            // Salvar checkpoint se configurado
            if (this.config.auto_save) {
                await this._saveCheckpoint(environment);
            }

            this.eventBus.publish({
                type: 'evolution_completed',
                environment_id: environment.id,
                generations_completed: environment.current_generation,
                best_fitness: environment.best_solutions.length > 0 ? 
                    environment.best_solutions[0].fitness : 0,
                timestamp: new Date().toISOString()
            });

        } catch (error) {
            this.logger.error(`Erro na evolução do ambiente ${environment.id}:`, error);

            this.eventBus.publish({
                type: 'evolution_error',
                environment_id: environment.id,
                error: error.message,
                timestamp: new Date().toISOString()
            });

        } finally {
            // Limpar task
            this.evolutionTasks.delete(environment.id);
        }
    }

    async _saveCheckpoint(environment) {
        try {
            const checkpoint = {
                timestamp: new Date().toISOString(),
                environment: environment.toJSON(),
                system_state: this.getSystemStatus()
            };

            // Salvar no localStorage para demonstração
            // Em produção, usar IndexedDB ou backend
            localStorage.setItem(
                `evolution_checkpoint_${environment.id}`,
                JSON.stringify(checkpoint)
            );

            this.logger.debug(`Checkpoint salvo para ambiente ${environment.id}`);
        } catch (error) {
            this.logger.error('Erro ao salvar checkpoint:', error);
        }
    }

    async stopEvolution(environment_id) {
        if (this.evolutionTasks.has(environment_id)) {
            // Em implementação real, cancelaríamos a task
            this.evolutionTasks.delete(environment_id);

            this.eventBus.publish({
                type: 'evolution_stopped',
                environment_id: environment_id,
                timestamp: new Date().toISOString()
            });

            this.logger.info(`Evolução parada para ambiente ${environment_id}`);
        }
    }

    async evolveMultipleEnvironments(environment_ids, generations = null) {
        const tasks = [];

        for (const env_id of environment_ids) {
            if (this.environments.has(env_id)) {
                tasks.push(this.startEvolution(env_id, generations));
            }
        }

        if (tasks.length > 0) {
            await Promise.all(tasks);
        }
    }

    getEnvironmentStatus(environment_id) {
        if (!this.environments.has(environment_id)) {
            return { error: 'Environment not found' };
        }

        const env = this.environments.get(environment_id);
        const report = env.getEvolutionReport();

        // Adicionar informações de execução
        report.is_evolving = this.evolutionTasks.has(environment_id);
        report.evolution_task_count = this.evolutionTasks.size;

        return report;
    }

    getSystemStatus() {
        return {
            system: 'Continuous Neural Evolution',
            timestamp: new Date().toISOString(),
            environments_count: this.environments.size,
            active_evolutions: this.evolutionTasks.size,
            config: this.config,
            metrics: this.metricsCollector.getSummary(),
            events_count: this.eventBus.getEventCount(),
            worker_pool_status: 'active'
        };
    }

    exportBestSolutions(environment_id, output_dir = 'best_solutions') {
        if (!this.environments.has(environment_id)) {
            return [];
        }

        const env = this.environments.get(environment_id);
        const exported_files = [];

        for (let i = 0; i < Math.min(5, env.best_solutions.length); i++) {
            const solution = env.best_solutions[i];
            
            for (const population of Object.values(env.populations)) {
                const genome = population.genomes[solution.genome_id];
                if (genome) {
                    const filename = `best_${i + 1}_gen${solution.generation}_fit${solution.fitness.toFixed(4)}.json`;
                    const data = JSON.stringify(genome.toJSON(), null, 2);
                    
                    // Salvar como arquivo (simulação)
                    const blob = new Blob([data], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    
                    exported_files.push({
                        filename: filename,
                        url: url,
                        genome_id: genome.id,
                        fitness: solution.fitness
                    });
                    break;
                }
            }
        }

        this.logger.info(`Exportadas ${exported_files.length} melhores soluções`);
        return exported_files;
    }

    async runContinuousEvolution(check_interval = 60) {
        this.isRunning = true;
        this.logger.info(`Iniciando evolução contínua (check a cada ${check_interval}s)`);

        try {
            while (this.isRunning) {
                // Verificar ambientes que precisam de evolução
                for (const [env_id, environment] of this.environments) {
                    if (!this.evolutionTasks.has(env_id)) {
                        // Verificar se precisa evoluir mais
                        if (!environment._checkTargetAchieved()) {
                            // Verificar estagnação
                            if (environment._checkStagnation()) {
                                this.logger.info(`Ambiente ${env_id} estagnado, reiniciando evolução`);
                                environment.createNewPopulation();
                            }

                            // Iniciar nova evolução
                            await this.startEvolution(env_id);
                        }
                    }
                }

                // Coletar métricas do sistema
                this.metricsCollector.recordSystemMetrics(this);

                // Aguardar próximo check
                await new Promise(resolve => 
                    setTimeout(resolve, check_interval * 1000)
                );
            }

        } catch (error) {
            this.logger.error('Erro na evolução contínua:', error);
        } finally {
            this.isRunning = false;
        }
    }

    stopContinuousEvolution() {
        this.isRunning = false;
        this.logger.info('Evolução contínua sendo parada...');
    }

    async terminate() {
        await this.workerPool.terminate();
        this.logger.info('Sistema terminado');
    }
}

// ============================================================================
// COMPONENTES AUXILIARES
// ============================================================================

class EvolutionMetricsCollector {
    constructor(max_history = 1000) {
        this.metrics_history = new Map();
        this.environment_metrics = new Map();
        this.max_history = max_history;
    }

    recordEvolution(environment) {
        const env_id = environment.id;
        const metrics = environment.getEvolutionReport();

        const key_metrics = {
            generation: environment.current_generation,
            best_fitness: metrics.best_solution ? metrics.best_solution.fitness : 0,
            average_fitness: metrics.evolution_stats.average_fitness_trend.length > 0 ?
                MathUtils.mean(metrics.evolution_stats.average_fitness_trend) : 0,
            diversity: metrics.evolution_stats.diversity_trend.length > 0 ?
                MathUtils.mean(metrics.evolution_stats.diversity_trend) : 0,
            innovation_rate: metrics.evolution_stats.innovation_rate_trend.length > 0 ?
                MathUtils.mean(metrics.evolution_stats.innovation_rate_trend) : 0,
            timestamp: new Date().toISOString()
        };

        for (const [key, value] of Object.entries(key_metrics)) {
            const history_key = `${env_id}_${key}`;
            if (!this.metrics_history.has(history_key)) {
                this.metrics_history.set(history_key, []);
            }
            
            const history = this.metrics_history.get(history_key);
            history.push(value);
            
            if (history.length > this.max_history) {
                history.shift();
            }
        }

        this.environment_metrics.set(env_id, key_metrics);
    }

    recordSystemMetrics(evolution_system) {
        const system_metrics = {
            active_environments: evolution_system.environments.size,
            active_evolutions: evolution_system.evolutionTasks.size,
            total_generations: Array.from(evolution_system.environments.values())
                .reduce((sum, env) => sum + env.current_generation, 0),
            timestamp: new Date().toISOString()
        };

        for (const [key, value] of Object.entries(system_metrics)) {
            const history_key = `system_${key}`;
            if (!this.metrics_history.has(history_key)) {
                this.metrics_history.set(history_key, []);
            }
            
            const history = this.metrics_history.get(history_key);
            history.push(value);
            
            if (history.length > this.max_history) {
                history.shift();
            }
        }
    }

    getEnvironmentTrend(environment_id, metric) {
        const key = `${environment_id}_${metric}`;
        return this.metrics_history.get(key) || [];
    }

    getSummary() {
        return {
            environments_tracked: this.environment_metrics.size,
            total_metrics_recorded: Array.from(this.metrics_history.values())
                .reduce((sum, arr) => sum + arr.length, 0),
            environment_summaries: Object.fromEntries(
                Array.from(this.environment_metrics.entries()).map(([id, metrics]) => [
                    id,
                    {
                        last_generation: metrics.generation || 0,
                        last_best_fitness: metrics.best_fitness || 0,
                        trend_length: this.getEnvironmentTrend(id, 'best_fitness').length
                    }
                ])
            )
        };
    }
}

class EvolutionEventBus {
    constructor() {
        this.subscribers = new Map();
        this.event_history = [];
        this.max_history = 10000;
    }

    subscribe(event_type, callback) {
        if (!this.subscribers.has(event_type)) {
            this.subscribers.set(event_type, []);
        }
        this.subscribers.get(event_type).push(callback);
    }

    publish(event) {
        const event_type = event.type || 'unknown';
        const full_event = {
            ...event,
            published_at: new Date().toISOString()
        };

        this.event_history.push(full_event);
        if (this.event_history.length > this.max_history) {
            this.event_history.shift();
        }

        // Notificar subscribers
        const subscribers = this.subscribers.get(event_type) || [];
        for (const callback of subscribers) {
            try {
                callback(full_event);
            } catch (error) {
                console.error(`Erro em callback de evento ${event_type}:`, error);
            }
        }
    }

    getEventCount() {
        return this.event_history.length;
    }

    getRecentEvents(event_type = null, limit = 100) {
        let events = this.event_history;

        if (event_type) {
            events = events.filter(e => e.type === event_type);
        }

        return events.slice(-limit);
    }
}

// ============================================================================
// INTERFACE WEB E VISUALIZAÇÃO
// ============================================================================

class EvolutionVisualizer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.charts = new Map();
        this.currentEnvironment = null;
    }

    initialize() {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="evolution-dashboard">
                <div class="dashboard-header">
                    <h1>🧬 Evolution Dashboard</h1>
                    <div class="environment-selector">
                        <select id="envSelector">
                            <option value="">Select Environment</option>
                        </select>
                        <button id="refreshBtn">🔄 Refresh</button>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <div class="card overview-card">
                        <h3>📊 Overview</h3>
                        <div id="overviewStats"></div>
                    </div>
                    
                    <div class="card fitness-card">
                        <h3>📈 Fitness Progress</h3>
                        <canvas id="fitnessChart"></canvas>
                    </div>
                    
                    <div class="card diversity-card">
                        <h3>🌐 Population Diversity</h3>
                        <canvas id="diversityChart"></canvas>
                    </div>
                    
                    <div class="card topology-card">
                        <h3>🕸️ Best Genome Topology</h3>
                        <div id="topologyVisualization"></div>
                    </div>
                    
                    <div class="card solutions-card">
                        <h3>🏆 Best Solutions</h3>
                        <div id="bestSolutionsList"></div>
                    </div>
                    
                    <div class="card recommendations-card">
                        <h3>💡 Recommendations</h3>
                        <div id="recommendationsList"></div>
                    </div>
                </div>
                
                <div class="controls">
                    <button id="exportBtn">📥 Export Best</button>
                    <button id="evolveBtn">⚡ Evolve (10 gens)</button>
                    <button id="continuousBtn">♾️ Continuous Evolution</button>
                </div>
            </div>
        `;

        this._setupEventListeners();
        this._initializeCharts();
    }

    _setupEventListeners() {
        document.getElementById('refreshBtn')?.addEventListener('click', () => this.refresh());
        document.getElementById('exportBtn')?.addEventListener('click', () => this.exportBest());
        document.getElementById('evolveBtn')?.addEventListener('click', () => this.evolve());
        document.getElementById('continuousBtn')?.addEventListener('click', () => this.toggleContinuous());
    }

    _initializeCharts() {
        // Inicializar gráficos Chart.js se disponível
        if (typeof Chart !== 'undefined') {
            const fitnessCtx = document.getElementById('fitnessChart')?.getContext('2d');
            const diversityCtx = document.getElementById('diversityChart')?.getContext('2d');

            if (fitnessCtx) {
                this.charts.set('fitness', new Chart(fitnessCtx, {
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [
                            {
                                label: 'Best Fitness',
                                data: [],
                                borderColor: 'rgb(75, 192, 192)',
                                tension: 0.1
                            },
                            {
                                label: 'Average Fitness',
                                data: [],
                                borderColor: 'rgb(255, 99, 132)',
                                tension: 0.1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            }
                        }
                    }
                }));
            }

            if (diversityCtx) {
                this.charts.set('diversity', new Chart(diversityCtx, {
                    type: 'bar',
                    data: {
                        labels: [],
                        datasets: [{
                            label: 'Diversity Score',
                            data: [],
                            backgroundColor: 'rgba(54, 162, 235, 0.5)'
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 1
                            }
                        }
                    }
                }));
            }
        }
    }

    async updateEnvironment(environment_id, evolutionSystem) {
        this.currentEnvironment = environment_id;
        const status = evolutionSystem.getEnvironmentStatus(environment_id);

        // Atualizar visão geral
        this._updateOverview(status);

        // Atualizar gráficos
        this._updateCharts(status);

        // Atualizar topologia
        this._updateTopology(status);

        // Atualizar melhores soluções
        this._updateBestSolutions(status);

        // Atualizar recomendações
        this._updateRecommendations(status);
    }

    _updateOverview(status) {
        const overviewEl = document.getElementById('overviewStats');
        if (!overviewEl) return;

        overviewEl.innerHTML = `
            <div class="stat-item">
                <span class="stat-label">Generation:</span>
                <span class="stat-value">${status.current_generation || 0}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Best Fitness:</span>
                <span class="stat-value">${status.best_solution?.fitness?.toFixed(4) || '0.0000'}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Population Size:</span>
                <span class="stat-value">${status.environment_status?.population_size || 0}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Diversity:</span>
                <span class="stat-value">${(status.evolution_stats?.diversity_trend?.slice(-1)[0] || 0).toFixed(3)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Status:</span>
                <span class="stat-value ${status.is_evolving ? 'status-active' : 'status-inactive'}">
                    ${status.is_evolving ? 'Evolving' : 'Idle'}
                </span>
            </div>
        `;
    }

    _updateCharts(status) {
        const fitnessChart = this.charts.get('fitness');
        const diversityChart = this.charts.get('diversity');

        if (fitnessChart && status.evolution_stats) {
            const history = status.evolution_stats.average_fitness_trend || [];
            const labels = history.map((_, i) => `Gen ${i + 1}`);

            fitnessChart.data.labels = labels;
            
            // Melhor fitness (simulado)
            const bestHistory = history.map((val, i) => val * (1 + i * 0.01));
            fitnessChart.data.datasets[0].data = bestHistory;
            fitnessChart.data.datasets[1].data = history;
            
            fitnessChart.update();
        }

        if (diversityChart && status.evolution_stats) {
            const diversity = status.evolution_stats.diversity_trend || [];
            const labels = diversity.map((_, i) => `Gen ${i + 1}`);

            diversityChart.data.labels = labels;
            diversityChart.data.datasets[0].data = diversity;
            diversityChart.update();
        }
    }

    _updateTopology(status) {
        const topologyEl = document.getElementById('topologyVisualization');
        if (!topologyEl) return;

        // Visualização simplificada da topologia
        topologyEl.innerHTML = `
            <div class="topology-graph">
                <div class="topology-node input">Input</div>
                <div class="topology-connector">→</div>
                <div class="topology-node hidden">Hidden</div>
                <div class="topology-connector">→</div>
                <div class="topology-node output">Output</div>
            </div>
            <div class="topology-stats">
                <p>Complexity: ${status.best_solution?.complexity?.toFixed(2) || '0.00'}</p>
                <p>Novelty: ${status.best_solution?.novelty?.toFixed(3) || '0.000'}</p>
                <p>Generation: ${status.best_solution?.generation || 0}</p>
            </div>
        `;
    }

    _updateBestSolutions(status) {
        const solutionsEl = document.getElementById('bestSolutionsList');
        if (!solutionsEl) return;

        // Em implementação real, mostraria várias soluções
        solutionsEl.innerHTML = status.best_solution ? `
            <div class="solution-item">
                <div class="solution-header">
                    <span class="solution-rank">🏆</span>
                    <span class="solution-fitness">${status.best_solution.fitness.toFixed(4)}</span>
                </div>
                <div class="solution-details">
                    <p><strong>ID:</strong> ${status.best_solution.genome_id}</p>
                    <p><strong>Generation:</strong> ${status.best_solution.generation}</p>
                    <p><strong>Complexity:</strong> ${status.best_solution.complexity.toFixed(2)}</p>
                </div>
            </div>
        ` : '<p>No solutions yet</p>';
    }

    _updateRecommendations(status) {
        const recommendationsEl = document.getElementById('recommendationsList');
        if (!recommendationsEl) return;

        recommendationsEl.innerHTML = status.recommendations ? 
            status.recommendations.map(rec => `<div class="recommendation">✅ ${rec}</div>`).join('') :
            '<p>No recommendations</p>';
    }

    async refresh() {
        // Implementar refresh
    }

    async exportBest() {
        // Implementar export
    }

    async evolve() {
        // Implementar evolução
    }

    async toggleContinuous() {
        // Implementar evolução contínua
    }
}

// ============================================================================
// API REST SIMULADA PARA INTEGRAÇÃO
// ============================================================================

class EvolutionAPI {
    constructor(evolutionSystem) {
        this.evolutionSystem = evolutionSystem;
        this.server = null;
    }

    async startServer(port = 3000) {
        if (typeof process !== 'undefined' && process.versions?.node) {
            // Node.js server
            const express = require('express');
            const app = express();
            app.use(express.json());

            this._setupRoutes(app);

            this.server = app.listen(port, () => {
                console.log(`Evolution API server running on port ${port}`);
            });
        } else {
            // Browser simulation
            console.log('API simulation mode (browser)');
        }
    }

    _setupRoutes(app) {
        // GET /api/environments
        app.get('/api/environments', (req, res) => {
            const environments = Array.from(this.evolutionSystem.environments.values())
                .map(env => ({
                    id: env.id,
                    name: env.name,
                    generation: env.current_generation,
                    status: this.evolutionSystem.evolutionTasks.has(env.id) ? 'evolving' : 'idle'
                }));
            res.json(environments);
        });

        // POST /api/environments
        app.post('/api/environments', (req, res) => {
            const { name, ...config } = req.body;
            const envId = this.evolutionSystem.createEnvironment(name, config);
            res.json({ id: envId, message: 'Environment created' });
        });

        // GET /api/environments/:id
        app.get('/api/environments/:id', (req, res) => {
            const envId = req.params.id;
            const status = this.evolutionSystem.getEnvironmentStatus(envId);
            if (status.error) {
                res.status(404).json(status);
            } else {
                res.json(status);
            }
        });

        // POST /api/environments/:id/evolve
        app.post('/api/environments/:id/evolve', async (req, res) => {
            const envId = req.params.id;
            const generations = req.body.generations || 10;

            try {
                await this.evolutionSystem.startEvolution(envId, generations);
                res.json({ message: 'Evolution started' });
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // GET /api/system
        app.get('/api/system', (req, res) => {
            res.json(this.evolutionSystem.getSystemStatus());
        });

        // WebSocket para atualizações em tempo real
        if (app.ws) {
            app.ws('/ws/evolution', (ws, req) => {
                const envId = req.query.environment;

                // Enviar atualizações periódicas
                const interval = setInterval(() => {
                    if (envId) {
                        const status = this.evolutionSystem.getEnvironmentStatus(envId);
                        ws.send(JSON.stringify(status));
                    } else {
                        ws.send(JSON.stringify(this.evolutionSystem.getSystemStatus()));
                    }
                }, 1000);

                ws.on('close', () => {
                    clearInterval(interval);
                });
            });
        }
    }

    stopServer() {
        if (this.server) {
            this.server.close();
            console.log('Evolution API server stopped');
        }
    }
}

// ============================================================================
// FACHADA SIMPLIFICADA
// ============================================================================

class NeuralEvolutionEngine {
    static instance = null;

    constructor() {
        if (NeuralEvolutionEngine.instance) {
            return NeuralEvolutionEngine.instance;
        }

        this.evolutionSystem = new ContinuousNeuralEvolution();
        this.visualizer = null;
        this.api = null;
        this.isInitialized = false;

        NeuralEvolutionEngine.instance = this;
    }

    static getInstance() {
        if (!NeuralEvolutionEngine.instance) {
            NeuralEvolutionEngine.instance = new NeuralEvolutionEngine();
        }
        return NeuralEvolutionEngine.instance;
    }

    async initialize(config = null) {
        if (this.isInitialized) return;

        if (config) {
            this.evolutionSystem.config = { ...this.evolutionSystem.config, ...config };
        }

        // Configurar event handlers
        this._setupEventHandlers();

        // Inicializar visualizador se no browser
        if (typeof document !== 'undefined') {
            this.visualizer = new EvolutionVisualizer('evolutionDashboard');
            this.visualizer.initialize();
        }

        // Inicializar API se em Node.js
        if (typeof process !== 'undefined' && process.versions?.node) {
            this.api = new EvolutionAPI(this.evolutionSystem);
            await this.api.startServer();
        }

        this.isInitialized = true;
        console.log('Neural Evolution Engine initialized');
    }

    _setupEventHandlers() {
        const eventBus = this.evolutionSystem.eventBus;

        eventBus.subscribe('environment_created', this._onEnvironmentCreated.bind(this));
        eventBus.subscribe('evolution_completed', this._onEvolutionCompleted.bind(this));
        eventBus.subscribe('evolution_error', this._onEvolutionError.bind(this));
    }

    _onEnvironmentCreated(event) {
        console.log(`New environment created: ${event.environment_id}`);
        
        if (this.visualizer) {
            // Atualizar seletor de ambientes
            const selector = document.getElementById('envSelector');
            if (selector) {
                const option = document.createElement('option');
                option.value = event.environment_id;
                option.textContent = `${event.name} (${event.environment_id})`;
                selector.appendChild(option);
            }
        }
    }

    _onEvolutionCompleted(event) {
        console.log(`Evolution completed: ${event.environment_id} (fitness: ${event.best_fitness.toFixed(4)})`);
        
        if (this.visualizer && this.visualizer.currentEnvironment === event.environment_id) {
            this.visualizer.refresh();
        }
    }

    _onEvolutionError(event) {
        console.error(`Evolution error in ${event.environment_id}:`, event.error);
    }

    async createAndEvolve(name, generations = 100, kwargs = {}) {
        const env_id = this.evolutionSystem.createEnvironment(name, kwargs);
        await this.evolutionSystem.startEvolution(env_id, generations);
        return env_id;
    }

    async evolveExisting(environment_id, generations = 50) {
        await this.evolutionSystem.startEvolution(environment_id, generations);
    }

    getProgress(environment_id) {
        return this.evolutionSystem.getEnvironmentStatus(environment_id);
    }

    async runOptimizationPipeline(num_environments = 3, generations_per_env = 200) {
        console.log(`Starting optimization pipeline with ${num_environments} environments`);

        const strategies = [
            EvolutionStrategy.GENETIC_ALGORITHM,
            EvolutionStrategy.NEUROEVOLUTION,
            EvolutionStrategy.MULTI_OBJECTIVE
        ];

        const env_ids = [];
        for (let i = 0; i < num_environments; i++) {
            const strategy = strategies[i % strategies.length];
            const env_id = this.evolutionSystem.createEnvironment(
                `Env_${i + 1}_${strategy}`,
                {
                    strategy: strategy,
                    population_size: 80,
                    mutation_rate: i % 2 === 0 ? 0.15 : 0.1
                }
            );
            env_ids.push(env_id);
        }

        await this.evolutionSystem.evolveMultipleEnvironments(env_ids, generations_per_env);

        // Analisar resultados
        const results = [];
        for (const env_id of env_ids) {
            const status = this.getProgress(env_id);
            results.push({
                environment_id: env_id,
                strategy: strategies[env_ids.indexOf(env_id) % strategies.length],
                best_fitness: status.best_solution?.fitness || 0,
                generations: status.current_generation
            });
        }

        const best_result = results.reduce((best, current) => 
            current.best_fitness > best.best_fitness ? current : best
        );

        console.log(`Best strategy: ${best_result.strategy} (fitness: ${best_result.best_fitness.toFixed(4)})`);

        return {
            results,
            best_strategy: best_result.strategy,
            best_fitness: best_result.best_fitness
        };
    }

    async continuousOptimization(check_interval = 30) {
        console.log(`Starting continuous optimization (check every ${check_interval}s)`);
        return this.evolutionSystem.runContinuousEvolution(check_interval);
    }

    getSystemReport() {
        return {
            engine: 'Neural Evolution Engine',
            initialized: this.isInitialized,
            system_status: this.evolutionSystem.getSystemStatus(),
            environments: Array.from(this.evolutionSystem.environments.keys()).map(env_id =>
                this.evolutionSystem.getEnvironmentStatus(env_id)
            ),
            timestamp: new Date().toISOString()
        };
    }

    async terminate() {
        await this.evolutionSystem.terminate();
        if (this.api) {
            this.api.stopServer();
        }
        console.log('Neural Evolution Engine terminated');
    }
}

// ============================================================================
// EXEMPLOS E DEMONSTRAÇÕES
// ============================================================================

async function evolutionExample() {
    console.log('=== SISTEMA DE EVOLUÇÃO NEURAL CONTÍNUA ===\n');

    // 1. Inicializar motor
    const engine = NeuralEvolutionEngine.getInstance();
    await engine.initialize({
        max_concurrent_environments: 3,
        default_generations_per_cycle: 50,
        auto_save: true
    });

    // 2. Criar e evoluir ambiente individual
    console.log('1. EVOLUINDO AMBIENTE INDIVIDUAL...');
    const env_id = await engine.createAndEvolve(
        'Test Environment',
        30,
        {
            strategy: EvolutionStrategy.GENETIC_ALGORITHM,
            population_size: 50,
            target_fitness: 0.8
        }
    );

    // Aguardar evolução
    await new Promise(resolve => setTimeout(resolve, 5000));

    // 3. Verificar progresso
    const progress = engine.getProgress(env_id);
    console.log(`\nProgresso do ambiente ${env_id}:`);
    console.log(`  Geração: ${progress.current_generation}`);
    console.log(`  Melhor fitness: ${progress.best_solution?.fitness?.toFixed(4) || '0.0000'}`);
    console.log(`  Fitness médio: ${progress.evolution_stats?.average_fitness_trend?.slice(-1)[0]?.toFixed(4) || '0.0000'}`);

    // 4. Executar pipeline de otimização
    console.log('\n2. EXECUTANDO PIPELINE DE OTIMIZAÇÃO...');
    const pipeline_results = await engine.runOptimizationPipeline(2, 20);

    console.log('\nResultados do pipeline:');
    for (const result of pipeline_results.results) {
        console.log(`  ${result.strategy}: Fitness ${result.best_fitness.toFixed(4)} (Geração ${result.generations})`);
    }
    console.log(`\nMelhor estratégia: ${pipeline_results.best_strategy}`);

    // 5. Obter relatório do sistema
    console.log('\n3. RELATÓRIO DO SISTEMA:');
    const report = engine.getSystemReport();
    console.log(`  Ambientes ativos: ${report.system_status.environments_count}`);
    console.log(`  Evoluções ativas: ${report.system_status.active_evolutions}`);
    console.log(`  Total de gerações: ${report.environments.reduce((sum, env) => sum + (env.current_generation || 0), 0)}`);

    // 6. Exportar melhores soluções
    console.log('\n4. EXPORTANDO MELHORES SOLUÇÕES...');
    for (const envId of engine.evolutionSystem.environments.keys()) {
        const exported = engine.evolutionSystem.exportBestSolutions(envId);
        console.log(`  Ambiente ${envId}: ${exported.length} soluções exportadas`);
    }

    return engine;
}

async function demo() {
    try {
        const engine = await evolutionExample();
        
        // Iniciar servidor de demonstração
        if (typeof document !== 'undefined') {
            // Adicionar dashboard ao DOM
            const container = document.createElement('div');
            container.id = 'evolutionDashboard';
            container.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                width: 400px;
                height: 600px;
                background: white;
                border: 2px solid #333;
                border-radius: 10px;
                padding: 15px;
                overflow-y: auto;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                z-index: 1000;
            `;
            document.body.appendChild(container);

            // Inicializar visualizador
            engine.visualizer = new EvolutionVisualizer('evolutionDashboard');
            engine.visualizer.initialize();
            
            // Atualizar com primeiro ambiente
            const envs = Array.from(engine.evolutionSystem.environments.keys());
            if (envs.length > 0) {
                engine.visualizer.updateEnvironment(envs[0], engine.evolutionSystem);
            }
        }

        console.log('\n=== DEMONSTRAÇÃO CONCLUÍDA ===');
        
        // Retornar engine para uso externo
        return engine;
    } catch (error) {
        console.error('Erro na demonstração:', error);
    }
}

// ============================================================================
// EXPORTAÇÕES PARA USO EXTERNO
// ============================================================================

// Exportar para Node.js (CommonJS)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        NeuralEvolutionEngine,
        ContinuousNeuralEvolution,
        EvolutionaryEnvironment,
        EvolutionaryPopulation,
        NeuralGenome,
        EvolutionStrategy,
        MutationType,
        FitnessMetric,
        MathUtils,
        evolutionExample,
        demo
    };
} 

// Exportar para navegador
if (typeof window !== 'undefined') {
    window.NeuralEvolutionEngine = NeuralEvolutionEngine;
    window.evolutionExample = evolutionExample;
    window.demo = demo;

    // Auto-inicialização quando o DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('🧬 Neural Evolution Engine carregado e pronto!');
            
            // Adicionar botão de demonstração se não existir
            if (!document.getElementById('evolutionDemoBtn')) {
                const btn = document.createElement('button');
                btn.id = 'evolutionDemoBtn';
                btn.textContent = '🧬 Start Evolution Demo';
                btn.style.cssText = `
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: bold;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    z-index: 999;
                `;
                btn.onclick = demo;
                document.body.appendChild(btn);
            }
        });
    } else {
        console.log('🧬 Neural Evolution Engine carregado e pronto!');
    }
}

// Executar demonstração se for o arquivo principal
if (typeof require !== 'undefined' && require.main === module) {
    evolutionExample().catch(console.error);
}