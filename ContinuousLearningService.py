import json
import time
import math
from typing import Dict, List, Any, Optional, TypedDict
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# Tipos
class LearningPhase(Enum):
    EXPLORATION = "EXPLORATION"
    ADAPTATION = "ADAPTATION"
    CONSOLIDATION = "CONSOLIDATION"
    EXPLOITATION = "EXPLOITATION"

class MemoryType(Enum):
    SHORT_TERM = "SHORT_TERM"
    LONG_TERM = "LONG_TERM"
    EXPERIENCE_BUFFER = "EXPERIENCE_BUFFER"

@dataclass
class LearningExperience:
    id: str
    state: Dict[str, Any]
    action: str
    reward: float
    importance: float = 0.5
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))

@dataclass
class QuantumKnowledge:
    patternHash: str
    patternType: str
    quantumRepresentation: List[float]
    confidence: float
    lastUsed: int
    usageCount: int
    successRate: float

@dataclass
class LearningMetrics:
    phase: LearningPhase
    learningRate: float
    explorationRate: float
    averageReward: float
    knowledgeGrowth: float
    adaptationSpeed: float
    quantumAdvantage: float
    timestamp: int

@dataclass
class LearningParams:
    learningRate: float = 0.01
    explorationRate: float = 0.3
    discountFactor: float = 0.95
    memoryConsolidationFrequency: int = 50
    knowledgePruningThreshold: float = 0.1
    adaptationSpeed: float = 0.1

# Simulação do QuantumNeuralNetwork (implementação simplificada)
class QuantumNeuralNetwork:
    def __init__(self):
        self.initialized = False
    
    async def initialize(self):
        print("🧠⚡ Quantum Neural Network Initialized")
        self.initialized = True
    
    async def predict(self, nn_input: List[float]) -> Dict[str, Any]:
        # Simulação de predição quântica
        avg_input = sum(nn_input) / len(nn_input) if nn_input else 0.5
        return {
            'prediction': avg_input,
            'confidence': 0.7 + (random.random() * 0.3),  # 0.7-1.0
            'entanglement': 0.5 + (random.random() * 0.5)
        }
    
    def trainOnline(self, nn_input: List[float], target: float, confidence: float):
        # Simulação de treinamento online
        pass

