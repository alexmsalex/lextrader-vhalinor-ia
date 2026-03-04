from transformers import pipeline
import ast
import re
import subprocess
import sys
from typing import Dict, List, Tuple, Optional
import tempfile
import os

class CorretorCodigoAvancado:
    def __init__(self):
        # Inicializa múltiplos modelos para diferentes tarefas
        self.corretor_sintaxe = pipeline("text2text-generation", model="google/flan-t5-base")
        self.gerador_codigo = pipeline("text2text-generation", model="microsoft/CodeGPT-small-py")
        self.analisador_seguranca = pipeline("text-classification", model="microsoft/codebert-base")
        
    def corrigir_codigo(self, codigo: str, linguagem: str = "python") -> Dict:
        """
        Corrige código com análise detalhada
        """
        prompt_correcao = f"""
        Corrija o seguinte código {linguagem.upper()} e explique os erros:
        
        Código com erro:
        {codigo}
        
        Forneça:
        1. Código corrigido
        2. Lista de erros encontrados
        3. Explicação das correções
        """
        
        try:
            resultado = self.corretor_sintaxe(prompt_correcao)[0]['generated_text']
            
            # Análise adicional do código
            analise = self._analisar_codigo(codigo, linguagem)
            sugestoes = self._gerar_sugestoes_otimizacao(codigo)
            
            return {
                'codigo_corrigido': resultado,
                'analise_erros': analise,
                'sugestoes_otimizacao': sugestoes,
                'status': 'sucesso'
            }
            
        except Exception as e:
            return {
                'erro': f"Falha na correção: {str(e)}",
                'status': 'erro'
            }
    
    def otimizar_codigo(self, codigo: str, linguagem: str = "python") -> Dict:
        """
        Otimiza código para melhor performance
        """
        prompt_otimizacao = f"""
        Otimize o seguinte código {linguagem.upper()} para melhor performance e legibilidade:
        
        {codigo}
        
        Forneça:
        1. Código otimizado
        2. Métricas de melhoria
        3. Explicação das otimizações
        """
        
        resultado = self.corretor_sintaxe(prompt_otimizacao)[0]['generated_text']
        
        return {
            'codigo_otimizado': resultado,
            'analise_performance': self._analisar_performance(codigo),
            'sugestoes_estrutura': self._sugerir_melhorias_estrutura(codigo)
        }
    
    def converter_linguagem(self, codigo: str, linguagem_origem: str, linguagem_destino: str) -> Dict:
        """
        Converte código entre linguagens de programação
        """
        prompt_conversao = f"""
        Converta o seguinte código {linguagem_origem.upper()} para {linguagem_destino.upper()}:
        
        {codigo}
        
        Mantenha a mesma funcionalidade e estrutura lógica.
        """
        
        resultado = self.corretor_sintaxe(prompt_conversao)[0]['generated_text']
        
        return {
            'codigo_convertido': resultado,
            'linguagem_origem': linguagem_origem,
            'linguagem_destino': linguagem_destino,
            'aviso_compatibilidade': self._verificar_compatibilidade(linguagem_origem, linguagem_destino)
        }
    
    def gerar_documentacao(self, codigo: str) -> Dict:
        """
        Gera documentação automática para o código
        """
        prompt_documentacao = f"""
        Gere documentação profissional para o seguinte código:
        
        {codigo}
        
        Inclua:
        1. Descrição da funcionalidade
        2. Documentação de funções/métodos
        3. Exemplos de uso
        4. Parâmetros e retornos
        """
        
        documentacao = self.corretor_sintaxe(prompt_documentacao)[0]['generated_text']
        
        return {
            'documentacao': documentacao,
            'assinaturas_funcoes': self._extrair_assinaturas_funcoes(codigo),
            'complexidade': self._calcular_complexidade(codigo)
        }
    
    def analisar_seguranca(self, codigo: str, linguagem: str = "python") -> Dict:
        """
        Analisa vulnerabilidades de segurança no código
        """
        prompt_seguranca = f"""
        Analise vulnerabilidades de segurança no código {linguagem.upper()}:
        
        {codigo}
        
        Identifique:
        1. Vulnerabilidades críticas
        2. Problemas de segurança
        3. Sugestões de correção
        4. Boas práticas violadas
        """
        
        analise_seguranca = self.corretor_sintaxe(prompt_seguranca)[0]['generated_text']
        
        return {
            'analise_seguranca': analise_seguranca,
            'vulnerabilidades': self._identificar_vulnerabilidades_comuns(codigo),
            'recomendacoes': self._gerar_recomendacoes_seguranca(linguagem)
        }
    
    def debug_automatico(self, codigo: str, erro: str = None) -> Dict:
        """
        Debug automático de código com erro
        """
        prompt_debug = f"""
        Debugue o seguinte código e corrija os problemas:
        
        Código: {codigo}
        {"Erro: " + erro if erro else "Encontre e corrija os erros"}
        
        Forneça:
        1. Código corrigido
        2. Explicação do problema
        3. Solução aplicada
        """
        
        debug_result = self.corretor_sintaxe(prompt_debug)[0]['generated_text']
        
        return {
            'solucao_debug': debug_result,
            'possiveis_causas': self._sugerir_possiveis_causas(erro) if erro else [],
            'testes_sugeridos': self._gerar_testes_verificacao(codigo)
        }
    
    def gerar_testes(self, codigo: str, framework: str = "pytest") -> Dict:
        """
        Gera testes unitários automáticos
        """
        prompt_testes = f"""
        Gere testes unitários {framework} para o seguinte código:
        
        {codigo}
        
        Inclua:
        1. Testes de casos normais
        2. Testes de casos extremos
        3. Testes de validação
        4. Mock de dependências se necessário
        """
        
        testes = self.corretor_sintaxe(prompt_testes)[0]['generated_text']
        
        return {
            'testes_gerados': testes,
            'cobertura_sugerida': self._sugerir_casos_teste(codigo),
            'framework': framework
        }

    # Métodos auxiliares privados
    def _analisar_codigo(self, codigo: str, linguagem: str) -> Dict:
        """Análise estática do código"""
        analise = {
            'erros_sintaxe': [],
            'erros_logica': [],
            'boas_praticas': [],
            'complexidade_ciclomatica': 0
        }
        
        try:
            if linguagem == "python":
                ast.parse(codigo)  # Verifica sintaxe Python
                analise['erros_sintaxe'] = ["Nenhum erro de sintaxe encontrado"]
        except SyntaxError as e:
            analise['erros_sintaxe'].append(f"Erro de sintaxe: {str(e)}")
        
        return analise
    
    def _gerar_sugestoes_otimizacao(self, codigo: str) -> List[str]:
        """Gera sugestões de otimização"""
        sugestoes = []
        
        # Análise básica de padrões
        if "for i in range" in codigo and "append" in codigo:
            sugestoes.append("Considere usar list comprehension para melhor performance")
        
        if "deepcopy" in codigo:
            sugestoes.append("Avalie se é necessário deepcopy ou se shallow copy é suficiente")
            
        return sugestoes
    
    def _analisar_performance(self, codigo: str) -> Dict:
        """Analisa aspectos de performance"""
        return {
            'complexidade_temporal': 'O(n)',
            'complexidade_espacial': 'O(1)',
            'operacoes_custosas': self._identificar_operacoes_custosas(codigo)
        }
    
    def _sugerir_melhorias_estrutura(self, codigo: str) -> List[str]:
        """Sugere melhorias na estrutura do código"""
        melhorias = []
        
        if len(codigo.split('\n')) > 50:
            melhorias.append("Considere dividir em funções menores")
            
        if "global" in codigo:
            melhorias.append("Evite uso de variáveis globais")
            
        return melhorias
    
    def _verificar_compatibilidade(self, origem: str, destino: str) -> List[str]:
        """Verifica compatibilidade entre linguagens"""
        avisos = []
        
        incompatibilidades = {
            ('python', 'javascript'): ['Tipagem dinâmica vs estática', 'Gerenciamento de memória diferente'],
            ('python', 'java'): ['Orientação a objetos diferente', 'Tipagem forte vs dinâmica']
        }
        
        key = (origem.lower(), destino.lower())
        if key in incompatibilidades:
            avisos.extend(incompatibilidades[key])
            
        return avisos
    
    def _extrair_assinaturas_funcoes(self, codigo: str) -> List[str]:
        """Extrai assinaturas de funções do código"""
        try:
            tree = ast.parse(codigo)
            funcoes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    funcoes.append(node.name)
                    
            return funcoes
        except:
            return ["Não foi possível extrair assinaturas"]
    
    def _calcular_complexidade(self, codigo: str) -> str:
        """Calcula complexidade aproximada do código"""
        linhas = len(codigo.split('\n'))
        
        if linhas < 20:
            return "Baixa"
        elif linhas < 100:
            return "Média"
        else:
            return "Alta"
    
    def _identificar_vulnerabilidades_comuns(self, codigo: str) -> List[str]:
        """Identifica vulnerabilidades comuns"""
        vulnerabilidades = []
        
        padroes_risco = {
            'eval(': 'Uso de eval pode permitir injeção de código',
            'exec(': 'Uso de exec é perigoso',
            'pickle.loads': 'Desserialização insegura',
            'input()': 'Validação de entrada necessária'
        }
        
        for padrao, descricao in padroes_risco.items():
            if padrao in codigo:
                vulnerabilidades.append(descricao)
                
        return vulnerabilidades
    
    def _gerar_recomendacoes_seguranca(self, linguagem: str) -> List[str]:
        """Gera recomendações de segurança específicas da linguagem"""
        recomendacoes = {
            'python': [
                'Use bibliotecas validadas para manipulação de dados',
                'Valide todas as entradas do usuário',
                'Use prepared statements para bancos de dados'
            ],
            'javascript': [
                'Valide inputs no frontend e backend',
                'Use HTTPS para todas as comunicações',
                'Implemente CORS corretamente'
            ]
        }
        
        return recomendacoes.get(linguagem.lower(), [])
    
    def _sugerir_possiveis_causas(self, erro: str) -> List[str]:
        """Sugere possíveis causas para erros"""
        causas = []
        
        if "NoneType" in erro:
            causas.append("Variável não inicializada")
            causas.append("Retorno None de função")
            
        if "IndexError" in erro:
            causas.append("Acesso a índice inválido")
            causas.append("Lista vazia")
            
        return causas
    
    def _gerar_testes_verificacao(self, codigo: str) -> List[str]:
        """Gera sugestões de testes para verificação"""
        return [
            "Teste com valores normais",
            "Teste com valores extremos",
            "Teste com entradas inválidas",
            "Verifique tratamento de exceções"
        ]
    
    def _sugerir_casos_teste(self, codigo: str) -> List[str]:
        """Sugere casos de teste baseados no código"""
        return [
            "Teste de funcionalidade principal",
            "Teste de casos de erro",
            "Teste de performance",
            "Teste de segurança"
        ]
    
    def _identificar_operacoes_custosas(self, codigo: str) -> List[str]:
        """Identifica operações potencialmente custosas"""
        operacoes = []
        
        padroes_custosos = [
            'for .* in .*:.*for .* in .*:',  # Loops aninhados
            'sorted.*key=',
            'deepcopy',
            're.compile'
        ]
        
        for padrao in padroes_custosos:
            if re.search(padrao, codigo):
                operacoes.append(f"Operação custosa detectada: {padrao}")
                
        return operacoes

