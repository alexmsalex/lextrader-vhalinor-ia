import { EventEmitter } from 'events';
import * as tf from '@tensorflow/tfjs';
import { PerformanceMonitor } from '../utils/PerformanceMonitor';
import { GeneticOperators } from '../utils/GeneticOperators';
import { PopulationAnalytics } from '../utils/PopulationAnalytics';
import { FitnessEvaluator } from '../utils/FitnessEvaluator';
import { ModelArchiver } from '../utils/ModelArchiver';

/**
 * Sistema de Evolução Neural Contínua - Algoritmos Genéticos Avançados
 * 
 * Este sistema implementa evolução contínua de redes neurais usando algoritmos genéticos,
 * com múltiplas estratégias de seleção, crossover, mutação e migração.
 */
export class ContinuousEvolution extends EventEmitter {
    private config: {
        populationSize: number;
        eliteSize: number;
        mutationRate: number;
        crossoverRate: number;
        migrationRate: number;
        selectionMethod: 'tournament' | 'roulette' | 'rank' | 'elitist';
        crossoverMethod: 'uniform' | 'singlePoint' | 'twoPoint' | 'arithmetic' | 'blend';
        mutationMethod: 'gaussian' | 'uniform' | 'adaptive' | 'polynomial';
        fitnessMetrics: string[];
        convergenceThreshold: number;
        maxGenerations: number;
        diversityThreshold: number;
        islandCount: number;
        migrationInterval: number;
        archiveSize: number;
        enableSpeciation: boolean;
        speciationThreshold: number;
        nichingMethod: 'fitnessSharing' | 'crowding' | 'restrictedTournament';
        parallelEvaluations: number;
        weightRange: [number, number];
        enableHybridTraining: boolean;
        hybridTrainingRatio: number;
    };

    private population: NeuralIndividual[];
    private fitnessEvaluator: FitnessEvaluator;
    private geneticOperators: GeneticOperators;
    private populationAnalytics: PopulationAnalytics;
    private performanceMonitor: PerformanceMonitor;
    private modelArchiver: ModelArchiver;

    private generation: number;
    private bestIndividual: NeuralIndividual | null;
    private hallOfFame: HallOfFameEntry[];
    private speciationClusters: Species[];
    private migrationIslands: MigrationIsland[];
    private convergenceHistory: ConvergenceMetrics[];
    private isEvolving: boolean;
    private evolutionHistory: EvolutionHistory[];
    private adaptiveRates: AdaptiveRates;

    constructor(config: Partial<typeof ContinuousEvolution.prototype.config> = {}) {
        super();

        this.config = {
            populationSize: config.populationSize || 100,
            eliteSize: config.eliteSize || 10,
            mutationRate: config.mutationRate || 0.1,
            crossoverRate: config.crossoverRate || 0.8,
            migrationRate: config.migrationRate || 0.05,
            selectionMethod: config.selectionMethod || 'tournament',
            crossoverMethod: config.crossoverMethod || 'blend',
            mutationMethod: config.mutationMethod || 'adaptive',
            fitnessMetrics: config.fitnessMetrics || ['sharpe', 'maxDrawdown', 'profitFactor', 'winRate', 'consistency'],
            convergenceThreshold: config.convergenceThreshold || 0.001,
            maxGenerations: config.maxGenerations || 1000,
            diversityThreshold: config.diversityThreshold || 0.3,
            islandCount: config.islandCount || 5,
            migrationInterval: config.migrationInterval || 10,
            archiveSize: config.archiveSize || 50,
            enableSpeciation: config.enableSpeciation !== false,
            speciationThreshold: config.speciationThreshold || 0.15,
            nichingMethod: config.nichingMethod || 'fitnessSharing',
            parallelEvaluations: config.parallelEvaluations || 4,
            weightRange: config.weightRange || [-1, 1],
            enableHybridTraining: config.enableHybridTraining || true,
            hybridTrainingRatio: config.hybridTrainingRatio || 0.3
        };

        this.population = [];
        this.fitnessEvaluator = new FitnessEvaluator();
        this.geneticOperators = new GeneticOperators();
        this.populationAnalytics = new PopulationAnalytics();
        this.performanceMonitor = new PerformanceMonitor();
        this.modelArchiver = new ModelArchiver();

        this.generation = 0;
        this.bestIndividual = null;
        this.hallOfFame = [];
        this.speciationClusters = [];
        this.migrationIslands = [];
        this.convergenceHistory = [];
        this.isEvolving = false;
        this.evolutionHistory = [];
        this.adaptiveRates = {
            mutationRate: this.config.mutationRate,
            crossoverRate: this.config.crossoverRate,
            lastImprovement: 0
        };

        this.setMaxListeners(50);
        this.log('Sistema de Evolução Neural Contínua inicializado', 'info');
    }

    /**
     * Inicializa o sistema de evolução
     */
    async initialize(): Promise<{
        success: boolean;
        message: string;
        populationSize: number;
        config: any;
    }> {
        try {
            // Inicializa avaliador de fitness
            await this.fitnessEvaluator.initialize(this.config.fitnessMetrics);

            // Inicializa operadores genéticos
            await this.geneticOperators.initialize(this.config);

            // Inicializa analytics
            await this.populationAnalytics.initialize();

            // Cria população inicial
            await this.initializePopulation();

            // Inicializa ilhas de migração se necessário
            if (this.config.islandCount > 1) {
                await this.initializeMigrationIslands();
            }

            this.log('✅ Sistema de Evolução Neural Contínua inicializado com sucesso', 'info');
            this.log(`População: ${this.population.length} indivíduos`, 'info');
            this.log(`Método de seleção: ${this.config.selectionMethod}`, 'debug');
            this.log(`Taxa de mutação: ${this.config.mutationRate}`, 'debug');

            this.emit('initialized', {
                populationSize: this.population.length,
                config: this.config,
                generation: this.generation
            });

            return {
                success: true,
                message: 'Sistema de evolução inicializado com sucesso',
                populationSize: this.population.length,
                config: this.config
            };

        } catch (error) {
            this.log(`Falha na inicialização: ${error.message}`, 'error');
            this.emit('error', error);

            return {
                success: false,
                message: `Falha na inicialização: ${error.message}`,
                populationSize: 0,
                config: null
            };
        }
    }

    /**
     * Inicializa população com indivíduos aleatórios
     */
    private async initializePopulation(): Promise<void> {
        this.population = [];

        for (let i = 0; i < this.config.populationSize; i++) {
            const individual = await this.createRandomIndividual(i);
            this.population.push(individual);
        }

        // Avalia fitness inicial
        await this.evaluatePopulationFitness();

        // Ordena por fitness
        this.sortPopulation();

        // Define melhor indivíduo
        this.bestIndividual = this.population[0];

        // Adiciona ao hall da fama
        this.addToHallOfFame(this.bestIndividual);

        this.log(`População inicial criada com ${this.population.length} indivíduos`, 'info');
        this.log(`Melhor fitness inicial: ${this.bestIndividual.fitness?.overall.toFixed(4)}`, 'info');
    }

