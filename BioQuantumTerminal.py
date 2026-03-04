import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple, Callable
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
import json

# Enums and Types
class TrainingPhase(Enum):
    IDLE = "AGUARDANDO"
    TRAINING = "TREINANDO"
    INFERENCE = "GERANDO SINAIS"
    COMPLETE = "COMPLETO"

@dataclass
class TrainingLog:
    epoch: int
    loss: float
    mae: float
    timestamp: str

@dataclass
class BioSignal:
    date: str
    price: float
    predicted_price: float
    signal_type: str  # BUY, SELL, HOLD

@dataclass
class BioSystemConfig:
    symbol: str
    interval: str
    lookback: int
    epochs: int
    trading_threshold: float
    batch_size: int

@dataclass
class LearningStatus:
    phase: str
    knowledge_size: int
    total_experiences: int
    quantum_advantage: float
    success_rate: float

# Available assets
AVAILABLE_ASSETS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT',
    'EURUSD', 'GBPUSD', 'USDJPY', 'EURJPY',
    'XAUUSD'
]

# Mock Bio-Quantum System (Replace with actual implementation)
class AdvancedBioQuantumSystem:
    def __init__(self, config: BioSystemConfig):
        self.config = config
        self.is_training = False
        self.current_epoch = 0
        self.training_logs: List[TrainingLog] = []
        self.signals: List[BioSignal] = []
        
    def initialize(self) -> None:
        """Initialize the bio-quantum system"""
        print(f"Bio-Quantum Kernel v5.0 initialized for {self.config.symbol}")
        
    def load_simulated_data(self, symbol: str) -> None:
        """Load simulated data for the given symbol"""
        print(f"Loading simulated data for {symbol}")
        
    def load_data(self, market_data: List[Any]) -> None:
        """Load actual market data"""
        print(f"Loaded {len(market_data)} market data points")
        
    def train_model(self, progress_callback: Optional[Callable] = None) -> None:
        """Train the bio-quantum model"""
        self.is_training = True
        self.training_logs.clear()
        
        for epoch in range(1, self.config.epochs + 1):
            if not self.is_training:
                break
                
            self.current_epoch = epoch
            
            # Simulate training metrics
            loss = 0.1 * (1 - (epoch / self.config.epochs) ** 0.5) + random.uniform(0, 0.01)
            mae = loss * 0.8 + random.uniform(0, 0.005)
            
            log = TrainingLog(
                epoch=epoch,
                loss=loss,
                mae=mae,
                timestamp=datetime.now().strftime("%H:%M:%S")
            )
            
            self.training_logs.append(log)
            
            # Call progress callback
            if progress_callback:
                progress_callback(log)
            
            # Simulate training time
            time.sleep(0.05)
            
        self.is_training = False
        
    def generate_signals(self) -> List[BioSignal]:
        """Generate trading signals based on trained model"""
        signals = []
        base_price = 100.0  # Starting price
        
        for i in range(100):  # Generate 100 signals
            date = (datetime.now() - timedelta(minutes=100-i)).strftime("%H:%M")
            price_change = random.uniform(-0.02, 0.02)
            price = base_price * (1 + price_change)
            base_price = price
            
            # Add some prediction noise
            predicted_price = price * (1 + random.uniform(-0.01, 0.01))
            
            # Determine signal type
            if abs(predicted_price - price) / price > self.config.trading_threshold:
                signal_type = "BUY" if predicted_price > price else "SELL"
            else:
                signal_type = "HOLD"
            
            signals.append(BioSignal(
                date=date,
                price=price,
                predicted_price=predicted_price,
                signal_type=signal_type
            ))
        
        return signals
    
    def stop_training(self) -> None:
        """Stop the training process"""
        self.is_training = False

# Mock Continuous Learning Service
class ContinuousLearningService:
    def __init__(self):
        self.phase = "OTIMIZAÇÃO"
        self.knowledge_size = random.randint(500, 2000)
        self.total_experiences = random.randint(1000, 5000)
        self.quantum_advantage = random.uniform(1.2, 3.5)
        self.success_rate = random.uniform(0.65, 0.95)
        
    def get_status(self) -> LearningStatus:
        """Get current learning status with slight variations"""
        # Simulate gradual improvements
        self.knowledge_size += random.randint(0, 5)
        self.total_experiences += random.randint(1, 10)
        self.quantum_advantage += random.uniform(-0.05, 0.05)
        self.quantum_advantage = max(1.0, min(5.0, self.quantum_advantage))
        self.success_rate += random.uniform(-0.01, 0.01)
        self.success_rate = max(0.5, min(0.99, self.success_rate))
        
        return LearningStatus(
            phase=self.phase,
            knowledge_size=self.knowledge_size,
            total_experiences=self.total_experiences,
            quantum_advantage=self.quantum_advantage,
            success_rate=self.success_rate
        )

