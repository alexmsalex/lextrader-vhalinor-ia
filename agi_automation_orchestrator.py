"""
AGI Automation Orchestrator - Integrador Principal
==================================================
Sistema de orquestração e inicialização da automação completa.
Coordena todos os componentes para operação automática 24/7.

Autor: AGI Trading System
Versão: 2.0.0
"""

import sys
import os
import threading
import time
import json
import signal
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import traceback

# Configurar paths do projeto de forma robusta
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PATHS = [
    _PROJECT_ROOT / '01_sensorial',
    _PROJECT_ROOT / '02_processamento', 
    _PROJECT_ROOT / '03_memoria_saida',
    _PROJECT_ROOT / '04_decisao',
    _PROJECT_ROOT / 'utils',
    _PROJECT_ROOT
]

for path in _PATHS:
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Configurar logging
try:
    from loguru import logger
    logger.remove()  # Remove handler padrão
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    logger.add(
        "logs/agi_orchestrator_{time:YYYY-MM-DD}.log",
        rotation="500 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )
except ImportError:
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'agi_orchestrator_{datetime.now():%Y%m%d}.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)


# Enums e Data Classes
class AutomationState(Enum):
    """Estados do sistema de automação"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    ERROR = "error"


class AnalysisFrequency(Enum):
    """Frequência de análise"""
    LOW = "low"      # 15 minutos
    NORMAL = "normal"   # 5 minutos
    HIGH = "high"    # 1 minuto
    REAL_TIME = "realtime"  # Em tempo real


@dataclass
class AutomationConfig:
    """Configuração do sistema de automação"""
    analysis_frequency: AnalysisFrequency = AnalysisFrequency.NORMAL
    max_concurrent_trades: int = 5
    max_daily_trades: int = 50
    risk_per_trade: float = 0.02  # 2% por trade
    max_daily_risk: float = 0.05  # 5% diário
    enable_live_trading: bool = False
    enable_paper_trading: bool = True
    symbols: List[str] = None
    initial_capital: float = 100000.0
    notify_on_errors: bool = True
    auto_restart: bool = True
    max_restart_attempts: int = 3
    heartbeat_interval: int = 60  # segundos
    
    def __post_init__(self):
        if self.symbols is None:
            self.symbols = ['EURUSD', 'GBPUSD', 'AUDUSD', 'BTC', 'ETH', 'BNB', 'ADA', 'SOL']
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AutomationConfig':
        if 'analysis_frequency' in data and isinstance(data['analysis_frequency'], str):
            data['analysis_frequency'] = AnalysisFrequency(data['analysis_frequency'])
        return cls(**data)


@dataclass
class SystemMetrics:
    """Métricas do sistema"""
    timestamp: datetime
    total_analyses: int = 0
    total_decisions: int = 0
    successful_trades: int = 0
    failed_trades: int = 0
    active_positions: int = 0
    total_pnl: float = 0.0
    daily_pnl: float = 0.0
    win_rate: float = 0.0
    system_uptime: float = 0.0  # em segundos
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result


class AGIOrchestrator:
    """
    Orquestrador de automação que integra e coordena todos os componentes.
    
    Responsabilidades:
    1. Inicialização e shutdown de componentes
    2. Comunicação entre módulos
    3. Monitoramento de saúde do sistema
    4. Gerenciamento de exceções
    5. Logging e relatórios
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa o orquestrador AGI.
        
        Args:
            config_path: Caminho para arquivo de configuração JSON
        """
        self.state = AutomationState.STOPPED
        self.start_time = None
        self.restart_count = 0
        self.heartbeat_thread = None
        self.monitor_thread = None
        self.stop_event = threading.Event()
        self.components_ready = threading.Event()
        
        # Carregar configuração
        self.config = self._load_config(config_path)
        
        # Inicializar componentes (lazy loading)
        self.automation_engine = None
        self.market_monitor = None
        self.portfolio_manager = None
        self.risk_manager = None
        
        # Callbacks registrados
        self.callbacks: Dict[str, List[Callable]] = {
            'on_analysis_complete': [],
            'on_decision_made': [],
            'on_trade_executed': [],
            'on_market_opportunity': [],
            'on_position_opened': [],
            'on_position_closed': [],
            'on_error': [],
            'on_state_change': [],
            'on_heartbeat': []
        }
        
        # Métricas
        self.metrics = SystemMetrics(timestamp=datetime.now())
        
        # Configurar handlers de sinal
        self._setup_signal_handlers()
        
        logger.info("AGI Orchestrator inicializado")
        logger.info(f"Configuração: {self.config}")
        
    def _load_config(self, config_path: Optional[str]) -> AutomationConfig:
        """Carrega configuração de arquivo ou usa padrão."""
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                config = AutomationConfig.from_dict(data)
                logger.info(f"Configuração carregada de {config_path}")
                return config
            except Exception as e:
                logger.error(f"Erro ao carregar configuração: {e}. Usando padrão.")
        
        # Configuração padrão
        return AutomationConfig()
    
    def _setup_signal_handlers(self):
        """Configura handlers para sinais do sistema."""
        def signal_handler(signum, frame):
            logger.warning(f"Sinal {signum} recebido. Desligando graciosamente...")
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
    def register_callback(self, event: str, callback: Callable):
        """Registra um callback para um evento específico.
        
        Args:
            event: Nome do evento
            callback: Função a ser chamada quando o evento ocorrer
        """
        if event in self.callbacks:
            self.callbacks[event].append(callback)
            logger.debug(f"Callback registrado para evento: {event}")
        else:
            logger.warning(f"Evento desconhecido: {event}")
    
    def _trigger_callback(self, event: str, data: Dict = None):
        """Dispara todos os callbacks registrados para um evento.
        
        Args:
            event: Nome do evento
            data: Dados a serem passados para os callbacks
        """
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                try:
                    if data is not None:
                        callback(data)
                    else:
                        callback()
                except Exception as e:
                    logger.error(f"Erro no callback {event}: {e}")
    
    def _initialize_components(self):
        """Inicializa todos os componentes do sistema."""
        try:
            logger.info("Inicializando componentes...")
            
            # Importar componentes dinamicamente
            from market_monitor import MarketMonitor
            from portfolio_manager import PortfolioManager
            from agi_automation_engine import AGIAutomationEngine
            from risk_manager import RiskManager
            
            # Inicializar componentes
            self.market_monitor = MarketMonitor(
                symbols=self.config.symbols,
                update_frequency=self._get_update_frequency(),
                callback=self._on_market_data
            )
            
            self.portfolio_manager = PortfolioManager(
                initial_capital=self.config.initial_capital,
                max_positions=self.config.max_concurrent_trades
            )
            
            self.automation_engine = AGIAutomationEngine(
                config=self.config,
                market_monitor=self.market_monitor,
                portfolio_manager=self.portfolio_manager
            )
            
            self.risk_manager = RiskManager(
                max_risk_per_trade=self.config.risk_per_trade,
                max_daily_risk=self.config.max_daily_risk
            )
            
            # Configurar dependências
            self.automation_engine.set_risk_manager(self.risk_manager)
            
            # Registrar callbacks internos
            self._register_internal_callbacks()
            
            self.components_ready.set()
            logger.success("✅ Todos os componentes inicializados")
            
        except ImportError as e:
            logger.error(f"Erro ao importar componentes: {e}")
            logger.warning("Usando componentes mock para demonstração...")
            self._initialize_mock_components()
        except Exception as e:
            logger.error(f"Erro na inicialização de componentes: {e}")
            raise
    
    def _initialize_mock_components(self):
        """Inicializa componentes mock para demonstração."""
        logger.warning("🔶 MODO DEMONSTRAÇÃO ATIVADO - Usando componentes mock")
        
        from .mock_components import (
            MockMarketMonitor, MockPortfolioManager, 
            MockAutomationEngine, MockRiskManager
        )
        
        self.market_monitor = MockMarketMonitor(
            symbols=self.config.symbols,
            update_frequency=self._get_update_frequency()
        )
        
        self.portfolio_manager = MockPortfolioManager(
            initial_capital=self.config.initial_capital
        )
        
        self.automation_engine = MockAutomationEngine(
            config=self.config
        )
        
        self.risk_manager = MockRiskManager(
            max_risk_per_trade=self.config.risk_per_trade
        )
        
        self._register_internal_callbacks()
        self.components_ready.set()
    
    def _get_update_frequency(self) -> int:
        """Retorna frequência de atualização em segundos."""
        freq_map = {
            AnalysisFrequency.LOW: 900,      # 15 minutos
            AnalysisFrequency.NORMAL: 300,    # 5 minutos
            AnalysisFrequency.HIGH: 60,       # 1 minuto
            AnalysisFrequency.REAL_TIME: 1    # 1 segundo
        }
        return freq_map.get(self.config.analysis_frequency, 300)
    
    def _register_internal_callbacks(self):
        """Registra callbacks internos entre componentes."""
        
        # Market Monitor -> Automation Engine
        self.market_monitor.register_callback(
            'on_opportunity',
            lambda data: self.automation_engine.on_market_opportunity(data)
        )
        
        # Automation Engine -> Portfolio Manager
        self.automation_engine.register_callback(
            'on_trade_executed',
            lambda data: self.portfolio_manager.update_position(data)
        )
        
        # Portfolio Manager -> Risk Manager
        self.portfolio_manager.register_callback(
            'on_position_update',
            lambda data: self.risk_manager.update_exposure(data)
        )
        
        # Registrar callbacks do orquestrador
        self.automation_engine.register_callback(
            'on_analysis_complete',
            self._on_analysis_complete
        )
        
        self.automation_engine.register_callback(
            'on_decision_made',
            self._on_decision_made
        )
        
        self.automation_engine.register_callback(
            'on_trade_executed',
            self._on_trade_executed
        )
        
        self.market_monitor.register_callback(
            'on_opportunity',
            self._on_market_opportunity
        )
        
        self.portfolio_manager.register_callback(
            'on_position_opened',
            self._on_position_opened
        )
        
        self.portfolio_manager.register_callback(
            'on_position_closed',
            self._on_position_closed
        )
    
    def start(self):
        """Inicia a automação completa."""
        if self.state != AutomationState.STOPPED:
            logger.warning(f"Sistema já está {self.state.value}. Use restart() para reiniciar.")
            return
        
        try:
            self.state = AutomationState.STARTING
            self.start_time = datetime.now()
            self._trigger_callback('on_state_change', {'state': self.state.value})
            
            logger.info("🚀 Iniciando AGI Orchestrator...")
            self._show_startup_banner()
            
            # Inicializar componentes
            self._initialize_components()
            
            # Aguardar componentes estarem prontos
            if not self.components_ready.wait(timeout=30):
                raise TimeoutError("Timeout na inicialização dos componentes")
            
            # Iniciar componentes
            self.market_monitor.start()
            self.portfolio_manager.start()
            self.automation_engine.start()
            
            # Atualizar estado
            self.state = AutomationState.RUNNING
            self._trigger_callback('on_state_change', {'state': self.state.value})
            
            # Iniciar threads de monitoramento
            self._start_monitor_threads()
            
            logger.success("✅ AGI Orchestrator iniciado com sucesso")
            logger.info("🤖 Sistema operando automaticamente 24/7")
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar sistema: {e}")
            self.state = AutomationState.ERROR
            self._trigger_callback('on_state_change', {'state': self.state.value})
            self._trigger_callback('on_error', {'error': str(e), 'context': 'startup'})
            
            # Tentar auto-restart se configurado
            if self.config.auto_restart and self.restart_count < self.config.max_restart_attempts:
                logger.info(f"Tentando auto-restart ({self.restart_count + 1}/{self.config.max_restart_attempts})...")
                time.sleep(5)
                self.restart()
    
    def stop(self):
        """Para a automação completa graciosamente."""
        if self.state in [AutomationState.STOPPED, AutomationState.STOPPING]:
            return
        
        logger.info("⏹️ Parando AGI Orchestrator...")
        self.state = AutomationState.STOPPING
        self._trigger_callback('on_state_change', {'state': self.state.value})
        
        # Sinalizar para threads pararem
        self.stop_event.set()
        
        try:
            # Parar componentes em ordem reversa
            if self.automation_engine:
                self.automation_engine.stop()
            
            if self.market_monitor:
                self.market_monitor.stop()
            
            if self.portfolio_manager:
                self.portfolio_manager.stop()
            
            # Aguardar threads terminarem
            if self.heartbeat_thread and self.heartbeat_thread.is_alive():
                self.heartbeat_thread.join(timeout=5)
            
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=5)
            
            # Salvar estado
            self._save_state()
            
            # Atualizar métricas finais
            self._update_metrics()
            
            self.state = AutomationState.STOPPED
            self._trigger_callback('on_state_change', {'state': self.state.value})
            
            logger.success("✅ AGI Orchestrator parado graciosamente")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema: {e}")
            self.state = AutomationState.ERROR
            self._trigger_callback('on_state_change', {'state': self.state.value})
    
    def restart(self):
        """Reinicia o sistema."""
        logger.info("🔄 Reiniciando sistema...")
        self.restart_count += 1
        
        try:
            self.stop()
            time.sleep(2)  # Pequena pausa
            self.start()
            
        except Exception as e:
            logger.error(f"Erro no restart: {e}")
    
    def pause(self):
        """Pausa a automação."""
        if self.state == AutomationState.RUNNING:
            logger.info("⏸️ Pausando automação...")
            self.state = AutomationState.PAUSED
            self._trigger_callback('on_state_change', {'state': self.state.value})
            
            if self.automation_engine:
                self.automation_engine.pause()
    
    def resume(self):
        """Retoma a automação pausada."""
        if self.state == AutomationState.PAUSED:
            logger.info("▶️ Retomando automação...")
            self.state = AutomationState.RUNNING
            self._trigger_callback('on_state_change', {'state': self.state.value})
            
            if self.automation_engine:
                self.automation_engine.resume()
    
    def _start_monitor_threads(self):
        """Inicia threads de monitoramento."""
        # Thread de heartbeat
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            name="HeartbeatThread",
            daemon=True
        )
        self.heartbeat_thread.start()
        
        # Thread de monitoramento de métricas
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            name="MonitorThread",
            daemon=True
        )
        self.monitor_thread.start()
    
    def _heartbeat_loop(self):
        """Loop de heartbeat para monitorar saúde do sistema."""
        logger.info("💓 Thread de heartbeat iniciada")
        
        while not self.stop_event.is_set() and self.state == AutomationState.RUNNING:
            try:
                # Verificar saúde dos componentes
                components_healthy = True
                
                if self.automation_engine:
                    components_healthy &= self.automation_engine.is_alive()
                
                if self.market_monitor:
                    components_healthy &= self.market_monitor.is_alive()
                
                if self.portfolio_manager:
                    components_healthy &= self.portfolio_manager.is_alive()
                
                # Trigger heartbeat callback
                heartbeat_data = {
                    'timestamp': datetime.now().isoformat(),
                    'components_healthy': components_healthy,
                    'system_state': self.state.value,
                    'uptime': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
                }
                
                self._trigger_callback('on_heartbeat', heartbeat_data)
                
                # Log se algum componente não está saudável
                if not components_healthy:
                    logger.warning("⚠️ Componente não saudável detectado")
                
                # Aguardar próximo heartbeat
                time.sleep(self.config.heartbeat_interval)
                
            except Exception as e:
                logger.error(f"Erro no heartbeat: {e}")
                time.sleep(self.config.heartbeat_interval)
        
        logger.info("💓 Thread de heartbeat encerrada")
    
    def _monitor_loop(self):
        """Loop principal de monitoramento."""
        logger.info("📊 Thread de monitoramento iniciada")
        
        while not self.stop_event.is_set() and self.state == AutomationState.RUNNING:
            try:
                # Atualizar métricas a cada 30 segundos
                time.sleep(30)
                
                if self.state != AutomationState.RUNNING:
                    continue
                
                # Coletar métricas
                self._update_metrics()
                
                # Log status
                status = self.get_status()
                
                logger.info(
                    f"📈 Status: "
                    f"Análises={status['metrics']['total_analyses']}, "
                    f"Decisões={status['metrics']['total_decisions']}, "
                    f"Trades={status['metrics']['successful_trades']}/"
                    f"{status['metrics']['failed_trades']}, "
                    f"Posições={status['metrics']['active_positions']}, "
                    f"P&L=${status['metrics']['total_pnl']:.2f}, "
                    f"Win Rate={status['metrics']['win_rate']:.1%}"
                )
                
            except KeyboardInterrupt:
                logger.info("Interrupção detectada no monitoramento")
                break
            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")
                time.sleep(30)  # Continuar mesmo com erro
        
        logger.info("📊 Thread de monitoramento encerrada")
    
    def _update_metrics(self):
        """Atualiza as métricas do sistema."""
        try:
            # Coletar métricas dos componentes
            if self.automation_engine:
                engine_stats = self.automation_engine.get_stats()
                self.metrics.total_analyses = engine_stats.get('total_analyses', 0)
                self.metrics.total_decisions = engine_stats.get('total_decisions', 0)
                self.metrics.successful_trades = engine_stats.get('successful_trades', 0)
                self.metrics.failed_trades = engine_stats.get('failed_trades', 0)
            
            if self.portfolio_manager:
                portfolio_metrics = self.portfolio_manager.get_metrics()
                self.metrics.active_positions = portfolio_metrics.get('active_positions', 0)
                self.metrics.total_pnl = portfolio_metrics.get('total_pnl', 0.0)
                self.metrics.daily_pnl = portfolio_metrics.get('daily_pnl', 0.0)
            
            # Calcular win rate
            total_trades = self.metrics.successful_trades + self.metrics.failed_trades
            if total_trades > 0:
                self.metrics.win_rate = self.metrics.successful_trades / total_trades
            
            # Calcular uptime
            if self.start_time:
                self.metrics.system_uptime = (datetime.now() - self.start_time).total_seconds()
            
            # Coletar métricas de sistema (opcional)
            try:
                import psutil
                self.metrics.cpu_usage = psutil.cpu_percent()
                self.metrics.memory_usage = psutil.Process().memory_percent()
            except ImportError:
                pass
            
            self.metrics.timestamp = datetime.now()
            
        except Exception as e:
            logger.error(f"Erro ao atualizar métricas: {e}")
    
    def _save_state(self):
        """Salva o estado do sistema."""
        try:
            state_dir = Path("system_state")
            state_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Salvar estado do sistema
            system_state = {
                'timestamp': timestamp,
                'state': self.state.value,
                'config': self.config.to_dict(),
                'metrics': self.metrics.to_dict(),
                'restart_count': self.restart_count
            }
            
            state_file = state_dir / f"system_state_{timestamp}.json"
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(system_state, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Estado do sistema salvo em {state_file}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar estado: {e}")
    
    # Callback handlers
    def _on_analysis_complete(self, data: dict):
        """Handler para conclusão de análise."""
        logger.info(f"📊 Análise concluída: {data.get('symbol', 'N/A')} - {data.get('action', 'N/A')}")
        self._trigger_callback('on_analysis_complete', data)
    
    def _on_decision_made(self, data: dict):
        """Handler para decisão tomada."""
        symbol = data.get('symbol', 'N/A')
        action = data.get('action', 'N/A')
        confidence = data.get('confidence', 0)
        
        logger.info(f"🎯 Decisão: {action} em {symbol} (confiança: {confidence:.1%})")
        self._trigger_callback('on_decision_made', data)
    
    def _on_trade_executed(self, data: dict):
        """Handler para trade executado."""
        if data.get('executed', False):
            symbol = data.get('symbol', 'N/A')
            action = data.get('action', 'N/A')
            price = data.get('price', 0)
            
            logger.success(f"✅ Trade executado: {action} {symbol} @ ${price:.2f}")
        else:
            error = data.get('error_message', 'Erro desconhecido')
            logger.error(f"❌ Falha no trade: {error}")
        
        self._trigger_callback('on_trade_executed', data)
    
    def _on_market_opportunity(self, data: dict):
        """Handler para oportunidade de mercado."""
        symbol = data.get('symbol', 'N/A')
        opportunities = data.get('opportunities', [])
        
        if opportunities:
            logger.info(f"💎 Oportunidade em {symbol}: {', '.join(opportunities)}")
        
        self._trigger_callback('on_market_opportunity', data)
    
    def _on_position_opened(self, data: dict):
        """Handler para posição aberta."""
        symbol = data.get('symbol', 'N/A')
        size = data.get('size', 0)
        entry_price = data.get('entry_price', 0)
        
        logger.info(f"📈 Posição aberta: {symbol} x{size} @ ${entry_price:.2f}")
        self._trigger_callback('on_position_opened', data)
    
    def _on_position_closed(self, data: dict):
        """Handler para posição fechada."""
        symbol = data.get('symbol', 'N/A')
        pnl = data.get('pnl', 0)
        pnl_percent = data.get('pnl_percent', 0)
        
        if pnl >= 0:
            logger.success(f"📉 Posição fechada: {symbol} | P&L: +${pnl:.2f} (+{pnl_percent:.1%})")
        else:
            logger.error(f"📉 Posição fechada: {symbol} | P&L: -${abs(pnl):.2f} ({pnl_percent:.1%})")
        
        self._trigger_callback('on_position_closed', data)
    
    def _on_market_data(self, data: dict):
        """Handler para dados de mercado atualizados."""
        # Este callback é chamado diretamente pelo MarketMonitor
        # Pode ser usado para atualizar caches ou dashboards em tempo real
        pass
    
    def get_status(self) -> dict:
        """Retorna status completo do sistema."""
        self._update_metrics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'state': self.state.value,
            'uptime': self.metrics.system_uptime,
            'config': self.config.to_dict(),
            'metrics': self.metrics.to_dict(),
            'components': {
                'automation_engine': self.automation_engine.get_status() if self.automation_engine else None,
                'market_monitor': self.market_monitor.get_status() if self.market_monitor else None,
                'portfolio_manager': self.portfolio_manager.get_status() if self.portfolio_manager else None,
                'risk_manager': self.risk_manager.get_status() if self.risk_manager else None
            },
            'restart_count': self.restart_count
        }
    
    def _show_startup_banner(self):
        """Exibe banner de inicialização."""
        banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║        🤖 AGI AUTOMATION ORCHESTRATOR v2.0.0                                ║
║        Sistema de Trading Automático com Inteligência Artificial Geral       ║
║                                                                              ║
║  ═══════════════════════════════════════════════════════════════════        ║
║                                                                              ║
║  📊 Configuração:                                                           ║
║     • Modo: {'LIVE TRADING' if self.config.enable_live_trading else 'PAPER TRADING'}                        ║
║     • Capital: ${self.config.initial_capital:,.2f}                                   ║
║     • Símbolos: {len(self.config.symbols)} ativos                                 ║
║     • Frequência: {self.config.analysis_frequency.value}                             ║
║                                                                              ║
║  ═══════════════════════════════════════════════════════════════════        ║
║                                                                              ║
║  Componentes Ativos:                                                         ║
║  ✅ Market Monitor     - Monitoramento contínuo de mercado                   ║
║  ✅ Automation Engine  - Orquestração inteligente de decisões               ║
║  ✅ Portfolio Manager  - Gestão avançada de posições                        ║
║  ✅ Risk Manager       - Controle de risco em tempo real                    ║
║                                                                              ║
║  ═══════════════════════════════════════════════════════════════════        ║
║                                                                              ║
║  Objetivos Esperados (30 dias):                                             ║
║  • 150-200 trades automatizados                                            ║
║  • Taxa de sucesso: 65-75%                                                 ║
║  • P&L: +$5,000 a +$15,000                                                 ║
║  • Retorno: +5% a +15%                                                     ║
║                                                                              ║
║  Sistema operacional 24/7 - Tudo Automaticamente! ✅                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)


def main():
    """Função principal de entrada."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AGI Automation Orchestrator - Sistema de Trading Automático",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s                        # Inicia com configuração padrão
  %(prog)s --config my_config.json # Usa configuração customizada
  %(prog)s --demo                 # Modo demonstração com mocks
  %(prog)s --status              # Apenas mostra status e sai
        """
    )
    
    parser.add_argument(
        '--config',
        help='Caminho para arquivo de configuração JSON',
        default=None
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Executa em modo demonstração com componentes mock'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Mostra status do sistema e sai'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Nível de logging (padrão: INFO)'
    )
    
    args = parser.parse_args()
    
    # Configurar nível de log
    if hasattr(logger, 'level'):  # loguru
        logger.remove()
        logger.add(sys.stdout, level=args.log_level)
    else:  # logging padrão
        logger.setLevel(getattr(logging, args.log_level))
    
    # Criar orquestrador
    orchestrator = AGIOrchestrator(config_path=args.config)
    
    if args.status:
        # Apenas mostrar status
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return
    
    try:
        # Iniciar sistema
        orchestrator.start()
        
        # Manter processo principal ativo
        while orchestrator.state != AutomationState.STOPPED:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\n🛑 Interrupção do usuário detectada")
                orchestrator.stop()
                break
        
    except Exception as e:
        logger.critical(f"❌ Erro fatal: {e}")
        logger.debug(traceback.format_exc())
        orchestrator.stop()
        sys.exit(1)


if __name__ == '__main__':
    main()