    /**
     * Cria um indivíduo aleatório
     */
    private async createRandomIndividual(id: number): Promise<NeuralIndividual> {
        const architecture = this.generateRandomArchitecture();
        const weights = await this.generateRandomWeights(architecture);

        const individual: NeuralIndividual = {
            id: `ind_${id}_gen_${this.generation}`,
            generation: this.generation,
            architecture,
            weights,
            biases: await this.generateRandomBiases(architecture),
            activationFunctions: this.generateRandomActivations(architecture),
            dropoutRates: this.generateRandomDropoutRates(architecture),
            learningRate: this.randomInRange(0.0001, 0.01),
            batchSize: this.randomChoice([16, 32, 64, 128]),
            fitness: null,
            metrics: {},
            metadata: {
                creationDate: new Date(),
                parentIds: [],
            },
            age: 0,
            speciesId: null,
            islandId: this.config.islandCount > 1 ? Math.floor(Math.random() * this.config.islandCount) : 0
        };

        return individual;
    }

    /**
     * Gera arquitetura aleatória
     */
    private generateRandomArchitecture(): LayerArchitecture[] {
        const layerCount = this.randomInt(2, 6); // 2 a 5 camadas ocultas
        const architectures: LayerArchitecture[] = [];

        let inputSize = 20; // Número padrão de features

        for (let i = 0; i < layerCount; i++) {
            const layerType = this.randomChoice(['dense', 'lstm', 'gru', 'conv1d']);
            let units: number;

            if (layerType === 'conv1d') {
                units = this.randomChoice([32, 64, 128]);
            } else {
                // Redução progressiva de unidades
                const maxUnits = Math.max(8, inputSize * (1 - i / layerCount));
                units = this.randomInt(Math.floor(maxUnits * 0.5), Math.floor(maxUnits * 1.5));
            }

            architectures.push({
                type: layerType,
                units,
                activation: this.randomChoice(['relu', 'tanh', 'sigmoid', 'leaky_relu']),
                kernelInitializer: this.randomChoice(['he_normal', 'glorot_uniform']),
                useBias: Math.random() > 0.2
            });

            inputSize = units;
        }

        // Camada de saída
        architectures.push({
            type: 'dense',
            units: 3, // BUY, SELL, HOLD
            activation: 'softmax',
            kernelInitializer: 'glorot_uniform',
            useBias: true
        });

        return architectures;
    }

    /**
     * Gera pesos aleatórios
     */
    private async generateRandomWeights(architecture: LayerArchitecture[]): Promise<tf.Tensor[]> {
        const weights: tf.Tensor[] = [];
        let prevUnits = 20; // Input size

        for (const layer of architecture) {
            if (layer.type === 'conv1d') {
                // Para conv1d: [filterSize, inputChannels, filters]
                const filterSize = 3;
                const inputChannels = prevUnits;
                const filters = layer.units;

                const weight = tf.randomUniform(
                    [filterSize, inputChannels, filters],
                    this.config.weightRange[0],
                    this.config.weightRange[1]
                );
                weights.push(weight);
                prevUnits = filters;
            } else {
                // Para dense/lstm/gru
                const weight = tf.randomUniform(
                    [prevUnits, layer.units],
                    this.config.weightRange[0],
                    this.config.weightRange[1]
                );
                weights.push(weight);
                prevUnits = layer.units;
            }
        }

        return weights;
    }

    /**
     * Gera biases aleatórios
     */
    private async generateRandomBiases(architecture: LayerArchitecture[]): Promise<tf.Tensor[]> {
        return architecture.map(layer => {
            if (!layer.useBias) return null;
            return tf.randomUniform(
                [layer.units],
                this.config.weightRange[0] * 0.1,
                this.config.weightRange[1] * 0.1
            );
        });
    }

    /**
     * Gera funções de ativação aleatórias
     */
    private generateRandomActivations(architecture: LayerArchitecture[]): string[] {
        return architecture.map(layer => layer.activation);
    }

    /**
     * Gera taxas de dropout aleatórias
     */
    private generateRandomDropoutRates(architecture: LayerArchitecture[]): number[] {
        return architecture.map(() => this.randomInRange(0, 0.5));
    }

    /**
     * Avalia fitness da população
     */
    private async evaluatePopulationFitness(): Promise<void> {
        const evaluationPromises = this.population.map(async (individual, index) => {
            if (individual.fitness && individual.age < 3) {
                // Reutiliza fitness se indivíduo for jovem
                return individual;
            }

            const fitness = await this.fitnessEvaluator.evaluate(individual);
            individual.fitness = fitness;
            individual.metrics = fitness.metrics;
            individual.age++;

            this.emit('individualEvaluated', {
                individualId: individual.id,
                fitness: fitness.overall,
                generation: this.generation,
                progress: (index + 1) / this.population.length
            });

            return individual;
        });

        this.population = await Promise.all(evaluationPromises);
    }

