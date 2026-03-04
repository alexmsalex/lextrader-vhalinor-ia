import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from dataclasses import dataclass
from typing import List, Literal
from datetime import datetime, timedelta
import threading
import time
import random
import math

@dataclass
class LearningProgram:
    """Estrutura para programa de aprendizagem (equivalente à interface LearningProgram)"""
    id: str
    name: str
    type: Literal['trading', 'analysis', 'prediction', 'risk', 'optimization', 'neural']
    status: Literal['active', 'learning', 'sharing', 'syncing', 'idle']
    knowledge: float
    accuracy: float
    learning_rate: float
    shared_knowledge: float
    received_knowledge: float
    contribution_score: float
    last_update: datetime
    connections: List[str]

@dataclass
class KnowledgeTransfer:
    """Estrutura para transferência de conhecimento (equivalente à interface KnowledgeTransfer)"""
    id: str
    from_program: str
    to_program: str
    type: Literal['pattern', 'strategy', 'model', 'insight', 'correction']
    data: str
    confidence: float
    impact: float
    timestamp: datetime
    status: Literal['transferring', 'completed', 'failed', 'validating']

@dataclass
class ShareMetrics:
    """Estrutura para métricas de compartilhamento (equivalente à interface ShareMetrics)"""
    total_programs: int
    active_sharing: int
    knowledge_volume: float
    transfer_rate: float
    sync_efficiency: float
    network_health: float
    redundancy: float
    consensus_level: float

