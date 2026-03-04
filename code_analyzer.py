"""
Analisador e Melhorador de Código Python - LEXTRADER-IAG 4.0
Aplica melhores práticas, type hints, error handling e otimizações
Author: Development Team
Date: 2026-01-18
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

# ============================================================================
# TIPOS E ESTRUTURAS
# ============================================================================

@dataclass
class CodeIssue:
    """Representa um problema de código identificado"""
    file: str
    line: int
    severity: str  # 'critical', 'warning', 'info'
    issue_type: str
    message: str
    suggestion: str
    
    def __repr__(self) -> str:
        return f"{self.severity.upper()} [{self.issue_type}] {self.file}:{self.line} - {self.message}"


@dataclass
class FileMetrics:
    """Métricas de qualidade de um arquivo"""
    file: str
    lines: int
    functions: int
    classes: int
    imports: int
    has_docstrings: bool
    has_type_hints: bool
    complexity: float
    issues_count: int
    score: float  # 0-100


# ============================================================================
# ANALISADOR DE CÓDIGO
# ============================================================================

class CodeAnalyzer:
    """Analisa arquivos Python para identificar problemas"""
    
    CRITICAL_PATTERNS = {
        r'exec\s*\(': ('Uso de exec() é perigoso', 'security'),
        r'eval\s*\(': ('Uso de eval() é perigoso', 'security'),
        r'import \*': ('Import com * reduz legibilidade', 'style'),
        r'TODO|FIXME|HACK': ('Código incompleto', 'quality'),
        r'print\s*\(': ('Use logging ao invés de print()', 'quality'),
        r'except\s*:\s*pass': ('Except genérico mascarado', 'error_handling'),
    }
    
    def __init__(self):
        self.issues: List[CodeIssue] = []
    
    def analyze_file(self, file_path: str) -> Tuple[List[CodeIssue], FileMetrics]:
        """Analisa um arquivo Python completo"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return [CodeIssue(
                file=file_path,
                line=0,
                severity='critical',
                issue_type='read_error',
                message=f'Erro ao ler arquivo: {str(e)}',
                suggestion='Verificar permissões de arquivo'
            )], FileMetrics(file_path, 0, 0, 0, 0, False, False, 0, 1, 0)
        
        # Análise de padrões
        issues.extend(self._analyze_patterns(file_path, content))
        
        # Análise AST
        try:
            tree = ast.parse(content)
            issues.extend(self._analyze_ast(file_path, tree, content))
        except SyntaxError as e:
            issues.append(CodeIssue(
                file=file_path,
                line=e.lineno or 0,
                severity='critical',
                issue_type='syntax_error',
                message=f'Erro de sintaxe: {str(e)}',
                suggestion='Verificar sintaxe Python'
            ))
        
        # Calcular métricas
        metrics = self._calculate_metrics(file_path, content, issues)
        
        return issues, metrics
    
    def _analyze_patterns(self, file_path: str, content: str) -> List[CodeIssue]:
        """Análise baseada em padrões regex"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern, (message, issue_type) in self.CRITICAL_PATTERNS.items():
                if re.search(pattern, line):
                    issues.append(CodeIssue(
                        file=file_path,
                        line=line_num,
                        severity='warning' if issue_type == 'style' else 'critical',
                        issue_type=issue_type,
                        message=message,
                        suggestion=f'Revisar linha {line_num}'
                    ))
        
        return issues
    
    def _analyze_ast(self, file_path: str, tree: ast.AST, content: str) -> List[CodeIssue]:
        """Análise baseada em AST"""
        issues = []
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            # Funções sem docstring
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node) and node.name != '__init__':
                    issues.append(CodeIssue(
                        file=file_path,
                        line=node.lineno,
                        severity='warning',
                        issue_type='documentation',
                        message=f'{node.__class__.__name__} sem docstring',
                        suggestion=f'Adicionar docstring a {node.name}'
                    ))
            
            # Funções sem type hints
            if isinstance(node, ast.FunctionDef):
                if not node.returns and node.name != '__init__':
                    issues.append(CodeIssue(
                        file=file_path,
                        line=node.lineno,
                        severity='info',
                        issue_type='type_hints',
                        message=f'Função {node.name} sem type hints de return',
                        suggestion=f'Adicionar -> ReturnType a {node.name}'
                    ))
            
            # Imports circulares potenciais (heurística)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if 'neural_layers' in alias.name:
                        # Verificar se é import cruzado
                        if '.' in alias.name and alias.name.count('.') > 2:
                            issues.append(CodeIssue(
                                file=file_path,
                                line=node.lineno,
                                severity='warning',
                                issue_type='imports',
                                message='Import profundo pode indicar acoplamento forte',
                                suggestion=f'Revisar: {alias.name}'
                            ))
        
        return issues
    
    def _calculate_metrics(self, file_path: str, content: str, issues: List[CodeIssue]) -> FileMetrics:
        """Calcula métricas de qualidade do arquivo"""
        lines = content.split('\n')
        functions = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
        classes = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
        imports = len(re.findall(r'^(?:from|import)\s+', content, re.MULTILINE))
        
        has_docstrings = bool(re.search(r'""".*?"""', content, re.DOTALL))
        has_type_hints = bool(re.search(r'->\s*\w+|:\s*\w+', content))
        
        # Complexidade ciclomática aproximada
        complexity = (
            len(re.findall(r'\bif\b', content)) +
            len(re.findall(r'\bfor\b', content)) +
            len(re.findall(r'\bwhile\b', content)) +
            len(re.findall(r'\bexcept\b', content))
        ) / max(functions, 1)
        
        # Score de qualidade (0-100)
        critical_issues = len([i for i in issues if i.severity == 'critical'])
        warning_issues = len([i for i in issues if i.severity == 'warning'])
        
        score = max(0, 100 - (critical_issues * 10 + warning_issues * 5))
        
        return FileMetrics(
            file=file_path,
            lines=len(lines),
            functions=functions,
            classes=classes,
            imports=imports,
            has_docstrings=has_docstrings,
            has_type_hints=has_type_hints,
            complexity=round(complexity, 2),
            issues_count=len(issues),
            score=score
        )


# ============================================================================
# GERADOR DE RELATÓRIO
# ============================================================================

class ReportGenerator:
    """Gera relatórios de análise de código"""
    
    @staticmethod
    def generate_summary(metrics_list: List[FileMetrics]) -> str:
        """Gera resumo das métricas"""
        if not metrics_list:
            return "Nenhum arquivo analisado"
        
        total_lines = sum(m.lines for m in metrics_list)
        avg_score = sum(m.score for m in metrics_list) / len(metrics_list)
        total_issues = sum(m.issues_count for m in metrics_list)
        
        files_with_hints = len([m for m in metrics_list if m.has_type_hints])
        files_with_docs = len([m for m in metrics_list if m.has_docstrings])
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║         ANÁLISE DE QUALIDADE DE CÓDIGO PYTHON                  ║
║              LEXTRADER-IAG 4.0                                  ║
╚════════════════════════════════════════════════════════════════╝

📊 RESUMO GERAL
──────────────────────────────────────────────────────────────────
  • Arquivos analisados: {len(metrics_list)}
  • Total de linhas: {total_lines:,}
  • Score médio: {avg_score:.1f}/100
  • Total de problemas: {total_issues}

📈 ESTATÍSTICAS
──────────────────────────────────────────────────────────────────
  • Arquivos com type hints: {files_with_hints}/{len(metrics_list)} ({100*files_with_hints//len(metrics_list)}%)
  • Arquivos com docstrings: {files_with_docs}/{len(metrics_list)} ({100*files_with_docs//len(metrics_list)}%)
  • Linhas médias por arquivo: {total_lines//len(metrics_list)}
  • Funções totais: {sum(m.functions for m in metrics_list)}
  • Classes totais: {sum(m.classes for m in metrics_list)}

🎯 ARQUIVOS COM MAIS PROBLEMAS
──────────────────────────────────────────────────────────────────
"""
        
        # Top 5 arquivos com mais problemas
        worst_files = sorted(metrics_list, key=lambda m: m.issues_count, reverse=True)[:5]
        for i, m in enumerate(worst_files, 1):
            report += f"  {i}. {m.file}: {m.issues_count} problemas (score: {m.score}/100)\n"
        
        return report
    
    @staticmethod
    def generate_detailed_report(issues: List[CodeIssue]) -> str:
        """Gera relatório detalhado de problemas"""
        if not issues:
            return "✅ Nenhum problema encontrado!"
        
        # Agrupar por tipo
        by_type = defaultdict(list)
        for issue in issues:
            by_type[issue.issue_type].append(issue)
        
        report = "\n🔍 PROBLEMAS DETALHADOS\n"
        report += "─" * 70 + "\n\n"
        
        for issue_type, type_issues in sorted(by_type.items()):
            report += f"📌 {issue_type.upper()} ({len(type_issues)} problemas)\n"
            
            for issue in sorted(type_issues, key=lambda x: (x.file, x.line))[:3]:
                report += f"  • {issue.file}:{issue.line}\n"
                report += f"    └─ {issue.message}\n"
                report += f"    └─ 💡 {issue.suggestion}\n\n"
            
            if len(type_issues) > 3:
                report += f"  ... e mais {len(type_issues) - 3} problemas\n\n"
        
        return report