    /**
     * Executa uma geração completa de evolução
     */
    async evolve(population?: NeuralIndividual[], options?: {
        generation?: number;
        marketData?: any;
        forceEvaluation?: boolean;
        hybridTraining?: boolean;
    }): Promise<{
        success: boolean;
        newPopulation: NeuralIndividual[];
        bestIndividual: NeuralIndividual;
        metrics: EvolutionMetrics;
        generation: number;
    }> {
        try {
            if (this.isEvolving) {
                throw new Error('Evolução já em progresso');
            }

            this.isEvolving = true;
            const startTime = Date.now();

            // Usa população fornecida ou a atual
            const currentPopulation = population || this.population;
            const generation = options?.generation || this.generation + 1;

            this.log(`🧬 Iniciando evolução para Geração ${generation}...`, 'info');
            this.emit('evolutionStarted', { generation, populationSize: currentPopulation.length });

            // Avalia fitness se necessário
            if (options?.forceEvaluation || this.generation % 5 === 0) {
                await this.evaluatePopulationFitness();
            }

            // Ordena população por fitness
            this.sortPopulation();

            // Coleta métricas antes da evolução
            const preEvolutionMetrics = this.collectPopulationMetrics();

            // Aplica especiação se habilitado
            if (this.config.enableSpeciation) {
                await this.applySpeciation();
            }

            // Cria nova população
            const newPopulation = await this.createNewGeneration(currentPopulation);

            // Aplica migração se houver ilhas
            if (this.config.islandCount > 1 && generation % this.config.migrationInterval === 0) {
                await this.applyMigration(newPopulation);
            }

            // Aplica treinamento híbrido se habilitado
            if (this.config.enableHybridTraining && options?.hybridTraining !== false) {
                await this.applyHybridTraining(newPopulation);
            }

            // Avalia fitness da nova população
            this.population = newPopulation;
            await this.evaluatePopulationFitness();
            this.sortPopulation();

            // Atualiza melhor indivíduo
            const newBest = this.population[0];
            const improvement = newBest.fitness!.overall - (this.bestIndividual?.fitness?.overall || 0);

            if (improvement > 0) {
                this.bestIndividual = newBest;
                this.addToHallOfFame(newBest);
                this.adaptiveRates.lastImprovement = generation;
            }

            // Atualiza taxas adaptativas
            this.updateAdaptiveRates(improvement);

            // Coleta métricas após evolução
            const postEvolutionMetrics = this.collectPopulationMetrics();

            // Calcula métricas da evolução
            const evolutionMetrics: EvolutionMetrics = {
                generation,
                duration: Date.now() - startTime,
                fitnessImprovement: improvement,
                bestFitness: newBest.fitness!.overall,
                averageFitness: postEvolutionMetrics.averageFitness,
                diversity: postEvolutionMetrics.diversity,
                convergence: this.calculateConvergence(),
                speciationCount: this.speciationClusters.length,
                mutationCount: this.countMutations(newPopulation),
                crossoverCount: this.countCrossovers(newPopulation)
            };

            // Atualiza histórico
            this.generation = generation;
            this.evolutionHistory.push({
                generation,
                metrics: evolutionMetrics,
                timestamp: new Date(),
                bestIndividual: { ...newBest, weights: [] } // Não armazenar pesos no histórico
            });

            // Verifica convergência
            const hasConverged = this.checkConvergence(evolutionMetrics);

            this.isEvolving = false;

            this.log(`✅ Evolução da Geração ${generation} completada em ${evolutionMetrics.duration}ms`, 'info');
            this.log(`Melhor fitness: ${evolutionMetrics.bestFitness.toFixed(4)} (${improvement > 0 ? '+' : ''}${improvement.toFixed(4)})`, 'info');
            this.log(`Diversidade: ${evolutionMetrics.diversity.toFixed(4)}`, 'debug');

            this.emit('evolutionCompleted', {
                generation,
                metrics: evolutionMetrics,
                bestIndividual: newBest,
                hasConverged
            });

            // Salva checkpoint se necessário
            if (generation % 10 === 0) {
                await this.saveCheckpoint(generation);
            }

            return {
                success: true,
                newPopulation: this.population,
                bestIndividual: newBest,
                metrics: evolutionMetrics,
                generation
            };

        } catch (error) {
            this.isEvolving = false;
            this.log(`Falha na evolução: ${error.message}`, 'error');
            this.emit('evolutionError', error);

            return {
                success: false,
                newPopulation: population || this.population,
                bestIndividual: this.bestIndividual!,
                metrics: null,
                generation: this.generation
            };
        }
    }

    /**
     * Cria nova geração através de seleção e operadores genéticos
     */
    private async createNewGeneration(currentPopulation: NeuralIndividual[]): Promise<NeuralIndividual[]> {
        const newPopulation: NeuralIndividual[] = [];
        const eliteCount = Math.floor(this.config.populationSize * 0.1); // 10% elite

        // Preserva elite (elitismo)
        const elite = currentPopulation.slice(0, eliteCount);
        newPopulation.push(...elite.map(ind => this.cloneIndividual(ind)));

        // Preenche resto da população
        while (newPopulation.length < this.config.populationSize) {
            // Seleciona pais
            const parent1 = this.selectParent(currentPopulation);
            const parent2 = this.selectParent(currentPopulation);

            let child: NeuralIndividual;

            // Aplica crossover
            if (Math.random() < this.adaptiveRates.crossoverRate && parent1.id !== parent2.id) {
                child = await this.applyCrossover(parent1, parent2);
            } else {
                // Clona um dos pais
                child = this.cloneIndividual(Math.random() > 0.5 ? parent1 : parent2);
            }

            // Aplica mutação
            if (Math.random() < this.adaptiveRates.mutationRate) {
                child = await this.applyMutation(child);
            }

            // Atualiza metadados
            child.id = `ind_${newPopulation.length}_gen_${this.generation + 1}`;
            child.generation = this.generation + 1;
            child.metadata.parentIds = [parent1.id, parent2.id];
            child.metadata.creationDate = new Date();
            child.age = 0;

            newPopulation.push(child);
        }

        return newPopulation;
    }

    /**
     * Seleciona pai usando método configurado
     */
    private selectParent(population: NeuralIndividual[]): NeuralIndividual {
        switch (this.config.selectionMethod) {
            case 'tournament':
                return this.tournamentSelection(population);
            case 'roulette':
                return this.rouletteWheelSelection(population);
            case 'rank':
                return this.rankSelection(population);
            case 'elitist':
                return this.elitistSelection(population);
            default:
                return this.tournamentSelection(population);
        }
    }

    /**
     * Seleção por torneio
     */
    private tournamentSelection(population: NeuralIndividual[], tournamentSize: number = 3): NeuralIndividual {
        const tournament: NeuralIndividual[] = [];

        for (let i = 0; i < tournamentSize; i++) {
            const randomIndex = Math.floor(Math.random() * population.length);
            tournament.push(population[randomIndex]);
        }

        // Retorna o melhor do torneio
        return tournament.reduce((best, current) =>
            (current.fitness?.overall || 0) > (best.fitness?.overall || 0) ? current : best
        );
    }

    /**
     * Seleção por roleta
     */
    private rouletteWheelSelection(population: NeuralIndividual[]): NeuralIndividual {
        const totalFitness = population.reduce((sum, ind) => sum + (ind.fitness?.overall || 0), 0);
        let randomFitness = Math.random() * totalFitness;

        for (const individual of population) {
            randomFitness -= individual.fitness?.overall || 0;
            if (randomFitness <= 0) {
                return individual;
            }
        }

        return population[population.length - 1];
    }

    /**
     * Seleção por rank
     */
    private rankSelection(population: NeuralIndividual[]): NeuralIndividual {
        // População já está ordenada por fitness
        const rankWeights = population.map((_, index) =>
            (population.length - index) / (population.length * (population.length + 1) / 2)
        );

        let randomValue = Math.random();
        for (let i = 0; i < population.length; i++) {
            randomValue -= rankWeights[i];
            if (randomValue <= 0) {
                return population[i];
            }
        }

        return population[population.length - 1];
    }

    /**
     * Seleção elitista
     */
    private elitistSelection(population: NeuralIndividual[]): NeuralIndividual {
        // Sempre seleciona entre os melhores 20%
        const elitePool = population.slice(0, Math.floor(population.length * 0.2));
        return elitePool[Math.floor(Math.random() * elitePool.length)];
    }

    /**
     * Aplica crossover entre dois pais
     */
    private async applyCrossover(parent1: NeuralIndividual, parent2: NeuralIndividual): Promise<NeuralIndividual> {
        switch (this.config.crossoverMethod) {
            case 'uniform':
                return this.uniformCrossover(parent1, parent2);
            case 'singlePoint':
                return this.singlePointCrossover(parent1, parent2);
            case 'twoPoint':
                return this.twoPointCrossover(parent1, parent2);
            case 'arithmetic':
                return this.arithmeticCrossover(parent1, parent2);
            case 'blend':
                return this.blendCrossover(parent1, parent2);
            default:
                return this.blendCrossover(parent1, parent2);
        }
    }

