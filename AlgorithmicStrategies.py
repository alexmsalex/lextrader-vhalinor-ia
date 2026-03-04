import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import datetime
import threading
import time
import random
from enum import Enum

# Enums para tipos de dados
class StrategyType(Enum):
    MOMENTUM = "MOMENTUM"
    MEAN_REVERSION = "MEAN_REVERSION"
    BREAKOUT = "BREAKOUT"
    GRID = "GRID"
    SCALPING = "SCALPING"

class StrategyStatus(Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"

class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class SignalAction(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

# Estruturas de dados equivalentes às interfaces TypeScript
@dataclass
class Strategy:
    name: str
    type: StrategyType
    status: StrategyStatus
    win_rate: float
    profit_factor: float
    sharpe_ratio: float
    max_drawdown: float
    total_trades: int
    avg_hold_time: str
    current_pnl: float
    risk_level: RiskLevel

@dataclass
class StrategySignal:
    strategy: str
    action: SignalAction
    strength: float
    price: float
    stop_loss: float
    take_profit: float
    timeframe: str
    confidence: float

class AlgorithmicStrategiesApp:
    """Aplicação principal que replica a funcionalidade do componente React AlgorithmicStrategies"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("💻 Estratégias Algorítmicas")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8fafc')
        
        # Estado da aplicação (equivalente aos useState hooks)
        self.strategies: List[Strategy] = []
        self.signals: List[StrategySignal] = []
        self.active_strategies = 0
        self.total_pnl = 0.0
        
        # Containers para widgets que precisam ser atualizados
        self.active_label = None
        self.pnl_label = None
        self.strategy_frames = []
        self.signal_frames = []
        
        # Configurar estilos
        self.setup_styles()
        
        # Inicializar dados
        self.initialize_data()
        
        # Configurar interface
        self.setup_ui()
        
        # Iniciar thread de atualização (equivalente ao useEffect)
        self.start_update_thread()
    
    def setup_styles(self) -> None:
        """Configurar estilos customizados para a aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores personalizadas
        style.configure('Primary.TButton', 
                       background='#3b82f6', 
                       foreground='white',
                       focuscolor='none')
        
        style.configure('Success.TLabel', foreground='#10b981')
        style.configure('Warning.TLabel', foreground='#f59e0b')
        style.configure('Error.TLabel', foreground='#ef4444')
        style.configure('Info.TLabel', foreground='#6366f1')
        style.configure('Momentum.TLabel', foreground='#3b82f6')
        style.configure('MeanReversion.TLabel', foreground='#8b5cf6')
        style.configure('Breakout.TLabel', foreground='#f59e0b')
        style.configure('Grid.TLabel', foreground='#10b981')
        style.configure('Scalping.TLabel', foreground='#ef4444')
        
        style.configure('Card.TFrame', 
                       background='white', 
                       relief='solid',
                       borderwidth=1)
    
    # Funções utilitárias (equivalentes às funções do React)
    def get_strategy_type_color(self, strategy_type: StrategyType) -> str:
        """Obter cor para tipo de estratégia (equivalente a getStrategyTypeColor)"""
        color_map = {
            StrategyType.MOMENTUM: "#3b82f6",
            StrategyType.MEAN_REVERSION: "#8b5cf6",
            StrategyType.BREAKOUT: "#f59e0b",
            StrategyType.GRID: "#10b981",
            StrategyType.SCALPING: "#ef4444"
        }
        return color_map.get(strategy_type, "#6366f1")
    
    def get_status_color(self, status: StrategyStatus) -> str:
        """Obter cor para status da estratégia (equivalente a getStatusColor)"""
        color_map = {
            StrategyStatus.ACTIVE: "#10b981",
            StrategyStatus.PAUSED: "#f59e0b",
            StrategyStatus.STOPPED: "#ef4444"
        }
        return color_map.get(status, "#6b7280")
    
    def get_risk_color(self, risk: RiskLevel) -> str:
        """Obter cor para nível de risco (equivalente a getRiskColor)"""
        color_map = {
            RiskLevel.LOW: "#10b981",
            RiskLevel.MEDIUM: "#f59e0b",
            RiskLevel.HIGH: "#ef4444"
        }
        return color_map.get(risk, "#6366f1")
    
    def get_action_icon(self, action: SignalAction) -> str:
        """Obter ícone para ação do sinal (equivalente a getActionIcon)"""
        icon_map = {
            SignalAction.BUY: "📈",
            SignalAction.SELL: "📉",
            SignalAction.HOLD: "📊"
        }
        return icon_map.get(action, "📊")
    
    def get_action_color(self, action: SignalAction) -> str:
        """Obter cor para ação do sinal"""
        color_map = {
            SignalAction.BUY: "#10b981",
            SignalAction.SELL: "#ef4444",
            SignalAction.HOLD: "#6b7280"
        }
        return color_map.get(action, "#6b7280")
    
    # Funções de inicialização de dados (equivalentes à inicialização do React)
    def init_strategies(self) -> List[Strategy]:
        """Inicializar estratégias (equivalente a initStrategies)"""
        return [
            Strategy(
                name='RSI Divergence Pro',
                type=StrategyType.MOMENTUM,
                status=StrategyStatus.ACTIVE,
                win_rate=73.2,
                profit_factor=2.41,
                sharpe_ratio=1.89,
                max_drawdown=-8.7,
                total_trades=347,
                avg_hold_time='4h 23m',
                current_pnl=12.4,
                risk_level=RiskLevel.MEDIUM
            ),
            Strategy(
                name='Bollinger Bands Squeeze',
                type=StrategyType.BREAKOUT,
                status=StrategyStatus.ACTIVE,
                win_rate=68.9,
                profit_factor=2.12,
                sharpe_ratio=1.67,
                max_drawdown=-12.1,
                total_trades=289,
                avg_hold_time='2h 45m',
                current_pnl=8.7,
                risk_level=RiskLevel.HIGH
            ),
            Strategy(
                name='EMA Crossover Neural',
                type=StrategyType.MOMENTUM,
                status=StrategyStatus.ACTIVE,
                win_rate=71.4,
                profit_factor=1.98,
                sharpe_ratio=1.45,
                max_drawdown=-9.8,
                total_trades=412,
                avg_hold_time='6h 12m',
                current_pnl=15.2,
                risk_level=RiskLevel.LOW
            ),
            Strategy(
                name='Support Resistance AI',
                type=StrategyType.MEAN_REVERSION,
                status=StrategyStatus.PAUSED,
                win_rate=69.7,
                profit_factor=2.33,
                sharpe_ratio=1.72,
                max_drawdown=-11.4,
                total_trades=256,
                avg_hold_time='3h 56m',
                current_pnl=-2.1,
                risk_level=RiskLevel.MEDIUM
            ),
            Strategy(
                name='Grid Trading Bot',
                type=StrategyType.GRID,
                status=StrategyStatus.ACTIVE,
                win_rate=82.1,
                profit_factor=1.34,
                sharpe_ratio=0.89,
                max_drawdown=-5.2,
                total_trades=1247,
                avg_hold_time='1h 18m',
                current_pnl=6.8,
                risk_level=RiskLevel.LOW
            ),
            Strategy(
                name='Scalping Master V3',
                type=StrategyType.SCALPING,
                status=StrategyStatus.ACTIVE,
                win_rate=76.8,
                profit_factor=1.67,
                sharpe_ratio=2.14,
                max_drawdown=-6.9,
                total_trades=2891,
                avg_hold_time='12m',
                current_pnl=21.3,
                risk_level=RiskLevel.HIGH
            )
        ]
    
    def init_signals(self) -> List[StrategySignal]:
        """Inicializar sinais (equivalente a initSignals)"""
        return [
            StrategySignal(
                strategy='RSI Divergence Pro',
                action=SignalAction.BUY,
                strength=87.3,
                price=42150,
                stop_loss=41200,
                take_profit=43800,
                timeframe='4H',
                confidence=91.2
            ),
            StrategySignal(
                strategy='Bollinger Bands Squeeze',
                action=SignalAction.SELL,
                strength=78.9,
                price=42080,
                stop_loss=42650,
                take_profit=41200,
                timeframe='1H',
                confidence=84.7
            ),
            StrategySignal(
                strategy='EMA Crossover Neural',
                action=SignalAction.HOLD,
                strength=45.2,
                price=42100,
                stop_loss=0,
                take_profit=0,
                timeframe='6H',
                confidence=62.1
            ),
            StrategySignal(
                strategy='Grid Trading Bot',
                action=SignalAction.BUY,
                strength=92.4,
                price=42090,
                stop_loss=41950,
                take_profit=42250,
                timeframe='15M',
                confidence=95.8
            )
        ]
    
    def initialize_data(self) -> None:
        """Inicializar todos os dados da aplicação"""
        self.strategies = self.init_strategies()
        self.signals = self.init_signals()
        self.active_strategies = len([s for s in self.strategies if s.status == StrategyStatus.ACTIVE])
        self.total_pnl = sum(s.current_pnl for s in self.strategies)
    
    # Configuração da interface gráfica
    def setup_ui(self) -> None:
        """Configurar interface principal"""
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="20", style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Cabeçalho
        self.setup_header(main_frame)
        
        # Notebook para abas (equivalente ao Tabs do React)
        self.setup_notebook(main_frame)
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def setup_header(self, parent: ttk.Frame) -> None:
        """Configurar cabeçalho da aplicação"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Título
        title_label = ttk.Label(header_frame, 
                               text="💻 Estratégias Algorítmicas", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Status e controles
        control_frame = ttk.Frame(header_frame)
        control_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Badge de estratégias ativas
        self.active_label = tk.Label(control_frame, 
                                    text=f"📊 {self.active_strategies} ATIVAS",
                                    bg="#10b981",
                                    fg="white",
                                    font=("Arial", 10, "bold"),
                                    padx=10, pady=5)
        self.active_label.grid(row=0, column=0, padx=(0, 10))
        
        # Badge de P&L
        pnl_color = "#3b82f6" if self.total_pnl > 0 else "#ef4444"
        pnl_text = f"P&L: {'+' if self.total_pnl > 0 else ''}{self.total_pnl:.1f}%"
        self.pnl_label = tk.Label(control_frame, 
                                 text=pnl_text,
                                 bg="white",
                                 fg=pnl_color,
                                 font=("Arial", 10, "bold"),
                                 relief='solid',
                                 borderwidth=1,
                                 padx=10, pady=5)
        self.pnl_label.grid(row=0, column=1)
        
        header_frame.columnconfigure(0, weight=1)
    
    def setup_notebook(self, parent: ttk.Frame) -> None:
        """Configurar notebook com abas (equivalente ao Tabs do React)"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba Estratégias
        strategies_frame = ttk.Frame(self.notebook)
        self.notebook.add(strategies_frame, text="🧠 Estratégias")
        self.setup_strategies_tab(strategies_frame)
        
        # Aba Sinais Ativos
        signals_frame = ttk.Frame(self.notebook)
        self.notebook.add(signals_frame, text="🎯 Sinais Ativos")
        self.setup_signals_tab(signals_frame)
    
    def setup_strategies_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de estratégias (equivalente ao TabsContent strategies)"""
        # Canvas com scroll para estratégias
        canvas = tk.Canvas(parent, bg='#f8fafc', height=320)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        strategies_container = ttk.Frame(canvas)
        
        strategies_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=strategies_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Criar cards de estratégias
        self.strategy_frames = []
        for i, strategy in enumerate(self.strategies):
            frame = self.create_strategy_card(strategies_container, strategy, i)
            self.strategy_frames.append(frame)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        strategies_container.columnconfigure(0, weight=1)
    
    def create_strategy_card(self, parent: ttk.Frame, strategy: Strategy, index: int) -> ttk.Frame:
        """Criar card individual de estratégia"""
        card_frame = ttk.LabelFrame(parent, 
                                   text="", 
                                   padding="15",
                                   style='Card.TFrame')
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Header da estratégia
        header_frame = ttk.Frame(card_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Lado esquerdo: ícone, nome, badges
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        # Ícone
        ttk.Label(left_frame, text="🧠", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
        
        # Nome e badges
        name_badges_frame = ttk.Frame(left_frame)
        name_badges_frame.grid(row=0, column=1)
        
        ttk.Label(name_badges_frame, text=strategy.name, 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W)
        
        badges_frame = ttk.Frame(name_badges_frame)
        badges_frame.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
        
        # Badge tipo
        type_color = self.get_strategy_type_color(strategy.type)
        type_label = tk.Label(badges_frame, 
                             text=strategy.type.value,
                             bg="white",
                             fg=type_color,
                             font=("Arial", 8, "bold"),
                             relief='solid',
                             borderwidth=1,
                             padx=6, pady=2)
        type_label.grid(row=0, column=0, padx=(0, 5))
        
        # Badge risco
        risk_color = self.get_risk_color(strategy.risk_level)
        risk_label = tk.Label(badges_frame, 
                             text=f"{strategy.risk_level.value} RISK",
                             bg="white",
                             fg=risk_color,
                             font=("Arial", 8, "bold"),
                             relief='solid',
                             borderwidth=1,
                             padx=6, pady=2)
        risk_label.grid(row=0, column=1)
        
        # Lado direito: status e P&L
        right_frame = ttk.Frame(header_frame)
        right_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Status
        status_color = self.get_status_color(strategy.status)
        status_icon = "▶️" if strategy.status == StrategyStatus.ACTIVE else "⏸️"
        status_label = tk.Label(right_frame, 
                               text=f"{status_icon} {strategy.status.value}",
                               bg=status_color,
                               fg="white",
                               font=("Arial", 8, "bold"),
                               padx=8, pady=2)
        status_label.grid(row=0, column=0, padx=(0, 10))
        
        # P&L
        pnl_color = "#3b82f6" if strategy.current_pnl > 0 else "#ef4444"
        pnl_text = f"{'+' if strategy.current_pnl > 0 else ''}{strategy.current_pnl:.1f}%"
        ttk.Label(right_frame, text=pnl_text, 
                 font=("Arial", 10, "bold"), 
                 foreground=pnl_color).grid(row=0, column=1)
        
        header_frame.columnconfigure(0, weight=1)
        
        # Grid de métricas principais
        main_metrics_frame = ttk.Frame(card_frame)
        main_metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Win Rate
        wr_frame = ttk.Frame(main_metrics_frame)
        wr_frame.grid(row=0, column=0, padx=(0, 20))
        
        ttk.Label(wr_frame, text="Win Rate", font=("Arial", 8)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(wr_frame, text=f"{strategy.win_rate:.1f}%", 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=1, column=0, sticky=tk.W)
        
        # Simular barra de progresso
        wr_progress_frame = ttk.Frame(wr_frame, relief='sunken', borderwidth=1)
        wr_progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        
        wr_width = int(strategy.win_rate * 1.5)
        wr_progress_label = tk.Label(wr_progress_frame, 
                                    text="", 
                                    bg="#3b82f6", 
                                    width=wr_width//8 if wr_width > 0 else 1,
                                    height=1)
        wr_progress_label.grid(row=0, column=0, sticky=tk.W)
        
        wr_frame.columnconfigure(0, weight=1)
        
        # Profit Factor
        pf_frame = ttk.Frame(main_metrics_frame)
        pf_frame.grid(row=0, column=1)
        
        ttk.Label(pf_frame, text="Profit Factor", font=("Arial", 8)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(pf_frame, text=f"{strategy.profit_factor:.2f}", 
                 font=("Arial", 8, "bold")).grid(row=1, column=0, sticky=tk.W)
        
        # Simular barra de progresso
        pf_progress_frame = ttk.Frame(pf_frame, relief='sunken', borderwidth=1)
        pf_progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        
        pf_width = int((strategy.profit_factor / 3.5) * 100 * 1.5)
        pf_progress_label = tk.Label(pf_progress_frame, 
                                    text="", 
                                    bg="#10b981", 
                                    width=pf_width//8 if pf_width > 0 else 1,
                                    height=1)
        pf_progress_label.grid(row=0, column=0, sticky=tk.W)
        
        pf_frame.columnconfigure(0, weight=1)
        
        # Grid de métricas detalhadas
        detail_metrics_frame = ttk.Frame(card_frame)
        detail_metrics_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Sharpe
        sharpe_frame = ttk.Frame(detail_metrics_frame)
        sharpe_frame.grid(row=0, column=0, padx=(0, 15))
        
        ttk.Label(sharpe_frame, text="Sharpe", font=("Arial", 8)).grid(row=0, column=0)
        ttk.Label(sharpe_frame, text=f"{strategy.sharpe_ratio:.2f}", 
                 font=("Arial", 8, "bold")).grid(row=1, column=0)
        
        # Max DD
        dd_frame = ttk.Frame(detail_metrics_frame)
        dd_frame.grid(row=0, column=1, padx=(0, 15))
        
        ttk.Label(dd_frame, text="Max DD", font=("Arial", 8)).grid(row=0, column=0)
        ttk.Label(dd_frame, text=f"{strategy.max_drawdown:.1f}%", 
                 font=("Arial", 8, "bold"), style='Error.TLabel').grid(row=1, column=0)
        
        # Trades
        trades_frame = ttk.Frame(detail_metrics_frame)
        trades_frame.grid(row=0, column=2, padx=(0, 15))
        
        ttk.Label(trades_frame, text="Trades", font=("Arial", 8)).grid(row=0, column=0)
        ttk.Label(trades_frame, text=str(strategy.total_trades), 
                 font=("Arial", 8, "bold")).grid(row=1, column=0)
        
        # Avg Hold
        hold_frame = ttk.Frame(detail_metrics_frame)
        hold_frame.grid(row=0, column=3)
        
        ttk.Label(hold_frame, text="Avg Hold", font=("Arial", 8)).grid(row=0, column=0)
        ttk.Label(hold_frame, text=strategy.avg_hold_time, 
                 font=("Arial", 8, "bold")).grid(row=1, column=0)
        
        card_frame.columnconfigure(0, weight=1)
        return card_frame
    
    def setup_signals_tab(self, parent: ttk.Frame) -> None:
        """Configurar aba de sinais ativos (equivalente ao TabsContent signals)"""
        # Header da aba
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(10, 20))
        
        title_label = ttk.Label(header_frame, 
                               text="🎯 Sinais de Trading Ativos", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        signals_badge = tk.Label(header_frame, 
                                text=f"⚡ {len(self.signals)} SINAIS",
                                bg="#6b7280",
                                fg="white",
                                font=("Arial", 10, "bold"),
                                padx=10, pady=5)
        signals_badge.grid(row=0, column=1, sticky=tk.E)
        
        header_frame.columnconfigure(0, weight=1)
        
        # Canvas com scroll para sinais
        canvas = tk.Canvas(parent, bg='#f8fafc')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        signals_container = ttk.Frame(canvas)
        
        signals_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=signals_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Criar cards de sinais
        self.signal_frames = []
        for i, signal in enumerate(self.signals):
            frame = self.create_signal_card(signals_container, signal, i)
            self.signal_frames.append(frame)
        
        # Área de informações dos algoritmos
        self.create_algorithms_info_card(signals_container, len(self.signals))
        
        canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        signals_container.columnconfigure(0, weight=1)
    
    def create_signal_card(self, parent: ttk.Frame, signal: StrategySignal, index: int) -> ttk.Frame:
        """Criar card individual de sinal"""
        card_frame = ttk.LabelFrame(parent, 
                                   text="", 
                                   padding="15",
                                   style='Card.TFrame')
        card_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), pady=8, padx=10)
        
        # Header do sinal
        header_frame = ttk.Frame(card_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Lado esquerdo: ícone, nome, detalhes
        left_frame = ttk.Frame(header_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        # Ícone da ação
        action_icon = self.get_action_icon(signal.action)
        ttk.Label(left_frame, text=action_icon, font=("Arial", 12)).grid(row=0, column=0, padx=(0, 5))
        
        # Nome e detalhes
        details_frame = ttk.Frame(left_frame)
        details_frame.grid(row=0, column=1)
        
        ttk.Label(details_frame, text=signal.strategy, 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(details_frame, text=f"{signal.timeframe} • Força: {signal.strength:.1f}", 
                 font=("Arial", 8), foreground="#6b7280").grid(row=1, column=0, sticky=tk.W)
        
        # Badge de ação
        action_color = self.get_action_color(signal.action)
        action_label = tk.Label(header_frame, 
                               text=signal.action.value,
                               bg=action_color,
                               fg="white",
                               font=("Arial", 8, "bold"),
                               padx=8, pady=2)
        action_label.grid(row=0, column=1, sticky=tk.E)
        
        header_frame.columnconfigure(0, weight=1)
        
        # Grid de preços
        prices_frame = ttk.Frame(card_frame)
        prices_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Preço Entrada
        entry_frame = ttk.Frame(prices_frame)
        entry_frame.grid(row=0, column=0, padx=(0, 20))
        
        ttk.Label(entry_frame, text="Preço Entrada", font=("Arial", 8)).grid(row=0, column=0)
        ttk.Label(entry_frame, text=f"${signal.price:,.0f}", 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=1, column=0)
        
        # Stop Loss
        sl_frame = ttk.Frame(prices_frame)
        sl_frame.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(sl_frame, text="Stop Loss", font=("Arial", 8)).grid(row=0, column=0)
        sl_text = f"${signal.stop_loss:,.0f}" if signal.stop_loss > 0 else "N/A"
        ttk.Label(sl_frame, text=sl_text, 
                 font=("Arial", 8, "bold"), style='Error.TLabel').grid(row=1, column=0)
        
        # Take Profit
        tp_frame = ttk.Frame(prices_frame)
        tp_frame.grid(row=0, column=2)
        
        ttk.Label(tp_frame, text="Take Profit", font=("Arial", 8)).grid(row=0, column=0)
        tp_text = f"${signal.take_profit:,.0f}" if signal.take_profit > 0 else "N/A"
        ttk.Label(tp_frame, text=tp_text, 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=1, column=0)
        
        # Confiança IA
        confidence_frame = ttk.Frame(card_frame)
        confidence_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(confidence_frame, text="Confiança IA", font=("Arial", 8)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(confidence_frame, text=f"{signal.confidence:.1f}%", 
                 font=("Arial", 8, "bold"), style='Info.TLabel').grid(row=1, column=0, sticky=tk.W)
        
        # Simular barra de progresso para confiança
        conf_progress_frame = ttk.Frame(confidence_frame, relief='sunken', borderwidth=1)
        conf_progress_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E), padx=(20, 0))
        
        conf_width = int(signal.confidence * 1.5)
        conf_progress_label = tk.Label(conf_progress_frame, 
                                      text="", 
                                      bg="#3b82f6", 
                                      width=conf_width//8 if conf_width > 0 else 1,
                                      height=1)
        conf_progress_label.grid(row=0, column=0, sticky=tk.W)
        
        confidence_frame.columnconfigure(1, weight=1)
        card_frame.columnconfigure(0, weight=1)
        
        return card_frame
    
    def create_algorithms_info_card(self, parent: ttk.Frame, row: int) -> None:
        """Criar card de informações dos algoritmos"""
        info_frame = ttk.LabelFrame(parent, 
                                   text="🧠 Algoritmos Avançados", 
                                   padding="15",
                                   style='Card.TFrame')
        info_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=15, padx=10)
        
        info_text = """• Machine Learning para otimização de parâmetros
• Redes neurais para detecção de padrões complexos
• Genetic algorithms para evolução de estratégias
• Reinforcement learning para adaptação ao mercado
• Ensemble methods para combinação de sinais
• Walk-forward analysis para validação robusta
• Monte Carlo simulation para análise de risco
• Backtesting com dados tick-by-tick"""
        
        info_label = ttk.Label(info_frame, 
                              text=info_text,
                              font=("Arial", 9),
                              wraplength=800,
                              foreground="#6b7280")
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        info_frame.columnconfigure(0, weight=1)
    
    def update_displays(self) -> None:
        """Atualizar todos os displays da interface"""
        # Recalcular valores
        self.active_strategies = len([s for s in self.strategies if s.status == StrategyStatus.ACTIVE])
        self.total_pnl = sum(s.current_pnl for s in self.strategies)
        
        # Atualizar labels do header
        if self.active_label:
            self.active_label.config(text=f"📊 {self.active_strategies} ATIVAS")
        
        if self.pnl_label:
            pnl_color = "#3b82f6" if self.total_pnl > 0 else "#ef4444"
            pnl_text = f"P&L: {'+' if self.total_pnl > 0 else ''}{self.total_pnl:.1f}%"
            self.pnl_label.config(text=pnl_text, fg=pnl_color)
    
    def start_update_thread(self) -> None:
        """Iniciar thread de atualização periódica (equivalente ao useEffect)"""
        def update_worker():
            while True:
                # Atualizar estratégias (equivalente ao setStrategies)
                for strategy in self.strategies:
                    strategy.current_pnl += (random.random() - 0.5) * 0.5
                    strategy.win_rate = max(60, min(90, strategy.win_rate + (random.random() - 0.5) * 1))
                    strategy.profit_factor = max(1.2, min(3.5, strategy.profit_factor + (random.random() - 0.5) * 0.05))
                    strategy.total_trades += random.randint(0, 2)
                
                # Atualizar sinais (equivalente ao setSignals)
                for signal in self.signals:
                    signal.strength = max(30, min(95, signal.strength + (random.random() - 0.5) * 5))
                    signal.confidence = max(50, min(98, signal.confidence + (random.random() - 0.5) * 3))
                    signal.price += (random.random() - 0.5) * 100
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_displays)
                
                time.sleep(3)  # Equivalente ao interval de 3000ms do React
        
        threading.Thread(target=update_worker, daemon=True).start()


def main() -> None:
    """Função principal para executar a aplicação (equivalente ao export do React)"""
    root = tk.Tk()
    app = AlgorithmicStrategiesApp(root)
    
    # Tornar a janela responsiva
    root.minsize(1200, 800)
    
    # Centralizar janela
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    main()
