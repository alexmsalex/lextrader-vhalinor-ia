import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Simulação do gerenciador autônomo
class AutonomousManager:
    def __init__(self):
        self.config = {
            'riskTolerance': 0.3,
            'minConfidence': 0.75,
            'memorySize': 10000
        }
        self.is_running = False
        self.buffer_size = 0
        self.performance = {
            'accuracy': 0.82,
            'avgReturn': 0.023,
            'positiveExperiences': 4231,
            'negativeExperiences': 876
        }
    
    def get_status(self):
        return {
            'isRunning': self.is_running,
            'bufferSize': self.buffer_size,
            'performance': self.performance
        }
    
    def start(self):
        self.is_running = True
        print("Motor autônomo iniciado")
    
    def stop(self):
        self.is_running = False
        print("Motor autônomo parado")

# Simulação do núcleo senciente
class SentientCore:
    @staticmethod
    def get_state():
        states = ['NEUTRAL', 'OPTIMISTIC', 'CAUTIOUS', 'EXPLORATORY']
        return random.choice(states)

@dataclass
class PerformancePoint:
    time: str
    accuracy: float
    return_val: float

class AutonomousDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador Autônomo Neural")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0a0a0a")
        
        # Inicializar gerenciadores
        self.autonomous_manager = AutonomousManager()
        self.sentient_core = SentientCore()
        
        # Estado da aplicação
        self.status = self.autonomous_manager.get_status()
        self.config = self.autonomous_manager.config
        self.agi_state = self.sentient_core.get_state()
        self.performance_history: List[PerformancePoint] = []
        self.active_memory = None
        
        # Configurar UI
        self.setup_ui()
        
        # Iniciar atualizações periódicas
        self.start_updates()
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        self.setup_header()
        
        # Conteúdo principal
        self.setup_content()
    
    def setup_header(self):
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Logo e título
        left_frame = tk.Frame(header_frame, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # Ícone
        icon_frame = tk.Frame(left_frame, bg="#064e3b", relief=tk.RAISED, borderwidth=1, padx=10, pady=10)
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        tk.Label(
            icon_frame,
            text="🤖",
            font=("Arial", 16),
            bg="#064e3b",
            fg="#2dd4bf"
        ).pack()
        
        # Texto
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(
            text_frame,
            text="GERENCIADOR AUTÔNOMO NEURAL",
            font=("Arial", 16, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        tk.Label(
            text_frame,
            text="SELF-LEARNING • EXPERIENCE REPLAY",
            font=("Courier", 10),
            fg="#2dd4bf",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        # Botões e status do lado direito
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        # Status AGI
        agi_frame = tk.Frame(right_frame, bg="#0a0a0a", relief=tk.RAISED, borderwidth=1, padx=10, pady=5)
        agi_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            agi_frame,
            text="🤖",
            font=("Arial", 12),
            bg="#0a0a0a",
            fg="#a855f7"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            agi_frame,
            text=f"AGI: {self.agi_state}",
            font=("Courier", 10, "bold"),
            fg="#a855f7",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT)
        
        # Botão de iniciar/parar
        self.toggle_button = tk.Button(
            right_frame,
            text="INICIAR MOTOR" if not self.status['isRunning'] else "PARAR MOTOR",
            command=self.toggle_run,
            bg="#064e3b" if not self.status['isRunning'] else "#991b1b",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.toggle_button.pack(side=tk.LEFT)
    
    def setup_content(self):
        # Frame principal do conteúdo
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Coluna esquerda: Replay & Memory
        left_frame = tk.Frame(content_frame, bg="#0a0a0a")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Painel de Replay de Experiência
        replay_frame = tk.Frame(
            left_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        replay_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            replay_frame,
            text="REPLAY DE EXPERIÊNCIA",
            font=("Arial", 11, "bold"),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Área de memória ativa
        self.memory_frame = tk.Frame(
            replay_frame,
            bg="#0a0a0a",
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=10,
            pady=10
        )
        self.memory_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Buffer size
        buffer_frame = tk.Frame(replay_frame, bg="#1a1a2e")
        buffer_frame.pack(fill=tk.X)
        
        tk.Label(
            buffer_frame,
            text="Buffer Size",
            font=("Arial", 10),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.buffer_label = tk.Label(
            buffer_frame,
            text=f"{self.status['bufferSize']} / {self.config['memorySize']}",
            font=("Courier", 10, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.buffer_label.pack(side=tk.RIGHT)
        
        # Barra de progresso do buffer
        self.buffer_bar = tk.Frame(replay_frame, bg="#374151", height=8)
        self.buffer_bar.pack(fill=tk.X, pady=(5, 0))
        self.buffer_bar.pack_propagate(False)
        
        self.buffer_progress = tk.Frame(
            self.buffer_bar,
            bg="#a855f7",
            width=int((self.status['bufferSize'] / self.config['memorySize']) * 100)
        )
        self.buffer_progress.pack(side=tk.LEFT, fill=tk.Y)
        
        # Painel de Parâmetros
        params_frame = tk.Frame(
            left_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        params_frame.pack(fill=tk.X)
        
        tk.Label(
            params_frame,
            text="PARÂMETROS",
            font=("Arial", 11, "bold"),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Tolerância ao Risco
        risk_frame = tk.Frame(params_frame, bg="#1a1a2e")
        risk_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            risk_frame,
            text="Tolerância ao Risco",
            font=("Arial", 10),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.risk_label = tk.Label(
            risk_frame,
            text=f"{self.config['riskTolerance'] * 100:.0f}%",
            font=("Courier", 10, "bold"),
            fg="#2dd4bf",
            bg="#1a1a2e"
        )
        self.risk_label.pack(side=tk.RIGHT)
        
        # Barra de risco
        risk_bar_frame = tk.Frame(params_frame, bg="#374151", height=6)
        risk_bar_frame.pack(fill=tk.X, pady=(5, 15))
        risk_bar_frame.pack_propagate(False)
        
        self.risk_bar = tk.Frame(
            risk_bar_frame,
            bg="#2dd4bf",
            width=int(self.config['riskTolerance'] * 100)
        )
        self.risk_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Confiança Mínima
        confidence_frame = tk.Frame(params_frame, bg="#1a1a2e")
        confidence_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            confidence_frame,
            text="Confiança Mínima",
            font=("Arial", 10),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.confidence_label = tk.Label(
            confidence_frame,
            text=f"{self.config['minConfidence'] * 100:.0f}%",
            font=("Courier", 10, "bold"),
            fg="#60a5fa",
            bg="#1a1a2e"
        )
        self.confidence_label.pack(side=tk.RIGHT)
        
        # Barra de confiança
        confidence_bar_frame = tk.Frame(params_frame, bg="#374151", height=6)
        confidence_bar_frame.pack(fill=tk.X, pady=(5, 0))
        confidence_bar_frame.pack_propagate(False)
        
        self.confidence_bar = tk.Frame(
            confidence_bar_frame,
            bg="#60a5fa",
            width=int(self.config['minConfidence'] * 100)
        )
        self.confidence_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Coluna direita: Performance Charts
        right_frame = tk.Frame(content_frame, bg="#0a0a0a")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Gráfico de performance
        chart_frame = tk.Frame(
            right_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            chart_frame,
            text="PERFORMANCE DE TREINAMENTO (ONLINE)",
            font=("Arial", 11, "bold"),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Criar gráfico matplotlib
        self.setup_chart(chart_frame)
        
        # Métricas de performance
        metrics_frame = tk.Frame(right_frame, bg="#0a0a0a")
        metrics_frame.pack(fill=tk.X)
        
        # Acurácia Global
        accuracy_frame = tk.Frame(
            metrics_frame,
            bg="#0a0a0a",
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=20,
            pady=15
        )
        accuracy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            accuracy_frame,
            text="ACURÁCIA GLOBAL",
            font=("Arial", 9),
            fg="#666666",
            bg="#0a0a0a"
        ).pack()
        
        self.accuracy_label = tk.Label(
            accuracy_frame,
            text=f"{self.status['performance']['accuracy'] * 100:.1f}%",
            font=("Courier", 20, "bold"),
            fg="#ffffff",
            bg="#0a0a0a"
        )
        self.accuracy_label.pack(pady=(5, 0))
        
        # Experiências Positivas
        positive_frame = tk.Frame(
            metrics_frame,
            bg="#0a0a0a",
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=20,
            pady=15
        )
        positive_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            positive_frame,
            text="EXP. POSITIVAS",
            font=("Arial", 9),
            fg="#666666",
            bg="#0a0a0a"
        ).pack()
        
        self.positive_label = tk.Label(
            positive_frame,
            text=str(self.status['performance']['positiveExperiences']),
            font=("Courier", 20, "bold"),
            fg="#4ade80",
            bg="#0a0a0a"
        )
        self.positive_label.pack(pady=(5, 0))
        
        # Experiências Negativas
        negative_frame = tk.Frame(
            metrics_frame,
            bg="#0a0a0a",
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=20,
            pady=15
        )
        negative_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            negative_frame,
            text="EXP. NEGATIVAS",
            font=("Arial", 9),
            fg="#666666",
            bg="#0a0a0a"
        ).pack()
        
        self.negative_label = tk.Label(
            negative_frame,
            text=str(self.status['performance']['negativeExperiences']),
            font=("Courier", 20, "bold"),
            fg="#ef4444",
            bg="#0a0a0a"
        )
        self.negative_label.pack(pady=(5, 0))
    
    def setup_chart(self, parent_frame):
        # Criar figura matplotlib
        self.fig = Figure(figsize=(10, 4), dpi=80, facecolor='#1a1a2e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1a1a2e')
        
        # Configurar eixos
        self.ax.set_xlabel('Tempo', color='#666666')
        self.ax.set_ylabel('Valor (%)', color='#666666')
        self.ax.tick_params(colors='#666666')
        self.ax.grid(True, color='#222222', linestyle='--', alpha=0.5)
        
        # Inicializar com dados vazios
        self.accuracy_line, = self.ax.plot([], [], color='#2dd4bf', linewidth=2, label='Acurácia')
        self.return_line, = self.ax.plot([], [], color='#facc15', linewidth=2, label='Retorno')
        self.ax.legend(facecolor='#1a1a2e', labelcolor='white')
        
        # Adicionar ao Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_chart(self):
        if len(self.performance_history) > 0:
            times = list(range(len(self.performance_history)))
            accuracies = [p.accuracy for p in self.performance_history]
            returns = [p.return_val for p in self.performance_history]
            
            self.accuracy_line.set_data(times, accuracies)
            self.return_line.set_data(times, returns)
            
            # Ajustar limites
            self.ax.set_xlim(0, max(times) if times else 1)
            self.ax.set_ylim(0, max(max(accuracies) if accuracies else 100, 
                                 max(returns) if returns else 100) * 1.1)
            
            self.canvas.draw()
    
    def update_memory_display(self):
        # Limpar frame de memória
        for widget in self.memory_frame.winfo_children():
            widget.destroy()
        
        if self.active_memory:
            # ID da memória
            tk.Label(
                self.memory_frame,
                text=f"PROCESSANDO MEMÓRIA: {self.active_memory['id']}",
                font=("Courier", 9),
                fg="#2dd4bf",
                bg="#0a0a0a"
            ).pack(anchor=tk.W, pady=(0, 10))
            
            # Ação e recompensa
            action_frame = tk.Frame(self.memory_frame, bg="#0a0a0a")
            action_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(
                action_frame,
                text=self.active_memory['action'],
                font=("Arial", 12, "bold"),
                fg="#ffffff",
                bg="#0a0a0a"
            ).pack(side=tk.LEFT)
            
            reward_color = "#4ade80" if self.active_memory['reward'] > 0 else "#ef4444"
            reward_text = "RECOMPENSA" if self.active_memory['reward'] > 0 else "PUNIÇÃO"
            
            tk.Label(
                action_frame,
                text=reward_text,
                font=("Arial", 10, "bold"),
                fg=reward_color,
                bg="#0a0a0a"
            ).pack(side=tk.RIGHT)
            
            # Barra de progresso
            progress_frame = tk.Frame(self.memory_frame, bg="#374151", height=6)
            progress_frame.pack(fill=tk.X, pady=(0, 5))
            progress_frame.pack_propagate(False)
            
            progress_bar = tk.Frame(
                progress_frame,
                bg="#2dd4bf",
                width=180  # 60% de 300
            )
            progress_bar.pack(side=tk.LEFT, fill=tk.Y)
            
            # Texto de ajuste
            tk.Label(
                self.memory_frame,
                text="Ajustando pesos sinápticos...",
                font=("Arial", 8),
                fg="#666666",
                bg="#0a0a0a"
            ).pack(anchor=tk.E)
        else:
            tk.Label(
                self.memory_frame,
                text="Buffer de sonho vazio.",
                font=("Arial", 10),
                fg="#666666",
                bg="#0a0a0a"
            ).pack(expand=True, pady=20)
    
    def toggle_run(self):
        if self.status['isRunning']:
            self.autonomous_manager.stop()
            self.toggle_button.config(
                text="INICIAR MOTOR",
                bg="#064e3b"
            )
        else:
            self.autonomous_manager.start()
            self.toggle_button.config(
                text="PARAR MOTOR",
                bg="#991b1b"
            )
        
        self.status = self.autonomous_manager.get_status()
    
    def start_updates(self):
        def update_loop():
            while True:
                time.sleep(1)  # Atualizar a cada segundo
                
                # Atualizar status
                self.status = self.autonomous_manager.get_status()
                self.agi_state = self.sentient_core.get_state()
                
                # Adicionar ponto de performance
                new_point = PerformancePoint(
                    time=datetime.now().strftime("%H:%M:%S"),
                    accuracy=self.status['performance']['accuracy'] * 100,
                    return_val=self.status['performance']['avgReturn'] * 100
                )
                
                self.performance_history.append(new_point)
                if len(self.performance_history) > 20:
                    self.performance_history.pop(0)
                
                # Atualizar buffer aleatoriamente
                if self.status['isRunning']:
                    self.status['bufferSize'] = min(
                        self.config['memorySize'],
                        self.status['bufferSize'] + random.randint(0, 50)
                    )
                    
                    # Simular visualização de memória ativa
                    if self.status['bufferSize'] > 0 and random.random() > 0.7:
                        self.active_memory = {
                            'id': ''.join(random.choices('0123456789abcdef', k=6)),
                            'action': random.choice(['BUY', 'SELL']),
                            'reward': (random.random() - 0.4) * 10
                        }
                    else:
                        self.active_memory = None
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_ui)
        
        # Iniciar thread de atualização
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def update_ui(self):
        # Atualizar labels
        self.buffer_label.config(
            text=f"{self.status['bufferSize']} / {self.config['memorySize']}"
        )
        
        # Atualizar barras de progresso
        buffer_percent = (self.status['bufferSize'] / self.config['memorySize']) * 100
        self.buffer_progress.config(width=int(buffer_percent))
        
        self.accuracy_label.config(
            text=f"{self.status['performance']['accuracy'] * 100:.1f}%"
        )
        
        self.positive_label.config(
            text=str(self.status['performance']['positiveExperiences'])
        )
        
        self.negative_label.config(
            text=str(self.status['performance']['negativeExperiences'])
        )
        
        # Atualizar display de memória
        self.update_memory_display()
        
        # Atualizar gráfico
        self.update_chart()
        
        # Atualizar cabeçalho
        for widget in self.main_frame.winfo_children()[0].winfo_children()[1].winfo_children():
            if isinstance(widget, tk.Label) and "AGI:" in widget.cget("text"):
                widget.config(text=f"AGI: {self.agi_state}")

def main():
    root = tk.Tk()
    app = AutonomousDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()