    /**
     * Crossover uniforme
     */
    private async uniformCrossover(parent1: NeuralIndividual, parent2: NeuralIndividual): Promise<NeuralIndividual> {
        const child = this.cloneIndividual(parent1);

        // Para cada camada, escolhe pesos aleatoriamente de um dos pais
        for (let i = 0; i < child.weights.length; i++) {
            const mask = tf.randomUniform(child.weights[i].shape, 0, 1);
            const parent1Weights = child.weights[i];
            const parent2Weights = parent2.weights[i];

            child.weights[i] = tf.where(
                mask.greater(0.5),
                parent1Weights,
                parent2Weights
            );

            tf.dispose([mask]);
        }

        // Combina arquitetura (escolhe aleatoriamente de cada pai)
        child.architecture = child.architecture.map((layer, i) =>
            Math.random() > 0.5 ? layer : parent2.architecture[i]
        );

        return child;
    }

    /**
     * Crossover de ponto único
     */
    private async singlePointCrossover(parent1: NeuralIndividual, parent2: NeuralIndividual): Promise<NeuralIndividual> {
        const child = this.cloneIndividual(parent1);
        const crossoverPoint = Math.floor(Math.random() * child.weights.length);

        // Troca pesos após o ponto de crossover
        for (let i = crossoverPoint; i < child.weights.length; i++) {
            tf.dispose(child.weights[i]);
            child.weights[i] = parent2.weights[i].clone();
        }

        return child;
    }

    /**
     * Crossover de dois pontos
     */
    private async twoPointCrossover(parent1: NeuralIndividual, parent2: NeuralIndividual): Promise<NeuralIndividual> {
        const child = this.cloneIndividual(parent1);
        const point1 = Math.floor(Math.random() * child.weights.length);
        const point2 = Math.floor(Math.random() * (child.weights.length - point1)) + point1;

        // Troca pesos entre os dois pontos
        for (let i = point1; i < point2; i++) {
            tf.dispose(child.weights[i]);
            child.weights[i] = parent2.weights[i].clone();
        }

        return child;
    }

    /**
     * Crossover aritmético
     */
    private async arithmeticCrossover(parent1: NeuralIndividual, parent2: NeuralIndividual): Promise<NeuralIndividual> {
        const child = this.cloneIndividual(parent1);
        const alpha = Math.random(); // Fator de mistura

        for (let i = 0; i < child.weights.length; i++) {
            const newWeights = parent1.weights[i].mul(alpha).add(
                parent2.weights[i].mul(1 - alpha)
            );

            tf.dispose(child.weights[i]);
            child.weights[i] = newWeights;
        }

        return child;
    }

    /**
     * Crossover BLX-α (Blend)
     */
    private async blendCrossover(parent1: NeuralIndividual, parent2: NeuralIndividual): Promise<NeuralIndividual> {
        const child = this.cloneIndividual(parent1);
        const alpha = 0.5; // Parâmetro BLX-α

        for (let i = 0; i < child.weights.length; i++) {
            const parent1Data = await parent1.weights[i].data();
            const parent2Data = await parent2.weights[i].data();

            const newData = parent1Data.map((w1, j) => {
                const w2 = parent2Data[j];
                const min = Math.min(w1, w2) - alpha * Math.abs(w2 - w1);
                const max = Math.max(w1, w2) + alpha * Math.abs(w2 - w1);

                return this.randomInRange(min, max);
            });

            tf.dispose(child.weights[i]);
            child.weights[i] = tf.tensor(newData, child.weights[i].shape);
        }

        return child;
    }

    /**
     * Aplica mutação a um indivíduo
     */
    private async applyMutation(individual: NeuralIndividual): Promise<NeuralIndividual> {
        const mutated = this.cloneIndividual(individual);

        switch (this.config.mutationMethod) {
            case 'gaussian':
                await this.gaussianMutation(mutated);
                break;
            case 'uniform':
                await this.uniformMutation(mutated);
                break;
            case 'adaptive':
                await this.adaptiveMutation(mutated);
                break;
            case 'polynomial':
                await this.polynomialMutation(mutated);
                break;
        }

        // Mutação de arquitetura (ocasional)
        if (Math.random() < 0.1) {
            await this.architectureMutation(mutated);
        }

        // Mutação de hiperparâmetros
        if (Math.random() < 0.2) {
            await this.hyperparameterMutation(mutated);
        }

        return mutated;
    }

    /**
     * Mutação gaussiana
     */
    private async gaussianMutation(individual: NeuralIndividual): Promise<void> {
        const mutationStrength = 0.1;

        for (let i = 0; i < individual.weights.length; i++) {
            const noise = tf.randomNormal(individual.weights[i].shape, 0, mutationStrength);
            const mutated = individual.weights[i].add(noise);

            tf.dispose([individual.weights[i], noise]);
            individual.weights[i] = mutated;
        }
    }

    /**
     * Mutação uniforme
     */
    private async uniformMutation(individual: NeuralIndividual): Promise<void> {
        const mutationRate = 0.05; // 5% dos pesos

        for (let i = 0; i < individual.weights.length; i++) {
            const mask = tf.randomUniform(individual.weights[i].shape, 0, 1);
            const mutation = tf.randomUniform(
                individual.weights[i].shape,
                this.config.weightRange[0],
                this.config.weightRange[1]
            );

            const mutated = tf.where(
                mask.less(mutationRate),
                mutation,
                individual.weights[i]
            );

            tf.dispose([individual.weights[i], mask, mutation]);
            individual.weights[i] = mutated;
        }
    }

    /**
     * Mutação adaptativa
     */
    private async adaptiveMutation(individual: NeuralIndividual): Promise<void> {
        // Taxa de mutação adaptativa baseada no fitness
        const fitness = individual.fitness?.overall || 0;
        const mutationStrength = 0.2 * (1 - fitness); // Mais mutação para fitness baixo

        for (let i = 0; i < individual.weights.length; i++) {
            const noise = tf.randomNormal(individual.weights[i].shape, 0, mutationStrength);
            const mutated = individual.weights[i].add(noise);

            tf.dispose([individual.weights[i], noise]);
            individual.weights[i] = mutated;
        }
    }

    /**
     * Mutação polinomial
     */
    private async polynomialMutation(individual: NeuralIndividual): Promise<void> {
        const distributionIndex = 20;

        for (let i = 0; i < individual.weights.length; i++) {
            const weightsData = await individual.weights[i].data();
            const mutatedData = weightsData.map(w => {
                if (Math.random() < 0.1) { // 10% chance de mutação por peso
                    const u = Math.random();
                    let delta;

                    if (u < 0.5) {
                        delta = Math.pow(2 * u, 1 / (distributionIndex + 1)) - 1;
                    } else {
                        delta = 1 - Math.pow(2 * (1 - u), 1 / (distributionIndex + 1));
                    }

                    return w + delta * (this.config.weightRange[1] - this.config.weightRange[0]);
                }
                return w;
            });

            tf.dispose(individual.weights[i]);
            individual.weights[i] = tf.tensor(mutatedData, individual.weights[i].shape);
        }
    }

