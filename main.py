"""
LEXTRADER-IAG 4.0 - Sistema Principal
======================================
Sistema de Inteligência Artificial Avançada para Trading e Análise de Mercados

Autor: LEXTRADER Team
Versão: 4.0.0
Data: Janeiro 2026
"""

import asyncio
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lextrader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Imports dos sistemas
try:
    from crypto_analysis_advanced import AdvancedCryptoAnalyzer
    from forex_analysis_advanced import AdvancedForexAnalyzer
    from arbitrage_analysis_advanced import AdvancedArbitrageAnalyzer
    from unified_market_analyzer import UnifiedMarketAnalyzer
    MARKET_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Sistemas de análise de mercados não disponíveis: {e}")
    MARKET_ANALYSIS_AVAILABLE = False

try:
    from advanced_integration_manager import AdvancedIntegrationManager
    INTEGRATION_AVAILABLE = True
except ImportError:
    logger.warning("Advanced Integration Manager não disponível")
    INTEGRATION_AVAILABLE = False

try:
    from Inteligencia_artificial_central import InteligenciaArtificialCentral
    IA_CENTRAL_AVAILABLE = True
except (ImportError, UnicodeEncodeError) as e:
    logger.warning(f"IA Central nao disponivel: {e}")
    IA_CENTRAL_AVAILABLE = False


