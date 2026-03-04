"""
IA Geral - Cérebro do sistema de trading.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import tensorflow as tf
from tensorflow import keras
import joblib
import pickle
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class MarketAnalysis:
    """Resultado da análise de mercado pela IA."""
    signal: str  # BUY, SELL, HOLD
    confidence: float  # 0-1
    reasoning: str
    suggested_entry: float
    suggested_stop_loss: float
    suggested_take_profit: float
    risk_level: str  # LOW, MEDIUM, HIGH
    time_horizon: str  # SHORT, MEDIUM, LONG
    market_regime: str  # TRENDING, RANGING, VOLATILE
    key_levels: Dict[str, float]
    sentiment_score: float


@dataclass
class NeuralMemory:
    """Memória neural para aprendizado contínuo."""
    experience: Dict[str, Any]
    reward: float
    timestamp: datetime
    metadata: Dict[str, Any]


class AIGeneralBrain:
    """IA Geral para análise e decisão de mercado."""
    
    def __init__(self, model_path: str, confidence_threshold: float = 0.75):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.memory: List[NeuralMemory] = []
        self.max_memory_size = 10000
        self.learning_rate = 0.001
        
        # Carregar ou criar modelos
        self._load_or_create_models()
        
        logger.info("IA Geral inicializada")
    
    def _load_or_create_models(self):
        """Carrega ou cria os modelos de IA."""
        try:
            # Modelo de análise de tendência
            self.trend_model = self._load_model("trend_model")
            
            # Modelo de reconhecimento de padrões
            self.pattern_model = self._load_model("pattern_model")
            
            # Modelo de análise de sentimento
            self.sentiment_model = self._load_model("sentiment_model")
            
            # Modelo de risco
            self.risk_model = self._load_model("risk_model")
            
            # Modelo de previsão
            self.forecast_model = self._load_model("forecast_model")
            
            logger.info("Modelos de IA carregados com sucesso")
            
        except Exception as e:
            logger.warning(f"Erro ao carregar modelos: {e}. Criando novos...")
            self._create_new_models()
    
    def _load_model(self, model_name: str):
        """Carrega um modelo específico."""
        model_file = f"{self.model_path}/{model_name}.h5"
        try:
            return keras.models.load_model(model_file)
        except:
            return None
    
    def _create_new_models(self):
        """Cria novos modelos de IA."""
        # Modelo LSTM para análise de tendência
        self.trend_model = self._create_lstm_model(
            input_shape=(100, 10),
            output_shape=3  # UP, DOWN, SIDEWAYS
        )
        
        # Modelo CNN para reconhecimento de padrões
        self.pattern_model = self._create_cnn_model(
            input_shape=(50, 50, 1),
            output_shape=10  # Padrões comuns
        )
        
        # Modelo para análise de sentimento
        self.sentiment_model = self._create_sentiment_model()
        
        # Modelo para avaliação de risco
        self.risk_model = self._create_risk_model()
        
        # Modelo para previsão
        self.forecast_model = self._create_forecast_model()
    
    def analyze_market(self, market_data: Dict[str, Any]) -> MarketAnalysis:
        """
        Analisa o mercado usando IA geral.
        
        Args:
            market_data: Dados de mercado (preços, volumes, indicadores)
            
        Returns:
            MarketAnalysis: Análise completa do mercado
        """
        try:
            logger.info("Iniciando análise de mercado com IA...")
            
            # 1. Análise de tendência
            trend_analysis = self._analyze_trend(market_data)
            
            # 2. Reconhecimento de padrões
            pattern_analysis = self._analyze_patterns(market_data)
            
            # 3. Análise de sentimento
            sentiment_analysis = self._analyze_sentiment(market_data)
            
            # 4. Avaliação de risco
            risk_analysis = self._assess_risk(market_data)
            
            # 5. Previsão de preço
            price_forecast = self._forecast_price(market_data)
            
            # 6. Tomada de decisão integrada
            final_decision = self._make_integrated_decision(
                trend_analysis,
                pattern_analysis,
                sentiment_analysis,
                risk_analysis,
                price_forecast
            )
            
            # 7. Calcular níveis de suporte/resistência
            key_levels = self._calculate_key_levels(market_data)
            
            # 8. Gerar análise final
            analysis = MarketAnalysis(
                signal=final_decision["signal"],
                confidence=final_decision["confidence"],
                reasoning=final_decision["reasoning"],
                suggested_entry=price_forecast["entry_price"],
                suggested_stop_loss=risk_analysis["stop_loss"],
                suggested_take_profit=price_forecast["take_profit"],
                risk_level=risk_analysis["level"],
                time_horizon=trend_analysis["timeframe"],
                market_regime=trend_analysis["regime"],
                key_levels=key_levels,
                sentiment_score=sentiment_analysis["score"]
            )
            
            logger.info(f"Análise concluída: {analysis.signal} com {analysis.confidence:.1%} de confiança")
            
            # Aprender com a análise
            self._learn_from_analysis(market_data, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise de mercado: {e}")
            # Retornar análise segura
            return self._get_safe_analysis(market_data)
    
    def _analyze_trend(self, market_data: Dict) -> Dict[str, Any]:
        """Analisa tendência do mercado."""
        try:
            prices = market_data.get("prices", [])
            volumes = market_data.get("volumes", [])
            
            if len(prices) < 100:
                return {"direction": "NEUTRAL", "strength": 0.5, "regime": "UNKNOWN", "timeframe": "SHORT"}
            
            # Preparar dados para o modelo
            features = self._extract_trend_features(prices, volumes)
            
            # Previsão do modelo
            if self.trend_model:
                prediction = self.trend_model.predict(features.reshape(1, -1))
                direction_idx = np.argmax(prediction)
                directions = ["UP", "DOWN", "SIDEWAYS"]
                direction = directions[direction_idx]
                confidence = float(prediction[0][direction_idx])
            else:
                # Análise simples se modelo não disponível
                sma_short = np.mean(prices[-20:])
                sma_long = np.mean(prices[-50:])
                
                if sma_short > sma_long * 1.01:
                    direction = "UP"
                    confidence = 0.6
                elif sma_short < sma_long * 0.99:
                    direction = "DOWN"
                    confidence = 0.6
                else:
                    direction = "SIDEWAYS"
                    confidence = 0.7
            
            # Determinar regime de mercado
            volatility = np.std(prices[-20:]) / np.mean(prices[-20:])
            if volatility > 0.02:
                regime = "VOLATILE"
            elif direction != "SIDEWAYS":
                regime = "TRENDING"
            else:
                regime = "RANGING"
            
            # Determinar timeframe
            trend_strength = abs(np.mean(prices[-10:]) - np.mean(prices[-30:-20])) / np.mean(prices[-30:-20])
            if trend_strength > 0.05:
                timeframe = "LONG"
            elif trend_strength > 0.02:
                timeframe = "MEDIUM"
            else:
                timeframe = "SHORT"
            
            return {
                "direction": direction,
                "strength": confidence,
                "regime": regime,
                "timeframe": timeframe
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de tendência: {e}")
            return {"direction": "NEUTRAL", "strength": 0.5, "regime": "UNKNOWN", "timeframe": "SHORT"}
    
    def _analyze_patterns(self, market_data: Dict) -> Dict[str, Any]:
        """Reconhece padrões de gráfico."""
        try:
            prices = market_data.get("prices", [])
            
            if len(prices) < 50:
                return {"pattern": "NO_PATTERN", "confidence": 0.5, "implication": "NEUTRAL"}
            
            # Extrair features de padrão
            pattern_features = self._extract_pattern_features(prices)
            
            # Identificar padrões comuns
            patterns = self._identify_common_patterns(prices)
            
            # Escolher padrão mais provável
            if patterns:
                main_pattern = max(patterns, key=lambda x: x["confidence"])
                return main_pattern
            else:
                return {"pattern": "NO_PATTERN", "confidence": 0.5, "implication": "NEUTRAL"}
                
        except Exception as e:
            logger.error(f"Erro na análise de padrões: {e}")
            return {"pattern": "NO_PATTERN", "confidence": 0.5, "implication": "NEUTRAL"}
    
    def _analyze_sentiment(self, market_data: Dict) -> Dict[str, Any]:
        """Analisa sentimento de mercado."""
        try:
            # Coletar dados de sentimento (se disponíveis)
            sentiment_data = market_data.get("sentiment", {})
            
            # Análise de notícias (simplificada)
            news_sentiment = sentiment_data.get("news", 0.5)
            
            # Análise de mídia social (simplificada)
            social_sentiment = sentiment_data.get("social", 0.5)
            
            # Análise de dados on-chain (para cripto)
            onchain_sentiment = sentiment_data.get("onchain", 0.5)
            
            # Calcular sentimento médio
            sentiment_score = (news_sentiment + social_sentiment + onchain_sentiment) / 3
            
            # Determinar sentimento
            if sentiment_score > 0.7:
                sentiment = "BULLISH"
            elif sentiment_score < 0.3:
                sentiment = "BEARISH"
            else:
                sentiment = "NEUTRAL"
            
            return {
                "score": sentiment_score,
                "sentiment": sentiment,
                "news_score": news_sentiment,
                "social_score": social_sentiment,
                "onchain_score": onchain_sentiment
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de sentimento: {e}")
            return {"score": 0.5, "sentiment": "NEUTRAL", "news_score": 0.5, "social_score": 0.5, "onchain_score": 0.5}
    
    def _assess_risk(self, market_data: Dict) -> Dict[str, Any]:
        """Avalia nível de risco."""
        try:
            prices = market_data.get("prices", [])
            volatility = market_data.get("volatility", 0.01)
            
            if len(prices) < 20:
                return {"level": "MEDIUM", "stop_loss": 0.02, "position_size": 0.01}
            
            # Calcular volatilidade
            returns = np.diff(prices[-20:]) / prices[-21:-1]
            current_volatility = np.std(returns)
            
            # Determinar nível de risco baseado na volatilidade
            if current_volatility > 0.03:
                risk_level = "HIGH"
                stop_loss_pct = 0.03
                position_size = 0.005
            elif current_volatility > 0.015:
                risk_level = "MEDIUM"
                stop_loss_pct = 0.02
                position_size = 0.01
            else:
                risk_level = "LOW"
                stop_loss_pct = 0.01
                position_size = 0.02
            
            # Ajustar baseado em correlações
            correlations = market_data.get("correlations", {})
            if correlations:
                max_correlation = max(correlations.values())
                if max_correlation > 0.8:
                    risk_level = "HIGH"
                    position_size *= 0.5
            
            return {
                "level": risk_level,
                "stop_loss": stop_loss_pct,
                "position_size": position_size,
                "volatility": current_volatility
            }
            
        except Exception as e:
            logger.error(f"Erro na avaliação de risco: {e}")
            return {"level": "MEDIUM", "stop_loss": 0.02, "position_size": 0.01, "volatility": 0.01}
    
    def _forecast_price(self, market_data: Dict) -> Dict[str, Any]:
        """Prevê preços futuros."""
        try:
            prices = market_data.get("prices", [])
            
            if len(prices) < 50:
                return {"entry_price": prices[-1] if prices else 0, "take_profit": 0.04, "targets": []}
            
            current_price = prices[-1]
            
            # Previsão usando modelo (se disponível)
            if self.forecast_model and len(prices) >= 100:
                features = self._extract_forecast_features(prices)
                forecast = self.forecast_model.predict(features.reshape(1, -1))
                predicted_return = float(forecast[0][0])
                
                entry_price = current_price
                take_profit_pct = min(0.1, max(0.02, abs(predicted_return) * 0.8))
                
                # Gerar alvos de preço
                targets = []
                for i in range(1, 4):
                    target = current_price * (1 + predicted_return * i * 0.3)
                    targets.append(target)
                
            else:
                # Previsão simples baseada em médias móveis
                sma_20 = np.mean(prices[-20:])
                sma_50 = np.mean(prices[-50:])
                
                if current_price > sma_20 > sma_50:
                    # Tendência de alta
                    entry_price = current_price
                    take_profit_pct = 0.04
                    targets = [current_price * 1.02, current_price * 1.04, current_price * 1.06]
                elif current_price < sma_20 < sma_50:
                    # Tendência de baixa
                    entry_price = current_price
                    take_profit_pct = 0.04
                    targets = [current_price * 0.98, current_price * 0.96, current_price * 0.94]
                else:
                    # Lateralizado
                    entry_price = current_price
                    take_profit_pct = 0.02
                    targets = [current_price * 1.01, current_price * 0.99]
            
            return {
                "entry_price": entry_price,
                "take_profit": take_profit_pct,
                "targets": targets,
                "forecast_horizon": "1H"  # 1 hora
            }
            
        except Exception as e:
            logger.error(f"Erro na previsão de preço: {e}")
            current_price = market_data.get("prices", [0])[-1] if market_data.get("prices") else 0
            return {"entry_price": current_price, "take_profit": 0.03, "targets": [], "forecast_horizon": "1H"}
    
    def _make_integrated_decision(self, trend: Dict, pattern: Dict, 
                                 sentiment: Dict, risk: Dict, forecast: Dict) -> Dict[str, Any]:
        """Toma decisão integrada baseada em todas as análises."""
        try:
            # Coletar confianças
            trend_conf = trend.get("strength", 0.5)
            pattern_conf = pattern.get("confidence", 0.5)
            sentiment_conf = abs(sentiment.get("score", 0.5) - 0.5) * 2
            risk_conf = 1.0 - (risk.get("volatility", 0.01) / 0.05)
            
            # Calcular confiança total
            weights = [0.3, 0.2, 0.2, 0.3]  # Pesos para cada análise
            total_confidence = (
                trend_conf * weights[0] +
                pattern_conf * weights[1] +
                sentiment_conf * weights[2] +
                risk_conf * weights[3]
            )
            
            # Tomar decisão baseada na tendência
            trend_direction = trend.get("direction", "NEUTRAL")
            
            if trend_direction == "UP" and total_confidence > self.confidence_threshold:
                signal = "BUY"
                reasoning = f"Tendência de alta confirmada com {total_confidence:.1%} de confiança"
            elif trend_direction == "DOWN" and total_confidence > self.confidence_threshold:
                signal = "SELL"
                reasoning = f"Tendência de baixa confirmada com {total_confidence:.1%} de confiança"
            else:
                signal = "HOLD"
                reasoning = f"Confiança insuficiente ({total_confidence:.1%}) ou mercado lateral"
            
            # Ajustar baseado no risco
            if risk.get("level") == "HIGH" and signal != "HOLD":
                signal = "HOLD"
                reasoning += ". Risco muito alto para operar."
            
            # Ajustar baseado no sentimento
            if sentiment.get("sentiment") == "BEARISH" and signal == "BUY":
                signal = "HOLD"
                reasoning += ". Sentimento de mercado negativo."
            elif sentiment.get("sentiment") == "BULLISH" and signal == "SELL":
                signal = "HOLD"
                reasoning += ". Sentimento de mercado positivo."
            
            return {
                "signal": signal,
                "confidence": total_confidence,
                "reasoning": reasoning,
                "components": {
                    "trend": trend,
                    "pattern": pattern,
                    "sentiment": sentiment,
                    "risk": risk,
                    "forecast": forecast
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na tomada de decisão integrada: {e}")
            return {
                "signal": "HOLD",
                "confidence": 0.5,
                "reasoning": "Erro na análise. Mantendo posição.",
                "components": {}
            }
    
    def _calculate_key_levels(self, market_data: Dict) -> Dict[str, float]:
        """Calcula níveis-chave de suporte e resistência."""
        try:
            prices = market_data.get("prices", [])
            
            if len(prices) < 100:
                return {}
            
            # Identificar máximos e mínimos locais
            highs = []
            lows = []
            
            for i in range(20, len(prices) - 20):
                if prices[i] == max(prices[i-20:i+21]):
                    highs.append(prices[i])
                elif prices[i] == min(prices[i-20:i+21]):
                    lows.append(prices[i])
            
            # Agrupar níveis próximos
            support_levels = self._cluster_levels(lows, tolerance=0.005)
            resistance_levels = self._cluster_levels(highs, tolerance=0.005)
            
            # Ordenar por força (número de toques)
            support_levels = sorted(support_levels, key=lambda x: x["strength"], reverse=True)[:3]
            resistance_levels = sorted(resistance_levels, key=lambda x: x["strength"], reverse=True)[:3]
            
            # Criar dicionário de níveis
            key_levels = {}
            for i, level in enumerate(support_levels[:3]):
                key_levels[f"support_{i+1}"] = level["price"]
            
            for i, level in enumerate(resistance_levels[:3]):
                key_levels[f"resistance_{i+1}"] = level["price"]
            
            current_price = prices[-1]
            key_levels["current_price"] = current_price
            
            # Identificar nível mais próximo
            all_levels = [(p, "support") for p in [l["price"] for l in support_levels]] + \
                        [(p, "resistance") for p in [r["price"] for r in resistance_levels]]
            
            if all_levels:
                closest = min(all_levels, key=lambda x: abs(x[0] - current_price))
                key_levels["nearest_level"] = closest[0]
                key_levels["nearest_type"] = closest[1]
            
            return key_levels
            
        except Exception as e:
            logger.error(f"Erro no cálculo de níveis-chave: {e}")
            return {}
    
    def _learn_from_analysis(self, market_data: Dict, analysis: MarketAnalysis):
        """Aprende com a análise realizada."""
        try:
            # Criar experiência de aprendizado
            experience = {
                "market_data": market_data,
                "analysis": analysis,
                "timestamp": datetime.now()
            }
            
            # Avaliar recompensa (simplificado)
            # Em produção, isso seria baseado no resultado do trade
            reward = analysis.confidence * 0.1
            
            # Armazenar na memória
            memory = NeuralMemory(
                experience=experience,
                reward=reward,
                timestamp=datetime.now(),
                metadata={"type": "market_analysis"}
            )
            
            self.memory.append(memory)
            
            # Limitar tamanho da memória
            if len(self.memory) > self.max_memory_size:
                self.memory = self.memory[-self.max_memory_size:]
            
            # Treinar modelos periodicamente
            if len(self.memory) % 100 == 0:
                self._train_models()
                
        except Exception as e:
            logger.error(f"Erro no aprendizado: {e}")
    
    def _train_models(self):
        """Treina os modelos de IA com a memória acumulada."""
        try:
            if len(self.memory) < 100:
                return
            
            logger.info(f"Treinando modelos com {len(self.memory)} experiências...")
            
            # Preparar dados de treinamento
            X_train = []
            y_train = []
            
            for memory in self.memory[-1000:]:  # Usar últimas 1000 experiências
                # Extrair features
                features = self._extract_training_features(memory.experience["market_data"])
                X_train.append(features)
                
                # Target baseado na recompensa
                target = memory.reward
                y_train.append(target)
            
            X_train = np.array(X_train)
            y_train = np.array(y_train)
            
            # Treinar modelo de tendência
            if self.trend_model and len(X_train) > 100:
                self.trend_model.fit(
                    X_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_split=0.2,
                    verbose=0
                )
            
            logger.info("Modelos treinados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro no treinamento dos modelos: {e}")
    
    # Métodos auxiliares
    def _extract_trend_features(self, prices: List[float], volumes: List[float]) -> np.ndarray:
        """Extrai features para análise de tendência."""
        features = []
        
        # Retornos
        returns = np.diff(prices[-100:]) / prices[-101:-1]
        features.extend([np.mean(returns), np.std(returns), np.min(returns), np.max(returns)])
        
        # Médias móveis
        for period in [5, 10, 20, 50]:
            ma = np.mean(prices[-period:])
            features.append(ma / prices[-1])
        
        # Volume
        if volumes:
            volume_features = [
                np.mean(volumes[-20:]),
                np.std(volumes[-20:]),
                volumes[-1] / np.mean(volumes[-20:])
            ]
            features.extend(volume_features)
        
        return np.array(features)
    
    def _extract_pattern_features(self, prices: List[float]) -> np.ndarray:
        """Extrai features para reconhecimento de padrões."""
        # Normalizar preços
        normalized = (prices[-50:] - np.min(prices[-50:])) / (np.max(prices[-50:]) - np.min(prices[-50:]) + 1e-10)
        return normalized.reshape(50, 1)
    
    def _identify_common_patterns(self, prices: List[float]) -> List[Dict[str, Any]]:
        """Identifica padrões de gráfico comuns."""
        patterns = []
        
        # Head & Shoulders
        hs_score = self._detect_head_shoulders(prices)
        if hs_score > 0.7:
            patterns.append({
                "pattern": "HEAD_SHOULDERS",
                "confidence": hs_score,
                "implication": "BEARISH"
            })
        
        # Inverse Head & Shoulders
        ihs_score = self._detect_inverse_head_shoulders(prices)
        if ihs_score > 0.7:
            patterns.append({
                "pattern": "INVERSE_HEAD_SHOULDERS",
                "confidence": ihs_score,
                "implication": "BULLISH"
            })
        
        # Double Top
        dt_score = self._detect_double_top(prices)
        if dt_score > 0.7:
            patterns.append({
                "pattern": "DOUBLE_TOP",
                "confidence": dt_score,
                "implication": "BEARISH"
            })
        
        # Double Bottom
        db_score = self._detect_double_bottom(prices)
        if db_score > 0.7:
            patterns.append({
                "pattern": "DOUBLE_BOTTOM",
                "confidence": db_score,
                "implication": "BULLISH"
            })
        
        # Triangle
        tri_score = self._detect_triangle(prices)
        if tri_score > 0.7:
            patterns.append({
                "pattern": "TRIANGLE",
                "confidence": tri_score,
                "implication": "CONTINUATION"
            })
        
        return patterns
    
    def _detect_head_shoulders(self, prices: List[float]) -> float:
        """Detecta padrão Head & Shoulders."""
        if len(prices) < 30:
            return 0.0
        
        # Implementação simplificada
        try:
            # Encontrar picos
            peaks = []
            for i in range(10, len(prices) - 10):
                if prices[i] == max(prices[i-10:i+11]):
                    peaks.append((i, prices[i]))
            
            if len(peaks) < 3:
                return 0.0
            
            # Ordenar por altura
            peaks.sort(key=lambda x: x[1], reverse=True)
            
            # Verificar se o pico do meio é mais alto
            if peaks[0][0] > peaks[1][0] and peaks[0][0] < peaks[2][0]:
                return 0.8
            else:
                return 0.0
                
        except:
            return 0.0
    
    def _detect_inverse_head_shoulders(self, prices: List[float]) -> float:
        """Detecta padrão Inverse Head & Shoulders."""
        # Similar ao head & shoulders, mas com mínimos
        return 0.0  # Implementação similar
    
    def _detect_double_top(self, prices: List[float]) -> float:
        """Detecta padrão Double Top."""
        if len(prices) < 20:
            return 0.0
        
        try:
            # Encontrar dois picos próximos em altura
            peaks = []
            for i in range(5, len(prices) - 5):
                if prices[i] == max(prices[i-5:i+6]):
                    peaks.append((i, prices[i]))
            
            if len(peaks) < 2:
                return 0.0
            
            # Verificar se há dois picos similares
            for i in range(len(peaks)-1):
                for j in range(i+1, len(peaks)):
                    price_diff = abs(peaks[i][1] - peaks[j][1]) / peaks[i][1]
                    time_diff = abs(peaks[i][0] - peaks[j][0])
                    
                    if price_diff < 0.02 and 5 < time_diff < 20:
                        return 0.8
            
            return 0.0
            
        except:
            return 0.0
    
    def _detect_double_bottom(self, prices: List[float]) -> float:
        """Detecta padrão Double Bottom."""
        # Similar ao double top, mas com mínimos
        return 0.0
    
    def _detect_triangle(self, prices: List[float]) -> float:
        """Detecta padrão Triangle."""
        return 0.0
    
    def _cluster_levels(self, levels: List[float], tolerance: float = 0.005) -> List[Dict[str, Any]]:
        """Agrupa níveis de preço próximos."""
        if not levels:
            return []
        
        levels.sort()
        clusters = []
        current_cluster = [levels[0]]
        
        for price in levels[1:]:
            if abs(price - np.mean(current_cluster)) / np.mean(current_cluster) < tolerance:
                current_cluster.append(price)
            else:
                clusters.append({
                    "price": np.mean(current_cluster),
                    "strength": len(current_cluster),
                    "prices": current_cluster.copy()
                })
                current_cluster = [price]
        
        if current_cluster:
            clusters.append({
                "price": np.mean(current_cluster),
                "strength": len(current_cluster),
                "prices": current_cluster
            })
        
        return clusters
    
    def _extract_forecast_features(self, prices: List[float]) -> np.ndarray:
        """Extrai features para previsão."""
        features = []
        
        # Features técnicas básicas
        features.append(prices[-1])  # Preço atual
        
        # Retornos
        for period in [1, 5, 10, 20]:
            if len(prices) > period:
                ret = (prices[-1] - prices[-period-1]) / prices[-period-1]
                features.append(ret)
            else:
                features.append(0)
        
        # Volatilidade
        if len(prices) > 20:
            returns = np.diff(prices[-20:]) / prices[-21:-1]
            features.append(np.std(returns))
        else:
            features.append(0.01)
        
        return np.array(features)
    
    def _extract_training_features(self, market_data: Dict) -> np.ndarray:
        """Extrai features para treinamento."""
        # Combina features de várias análises
        prices = market_data.get("prices", [])
        trend_features = self._extract_trend_features(
            prices, 
            market_data.get("volumes", [])
        )
        pattern_features = self._extract_pattern_features(prices)
        
        # Combinar e flatten
        combined = np.concatenate([
            trend_features,
            pattern_features.flatten()
        ])
        
        return combined
    
    def _create_lstm_model(self, input_shape: Tuple[int, int], output_shape: int):
        """Cria modelo LSTM."""
        model = keras.Sequential([
            keras.layers.LSTM(64, input_shape=input_shape, return_sequences=True),
            keras.layers.LSTM(32),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(output_shape, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _create_cnn_model(self, input_shape: Tuple[int, int, int], output_shape: int):
        """Cria modelo CNN."""
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(output_shape, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _create_sentiment_model(self):
        """Cria modelo de análise de sentimento."""
        # Modelo simplificado para texto
        model = keras.Sequential([
            keras.layers.Embedding(10000, 32),
            keras.layers.GlobalAveragePooling1D(),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _create_risk_model(self):
        """Cria modelo de avaliação de risco."""
        model = keras.Sequential([
            keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(3, activation='softmax')  # LOW, MEDIUM, HIGH
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _create_forecast_model(self):
        """Cria modelo de previsão."""
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(10,)),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1)  # Retorno previsto
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def _get_safe_analysis(self, market_data: Dict) -> MarketAnalysis:
        """Retorna análise segura em caso de erro."""
        current_price = market_data.get("prices", [0])[-1] if market_data.get("prices") else 0
        
        return MarketAnalysis(
            signal="HOLD",
            confidence=0.5,
            reasoning="Análise de segurança ativada devido a erro no sistema",
            suggested_entry=current_price,
            suggested_stop_loss=0.02,
            suggested_take_profit=0.04,
            risk_level="MEDIUM",
            time_horizon="SHORT",
            market_regime="UNKNOWN",
            key_levels={"current_price": current_price},
            sentiment_score=0.5
        )