class NeuralLearningShareApp:
    """Aplicação principal que replica a funcionalidade do componente React NeuralLearningShare"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🧠 Compartilhamento Neural de Aprendizagem")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação (equivalente aos useState hooks)
        self.programs: List[LearningProgram] = []
        self.transfers: List[KnowledgeTransfer] = []
        self.metrics = ShareMetrics(0, 0, 0, 0, 0, 0, 0, 0)
        self.share_enabled = True
        self.auto_sync = True
        
        # Widgets principais
        self.notebook = None
        self.share_switch = None
        self.auto_sync_switch = None
        self.network_figure = None
        self.network_canvas = None
        self.status_indicators = {}
        
        # Thread de atualização
        self.update_thread = None
        self.stop_updates = False
        
        # Configurar estilos matplotlib
        self.setup_plot_style()
        
        # Inicializar dados
        self.initialize_data()
        
        # Configurar interface
        self.setup_ui()
        
        # Iniciar atualizações (equivalente ao useEffect)
        self.start_updates()
    
    def setup_plot_style(self) -> None:
        """Configurar estilo dos gráficos matplotlib"""
        plt.style.use('dark_background')
        plt.rcParams.update({
            'axes.facecolor': '#1f2937',
            'figure.facecolor': '#111827',
            'text.color': 'white',
            'axes.labelcolor': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'grid.color': '#374151',
            'grid.alpha': 0.3
        })
    
    # Funções de inicialização de dados (equivalentes às funções utilitárias do React)
    def create_initial_programs(self) -> List[LearningProgram]:
        """Criar programas iniciais (equivalente a createInitialPrograms)"""
        return [
            LearningProgram(
                id='trading-ai',
                name='Trading AI Core',
                type='trading',
                status='active',
                knowledge=85.0,
                accuracy=92.0,
                learning_rate=0.8,
                shared_knowledge=120.0,
                received_knowledge=95.0,
                contribution_score=8.5,
                last_update=datetime.now(),
                connections=['risk-analyzer', 'pattern-detector', 'neural-engine']
            ),
            LearningProgram(
                id='pattern-detector',
                name='Pattern Recognition',
                type='analysis',
                status='learning',
                knowledge=78.0,
                accuracy=88.0,
                learning_rate=1.2,
                shared_knowledge=85.0,
                received_knowledge=110.0,
                contribution_score=7.8,
                last_update=datetime.now(),
                connections=['trading-ai', 'market-predictor', 'neural-engine']
            ),
            LearningProgram(
                id='risk-analyzer',
                name='Risk Management',
                type='risk',
                status='sharing',
                knowledge=91.0,
                accuracy=95.0,
                learning_rate=0.6,
                shared_knowledge=140.0,
                received_knowledge=75.0,
                contribution_score=9.1,
                last_update=datetime.now(),
                connections=['trading-ai', 'portfolio-optimizer']
            ),
            LearningProgram(
                id='market-predictor',
                name='Market Prediction',
                type='prediction',
                status='syncing',
                knowledge=82.0,
                accuracy=89.0,
                learning_rate=1.0,
                shared_knowledge=95.0,
                received_knowledge=105.0,
                contribution_score=8.2,
                last_update=datetime.now(),
                connections=['pattern-detector', 'neural-engine']
            ),
            LearningProgram(
                id='portfolio-optimizer',
                name='Portfolio Optimizer',
                type='optimization',
                status='active',
                knowledge=87.0,
                accuracy=93.0,
                learning_rate=0.7,
                shared_knowledge=105.0,
                received_knowledge=90.0,
                contribution_score=8.7,
                last_update=datetime.now(),
                connections=['risk-analyzer', 'trading-ai']
            ),
            LearningProgram(
                id='neural-engine',
                name='Neural Processing Engine',
                type='neural',
                status='learning',
                knowledge=94.0,
                accuracy=97.0,
                learning_rate=1.5,
                shared_knowledge=160.0,
                received_knowledge=130.0,
                contribution_score=9.4,
                last_update=datetime.now(),
                connections=['trading-ai', 'pattern-detector', 'market-predictor']
            )
        ]
    
    def create_initial_transfers(self) -> List[KnowledgeTransfer]:
        """Criar transferências iniciais (equivalente a createInitialTransfers)"""
        transfers = []
        transfer_types = ['pattern', 'strategy', 'model', 'insight', 'correction']
        sample_data = [
            'Padrão de reversão identificado em EUR/USD',
            'Estratégia de breakout otimizada',
            'Modelo neural de previsão de volatilidade',
            'Insight sobre correlações de pares',
            'Correção de bias em análise de sentimento'
        ]
        
        for i in range(8):
            from_program = random.choice(self.programs)
            to_program = random.choice(self.programs)
            if from_program.id != to_program.id:
                transfers.append(KnowledgeTransfer(
                    id=f'transfer-{i}',
                    from_program=from_program.id,
                    to_program=to_program.id,
                    type=random.choice(transfer_types),
                    data=random.choice(sample_data),
                    confidence=random.uniform(60, 100),
                    impact=random.uniform(20, 50),
                    timestamp=datetime.now() - timedelta(seconds=random.randint(0, 3600)),
                    status='completed' if random.random() > 0.8 else 'transferring'
                ))
        
        return transfers
    
    def create_metrics(self) -> ShareMetrics:
        """Criar métricas (equivalente a createMetrics)"""
        active_sharing = len([p for p in self.programs if p.status in ['sharing', 'syncing']])
        total_knowledge = sum(p.shared_knowledge for p in self.programs)
        
        return ShareMetrics(
            total_programs=len(self.programs),
            active_sharing=active_sharing,
            knowledge_volume=total_knowledge,
            transfer_rate=random.uniform(20, 70),
            sync_efficiency=random.uniform(80, 100),
            network_health=random.uniform(85, 100),
            redundancy=random.uniform(70, 100),
            consensus_level=random.uniform(90, 100)
        )
    
    def initialize_data(self) -> None:
        """Inicializar todos os dados"""
        self.programs = self.create_initial_programs()
        self.transfers = self.create_initial_transfers()
        self.metrics = self.create_metrics()
    
    # Funções de atualização (equivalentes às funções do React)
    def update_programs(self) -> None:
        """Atualizar programas (equivalente a updatePrograms)"""
        for program in self.programs:
            # Atualizar conhecimento baseado na taxa de aprendizagem
            program.knowledge = min(100, program.knowledge + (random.random() * 2 - 1) * program.learning_rate)
            program.accuracy = min(100, program.accuracy + (random.random() - 0.5))
            program.shared_knowledge += random.random() * 5
            program.received_knowledge += random.random() * 3
            
            # Mudança ocasional de status
            if random.random() > 0.7:
                program.status = random.choice(['active', 'learning', 'sharing', 'syncing'])
            
            program.last_update = datetime.now()
    
    def create_new_transfer(self) -> KnowledgeTransfer:
        """Criar nova transferência (equivalente a createNewTransfer)"""
        if len(self.programs) < 2:
            return None
        
        from_program = random.choice(self.programs)
        to_program = random.choice(self.programs)
        
        if from_program.id != to_program.id:
            return KnowledgeTransfer(
                id=f'transfer-{int(time.time())}',
                from_program=from_program.id,
                to_program=to_program.id,
                type=random.choice(['pattern', 'strategy', 'model', 'insight', 'correction']),
                data='Transferência automática de conhecimento',
                confidence=random.uniform(60, 100),
                impact=random.uniform(20, 50),
                timestamp=datetime.now(),
                status='transferring'
            )
        
        return None
    
    # Funções utilitárias de cor
    def get_program_type_color(self, type: str) -> str:
        """Obter cor para tipo de programa"""
        colors = {
            'trading': '#10b981',
            'analysis': '#3b82f6',
            'prediction': '#8b5cf6',
            'risk': '#ef4444',
            'optimization': '#f97316',
            'neural': '#ec4899'
        }
        return colors.get(type, '#6b7280')
    
    def get_status_color(self, status: str) -> str:
        """Obter cor para status"""
        colors = {
            'active': '#10b981',
            'learning': '#3b82f6',
            'sharing': '#eab308',
            'syncing': '#8b5cf6',
            'idle': '#6b7280'
        }
        return colors.get(status, '#6b7280')
    
    # Configuração da interface gráfica
    def setup_ui(self) -> None:
        """Configurar interface principal"""
        # Frame principal com scroll
        main_canvas = tk.Canvas(self.root, bg='#f8fafc')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Container principal
        container = ttk.Frame(scrollable_frame, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Card principal
        main_card = ttk.Frame(container, relief='solid', borderwidth=1, padding="20")
        main_card.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Cabeçalho
        self.setup_header(main_card)
        
        # Notebook para abas
        self.setup_notebook(main_card)
        
        # Configurar scroll
        main_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        scrollable_frame.columnconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        main_card.columnconfigure(0, weight=1)
    
    def setup_header(self, parent: ttk.Frame) -> None:
        """Configurar cabeçalho"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Lado esquerdo: título
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(left_frame, text="🔄", font=("Arial", 18)).grid(row=0, column=0, padx=(0, 8))
        ttk.Label(left_frame, text="Compartilhamento Neural de Aprendizagem", 
                 font=("Arial", 18, "bold")).grid(row=0, column=1)
        
        # Lado direito: switches
        right_frame = ttk.Frame(header_frame)
        right_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Switch compartilhamento
        share_frame = ttk.Frame(right_frame)
        share_frame.grid(row=0, column=0, padx=(0, 20))
        
        self.share_var = tk.BooleanVar(value=self.share_enabled)
        share_check = tk.Checkbutton(share_frame, text="Compartilhamento", 
                                    variable=self.share_var,
                                    command=self.toggle_sharing)
        share_check.grid(row=0, column=0)
        
        # Switch auto-sync
        sync_frame = ttk.Frame(right_frame)
        sync_frame.grid(row=0, column=1)
        
        self.sync_var = tk.BooleanVar(value=self.auto_sync)
        sync_check = tk.Checkbutton(sync_frame, text="Auto-Sync", 
                                   variable=self.sync_var,
                                   command=self.toggle_auto_sync)
        sync_check.grid(row=0, column=0)
        
        header_frame.columnconfigure(0, weight=1)
    
    def setup_notebook(self, parent: ttk.Frame) -> None:
        """Configurar notebook com abas"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba Visão Geral
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📊 Visão Geral")
        self.setup_overview_tab(overview_frame)
        
        # Aba Programas
        programs_frame = ttk.Frame(self.notebook)
        self.notebook.add(programs_frame, text="🧠 Programas")
        self.setup_programs_tab(programs_frame)
        
        # Aba Transferências
        transfers_frame = ttk.Frame(self.notebook)
        self.notebook.add(transfers_frame, text="🔄 Transferências")
        self.setup_transfers_tab(transfers_frame)
        
        # Aba Rede
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text="🌐 Rede")
        self.setup_network_tab(network_frame)
        
        # Aba Controles
        controls_frame = ttk.Frame(self.notebook)
        self.notebook.add(controls_frame, text="⚙️ Controles")
        self.setup_controls_tab(controls_frame)
    
    def setup_overview_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de visão geral"""
        container = ttk.Frame(parent, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid de métricas principais
        metrics_grid = ttk.Frame(container)
        metrics_grid.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Cards de métricas
        metrics_cards = [
            ("🌐", "Programas Ativos", lambda: self.metrics.total_programs, "#3b82f6"),
            ("🔄", "Compartilhando", lambda: self.metrics.active_sharing, "#10b981"),
            ("💾", "Volume Conhecimento", lambda: int(self.metrics.knowledge_volume), "#8b5cf6"),
            ("📈", "Taxa Transferência", lambda: f"{int(self.metrics.transfer_rate)}/s", "#f97316")
        ]
        
        self.metric_widgets = {}
        
        for i, (icon, name, value_func, color) in enumerate(metrics_cards):
            card = ttk.Frame(metrics_grid, relief='solid', borderwidth=1, padding="15")
            card.grid(row=0, column=i, sticky=(tk.W, tk.E), padx=5)
            
            # Header
            header_frame = ttk.Frame(card)
            header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
            
            ttk.Label(header_frame, text=icon, font=("Arial", 16)).grid(row=0, column=0, padx=(0, 8))
            ttk.Label(header_frame, text=name, font=("Arial", 9), foreground='#6b7280').grid(row=1, column=0)
            
            # Valor
            value_label = tk.Label(card, text="0", font=("Arial", 20, "bold"), 
                                  fg=color, bg="white")
            value_label.grid(row=1, column=0, pady=(5, 0))
            
            self.metric_widgets[name] = {
                'value_label': value_label,
                'value_func': value_func
            }
            
            card.columnconfigure(0, weight=1)
        
        # Configurar grid
        for i in range(4):
            metrics_grid.columnconfigure(i, weight=1)
        
        # Grid inferior com eficiência da rede e transferências recentes
        bottom_grid = ttk.Frame(container)
        bottom_grid.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Card eficiência da rede
        efficiency_card = ttk.Frame(bottom_grid, relief='solid', borderwidth=1, padding="15")
        efficiency_card.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(efficiency_card, text="Eficiência da Rede", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 15))
        
        # Métricas de eficiência
        efficiency_metrics = [
            ("Sincronização", lambda: self.metrics.sync_efficiency),
            ("Saúde da Rede", lambda: self.metrics.network_health),
            ("Redundância", lambda: self.metrics.redundancy),
            ("Consenso", lambda: self.metrics.consensus_level)
        ]
        
        self.efficiency_widgets = {}
        
        for i, (name, value_func) in enumerate(efficiency_metrics):
            metric_frame = ttk.Frame(efficiency_card)
            metric_frame.grid(row=i+1, column=0, sticky=(tk.W, tk.E), pady=3)
            
            ttk.Label(metric_frame, text=name, font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W)
            
            value_label = tk.Label(metric_frame, text="0%", font=("Arial", 9, "bold"), 
                                  fg="#3b82f6", bg="white")
            value_label.grid(row=0, column=1, sticky=tk.E)
            
            progress_bar = ttk.Progressbar(metric_frame, length=200, mode='determinate')
            progress_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(2, 0))
            
            self.efficiency_widgets[name] = {
                'value_label': value_label,
                'progress_bar': progress_bar,
                'value_func': value_func
            }
            
            metric_frame.columnconfigure(0, weight=1)
        
        # Card transferências recentes
        transfers_card = ttk.Frame(bottom_grid, relief='solid', borderwidth=1, padding="15")
        transfers_card.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        ttk.Label(transfers_card, text="Transferências Recentes", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 10))
        
        # Frame scrollável para transferências
        transfers_canvas = tk.Canvas(transfers_card, height=200, bg='white')
        transfers_scrollbar = ttk.Scrollbar(transfers_card, orient="vertical", command=transfers_canvas.yview)
        self.transfers_frame = ttk.Frame(transfers_canvas)
        
        self.transfers_frame.bind(
            "<Configure>",
            lambda e: transfers_canvas.configure(scrollregion=transfers_canvas.bbox("all"))
        )
        
        transfers_canvas.create_window((0, 0), window=self.transfers_frame, anchor="nw")
        transfers_canvas.configure(yscrollcommand=transfers_scrollbar.set)
        
        transfers_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E))
        transfers_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Configurar grid
        bottom_grid.columnconfigure(0, weight=1)
        bottom_grid.columnconfigure(1, weight=1)
        efficiency_card.columnconfigure(0, weight=1)
        transfers_card.columnconfigure(0, weight=1)
        
        container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_programs_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de programas"""
        # Frame scrollável para programas
        canvas = tk.Canvas(parent, bg='#f8fafc')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.programs_frame = ttk.Frame(canvas)
        
        self.programs_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.programs_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.programs_frame.columnconfigure(0, weight=1)
    
    def setup_transfers_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de transferências"""
        # ...existing code... (implementação similar)
        pass
    
    def setup_network_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de rede"""
        container = ttk.Frame(parent, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid com topologia e estatísticas
        main_grid = ttk.Frame(container)
        main_grid.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Card topologia da rede
        topology_card = ttk.Frame(main_grid, relief='solid', borderwidth=1, padding="15")
        topology_card.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(topology_card, text="Topologia da Rede", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 15))
        
        # Figura matplotlib para visualização da rede
        self.network_figure = Figure(figsize=(6, 6), facecolor='white')
        self.network_canvas = FigureCanvasTkAgg(self.network_figure, topology_card)
        self.network_canvas.get_tk_widget().grid(row=1, column=0)
        
        # Card estatísticas
        stats_card = ttk.Frame(main_grid, relief='solid', borderwidth=1, padding="15")
        stats_card.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        ttk.Label(stats_card, text="Estatísticas da Rede", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 15))
        
        # Grid de estatísticas
        stats_grid = ttk.Frame(stats_card)
        stats_grid.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        network_stats = [
            ("Programas", lambda: len(self.programs)),
            ("Transferências", lambda: len(self.transfers)),
            ("Conexões", lambda: sum(len(p.connections) for p in self.programs)),
            ("Consenso", lambda: f"{int(self.metrics.consensus_level)}%")
        ]
        
        self.network_stats_widgets = {}
        
        for i, (name, value_func) in enumerate(network_stats):
            row = i // 2
            col = i % 2
            
            stat_frame = ttk.Frame(stats_grid, padding="10")
            stat_frame.grid(row=row, column=col, sticky=(tk.W, tk.E), padx=5, pady=5)
            
            value_label = tk.Label(stat_frame, text="0", font=("Arial", 16, "bold"), 
                                  fg="#3b82f6", bg="white")
            value_label.grid(row=0, column=0)
            
            name_label = tk.Label(stat_frame, text=name, font=("Arial", 9), 
                                 fg="#6b7280", bg="white")
            name_label.grid(row=1, column=0)
            
            self.network_stats_widgets[name] = {
                'value_label': value_label,
                'value_func': value_func
            }
        
        # Configurar grid
        for i in range(2):
            stats_grid.columnconfigure(i, weight=1)
        
        main_grid.columnconfigure(0, weight=1)
        main_grid.columnconfigure(1, weight=1)
        
        container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_controls_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de controles"""
        container = ttk.Frame(parent, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Card controles do sistema
        controls_card = ttk.Frame(container, relief='solid', borderwidth=1, padding="15")
        controls_card.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(controls_card, text="Controles do Sistema", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Grid de operações
        operations_frame = ttk.Frame(controls_card)
        operations_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 20))
        
        ttk.Label(operations_frame, text="Operações da Rede", 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, pady=(0, 10))
        
        # Botões de operações
        force_sync_btn = tk.Button(operations_frame, text="🔄 Forçar Sincronização",
                                  font=("Arial", 10), padx=15, pady=8,
                                  command=self.force_sync)
        force_sync_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=3)
        
        reset_network_btn = tk.Button(operations_frame, text="🌐 Resetar Rede",
                                     font=("Arial", 10), padx=15, pady=8,
                                     command=self.reset_network)
        reset_network_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=3)
        
        emergency_btn = tk.Button(operations_frame, text="🛡️ Modo Emergência",
                                 font=("Arial", 10), padx=15, pady=8,
                                 bg="#ef4444", fg="white")
        emergency_btn.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=3)
        
        # Grid de configurações
        config_frame = ttk.Frame(controls_card)
        config_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(config_frame, text="Configurações", 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Checkboxes de configuração
        configs = [
            ("Compartilhamento Ativo", self.share_var, self.toggle_sharing),
            ("Sincronização Automática", self.sync_var, self.toggle_auto_sync),
            ("Validação de Conhecimento", tk.BooleanVar(value=True), None),
            ("Backup Redundante", tk.BooleanVar(value=True), None)
        ]
        
        for i, (text, var, command) in enumerate(configs):
            check = tk.Checkbutton(config_frame, text=text, variable=var, command=command)
            check.grid(row=i+1, column=0, sticky=tk.W, pady=2)
        
        controls_card.columnconfigure(0, weight=1)
        controls_card.columnconfigure(1, weight=1)
        
        # Status indicators
        self.setup_status_indicators(container)
        
        container.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_status_indicators(self, parent: ttk.Frame) -> None:
        """Configurar indicadores de status"""
        status_card = ttk.Frame(parent, relief='solid', borderwidth=1, padding="15")
        status_card.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(status_card, text="Status do Sistema", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 15))
        
        # Indicadores de status
        statuses = [
            ("Rede Online", True),
            ("Sharing Ativo", lambda: self.share_enabled),
            ("Sync em Progresso", lambda: any(p.status == 'syncing' for p in self.programs)),
            ("Todos Programas OK", True)
        ]
        
        self.status_indicators = {}
        
        for i, (name, status_func) in enumerate(statuses):
            indicator_frame = ttk.Frame(status_card)
            indicator_frame.grid(row=1, column=i, padx=10)
            
            # Círculo de status
            status_circle = tk.Canvas(indicator_frame, width=12, height=12, 
                                    bg='white', highlightthickness=0)
            status_circle.grid(row=0, column=0, padx=(0, 5))
            
            # Label
            status_label = tk.Label(indicator_frame, text=name, font=("Arial", 9),
                                   bg='white')
            status_label.grid(row=0, column=1)
            
            self.status_indicators[name] = {
                'circle': status_circle,
                'status_func': status_func
            }
        
        status_card.columnconfigure(0, weight=1)
        status_card.columnconfigure(1, weight=1)
        status_card.columnconfigure(2, weight=1)
        status_card.columnconfigure(3, weight=1)
    
    # Funções de controle
    def toggle_sharing(self) -> None:
        """Alternar compartilhamento"""
        self.share_enabled = self.share_var.get()
    
    def toggle_auto_sync(self) -> None:
        """Alternar auto-sync"""
        self.auto_sync = self.sync_var.get()
    
    def force_sync(self) -> None:
        """Forçar sincronização (equivalente a forceSync)"""
        for program in self.programs:
            program.status = 'syncing'
            program.last_update = datetime.now()
    
    def reset_network(self) -> None:
        """Resetar rede (equivalente a resetNetwork)"""
        self.transfers = self.create_initial_transfers()
        self.metrics = self.create_metrics()
    
    # Funções de atualização da interface
    def update_network_visualization(self) -> None:
        """Atualizar visualização da rede"""
        if not self.network_figure:
            return
        
        self.network_figure.clear()
        ax = self.network_figure.add_subplot(111)
        
        # Desenhar rede circular
        center_x, center_y = 0, 0
        radius = 1
        
        # Centro da rede
        ax.scatter(center_x, center_y, s=800, c='#3b82f6', marker='o', alpha=0.8)
        ax.text(center_x, center_y, '🌐', ha='center', va='center', fontsize=16)
        
        # Programas ao redor
        for i, program in enumerate(self.programs[:6]):
            angle = (i * 60) * (math.pi / 180)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            color = self.get_program_type_color(program.type)
            ax.scatter(x, y, s=400, c=color, alpha=0.8)
            
            # Linha de conexão
            ax.plot([center_x, x], [center_y, y], 'k-', alpha=0.3, linewidth=1)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Rede Neural Distribuída - {len(self.programs)} Nós Ativos', 
                    fontsize=12, color='#374151')
        
        self.network_figure.tight_layout()
    
    def update_all_displays(self) -> None:
        """Atualizar todos os displays"""
        # Atualizar métricas principais
        for name, widget_info in self.metric_widgets.items():
            try:
                value = widget_info['value_func']()
                widget_info['value_label'].config(text=str(value))
            except:
                pass
        
        # Atualizar eficiência da rede
        for name, widget_info in self.efficiency_widgets.items():
            try:
                value = widget_info['value_func']()
                widget_info['value_label'].config(text=f"{int(value)}%")
                widget_info['progress_bar']['value'] = value
            except:
                pass
        
        # Atualizar estatísticas da rede
        for name, widget_info in self.network_stats_widgets.items():
            try:
                value = widget_info['value_func']()
                widget_info['value_label'].config(text=str(value))
            except:
                pass
        
        # Atualizar indicadores de status
        for name, widget_info in self.status_indicators.items():
            try:
                status_func = widget_info['status_func']
                if callable(status_func):
                    is_active = status_func()
                else:
                    is_active = status_func
                
                color = '#10b981' if is_active else '#ef4444'
                widget_info['circle'].delete("all")
                widget_info['circle'].create_oval(2, 2, 10, 10, fill=color, outline=color)
            except:
                pass
        
        # Atualizar visualização da rede
        self.update_network_visualization()
        
        # Atualizar transferências recentes
        self.update_transfers_display()
        
        # Atualizar programas
        self.update_programs_display()
    
    def update_transfers_display(self) -> None:
        """Atualizar display de transferências recentes"""
        if not hasattr(self, 'transfers_frame'):
            return
        
        # Limpar transferências existentes
        for widget in self.transfers_frame.winfo_children():
            widget.destroy()
        
        # Mostrar até 6 transferências mais recentes
        recent_transfers = sorted(self.transfers, key=lambda t: t.timestamp, reverse=True)[:6]
        
        for i, transfer in enumerate(recent_transfers):
            transfer_frame = ttk.Frame(self.transfers_frame, padding="8")
            transfer_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
            
            # Badge do tipo
            type_color = self.get_program_type_color(transfer.type)
            type_badge = tk.Label(transfer_frame, text=transfer.type.upper(),
                                 bg=type_color, fg="white",
                                 font=("Arial", 8, "bold"), padx=4, pady=1)
            type_badge.grid(row=0, column=0, padx=(0, 8))
            
            # Informações da transferência
            info_frame = ttk.Frame(transfer_frame)
            info_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
            
            from_prog = next((p for p in self.programs if p.id == transfer.from_program), None)
            to_prog = next((p for p in self.programs if p.id == transfer.to_program), None)
            
            if from_prog and to_prog:
                transfer_text = f"{from_prog.name} → {to_prog.name}"
            else:
                transfer_text = f"{transfer.from_program} → {transfer.to_program}"
            
            ttk.Label(info_frame, text=transfer_text, 
                     font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W)
            ttk.Label(info_frame, text=transfer.timestamp.strftime('%H:%M:%S'), 
                     font=("Arial", 8), foreground='#6b7280').grid(row=1, column=0, sticky=tk.W)
            
            # Status e confiança
            status_frame = ttk.Frame(transfer_frame)
            status_frame.grid(row=0, column=2, sticky=tk.E)
            
            status_icon = "✅" if transfer.status == 'completed' else "🔄"
            ttk.Label(status_frame, text=status_icon, font=("Arial", 10)).grid(row=0, column=0)
            ttk.Label(status_frame, text=f"{int(transfer.confidence)}%", 
                     font=("Arial", 8)).grid(row=0, column=1, padx=(3, 0))
            
            info_frame.columnconfigure(0, weight=1)
            transfer_frame.columnconfigure(1, weight=1)
            self.transfers_frame.columnconfigure(0, weight=1)
    
    def update_programs_display(self) -> None:
        """Atualizar display de programas"""
        if not hasattr(self, 'programs_frame'):
            return
        
        # Limpar programas existentes
        for widget in self.programs_frame.winfo_children():
            widget.destroy()
        
        # Criar cards para cada programa
        for i, program in enumerate(self.programs):
            program_card = ttk.Frame(self.programs_frame, relief='solid', borderwidth=1, padding="15")
            program_card.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=8)
            
            # Header do programa
            header_frame = ttk.Frame(program_card)
            header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            # Lado esquerdo: indicador, nome e badges
            left_frame = ttk.Frame(header_frame)
            left_frame.grid(row=0, column=0, sticky=tk.W)
            
            # Indicador de tipo
            type_indicator = tk.Canvas(left_frame, width=12, height=12, 
                                     bg='white', highlightthickness=0)
            type_indicator.grid(row=0, column=0, padx=(0, 10))
            type_color = self.get_program_type_color(program.type)
            type_indicator.create_oval(2, 2, 10, 10, fill=type_color, outline=type_color)
            
            # Info do programa
            info_frame = ttk.Frame(left_frame)
            info_frame.grid(row=0, column=1)
            
            ttk.Label(info_frame, text=program.name, 
                     font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W)
            
            badges_frame = ttk.Frame(info_frame)
            badges_frame.grid(row=1, column=0, sticky=tk.W, pady=(3, 0))
            
            # Badge de status
            status_color = self.get_status_color(program.status)
            status_badge = tk.Label(badges_frame, text=program.status.upper(),
                                   bg=status_color, fg="white",
                                   font=("Arial", 8, "bold"), padx=4, pady=1)
            status_badge.grid(row=0, column=0, padx=(0, 5))
            
            # Badge de tipo
            type_badge = tk.Label(badges_frame, text=program.type,
                                 bg="white", fg="#6b7280",
                                 font=("Arial", 8), relief='solid', borderwidth=1, padx=4, pady=1)
            type_badge.grid(row=0, column=1)
            
            # Lado direito: score e tempo
            right_frame = ttk.Frame(header_frame)
            right_frame.grid(row=0, column=1, sticky=tk.E)
            
            ttk.Label(right_frame, text=f"Score: {program.contribution_score:.1f}", 
                     font=("Arial", 9), foreground='#6b7280').grid(row=0, column=0)
            ttk.Label(right_frame, text=program.last_update.strftime('%H:%M:%S'), 
                     font=("Arial", 8), foreground='#6b7280').grid(row=1, column=0)
            
            header_frame.columnconfigure(0, weight=1)
            
            # Grid de métricas
            metrics_grid = ttk.Frame(program_card)
            metrics_grid.grid(row=1, column=0, sticky=(tk.W, tk.E))
            
            # Métricas do programa
            program_metrics = [
                ("Conhecimento", program.knowledge),
                ("Precisão", program.accuracy),
                ("Compartilhado", program.shared_knowledge),
                ("Recebido", program.received_knowledge)
            ]
            
            for j, (name, value) in enumerate(program_metrics):
                metric_frame = ttk.Frame(metrics_grid)
                metric_frame.grid(row=0, column=j, sticky=(tk.W, tk.E), padx=5)
                
                ttk.Label(metric_frame, text=name, font=("Arial", 9), 
                         foreground='#6b7280').grid(row=0, column=0)
                
                if name in ["Conhecimento", "Precisão"]:
                    # Progress bar para percentuais
                    progress_frame = ttk.Frame(metric_frame)
                    progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(2, 0))
                    
                    progress_bar = ttk.Progressbar(progress_frame, length=100, mode='determinate')
                    progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
                    progress_bar['value'] = value
                    
                    value_label = tk.Label(progress_frame, text=f"{int(value)}%",
                                          font=("Arial", 9, "bold"), bg="white")
                    value_label.grid(row=0, column=1, padx=(5, 0))
                    
                    progress_frame.columnconfigure(0, weight=1)
                else:
                    # Valor numérico simples
                    value_label = tk.Label(metric_frame, text=f"{int(value)}",
                                          font=("Arial", 11, "bold"), fg="#3b82f6", bg="white")
                    value_label.grid(row=1, column=0)
            
            # Configurar grid
            for j in range(4):
                metrics_grid.columnconfigure(j, weight=1)
            
            # Conexões
            if program.connections:
                connections_frame = ttk.Frame(program_card)
                connections_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
                
                ttk.Label(connections_frame, text="Conexões:", 
                         font=("Arial", 9), foreground='#6b7280').grid(row=0, column=0, sticky=tk.W)
                
                conn_badges_frame = ttk.Frame(connections_frame)
                conn_badges_frame.grid(row=1, column=0, sticky=tk.W, pady=(3, 0))
                
                for k, conn_id in enumerate(program.connections):
                    conn_program = next((p for p in self.programs if p.id == conn_id), None)
                    if conn_program:
                        conn_badge = tk.Label(conn_badges_frame, text=conn_program.name,
                                             bg="#f1f5f9", fg="#6b7280",
                                             font=("Arial", 8), padx=3, pady=1)
                        conn_badge.grid(row=0, column=k, padx=(0, 3))
            
            program_card.columnconfigure(0, weight=1)
            self.programs_frame.columnconfigure(0, weight=1)
    
    # Funções de atualização de dados
    def update_data(self) -> None:
        """Atualizar dados (equivalente ao useEffect)"""
        if not self.share_enabled:
            return
        
        # Atualizar programas
        self.update_programs()
        
        # Criar nova transferência ocasionalmente
        if random.random() > 0.7:
            new_transfer = self.create_new_transfer()
            if new_transfer:
                self.transfers = [new_transfer] + self.transfers[:19]
        
        # Atualizar métricas
        self.metrics = self.create_metrics()
        
        # Atualizar interface
        self.root.after(0, self.update_all_displays)
    
    def start_updates(self) -> None:
        """Iniciar atualizações (equivalente ao useEffect)"""
        def update_worker():
            while not self.stop_updates:
                time.sleep(2)  # Atualizar a cada 2 segundos
                if not self.stop_updates:
                    self.update_data()
        
        # Primeira atualização
        self.update_all_displays()
        
        # Iniciar thread de atualização
        self.update_thread = threading.Thread(target=update_worker, daemon=True)
        self.update_thread.start()
    
    def __del__(self):
        """Destrutor para parar thread de atualização"""
        self.stop_updates = True

def main() -> None:
    """Função principal para executar a aplicação"""
    root = tk.Tk()
    app = NeuralLearningShareApp(root)
    
    # Tornar a janela responsiva
    root.minsize(1400, 900)
    
    # Centralizar janela
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()