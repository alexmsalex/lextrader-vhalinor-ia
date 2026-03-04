import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
import sys
import platform
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
import threading
import subprocess
import json
import os

# Data Types
class ProjectProfileType(Enum):
    COMPLETO = "COMPLETO"
    IA_CORE = "IA_CORE"
    TRADING_ENGINE = "TRADING_ENGINE"
    QUANTUM_SIM = "QUANTUM_SIM"

class PackageStatus(Enum):
    INSTALLED = "INSTALLED"
    MISSING = "MISSING"
    OUTDATED = "OUTDATED"

class CriticalityLevel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class PackageCategory(Enum):
    AI = "AI"
    TRADING = "TRADING"
    SYSTEM = "SYSTEM"
    DATA = "DATA"
    QUANTUM = "QUANTUM"

@dataclass
class SystemInfo:
    os: str
    python_version: str
    node_version: str
    gpu_available: bool
    cuda_version: Optional[str]
    total_memory: str
    cpu_cores: int

@dataclass
class DependencyPackage:
    name: str
    category: PackageCategory
    criticality: CriticalityLevel
    required_version: str
    installed_version: Optional[str]
    status: PackageStatus
    description: str

@dataclass
class DependencyReport:
    score: float
    total_count: int
    installed_count: int
    missing_count: int
    outdated_count: int
    agi_diagnosis: str

# Mock Dependency Manager
class DependencyManager:
    def __init__(self):
        self.system_info = self.get_system_environment()
        self.package_db = self.load_package_database()
        
    def load_package_database(self) -> Dict[str, Dict[str, Any]]:
        """Load mock package database"""
        return {
            "tensorflow": {"category": "AI", "criticality": "HIGH", "version": "2.15.0"},
            "pytorch": {"category": "AI", "criticality": "HIGH", "version": "2.1.0"},
            "transformers": {"category": "AI", "criticality": "HIGH", "version": "4.35.0"},
            "stable-baselines3": {"category": "AI", "criticality": "MEDIUM", "version": "2.0.0"},
            
            "ccxt": {"category": "TRADING", "criticality": "HIGH", "version": "4.2.20"},
            "backtrader": {"category": "TRADING", "criticality": "MEDIUM", "version": "1.9.78.123"},
            "ta-lib": {"category": "TRADING", "criticality": "HIGH", "version": "0.4.26"},
            "vectorbt": {"category": "TRADING", "criticality": "MEDIUM", "version": "0.25.0"},
            
            "numpy": {"category": "SYSTEM", "criticality": "HIGH", "version": "1.24.0"},
            "pandas": {"category": "SYSTEM", "criticality": "HIGH", "version": "2.1.0"},
            "matplotlib": {"category": "SYSTEM", "criticality": "MEDIUM", "version": "3.8.0"},
            "scipy": {"category": "SYSTEM", "criticality": "MEDIUM", "version": "1.11.0"},
            
            "postgresql": {"category": "DATA", "criticality": "MEDIUM", "version": "14.0"},
            "redis": {"category": "DATA", "criticality": "MEDIUM", "version": "5.0.0"},
            "influxdb": {"category": "DATA", "criticality": "LOW", "version": "2.7.0"},
            "elasticsearch": {"category": "DATA", "criticality": "MEDIUM", "version": "8.11.0"},
            
            "qiskit": {"category": "QUANTUM", "criticality": "HIGH", "version": "0.45.0"},
            "cirq": {"category": "QUANTUM", "criticality": "MEDIUM", "version": "1.3.0"},
            "pennylane": {"category": "QUANTUM", "criticality": "MEDIUM", "version": "0.32.0"},
            "tensorflow-quantum": {"category": "QUANTUM", "criticality": "LOW", "version": "0.7.2"},
        }
    
    def get_system_environment(self) -> SystemInfo:
        """Get system environment information"""
        # Check for CUDA/GPU
        try:
            import torch
            gpu_available = torch.cuda.is_available()
            cuda_version = torch.version.cuda if gpu_available else None
        except:
            gpu_available = False
            cuda_version = None
        
        # Check Node.js
        try:
            node_result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            node_version = node_result.stdout.strip() if node_result.returncode == 0 else "Not Available"
        except:
            node_version = "Not Available"
        
        return SystemInfo(
            os=platform.system() + " " + platform.release(),
            python_version=platform.python_version(),
            node_version=node_version,
            gpu_available=gpu_available,
            cuda_version=cuda_version,
            total_memory=self.get_total_memory(),
            cpu_cores=os.cpu_count() or 4
        )
    
    def get_total_memory(self) -> str:
        """Get total system memory"""
        try:
            if platform.system() == "Linux":
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if line.startswith('MemTotal:'):
                            mem_kb = int(line.split()[1])
                            mem_gb = mem_kb / 1024 / 1024
                            return f"{mem_gb:.1f} GB"
            elif platform.system() == "Darwin":  # macOS
                result = subprocess.run(['sysctl', 'hw.memsize'], capture_output=True, text=True)
                mem_bytes = int(result.stdout.split()[1])
                mem_gb = mem_bytes / 1024 / 1024 / 1024
                return f"{mem_gb:.1f} GB"
        except:
            pass
        return "Unknown"
    
    def scan_system(self, profile: ProjectProfileType) -> List[DependencyPackage]:
        """Scan system for dependencies based on profile"""
        time.sleep(1)  # Simulate scanning
        
        packages = []
        profile_filters = {
            ProjectProfileType.COMPLETO: ["AI", "TRADING", "SYSTEM", "DATA", "QUANTUM"],
            ProjectProfileType.IA_CORE: ["AI", "SYSTEM"],
            ProjectProfileType.TRADING_ENGINE: ["TRADING", "SYSTEM", "DATA"],
            ProjectProfileType.QUANTUM_SIM: ["QUANTUM", "SYSTEM"]
        }
        
        categories = profile_filters.get(profile, ["AI", "TRADING", "SYSTEM", "DATA", "QUANTUM"])
        
        for pkg_name, pkg_info in self.package_db.items():
            category = PackageCategory(pkg_info["category"])
            if category.value in categories:
                # Simulate random installation status
                status_roll = random.random()
                if status_roll < 0.6:
                    status = PackageStatus.INSTALLED
                    installed_version = pkg_info["version"]
                elif status_roll < 0.8:
                    status = PackageStatus.OUTDATED
                    installed_version = self.get_older_version(pkg_info["version"])
                else:
                    status = PackageStatus.MISSING
                    installed_version = None
                
                packages.append(DependencyPackage(
                    name=pkg_name,
                    category=category,
                    criticality=CriticalityLevel(pkg_info["criticality"]),
                    required_version=pkg_info["version"],
                    installed_version=installed_version,
                    status=status,
                    description=f"Essential {category.value} package for {profile.value} profile"
                ))
        
        return packages
    
    def get_older_version(self, version: str) -> str:
        """Generate an older version for outdated packages"""
        parts = version.split('.')
        if len(parts) >= 3:
            major, minor, patch = parts[:3]
            patch = str(max(0, int(patch) - random.randint(1, 3)))
            return f"{major}.{minor}.{patch}"
        return version
    
    def generate_report(self, packages: List[DependencyPackage]) -> DependencyReport:
        """Generate dependency report"""
        total = len(packages)
        installed = sum(1 for p in packages if p.status == PackageStatus.INSTALLED)
        missing = sum(1 for p in packages if p.status == PackageStatus.MISSING)
        outdated = sum(1 for p in packages if p.status == PackageStatus.OUTDATED)
        
        score = (installed / total * 100) if total > 0 else 100
        
        # AGI Diagnosis
        if score == 100:
            diagnosis = "Sistema em perfeita integridade"
        elif score >= 80:
            diagnosis = "Sistema operacional com leve otimização recomendada"
        elif score >= 60:
            diagnosis = "Sistema funcional com dependências críticas atendidas"
        elif score >= 40:
            diagnosis = "Sistema comprometido - ações recomendadas"
        else:
            diagnosis = "Sistema crítico - intervenção imediata necessária"
        
        return DependencyReport(
            score=score,
            total_count=total,
            installed_count=installed,
            missing_count=missing,
            outdated_count=outdated,
            agi_diagnosis=diagnosis
        )
    
    def install_package(self, package_name: str) -> bool:
        """Mock package installation"""
        time.sleep(2)  # Simulate installation time
        return True
    
    def fix_all(self, packages: List[DependencyPackage]) -> bool:
        """Mock fix all packages"""
        time.sleep(3)  # Simulate fixing all
        return True

