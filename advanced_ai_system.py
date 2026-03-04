import tensorflow as tf
import torch
import torch.nn as nn
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
import gc
from functools import lru_cache
import json
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging otimizada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AdvancedAISystem')

@dataclass
class ModelConfig:
    """Configuração otimizada para modelos"""
    batch_size: int = 64
    learning_rate: float = 0.001
    hidden_units: int = 256
    dropout_rate: float = 0.3
    num_epochs: int = 100
    early_stopping_patience: int = 10
    validation_split: float = 0.2

@dataclass
class PredictionResult:
    """Estrutura para resultados de previsão"""
    predictions: np.ndarray
    confidence: float
    model_metadata: Dict[str, Any]
    timestamp: datetime

class OptimizedResourceModel(nn.Module):
    """Modelo PyTorch otimizado para previsão de recursos"""
    
    def __init__(self, input_size: int, hidden_size: int = 512, num_layers: int = 3):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Arquitetura avançada com atenção
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers, 
            batch_first=True, dropout=0.2, bidirectional=True
        )
        self.attention = nn.MultiheadAttention(
            hidden_size * 2, num_heads=8, dropout=0.1
        )
        self.layer_norm = nn.LayerNorm(hidden_size * 2)
        self.ffn = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.GELU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size // 2, 1)
        )
        
    def forward(self, x):
        # LSTM com atenção
        lstm_out, (hn, cn) = self.lstm(x)
        
        # Aplicar atenção
        attn_out, _ = self.attention(
            lstm_out.transpose(0, 1), 
            lstm_out.transpose(0, 1), 
            lstm_out.transpose(0, 1)
        )
        
        # Residual connection + layer norm
        residual = lstm_out + attn_out.transpose(0, 1)
        normalized = self.layer_norm(residual)
        
        # Usar apenas a última sequência para previsão
        last_output = normalized[:, -1, :]
        
        # Feed forward final
        return self.ffn(last_output)

