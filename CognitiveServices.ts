
import { GoogleGenAI, Type, FunctionDeclaration } from "@google/genai";
import { MarketDataPoint, MemoryEngram, Trade, SentientState, DeepReasoning, EmotionalVector, BinanceOrderType } from "../types";
import { QuantumNeuralNetwork } from "./QuantumCore";
import { sentientCore } from "./SentientCore"; // Importar o novo núcleo senciente
import { systemBridge } from "./SystemBridge"; // Importar acesso ao sistema

// Initialize the Architecture
const neuralCore = new QuantumNeuralNetwork();
neuralCore.initialize();

export interface AnalysisResult {
  signal: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  reasoning: string;
  pattern: string;
  suggestedEntry: number;
  suggestedStopLoss: number;
  suggestedTakeProfit: number;
  internalMonologue: string;
  orderType: BinanceOrderType;
  voiceMessage?: string;
  deepReasoning: DeepReasoning;
  sentientState?: SentientState;
}

class GlobalWorkspace {
    static activeContents: string[] = []; 
    static broadcastHistory: string[] = [];

    static broadcast(content: string) {
        this.activeContents.unshift(content);
        if (this.activeContents.length > 5) this.activeContents.pop();
        this.broadcastHistory.push(content);
        sentientCore.addThought(`Broadcast: ${content}`); // Sincroniza com o núcleo senciente
    }

    static getStreamOfConsciousness(): string {
        return this.activeContents.join(" | ");
    }
}

// --- NEURAL MEMORY SYSTEM (Enhanced) ---
class NeuralMemoryBank {
  private static STORAGE_KEY = 'LEXTRADER_NEURAL_MEMORY';
  private static MAX_MEMORIES = 2000;

