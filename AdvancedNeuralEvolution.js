
export const MutationType = Object.freeze({
    ADD_NEURON: "add_neuron",
    MODIFY_WEIGHTS: "modify_weights",
    QUANTUM_SUPERPOSITION: "quantum_superposition"
});

export const ActivationFunction = Object.freeze({
    RELU: "relu",
    SIGMOID: "sigmoid",
    GELU: "gelu"
});

export class AdvancedNeuralLayer {
    constructor(config = {}) {
        this.id = `layer_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        this.neurons = config.neurons || 32;
        this.activation = config.activation || ActivationFunction.RELU;
        this.fitness = 0;
        this.age = 0;
    }

    activate(input) {
        return input.map(x => Math.tanh(x));
    }

    mutate(type, intensity) {
        console.log(`🧬 Mutação aplicada: ${type} na intensidade ${intensity}`);
    }
}
