#!/usr/bin/env python3
"""
Script para verificar e corrigir registros de módulos neurais no NeuralBus
Identifica módulos que deveriam estar registrados e adiciona o registro quando necessário
"""

import sys
import os
from pathlib import Path
import importlib.util
import ast
import re

def find_neural_modules():
    """Encontra todos os arquivos Python que parecem ser módulos neurais"""
    base_dir = Path(__file__).parent.resolve()
    neural_modules = []
    
    # Padrões de nomes de arquivos neurais
    neural_patterns = [
        r'.*[Nn]eural.*\.py$',
        r'.*[Dd]eep.*[Nn]eural.*\.py$',
        r'.*[Aa]dvanced.*[Nn]eural.*\.py$',
        r'.*[Rr]einforcement.*\.py$',
        r'.*[Ll]earning.*\.py$',
    ]
    
    for file_path in base_dir.glob("*.py"):
        filename = file_path.name
        for pattern in neural_patterns:
            if re.match(pattern, filename):
                neural_modules.append(file_path)
                break
    
    return neural_modules

def check_neural_bus_registration(file_path):
    """Verifica se um arquivo se registra no NeuralBus"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se tem import do neural_bus
        has_import = (
            'from neural_bus import' in content or
            'import neural_bus' in content or
            'from .neural_bus import' in content or
            '.neural_bus' in content
        )
        
        # Verificar se tem registro
        has_register = (
            'NeuralBus.get_instance().register' in content or
            '.register(' in content and 'neural_bus' in content.lower()
        )
        
        # Verificar se tem classe principal
        tree = ast.parse(content)
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        return {
            'file': file_path.name,
            'has_import': has_import,
            'has_register': has_register,
            'classes': classes,
            'should_register': len(classes) > 0 and any(
                'neural' in cls.lower() or 
                'deep' in cls.lower() or
                'advanced' in cls.lower() or
                'learning' in cls.lower()
                for cls in classes
            )
        }
    except Exception as e:
        return {
            'file': file_path.name,
            'error': str(e),
            'has_import': False,
            'has_register': False,
            'classes': []
        }

def add_neural_bus_registration(file_path):
    """Adiciona registro no NeuralBus ao arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Encontrar __init__ ou primeira classe
        tree = ast.parse(''.join(lines))
        init_line = None
        first_class = None
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if first_class is None:
                    first_class = node
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                        init_line = item.lineno - 1
                        break
                if init_line is not None:
                    break
        
        if init_line is None:
            return False, "Não foi possível encontrar __init__"
        
        # Verificar se já tem import
        has_import = any('neural_bus' in line for line in lines)
        
        # Verificar se já tem registro
        has_register = any('NeuralBus.get_instance().register' in line for line in lines)
        
        if has_register:
            return True, "Já registrado"
        
        # Adicionar import se necessário
        if not has_import:
            import_line = None
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_line = i
                    break
            
            if import_line is not None:
                lines.insert(import_line + 1, 'try:\n')
                lines.insert(import_line + 2, '    from neural_bus import NeuralBus\n')
                lines.insert(import_line + 3, 'except ImportError:\n')
                lines.insert(import_line + 4, '    NeuralBus = None\n')
            else:
                # Adicionar no início
                lines.insert(0, 'try:\n')
                lines.insert(1, '    from neural_bus import NeuralBus\n')
                lines.insert(2, 'except ImportError:\n')
                lines.insert(3, '    NeuralBus = None\n')
        
        # Encontrar nome da classe principal
        class_name = first_class.name if first_class else None
        
        if class_name is None:
            return False, "Não foi possível encontrar classe principal"
        
        # Adicionar registro no __init__
        registration_code = f"""        # Registrar no NeuralBus para comunicação entre módulos
        if NeuralBus:
            try:
                NeuralBus.get_instance().register(
                    "{class_name.lower()}", 
                    self,
                    {{"type": "{class_name}", "file": "{file_path.name}"}}
                )
            except Exception:
                pass
"""
        
        # Encontrar linha após última instrução do __init__
        indent = '        '  # 8 espaços
        lines.insert(init_line + 1, registration_code)
        
        # Salvar arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return True, "Registro adicionado"
        
    except Exception as e:
        return False, f"Erro: {str(e)}"

def main():
    """Função principal"""
    print("=" * 60)
    print("VERIFICACAO E CORRECAO DE REGISTRO NOURALBUS")
    print("=" * 60)
    
    neural_modules = find_neural_modules()
    print(f"\nEncontrados {len(neural_modules)} arquivos neurais:\n")
    
    results = []
    needs_registration = []
    
    for module_path in neural_modules:
        result = check_neural_bus_registration(module_path)
        results.append(result)
        
        status = ""
        if result.get('error'):
            status = f"[ERRO] {result['error']}"
            print(f"  {result['file']}: {status}")
        elif result.get('has_register'):
            status = "[OK] Já registrado"
            print(f"  {result['file']}: {status}")
        elif result.get('should_register'):
            status = "[PENDENTE] Precisa registro"
            print(f"  {result['file']}: {status}")
            needs_registration.append((module_path, result))
        else:
            status = "[SKIP] Não precisa registro"
            print(f"  {result['file']}: {status}")
    
    if needs_registration:
        print(f"\n\n{len(needs_registration)} módulos precisam de registro:")
        for module_path, result in needs_registration:
            print(f"  - {module_path.name} (Classes: {', '.join(result['classes'])})")
        
        print("\nDeseja adicionar registros automaticamente? (s/n)")
        response = input().strip().lower()
        
        if response == 's':
            print("\nAdicionando registros...")
            for module_path, result in needs_registration:
                success, message = add_neural_bus_registration(module_path)
                if success:
                    print(f"  [OK] {module_path.name}: {message}")
                else:
                    print(f"  [ERRO] {module_path.name}: {message}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    registered = sum(1 for r in results if r.get('has_register'))
    needs_fix = sum(1 for r in results if r.get('should_register') and not r.get('has_register'))
    total = len(results)
    
    print(f"Total de módulos verificados: {total}")
    print(f"Já registrados: {registered}")
    print(f"Precisam registro: {needs_fix}")
    
    return 0 if needs_fix == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

