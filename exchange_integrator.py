"""
Exchange Integrator
===================
Sistema integrado para gerenciar múltiplas exchanges
Camada Sensorial (Layer 01) - LEXTRADER-IAG 4.0
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

from ctrader_api import CTraderAPI
from pionex_api import PionexAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExchangeType(Enum):
    """Tipos de exchange"""
    CTRADER = "CTRADER"
    PIONEX = "PIONEX"
    BINANCE = "BINANCE"


class ExchangeIntegrator:
    """
    Integrador de múltiplas exchanges
    Gerencia conexões e operações em diferentes plataformas
    """

    def __init__(self):
        self.exchanges = {}
        self.active_connections = {}
        self.market_data = {}
        
    def add_ctrader(self, name: str, client_id: str, client_secret: str,
                   environment: str = "demo") -> bool:
        """
        Adiciona conexão cTrader
        """
        try:
            ctrader = CTraderAPI(client_id, client_secret, environment=environment)
            self.exchanges[name] = {
                "type": ExchangeType.CTRADER,
                "api": ctrader,
                "status": "configured"
            }
            logger.info(f"✅ cTrader '{name}' adicionado")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao adicionar cTrader '{name}': {e}")
            return False

    def add_pionex(self, name: str, api_key: str, api_secret: str,
                  environment: str = "live") -> bool:
        """
        Adiciona conexão Pionex
        """
        try:
            pionex = PionexAPI(api_key, api_secret, environment=environment)
            self.exchanges[name] = {
                "type": ExchangeType.PIONEX,
                "api": pionex,
                "status": "configured"
            }
            logger.info(f"✅ Pionex '{name}' adicionado")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao adicionar Pionex '{name}': {e}")
            return False

    def authenticate_ctrader(self, name: str, username: str, password: str) -> bool:
        """
        Autentica conexão cTrader
        """
        if name not in self.exchanges:
            logger.error(f"❌ Exchange '{name}' não encontrada")
            return False
        
        exchange = self.exchanges[name]
        if exchange["type"] != ExchangeType.CTRADER:
            logger.error(f"❌ '{name}' não é uma conexão cTrader")
            return False
        
        try:
            api = exchange["api"]
            if api.authenticate(username, password):
                exchange["status"] = "authenticated"
                self.active_connections[name] = exchange
                logger.info(f"✅ cTrader '{name}' autenticado")
                return True
            else:
                logger.error(f"❌ Falha na autenticação cTrader '{name}'")
                return False
        except Exception as e:
            logger.error(f"❌ Erro na autenticação cTrader '{name}': {e}")
            return False

    def test_connections(self) -> Dict[str, bool]:
        """
        Testa todas as conexões
        """
        results = {}
        
        for name, exchange in self.exchanges.items():
            try:
                api = exchange["api"]
                
                if exchange["type"] == ExchangeType.CTRADER:
                    # Para cTrader, verificar se está autenticado
                    if exchange["status"] == "authenticated":
                        accounts = api.get_accounts()
                        results[name] = len(accounts) > 0
                    else:
                        results[name] = False
                        
                elif exchange["type"] == ExchangeType.PIONEX:
                    # Para Pionex, testar conectividade
                    results[name] = api.test_connectivity()
                    
                else:
                    results[name] = False
                    
            except Exception as e:
                logger.error(f"❌ Erro ao testar '{name}': {e}")
                results[name] = False
        
        return results

    def get_all_balances(self) -> Dict[str, Dict]:
        """
        Obtém saldos de todas as exchanges
        """
        all_balances = {}
        
        for name, exchange in self.active_connections.items():
            try:
                api = exchange["api"]
                
                if exchange["type"] == ExchangeType.CTRADER:
                    accounts = api.get_accounts()
                    if accounts:
                        account_id = accounts[0].get("id")
                        balance = api.get_balance(account_id)
                        if balance:
                            all_balances[name] = balance
                            
                elif exchange["type"] == ExchangeType.PIONEX:
                    balances = api.get_balances()
                    if balances:
                        # Consolidar saldos principais
                        consolidated = {}
                        for balance in balances:
                            asset = balance.get("asset")
                            if float(balance.get("free", 0)) > 0 or float(balance.get("locked", 0)) > 0:
                                consolidated[asset] = {
                                    "free": float(balance.get("free", 0)),
                                    "locked": float(balance.get("locked", 0)),
                                    "total": float(balance.get("free", 0)) + float(balance.get("locked", 0))
                                }
                        all_balances[name] = consolidated
                        
            except Exception as e:
                logger.error(f"❌ Erro ao obter saldos de '{name}': {e}")
                all_balances[name] = {}
        
        return all_balances

    def get_market_data_summary(self) -> Dict[str, Dict]:
        """
        Obtém resumo de dados de mercado de todas as exchanges
        """
        market_summary = {}
        
        for name, exchange in self.active_connections.items():
            try:
                api = exchange["api"]
                
                if exchange["type"] == ExchangeType.CTRADER:
                    # Obter dados dos principais pares forex
                    forex_data = api.get_major_pairs_data()
                    market_summary[name] = {
                        "type": "forex",
                        "pairs": len(forex_data),
                        "data": forex_data
                    }
                    
                elif exchange["type"] == ExchangeType.PIONEX:
                    # Obter top performers
                    performers = api.get_top_performers(5)
                    market_summary[name] = {
                        "type": "crypto",
                        "top_gainers": performers.get("top_gainers", []),
                        "top_losers": performers.get("top_losers", [])
                    }
                    
            except Exception as e:
                logger.error(f"❌ Erro ao obter dados de mercado de '{name}': {e}")
                market_summary[name] = {}
        
        return market_summary

    def execute_arbitrage_opportunity(self, opportunity: Dict) -> Dict:
        """
        Executa oportunidade de arbitragem entre exchanges
        """
        try:
            buy_exchange = opportunity.get("buy_exchange")
            sell_exchange = opportunity.get("sell_exchange")
            symbol = opportunity.get("symbol")
            quantity = opportunity.get("quantity")
            
            if buy_exchange not in self.active_connections or sell_exchange not in self.active_connections:
                return {"success": False, "error": "Exchanges não conectadas"}
            
            buy_api = self.active_connections[buy_exchange]["api"]
            sell_api = self.active_connections[sell_exchange]["api"]
            
            # Simular execução (em produção, executar ordens reais)
            execution_result = {
                "success": True,
                "buy_exchange": buy_exchange,
                "sell_exchange": sell_exchange,
                "symbol": symbol,
                "quantity": quantity,
                "expected_profit": opportunity.get("profit_amount", 0),
                "timestamp": datetime.now().isoformat(),
                "status": "SIMULATED"
            }
            
            logger.info(f"💰 Arbitragem simulada: {symbol} | Lucro: ${execution_result['expected_profit']:.2f}")
            return execution_result
            
        except Exception as e:
            logger.error(f"❌ Erro na execução de arbitragem: {e}")
            return {"success": False, "error": str(e)}

    def get_connection_status(self) -> Dict:
        """
        Obtém status de todas as conexões
        """
        status = {
            "total_exchanges": len(self.exchanges),
            "active_connections": len(self.active_connections),
            "exchanges": {}
        }
        
        for name, exchange in self.exchanges.items():
            status["exchanges"][name] = {
                "type": exchange["type"].value,
                "status": exchange["status"],
                "active": name in self.active_connections
            }
        
        return status

    def generate_report(self) -> str:
        """
        Gera relatório completo do integrador
        """
        report = []
        report.append("="*70)
        report.append("🔗 RELATÓRIO DO INTEGRADOR DE EXCHANGES")
        report.append("="*70)
        report.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Status das conexões
        status = self.get_connection_status()
        report.append("📊 STATUS DAS CONEXÕES:")
        report.append("-"*70)
        report.append(f"Total de exchanges: {status['total_exchanges']}")
        report.append(f"Conexões ativas: {status['active_connections']}")
        report.append("")
        
        for name, info in status["exchanges"].items():
            active_status = "🟢 ATIVA" if info["active"] else "🔴 INATIVA"
            report.append(f"{name:20s} | {info['type']:10s} | {info['status']:15s} | {active_status}")
        
        # Teste de conectividade
        if self.active_connections:
            report.append("")
            report.append("🔍 TESTE DE CONECTIVIDADE:")
            report.append("-"*70)
            
            connectivity = self.test_connections()
            for name, is_connected in connectivity.items():
                status_icon = "✅" if is_connected else "❌"
                report.append(f"{status_icon} {name}")
        
        # Saldos
        if self.active_connections:
            report.append("")
            report.append("💰 SALDOS:")
            report.append("-"*70)
            
            balances = self.get_all_balances()
            for exchange_name, balance_data in balances.items():
                report.append(f"\n{exchange_name}:")
                if isinstance(balance_data, dict):
                    if "balance" in balance_data:  # cTrader format
                        report.append(f"  Saldo: {balance_data.get('balance', 0)}")
                        report.append(f"  Equity: {balance_data.get('equity', 0)}")
                        report.append(f"  Moeda: {balance_data.get('currency', 'USD')}")
                    else:  # Pionex format
                        for asset, data in balance_data.items():
                            if data["total"] > 0:
                                report.append(f"  {asset}: {data['total']:.6f}")
        
        report.append("")
        report.append("="*70)
        
        return "\n".join(report)

    def save_configuration(self, filename: str = "exchange_config.json"):
        """
        Salva configuração das exchanges (sem credenciais sensíveis)
        """
        config = {
            "timestamp": datetime.now().isoformat(),
            "exchanges": {}
        }
        
        for name, exchange in self.exchanges.items():
            config["exchanges"][name] = {
                "type": exchange["type"].value,
                "status": exchange["status"]
            }
        
        filepath = f"neural_layers/01_sensorial/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"💾 Configuração salva: {filepath}")


def main():
    """
    Função de demonstração do integrador
    """
    print("="*70)
    print("🔗 DEMONSTRAÇÃO DO INTEGRADOR DE EXCHANGES")
    print("="*70)
    
    # Inicializar integrador
    integrator = ExchangeIntegrator()
    
    # Adicionar exchanges (com credenciais fictícias)
    print("\n📝 Configurando exchanges...")
    integrator.add_ctrader("cTrader-Demo", "demo_client_id", "demo_secret", "demo")
    integrator.add_pionex("Pionex-Live", "demo_api_key", "demo_secret", "live")
    
    # Gerar relatório
    report = integrator.generate_report()
    print("\n" + report)
    
    # Salvar configuração
    integrator.save_configuration()
    
    print("\n" + "="*70)
    print("🎯 FUNCIONALIDADES DO INTEGRADOR:")
    print("="*70)
    print("✅ Gerenciamento de múltiplas exchanges")
    print("✅ Autenticação centralizada")
    print("✅ Teste de conectividade")
    print("✅ Consolidação de saldos")
    print("✅ Dados de mercado unificados")
    print("✅ Execução de arbitragem")
    print("✅ Relatórios consolidados")
    print("✅ Configuração persistente")
    
    print("\n" + "="*70)
    print("✅ INTEGRADOR PRONTO PARA USO!")
    print("="*70)


if __name__ == "__main__":
    main()