import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
import asyncio
from enum import Enum
import json

# Simulação dos módulos de IA
class ContinuousLearningService:
    async def learn_from_experience(self, experience: Dict[str, Any]) -> None:
        print(f"🔄 ContinuousLearning: Aprendendo com experiência {experience.get('id', 'N/A')}")
        await asyncio.sleep(0.1)

class SentientCore:
    def add_thought(self, thought: str) -> None:
        print(f"💭 SentientCore: {thought}")

# Inicialização dos serviços de IA
continuous_learner = ContinuousLearningService()
sentient_core = SentientCore()

# Enums e Tipos
class IndicatorType(Enum):
    TREND = "TREND"
    OSCILLATOR = "OSCILLATOR"
    VOLATILITY = "VOLATILITY"
    VOLUME = "VOLUME"

class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"

class BotStatus(Enum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    COMPILING = "COMPILING"

class BuildStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    BUY = "BUY"
    SELL = "SELL"

class MemoryType(Enum):
    EPISODIC = "EPISODIC"
    SEMANTIC = "SEMANTIC"
    PROCEDURAL = "PROCEDURAL"

# Classes de Dados
class CTraderIndicator:
    def __init__(self, id: str, name: str, type: IndicatorType, value: float, signal: Signal, code_snippet: str):
        self.id = id
        self.name = name
        self.type = type
        self.value = value
        self.signal = signal
        self.code_snippet = code_snippet
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'value': self.value,
            'signal': self.signal.value,
            'code_snippet': self.code_snippet
        }

class BotParameter:
    def __init__(self, name: str, param_type: str, value: Any, default_value: Any):
        self.name = name
        self.type = param_type
        self.value = value
        self.default_value = default_value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': self.type,
            'value': self.value,
            'default_value': self.default_value
        }

class CBotInstance:
    def __init__(self, id: str, name: str, language: str, status: BotStatus, win_rate: float, 
                 net_profit: float, code: str, parameters: List[BotParameter], 
                 build_status: BuildStatus, logs: List[str]):
        self.id = id
        self.name = name
        self.language = language
        self.status = status
        self.win_rate = win_rate
        self.net_profit = net_profit
        self.code = code
        self.parameters = parameters
        self.build_status = build_status
        self.logs = logs
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'language': self.language,
            'status': self.status.value,
            'win_rate': self.win_rate,
            'net_profit': self.net_profit,
            'code': self.code,
            'parameters': [p.to_dict() for p in self.parameters],
            'build_status': self.build_status.value,
            'logs': self.logs
        }

class MarketDepthLevel:
    def __init__(self, price: float, volume: float, orders: int, level_type: str):
        self.price = price
        self.volume = volume
        self.orders = orders
        self.type = level_type
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'price': self.price,
            'volume': self.volume,
            'orders': self.orders,
            'type': self.type
        }

class OrderBook:
    def __init__(self, bids: List[Dict], asks: List[Dict], timestamp: int):
        self.bids = bids
        self.asks = asks
        self.timestamp = timestamp

class FuturesPosition:
    def __init__(self, symbol: str, amount: float, entry_price: float, mark_price: float, 
                 pnl: float, roe: float, leverage: float, margin_type: str, 
                 liquidation_price: float):
        self.symbol = symbol
        self.amount = amount
        self.entry_price = entry_price
        self.mark_price = mark_price
        self.pnl = pnl
        self.roe = roe
        self.leverage = leverage
        self.margin_type = margin_type
        self.liquidation_price = liquidation_price
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'symbol': self.symbol,
            'amount': self.amount,
            'entry_price': self.entry_price,
            'mark_price': self.mark_price,
            'pnl': self.pnl,
            'roe': self.roe,
            'leverage': self.leverage,
            'margin_type': self.margin_type,
            'liquidation_price': self.liquidation_price
        }