class LexTraderIAG:
    """Sistema Principal LEXTRADER-IAG 4.0"""
    
    def __init__(self):
        self.version = "4.0.0"
        self.name = "LEXTRADER-IAG"
        self.initialized = False
        
        # Analisadores
        self.crypto_analyzer: Optional[AdvancedCryptoAnalyzer] = None
        self.forex_analyzer: Optional[AdvancedForexAnalyzer] = None
        self.arbitrage_analyzer: Optional[AdvancedArbitrageAnalyzer] = None
        self.unified_analyzer: Optional[UnifiedMarketAnalyzer] = None
        
        # Sistemas avançados
        self.integration_manager: Optional[AdvancedIntegrationManager] = None
        self.ia_central: Optional[InteligenciaArtificialCentral] = None
        
        logger.info(f"🚀 {self.name} v{self.version} inicializado")
    
    async def initialize(self):
        """Inicializa todos os sistemas"""
        logger.info("=" * 80)
        logger.info(f"🚀 Inicializando {self.name} v{self.version}")
        logger.info("=" * 80)
        
        # Inicializar sistemas de análise de mercados
        if MARKET_ANALYSIS_AVAILABLE:
            logger.info("📊 Inicializando sistemas de análise de mercados...")
            try:
                self.crypto_analyzer = AdvancedCryptoAnalyzer()
                logger.info("  ✅ Crypto Analyzer inicializado")
            except Exception as e:
                logger.error(f"  ❌ Erro ao inicializar Crypto Analyzer: {e}")
            
            try:
                self.forex_analyzer = AdvancedForexAnalyzer()
                logger.info("  ✅ Forex Analyzer inicializado")
            except Exception as e:
                logger.error(f"  ❌ Erro ao inicializar Forex Analyzer: {e}")
            
            try:
                self.arbitrage_analyzer = AdvancedArbitrageAnalyzer()
                logger.info("  ✅ Arbitrage Analyzer inicializado")
            except Exception as e:
                logger.error(f"  ❌ Erro ao inicializar Arbitrage Analyzer: {e}")
            
            try:
                self.unified_analyzer = UnifiedMarketAnalyzer()
                logger.info("  ✅ Unified Analyzer inicializado")
            except Exception as e:
                logger.error(f"  ❌ Erro ao inicializar Unified Analyzer: {e}")
        
        # Inicializar sistemas avançados
        if INTEGRATION_AVAILABLE:
            logger.info("🔧 Inicializando Advanced Integration Manager...")
            try:
                self.integration_manager = AdvancedIntegrationManager()
                status = self.integration_manager.get_systems_status()
                logger.info(f"  ✅ Integration Manager inicializado")
                logger.info(f"  📊 Sistemas ativos: {status['active_systems']}")
                logger.info(f"  ⚠️ Sistemas inativos: {status['inactive_systems']}")
            except Exception as e:
                logger.error(f"  ❌ Erro ao inicializar Integration Manager: {e}")
        
        if IA_CENTRAL_AVAILABLE:
            logger.info("🧠 Inicializando IA Central...")
            try:
                self.ia_central = InteligenciaArtificialCentral()
                logger.info("  ✅ IA Central inicializada")
            except Exception as e:
                logger.error(f"  ❌ Erro ao inicializar IA Central: {e}")
        
        self.initialized = True
        logger.info("=" * 80)
        logger.info("✅ Sistema inicializado com sucesso!")
        logger.info("=" * 80)
    
    async def analyze_crypto(self, symbol: str = 'BTC/USDT', timeframe: str = '1h'):
        """Analisa criptomoeda"""
        if not self.crypto_analyzer:
            logger.error("❌ Crypto Analyzer não disponível")
            return None
        
        logger.info(f"🪙 Analisando {symbol}...")
        try:
            result = await self.crypto_analyzer.analyze(symbol, timeframe)
            
            logger.info(f"  Preço: ${result.price:,.2f}")
            logger.info(f"  Sinal: {result.signal.value}")
            logger.info(f"  Confiança: {result.confidence:.1f}%")
            logger.info(f"  Score Técnico: {result.technical_score:.1f}/100")
            logger.info(f"  Risco: {result.risk_score:.1f}/100")
            logger.info(f"  Previsão 24h: ${result.predicted_price_24h:,.2f}")
            
            return result
        except Exception as e:
            logger.error(f"❌ Erro na análise de crypto: {e}")
            return None
    
    async def analyze_forex(self, pair: str = 'EUR/USD', timeframe: str = '1h'):
        """Analisa par de forex"""
        if not self.forex_analyzer:
            logger.error("❌ Forex Analyzer não disponível")
            return None
        
        logger.info(f"💱 Analisando {pair}...")
        try:
            result = await self.forex_analyzer.analyze(pair, timeframe)
            
            logger.info(f"  Bid/Ask: {result.bid:.5f} / {result.ask:.5f}")
            logger.info(f"  Sinal: {result.signal.value}")
            logger.info(f"  Confiança: {result.confidence:.1f}%")
            logger.info(f"  Sessão: {result.session.value}")
            logger.info(f"  Tendência: {result.trend_strength.value}")
            
            return result
        except Exception as e:
            logger.error(f"❌ Erro na análise de forex: {e}")
            return None
    
    async def scan_arbitrage(self, assets: list = None, exchanges: list = None):
        """Escaneia oportunidades de arbitragem"""
        if not self.arbitrage_analyzer:
            logger.error("❌ Arbitrage Analyzer não disponível")
            return None
        
        if assets is None:
            assets = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
        if exchanges is None:
            exchanges = ['binance', 'coinbase', 'kraken']
        
        logger.info(f"⚡ Escaneando arbitragem...")
        try:
            result = await self.arbitrage_analyzer.scan_all_opportunities(assets, exchanges)
            
            logger.info(f"  Oportunidades: {result.opportunities_found}")
            logger.info(f"  Lucro Total: {result.total_profit_potential:.2f}%")
            
            if result.best_opportunity:
                best = result.best_opportunity
                logger.info(f"  Melhor: {best.type.value} - {best.asset}")
                logger.info(f"  Lucro Líquido: {best.net_profit:.2f}%")
                logger.info(f"  Risco: {best.risk_score}/100")
            
            return result
        except Exception as e:
            logger.error(f"❌ Erro no scan de arbitragem: {e}")
            return None
    
    async def analyze_unified(self, crypto_symbols: list = None, forex_pairs: list = None,
                            arbitrage_assets: list = None, exchanges: list = None):
        """Análise unificada de todos os mercados"""
        if not self.unified_analyzer:
            logger.error("❌ Unified Analyzer não disponível")
            return None
        
        if crypto_symbols is None:
            crypto_symbols = ['BTC/USDT']
        if forex_pairs is None:
            forex_pairs = ['EUR/USD']
        if arbitrage_assets is None:
            arbitrage_assets = ['BTC/USDT', 'ETH/USDT']
        if exchanges is None:
            exchanges = ['binance', 'coinbase']
        
        logger.info(f"🌐 Análise unificada de mercados...")
        try:
            result = await self.unified_analyzer.analyze_all_markets(
                crypto_symbols=crypto_symbols,
                forex_pairs=forex_pairs,
                arbitrage_assets=arbitrage_assets,
                exchanges=exchanges
            )
            
            logger.info(f"  Sinal Geral: {result.overall_signal.value}")
            logger.info(f"  Confiança: {result.confidence:.1f}%")
            logger.info(f"  Risco Geral: {result.risk_assessment['overall_risk']:.1f}/100")
            logger.info(f"  Mercados: {result.metadata['markets_analyzed']}")
            
            return result
        except Exception as e:
            logger.error(f"❌ Erro na análise unificada: {e}")
            return None
    
    async def run_full_analysis(self):
        """Executa análise completa de todos os mercados"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 ANÁLISE COMPLETA DE MERCADOS")
        logger.info("=" * 80)
        
        results = {}
        
        # Análise de Crypto
        crypto_result = await self.analyze_crypto('BTC/USDT')
        if crypto_result:
            results['crypto'] = crypto_result
        
        # Análise de Forex
        forex_result = await self.analyze_forex('EUR/USD')
        if forex_result:
            results['forex'] = forex_result
        
        # Análise de Arbitragem
        arb_result = await self.scan_arbitrage()
        if arb_result:
            results['arbitrage'] = arb_result
        
        # Análise Unificada
        unified_result = await self.analyze_unified()
        if unified_result:
            results['unified'] = unified_result
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ ANÁLISE COMPLETA CONCLUÍDA")
        logger.info("=" * 80)
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        status = {
            'version': self.version,
            'initialized': self.initialized,
            'timestamp': datetime.now().isoformat(),
            'systems': {
                'crypto_analyzer': self.crypto_analyzer is not None,
                'forex_analyzer': self.forex_analyzer is not None,
                'arbitrage_analyzer': self.arbitrage_analyzer is not None,
                'unified_analyzer': self.unified_analyzer is not None,
                'integration_manager': self.integration_manager is not None,
                'ia_central': self.ia_central is not None
            }
        }
        
        if self.integration_manager:
            status['advanced_systems'] = self.integration_manager.get_systems_status()
        
        return status
    
    def print_banner(self):
        """Imprime banner do sistema"""
        banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        LEXTRADER-IAG 4.0                                     ║
║                                                                              ║
║           Sistema de IA Avançada para Trading e Análise de Mercados         ║
║                                                                              ║
║  🪙 Análise de Criptomoedas  |  💱 Análise de Forex                         ║
║  ⚡ Análise de Arbitragem    |  🌐 Análise Unificada                        ║
║  🧠 IA Central               |  🔧 Sistemas Avançados                        ║
║                                                                              ║
║  Versão: {self.version}                                                         ║
║  Status: {'🟢 OPERACIONAL' if self.initialized else '🟡 INICIALIZANDO'}                                                    ║
║  Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}                                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)


async def main():
    """Função principal"""
    # Criar sistema
    system = LexTraderIAG()
    system.print_banner()
    
    # Inicializar
    await system.initialize()
    
    # Menu interativo
    while True:
        print("\n" + "=" * 80)
        print("MENU PRINCIPAL")
        print("=" * 80)
        print("1. Analisar Criptomoeda (BTC/USDT)")
        print("2. Analisar Forex (EUR/USD)")
        print("3. Escanear Arbitragem")
        print("4. Análise Unificada")
        print("5. Análise Completa (Todos os Mercados)")
        print("6. Ver Status do Sistema")
        print("7. Executar Testes")
        print("0. Sair")
        print("=" * 80)
        
        try:
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == '1':
                symbol = input("Símbolo (padrão BTC/USDT): ").strip() or 'BTC/USDT'
                await system.analyze_crypto(symbol)
            
            elif choice == '2':
                pair = input("Par (padrão EUR/USD): ").strip() or 'EUR/USD'
                await system.analyze_forex(pair)
            
            elif choice == '3':
                await system.scan_arbitrage()
            
            elif choice == '4':
                await system.analyze_unified()
            
            elif choice == '5':
                await system.run_full_analysis()
            
            elif choice == '6':
                status = system.get_status()
                print("\n📊 STATUS DO SISTEMA:")
                print(f"  Versão: {status['version']}")
                print(f"  Inicializado: {'✅' if status['initialized'] else '❌'}")
                print(f"  Timestamp: {status['timestamp']}")
                print("\n  Sistemas:")
                for sys_name, sys_status in status['systems'].items():
                    print(f"    {sys_name}: {'✅' if sys_status else '❌'}")
                
                if 'advanced_systems' in status:
                    print(f"\n  Sistemas Avançados:")
                    print(f"    Ativos: {status['advanced_systems']['active_systems']}")
                    print(f"    Inativos: {status['advanced_systems']['inactive_systems']}")
            
            elif choice == '7':
                print("\n🧪 Executando testes...")
                import subprocess
                result = subprocess.run(['python', 'test_market_analysis.py'], 
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.returncode != 0:
                    print(result.stderr)
            
            elif choice == '0':
                print("\n👋 Encerrando LEXTRADER-IAG 4.0...")
                break
            
            else:
                print("❌ Opção inválida!")
        
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando LEXTRADER-IAG 4.0...")
            break
        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        logger.error(f"💥 Erro crítico: {e}")
        print(f"💥 Erro crítico: {e}")
        sys.exit(1)