    /**
     * Mutação de arquitetura
     */
    private async architectureMutation(individual: NeuralIndividual): Promise<void> {
        const mutationType = Math.random();

        if (mutationType < 0.33 && individual.architecture.length > 2) {
            // Remove camada
            const removeIndex = Math.floor(Math.random() * (individual.architecture.length - 2)) + 1;
            individual.architecture.splice(removeIndex, 1);

            // Remove pesos correspondentes
            individual.weights.splice(removeIndex, 1);

        } else if (mutationType < 0.66 && individual.architecture.length < 8) {
            // Adiciona camada
            const insertIndex = Math.floor(Math.random() * (individual.architecture.length - 1)) + 1;
            const newLayer = this.generateRandomArchitecture()[0];
            individual.architecture.splice(insertIndex, 0, newLayer);

            // Adiciona pesos aleatórios
            const prevUnits = individual.architecture[insertIndex - 1].units;
            const newWeights = tf.randomUniform(
                [prevUnits, newLayer.units],
                this.config.weightRange[0],
                this.config.weightRange[1]
            );
            individual.weights.splice(insertIndex, 0, newWeights);

        } else {
            // Modifica camada existente
            const modifyIndex = Math.floor(Math.random() * (individual.architecture.length - 1)) + 1;
            const layer = individual.architecture[modifyIndex];

            // Modifica unidades
            const change = Math.random() > 0.5 ? 0.8 : 1.2;
            layer.units = Math.max(4, Math.min(512, Math.round(layer.units * change)));

            // Modifica função de ativação
            layer.activation = this.randomChoice(['relu', 'tanh', 'sigmoid', 'leaky_relu']);
        }
    }

    /**
     * Mutação de hiperparâmetros
     */
    private async hyperparameterMutation(individual: NeuralIndividual): Promise<void> {
        const mutations = [
            () => individual.learningRate *= this.randomInRange(0.8, 1.2),
            () => individual.batchSize = this.randomChoice([16, 32, 64, 128]),
            () => individual.dropoutRates = individual.dropoutRates.map(() => this.randomInRange(0, 0.5))
        ];

        const mutation = mutations[Math.floor(Math.random() * mutations.length)];
        mutation();
    }

    /**
     * Aplica especiação à população
     */
    private async applySpeciation(): Promise<void> {
        if (!this.config.enableSpeciation) return;

        // Calcula distância genética entre indivíduos
        const distanceMatrix = this.calculateGeneticDistance();

        // Agrupa em espécies usando threshold
        this.speciationClusters = this.clusterByDistance(distanceMatrix);

        // Ajusta fitness por nicho
        this.applyFitnessSharing();
    }

    /**
     * Calcula distância genética entre indivíduos
     */
    private calculateGeneticDistance(): number[][] {
        const distances: number[][] = [];

        for (let i = 0; i < this.population.length; i++) {
            distances[i] = [];
            for (let j = 0; j < this.population.length; j++) {
                if (i === j) {
                    distances[i][j] = 0;
                } else {
                    distances[i][j] = this.calculateIndividualDistance(
                        this.population[i],
                        this.population[j]
                    );
                }
            }
        }

        return distances;
    }

    /**
     * Calcula distância entre dois indivíduos
     */
    private calculateIndividualDistance(ind1: NeuralIndividual, ind2: NeuralIndividual): number {
        // Distância baseada em arquitetura e pesos
        let distance = 0;

        // Diferença no número de camadas
        const layerDiff = Math.abs(ind1.architecture.length - ind2.architecture.length);
        distance += layerDiff * 0.3;

        // Para camadas correspondentes, calcula diferença
        const minLayers = Math.min(ind1.architecture.length, ind2.architecture.length);
        for (let i = 0; i < minLayers; i++) {
            const layer1 = ind1.architecture[i];
            const layer2 = ind2.architecture[i];

            // Diferença no número de unidades
            const unitDiff = Math.abs(layer1.units - layer2.units) / Math.max(layer1.units, layer2.units);
            distance += unitDiff * 0.2;

            // Diferença nos pesos (se disponível)
            if (i < ind1.weights.length && i < ind2.weights.length) {
                const weightDiff = this.calculateWeightDistance(ind1.weights[i], ind2.weights[i]);
                distance += weightDiff * 0.5;
            }
        }

        return distance;
    }

    /**
     * Calcula distância entre pesos
     */
    private calculateWeightDistance(weights1: tf.Tensor, weights2: tf.Tensor): number {
        const diff = weights1.sub(weights2);
        const squared = diff.square();
        const mean = squared.mean();
        const distance = Math.sqrt(mean.dataSync()[0]);

        tf.dispose([diff, squared, mean]);
        return distance;
    }

    /**
     * Agrupa indivíduos por distância
     */
    private clusterByDistance(distanceMatrix: number[][]): Species[] {
        const clusters: Species[] = [];
        const assigned = new Set < number > ();

        for (let i = 0; i < this.population.length; i++) {
            if (assigned.has(i)) continue;

            const cluster: Species = {
                id: `species_${clusters.length}`,
                members: [this.population[i]],
                centroid: i,
                averageFitness: this.population[i].fitness?.overall || 0,
                diversity: 0
            };

            assigned.add(i);

            // Encontra indivíduos similares
            for (let j = i + 1; j < this.population.length; j++) {
                if (assigned.has(j)) continue;

                if (distanceMatrix[i][j] < this.config.speciationThreshold) {
                    cluster.members.push(this.population[j]);
                    assigned.add(j);
                }
            }

            // Calcula métricas do cluster
            if (cluster.members.length > 0) {
                cluster.averageFitness = cluster.members.reduce((sum, ind) =>
                    sum + (ind.fitness?.overall || 0), 0) / cluster.members.length;

                clusters.push(cluster);
            }
        }

        // Atribui speciesId aos indivíduos
        clusters.forEach((cluster, clusterIndex) => {
            cluster.members.forEach(ind => {
                ind.speciesId = cluster.id;
            });
        });

        return clusters;
    }

    /**
     * Aplica fitness sharing para preservar diversidade
     */
    private applyFitnessSharing(): void {
        if (this.config.nichingMethod !== 'fitnessSharing') return;

        const sharingRadius = this.config.speciationThreshold * 2;

        this.population.forEach((ind1, i) => {
            let nicheCount = 0;

            this.population.forEach((ind2, j) => {
                if (i !== j) {
                    // Calcula distância
                    const distance = this.calculateIndividualDistance(ind1, ind2);
                    if (distance < sharingRadius) {
                        nicheCount++;
                    }
                }
            });

            // Ajusta fitness
            if (nicheCount > 0 && ind1.fitness) {
                ind1.fitness.overall /= nicheCount;
            }
        });
    }

