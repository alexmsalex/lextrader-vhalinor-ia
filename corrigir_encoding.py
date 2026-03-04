#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige encoding em todos os arquivos Python criados"""

import os
from pathlib import Path

def corrigir_encoding():
    """Adiciona encoding header em todos os arquivos"""
    
    paths = [
        'neural_layers/01_sensorial/data_aggregator.py',
        'neural_layers/02_processamento/technical_analysis.py',
        'neural_layers/02_processamento/pattern_recognition.py',
        'neural_layers/02_processamento/signal_generator.py',
        'neural_layers/03_memoria_saida/trade_executor.py',
        'neural_layers/03_memoria_saida/order_manager.py',
        'neural_layers/04_decisao/strategy_evaluator.py',
        'neural_layers/04_decisao/risk_calculator.py',
        'neural_layers/04_decisao/decision_maker.py',
        'neural_layers/05_quantico/optimization_engine.py',
        'neural_layers/05_quantico/quantum_simulator.py',
        'neural_layers/06_seguranca/credential_manager.py',
        'neural_layers/06_seguranca/encryption.py',
        'neural_layers/06_seguranca/audit_logger.py',
        'neural_layers/06_seguranca/SecurityManager.py',
        'neural_layers/06_seguranca/AuthManager.py',
    ]
    
    print("\nCorrigindo encoding dos arquivos Python...")
    print("="*60)
    
    for path_str in paths:
        p = Path(path_str)
        if p.exists():
            try:
                # Lê com tratamento de erro
                content = p.read_text(encoding='utf-8', errors='replace')
                
                # Garante encoding header
                if not content.startswith('#!/usr/bin/env python3'):
                    lines = content.split('\n')
                    lines.insert(0, '#!/usr/bin/env python3')
                    lines.insert(1, '# -*- coding: utf-8 -*-')
                    content = '\n'.join(lines)
                elif '# -*- coding: utf-8 -*-' not in content:
                    lines = content.split('\n')
                    lines.insert(1, '# -*- coding: utf-8 -*-')
                    content = '\n'.join(lines)
                
                # Escreve com encoding UTF-8
                p.write_text(content, encoding='utf-8')
                print(f"[OK] {path_str}")
            except Exception as e:
                print(f"[ERRO] {path_str}: {e}")
        else:
            print(f"[SKIP] {path_str} (não existe)")
    
    print("="*60)
    print("[COMPLETO] Encoding corrigido!\n")

if __name__ == "__main__":
    corrigir_encoding()
