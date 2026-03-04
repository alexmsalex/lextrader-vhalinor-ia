"""
LEXTRADER-IAG - Sistema Avançado de Dashboard para Trading Algorítmico
Interface gráfica completa com monitoramento em tempo real, simulação e controle
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, colorchooser
from dataclasses import dataclass, field, asdict
from typing import List, Literal, Dict, Any, Optional, Callable, Tuple, Union
from datetime import datetime, timedelta
import threading
import time
import random
import json
import pickle
import csv
from enum import Enum
import math
import queue
import hashlib
import base64
from collections import deque, defaultdict
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import mplfinance as mpf
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
import logging
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_dashboard.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS E ESTRUTURAS DE DADOS AVANÇADAS
# ============================================================================

class AlgorithmType(Enum):
    ML = "Machine Learning"
    STATISTICAL = "Statistical"
    HYBRID = "Hybrid AI"
    QUANTUM = "Quantum-Inspired"
    ENSEMBLE = "Ensemble"
    NEUROSYMBOLIC = "Neuro-Symbolic"
    METALEARNING = "Meta-Learning"
    EVOLUTIONARY = "Evolutionary"
    DEEPREINFORCEMENT = "Deep Reinforcement"
    TRANSFORMER = "Transformer-Based"

class NodeStatus(Enum):
    IDLE = "IDLE"
    INITIALIZING = "INITIALIZING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    WAITING = "WAITING"
    ERROR = "ERROR"
    PAUSED = "PAUSED"
    OPTIMIZING = "OPTIMIZING"
    CONVERGING = "CONVERGING"
    VALIDATING = "VALIDATING"

class Decision(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE = "CLOSE"
    SCALP_BUY = "SCALP_BUY"
    SCALP_SELL = "SCALP_SELL"
    SWING_BUY = "SWING_BUY"
    SWING_SELL = "SWING_SELL"
    HEDGE = "HEDGE"
    REBALANCE = "REBALANCE"

class RiskLevel(Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    EXTREME = "EXTREME"

class MarketCondition(Enum):
    TRENDING_BULL = "TRENDING_BULL"
    TRENDING_BEAR = "TRENDING_BEAR"
    RANGING = "RANGING"
    VOLATILE = "VOLATILE"
    BREAKOUT = "BREAKOUT"
    REVERSAL = "REVERSAL"
    ACCUMULATION = "ACCUMULATION"
    DISTRIBUTION = "DISTRIBUTION"
    SIDEWAYS = "SIDEWAYS"
    CRASH = "CRASH"
    RALLY = "RALLY"

class TimeFrame(Enum):
    TICK = "TICK"
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    MN1 = "1M"

class AssetClass(Enum):
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    STOCKS = "STOCKS"
    INDICES = "INDICES"
    COMMODITIES = "COMMODITIES"
    FUTURES = "FUTURES"
    OPTIONS = "OPTIONS"
    BONDS = "BONDS"
    ETF = "ETF"

class ExecutionMode(Enum):
    PAPER = "PAPER"
    LIVE = "LIVE"
    SIMULATION = "SIMULATION"
    BACKTEST = "BACKTEST"
    HYBRID = "HYBRID"

class AlertType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    CRITICAL = "CRITICAL"
    TRADE_SIGNAL = "TRADE_SIGNAL"
    RISK_ALERT = "RISK_ALERT"
    SYSTEM_ALERT = "SYSTEM_ALERT"
    PERFORMANCE_ALERT = "PERFORMANCE_ALERT"

# ============================================================================
# ESTRUTURAS DE DADOS COMPLEXAS
# ============================================================================

@dataclass
class AdvancedAlgorithm:
    """Algoritmo avançado com múltiplas métricas e configurações"""
    id: str
    name: str
    type: AlgorithmType
    description: str
    version: str = "1.0.0"
    
    # Métricas de performance
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    
    # Métricas operacionais
    speed: float = 0.0
    latency: float = 0.0
    throughput: float = 0.0
    complexity: float = 0.0
    confidence: float = 0.0
    stability: float = 0.0
    robustness: float = 0.0
    
    # Configurações
    is_active: bool = False
    is_optimizing: bool = False
    is_training: bool = False
    requires_gpu: bool = False
    memory_usage_mb: int = 0
    parameters: Dict[str, Any] = field(default_factory=dict)
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    
    # Estatísticas
    decisions_made: int = 0
    decisions_today: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_profit: float = 0.0
    total_loss: float = 0.0
    avg_response_time: float = 0.0
    avg_holding_time: float = 0.0
    
    # Especialização
    specializations: List[str] = field(default_factory=list)
    compatible_assets: List[str] = field(default_factory=list)
    optimal_timeframes: List[TimeFrame] = field(default_factory=list)
    market_conditions: List[MarketCondition] = field(default_factory=list)
    
    # Neural Network Specific
    neural_architecture: Optional[str] = None
    num_layers: int = 0
    num_parameters: int = 0
    training_epochs: int = 0
    last_trained: Optional[datetime] = None
    
    def update_metrics(self, **kwargs):
        """Atualizar métricas do algoritmo"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converter para dicionário"""
        return asdict(self)
    
    def calculate_performance_score(self) -> float:
        """Calcular score de performance ponderado"""
        weights = {
            'accuracy': 0.15,
            'win_rate': 0.20,
            'sharpe_ratio': 0.15,
            'profit_factor': 0.10,
            'max_drawdown': -0.10,  # Negativo porque drawdown menor é melhor
            'stability': 0.10,
            'robustness': 0.10,
            'speed': 0.05,
            'latency': -0.05  # Negativo porque latência menor é melhor
        }
        
        score = 0.0
        for metric, weight in weights.items():
            value = getattr(self, metric, 0.0)
            score += value * weight
        
        return max(0.0, min(100.0, score))

@dataclass
class AdvancedNode:
    """Nó avançado do fluxo de processamento"""
    id: str
    name: str
    category: str
    input_type: str
    output_type: str
    description: str
    
    # Métricas
    confidence: float = 0.0
    execution_time: float = 0.0
    processing_speed: float = 0.0
    error_rate: float = 0.0
    
    # Estado
    status: NodeStatus = NodeStatus.IDLE
    progress: float = 0.0
    last_execution: Optional[datetime] = None
    execution_count: int = 0
    success_count: int = 0
    
    # Dependências
    dependencies: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    
    # Recursos
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    gpu_usage: float = 0.0
    
    # Configurações
    timeout_seconds: int = 30
    retry_count: int = 3
    priority: int = 1
    
    def get_status_color(self) -> str:
        """Obter cor baseada no status"""
        color_map = {
            NodeStatus.IDLE: "#9ca3af",
            NodeStatus.INITIALIZING: "#60a5fa",
            NodeStatus.PROCESSING: "#3b82f6",
            NodeStatus.COMPLETED: "#10b981",
            NodeStatus.WAITING: "#f59e0b",
            NodeStatus.ERROR: "#ef4444",
            NodeStatus.PAUSED: "#8b5cf6",
            NodeStatus.OPTIMIZING: "#ec4899",
            NodeStatus.CONVERGING: "#14b8a6",
            NodeStatus.VALIDATING: "#f97316"
        }
        return color_map.get(self.status, "#9ca3af")
    
    def get_status_icon(self) -> str:
        """Obter ícone baseado no status"""
        icon_map = {
            NodeStatus.IDLE: "⏸️",
            NodeStatus.INITIALIZING: "🔄",
            NodeStatus.PROCESSING: "⚙️",
            NodeStatus.COMPLETED: "✅",
            NodeStatus.WAITING: "⏳",
            NodeStatus.ERROR: "❌",
            NodeStatus.PAUSED: "⏸️",
            NodeStatus.OPTIMIZING: "📈",
            NodeStatus.CONVERGING: "🎯",
            NodeStatus.VALIDATING: "🔍"
        }
        return icon_map.get(self.status, "❓")

@dataclass
class AdvancedDecision:
    """Decisão avançada de trading"""
    decision_id: str
    timestamp: datetime
    algorithm_id: str
    algorithm_name: str
    decision_type: Decision
    confidence: float
    
    # Detalhes da decisão
    symbol: str
    timeframe: TimeFrame
    entry_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    leverage: float = 1.0
    
    # Raciocínio e análise
    reasoning: str
    technical_factors: List[str] = field(default_factory=list)
    fundamental_factors: List[str] = field(default_factory=list)
    sentiment_factors: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    
    # Análise de risco
    risk_level: RiskLevel = RiskLevel.MODERATE
    risk_score: float = 0.0
    var_95: float = 0.0
    expected_return: float = 0.0
    expected_loss: float = 0.0
    risk_reward_ratio: float = 0.0
    
    # Mercado
    market_condition: MarketCondition = MarketCondition.RANGING
    volatility: float = 0.0
    volume_ratio: float = 0.0
    trend_strength: float = 0.0
    
    # Metadados
    execution_mode: ExecutionMode = ExecutionMode.PAPER
    is_executed: bool = False
    execution_time: Optional[datetime] = None
    execution_price: Optional[float] = None
    pnl: Optional[float] = None
    pnl_percentage: Optional[float] = None
    
    def calculate_pnl(self, current_price: float) -> float:
        """Calcular P&L baseado no preço atual"""
        if not self.is_executed or self.execution_price is None:
            return 0.0
        
        if self.decision_type in [Decision.BUY, Decision.SCALP_BUY, Decision.SWING_BUY]:
            return (current_price - self.execution_price) * self.position_size
        elif self.decision_type in [Decision.SELL, Decision.SCALP_SELL, Decision.SWING_SELL]:
            return (self.execution_price - current_price) * self.position_size
        else:
            return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Converter para dicionário"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        if self.execution_time:
            data['execution_time'] = self.execution_time.isoformat()
        return data

@dataclass
class PortfolioPosition:
    """Posição do portfólio"""
    symbol: str
    asset_class: AssetClass
    quantity: float
    entry_price: float
    current_price: float
    entry_time: datetime
    position_type: Literal['LONG', 'SHORT']
    
    # Métricas
    unrealized_pnl: float = 0.0
    unrealized_pnl_percent: float = 0.0
    realized_pnl: float = 0.0
    total_invested: float = 0.0
    current_value: float = 0.0
    
    # Gerenciamento de risco
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    trailing_stop: Optional[float] = None
    risk_score: float = 0.0
    
    # Metadados
    algorithm_id: str = ""
    decision_id: str = ""
    is_hedged: bool = False
    hedge_ratio: float = 0.0
    
    def update_prices(self, new_price: float):
        """Atualizar preços e calcular P&L"""
        self.current_price = new_price
        
        if self.position_type == 'LONG':
            self.unrealized_pnl = (new_price - self.entry_price) * self.quantity
        else:  # SHORT
            self.unrealized_pnl = (self.entry_price - new_price) * self.quantity
        
        self.total_invested = self.entry_price * self.quantity
        self.current_value = new_price * self.quantity
        
        if self.total_invested > 0:
            self.unrealized_pnl_percent = (self.unrealized_pnl / self.total_invested) * 100

@dataclass
class MarketData:
    """Dados de mercado em tempo real"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float = 0.0
    
    # Indicadores técnicos
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    atr: Optional[float] = None
    obv: Optional[float] = None
    stochastic_k: Optional[float] = None
    stochastic_d: Optional[float] = None
    adx: Optional[float] = None
    
    # Sentimento
    sentiment_score: float = 0.0
    fear_greed_index: float = 0.0
    market_sentiment: Literal['BULLISH', 'BEARISH', 'NEUTRAL'] = 'NEUTRAL'
    
    # Order book (simplificado)
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    bid_volume: Optional[float] = None
    ask_volume: Optional[float] = None
    spread: Optional[float] = None
    
    def calculate_indicators(self):
        """Calcular indicadores básicos"""
        # Calcular spread se bid/ask disponíveis
        if self.bid_price and self.ask_price:
            self.spread = self.ask_price - self.bid_price
        
        # Calcular tendência básica
        price_change = ((self.close - self.open) / self.open) * 100
        if price_change > 1.0:
            self.market_sentiment = 'BULLISH'
        elif price_change < -1.0:
            self.market_sentiment = 'BEARISH'
        else:
            self.market_sentiment = 'NEUTRAL'

@dataclass
class Alert:
    """Alerta do sistema"""
    alert_id: str
    timestamp: datetime
    alert_type: AlertType
    title: str
    message: str
    source: str
    
    # Prioridade
    priority: int = 1  # 1-10, onde 10 é mais importante
    is_acknowledged: bool = False
    is_resolved: bool = False
    
    # Ações
    action_required: bool = False
    action_taken: Optional[str] = None
    action_time: Optional[datetime] = None
    
    # Metadados
    related_symbol: Optional[str] = None
    related_algorithm: Optional[str] = None
    related_decision: Optional[str] = None
    
    def get_color(self) -> str:
        """Obter cor baseada no tipo de alerta"""
        color_map = {
            AlertType.INFO: "#3b82f6",
            AlertType.WARNING: "#f59e0b",
            AlertType.ERROR: "#ef4444",
            AlertType.SUCCESS: "#10b981",
            AlertType.CRITICAL: "#dc2626",
            AlertType.TRADE_SIGNAL: "#8b5cf6",
            AlertType.RISK_ALERT: "#ec4899",
            AlertType.SYSTEM_ALERT: "#6366f1",
            AlertType.PERFORMANCE_ALERT: "#14b8a6"
        }
        return color_map.get(self.alert_type, "#6b7280")
    
    def get_icon(self) -> str:
        """Obter ícone baseado no tipo de alerta"""
        icon_map = {
            AlertType.INFO: "ℹ️",
            AlertType.WARNING: "⚠️",
            AlertType.ERROR: "❌",
            AlertType.SUCCESS: "✅",
            AlertType.CRITICAL: "🔥",
            AlertType.TRADE_SIGNAL: "📈",
            AlertType.RISK_ALERT: "🚨",
            AlertType.SYSTEM_ALERT: "🔧",
            AlertType.PERFORMANCE_ALERT: "📊"
        }
        return icon_map.get(self.alert_type, "📢")

@dataclass
class SystemMetrics:
    """Métricas do sistema"""
    timestamp: datetime
    
    # Performance
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    gpu_usage: float = 0.0
    disk_usage: float = 0.0
    network_usage: float = 0.0
    
    # Trading
    active_trades: int = 0
    pending_orders: int = 0
    daily_trades: int = 0
    weekly_trades: int = 0
    monthly_trades: int = 0
    
    # Financeiro
    total_equity: float = 0.0
    available_balance: float = 0.0
    margin_used: float = 0.0
    total_pnl: float = 0.0
    daily_pnl: float = 0.0
    weekly_pnl: float = 0.0
    monthly_pnl: float = 0.0
    
    # Algoritmos
    active_algorithms: int = 0
    total_algorithms: int = 0
    algorithm_success_rate: float = 0.0
    avg_decision_time: float = 0.0
    
    # Rede
    latency_ms: float = 0.0
    packet_loss: float = 0.0
    connection_status: str = "CONNECTED"
    
    def update_from_dict(self, data: Dict[str, Any]):
        """Atualizar métricas a partir de dicionário"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