    /**
     * Inicializa ilhas de migração
     */
    private async initializeMigrationIslands(): Promise<void> {
        this.migrationIslands = [];
        const islandSize = Math.floor(this.config.populationSize / this.config.islandCount);

        for (let i = 0; i < this.config.islandCount; i++) {
            const island: MigrationIsland = {
                id: `island_${i}`,
                population: [],
                bestIndividual: null,
                migrationRate: this.config.migrationRate,
                topology: 'ring', // Topologia de conexão entre ilhas
                generationOffset: i * 10 // Deslocamento de geração para diversidade
            };

            // Distribui população entre ilhas
            const startIdx = i * islandSize;
            const endIdx = Math.min(startIdx + islandSize, this.config.populationSize);
            island.population = this.population.slice(startIdx, endIdx);

            // Encontra melhor indivíduo da ilha
            island.bestIndividual = island.population.reduce((best, current) =>
                (current.fitness?.overall || 0) > (best.fitness?.overall || 0) ? current : best
            );

            this.migrationIslands.push(island);
        }

        this.log(`${this.config.islandCount} ilhas de migração inicializadas`, 'info');
    }

    /**
     * Aplica migração entre ilhas
     */
    private async applyMigration(population: NeuralIndividual[]): Promise<void> {
        if (this.migrationIslands.length <= 1) return;

        const migrants: NeuralIndividual[] = [];

        // Coleta migrantes de cada ilha
        this.migrationIslands.forEach(island => {
            const migrantCount = Math.floor(island.population.length * island.migrationRate);

            for (let i = 0; i < migrantCount; i++) {
                // Seleciona aleatoriamente (com bias para melhores indivíduos)
                const pool = island.population.slice(0, Math.floor(island.population.length * 0.5));
                const migrant = pool[Math.floor(Math.random() * pool.length)];

                if (migrant) {
                    migrants.push(this.cloneIndividual(migrant));
                }
            }
        });

        // Distribui migrantes entre ilhas (topologia ring)
        for (let i = 0; i < this.migrationIslands.length; i++) {
            const sourceIsland = this.migrationIslands[i];
            const targetIsland = this.migrationIslands[(i + 1) % this.migrationIslands.length];

            // Substitui piores indivíduos da ilha alvo por migrantes
            targetIsland.population.sort((a, b) =>
                (a.fitness?.overall || 0) - (b.fitness?.overall || 0)
            );

            const migrant = migrants[i % migrants.length];
            if (migrant && targetIsland.population.length > 0) {
                // Remove pior indivíduo
                const worstIndex = 0;
                tf.dispose(targetIsland.population[worstIndex].weights);
                targetIsland.population[worstIndex] = migrant;

                // Atualiza melhor indivíduo
                targetIsland.bestIndividual = targetIsland.population.reduce((best, current) =>
                    (current.fitness?.overall || 0) > (best.fitness?.overall || 0) ? current : best
                );
            }
        }

        this.log(`Migração aplicada: ${migrants.length} indivíduos migrados`, 'debug');
        this.emit('migrationApplied', { migrantCount: migrants.length });
    }

    /**
     * Aplica treinamento híbrido (evolução + gradiente)
     */
    private async applyHybridTraining(population: NeuralIndividual[]): Promise<void> {
        const trainingCount = Math.floor(population.length * this.config.hybridTrainingRatio);
        const candidates = population.slice(0, trainingCount); // Treina os melhores

        const trainingPromises = candidates.map(async (individual, index) => {
            try {
                // Converte indivíduo para modelo TensorFlow
                const model = await this.individualToModel(individual);

                // Cria dados de treinamento sintéticos baseados no fitness
                const syntheticData = await this.generateSyntheticTrainingData(individual);

                // Treina por algumas épocas
                await model.fit(syntheticData.features, syntheticData.labels, {
                    epochs: 3,
                    batchSize: individual.batchSize,
                    verbose: 0,
                    callbacks: [{
                        onEpochEnd: (epoch, logs) => {
                            this.emit('hybridTrainingProgress', {
                                individualId: individual.id,
                                epoch,
                                loss: logs?.loss || 0,
                                index,
                                total: candidates.length
                            });
                        }
                    }]
                });

                // Atualiza pesos do indivíduo
                individual.weights = model.getWeights();

                // Avalia fitness atualizado
                individual.fitness = await this.fitnessEvaluator.evaluate(individual);

                tf.dispose(model);

            } catch (error) {
                this.log(`Treinamento híbrido falhou para ${individual.id}: ${error.message}`, 'debug');
            }
        });

        await Promise.allSettled(trainingPromises);

        this.log(`Treinamento híbrido aplicado a ${candidates.length} indivíduos`, 'info');
    }

    /**
     * Converte indivíduo para modelo TensorFlow
     */
    private async individualToModel(individual: NeuralIndividual): Promise<tf.LayersModel> {
        const layers: tf.layers.Layer[] = [];
        let inputShape: number[] = [20]; // Shape de input padrão

        individual.architecture.forEach((layerConfig, index) => {
            let layer: tf.layers.Layer;

            switch (layerConfig.type) {
                case 'dense':
                    layer = tf.layers.dense({
                        units: layerConfig.units,
                        activation: layerConfig.activation,
                        kernelInitializer: layerConfig.kernelInitializer,
                        useBias: layerConfig.useBias
                    });
                    break;

                case 'lstm':
                    layer = tf.layers.lstm({
                        units: layerConfig.units,
                        activation: layerConfig.activation,
                        kernelInitializer: layerConfig.kernelInitializer,
                        returnSequences: index < individual.architecture.length - 2
                    });
                    break;

                case 'gru':
                    layer = tf.layers.gru({
                        units: layerConfig.units,
                        activation: layerConfig.activation,
                        kernelInitializer: layerConfig.kernelInitializer,
                        returnSequences: index < individual.architecture.length - 2
                    });
                    break;

                case 'conv1d':
                    layer = tf.layers.conv1d({
                        filters: layerConfig.units,
                        kernelSize: 3,
                        activation: layerConfig.activation,
                        kernelInitializer: layerConfig.kernelInitializer
                    });
                    break;
            }

            layers.push(layer);

            if (individual.dropoutRates[index] > 0 && index < individual.architecture.length - 1) {
                layers.push(tf.layers.dropout({ rate: individual.dropoutRates[index] }));
            }
        });

        const model = tf.sequential({ layers });
        model.compile({
            optimizer: tf.train.adam(individual.learningRate),
            loss: 'categoricalCrossentropy',
            metrics: ['accuracy']
        });

        // Define pesos
        model.setWeights(individual.weights);

        return model;
    }

    /**
     * Gera dados de treinamento sintéticos
     */
    private async generateSyntheticTrainingData(individual: NeuralIndividual): Promise<{
        features: tf.Tensor;
        labels: tf.Tensor;
    }> {
        // Baseado no fitness, gera dados que reforçam comportamentos positivos
        const sampleCount = 100;
        const featureCount = 20;

        const features = tf.randomNormal([sampleCount, featureCount]);

        // Labels baseados no comportamento do indivíduo
        const fitness = individual.fitness?.metrics || {};
        const buyProbability = fitness.winRate || 0.5;

        const labels = tf.tidy(() => {
            const random = tf.randomUniform([sampleCount, 1]);
            const buyMask = random.less(buyProbability);

            return tf.where(
                buyMask,
                tf.tensor2d([[1, 0, 0]]).tile([sampleCount, 1]), // BUY
                tf.tensor2d([[0, 0, 1]]).tile([sampleCount, 1])  // HOLD
            );
        });

        return { features, labels };
    }