# Main Application
class DependencyDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("GERENCIADOR DE DEPENDÊNCIAS")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0a0a0a")
        
        # Initialize services
        self.dependency_manager = DependencyManager()
        
        # State variables
        self.profile = ProjectProfileType.COMPLETO
        self.dependencies: List[DependencyPackage] = []
        self.report: Optional[DependencyReport] = None
        self.is_scanning = False
        self.installing: Optional[str] = None
        self.sys_info = self.dependency_manager.get_system_environment()
        
        # Setup UI
        self.setup_ui()
        
        # Initial scan
        self.scan_dependencies()
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Main container
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
        tk.Label(icon_frame, text="📦", font=("Arial", 16), 
                bg="#064e3b", fg="#10b981").pack()
        
        # Text
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(text_frame, text="GERENCIADOR DE DEPENDÊNCIAS", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#1a1a2e").pack(anchor=tk.W)
        
        tk.Label(text_frame, text="SYSTEM INTEGRITY • PACKAGE HEALTH", 
                font=("Courier", 10), fg="#10b981", bg="#1a1a2e").pack(anchor=tk.W)
        
        # Right side: Controls
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        # Profile selector
        profile_frame = tk.Frame(right_frame, bg="black", relief=tk.RAISED, 
                                borderwidth=1, padx=1, pady=1)
        profile_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        profiles = [
            ("COMPLETO", ProjectProfileType.COMPLETO),
            ("IA CORE", ProjectProfileType.IA_CORE),
            ("TRADING ENGINE", ProjectProfileType.TRADING_ENGINE),
            ("QUANTUM SIM", ProjectProfileType.QUANTUM_SIM)
        ]
        
        for text, profile_type in profiles:
            btn = tk.Button(
                profile_frame,
                text=text,
                command=lambda pt=profile_type: self.switch_profile(pt),
                font=("Arial", 8),
                bg="#1e40af" if self.profile == profile_type else "black",
                fg="white" if self.profile == profile_type else "#666666",
                activebackground="#1d4ed8",
                activeforeground="white",
                padx=10,
                pady=5,
                borderwidth=0
            )
            btn.pack(side=tk.LEFT)
        
        # Scan button
        self.scan_button = tk.Button(
            right_frame,
            text="⟳",
            command=self.scan_dependencies,
            font=("Arial", 14),
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            padx=10,
            pady=5,
            relief=tk.RAISED,
            state="normal"
        )
        self.scan_button.pack()
    
    def setup_content(self):
        """Setup the main content area"""
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left column: Stats and System Info
        left_panel = tk.Frame(content_frame, bg="#0a0a0a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Health Score
        self.setup_health_score(left_panel)
        
        # Environment Info
        self.setup_environment_info(left_panel)
        
        # Right column: Package List
        right_panel = tk.Frame(content_frame, bg="#0a0a0a")
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.setup_package_list(right_panel)
    
    def setup_health_score(self, parent):
        """Setup health score panel"""
        health_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        health_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Decorative icon
        icon_frame = tk.Frame(health_frame, bg="#1a1a2e")
        icon_frame.pack(anchor=tk.NE)
        
        tk.Label(
            icon_frame,
            text="🛡️",
            font=("Arial", 24),
            fg="#10b981",
            bg="#1a1a2e",
            alpha=0.1
        ).pack()
        
        # Title
        tk.Label(
            health_frame,
            text="Integridade do Sistema",
            font=("Arial", 10, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(pady=(0, 10))
        
        # Score
        self.score_label = tk.Label(
            health_frame,
            text="0%",
            font=("Courier", 36, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.score_label.pack(pady=(0, 5))
        
        # Diagnosis
        self.diagnosis_label = tk.Label(
            health_frame,
            text="Escaneando sistema...",
            font=("Arial", 9),
            fg="#fbbf24",
            bg="#1a1a2e"
        )
        self.diagnosis_label.pack()
    
    def setup_environment_info(self, parent):
        """Setup environment information panel"""
        env_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        env_frame.pack(fill=tk.X)
        
        # Title
        title_frame = tk.Frame(env_frame, bg="#1a1a2e")
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            title_frame,
            text="🖥️",
            font=("Arial", 14),
            fg="#3b82f6",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            title_frame,
            text="AMBIENTE DE EXECUÇÃO",
            font=("Arial", 10, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        # System info grid
        info_frame = tk.Frame(env_frame, bg="#1a1a2e")
        info_frame.pack(fill=tk.X)
        
        # OS Kernel
        os_frame = tk.Frame(info_frame, bg="#1a1a2e")
        os_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            os_frame,
            text="OS Kernel",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            os_frame,
            text=self.sys_info.os,
            font=("Courier", 9, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
        
        # Python Runtime
        python_frame = tk.Frame(info_frame, bg="#1a1a2e")
        python_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            python_frame,
            text="Python Runtime",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            python_frame,
            text=self.sys_info.python_version,
            font=("Courier", 9, "bold"),
            fg="#3b82f6",
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
        
        # Node Bridge
        node_frame = tk.Frame(info_frame, bg="#1a1a2e")
        node_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            node_frame,
            text="Node Bridge",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            node_frame,
            text=self.sys_info.node_version,
            font=("Courier", 9, "bold"),
            fg="#10b981",
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
        
        # GPU Acceleration
        gpu_frame = tk.Frame(info_frame, bg="#1a1a2e")
        gpu_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            gpu_frame,
            text="GPU Acceleration",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        gpu_text = "ENABLED (CUDA)" if self.sys_info.gpu_available else "DISABLED"
        gpu_color = "#10b981" if self.sys_info.gpu_available else "#ef4444"
        tk.Label(
            gpu_frame,
            text=gpu_text,
            font=("Courier", 9, "bold"),
            fg=gpu_color,
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
        
        # CPU Cores
        cpu_frame = tk.Frame(info_frame, bg="#1a1a2e")
        cpu_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            cpu_frame,
            text="CPU Cores",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            cpu_frame,
            text=str(self.sys_info.cpu_cores),
            font=("Courier", 9, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
        
        # Total Memory
        mem_frame = tk.Frame(info_frame, bg="#1a1a2e")
        mem_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            mem_frame,
            text="Total Memory",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            mem_frame,
            text=self.sys_info.total_memory,
            font=("Courier", 9, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side=tk.RIGHT)
    
    def setup_package_list(self, parent):
        """Setup package list panel"""
        list_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(list_frame, bg="#1a1a2e", height=50)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        header_frame.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(header_frame, bg="#1a1a2e")
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(
            title_frame,
            text="📦",
            font=("Arial", 14),
            fg="#3b82f6",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.package_count_label = tk.Label(
            title_frame,
            text="LISTA DE PACOTES (0)",
            font=("Arial", 10, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        )
        self.package_count_label.pack(side=tk.LEFT)
        
        # Fix All button
        self.fix_all_button = tk.Button(
            header_frame,
            text="🔧 AUTO-CORREÇÃO (0)",
            command=self.fix_all_packages,
            font=("Arial", 9, "bold"),
            bg="#065f46",
            fg="#10b981",
            activebackground="#059669",
            activeforeground="#a7f3d0",
            padx=15,
            pady=5,
            relief=tk.RAISED,
            state="disabled"
        )
        self.fix_all_button.pack(side=tk.RIGHT)
        
        # Package list container
        self.package_container = tk.Frame(list_frame, bg="#0a0a0a")
        self.package_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_package_card(self, parent, pkg: DependencyPackage):
        """Create a package card widget"""
        card_frame = tk.Frame(
            parent,
            bg="#0a0a0a",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        card_frame.pack(fill=tk.X, pady=5)
        
        # Left side: Package info
        left_frame = tk.Frame(card_frame, bg="#0a0a0a")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Icon and name
        name_frame = tk.Frame(left_frame, bg="#0a0a0a")
        name_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Category icon
        icons = {
            PackageCategory.AI: "🧠",
            PackageCategory.TRADING: "📈",
            PackageCategory.SYSTEM: "💻",
            PackageCategory.DATA: "🗄️",
            PackageCategory.QUANTUM: "⚛️"
        }
        
        icon_color = {
            PackageCategory.AI: "#a855f7",
            PackageCategory.TRADING: "#10b981",
            PackageCategory.SYSTEM: "#6b7280",
            PackageCategory.DATA: "#fbbf24",
            PackageCategory.QUANTUM: "#0ea5e9"
        }
        
        tk.Label(
            name_frame,
            text=icons.get(pkg.category, "📦"),
            font=("Arial", 16),
            fg=icon_color.get(pkg.category, "#9ca3af"),
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Package name and criticality
        text_frame = tk.Frame(name_frame, bg="#0a0a0a")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        name_critical_frame = tk.Frame(text_frame, bg="#0a0a0a")
        name_critical_frame.pack(fill=tk.X)
        
        tk.Label(
            name_critical_frame,
            text=pkg.name,
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT)
        
        # Criticality icon
        crit_icons = {
            CriticalityLevel.HIGH: "🔴",
            CriticalityLevel.MEDIUM: "🟡",
            CriticalityLevel.LOW: "🔵"
        }
        
        tk.Label(
            name_critical_frame,
            text=crit_icons.get(pkg.criticality, "⚪"),
            font=("Arial", 12),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Version info
        version_frame = tk.Frame(text_frame, bg="#0a0a0a")
        version_frame.pack(fill=tk.X, pady=(2, 0))
        
        tk.Label(
            version_frame,
            text=f"Req: {pkg.required_version} | Inst: {pkg.installed_version or 'N/A'}",
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#0a0a0a"
        ).pack(anchor=tk.W)
        
        # Right side: Status and actions
        right_frame = tk.Frame(card_frame, bg="#0a0a0a")
        right_frame.pack(side=tk.RIGHT)
        
        # Status badge
        status_colors = {
            PackageStatus.INSTALLED: ("#10b981", "#065f46"),
            PackageStatus.MISSING: ("#ef4444", "#7f1d1d"),
            PackageStatus.OUTDATED: ("#fbbf24", "#854d0e")
        }
        
        text_color, bg_color = status_colors.get(pkg.status, ("#9ca3af", "#374151"))
        
        status_frame = tk.Frame(
            right_frame,
            bg=bg_color,
            relief=tk.RAISED,
            borderwidth=1,
            padx=10,
            pady=5
        )
        status_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            status_frame,
            text=pkg.status.value,
            font=("Arial", 9, "bold"),
            fg=text_color,
            bg=bg_color
        ).pack()
        
        # Install button (if not installed)
        if pkg.status != PackageStatus.INSTALLED:
            install_btn = tk.Button(
                right_frame,
                text="⬇️",
                command=lambda p=pkg.name: self.install_package(p),
                font=("Arial", 12),
                bg="#374151",
                fg="#9ca3af",
                activebackground="#4b5563",
                activeforeground="#ffffff",
                padx=10,
                pady=5,
                relief=tk.RAISED,
                state="normal" if not self.installing else "disabled"
            )
            install_btn.pack(side=tk.LEFT)
    
    def switch_profile(self, profile: ProjectProfileType):
        """Switch project profile"""
        self.profile = profile
        self.scan_dependencies()
    
    def scan_dependencies(self):
        """Scan system dependencies"""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        self.scan_button.config(state="disabled", text="⏳")
        
        # Clear package container
        for widget in self.package_container.winfo_children():
            widget.destroy()
        
        # Show scanning message
        scanning_frame = tk.Frame(self.package_container, bg="#0a0a0a")
        scanning_frame.pack(expand=True, fill=tk.BOTH, pady=50)
        
        tk.Label(
            scanning_frame,
            text="🔍",
            font=("Arial", 48),
            fg="#fbbf24",
            bg="#0a0a0a"
        ).pack(pady=(0, 20))
        
        tk.Label(
            scanning_frame,
            text="ESCANEANDO SISTEMA...",
            font=("Courier", 14, "bold"),
            fg="#fbbf24",
            bg="#0a0a0a"
        ).pack()
        
        # Run scan in separate thread
        def scan_thread():
            # Simulate scanning delay
            time.sleep(2)
            
            # Get dependencies
            dependencies = self.dependency_manager.scan_system(self.profile)
            report = self.dependency_manager.generate_report(dependencies)
            
            # Update UI in main thread
            self.root.after(0, self.update_scan_results, dependencies, report)
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def update_scan_results(self, dependencies: List[DependencyPackage], report: DependencyReport):
        """Update UI with scan results"""
        self.is_scanning = False
        self.dependencies = dependencies
        self.report = report
        
        # Update scan button
        self.scan_button.config(state="normal", text="⟳")
        
        # Clear package container
        for widget in self.package_container.winfo_children():
            widget.destroy()
        
        # Update health score
        score_color = "#10b981" if report.score >= 80 else "#fbbf24" if report.score >= 60 else "#ef4444"
        self.score_label.config(text=f"{report.score:.0f}%", fg=score_color)
        self.diagnosis_label.config(text=report.agi_diagnosis, 
                                  fg="#10b981" if report.score == 100 else 
                                      "#fbbf24" if report.score >= 60 else "#ef4444")
        
        # Update package count
        self.package_count_label.config(text=f"LISTA DE PACOTES ({len(dependencies)})")
        
        # Update fix all button
        if report.missing_count > 0:
            self.fix_all_button.config(
                text=f"🔧 AUTO-CORREÇÃO ({report.missing_count})",
                state="normal"
            )
        else:
            self.fix_all_button.config(
                text="🔧 AUTO-CORREÇÃO (0)",
                state="disabled"
            )
        
        # Create package cards
        if dependencies:
            # Create scrollable container
            canvas = tk.Canvas(self.package_container, bg="#0a0a0a", highlightthickness=0)
            scrollbar = tk.Scrollbar(self.package_container, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Add package cards
            for pkg in dependencies:
                self.create_package_card(scrollable_frame, pkg)
        else:
            # No packages message
            empty_frame = tk.Frame(self.package_container, bg="#0a0a0a")
            empty_frame.pack(expand=True, fill=tk.BOTH, pady=50)
            
            tk.Label(
                empty_frame,
                text="📦",
                font=("Arial", 48),
                fg="#666666",
                bg="#0a0a0a"
            ).pack(pady=(0, 20))
            
            tk.Label(
                empty_frame,
                text="NENHUM PACOTE ENCONTRADO",
                font=("Courier", 14, "bold"),
                fg="#666666",
                bg="#0a0a0a"
            ).pack()
    
    def install_package(self, package_name: str):
        """Install a package"""
        if self.installing:
            return
        
        self.installing = package_name
        
        # Run installation in separate thread
        def install_thread():
            success = self.dependency_manager.install_package(package_name)
            
            # Update UI in main thread
            self.root.after(0, self.finish_installation, package_name, success)
        
        threading.Thread(target=install_thread, daemon=True).start()
    
# Data Types
class ProjectProfileType(Enum):
    COMPLETO = "COMPLETO"
    IA_CORE = "IA_CORE"
    TRADING_ENGINE = "TRADING_ENGINE"
    QUANTUM_SIM = "QUANTUM_SIM"

class DependencyStatus(Enum):
    INSTALLED = "INSTALLED"
    MISSING = "MISSING"
    OUTDATED = "OUTDATED"

class CriticalityLevel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class PackageCategory(Enum):
    AI = "AI"
    TRADING = "TRADING"
    SYSTEM = "SYSTEM"
    DATA = "DATA"
    QUANTUM = "QUANTUM"

@dataclass
class DependencyPackage:
    name: str
    category: PackageCategory
    required_version: str
    installed_version: Optional[str]
    status: DependencyStatus
    criticality: CriticalityLevel
    description: str

@dataclass
class DependencyReport:
    score: float
    agi_diagnosis: str
    missing_count: int
    outdated_count: int
    total_dependencies: int

@dataclass
class SystemInfo:
    os: str
    python_version: str
    node_version: str
    gpu_available: bool
    cpu_cores: int
    total_memory: str

# Mock Dependency Manager Service
class DependencyManager:
    def __init__(self):
        self.packages_data = {
            "COMPLETO": self._get_complete_packages(),
            "IA_CORE": self._get_ai_core_packages(),
            "TRADING_ENGINE": self._get_trading_packages(),
            "QUANTUM_SIM": self._get_quantum_packages()
        }
    
    def _get_complete_packages(self) -> List[DependencyPackage]:
        return [
            DependencyPackage(
                name="torch",
                category=PackageCategory.AI,
                required_version="2.0.0+",
                installed_version="2.1.0" if random.random() > 0.3 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.3 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.HIGH,
                description="PyTorch - Framework de Deep Learning"
            ),
            DependencyPackage(
                name="tensorflow",
                category=PackageCategory.AI,
                required_version="2.13.0+",
                installed_version="2.12.0" if random.random() > 0.4 else None,
                status=DependencyStatus.OUTDATED if random.random() > 0.4 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.HIGH,
                description="TensorFlow - Machine Learning Framework"
            ),
            DependencyPackage(
                name="transformers",
                category=PackageCategory.AI,
                required_version="4.35.0+",
                installed_version="4.34.0" if random.random() > 0.5 else "4.35.2",
                status=DependencyStatus.OUTDATED if random.random() > 0.5 else DependencyStatus.INSTALLED,
                criticality=CriticalityLevel.MEDIUM,
                description="Hugging Face Transformers - Modelos LLM"
            ),
            DependencyPackage(
                name="ta-lib",
                category=PackageCategory.TRADING,
                required_version="0.4.28",
                installed_version="0.4.28" if random.random() > 0.2 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.2 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.HIGH,
                description="TA-Lib - Análise Técnica para Trading"
            ),
            DependencyPackage(
                name="ccxt",
                category=PackageCategory.TRADING,
                required_version="4.1.0+",
                installed_version="4.1.5" if random.random() > 0.3 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.3 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.HIGH,
                description="CCXT - Biblioteca de Exchanges Cripto"
            ),
            DependencyPackage(
                name="backtrader",
                category=PackageCategory.TRADING,
                required_version="1.9.78.123",
                installed_version="1.9.78.123" if random.random() > 0.4 else "1.9.70.0",
                status=DependencyStatus.INSTALLED if random.random() > 0.4 else DependencyStatus.OUTDATED,
                criticality=CriticalityLevel.MEDIUM,
                description="Backtrader - Backtesting Trading"
            ),
            DependencyPackage(
                name="qiskit",
                category=PackageCategory.QUANTUM,
                required_version="0.44.0+",
                installed_version="0.44.1" if random.random() > 0.5 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.5 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.MEDIUM,
                description="Qiskit - Computação Quântica"
            ),
            DependencyPackage(
                name="pennylane",
                category=PackageCategory.QUANTUM,
                required_version="0.32.0",
                installed_version="0.32.0" if random.random() > 0.6 else "0.31.0",
                status=DependencyStatus.INSTALLED if random.random() > 0.6 else DependencyStatus.OUTDATED,
                criticality=CriticalityLevel.LOW,
                description="PennyLane - Machine Learning Quântico"
            ),
            DependencyPackage(
                name="redis",
                category=PackageCategory.SYSTEM,
                required_version="5.0.1",
                installed_version="5.0.1" if random.random() > 0.3 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.3 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.HIGH,
                description="Redis - Cache e Mensageria"
            ),
            DependencyPackage(
                name="docker",
                category=PackageCategory.SYSTEM,
                required_version="6.1.0+",
                installed_version="6.1.5" if random.random() > 0.4 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.4 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.MEDIUM,
                description="Docker SDK - Containerização"
            ),
            DependencyPackage(
                name="fastapi",
                category=PackageCategory.SYSTEM,
                required_version="0.104.0",
                installed_version="0.104.0" if random.random() > 0.5 else "0.103.0",
                status=DependencyStatus.INSTALLED if random.random() > 0.5 else DependencyStatus.OUTDATED,
                criticality=CriticalityLevel.MEDIUM,
                description="FastAPI - Framework Web Assíncrono"
            ),
            DependencyPackage(
                name="pandas",
                category=PackageCategory.DATA,
                required_version="2.1.0+",
                installed_version="2.1.3" if random.random() > 0.2 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.2 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.HIGH,
                description="Pandas - Manipulação de Dados"
            ),
            DependencyPackage(
                name="numpy",
                category=PackageCategory.DATA,
                required_version="1.24.0+",
                installed_version="1.24.3" if random.random() > 0.1 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.1 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.HIGH,
                description="NumPy - Computação Numérica"
            ),
            DependencyPackage(
                name="sqlalchemy",
                category=PackageCategory.DATA,
                required_version="2.0.20+",
                installed_version="2.0.20" if random.random() > 0.4 else "2.0.15",
                status=DependencyStatus.INSTALLED if random.random() > 0.4 else DependencyStatus.OUTDATED,
                criticality=CriticalityLevel.MEDIUM,
                description="SQLAlchemy - ORM Database"
            ),
            DependencyPackage(
                name="plotly",
                category=PackageCategory.DATA,
                required_version="5.17.0",
                installed_version="5.17.0" if random.random() > 0.5 else None,
                status=DependencyStatus.INSTALLED if random.random() > 0.5 else DependencyStatus.MISSING,
                criticality=CriticalityLevel.LOW,
                description="Plotly - Visualização Interativa"
            )
        ]
    
    def _get_ai_core_packages(self) -> List[DependencyPackage]:
        return [pkg for pkg in self._get_complete_packages() 
                if pkg.category in [PackageCategory.AI, PackageCategory.DATA]]
    
    def _get_trading_packages(self) -> List[DependencyPackage]:
        return [pkg for pkg in self._get_complete_packages() 
                if pkg.category in [PackageCategory.TRADING, PackageCategory.DATA]]
    
    def _get_quantum_packages(self) -> List[DependencyPackage]:
        return [pkg for pkg in self._get_complete_packages() 
                if pkg.category in [PackageCategory.QUANTUM, PackageCategory.AI]]
    
    def scan_system(self, profile: ProjectProfileType) -> List[DependencyPackage]:
        """Mock system scan - returns packages for given profile"""
        time.sleep(0.5)  # Simulate scan time
        return self.packages_data.get(profile.value, [])
    
    def generate_report(self, packages: List[DependencyPackage]) -> DependencyReport:
        """Generate dependency health report"""
        total = len(packages)
        missing = sum(1 for p in packages if p.status == DependencyStatus.MISSING)
        outdated = sum(1 for p in packages if p.status == DependencyStatus.OUTDATED)
        installed = total - missing - outdated
        
        score = (installed / total * 100) if total > 0 else 100
        
        if score == 100:
            diagnosis = "Sistema totalmente otimizado"
        elif score >= 80:
            diagnosis = "Sistema funcional com pequenas otimizações necessárias"
        elif score >= 60:
            diagnosis = "Sistema operacional, recomenda-se atualizações"
        else:
            diagnosis = "Sistema crítico, instalação de dependências necessária"
        
        return DependencyReport(
            score=score,
            agi_diagnosis=diagnosis,
            missing_count=missing,
            outdated_count=outdated,
            total_dependencies=total
        )
    
    def install_package(self, package_name: str):
        """Mock package installation"""
        time.sleep(1)  # Simulate installation time
    
    def fix_all(self, packages: List[DependencyPackage]):
        """Mock fix all missing packages"""
        time.sleep(2)  # Simulate fix time
    
    def get_system_environment(self) -> SystemInfo:
        """Get system environment information"""
        # Detect OS
        os_name = platform.system()
        if os_name == "Darwin":
            os_display = "macOS 13.5+"
        elif os_name == "Linux":
            os_display = "Linux (Ubuntu 22.04 LTS)"
        else:
            os_display = "Windows 11"
        
        # Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        # Mock other info
        return SystemInfo(
            os=os_display,
            python_version=python_version,
            node_version="18.17.0",
            gpu_available=random.choice([True, False]),
            cpu_cores=os.cpu_count() or 8,
            total_memory=f"{random.randint(16, 64)}GB"
        )

# Main Application
class DependencyDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("GERENCIADOR DE DEPENDÊNCIAS")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a0a")
        
        # Initialize services
        self.dependency_manager = DependencyManager()
        
        # State variables
        self.profile = ProjectProfileType.COMPLETO
        self.dependencies: List[DependencyPackage] = []
        self.report: Optional[DependencyReport] = None
        self.is_scanning = False
        self.installing: Optional[str] = None
        self.sys_info = self.dependency_manager.get_system_environment()
        
        # Setup UI
        self.setup_ui()
        
        # Initial scan
        self.scan_system()
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header()
        
        # Main content
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
        tk.Label(icon_frame, text="📦", font=("Arial", 16), 
                bg="#064e3b", fg="#10b981").pack()
        
        # Text
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(text_frame, text="GERENCIADOR DE DEPENDÊNCIAS", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#1a1a2e").pack(anchor=tk.W)
        
        tk.Label(text_frame, text="SYSTEM INTEGRITY • PACKAGE HEALTH", 
                font=("Courier", 10), fg="#10b981", bg="#1a1a2e").pack(anchor=tk.W)
        
        # Right side: Controls
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        # Profile selector
        profile_frame = tk.Frame(right_frame, bg="black", relief=tk.RAISED, 
                                borderwidth=1, padx=1, pady=1)
        profile_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        profiles = [
            ("COMPLETO", ProjectProfileType.COMPLETO),
            ("IA CORE", ProjectProfileType.IA_CORE),
            ("TRADING ENGINE", ProjectProfileType.TRADING_ENGINE),
            ("QUANTUM SIM", ProjectProfileType.QUANTUM_SIM)
        ]
        
        for text, profile_type in profiles:
            btn = tk.Button(
                profile_frame,
                text=text,
                command=lambda pt=profile_type: self.switch_profile(pt),
                font=("Arial", 8),
                bg="#1e3a8a" if self.profile == profile_type else "black",
                fg="white" if self.profile == profile_type else "#666666",
                activebackground="#1e40af",
                activeforeground="white",
                padx=10,
                pady=5,
                borderwidth=0
            )
            btn.pack(side=tk.LEFT)
        
        # Scan button
        self.scan_button = tk.Button(
            right_frame,
            text="🔄",
            command=self.scan_system,
            font=("Arial", 12),
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            padx=10,
            pady=8,
            relief=tk.RAISED,
            borderwidth=1,
            state="normal"
        )
        self.scan_button.pack(side=tk.LEFT)
    
    def setup_content(self):
        """Setup the main content area"""
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left column: Stats & System Info
        left_column = tk.Frame(content_frame, bg="#0a0a0a")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.setup_left_column(left_column)
        
        # Right column: Package List
        right_column = tk.Frame(content_frame, bg="#0a0a0a")
        right_column.grid(row=0, column=1, sticky="nsew")
        
        self.setup_right_column(right_column)
    
    def setup_left_column(self, parent):
        """Setup left column with stats and system info"""
        # Health Score
        health_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        health_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Decorative icon
        icon_frame = tk.Frame(health_frame, bg="#1a1a2e")
        icon_frame.pack(anchor=tk.NE)
        tk.Label(icon_frame, text="🛡️", font=("Arial", 24), 
                fg="#ffffff", bg="#1a1a2e", alpha=0.1).pack()
        
        # Title
        tk.Label(
            health_frame,
            text="Integridade do Sistema",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(pady=(0, 10))
        
        # Score
        self.score_label = tk.Label(
            health_frame,
            text="100%",
            font=("Courier", 32, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.score_label.pack(pady=(0, 5))
        
        # Diagnosis
        self.diagnosis_label = tk.Label(
            health_frame,
            text="Sistema totalmente otimizado",
            font=("Arial", 9),
            fg="#10b981",
            bg="#1a1a2e"
        )
        self.diagnosis_label.pack()
        
        # Chart placeholder (simplified - could use matplotlib for real chart)
        chart_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(
            chart_frame,
            text="📊 COBERTURA POR MÓDULO",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Simple text-based chart simulation
        chart_text = scrolledtext.ScrolledText(
            chart_frame,
            bg="#1a1a2e",
            fg="#d1d5db",
            font=("Courier", 9),
            height=10,
            borderwidth=0,
            highlightthickness=0
        )
        chart_text.pack(fill=tk.BOTH, expand=True)
        chart_text.insert(tk.END, "AI: ████████████████████ 95%\n")
        chart_text.insert(tk.END, "TRADING: ███████████████ 85%\n")
        chart_text.insert(tk.END, "SYSTEM: ██████████████████ 90%\n")
        chart_text.insert(tk.END, "DATA: ████████████████████ 96%\n")
        chart_text.insert(tk.END, "QUANTUM: ████████████ 70%\n")
        chart_text.config(state='disabled')
        
        # Environment Info
        env_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=20
        )
        env_frame.pack(fill=tk.X)
        
        tk.Label(
            env_frame,
            text="🖥️ AMBIENTE DE EXECUÇÃO",
            font=("Arial", 9, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # System info grid
        self.setup_system_info(env_frame)
    
    def setup_system_info(self, parent):
        """Setup system information display"""
        info_frame = tk.Frame(parent, bg="#1a1a2e")
        info_frame.pack(fill=tk.X)
        
        # OS Kernel
        os_frame = tk.Frame(info_frame, bg="#1a1a2e")
        os_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            os_frame,
            text="OS Kernel",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.os_label = tk.Label(
            os_frame,
            text=self.sys_info.os,
            font=("Courier", 9),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.os_label.pack(side=tk.RIGHT)
        
        # Python Runtime
        python_frame = tk.Frame(info_frame, bg="#1a1a2e")
        python_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            python_frame,
            text="Python Runtime",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.python_label = tk.Label(
            python_frame,
            text=self.sys_info.python_version,
            font=("Courier", 9),
            fg="#3b82f6",
            bg="#1a1a2e"
        )
        self.python_label.pack(side=tk.RIGHT)
        
        # Node Bridge
        node_frame = tk.Frame(info_frame, bg="#1a1a2e")
        node_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            node_frame,
            text="Node Bridge",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.node_label = tk.Label(
            node_frame,
            text=self.sys_info.node_version,
            font=("Courier", 9),
            fg="#10b981",
            bg="#1a1a2e"
        )
        self.node_label.pack(side=tk.RIGHT)
        
        # GPU Acceleration
        gpu_frame = tk.Frame(info_frame, bg="#1a1a2e")
        gpu_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            gpu_frame,
            text="GPU Acceleration",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        gpu_status = "ENABLED (CUDA)" if self.sys_info.gpu_available else "DISABLED"
        gpu_color = "#10b981" if self.sys_info.gpu_available else "#ef4444"
        
        self.gpu_label = tk.Label(
            gpu_frame,
            text=gpu_status,
            font=("Courier", 9),
            fg=gpu_color,
            bg="#1a1a2e"
        )
        self.gpu_label.pack(side=tk.RIGHT)
        
        # CPU Cores
        cpu_frame = tk.Frame(info_frame, bg="#1a1a2e")
        cpu_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            cpu_frame,
            text="CPU Cores",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.cpu_label = tk.Label(
            cpu_frame,
            text=str(self.sys_info.cpu_cores),
            font=("Courier", 9),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.cpu_label.pack(side=tk.RIGHT)
        
        # Total Memory
        mem_frame = tk.Frame(info_frame, bg="#1a1a2e")
        mem_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            mem_frame,
            text="Total Memory",
            font=("Arial", 8),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        self.mem_label = tk.Label(
            mem_frame,
            text=self.sys_info.total_memory,
            font=("Courier", 9),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        self.mem_label.pack(side=tk.RIGHT)
    
    def setup_right_column(self, parent):
        """Setup right column with package list"""
        # Main package frame
        package_frame = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=1
        )
        package_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(package_frame, bg="#1a1a2e", padx=20, pady=15)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="📦 LISTA DE PACOTES (0)",
            font=("Arial", 10, "bold"),
            fg="#9ca3af",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT)
        
        # Fix All button
        self.fix_button = tk.Button(
            header_frame,
            text="🔨 AUTO-CORREÇÃO (0)",
            command=self.fix_all_packages,
            font=("Arial", 9),
            bg="#065f46",
            fg="#10b981",
            activebackground="#047857",
            activeforeground="#a7f3d0",
            padx=15,
            pady=5,
            relief=tk.RAISED,
            borderwidth=1,
            state="disabled"
        )
        self.fix_button.pack(side=tk.RIGHT)
        
        # Package list
        self.setup_package_list(package_frame)
    
    def setup_package_list(self, parent):
        """Setup scrollable package list"""
        # Create a frame for the canvas and scrollbar
        list_container = tk.Frame(parent, bg="#1a1a2e")
        list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create canvas and scrollbar
        self.package_canvas = tk.Canvas(
            list_container,
            bg="#0a0a0a",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            list_container,
            orient=tk.VERTICAL,
            command=self.package_canvas.yview
        )
        
        # Create frame inside canvas for packages
        self.package_list_frame = tk.Frame(
            self.package_canvas,
            bg="#0a0a0a"
        )
        
        self.package_list_frame.bind(
            "<Configure>",
            lambda e: self.package_canvas.configure(scrollregion=self.package_canvas.bbox("all"))
        )
        
        self.package_canvas.create_window((0, 0), window=self.package_list_frame, anchor="nw")
        self.package_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.package_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initial empty state
        self.update_package_list()
    
    def update_package_list(self):
        """Update the package list display"""
        # Clear existing packages
        for widget in self.package_list_frame.winfo_children():
            widget.destroy()
        
        # Add package cards
        for pkg in self.dependencies:
            self.create_package_card(pkg)
        
        # Update package count
        header_widgets = self.package_canvas.master.master.winfo_children()[0].winfo_children()
        if header_widgets:
            header_widgets[0].config(text=f"📦 LISTA DE PACOTES ({len(self.dependencies)})")
    
    def create_package_card(self, pkg: DependencyPackage):
        """Create a card for a package"""
        card_frame = tk.Frame(
            self.package_list_frame,
            bg="#0a0a0a",
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=15
        )
        card_frame.pack(fill=tk.X, pady=5)
        
        # Main content
        content_frame = tk.Frame(card_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.X)
        
        # Left: Icon and info
        left_frame = tk.Frame(content_frame, bg="#0a0a0a")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Icon based on category
        icons = {
            PackageCategory.AI: ("🧠", "#a855f7"),
            PackageCategory.TRADING: ("📈", "#10b981"),
            PackageCategory.SYSTEM: ("💻", "#6b7280"),
            PackageCategory.DATA: ("🗄️", "#fbbf24"),
            PackageCategory.QUANTUM: ("⚛️", "#3b82f6")
        }
        
        icon, icon_color = icons.get(pkg.category, ("📦", "#9ca3af"))
        
        icon_frame = tk.Frame(left_frame, bg="#0a0a0a")
        icon_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            icon_frame,
            text=icon,
            font=("Arial", 16),
            fg=icon_color,
            bg="#0a0a0a"
        ).pack()
        
        # Package info
        info_frame = tk.Frame(left_frame, bg="#0a0a0a")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Package name and criticality
        name_frame = tk.Frame(info_frame, bg="#0a0a0a")
        name_frame.pack(anchor=tk.W)
        
        tk.Label(
            name_frame,
            text=pkg.name,
            font=("Arial", 11, "bold"),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT)
        
        # Criticality icon
        crit_icon = "⚠️" if pkg.criticality == CriticalityLevel.HIGH else \
                   "⚠️" if pkg.criticality == CriticalityLevel.MEDIUM else "✓"
        crit_color = "#ef4444" if pkg.criticality == CriticalityLevel.HIGH else \
                    "#fbbf24" if pkg.criticality == CriticalityLevel.MEDIUM else "#3b82f6"
        
        tk.Label(
            name_frame,
            text=crit_icon,
            font=("Arial", 12),
            fg=crit_color,
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Version info
        version_text = f"Req: {pkg.required_version} | Inst: {pkg.installed_version or 'N/A'}"
        tk.Label(
            info_frame,
            text=version_text,
            font=("Courier", 9),
            fg="#9ca3af",
            bg="#0a0a0a"
        ).pack(anchor=tk.W, pady=(2, 0))
        
        # Right: Status and action
        right_frame = tk.Frame(content_frame, bg="#0a0a0a")
        right_frame.pack(side=tk.RIGHT)
        
        # Status badge
        status_colors = {
            DependencyStatus.INSTALLED: ("#065f46", "#10b981"),
            DependencyStatus.MISSING: ("#7f1d1d", "#ef4444"),
            DependencyStatus.OUTDATED: ("#854d0e", "#fbbf24")
        }
        
        bg_color, text_color = status_colors.get(pkg.status, ("#374151", "#9ca3af"))
        
        status_frame = tk.Frame(
            right_frame,
            bg=bg_color,
            relief=tk.RAISED,
            borderwidth=1,
            padx=8,
            pady=3
        )
        status_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            status_frame,
            text=pkg.status.value,
            font=("Arial", 9, "bold"),
            fg=text_color,
            bg=bg_color
        ).pack()
        
        # Install button (if not installed)
        if pkg.status != DependencyStatus.INSTALLED:
            install_btn = tk.Button(
                right_frame,
                text="⬇️",
                command=lambda p=pkg.name: self.install_package(p),
                font=("Arial", 12),
                bg="#374151",
                fg="#9ca3af",
                activebackground="#4b5563",
                activeforeground="#ffffff",
                relief=tk.RAISED,
                borderwidth=1,
                padx=8,
                pady=4,
                state="normal" if self.installing is None else "disabled"
            )
            install_btn.pack(side=tk.LEFT)
    
    def switch_profile(self, profile: ProjectProfileType):
        """Switch project profile"""
        self.profile = profile
        self.scan_system()
    
    def scan_system(self):
        """Scan system for dependencies"""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        self.scan_button.config(state="disabled", text="🔄")
        
        # Run scan in separate thread
        def scan_thread():
            try:
                # Get dependencies
                deps = self.dependency_manager.scan_system(self.profile)
                report = self.dependency_manager.generate_report(deps)
                
                # Update UI in main thread
                self.root.after(0, self.update_scan_results, deps, report)
                
                # Update fix button state
                self.root.after(0, self.update_fix_button)
                
                # Update package list
                self.root.after(0, self.update_package_list)
            except Exception as e:
                print(f"Error scanning system: {e}")
                self.root.after(0, self.show_error, "Erro ao escanear o sistema")
            finally:
                self.is_scanning = False
                self.scan_button.config(state="normal", text="🔍")
                
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def update_scan_results(self, dependencies: List[DependencyPackage], report: DependencyReport):
        """Update the scan results display"""
        # Update health score   
        self.health_score = report.score
        self.health_score_label.config(text=f"🏆 Saúde do Sistema: {report.score:.2f}%")
        
        # Update environment info
        self.update_environment_info()
        
        # Update package list
        self.update_package_list()
        
        # Update fix button state
        self.update_fix_button()
        