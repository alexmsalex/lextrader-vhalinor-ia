"""
Dependency Checker - Ferramenta completa para verificação e gerenciamento de dependências
Suporta verificação, instalação, relatórios detalhados e análise de compatibilidade
"""

import pkg_resources
import sys
import platform
import subprocess
import importlib
import os
import json
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import warnings
from packaging import version
from enum import Enum


class DependencyStatus(Enum):
    """Status das dependências"""
    INSTALLED = "instalado"
    MISSING = "ausente"
    OUTDATED = "desatualizado"
    INCOMPATIBLE = "incompatível"
    ERROR = "erro"


class ProjectType(Enum):
    """Tipos de projetos suportados"""
    COMPLETE = "completo"
    IA = "ia"
    TRADING = "trading"
    SYSTEM = "sistema"
    WEB = "web"
    DATA = "dados"
    VISUALIZATION = "visualizacao"
    API = "api"
    TESTING = "testes"


class DependencyChecker:
    """Classe principal para verificação e gerenciamento de dependências"""
    
    def __init__(self, project_type: str='completo', verbose: bool=True,
                 check_compatibility: bool=True, config_file: Optional[str]=None):
        """
        Inicializa o verificador de dependências
        
        Args:
            project_type: Tipo de projeto (completo, ia, trading, etc.)
            verbose: Modo detalhado
            check_compatibility: Verificar compatibilidade entre pacotes
            config_file: Caminho para arquivo de configuração JSON
        """
        self.project_type = project_type
        self.verbose = verbose
        self.check_compatibility = check_compatibility
        self.system_info = self._get_system_info()
        
        # Carrega configurações padrão ou do arquivo
        if config_file and os.path.exists(config_file):
            self.config = self._load_config(config_file)
        else:
            self.config = self._get_default_config()
        
        self.dependencies = self._build_dependency_list()
        self.results = {
            'instalados': [],
            'ausentes': [],
            'desatualizados': [],
            'incompativeis': [],
            'erros': [],
            'warnings': []
        }
        self.compatibility_issues = []
        
        if self.verbose:
            self._print_header()
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Coleta informações do sistema"""
        return {
            'python_version': sys.version,
            'platform': platform.platform(),
            'processor': platform.processor(),
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'python_executable': sys.executable
        }
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retorna configuração padrão de dependências"""
        return {
            'dependencies': {
                'base': {
                    'numpy': {'min': '1.24.3', 'max': None, 'required': True},
                    'pandas': {'min': '2.1.1', 'max': None, 'required': True},
                    'python-dotenv': {'min': '1.0.0', 'max': None, 'required': True},
                    'packaging': {'min': '23.1', 'max': None, 'required': True},
                },
                'ia': {
                    'tensorflow': {'min': '2.14.0', 'max': None, 'required': False},
                    'scikit-learn': {'min': '1.3.0', 'max': None, 'required': False},
                    'keras': {'min': '2.14.0', 'max': None, 'required': False},
                    'torch': {'min': '2.1.0', 'max': None, 'required': False},
                    'xgboost': {'min': '2.0.0', 'max': None, 'required': False}
                },
                'trading': {
                    'ccxt': {'min': '4.1.13', 'max': None, 'required': False},
                    'ta-lib': {'min': '0.4.28', 'max': None, 'required': False},
                    'pandas-ta': {'min': '0.3.14b0', 'max': None, 'required': False},
                    'yfinance': {'min': '0.2.28', 'max': None, 'required': False}
                },
                'sistema': {
                    'psutil': {'min': '5.9.0', 'max': None, 'required': False},
                    'py-cpuinfo': {'min': '9.0.0', 'max': None, 'required': False},
                    'gputil': {'min': '1.4.0', 'max': None, 'required': False},
                },
                'web': {
                    'flask': {'min': '2.3.3', 'max': None, 'required': False},
                    'requests': {'min': '2.31.0', 'max': None, 'required': False},
                    'beautifulsoup4': {'min': '4.12.2', 'max': None, 'required': False},
                    'selenium': {'min': '4.12.0', 'max': None, 'required': False}
                },
                'dados': {
                    'sqlalchemy': {'min': '2.0.21', 'max': None, 'required': False},
                    'pymongo': {'min': '4.5.0', 'max': None, 'required': False},
                    'redis': {'min': '5.0.1', 'max': None, 'required': False},
                },
                'visualizacao': {
                    'matplotlib': {'min': '3.8.0', 'max': None, 'required': False},
                    'seaborn': {'min': '0.12.2', 'max': None, 'required': False},
                    'plotly': {'min': '5.17.0', 'max': None, 'required': False},
                },
                'api': {
                    'fastapi': {'min': '0.103.0', 'max': None, 'required': False},
                    'uvicorn': {'min': '0.24.0', 'max': None, 'required': False},
                    'pydantic': {'min': '2.3.0', 'max': None, 'required': False},
                },
                'testes': {
                    'pytest': {'min': '7.4.0', 'max': None, 'required': False},
                    'pytest-cov': {'min': '4.1.0', 'max': None, 'required': False},
                    'unittest': {'min': None, 'max': None, 'required': False},
                }
            },
            'compatibility': {
                'numpy': ['pandas<2.2', 'tensorflow<2.15'],
                'tensorflow': ['numpy>=1.24,<1.26']
            }
        }
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Carrega configuração de arquivo JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            warnings.warn(f"Erro ao carregar arquivo de configuração: {e}")
            return self._get_default_config()
    
    def _build_dependency_list(self) -> Dict[str, Dict]:
        """Constrói a lista de dependências baseada no tipo de projeto"""
        dependencies = {}
        
        # Adiciona dependências base
        base_deps = self.config['dependencies'].get('base', {})
        dependencies.update(base_deps)
        
        # Adiciona dependências específicas do tipo de projeto
        if self.project_type == 'completo':
            for category in self.config['dependencies']:
                if category != 'base':
                    dependencies.update(self.config['dependencies'][category])
        elif self.project_type in self.config['dependencies']:
            dependencies.update(self.config['dependencies'][self.project_type])
        elif self.project_type in [pt.value for pt in ProjectType]:
            # Se for um tipo válido mas não está na configuração
            warnings.warn(f"Tipo de projeto '{self.project_type}' não encontrado na configuração")
        
        return dependencies
    
    def _print_header(self):
        """Imprime cabeçalho informativo"""
        print("\n" + "="*70)
        print("📦 DEPENDENCY CHECKER - Verificação de Dependências Python")
        print("="*70)
        print(f"📁 Tipo de projeto: {self.project_type}")
        print(f"🐍 Python: {self.system_info['python_version'].split()[0]}")
        print(f"💻 Sistema: {self.system_info['platform']}")
        print("="*70)
    
    def check_all(self) -> Dict[str, List]:
        """
        Verifica todas as dependências
        
        Returns:
            Dicionário com resultados da verificação
        """
        if self.verbose:
            print(f"\n🔍 Verificando {len(self.dependencies)} dependências...")
        
        for dep_name, dep_info in self.dependencies.items():
            self._check_dependency(dep_name, dep_info)
        
        if self.check_compatibility:
            self._check_compatibility()
        
        self._generate_summary()
        return self.results
    
    def _check_dependency(self, dep_name: str, dep_info: Dict):
        """Verifica uma dependência individual"""
        try:
            # Tenta obter a distribuição instalada
            dist = pkg_resources.get_distribution(dep_name)
            installed_version = dist.version
            
            # Verifica versão mínima
            min_version = dep_info.get('min')
            if min_version and version.parse(installed_version) < version.parse(min_version):
                self.results['desatualizados'].append({
                    'nome': dep_name,
                    'instalado': installed_version,
                    'requerido': min_version,
                    'tipo': 'min_version'
                })
                status = DependencyStatus.OUTDATED
            else:
                # Verifica versão máxima
                max_version = dep_info.get('max')
                if max_version and version.parse(installed_version) > version.parse(max_version):
                    self.results['incompativeis'].append({
                        'nome': dep_name,
                        'instalado': installed_version,
                        'max_permitido': max_version,
                        'tipo': 'max_version'
                    })
                    status = DependencyStatus.INCOMPATIBLE
                else:
                    self.results['instalados'].append({
                        'nome': dep_name,
                        'versao': installed_version
                    })
                    status = DependencyStatus.INSTALLED
            
            if self.verbose:
                self._print_dependency_status(dep_name, status, installed_version)
                
        except pkg_resources.DistributionNotFound:
            if dep_info.get('required', False):
                self.results['ausentes'].append({
                    'nome': dep_name,
                    'requerido': dep_info.get('min', 'any'),
                    'tipo': 'required'
                })
            else:
                self.results['warnings'].append({
                    'nome': dep_name,
                    'mensagem': f"Dependência opcional não instalada",
                    'tipo': 'optional_missing'
                })
            
            status = DependencyStatus.MISSING
            if self.verbose:
                self._print_dependency_status(dep_name, status)
                
        except Exception as e:
            self.results['erros'].append({
                'nome': dep_name,
                'erro': str(e),
                'tipo': 'check_error'
            })
            status = DependencyStatus.ERROR
            if self.verbose:
                print(f"❌ {dep_name}: ERRO - {str(e)}")
    
    def _print_dependency_status(self, dep_name: str, status: DependencyStatus,
                                version: Optional[str]=None):
        """Imprime o status de uma dependência"""
        icons = {
            DependencyStatus.INSTALLED: "✅",
            DependencyStatus.MISSING: "❌",
            DependencyStatus.OUTDATED: "⚠️ ",
            DependencyStatus.INCOMPATIBLE: "🚫",
            DependencyStatus.ERROR: "💥"
        }
        
        status_text = {
            DependencyStatus.INSTALLED: f"OK ({version})",
            DependencyStatus.MISSING: "NÃO INSTALADO",
            DependencyStatus.OUTDATED: f"DESATUALIZADO ({version} < requerida)",
            DependencyStatus.INCOMPATIBLE: f"INCOMPATÍVEL ({version} > máxima permitida)",
            DependencyStatus.ERROR: "ERRO NA VERIFICAÇÃO"
        }
        
        print(f"{icons[status]} {dep_name}: {status_text[status]}")
    
    def _check_compatibility(self):
        """Verifica compatibilidade entre pacotes instalados"""
        compatibility_rules = self.config.get('compatibility', {})
        
        for package, rules in compatibility_rules.items():
            try:
                installed = pkg_resources.get_distribution(package)
                for rule in rules:
                    # Implementar lógica de verificação de compatibilidade
                    pass
            except:
                continue
    
    def _generate_summary(self):
        """Gera resumo da verificação"""
        print("\n" + "="*70)
        print("📊 RESUMO DA VERIFICAÇÃO")
        print("="*70)
        
        print(f"✅  Instalados: {len(self.results['instalados'])}")
        print(f"❌  Ausentes: {len(self.results['ausentes'])}")
        print(f"⚠️   Desatualizados: {len(self.results['desatualizados'])}")
        print(f"🚫  Incompatíveis: {len(self.results['incompativeis'])}")
        print(f"💥  Erros: {len(self.results['erros'])}")
        print(f"🔶  Warnings: {len(self.results['warnings'])}")
        print("-"*70)
        
        # Mostra recomendações
        if self.results['ausentes']:
            print("\n📋 DEPENDÊNCIAS AUSENTES (Recomendadas):")
            for dep in self.results['ausentes']:
                print(f"   pip install {dep['nome']}>={dep['requerido']}")
        
        if self.results['desatualizados']:
            print("\n🔄 DEPENDÊNCIAS DESATUALIZADAS:")
            for dep in self.results['desatualizados']:
                print(f"   pip install --upgrade {dep['nome']}")
    
    def generate_requirements_file(self, filename: str="requirements.txt"):
        """Gera arquivo requirements.txt com as versões instaladas"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Requirements generated by DependencyChecker\n")
                f.write(f"# Project type: {self.project_type}\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Python: {sys.version.split()[0]}\n\n")
                
                for dep in self.results['instalados']:
                    f.write(f"{dep['nome']}=={dep['versao']}\n")
            
            print(f"\n💾 Arquivo '{filename}' gerado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao gerar arquivo: {e}")
            return False
    
    def save_report(self, format: str='markdown', output_dir: str='.'):
        """Salva relatório detalhado"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'markdown':
            filename = os.path.join(output_dir, f'dependency_report_{timestamp}.md')
            self._save_markdown_report(filename)
        elif format == 'json':
            filename = os.path.join(output_dir, f'dependency_report_{timestamp}.json')
            self._save_json_report(filename)
        else:
            print(f"❌ Formato '{format}' não suportado")
            return
        
        print(f"📄 Relatório salvo em: {filename}")
        return filename
    
    def _save_markdown_report(self, filename: str):
        """Salva relatório em formato Markdown"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Relatório de Dependências\n\n")
                
                # Informações do sistema
                f.write("## Informações do Sistema\n")
                f.write(f"- **Python**: {self.system_info['python_version'].split()[0]}\n")
                f.write(f"- **Sistema**: {self.system_info['platform']}\n")
                f.write(f"- **Processador**: {self.system_info['processor']}\n")
                f.write(f"- **Tipo de projeto**: {self.project_type}\n")
                f.write(f"- **Data da verificação**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Resumo
                f.write("## Resumo\n")
                f.write(f"- ✅ **Instalados**: {len(self.results['instalados'])}\n")
                f.write(f"- ❌ **Ausentes**: {len(self.results['ausentes'])}\n")
                f.write(f"- ⚠️  **Desatualizados**: {len(self.results['desatualizados'])}\n")
                f.write(f"- 🚫 **Incompatíveis**: {len(self.results['incompativeis'])}\n")
                f.write(f"- 💥 **Erros**: {len(self.results['erros'])}\n")
                f.write(f"- 🔶 **Warnings**: {len(self.results['warnings'])}\n\n")
                
                # Detalhes
                if self.results['instalados']:
                    f.write("## ✅ Dependências Instaladas\n")
                    for dep in self.results['instalados']:
                        f.write(f"- **{dep['nome']}**: {dep['versao']}\n")
                    f.write("\n")
                
                if self.results['ausentes']:
                    f.write("## ❌ Dependências Ausentes\n")
                    for dep in self.results['ausentes']:
                        f.write(f"- **{dep['nome']}** (requerido: {dep['requerido']})\n")
                    f.write("\n")
                
                if self.results['desatualizados']:
                    f.write("## ⚠️  Dependências Desatualizadas\n")
                    for dep in self.results['desatualizados']:
                        f.write(f"- **{dep['nome']}**: {dep['instalado']} < {dep['requerido']}\n")
                    f.write("\n")
                
                # Comandos de instalação
                if self.results['ausentes'] or self.results['desatualizados']:
                    f.write("## 📦 Comandos de Instalação\n")
                    f.write("```bash\n")
                    for dep in self.results['ausentes']:
                        f.write(f"pip install {dep['nome']}>={dep['requerido']}\n")
                    for dep in self.results['desatualizados']:
                        f.write(f"pip install --upgrade {dep['nome']}\n")
                    f.write("```\n")
        except Exception as e:
            print(f"❌ Erro ao salvar relatório Markdown: {e}")
    
    def _save_json_report(self, filename: str):
        """Salva relatório em formato JSON"""
        try:
            report = {
                'metadata': {
                    'project_type': self.project_type,
                    'system_info': self.system_info,
                    'timestamp': datetime.now().isoformat(),
                    'checker_version': '1.0.0'
                },
                'results': self.results,
                'dependencies_checked': self.dependencies
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar relatório JSON: {e}")
    
    def list_project_types(self):
        """Lista todos os tipos de projetos disponíveis"""
        print("\n📂 Tipos de Projetos Disponíveis:\n")
        for project_type in ProjectType:
            print(f"  • {project_type.value}")
        
        print("\n📋 Dependências por tipo:")
        for project_type in ProjectType:
            print(f"\n  {project_type.value.upper()}:")
            temp_checker = DependencyChecker(project_type.value, verbose=False)
            deps_count = len(temp_checker.dependencies)
            print(f"    {deps_count} dependências")
    
    def install_missing(self, upgrade_outdated: bool=True):
        """Instala dependências ausentes e atualiza desatualizadas"""
        commands = []
        
        # Comandos para instalar ausentes
        for dep in self.results['ausentes']:
            commands.append(f"pip install {dep['nome']}>={dep['requerido']}")
        
        # Comandos para atualizar desatualizados
        if upgrade_outdated:
            for dep in self.results['desatualizados']:
                commands.append(f"pip install --upgrade {dep['nome']}")
        
        if not commands:
            print("✅ Todas as dependências estão atualizadas!")
            return
        
        print(f"\n🔧 Executando {len(commands)} comandos de instalação...")
        
        for cmd in commands:
            print(f"\n⚙️  Executando: {cmd}")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ Sucesso!")
                else:
                    print(f"   ❌ Erro: {result.stderr[:200]}")
            except Exception as e:
                print(f"   💥 Falha: {e}")


def main():
    """Função principal com suporte a argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description='Verificador e Gerenciador de Dependências Python',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s                        # Verifica todas as dependências
  %(prog)s --type ia              # Verifica apenas dependências de IA
  %(prog)s --type trading --install  # Verifica e instala dependências de trading
  %(prog)s --list-types           # Lista todos os tipos de projetos
  %(prog)s --generate-requirements # Gera arquivo requirements.txt
  %(prog)s --config custom.json   # Usa arquivo de configuração customizado
        """
    )
    
    parser.add_argument('--type', '-t', default='completo',
                       choices=[pt.value for pt in ProjectType],
                       help='Tipo de projeto (padrão: completo)')
    
    parser.add_argument('--list-types', '-l', action='store_true',
                       help='Lista todos os tipos de projetos disponíveis')
    
    parser.add_argument('--install', '-i', action='store_true',
                       help='Instala dependências ausentes e atualiza desatualizadas')
    
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Modo silencioso (menos saída)')
    
    parser.add_argument('--generate-requirements', '-g', action='store_true',
                       help='Gera arquivo requirements.txt')
    
    parser.add_argument('--config', '-c', type=str,
                       help='Arquivo de configuração JSON customizado')
    
    parser.add_argument('--output', '-o', default='.',
                       help='Diretório de saída para relatórios')
    
    parser.add_argument('--format', '-f', default='markdown',
                       choices=['markdown', 'json', 'both'],
                       help='Formato do relatório')
    
    args = parser.parse_args()
    
    # Listar tipos de projetos se solicitado
    if args.list_types:
        checker = DependencyChecker(verbose=False)
        checker.list_project_types()
        return
    
    # Inicializa o verificador
    checker = DependencyChecker(
        project_type=args.type,
        verbose=not args.quiet,
        config_file=args.config
    )
    
    # Executa verificação
    results = checker.check_all()
    
    # Gera requirements.txt se solicitado
    if args.generate_requirements:
        checker.generate_requirements_file()
    
    # Instala dependências se solicitado
    if args.install:
        checker.install_missing()
    
    # Salva relatórios
    if args.format in ['markdown', 'both']:
        checker.save_report('markdown', args.output)
    
    if args.format in ['json', 'both']:
        checker.save_report('json', args.output)
    
    # Retorna código de saída apropriado
    if results['ausentes'] or results['erros']:
        sys.exit(1)
    elif results['desatualizados']:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    # Instala o módulo packaging se não estiver disponível
    try:
        import packaging.version
    except ImportError:
        print("⚠️  Instalando módulo 'packaging' necessário para verificação de versões...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "packaging"])
        import packaging.version
    
    main()
