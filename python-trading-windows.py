# -*- coding: utf-8 -*-
# LEXTRADER-IAG 4.0 - Sistema de Trading com Aprendizado (Versão Windows)
import asyncio
import sys

# Importações com fallback
try:
    from learningService import TraderComAprendizado
    TRADER_AVAILABLE = True
except ImportError:
    try:
        from quantum_algorithms_trader import QuantumAlgorithmsTrader as TraderComAprendizado
        TRADER_AVAILABLE = True
    except ImportError:
        print("[AVISO] Nenhum trader disponível. Usando modo simulado.")
        TRADER_AVAILABLE = False
        
        # Classe simulada para desenvolvimento
        class TraderComAprendizado:
            """Trader simulado para desenvolvimento"""
            async def initialize(self):
                print("[OK] Trader simulado inicializado")
            
            async def get_market_prediction(self, market_data):
                print("[INFO] Gerando predição simulada...")
                return {"prediction": "HOLD", "confidence": 0.75}
            
            async def execute_trading_cycle(self):
                print("[INFO] Executando ciclo de trading simulado...")
                return {"status": "success", "trades": 0}
            
            async def train_on_historical_data(self, historical_data):
                print("[INFO] Treinamento simulado com dados históricos...")
                return {"status": "trained", "accuracy": 0.85}

async def main():
    print("=" * 70)
    print("LEXTRADER-IAG 4.0 - Sistema de Trading com Aprendizado")
    print("=" * 70)
    
    try:
        # Criar trader
        print("\n[1] Criando trader...")
        trader = TraderComAprendizado(initial_capital=100000.0)
        print(f"[OK] Trader criado com capital inicial: ${trader.capital:,.2f}")
        
        # Inicializar
        print("\n[2] Inicializando sistema...")
        await trader.initialize()
        print("[OK] Sistema inicializado")
        
        # Executar ciclo de trading completo
        print("\n[3] Executando ciclo de trading...")
        await trader.execute_trading_cycle()
        print("[OK] Ciclo de trading concluído")
        
        # Mostrar métricas
        print("\n[4] Métricas de Performance:")
        print(f"   [CAPITAL] Capital Atual: ${trader.capital:,.2f}")
        print(f"   [TRADES] Trades Executados: {trader.total_trades}")
        print(f"   [P&L] P&L Diário: ${trader.daily_pnl:,.2f}")
        print(f"   [SINAIS] Sinais Ativos: {len(trader.trading_signals)}")
        print(f"   [AGENTES] Agentes Ativos: {len(trader.active_agents)}")
        print(f"   [ARBITRAGEM] Oportunidades: {len(trader.arbitrage_opportunities)}")
        
        # Mostrar agentes do enxame
        print("\n[5] Status dos Agentes:")
        for agent in trader.active_agents:
            status_symbol = "[ATIVO]" if agent.status == "ACTIVE" else "[HUNT]" if agent.status == "HUNTING" else "[IDLE]"
            print(f"   {status_symbol} {agent.name} ({agent.type})")
            print(f"      Confiança: {agent.confidence:.2%} | P&L: ${agent.daily_pnl:,.2f} | Trades: {agent.trades_executed}")
        
        # Mostrar histórico de execução
        if trader.execution_history:
            print("\n[6] Últimas Execuções:")
            for i, result in enumerate(trader.execution_history[-5:], 1):
                success_symbol = "[OK]" if result.get('success', False) else "[FAIL]"
                print(f"   {success_symbol} Trade {i}: {result.get('symbol', 'N/A')} - P&L: ${result.get('pnl', 0):,.2f}")
        
        print("\n" + "=" * 70)
        print("[SUCESSO] Sistema de trading executado com sucesso!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[ERRO] Erro durante execução: {e}")
        print("[DICA] Verifique se todos os módulos necessários estão instalados")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Executar sistema de trading
    print("\n[INICIO] Iniciando LEXTRADER-IAG 4.0...")
    asyncio.run(main())
