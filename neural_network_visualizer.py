"""
LEXTRADER-IAG 4.0 - Visualizador de Rede Neural
================================================
Visualização gráfica da rede neural mostrando conexões entre arquivos/neurônios
em blocos verticais organizados por camadas.

Versão: 1.0.0
Data: Janeiro 2026
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import random

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib não disponível. Visualização limitada.")

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    print("NetworkX não disponível. Análise de grafos desabilitada.")


class NeuralNetworkVisualizer:
    """Visualizador de rede neural com interface gráfica"""

    def __init__(self, root):
        self.root = root
        self.root.title("LEXTRADER-IAG 4.0 - Visualizador de Rede Neural")
        self.root.geometry("1400x900")
        
        # Dados da rede
        self.neurons = {}
        self.connections = []
        self.layers = {}
        
        # Cores por tipo de neurônio
        self.neuron_colors = {
            'sensory': '#FF6B6B',      # Vermelho
            'processing': '#4ECDC4',   # Ciano
            'memory': '#95E1D3',       # Verde claro
            'decision': '#FFD93D',     # Amarelo
            'output': '#6BCB77',       # Verde
            'quantum': '#9D4EDD',      # Roxo
            'analytical': '#3A86FF',   # Azul
            'security': '#FB5607',     # Laranja
            'api': '#8338EC',          # Roxo escuro
            'database': '#06FFA5',     # Verde neon
            'default': '#CCCCCC'       # Cinza
        }
        
        # Configuração da interface
        self.setup_ui()
        
        # Carrega dados de exemplo
        self.load_sample_data()
        
        # Desenha a rede
        self.draw_network()

    def setup_ui(self):
        """Configura interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior - Controles
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botões
        ttk.Button(control_frame, text="🔄 Atualizar", 
                  command=self.refresh_network).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📊 Estatísticas", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔍 Buscar Neurônio", 
                  command=self.search_neuron).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 Exportar", 
                  command=self.export_network).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🎨 Mudar Layout", 
                  command=self.change_layout).pack(side=tk.LEFT, padx=5)
        
        # Filtros
        ttk.Label(control_frame, text="Filtrar por tipo:").pack(side=tk.LEFT, padx=(20, 5))
        self.filter_var = tk.StringVar(value="Todos")
        filter_combo = ttk.Combobox(control_frame, textvariable=self.filter_var, 
                                    values=["Todos", "sensory", "processing", "memory", 
                                           "decision", "output", "quantum", "analytical"],
                                    width=15, state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
        
        # Frame do meio - Visualização
        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para visualização
        if MATPLOTLIB_AVAILABLE:
            self.fig = Figure(figsize=(14, 8), facecolor='#1a1a1a')
            self.ax = self.fig.add_subplot(111, facecolor='#1a1a1a')
            self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            # Fallback para canvas simples
            self.canvas = tk.Canvas(viz_frame, bg='#1a1a1a')
            self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame inferior - Informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações da Rede", padding=10)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Texto de informações
        self.info_text = scrolledtext.ScrolledText(info_frame, height=8, 
                                                   bg='#2a2a2a', fg='#00ff00',
                                                   font=('Consolas', 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_sample_data(self):
        """Carrega dados de exemplo da rede neural"""
        # Define camadas
        self.layers = {
            'Entrada': [],
            'Processamento 1': [],
            'Processamento 2': [],
            'Memória': [],
            'Decisão': [],
            'Saída': []
        }
        
        # Neurônios de entrada (sensores)
        input_neurons = [
            ('crypto_analysis', 'sensory', 'Entrada'),
            ('forex_analysis', 'sensory', 'Entrada'),
            ('arbitrage_analysis', 'sensory', 'Entrada'),
            ('market_data', 'sensory', 'Entrada'),
        ]
        
        # Neurônios de processamento
        processing_neurons = [
            ('data_analyzer', 'processing', 'Processamento 1'),
            ('pattern_recognizer', 'analytical', 'Processamento 1'),
            ('risk_analyzer', 'analytical', 'Processamento 1'),
            ('quantum_core', 'quantum', 'Processamento 2'),
            ('quantum_algorithms', 'quantum', 'Processamento 2'),
            ('neural_bus', 'processing', 'Processamento 2'),
        ]
        
        # Neurônios de memória
        memory_neurons = [
            ('advanced_memory', 'memory', 'Memória'),
            ('neural_connection_matrix', 'memory', 'Memória'),
            ('brain_memory_db', 'database', 'Memória'),
        ]
        
        # Neurônios de decisão
        decision_neurons = [
            ('decision_engine', 'decision', 'Decisão'),
            ('autonomous_manager', 'decision', 'Decisão'),
            ('ml_module', 'analytical', 'Decisão'),
        ]
        
        # Neurônios de saída
        output_neurons = [
            ('autotrader', 'output', 'Saída'),
            ('trading_controller', 'output', 'Saída'),
            ('api_interface', 'api', 'Saída'),
        ]
        
        # Adiciona todos os neurônios
        all_neurons = (input_neurons + processing_neurons + 
                      memory_neurons + decision_neurons + output_neurons)
        
        neuron_id = 0
        for name, ntype, layer in all_neurons:
            neuron_data = {
                'id': neuron_id,
                'name': name,
                'type': ntype,
                'layer': layer,
                'activation': random.uniform(0, 1),
                'connections': []
            }
            self.neurons[neuron_id] = neuron_data
            self.layers[layer].append(neuron_id)
            neuron_id += 1
        
        # Cria conexões entre camadas
        self.create_connections()
        
        self.log_info("✅ Dados da rede carregados com sucesso")
        self.log_info(f"📊 Total de neurônios: {len(self.neurons)}")
        self.log_info(f"🔗 Total de conexões: {len(self.connections)}")

    def create_connections(self):
        """Cria conexões entre neurônios"""
        layer_names = list(self.layers.keys())
        
        # Conecta camadas sequencialmente
        for i in range(len(layer_names) - 1):
            current_layer = self.layers[layer_names[i]]
            next_layer = self.layers[layer_names[i + 1]]
            
            # Cada neurônio da camada atual conecta com alguns da próxima
            for source_id in current_layer:
                # Conecta com 2-4 neurônios da próxima camada
                num_connections = min(random.randint(2, 4), len(next_layer))
                targets = random.sample(next_layer, num_connections)
                
                for target_id in targets:
                    weight = random.uniform(0.3, 1.0)
                    self.connections.append({
                        'source': source_id,
                        'target': target_id,
                        'weight': weight
                    })
                    self.neurons[source_id]['connections'].append(target_id)
        
        # Adiciona algumas conexões recorrentes (feedback)
        for _ in range(5):
            source = random.choice(list(self.neurons.keys()))
            target = random.choice(list(self.neurons.keys()))
            if source != target:
                self.connections.append({
                    'source': source,
                    'target': target,
                    'weight': random.uniform(0.1, 0.5),
                    'recurrent': True
                })

    def draw_network(self):
        """Desenha a rede neural"""
        if not MATPLOTLIB_AVAILABLE:
            self.draw_simple_network()
            return
        
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        self.ax.set_title('LEXTRADER-IAG 4.0 - Rede Neural', 
                         color='white', fontsize=16, fontweight='bold')
        
        # Posições dos neurônios em blocos verticais
        positions = {}
        layer_names = list(self.layers.keys())
        layer_width = 1.0 / (len(layer_names) + 1)
        
        for i, layer_name in enumerate(layer_names):
            layer_neurons = self.layers[layer_name]
            x = (i + 1) * layer_width
            
            if len(layer_neurons) > 0:
                y_spacing = 0.8 / len(layer_neurons)
                for j, neuron_id in enumerate(layer_neurons):
                    y = 0.1 + (j + 0.5) * y_spacing
                    positions[neuron_id] = (x, y)
        
        # Desenha conexões
        for conn in self.connections:
            source_id = conn['source']
            target_id = conn['target']
            
            if source_id in positions and target_id in positions:
                x1, y1 = positions[source_id]
                x2, y2 = positions[target_id]
                
                # Cor baseada no peso
                weight = conn['weight']
                alpha = weight * 0.6
                color = '#00ff00' if not conn.get('recurrent') else '#ff00ff'
                
                self.ax.plot([x1, x2], [y1, y2], 
                           color=color, alpha=alpha, linewidth=weight*2,
                           zorder=1)
        
        # Desenha neurônios
        for neuron_id, neuron in self.neurons.items():
            if neuron_id in positions:
                x, y = positions[neuron_id]
                
                # Cor baseada no tipo
                color = self.neuron_colors.get(neuron['type'], 
                                              self.neuron_colors['default'])
                
                # Tamanho baseado na ativação
                size = 300 + (neuron['activation'] * 500)
                
                # Desenha círculo
                self.ax.scatter(x, y, s=size, c=color, 
                              edgecolors='white', linewidths=2,
                              alpha=0.8, zorder=2)
                
                # Label
                self.ax.text(x, y, neuron['name'][:8], 
                           ha='center', va='center',
                           fontsize=7, color='black', fontweight='bold',
                           zorder=3)
        
        # Labels das camadas
        for i, layer_name in enumerate(layer_names):
            x = (i + 1) * layer_width
            self.ax.text(x, 0.95, layer_name, 
                       ha='center', va='top',
                       fontsize=10, color='white', fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='#333333', alpha=0.8))
        
        # Legenda
        legend_elements = [
            mpatches.Patch(color=self.neuron_colors['sensory'], label='Sensorial'),
            mpatches.Patch(color=self.neuron_colors['processing'], label='Processamento'),
            mpatches.Patch(color=self.neuron_colors['memory'], label='Memória'),
            mpatches.Patch(color=self.neuron_colors['decision'], label='Decisão'),
            mpatches.Patch(color=self.neuron_colors['quantum'], label='Quântico'),
            mpatches.Patch(color=self.neuron_colors['output'], label='Saída'),
        ]
        self.ax.legend(handles=legend_elements, loc='upper left',
                      facecolor='#2a2a2a', edgecolor='white',
                      labelcolor='white', fontsize=8)
        
        self.ax.set_xlim(-0.05, 1.05)
        self.ax.set_ylim(-0.05, 1.05)
        self.ax.axis('off')
        
        self.canvas.draw()
        self.status_var.set(f"Rede desenhada: {len(self.neurons)} neurônios, {len(self.connections)} conexões")

    def draw_simple_network(self):
        """Desenha rede simples sem matplotlib"""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1:
            width = 1200
        if height <= 1:
            height = 600
        
        # Desenha camadas
        layer_names = list(self.layers.keys())
        layer_width = width / (len(layer_names) + 1)
        
        positions = {}
        
        for i, layer_name in enumerate(layer_names):
            layer_neurons = self.layers[layer_name]
            x = (i + 1) * layer_width
            
            # Label da camada
            self.canvas.create_text(x, 30, text=layer_name, 
                                   fill='white', font=('Arial', 10, 'bold'))
            
            if len(layer_neurons) > 0:
                y_spacing = (height - 100) / len(layer_neurons)
                for j, neuron_id in enumerate(layer_neurons):
                    y = 80 + (j + 0.5) * y_spacing
                    positions[neuron_id] = (x, y)
                    
                    # Desenha neurônio
                    neuron = self.neurons[neuron_id]
                    color = self.neuron_colors.get(neuron['type'], 
                                                  self.neuron_colors['default'])
                    
                    radius = 15 + (neuron['activation'] * 10)
                    self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                          fill=color, outline='white', width=2)
                    
                    # Label
                    self.canvas.create_text(x, y, text=neuron['name'][:6],
                                          fill='black', font=('Arial', 7, 'bold'))
        
        # Desenha conexões
        for conn in self.connections:
            source_id = conn['source']
            target_id = conn['target']
            
            if source_id in positions and target_id in positions:
                x1, y1 = positions[source_id]
                x2, y2 = positions[target_id]
                
                color = '#00ff00' if not conn.get('recurrent') else '#ff00ff'
                width = int(conn['weight'] * 3)
                
                self.canvas.create_line(x1, y1, x2, y2, 
                                      fill=color, width=width, arrow=tk.LAST)

    def refresh_network(self):
        """Atualiza visualização da rede"""
        # Atualiza ativações
        for neuron in self.neurons.values():
            neuron['activation'] = random.uniform(0, 1)
        
        self.draw_network()
        self.log_info("🔄 Rede atualizada")

    def show_statistics(self):
        """Mostra estatísticas da rede"""
        stats = f"""
╔══════════════════════════════════════════════════════════════╗
║           ESTATÍSTICAS DA REDE NEURAL                        ║
╚══════════════════════════════════════════════════════════════╝

📊 Neurônios por Tipo:
"""
        # Conta neurônios por tipo
        type_counts = {}
        for neuron in self.neurons.values():
            ntype = neuron['type']
            type_counts[ntype] = type_counts.get(ntype, 0) + 1
        
        for ntype, count in sorted(type_counts.items()):
            stats += f"   • {ntype.capitalize()}: {count}\n"
        
        stats += f"""
🔗 Conexões:
   • Total: {len(self.connections)}
   • Média por neurônio: {len(self.connections) / len(self.neurons):.2f}
   • Recorrentes: {sum(1 for c in self.connections if c.get('recurrent', False))}

📈 Ativação:
   • Média: {sum(n['activation'] for n in self.neurons.values()) / len(self.neurons):.2%}
   • Máxima: {max(n['activation'] for n in self.neurons.values()):.2%}
   • Mínima: {min(n['activation'] for n in self.neurons.values()):.2%}

🏗️ Camadas:
"""
        for layer_name, neurons in self.layers.items():
            stats += f"   • {layer_name}: {len(neurons)} neurônios\n"
        
        self.log_info(stats)
        messagebox.showinfo("Estatísticas da Rede", stats)

    def search_neuron(self):
        """Busca neurônio específico"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Buscar Neurônio")
        search_window.geometry("400x300")
        
        ttk.Label(search_window, text="Nome do neurônio:").pack(pady=10)
        search_entry = ttk.Entry(search_window, width=40)
        search_entry.pack(pady=5)
        
        result_text = scrolledtext.ScrolledText(search_window, height=10)
        result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        def do_search():
            query = search_entry.get().lower()
            results = []
            
            for neuron_id, neuron in self.neurons.items():
                if query in neuron['name'].lower():
                    results.append(f"ID: {neuron_id}\n"
                                 f"Nome: {neuron['name']}\n"
                                 f"Tipo: {neuron['type']}\n"
                                 f"Camada: {neuron['layer']}\n"
                                 f"Ativação: {neuron['activation']:.2%}\n"
                                 f"Conexões: {len(neuron['connections'])}\n"
                                 f"{'-'*40}\n")
            
            result_text.delete(1.0, tk.END)
            if results:
                result_text.insert(1.0, ''.join(results))
            else:
                result_text.insert(1.0, "Nenhum neurônio encontrado.")
        
        ttk.Button(search_window, text="Buscar", command=do_search).pack(pady=5)

    def export_network(self):
        """Exporta dados da rede"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"neural_network_export_{timestamp}.json"
        
        export_data = {
            'timestamp': timestamp,
            'neurons': self.neurons,
            'connections': self.connections,
            'layers': self.layers,
            'statistics': {
                'total_neurons': len(self.neurons),
                'total_connections': len(self.connections),
                'layers': len(self.layers)
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            self.log_info(f"✅ Rede exportada para {filename}")
            messagebox.showinfo("Exportação", f"Rede exportada com sucesso!\n{filename}")
        except Exception as e:
            self.log_info(f"❌ Erro ao exportar: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")

    def change_layout(self):
        """Muda layout da visualização"""
        self.draw_network()
        self.log_info("🎨 Layout atualizado")

    def apply_filter(self):
        """Aplica filtro por tipo de neurônio"""
        filter_type = self.filter_var.get()
        
        if filter_type == "Todos":
            self.draw_network()
        else:
            # Filtra neurônios
            # Implementação simplificada - redesenha com destaque
            self.draw_network()
            self.log_info(f"🔍 Filtro aplicado: {filter_type}")

    def log_info(self, message: str):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.info_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.info_text.see(tk.END)


def main():
    """Função principal"""
    root = tk.Tk()
    app = NeuralNetworkVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