class CTraderService:
    def __init__(self):
        self.is_connected = False
        self.indicators: List[CTraderIndicator] = []
        self.bots: List[CBotInstance] = []
        self.simulation_task = None
        self.listeners: List[Callable] = []
        self.simulation_active = False
        self.initialize_mock_data()
        
        # Configurações de UI
        self.show_indicators = True
        self.show_market_depth = True
        self.show_bots = True
        self.simulation_speed = 1
    
    def initialize_mock_data(self):
        """Inicializa dados de exemplo para simulação"""
        self.indicators = [
            CTraderIndicator(
                id='ind_1',
                name='Hull Moving Average (HMA)',
                type=IndicatorType.TREND,
                value=1.0850,
                signal=Signal.BUY,
                code_snippet='public override void Calculate(int index) { ... }'
            ),
            CTraderIndicator(
                id='ind_2',
                name='Fisher Transform',
                type=IndicatorType.OSCILLATOR,
                value=2.4,
                signal=Signal.SELL,
                code_snippet='var fisher = (Math.Log((1 + val) / (1 - val)));'
            ),
            CTraderIndicator(
                id='ind_3',
                name='Center of Gravity',
                type=IndicatorType.OSCILLATOR,
                value=0.5,
                signal=Signal.NEUTRAL,
                code_snippet='double num = 0; double den = 0; ...'
            ),
            CTraderIndicator(
                id='ind_4',
                name='Volatility Quality Index',
                type=IndicatorType.VOLATILITY,
                value=45.2,
                signal=Signal.BUY,
                code_snippet='if (vqi > prev_vqi) ...'
            )
        ]
        
        self.bots = [
            CBotInstance(
                id='bot_1',
                name='cBot_Scalper_Pro',
                language='C#',
                status=BotStatus.STOPPED,
                win_rate=68.5,
                net_profit=1420,
                code='''using cAlgo.API;

[Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.None)]
public class ScalperBot : Robot {
    [Parameter("Source")]
    public DataSeries Source { get; set; }
    
    protected override void OnStart() {
        Print("ScalperBot Initialized");
    }
}''',
                parameters=[
                    BotParameter('Take Profit (pips)', 'INT', 10, 10),
                    BotParameter('Stop Loss (pips)', 'INT', 5, 5),
                    BotParameter('Volume', 'DOUBLE', 1.0, 1.0)
                ],
                build_status=BuildStatus.SUCCESS,
                logs=[]
            ),
            CBotInstance(
                id='bot_2',
                name='Neural_Grid_v2',
                language='C#',
                status=BotStatus.RUNNING,
                win_rate=72.1,
                net_profit=856,
                code='''using cAlgo.API;
using System.Linq;

public class NeuralGrid : Robot {
    protected override void OnBar() {
        // Neural logic here
    }
}''',
                parameters=[
                    BotParameter('Grid Step', 'INT', 20, 20),
                    BotParameter('Max Trades', 'INT', 10, 10)
                ],
                build_status=BuildStatus.SUCCESS,
                logs=['[INFO] Grid started', '[INFO] Neural net loaded']
            )
        ]
    
    async def connect(self, api_key: str) -> bool:
        """Conecta ao serviço cTrader"""
        print(f"🔌 cTrader Open API: Iniciando Handshake com chave {api_key[:5]}...")
        await asyncio.sleep(1.5)  # Latência de rede simulada
        self.is_connected = True
        sentient_core.add_thought("Conexão estabelecida com cTrader Open API. Fluxo de dados externo sincronizado.")
        return True
    
    def disconnect(self):
        """Desconecta do serviço cTrader"""
        self.is_connected = False
        self.stop_simulation()
        print("🔴 Desconectado do cTrader API")
    
    def subscribe(self, callback: Callable):
        """Adiciona um listener para eventos"""
        self.listeners.append(callback)
    
    async def compile_algo(self, bot_id: str, code: str) -> Dict[str, Any]:
        """Compila um algoritmo C#"""
        bot = next((b for b in self.bots if b.id == bot_id), None)
        if not bot:
            return {'success': False, 'logs': ['Bot não encontrado']}
        
        bot.status = BotStatus.COMPILING
        self.notify_listeners({'type': 'BOT_UPDATE', 'data': bot.to_dict()})
        
        # Simulação do tempo de compilação
        print(f"🔧 Compilando robô {bot.name}...")
        await asyncio.sleep(2)
        
        # Simulação de sucesso/falha baseada no tamanho do código
        success = len(code) > 50
        
        bot.code = code
        bot.build_status = BuildStatus.SUCCESS if success else BuildStatus.FAILED
        bot.status = BotStatus.STOPPED
        current_time = datetime.now().strftime("%H:%M:%S")
        bot.logs.append(f"[BUILD] {'Build bem-sucedido' if success else 'Build falhou (Erro de Sintaxe)'} às {current_time}")
        
        if success:
            sentient_core.add_thought(f"Código C# do robô {bot.name} compilado com sucesso. Lógica otimizada.")
        else:
            sentient_core.add_thought(f"Falha na compilação do robô {bot.name}. Analisando erros de sintaxe.")
        
        self.notify_listeners({'type': 'BOT_UPDATE', 'data': bot.to_dict()})
        return {'success': success, 'logs': bot.logs}
    
    def toggle_bot(self, bot_id: str):
        """Alterna o estado do bot (RUNNING/STOPPED)"""
        bot = next((b for b in self.bots if b.id == bot_id), None)
        if bot:
            bot.status = BotStatus.RUNNING if bot.status == BotStatus.STOPPED else BotStatus.STOPPED
            current_time = datetime.now().strftime("%H:%M:%S")
            bot.logs.append(f"[SYSTEM] Bot {bot.status.value} às {current_time}")
            self.notify_listeners({'type': 'BOT_UPDATE', 'data': bot.to_dict()})
    
    async def get_market_depth(self, symbol: str) -> List[MarketDepthLevel]:
        """Obtém dados de profundidade de mercado"""
        base_price = 150.00 if 'JPY' in symbol else 1.0850
        spread = 0.01 if 'JPY' in symbol else 0.0001
        
        levels = []
        
        # Asks (Ordens de Venda - Acima do Preço)
        for i in range(9, -1, -1):
            levels.append(MarketDepthLevel(
                price=base_price + (i + 1) * spread,
                volume=random.randint(100000, 600000),
                orders=random.randint(1, 20),
                level_type='ASK'
            ))
        
        # Bids (Ordens de Compra - Abaixo do Preço)
        for i in range(10):
            levels.append(MarketDepthLevel(
                price=base_price - (i + 1) * spread,
                volume=random.randint(100000, 600000),
                orders=random.randint(1, 20),
                level_type='BID'
            ))
        
        return levels
    
    async def get_order_book(self, symbol: str) -> OrderBook:
        """Obtém o livro de ordens"""
        depth = await self.get_market_depth(symbol)
        bids = [{'price': l.price, 'amount': l.volume, 'total': 0} 
                for l in depth if l.type == 'BID']
        asks = [{'price': l.price, 'amount': l.volume, 'total': 0} 
                for l in depth if l.type == 'ASK']
        
        return OrderBook(bids=bids, asks=asks, timestamp=int(time.time() * 1000))
    
    async def get_open_positions(self) -> List[FuturesPosition]:
        """Obtém posições abertas"""
        if not self.is_connected:
            return []
        
        return [
            FuturesPosition(
                symbol='EURUSD',
                amount=100000,
                entry_price=1.0840,
                mark_price=1.0860,
                pnl=200,
                roe=2.5,
                leverage=100,
                margin_type='cross',
                liquidation_price=1.0700
            ),
            FuturesPosition(
                symbol='XAUUSD',
                amount=10,
                entry_price=2350.00,
                mark_price=2345.00,
                pnl=-50,
                roe=-0.5,
                leverage=50,
                margin_type='isolated',
                liquidation_price=2380.00
            )
        ]
    
    async def place_order(self, symbol: str, order_type: OrderType, 
                         volume: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Executa uma ordem"""
        if not self.is_connected:
            raise Exception("cTrader API não conectada")
        
        # Simular latência de execução
        await asyncio.sleep(0.15)
        
        exec_price = price or (1.0850 + (random.random() - 0.5) * 0.0020)
        order_id = f"CT-{int(time.time() * 1000)}"
        
        print(f"[cTrader API] Ordem Executada: {order_type.value} {volume} {symbol} @ {exec_price:.5f}")
        
        # Notificar listeners
        self.notify_listeners({
            'type': 'ORDER_FILLED',
            'data': {
                'id': order_id,
                'symbol': symbol,
                'type': order_type.value,
                'volume': volume,
                'price': exec_price
            }
        })
        
        return {'order_id': order_id, 'price': exec_price}
    
    def get_active_indicators(self) -> List[CTraderIndicator]:
        """Atualiza e retorna indicadores ativos"""
        for indicator in self.indicators:
            indicator.value *= (1 + (random.random() - 0.5) * 0.01)
            if random.random() > 0.6:
                indicator.signal = Signal.BUY if random.random() > 0.5 else Signal.SELL
            else:
                indicator.signal = Signal.NEUTRAL
        return self.indicators
    
    async def simulation_loop(self, speed: float = 1):
        """Loop principal da simulação"""
        print(f"🚀 Iniciando Simulador cTrader (Velocidade {speed}x)...")
        sentient_core.add_thought("Modo de Treinamento Acelerado: Ingerindo dados históricos do cTrader.")
        
        base_interval = 1.0 / speed
        
        while self.simulation_active:
            start_time = time.time()
            
            # 1. Gerar Dados de Mercado do Simulador
            mock_state = {
                'price': 1.0845 + (random.random() - 0.5) * 0.005,
                'rsi': 30 + random.random() * 40,
                'macd': (random.random() - 0.5) * 0.002,
                'volatility': random.random() * 0.05,
                'cTraderIndicators': [ind.to_dict() for ind in self.get_active_indicators()]
            }
            
            # 2. Enviar para a IA (Continuous Learning)
            action = 'SELL' if mock_state['price'] > 1.0850 else 'BUY'
            reward = 1.0 if random.random() > 0.4 else -0.5
            
            experience = {
                'id': f'CTRADER-SIM-{int(time.time() * 1000)}',
                'timestamp': int(time.time() * 1000),
                'state': mock_state,
                'action': action,
                'reward': reward,
                'nextState': {},
                'quantumMetrics': {},
                'confidence': 0.8 + (random.random() * 0.2),
                'memoryType': MemoryType.EPISODIC.value,
                'importance': 0.6
            }
            
            await continuous_learner.learn_from_experience(experience)
            
            # 3. Notificar UI
            self.notify_listeners({
                'type': 'SIMULATION_TICK',
                'data': mock_state,
                'pnl': reward * 100
            })
            
            # Controlar velocidade da simulação
            elapsed = time.time() - start_time
            sleep_time = max(0, base_interval - elapsed)
            await asyncio.sleep(sleep_time)
    
    def start_simulation(self, speed: float = 1):
        """Inicia a simulação"""
        if self.simulation_active:
            return
        
        self.simulation_speed = speed
        self.simulation_active = True
        self.simulation_task = asyncio.create_task(self.simulation_loop(speed))
    
    def stop_simulation(self):
        """Para a simulação"""
        self.simulation_active = False
        if self.simulation_task:
            self.simulation_task.cancel()
            self.simulation_task = None
        print("⏸️ Simulador cTrader Pausado.")
    
    def notify_listeners(self, event: Dict[str, Any]):
        """Notifica todos os listeners registrados"""
        for callback in self.listeners:
            try:
                callback(event)
            except Exception as e:
                print(f"Erro ao notificar listener: {e}")
    
    def get_bot_summary(self) -> str:
        """Retorna um resumo dos bots em execução"""
        running_bots = [b for b in self.bots if b.status == BotStatus.RUNNING]
        if not running_bots:
            return "Nenhum bot em execução"
        
        summary = "🤖 Bots Ativos:\n"
        for bot in running_bots:
            summary += f"  • {bot.name}: Win Rate {bot.win_rate}%, P&L ${bot.net_profit}\n"
        return summary
    
    def get_market_summary(self) -> str:
        """Retorna um resumo do mercado"""
        indicators = self.get_active_indicators()
        buy_signals = sum(1 for i in indicators if i.signal == Signal.BUY)
        sell_signals = sum(1 for i in indicators if i.signal == Signal.SELL)
        
        return (f"📊 Resumo do Mercado:\n"
                f"  • Sinais de COMPRA: {buy_signals}\n"
                f"  • Sinais de VENDA: {sell_signals}\n"
                f"  • Conectado: {'✅ Sim' if self.is_connected else '❌ Não'}\n"
                f"  • Simulação: {'✅ Ativa' if self.simulation_active else '⏸️ Pausada'}")
    
    async def export_bot_config(self, bot_id: str, filepath: str):
        """Exporta configuração do bot para JSON"""
        bot = next((b for b in self.bots if b.id == bot_id), None)
        if bot:
            config = bot.to_dict()
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Configuração exportada para {filepath}")
    
    def update_bot_parameter(self, bot_id: str, param_name: str, value: Any):
        """Atualiza parâmetro de um bot"""
        bot = next((b for b in self.bots if b.id == bot_id), None)
        if bot:
            for param in bot.parameters:
                if param.name == param_name:
                    param.value = value
                    bot.logs.append(f"[PARAM] {param_name} atualizado para {value}")
                    self.notify_listeners({'type': 'BOT_UPDATE', 'data': bot.to_dict()})
                    break

# Instância global do serviço
ctrader_service = CTraderService()


# Interface de Interação Melhorada
class CTraderCLI:
    """Interface de linha de comando para interação com o cTrader"""
    
    def __init__(self, service: CTraderService):
        self.service = service
        self.running = True
    
    async def run(self):
        """Executa a interface principal"""
        print("=" * 60)
        print("🤖 cTrader AI Service - Python Edition")
        print("=" * 60)
        
        while self.running:
            print("\n" + "=" * 40)
            print("MENU PRINCIPAL")
            print("=" * 40)
            print("1. 🔌 Conectar ao cTrader")
            print("2. 📊 Ver Indicadores")
            print("3. 🤖 Gerenciar Bots")
            print("4. 📈 Ver Profundidade de Mercado")
            print("5. 💰 Ver Posições Abertas")
            print("6. 🚀 Iniciar Simulação")
            print("7. ⏸️ Parar Simulação")
            print("8. 📋 Resumo do Sistema")
            print("9. 📤 Executar Ordem")
            print("0. ❌ Sair")
            print("=" * 40)
            
            choice = input("\nEscolha uma opção: ").strip()
            
            try:
                if choice == "1":
                    await self.connect_service()
                elif choice == "2":
                    self.show_indicators()
                elif choice == "3":
                    await self.manage_bots()
                elif choice == "4":
                    await self.show_market_depth()
                elif choice == "5":
                    await self.show_positions()
                elif choice == "6":
                    self.start_simulation()
                elif choice == "7":
                    self.stop_simulation()
                elif choice == "8":
                    self.show_summary()
                elif choice == "9":
                    await self.place_order_interactive()
                elif choice == "0":
                    self.running = False
                    self.service.disconnect()
                    print("\n👋 Até logo!")
                else:
                    print("❌ Opção inválida!")
            
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    async def connect_service(self):
        """Interface de conexão"""
        api_key = input("Digite sua API Key (ou pressione Enter para simular): ").strip()
        if not api_key:
            api_key = "sim-1234567890"
        
        print("\n🔌 Conectando ao cTrader...")
        success = await self.service.connect(api_key)
        if success:
            print("✅ Conectado com sucesso!")
        else:
            print("❌ Falha na conexão")
    
    def show_indicators(self):
        """Mostra indicadores ativos"""
        indicators = self.service.get_active_indicators()
        print("\n" + "=" * 40)
        print("📈 INDICADORES ATIVOS")
        print("=" * 40)
        
        for indicator in indicators:
            signal_emoji = "🟢" if indicator.signal == Signal.BUY else "🔴" if indicator.signal == Signal.SELL else "⚪"
            print(f"\n{signal_emoji} {indicator.name}")
            print(f"   Tipo: {indicator.type.value}")
            print(f"   Valor: {indicator.value:.4f}")
            print(f"   Sinal: {indicator.signal.value}")
            print(f"   Snippet: {indicator.code_snippet[:50]}...")
    
    async def manage_bots(self):
        """Interface de gerenciamento de bots"""
        print("\n" + "=" * 40)
        print("🤖 GERENCIAR BOTS")
        print("=" * 40)
        
        for i, bot in enumerate(self.service.bots, 1):
            status_emoji = "🟢" if bot.status == BotStatus.RUNNING else "🔴"
            print(f"{i}. {status_emoji} {bot.name}")
            print(f"   Status: {bot.status.value}")
            print(f"   Win Rate: {bot.win_rate}%")
            print(f"   P&L: ${bot.net_profit}")
        
        choice = input("\nSelecione um bot (número) ou 'c' para compilar: ").strip()
        
        if choice.lower() == 'c':
            await self.compile_bot()
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.service.bots):
                await self.bot_details(self.service.bots[idx])
    
    async def compile_bot(self):
        """Interface para compilar bot"""
        bot_id = input("ID do bot para compilar: ").strip()
        code = input("Código C# (digite 'default' para usar padrão): ").strip()
        
        if code.lower() == 'default':
            bot = next((b for b in self.service.bots if b.id == bot_id), None)
            if bot:
                code = bot.code
        
        print("\n🔧 Compilando...")
        result = await self.service.compile_algo(bot_id, code)
        
        if result['success']:
            print("✅ Compilação bem-sucedida!")
        else:
            print("❌ Falha na compilação")
        
        print("Logs:", "\n".join(result['logs'][-3:]))  # Mostra últimos 3 logs
    
    async def bot_details(self, bot: CBotInstance):
        """Mostra detalhes de um bot específico"""
        print(f"\n🔍 DETALHES: {bot.name}")
        print(f"ID: {bot.id}")
        print(f"Linguagem: {bot.language}")
        print(f"Status: {bot.status.value}")
        print(f"Build: {bot.build_status.value}")
        
        print("\n📋 Parâmetros:")
        for param in bot.parameters:
            print(f"  • {param.name}: {param.value} ({param.type})")
        
        print("\n📝 Logs Recentes:")
        for log in bot.logs[-5:]:  # Últimos 5 logs
            print(f"  {log}")
        
        action = input("\n[1] Alternar ON/OFF [2] Atualizar Parâmetro [3] Voltar: ").strip()
        
        if action == "1":
            self.service.toggle_bot(bot.id)
            print(f"✅ Bot {bot.name} alternado!")
        elif action == "2":
            param_name = input("Nome do parâmetro: ").strip()
            value = input("Novo valor: ").strip()
            # Tentar converter para o tipo apropriado
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                self.service.update_bot_parameter(bot.id, param_name, value)
                print("✅ Parâmetro atualizado!")
            except ValueError:
                print("❌ Valor inválido!")
    
    async def show_market_depth(self):
        """Mostra profundidade de mercado"""
        symbol = input("Símbolo (ex: EURUSD): ").strip() or "EURUSD"
        
        print(f"\n📊 PROFUNDIDADE DE MERCADO: {symbol}")
        depth = await self.service.get_market_depth(symbol)
        
        print("\n🔴 ASKS (Venda):")
        for level in sorted([l for l in depth if l.type == 'ASK'], key=lambda x: x.price)[:5]:
            print(f"  {level.price:.5f} | Vol: {level.volume:,.0f} | Ordens: {level.orders}")
        
        print("\n🟢 BIDS (Compra):")
        for level in sorted([l for l in depth if l.type == 'BID'], key=lambda x: x.price, reverse=True)[:5]:
            print(f"  {level.price:.5f} | Vol: {level.volume:,.0f} | Ordens: {level.orders}")
    
    async def show_positions(self):
        """Mostra posições abertas"""
        positions = await self.service.get_open_positions()
        
        if not positions:
            print("\n📭 Nenhuma posição aberta")
            return
        
        print("\n" + "=" * 40)
        print("💰 POSIÇÕES ABERTAS")
        print("=" * 40)
        
        total_pnl = 0
        for pos in positions:
            pnl_emoji = "🟢" if pos.pnl >= 0 else "🔴"
            print(f"\n{pnl_emoji} {pos.symbol}")
            print(f"  Quantidade: {pos.amount:,.2f}")
            print(f"  Entrada: {pos.entry_price:.4f}")
            print(f"  Atual: {pos.mark_price:.4f}")
            print(f"  P&L: ${pos.pnl:,.2f} ({pos.roe:.2f}%)")
            print(f"  Alavancagem: {pos.leverage}x")
            total_pnl += pos.pnl
        
        print(f"\n📊 P&L Total: ${total_pnl:,.2f}")
    
    def start_simulation(self):
        """Inicia simulação"""
        try:
            speed = float(input("Velocidade (1 = tempo real, 10 = 10x mais rápido): ") or "1")
            self.service.start_simulation(speed)
            print(f"🚀 Simulação iniciada a {speed}x")
        except ValueError:
            print("❌ Velocidade inválida!")
    
    def stop_simulation(self):
        """Para simulação"""
        self.service.stop_simulation()
        print("⏸️ Simulação parada")
    
    def show_summary(self):
        """Mostra resumo do sistema"""
        print("\n" + "=" * 40)
        print("📋 RESUMO DO SISTEMA")
        print("=" * 40)
        
        print("\n" + self.service.get_market_summary())
        print("\n" + self.service.get_bot_summary())
        
        # Contadores
        print(f"\n📊 Estatísticas:")
        print(f"  • Indicadores: {len(self.service.indicators)}")
        print(f"  • Bots: {len(self.service.bots)}")
        print(f"  • Listeners: {len(self.service.listeners)}")
    
    async def place_order_interactive(self):
        """Interface para executar ordens"""
        if not self.service.is_connected:
            print("❌ Conecte-se primeiro ao cTrader!")
            return
        
        print("\n" + "=" * 40)
        print("📤 EXECUTAR ORDEM")
        print("=" * 40)
        
        symbol = input("Símbolo (ex: EURUSD): ").strip() or "EURUSD"
        order_type = input("Tipo [BUY/SELL/market/limit]: ").strip().upper()
        volume = float(input("Volume (ex: 100000): ").strip() or "100000")
        
        price = None
        if order_type == "LIMIT":
            price = float(input("Preço limite: ").strip())
        
        try:
            order_type_enum = OrderType(order_type.lower())
            result = await self.service.place_order(symbol, order_type_enum, volume, price)
            print(f"\n✅ Ordem executada!")
            print(f"   ID: {result['order_id']}")
            print(f"   Preço: {result['price']:.5f}")
        except ValueError:
            print("❌ Tipo de ordem inválido!")
        except Exception as e:
            print(f"❌ Erro: {e}")


# Função para adicionar listener de exemplo
def example_listener(event: Dict[str, Any]):
    """Exemplo de listener para eventos"""
    event_type = event.get('type', 'UNKNOWN')
    
    if event_type == 'ORDER_FILLED':
        data = event.get('data', {})
        print(f"\n🎯 EVENTO: Ordem Executada - {data.get('symbol')} "
              f"{data.get('type')} @ {data.get('price'):.5f}")
    
    elif event_type == 'SIMULATION_TICK':
        pnl = event.get('pnl', 0)
        color = "🟢" if pnl >= 0 else "🔴"
        print(f"{color} Simulação Tick | P&L: ${pnl:+.2f}", end='\r')


# Função principal
async def main():
    """Função principal"""
    # Adicionar listener de exemplo
    ctrader_service.subscribe(example_listener)
    
    # Iniciar CLI
    cli = CTraderCLI(ctrader_service)
    await cli.run()

# Executar se este arquivo for o principal
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário")
        ctrader_service.disconnect()