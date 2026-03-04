import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
import threading
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum

# Enums e tipos
@dataclass
class AutoSystemConfig:
    max_processes: int
    auto_recovery: bool
    neural_networks: int
    quantum_processing: bool

@dataclass
class SystemHealth:
    cpu_load: float
    memory_usage: float
    integrity_score: float
    network_latency: float

@dataclass
class AutoLog:
    id: int
    timestamp: datetime
    module: str
    message: str

# Simulação do sistema autônomo
class AutonomousSystem:
    def __init__(self):
        self.config = AutoSystemConfig(
            max_processes=256,
            auto_recovery=True,
            neural_networks=8,
            quantum_processing=True
        )
        self.health = SystemHealth(
            cpu_load=35.5,
            memory_usage=42.3,
            integrity_score=99.8,
            network_latency=12.0
        )
        self.active = False
        self.logs: List[AutoLog] = []
        self.log_counter = 0
        
        # Log inicial
        self.add_log("SYSTEM", "Sistema autônomo inicializado em modo standby")
    
    def get_status(self):
        return {
            'active': self.active,
            'config': self.config,
            'health': self.health,
            'logs': self.logs[-20:]  # Últimos 20 logs
        }
    
    def toggle_system(self):
        self.active = not self.active
        status = "ATIVADO" if self.active else "DESATIVADO"
        self.add_log("CONTROL", f"Sistema {status}")
        return self.active
    
    def add_log(self, module: str, message: str):
        log = AutoLog(
            id=self.log_counter,
            timestamp=datetime.now(),
            module=module,
            message=message
        )
        self.logs.append(log)
        self.log_counter += 1
    
    def update_health(self):
        # Simular variação nos valores de saúde
        if self.active:
            self.health.cpu_load = max(10, min(90, self.health.cpu_load + random.uniform(-5, 5)))
            self.health.memory_usage = max(20, min(80, self.health.memory_usage + random.uniform(-3, 3)))
            self.health.integrity_score = max(95, min(100, self.health.integrity_score + random.uniform(-0.1, 0.1)))
            self.health.network_latency = max(5, min(50, self.health.network_latency + random.uniform(-2, 2)))
            
            # Adicionar logs aleatórios quando ativo
            if random.random() > 0.7:
                modules = ["NEURAL", "QUANTUM", "MEMORY", "NETWORK", "SECURITY"]
                messages = [
                    "Processamento neural otimizado",
                    "Cálculo quântico em execução",
                    "Buffer de memória reorganizado",
                    "Conexão de rede estabilizada",
                    "Verificação de segurança concluída",
                    "Sincronização de dados realizada",
                    "Backup automático executado",
                    "Diagnóstico de sistema em andamento"
                ]
                self.add_log(
                    random.choice(modules),
                    random.choice(messages)
                )

class AutonomousSystemDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Autônomo Central")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0a0a0a")
        
        # Inicializar sistema
        self.autonomous_system = AutonomousSystem()
        self.active = False
        self.config = self.autonomous_system.config
        self.health = self.autonomous_system.health
        self.logs = self.autonomous_system.logs
        
        # Configurar UI
        self.setup_ui()
        
        # Iniciar atualizações
        self.start_updates()
        
        # Animação do cubo 3D
        self.cube_angle = 0
        self.animate_cube()
    
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
        
        # Ícone giratório
        self.icon_label = tk.Label(
            left_frame,
            text="⚙️",
            font=("Arial", 20),
            bg="#374151",
            fg="#d1d5db",
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=10
        )
        self.icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Texto
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(
            text_frame,
            text="SISTEMA AUTÔNOMO CENTRAL",
            font=("Arial", 16, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        tk.Label(
            text_frame,
            text="NÚCLEO DE PROCESSAMENTO • HOLOGRAPHIC CORE",
            font=("Courier", 10),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        # Botão de ligar/desligar
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        self.toggle_button = tk.Button(
            right_frame,
            text="INICIAR" if not self.active else "DESLIGAR",
            command=self.toggle_system,
            bg="#166534" if not self.active else "#991b1b",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.toggle_button.pack()
    
    def setup_content(self):
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Painel esquerdo: Holographic Core
        left_frame = tk.Frame(
            content_frame,
            bg="#000000",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Gradiente de fundo (simulado)
        gradient_canvas = tk.Canvas(left_frame, bg="#000000", highlightthickness=0)
        gradient_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Desenhar gradiente radial
        width = 400
        height = 400
        center_x = width // 2
        center_y = height // 2
        max_radius = min(width, height) // 2
        
        for r in range(max_radius, 0, -5):
            alpha = int(50 * (1 - r/max_radius))
            color = f'#0000ff{alpha:02x}'  # Azul com transparência
            gradient_canvas.create_oval(
                center_x - r, center_y - r,
                center_x + r, center_y + r,
                fill=color, outline=""
            )
        
        # Canvas para cubo 3D
        self.cube_canvas = tk.Canvas(
            left_frame,
            bg="#000000",
            highlightthickness=0,
            width=200,
            height=200
        )
        self.cube_canvas.pack()
        
        # Status do core
        status_frame = tk.Frame(left_frame, bg="#000000")
        status_frame.pack(pady=20)
        
        tk.Label(
            status_frame,
            text="CORE STATUS",
            font=("Courier", 12),
            fg="#22d3ee",
            bg="#000000"
        ).pack()
        
        self.status_label = tk.Label(
            status_frame,
            text="STANDBY",
            font=("Arial", 24, "bold"),
            fg="#9ca3af",
            bg="#000000"
        )
        self.status_label.pack(pady=(5, 0))
        
        self.integrity_label = tk.Label(
            status_frame,
            text=f"Integridade: {self.health.integrity_score:.1f}%",
            font=("Courier", 10),
            fg="#666666",
            bg="#000000"
        )
        self.integrity_label.pack(pady=(10, 0))
        
        # Painel direito: Métricas e Logs
        right_frame = tk.Frame(content_frame, bg="#0a0a0a")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Métricas
        metrics_frame = tk.Frame(right_frame, bg="#0a0a0a")
        metrics_frame.pack(fill=tk.X, pady=(0, 15))
        
        # CPU Load
        cpu_frame = tk.Frame(
            metrics_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            cpu_frame,
            text="⚙️ CPU LOAD",
            font=("Arial", 10),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        self.cpu_label = tk.Label(
            cpu_frame,
            text=f"{self.health.cpu_load:.1f}%",
            font=("Courier", 20, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.cpu_label.pack(pady=(5, 0))
        
        # Barra de CPU
        self.cpu_bar_frame = tk.Frame(cpu_frame, bg="#374151", height=6)
        self.cpu_bar_frame.pack(fill=tk.X, pady=(10, 0))
        self.cpu_bar_frame.pack_propagate(False)
        
        self.cpu_bar = tk.Frame(
            self.cpu_bar_frame,
            bg="#3b82f6",
            width=int(self.health.cpu_load * 2)  # Escala: 100% = 200px
        )
        self.cpu_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Memory Usage
        memory_frame = tk.Frame(
            metrics_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        memory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            memory_frame,
            text="💾 MEMORY",
            font=("Arial", 10),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        self.memory_label = tk.Label(
            memory_frame,
            text=f"{self.health.memory_usage:.1f}%",
            font=("Courier", 20, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.memory_label.pack(pady=(5, 0))
        
        # Barra de memória
        self.memory_bar_frame = tk.Frame(memory_frame, bg="#374151", height=6)
        self.memory_bar_frame.pack(fill=tk.X, pady=(10, 0))
        self.memory_bar_frame.pack_propagate(False)
        
        self.memory_bar = tk.Frame(
            self.memory_bar_frame,
            bg="#8b5cf6",
            width=int(self.health.memory_usage * 2)
        )
        self.memory_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Network Latency
        network_frame = tk.Frame(
            metrics_frame,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        network_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            network_frame,
            text="🌐 LATENCY",
            font=("Arial", 10),
            fg="#666666",
            bg="#1a1a2e"
        ).pack(anchor=tk.W)
        
        self.latency_label = tk.Label(
            network_frame,
            text=f"{self.health.network_latency:.0f}ms",
            font=("Courier", 20, "bold"),
            fg="#4ade80",
            bg="#1a1a2e"
        )
        self.latency_label.pack(pady=(5, 0))
        
        # Logs do sistema
        logs_frame = tk.Frame(
            right_frame,
            bg="#000000",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            logs_frame,
            text="⚡ SYSTEM_KERNEL_LOGS",
            font=("Courier", 11, "bold"),
            fg="#4ade80",
            bg="#000000"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Área de logs com scroll
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            bg="#000000",
            fg="#cccccc",
            font=("Courier", 9),
            height=15,
            relief=tk.FLAT,
            borderwidth=0,
            insertbackground="#cccccc"
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para cores
        self.logs_text.tag_config("timestamp", foreground="#666666")
        self.logs_text.tag_config("module", foreground="#a855f7")
        self.logs_text.tag_config("message", foreground="#d1d5db")
        
        # Adicionar logs existentes
        self.update_logs_display()
    
    def animate_cube(self):
        # Atualizar ângulo
        self.cube_angle += 1
        if self.cube_angle >= 360:
            self.cube_angle = 0
        
        # Limpar canvas
        self.cube_canvas.delete("all")
        
        # Configurações do cubo
        size = 80
        center_x = 100
        center_y = 100
        
        # Ângulos para rotação 3D
        angle_x = self.cube_angle * 0.0174533  # Convert to radians
        angle_y = self.cube_angle * 0.00872665
        
        # Definir vértices do cubo
        vertices = [
            [-size, -size, -size],
            [size, -size, -size],
            [size, size, -size],
            [-size, size, -size],
            [-size, -size, size],
            [size, -size, size],
            [size, size, size],
            [-size, size, size]
        ]
        
        # Rotacionar vértices
        rotated = []
        for vertex in vertices:
            x, y, z = vertex
            
            # Rotação em Y
            x1 = x * np.cos(angle_y) - z * np.sin(angle_y)
            z1 = x * np.sin(angle_y) + z * np.cos(angle_y)
            
            # Rotação em X
            y1 = y * np.cos(angle_x) - z1 * np.sin(angle_x)
            z2 = y * np.sin(angle_x) + z1 * np.cos(angle_x)
            
            # Projeção perspectiva
            factor = 300 / (300 + z2)
            x_proj = x1 * factor
            y_proj = y1 * factor
            
            rotated.append((center_x + x_proj, center_y + y_proj))
        
        # Definir faces do cubo
        faces = [
            [0, 1, 2, 3],  # Back
            [4, 5, 6, 7],  # Front
            [0, 1, 5, 4],  # Bottom
            [2, 3, 7, 6],  # Top
            [0, 3, 7, 4],  # Left
            [1, 2, 6, 5]   # Right
        ]
        
        # Cores das faces
        colors = [
            "#22d3ee50",  # Back - ciano
            "#22d3ee30",  # Front - ciano mais claro
            "#0ea5e950",  # Bottom - azul
            "#0ea5e950",  # Top - azul
            "#3b82f650",  # Left - azul médio
            "#3b82f650"   # Right - azul médio
        ]
        
        # Desenhar faces
        for i, face in enumerate(faces):
            points = [rotated[vertex] for vertex in face]
            self.cube_canvas.create_polygon(
                points,
                fill=colors[i] if self.active else "#66666620",
                outline="#22d3ee" if self.active else "#666666",
                width=1
            )
        
        # Núcleo interno (círculo pulsante)
        if self.active:
            pulse_size = 20 + 5 * np.sin(self.cube_angle * 0.1)
            self.cube_canvas.create_oval(
                center_x - pulse_size,
                center_y - pulse_size,
                center_x + pulse_size,
                center_y + pulse_size,
                fill="#ffffff",
                outline="",
                stipple="gray50"
            )
        
        # Agendar próxima animação
        self.root.after(30, self.animate_cube)
    
    def toggle_system(self):
        self.active = self.autonomous_system.toggle_system()
        
        # Atualizar UI
        self.toggle_button.config(
            text="DESLIGAR" if self.active else "INICIAR",
            bg="#991b1b" if self.active else "#166534"
        )
        
        self.status_label.config(
            text="ONLINE" if self.active else "STANDBY",
            fg="#ffffff" if self.active else "#9ca3af"
        )
        
        # Atualizar ícone giratório
        if self.active:
            self.start_icon_animation()
        else:
            self.stop_icon_animation()
    
    def start_icon_animation(self):
        self.rotate_icon(0)
    
    def stop_icon_animation(self):
        if hasattr(self, 'icon_animation_id'):
            self.root.after_cancel(self.icon_animation_id)
    
    def rotate_icon(self, angle):
        self.icon_label.config(text="⚙️")
        
        # Simular rotação mudando o caractere
        if self.active:
            self.icon_animation_id = self.root.after(100, lambda: self.rotate_icon((angle + 45) % 360))
    
    def update_logs_display(self):
        # Limpar logs
        self.logs_text.delete(1.0, tk.END)
        
        # Adicionar logs mais recentes
        for log in self.logs[-20:]:  # Últimos 20 logs
            timestamp = log.timestamp.strftime("%H:%M:%S")
            self.logs_text.insert(tk.END, f"[", "timestamp")
            self.logs_text.insert(tk.END, f"{timestamp}", "timestamp")
            self.logs_text.insert(tk.END, f"] ", "timestamp")
            self.logs_text.insert(tk.END, f"[{log.module}]", "module")
            self.logs_text.insert(tk.END, f" {log.message}\n", "message")
        
        # Scroll para o final
        self.logs_text.see(tk.END)
    
    def start_updates(self):
        def update_loop():
            while True:
                time.sleep(1)  # Atualizar a cada segundo
                
                # Atualizar status do sistema
                status = self.autonomous_system.get_status()
                self.active = status['active']
                self.config = status['config']
                self.health = status['health']
                self.logs = status['logs']
                
                # Atualizar métricas de saúde
                self.autonomous_system.update_health()
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_ui)
        
        # Iniciar thread de atualização
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def update_ui(self):
        # Atualizar métricas
        self.cpu_label.config(text=f"{self.health.cpu_load:.1f}%")
        self.cpu_bar.config(width=int(self.health.cpu_load * 2))
        
        self.memory_label.config(text=f"{self.health.memory_usage:.1f}%")
        self.memory_bar.config(width=int(self.health.memory_usage * 2))
        
        self.latency_label.config(text=f"{self.health.network_latency:.0f}ms")
        self.integrity_label.config(text=f"Integridade: {self.health.integrity_score:.1f}%")
        
        # Atualizar logs
        self.update_logs_display()

# Para o cubo 3D, precisamos do numpy
try:
    import numpy as np
except ImportError:
    print("Instalando numpy...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np

def main():
    root = tk.Tk()
    app = AutonomousSystemDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()