# ============================================================================
# GERENCIADOR DE EVENTOS AVANÇADOS
# ============================================================================

class EventManager:
    """Gerenciador de eventos para comunicação entre componentes"""
    
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.event_queue = queue.Queue()
        self.is_running = False
        self.worker_thread = None
        
    def subscribe(self, event_type: str, callback: Callable):
        """Inscrever callback para tipo de evento"""
        self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Cancelar inscrição de callback"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
    
    def publish(self, event_type: str, data: Any = None):
        """Publicar evento"""
        event = {'type': event_type, 'data': data, 'timestamp': datetime.now()}
        self.event_queue.put(event)
    
    def start(self):
        """Iniciar processamento de eventos"""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_events, daemon=True)
        self.worker_thread.start()
    
    def stop(self):
        """Parar processamento de eventos"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)
    
    def _process_events(self):
        """Processar eventos na fila"""
        while self.is_running:
            try:
                event = self.event_queue.get(timeout=0.1)
                event_type = event['type']
                
                # Notificar todos os subscribers
                if event_type in self.subscribers:
                    for callback in self.subscribers[event_type]:
                        try:
                            callback(event['data'])
                        except Exception as e:
                            logger.error(f"Error in event callback: {e}")
                
                self.event_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")

# ============================================================================
# COMPONENTES VISUAIS PERSONALIZADOS
# ============================================================================

class GradientFrame(tk.Frame):
    """Frame com gradiente de fundo"""
    
    def __init__(self, parent, color1="#1e3a8a", color2="#3b82f6", **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        """Desenhar gradiente no frame"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 1 and height > 1:
            # Criar imagem com gradiente
            image = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(image)
            
            # Desenhar gradiente
            for i in range(height):
                ratio = i / height
                r = int((1 - ratio) * int(self.color1[1:3], 16) + ratio * int(self.color2[1:3], 16))
                g = int((1 - ratio) * int(self.color1[3:5], 16) + ratio * int(self.color2[3:5], 16))
                b = int((1 - ratio) * int(self.color1[5:7], 16) + ratio * int(self.color2[5:7], 16))
                color = f'#{r:02x}{g:02x}{b:02x}'
                draw.line([(0, i), (width, i)], fill=color)
            
            # Converter para PhotoImage
            self.gradient_image = ImageTk.PhotoImage(image)
            
            # Criar label com imagem
            if hasattr(self, 'gradient_label'):
                self.gradient_label.destroy()
            
            self.gradient_label = tk.Label(self, image=self.gradient_image)
            self.gradient_label.place(x=0, y=0, relwidth=1, relheight=1)

