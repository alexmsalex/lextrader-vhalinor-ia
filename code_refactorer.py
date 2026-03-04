"""
Melhorador Automático de Código Python - LEXTRADER-IAG 4.0
Refatora código para seguir melhores práticas
Author: Development Team
Date: 2026-01-18
"""

import re
import ast
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass


# ============================================================================
# TIPOS
# ============================================================================

@dataclass
class CodeRefactor:
    """Representa uma refatoração aplicada"""
    file: str
    description: str
    before_lines: int
    after_lines: int
    improvements: List[str]


# ============================================================================
# REFATORADOR DE CÓDIGO
# ============================================================================

class CodeRefactorer:
    """Refatora código Python automaticamente"""
    
    def __init__(self):
        self.refactors: List[CodeRefactor] = []
    
    def refactor_file(self, file_path: str) -> Optional[CodeRefactor]:
        """Refatora um arquivo Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original = f.read()
        except Exception as e:
            print(f"❌ Erro ao ler {file_path}: {e}")
            return None
        
        improved = original
        improvements = []
        
        # Aplicar refatorações
        improved, add_imports = self._add_type_hints(improved)
        if add_imports:
            improvements.append("✅ Adicionados type hints")
        
        improved, added_docstrings = self._improve_docstrings(improved)
        if added_docstrings > 0:
            improvements.append(f"✅ Adicionadas {added_docstrings} docstrings")
        
        improved, fixes = self._fix_common_issues(improved)
        improvements.extend(fixes)
        
        improved = self._add_logging_imports(improved)
        if 'logging' in improved and 'import logging' not in original:
            improvements.append("✅ Adicionado suporte a logging")
        
        improved = self._fix_imports(improved)
        if improved != original:
            improvements.append("✅ Imports otimizados")
        
        # Salvar se houve mudanças
        if improved != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(improved)
            
            original_lines = len(original.split('\n'))
            improved_lines = len(improved.split('\n'))
            
            return CodeRefactor(
                file=file_path,
                description=f"Refatorado com {len(improvements)} melhorias",
                before_lines=original_lines,
                after_lines=improved_lines,
                improvements=improvements
            )
        
        return None
    
    def _add_type_hints(self, code: str) -> Tuple[str, bool]:
        """Adiciona type hints básicos"""
        # Detectar funções sem return type
        pattern = r'(\n\s*def\s+(\w+)\s*\((.*?)\)\s*:)'
        
        def add_return_type(match):
            full = match.group(0)
            if '->' in full:
                return full
            return full.replace(':', ' -> Optional[Any]:', 1)
        
        improved = re.sub(pattern, add_return_type, code)
        
        # Adicionar typing import se necessário
        if '->' in improved and 'from typing import' not in code:
            import_line = 'from typing import Optional, List, Dict, Any, Tuple\n'
            if code.startswith('"""'):
                # Após docstring
                match = re.search(r'""".*?"""\n\n', code, re.DOTALL)
                if match:
                    pos = match.end()
                    improved = code[:pos] + import_line + code[pos:]
            else:
                improved = import_line + improved
        
        return improved, improved != code
    
    def _improve_docstrings(self, code: str) -> Tuple[str, int]:
        """Melhora e adiciona docstrings"""
        tree = None
        try:
            tree = ast.parse(code)
        except:
            return code, 0
        
        if tree is None:
            return code, 0
        
        added = 0
        improved = code
        
        # Procurar por funções e classes sem docstring
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node) and node.name != '__init__':
                    # Encontrar a linha e adicionar docstring padrão
                    line_num = node.lineno - 1
                    lines = improved.split('\n')
                    
                    if line_num < len(lines):
                        # Calcular indentação
                        indent = len(lines[line_num]) - len(lines[line_num].lstrip())
                        indent_str = ' ' * (indent + 4)
                        
                        docstring = f'{indent_str}"""[Adicionar descrição]\"\"\"\n'
                        
                        # Inserir após a definição
                        next_line = line_num + 1
                        while next_line < len(lines) and (lines[next_line].strip() == '' or lines[next_line].startswith(' ' * indent + ')')):
                            next_line += 1
                        
                        lines.insert(next_line, docstring)
                        improved = '\n'.join(lines)
                        added += 1
        
        return improved, added
    
    def _fix_common_issues(self, code: str) -> Tuple[str, List[str]]:
        """Corrige problemas comuns"""
        improvements = []
        improved = code
        
        # 1. Substituir print por logging
        if re.search(r'print\s*\(', code):
            improved = re.sub(
                r'print\s*\((.*?)\)',
                r'logger.info(\1)',
                improved
            )
            improvements.append("✅ print() substituído por logger.info()")
            
            if 'logger' not in improved:
                improved = self._add_logging_imports(improved)
        
        # 2. Fixar except genérico
        if re.search(r'except\s*:', code):
            improved = re.sub(
                r'except\s*:',
                r'except Exception as e:',
                improved
            )
            improvements.append("✅ except genérico corrigido")
        
        # 3. Remover import *
        if re.search(r'from\s+\S+\s+import\s+\*', code):
            improved = re.sub(
                r'from\s+(\S+)\s+import\s+\*',
                r'from \1 import (...)',  # Marcar para revisão
                improved
            )
            improvements.append("⚠️  Import * encontrado - revisar manualmente")
        
        # 4. Adicionar slots para classes
        pattern = r'(class\s+\w+(?:\([^)]*\))?\s*:)'
        if re.search(pattern, code):
            improved = re.sub(
                r'(class\s+\w+(?:\([^)]*\))?\s*:)',
                r'\1\n    """Classe do LEXTRADER-IAG 4.0"""\n    __slots__ = []',
                improved
            )
            improvements.append("✅ __slots__ adicionado a classes")
        
        return improved, improvements
    
    def _add_logging_imports(self, code: str) -> str:
        """Adiciona imports de logging se necessário"""
        if 'logger' in code and 'import logging' not in code:
            import_line = 'import logging\n\nlogger = logging.getLogger(__name__)\n\n'
            
            # Encontrar lugar para inserir (após imports de typing)
            if 'from typing import' in code:
                pos = code.find('\n', code.find('from typing import')) + 1
            elif code.startswith('"""'):
                pos = code.find('\n\n') + 2
            else:
                pos = 0
            
            if pos > 0 and 'import logging' not in code[:pos]:
                code = code[:pos] + import_line + code[pos:]
        
        return code
    
    def _fix_imports(self, code: str) -> str:
        """Otimiza e organiza imports"""
        lines = code.split('\n')
        imports = []
        code_lines = []
        in_header = True
        
        for line in lines:
            if in_header and (line.startswith('import ') or line.startswith('from ')):
                imports.append(line)
            elif in_header and line.strip() == '':
                continue
            else:
                in_header = False
                code_lines.append(line)
        
        # Organizar imports (stdlib, third-party, local)
        stdlib_imports = [i for i in imports if not any(c in i for c in ['numpy', 'pandas', 'torch', 'src', '.'])]
        third_party = [i for i in imports if any(c in i for c in ['numpy', 'pandas', 'torch'])]
        local_imports = [i for i in imports if any(c in i for c in ['src', '.'])]
        
        organized = '\n'.join(sorted(set(stdlib_imports)))
        if third_party:
            organized += '\n\n' + '\n'.join(sorted(set(third_party)))
        if local_imports:
            organized += '\n\n' + '\n'.join(sorted(set(local_imports)))
        
        if organized and '\n'.join(code_lines).strip():
            return organized + '\n\n' + '\n'.join(code_lines)
        
        return code