# ============================================================================
# MELHORADOR DE CÓDIGO
# ============================================================================

class CodeImprover:
    """Propõe melhorias para código Python"""
    
    @staticmethod
    def suggest_improvements(file_path: str, metrics: FileMetrics) -> List[str]:
        """Sugere melhorias específicas"""
        suggestions = []
        
        if not metrics.has_type_hints:
            suggestions.append("❌ Adicionar type hints a todas as funções")
        
        if not metrics.has_docstrings:
            suggestions.append("❌ Adicionar docstrings a funções e classes")
        
        if metrics.complexity > 5:
            suggestions.append(f"⚠️  Complexidade alta ({metrics.complexity}) - Considere refatorar")
        
        if metrics.lines > 500:
            suggestions.append(f"📦 Arquivo grande ({metrics.lines} linhas) - Considere dividir")
        
        if metrics.imports > 15:
            suggestions.append(f"🔗 Muitos imports ({metrics.imports}) - Considere revisar dependências")
        
        return suggestions
    
    @staticmethod
    def generate_template(file_path: str, metrics: FileMetrics) -> str:
        """Gera template melhorado do arquivo"""
        template = f'''"""
{Path(file_path).stem} - Módulo do LEXTRADER-IAG 4.0

Descrição:
    [Adicionar descrição do módulo]

Author: Development Team
Date: 2026-01-18
Version: 1.0

Example:
    >>> from {Path(file_path).stem} import MainClass
    >>> obj = MainClass()
    >>> result = obj.method()
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import logging

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

logger = logging.getLogger(__name__)


# ============================================================================
# TIPOS
# ============================================================================

@dataclass
class ExampleType:
    """Tipo de exemplo"""
    field: str
    value: Any


# ============================================================================
# CLASSES PRINCIPAIS
# ============================================================================

class MainClass:
    """Classe principal do módulo"""
    
    def __init__(self):
        """Inicializa a classe"""
        logger.info("MainClass inicializada")
    
    def method(self) -> str:
        """
        Método de exemplo
        
        Returns:
            str: Resultado do método
        """
        return "resultado"


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def helper_function(param: str) -> Optional[str]:
    """
    Função auxiliar
    
    Args:
        param: Parâmetro de entrada
    
    Returns:
        Resultado processado ou None em caso de erro
    
    Raises:
        ValueError: Se param for vazio
    """
    if not param:
        raise ValueError("param não pode ser vazio")
    
    return param.upper()


if __name__ == "__main__":
    # Exemplo de uso
    obj = MainClass()
    result = obj.method()
    print(f"Resultado: {{result}}")
'''
        
        return template


