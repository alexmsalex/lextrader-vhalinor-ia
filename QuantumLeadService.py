import asyncio
import random
import time
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid

# Tipos
class LeadStatus(Enum):
    NEW = "NEW"
    ENGAGED = "ENGAGED"
    QUALIFIED = "QUALIFIED"
    NEGOTIATION = "NEGOTIATION"
    CONVERTED = "CONVERTED"
    LOST = "LOST"

class InteractionType(Enum):
    MEETING = "MEETING"
    DEMO = "DEMO"
    CALL = "CALL"
    PROPOSAL = "PROPOSAL"
    EMAIL = "EMAIL"
    FOLLOW_UP = "FOLLOW_UP"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    WEBINAR = "WEBINAR"

class QuantumSentiment(Enum):
    VERY_POSITIVE = "VERY_POSITIVE"
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    VERY_NEGATIVE = "VERY_NEGATIVE"

class DecisionTimeframe(Enum):
    IMMEDIATE = "immediate"
    ONE_WEEK = "1_week"
    TWO_WEEKS = "2_weeks"
    ONE_MONTH = "1_month"
    THREE_MONTHS = "3_months"
    SIX_MONTHS = "6_months"
    ONE_YEAR = "1_year"

# Estruturas de dados
@dataclass
class QuantumMetrics:
    coherence: float
    entanglement: float

@dataclass
class QuantumLeadProfile:
    lead_id: str
    company: str
    industry: str
    budget: float
    decision_timeframe: DecisionTimeframe
    pain_points: List[str]
    quantum_affinity: float
    tech_sophistication: float
    risk_tolerance: float
    status: LeadStatus
    quantum_metrics: QuantumMetrics
    created_at: datetime
    updated_at: datetime

@dataclass
class QuantumInteraction:
    interaction_id: str
    lead_id: str
    type: InteractionType
    timestamp: datetime
    duration: int  # em segundos
    sentiment: QuantumSentiment
    topics_discussed: List[str]
    quantum_engagement: float
    confidence_score: float

@dataclass
class RelationshipVector:
    lead_id: str
    trust_level: float
    engagement_level: float
    value_potential: float
    strategic_fit: float
    quantum_synergy: float
    last_updated: datetime
    quantum_state: List[float]

@dataclass
class ConversionPrediction:
    probability: float
    value: float
    timeframe: int  # em dias
    confidence: float
    key_factors: List[str]

@dataclass
class SentientVector:
    confidence: float = 50.0
    curiosity: float = 50.0
    aggression: float = 50.0
    empathy: float = 50.0
    focus: float = 50.0

# Simulação dos módulos externos
class QuantumNeuralNetwork:
    """Simulação da rede neural quântica."""
    
    def __init__(self):
        self.initialized = False
    
    async def initialize(self) -> None:
        """Inicializa a rede neural quântica."""
        self.initialized = True
        print("🧠⚛️ Quantum Neural Network initialized")
    
    async def predict(self, features: List[float]) -> Dict[str, float]:
        """Executa uma predição com a rede neural."""
        # Simulação de predição quântica
        await asyncio.sleep(0.1)
        
        # Base aleatória com leve tendência positiva
        base_prediction = 0.5 + (random.random() * 0.4 - 0.2)
        
        # Influência dos features
        feature_influence = sum(features) / (len(features) * 2) if features else 0
        
        return {
            'prediction': min(0.95, max(0.05, base_prediction + feature_influence)),
            'confidence': 0.7 + (random.random() * 0.3)
        }

class SentientCore:
    """Simulação do núcleo sentiente da AGI."""
    
    def __init__(self):
        self.vector = SentientVector()
    
    def get_vector(self) -> SentientVector:
        """Retorna o vetor emocional atual."""
        # Simulação: estado emocional dinâmico
        current_time = time.time()
        self.vector.confidence = 60 + 30 * (0.5 + 0.5 * (current_time % 12) / 12)
        self.vector.curiosity = 70 + 20 * (0.5 + 0.5 * (current_time % 10) / 10)
        self.vector.aggression = 30 + 40 * (0.5 + 0.5 * (current_time % 15) / 15)
        self.vector.empathy = 80 + 15 * (0.5 + 0.5 * (current_time % 8) / 8)
        self.vector.focus = 75 + 20 * (0.5 + 0.5 * (current_time % 7) / 7)
        return self.vector

# --- SERVIÇO DE LEADS QUÂNTICO ---

