#!/usr/bin/env python3
"""
ENVIRONMENT VALIDATOR - Sistema Avançado de Verificação de Ambiente
Integrado com a estrutura do projeto SENCIENT AI
"""

import sys
import os
import subprocess
import pkg_resources
import platform
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import json

class AdvancedEnvironmentValidator:
    """
    Sistema completo de validação de ambiente para o projeto SENCIENT AI
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {},
            "python_environment": {},
            "packages": {},
            "compilers": {},
            "directory_structure": {},
            "recommendations": [],
            "overall_status": "unknown"
        }
        
    def get_system_info(self) -> Dict[str, Any]:
        """Coleta informações detalhadas do sistema"""
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "python_build": platform.python_build(),
            "python_compiler": platform.python_compiler()
        }
        
        # Informações específicas do Windows
        if platform.system() == "Windows":
            system_info["windows_edition"] = platform.win32_edition()
        
        self.validation_results["system_info"] = system_info
        return system_info
    
    def check_python_environment(self) -> Dict[str, Any]:
        """Verificação avançada do ambiente Python"""
        python_info = {
            "version": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro,
                "full": sys.version
            },
            "implementation": platform.python_implementation(),
            "path": sys.executable,
            "requirements_met": False,
            "recommended_version": "3.9+"
        }
        
        # Verifica versão mínima
        python_info["requirements_met"] = (
            python_info["version"]["major"] == 3 and 
            python_info["version"]["minor"] >= 9
        )
        
        self.validation_results["python_environment"] = python_info
        return python_info
    
    def check_required_packages(self) -> Dict[str, Any]:
        """
        Verifica pacotes necessários para o projeto SENCIENT AI
        """
        required_packages = {
            'torch': '2.0.0',
            'torchvision': '0.15.0',
            'numpy': '1.21.0',
            'opencv-python': '4.7.0',
            'Pillow': '9.0.0',
            'asyncio': None,  # Built-in
            'pathlib': None,  # Built-in
            'dataclasses': None,  # Built-in
            'typing': None,  # Built-in
            'uuid': None,  # Built-in
            'hashlib': None,  # Built-in
            'json': None,  # Built-in
            'logging': None  # Built-in
        }
        
        # Pacotes opcionais para funcionalidades avançadas
        optional_packages = {
            'bpy': '3.4.0',  # Blender Python - para geração de avatar
            'scipy': '1.7.0',  # Processamento científico
            'matplotlib': '3.5.0',  # Visualização
            'tqdm': '4.64.0',  # Progress bars
            'psutil': '5.9.0',  # Monitoramento de sistema
            'colorama': '0.4.6'  # Cores no terminal
        }
        
        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        package_results = {
            "required": {"missing": [], "outdated": [], "ok": []},
            "optional": {"missing": [], "outdated": [], "ok": []},
            "summary": {
                "total_required": len(required_packages),
                "total_optional": len(optional_packages),
                "required_met": 0,
                "optional_met": 0
            }
        }
        
        # Verifica pacotes requeridos
        for package, min_version in required_packages.items():
            if package.lower() not in [pkg.lower() for pkg in installed_packages.keys()]:
                package_results["required"]["missing"].append({
                    "package": package,
                    "required_version": min_version
                })
            elif min_version and installed_packages[package] < min_version:
                package_results["required"]["outdated"].append({
                    "package": package,
                    "current_version": installed_packages[package],
                    "required_version": min_version
                })
            else:
                package_results["required"]["ok"].append({
                    "package": package,
                    "version": installed_packages.get(package, "built-in")
                })
        
        # Verifica pacotes opcionais
        for package, min_version in optional_packages.items():
            if package.lower() not in [pkg.lower() for pkg in installed_packages.keys()]:
                package_results["optional"]["missing"].append({
                    "package": package,
                    "required_version": min_version
                })
            elif min_version and installed_packages[package] < min_version:
                package_results["optional"]["outdated"].append({
                    "package": package,
                    "current_version": installed_packages[package],
                    "required_version": min_version
                })
            else:
                package_results["optional"]["ok"].append({
                    "package": package,
                    "version": installed_packages.get(package, "built-in")
                })
        
        # Calcula estatísticas
        package_results["summary"]["required_met"] = len(package_results["required"]["ok"])
        package_results["summary"]["optional_met"] = len(package_results["optional"]["ok"])
        
        self.validation_results["packages"] = package_results
        return package_results
    
    def check_compilers(self) -> Dict[str, Any]:
        """Verifica compiladores disponíveis no sistema"""
        compilers = {
            "c++": {"available": False, "version": None, "path": None},
            "c": {"available": False, "version": None, "path": None},
            "nvcc": {"available": False, "version": None, "path": None}  # CUDA compiler
        }
        
        # Verifica GCC/G++ no Linux/Mac
        if platform.system() in ["Linux", "Darwin"]:
            for compiler, command in [("c++", "g++"), ("c", "gcc")]:
                try:
                    result = subprocess.run([command, "--version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        compilers[compiler]["available"] = True
                        compilers[compiler]["version"] = result.stdout.split('\n')[0]
                        compilers[compiler]["path"] = shutil.which(command)
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
        
        # Verifica MSVC no Windows
        elif platform.system() == "Windows":
            try:
                result = subprocess.run(["cl"], capture_output=True, text=True, timeout=10)
                if "Microsoft (R) C/C++ Optimizing Compiler" in result.stderr:
                    compilers["c++"]["available"] = True
                    compilers["c"]["available"] = True
                    compilers["c++"]["version"] = "MSVC"
                    compilers["c"]["version"] = "MSVC"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        # Verifica NVCC (CUDA)
        try:
            result = subprocess.run(["nvcc", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                compilers["nvcc"]["available"] = True
                compilers["nvcc"]["version"] = result.stdout.split('\n')[3]  # Linha da versão
                compilers["nvcc"]["path"] = shutil.which("nvcc")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.validation_results["compilers"] = compilers
        return compilers
    
    def analyze_directory_structure(self) -> Dict[str, Any]:
        """
        Analisa e valida a estrutura de diretórios do projeto SENCIENT AI
        """
        expected_structure = {
            "src": {
                "required": True,
                "description": "Código fonte principal",
                "subdirs": ["core", "models", "avatar", "quantum", "utils"]
            },
            "data": {
                "required": True,
                "description": "Dados e modelos treinados",
                "subdirs": ["training", "memories", "models"]
            },
            "config": {
                "required": True,
                "description": "Arquivos de configuração",
                "files": ["neural_learn_config.json", "ethical_constraints.json"]
            },
            "tests": {
                "required": False,
                "description": "Testes unitários",
                "subdirs": ["unit", "integration"]
            },
            "docs": {
                "required": False,
                "description": "Documentação",
                "files": ["README.md", "API.md"]
            },
            "scripts": {
                "required": False,
                "description": "Scripts utilitários",
                "files": ["setup.py", "deploy.py"]
            },
            "logs": {
                "required": False,
                "description": "Logs do sistema",
                "gitkeep": True
            },
            "exports": {
                "required": False,
                "description": "Exportações e resultados",
                "subdirs": ["avatars", "reports", "insights"]
            }
        }
        
        analysis = {
            "expected_structure": expected_structure,
            "actual_structure": {},
            "validation": {
                "missing_dirs": [],
                "missing_files": [],
                "extra_dirs": [],
                "compliance_score": 0.0
            },
            "statistics": {
                "total_directories": 0,
                "total_files": 0,
                "total_size_bytes": 0,
                "largest_directory": {"path": "", "size": 0}
            }
        }
        
        # Analisa estrutura atual
        self._scan_directory_structure(self.project_root, analysis)
        
        # Valida estrutura esperada
        self._validate_expected_structure(expected_structure, analysis)
        
        # Calcula score de compliance
        total_expected = sum(1 for config in expected_structure.values() if config["required"])
        total_missing = len(analysis["validation"]["missing_dirs"])
        analysis["validation"]["compliance_score"] = (
            (total_expected - total_missing) / total_expected * 100 
            if total_expected > 0 else 100.0
        )
        
        self.validation_results["directory_structure"] = analysis
        return analysis
    
    def _scan_directory_structure(self, current_path: Path, analysis: Dict[str, Any], depth: int = 0, max_depth: int = 5):
        """Escaneia recursivamente a estrutura de diretórios"""
        if depth > max_depth:
            return
        
        try:
            for item in current_path.iterdir():
                relative_path = item.relative_to(self.project_root)
                
                if item.is_dir():
                    # Ignora diretórios do sistema
                    if item.name in ['.git', '__pycache__', '.pytest_cache', '.vscode', '.idea']:
                        continue
                    
                    # Estatísticas do diretório
                    dir_size = self._get_directory_size(item)
                    analysis["statistics"]["total_directories"] += 1
                    
                    if dir_size > analysis["statistics"]["largest_directory"]["size"]:
                        analysis["statistics"]["largest_directory"] = {
                            "path": str(relative_path),
                            "size": dir_size
                        }
                    
                    # Adiciona à estrutura atual
                    analysis["actual_structure"][str(relative_path)] = {
                        "type": "directory",
                        "size_bytes": dir_size,
                        "file_count": len(list(item.glob("**/*"))),
                        "depth": depth
                    }
                    
                    # Escaneia recursivamente
                    self._scan_directory_structure(item, analysis, depth + 1, max_depth)
                
                elif item.is_file():
                    analysis["statistics"]["total_files"] += 1
                    analysis["statistics"]["total_size_bytes"] += item.stat().st_size
                    
                    analysis["actual_structure"][str(relative_path)] = {
                        "type": "file",
                        "size_bytes": item.stat().st_size,
                        "extension": item.suffix,
                        "depth": depth
                    }
        
        except PermissionError:
            # Ignora diretórios sem permissão
            pass
    
    def _get_directory_size(self, directory: Path) -> int:
        """Calcula o tamanho total de um diretório"""
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except PermissionError:
            pass
        return total_size
    
    def _validate_expected_structure(self, expected: Dict[str, Any], analysis: Dict[str, Any]):
        """Valida a estrutura atual contra a esperada"""
        actual_paths = set(analysis["actual_structure"].keys())
        
        for dir_name, config in expected.items():
            expected_path = Path(dir_name)
            
            # Verifica se diretório existe
            if config["required"] and str(expected_path) not in actual_paths:
                analysis["validation"]["missing_dirs"].append({
                    "directory": dir_name,
                    "description": config["description"],
                    "required": config["required"]
                })
            
            # Verifica subdiretórios esperados
            for subdir in config.get("subdirs", []):
                subdir_path = expected_path / subdir
                if str(subdir_path) not in actual_paths:
                    analysis["validation"]["missing_dirs"].append({
                        "directory": str(subdir_path),
                        "description": f"Subdiretorio de {dir_name}",
                        "required": config["required"]
                    })
            
            # Verifica arquivos esperados
            for file in config.get("files", []):
                file_path = expected_path / file
                if str(file_path) not in actual_paths:
                    analysis["validation"]["missing_files"].append({
                        "file": str(file_path),
                        "description": f"Arquivo em {dir_name}",
                        "required": config["required"]
                    })
        
        # Identifica diretórios extras
        expected_paths = set()
        for dir_name, config in expected.items():
            expected_paths.add(dir_name)
            for subdir in config.get("subdirs", []):
                expected_paths.add(str(Path(dir_name) / subdir))
        
        extra_dirs = actual_paths - expected_paths
        analysis["validation"]["extra_dirs"] = [
            {"path": path, "type": analysis["actual_structure"][path]["type"]}
            for path in extra_dirs if analysis["actual_structure"][path]["type"] == "directory"
        ]
    
    def generate_recommendations(self) -> List[str]:
        """Gera recomendações baseadas na análise do ambiente"""
        recommendations = []
        
        # Recomendações de Python
        python_env = self.validation_results["python_environment"]
        if not python_env["requirements_met"]:
            recommendations.append(
                f"⚠️  Atualize para Python {python_env['recommended_version']} "
                f"(atual: {python_env['version']['major']}.{python_env['version']['minor']})"
            )
        
        # Recomendações de pacotes
        packages = self.validation_results["packages"]
        for missing in packages["required"]["missing"]:
            recommendations.append(
                f"📦 Instale pacote requerido: {missing['package']} "
                f"(versão: {missing['required_version'] or 'qualquer'})"
            )
        
        for outdated in packages["required"]["outdated"]:
            recommendations.append(
                f"🔄 Atualize {outdated['package']}: {outdated['current_version']} → {outdated['required_version']}"
            )
        
        # Recomendações de estrutura
        dir_structure = self.validation_results["directory_structure"]
        for missing_dir in dir_structure["validation"]["missing_dirs"]:
            if missing_dir["required"]:
                recommendations.append(
                    f"📁 Crie diretório necessário: {missing_dir['directory']} "
                    f"({missing_dir['description']})"
                )
        
        # Recomendações de compiladores
        compilers = self.validation_results["compilers"]
        if not compilers["c++"]["available"]:
            if platform.system() == "Windows":
                recommendations.append("🔧 Instale Visual Studio com ferramentas C++")
            else:
                recommendations.append("🔧 Instale g++ (GNU C++ compiler)")
        
        # Recomendações de performance
        if compilers["nvcc"]["available"]:
            recommendations.append("🎯 CUDA detectado - Otimize para GPU")
        else:
            recommendations.append("💡 Considere instalar CUDA para aceleração GPU")
        
        self.validation_results["recommendations"] = recommendations
        return recommendations
    
    def calculate_overall_status(self) -> str:
        """Calcula status geral do ambiente"""
        python_ok = self.validation_results["python_environment"]["requirements_met"]
        
        packages_ok = (
            len(self.validation_results["packages"]["required"]["missing"]) == 0 and
            len(self.validation_results["packages"]["required"]["outdated"]) == 0
        )
        
        dir_structure = self.validation_results["directory_structure"]
        structure_ok = dir_structure["validation"]["compliance_score"] >= 80.0
        
        if python_ok and packages_ok and structure_ok:
            status = "optimal"
        elif python_ok and packages_ok:
            status = "good"
        elif python_ok:
            status = "fair"
        else:
            status = "poor"
        
        self.validation_results["overall_status"] = status
        return status
    
    def create_directories(self) -> Dict[str, Any]:
        """Cria diretórios faltantes baseado na análise"""
        creation_results = {
            "created_directories": [],
            "failed_creations": [],
            "gitkeep_files_created": 0
        }
        
        dir_structure = self.validation_results["directory_structure"]
        
        for missing_dir in dir_structure["validation"]["missing_dirs"]:
            if missing_dir["required"]:
                dir_path = self.project_root / missing_dir["directory"]
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    creation_results["created_directories"].append(str(dir_path))
                    
                    # Cria .gitkeep se necessário
                    gitkeep_path = dir_path / ".gitkeep"
                    gitkeep_path.touch()
                    creation_results["gitkeep_files_created"] += 1
                    
                except Exception as e:
                    creation_results["failed_creations"].append({
                        "directory": str(dir_path),
                        "error": str(e)
                    })
        
        return creation_results
    
    def generate_report(self) -> str:
        """Gera relatório completo da validação"""
        report = [
            "🧠 SENCIENT AI - RELATÓRIO DE VALIDAÇÃO DE AMBIENTE",
            "=" * 60,
            f"Data: {self.validation_results['timestamp']}",
            f"Status Geral: {self.validation_results['overall_status'].upper()}",
            ""
        ]
        
        # Sistema
        system = self.validation_results["system_info"]
        report.extend([
            "💻 SISTEMA:",
            f"  Plataforma: {system['platform']} {system['platform_release']}",
            f"  Arquitetura: {system['architecture'][0]}",
            f"  Processador: {system['processor']}",
            ""
        ])
        
        # Python
        python_env = self.validation_results["python_environment"]
        status_icon = "✅" if python_env["requirements_met"] else "❌"
        report.extend([
            "🐍 PYTHON:",
            f"  {status_icon} Versão: {python_env['version']['full'].split()[0]}",
            f"  Implementação: {python_env['implementation']}",
            f"  Executável: {python_env['path']}",
            ""
        ])
        
        # Pacotes
        packages = self.validation_results["packages"]
        report.extend([
            "📦 PACOTES:",
            f"  Requeridos: {packages['summary']['required_met']}/{packages['summary']['total_required']} OK",
            f"  Opcionais: {packages['summary']['optional_met']}/{packages['summary']['total_optional']} OK",
        ])
        
        if packages["required"]["missing"]:
            report.append("  ❌ Faltando:")
            for missing in packages["required"]["missing"]:
                report.append(f"     - {missing['package']} ({missing['required_version']})")
        
        if packages["required"]["outdated"]:
            report.append("  🔄 Desatualizados:")
            for outdated in packages["required"]["outdated"]:
                report.append(f"     - {outdated['package']}: {outdated['current_version']} → {outdated['required_version']}")
        
        report.append("")
        
        # Estrutura de Diretórios
        dir_structure = self.validation_results["directory_structure"]
        stats = dir_structure["statistics"]
        report.extend([
            "📁 ESTRUTURA DE DIRETÓRIOS:",
            f"  Compliance: {dir_structure['validation']['compliance_score']:.1f}%",
            f"  Diretórios: {stats['total_directories']}",
            f"  Arquivos: {stats['total_files']}",
            f"  Tamanho total: {stats['total_size_bytes'] / (1024**2):.1f} MB",
            f"  Maior diretório: {stats['largest_directory']['path']} "
            f"({stats['largest_directory']['size'] / (1024**2):.1f} MB)",
        ])
        
        if dir_structure["validation"]["missing_dirs"]:
            report.append("  📌 Diretórios faltantes:")
            for missing in dir_structure["validation"]["missing_dirs"][:5]:  # Mostra apenas 5
                report.append(f"     - {missing['directory']} ({missing['description']})")
        
        report.append("")
        
        # Recomendações
        recommendations = self.validation_results["recommendations"]
        if recommendations:
            report.extend(["🎯 RECOMENDAÇÕES:", ""])
            for i, rec in enumerate(recommendations[:8], 1):  # Limita a 8 recomendações
                report.append(f"  {i}. {rec}")
        
        return "\n".join(report)
    
    def save_report(self, filename: str = "environment_validation_report.txt") -> str:
        """Salva o relatório em arquivo"""
        report_path = self.project_root / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        return str(report_path)
    
    def run_complete_validation(self) -> Dict[str, Any]:
        """Executa validação completa do ambiente"""
        print("🚀 Iniciando validação completa do ambiente SENCIENT AI...")
        
        # Executa todas as verificações
        self.get_system_info()
        self.check_python_environment()
        self.check_required_packages()
        self.check_compilers()
        self.analyze_directory_structure()
        self.generate_recommendations()
        self.calculate_overall_status()
        
        return self.validation_results

def main():
    """Função principal"""
    validator = AdvancedEnvironmentValidator()
    
    print("🧠 SENCIENT AI - Validador de Ambiente Avançado")
    print("=" * 50)
    
    # Validação completa
    results = validator.run_complete_validation()
    
    # Exibe relatório
    print("\n" + validator.generate_report())
    
    # Cria diretórios faltantes se necessário
    if results["overall_status"] in ["fair", "poor"]:
        print("\n🛠️  Criando diretórios faltantes...")
        creation_results = validator.create_directories()
        
        if creation_results["created_directories"]:
            print("✅ Diretórios criados:")
            for dir_path in creation_results["created_directories"]:
                print(f"   📁 {dir_path}")
        
        if creation_results["gitkeep_files_created"] > 0:
            print(f"   📄 {creation_results['gitkeep_files_created']} arquivos .gitkeep criados")
    
    # Salva relatório
    report_path = validator.save_report()
    print(f"\n💾 Relatório salvo em: {report_path}")
    
    # Status final
    status_icons = {
        "optimal": "🎉",
        "good": "✅", 
        "fair": "⚠️",
        "poor": "❌"
    }
    
    print(f"\n{status_icons[results['overall_status']]} "
          f"STATUS FINAL: {results['overall_status'].upper()}")
    
    return results["overall_status"] in ["optimal", "good"]

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)