    /**
     * Adiciona indivíduo ao hall da fama
     */
    private addToHallOfFame(individual: NeuralIndividual): void {
        const entry: HallOfFameEntry = {
            individual: { ...individual, weights: [] }, // Não armazenar pesos completos
            generation: this.generation,
            fitness: individual.fitness!,
            timestamp: new Date(),
            rank: this.hallOfFame.length + 1
        };

        this.hallOfFame.push(entry);

        // Mantém tamanho fixo
        if (this.hallOfFame.length > this.config.archiveSize) {
            this.hallOfFame.sort((a, b) => b.fitness.overall - a.fitness.overall);
            this.hallOfFame = this.hallOfFame.slice(0, this.config.archiveSize);
        }

        this.emit('hallOfFameUpdated', { entry, hallSize: this.hallOfFame.length });
    }

    /**
     * Atualiza taxas adaptativas
     */
    private updateAdaptiveRates(improvement: number): void {
        const generationsSinceImprovement = this.generation - this.adaptiveRates.lastImprovement;

        // Aumenta taxa de mutação se não houver melhoria há muitas gerações
        if (generationsSinceImprovement > 20) {
            this.adaptiveRates.mutationRate = Math.min(0.5, this.adaptiveRates.mutationRate * 1.2);
            this.adaptiveRates.crossoverRate = Math.max(0.3, this.adaptiveRates.crossoverRate * 0.9);
        }

        // Reduz taxa de mutação se houver melhoria consistente
        if (improvement > 0 && generationsSinceImprovement <= 5) {
            this.adaptiveRates.mutationRate = Math.max(0.01, this.adaptiveRates.mutationRate * 0.95);
            this.adaptiveRates.crossoverRate = Math.min(0.95, this.adaptiveRates.crossoverRate * 1.05);
        }
    }

    /**
     * Coleta métricas da população
     */
    private collectPopulationMetrics(): PopulationMetrics {
        const fitnessValues = this.population
            .map(ind => ind.fitness?.overall || 0)
            .filter(f => f > 0);

        const averageFitness = fitnessValues.length > 0
            ? fitnessValues.reduce((a, b) => a + b, 0) / fitnessValues.length
            : 0;

        const maxFitness = Math.max(...fitnessValues);
        const minFitness = Math.min(...fitnessValues);

        // Calcula diversidade genética
        const diversity = this.calculatePopulationDiversity();

        return {
            size: this.population.length,
            averageFitness,
            maxFitness,
            minFitness,
            fitnessStd: this.calculateStandardDeviation(fitnessValues),
            diversity,
            ageRange: [Math.min(...this.population.map(ind => ind.age)),
            Math.max(...this.population.map(ind => ind.age))],
            speciesCount: this.speciationClusters.length
        };
    }

    /**
     * Calcula diversidade da população
     */
    private calculatePopulationDiversity(): number {
        if (this.population.length <= 1) return 1;

        let totalDistance = 0;
        let pairCount = 0;

        for (let i = 0; i < this.population.length; i++) {
            for (let j = i + 1; j < this.population.length; j++) {
                totalDistance += this.calculateIndividualDistance(this.population[i], this.population[j]);
                pairCount++;
            }
        }

        return pairCount > 0 ? totalDistance / pairCount : 0;
    }

    /**
     * Calcula convergência
     */
    private calculateConvergence(): number {
        if (this.convergenceHistory.length < 2) return 0;

        const recent = this.convergenceHistory.slice(-5);
        const improvements = recent.slice(1).map((curr, i) =>
            Math.abs(curr.bestFitness - recent[i].bestFitness)
        );

        const avgImprovement = improvements.reduce((a, b) => a + b, 0) / improvements.length;
        return avgImprovement;
    }

    /**
     * Verifica se população convergiu
     */
    private checkConvergence(metrics: EvolutionMetrics): boolean {
        this.convergenceHistory.push({
            generation: metrics.generation,
            bestFitness: metrics.bestFitness,
            averageFitness: metrics.averageFitness,
            diversity: metrics.diversity
        });

        // Mantém histórico limitado
        if (this.convergenceHistory.length > 20) {
            this.convergenceHistory.shift();
        }

        // Verifica critérios de convergência
        const convergedByFitness = metrics.fitnessImprovement < this.config.convergenceThreshold;
        const convergedByDiversity = metrics.diversity < this.config.diversityThreshold;
        const maxGenerationsReached = this.generation >= this.config.maxGenerations;

        return (convergedByFitness && convergedByDiversity) || maxGenerationsReached;
    }

    /**
     * Conta mutações na população
     */
    private countMutations(population: NeuralIndividual[]): number {
        return population.filter(ind =>
            ind.metadata.parentIds && ind.metadata.parentIds.length > 0
        ).length;
    }

    /**
     * Conta crossovers na população
     */
    private countCrossovers(population: NeuralIndividual[]): number {
        return population.filter(ind =>
            ind.metadata.parentIds && ind.metadata.parentIds.length === 2
        ).length;
    }

    /**
     * Salva checkpoint da evolução
     */
    private async saveCheckpoint(generation: number): Promise<void> {
        try {
            const checkpoint: EvolutionCheckpoint = {
                generation,
                population: this.population.map(ind => ({
                    ...ind,
                    weights: [] // Não salvar pesos no checkpoint
                })),
                bestIndividual: this.bestIndividual ? {
                    ...this.bestIndividual,
                    weights: []
                } : null,
                hallOfFame: this.hallOfFame,
                convergenceHistory: this.convergenceHistory,
                config: this.config,
                timestamp: new Date(),
                metrics: this.collectPopulationMetrics()
            };

            await this.modelArchiver.saveCheckpoint(checkpoint, `evolution_gen_${generation}`);

            this.log(`Checkpoint salvo para geração ${generation}`, 'info');
            this.emit('checkpointSaved', { generation });

        } catch (error) {
            this.log(`Falha ao salvar checkpoint: ${error.message}`, 'error');
        }
    }

    /**
     * Carrega checkpoint da evolução
     */
    async loadCheckpoint(checkpointId: string): Promise<{
        success: boolean;
        message: string;
        checkpoint: EvolutionCheckpoint;
    }> {
        try {
            const checkpoint = await this.modelArchiver.loadCheckpoint(checkpointId);

            this.population = checkpoint.population;
            this.bestIndividual = checkpoint.bestIndividual;
            this.hallOfFame = checkpoint.hallOfFame;
            this.convergenceHistory = checkpoint.convergenceHistory;
            this.generation = checkpoint.generation;

            // Reavalia população
            await this.evaluatePopulationFitness();
            this.sortPopulation();

            this.log(`Checkpoint carregado: ${checkpointId} (Geração ${checkpoint.generation})`, 'info');
            this.emit('checkpointLoaded', { checkpoint });

            return {
                success: true,
                message: 'Checkpoint carregado com sucesso',
                checkpoint
            };

        } catch (error) {
            this.log(`Falha ao carregar checkpoint: ${error.message}`, 'error');
            return {
                success: false,
                message: `Falha ao carregar checkpoint: ${error.message}`,
                checkpoint: null
            };
        }
    }

