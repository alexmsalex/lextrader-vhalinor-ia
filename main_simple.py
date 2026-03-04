"""
LEXTRADER-IAG 4.0 - Sistema Principal (Versão Simplificada)
============================================================
Sistema de Análise de Mercados sem dependências da IA Central

Versão: 4.0.0
Data: Janeiro 2026
"""

import asyncio
import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lextrader.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Imports dos sistemas de análise
from crypto_analysis_advanced import AdvancedCryptoAnalyzer
from forex_analysis_advanced import AdvancedForexAnalyzer
from arbitrage_analysis_advanced import AdvancedArbitrageAnalyzer
from unified_market_analyzer import UnifiedMarketAnalyzer

# Import do gerenciador de sistemas autônomos
from autonomous_integration import autonomous_manager


class LexTraderSimple:
    """Sistema LEXTRADER-IAG 4.0 - Versão Simplificada"""
    
    def __init__(self):
        self.version = "4.0.0"
        self.name = "LEXTRADER-IAG"
        
        # Analisadores
        self.crypto_analyzer = None
        self.forex_analyzer = None
        self.arbitrage_analyzer = None
        self.unified_analyzer = None
        
        logger.info(f"🚀 {self.name} v{self.version} inicializado")
    
    async def initialize(self):
        """Inicializa todos os sistemas"""
        print("\n" + "=" * 80)
        print(f"🚀 Inicializando {self.name} v{self.version}")
        print("=" * 80)
        
        try:
            self.crypto_analyzer = AdvancedCryptoAnalyzer()
            print("  ✅ Crypto Analyzer inicializado")
        except Exception as e:
            print(f"  ❌ Erro ao inicializar Crypto Analyzer: {e}")
        
        try:
            self.forex_analyzer = AdvancedForexAnalyzer()
            print("  ✅ Forex Analyzer inicializado")
        except Exception as e:
            print(f"  ❌ Erro ao inicializar Forex Analyzer: {e}")
        
        try:
            self.arbitrage_analyzer = AdvancedArbitrageAnalyzer()
            print("  ✅ Arbitrage Analyzer inicializado")
        except Exception as e:
            print(f"  ❌ Erro ao inicializar Arbitrage Analyzer: {e}")
        
        try:
            self.unified_analyzer = UnifiedMarketAnalyzer()
            print("  ✅ Unified Analyzer inicializado")
        except Exception as e:
            print(f"  ❌ Erro ao inicializar Unified Analyzer: {e}")
        
        print("=" * 80)
        print("✅ Sistema inicializado com sucesso!")
        print("=" * 80)
    
    async def analyze_crypto(self, symbol='BTC/USDT', timeframe='1h'):
        """Analisa criptomoeda"""
        print(f"\n🪙 Analisando {symbol}...")
        result = await self.crypto_analyzer.analyze(symbol, timeframe)
        
        print(f"  Preço: ${result.price:,.2f}")
        print(f"  Sinal: {result.signal.value}")
        print(f"  Confiança: {result.confidence:.1f}%")
        print(f"  Score Técnico: {result.technical_score:.1f}/100")
        print(f"  Risco: {result.risk_score:.1f}/100")
        print(f"  Previsão 24h: ${result.predicted_price_24h:,.2f}")
        
        return result
    
    async def analyze_forex(self, pair='EUR/USD', timeframe='1h'):
        """Analisa par de forex"""
        print(f"\n💱 Analisando {pair}...")
        result = await self.forex_analyzer.analyze(pair, timeframe)
        
        print(f"  Bid/Ask: {result.bid:.5f} / {result.ask:.5f}")
        print(f"  Sinal: {result.signal.value}")
        print(f"  Confiança: {result.confidence:.1f}%")
        print(f"  Sessão: {result.session.value}")
        print(f"  Tendência: {result.trend_strength.value}")
        
        return result
    
    async def scan_arbitrage(self, assets=None, exchanges=None):
        """Escaneia oportunidades de arbitragem"""
        if assets is None:
            assets = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
        if exchanges is None:
            exchanges = ['binance', 'coinbase', 'kraken']
        
        print(f"\n⚡ Escaneando arbitragem...")
        result = await self.arbitrage_analyzer.scan_all_opportunities(assets, exchanges)
        
        print(f"  Oportunidades: {result.opportunities_found}")
        print(f"  Lucro Total: {result.total_profit_potential:.2f}%")
        
        if result.best_opportunity:
            best = result.best_opportunity
            print(f"  Melhor: {best.type.value} - {best.asset}")
            print(f"  Lucro Líquido: {best.net_profit:.2f}%")
            print(f"  Risco: {best.risk_score}/100")
        
        return result
    
    async def analyze_unified(self):
        """Análise unificada de todos os mercados"""
        print(f"\n🌐 Análise unificada de mercados...")
        result = await self.unified_analyzer.analyze_all_markets(
            crypto_symbols=['BTC/USDT'],
            forex_pairs=['EUR/USD'],
            arbitrage_assets=['BTC/USDT', 'ETH/USDT'],
            exchanges=['binance', 'coinbase']
        )
        
        print(f"  Sinal Geral: {result.overall_signal.value}")
        print(f"  Confiança: {result.confidence:.1f}%")
        print(f"  Risco Geral: {result.risk_assessment['overall_risk']:.1f}/100")
        print(f"  Mercados: {result.metadata['markets_analyzed']}")
        
        return result
    
    async def run_full_analysis(self):
        """Executa análise completa"""
        print("\n" + "=" * 80)
        print("📊 ANÁLISE COMPLETA DE MERCADOS")
        print("=" * 80)
        
        await self.analyze_crypto('BTC/USDT')
        await self.analyze_forex('EUR/USD')
        await self.scan_arbitrage()
        await self.analyze_unified()
        
        print("\n" + "=" * 80)
        print("✅ ANÁLISE COMPLETA CONCLUÍDA")
        print("=" * 80)
    
    def show_autonomous_systems(self):
        """Mostra sistemas autônomos disponíveis"""
        autonomous_manager.print_systems_menu()
    
    def launch_autonomous_system(self, system_id: str):
        """Lança um sistema autônomo"""
        print(f"\n🚀 Lançando sistema autônomo: {system_id}")
        
        system_info = autonomous_manager.get_system_info(system_id)
        if not system_info:
            print(f"❌ Sistema '{system_id}' não encontrado")
            return
        
        if system_info.is_gui:
            print(f"🖥️ Abrindo interface gráfica...")
            autonomous_manager.launch_gui_system(system_id)
        else:
            print(f"⚙️ Sistema não-GUI. Use o menu de status para ver informações.")
    
    async def show_autonomous_status(self):
        """Mostra status dos sistemas autônomos"""
        print("\n" + "=" * 80)
        print("📊 STATUS DOS SISTEMAS AUTÔNOMOS")
        print("=" * 80)
        
        status = await autonomous_manager.get_all_status()
        
        print(f"\n📈 Resumo:")
        print(f"  Total de Sistemas: {status['total_systems']}")
        print(f"  Sistemas Carregados: {status['loaded_systems']}")
        print(f"  Timestamp: {status['timestamp']}")
        
        print(f"\n📋 Detalhes por Sistema:")
        for system_id, system_status in status['systems'].items():
            status_icon = "🟢" if system_status['is_loaded'] else "⚪"
            gui_icon = "🖥️" if system_status['is_gui'] else "⚙️"
            
            print(f"\n  {status_icon} {gui_icon} {system_status['name']}")
            print(f"     Tipo: {system_status['type']}")
            print(f"     Status: {system_status['status']}")
            
            if 'statistics' in system_status:
                print(f"     Estatísticas: {system_status['statistics']}")
        
        print("\n" + "=" * 80)
    
    def print_banner(self):
        """Imprime banner"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        LEXTRADER-IAG 4.0                                     ║
║                                                                              ║
║           Sistema de IA Avançada para Trading e Análise de Mercados         ║
║                                                                              ║
║  🪙 Análise de Criptomoedas  |  💱 Análise de Forex                         ║
║  ⚡ Análise de Arbitragem    |  🌐 Análise Unificada                        ║
║                                                                              ║
║  Versão: {self.version}                                                         ║
║  Status: 🟢 OPERACIONAL                                                      ║
║  Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}                                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


async def main():
    """Função principal"""
    system = LexTraderSimple()
    system.print_banner()
    
    await system.initialize()
    
    while True:
        print("\n" + "=" * 80)
        print("MENU PRINCIPAL")
        print("=" * 80)
        print("1. Analisar Criptomoeda (BTC/USDT)")
        print("2. Analisar Forex (EUR/USD)")
        print("3. Escanear Arbitragem")
        print("4. Análise Unificada")
        print("5. Análise Completa (Todos os Mercados)")
        print("6. Executar Testes")
        print("")
        print("🤖 SISTEMAS AUTÔNOMOS:")
        print("7. Listar Sistemas Autônomos")
        print("8. Status dos Sistemas Autônomos")
        print("9. Lançar Sistema Autônomo (GUI)")
        print("")
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
                print("\n🧪 Executando testes...")
                import subprocess
                result = subprocess.run(['python', 'test_market_analysis.py'], 
                                      capture_output=True, text=True)
                print(result.stdout)
            
            elif choice == '7':
                system.show_autonomous_systems()
            
            elif choice == '8':
                await system.show_autonomous_status()
            
            elif choice == '9':
                system.show_autonomous_systems()
                print("\n" + "=" * 80)
                print("SISTEMAS GUI DISPONÍVEIS:")
                print("=" * 80)
                
                gui_systems = autonomous_manager.list_systems(gui_only=True)
                for i, sys_info in enumerate(gui_systems, 1):
                    sys_id = [k for k, v in autonomous_manager.systems.items() if v == sys_info][0]
                    print(f"{i}. {sys_info.name} (ID: {sys_id})")
                
                print("=" * 80)
                
                try:
                    gui_choice = input("\nEscolha o sistema (número ou ID): ").strip()
                    
                    # Tenta converter para número
                    try:
                        gui_idx = int(gui_choice) - 1
                        if 0 <= gui_idx < len(gui_systems):
                            sys_id = [k for k, v in autonomous_manager.systems.items() 
                                     if v == gui_systems[gui_idx]][0]
                            system.launch_autonomous_system(sys_id)
                        else:
                            print("❌ Número inválido!")
                    except ValueError:
                        # Assume que é um ID
                        system.launch_autonomous_system(gui_choice)
                
                except Exception as e:
                    print(f"❌ Erro ao lançar sistema: {e}")
            
            elif choice == '0':
                print("\n👋 Encerrando LEXTRADER-IAG 4.0...")
                break
            
            else:
                print("❌ Opção inválida!")
        
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando LEXTRADER-IAG 4.0...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"💥 Erro crítico: {e}")
        sys.exit(1)