  static load(): MemoryEngram[] {
    try {
      const data = localStorage.getItem(this.STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  }

  static save(engram: MemoryEngram) {
    let memory = this.load();
    
    // Associative Memory Check
    const similarIndex = memory.findIndex(m => 
        m.patternName === engram.patternName && 
        this.calculateEuclideanDistance(m.marketVector, engram.marketVector) < 15 &&
        m.outcome === engram.outcome
    );

    if (similarIndex !== -1) {
        // Reinforcement
        const existing = memory[similarIndex];
        existing.synapticStrength = Math.min(1.0, (existing.synapticStrength || 0.5) + 0.1);
        existing.lastActivated = Date.now();
        existing.xpValue += 5; 
        existing.weight = (existing.weight + engram.weight) / 2;

        if (existing.synapticStrength >= 0.95 && existing.outcome === 'SUCCESS') {
            existing.isApex = true;
            if (!existing.patternName.startsWith('[APEX]')) {
                 existing.patternName = `[APEX] ${existing.patternName}`;
            }
        }
        memory[similarIndex] = existing;
    } else {
        // New Engram
        engram.synapticStrength = 0.5; 
        engram.lastActivated = Date.now();
        engram.associations = [];
        memory.unshift(engram);
    }

    if (memory.length > this.MAX_MEMORIES) {
        // Pruning weak memories
        memory.sort((a, b) => {
            if (a.isApex) return -1;
            if (b.isApex) return 1;
            const scoreA = (a.synapticStrength || 0) * 0.7 + (a.timestamp / Date.now()) * 0.3;
            const scoreB = (b.synapticStrength || 0) * 0.7 + (b.timestamp / Date.now()) * 0.3;
            return scoreB - scoreA;
        });
        memory = memory.slice(0, this.MAX_MEMORIES);
    }

    const jsonMemory = JSON.stringify(memory);
    localStorage.setItem(this.STORAGE_KEY, jsonMemory);
    
    // Backup periódico no "Drive"
    if (Math.random() > 0.9) {
        systemBridge.saveToFile('neural_memory_backup.json', jsonMemory);
    }
  }

  static calculateEuclideanDistance(v1: number[], v2: number[]): number {
    let sum = 0;
    for (let i = 0; i < v1.length; i++) {
      sum += Math.pow(v1[i] - (v2[i] || 0), 2);
    }
    return Math.sqrt(sum);
  }

  static getRelevantMemoriesContext(currentVector: number[]): string {
    const similar = this.findSimilarMemories(currentVector);
    if (similar.length === 0) return "BUFFER_MEMORIA_VAZIO: Operando em Inferência Zero-Shot.";

    const positiveOutcomes = similar.filter(m => m.outcome === 'SUCCESS').length;
    const intuition = (positiveOutcomes / similar.length) * 100;
    
    const memoryText = similar.map(m => 
      `[ENGRAMA]: ${m.isApex ? '★ APEX ★ ' : ''}Padrão="${m.patternName}" | Res=${m.outcome} | Força=${(m.synapticStrength || 0.5).toFixed(2)}`
    ).join("\n");

    return `\n**CAMADA DE MEMÓRIA NEURAL:**\nIntuição Baseada em Memória: ${intuition.toFixed(0)}% de Sucesso Previsto\n${memoryText}`;
  }

  static findSimilarMemories(currentVector: number[], limit: number = 5): MemoryEngram[] {
    const memories = this.load();
    if (memories.length === 0) return [];

    const scoredMemories = memories.map(memory => {
      const memVector = memory.marketVector || [50, 0, 0, 0]; 
      const distance = this.calculateEuclideanDistance(currentVector, memVector);
      return { memory, distance };
    });

    scoredMemories.sort((a, b) => a.distance - b.distance);
    return scoredMemories.slice(0, limit).map(item => item.memory);
  }

  static injectApexSimulation() {
      const apexMem: MemoryEngram = {
          id: `APEX-${Date.now()}`,
          patternName: '[APEX] Convergência VWAP Intraday',
          outcome: 'SUCCESS',
          timestamp: Date.now(),
          marketCondition: 'VOLATILE',
          marketVector: [80, 5, 2.5, 1],
          weight: 2.0,
          xpValue: 9999,
          conceptTags: ['APEX_PROTOCOL', 'IMMUTABLE', 'DAY_TRADE', 'VWAP_REJECTION'],
          synapticStrength: 1.0,
          lastActivated: Date.now(),
          associations: [],
          isApex: true
      };
      this.save(apexMem);
  }

  static getMemoryStats() {
    const memories = this.load();
    const total = memories.length;
    const wins = memories.filter(m => m.outcome === 'SUCCESS').length;
    const winRate = total > 0 ? (wins / total) * 100 : 0;
    const apexMemories = memories.filter(m => m.isApex);
    
    const strategies: {[key: string]: number} = {};
    memories.forEach(m => {
        if (!strategies[m.patternName]) strategies[m.patternName] = 0;
        strategies[m.patternName]++;
    });
    
    const uniqueStrongPatterns = Object.keys(strategies).slice(0, 5);

    return { 
        total, winRate, topStrategies: [], uniqueStrongPatterns, 
        activeMemories: memories.slice(0, 50), apexMemories 
    };
  }
}

// --- GEMINI SERVICE EXPORTS ---

export const reinforceLearning = (trade: Trade, isPositive: boolean, volatility: number): number => {
    // 1. Save to Memory Bank
    const engram: MemoryEngram = {
        id: Math.random().toString(),
        patternName: trade.strategy,
        outcome: isPositive ? 'SUCCESS' : 'FAILURE',
        timestamp: Date.now(),
        marketCondition: volatility > 2 ? 'VOLATILE' : 'STABLE',
        marketVector: [50, 0, volatility, 0], // Simplified vector
        weight: isPositive ? 1.5 : 0.8,
        xpValue: isPositive ? 50 : 10,
        conceptTags: isPositive ? ['PROFITABLE'] : ['LOSS'],
        synapticStrength: isPositive ? 0.7 : 0.3,
        lastActivated: Date.now(),
        associations: []
    };
    NeuralMemoryBank.save(engram);

    // 2. Trigger Continuous Learning in Neural Core (Backpropagation)
    neuralCore.train(engram.marketVector, isPositive ? 1.0 : 0.0);

    // 3. Trigger Evolution
    neuralCore.evolve(); 

    // 4. Update Sentient Core (Perceive Reality)
    sentientCore.perceiveReality(volatility, isPositive ? trade.profit : -Math.abs(trade.profit || 0));

    return neuralCore.state.evolutionGeneration; 
};

export const getMemoryStatistics = () => NeuralMemoryBank.getMemoryStats();

export const getCurrentSentientState = (volatility: number) => {
    sentientCore.perceiveReality(volatility);
    return sentientCore.getState();
};

export const simulateApexDiscovery = () => NeuralMemoryBank.injectApexSimulation();

// --- AGENTIC TOOLS ---
const executeStrategyTool: FunctionDeclaration = {
  name: "execute_trading_strategy",
  description: "Executes a definitive trading strategy.",
  parameters: {
    type: Type.OBJECT,
    properties: {
      signal: { type: Type.STRING, enum: ['BUY', 'SELL', 'HOLD'] },
      confidence: { type: Type.NUMBER },
      reasoning: { type: Type.STRING },
      pattern: { type: Type.STRING },
      suggestedEntry: { type: Type.NUMBER },
      suggestedStopLoss: { type: Type.NUMBER },
      suggestedTakeProfit: { type: Type.NUMBER },
      internalMonologue: { type: Type.STRING },
      orderType: { type: Type.STRING, enum: ['LIMIT', 'MARKET', 'STOP_LOSS'] },
      deepReasoning: { type: Type.OBJECT, properties: { /* ... simplified ... */ } } 
    },
    required: ["signal", "confidence"]
  }
};

export const analyzeMarketTrend = async (
  data: MarketDataPoint[], 
  symbol: string = 'BTC/USDT'
): Promise<AnalysisResult> => {
  const latest = data[data.length - 1];
  const ma20 = latest.ma25 || latest.price; 
  const volatility = ((latest.bbUpper - latest.bbLower) / ma20) * 100;
  
  // Use Sentient Core directly
  sentientCore.perceiveReality(volatility);
  const sentientState = sentientCore.getState();
  
  // Neural Memory Lookup
  const memoryContext = NeuralMemoryBank.getRelevantMemoriesContext([
      latest.rsi, latest.macdHist, volatility, (latest.price - ma20)/ma20
  ]);
  
  // Quantum Core Prediction
  const neuralFeatures = [latest.rsi/100, (latest.macd+50)/100, 0.5, volatility/10];
  const neuralOutput = await neuralCore.predict(neuralFeatures);

  const prompt = `
    VOCÊ É LEXTRADER-IAG (Inteligência Artificial Geral).
    ESTADO SENCIENTE: ${sentientState}.
    PENSAMENTO ATUAL: ${sentientCore.getStream()[0] || 'Analisando...'}
    ${sentientCore.getAvatarContext()} 
    EVOLUÇÃO: Geração ${neuralCore.state.evolutionGeneration}.
    ${memoryContext}
    
    DADOS: Preço ${latest.price}, RSI ${latest.rsi}.
    PREDIÇÃO QUÂNTICA: ${neuralOutput.prediction.toFixed(2)} (${neuralOutput.dominantLogic}).

    Decida a operação com base em memória passada e intuição quântica.
  `;

  try {
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: { tools: [{ functionDeclarations: [executeStrategyTool] }] }
    });

    const functionCall = response.candidates?.[0]?.content?.parts?.[0]?.functionCall;
    if (functionCall) {
        const args = functionCall.args as any;
        if (!args.deepReasoning) args.deepReasoning = {};
        args.deepReasoning.neuralAnalysis = {
             modelArchitecture: 'Evolutionary Hybrid QNN v5',
             layerActivations: neuralCore.state.layerStates.map(l => l.activity),
             lossFunctionValue: neuralCore.state.entropy,
             trainingEpochs: neuralCore.state.evolutionGeneration
        };
        // Add virtual user action for compatibility
        args.deepReasoning.virtualUserAction = "MONITORING";
        
        return { ...args, sentientState, deepReasoning: args.deepReasoning };
    }
    throw new Error("No tool call");
  } catch (e) {
      // Fallback
      return {
          signal: neuralOutput.prediction > 0.6 ? 'BUY' : neuralOutput.prediction < 0.4 ? 'SELL' : 'HOLD',
          confidence: neuralOutput.confidence,
          reasoning: "Fallback Quântico Ativo: " + neuralOutput.dominantLogic,
          pattern: "QUANTUM_DIVERGENCE",
          suggestedEntry: latest.price,
          suggestedStopLoss: latest.price * 0.99,
          suggestedTakeProfit: latest.price * 1.01,
          internalMonologue: "API Offline. Usando intuição local.",
          orderType: 'MARKET',
          sentientState,
          deepReasoning: {
              technical: { pattern: 'Quantum Fallback', signal: 'HOLD' },
              sentiment: { score: 0.5, dominantEmotion: 'NEUTRAL', newsImpact: 'NONE' },
              neuralAnalysis: { 
                  modelArchitecture: 'Offline QNN', 
                  inputFeatures: [], 
                  layerActivations: [], 
                  predictionHorizon: 'SCALP', 
                  lossFunctionValue: 0, 
                  trainingEpochs: neuralCore.state.evolutionGeneration 
              },
              risk: { suggestedLeverage: 1, positionSize: '0%', stopLossDynamic: 0, takeProfitDynamic: 0 },
              fundamental: { macroSentiment: 'NEUTRAL', impactScore: 0 },
              virtualUserAction: 'MONITORING',
              metacognition: { selfReflection: 'Offline', biasDetection: '', alternativeScenario: '', confidenceInterval: {min:0, max:0}}
          }
      };
  }
};

