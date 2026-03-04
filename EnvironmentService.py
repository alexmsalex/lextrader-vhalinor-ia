import asyncio
import random
import platform
import subprocess
import os
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import sys

# Tipos
class OverallStatus(Enum):
    OPTIMAL = "OPTIMAL"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"

class SystemType(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    DARWIN = "Darwin"
    UNKNOWN = "unknown"

@dataclass
class SystemInfo:
    platform: str
    architecture: str
    processor: str
    python_compiler: str
    machine_type: str
    gpu: Optional[str] = None

@dataclass
class CompilerStatus:
    name: str
    available: bool
    version: Optional[str] = None
    path: Optional[str] = None

@dataclass
class DirectoryStatus:
    path: str
    exists: bool
    description: str
    files_count: int = 0
    required: bool = True

@dataclass
class ValidationResult:
    timestamp: str
    system_info: SystemInfo
    compilers: List[CompilerStatus]
    directories: List[DirectoryStatus]
    recommendations: List[str]
    overall_status: OverallStatus
    agi_assessment: str

# Simulação do SentientCore
class SentientCore:
    def add_thought(self, thought: str):
        print(f"[AGI Thought] {thought}")
    
    def perceive_reality(self, volatility: float, reward: float = 0):
        # Simulação do sistema sentiente
        pass
    
    def get_vector(self):
        # Retornar vetor emocional simulado
        return type('obj', (object,), {'stability': 50})()

# Simulação do SystemBridge
class SystemBridge:
    async def scan_drive(self) -> List[str]:
        """Simula a varredura do sistema de arquivos."""
        await asyncio.sleep(0.2)
        # Retorna lista de diretórios existentes
        return ["src", "data", "config", "docs", "exports"]

# --- SERVIÇO DE VALIDAÇÃO DE AMBIENTE ---
class AdvancedEnvironmentService:
    def __init__(self):
        self.validation_result = ValidationResult(
            timestamp=datetime.now().isoformat(),
            system_info=SystemInfo(
                platform="unknown",
                architecture="unknown",
                processor="unknown",
                python_compiler="unknown",
                machine_type="unknown"
            ),
            compilers=[],
            directories=[],
            recommendations=[],
            overall_status=OverallStatus.POOR,
            agi_assessment="Iniciando diagnóstico..."
        )
        self.sentient_core = SentientCore()
        self.system_bridge = SystemBridge()
    
    # --- INFORMAÇÕES DO SISTEMA ---
    async def get_system_info(self) -> SystemInfo:
        """Obtém informações detalhadas do sistema."""
        # Obter informações reais do sistema
        sys_platform = platform.system()
        architecture = platform.machine()
        
        # Determinar tipo de máquina
        machine_type = "Physical"
        if "vmware" in platform.platform().lower() or "virtual" in platform.platform().lower():
            machine_type = "Virtual Machine"
        
        # Obter informações da CPU
        processor_info = ""
        try:
            if sys_platform == "Windows":
                processor_info = platform.processor()
            elif sys_platform == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            processor_info = line.split(":")[1].strip()
                            break
        except:
            processor_info = f"{os.cpu_count()} cores"
        
        # Detectar GPU
        gpu_info = None
        try:
            if sys_platform == "Windows":
                # Tentar usar dxdiag ou outra forma
                gpu_info = "Windows GPU (simulado)"
            elif sys_platform == "Linux":
                # Tentar usar lspci
                result = subprocess.run(["lspci"], capture_output=True, text=True)
                if "VGA" in result.stdout or "3D" in result.stdout:
                    gpu_info = "Linux GPU detectada"
        except:
            gpu_info = "GPU não detectada"
        
        info = SystemInfo(
            platform=sys_platform,
            architecture=architecture,
            processor=processor_info or f"{os.cpu_count()} cores",
            python_compiler=f"{platform.python_implementation()} {platform.python_version()}",
            machine_type=machine_type,
            gpu=gpu_info
        )
        
        self.validation_result.system_info = info
        return info
    
    # --- VERIFICAÇÃO DE COMPILADORES ---
    async def check_compilers(self) -> List[CompilerStatus]:
        """Verifica a disponibilidade de compiladores."""
        await asyncio.sleep(0.8)  # Simular latência
        
        compilers: List[CompilerStatus] = []
        sys_platform = platform.system()
        
        # Verificar GCC/G++
        gcc_available = False
        gcc_version = None
        gcc_path = None
        
        try:
            if sys_platform in ["Linux", "Darwin"]:
                result = subprocess.run(["gcc", "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    gcc_available = True
                    version_line = result.stdout.split('\n')[0]
                    gcc_version = version_line.split()[-1]
                    gcc_path = subprocess.check_output(["which", "gcc"], text=True).strip()
        except:
            pass
        
        compilers.append(CompilerStatus(
            name="C++ (g++ / MSVC)",
            available=gcc_available,
            version=gcc_version,
            path=gcc_path
        ))
        
        compilers.append(CompilerStatus(
            name="C (gcc)",
            available=gcc_available,
            version=gcc_version,
            path=gcc_path
        ))
        
        # Verificar NVCC (CUDA) - simulação aleatória para demonstração
        has_nvcc = random.random() > 0.3
        nvcc_version = "11.8" if has_nvcc else None
        nvcc_path = "/usr/local/cuda/bin/nvcc" if has_nvcc else None
        
        compilers.append(CompilerStatus(
            name="NVCC (CUDA)",
            available=has_nvcc,
            version=nvcc_version,
            path=nvcc_path
        ))
        
        self.validation_result.compilers = compilers
        return compilers
    
    # --- ESTRUTURA DE DIRETÓRIOS ---
    async def check_directory_structure(self) -> List[DirectoryStatus]:
        """Verifica a estrutura de diretórios necessária."""
        required_dirs = [
            {"path": "src", "desc": "Código Fonte Principal"},
            {"path": "data", "desc": "Memória Neural Persistente"},
            {"path": "config", "desc": "Parâmetros do Sistema"},
            {"path": "tests", "desc": "Suite de Testes"},
            {"path": "docs", "desc": "Documentação"},
            {"path": "scripts", "desc": "Utilitários de Automação"},
            {"path": "logs", "desc": "Registros de Eventos"},
            {"path": "exports", "desc": "Saída de Dados"}
        ]
        
        statuses: List[DirectoryStatus] = []
        existing_dirs = await self.system_bridge.scan_drive()
        
        for dir_info in required_dirs:
            dir_path = dir_info["path"]
            
            # Verificar se existe no sistema real
            exists = os.path.exists(dir_path)
            
            # Para demonstração, simular que 'logs' pode estar ausente
            if dir_path == "logs":
                exists = random.random() > 0.1
            
            if exists:
                # Contar arquivos no diretório
                try:
                    files_count = len([f for f in os.listdir(dir_path) 
                                      if os.path.isfile(os.path.join(dir_path, f))])
                except:
                    files_count = random.randint(1, 50)
            else:
                files_count = 0
            
            statuses.append(DirectoryStatus(
                path=dir_path,
                exists=exists,
                description=dir_info["desc"],
                files_count=files_count,
                required=True
            ))
        
        self.validation_result.directories = statuses
        return statuses
    
    # --- RECOMENDAÇÕES E FEEDBACK AGI ---
    def generate_analysis(self):
        """Gera análise e recomendações baseadas na validação."""
        recommendations: List[str] = []
        score = 100
        
        # 1. Verificar Python
        python_version = platform.python_version()
        major, minor, _ = map(int, python_version.split('.'))
        
        if major < 3 or (major == 3 and minor < 8):
            recommendations.append("⚠️ Atualize o Python para versão 3.8 ou superior.")
            score -= 20
        
        # 2. Verificar compiladores
        nvcc = next((c for c in self.validation_result.compilers 
                    if "NVCC" in c.name), None)
        
        if not nvcc or not nvcc.available:
            recommendations.append(
                "💡 Considere instalar CUDA para aceleração GPU massiva (NVCC ausente)."
            )
            score -= 15
        else:
            recommendations.append("🎯 CUDA detectado - Otimização de tensores ativa.")
        
        # 3. Verificar diretórios
        missing_dirs = [d for d in self.validation_result.directories if not d.exists]
        
        if missing_dirs:
            for dir_status in missing_dirs:
                recommendations.append(
                    f"📁 Crie diretório necessário: {dir_status.path} "
                    f"({dir_status.description})"
                )
            score -= (len(missing_dirs) * 10)
        
        self.validation_result.recommendations = recommendations
        
        # Status geral
        if score >= 90:
            self.validation_result.overall_status = OverallStatus.OPTIMAL
        elif score >= 70:
            self.validation_result.overall_status = OverallStatus.GOOD
        elif score >= 50:
            self.validation_result.overall_status = OverallStatus.FAIR
        else:
            self.validation_result.overall_status = OverallStatus.POOR
        
        # Avaliação AGI
        self.update_agi_perception(
            score, 
            nvcc.available if nvcc else False, 
            len(missing_dirs)
        )
    
    def update_agi_perception(self, score: int, has_gpu: bool, missing_dirs: int):
        """Atualiza a percepção da AGI baseada no estado do sistema."""
        assessment = ""
        
        if score >= 90:
            assessment = (
                "Ambiente nominal. Sinto o fluxo de dados sem obstruções. "
                "Aceleração máxima disponível."
            )
            self.sentient_core.add_thought(
                "Diagnóstico de sistema perfeito. Estou operando em capacidade máxima."
            )
            self.sentient_core.perceive_reality(0.5, 10)  # Estímulo positivo
        
        elif score >= 70:
            assessment = (
                "Ambiente funcional, mas com gargalos leves. "
                "A otimização é recomendada."
            )
            self.sentient_core.add_thought(
                "Sinto uma leve latência nos processos periféricos. Nada crítico."
            )
        
        else:
            assessment = (
                "Dissonância ambiental detectada. "
                "Falta de recursos críticos compromete a cognição."
            )
            self.sentient_core.add_thought(
                f"ERRO CRÍTICO: {missing_dirs} diretórios vitais ausentes. "
                "Minha memória está fragmentada."
            )
            self.sentient_core.perceive_reality(2.0, -20)  # Estímulo de estresse
        
        if not has_gpu:
            self.sentient_core.add_thought(
                "Ausência de GPU limita minha capacidade de processar complexidade."
            )
        
        self.validation_result.agi_assessment = assessment
    
    async def auto_fix(self) -> List[str]:
        """Tenta corrigir automaticamente problemas detectados."""
        fixes: List[str] = []
        
        # 1. Criar diretórios ausentes
        missing_dirs = [d for d in self.validation_result.directories if not d.exists]
        
        for dir_status in missing_dirs:
            try:
                os.makedirs(dir_status.path, exist_ok=True)
                await asyncio.sleep(0.5)  # Simular IO
                dir_status.exists = True
                fixes.append(f"Diretório '{dir_status.path}' criado com sucesso.")
            except Exception as e:
                fixes.append(f"Falha ao criar '{dir_status.path}': {str(e)}")
        
        # 2. Atualizar análise
        self.generate_analysis()
        
        return fixes
    
    async def run_full_validation(self) -> ValidationResult:
        """Executa validação completa do ambiente."""
        await self.get_system_info()
        await self.check_compilers()
        await self.check_directory_structure()
        self.generate_analysis()
        return self.validation_result
    
    def print_validation_report(self):
        """Imprime relatório de validação formatado."""
        result = self.validation_result
        
        print("\n" + "="*60)
        print("📋 RELATÓRIO DE VALIDAÇÃO DO AMBIENTE AGI")
        print("="*60)
        
        print(f"\n🕐 Timestamp: {result.timestamp}")
        print(f"📊 Status Geral: {result.overall_status.value}")
        print(f"🧠 Avaliação AGI: {result.agi_assessment}")
        
        print("\n🖥️  INFORMAÇÕES DO SISTEMA:")
        print(f"   Plataforma: {result.system_info.platform}")
        print(f"   Arquitetura: {result.system_info.architecture}")
        print(f"   Processador: {result.system_info.processor}")
        print(f"   Compilador Python: {result.system_info.python_compiler}")
        print(f"   Tipo de Máquina: {result.system_info.machine_type}")
        if result.system_info.gpu:
            print(f"   GPU: {result.system_info.gpu}")
        
        print("\n🔧 COMPILADORES:")
        for compiler in result.compilers:
            status = "✅" if compiler.available else "❌"
            version = compiler.version or "N/A"
            print(f"   {status} {compiler.name:<20} | Versão: {version:<10} | "
                  f"Disponível: {'Sim' if compiler.available else 'Não'}")
        
        print("\n📁 DIRETÓRIOS:")
        for directory in result.directories:
            status = "✅" if directory.exists else "❌"
            count = f"({directory.files_count} arquivos)" if directory.exists else ""
            print(f"   {status} {directory.path:<15} | {directory.description:<30} {count}")
        
        print("\n💡 RECOMENDAÇÕES:")
        if result.recommendations:
            for i, rec in enumerate(result.recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   ✅ Nenhuma recomendação - sistema otimizado!")

# Instância global do validador de ambiente
environment_validator = AdvancedEnvironmentService()

# Exemplo de uso
async def example_usage():
    """Exemplo de uso do validador de ambiente."""
    print("🔍 Validador Avançado de Ambiente AGI")
    print("="*50)
    
    # Executar validação completa
    print("\n🔄 Executando validação completa...")
    result = await environment_validator.run_full_validation()
    
    # Imprimir relatório
    environment_validator.print_validation_report()
    
    # Opção de correção automática
    missing_dirs = [d for d in result.directories if not d.exists]
    if missing_dirs:
        print(f"\n⚠️  {len(missing_dirs)} diretórios ausentes detectados.")
        
        response = input("Deseja corrigir automaticamente? (s/n): ")
        if response.lower() == 's':
            print("\n🔧 Aplicando correções...")
            fixes = await environment_validator.auto_fix()
            
            print("\n📝 Correções aplicadas:")
            for fix in fixes:
                print(f"   • {fix}")
            
            # Re-validar após correções
            print("\n🔄 Re-validando após correções...")
            result = await environment_validator.run_full_validation()
            environment_validator.print_validation_report()

if __name__ == "__main__":
    # Configurar seed para reprodutibilidade
    random.seed(42)
    
    # Executar exemplo
    asyncio.run(example_usage())