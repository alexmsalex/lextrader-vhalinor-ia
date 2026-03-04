import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import random

# --- TYPES ---
@dataclass
class MemoryEngram:
    pattern_name: str
    timestamp: datetime
    outcome: str
    synaptic_strength: float
    is_apex: bool = False

# --- STREAMLIT COMPONENT ---
def render_memory_core(active_memories: List[MemoryEngram], total_memories: int):
    """
    Renderiza o componente Córtex de Memória Contínua
    
    Args:
        active_memories: Lista de memórias ativas/recuperadas
        total_memories: Total de engramas armazenados
    """
    
    # CSS Styles
    st.markdown("""
    <style>
        .matrix-panel {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 0.5rem;
            padding: 1rem;
            position: relative;
            overflow: hidden;
        }
        
        .matrix-panel::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(ellipse at center, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
            pointer-events: none;
        }
        
        .memory-grid {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 0.125rem;
            height: 8rem;
        }
        
        .grid-cell {
            border-radius: 0.125rem;
            transition: all 1s ease;
        }
        
        .grid-cell-active {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            box-shadow: 0 0 5px #6366f1;
        }
        
        .grid-cell-inactive {
            background-color: #1f2937;
        }
        
        .engram-card {
            padding: 0.5rem;
            border-radius: 0.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
            margin-bottom: 0.5rem;
        }
        
        .engram-apex {
            background: rgba(234, 179, 8, 0.1);
            border: 1px solid rgba(234, 179, 8, 0.5);
            box-shadow: 0 0 10px rgba(234, 179, 8, 0.1);
        }
        
        .engram-normal {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        
        .engram-normal:hover {
            border-color: rgba(99, 102, 241, 0.5);
        }
        
        .strength-bar {
            width: 4rem;
            height: 0.125rem;
            background-color: #1f2937;
            border-radius: 0.0625rem;
            overflow: hidden;
            margin-top: 0.125rem;
        }
        
        .strength-fill {
            height: 100%;
            border-radius: 0.0625rem;
        }
        
        .strength-apex {
            background-color: #eab308;
            box-shadow: 0 0 5px #eab308;
        }
        
        .strength-normal {
            background: linear-gradient(90deg, #4f46e5 0%, #8b5cf6 100%);
        }
        
        .scroll-container {
            max-height: 8rem;
            overflow-y: auto;
            padding-right: 0.25rem;
        }
        
        .scroll-container::-webkit-scrollbar {
            width: 4px;
        }
        
        .scroll-container::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 2px;
        }
        
        .scroll-container::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.5);
            border-radius: 2px;
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Generate memory grid visualization
    grid_cells = []
    for i in range(64):
        is_active = random.random() > 0.8
        intensity = random.random() if is_active else 0.2
        grid_cells.append({
            'id': i,
            'active': is_active,
            'intensity': intensity
        })
    
    # Main container
    st.markdown(f"""
    <div class="matrix-panel">
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; position: relative; z-index: 1;">
            <h3 style="font-size: 0.875rem; font-weight: bold; color: #818cf8; display: flex; align-items: center; gap: 0.5rem;">
                <span class="pulse">🧠</span> CÓRTEX DE MEMÓRIA CONTÍNUA
            </h3>
            <div style="font-size: 0.625rem; color: #6b7280; font-family: monospace;">
                ENGRAMAS TOTAIS: <span style="color: white;">{total_memories:,}</span>
            </div>
        </div>
        
        <!-- Content -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; position: relative; z-index: 1;">
            
            <!-- LEFT: Memory Activation Visualizer -->
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <div style="font-size: 0.625rem; color: #6b7280; text-transform: uppercase; font-family: monospace; margin-bottom: 0.25rem;">
                    Mapa de Ativação Sináptica
                </div>
                
                <div class="memory-grid">
    """, unsafe_allow_html=True)
    
    # Render grid cells
    for cell in grid_cells:
        cell_class = "grid-cell-active" if cell['active'] else "grid-cell-inactive"
        opacity = cell['intensity'] if cell['active'] else 0.2
        
        st.markdown(f"""
        <div class="grid-cell {cell_class}" style="opacity: {opacity};"></div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
                </div>
                
                <div style="display: flex; justify-content: space-between; font-size: 0.5625rem; color: #4b5563; margin-top: 0.25rem;">
                    <span>Plasticidade: ALTA</span>
                    <span>Consolidação: 98%</span>
                </div>
            </div>
            
            <!-- RIGHT: Active Engrams List -->
            <div style="display: flex; flex-direction: column; height: 100%;">
                <div style="font-size: 0.625rem; color: #6b7280; text-transform: uppercase; font-family: monospace; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.25rem;">
                    <span style="color: #eab308;">⚡</span> Engramas Recuperados (Contexto Atual)
                </div>
                
                <div class="scroll-container">
    """, unsafe_allow_html=True)
    
    # Render active memories
    if active_memories:
        for idx, mem in enumerate(active_memories):
            is_apex = mem.is_apex
            engram_class = "engram-apex" if is_apex else "engram-normal"
            title_color = "#fbbf24" if is_apex else "white"
            outcome_color = "#10b981" if mem.outcome == "SUCCESS" else "#ef4444"
            
            # Clean pattern name
            pattern_name = mem.pattern_name.replace('[APEX] ', '')
            
            # Format date
            date_str = mem.timestamp.strftime("%d/%m/%Y")
            
            # Synaptic strength
            strength = mem.synaptic_strength or 0.5
            strength_percent = strength * 100
            strength_class = "strength-apex" if is_apex else "strength-normal"
            strength_text = "100% EFICÁCIA" if is_apex else "Força Sináptica"
            
            st.markdown(f"""
            <div class="engram-card {engram_class}">
                <div>
                    <div style="font-size: 0.625rem; font-weight: bold; color: {title_color}; display: flex; align-items: center; gap: 0.25rem;">
                        {('⭐' if is_apex else '')} {pattern_name}
                    </div>
                    <div style="font-size: 0.5625rem; color: #6b7280; display: flex; align-items: center; gap: 0.5rem; margin-top: 0.125rem;">
                        <span style="color: {outcome_color};">{mem.outcome}</span>
                        <span style="display: flex; align-items: center; gap: 0.125rem;">🕒 {date_str}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.5625rem; color: {'#eab308' if is_apex else '#9ca3af'}; margin-bottom: 0.125rem;">
                        {strength_text}
                    </div>
                    <div class="strength-bar">
                        <div class="strength-fill {strength_class}" style="width: {strength_percent}%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="font-size: 0.625rem; color: #6b7280; font-style: italic; text-align: center; padding: 1rem; border: 1px dashed #374151; border-radius: 0.25rem;">
                Nenhum engrama semelhante detectado no buffer de curto prazo.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def create_sample_memories(count: int = 5) -> List[MemoryEngram]:
    """Cria memórias de exemplo para demonstração"""
    sample_patterns = [
        "Padrão de Alta Frequência",
        "Sequência Fibonacci",
        "Resposta ao Medo",
        "Recompensa Positiva",
        "Ponto de Virada",
        "Padrão de Confiança",
        "Estabilidade Temporal",
        "Divergência de Preço",
        "Retorno à Média",
        "Momentum Inverso"
    ]
    
    apex_patterns = [
        "[APEX] Memória de Sucesso Total",
        "[APEX] Experiência Ótima",
        "[APEX] Pico de Performance"
    ]
    
    memories = []
    
    for i in range(count):
        is_apex = random.random() > 0.8
        if is_apex and len(apex_patterns) > 0:
            pattern = random.choice(apex_patterns)
        else:
            pattern = random.choice(sample_patterns)
        
        memory = MemoryEngram(
            pattern_name=pattern,
            timestamp=datetime.now() - timedelta(days=random.randint(0, 365)),
            outcome=random.choice(["SUCCESS", "FAILURE", "NEUTRAL"]),
            synaptic_strength=random.uniform(0.3, 1.0),
            is_apex=is_apex
        )
        memories.append(memory)
    
    return memories

# --- EXAMPLE USAGE ---
def main():
    st.set_page_config(
        page_title="Memory Core - Neural Matrix",
        page_icon="🧠",
        layout="centered"
    )
    
    st.title("🧠 Córtex de Memória Contínua")
    st.markdown("---")
    
    # Create sample data
    sample_memories = create_sample_memories(6)
    total_memories = 123456
    
    # Render the component
    render_memory_core(sample_memories, total_memories)
    
    # Add controls
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Atualizar Memórias"):
            st.rerun()
    
    with col2:
        show_details = st.checkbox("Mostrar Detalhes")
    
    with col3:
        st.metric("Taxa de Recuperação", "87.3%", "2.1%")
    
    if show_details:
        st.markdown("### 📋 Detalhes das Memórias")
        df = pd.DataFrame([
            {
                "Padrão": m.pattern_name,
                "Data": m.timestamp.strftime("%d/%m/%Y"),
                "Resultado": m.outcome,
                "Força": f"{m.synaptic_strength*100:.1f}%",
                "APEX": "⭐" if m.is_apex else ""
            }
            for m in sample_memories
        ])
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()