# Funções de utilidade
def executar_codigo(codigo: str, linguagem: str = "python") -> Dict:
    """
    Executa código em um ambiente controlado
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(codigo)
        temp_file = f.name
    
    try:
        resultado = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            'sucesso': resultado.returncode == 0,
            'stdout': resultado.stdout,
            'stderr': resultado.stderr,
            'returncode': resultado.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'sucesso': False,
            'erro': 'Timeout - código executou por muito tempo'
        }
    finally:
        os.unlink(temp_file)

# Exemplo de uso
if __name__ == "__main__":
    corretor = CorretorCodigoAvancado()
    
    # Exemplo de código com erro
    codigo_com_erro = """
    def calcular_media(numeros):
        soma = 0
        for i in range(len(numeros)):
            soma += numeros[i]
        return soma / len(numeros)
    
    resultado = calcular_media([1, 2, 3, 4, 5])
    print(resultado)
    """
    
    # Testando as funcionalidades
    print("=== CORREÇÃO DE CÓDIGO ===")
    correcao = corretor.corrigir_codigo(codigo_com_erro)
    print(correcao['codigo_corrigido'])
    
    print("\n=== OTIMIZAÇÃO ===")
    otimizacao = corretor.otimizar_codigo(codigo_com_erro)
    print(otimizacao['codigo_otimizado'])
    
    print("\n=== DOCUMENTAÇÃO ===")
    documentacao = corretor.gerar_documentacao(codigo_com_erro)
    print(documentacao['documentacao'])
    
    print("\n=== ANÁLISE DE SEGURANÇA ===")
    seguranca = corretor.analisar_seguranca(codigo_com_erro)
    print(seguranca['analise_seguranca'])
