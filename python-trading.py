# -*- coding: utf-8 -*-
# LEXTRADER-IAG 4.0 - Sistema de Trading com Aprendizado - LEXTRADER-IAG 4.0
import asyncio
import sys
import io

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Importações com fallback
try:
    from learningService import TraderComAprendizado
    TRADER_AVAILABLE = True
except ImportError:
    try:
        from quantum_algorithms_trader import QuantumAlgorithmsTrader as TraderComAprendizado
        TRADER_AVAILABLE = True
    except ImportError:
        print("⚠️  Nenhum trader disponível. Usando modo simulado.")
        TRADER_AVAILABLE = False
        
        # Classe simulada para desenvolvimento
        class TraderComAprendizado:
            """Trader simulado para desenvolvimento"""
            async def initialize(self):
                print("✅ Trader simulado inicializado")
            
            async def get_market_prediction(self, market_data):
                print("📊 Gerando predição simulada...")
                return {"prediction": "HOLD", "confidence": 0.75}
            
            async def execute_trading_cycle(self):
                print("🔄 Executando ciclo de trading simulado...")
                return {"status": "success", "trades": 0}
            
            async def train_on_historical_data(self, historical_data):
                print("📚 Treinamento simulado com dados históricos...")
                return {"status": "trained", "accuracy": 0.85}

async def main():
    print("=" * 70)
    print("🚀 LEXTRADER-IAG 4.0 - Sistema de Trading com Aprendizado")
    print("=" * 70)
    
    try:
        # Criar trader
        print("\n1️⃣ Criando trader...")
        trader = TraderComAprendizado(initial_capital=100000.0)
        print(f"✅ Trader criado com capital inicial: ${trader.capital:,.2f}")
        
        # Inicializar
        print("\n2️⃣ Inicializando sistema...")
        await trader.initialize()
        print("✅ Sistema inicializado")
        
        # Executar ciclo de trading completo
        print("\n3️⃣ Executando ciclo de trading...")
        await trader.execute_trading_cycle()
        print("✅ Ciclo de trading concluído")
        
        # Mostrar métricas
        print("\n4️⃣ Métricas de Performance:")
        print(f"   💰 Capital Atual: ${trader.capital:,.2f}")
        print(f"   📊 Trades Executados: {trader.total_trades}")
        print(f"   📈 P&L Diário: ${trader.daily_pnl:,.2f}")
        print(f"   🎯 Sinais Ativos: {len(trader.trading_signals)}")
        print(f"   🤖 Agentes Ativos: {len(trader.active_agents)}")
        print(f"   💎 Oportunidades de Arbitragem: {len(trader.arbitrage_opportunities)}")
        
        # Mostrar agentes do enxame
        print("\n5️⃣ Status dos Agentes:")
        for agent in trader.active_agents:
            status_emoji = "🟢" if agent.status == "ACTIVE" else "🟡" if agent.status == "HUNTING" else "⚪"
            print(f"   {status_emoji} {agent.name} ({agent.type})")
            print(f"      Confiança: {agent.confidence:.2%} | P&L: ${agent.daily_pnl:,.2f} | Trades: {agent.trades_executed}")
        
        # Mostrar histórico de execução
        if trader.execution_history:
            print("\n6️⃣ Últimas Execuções:")
            for i, result in enumerate(trader.execution_history[-5:], 1):
                success_emoji = "✅" if result.get('success', False) else "❌"
                print(f"   {success_emoji} Trade {i}: {result.get('symbol', 'N/A')} - P&L: ${result.get('pnl', 0):,.2f}")
        
        print("\n" + "=" * 70)
        print("✅ Sistema de trading executado com sucesso!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("💡 Dica: Verifique se todos os módulos necessários estão instalados")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Executar sistema de trading
    print("\n🔧 Iniciando LEXTRADER-IAG 4.0...")
    asyncio.run(main())