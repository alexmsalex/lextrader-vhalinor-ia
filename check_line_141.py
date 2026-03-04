"""
Verifica linha específica do arquivo AutomationService.py
Mostra contexto e informações detalhadas sobre a linha 141
"""

import os
import sys


def verificar_linha_arquivo(nome_arquivo='AutomationService.py', numero_linha=141, contexto=3):
    """
    Verifica uma linha específica de um arquivo com contexto.
    
    Args:
        nome_arquivo (str): Nome do arquivo a ser verificado
        numero_linha (int): Número da linha para verificar (1-indexed)
        contexto (int): Número de linhas de contexto para mostrar
    """
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(nome_arquivo):
            print(f"❌ Arquivo '{nome_arquivo}' não encontrado!")
            return False
        
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Informações gerais
        print(f"📄 Arquivo: {nome_arquivo}")
        print(f"📊 Total de linhas: {len(lines)}")
        print(f"🎯 Linha solicitada: {numero_linha}")
        print("-" * 60)
        
        # Verifica se a linha existe
        if numero_linha > len(lines) or numero_linha < 1:
            print(f"⚠️  Aviso: Linha {numero_linha} está fora do intervalo do arquivo")
            print(f"   Intervalo válido: 1 a {len(lines)}")
            return False
        
        # Calcula o intervalo para mostrar contexto
        inicio = max(0, numero_linha - contexto - 1)  # -1 para converter para 0-indexed
        fim = min(len(lines), numero_linha + contexto)  # já em 0-indexed
        
        print(f"\n📋 Contexto da linha {numero_linha} (linhas {inicio+1} a {fim}):")
        print("-" * 60)
        
        # Mostra as linhas com contexto
        for i in range(inicio, fim):
            linha_atual = i + 1  # Converte para 1-indexed para exibição
            prefixo = ">>>" if linha_atual == numero_linha else "   "
            print(f"{prefixo} Linha {linha_atual:4d}: {repr(lines[i])}")
        
        # Informações específicas da linha solicitada
        print("-" * 60)
        linha_alvo = lines[numero_linha - 1]
        print(f"\n🔍 Análise da linha {numero_linha}:")
        print(f"   Conteúdo bruto: {repr(linha_alvo)}")
        print(f"   Comprimento: {len(linha_alvo)} caracteres")
        print(f"   Está vazia? {linha_alvo.strip() == ''}")
        print(f"   É apenas espaços? {linha_alvo.strip(' \t\n\r') == ''}")
        
        # Mostra conteúdo sem formatação
        if linha_alvo.strip():
            print(f"   Conteúdo limpo: '{linha_alvo.rstrip()}'")
        
        return True
        
    except UnicodeDecodeError:
        print(f"❌ Erro de codificação ao ler '{nome_arquivo}'")
        print("   Tente uma codificação diferente ou verifique o arquivo.")
        return False
    except PermissionError:
        print(f"❌ Permissão negada para ler '{nome_arquivo}'")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {type(e).__name__}: {e}")
        return False


def salvar_linha_em_arquivo(nome_arquivo='AutomationService.py', numero_linha=141,
                           arquivo_saida='linha_141.txt'):
    """Salva uma linha específica em um arquivo separado."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if numero_linha <= len(lines):
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write(f"Linha {numero_linha} de {nome_arquivo}:\n")
                f.write(f"Conteúdo: {repr(lines[numero_linha-1])}\n")
                f.write(f"Texto limpo: {lines[numero_linha-1].rstrip()}\n")
            print(f"\n💾 Linha salva em '{arquivo_saida}'")
            return True
    except Exception as e:
        print(f"❌ Erro ao salvar linha: {e}")
        return False


if __name__ == "__main__":
    # Configurações
    ARQUIVO = 'AutomationService.py'
    LINHA = 141
    CONTEXTO = 5  # Mostra 5 linhas antes e depois
    
    # Executa a verificação
    sucesso = verificar_linha_arquivo(ARQUIVO, LINHA, CONTEXTO)
    
    # Opção para salvar a linha
    if sucesso:
        resposta = input("\n💾 Deseja salvar esta linha em um arquivo separado? (s/N): ")
        if resposta.lower() == 's':
            salvar_linha_em_arquivo(ARQUIVO, LINHA)
    
    # Adiciona linha em branco no final
    print()
    
    # Verifica a linha 141 com contexto padrão
verificar_linha_arquivo('AutomationService.py', 141)

# Verifica com mais contexto
verificar_linha_arquivo('AutomationService.py', 141, contexto=10)

# Verifica outro arquivo
verificar_linha_arquivo('outro_arquivo.py', 50)
# Tenta salvar a linha 141 em um arquivo separado
salvar_linha_em_arquivo('AutomationService.py', 141, 'linha_141.txt')