# ============================================================================
# EXECUTOR PRINCIPAL
# ============================================================================

def analyze_all_python_files(root_dir: str = ".") -> Tuple[List[FileMetrics], List[CodeIssue]]:
    """Analisa todos os arquivos Python do projeto"""
    
    analyzer = CodeAnalyzer()
    all_metrics = []
    all_issues = []
    
    py_files = list(Path(root_dir).rglob("*.py"))
    
    print(f"\n🔍 Analisando {len(py_files)} arquivos Python...\n")
    
    for py_file in py_files:
        # Pular arquivos de backup e venv
        if any(skip in str(py_file) for skip in ['backups', '.venv', 'venv', '__pycache__']):
            continue
        
        issues, metrics = analyzer.analyze_file(str(py_file))
        all_metrics.append(metrics)
        all_issues.extend(issues)
    
    return all_metrics, all_issues


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("\n" + "="*70)
    print("  ANALISADOR DE CÓDIGO PYTHON - LEXTRADER-IAG 4.0")
    print("="*70)
    
    metrics, issues = analyze_all_python_files(root)
    
    if metrics:
        print(ReportGenerator.generate_summary(metrics))
        print(ReportGenerator.generate_detailed_report(issues[:20]))
        
        # Arquivos com melhor score
        print("\n✅ ARQUIVOS COM MELHOR QUALIDADE")
        print("─" * 70)
        best = sorted(metrics, key=lambda m: m.score, reverse=True)[:5]
        for m in best:
            print(f"  • {m.file}: {m.score:.0f}/100")
    
    print("\n" + "="*70)
