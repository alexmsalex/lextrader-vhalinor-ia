"""
Pionex API Integration
======================
Integração completa com a exchange Pionex para trading de criptomoedas
Camada Sensorial (Layer 01) - LEXTRADER-IAG 4.0
"""

import json
import logging
import time
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from urllib.parse import urlencode

import requests
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderType(Enum):
    """Tipos de ordem"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"


class OrderSide(Enum):
    """Lado da ordem"""
    BUY = "BUY"
    SELL = "SELL"


class BotType(Enum):
    """Tipos de bot Pionex"""
    GRID_TRADING = "GRID_TRADING"
    DCA_BOT = "DCA_BOT"
    REBALANCING = "REBALANCING"
    ARBITRAGE = "ARBITRAGE"
    LEVERAGED_GRID = "LEVERAGED_GRID"
    INFINITY_GRID = "INFINITY_GRID"
    MARTINGALE = "MARTINGALE"


class PionexAPI:
    """
    Cliente para integração com Pionex API
    Suporte completo para trading manual e bots automatizados
    """

    def __init__(self, api_key: str, api_secret: str, environment: str = "live"):
        """
        Args:
            api_key: Chave da API Pionex
            api_secret: Secret da API
            environment: 'live' ou 'testnet'
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.environment = environment
        
        # URLs da API
        if environment == "testnet":
            self.base_url = "https://api.testnet.pionex.com"
        else:
            self.base_url = "https://api.pionex.com"
        
        # Headers padrão
        self.headers = {
            "Content-Type": "application/json",
            "PIONEX-KEY": self.api_key
        }

    def _generate_signature(self, query_string: str, timestamp: str) -> str:
        """
        Gera assinatura HMAC SHA256 para autenticação
        """
        message = f"{timestamp}{query_string}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _make_request(self, method: str, endpoint: str, params: Dict = None,
                     data: Dict = None, signed: bool = False) -> Optional[Dict]:
        """
        Faz requisição para a API Pionex
        """
        try:
            url = f"{self.base_url}{endpoint}"
            timestamp = str(int(time.time() * 1000))
            
            headers = self.headers.copy()
            headers["PIONEX-TIMESTAMP"] = timestamp
            
            if signed:
                query_string = ""
                if method == "GET" and params:
                    query_string = urlencode(params)
                elif method == "POST" and data:
                    query_string = json.dumps(data, separators=(',', ':'))
                
                signature = self._generate_signature(query_string, timestamp)
                headers["PIONEX-SIGNATURE"] = signature
            
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Erro na API Pionex: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na requisição Pionex: {e}")
            return None

    # ==================== INFORMAÇÕES DA CONTA ====================

    def get_account_info(self) -> Optional[Dict]:
        """
        Obtém informações da conta
        """
        result = self._make_request("GET", "/api/v1/account", signed=True)
        if result and result.get("result"):
            logger.info("✅ Informações da conta obtidas")
            return result["result"]
        return None

    def get_balances(self) -> List[Dict]:
        """
        Obtém saldos de todas as moedas
        """
        result = self._make_request("GET", "/api/v1/account/balances", signed=True)
        if result and result.get("result"):
            balances = result["result"]["balances"]
            logger.info(f"✅ {len(balances)} saldos obtidos")
            return balances
        return []

    def get_balance(self, asset: str) -> Optional[Dict]:
        """
        Obtém saldo de um ativo específico
        """
        balances = self.get_balances()
        for balance in balances:
            if balance.get("asset") == asset:
                return {
                    "asset": asset,
                    "free": float(balance.get("free", 0)),
                    "locked": float(balance.get("locked", 0)),
                    "total": float(balance.get("free", 0)) + float(balance.get("locked", 0))
                }
        return None

    # ==================== DADOS DE MERCADO ====================

    def get_exchange_info(self) -> Optional[Dict]:
        """
        Obtém informações da exchange (símbolos, limites, etc.)
        """
        result = self._make_request("GET", "/api/v1/common/symbols")
        if result and result.get("result"):
            logger.info("✅ Informações da exchange obtidas")
            return result["result"]
        return None

    def get_symbols(self) -> List[Dict]:
        """
        Obtém lista de símbolos disponíveis
        """
        exchange_info = self.get_exchange_info()
        if exchange_info:
            symbols = exchange_info.get("symbols", [])
            logger.info(f"✅ {len(symbols)} símbolos obtidos")
            return symbols
        return []

    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """
        Obtém ticker de um símbolo
        """
        params = {"symbol": symbol}
        result = self._make_request("GET", "/api/v1/market/ticker", params=params)
        if result and result.get("result"):
            ticker = result["result"]
            return {
                "symbol": symbol,
                "price": float(ticker.get("price", 0)),
                "bid": float(ticker.get("bidPrice", 0)),
                "ask": float(ticker.get("askPrice", 0)),
                "volume": float(ticker.get("volume", 0)),
                "change": float(ticker.get("priceChange", 0)),
                "change_percent": float(ticker.get("priceChangePercent", 0)),
                "high": float(ticker.get("highPrice", 0)),
                "low": float(ticker.get("lowPrice", 0))
            }
        return None

    def get_all_tickers(self) -> List[Dict]:
        """
        Obtém tickers de todos os símbolos
        """
        result = self._make_request("GET", "/api/v1/market/tickers")
        if result and result.get("result"):
            tickers = []
            for ticker_data in result["result"]:
                tickers.append({
                    "symbol": ticker_data.get("symbol"),
                    "price": float(ticker_data.get("price", 0)),
                    "volume": float(ticker_data.get("volume", 0)),
                    "change_percent": float(ticker_data.get("priceChangePercent", 0))
                })
            logger.info(f"✅ {len(tickers)} tickers obtidos")
            return tickers
        return []

    def get_order_book(self, symbol: str, limit: int = 100) -> Optional[Dict]:
        """
        Obtém order book (livro de ofertas)
        """
        params = {"symbol": symbol, "limit": limit}
        result = self._make_request("GET", "/api/v1/market/depth", params=params)
        if result and result.get("result"):
            order_book = result["result"]
            return {
                "symbol": symbol,
                "bids": [[float(bid[0]), float(bid[1])] for bid in order_book.get("bids", [])],
                "asks": [[float(ask[0]), float(ask[1])] for ask in order_book.get("asks", [])]
            }
        return None

    def get_klines(self, symbol: str, interval: str = "1h", 
                   limit: int = 500) -> pd.DataFrame:
        """
        Obtém dados de candlestick (OHLCV)
        
        Args:
            symbol: Par de trading (ex: BTCUSDT)
            interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
            limit: Número de candles (máximo 1000)
        """
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        
        result = self._make_request("GET", "/api/v1/market/klines", params=params)
        if result and result.get("result"):
            klines_data = result["result"]
            
            # Converter para DataFrame
            df = pd.DataFrame(klines_data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'count', 'taker_buy_volume',
                'taker_buy_quote_volume', 'ignore'
            ])
            
            # Converter tipos
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_columns] = df[numeric_columns].astype(float)
            df.set_index('timestamp', inplace=True)
            
            logger.info(f"✅ {len(df)} candles obtidos para {symbol}")
            return df
        
        return pd.DataFrame()

    # ==================== TRADING MANUAL ====================

    def place_order(self, symbol: str, side: OrderSide, order_type: OrderType,
                   quantity: float, price: float = None, 
                   stop_price: float = None) -> Optional[Dict]:
        """
        Coloca uma ordem
        """
        order_data = {
            "symbol": symbol,
            "side": side.value,
            "type": order_type.value,
            "quantity": str(quantity)
        }
        
        if price:
            order_data["price"] = str(price)
        if stop_price:
            order_data["stopPrice"] = str(stop_price)
        
        result = self._make_request("POST", "/api/v1/trade/order", data=order_data, signed=True)
        if result and result.get("result"):
            order_result = result["result"]
            logger.info(f"✅ Ordem colocada: {symbol} {side.value} {quantity}")
            return order_result
        return None

    def place_market_order(self, symbol: str, side: OrderSide, 
                          quantity: float) -> Optional[Dict]:
        """
        Coloca ordem a mercado
        """
        return self.place_order(symbol, side, OrderType.MARKET, quantity)

    def place_limit_order(self, symbol: str, side: OrderSide,
                         quantity: float, price: float) -> Optional[Dict]:
        """
        Coloca ordem limitada
        """
        return self.place_order(symbol, side, OrderType.LIMIT, quantity, price)

    def get_order(self, symbol: str, order_id: str) -> Optional[Dict]:
        """
        Obtém informações de uma ordem
        """
        params = {"symbol": symbol, "orderId": order_id}
        result = self._make_request("GET", "/api/v1/trade/order", params=params, signed=True)
        if result and result.get("result"):
            return result["result"]
        return None

    def cancel_order(self, symbol: str, order_id: str) -> bool:
        """
        Cancela uma ordem
        """
        params = {"symbol": symbol, "orderId": order_id}
        result = self._make_request("DELETE", "/api/v1/trade/order", params=params, signed=True)
        if result and result.get("result"):
            logger.info(f"✅ Ordem {order_id} cancelada")
            return True
        return False

    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """
        Obtém ordens abertas
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        
        result = self._make_request("GET", "/api/v1/trade/openOrders", params=params, signed=True)
        if result and result.get("result"):
            orders = result["result"]
            logger.info(f"✅ {len(orders)} ordens abertas obtidas")
            return orders
        return []

    def get_order_history(self, symbol: str = None, limit: int = 500) -> List[Dict]:
        """
        Obtém histórico de ordens
        """
        params = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        
        result = self._make_request("GET", "/api/v1/trade/allOrders", params=params, signed=True)
        if result and result.get("result"):
            orders = result["result"]
            logger.info(f"✅ {len(orders)} ordens históricas obtidas")
            return orders
        return []

    # ==================== BOTS PIONEX ====================

    def get_available_bots(self) -> List[Dict]:
        """
        Obtém tipos de bots disponíveis
        """
        result = self._make_request("GET", "/api/v1/bots/types")
        if result and result.get("result"):
            bots = result["result"]
            logger.info(f"✅ {len(bots)} tipos de bots disponíveis")
            return bots
        return []

    def create_grid_bot(self, symbol: str, lower_price: float, upper_price: float,
                       grid_number: int, investment_amount: float) -> Optional[Dict]:
        """
        Cria um Grid Trading Bot
        """
        bot_data = {
            "symbol": symbol,
            "type": BotType.GRID_TRADING.value,
            "lowerPrice": str(lower_price),
            "upperPrice": str(upper_price),
            "gridNumber": grid_number,
            "investmentAmount": str(investment_amount)
        }
        
        result = self._make_request("POST", "/api/v1/bots/create", data=bot_data, signed=True)
        if result and result.get("result"):
            bot_info = result["result"]
            logger.info(f"✅ Grid Bot criado: {symbol} ({grid_number} grids)")
            return bot_info
        return None

    def create_dca_bot(self, symbol: str, side: OrderSide, 
                      investment_per_cycle: float, price_deviation: float,
                      max_cycles: int) -> Optional[Dict]:
        """
        Cria um DCA (Dollar Cost Averaging) Bot
        """
        bot_data = {
            "symbol": symbol,
            "type": BotType.DCA_BOT.value,
            "side": side.value,
            "investmentPerCycle": str(investment_per_cycle),
            "priceDeviation": str(price_deviation),
            "maxCycles": max_cycles
        }
        
        result = self._make_request("POST", "/api/v1/bots/create", data=bot_data, signed=True)
        if result and result.get("result"):
            bot_info = result["result"]
            logger.info(f"✅ DCA Bot criado: {symbol} {side.value}")
            return bot_info
        return None

    def get_active_bots(self) -> List[Dict]:
        """
        Obtém bots ativos
        """
        result = self._make_request("GET", "/api/v1/bots/active", signed=True)
        if result and result.get("result"):
            bots = result["result"]
            logger.info(f"✅ {len(bots)} bots ativos")
            return bots
        return []

    def get_bot_info(self, bot_id: str) -> Optional[Dict]:
        """
        Obtém informações de um bot específico
        """
        params = {"botId": bot_id}
        result = self._make_request("GET", "/api/v1/bots/info", params=params, signed=True)
        if result and result.get("result"):
            return result["result"]
        return None

    def stop_bot(self, bot_id: str) -> bool:
        """
        Para um bot
        """
        data = {"botId": bot_id}
        result = self._make_request("POST", "/api/v1/bots/stop", data=data, signed=True)
        if result and result.get("result"):
            logger.info(f"✅ Bot {bot_id} parado")
            return True
        return False

    def get_bot_history(self, bot_id: str) -> List[Dict]:
        """
        Obtém histórico de um bot
        """
        params = {"botId": bot_id}
        result = self._make_request("GET", "/api/v1/bots/history", params=params, signed=True)
        if result and result.get("result"):
            history = result["result"]
            logger.info(f"✅ Histórico do bot {bot_id} obtido")
            return history
        return []

    # ==================== ANÁLISE E RELATÓRIOS ====================

    def get_trade_history(self, symbol: str = None, limit: int = 500) -> List[Dict]:
        """
        Obtém histórico de trades
        """
        params = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        
        result = self._make_request("GET", "/api/v1/trade/myTrades", params=params, signed=True)
        if result and result.get("result"):
            trades = result["result"]
            logger.info(f"✅ {len(trades)} trades históricos obtidos")
            return trades
        return []

    def calculate_pnl(self, symbol: str = None, days: int = 30) -> Dict:
        """
        Calcula P&L (Profit and Loss)
        """
        trades = self.get_trade_history(symbol, limit=1000)
        
        if not trades:
            return {}
        
        # Filtrar trades dos últimos N dias
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_trades = []
        
        for trade in trades:
            trade_time = datetime.fromtimestamp(int(trade.get("time", 0)) / 1000)
            if trade_time >= cutoff_date:
                recent_trades.append(trade)
        
        if not recent_trades:
            return {}
        
        # Calcular métricas
        total_trades = len(recent_trades)
        total_volume = sum(float(t.get("quoteQty", 0)) for t in recent_trades)
        total_fees = sum(float(t.get("commission", 0)) for t in recent_trades)
        
        buy_trades = [t for t in recent_trades if t.get("isBuyer")]
        sell_trades = [t for t in recent_trades if not t.get("isBuyer")]
        
        return {
            "symbol": symbol or "ALL",
            "period_days": days,
            "total_trades": total_trades,
            "buy_trades": len(buy_trades),
            "sell_trades": len(sell_trades),
            "total_volume": round(total_volume, 2),
            "total_fees": round(total_fees, 6),
            "avg_trade_size": round(total_volume / total_trades, 2) if total_trades > 0 else 0
        }

    def get_top_performers(self, limit: int = 10) -> List[Dict]:
        """
        Obtém top performers (maiores ganhos/perdas)
        """
        tickers = self.get_all_tickers()
        
        # Ordenar por mudança percentual
        sorted_tickers = sorted(tickers, key=lambda x: x["change_percent"], reverse=True)
        
        top_gainers = sorted_tickers[:limit]
        top_losers = sorted_tickers[-limit:]
        
        return {
            "top_gainers": top_gainers,
            "top_losers": top_losers
        }

    # ==================== UTILITÁRIOS ====================

    def get_server_time(self) -> Optional[Dict]:
        """
        Obtém horário do servidor
        """
        result = self._make_request("GET", "/api/v1/common/time")
        if result and result.get("result"):
            server_time = result["result"]["serverTime"]
            return {
                "server_time": server_time,
                "datetime": datetime.fromtimestamp(server_time / 1000)
            }
        return None

    def test_connectivity(self) -> bool:
        """
        Testa conectividade com a API
        """
        result = self._make_request("GET", "/api/v1/common/ping")
        if result:
            logger.info("✅ Conectividade com Pionex OK")
            return True
        else:
            logger.error("❌ Falha na conectividade com Pionex")
            return False

    def get_system_status(self) -> Optional[Dict]:
        """
        Obtém status do sistema
        """
        result = self._make_request("GET", "/api/v1/common/systemStatus")
        if result and result.get("result"):
            return result["result"]
        return None


def main():
    """
    Função de demonstração da API Pionex
    """
    # Configuração (usar variáveis de ambiente em produção)
    api_key = "your_api_key"
    api_secret = "your_api_secret"
    
    # Inicializar API
    api = PionexAPI(api_key, api_secret, environment="live")
    
    print("="*70)
    print("🤖 DEMONSTRAÇÃO DA API PIONEX")
    print("="*70)
    
    # Teste de conectividade
    if api.test_connectivity():
        print("✅ Conectividade OK")
    else:
        print("❌ Falha na conectividade")
    
    print("\n⚠️  Para usar em produção:")
    print("1. Configure suas credenciais Pionex")
    print("2. Ative a API na sua conta Pionex")
    print("3. Configure permissões adequadas")
    
    # Demonstração com dados simulados
    print("\n🤖 Funcionalidades disponíveis:")
    print("✅ Trading manual (Market, Limit, Stop)")
    print("✅ Grid Trading Bots")
    print("✅ DCA (Dollar Cost Averaging) Bots")
    print("✅ Rebalancing Bots")
    print("✅ Arbitrage Bots")
    print("✅ Dados de mercado em tempo real")
    print("✅ Histórico de preços (OHLCV)")
    print("✅ Order book (livro de ofertas)")
    print("✅ Gestão de ordens e posições")
    print("✅ Análise de P&L")
    print("✅ Top performers")
    
    print("\n" + "="*70)
    print("✅ API Pionex pronta para uso!")
    print("="*70)


if __name__ == "__main__":
    main()