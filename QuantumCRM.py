import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Any, Optional
from enum import Enum
import random

# Configuração da página
st.set_page_config(
    page_title="CRM Quântico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enums e Classes de Tipos
class InteractionType(str, Enum):
    EMAIL = "EMAIL"
    CALL = "CALL"
    MEETING = "MEETING"

class QuantumSentiment(str, Enum):
    VERY_NEGATIVE = "VERY_NEGATIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"
    VERY_POSITIVE = "VERY_POSITIVE"

class LeadStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    CLOSED_WON = "CLOSED_WON"
    CLOSED_LOST = "CLOSED_LOST"

class Interaction:
    def __init__(self, type: InteractionType, content: str, sentiment: QuantumSentiment, 
                 quantum_engagement: float, timestamp: datetime):
        self.type = type
        self.content = content
        self.sentiment = sentiment
        self.quantum_engagement = quantum_engagement
        self.timestamp = timestamp

class QuantumLeadProfile:
    def __init__(self, lead_id: str, company: str, industry: str, budget: float, 
                 status: LeadStatus, quantum_affinity: float):
        self.lead_id = lead_id
        self.company = company
        self.industry = industry
        self.budget = budget
        self.status = status
        self.quantum_affinity = quantum_affinity
        self.interactions: List[Interaction] = []
        self.created_at = datetime.now()

class QuantumVector:
    def __init__(self, trust_level: float, engagement_level: float, 
                 value_potential: float, strategic_fit: float, quantum_synergy: float):
        self.trust_level = trust_level
        self.engagement_level = engagement_level
        self.value_potential = value_potential
        self.strategic_fit = strategic_fit
        self.quantum_synergy = quantum_synergy

class QuantumPrediction:
    def __init__(self, probability: float, value: float, key_factors: List[str]):
        self.probability = probability
        self.value = value
        self.key_factors = key_factors

# Serviço CRM Quântico
class QuantumCRMService:
    def __init__(self):
        self.leads: Dict[str, QuantumLeadProfile] = {}
        self.vectors: Dict[str, QuantumVector] = {}
        self.predictions: Dict[str, QuantumPrediction] = {}
        
    def initialize(self):
        """Inicializa com dados de exemplo"""
        if not self.leads:
            sample_leads = [
                ("QuantumTech Solutions", "Tecnologia Quântica", 250000, LeadStatus.QUALIFIED, 0.85),
                ("NeuroFinance Corp", "Finanças", 150000, LeadStatus.CONTACTED, 0.72),
                ("AstraLogistics", "Logística", 80000, LeadStatus.NEW, 0.65),
                ("BioSynth Research", "Biotecnologia", 350000, LeadStatus.NEGOTIATION, 0.91),
                ("CyberSecure Ltd", "Segurança", 120000, LeadStatus.PROPOSAL, 0.78),
            ]
            
            for company, industry, budget, status, affinity in sample_leads:
                lead_id = str(uuid.uuid4())[:8]
                lead = QuantumLeadProfile(lead_id, company, industry, budget, status, affinity)
                self.leads[lead_id] = lead
                
                # Criar vetor quântico
                self.vectors[lead_id] = QuantumVector(
                    trust_level=random.uniform(0.6, 0.9),
                    engagement_level=random.uniform(0.5, 0.85),
                    value_potential=random.uniform(0.7, 1.0),
                    strategic_fit=random.uniform(0.6, 0.95),
                    quantum_synergy=affinity
                )
                
                # Criar predição
                self.predictions[lead_id] = QuantumPrediction(
                    probability=random.uniform(0.3, 0.95),
                    value=budget * random.uniform(0.8, 1.2),
                    key_factors=[
                        "Alinhamento estratégico",
                        "Orçamento disponível",
                        "Necessidade clara",
                        "Cultura organizacional",
                        f"Sinergia com {industry}"
                    ]
                )
                
                # Adicionar interações de exemplo
                for _ in range(random.randint(2, 5)):
                    lead.interactions.append(Interaction(
                        type=random.choice(list(InteractionType)),
                        content=f"Discussão sobre {industry}",
                        sentiment=random.choice(list(QuantumSentiment)),
                        quantum_engagement=random.uniform(0.5, 0.95),
                        timestamp=datetime.now() - timedelta(days=random.randint(0, 30))
                    ))
    
    def add_lead(self, company: str, industry: str, budget: float) -> str:
        """Adiciona um novo lead"""
        lead_id = str(uuid.uuid4())[:8]
        lead = QuantumLeadProfile(
            lead_id=lead_id,
            company=company,
            industry=industry,
            budget=budget,
            status=LeadStatus.NEW,
            quantum_affinity=random.uniform(0.5, 0.9)
        )
        
        self.leads[lead_id] = lead
        
        # Criar vetor quântico
        self.vectors[lead_id] = QuantumVector(
            trust_level=random.uniform(0.4, 0.7),
            engagement_level=random.uniform(0.4, 0.7),
            value_potential=budget / 500000,  # Normalizado
            strategic_fit=random.uniform(0.5, 0.8),
            quantum_synergy=lead.quantum_affinity
        )
        
        # Criar predição inicial
        self.predictions[lead_id] = QuantumPrediction(
            probability=random.uniform(0.2, 0.6),
            value=budget * random.uniform(0.5, 0.8),
            key_factors=[
                "Lead novo - análise preliminar",
                f"Potencial em {industry}",
                "Necessidade de validação",
                "Contato inicial pendente"
            ]
        )
        
        return lead_id
    
    def record_interaction(self, lead_id: str, type: InteractionType, content: str):
        """Registra uma interação com o lead"""
        if lead_id not in self.leads:
            return
        
        interaction = Interaction(
            type=type,
            content=content,
            sentiment=QuantumSentiment.NEUTRAL,  # Em produção, seria analisado por NLP
            quantum_engagement=random.uniform(0.5, 0.95),
            timestamp=datetime.now()
        )
        
        self.leads[lead_id].interactions.append(interaction)
        
        # Atualizar vetor com base na interação
        if lead_id in self.vectors:
            self.vectors[lead_id].engagement_level = min(1.0, self.vectors[lead_id].engagement_level + 0.05)
            self.vectors[lead_id].trust_level = min(1.0, self.vectors[lead_id].trust_level + 0.03)
    
    def get_all_leads(self) -> List[QuantumLeadProfile]:
        """Retorna todos os leads"""
        return list(self.leads.values())
    
    def get_lead(self, lead_id: str) -> Optional[QuantumLeadProfile]:
        """Retorna um lead específico"""
        return self.leads.get(lead_id)
    
    def get_vector(self, lead_id: str) -> Optional[QuantumVector]:
        """Retorna o vetor quântico do lead"""
        return self.vectors.get(lead_id)
    
    def get_prediction(self, lead_id: str) -> Optional[QuantumPrediction]:
        """Retorna a predição do lead"""
        return self.predictions.get(lead_id)
    
    def get_interactions(self, lead_id: str) -> List[Interaction]:
        """Retorna as interações do lead"""
        lead = self.get_lead(lead_id)
        return lead.interactions if lead else []

# Inicialização do serviço
if 'crm_service' not in st.session_state:
    st.session_state.crm_service = QuantumCRMService()
    st.session_state.crm_service.initialize()

if 'selected_lead' not in st.session_state:
    st.session_state.selected_lead = None

if 'is_adding_lead' not in st.session_state:
    st.session_state.is_adding_lead = False

if 'interaction_type' not in st.session_state:
    st.session_state.interaction_type = InteractionType.EMAIL

if 'interaction_content' not in st.session_state:
    st.session_state.interaction_content = ""

# CSS Customizado
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #d1d5db;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .lead-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .lead-card:hover {
        background-color: #1f2937;
        border-color: #4b5563;
    }
    
    .lead-card.selected {
        background-color: rgba(14, 165, 233, 0.1);
        border-left: 3px solid #0ea5e9;
    }
    
    .quantum-panel {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .metric-value {
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .new-badge { background-color: #3b82f6; color: white; }
    .contacted-badge { background-color: #8b5cf6; color: white; }
    .qualified-badge { background-color: #10b981; color: white; }
    .proposal-badge { background-color: #f59e0b; color: white; }
    .negotiation-badge { background-color: #ec4899; color: white; }
    
    .interaction-email { color: #3b82f6; }
    .interaction-call { color: #10b981; }
    .interaction-meeting { color: #8b5cf6; }
    
    .sentiment-positive { color: #10b981; }
    .sentiment-negative { color: #ef4444; }
    .sentiment-neutral { color: #6b7280; }
    
    .quantum-text {
        color: #0ea5e9;
    }
</style>
""", unsafe_allow_html=True)

# Layout Principal
col1, col2 = st.columns([1, 2])

with col1:
    # Sidebar de Leads
    st.markdown("""
    <div style="padding: 1rem; border-bottom: 1px solid #374151; background-color: #111827; display: flex; justify-content: space-between; align-items: center;">
        <h2 style="color: white; font-weight: bold; margin: 0;">
            📊 CRM QUÂNTICO
        </h2>
        <button onclick="window.location.reload()" style="background: none; border: none; color: #0ea5e9; cursor: pointer;">
            ➕
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão para adicionar lead (simulado)
    if st.button("➕ Adicionar Lead", use_container_width=True):
        st.session_state.is_adding_lead = True
    
    # Formulário para adicionar lead
    if st.session_state.is_adding_lead:
        with st.form("add_lead_form"):
            new_company = st.text_input("Empresa")
            new_industry = st.text_input("Indústria")
            new_budget = st.number_input("Orçamento ($)", min_value=0.0, step=1000.0)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.form_submit_button("✅ Adicionar"):
                    if new_company and new_industry:
                        st.session_state.crm_service.add_lead(new_company, new_industry, new_budget)
                        st.session_state.is_adding_lead = False
                        st.rerun()
            with col_b:
                if st.form_submit_button("❌ Cancelar"):
                    st.session_state.is_adding_lead = False
    
    # Lista de Leads
    leads = st.session_state.crm_service.get_all_leads()
    
    for lead in leads:
        pred = st.session_state.crm_service.get_prediction(lead.lead_id)
        prob_color = "green" if pred and pred.probability > 0.7 else "yellow" if pred and pred.probability > 0.4 else "gray"
        
        if st.button(
            f"""
            **{lead.company}**  
            🏢 {lead.industry}  
            💰 ${lead.budget/1000:.0f}k  
            📈 {pred.probability*100:.0f}% Conv.
            """,
            key=f"lead_{lead.lead_id}",
            use_container_width=True
        ):
            st.session_state.selected_lead = lead
        
        st.divider()

with col2:
    if st.session_state.selected_lead:
        lead = st.session_state.selected_lead
        pred = st.session_state.crm_service.get_prediction(lead.lead_id)
        vector = st.session_state.crm_service.get_vector(lead.lead_id)
        
        # Header
        col_header1, col_header2 = st.columns([3, 1])
        
        with col_header1:
            st.markdown(f"### 🏢 {lead.company}")
            st.markdown(f"""
            <div style="display: flex; gap: 1rem; color: #9ca3af; font-size: 0.875rem;">
                <span>⚡ Afinidade Quântica: <strong class="quantum-text">{lead.quantum_affinity*100:.0f}%</strong></span>
                <span>📊 Status: <strong>{lead.status.value}</strong></span>
            </div>
            """, unsafe_allow_html=True)
        
        with col_header2:
            st.markdown('<div class="quantum-panel">', unsafe_allow_html=True)
            st.markdown("**Valor Predito (IAG)**")
            st.markdown(f'<div class="metric-value" style="color: #10b981;">${pred.value:,.0f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Métricas e Radar
        st.markdown("---")
        col_metrics1, col_metrics2 = st.columns(2)
        
        with col_metrics1:
            st.markdown("#### 📊 Vetor de Relacionamento")
            
            if vector:
                radar_data = pd.DataFrame({
                    'subject': ['Confiança', 'Engajamento', 'Valor', 'Fit Estratégico', 'Sinergia'],
                    'value': [
                        vector.trust_level * 100,
                        vector.engagement_level * 100,
                        vector.value_potential * 100,
                        vector.strategic_fit * 100,
                        vector.quantum_synergy * 100
                    ]
                })
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=radar_data['value'],
                    theta=radar_data['subject'],
                    fill='toself',
                    line=dict(color='#0ea5e9'),
                    fillcolor='rgba(14, 165, 233, 0.3)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickfont=dict(color='#666')
                        ),
                        angularaxis=dict(
                            tickfont=dict(color='#666', size=10)
                        ),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    showlegend=False,
                    height=300,
                    margin=dict(l=50, r=50, t=30, b=30),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col_metrics2:
            st.markdown("#### 🧠 Análise Neural")
            
            if pred:
                for factor in pred.key_factors[:5]:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #10b981;"></div>
                        <span style="font-size: 0.875rem;">{factor}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin-top: 1rem; padding: 1rem; background-color: rgba(14, 165, 233, 0.1); border: 1px solid #0ea5e9; border-radius: 0.5rem; font-size: 0.875rem; color: #93c5fd; font-style: italic;">
                "A IAG sugere aumentar o nível de confiança através de demonstrações técnicas focadas em {lead.industry}."
            </div>
            """.format(lead=lead), unsafe_allow_html=True)
        
        # Interações
        st.markdown("---")
        col_interactions1, col_interactions2 = st.columns([2, 1])
        
        with col_interactions1:
            st.markdown("#### 💬 Histórico de Interações")
            
            interactions = st.session_state.crm_service.get_interactions(lead.lead_id)
            
            if interactions:
                for interaction in sorted(interactions, key=lambda x: x.timestamp, reverse=True)[:10]:
                    icon = "📧" if interaction.type == InteractionType.EMAIL else "📞" if interaction.type == InteractionType.CALL else "👥"
                    color = "#3b82f6" if interaction.type == InteractionType.EMAIL else "#10b981" if interaction.type == InteractionType.CALL else "#8b5cf6"
                    sentiment_color = "#10b981" if interaction.sentiment in ["POSITIVE", "VERY_POSITIVE"] else "#ef4444" if interaction.sentiment in ["NEGATIVE", "VERY_NEGATIVE"] else "#6b7280"
                    
                    st.markdown(f"""
                    <div style="background-color: rgba(0,0,0,0.4); border: 1px solid #374151; border-radius: 0.5rem; padding: 1rem; margin-bottom: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="color: {color}; font-size: 1.5rem;">{icon}</div>
                                <div>
                                    <div style="font-weight: bold; color: white;">{interaction.type.value}</div>
                                    <div style="font-size: 0.75rem; color: #9ca3af;">{interaction.timestamp.strftime('%d/%m/%Y %H:%M')}</div>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-weight: bold; color: {sentiment_color};">{interaction.sentiment.value}</div>
                                <div style="font-size: 0.75rem; color: #9ca3af;">Engajamento: {interaction.quantum_engagement*100:.0f}%</div>
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem; font-size: 0.875rem; color: #d1d5db;">{interaction.content}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhuma interação registrada.")
        
        with col_interactions2:
            st.markdown("#### 📝 Registrar Evento")
            
            interaction_type = st.selectbox(
                "Tipo",
                options=list(InteractionType),
                format_func=lambda x: x.value,
                key="interaction_type_select"
            )
            
            interaction_content = st.text_area(
                "Notas / Conteúdo",
                placeholder="Resumo da interação...",
                height=150,
                key="interaction_content_text"
            )
            
            if st.button("📝 Registrar Interação", use_container_width=True):
                if interaction_content:
                    st.session_state.crm_service.record_interaction(
                        lead.lead_id,
                        interaction_type,
                        interaction_content
                    )
                    st.success("Interação registrada com sucesso!")
                    st.rerun()
    
    else:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh; color: #6b7280;">
            <div style="font-size: 4rem; opacity: 0.2;">📊</div>
            <h3 style="margin-top: 1rem;">Selecione um Lead para análise quântica detalhada</h3>
        </div>
        """, unsafe_allow_html=True)

# Rodapé com estatísticas
st.markdown("---")
col_stats1, col_stats2, col_stats3 = st.columns(3)

with col_stats1:
    st.metric("Total de Leads", len(leads))

with col_stats2:
    avg_prob = np.mean([st.session_state.crm_service.get_prediction(l.lead_id).probability for l in leads if st.session_state.crm_service.get_prediction(l.lead_id)])
    st.metric("Probabilidade Média", f"{avg_prob*100:.1f}%")

with col_stats3:
    total_interactions = sum([len(l.interactions) for l in leads])
    st.metric("Total de Interações", total_interactions)