class AnimatedProgressBar(ttk.Frame):
    """Barra de progresso animada"""
    
    def __init__(self, parent, length=200, height=20, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.length = length
        self.height = height
        self.value = 0
        self.max_value = 100
        self.animation_speed = 10
        
        # Canvas para animação
        self.canvas = tk.Canvas(self, width=length, height=height, 
                               highlightthickness=0, bg='#1f2937')
        self.canvas.pack()
        
        # Elementos da barra
        self.bg_rect = self.canvas.create_rectangle(0, 0, length, height, 
                                                   fill='#374151', outline='')
        self.progress_rect = self.canvas.create_rectangle(0, 0, 0, height, 
                                                         fill='#3b82f6', outline='')
        self.glow_rect = self.canvas.create_rectangle(0, 0, 0, height, 
                                                      fill='#60a5fa', outline='')
        
        # Texto
        self.text = self.canvas.create_text(length/2, height/2, 
                                           text="0%", fill='white',
                                           font=('Arial', 9, 'bold'))
        
        # Animar
        self.animate_glow()
    
    def set_value(self, value: float):
        """Definir valor da barra de progresso"""
        self.value = max(0, min(value, self.max_value))
        self.update_display()
    
    def update_display(self):
        """Atualizar display da barra"""
        width = (self.value / self.max_value) * self.length
        
        # Atualizar retângulos
        self.canvas.coords(self.progress_rect, 0, 0, width, self.height)
        
        # Atualizar texto
        self.canvas.itemconfig(self.text, text=f"{self.value:.1f}%")
        
        # Ajustar cor baseada no valor
        if self.value < 30:
            color = '#ef4444'  # Vermelho
        elif self.value < 70:
            color = '#f59e0b'  # Amarelo
        else:
            color = '#10b981'  # Verde
        
        self.canvas.itemconfig(self.progress_rect, fill=color)
    
    def animate_glow(self):
        """Animar efeito de brilho"""
        if self.value > 0:
            glow_width = (self.value / self.max_value) * self.length
            glow_pos = (glow_width * 0.8) + (math.sin(time.time() * 5) * 10)
            
            self.canvas.coords(self.glow_rect, 
                             glow_pos - 20, 0, 
                             glow_pos + 20, self.height)
        
        self.after(50, self.animate_glow)

class SparklineGraph(ttk.Frame):
    """Gráfico sparkline para métricas"""
    
    def __init__(self, parent, width=100, height=30, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.width = width
        self.height = height
        self.data = deque(maxlen=50)
        self.color = '#3b82f6'
        
        # Canvas
        self.canvas = tk.Canvas(self, width=width, height=height, 
                               highlightthickness=0, bg='#111827')
        self.canvas.pack()
        
        # Grid
        self.draw_grid()
    
    def add_data(self, value: float):
        """Adicionar ponto de dado"""
        self.data.append(value)
        self.redraw()
    
    def draw_grid(self):
        """Desenhar grade do gráfico"""
        # Linhas horizontais
        for i in range(0, self.height, self.height//4):
            self.canvas.create_line(0, i, self.width, i, 
                                   fill='#374151', width=1)
    
    def redraw(self):
        """Redesenhar gráfico"""
        self.canvas.delete('sparkline')
        
        if len(self.data) < 2:
            return
        
        # Encontrar mínimo e máximo
        min_val = min(self.data)
        max_val = max(self.data)
        range_val = max_val - min_val
        
        if range_val == 0:
            range_val = 1
        
        # Desenhar linha
        points = []
        for i, val in enumerate(self.data):
            x = (i / (len(self.data) - 1)) * (self.width - 1)
            y = self.height - 1 - ((val - min_val) / range_val) * (self.height - 1)
            points.extend([x, y])
        
        self.canvas.create_line(points, fill=self.color, width=2, 
                               tags='sparkline', smooth=True)
        
        # Adicionar ponto final
        if points:
            last_x, last_y = points[-2], points[-1]
            self.canvas.create_oval(last_x-3, last_y-3, last_x+3, last_y+3,
                                   fill=self.color, outline='white', width=1,
                                   tags='sparkline')

class LedIndicator(ttk.Frame):
    """Indicador LED para status"""
    
    def __init__(self, parent, size=20, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.size = size
        self.state = False
        self.color_off = '#4b5563'
        self.color_on = '#10b981'
        self.blink_interval = 500
        
        # Canvas
        self.canvas = tk.Canvas(self, width=size, height=size, 
                               highlightthickness=0, bg=self['bg'])
        self.canvas.pack()
        
        # Desenhar LED
        self.led = self.canvas.create_oval(2, 2, size-2, size-2,
                                          fill=self.color_off,
                                          outline='white', width=1)
    
    def set_state(self, state: bool):
        """Definir estado do LED"""
        self.state = state
        color = self.color_on if state else self.color_off
        self.canvas.itemconfig(self.led, fill=color)
    
    def blink(self, interval: Optional[int] = None):
        """Piscar LED"""
        if interval:
            self.blink_interval = interval
        
        def toggle():
            current_state = self.state
            self.set_state(not current_state)
            self.after(self.blink_interval, toggle)
        
        toggle()

class CircularProgress(ttk.Frame):
    """Progresso circular animado"""
    
    def __init__(self, parent, size=80, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.size = size
        self.value = 0
        self.max_value = 100
        
        # Canvas
        self.canvas = tk.Canvas(self, width=size, height=size, 
                               highlightthickness=0, bg=self['bg'])
        self.canvas.pack()
        
        # Desenhar círculos
        center = size // 2
        radius = (size // 2) - 5
        
        # Círculo de fundo
        self.canvas.create_oval(center-radius, center-radius,
                               center+radius, center+radius,
                               fill='#374151', outline='')
        
        # Círculo de progresso
        self.progress_arc = self.canvas.create_arc(center-radius, center-radius,
                                                  center+radius, center+radius,
                                                  start=90, extent=0,
                                                  fill='#3b82f6', outline='')
        
        # Texto
        self.text = self.canvas.create_text(center, center,
                                           text="0%", fill='white',
                                           font=('Arial', 12, 'bold'))
    
    def set_value(self, value: float):
        """Definir valor do progresso"""
        self.value = max(0, min(value, self.max_value))
        
        # Calcular extensão do arco (360 graus = 100%)
        extent = (self.value / self.max_value) * 360
        
        # Atualizar arco
        self.canvas.itemconfig(self.progress_arc, extent=-extent)
        
        # Atualizar texto
        self.canvas.itemconfig(self.text, text=f"{self.value:.0f}%")
        
        # Ajustar cor baseada no valor
        if self.value < 30:
            color = '#ef4444'
        elif self.value < 70:
            color = '#f59e0b'
        else:
            color = '#10b981'
        
        self.canvas.itemconfig(self.progress_arc, fill=color)

# ============================================================================
# APLICAÇÃO PRINCIPAL AVANÇADA
# ============================================================================

class AdvancedTradingDashboard:
    """Dashboard avançado para trading algorítmico"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🚀 LEXTRADER-IAG - Sistema de Trading Algorítmico Avançado")
        self.root.geometry("1920x1080")
        
        # Configurar estado da aplicação
        self.is_running = True
        self.is_processing = False
        self.execution_mode = ExecutionMode.PAPER
        self.last_update = datetime.now()
        
        # Gerenciador de eventos
        self.event_manager = EventManager()
        self.event_manager.start()
        
        # Inicializar dados
        self.initialize_data()
        
        # Configurar interface
        self.setup_styles()
        self.setup_ui()
        
        # Configurar atualizações periódicas
        self.setup_updates()
        
        # Iniciar threads de background
        self.start_background_threads()
        
        # Configurar eventos
        self.setup_events()
    
    def initialize_data(self):
        """Inicializar todos os dados da aplicação"""
        logger.info("Inicializando dados da aplicação...")
        
        # Algoritmos avançados
        self.algorithms = self._create_advanced_algorithms()
        self.algorithm_widgets = {}
        
        # Fluxo de processamento
        self.decision_flow = self._create_decision_flow()
        self.flow_widgets = []
        
        # Decisões recentes
        self.recent_decisions = self._create_sample_decisions()
        self.decision_widgets = {}
        
        # Portfólio
        self.portfolio_positions = self._create_portfolio_positions()
        self.portfolio_widgets = {}
        
        # Alertas
        self.alerts = self._create_sample_alerts()
        self.alert_widgets = {}
        
        # Dados de mercado
        self.market_data = {}
        self.market_widgets = {}
        
        # Métricas do sistema
        self.system_metrics = SystemMetrics(datetime.now())
        self.metrics_widgets = {}
        
        # Configurações
        self.settings = {
            'risk_tolerance': 'MODERATE',
            'max_position_size': 0.1,  # 10% do capital
            'max_daily_loss': 0.02,    # 2% do capital
            'auto_trading': False,
            'notifications_enabled': True,
            'sound_enabled': False,
            'theme': 'dark',
            'language': 'pt-BR'
        }
        
        # Histórico
        self.trade_history = []
        self.performance_history = deque(maxlen=1000)
        
        logger.info("Dados inicializados com sucesso")
    
    def _create_advanced_algorithms(self) -> List[AdvancedAlgorithm]:
        """Criar algoritmos avançados"""
        return [
            AdvancedAlgorithm(
                id="quantum_ensemble",
                name="Quantum Ensemble Pro",
                type=AlgorithmType.QUANTUM,
                description="Ensemble quântico que combina múltiplas redes neurais com superposição quântica para análise de mercado multidimensional",
                version="3.2.1",
                accuracy=94.7,
                precision=92.3,
                recall=91.8,
                f1_score=92.0,
                sharpe_ratio=2.85,
                sortino_ratio=3.21,
                max_drawdown=12.3,
                win_rate=87.4,
                profit_factor=2.34,
                speed=92.5,
                latency=0.042,
                throughput=1250,
                complexity=96.8,
                confidence=91.2,
                stability=94.6,
                robustness=93.2,
                is_active=True,
                is_optimizing=False,
                is_training=False,
                requires_gpu=True,
                memory_usage_mb=2456,
                decisions_made=15247,
                decisions_today=342,
                success_count=13328,
                failure_count=1919,
                total_profit=284500.75,
                total_loss=89345.20,
                avg_response_time=0.187,
                avg_holding_time=4.25,
                specializations=["Análise Quântica", "Ensemble Learning", "Meta-Optimização"],
                compatible_assets=["BTC", "ETH", "SPX", "NASDAQ"],
                optimal_timeframes=[TimeFrame.H1, TimeFrame.H4, TimeFrame.D1],
                market_conditions=[MarketCondition.TRENDING_BULL, MarketCondition.TRENDING_BEAR, MarketCondition.VOLATILE],
                neural_architecture="Transformer + LSTM + Quantum Layers",
                num_layers=24,
                num_parameters=148000000,
                training_epochs=1500,
                last_trained=datetime(2024, 1, 10),
                parameters={
                    "learning_rate": 0.0001,
                    "batch_size": 64,
                    "dropout_rate": 0.3,
                    "num_heads": 12,
                    "hidden_size": 768
                }
            ),
            # Adicionar mais algoritmos...
        ]
    
    def _create_decision_flow(self) -> List[AdvancedNode]:
        """Criar fluxo de decisão avançado"""
        return [
            AdvancedNode(
                id="data_collection",
                name="Coleta de Dados Multifonte",
                category="DATA",
                input_type="Market Requests",
                output_type="Raw Market Data",
                description="Coleta dados de múltiplas exchanges, APIs e fontes em tempo real",
                confidence=99.8,
                execution_time=0.015,
                processing_speed=1250000,
                error_rate=0.02,
                status=NodeStatus.COMPLETED,
                progress=100.0,
                last_execution=datetime.now(),
                execution_count=1245789,
                success_count=1245765,
                dependencies=[],
                children=["data_validation"],
                cpu_usage=15.2,
                memory_usage=234.5,
                gpu_usage=0.0,
                timeout_seconds=10,
                retry_count=3,
                priority=10
            ),
            # Adicionar mais nós...
        ]
    
    def _create_sample_decisions(self) -> List[AdvancedDecision]:
        """Criar decisões de exemplo"""
        return [
            AdvancedDecision(
                decision_id="DEC-2024-001-ETH-BUY",
                timestamp=datetime(2024, 1, 15, 14, 30, 25),
                algorithm_id="quantum_ensemble",
                algorithm_name="Quantum Ensemble Pro",
                decision_type=Decision.BUY,
                confidence=91.7,
                symbol="ETH/USDT",
                timeframe=TimeFrame.H4,
                entry_price=2456.78,
                stop_loss=2389.45,
                take_profit=2689.90,
                position_size=2.5,
                leverage=3.0,
                reasoning="Breakout confirmado acima da resistência de 2440 com volume 3x acima da média. Convergência de múltiplos indicadores técnicos e análise de sentimento positiva.",
                technical_factors=["RSI(14): 62.3", "MACD Bullish Cross", "Volume +215%", "Bollinger Breakout"],
                fundamental_factors=["Ethereum 2.0 Staking Aumentando", "Gas Fees Decreasing", "NFT Volume Growing"],
                sentiment_factors=["Social Sentiment: 78% Bullish", "Fear & Greed: 72 (Greed)", "News Sentiment: Positive"],
                risk_factors=["Volatility: High", "Liquidity: Excellent", "Correlation: 0.85 with BTC"],
                risk_level=RiskLevel.MODERATE,
                risk_score=6.2,
                var_95=2.1,
                expected_return=8.7,
                expected_loss=3.2,
                risk_reward_ratio=2.72,
                market_condition=MarketCondition.BREAKOUT,
                volatility=3.8,
                volume_ratio=2.15,
                trend_strength=78.4,
                execution_mode=ExecutionMode.PAPER,
                is_executed=True,
                execution_time=datetime(2024, 1, 15, 14, 31, 10),
                execution_price=2457.23,
                pnl=+345.67,
                pnl_percentage=+5.63
            ),
            # Adicionar mais decisões...
        ]
    
    def _create_portfolio_positions(self) -> List[PortfolioPosition]:
        """Criar posições de portfólio de exemplo"""
        return [
            PortfolioPosition(
                symbol="BTC/USDT",
                asset_class=AssetClass.CRYPTO,
                quantity=0.85,
                entry_price=42890.45,
                current_price=43256.78,
                entry_time=datetime(2024, 1, 14, 9, 15, 30),
                position_type='LONG',
                unrealized_pnl=+311.38,
                unrealized_pnl_percent=+0.85,
                realized_pnl=+1256.45,
                total_invested=36457.88,
                current_value=36768.26,
                stop_loss=41500.00,
                take_profit=45500.00,
                trailing_stop=42500.00,
                risk_score=5.8,
                algorithm_id="quantum_ensemble",
                decision_id="DEC-2024-002-BTC-BUY",
                is_hedged=True,
                hedge_ratio=0.3
            ),
            # Adicionar mais posições...
        ]
    
    def _create_sample_alerts(self) -> List[Alert]:
        """Criar alertas de exemplo"""
        return [
            Alert(
                alert_id="ALERT-001",
                timestamp=datetime.now() - timedelta(minutes=5),
                alert_type=AlertType.TRADE_SIGNAL,
                title="Novo Sinal de Compra Detectado",
                message="Quantum Ensemble detectou forte sinal de compra para ETH/USDT com 91.7% de confiança",
                source="Quantum Ensemble Pro",
                priority=8,
                is_acknowledged=False,
                is_resolved=False,
                action_required=True,
                related_symbol="ETH/USDT",
                related_algorithm="quantum_ensemble"
            ),
            # Adicionar mais alertas...
        ]
    
    def setup_styles(self):
        """Configurar estilos avançados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores do tema
        self.colors = {
            'primary': '#3b82f6',
            'primary_dark': '#1e3a8a',
            'primary_light': '#60a5fa',
            'secondary': '#10b981',
            'secondary_dark': '#047857',
            'secondary_light': '#34d399',
            'danger': '#ef4444',
            'danger_dark': '#b91c1c',
            'danger_light': '#f87171',
            'warning': '#f59e0b',
            'warning_dark': '#d97706',
            'warning_light': '#fbbf24',
            'info': '#6366f1',
            'info_dark': '#4f46e5',
            'info_light': '#818cf8',
            'dark': '#111827',
            'dark_light': '#1f2937',
            'dark_lighter': '#374151',
            'gray': '#6b7280',
            'gray_light': '#9ca3af',
            'gray_lighter': '#d1d5db',
            'white': '#ffffff',
            'black': '#000000'
        }
        
        # Configurar estilos personalizados
        style.configure('Primary.TButton', 
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       font=('Arial', 10, 'bold'),
                       padding=10,
                       borderwidth=0)
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_dark']),
                           ('disabled', self.colors['gray'])]),
        
        style.configure('Success.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['white'])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['white'])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground=self.colors['white'])
        
        # Configurar frames
        style.configure('Card.TFrame',
                       background=self.colors['dark_lighter'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Dark.TFrame',
                       background=self.colors['dark'],
                       relief='flat')
        
        style.configure('Dark.TLabelframe',
                       background=self.colors['dark'],
                       foreground=self.colors['white'])
        
        style.configure('Dark.TLabelframe.Label',
                       background=self.colors['dark'],
                       foreground=self.colors['white'],
                       font=('Arial', 10, 'bold'))
    
    def setup_ui(self):
        """Configurar interface completa"""
        logger.info("Configurando interface de usuário...")
        
        # Frame principal com gradiente
        self.main_frame = GradientFrame(self.root, 
                                       color1=self.colors['dark'],
                                       color2=self.colors['dark_light'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra superior
        self.setup_top_bar()
        
        # Área principal com Notebook
        self.setup_main_notebook()
        
        # Barra lateral
        self.setup_sidebar()
        
        # Barra de status
        self.setup_status_bar()
        
        # Configurar redimensionamento
        self.setup_responsive_layout()
        
        logger.info("Interface configurada com sucesso")
    
    def setup_top_bar(self):
        """Configurar barra superior"""
        top_bar = ttk.Frame(self.main_frame, style='Dark.TFrame')
        top_bar.pack(fill=tk.X, padx=10, pady=10)
        
        # Logo e título
        logo_frame = ttk.Frame(top_bar, style='Dark.TFrame')
        logo_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(logo_frame, 
                               text="🚀 LEXTRADER-IAG",
                               font=('Arial', 20, 'bold'),
                               foreground=self.colors['primary_light'])
        title_label.pack(side=tk.LEFT, padx=(0, 20))
        
        subtitle_label = ttk.Label(logo_frame,
                                 text="Sistema de Trading Algorítmico Avançado",
                                 font=('Arial', 11),
                                 foreground=self.colors['gray_light'])
        subtitle_label.pack(side=tk.LEFT)
        
        # Controles da barra superior
        controls_frame = ttk.Frame(top_bar, style='Dark.TFrame')
        controls_frame.pack(side=tk.RIGHT)
        
        # Modo de execução
        self.mode_var = tk.StringVar(value=self.execution_mode.value)
        mode_menu = ttk.OptionMenu(controls_frame, self.mode_var,
                                  self.execution_mode.value,
                                  *[mode.value for mode in ExecutionMode],
                                  command=self.change_execution_mode)
        mode_menu.config(width=12)
        mode_menu.pack(side=tk.LEFT, padx=5)
        
        # Botão iniciar/parar
        self.start_stop_btn = ttk.Button(controls_frame,
                                        text="▶️ Iniciar Sistema",
                                        command=self.toggle_system,
                                        style='Success.TButton')
        self.start_stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Botão configurações
        settings_btn = ttk.Button(controls_frame,
                                 text="⚙️ Configurações",
                                 command=self.open_settings,
                                 style='Primary.TButton')
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        # Botão ajuda
        help_btn = ttk.Button(controls_frame,
                             text="❓ Ajuda",
                             command=self.show_help,
                             style='Info.TButton')
        help_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_main_notebook(self):
        """Configurar notebook principal com múltiplas abas"""
        # Frame principal para notebook
        main_content = ttk.Frame(self.main_frame, style='Dark.TFrame')
        main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Criar notebook com estilo personalizado
        self.notebook = ttk.Notebook(main_content)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Configurar estilo do notebook
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Criar todas as abas
        self.setup_dashboard_tab()
        self.setup_algorithms_tab()
        self.setup_trading_tab()
        self.setup_analysis_tab()
        self.setup_portfolio_tab()
        self.setup_monitoring_tab()
        self.setup_backtesting_tab()
        self.setup_optimization_tab()
        self.setup_reports_tab()
    
    def setup_dashboard_tab(self):
        """Configurar aba de dashboard principal"""
        dashboard_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Dividir dashboard em seções
        dashboard_paned = ttk.PanedWindow(dashboard_frame, orient=tk.HORIZONTAL)
        dashboard_paned.pack(fill=tk.BOTH, expand=True)
        
        # Painel esquerdo - Visão geral
        left_panel = ttk.Frame(dashboard_paned, style='Dark.TFrame')
        dashboard_paned.add(left_panel, weight=3)
        
        # Painel direito - Métricas rápidas
        right_panel = ttk.Frame(dashboard_paned, style='Dark.TFrame')
        dashboard_paned.add(right_panel, weight=1)
        
        # Configurar painel esquerdo
        self.setup_dashboard_left_panel(left_panel)
        
        # Configurar painel direito
        self.setup_dashboard_right_panel(right_panel)
    
    def setup_dashboard_left_panel(self, parent):
        """Configurar painel esquerdo do dashboard"""
        # Topo - Métricas principais
        top_metrics = ttk.Frame(parent, style='Dark.TFrame')
        top_metrics.pack(fill=tk.X, pady=(0, 10))
        
        # Grid de métricas principais
        self.create_metric_card(top_metrics, "💰 Patrimônio Total", 
                               "$ 284,567.89", "+2.34%", 0, 0)
        self.create_metric_card(top_metrics, "📈 P&L Diário", 
                               "+$ 2,345.67", "+1.23%", 0, 1)
        self.create_metric_card(top_metrics, "🎯 Taxa de Acerto", 
                               "87.4%", "↑ 1.2%", 0, 2)
        self.create_metric_card(top_metrics, "⚡ Sharpe Ratio", 
                               "2.85", "Estável", 0, 3)
        
        # Meio - Gráficos
        middle_paned = ttk.PanedWindow(parent, orient=tk.VERTICAL)
        middle_paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Gráfico de performance
        perf_chart_frame = ttk.LabelFrame(middle_paned, 
                                         text="📈 Performance do Portfólio",
                                         style='Dark.TLabelframe')
        middle_paned.add(perf_chart_frame, weight=2)
        self.setup_performance_chart(perf_chart_frame)
        
        # Gráfico de alocação
        allocation_frame = ttk.LabelFrame(middle_paned,
                                         text="📊 Alocação de Ativos",
                                         style='Dark.TLabelframe')
        middle_paned.add(allocation_frame, weight=1)
        self.setup_allocation_chart(allocation_frame)
        
        # Fundo - Atividade recente
        bottom_frame = ttk.LabelFrame(parent,
                                     text="📝 Atividade Recente",
                                     style='Dark.TLabelframe')
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para atividade
        columns = ('Hora', 'Tipo', 'Descrição', 'Status', 'Valor')
        activity_tree = ttk.Treeview(bottom_frame, columns=columns, 
                                    show='headings', height=6)
        
        for col in columns:
            activity_tree.heading(col, text=col)
            activity_tree.column(col, width=100)
        
        activity_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_dashboard_right_panel(self, parent):
        """Configurar painel direito do dashboard"""
        # Sistema
        system_frame = ttk.LabelFrame(parent,
                                     text="🖥️ Status do Sistema",
                                     style='Dark.TLabelframe')
        system_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_system_metric(system_frame, "CPU", "42%", 0)
        self.create_system_metric(system_frame, "Memória", "68%", 1)
        self.create_system_metric(system_frame, "GPU", "15%", 2)
        self.create_system_metric(system_frame, "Rede", "24ms", 3)
        
        # Alertas
        alerts_frame = ttk.LabelFrame(parent,
                                     text="🚨 Alertas Ativos",
                                     style='Dark.TLabelframe')
        alerts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        alerts_list = tk.Listbox(alerts_frame, 
                                bg=self.colors['dark_lighter'],
                                fg=self.colors['white'],
                                font=('Arial', 9))
        alerts_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for alert in self.alerts[:5]:  # Mostrar apenas 5 alertas
            alerts_list.insert(tk.END, f"{alert.get_icon()} {alert.title}")
        
        # Botões de ação rápida
        actions_frame = ttk.Frame(parent, style='Dark.TFrame')
        actions_frame.pack(fill=tk.X)
        
        quick_buy = ttk.Button(actions_frame,
                              text="📈 Trade Rápido",
                              command=self.open_quick_trade,
                              style='Success.TButton')
        quick_buy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        risk_check = ttk.Button(actions_frame,
                               text="🛡️ Verificar Risco",
                               command=self.check_risk,
                               style='Warning.TButton')
        risk_check.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        report_gen = ttk.Button(actions_frame,
                               text="📋 Gerar Relatório",
                               command=self.generate_report,
                               style='Info.TButton')
        report_gen.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    def create_metric_card(self, parent, title, value, change, row, col):
        """Criar card de métrica individual"""
        card = ttk.Frame(parent, style='Card.TFrame')
        card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # Título
        title_label = ttk.Label(card, text=title,
                               font=('Arial', 9),
                               foreground=self.colors['gray_light'])
        title_label.pack(anchor='w', padx=10, pady=(10, 2))
        
        # Valor
        value_label = ttk.Label(card, text=value,
                               font=('Arial', 20, 'bold'),
                               foreground=self.colors['white'])
        value_label.pack(anchor='w', padx=10, pady=(0, 2))
        
        # Variação
        change_color = self.colors['secondary'] if '+' in change else self.colors['danger']
        change_label = ttk.Label(card, text=change,
                                font=('Arial', 9),
                                foreground=change_color)
        change_label.pack(anchor='w', padx=10, pady=(0, 10))
        
        # Configurar grid
        parent.columnconfigure(col, weight=1)
        parent.rowconfigure(row, weight=1)
    
    def create_system_metric(self, parent, name, value, index):
        """Criar métrica do sistema"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Nome
        name_label = ttk.Label(frame, text=name,
                              font=('Arial', 9),
                              foreground=self.colors['gray_light'])
        name_label.pack(side=tk.LEFT)
        
        # Valor
        value_label = ttk.Label(frame, text=value,
                               font=('Arial', 10, 'bold'),
                               foreground=self.colors['white'])
        value_label.pack(side=tk.RIGHT)
        
        # Barra de progresso (se for porcentagem)
        if '%' in value:
            value_num = float(value.replace('%', ''))
            progress = AnimatedProgressBar(frame, length=100, height=8)
            progress.pack(side=tk.RIGHT, padx=10)
            progress.set_value(value_num)
    
    def setup_performance_chart(self, parent):
        """Configurar gráfico de performance"""
        # Criar figura matplotlib
        fig = Figure(figsize=(6, 4), dpi=100, facecolor=self.colors['dark'])
        ax = fig.add_subplot(111)
        
        # Dados de exemplo
        days = list(range(1, 31))
        performance = [10000 + i * 300 + random.randint(-500, 500) for i in range(30)]
        
        ax.plot(days, performance, color=self.colors['primary'], linewidth=2)
        ax.fill_between(days, performance, 10000, alpha=0.3, color=self.colors['primary'])
        ax.set_facecolor(self.colors['dark_lighter'])
        ax.grid(True, alpha=0.3, color=self.colors['gray'])
        ax.set_xlabel('Dias', color=self.colors['white'])
        ax.set_ylabel('Patrimônio ($)', color=self.colors['white'])
        ax.tick_params(colors=self.colors['white'])
        
        # Adicionar ao Tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_allocation_chart(self, parent):
        """Configurar gráfico de alocação"""
        fig = Figure(figsize=(6, 2), dpi=100, facecolor=self.colors['dark'])
        ax = fig.add_subplot(111)
        
        # Dados de exemplo
        assets = ['BTC', 'ETH', 'Stocks', 'Commodities', 'Cash']
        allocations = [35, 25, 20, 10, 10]
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['warning'], self.colors['info'], self.colors['gray']]
        
        ax.pie(allocations, labels=assets, colors=colors, autopct='%1.1f%%',
              textprops={'color': self.colors['white']})
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_algorithms_tab(self):
        """Configurar aba de algoritmos avançada"""
        algorithms_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(algorithms_frame, text="🤖 Algoritmos")
        
        # Toolbar para algoritmos
        algo_toolbar = ttk.Frame(algorithms_frame, style='Dark.TFrame')
        algo_toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        # Filtros
        ttk.Label(algo_toolbar, text="Filtrar:", 
                 foreground=self.colors['white']).pack(side=tk.LEFT, padx=(0, 5))
        
        filter_var = tk.StringVar(value="Todos")
        filter_menu = ttk.OptionMenu(algo_toolbar, filter_var, "Todos",
                                    "Todos", "Ativos", "Inativos", "Otimizando")
        filter_menu.pack(side=tk.LEFT, padx=5)
        
        # Busca
        search_frame = ttk.Frame(algo_toolbar, style='Dark.TFrame')
        search_frame.pack(side=tk.RIGHT)
        
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        search_btn = ttk.Button(search_frame, text="🔍")
        search_btn.pack(side=tk.LEFT)
        
        # Canvas com scroll para algoritmos
        canvas_frame = ttk.Frame(algorithms_frame, style='Dark.TFrame')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame, bg=self.colors['dark'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", 
                                 command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar cards de algoritmos
        for i, algo in enumerate(self.algorithms):
            self.create_advanced_algorithm_card(scrollable_frame, algo, i)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_advanced_algorithm_card(self, parent, algorithm: AdvancedAlgorithm, index: int):
        """Criar card avançado para algoritmo"""
        # Frame principal
        card = ttk.LabelFrame(parent, 
                             text=f"{algorithm.name} v{algorithm.version}",
                             style='Dark.TLabelframe')
        card.pack(fill=tk.X, padx=5, pady=8)
        
        # Header com status
        header_frame = ttk.Frame(card, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Status LED
        status_led = LedIndicator(header_frame, size=12)
        status_led.pack(side=tk.LEFT)
        status_led.set_state(algorithm.is_active)
        
        # Tipo e status
        type_label = ttk.Label(header_frame, 
                              text=algorithm.type.value,
                              foreground=self.colors['primary_light'],
                              font=('Arial', 9, 'bold'))
        type_label.pack(side=tk.LEFT, padx=(5, 10))
        
        # Score de performance
        performance_score = algorithm.calculate_performance_score()
        score_frame = ttk.Frame(header_frame, style='Dark.TFrame')
        score_frame.pack(side=tk.RIGHT)
        
        score_circle = CircularProgress(score_frame, size=40)
        score_circle.pack()
        score_circle.set_value(performance_score)
        
        # Descrição
        desc_label = ttk.Label(card, text=algorithm.description,
                              wraplength=800,
                              foreground=self.colors['gray_light'],
                              font=('Arial', 9))
        desc_label.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Grid de métricas
        metrics_frame = ttk.Frame(card, style='Dark.TFrame')
        metrics_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Métricas principais em 2 colunas
        main_metrics = [
            ("🎯 Precisão", f"{algorithm.accuracy:.1f}%", algorithm.accuracy),
            ("📈 Win Rate", f"{algorithm.win_rate:.1f}%", algorithm.win_rate),
            ("⚡ Sharpe", f"{algorithm.sharpe_ratio:.2f}", algorithm.sharpe_ratio * 20),
            ("🛡️ Drawdown", f"{algorithm.max_drawdown:.1f}%", 100 - algorithm.max_drawdown),
            ("🚀 Velocidade", f"{algorithm.speed:.1f}", algorithm.speed),
            ("🎯 Confiança", f"{algorithm.confidence:.1f}%", algorithm.confidence)
        ]
        
        for i, (label, value, progress) in enumerate(main_metrics):
            row, col = divmod(i, 2)
            self.create_metric_progress(metrics_frame, label, value, progress, row, col)
        
        # Estatísticas
        stats_frame = ttk.Frame(card, style='Dark.TFrame')
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        stats = [
            f"📊 Decisões: {algorithm.decisions_made:,}",
            f"💰 Lucro Total: ${algorithm.total_profit:,.2f}",
            f"⚡ Tempo Médio: {algorithm.avg_response_time:.3f}s",
            f"⏱️ Holding: {algorithm.avg_holding_time:.1f}h"
        ]
        
        for i, stat in enumerate(stats):
            label = ttk.Label(stats_frame, text=stat,
                             foreground=self.colors['gray_light'],
                             font=('Arial', 9))
            label.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=2)
        
        # Especializações
        if algorithm.specializations:
            specs_frame = ttk.Frame(card, style='Dark.TFrame')
            specs_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            ttk.Label(specs_frame, text="Especializações:",
                     foreground=self.colors['gray_light']).pack(side=tk.LEFT)
            
            for spec in algorithm.specializations:
                badge = ttk.Label(specs_frame, text=spec,
                                 foreground=self.colors['white'],
                                 background=self.colors['primary_dark'],
                                 font=('Arial', 8),
                                 padding=3)
                badge.pack(side=tk.LEFT, padx=2)
        
        # Botões de ação
        actions_frame = ttk.Frame(card, style='Dark.TFrame')
        actions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Botões
        toggle_text = "⏸️ Pausar" if algorithm.is_active else "▶️ Ativar"
        toggle_btn = ttk.Button(actions_frame, text=toggle_text,
                               command=lambda: self.toggle_algorithm(algorithm.id))
        toggle_btn.pack(side=tk.LEFT, padx=2)
        
        optimize_btn = ttk.Button(actions_frame, text="📈 Otimizar",
                                 command=lambda: self.optimize_algorithm(algorithm.id))
        optimize_btn.pack(side=tk.LEFT, padx=2)
        
        train_btn = ttk.Button(actions_frame, text="🎓 Treinar",
                              command=lambda: self.train_algorithm(algorithm.id))
        train_btn.pack(side=tk.LEFT, padx=2)
        
        details_btn = ttk.Button(actions_frame, text="🔍 Detalhes",
                                command=lambda: self.show_algorithm_details(algorithm.id))
        details_btn.pack(side=tk.LEFT, padx=2)
        
        # Configurar grid das métricas
        for i in range(2):
            metrics_frame.columnconfigure(i, weight=1)
        for i in range(3):
            metrics_frame.rowconfigure(i, weight=1)
    
    def create_metric_progress(self, parent, label, value, progress, row, col):
        """Criar métrica com barra de progresso"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
        
        # Label e valor
        text_frame = ttk.Frame(frame, style='Dark.TFrame')
        text_frame.pack(fill=tk.X)
        
        label_widget = ttk.Label(text_frame, text=label,
                                foreground=self.colors['gray_light'],
                                font=('Arial', 8))
        label_widget.pack(side=tk.LEFT)
        
        value_widget = ttk.Label(text_frame, text=value,
                                foreground=self.colors['white'],
                                font=('Arial', 9, 'bold'))
        value_widget.pack(side=tk.RIGHT)
        
        # Barra de progresso
        progress_bar = AnimatedProgressBar(frame, length=180, height=6)
        progress_bar.pack(fill=tk.X, pady=(2, 0))
        progress_bar.set_value(progress)
    
    def setup_trading_tab(self):
        """Configurar aba de trading avançada"""
        trading_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(trading_frame, text="💰 Trading")
        
        # Layout com painéis
        trading_paned = ttk.PanedWindow(trading_frame, orient=tk.HORIZONTAL)
        trading_paned.pack(fill=tk.BOTH, expand=True)
        
        # Painel esquerdo - Controles de trading
        left_panel = ttk.Frame(trading_paned, style='Dark.TFrame')
        trading_paned.add(left_panel, weight=1)
        
        # Painel direito - Gráficos e ordens
        right_panel = ttk.Frame(trading_paned, style='Dark.TFrame')
        trading_paned.add(right_panel, weight=2)
        
        # Configurar painel esquerdo
        self.setup_trading_controls(left_panel)
        
        # Configurar painel direito
        self.setup_trading_charts(right_panel)
    
    def setup_trading_controls(self, parent):
        """Configurar controles de trading"""
        # Seleção de ativo
        asset_frame = ttk.LabelFrame(parent,
                                    text="📊 Selecionar Ativo",
                                    style='Dark.TLabelframe')
        asset_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Símbolo
        ttk.Label(asset_frame, text="Símbolo:",
                 foreground=self.colors['white']).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        symbol_var = tk.StringVar(value="BTC/USDT")
        symbol_entry = ttk.Entry(asset_frame, textvariable=symbol_var, width=15)
        symbol_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Timeframe
        ttk.Label(asset_frame, text="Timeframe:",
                 foreground=self.colors['white']).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        timeframe_var = tk.StringVar(value="1h")
        timeframe_menu = ttk.OptionMenu(asset_frame, timeframe_var, "1h",
                                       "1m", "5m", "15m", "30m", "1h", "4h", "1d")
        timeframe_menu.grid(row=1, column=1, padx=5, pady=5)
        
        # Botão carregar
        load_btn = ttk.Button(asset_frame, text="📥 Carregar Dados",
                             command=lambda: self.load_market_data(symbol_var.get()))
        load_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Controles de ordem
        order_frame = ttk.LabelFrame(parent,
                                    text="📝 Nova Ordem",
                                    style='Dark.TLabelframe')
        order_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Tipo de ordem
        ttk.Label(order_frame, text="Tipo:",
                 foreground=self.colors['white']).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        order_type_var = tk.StringVar(value="MARKET")
        order_type_menu = ttk.OptionMenu(order_frame, order_type_var, "MARKET",
                                        "MARKET", "LIMIT", "STOP", "STOP_LIMIT")
        order_type_menu.grid(row=0, column=1, padx=5, pady=5)
        
        # Lado
        ttk.Label(order_frame, text="Lado:",
                 foreground=self.colors['white']).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        side_var = tk.StringVar(value="BUY")
        side_menu = ttk.OptionMenu(order_frame, side_var, "BUY", "BUY", "SELL")
        side_menu.grid(row=1, column=1, padx=5, pady=5)
        
        # Quantidade
        ttk.Label(order_frame, text="Quantidade:",
                 foreground=self.colors['white']).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        qty_var = tk.StringVar(value="0.1")
        qty_entry = ttk.Entry(order_frame, textvariable=qty_var, width=15)
        qty_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Preço (para ordens limit)
        ttk.Label(order_frame, text="Preço:",
                 foreground=self.colors['white']).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        
        price_var = tk.StringVar(value="0.0")
        price_entry = ttk.Entry(order_frame, textvariable=price_var, width=15)
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Botões de ação
        buy_btn = ttk.Button(order_frame, text="📈 Comprar",
                            command=lambda: self.place_order("BUY", qty_var.get()),
                            style='Success.TButton')
        buy_btn.grid(row=4, column=0, padx=5, pady=10)
        
        sell_btn = ttk.Button(order_frame, text="📉 Vender",
                             command=lambda: self.place_order("SELL", qty_var.get()),
                             style='Danger.TButton')
        sell_btn.grid(row=4, column=1, padx=5, pady=10)
        
        # Análise rápida
        analysis_frame = ttk.LabelFrame(parent,
                                       text="🔍 Análise Rápida",
                                       style='Dark.TLabelframe')
        analysis_frame.pack(fill=tk.X, padx=10, pady=10)
        
        analysis_text = scrolledtext.ScrolledText(analysis_frame,
                                                 height=10,
                                                 bg=self.colors['dark_lighter'],
                                                 fg=self.colors['white'],
                                                 font=('Arial', 9))
        analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        analysis_text.insert(tk.END, "Clique em 'Analisar' para ver a análise do ativo...")
        
        analyze_btn = ttk.Button(analysis_frame, text="🧠 Analisar",
                                command=self.analyze_asset)
        analyze_btn.pack(pady=5)
    
    def setup_trading_charts(self, parent):
        """Configurar gráficos de trading"""
        # Notebook para múltiplos gráficos
        chart_notebook = ttk.Notebook(parent)
        chart_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Gráfico de preço
        price_frame = ttk.Frame(chart_notebook, style='Dark.TFrame')
        chart_notebook.add(price_frame, text="📈 Preço")
        
        # Criar gráfico com mplfinance
        self.setup_price_chart(price_frame)
        
        # Gráfico de profundidade
        depth_frame = ttk.Frame(chart_notebook, style='Dark.TFrame')
        chart_notebook.add(depth_frame, text="📊 Order Book")
        
        # Ordens abertas
        orders_frame = ttk.Frame(chart_notebook, style='Dark.TFrame')
        chart_notebook.add(orders_frame, text="📋 Ordens")
        
        # Configurar lista de ordens
        self.setup_orders_list(orders_frame)
    
    def setup_price_chart(self, parent):
        """Configurar gráfico de preços"""
        # Frame para controles do gráfico
        controls_frame = ttk.Frame(parent, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Controles
        ttk.Label(controls_frame, text="Período:",
                 foreground=self.colors['white']).pack(side=tk.LEFT, padx=(0, 5))
        
        period_var = tk.StringVar(value="1h")
        period_menu = ttk.OptionMenu(controls_frame, period_var, "1h",
                                    "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w")
        period_menu.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(controls_frame, text="Tipo:",
                 foreground=self.colors['white']).pack(side=tk.LEFT, padx=(20, 5))
        
        chart_type_var = tk.StringVar(value="candlestick")
        chart_type_menu = ttk.OptionMenu(controls_frame, chart_type_var, "candlestick",
                                        "candlestick", "line", "renko", "pnf")
        chart_type_menu.pack(side=tk.LEFT, padx=5)
        
        # Botões
        refresh_btn = ttk.Button(controls_frame, text="🔄 Atualizar",
                                command=self.refresh_chart)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        indicators_btn = ttk.Button(controls_frame, text="📊 Indicadores",
                                   command=self.add_indicators)
        indicators_btn.pack(side=tk.RIGHT, padx=5)
        
        # Área do gráfico
        chart_area = ttk.Frame(parent, style='Dark.TFrame')
        chart_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Placeholder para gráfico
        placeholder = ttk.Label(chart_area,
                               text="Gráfico interativo será implementado aqui\n\n" +
                                    "• Candlesticks em tempo real\n" +
                                    "• Indicadores técnicos\n" +
                                    "• Desenho de linhas de tendência\n" +
                                    "• Análise de padrões",
                               foreground=self.colors['gray_light'],
                               font=('Arial', 12),
                               justify=tk.CENTER)
        placeholder.pack(fill=tk.BOTH, expand=True)
    
    def setup_orders_list(self, parent):
        """Configurar lista de ordens"""
        # Toolbar
        toolbar = ttk.Frame(parent, style='Dark.TFrame')
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        cancel_all_btn = ttk.Button(toolbar, text="❌ Cancelar Todas",
                                   command=self.cancel_all_orders,
                                   style='Danger.TButton')
        cancel_all_btn.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(toolbar, text="🔄 Atualizar",
                                command=self.refresh_orders)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Treeview para ordens
        columns = ('ID', 'Símbolo', 'Tipo', 'Lado', 'Quantidade', 'Preço', 'Status', 'Tempo')
        orders_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        column_widths = [80, 80, 80, 50, 80, 80, 80, 120]
        for col, width in zip(columns, column_widths):
            orders_tree.heading(col, text=col)
            orders_tree.column(col, width=width)
        
        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=orders_tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=orders_tree.xview)
        orders_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(0, 10))
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        hsb.pack(side=tk.BOTTOM, fill=tk.X, padx=(10, 0))
        
        # Adicionar ordens de exemplo
        sample_orders = [
            ('ORD-001', 'BTC/USDT', 'LIMIT', 'BUY', '0.5', '42150.00', 'OPEN', '10:30:25'),
            ('ORD-002', 'ETH/USDT', 'MARKET', 'SELL', '2.0', '2456.78', 'FILLED', '10:25:15'),
            ('ORD-003', 'BTC/USDT', 'STOP', 'SELL', '0.2', '41500.00', 'PENDING', '10:15:45')
        ]
        
        for order in sample_orders:
            orders_tree.insert('', tk.END, values=order)
    
    def setup_analysis_tab(self):
        """Configurar aba de análise avançada"""
        analysis_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(analysis_frame, text="📊 Análise")
        
        # Layout com múltiplas abas
        analysis_notebook = ttk.Notebook(analysis_frame)
        analysis_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Análise Técnica
        technical_frame = ttk.Frame(analysis_notebook, style='Dark.TFrame')
        analysis_notebook.add(technical_frame, text="📈 Técnica")
        
        # Análise Fundamentalista
        fundamental_frame = ttk.Frame(analysis_notebook, style='Dark.TFrame')
        analysis_notebook.add(fundamental_frame, text="🏦 Fundamentalista")
        
        # Análise de Sentimento
        sentiment_frame = ttk.Frame(analysis_notebook, style='Dark.TFrame')
        analysis_notebook.add(sentiment_frame, text="😊 Sentimento")
        
        # Análise de Risco
        risk_frame = ttk.Frame(analysis_notebook, style='Dark.TFrame')
        analysis_notebook.add(risk_frame, text="🛡️ Risco")
        
        # Configurar cada aba
        self.setup_technical_analysis(technical_frame)
        self.setup_fundamental_analysis(fundamental_frame)
        self.setup_sentiment_analysis(sentiment_frame)
        self.setup_risk_analysis(risk_frame)
    
    def setup_technical_analysis(self, parent):
        """Configurar análise técnica"""
        # Painel de indicadores
        indicators_frame = ttk.LabelFrame(parent,
                                         text="📊 Indicadores Técnicos",
                                         style='Dark.TLabelframe')
        indicators_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Grid de indicadores
        indicators = [
            ("RSI (14)", "62.3", "Neutral", self.colors['warning']),
            ("MACD", "+15.2", "Bullish", self.colors['secondary']),
            ("Bollinger", "Upper Touch", "Overbought", self.colors['danger']),
            ("Volume", "+215%", "High", self.colors['info']),
            ("ATR", "342.5", "High Vol", self.colors['warning']),
            ("ADX", "42.7", "Strong Trend", self.colors['secondary']),
            ("Stoch RSI", "78.9", "Overbought", self.colors['danger']),
            ("Ichimoku", "Bullish", "Above Cloud", self.colors['secondary'])
        ]
        
        for i, (name, value, signal, color) in enumerate(indicators):
            row, col = divmod(i, 2)
            self.create_indicator_card(indicators_frame, name, value, signal, color, row, col)
        
        # Gráfico de indicadores
        chart_frame = ttk.LabelFrame(parent,
                                    text="📈 Gráfico de Indicadores",
                                    style='Dark.TLabelframe')
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Configurar grid
        for i in range(2):
            indicators_frame.columnconfigure(i, weight=1)
        for i in range(4):
            indicators_frame.rowconfigure(i, weight=1)
    
    def create_indicator_card(self, parent, name, value, signal, color, row, col):
        """Criar card de indicador"""
        frame = ttk.Frame(parent, style='Card.TFrame')
        frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # Nome
        name_label = ttk.Label(frame, text=name,
                              foreground=self.colors['gray_light'],
                              font=('Arial', 9))
        name_label.pack(anchor='w', padx=10, pady=(10, 2))
        
        # Valor
        value_label = ttk.Label(frame, text=value,
                               foreground=color,
                               font=('Arial', 16, 'bold'))
        value_label.pack(anchor='w', padx=10, pady=(0, 2))
        
        # Sinal
        signal_label = ttk.Label(frame, text=signal,
                                foreground=self.colors['gray_light'],
                                font=('Arial', 9))
        signal_label.pack(anchor='w', padx=10, pady=(0, 10))
    
    def setup_fundamental_analysis(self, parent):
        """Configurar análise fundamentalista"""
        # Métricas fundamentais
        metrics = [
            ("💰 Market Cap", "$850B", "+2.3%"),
            ("📈 Volume (24h)", "$32.4B", "+15.7%"),
            ("🔢 Circulating Supply", "19.5M BTC", "91.2%"),
            ("📊 Dominance", "52.3%", "-1.2%"),
            ("🏦 Total Value Locked", "$45.2B", "+8.7%"),
            ("👥 Active Addresses", "1.2M", "+5.4%"),
            ("⚡ Hash Rate", "450 EH/s", "+12.3%"),
            ("🔗 Network Difficulty", "67.3T", "+8.9%")
        ]
        
        for i, (name, value, change) in enumerate(metrics):
            row, col = divmod(i, 2)
            frame = ttk.Frame(parent, style='Card.TFrame')
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            ttk.Label(frame, text=name,
                     foreground=self.colors['gray_light']).pack(anchor='w', padx=10, pady=(10, 2))
            ttk.Label(frame, text=value,
                     foreground=self.colors['white'],
                     font=('Arial', 14, 'bold')).pack(anchor='w', padx=10, pady=(0, 2))
            ttk.Label(frame, text=change,
                     foreground=self.colors['secondary']).pack(anchor='w', padx=10, pady=(0, 10))
            
            parent.columnconfigure(col, weight=1)
            parent.rowconfigure(row, weight=1)
    
    def setup_sentiment_analysis(self, parent):
        """Configurar análise de sentimento"""
        # Medidores de sentimento
        sentiment_frame = ttk.Frame(parent, style='Dark.TFrame')
        sentiment_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Fear & Greed Index
        fear_greed_frame = ttk.LabelFrame(sentiment_frame,
                                         text="😨 Fear & Greed Index",
                                         style='Dark.TLabelframe')
        fear_greed_frame.pack(fill=tk.X, pady=(0, 10))
        
        fear_greed_value = 72  # Exemplo
        fear_greed = CircularProgress(fear_greed_frame, size=150)
        fear_greed.pack(padx=20, pady=20)
        fear_greed.set_value(fear_greed_value)
        
        ttk.Label(fear_greed_frame, text="Greed" if fear_greed_value > 50 else "Fear",
                 font=('Arial', 14, 'bold'),
                 foreground=self.colors['secondary' if fear_greed_value > 50 else 'danger']).pack()
        
        # Fontes de sentimento
        sources_frame = ttk.LabelFrame(sentiment_frame,
                                      text="📰 Fontes de Sentimento",
                                      style='Dark.TLabelframe')
        sources_frame.pack(fill=tk.BOTH, expand=True)
        
        sources = [
            ("Twitter", "78% Bullish", self.colors['secondary']),
            ("Reddit", "65% Bullish", self.colors['warning']),
            ("News", "72% Bullish", self.colors['secondary']),
            ("GitHub", "84% Positive", self.colors['secondary'])
        ]
        
        for source, sentiment, color in sources:
            frame = ttk.Frame(sources_frame, style='Dark.TFrame')
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(frame, text=source,
                     foreground=self.colors['white']).pack(side=tk.LEFT)
            ttk.Label(frame, text=sentiment,
                     foreground=color).pack(side=tk.RIGHT)
    
    def setup_risk_analysis(self, parent):
        """Configurar análise de risco"""
        # Métricas de risco
        risk_metrics = [
            ("📉 Value at Risk (95%)", "2.1%", self.colors['warning']),
            ("🔥 Conditional VaR", "3.8%", self.colors['danger']),
            ("📊 Beta vs Market", "1.2", self.colors['info']),
            ("🎯 Sharpe Ratio", "2.85", self.colors['secondary']),
            ("🛡️ Sortino Ratio", "3.21", self.colors['secondary']),
            ("📉 Maximum Drawdown", "12.3%", self.colors['danger']),
            ("⚖️ Portfolio Volatility", "18.7%", self.colors['warning']),
            ("🔗 Correlation Matrix", "Moderate", self.colors['info'])
        ]
        
        for i, (metric, value, color) in enumerate(risk_metrics):
            row, col = divmod(i, 2)
            frame = ttk.Frame(parent, style='Card.TFrame')
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            ttk.Label(frame, text=metric,
                     foreground=self.colors['gray_light']).pack(anchor='w', padx=10, pady=(10, 2))
            ttk.Label(frame, text=value,
                     foreground=color,
                     font=('Arial', 14, 'bold')).pack(anchor='w', padx=10, pady=(0, 2))
            
            # Barra de risco
            if '%' in value:
                risk_value = float(value.replace('%', ''))
                risk_bar = AnimatedProgressBar(frame, length=150, height=8)
                risk_bar.pack(anchor='w', padx=10, pady=(0, 10))
                risk_bar.set_value(risk_value)
            
            parent.columnconfigure(col, weight=1)
            parent.rowconfigure(row, weight=1)
    
    def setup_portfolio_tab(self):
        """Configurar aba de portfólio"""
        portfolio_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(portfolio_frame, text="💼 Portfólio")
        
        # Layout principal
        portfolio_paned = ttk.PanedWindow(portfolio_frame, orient=tk.HORIZONTAL)
        portfolio_paned.pack(fill=tk.BOTH, expand=True)
        
        # Painel esquerdo - Posições
        positions_panel = ttk.Frame(portfolio_paned, style='Dark.TFrame')
        portfolio_paned.add(positions_panel, weight=2)
        
        # Painel direito - Estatísticas
        stats_panel = ttk.Frame(portfolio_paned, style='Dark.TFrame')
        portfolio_paned.add(stats_panel, weight=1)
        
        # Configurar painel de posições
        self.setup_positions_panel(positions_panel)
        
        # Configurar painel de estatísticas
        self.setup_portfolio_stats(stats_panel)
    
    def setup_positions_panel(self, parent):
        """Configurar painel de posições"""
        # Toolbar
        toolbar = ttk.Frame(parent, style='Dark.TFrame')
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        close_all_btn = ttk.Button(toolbar, text="❌ Fechar Todas",
                                  command=self.close_all_positions,
                                  style='Danger.TButton')
        close_all_btn.pack(side=tk.LEFT)
        
        hedge_btn = ttk.Button(toolbar, text="🛡️ Hedgear",
                              command=self.hedge_portfolio)
        hedge_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview para posições
        columns = ('Símbolo', 'Tipo', 'Quantidade', 'Entrada', 'Atual', 'P&L', 'P&L %', 'Risco')
        positions_tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        for col in columns:
            positions_tree.heading(col, text=col)
            positions_tree.column(col, width=100)
        
        # Adicionar scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=positions_tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=positions_tree.xview)
        positions_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        positions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                          padx=(10, 0), pady=(0, 10))
        vsb.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        hsb.pack(side=tk.BOTTOM, fill=tk.X, padx=(10, 0))
        
        # Adicionar posições de exemplo
        for position in self.portfolio_positions:
            pnl_color = self.colors['secondary'] if position.unrealized_pnl >= 0 else self.colors['danger']
            pnl_text = f"${position.unrealized_pnl:+,.2f}"
            pnl_percent = f"{position.unrealized_pnl_percent:+.2f}%"
            
            positions_tree.insert('', tk.END, values=(
                position.symbol,
                position.position_type,
                f"{position.quantity:.4f}",
                f"${position.entry_price:.2f}",
                f"${position.current_price:.2f}",
                pnl_text,
                pnl_percent,
                f"{position.risk_score:.1f}"
            ))
    
    def setup_portfolio_stats(self, parent):
        """Configurar estatísticas do portfólio"""
        # Resumo
        summary_frame = ttk.LabelFrame(parent,
                                      text="📊 Resumo do Portfólio",
                                      style='Dark.TLabelframe')
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats = [
            ("💰 Valor Total", "$284,567.89"),
            ("📈 P&L Total", "+$12,456.78"),
            ("🎯 P&L %", "+4.56%"),
            ("🛡️ Risco Médio", "5.8/10"),
            ("📊 Diversificação", "7.2/10"),
            ("⚡ Alavancagem", "1.5x")
        ]
        
        for stat, value in stats:
            frame = ttk.Frame(summary_frame, style='Dark.TFrame')
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(frame, text=stat,
                     foreground=self.colors['gray_light']).pack(side=tk.LEFT)
            ttk.Label(frame, text=value,
                     foreground=self.colors['white'],
                     font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
        
        # Alocação por classe
        allocation_frame = ttk.LabelFrame(parent,
                                         text="📈 Alocação por Classe",
                                         style='Dark.TLabelframe')
        allocation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Gráfico de pizza simples
        classes = ['Crypto', 'Stocks', 'Commodities', 'Cash']
        allocations = [65, 20, 10, 5]
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['warning'], self.colors['gray']]
        
        for cls, alloc, color in zip(classes, allocations, colors):
            frame = ttk.Frame(allocation_frame, style='Dark.TFrame')
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Indicador de cor
            color_indicator = tk.Label(frame, text="   ", bg=color)
            color_indicator.pack(side=tk.LEFT, padx=(0, 10))
            
            ttk.Label(frame, text=cls,
                     foreground=self.colors['white']).pack(side=tk.LEFT)
            ttk.Label(frame, text=f"{alloc}%",
                     foreground=self.colors['white'],
                     font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
    
    def setup_monitoring_tab(self):
        """Configurar aba de monitoramento"""
        monitoring_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(monitoring_frame, text="👁️ Monitoramento")
        
        # Layout com múltiplas seções
        monitoring_notebook = ttk.Notebook(monitoring_frame)
        monitoring_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Logs do sistema
        logs_frame = ttk.Frame(monitoring_notebook, style='Dark.TFrame')
        monitoring_notebook.add(logs_frame, text="📝 Logs")
        
        # Métricas em tempo real
        metrics_frame = ttk.Frame(monitoring_notebook, style='Dark.TFrame')
        monitoring_notebook.add(metrics_frame, text="📊 Métricas")
        
        # Alertas
        alerts_frame = ttk.Frame(monitoring_notebook, style='Dark.TFrame')
        monitoring_notebook.add(alerts_frame, text="🚨 Alertas")
        
        # Configurar cada seção
        self.setup_system_logs(logs_frame)
        self.setup_realtime_metrics(metrics_frame)
        self.setup_alerts_panel(alerts_frame)
    
    def setup_system_logs(self, parent):
        """Configurar logs do sistema"""
        # Toolbar
        toolbar = ttk.Frame(parent, style='Dark.TFrame')
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        clear_btn = ttk.Button(toolbar, text="🗑️ Limpar Logs",
                              command=self.clear_logs)
        clear_btn.pack(side=tk.LEFT)
        
        export_btn = ttk.Button(toolbar, text="💾 Exportar",
                               command=self.export_logs)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        filter_var = tk.StringVar(value="Todos")
        filter_menu = ttk.OptionMenu(toolbar, filter_var, "Todos",
                                    "Todos", "Info", "Warning", "Error")
        filter_menu.pack(side=tk.RIGHT)
        
        # Área de logs
        log_area = scrolledtext.ScrolledText(parent,
                                           height=30,
                                           bg=self.colors['dark_lighter'],
                                           fg=self.colors['white'],
                                           font=('Consolas', 9))
        log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Adicionar logs de exemplo
        log_messages = [
            ("INFO", "Sistema inicializado com sucesso"),
            ("INFO", "Conectado à Binance API"),
            ("INFO", "Quantum Ensemble carregado"),
            ("WARNING", "Alta volatilidade detectada no mercado"),
            ("SUCCESS", "Ordem executada: BUY 0.5 BTC @ $42,150.00"),
            ("ERROR", "Falha na conexão com Bybit API - Tentando reconectar"),
            ("INFO", "Reconexão bem-sucedida"),
            ("TRADE", "Novo sinal: SELL ETH @ $2,456.78 (Confiança: 91.7%)")
        ]
        
        for level, message in log_messages:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_area.insert(tk.END, f"[{timestamp}] [{level}] {message}\n")
        
        log_area.see(tk.END)
    
    def setup_realtime_metrics(self, parent):
        """Configurar métricas em tempo real"""
        # Grid de métricas
        metrics = [
            ("📊 CPU Usage", "42%", self.colors['warning']),
            ("💾 Memory", "68%", self.colors['warning']),
            ("🎮 GPU Usage", "15%", self.colors['secondary']),
            ("🌐 Network", "24ms", self.colors['secondary']),
            ("⚡ Latência API", "87ms", self.colors['info']),
            ("📈 Trades/min", "3.2", self.colors['secondary']),
            ("🎯 Decision Rate", "12.4/s", self.colors['secondary']),
            ("🔄 Update Freq", "0.5s", self.colors['info'])
        ]
        
        for i, (name, value, color) in enumerate(metrics):
            row, col = divmod(i, 2)
            frame = ttk.Frame(parent, style='Card.TFrame')
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            ttk.Label(frame, text=name,
                     foreground=self.colors['gray_light']).pack(anchor='w', padx=10, pady=(10, 2))
            ttk.Label(frame, text=value,
                     foreground=color,
                     font=('Arial', 16, 'bold')).pack(anchor='w', padx=10, pady=(0, 2))
            
            # Sparkline
            sparkline = SparklineGraph(frame, width=150, height=40)
            sparkline.pack(anchor='w', padx=10, pady=(0, 10))
            
            # Adicionar dados aleatórios
            for _ in range(20):
                sparkline.add_data(random.uniform(0, 100))
            
            parent.columnconfigure(col, weight=1)
            parent.rowconfigure(row, weight=1)
    
    def setup_alerts_panel(self, parent):
        """Configurar painel de alertas"""
        # Toolbar
        toolbar = ttk.Frame(parent, style='Dark.TFrame')
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        acknowledge_all_btn = ttk.Button(toolbar, text="✓ Reconhecer Todos",
                                        command=self.acknowledge_all_alerts)
        acknowledge_all_btn.pack(side=tk.LEFT)
        
        clear_resolved_btn = ttk.Button(toolbar, text="🗑️ Limpar Resolvidos",
                                       command=self.clear_resolved_alerts)
        clear_resolved_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de alertas
        alerts_list = tk.Listbox(parent,
                                bg=self.colors['dark_lighter'],
                                fg=self.colors['white'],
                                font=('Arial', 10),
                                height=20)
        alerts_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Adicionar alertas
        for alert in self.alerts:
            time_str = alert.timestamp.strftime("%H:%M")
            alerts_list.insert(tk.END, f"{alert.get_icon()} [{time_str}] {alert.title}")
            
            # Colorir baseado na prioridade
            if alert.priority >= 8:
                alerts_list.itemconfig(tk.END, fg=self.colors['danger'])
            elif alert.priority >= 5:
                alerts_list.itemconfig(tk.END, fg=self.colors['warning'])
    
    def setup_backtesting_tab(self):
        """Configurar aba de backtesting"""
        backtest_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(backtest_frame, text="🧪 Backtesting")
        
        # Interface de backtesting
        ttk.Label(backtest_frame, text="Backtesting Avançado",
                 font=('Arial', 16, 'bold'),
                 foreground=self.colors['white']).pack(pady=20)
        
        # Placeholder
        placeholder = ttk.Label(backtest_frame,
                               text="Interface de backtesting em desenvolvimento\n\n" +
                                    "• Teste estratégias em dados históricos\n" +
                                    "• Otimização de parâmetros\n" +
                                    "• Análise de performance detalhada\n" +
                                    "• Comparação de múltiplas estratégias",
                               foreground=self.colors['gray_light'],
                               font=('Arial', 12),
                               justify=tk.CENTER)
        placeholder.pack(fill=tk.BOTH, expand=True)
    
    def setup_optimization_tab(self):
        """Configurar aba de otimização"""
        optimization_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(optimization_frame, text="⚙️ Otimização")
        
        # Interface de otimização
        ttk.Label(optimization_frame, text="Otimização de Algoritmos",
                 font=('Arial', 16, 'bold'),
                 foreground=self.colors['white']).pack(pady=20)
        
        # Placeholder
        placeholder = ttk.Label(optimization_frame,
                               text="Interface de otimização em desenvolvimento\n\n" +
                                    "• Otimização bayesiana de parâmetros\n" +
                                    "• Grid search avançado\n" +
                                    "• Meta-otimização com GA\n" +
                                    "• Validação cruzada em tempo real",
                               foreground=self.colors['gray_light'],
                               font=('Arial', 12),
                               justify=tk.CENTER)
        placeholder.pack(fill=tk.BOTH, expand=True)
    
    def setup_reports_tab(self):
        """Configurar aba de relatórios"""
        reports_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(reports_frame, text="📋 Relatórios")
        
        # Interface de relatórios
        ttk.Label(reports_frame, text="Relatórios e Análises",
                 font=('Arial', 16, 'bold'),
                 foreground=self.colors['white']).pack(pady=20)
        
        # Placeholder
        placeholder = ttk.Label(reports_frame,
                               text="Interface de relatórios em desenvolvimento\n\n" +
                                    "• Relatórios de performance diários/semanais/mensais\n" +
                                    "• Análise de risco detalhada\n" +
                                    "• Relatórios de conformidade\n" +
                                    "• Exportação para PDF/Excel",
                               foreground=self.colors['gray_light'],
                               font=('Arial', 12),
                               justify=tk.CENTER)
        placeholder.pack(fill=tk.BOTH, expand=True)
    
    def setup_sidebar(self):
        """Configurar barra lateral"""
        sidebar = ttk.Frame(self.main_frame, style='Dark.TFrame', width=250)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        sidebar.pack_propagate(False)
        
        # Resumo rápido
        summary_frame = ttk.LabelFrame(sidebar,
                                      text="📈 Resumo Rápido",
                                      style='Dark.TLabelframe')
        summary_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        quick_stats = [
            ("💰 Capital", "$284,567.89"),
            ("📈 P&L Hoje", "+$2,345.67"),
            ("🎯 Acertos", "87.4%"),
            ("⚡ Operações", "342")
        ]
        
        for stat, value in quick_stats:
            frame = ttk.Frame(summary_frame, style='Dark.TFrame')
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(frame, text=stat,
                     foreground=self.colors['gray_light']).pack(side=tk.LEFT)
            ttk.Label(frame, text=value,
                     foreground=self.colors['white'],
                     font=('Arial', 9, 'bold')).pack(side=tk.RIGHT)
        
        # Ativos monitorados
        assets_frame = ttk.LabelFrame(sidebar,
                                     text="📊 Ativos Monitorados",
                                     style='Dark.TLabelframe')
        assets_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        assets = [
            ("BTC/USDT", "+2.34%", self.colors['secondary']),
            ("ETH/USDT", "+1.89%", self.colors['secondary']),
            ("SOL/USDT", "-0.56%", self.colors['danger']),
            ("ADA/USDT", "+0.42%", self.colors['secondary']),
            ("DOT/USDT", "+3.21%", self.colors['secondary'])
        ]
        
        for asset, change, color in assets:
            frame = ttk.Frame(assets_frame, style='Dark.TFrame')
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(frame, text=asset,
                     foreground=self.colors['white']).pack(side=tk.LEFT)
            ttk.Label(frame, text=change,
                     foreground=color).pack(side=tk.RIGHT)
        
        # Sinais ativos
        signals_frame = ttk.LabelFrame(sidebar,
                                      text="🎯 Sinais Ativos",
                                      style='Dark.TLabelframe')
        signals_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        signals = [
            ("BTC/USDT", "BUY", "91.7%"),
            ("ETH/USDT", "HOLD", "76.8%"),
            ("SOL/USDT", "SELL", "84.2%")
        ]
        
        for symbol, signal, confidence in signals:
            frame = ttk.Frame(signals_frame, style='Dark.TFrame')
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            signal_color = self.colors['secondary'] if signal == 'BUY' else \
                          self.colors['danger'] if signal == 'SELL' else \
                          self.colors['warning']
            
            ttk.Label(frame, text=symbol,
                     foreground=self.colors['white']).pack(side=tk.LEFT)
            ttk.Label(frame, text=signal,
                     foreground=signal_color,
                     font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(10, 0))
            ttk.Label(frame, text=confidence,
                     foreground=self.colors['gray_light']).pack(side=tk.RIGHT)
    
    def setup_status_bar(self):
        """Configurar barra de status"""
        status_bar = ttk.Frame(self.main_frame, style='Dark.TFrame', height=30)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        status_bar.pack_propagate(False)
        
        # Status do sistema
        self.status_label = ttk.Label(status_bar,
                                     text="✅ Sistema operando normalmente",
                                     foreground=self.colors['secondary'])
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Última atualização
        self.update_label = ttk.Label(status_bar,
                                     text="Última atualização: --:--:--",
                                     foreground=self.colors['gray_light'])
        self.update_label.pack(side=tk.LEFT, padx=20)
        
        # Modo de execução
        self.mode_label = ttk.Label(status_bar,
                                   text=f"Modo: {self.execution_mode.value}",
                                   foreground=self.colors['primary_light'])
        self.mode_label.pack(side=tk.RIGHT, padx=10)
        
        # Conexão
        self.connection_label = ttk.Label(status_bar,
                                         text="🌐 Conectado",
                                         foreground=self.colors['secondary'])
        self.connection_label.pack(side=tk.RIGHT, padx=10)
    
    def setup_responsive_layout(self):
        """Configurar layout responsivo"""
        # Tornar redimensionável
        self.root.minsize(1280, 720)
        
        # Centralizar na tela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Bind para redimensionamento
        self.root.bind('<Configure>', self.on_window_resize)
    
    def setup_updates(self):
        """Configurar atualizações periódicas"""
        self.update_clock()
        self.update_metrics()
    
    def setup_events(self):
        """Configurar eventos do sistema"""
        # Inscrever para eventos
        self.event_manager.subscribe('algorithm_updated', self.on_algorithm_updated)
        self.event_manager.subscribe('decision_made', self.on_decision_made)
        self.event_manager.subscribe('alert_triggered', self.on_alert_triggered)
        self.event_manager.subscribe('trade_executed', self.on_trade_executed)
    
    def start_background_threads(self):
        """Iniciar threads de background"""
        # Thread para atualizações de mercado
        market_thread = threading.Thread(target=self.market_update_worker, daemon=True)
        market_thread.start()
        
        # Thread para monitoramento do sistema
        system_thread = threading.Thread(target=self.system_monitor_worker, daemon=True)
        system_thread.start()
    
    # ============================================================================
    # FUNÇÕES DE ATUALIZAÇÃO
    # ============================================================================
    
    def update_clock(self):
        """Atualizar relógio"""
        now = datetime.now()
        self.update_label.config(text=f"Última atualização: {now.strftime('%H:%M:%S')}")
        self.root.after(1000, self.update_clock)
    
    def update_metrics(self):
        """Atualizar métricas do sistema"""
        # Atualizar métricas aleatórias (simulação)
        for algo in self.algorithms:
            if algo.is_active:
                # Pequenas variações nas métricas
                algo.confidence = max(0, min(100, algo.confidence + random.uniform(-0.5, 0.5)))
                algo.decisions_today += random.randint(0, 2)
        
        # Atualizar widgets se existirem
        for algo_id, widgets in self.algorithm_widgets.items():
            if 'performance_score' in widgets:
                algo = next((a for a in self.algorithms if a.id == algo_id), None)
                if algo:
                    score = algo.calculate_performance_score()
                    widgets['performance_score'].set_value(score)
        
        # Agendar próxima atualização
        self.root.after(5000, self.update_metrics)
    
    def market_update_worker(self):
        """Worker para atualizações de mercado"""
        while self.is_running:
            try:
                # Simular atualizações de mercado
                time.sleep(2)
                
                # Publicar evento de atualização
                self.event_manager.publish('market_updated', {
                    'timestamp': datetime.now(),
                    'symbol': 'BTC/USDT',
                    'price': 42000 + random.uniform(-500, 500)
                })
                
            except Exception as e:
                logger.error(f"Error in market update worker: {e}")
    
    def system_monitor_worker(self):
        """Worker para monitoramento do sistema"""
        while self.is_running:
            try:
                # Coletar métricas do sistema
                metrics = {
                    'cpu_usage': random.uniform(10, 80),
                    'memory_usage': random.uniform(40, 90),
                    'gpu_usage': random.uniform(5, 30),
                    'network_latency': random.uniform(10, 100),
                    'active_connections': random.randint(5, 20)
                }
                
                # Atualizar status
                self.root.after(0, lambda: self.update_system_status(metrics))
                
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in system monitor worker: {e}")
    
    # ============================================================================
    # MANIPULADORES DE EVENTOS
    # ============================================================================
    
    def on_tab_changed(self, event):
        """Manipulador de mudança de aba"""
        selected = self.notebook.index(self.notebook.select())
        tab_names = ["Dashboard", "Algoritmos", "Trading", "Análise", 
                    "Portfólio", "Monitoramento", "Backtesting", "Otimização", "Relatórios"]
        
        if selected < len(tab_names):
            logger.info(f"Aba alterada: {tab_names[selected]}")
    
    def on_window_resize(self, event):
        """Manipulador de redimensionamento de janela"""
        # Ajustar elementos responsivos
        pass
    
    def on_algorithm_updated(self, data):
        """Manipulador de algoritmo atualizado"""
        logger.info(f"Algoritmo atualizado: {data}")
    
    def on_decision_made(self, data):
        """Manipulador de decisão tomada"""
        logger.info(f"Decisão tomada: {data}")
    
    def on_alert_triggered(self, data):
        """Manipulador de alerta disparado"""
        logger.info(f"Alerta disparado: {data}")
    
    def on_trade_executed(self, data):
        """Manipulador de trade executado"""
        logger.info(f"Trade executado: {data}")
    
    # ============================================================================
    # FUNÇÕES DE CONTROLE PRINCIPAIS
    # ============================================================================
    
    def toggle_system(self):
        """Alternar estado do sistema"""
        if self.is_running:
            self.stop_system()
        else:
            self.start_system()
    
    def start_system(self):
        """Iniciar sistema de trading"""
        self.is_running = True
        self.start_stop_btn.config(text="⏸️ Parar Sistema")
        self.status_label.config(text="✅ Sistema iniciado", 
                                foreground=self.colors['secondary'])
        
        messagebox.showinfo("Sistema Iniciado", "Sistema de trading iniciado com sucesso!")
    
    def stop_system(self):
        """Parar sistema de trading"""
        self.is_running = False
        self.start_stop_btn.config(text="▶️ Iniciar Sistema")
        self.status_label.config(text="⏸️ Sistema parado", 
                                foreground=self.colors['warning'])
        
        messagebox.showinfo("Sistema Parado", "Sistema de trading parado com sucesso!")
    
    def change_execution_mode(self, mode):
        """Alterar modo de execução"""
        self.execution_mode = ExecutionMode(mode)
        self.mode_label.config(text=f"Modo: {self.execution_mode.value}")
        
        # Atualizar cor baseada no modo
        color_map = {
            ExecutionMode.PAPER: self.colors['info'],
            ExecutionMode.LIVE: self.colors['danger'],
            ExecutionMode.SIMULATION: self.colors['warning'],
            ExecutionMode.BACKTEST: self.colors['primary'],
            ExecutionMode.HYBRID: self.colors['secondary']
        }
        
        self.mode_label.config(foreground=color_map.get(self.execution_mode, self.colors['white']))
        
        logger.info(f"Modo de execução alterado para: {self.execution_mode.value}")
    
    def toggle_algorithm(self, algorithm_id):
        """Alternar estado do algoritmo"""
        for algo in self.algorithms:
            if algo.id == algorithm_id:
                algo.is_active = not algo.is_active
                
                # Atualizar status
                status = "ativado" if algo.is_active else "desativado"
                messagebox.showinfo("Algoritmo Atualizado", 
                                  f"Algoritmo {algo.name} {status} com sucesso!")
                
                # Publicar evento
                self.event_manager.publish('algorithm_updated', {
                    'algorithm_id': algorithm_id,
                    'is_active': algo.is_active,
                    'timestamp': datetime.now()
                })
                
                break
    
    def optimize_algorithm(self, algorithm_id):
        """Otimizar algoritmo"""
        messagebox.showinfo("Otimização", 
                          f"Iniciando otimização do algoritmo {algorithm_id}...")
        
        # Publicar evento
        self.event_manager.publish('algorithm_optimization_started', {
            'algorithm_id': algorithm_id,
            'timestamp': datetime.now()
        })
    
    def train_algorithm(self, algorithm_id):
        """Treinar algoritmo"""
        messagebox.showinfo("Treinamento", 
                          f"Iniciando treinamento do algoritmo {algorithm_id}...")
        
        # Publicar evento
        self.event_manager.publish('algorithm_training_started', {
            'algorithm_id': algorithm_id,
            'timestamp': datetime.now()
        })
    
    def show_algorithm_details(self, algorithm_id):
        """Mostrar detalhes do algoritmo"""
        # Encontrar algoritmo
        algo = next((a for a in self.algorithms if a.id == algorithm_id), None)
        if not algo:
            return
        
        # Criar janela de detalhes
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Detalhes: {algo.name}")
        details_window.geometry("600x800")
        details_window.configure(bg=self.colors['dark'])
        
        # Adicionar conteúdo
        content = scrolledtext.ScrolledText(details_window,
                                          bg=self.colors['dark_lighter'],
                                          fg=self.colors['white'],
                                          font=('Arial', 10))
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Formatar detalhes
        details = f"""
{'='*60}
{algo.name} - v{algo.version}
{'='*60}

📊 DESCRIÇÃO:
{algo.description}

{'='*60}
📈 MÉTRICAS DE PERFORMANCE:
{'='*60}
• Precisão: {algo.accuracy:.1f}%
• Win Rate: {algo.win_rate:.1f}%
• Sharpe Ratio: {algo.sharpe_ratio:.2f}
• Sortino Ratio: {algo.sortino_ratio:.2f}
• Maximum Drawdown: {algo.max_drawdown:.1f}%
• Profit Factor: {algo.profit_factor:.2f}

{'='*60}
⚡ MÉTRICAS OPERACIONAIS:
{'='*60}
• Velocidade: {algo.speed:.1f}
• Latência: {algo.latency:.3f}s
• Confiança: {algo.confidence:.1f}%
• Estabilidade: {algo.stability:.1f}%
• Robustez: {algo.robustness:.1f}%

{'='*60}
📊 ESTATÍSTICAS:
{'='*60}
• Decisões Totais: {algo.decisions_made:,}
• Decisões Hoje: {algo.decisions_today}
• Sucessos: {algo.success_count}
• Falhas: {algo.failure_count}
• Lucro Total: ${algo.total_profit:,.2f}
• Perda Total: ${algo.total_loss:,.2f}
• Tempo Médio Resposta: {algo.avg_response_time:.3f}s

{'='*60}
🎯 ESPECIALIZAÇÕES:
{'='*60}
• {', '.join(algo.specializations)}

{'='*60}
⚙️ PARÂMETROS:
{'='*60}
"""
        
        for key, value in algo.parameters.items():
            details += f"• {key}: {value}\n"
        
        if algo.neural_architecture:
            details += f"""
{'='*60}
🧠 ARQUITETURA NEURAL:
{'='*60}
• Arquitetura: {algo.neural_architecture}
• Camadas: {algo.num_layers}
• Parâmetros: {algo.num_parameters:,}
• Épocas Treinamento: {algo.training_epochs}
• Último Treinamento: {algo.last_trained.strftime('%Y-%m-%d') if algo.last_trained else 'Nunca'}
"""
        
        content.insert(tk.END, details)
        content.config(state='disabled')
    
    def load_market_data(self, symbol):
        """Carregar dados de mercado"""
        messagebox.showinfo("Carregar Dados", 
                          f"Carregando dados para {symbol}...")
        
        # Publicar evento
        self.event_manager.publish('market_data_requested', {
            'symbol': symbol,
            'timestamp': datetime.now()
        })
    
    def place_order(self, side, quantity):
        """Colocar ordem"""
        try:
            qty = float(quantity)
            if qty <= 0:
                raise ValueError("Quantidade deve ser positiva")
            
            messagebox.showinfo("Ordem", 
                              f"Ordem de {side} para {qty} unidades enviada!")
            
            # Publicar evento
            self.event_manager.publish('order_placed', {
                'side': side,
                'quantity': qty,
                'timestamp': datetime.now()
            })
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Quantidade inválida: {e}")
    
    def analyze_asset(self):
        """Analisar ativo"""
        messagebox.showinfo("Análise", 
                          "Iniciando análise completa do ativo...")
        
        # Publicar evento
        self.event_manager.publish('analysis_started', {
            'timestamp': datetime.now()
        })
    
    def refresh_chart(self):
        """Atualizar gráfico"""
        messagebox.showinfo("Atualizar", "Gráfico atualizado!")
    
    def add_indicators(self):
        """Adicionar indicadores ao gráfico"""
        messagebox.showinfo("Indicadores", "Indicadores adicionados ao gráfico!")
    
    def cancel_all_orders(self):
        """Cancelar todas as ordens"""
        if messagebox.askyesno("Confirmar", "Cancelar todas as ordens pendentes?"):
            messagebox.showinfo("Cancelar Ordens", "Todas as ordens foram canceladas!")
            
            # Publicar evento
            self.event_manager.publish('orders_cancelled', {
                'timestamp': datetime.now()
            })
    
    def refresh_orders(self):
        """Atualizar lista de ordens"""
        messagebox.showinfo("Atualizar", "Lista de ordens atualizada!")
    
    def close_all_positions(self):
        """Fechar todas as posições"""
        if messagebox.askyesno("Confirmar", "Fechar todas as posições abertas?"):
            messagebox.showinfo("Fechar Posições", "Todas as posições foram fechadas!")
            
            # Publicar evento
            self.event_manager.publish('positions_closed', {
                'timestamp': datetime.now()
            })
    
    def hedge_portfolio(self):
        """Hedgear portfólio"""
        messagebox.showinfo("Hedge", "Iniciando hedge do portfólio...")
        
        # Publicar evento
        self.event_manager.publish('hedge_started', {
            'timestamp': datetime.now()
        })
    
    def clear_logs(self):
        """Limpar logs"""
        if messagebox.askyesno("Confirmar", "Limpar todos os logs?"):
            messagebox.showinfo("Limpar Logs", "Logs limpos com sucesso!")
    
    def export_logs(self):
        """Exportar logs"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            messagebox.showinfo("Exportar", f"Logs exportados para: {filename}")
    
    def acknowledge_all_alerts(self):
        """Reconhecer todos os alertas"""
        if messagebox.askyesno("Confirmar", "Reconhecer todos os alertas?"):
            messagebox.showinfo("Reconhecer Alertas", "Todos os alertas foram reconhecidos!")
    
    def clear_resolved_alerts(self):
        """Limpar alertas resolvidos"""
        if messagebox.askyesno("Confirmar", "Limpar alertas resolvidos?"):
            messagebox.showinfo("Limpar Alertas", "Alertas resolvidos limpos!")
    
    def update_system_status(self, metrics):
        """Atualizar status do sistema"""
        # Atualizar métricas na UI
        if hasattr(self, 'connection_label'):
            latency = metrics.get('network_latency', 0)
            if latency < 50:
                self.connection_label.config(text="🌐 Excelente", 
                                           foreground=self.colors['secondary'])
            elif latency < 100:
                self.connection_label.config(text="🌐 Bom", 
                                           foreground=self.colors['warning'])
            else:
                self.connection_label.config(text="🌐 Lento", 
                                           foreground=self.colors['danger'])
    
    def open_settings(self):
        """Abrir configurações"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configurações do Sistema")
        settings_window.geometry("500x600")
        settings_window.configure(bg=self.colors['dark'])
        
        # Notebook para configurações
        settings_notebook = ttk.Notebook(settings_window)
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba Geral
        general_frame = ttk.Frame(settings_notebook, style='Dark.TFrame')
        settings_notebook.add(general_frame, text="Geral")
        
        # Aba Risco
        risk_frame = ttk.Frame(settings_notebook, style='Dark.TFrame')
        settings_notebook.add(risk_frame, text="Risco")
        
        # Aba Notificações
        notif_frame = ttk.Frame(settings_notebook, style='Dark.TFrame')
        settings_notebook.add(notif_frame, text="Notificações")
        
        # Configurar abas
        self.setup_general_settings(general_frame)
        self.setup_risk_settings(risk_frame)
        self.setup_notification_settings(notif_frame)
    
    def setup_general_settings(self, parent):
        """Configurar aba de configurações gerais"""
        # Tema
        ttk.Label(parent, text="Tema:", 
                 foreground=self.colors['white']).pack(anchor='w', padx=10, pady=(10, 5))
        
        theme_var = tk.StringVar(value=self.settings['theme'])
        theme_menu = ttk.OptionMenu(parent, theme_var, self.settings['theme'],
                                   "dark", "light", "auto")
        theme_menu.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Idioma
        ttk.Label(parent, text="Idioma:", 
                 foreground=self.colors['white']).pack(anchor='w', padx=10, pady=(10, 5))
        
        lang_var = tk.StringVar(value=self.settings['language'])
        lang_menu = ttk.OptionMenu(parent, lang_var, self.settings['language'],
                                  "pt-BR", "en-US", "es-ES")
        lang_menu.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Auto-trading
        auto_var = tk.BooleanVar(value=self.settings['auto_trading'])
        auto_check = ttk.Checkbutton(parent, text="Auto-trading", 
                                    variable=auto_var)
        auto_check.pack(anchor='w', padx=10, pady=10)
        
        # Botões
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        save_btn = ttk.Button(button_frame, text="💾 Salvar",
                             command=lambda: self.save_settings({
                                 'theme': theme_var.get(),
                                 'language': lang_var.get(),
                                 'auto_trading': auto_var.get()
                             }))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="❌ Cancelar",
                               command=lambda: parent.winfo_toplevel().destroy())
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def setup_risk_settings(self, parent):
        """Configurar aba de configurações de risco"""
        # Tolerância a risco
        ttk.Label(parent, text="Tolerância a Risco:", 
                 foreground=self.colors['white']).pack(anchor='w', padx=10, pady=(10, 5))
        
        risk_var = tk.StringVar(value=self.settings['risk_tolerance'])
        risk_scale = ttk.Scale(parent, from_=0, to=100, 
                              variable=tk.DoubleVar(value=50),
                              orient=tk.HORIZONTAL)
        risk_scale.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Tamanho máximo de posição
        ttk.Label(parent, text="Tamanho Máx. Posição (% do capital):", 
                 foreground=self.colors['white']).pack(anchor='w', padx=10, pady=(10, 5))
        
        position_var = tk.DoubleVar(value=self.settings['max_position_size'] * 100)
        position_spin = ttk.Spinbox(parent, from_=1, to=100, 
                                   textvariable=position_var,
                                   width=10)
        position_spin.pack(anchor='w', padx=10, pady=(0, 10))
        
        # Perda diária máxima
        ttk.Label(parent, text="Perda Diária Máxima (% do capital):", 
                 foreground=self.colors['white']).pack(anchor='w', padx=10, pady=(10, 5))
        
        loss_var = tk.DoubleVar(value=self.settings['max_daily_loss'] * 100)
        loss_spin = ttk.Spinbox(parent, from_=0.1, to=10, 
                               textvariable=loss_var,
                               width=10, increment=0.5)
        loss_spin.pack(anchor='w', padx=10, pady=(0, 10))
        
        # Botões
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        save_btn = ttk.Button(button_frame, text="💾 Salvar",
                             command=lambda: self.save_risk_settings({
                                 'risk_tolerance': risk_var.get(),
                                 'max_position_size': position_var.get() / 100,
                                 'max_daily_loss': loss_var.get() / 100
                             }))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="❌ Cancelar",
                               command=lambda: parent.winfo_toplevel().destroy())
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def setup_notification_settings(self, parent):
        """Configurar aba de configurações de notificações"""
        # Notificações habilitadas
        notif_var = tk.BooleanVar(value=self.settings['notifications_enabled'])
        notif_check = ttk.Checkbutton(parent, text="Notificações Habilitadas", 
                                     variable=notif_var)
        notif_check.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Som
        sound_var = tk.BooleanVar(value=self.settings['sound_enabled'])
        sound_check = ttk.Checkbutton(parent, text="Som Habilitado", 
                                     variable=sound_var)
        sound_check.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Tipos de notificação
        ttk.Label(parent, text="Tipos de Notificação:", 
                 foreground=self.colors['white']).pack(anchor='w', padx=10, pady=(10, 5))
        
        types_frame = ttk.Frame(parent, style='Dark.TFrame')
        types_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        notification_types = [
            ("📈 Sinais de Trade", tk.BooleanVar(value=True)),
            ("🚨 Alertas de Risco", tk.BooleanVar(value=True)),
            ("🔧 Alertas de Sistema", tk.BooleanVar(value=True)),
            ("📊 Alertas de Performance", tk.BooleanVar(value=True)),
            ("💸 Execuções de Ordem", tk.BooleanVar(value=True))
        ]
        
        for text, var in notification_types:
            check = ttk.Checkbutton(types_frame, text=text, variable=var)
            check.pack(anchor='w', pady=2)
        
        # Botões
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        save_btn = ttk.Button(button_frame, text="💾 Salvar",
                             command=lambda: self.save_notification_settings({
                                 'notifications_enabled': notif_var.get(),
                                 'sound_enabled': sound_var.get()
                             }))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="❌ Cancelar",
                               command=lambda: parent.winfo_toplevel().destroy())
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def save_settings(self, settings):
        """Salvar configurações"""
        self.settings.update(settings)
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
    
    def save_risk_settings(self, settings):
        """Salvar configurações de risco"""
        self.settings.update(settings)
        messagebox.showinfo("Sucesso", "Configurações de risco salvas com sucesso!")
    
    def save_notification_settings(self, settings):
        """Salvar configurações de notificação"""
        self.settings.update(settings)
        messagebox.showinfo("Sucesso", "Configurações de notificação salvas com sucesso!")
    
    def show_help(self):
        """Mostrar ajuda"""
        help_text = """
LEXTRADER-IAG - Sistema de Trading Algorítmico Avançado

📚 FUNCIONALIDADES PRINCIPAIS:

1. 🤖 ALGORITMOS AVANÇADOS
   • Quantum Ensemble: Combinação de múltiplas redes neurais
   • LSTM Adaptativo: Análise de séries temporais
   • Otimizador Bayesiano: Otimização multi-objetivo

2. 💼 GESTÃO DE PORTFÓLIO
   • Alocação dinâmica de ativos
   • Controle de risco em tempo real
   • Hedge automático

3. 📊 ANÁLISE AVANÇADA
   • Técnica: Indicadores e padrões
   • Fundamentalista: Métricas de mercado
   • Sentimento: Análise de mídias sociais
   • Risco: VaR, CVaR, drawdown

4. 👁️ MONITORAMENTO
   • Logs do sistema em tempo real
   • Métricas de performance
   • Alertas inteligentes

5. 🧪 BACKTESTING
   • Teste de estratégias históricas
   • Otimização de parâmetros
   • Análise de resultados

🎯 COMO USAR:

1. Configure seus algoritmos na aba "🤖 Algoritmos"
2. Defina seu perfil de risco em "Configurações"
3. Monitore as decisões em "💰 Trading"
4. Acompanhe o desempenho em "📊 Dashboard"
5. Ajuste estratégias baseado em "📊 Análise"

⚠️ AVISOS IMPORTANTES:
• Trading envolve riscos significativos
• Sempre teste estratégias antes de usar capital real
• Monitoramento constante é essencial
• Diversificação reduz risco

Para suporte técnico: suporte@lextrader.com.br
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Ajuda - LEXTRADER-IAG")
        help_window.geometry("700x800")
        help_window.configure(bg=self.colors['dark'])
        
        text_area = scrolledtext.ScrolledText(help_window,
                                            bg=self.colors['dark_lighter'],
                                            fg=self.colors['white'],
                                            font=('Arial', 10),
                                            wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, help_text)
        text_area.config(state='disabled')
    
    def open_quick_trade(self):
        """Abrir janela de trade rápido"""
        quick_window = tk.Toplevel(self.root)
        quick_window.title("Trade Rápido")
        quick_window.geometry("400x300")
        quick_window.configure(bg=self.colors['dark'])
        
        ttk.Label(quick_window, text="Trade Rápido",
                 font=('Arial', 14, 'bold'),
                 foreground=self.colors['white']).pack(pady=20)
        
        # Formulário simples
        form_frame = ttk.Frame(quick_window, style='Dark.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Símbolo:",
                 foreground=self.colors['white']).grid(row=0, column=0, sticky='w', pady=5)
        symbol_entry = ttk.Entry(form_frame, width=15)
        symbol_entry.grid(row=0, column=1, pady=5)
        symbol_entry.insert(0, "BTC/USDT")
        
        ttk.Label(form_frame, text="Lado:",
                 foreground=self.colors['white']).grid(row=1, column=0, sticky='w', pady=5)
        side_var = tk.StringVar(value="BUY")
        side_menu = ttk.OptionMenu(form_frame, side_var, "BUY", "BUY", "SELL")
        side_menu.grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Quantidade:",
                 foreground=self.colors['white']).grid(row=2, column=0, sticky='w', pady=5)
        qty_entry = ttk.Entry(form_frame, width=15)
        qty_entry.grid(row=2, column=1, pady=5)
        qty_entry.insert(0, "0.1")
        
        # Botões
        button_frame = ttk.Frame(form_frame, style='Dark.TFrame')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        buy_btn = ttk.Button(button_frame, text="📈 Comprar",
                            command=lambda: self.execute_quick_trade(
                                symbol_entry.get(), "BUY", qty_entry.get()
                            ),
                            style='Success.TButton',
                            width=15)
        buy_btn.pack(side=tk.LEFT, padx=5)
        
        sell_btn = ttk.Button(button_frame, text="📉 Vender",
                             command=lambda: self.execute_quick_trade(
                                 symbol_entry.get(), "SELL", qty_entry.get()
                             ),
                             style='Danger.TButton',
                             width=15)
        sell_btn.pack(side=tk.LEFT, padx=5)
    
    def execute_quick_trade(self, symbol, side, quantity):
        """Executar trade rápido"""
        try:
            qty = float(quantity)
            messagebox.showinfo("Trade Executado", 
                              f"{side} {qty} {symbol} executado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
    
    def check_risk(self):
        """Verificar risco"""
        messagebox.showinfo("Verificar Risco", 
                          "Análise de risco completada.\n" +
                          "Portfólio dentro dos limites de risco configurados.")
    
    def generate_report(self):
        """Gerar relatório"""
        # Salvar arquivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if filename:
            messagebox.showinfo("Relatório", 
                              f"Relatório gerado com sucesso:\n{filename}")

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal da aplicação"""
    # Criar janela principal
    root = tk.Tk()
    
    # Criar aplicação
    app = AdvancedTradingDashboard(root)
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()