    /**
     * Clona indivíduo
     */
    private cloneIndividual(individual: NeuralIndividual): NeuralIndividual {
        return {
            ...individual,
            weights: individual.weights.map(w => w.clone()),
            biases: individual.biases?.map(b => b ? b.clone() : null),
            metadata: {
                ...individual.metadata,
                parentIds: [...individual.metadata.parentIds]
            }
        };
    }

    /**
     * Ordena população por fitness
     */
    private sortPopulation(): void {
        this.population.sort((a, b) =>
            (b.fitness?.overall || 0) - (a.fitness?.overall || 0)
        );
    }

    /**
     * Utilitário: número aleatório em intervalo
     */
    private randomInRange(min: number, max: number): number {
        return Math.random() * (max - min) + min;
    }

    /**
     * Utilitário: inteiro aleatório em intervalo
     */
    private randomInt(min: number, max: number): number {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    /**
     * Utilitário: escolha aleatória de array
     */
    private randomChoice<T>(array: T[]): T {
        return array[Math.floor(Math.random() * array.length)];
    }

    /**
     * Utilitário: desvio padrão
     */
    private calculateStandardDeviation(values: number[]): number {
        if (values.length === 0) return 0;

        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;

        return Math.sqrt(variance);
    }

    /**
     * Obtém estatísticas da evolução
     */
    getEvolutionStats(): EvolutionStats {
        return {
            generation: this.generation,
            populationSize: this.population.length,
            bestFitness: this.bestIndividual?.fitness?.overall || 0,
            averageFitness: this.collectPopulationMetrics().averageFitness,
            diversity: this.calculatePopulationDiversity(),
            hallOfFameSize: this.hallOfFame.length,
            speciesCount: this.speciationClusters.length,
            islandCount: this.migrationIslands.length,
            convergenceRate: this.calculateConvergence(),
            adaptiveRates: this.adaptiveRates,
            evolutionHistory: this.evolutionHistory.slice(-10)
        };
    }

    /**
     * Exporta melhor indivíduo como modelo treinável
     */
    async exportBestModel(): Promise<{
        success: boolean;
        model: any;
        architecture: LayerArchitecture[];
        fitness: FitnessScore;
        metadata: any;
    }> {
        if (!this.bestIndividual) {
            throw new Error('Nenhum melhor indivíduo disponível');
        }

        try {
            const model = await this.individualToModel(this.bestIndividual);

            return {
                success: true,
                model,
                architecture: this.bestIndividual.architecture,
                fitness: this.bestIndividual.fitness!,
                metadata: {
                    generation: this.generation,
                    individualId: this.bestIndividual.id,
                    exportDate: new Date(),
                    config: this.config
                }
            };

        } catch (error) {
            this.log(`Falha ao exportar melhor modelo: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * Reinicia sistema de evolução
     */
    reset(): void {
        // Libera memória dos tensores
        this.population.forEach(ind => {
            ind.weights.forEach(w => tf.dispose(w));
            ind.biases?.forEach(b => b && tf.dispose(b));
        });

        // Reseta estado
        this.population = [];
        this.generation = 0;
        this.bestIndividual = null;
        this.hallOfFame = [];
        this.speciationClusters = [];
        this.migrationIslands = [];
        this.convergenceHistory = [];
        this.evolutionHistory = [];
        this.adaptiveRates = {
            mutationRate: this.config.mutationRate,
            crossoverRate: this.config.crossoverRate,
            lastImprovement: 0
        };

        this.log('Sistema de evolução reiniciado', 'info');
        this.emit('reset');
    }

    /**
     * Logging com níveis
     */
    private log(message: string, level: 'debug' | 'info' | 'warn' | 'error' = 'info'): void {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] [ContinuousEvolution] [${level.toUpperCase()}] ${message}`;

        this.emit('log', { level, message, timestamp });

        if (level === 'error') console.error(logMessage);
        else if (level === 'warn') console.warn(logMessage);
        else if (level === 'info') console.info(logMessage);
        else console.debug(logMessage);
    }
}

// Interfaces e Tipos

interface NeuralIndividual {
    id: string;
    generation: number;
    architecture: LayerArchitecture[];
    weights: tf.Tensor[];
    biases: tf.Tensor[] | null;
    activationFunctions: string[];
    dropoutRates: number[];
    learningRate: number;
    batchSize: number;
    fitness: FitnessScore | null;
    metrics: { [key: string]: number };
    metadata: {
        creationDate: Date;
        parentIds: string[];
    };
    age: number;
    speciesId: string | null;
    islandId: number;
}

interface LayerArchitecture {
    type: 'dense' | 'lstm' | 'gru' | 'conv1d';
    units: number;
    activation: string;
    kernelInitializer: string;
    useBias: boolean;
}

interface FitnessScore {
    overall: number;
    metrics: {
        sharpe?: number;
        maxDrawdown?: number;
        profitFactor?: number;
        winRate?: number;
        consistency?: number;
        [key: string]: number | undefined;
    };
}

interface Species {
    id: string;
    members: NeuralIndividual[];
    centroid: number;
    averageFitness: number;
    diversity: number;
}

interface MigrationIsland {
    id: string;
    population: NeuralIndividual[];
    bestIndividual: NeuralIndividual | null;
    migrationRate: number;
    topology: 'ring' | 'mesh' | 'star';
    generationOffset: number;
}

interface HallOfFameEntry {
    individual: NeuralIndividual;
    generation: number;
    fitness: FitnessScore;
    timestamp: Date;
    rank: number;
}

interface ConvergenceMetrics {
    generation: number;
    bestFitness: number;
    averageFitness: number;
    diversity: number;
}

interface EvolutionHistory {
    generation: number;
    metrics: EvolutionMetrics;
    timestamp: Date;
    bestIndividual: NeuralIndividual;
}

interface AdaptiveRates {
    mutationRate: number;
    crossoverRate: number;
    lastImprovement: number;
}

interface EvolutionMetrics {
    generation: number;
    duration: number;
    fitnessImprovement: number;
    bestFitness: number;
    averageFitness: number;
    diversity: number;
    convergence: number;
    speciationCount: number;
    mutationCount: number;
    crossoverCount: number;
}

interface PopulationMetrics {
    size: number;
    averageFitness: number;
    maxFitness: number;
    minFitness: number;
    fitnessStd: number;
    diversity: number;
    ageRange: [number, number];
    speciesCount: number;
}

interface EvolutionCheckpoint {
    generation: number;
    population: NeuralIndividual[];
    bestIndividual: NeuralIndividual | null;
    hallOfFame: HallOfFameEntry[];
    convergenceHistory: ConvergenceMetrics[];
    config: any;
    timestamp: Date;
    metrics: PopulationMetrics;
}

interface EvolutionStats {
    generation: number;
    populationSize: number;
    bestFitness: number;
    averageFitness: number;
    diversity: number;
    hallOfFameSize: number;
    speciesCount: number;
    islandCount: number;
    convergenceRate: number;
    adaptiveRates: AdaptiveRates;
    evolutionHistory: EvolutionHistory[];
}

export default ContinuousEvolution;