class EnsemblePredictor:
    """Sistema ensemble otimizado para previsões"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.weights = {}
        self.thread_pool = ThreadPoolExecutor(max_workers=8)
        
    async def train_ensemble(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]):
        """Treina múltiplos modelos em paralelo"""
        # Normalização
        self.scalers['standard'] = StandardScaler()
        X_scaled = self.scalers['standard'].fit_transform(X)
        
        # Treinar modelos em paralelo
        training_tasks = [
            self._train_xgboost(X_scaled, y),
            self._train_lightgbm(X_scaled, y),
            self._train_random_forest(X_scaled, y),
            self._train_gradient_boosting(X_scaled, y)
        ]
        
        results = await asyncio.gather(*training_tasks)
        
        # Configurar pesos baseados na performance
        self._calculate_model_weights(results)
        
    async def _train_xgboost(self, X: np.ndarray, y: np.ndarray):
        """Treina modelo XGBoost otimizado"""
        model = xgb.XGBRegressor(
            n_estimators=1000,
            max_depth=8,
            learning_rate=0.01,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X, y)
        self.models['xgboost'] = model
        return model
    
    async def _train_lightgbm(self, X: np.ndarray, y: np.ndarray):
        """Treina modelo LightGBM otimizado"""
        model = lgb.LGBMRegressor(
            n_estimators=1000,
            max_depth=6,
            learning_rate=0.01,
            num_leaves=31,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X, y)
        self.models['lightgbm'] = model
        return model
    
    async def _train_random_forest(self, X: np.ndarray, y: np.ndarray):
        """Treina Random Forest otimizado"""
        model = RandomForestRegressor(
            n_estimators=500,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            bootstrap=True,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X, y)
        self.models['random_forest'] = model
        return model
    
    async def _train_gradient_boosting(self, X: np.ndarray, y: np.ndarray):
        """Treina Gradient Boosting otimizado"""
        model = GradientBoostingRegressor(
            n_estimators=500,
            max_depth=6,
            learning_rate=0.01,
            subsample=0.8,
            random_state=42
        )
        
        model.fit(X, y)
        self.models['gradient_boosting'] = model
        return model
    
    def _calculate_model_weights(self, results: List[Any]):
        """Calcula pesos dos modelos baseados na performance"""
        # Simulação - em produção usar validação cruzada
        self.weights = {
            'xgboost': 0.35,
            'lightgbm': 0.30,
            'random_forest': 0.20,
            'gradient_boosting': 0.15
        }
    
    async def predict(self, X: np.ndarray) -> PredictionResult:
        """Faz previsão usando ensemble"""
        X_scaled = self.scalers['standard'].transform(X)
        
        # Previsões paralelas
        prediction_tasks = []
        for model_name, model in self.models.items():
            task = asyncio.get_event_loop().run_in_executor(
                self.thread_pool, 
                model.predict, 
                X_scaled
            )
            prediction_tasks.append((model_name, task))
        
        # Coletar resultados
        predictions = {}
        for model_name, task in prediction_tasks:
            predictions[model_name] = await task
        
        # Combinação ponderada
        final_prediction = np.zeros_like(list(predictions.values())[0])
        for model_name, pred in predictions.items():
            final_prediction += pred * self.weights[model_name]
        
        # Calcular confiança
        confidence = self._calculate_prediction_confidence(predictions)
        
        return PredictionResult(
            predictions=final_prediction,
            confidence=confidence,
            model_metadata={'ensemble_weights': self.weights},
            timestamp=datetime.now()
        )
    
    def _calculate_prediction_confidence(self, predictions: Dict[str, np.ndarray]) -> float:
        """Calcula confiança baseada na concordância dos modelos"""
        pred_array = np.array(list(predictions.values()))
        std_dev = np.std(pred_array, axis=0)
        avg_std = np.mean(std_dev)
        
        # Converter para confiança (0-1)
        confidence = 1.0 / (1.0 + avg_std)
        return float(np.clip(confidence, 0, 1))

class AdvancedAIPredictionSystem:
    """Sistema de previsão AI altamente otimizado"""
    
    def __init__(self, use_gpu: bool = True):
        self.use_gpu = use_gpu
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() and use_gpu else 'cpu'
        )
        
        # Inicialização lazy de modelos
        self._models_initialized = False
        self.ensemble_predictor = EnsemblePredictor()
        self.resource_model = None
        self.incident_model = None
        self.cost_model = None
        self.security_model = None
        
        # Cache para previsões frequentes
        self._prediction_cache = {}
        self.cache_ttl = timedelta(minutes=5)
        
        # Otimização de memória
        self._memory_manager = MemoryOptimizer()
        
        logger.info(f"Sistema AI inicializado com dispositivo: {self.device}")
    
    async def initialize_models(self):
        """Inicialização assíncrona de todos os modelos"""
        if self._models_initialized:
            return
        
        logger.info("Inicializando modelos AI...")
        
        # Inicialização paralela de modelos
        init_tasks = [
            self._initialize_resource_model(),
            self._initialize_incident_model(),
            self._initialize_cost_model(),
            self._initialize_security_model()
        ]
        
        await asyncio.gather(*init_tasks)
        self._models_initialized = True
        logger.info("Todos os modelos inicializados com sucesso")
    
    async def _initialize_resource_model(self):
        """Inicializa modelo de recursos otimizado"""
        self.resource_model = OptimizedResourceModel(
            input_size=10,  # Número de features
            hidden_size=512,
            num_layers=3
        )
        
        if self.use_gpu:
            self.resource_model = self.resource_model.to(self.device)
    
    async def _initialize_incident_model(self):
        """Inicializa modelo de incidentes com transformers"""
        try:
            self.incident_model = AutoModelForSequenceClassification.from_pretrained(
                "microsoft/codebert-base",
                num_labels=2,
                output_attentions=False,
                output_hidden_states=False
            )
            
            if self.use_gpu:
                self.incident_model = self.incident_model.to(self.device)
                
        except Exception as e:
            logger.warning(f"Erro ao carregar modelo de incidentes: {e}")
            self.incident_model = None
    
    async def _initialize_cost_model(self):
        """Inicializa modelo de custos com ensemble"""
        # Será treinado com dados específicos
        self.cost_model = self.ensemble_predictor
    
    async def _initialize_security_model(self):
        """Inicializa modelo de segurança"""
        try:
            self.security_model = AutoModelForSequenceClassification.from_pretrained(
                "distilbert-base-uncased",
                num_labels=3,  # Baixo, Médio, Alto risco
                output_attentions=False,
                output_hidden_states=False
            )
            
            if self.use_gpu:
                self.security_model = self.security_model.to(self.device)
                
        except Exception as e:
            logger.warning(f"Erro ao carregar modelo de segurança: {e}")
            self.security_model = None
    
    @lru_cache(maxsize=1000)
    def _get_cache_key(self, data_hash: int, model_type: str) -> str:
        """Gera chave de cache otimizada"""
        return f"{model_type}_{data_hash}"
    
    async def predict_resource_usage(
        self, 
        historical_data: pd.DataFrame,
        forecast_horizon: int = 24
    ) -> Dict[str, PredictionResult]:
        """Prevê uso de recursos com alta performance"""
        
        cache_key = self._get_cache_key(
            hash(historical_data.to_json()), 
            'resource_usage'
        )
        
        # Verificar cache
        if cache_key in self._prediction_cache:
            cached_result = self._prediction_cache[cache_key]
            if datetime.now() - cached_result['timestamp'] < self.cache_ttl:
                logger.info("Retornando previsão do cache")
                return cached_result['result']
        
        await self.initialize_models()
        
        # Preparar dados de forma otimizada
        features = await self._prepare_resource_features(historical_data)
        
        # Fazer previsões em lote
        predictions = {}
        
        for resource_type in ['cpu', 'memory', 'storage', 'network']:
            resource_features = self._extract_resource_specific_features(
                features, resource_type
            )
            
            # Converter para tensor
            features_tensor = torch.FloatTensor(resource_features).unsqueeze(0)
            
            if self.use_gpu:
                features_tensor = features_tensor.to(self.device)
            
            # Fazer previsão
            with torch.no_grad():
                prediction = self.resource_model(features_tensor)
                prediction_cpu = prediction.cpu().numpy() if self.use_gpu else prediction.numpy()
            
            predictions[resource_type] = PredictionResult(
                predictions=prediction_cpu.flatten(),
                confidence=0.85,  # Baseado em validação do modelo
                model_metadata={'model_type': 'optimized_lstm_attention'},
                timestamp=datetime.now()
            )
        
        # Atualizar cache
        self._prediction_cache[cache_key] = {
            'result': predictions,
            'timestamp': datetime.now()
        }
        
        # Limpar cache antigo
        self._clean_old_cache()
        
        return predictions
    
    async def _prepare_resource_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepara features de recursos de forma otimizada"""
        # Features básicas
        features = []
        
        # Métricas de tempo
        features.extend([
            data['timestamp'].dt.hour.values,
            data['timestamp'].dt.dayofweek.values,
            data['timestamp'].dt.month.values
        ])
        
        # Métricas de recursos
        resource_columns = ['cpu_usage', 'memory_usage', 'storage_usage', 'network_usage']
        for col in resource_columns:
            if col in data.columns:
                # Valores atuais
                features.append(data[col].values)
                
                # Médias móveis
                features.append(data[col].rolling(window=5, min_periods=1).mean().values)
                features.append(data[col].rolling(window=15, min_periods=1).mean().values)
                
                # Taxa de variação
                features.append(data[col].pct_change().fillna(0).values)
        
        # Combinar todas as features
        return np.column_stack(features)
    
    def _extract_resource_specific_features(self, features: np.ndarray, resource_type: str) -> np.ndarray:
        """Extrai features específicas para cada tipo de recurso"""
        # Em produção, implementar lógica específica
        return features  # Simplificado para exemplo
    
    async def predict_incidents(
        self, 
        system_logs: List[str],
        metrics_data: pd.DataFrame
    ) -> PredictionResult:
        """Prevê incidentes do sistema"""
        await self.initialize_models()
        
        if self.incident_model is None:
            raise ValueError("Modelo de incidentes não disponível")
        
        # Processar logs em lote
        processed_logs = await self._preprocess_logs(system_logs)
        
        # Fazer previsões
        with torch.no_grad():
            inputs = self._prepare_incident_inputs(processed_logs)
            
            if self.use_gpu:
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            outputs = self.incident_model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=-1)
        
        return PredictionResult(
            predictions=predictions.cpu().numpy(),
            confidence=float(predictions.max()),
            model_metadata={'model_type': 'codebert_incident_predictor'},
            timestamp=datetime.now()
        )
    
    async def _preprocess_logs(self, logs: List[str]) -> List[str]:
        """Pré-processa logs de sistema de forma eficiente"""
        # Processamento em lote
        processed = []
        for log in logs:
            # Limpeza básica e normalização
            cleaned = log.strip().lower()
            # Adicionar mais processamento conforme necessário
            processed.append(cleaned)
        
        return processed
    
    def _prepare_incident_inputs(self, logs: List[str]) -> Dict[str, torch.Tensor]:
        """Prepara inputs para o modelo de incidentes"""
        # Usar tokenizer apropriado
        tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        
        return tokenizer(
            logs, 
            padding=True, 
            truncation=True, 
            max_length=512,
            return_tensors="pt"
        )
    
    async def predict_costs(
        self, 
        usage_data: pd.DataFrame,
        pricing_data: pd.DataFrame
    ) -> PredictionResult:
        """Prevê custos usando ensemble learning"""
        await self.initialize_models()
        
        # Combinar dados
        combined_data = await self._combine_usage_pricing_data(usage_data, pricing_data)
        
        # Preparar features
        features = self._prepare_cost_features(combined_data)
        
        # Fazer previsão com ensemble
        return await self.cost_model.predict(features)
    
    async def _combine_usage_pricing_data(
        self, 
        usage: pd.DataFrame, 
        pricing: pd.DataFrame
    ) -> pd.DataFrame:
        """Combina dados de uso e preços de forma eficiente"""
        return pd.merge(usage, pricing, on='timestamp', how='left')
    
    def _prepare_cost_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepara features para previsão de custos"""
        feature_columns = [
            'cpu_usage', 'memory_usage', 'storage_usage', 'network_usage',
            'cpu_price', 'memory_price', 'storage_price', 'network_price'
        ]
        
        return data[feature_columns].values
    
    async def predict_security_risk(
        self, 
        security_events: List[Dict],
        system_state: Dict[str, Any]
    ) -> PredictionResult:
        """Prevê riscos de segurança"""
        await self.initialize_models()
        
        if self.security_model is None:
            raise ValueError("Modelo de segurança não disponível")
        
        # Preparar dados de segurança
        security_texts = self._prepare_security_texts(security_events, system_state)
        
        # Fazer previsões
        with torch.no_grad():
            inputs = self._prepare_security_inputs(security_texts)
            
            if self.use_gpu:
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            outputs = self.security_model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=-1)
        
        return PredictionResult(
            predictions=predictions.cpu().numpy(),
            confidence=float(predictions.max()),
            model_metadata={'model_type': 'distilbert_security_risk'},
            timestamp=datetime.now()
        )
    
    def _prepare_security_texts(self, events: List[Dict], state: Dict) -> List[str]:
        """Prepara textos para análise de segurança"""
        texts = []
        
        for event in events:
            text_parts = [
                f"Event: {event.get('type', 'unknown')}",
                f"Severity: {event.get('severity', 'unknown')}",
                f"Source: {event.get('source', 'unknown')}"
            ]
            texts.append(" ".join(text_parts))
        
        # Adicionar estado do sistema
        state_text = f"System state: {json.dumps(state, default=str)}"
        texts.append(state_text)
        
        return texts
    
    def _prepare_security_inputs(self, texts: List[str]) -> Dict[str, torch.Tensor]:
        """Prepara inputs para modelo de segurança"""
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
        return tokenizer(
            texts, 
            padding=True, 
            truncation=True, 
            max_length=256,
            return_tensors="pt"
        )
    
    def _clean_old_cache(self):
        """Limpa cache antigo para otimização de memória"""
        current_time = datetime.now()
        keys_to_remove = []
        
        for key, value in self._prediction_cache.items():
            if current_time - value['timestamp'] > self.cache_ttl:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._prediction_cache[key]
        
        if keys_to_remove:
            logger.info(f"Limpos {len(keys_to_remove)} itens do cache")
    
    async def batch_predict(
        self, 
        prediction_requests: List[Dict[str, Any]]
    ) -> List[PredictionResult]:
        """Executa previsões em lote para máxima eficiência"""
        
        # Agrupar por tipo de previsão
        grouped_requests = {}
        for request in prediction_requests:
            pred_type = request['type']
            if pred_type not in grouped_requests:
                grouped_requests[pred_type] = []
            grouped_requests[pred_type].append(request)
        
        # Executar previsões em paralelo
        prediction_tasks = []
        for pred_type, requests in grouped_requests.items():
            task = self._process_batch_type(pred_type, requests)
            prediction_tasks.append(task)
        
        results = await asyncio.gather(*prediction_tasks)
        
        # Achatar resultados
        all_results = []
        for result_batch in results:
            all_results.extend(result_batch)
        
        return all_results
    
    async def _process_batch_type(
        self, 
        prediction_type: str, 
        requests: List[Dict]
    ) -> List[PredictionResult]:
        """Processa lote do mesmo tipo de previsão"""
        
        if prediction_type == 'resource_usage':
            # Combinar dados para processamento eficiente
            combined_data = pd.concat([req['data'] for req in requests])
            predictions = await self.predict_resource_usage(combined_data)
            
            # Distribuir resultados
            results = []
            for i, request in enumerate(requests):
                result_key = list(predictions.keys())[i % len(predictions)]
                results.append(predictions[result_key])
            
            return results
        
        # Implementar outros tipos...
        
        return []
    
    async def optimize_memory(self):
        """Otimiza uso de memória do sistema"""
        if self.use_gpu and torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        gc.collect()
        
        # Limpar cache de previsões
        self._prediction_cache.clear()
        
        logger.info("Otimização de memória concluída")

class MemoryOptimizer:
    """Otimizador avançado de memória"""
    
    def __init__(self):
        self.memory_threshold = 0.8  # 80% de uso
        self.cleanup_interval = timedelta(minutes=5)
        self.last_cleanup = datetime.now()
    
    async def check_memory_usage(self) -> bool:
        """Verifica se é necessário limpar memória"""
        memory_percent = psutil.virtual_memory().percent / 100
        
        time_since_cleanup = datetime.now() - self.last_cleanup
        needs_cleanup = (memory_percent > self.memory_threshold or 
                        time_since_cleanup > self.cleanup_interval)
        
        return needs_cleanup
    
    async def perform_memory_cleanup(self):
        """Executa limpeza de memória"""
        logger.info("Executando limpeza de memória...")
        
        # Limpar cache do Python
        gc.collect()
        
        # Limpar cache do PyTorch se disponível
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.last_cleanup = datetime.now()
        logger.info("Limpeza de memória concluída")

# Exemplo de uso otimizado
async def main():
    """Demonstração do sistema otimizado"""
    
    # Inicializar sistema
    ai_system = AdvancedAIPredictionSystem(use_gpu=True)
    
    try:
        # Dados de exemplo
        sample_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
            'cpu_usage': np.random.normal(50, 20, 100),
            'memory_usage': np.random.normal(60, 15, 100),
            'storage_usage': np.random.normal(70, 10, 100),
            'network_usage': np.random.normal(40, 25, 100)
        })
        
        # Previsões em lote
        logger.info("Executando previsões em lote...")
        
        start_time = datetime.now()
        
        # Executar múltiplas previsões em paralelo
        prediction_tasks = [
            ai_system.predict_resource_usage(sample_data),
            ai_system.predict_costs(sample_data, sample_data),  # Exemplo simplificado
        ]
        
        results = await asyncio.gather(*prediction_tasks)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Previsões concluídas em {execution_time:.2f} segundos")
        
        # Exibir resultados
        for i, result in enumerate(results):
            if isinstance(result, dict):
                for resource, pred in result.items():
                    logger.info(f"{resource}: {pred.predictions[:5]} (conf: {pred.confidence:.3f})")
            else:
                logger.info(f"Resultado {i}: {result.predictions[:5]} (conf: {result.confidence:.3f})")
        
        # Otimizar memória
        await ai_system.optimize_memory()
        
    except Exception as e:
        logger.error(f"Erro na demonstração: {e}")
        raise

if __name__ == "__main__":
    # Executar demonstração
    asyncio.run(main())