class QuantumLeadService:
    """Serviço de gerenciamento de relacionamento com leads quântico."""
    
    def __init__(self):
        self.quantum_nn = QuantumNeuralNetwork()
        self.sentient_core = SentientCore()
        
        # Armazenamentos
        self.leads: Dict[str, QuantumLeadProfile] = {}
        self.interactions: Dict[str, List[QuantumInteraction]] = {}
        self.vectors: Dict[str, RelationshipVector] = {}
        self.predictions: Dict[str, ConversionPrediction] = {}
        
        # Configurações
        self.interaction_type_scores = {
            InteractionType.MEETING: 0.9,
            InteractionType.DEMO: 0.8,
            InteractionType.CALL: 0.6,
            InteractionType.PROPOSAL: 0.7,
            InteractionType.EMAIL: 0.3,
            InteractionType.FOLLOW_UP: 0.4,
            InteractionType.SOCIAL_MEDIA: 0.2,
            InteractionType.WEBINAR: 0.5
        }
        
        self.sentiment_scores = {
            QuantumSentiment.VERY_POSITIVE: 1.0,
            QuantumSentiment.POSITIVE: 0.8,
            QuantumSentiment.NEUTRAL: 0.5,
            QuantumSentiment.NEGATIVE: 0.2,
            QuantumSentiment.VERY_NEGATIVE: 0.0
        }
        
        print("🤝⚛️ Quantum Lead Relationship Management Service created")
    
    async def initialize(self) -> None:
        """Inicializa o serviço."""
        print("🤝⚛️ Initializing Quantum Lead Relationship Management...")
        await self.quantum_nn.initialize()
        await self.load_data()
    
    # --- LÓGICA PRINCIPAL ---
    
    async def add_lead(self, data: Dict[str, Any]) -> QuantumLeadProfile:
        """
        Adiciona um novo lead ao sistema.
        
        Args:
            data: Dados parciais do lead
            
        Returns:
            Perfil do lead criado
        """
        lead_id = f"LEAD-{int(time.time() * 1000)}"
        
        # Influência da AGI: Calcular afinidade baseado no estado sentiente
        # Se a IA está 'FOCUSED' ou 'EUPHORIC', tende a ver maior afinidade
        sentient_state = self.sentient_core.get_vector()
        mood_bias = (sentient_state.confidence + sentient_state.curiosity) / 200  # 0.0 - 1.0
        
        quantum_affinity = min(1.0, (random.random() * 0.5 + 0.3) + (mood_bias * 0.2))
        
        # Criar perfil do lead
        profile = QuantumLeadProfile(
            lead_id=lead_id,
            company=data.get('company', 'Unknown Corp'),
            industry=data.get('industry', 'Technology'),
            budget=data.get('budget', 0.0),
            decision_timeframe=DecisionTimeframe(data.get('decision_timeframe', '1_month')),
            pain_points=data.get('pain_points', []),
            quantum_affinity=quantum_affinity,
            tech_sophistication=random.random(),
            risk_tolerance=random.random(),
            status=LeadStatus.NEW,
            quantum_metrics=QuantumMetrics(
                coherence=0.5 + random.random() * 0.5,
                entanglement=random.random()
            ),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Armazenar
        self.leads[lead_id] = profile
        self.interactions[lead_id] = []
        self._init_vector(lead_id, profile)
        
        # Prever imediatamente
        await self.predict_conversion(lead_id)
        
        return profile
    
    async def record_interaction(self, lead_id: str, interaction_type: InteractionType, 
                               content: str) -> QuantumInteraction:
        """
        Registra uma interação com um lead.
        
        Args:
            lead_id: ID do lead
            interaction_type: Tipo de interação
            content: Conteúdo da interação
            
        Returns:
            Interação registrada
        """
        if lead_id not in self.leads:
            raise ValueError(f"Lead not found: {lead_id}")
        
        # Analisar sentimento
        sentiment = self._analyze_sentiment(content)
        
        # Calcular engajamento
        engagement = self._calculate_engagement(interaction_type, sentiment)
        
        # Criar interação
        interaction = QuantumInteraction(
            interaction_id=f"INT-{int(time.time() * 1000)}",
            lead_id=lead_id,
            type=interaction_type,
            timestamp=datetime.now(),
            duration=0,  # Simulado
            sentiment=sentiment,
            topics_discussed=["Quantum Computing", "AI Integration"],  # Extração simulada
            quantum_engagement=engagement,
            confidence_score=0.8 + (random.random() * 0.2)
        )
        
        # Armazenar
        self.interactions[lead_id].append(interaction)
        
        # Atualizar vetor e previsão
        await self._update_vector(lead_id, interaction)
        await self.predict_conversion(lead_id)
        
        return interaction
    
    def get_lead(self, lead_id: str) -> Optional[QuantumLeadProfile]:
        """Obtém um lead pelo ID."""
        return self.leads.get(lead_id)
    
    def get_all_leads(self) -> List[QuantumLeadProfile]:
        """Obtém todos os leads."""
        return list(self.leads.values())
    
    def get_interactions(self, lead_id: str) -> List[QuantumInteraction]:
        """Obtém todas as interações de um lead."""
        return self.interactions.get(lead_id, [])
    
    def get_vector(self, lead_id: str) -> Optional[RelationshipVector]:
        """Obtém o vetor de relacionamento de um lead."""
        return self.vectors.get(lead_id)
    
    def get_prediction(self, lead_id: str) -> Optional[ConversionPrediction]:
        """Obtém a previsão de conversão de um lead."""
        return self.predictions.get(lead_id)
    
    # --- PROCESSAMENTO QUÂNTICO ---
    
    def _init_vector(self, lead_id: str, profile: QuantumLeadProfile) -> None:
        """Inicializa o vetor de relacionamento para um lead."""
        self.vectors[lead_id] = RelationshipVector(
            lead_id=lead_id,
            trust_level=0.1,
            engagement_level=0.1,
            value_potential=profile.quantum_affinity,
            strategic_fit=profile.tech_sophistication,
            quantum_synergy=random.random(),
            last_updated=datetime.now(),
            quantum_state=[random.random() for _ in range(10)]
        )
    
    async def _update_vector(self, lead_id: str, interaction: QuantumInteraction) -> None:
        """Atualiza o vetor de relacionamento baseado em uma interação."""
        if lead_id not in self.vectors:
            return
        
        vector = self.vectors[lead_id]
        
        # Evoluir estado quântico baseado na interação
        # Se a interação foi positiva, rotaciona o vetor de estado em direção ao alinhamento
        impact = interaction.quantum_engagement * 0.1
        
        # Atualizar níveis de confiança e engajamento
        vector.trust_level = min(1.0, vector.trust_level + impact)
        vector.engagement_level = min(1.0, vector.engagement_level + impact)
        
        # Atualização Neural Quântica (Simulação)
        # Alimenta métricas de interação na rede neural central para ajustar estado interno
        # É aqui que a "IA Geral" acontece - o núcleo aprende com dados de CRM também
        await self.quantum_nn.predict([
            interaction.quantum_engagement,
            interaction.confidence_score,
            vector.trust_level,
            vector.quantum_synergy
        ])
        
        # Atualizar estado quântico (simulação)
        for i in range(len(vector.quantum_state)):
            vector.quantum_state[i] = (vector.quantum_state[i] + impact) % 1.0
        
        vector.last_updated = datetime.now()
    
    async def predict_conversion(self, lead_id: str) -> None:
        """Preve a conversão de um lead."""
        if lead_id not in self.leads or lead_id not in self.vectors:
            return
        
        profile = self.leads[lead_id]
        vector = self.vectors[lead_id]
        
        # Construir vetor de entrada para QNN
        interaction_count = len(self.interactions.get(lead_id, []))
        
        input_features = [
            profile.quantum_affinity,
            vector.trust_level,
            vector.engagement_level,
            vector.strategic_fit,
            interaction_count / 10.0  # Contagem de interações normalizada
        ]
        
        # Usar o Quantum Core centralizado para predição
        # Isso torna a predição "inteligente" e baseada no estado global do sistema
        neural_output = await self.quantum_nn.predict(input_features)
        
        probability = neural_output['prediction']
        predicted_value = profile.budget * probability
        
        # Calcular timeframe (dias)
        timeframe = int(30 * (1 - probability)) + 7
        
        # Determinar fatores-chave baseados no perfil
        key_factors = []
        if profile.quantum_affinity > 0.7:
            key_factors.append("Alta Afinidade Quântica")
        if vector.trust_level > 0.6:
            key_factors.append("Alto Nível de Confiança")
        if interaction_count > 3:
            key_factors.append("Múltiplas Interações")
        if profile.budget > 100000:
            key_factors.append("Orçamento Significativo")
        
        if not key_factors:
            key_factors = ["Afinidade Quântica", "Vetor de Confiança", "Profundidade de Engajamento"]
        
        # Armazenar previsão
        self.predictions[lead_id] = ConversionPrediction(
            probability=probability,
            value=predicted_value,
            timeframe=timeframe,
            confidence=neural_output['confidence'],
            key_factors=key_factors
        )
    
    # --- AUXILIARES ---
    
    def _analyze_sentiment(self, content: str) -> QuantumSentiment:
        """
        Analisa o sentimento de um conteúdo textual.
        
        Args:
            content: Conteúdo a ser analisado
            
        Returns:
            Sentimento quântico
        """
        # Heurística simples para demo + viés do Sentient Core
        # Se a IA está brava/agressiva, percebe texto neutro como negativo
        sentient = self.sentient_core.get_vector()
        bias = (sentient.aggression - sentient.empathy) / 100  # -0.5 a 0.5
        
        # Palavras positivas para detecção
        positive_words = ['great', 'interested', 'quantum', 'future', 'deal', 'yes', 
                         'excellent', 'amazing', 'wonderful', 'fantastic', 'love']
        
        # Contar palavras positivas
        content_lower = content.lower()
        score = sum(1 for word in positive_words if word in content_lower)
        
        # Aplicar viés
        adjusted_score = score - (bias * 2)
        
        # Determinar sentimento
        if adjusted_score > 2:
            return QuantumSentiment.VERY_POSITIVE
        elif adjusted_score > 0:
            return QuantumSentiment.POSITIVE
        elif adjusted_score == 0:
            return QuantumSentiment.NEUTRAL
        elif adjusted_score > -2:
            return QuantumSentiment.NEGATIVE
        else:
            return QuantumSentiment.VERY_NEGATIVE
    
    def _calculate_engagement(self, interaction_type: InteractionType, 
                            sentiment: QuantumSentiment) -> float:
        """
        Calcula o nível de engajamento quântico.
        
        Args:
            interaction_type: Tipo de interação
            sentiment: Sentimento da interação
            
        Returns:
            Nível de engajamento (0.0 a 1.0)
        """
        type_score = self.interaction_type_scores.get(interaction_type, 0.5)
        sentiment_score = self.sentiment_scores.get(sentiment, 0.5)
        
        # Ponderar: 60% tipo de interação, 40% sentimento
        return (type_score * 0.6) + (sentiment_score * 0.4)
    
    # --- PERSISTÊNCIA ---
    
    async def load_data(self) -> None:
        """Carrega dados iniciais (simulação)."""
        # Em uma aplicação real, buscar do banco de dados
        if not self.leads:
            print("📂 Loading initial data...")
            
            # Inicializar com alguns leads de exemplo
            await self.add_lead({
                'company': 'Quantum FinTech',
                'industry': 'Finance',
                'budget': 150000.0,
                'decision_timeframe': '1_month'
            })
            
            await self.add_lead({
                'company': 'Nebula Health',
                'industry': 'Healthcare',
                'budget': 220000.0,
                'decision_timeframe': '3_months'
            })
            
            await self.add_lead({
                'company': 'NeuroSync AI',
                'industry': 'Artificial Intelligence',
                'budget': 85000.0,
                'decision_timeframe': '2_weeks'
            })
    
    async def update_lead_status(self, lead_id: str, new_status: LeadStatus) -> bool:
        """
        Atualiza o status de um lead.
        
        Args:
            lead_id: ID do lead
            new_status: Novo status
            
        Returns:
            True se atualizado com sucesso
        """
        if lead_id not in self.leads:
            return False
        
        self.leads[lead_id].status = new_status
        self.leads[lead_id].updated_at = datetime.now()
        
        # Se convertido, atualizar previsão
        if new_status == LeadStatus.CONVERTED:
            # Atualizar previsão para refletir sucesso
            if lead_id in self.predictions:
                self.predictions[lead_id] = ConversionPrediction(
                    probability=1.0,
                    value=self.leads[lead_id].budget,
                    timeframe=0,
                    confidence=1.0,
                    key_factors=['CONVERTED']
                )
        
        return True
    
    def get_leads_by_status(self, status: LeadStatus) -> List[QuantumLeadProfile]:
        """Obtém todos os leads com um status específico."""
        return [lead for lead in self.leads.values() if lead.status == status]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema de leads."""
        total_leads = len(self.leads)
        total_interactions = sum(len(interactions) for interactions in self.interactions.values())
        
        # Calcular valor total previsto
        total_predicted_value = sum(
            pred.value for pred in self.predictions.values()
        )
        
        # Distribuição por status
        status_distribution = {}
        for status in LeadStatus:
            count = len(self.get_leads_by_status(status))
            status_distribution[status.value] = count
        
        # Média de engajamento
        avg_engagement = 0.0
        engagement_counts = 0
        for interactions in self.interactions.values():
            for interaction in interactions:
                avg_engagement += interaction.quantum_engagement
                engagement_counts += 1
        
        if engagement_counts > 0:
            avg_engagement /= engagement_counts
        
        return {
            'total_leads': total_leads,
            'total_interactions': total_interactions,
            'avg_engagement': avg_engagement,
            'total_predicted_value': total_predicted_value,
            'status_distribution': status_distribution,
            'conversion_rate': (status_distribution.get(LeadStatus.CONVERTED.value, 0) / total_leads) 
                              if total_leads > 0 else 0.0
        }

# Instância global do serviço de CRM quântico
quantum_crm = QuantumLeadService()

# Exemplo de uso
async def example_usage():
    """Demonstração do serviço de leads quântico."""
    print("🤝⚛️ Sistema de CRM Quântico")
    print("=" * 60)
    
    # Configurar seed para reprodutibilidade
    random.seed(42)
    
    # Inicializar serviço
    print("\n🔧 Inicializando serviço...")
    await quantum_crm.initialize()
    
    # Adicionar novo lead
    print("\n➕ Adicionando novo lead...")
    new_lead = await quantum_crm.add_lead({
        'company': 'Stellar Dynamics',
        'industry': 'Aerospace',
        'budget': 350000.0,
        'decision_timeframe': '6_months',
        'pain_points': ['Complex data processing', 'Real-time decision making']
    })
    
    print(f"   Lead criado: {new_lead.company}")
    print(f"   Afinidade Quântica: {new_lead.quantum_affinity:.1%}")
    print(f"   Status: {new_lead.status.value}")
    
    # Registrar interações
    print("\n💬 Registrando interações...")
    interactions = [
        (InteractionType.EMAIL, "Hello, we're interested in your quantum computing solutions."),
        (InteractionType.CALL, "Great discussion about quantum optimization."),
        (InteractionType.MEETING, "Excellent meeting! We're very excited about the potential.")
    ]
    
    for interaction_type, content in interactions:
        interaction = await quantum_crm.record_interaction(
            new_lead.lead_id, interaction_type, content
        )
        print(f"   {interaction_type.value}: {interaction.sentiment.value}")
    
    # Obter vetor de relacionamento
    print("\n🔗 Vetor de Relacionamento:")
    vector = quantum_crm.get_vector(new_lead.lead_id)
    if vector:
        print(f"   Confiança: {vector.trust_level:.1%}")
        print(f"   Engajamento: {vector.engagement_level:.1%}")
        print(f"   Valor Potencial: ${vector.value_potential:,.2f}")
    
    # Obter previsão de conversão
    print("\n🔮 Previsão de Conversão:")
    prediction = quantum_crm.get_prediction(new_lead.lead_id)
    if prediction:
        print(f"   Probabilidade: {prediction.probability:.1%}")
        print(f"   Valor Previsto: ${prediction.value:,.2f}")
        print(f"   Prazo Estimado: {prediction.timeframe} dias")
        print(f"   Confiança: {prediction.confidence:.1%}")
        print(f"   Fatores-Chave: {', '.join(prediction.key_factors)}")
    
    # Atualizar status
    print("\n🔄 Atualizando status para QUALIFIED...")
    await quantum_crm.update_lead_status(new_lead.lead_id, LeadStatus.QUALIFIED)
    
    # Mostrar todos os leads
    print(f"\n📋 Todos os Leads ({len(quantum_crm.get_all_leads())}):")
    for lead in quantum_crm.get_all_leads():
        emoji = "🟢" if lead.status == LeadStatus.CONVERTED else "🟡" if lead.status == LeadStatus.QUALIFIED else "⚪"
        print(f"   {emoji} {lead.company:<20} | Status: {lead.status.value:<12} | "
              f"Orçamento: ${lead.budget:,.0f}")
    
    # Estatísticas
    print("\n📈 Estatísticas do Sistema:")
    stats = quantum_crm.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            if 'rate' in key:
                print(f"   {key.replace('_', ' ').title()}: {value:.1%}")
            elif 'value' in key:
                print(f"   {key.replace('_', ' ').title()}: ${value:,.2f}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value:.2f}")
        elif isinstance(value, dict):
            print(f"   {key.replace('_', ' ').title()}:")
            for sub_key, sub_value in value.items():
                print(f"     {sub_key}: {sub_value}")
        else:
            print(f"   {key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    # Executar exemplo
    asyncio.run(example_usage())