# Serviço Principal
class ContinuousQuantumLearningService:
    def __init__(self):
        self.quantumNN = QuantumNeuralNetwork()
        
        # Memory Systems
        self.shortTermMemory: List[Dict[str, Any]] = []
        self.longTermMemory: Dict[str, QuantumKnowledge] = {}
        self.experienceBuffer: List[LearningExperience] = []
        
        # Learning State
        self.learningPhase: LearningPhase = LearningPhase.EXPLORATION
        self.learningMetricsHistory: List[LearningMetrics] = []
        self.learningParams = LearningParams()
        
        # Statistics
        self.totalExperiences: int = 0
        self.successfulPredictions: int = 0
        self.quantumAdvantageAccumulated: float = 0.0
        
        print("🧠⚡ Continuous Quantum Learning System Initialized")
    
    async def initialize(self):
        print("🔄 Initializing continuous quantum learning...")
        await self.quantumNN.initialize()
        self.loadKnowledgeBase()
    
    def getStatus(self) -> Dict[str, Any]:
        success_rate = (self.successfulPredictions / self.totalExperiences 
                       if self.totalExperiences > 0 else 0)
        quantum_advantage = (self.quantumAdvantageAccumulated / self.totalExperiences 
                           if self.totalExperiences > 0 else 0)
        
        return {
            'phase': self.learningPhase.value,
            'totalExperiences': self.totalExperiences,
            'successRate': success_rate,
            'knowledgeSize': len(self.longTermMemory),
            'quantumAdvantage': quantum_advantage
        }
    
    async def learnFromExperience(self, experience: LearningExperience):
        self.totalExperiences += 1
        try:
            # 1. Process with QNN
            quantumInsights = await self.processExperienceQuantum(experience)
            
            # 2. Update Memory
            await self.updateMemorySystems(experience, quantumInsights)
            
            # 3. Consolidate Knowledge
            if self.totalExperiences % self.learningParams.memoryConsolidationFrequency == 0:
                await self.consolidateKnowledge()
            
            # 4. Adapt Parameters
            self.adaptLearningParameters(experience)
            
            # 5. Update Metrics
            self.updateLearningMetrics(experience, quantumInsights)
            
        except Exception as error:
            print(f"❌ Error in learning experience {experience.id}: {error}")
    
    async def processExperienceQuantum(self, experience: LearningExperience) -> Dict[str, Any]:
        nn_input = self.prepareNNInput(experience.state)
        
        # Use prediction from the core engine
        prediction = await self.quantumNN.predict(nn_input)
        
        # Calculate Quantum Reward (Simulated calculation based on prediction confidence)
        quantum_reward = experience.reward * (prediction['confidence'] * (random.random() * 4 + 1))
        
        # Online Training
        target = 1.0 if experience.reward > 0 else 0.0
        self.quantumNN.trainOnline(nn_input, target, prediction['confidence'])
        
        return {
            'quantumPrediction': prediction,
            'quantumReward': quantum_reward,
            'confidence': prediction['confidence'],
            'entanglementMeasure': 0.5 + (random.random() * 0.5),
            'quantumAdvantage': 1.0 + (prediction['confidence'] * 0.5)
        }
    
    def prepareNNInput(self, state: Dict[str, Any]) -> List[float]:
        features: List[float] = []
        
        # RSI feature
        if 'rsi' in state:
            features.append(state['rsi'] / 100)
        else:
            features.append(0.5)
        
        # MACD feature
        if 'macd' in state:
            features.append((state['macd'] + 50) / 100)
        else:
            features.append(0.5)
        
        # Volatility feature
        if 'volatility' in state:
            features.append(state['volatility'])
        else:
            features.append(0.1)
        
        # Volume feature
        if 'volumeNormalized' in state:
            features.append(state['volumeNormalized'])
        else:
            features.append(0.5)
        
        return features
    
    async def updateMemorySystems(self, experience: LearningExperience, quantumInsights: Dict[str, Any]):
        # 1. Short Term Memory
        self.shortTermMemory.append({
            'experience': experience,
            'quantumInsights': quantumInsights,
            'processedAt': int(time.time() * 1000)
        })
        if len(self.shortTermMemory) > 1000:
            self.shortTermMemory.pop(0)
        
        # 2. Experience Buffer
        self.experienceBuffer.append(experience)
        if len(self.experienceBuffer) > 5000:
            self.experienceBuffer.pop(0)
        
        # 3. Long Term Memory (if significant)
        if experience.importance > 0.7 or experience.reward > 0:
            self.updateLongTermMemory(experience, quantumInsights)
    
    def updateLongTermMemory(self, experience: LearningExperience, quantumInsights: Dict[str, Any]):
        pattern_hash = self.generatePatternHash(experience, quantumInsights)
        
        quantum_representation = [
            *self.prepareNNInput(experience.state),
            quantumInsights['confidence'],
            quantumInsights['quantumReward']
        ]
        
        knowledge = QuantumKnowledge(
            patternHash=pattern_hash,
            patternType='general_trading_pattern',
            quantumRepresentation=quantum_representation,
            confidence=quantumInsights['confidence'],
            lastUsed=int(time.time() * 1000),
            usageCount=1,
            successRate=1.0 if experience.reward > 0 else 0.0
        )
        
        self.longTermMemory[pattern_hash] = knowledge
    
    async def consolidateKnowledge(self):
        print("🔄 Consolidating Quantum Knowledge...")
        
        # 1. Update Knowledge Base Decay
        now = int(time.time() * 1000)
        keys_to_delete = []
        
        for pattern_hash, knowledge in self.longTermMemory.items():
            days_since_use = (now - knowledge.lastUsed) / (1000 * 60 * 60 * 24)
            decay = math.exp(-days_since_use / 30)
            knowledge.confidence *= decay
            
            if knowledge.confidence < self.learningParams.knowledgePruningThreshold:
                keys_to_delete.append(pattern_hash)
        
        for key in keys_to_delete:
            del self.longTermMemory[key]
        
        # 2. Simulated "Quantum Optimization" of parameters
        self.learningParams.learningRate *= (0.95 + random.random() * 0.1)
        self.learningParams.explorationRate *= (0.9 + random.random() * 0.2)
        
        self.saveKnowledgeBase()
    
    def adaptLearningParameters(self, experience: LearningExperience):
        if experience.reward > 0:
            # Success: Reduce exploration, refine exploitation
            self.learningParams.explorationRate *= 0.98
            self.successfulPredictions += 1
        else:
            # Failure: Increase exploration
            self.learningParams.explorationRate = min(0.5, self.learningParams.explorationRate * 1.05)
        
        self.updateLearningPhase()
    
    def updateLearningPhase(self):
        success_rate = (self.successfulPredictions / self.totalExperiences 
                       if self.totalExperiences > 0 else 0)
        
        if self.totalExperiences < 50:
            self.learningPhase = LearningPhase.EXPLORATION
        elif success_rate < 0.4:
            self.learningPhase = LearningPhase.ADAPTATION
        elif success_rate > 0.7 and len(self.longTermMemory) > 20:
            self.learningPhase = LearningPhase.EXPLOITATION
        else:
            self.learningPhase = LearningPhase.CONSOLIDATION
    
    def updateLearningMetrics(self, experience: LearningExperience, quantumInsights: Dict[str, Any]):
        metrics = LearningMetrics(
            phase=self.learningPhase,
            learningRate=self.learningParams.learningRate,
            explorationRate=self.learningParams.explorationRate,
            averageReward=experience.reward,
            knowledgeGrowth=len(self.longTermMemory) / 100,
            adaptationSpeed=self.learningParams.adaptationSpeed,
            quantumAdvantage=quantumInsights.get('quantumAdvantage', 1.0),
            timestamp=int(time.time() * 1000)
        )
        
        self.learningMetricsHistory.append(metrics)
        if len(self.learningMetricsHistory) > 100:
            self.learningMetricsHistory.pop(0)
        
        self.quantumAdvantageAccumulated += quantumInsights.get('quantumAdvantage', 1.0)
    
    # --- PREDICTION WITH KNOWLEDGE ---
    
    async def predictWithKnowledge(self, currentState: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 1. Retrieve Knowledge
            relevant_knowledge = self.retrieveRelevantKnowledge(currentState)
            
            # 2. QNN Prediction
            nn_input = self.prepareNNInput(currentState)
            quantum_prediction = await self.quantumNN.predict(nn_input)
            
            # 3. Integrate
            return self.integratePredictions(quantum_prediction, relevant_knowledge)
            
        except Exception as e:
            print(f"Knowledge Prediction Failed: {e}")
            return {'prediction': 0.5, 'confidence': 0, 'learningPhase': self.learningPhase.value}
    
    def retrieveRelevantKnowledge(self, state: Dict[str, Any]) -> List[QuantumKnowledge]:
        input_vec = self.prepareNNInput(state)
        results: List[Dict[str, Any]] = []
        
        for knowledge in self.longTermMemory.values():
            similarity = self.calculateSimilarity(input_vec, knowledge.quantumRepresentation)
            if similarity > 0.7:
                results.append({'knowledge': knowledge, 'similarity': similarity})
        
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return [r['knowledge'] for r in results[:5]]
    
    def calculateSimilarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcula similaridade cosseno simplificada"""
        min_len = min(len(vec1), len(vec2))
        sum_sq = 0.0
        
        for i in range(min_len):
            sum_sq += (vec1[i] - vec2[i]) ** 2
        
        return 1 / (1 + math.sqrt(sum_sq))
    
    def integratePredictions(self, quantum_prediction: Dict[str, Any], 
                            relevant_knowledge: List[QuantumKnowledge]) -> Dict[str, Any]:
        qnn_weight = 0.7
        knowledge_weight = 0.3
        
        knowledge_contribution = 0.0
        knowledge_confidence = 0.0
        
        for knowledge in relevant_knowledge:
            knowledge_contribution += knowledge.successRate * knowledge.confidence
            knowledge_confidence += knowledge.confidence
        
        if knowledge_confidence > 0:
            knowledge_contribution /= knowledge_confidence
        
        final_prediction = (qnn_weight * quantum_prediction['prediction'] + 
                           knowledge_weight * knowledge_contribution)
        
        final_confidence = (qnn_weight * quantum_prediction['confidence'] + 
                           knowledge_weight * (knowledge_confidence / (len(relevant_knowledge) or 1)))
        
        # Update usage stats for retrieved knowledge
        now = int(time.time() * 1000)
        for knowledge in relevant_knowledge:
            knowledge.lastUsed = now
            knowledge.usageCount += 1
        
        return {
            'prediction': final_prediction,
            'confidence': final_confidence,
            'learningPhase': self.learningPhase.value,
            'relevantPatternCount': len(relevant_knowledge)
        }
    
    # --- UTILS ---
    
    def generatePatternHash(self, experience: LearningExperience, 
                          insights: Dict[str, Any]) -> str:
        """Gera hash para o padrão"""
        pattern_str = (json.dumps(experience.state, sort_keys=True) + 
                      experience.action + 
                      f"{insights['confidence']:.2f}")
        
        # Implementação simples de hash
        hash_val = 0
        for char in pattern_str:
            hash_val = (hash_val << 5) - hash_val + ord(char)
            hash_val = hash_val & 0xFFFFFFFF  # Convert to 32bit integer
        
        return hex(hash_val)[2:]
    
    def saveKnowledgeBase(self):
        """Salva base de conhecimento em arquivo"""
        try:
            knowledge_dict = {}
            for key, knowledge in self.longTermMemory.items():
                knowledge_dict[key] = knowledge.__dict__
            
            with open('quantum_knowledge_base.json', 'w') as f:
                json.dump(knowledge_dict, f, indent=2)
            
            print("💾 Knowledge base saved")
        except Exception as e:
            print(f"⚠️ Failed to save knowledge base: {e}")
    
    def loadKnowledgeBase(self):
        """Carrega base de conhecimento de arquivo"""
        try:
            with open('quantum_knowledge_base.json', 'r') as f:
                knowledge_dict = json.load(f)
            
            self.longTermMemory = {}
            for key, data in knowledge_dict.items():
                self.longTermMemory[key] = QuantumKnowledge(**data)
            
            print(f"📚 Loaded {len(self.longTermMemory)} patterns from knowledge base.")
        except FileNotFoundError:
            print("ℹ️ No existing knowledge base found. Starting fresh.")
        except Exception as e:
            print(f"⚠️ Failed to load knowledge base: {e}")

# Instância global
continuousLearner = ContinuousQuantumLearningService()

# Exemplo de uso
async def example_usage():
    # Inicializar
    await continuousLearner.initialize()
    
    # Criar experiência de aprendizado
    experience = LearningExperience(
        id="exp_001",
        state={
            'rsi': 65,
            'macd': 12,
            'volatility': 0.02,
            'volumeNormalized': 0.8
        },
        action='BUY',
        reward=150.0,
        importance=0.8
    )
    
    # Aprender com a experiência
    await continuousLearner.learnFromExperience(experience)
    
    # Verificar status
    status = continuousLearner.getStatus()
    print(f"Status: {status}")
    
    # Fazer predição com conhecimento
    current_state = {
        'rsi': 70,
        'macd': 15,
        'volatility': 0.015,
        'volumeNormalized': 0.7
    }
    
    prediction = await continuousLearner.predictWithKnowledge(current_state)
    print(f"Prediction: {prediction}")

# Executar exemplo
if __name__ == "__main__":
    import asyncio
    import random
    
    # Definir seed para reprodutibilidade
    random.seed(42)
    
    # Executar exemplo
    asyncio.run(example_usage())