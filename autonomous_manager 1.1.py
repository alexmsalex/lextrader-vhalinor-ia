import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

class AutonomoGerenciador:
    """Gerenciador Autônomo com IA Neural"""
    def __init__(self):
        self.config = {
            'risk_tolerance': 0.3,
            'min_confidence': 0.75,
            'learning_rate': 0.001,
            'memory_size': 1000,
            'batch_size': 32
        }
        
        self.memory_buffer = []
        self.model = self.criar_modelo_neural()
        self.scaler = MinMaxScaler()
        self.experiencia = ExperienciaManager()

    def criar_modelo_neural(self):
        """Cria modelo LSTM para aprendizado"""
        model = Sequential([
            LSTM(units=64, return_sequences=True, 
                 input_shape=(60, 6)),  # 60 timesteps, 6 features
            Dropout(0.2),
            LSTM(units=32),
            Dropout(0.2),
            Dense(units=16, activation='relu'),
            Dense(units=3, activation='softmax')  # Comprar, Vender, Manter
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=self.config['learning_rate']
            ),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def aprender_experiencia(self, estado, acao, recompensa, proximo_estado):
        """Aprende com experiências passadas"""
        self.memory_buffer.append({
            'estado': estado,
            'acao': acao,
            'recompensa': recompensa,
            'proximo_estado': proximo_estado
        })
        
        if len(self.memory_buffer) > self.config['memory_size']:
            self.memory_buffer.pop(0)
            
        # Treina com batch de experiências
        if len(self.memory_buffer) >= self.config['batch_size']:
            self.treinar_com_experiencias()

    def treinar_com_experiencias(self):
        """Treina modelo com experiências armazenadas"""
        batch = np.random.choice(
            self.memory_buffer, 
            size=self.config['batch_size']
        )
        
        estados = np.array([exp['estado'] for exp in batch])
        acoes = np.array([exp['acao'] for exp in batch])
        recompensas = np.array([exp['recompensa'] for exp in batch])
        
        # Treina modelo
        self.model.fit(
            estados, acoes,
            batch_size=self.config['batch_size'],
            epochs=1,
            verbose=0
        )
        
        # Atualiza experiência
        self.experiencia.adicionar_resultado(
            estados=estados,
            acoes=acoes,
            recompensas=recompensas
        )

class ExperienciaManager:
    """Gerenciador de Experiências da IA"""
    def __init__(self):
        self.experiencias = {
            'sucesso': [],
            'falha': [],
            'neutro': []
        }
        self.metricas = {
            'acertos': 0,
            'erros': 0,
            'retorno_total': 0.0
        }

    def adicionar_resultado(self, estados, acoes, recompensas):
        """Adiciona resultados à base de experiências"""
        for estado, acao, recompensa in zip(estados, acoes, recompensas):
            resultado = {
                'estado': estado,
                'acao': acao,
                'recompensa': recompensa,
                'timestamp': pd.Timestamp.now()
            }
            
            # Classifica experiência
            if recompensa > 0:
                self.experiencias['sucesso'].append(resultado)
                self.metricas['acertos'] += 1
            elif recompensa < 0:
                self.experiencias['falha'].append(resultado)
                self.metricas['erros'] += 1
            else:
                self.experiencias['neutro'].append(resultado)
                
            self.metricas['retorno_total'] += recompensa

    def analisar_performance(self):
        """Analisa performance das decisões"""
        total_operacoes = self.metricas['acertos'] + self.metricas['erros']
        if total_operacoes == 0:
            return None
            
        return {
            'taxa_acerto': self.metricas['acertos'] / total_operacoes,
            'retorno_medio': self.metricas['retorno_total'] / total_operacoes,
            'total_operacoes': total_operacoes,
            'experiencias_positivas': len(self.experiencias['sucesso']),
            'experiencias_negativas': len(self.experiencias['falha'])
        }

    def otimizar_estrategia(self):
        """Otimiza estratégia baseado em experiências"""
        performance = self.analisar_performance()
        if not performance:
            return None
            
        # Analisa padrões de sucesso
        padroes_sucesso = self.identificar_padroes(
            self.experiencias['sucesso']
        )
        
        # Analisa padrões de falha
        padroes_falha = self.identificar_padroes(
            self.experiencias['falha']
        )
        
        return {
            'padroes_sucesso': padroes_sucesso,
            'padroes_falha': padroes_falha,
            'recomendacoes': self.gerar_recomendacoes(
                padroes_sucesso, 
                padroes_falha
            )
        }

def main():
    # Inicializa gerenciador
    gerenciador = AutonomoGerenciador()
    
    # Exemplo de uso
    while True:
        # Obtém estado atual do mercado
        estado = obter_estado_mercado()
        
        # Prediz ação
        acao = gerenciador.model.predict(estado)
        
        # Executa ação
        recompensa = executar_acao(acao)
        
        # Aprende com experiência
        gerenciador.aprender_experiencia(
            estado=estado,
            acao=acao,
            recompensa=recompensa,
            proximo_estado=obter_estado_mercado()
        )
        
        # Analisa e otimiza periodicamente
        if necessita_otimizacao():
            performance = gerenciador.experiencia.analisar_performance()
            otimizacoes = gerenciador.experiencia.otimizar_estrategia()
            
            aplicar_otimizacoes(otimizacoes)

if __name__ == "__main__":
    main() 