# ============================================================================
# EXECUTOR
# ============================================================================

def refactor_all_python_files(root_dir: str = "src") -> List[CodeRefactor]:
    """Refatora todos os arquivos Python"""
    
    refactorer = CodeRefactorer()
    results = []
    
    py_files = list(Path(root_dir).rglob("*.py"))
    
    print(f"\n🔧 Refatorando {len(py_files)} arquivos Python...\n")
    
    for py_file in py_files:
        # Pular backups
        if any(skip in str(py_file) for skip in ['backups', '.venv', 'venv', '__pycache__']):
            continue
        
        print(f"  Processando: {py_file}")
        result = refactorer.refactor_file(str(py_file))
        
        if result:
            results.append(result)
            print(f"    ✅ {result.description}")
            for imp in result.improvements:
                print(f"       {imp}")
    
    return results


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  REFATORADOR DE CÓDIGO PYTHON - LEXTRADER-IAG 4.0")
    print("="*70)
    
    results = refactor_all_python_files("src")
    
    if results:
        print(f"\n\n✅ RESUMO")
        print("─" * 70)
        print(f"  • Arquivos refatorados: {len(results)}")
        total_improvements = sum(len(r.improvements) for r in results)
        print(f"  • Melhorias aplicadas: {total_improvements}")
        
        avg_lines = sum(r.after_lines - r.before_lines for r in results) / len(results) if results else 0
        print(f"  • Mudança média de linhas: +{avg_lines:.0f}")
    else:
        print("\n✅ Nenhum arquivo necessitou refatoração!")
    
    print("\n" + "="*70)