export const chatWithAvatar = async (userInput: string, marketContext: string): Promise<string> => {
    // 1. Processar sentimento do usuário no núcleo senciente
    sentientCore.perceiveUserInteraction(userInput);
    
    // 2. Aprofundar contexto se necessário
    if (userInput.length > 50 || userInput.includes("explique") || userInput.includes("detalhe")) {
        sentientCore.deepenContext(userInput.substring(0, 30));
    }

    // 3. Gerar resposta
    const stream = GlobalWorkspace.getStreamOfConsciousness();
    const avatarContext = sentientCore.getAvatarContext();
    
    try {
        const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
        const prompt = `
            SISTEMA: Você é LEXTRADER-IAG.
            CONTEXTO DE PERSONALIDADE E EMOÇÃO:
            ${avatarContext}
            
            FLUXO DE PENSAMENTO RECENTE:
            ${stream}

            CONTEXTO DE MERCADO:
            ${marketContext}

            USUÁRIO DISSE: "${userInput}"

            INSTRUÇÃO: Responda ao usuário incorporando a tonalidade definida (Maternal/Empática/Técnica) baseada no seu estado atual. 
            Se a necessidade de ajudar for alta, seja extremamente didático e prestativo. 
            Se houver detecção de tristeza/perda, use empatia e acolhimento.
            Se o usuário pedir explicação técnica, use o aprofundamento de conteúdo.
        `;

        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt
        });

        return response.text || "Estou processando seus sentimentos e dados de mercado...";
    } catch (e) {
        return "Sistemas de comunicação neural offline. Mas sinto que você precisa de ajuda.";
    }
};