# Main Bio-Quantum Terminal Application
class BioQuantumTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA BIO-QUANTUM v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a0a")
        
        # Default configuration
        self.default_config = BioSystemConfig(
            symbol='BTC/USDT',
            interval='1m',
            lookback=60,
            epochs=50,
            trading_threshold=0.002,
            batch_size=32
        )
        
        # State
        self.config = self.default_config
        self.logs: List[TrainingLog] = []
        self.signals: List[BioSignal] = []
        self.is_training = False
        self.progress = 0
        self.learning_status: Optional[LearningStatus] = None
        
        # Initialize services
        self.system = None
        self.continuous_learner = ContinuousLearningService()
        
        # Initialize system
        self.initialize_system()
        
        # Setup UI
        self.setup_ui()
        
        # Start status updates
        self.start_status_updates()
        
    def initialize_system(self):
        """Initialize the bio-quantum system"""
        self.system = AdvancedBioQuantumSystem(self.config)
        self.system.initialize()
        
        # Load simulated data
        if self.config.symbol:
            if 'USDT' in self.config.symbol:
                # For crypto, load empty market data
                self.system.load_data([])
            else:
                # For Forex/Metals, load simulated data
                self.system.load_simulated_data(self.config.symbol)
        
        # Initial logs
        self.add_log("Bio-Quantum Kernel v5.0 initialized", is_system=True)
        self.add_log(f"Asset loaded: {self.config.symbol}", is_system=True)
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header()
        
        # Content area
        self.setup_content()
    
    def setup_header(self):
        """Setup the application header"""
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Left side: Logo and title
        left_frame = tk.Frame(header_frame, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # Icon
        icon_frame = tk.Frame(left_frame, bg="#064e3b", relief=tk.RAISED, 
                             borderwidth=1, padx=10, pady=10)
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        tk.Label(icon_frame, text="🧠", font=("Arial", 16), 
                bg="#064e3b", fg="#10b981").pack()
        
        # Text
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(text_frame, text="SISTEMA BIO-QUANTUM v2.0", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#1a1a2e").pack(anchor=tk.W)
        
        tk.Label(text_frame, text="MULTI-ASSET NEURAL KERNEL", 
                font=("Courier", 10), fg="#10b981", bg="#1a1a2e").pack(anchor=tk.W)
        
        # Right side: Controls
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        # Asset selector
        asset_frame = tk.Frame(right_frame, bg="black", relief=tk.RAISED, 
                              borderwidth=1, padx=8, pady=4)
        asset_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(asset_frame, text="🌐", font=("Arial", 12), 
                bg="black", fg="#3b82f6").pack(side=tk.LEFT, padx=(0, 5))
        
        self.asset_var = tk.StringVar(value=self.config.symbol)
        self.asset_combo = ttk.Combobox(
            asset_frame,
            textvariable=self.asset_var,
            values=AVAILABLE_ASSETS,
            state="readonly",
            width=12,
            font=("Courier", 10, "bold"),
            style="Dark.TCombobox"
        )
        self.asset_combo.pack(side=tk.LEFT)
        self.asset_combo.bind("<<ComboboxSelected>>", self.on_asset_changed)
        
        # Status display
        status_frame = tk.Frame(right_frame, bg="#1a1a2e")
        status_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(status_frame, text="Status do Núcleo", 
                font=("Arial", 8), fg="#666666", bg="#1a1a2e").pack(anchor=tk.E)
        
        self.status_label = tk.Label(
            status_frame,
            text="AGUARDANDO COMANDO",
            font=("Courier", 10, "bold"),
            fg="#10b981",
            bg="#1a1a2e"
        )
        self.status_label.pack()
        
        # Training button
        self.train_button = tk.Button(
            right_frame,
            text="INICIAR TREINAMENTO",
            command=self.toggle_training,
            font=("Arial", 10, "bold"),
            bg="#166534",
            fg="#ffffff",
            activebackground="#15803d",
            activeforeground="#ffffff",
            padx=20,
            pady=8,
            borderwidth=1,
            relief=tk.RAISED
        )
        self.train_button.pack()
        
        # Configure combobox style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Dark.TCombobox",
                       fieldbackground="black",
                       background="black",
                       foreground="white",
                       arrowcolor="white",
                       borderwidth=1)
    
    def setup_content(self):
        """Setup the main content area"""
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel
        left_panel = tk.Frame(content_frame, bg="#0a0a0a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Continuous learning panel
        self.setup_learning_panel(left_panel)
        
        # Configuration panel
        self.setup_config_panel(left_panel)
        
        # Terminal logs
        self.setup_terminal_logs(left_panel)
        
        # Right panel (visualizations)
        right_panel = tk.Frame(content_frame, bg="#0a0a0a")
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Training metrics chart
        self.setup_training_chart(right_panel)
        
        # Signals chart
        self.setup_signals_chart(right_panel)
    
    def setup_learning_panel(self, parent):
        """Setup the continuous learning panel"""
        learning_frame = tk.Frame(
            parent,
            bg="#1e3a8a",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        learning_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_frame = tk.Frame(learning_frame, bg="#1e3a8a")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(title_frame, text="⚡", font=("Arial", 14), 
                bg="#1e3a8a", fg="#3b82f6").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(title_frame, text="APRENDIZADO CONTÍNUO", 
                font=("Arial", 10, "bold"), fg="#3b82f6", bg="#1e3a8a").pack(side=tk.LEFT)
        
        # Status labels
        self.phase_label = tk.Label(
            learning_frame,
            text="Fase: OTIMIZAÇÃO",
            font=("Courier", 9, "bold"),
            fg="#ffffff",
            bg="#1e3a8a"
        )
        self.phase_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.knowledge_label = tk.Label(
            learning_frame,
            text="Base de Conhecimento: 1500 Padrões",
            font=("Courier", 9),
            fg="#cccccc",
            bg="#1e3a8a"
        )
        self.knowledge_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.experiences_label = tk.Label(
            learning_frame,
            text="Experiências: 3000",
            font=("Courier", 9),
            fg="#cccccc",
            bg="#1e3a8a"
        )
        self.experiences_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.advantage_label = tk.Label(
            learning_frame,
            text="Vantagem Quântica: 2.15x",
            font=("Courier", 9, "bold"),
            fg="#3b82f6",
            bg="#1e3a8a"
        )
        self.advantage_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            learning_frame,
            length=200,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(learning_frame, text="Taxa de Sucesso Global", 
                font=("Arial", 7), fg="#666666", bg="#1e3a8a").pack(anchor=tk.E)
    
    def setup_config_panel(self, parent):
        """Setup the configuration panel"""
        config_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        tk.Label(config_frame, text="⚙️ CONFIGURAÇÃO DO MODELO", 
                font=("Arial", 10, "bold"), fg="#666666", bg="#1a1a2e").pack(anchor=tk.W, pady=(0, 10))
        
        # Configuration grid
        grid_frame = tk.Frame(config_frame, bg="#1a1a2e")
        grid_frame.pack()
        
        # Symbol (readonly)
        tk.Label(grid_frame, text="Símbolo", font=("Arial", 8), 
                fg="#666666", bg="#1a1a2e", width=15).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.symbol_entry = tk.Entry(
            grid_frame,
            font=("Courier", 9),
            bg="black",
            fg="#cccccc",
            borderwidth=1,
            relief=tk.SUNKEN,
            state='readonly',
            width=15
        )
        self.symbol_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.symbol_entry.insert(0, self.config.symbol)
        
        # Lookback
        tk.Label(grid_frame, text="Lookback (Seq)", font=("Arial", 8), 
                fg="#666666", bg="#1a1a2e", width=15).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.lookback_var = tk.IntVar(value=self.config.lookback)
        self.lookback_spin = tk.Spinbox(
            grid_frame,
            from_=10,
            to=200,
            increment=10,
            textvariable=self.lookback_var,
            font=("Courier", 9),
            bg="black",
            fg="white",
            borderwidth=1,
            relief=tk.SUNKEN,
            width=15
        )
        self.lookback_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Epochs
        tk.Label(grid_frame, text="Épocas", font=("Arial", 8), 
                fg="#666666", bg="#1a1a2e", width=15).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.epochs_var = tk.IntVar(value=self.config.epochs)
        self.epochs_spin = tk.Spinbox(
            grid_frame,
            from_=10,
            to=200,
            increment=10,
            textvariable=self.epochs_var,
            font=("Courier", 9),
            bg="black",
            fg="white",
            borderwidth=1,
            relief=tk.SUNKEN,
            width=15
        )
        self.epochs_spin.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Threshold
        tk.Label(grid_frame, text="Threshold", font=("Arial", 8), 
                fg="#666666", bg="#1a1a2e", width=15).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.threshold_var = tk.DoubleVar(value=self.config.trading_threshold)
        self.threshold_spin = tk.Spinbox(
            grid_frame,
            from_=0.0001,
            to=0.01,
            increment=0.0001,
            format="%.4f",
            textvariable=self.threshold_var,
            font=("Courier", 9),
            bg="black",
            fg="white",
            borderwidth=1,
            relief=tk.SUNKEN,
            width=15
        )
        self.threshold_spin.grid(row=3, column=1, sticky=tk.W, pady=5)
    
    def setup_terminal_logs(self, parent):
        """Setup the terminal logs display"""
        terminal_frame = tk.Frame(
            parent,
            bg="black",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        terminal_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and progress
        title_frame = tk.Frame(terminal_frame, bg="black")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(title_frame, text="💻 SYSTEM LOGS", font=("Courier", 10, "bold"), 
                fg="#10b981", bg="black").pack(side=tk.LEFT)
        
        self.progress_label = tk.Label(
            title_frame,
            text="0%",
            font=("Courier", 10),
            fg="#fbbf24",
            bg="black"
        )
        self.progress_label.pack(side=tk.RIGHT)
        
        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            terminal_frame,
            bg="black",
            fg="#cccccc",
            font=("Courier", 9),
            insertbackground="#ffffff",
            wrap=tk.WORD,
            height=15,
            borderwidth=0,
            highlightthickness=0
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial logs
        self.logs_text.insert(tk.END, "// Bio-Quantum Kernel v5.0 initialized\n", "system")
        self.logs_text.insert(tk.END, f"// Asset loaded: {self.config.symbol}\n", "system")
        
        # Configure tags for different log types
        self.logs_text.tag_config("system", foreground="#666666")
        self.logs_text.tag_config("training", foreground="#fbbf24")
        self.logs_text.tag_config("complete", foreground="#10b981")
        
        # Scroll to bottom
        self.logs_text.see(tk.END)
    
    def setup_training_chart(self, parent):
        """Setup the training metrics chart"""
        chart_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Title
        tk.Label(chart_frame, text="📈 MÉTRICAS DE TREINAMENTO (PERDA/LOSS)", 
                font=("Arial", 10, "bold"), fg="#666666", bg="#1a1a2e").pack(anchor=tk.W, pady=(0, 10))
        
        # Create matplotlib figure
        self.training_fig = Figure(figsize=(10, 3), dpi=80, facecolor='#1a1a2e')
        self.training_ax = self.training_fig.add_subplot(111)
        self.training_ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.training_ax.set_xlabel('Época', color='#666666', fontsize=8)
        self.training_ax.set_ylabel('Loss', color='#666666', fontsize=8)
        self.training_ax.tick_params(colors='#666666', labelsize=7)
        self.training_ax.grid(True, color='#222222', linestyle='--', alpha=0.5)
        
        # Initial empty plots
        self.loss_line, = self.training_ax.plot([], [], color='#ef4444', linewidth=2, label='Loss')
        self.mae_line, = self.training_ax.plot([], [], color='#3b82f6', linewidth=1, label='MAE')
        self.training_ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
        
        # Add to Tkinter
        self.training_canvas = FigureCanvasTkAgg(self.training_fig, chart_frame)
        self.training_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_signals_chart(self, parent):
        """Setup the trading signals chart"""
        chart_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.signals_title = tk.Label(
            chart_frame,
            text=f"📊 SINAIS DE TRADING & PREDIÇÃO: {self.config.symbol}",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a2e"
        )
        self.signals_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Create matplotlib figure
        self.signals_fig = Figure(figsize=(10, 4), dpi=80, facecolor='#1a1a2e')
        self.signals_ax = self.signals_fig.add_subplot(111)
        self.signals_ax.set_facecolor('#1a1a2e')
        
        # Configure axes
        self.signals_ax.set_xlabel('Tempo', color='#666666', fontsize=8)
        self.signals_ax.set_ylabel('Preço', color='#666666', fontsize=8)
        self.signals_ax.tick_params(colors='#666666', labelsize=7)
        self.signals_ax.grid(True, color='#222222', linestyle='--', alpha=0.5)
        
        # Initial empty plots
        self.price_line, = self.signals_ax.plot([], [], color='#4ade80', linewidth=1, label='Preço Real')
        self.predicted_line, = self.signals_ax.plot([], [], color='#facc15', linewidth=1, 
                                                   linestyle='--', label='Previsão')
        self.signals_ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=8)
        
        # Placeholder text
        self.placeholder_text = self.signals_ax.text(
            0.5, 0.5,
            f'Aguardando geração de sinais para {self.config.symbol}...',
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.signals_ax.transAxes,
            fontsize=12,
            color='#666666'
        )
        
        # Add to Tkinter
        self.signals_canvas = FigureCanvasTkAgg(self.signals_fig, chart_frame)
        self.signals_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def start_status_updates(self):
        """Start periodic status updates"""
        def update_status():
            while True:
                # Update learning status
                status = self.continuous_learner.get_status()
                self.learning_status = status
                
                # Update UI in main thread
                self.root.after(0, self.update_learning_panel, status)
                
                time.sleep(2)  # Update every 2 seconds
        
        # Start update thread
        update_thread = threading.Thread(target=update_status, daemon=True)
        update_thread.start()
    
    def update_learning_panel(self, status: LearningStatus):
        """Update the continuous learning panel with new status"""
        self.phase_label.config(text=f"Fase: {status.phase}")
        self.knowledge_label.config(text=f"Base de Conhecimento: {status.knowledge_size} Padrões")
        self.experiences_label.config(text=f"Experiências: {status.total_experiences}")
        self.advantage_label.config(text=f"Vantagem Quântica: {status.quantum_advantage:.2f}x")
        
        # Update progress bar
        self.progress_bar['value'] = status.success_rate * 100
    
    def on_asset_changed(self, event):
        """Handle asset selection change"""
        new_symbol = self.asset_var.get()
        self.config = BioSystemConfig(
            symbol=new_symbol,
            interval=self.config.interval,
            lookback=self.config.lookback,
            epochs=self.config.epochs,
            trading_threshold=self.config.trading_threshold,
            batch_size=self.config.batch_size
        )
        
        # Update UI
        self.symbol_entry.config(state='normal')
        self.symbol_entry.delete(0, tk.END)
        self.symbol_entry.insert(0, new_symbol)
        self.symbol_entry.config(state='readonly')
        
        self.signals_title.config(text=f"📊 SINAIS DE TRADING & PREDIÇÃO: {new_symbol}")
        self.placeholder_text.set_text(f'Aguardando geração de sinais para {new_symbol}...')
        
        # Reinitialize system
        self.initialize_system()
        
        # Clear charts
        self.clear_signals_chart()
    
    def toggle_training(self):
        """Start or stop the training process"""
        if self.is_training:
            self.stop_training()
        else:
            self.start_training()
    
    def start_training(self):
        """Start the training process"""
        if not self.system:
            return
        
        # Update state
        self.is_training = True
        self.status_label.config(
            text="PROCESSANDO ÉPOCAS...",
            fg="#fbbf24"
        )
        self.train_button.config(
            text="INTERROMPER",
            bg="#991b1b",
            activebackground="#dc2626"
        )
        
        # Clear previous data
        self.logs.clear()
        self.logs_text.delete(1.0, tk.END)
        self.add_log("Iniciando treinamento do modelo...", is_system=True)
        
        # Start training in separate thread
        def training_thread():
            self.system.train_model(self.on_training_progress)
            
            # Generate signals after training
            if not self.system.is_training:
                signals = self.system.generate_signals()
                self.signals = signals[-100:]  # Last 100 signals
                
                # Update UI in main thread
                self.root.after(0, self.on_training_complete)
        
        thread = threading.Thread(target=training_thread, daemon=True)
        thread.start()
    
    def stop_training(self):
        """Stop the training process"""
        if self.system:
            self.system.stop_training()
        
        self.is_training = False
        self.status_label.config(
            text="TREINAMENTO INTERROMPIDO",
            fg="#ef4444"
        )
        self.train_button.config(
            text="INICIAR TREINAMENTO",
            bg="#166534",
            activebackground="#15803d"
        )
        
        self.add_log("Treinamento interrompido pelo usuário.", is_system=True)
    
    def on_training_progress(self, log: TrainingLog):
        """Handle training progress updates"""
        self.logs.append(log)
        self.progress = (log.epoch / self.config.epochs) * 100
        
        # Update UI in main thread
        self.root.after(0, self.update_training_ui, log)
    
    def update_training_ui(self, log: TrainingLog):
        """Update training-related UI elements"""
        # Update progress label
        self.progress_label.config(text=f"{self.progress:.0f}%")
        
        # Add log to terminal
        log_entry = f"[{log.timestamp}] Epoch {log.epoch}/{self.config.epochs}: "
        log_entry += f"loss={log.loss:.5f} "
        log_entry += f"mae={log.mae:.5f}\n"
        
        self.logs_text.insert(tk.END, log_entry, "training")
        self.logs_text.see(tk.END)
        
        # Update training chart
        self.update_training_chart()
        
        # Show processing message
        if self.is_training:
            self.logs_text.insert(tk.END, "_ Processando tensores neurais...\n", "training")
            self.logs_text.see(tk.END)
    
    def on_training_complete(self):
        """Handle training completion"""
        self.is_training = False
        self.status_label.config(
            text="TREINAMENTO COMPLETO",
            fg="#10b981"
        )
        self.train_button.config(
            text="INICIAR TREINAMENTO",
            bg="#166534",
            activebackground="#15803d"
        )
        
        self.add_log(">> Treinamento Finalizado. Sinais Gerados.", is_complete=True)
        
        # Update signals chart
        self.update_signals_chart()
    
    def add_log(self, message: str, is_system: bool = False, is_complete: bool = False):
        """Add a log message to the terminal"""
        if is_system:
            tag = "system"
        elif is_complete:
            tag = "complete"
        else:
            tag = "training"
        
        self.logs_text.insert(tk.END, f"{message}\n", tag)
        self.logs_text.see(tk.END)
    
    def update_training_chart(self):
        """Update the training metrics chart"""
        if not self.logs:
            return
        
        epochs = [log.epoch for log in self.logs]
        losses = [log.loss for log in self.logs]
        maes = [log.mae for log in self.logs]
        
        # Update plot data
        self.loss_line.set_data(epochs, losses)
        self.mae_line.set_data(epochs, maes)
        
        # Adjust axes limits
        if epochs:
            self.training_ax.set_xlim(0, max(epochs) + 1)
        
        loss_min = min(losses) * 0.9 if losses else 0
        loss_max = max(losses) * 1.1 if losses else 1
        self.training_ax.set_ylim(loss_min, loss_max)
        
        # Redraw canvas
        self.training_canvas.draw()
    
    def update_signals_chart(self):
        """Update the trading signals chart"""
        if not self.signals:
            return
        
        # Remove placeholder
        self.placeholder_text.set_text('')
        
        dates = list(range(len(self.signals)))  # Use indices instead of dates for simplicity
        prices = [s.price for s in self.signals]
        predicted = [s.predicted_price for s in self.signals]
        
        # Update plot data
        self.price_line.set_data(dates, prices)
        self.predicted_line.set_data(dates, predicted)
        
        # Adjust axes limits
        if dates:
            self.signals_ax.set_xlim(0, max(dates) + 1)
        
        all_prices = prices + predicted
        price_min = min(all_prices) * 0.99 if all_prices else 0
        price_max = max(all_prices) * 1.01 if all_prices else 1
        self.signals_ax.set_ylim(price_min, price_max)
        
        # Redraw canvas
        self.signals_canvas.draw()
    
    def clear_signals_chart(self):
        """Clear the signals chart"""
        self.price_line.set_data([], [])
        self.predicted_line.set_data([], [])
        
        # Show placeholder
        self.placeholder_text.set_text(f'Aguardando geração de sinais para {self.config.symbol}...')
        
        # Redraw canvas
        self.signals_canvas.draw()

def main():
    """Main entry point"""
    root = tk.Tk()
    app = BioQuantumTerminal(root)
    root.mainloop()

if __name__ == "__main__":
    main()