#!/usr/bin/env python3
"""
Script de atalho para executar a análise de criptomoedas
O arquivo foi movido para neural_layers/02_processamento/
"""

import sys
import os

# Adiciona o caminho da camada de processamento ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'neural_layers', '02_processamento'))

# Importa e executa o módulo
if __name__ == "__main__":
    import asyncio
    from crypto_analysis_advanced import main
    
    print("🚀 Executando Análise Avançada de Criptomoedas")
    print(f"📁 Localização: neural_layers/02_processamento/crypto_analysis_advanced.py")
    print()
    
    asyncio.run(main())
