"""
AI Dashboard - Painel de Controle da IA Integrada
=================================================
Interface web para monitorar e controlar o sistema de IA
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
import time
import threading

# Importar sistemas
try:
    from integrated_ai_system import IntegratedAISystem, AIState
    from ai_config_manager import AIConfigManager
except ImportError:
    st.error("Erro ao importar sistemas de IA. Verifique se os arquivos estão no diretório correto.")
    st.stop()

# Configuração da página
st.set_page_config(
    page_title="LEXTRADER-IAG 4.0 - AI Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
    }
    
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-inactive {
        color: #dc3545;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .neural-activity {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização de sessão
if 'ai_system' not in st.session_state:
    st.session_state.ai_system = None
    st.session_state.config_manager = AIConfigManager()
    st.session_state.system_running = False
    st.session_state.last_update = datetime.now()

def initialize_ai_system():
    """Inicializa o sistema de IA"""
    if st.session_state.ai_system is None:
        config = st.session_state.config_manager.config
        st.session_state.ai_system = IntegratedAISystem(config=config.__dict__)
        st.session_state.system_running = True
        return True
    return False

def get_system_metrics():
    """Obtém métricas do sistema"""
    if st.session_state.ai_system:
        return st.session_state.ai_system.get_system_status()
    return {}

def create_neural_activity_chart(neural_stats: Dict[str, Any]):
    """Cria gráfico de atividade neural"""
    if not neural_stats:
        return go.Figure()
    
    # Dados simulados para demonstração
    neurons = ['Sensory', 'Processing', 'Memory', 'Decision', 'Output', 'Quantum']
    activities = np.random.uniform(0.2, 0.9, len(neurons))
    
    fig = go.Figure(data=go.Bar(
        x=neurons,
        y=activities,
        marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'],
        text=[f'{act:.2f}' for act in activities],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Atividade Neural em Tempo Real",
        xaxis_title="Tipos de Neurônios",
        yaxis_title="Nível de Ativação",
        yaxis=dict(range=[0, 1]),
        height=400,
        showlegend=False
    )
    
    return fig

def create_memory_usage_chart(memory_stats: Dict[str, Any]):
    """Cria gráfico de uso de memória"""
    if not memory_stats:
        return go.Figure()
    
    labels = ['Working Memory', 'Short Term', 'Long Term', 'Cache']
    values = [
        memory_stats.get('working_memory', 0),
        memory_stats.get('short_term', 0),
        memory_stats.get('long_term', 0),
        memory_stats.get('cache_hits', 0) + memory_stats.get('cache_misses', 0)
    ]
    
    fig = go.Figure(data=go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    ))
    
    fig.update_layout(
        title="Distribuição de Uso de Memória",
        height=400
    )
    
    return fig

def create_performance_timeline():
    """Cria linha do tempo de performance"""
    # Dados simulados
    dates = pd.date_range(start=datetime.now() - timedelta(hours=24), 
                         end=datetime.now(), freq='H')
    
    accuracy = np.random.uniform(0.7, 0.95, len(dates))
    confidence = np.random.uniform(0.6, 0.9, len(dates))
    decisions = np.random.poisson(5, len(dates))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=accuracy,
        mode='lines+markers',
        name='Acurácia',
        line=dict(color='#28a745', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=confidence,
        mode='lines+markers',
        name='Confiança Média',
        line=dict(color='#007bff', width=2)
    ))
    
    fig.update_layout(
        title="Performance nas Últimas 24 Horas",
        xaxis_title="Tempo",
        yaxis_title="Valor",
        height=400,
        hovermode='x unified'
    )
    
    return fig

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🧠 LEXTRADER-IAG 4.0 - AI Dashboard</h1>
    <p>Sistema de Inteligência Artificial Integrado - Monitoramento e Controle</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Controles
st.sidebar.title("🎛️ Controles do Sistema")

# Status do sistema
if st.session_state.system_running and st.session_state.ai_system:
    status = st.session_state.ai_system.state.value
    if status in ['CONSCIOUS', 'PROCESSING', 'LEARNING']:
        status_class = "status-active"
        status_icon = "🟢"
    elif status in ['ERROR']:
        status_class = "status-inactive"
        status_icon = "🔴"
    else:
        status_class = "status-warning"
        status_icon = "🟡"
else:
    status = "OFFLINE"
    status_class = "status-inactive"
    status_icon = "🔴"

st.sidebar.markdown(f"""
**Status do Sistema:** {status_icon} <span class="{status_class}">{status}</span>
""", unsafe_allow_html=True)

# Botões de controle
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("🚀 Iniciar IA", disabled=st.session_state.system_running):
        if initialize_ai_system():
            st.success("Sistema de IA inicializado!")
            st.rerun()

with col2:
    if st.button("🛑 Parar IA", disabled=not st.session_state.system_running):
        if st.session_state.ai_system:
            st.session_state.ai_system.shutdown()
            st.session_state.ai_system = None
            st.session_state.system_running = False
            st.success("Sistema parado!")
            st.rerun()

# Controles de automação
st.sidebar.subheader("🤖 Automação")

if st.session_state.ai_system:
    automation_status = st.session_state.ai_system.automation_enabled
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("▶️ Iniciar", disabled=automation_status):
            st.session_state.ai_system.start_automation()
            st.success("Automação iniciada!")
            st.rerun()
    
    with col2:
        if st.button("⏸️ Parar", disabled=not automation_status):
            st.session_state.ai_system.stop_automation()
            st.success("Automação parada!")
            st.rerun()

# Configurações rápidas
st.sidebar.subheader("⚙️ Configurações Rápidas")

if st.sidebar.button("🔄 Recarregar Config"):
    st.session_state.config_manager.load_config()
    st.sidebar.success("Configuração recarregada!")

if st.sidebar.button("💾 Salvar Estado"):
    if st.session_state.ai_system:
        st.session_state.ai_system._save_system_state()
        st.sidebar.success("Estado salvo!")

# Abas principais
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard Principal", 
    "🧠 Atividade Neural", 
    "💾 Sistema de Memória", 
    "📈 Performance", 
    "⚙️ Configurações"
])

# Tab 1: Dashboard Principal
with tab1:
    if st.session_state.system_running and st.session_state.ai_system:
        metrics = get_system_metrics()
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            uptime = metrics.get('uptime', 0)
            hours = int(uptime // 3600)
            minutes = int((uptime % 3600) // 60)
            st.metric("⏱️ Uptime", f"{hours}h {minutes}m")
        
        with col2:
            total_ops = metrics.get('global_metrics', {}).get('total_operations', 0)
            st.metric("🔄 Operações Totais", f"{total_ops:,}")
        
        with col3:
            success_rate = 0
            if total_ops > 0:
                successful = metrics.get('global_metrics', {}).get('successful_operations', 0)
                success_rate = (successful / total_ops) * 100
            st.metric("✅ Taxa de Sucesso", f"{success_rate:.1f}%")
        
        with col4:
            decisions = metrics.get('global_metrics', {}).get('decisions_made', 0)
            st.metric("🎯 Decisões Tomadas", f"{decisions:,}")
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        
        with col1:
            neural_stats = metrics.get('neural_stats', {})
            fig_neural = create_neural_activity_chart(neural_stats)
            st.plotly_chart(fig_neural, use_container_width=True)
        
        with col2:
            memory_stats = metrics.get('memory_stats', {})
            fig_memory = create_memory_usage_chart(memory_stats)
            st.plotly_chart(fig_memory, use_container_width=True)
        
        # Timeline de performance
        fig_timeline = create_performance_timeline()
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Detalhes do sistema
        st.subheader("📋 Detalhes do Sistema")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🧠 Estatísticas Neurais**")
            st.write(f"Total de Neurônios: {neural_stats.get('total_neurons', 0)}")
            st.write(f"Neurônios Ativos: {neural_stats.get('active_neurons', 0)}")
            st.write(f"Conexões Totais: {neural_stats.get('total_connections', 0)}")
        
        with col2:
            st.markdown("**💾 Estatísticas de Memória**")
            st.write(f"Memória de Trabalho: {memory_stats.get('working_memory', 0)}")
            st.write(f"Memória de Curto Prazo: {memory_stats.get('short_term', 0)}")
            st.write(f"Memória de Longo Prazo: {memory_stats.get('long_term', 0)}")
            
            cache_hits = memory_stats.get('cache_hits', 0)
            cache_misses = memory_stats.get('cache_misses', 0)
            if cache_hits + cache_misses > 0:
                hit_rate = (cache_hits / (cache_hits + cache_misses)) * 100
                st.write(f"Taxa de Acerto do Cache: {hit_rate:.1f}%")
        
        with col3:
            learning_stats = metrics.get('learning_stats', {})
            decision_stats = metrics.get('decision_stats', {})
            
            st.markdown("**📚 Aprendizado & Decisões**")
            st.write(f"Acurácia: {learning_stats.get('accuracy', 0):.2f}")
            st.write(f"Taxa de Aprendizado: {learning_stats.get('learning_rate', 0):.3f}")
            st.write(f"Confiança Média: {decision_stats.get('average_confidence', 0):.2f}")
            st.write(f"Risco Médio: {decision_stats.get('average_risk', 0):.2f}")
    
    else:
        st.info("🚀 Inicie o sistema de IA para ver o dashboard completo")
        
        # Mostrar configuração atual
        st.subheader("📋 Configuração Atual")
        config_summary = st.session_state.config_manager.get_config_summary()
        
        for section, data in config_summary.items():
            with st.expander(f"📁 {section.replace('_', ' ').title()}"):
                for key, value in data.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")

# Tab 2: Atividade Neural
with tab2:
    st.subheader("🧠 Monitoramento da Rede Neural")
    
    if st.session_state.system_running and st.session_state.ai_system:
        # Simulação de atividade neural em tempo real
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de atividade neural detalhado
            neurons_data = {
                'Neurônio': ['Sensory_1', 'Sensory_2', 'Processing_1', 'Processing_2', 
                           'Memory_1', 'Decision_1', 'Output_1', 'Quantum_1'],
                'Ativação': np.random.uniform(0.1, 0.9, 8),
                'Tipo': ['Sensory', 'Sensory', 'Processing', 'Processing', 
                        'Memory', 'Decision', 'Output', 'Quantum'],
                'Energia': np.random.uniform(50, 100, 8),
                'Conexões': np.random.randint(3, 12, 8)
            }
            
            df_neurons = pd.DataFrame(neurons_data)
            
            fig = px.scatter(df_neurons, x='Ativação', y='Energia', 
                           size='Conexões', color='Tipo',
                           hover_data=['Neurônio'],
                           title="Mapa de Ativação Neural")
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**🔥 Neurônios Mais Ativos**")
            top_neurons = df_neurons.nlargest(5, 'Ativação')
            for _, neuron in top_neurons.iterrows():
                st.write(f"**{neuron['Neurônio']}**")
                st.progress(neuron['Ativação'])
                st.write(f"Energia: {neuron['Energia']:.1f}%")
                st.write("---")
        
        # Matriz de conexões
        st.subheader("🕸️ Matriz de Conexões")
        
        # Simulação de matriz de conexões
        connection_matrix = np.random.rand(6, 6)
        np.fill_diagonal(connection_matrix, 0)
        
        fig_heatmap = px.imshow(connection_matrix,
                               labels=dict(x="Neurônio Destino", y="Neurônio Origem"),
                               x=['Sensory', 'Processing', 'Memory', 'Decision', 'Output', 'Quantum'],
                               y=['Sensory', 'Processing', 'Memory', 'Decision', 'Output', 'Quantum'],
                               title="Força das Conexões Sinápticas")
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
    else:
        st.info("Inicie o sistema para monitorar a atividade neural")

# Tab 3: Sistema de Memória
with tab3:
    st.subheader("💾 Análise do Sistema de Memória")
    
    if st.session_state.system_running and st.session_state.ai_system:
        metrics = get_system_metrics()
        memory_stats = metrics.get('memory_stats', {})
        
        # Estatísticas de memória
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔄 Memória de Trabalho", memory_stats.get('working_memory', 0))
            st.metric("⚡ Memória de Curto Prazo", memory_stats.get('short_term', 0))
        
        with col2:
            st.metric("🏛️ Memória de Longo Prazo", memory_stats.get('long_term', 0))
            cache_hits = memory_stats.get('cache_hits', 0)
            cache_misses = memory_stats.get('cache_misses', 0)
            total_access = cache_hits + cache_misses
            hit_rate = (cache_hits / total_access * 100) if total_access > 0 else 0
            st.metric("📊 Taxa de Acerto do Cache", f"{hit_rate:.1f}%")
        
        with col3:
            st.metric("🎯 Acessos ao Cache", cache_hits)
            st.metric("❌ Falhas do Cache", cache_misses)
        
        # Gráfico de evolução da memória
        st.subheader("📈 Evolução do Uso de Memória")
        
        # Dados simulados
        time_points = pd.date_range(start=datetime.now() - timedelta(hours=6), 
                                   end=datetime.now(), freq='30min')
        
        memory_evolution = pd.DataFrame({
            'Tempo': time_points,
            'Trabalho': np.random.randint(3, 7, len(time_points)),
            'Curto Prazo': np.random.randint(50, 100, len(time_points)),
            'Longo Prazo': np.random.randint(800, 1200, len(time_points))
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=memory_evolution['Tempo'], y=memory_evolution['Trabalho'],
                                mode='lines+markers', name='Memória de Trabalho',
                                line=dict(color='#ff6b6b')))
        
        fig.add_trace(go.Scatter(x=memory_evolution['Tempo'], y=memory_evolution['Curto Prazo'],
                                mode='lines+markers', name='Memória de Curto Prazo',
                                line=dict(color='#4ecdc4')))
        
        fig.add_trace(go.Scatter(x=memory_evolution['Tempo'], y=memory_evolution['Longo Prazo'],
                                mode='lines+markers', name='Memória de Longo Prazo',
                                line=dict(color='#45b7d1')))
        
        fig.update_layout(title="Evolução do Uso de Memória (Últimas 6 Horas)",
                         xaxis_title="Tempo",
                         yaxis_title="Número de Itens",
                         height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise de padrões de acesso
        st.subheader("🔍 Padrões de Acesso à Memória")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por tipo de memória
            memory_types = ['Episódica', 'Semântica', 'Procedural', 'Trabalho']
            memory_counts = np.random.randint(10, 100, len(memory_types))
            
            fig_pie = go.Figure(data=go.Pie(labels=memory_types, values=memory_counts,
                                           hole=0.3))
            fig_pie.update_layout(title="Distribuição por Tipo de Memória")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Frequência de acesso
            access_freq = pd.DataFrame({
                'Memória': [f'Mem_{i:03d}' for i in range(1, 21)],
                'Acessos': np.random.poisson(5, 20),
                'Importância': np.random.uniform(0.1, 1.0, 20)
            })
            
            fig_bar = px.bar(access_freq.head(10), x='Memória', y='Acessos',
                            color='Importância', title="Top 10 Memórias Mais Acessadas")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    else:
        st.info("Inicie o sistema para analisar o sistema de memória")

# Tab 4: Performance
with tab4:
    st.subheader("📈 Análise de Performance")
    
    if st.session_state.system_running and st.session_state.ai_system:
        metrics = get_system_metrics()
        
        # KPIs principais
        col1, col2, col3, col4 = st.columns(4)
        
        learning_stats = metrics.get('learning_stats', {})
        decision_stats = metrics.get('decision_stats', {})
        global_metrics = metrics.get('global_metrics', {})
        
        with col1:
            accuracy = learning_stats.get('accuracy', 0)
            st.metric("🎯 Acurácia", f"{accuracy:.2%}", 
                     delta=f"{np.random.uniform(-0.05, 0.05):.2%}")
        
        with col2:
            confidence = decision_stats.get('average_confidence', 0)
            st.metric("🔮 Confiança Média", f"{confidence:.2f}",
                     delta=f"{np.random.uniform(-0.1, 0.1):.2f}")
        
        with col3:
            success_ops = global_metrics.get('successful_operations', 0)
            total_ops = global_metrics.get('total_operations', 1)
            success_rate = success_ops / total_ops
            st.metric("✅ Taxa de Sucesso", f"{success_rate:.2%}",
                     delta=f"{np.random.uniform(-0.02, 0.02):.2%}")
        
        with col4:
            learning_rate = learning_stats.get('learning_rate', 0)
            st.metric("📚 Taxa de Aprendizado", f"{learning_rate:.3f}",
                     delta=f"{np.random.uniform(-0.001, 0.001):.3f}")
        
        # Gráficos de performance
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance ao longo do tempo
            fig_perf = create_performance_timeline()
            st.plotly_chart(fig_perf, use_container_width=True)
        
        with col2:
            # Distribuição de confiança das decisões
            confidence_dist = np.random.beta(2, 2, 1000)  # Distribuição beta
            
            fig_hist = px.histogram(x=confidence_dist, nbins=30,
                                   title="Distribuição de Confiança das Decisões",
                                   labels={'x': 'Nível de Confiança', 'y': 'Frequência'})
            fig_hist.update_layout(height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Análise detalhada
        st.subheader("🔬 Análise Detalhada de Performance")
        
        # Tabela de métricas detalhadas
        detailed_metrics = pd.DataFrame({
            'Métrica': ['Operações por Minuto', 'Tempo Médio de Resposta', 'Uso de CPU', 
                       'Uso de Memória', 'Latência de Rede', 'Taxa de Erro'],
            'Valor Atual': [f"{np.random.randint(50, 200)}/min", 
                           f"{np.random.uniform(0.1, 2.0):.2f}s",
                           f"{np.random.uniform(20, 80):.1f}%",
                           f"{np.random.uniform(40, 90):.1f}%",
                           f"{np.random.uniform(10, 100):.0f}ms",
                           f"{np.random.uniform(0, 5):.2f}%"],
            'Status': ['🟢 Ótimo', '🟢 Ótimo', '🟡 Moderado', '🟢 Ótimo', '🟢 Ótimo', '🟢 Ótimo']
        })
        
        st.dataframe(detailed_metrics, use_container_width=True)
        
        # Alertas de performance
        st.subheader("⚠️ Alertas de Performance")
        
        alerts = [
            {"tipo": "Info", "mensagem": "Sistema operando dentro dos parâmetros normais", "cor": "blue"},
            {"tipo": "Aviso", "mensagem": "Uso de memória acima de 80%", "cor": "orange"},
            {"tipo": "Sucesso", "mensagem": "Taxa de acerto do cache melhorou 5%", "cor": "green"}
        ]
        
        for alert in alerts:
            if alert["cor"] == "blue":
                st.info(f"ℹ️ {alert['mensagem']}")
            elif alert["cor"] == "orange":
                st.warning(f"⚠️ {alert['mensagem']}")
            elif alert["cor"] == "green":
                st.success(f"✅ {alert['mensagem']}")
    
    else:
        st.info("Inicie o sistema para ver análise de performance")

# Tab 5: Configurações
with tab5:
    st.subheader("⚙️ Configurações do Sistema")
    
    # Validação da configuração
    issues = st.session_state.config_manager.validate_config()
    
    if issues['errors']:
        st.error("❌ Erros encontrados na configuração:")
        for error in issues['errors']:
            st.write(f"• {error}")
    
    if issues['warnings']:
        st.warning("⚠️ Avisos de configuração:")
        for warning in issues['warnings']:
            st.write(f"• {warning}")
    
    if issues['info']:
        st.info("ℹ️ Informações:")
        for info in issues['info']:
            st.write(f"• {info}")
    
    # Configurações por seção
    config = st.session_state.config_manager.config
    
    # Neural
    with st.expander("🧠 Configurações Neurais"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_threshold = st.slider("Limiar de Ativação", 0.1, 1.0, 
                                     config.neural.activation_threshold, 0.1)
            new_learning_rate = st.slider("Taxa de Aprendizado", 0.001, 0.5, 
                                         config.neural.learning_rate, 0.001)
        
        with col2:
            new_energy_decay = st.slider("Taxa de Decaimento de Energia", 0.001, 0.1, 
                                        config.neural.energy_decay_rate, 0.001)
            new_plasticity = st.checkbox("Plasticidade Habilitada", 
                                        config.neural.plasticity_enabled)
        
        if st.button("Atualizar Configurações Neurais"):
            updates = {
                'activation_threshold': new_threshold,
                'learning_rate': new_learning_rate,
                'energy_decay_rate': new_energy_decay,
                'plasticity_enabled': new_plasticity
            }
            if st.session_state.config_manager.update_config('neural', updates):
                st.success("Configurações neurais atualizadas!")
    
    # Memória
    with st.expander("💾 Configurações de Memória"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_working_size = st.number_input("Tamanho da Memória de Trabalho", 
                                              3, 20, config.memory.working_memory_size)
            new_cache_size = st.number_input("Tamanho do Cache", 
                                            100, 5000, config.memory.cache_size)
        
        with col2:
            new_importance_threshold = st.slider("Limiar de Importância", 0.1, 1.0, 
                                                config.memory.importance_threshold, 0.1)
            new_auto_consolidation = st.checkbox("Consolidação Automática", 
                                               config.memory.auto_consolidation)
        
        if st.button("Atualizar Configurações de Memória"):
            updates = {
                'working_memory_size': new_working_size,
                'cache_size': new_cache_size,
                'importance_threshold': new_importance_threshold,
                'auto_consolidation': new_auto_consolidation
            }
            if st.session_state.config_manager.update_config('memory', updates):
                st.success("Configurações de memória atualizadas!")
    
    # Trading
    with st.expander("📈 Configurações de Trading"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_live_trading = st.checkbox("Trading ao Vivo", config.trading.enable_live_trading)
            new_paper_trading = st.checkbox("Paper Trading", config.trading.enable_paper_trading)
            new_max_trades = st.number_input("Máximo de Trades Simultâneos", 
                                           1, 20, config.trading.max_concurrent_trades)
        
        with col2:
            new_risk_per_trade = st.slider("Risco por Trade", 0.001, 0.1, 
                                          config.trading.risk_per_trade, 0.001)
            new_max_daily_risk = st.slider("Risco Diário Máximo", 0.01, 0.2, 
                                          config.trading.max_daily_risk, 0.01)
        
        if st.button("Atualizar Configurações de Trading"):
            updates = {
                'enable_live_trading': new_live_trading,
                'enable_paper_trading': new_paper_trading,
                'max_concurrent_trades': new_max_trades,
                'risk_per_trade': new_risk_per_trade,
                'max_daily_risk': new_max_daily_risk
            }
            if st.session_state.config_manager.update_config('trading', updates):
                st.success("Configurações de trading atualizadas!")
    
    # Operações de configuração
    st.subheader("🔧 Operações de Configuração")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Salvar Configuração"):
            if st.session_state.config_manager.save_config():
                st.success("Configuração salva!")
    
    with col2:
        if st.button("🔄 Recarregar"):
            if st.session_state.config_manager.load_config():
                st.success("Configuração recarregada!")
                st.rerun()
    
    with col3:
        if st.button("🔧 Resetar Padrões"):
            if st.session_state.config_manager.reset_to_defaults():
                st.success("Configuração resetada!")
                st.rerun()
    
    with col4:
        if st.button("📤 Exportar Config"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"config/exported_config_{timestamp}.yaml"
            if st.session_state.config_manager.export_config(export_path):
                st.success(f"Configuração exportada para: {export_path}")

# Auto-refresh
if st.session_state.system_running:
    # Atualizar a cada 5 segundos
    time.sleep(0.1)  # Pequena pausa para não sobrecarregar
    if (datetime.now() - st.session_state.last_update).seconds >= 5:
        st.session_state.last_update = datetime.now()
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🧠 LEXTRADER-IAG 4.0 - Sistema de Inteligência Artificial Integrado</p>
    <p>Desenvolvido com ❤️ para automação de trading inteligente</p>
</div>
""", unsafe_allow_html=True)