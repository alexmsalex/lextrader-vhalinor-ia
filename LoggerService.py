import logging
import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import traceback
import asyncio
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import inspect
import threading
import queue
import colorama
from colorama import Fore, Back, Style

# Inicializar colorama para cores no terminal
colorama.init(autoreset=True)

# Tipos e enums
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AlertType(Enum):
    TRADE_SIGNAL = "TRADE_SIGNAL"
    SYSTEM_ALERT = "SYSTEM_ALERT"
    RISK_ALERT = "RISK_ALERT"
    PERFORMANCE_ALERT = "PERFORMANCE_ALERT"
    SECURITY_ALERT = "SECURITY_ALERT"

class AlertSeverity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

# Estruturas de dados
@dataclass
class TradeSignal:
    id: str
    symbol: str
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float
    price_target: float
    stop_loss: float
    take_profit: float
    timestamp: datetime
    indicators: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'symbol': self.symbol,
            'signal_type': self.signal_type,
            'confidence': self.confidence,
            'price_target': self.price_target,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'timestamp': self.timestamp.isoformat(),
            'indicators': self.indicators
        }

@dataclass
class AutomationAlert:
    id: str
    type: AlertType
    severity: AlertSeverity
    message: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False
    source: str = "system"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type.value,
            'severity': self.severity.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'acknowledged': self.acknowledged,
            'source': self.source
        }

@dataclass
class AutomationMetrics:
    timestamp: datetime
    performance: Dict[str, float]
    risk_metrics: Dict[str, float]
    system_metrics: Dict[str, Any]
    trading_stats: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'performance': self.performance,
            'risk_metrics': self.risk_metrics,
            'system_metrics': self.system_metrics,
            'trading_stats': self.trading_stats
        }

@dataclass
class LogEntry:
    level: LogLevel
    message: str
    timestamp: datetime
    data: Dict[str, Any]
    source: str
    correlation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'level': self.level.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'source': self.source,
            'correlation_id': self.correlation_id
        }

# Formatters personalizados
class ColoredFormatter(logging.Formatter):
    """Formatter colorido para terminal"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

class JSONFormatter(logging.Formatter):
    """Formatter para saída em JSON"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Adicionar dados extras se existirem
        if hasattr(record, 'data'):
            log_entry['data'] = record.data
        
        return json.dumps(log_entry, ensure_ascii=False)

# Handlers customizados
class WebSocketHandler(logging.Handler):
    """Handler para enviar logs via WebSocket"""
    
    def __init__(self, websocket_url: Optional[str] = None):
        super().__init__()
        self.websocket_url = websocket_url
        self.connected = False
        self.queue = queue.Queue()
        self.worker_thread = None
        
    def emit(self, record):
        try:
            # Serializar o registro
            log_data = self.format(record)
            
            # Em produção, enviaria via WebSocket
            # Por enquanto, apenas coloca na fila
            if self.connected:
                self.queue.put(log_data)
            else:
                # Fallback para console
                print(f"[WS LOG] {log_data}")
                
        except Exception:
            self.handleError(record)
    
    def start(self):
        """Inicia worker para WebSocket"""
        if self.websocket_url:
            self.worker_thread = threading.Thread(target=self._ws_worker, daemon=True)
            self.worker_thread.start()
    
    def _ws_worker(self):
        """Worker para WebSocket"""
        # Implementação real de conexão WebSocket
        # Por enquanto, apenas simula
        while True:
            try:
                if not self.queue.empty():
                    log_data = self.queue.get()
                    # Aqui enviaria via WebSocket
                    # print(f"Enviando via WS: {log_data[:50]}...")
                asyncio.sleep(0.1)
            except Exception as e:
                print(f"Erro no worker WS: {e}")

class DatabaseHandler(logging.Handler):
    """Handler para salvar logs em banco de dados"""
    
    def __init__(self, db_config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.db_config = db_config or {}
        self.buffer = []
        self.buffer_size = 100
        self.buffer_lock = threading.Lock()
        
    def emit(self, record):
        try:
            log_entry = {
                'timestamp': datetime.fromtimestamp(record.created),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module,
                'data': getattr(record, 'data', {}),
                'traceback': getattr(record, 'exc_info', None)
            }
            
            with self.buffer_lock:
                self.buffer.append(log_entry)
                
                # Se buffer cheio, salvar em lote
                if len(self.buffer) >= self.buffer_size:
                    self._save_buffer()
                    
        except Exception:
            self.handleError(record)
    
    def _save_buffer(self):
        """Salva buffer no banco de dados"""
        try:
            # Em produção, salvaria em banco de dados
            # Por enquanto, apenas salva em arquivo
            if self.buffer:
                logs_dir = Path("logs/database")
                logs_dir.mkdir(parents=True, exist_ok=True)
                
                filename = logs_dir / f"db_logs_{datetime.now().strftime('%Y%m%d')}.json"
                
                # Carregar logs existentes
                existing_logs = []
                if filename.exists():
                    with open(filename, 'r', encoding='utf-8') as f:
                        existing_logs = json.load(f)
                
                # Adicionar novos logs
                existing_logs.extend(self.buffer)
                
                # Salvar
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(existing_logs, f, indent=2, ensure_ascii=False)
                
                # Limpar buffer
                self.buffer.clear()
                
        except Exception as e:
            print(f"Erro ao salvar logs no banco de dados: {e}")
    
    def flush(self):
        """Força salvamento do buffer"""
        with self.buffer_lock:
            if self.buffer:
                self._save_buffer()

# Classe principal do Logger
class AdvancedLogger:
    """Logger avançado com múltiplos handlers e funcionalidades"""
    
    def __init__(self, name: str = "lextrader-iag", log_level: LogLevel = LogLevel.INFO):
        self.name = name
        self.log_level = log_level
        self.correlation_id = None
        self.metrics_buffer = []
        self.alerts_buffer = []
        self.performance_stats = {}
        
        # Configurar diretório de logs
        self._setup_log_directory()
        
        # Configurar logger
        self._setup_logger()
        
        # Iniciar handlers especiais
        self._start_special_handlers()
        
        print(f"{Fore.GREEN}✅ AdvancedLogger inicializado: {name}{Style.RESET_ALL}")
    
    def _setup_log_directory(self):
        """Configura diretório de logs"""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Subdiretórios
        subdirs = ["error", "performance", "alerts", "trades", "database"]
        for subdir in subdirs:
            (logs_dir / subdir).mkdir(exist_ok=True)
    
    def _setup_logger(self):
        """Configura o logger principal"""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.log_level.value)
        self.logger.propagate = False  # Evitar logs duplicados
        
        # Limpar handlers existentes
        self.logger.handlers.clear()
        
        # Handler para console (colorido)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(self.log_level.value)
        self.logger.addHandler(console_handler)
        
        # Handler para arquivo de logs gerais (rotativo)
        file_handler = RotatingFileHandler(
            filename='logs/combined.log',
            maxBytes=10_485_760,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(self.log_level.value)
        self.logger.addHandler(file_handler)
        
        # Handler para erros (arquivo separado)
        error_handler = RotatingFileHandler(
            filename='logs/error/error.log',
            maxBytes=5_242_880,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setFormatter(file_formatter)
        error_handler.setLevel(logging.ERROR)
        self.logger.addHandler(error_handler)
        
        # Handler para arquivo JSON (para análise estruturada)
        json_handler = TimedRotatingFileHandler(
            filename='logs/structured_logs.json',
            when='midnight',
            backupCount=7,
            encoding='utf-8'
        )
        json_formatter = JSONFormatter()
        json_handler.setFormatter(json_formatter)
        json_handler.setLevel(self.log_level.value)
        self.logger.addHandler(json_handler)
        
        # Handler para banco de dados
        db_handler = DatabaseHandler()
        db_handler.setLevel(self.log_level.value)
        self.logger.addHandler(db_handler)
        
        # Handler para WebSocket (opcional)
        try:
            ws_handler = WebSocketHandler()
            ws_handler.setLevel(LogLevel.INFO.value)
            self.logger.addHandler(ws_handler)
        except Exception as e:
            self.logger.warning(f"Não foi possível inicializar WebSocketHandler: {e}")
    
    def _start_special_handlers(self):
        """Inicia handlers especiais em threads separadas"""
        # Iniciar worker para métricas
        self.metrics_thread = threading.Thread(target=self._metrics_worker, daemon=True)
        self.metrics_thread.start()
        
        # Iniciar worker para alertas
        self.alerts_thread = threading.Thread(target=self._alerts_worker, daemon=True)
        self.alerts_thread.start()
    
    def _metrics_worker(self):
        """Worker para processar métricas em lote"""
        while True:
            try:
                if self.metrics_buffer:
                    self._save_metrics_batch()
                asyncio.sleep(10)  # Processar a cada 10 segundos
            except Exception as e:
                print(f"Erro no worker de métricas: {e}")
                asyncio.sleep(30)
    
    def _alerts_worker(self):
        """Worker para processar alertas em lote"""
        while True:
            try:
                if self.alerts_buffer:
                    self._save_alerts_batch()
                asyncio.sleep(5)  # Processar a cada 5 segundos
            except Exception as e:
                print(f"Erro no worker de alertas: {e}")
                asyncio.sleep(30)
    
    def _save_metrics_batch(self):
        """Salva lote de métricas"""
        try:
            if self.metrics_buffer:
                metrics_dir = Path("logs/performance")
                metrics_dir.mkdir(exist_ok=True)
                
                filename = metrics_dir / f"metrics_{datetime.now().strftime('%Y%m%d')}.json"
                
                # Carregar métricas existentes
                existing_metrics = []
                if filename.exists():
                    with open(filename, 'r', encoding='utf-8') as f:
                        existing_metrics = json.load(f)
                
                # Adicionar novas métricas
                batch = [m.to_dict() for m in self.metrics_buffer]
                existing_metrics.extend(batch)
                
                # Salvar
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(existing_metrics, f, indent=2, ensure_ascii=False)
                
                # Limpar buffer
                self.metrics_buffer.clear()
                
        except Exception as e:
            self.logger.error(f"Erro ao salvar métricas: {e}")
    
    def _save_alerts_batch(self):
        """Salva lote de alertas"""
        try:
            if self.alerts_buffer:
                alerts_dir = Path("logs/alerts")
                alerts_dir.mkdir(exist_ok=True)
                
                filename = alerts_dir / f"alerts_{datetime.now().strftime('%Y%m%d')}.json"
                
                # Carregar alertas existentes
                existing_alerts = []
                if filename.exists():
                    with open(filename, 'r', encoding='utf-8') as f:
                        existing_alerts = json.load(f)
                
                # Adicionar novos alertas
                batch = [a.to_dict() for a in self.alerts_buffer]
                existing_alerts.extend(batch)
                
                # Salvar
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(existing_alerts, f, indent=2, ensure_ascii=False)
                
                # Limpar buffer
                self.alerts_buffer.clear()
                
        except Exception as e:
            self.logger.error(f"Erro ao salvar alertas: {e}")
    
    # Métodos principais de logging
    def log_trade(self, signal: TradeSignal, result: Dict[str, Any]):
        """Log de trade executado"""
        try:
            log_data = {
                'signal': signal.to_dict(),
                'result': result,
                'correlation_id': self.correlation_id,
                'source': 'trading_engine'
            }
            
            # Log principal
            self.logger.info(
                f"Trade Executado: {signal.symbol} | "
                f"{signal.signal_type} | "
                f"Conf: {signal.confidence:.2%}",
                extra={'data': log_data}
            )
            
            # Salvar em arquivo de trades
            self._save_trade_log(signal, result)
            
            # Atualizar estatísticas
            self._update_trading_stats(signal, result)
            
        except Exception as e:
            self.logger.error(f"Erro ao logar trade: {e}")
    
    def log_alert(self, alert: AutomationAlert):
        """Log de alerta do sistema"""
        try:
            # Determinar nível baseado na severidade
            log_level = {
                AlertSeverity.LOW: logging.INFO,
                AlertSeverity.MEDIUM: logging.WARNING,
                AlertSeverity.HIGH: logging.ERROR,
                AlertSeverity.CRITICAL: logging.CRITICAL
            }.get(alert.severity, logging.WARNING)
            
            log_data = {
                'alert': alert.to_dict(),
                'correlation_id': self.correlation_id,
                'source': alert.source
            }
            
            # Log com nível apropriado
            self.logger.log(
                log_level,
                f"Alerta {alert.type.value}: {alert.message}",
                extra={'data': log_data}
            )
            
            # Adicionar ao buffer de alertas
            self.alerts_buffer.append(alert)
            
            # Notificação visual para alertas críticos
            if alert.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]:
                self._notify_critical_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Erro ao logar alerta: {e}")
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Log de erro do sistema"""
        try:
            error_data = {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc(),
                'context': context or {},
                'correlation_id': self.correlation_id,
                'source': self._get_caller_info()
            }
            
            self.logger.error(
                f"Erro do Sistema: {error}",
                extra={'data': error_data},
                exc_info=True
            )
            
            # Enviar email para erros críticos (em produção)
            if self._is_critical_error(error):
                self._send_error_notification(error, context)
                
        except Exception as e:
            # Fallback para erro no logger
            print(f"ERRO CRÍTICO NO LOGGER: {e}")
            print(f"Erro original: {error}")
            if context:
                print(f"Contexto: {context}")
    
    def log_performance(self, metrics: AutomationMetrics):
        """Log de métricas de performance"""
        try:
            log_data = {
                'metrics': metrics.to_dict(),
                'correlation_id': self.correlation_id,
                'source': 'performance_monitor'
            }
            
            # Formatar métricas para log
            perf_summary = (
                f"Performance | Retorno: {metrics.performance.get('total_return', 0):.2%} | "
                f"Sharpe: {metrics.risk_metrics.get('sharpe_ratio', 0):.2f} | "
                f"Drawdown: {metrics.risk_metrics.get('max_drawdown', 0):.2%}"
            )
            
            self.logger.info(
                perf_summary,
                extra={'data': log_data}
            )
            
            # Adicionar ao buffer de métricas
            self.metrics_buffer.append(metrics)
            
            # Verificar anomalias
            self._check_performance_anomalies(metrics)
            
        except Exception as e:
            self.logger.error(f"Erro ao logar performance: {e}")
    
    def debug(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log de debug"""
        self._log_with_level(LogLevel.DEBUG, message, data)
    
    def info(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log de informação"""
        self._log_with_level(LogLevel.INFO, message, data)
    
    def warning(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log de warning"""
        self._log_with_level(LogLevel.WARNING, message, data)
    
    def error(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log de erro"""
        self._log_with_level(LogLevel.ERROR, message, data)
    
    def critical(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log crítico"""
        self._log_with_level(LogLevel.CRITICAL, message, data)
    
    def _log_with_level(self, level: LogLevel, message: str, data: Optional[Dict[str, Any]] = None):
        """Método genérico para log com nível"""
        try:
            log_data = {
                'data': data or {},
                'correlation_id': self.correlation_id,
                'source': self._get_caller_info()
            }
            
            log_method = getattr(self.logger, level.value.lower())
            log_method(message, extra={'data': log_data})
            
        except Exception as e:
            print(f"Erro no log genérico: {e}")
    
    # Métodos utilitários
    def _save_trade_log(self, signal: TradeSignal, result: Dict[str, Any]):
        """Salva log de trade em arquivo separado"""
        try:
            trades_dir = Path("logs/trades")
            trades_dir.mkdir(exist_ok=True)
            
            filename = trades_dir / f"trades_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Carregar trades existentes
            existing_trades = []
            if filename.exists():
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_trades = json.load(f)
            
            # Novo trade
            trade_log = {
                'timestamp': datetime.now().isoformat(),
                'signal': signal.to_dict(),
                'result': result,
                'correlation_id': self.correlation_id
            }
            
            existing_trades.append(trade_log)
            
            # Salvar
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_trades, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Erro ao salvar trade: {e}")
    
    def _update_trading_stats(self, signal: TradeSignal, result: Dict[str, Any]):
        """Atualiza estatísticas de trading"""
        try:
            stats_key = signal.symbol
            
            if stats_key not in self.performance_stats:
                self.performance_stats[stats_key] = {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'total_pnl': 0.0,
                    'avg_pnl': 0.0,
                    'last_trade_time': None
                }
            
            stats = self.performance_stats[stats_key]
            stats['total_trades'] += 1
            stats['last_trade_time'] = datetime.now().isoformat()
            
            # Verificar se foi um trade vencedor
            pnl = result.get('pnl', 0.0)
            stats['total_pnl'] += pnl
            
            if pnl > 0:
                stats['winning_trades'] += 1
            elif pnl < 0:
                stats['losing_trades'] += 1
            
            # Calcular média
            if stats['total_trades'] > 0:
                stats['avg_pnl'] = stats['total_pnl'] / stats['total_trades']
            
            # Log estatísticas periódicas
            if stats['total_trades'] % 10 == 0:
                self.logger.info(
                    f"Estatísticas {signal.symbol}: "
                    f"{stats['total_trades']} trades | "
                    f"Win Rate: {stats['winning_trades']/stats['total_trades']:.1%} | "
                    f"P&L Total: {stats['total_pnl']:.2f}",
                    extra={'data': {'stats': stats}}
                )
                
        except Exception as e:
            self.logger.error(f"Erro ao atualizar estatísticas: {e}")
    
    def _notify_critical_alert(self, alert: AutomationAlert):
        """Notificação visual para alertas críticos"""
        try:
            # Em produção, enviaria notificação push/email
            # Por enquanto, apenas log colorido
            alert_color = {
                AlertSeverity.HIGH: Fore.RED,
                AlertSeverity.CRITICAL: Fore.RED + Style.BRIGHT + Back.YELLOW
            }.get(alert.severity, Fore.YELLOW)
            
            border = "=" * 80
            alert_msg = (
                f"\n{border}\n"
                f"🚨 ALERTA CRÍTICO 🚨\n"
                f"Tipo: {alert.type.value}\n"
                f"Severidade: {alert.severity.value}\n"
                f"Mensagem: {alert.message}\n"
                f"Horário: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Fonte: {alert.source}\n"
                f"{border}\n"
            )
            
            print(f"{alert_color}{alert_msg}{Style.RESET_ALL}")
            
        except Exception as e:
            self.logger.error(f"Erro na notificação de alerta: {e}")
    
    def _check_performance_anomalies(self, metrics: AutomationMetrics):
        """Verifica anomalias nas métricas de performance"""
        try:
            # Verificar drawdown excessivo
            max_drawdown = metrics.risk_metrics.get('max_drawdown', 0)
            if max_drawdown > 0.1:  # 10% drawdown
                alert = AutomationAlert(
                    id=f"drawdown-alert-{datetime.now().timestamp()}",
                    type=AlertType.RISK_ALERT,
                    severity=AlertSeverity.HIGH,
                    message=f"Drawdown excessivo detectado: {max_drawdown:.2%}",
                    timestamp=datetime.now(),
                    data={'metrics': metrics.to_dict()},
                    source="performance_monitor"
                )
                self.log_alert(alert)
            
            # Verificar sharpe ratio muito baixo
            sharpe = metrics.risk_metrics.get('sharpe_ratio', 0)
            if sharpe < 0.5:
                alert = AutomationAlert(
                    id=f"sharpe-alert-{datetime.now().timestamp()}",
                    type=AlertType.PERFORMANCE_ALERT,
                    severity=AlertSeverity.MEDIUM,
                    message=f"Sharpe ratio muito baixo: {sharpe:.2f}",
                    timestamp=datetime.now(),
                    data={'metrics': metrics.to_dict()},
                    source="performance_monitor"
                )
                self.log_alert(alert)
                
        except Exception as e:
            self.logger.error(f"Erro ao verificar anomalias: {e}")
    
    def _is_critical_error(self, error: Exception) -> bool:
        """Determina se um erro é crítico"""
        critical_errors = [
            'MemoryError',
            'ConnectionError', 
            'TimeoutError',
            'FileNotFoundError',
            'PermissionError'
        ]
        
        return type(error).__name__ in critical_errors
    
    def _send_error_notification(self, error: Exception, context: Optional[Dict[str, Any]]):
        """Envia notificação de erro (simulação)"""
        try:
            # Em produção, enviaria email/SMS/notificação push
            error_summary = {
                'error': str(error),
                'type': type(error).__name__,
                'timestamp': datetime.now().isoformat(),
                'context': context,
                'system': self.name
            }
            
            # Por enquanto, apenas log
            self.logger.critical(
                "ERRO CRÍTICO - NOTIFICAÇÃO REQUERIDA",
                extra={'data': error_summary}
            )
            
        except Exception as e:
            print(f"Erro ao enviar notificação: {e}")
    
    def _get_caller_info(self) -> str:
        """Obtém informações sobre quem chamou o log"""
        try:
            # Pegar o frame do caller (2 níveis acima)
            frame = inspect.currentframe().f_back.f_back
            module = inspect.getmodule(frame)
            func_name = frame.f_code.co_name
            line_no = frame.f_lineno
            
            return f"{module.__name__ if module else 'unknown'}:{func_name}:{line_no}"
        except:
            return "unknown"
    
    # Métodos de configuração
    def set_correlation_id(self, correlation_id: str):
        """Define ID de correlação para rastreamento"""
        self.correlation_id = correlation_id
        self.logger.debug(f"Correlation ID definido: {correlation_id}")
    
    def set_log_level(self, level: LogLevel):
        """Altera nível de log em tempo de execução"""
        self.log_level = level
        self.logger.setLevel(level.value)
        
        # Atualizar handlers
        for handler in self.logger.handlers:
            handler.setLevel(level.value)
        
        self.logger.info(f"Nível de log alterado para: {level.value}")
    
    def add_handler(self, handler: logging.Handler):
        """Adiciona handler customizado"""
        self.logger.addHandler(handler)
        self.logger.debug(f"Handler adicionado: {type(handler).__name__}")
    
    def remove_handler(self, handler: logging.Handler):
        """Remove handler"""
        self.logger.removeHandler(handler)
        self.logger.debug(f"Handler removido: {type(handler).__name__}")
    
    # Métodos de consulta e relatórios
    def get_performance_summary(self) -> Dict[str, Any]:
        """Retorna resumo de performance"""
        return {
            'performance_stats': self.performance_stats,
            'total_alerts': len(self.alerts_buffer),
            'total_metrics': len(self.metrics_buffer),
            'correlation_id': self.correlation_id,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_recent_logs(self, count: int = 100) -> List[Dict[str, Any]]:
        """Obtém logs recentes (simulação)"""
        try:
            # Em produção, buscaria do banco de dados
            # Por enquanto, retorna dados simulados
            logs = []
            
            # Tentar ler do arquivo de logs combinados
            log_file = Path("logs/combined.log")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-count:]
                    for line in lines:
                        try:
                            parts = line.strip().split(' | ')
                            if len(parts) >= 4:
                                logs.append({
                                    'timestamp': parts[0],
                                    'level': parts[1],
                                    'message': ' | '.join(parts[3:])
                                })
                        except:
                            continue
            
            return logs
            
        except Exception as e:
            self.logger.error(f"Erro ao obter logs recentes: {e}")
            return []
    
    def generate_report(self, report_type: str = "daily") -> Dict[str, Any]:
        """Gera relatório consolidado"""
        try:
            report = {
                'report_id': f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'generated_at': datetime.now().isoformat(),
                'report_type': report_type,
                'performance_summary': self.get_performance_summary(),
                'system_info': {
                    'logger_name': self.name,
                    'log_level': self.log_level.value,
                    'handlers': [type(h).__name__ for h in self.logger.handlers]
                }
            }
            
            # Salvar relatório
            reports_dir = Path("logs/reports")
            reports_dir.mkdir(exist_ok=True)
            
            filename = reports_dir / f"report_{report['report_id']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Relatório gerado: {report['report_id']}")
            return report
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            return {'error': str(e)}
    
    def flush(self):
        """Força flush de todos os buffers"""
        try:
            # Flush handlers
            for handler in self.logger.handlers:
                if hasattr(handler, 'flush'):
                    handler.flush()
            
            # Flush buffers internos
            if self.metrics_buffer:
                self._save_metrics_batch()
            
            if self.alerts_buffer:
                self._save_alerts_batch()
            
            self.logger.debug("Todos os buffers foram sincronizados")
            
        except Exception as e:
            print(f"Erro ao fazer flush: {e}")

# Instância global
logger = AdvancedLogger()

# Funções de conveniência para uso rápido
def setup_logger(name: str = "lextrader-iag", level: LogLevel = LogLevel.INFO) -> AdvancedLogger:
    """Configura e retorna um novo logger"""
    return AdvancedLogger(name, level)

def get_logger(name: str = "lextrader-iag") -> AdvancedLogger:
    """Obtém logger existente ou cria novo"""
    return AdvancedLogger(name)

# Exemplo de uso
if __name__ == "__main__":
    # Teste do logger
    print("🧪 Testando AdvancedLogger...")
    
    # Configurar logger
    log = AdvancedLogger("test-logger", LogLevel.DEBUG)
    
    # Definir correlation ID
    log.set_correlation_id("test-session-123")
    
    # Testar diferentes níveis de log
    log.debug("Mensagem de debug", {"debug_data": True})
    log.info("Mensagem de informação", {"info_data": "teste"})
    log.warning("Mensagem de warning", {"warning_level": "medium"})
    
    # Testar trade
    signal = TradeSignal(
        id="trade-001",
        symbol="BTC/USDT",
        signal_type="BUY",
        confidence=0.85,
        price_target=65000,
        stop_loss=62000,
        take_profit=67000,
        timestamp=datetime.now(),
        indicators={"RSI": 65, "MACD": "bullish"}
    )
    
    result = {
        "executed_price": 64500,
        "pnl": 150.50,
        "status": "filled",
        "order_id": "order-12345"
    }
    
    log.log_trade(signal, result)
    
    # Testar alerta
    alert = AutomationAlert(
        id="alert-001",
        type=AlertType.RISK_ALERT,
        severity=AlertSeverity.HIGH,
        message="Drawdown excessivo detectado!",
        timestamp=datetime.now(),
        data={"drawdown": 0.12, "threshold": 0.10},
        source="risk_manager"
    )
    
    log.log_alert(alert)
    
    # Testar performance
    metrics = AutomationMetrics(
        timestamp=datetime.now(),
        performance={
            "total_return": 0.15,
            "daily_return": 0.002,
            "monthly_return": 0.08
        },
        risk_metrics={
            "sharpe_ratio": 1.8,
            "max_drawdown": 0.05,
            "volatility": 0.12
        },
        system_metrics={
            "cpu_usage": 45.2,
            "memory_usage": 1234,
            "active_threads": 8
        }
    )
    
    log.log_performance(metrics)
    
    # Testar erro
    try:
        raise ValueError("Erro de teste intencional")
    except Exception as e:
        log.log_error(e, {"context": "teste de erro"})
    
    # Gerar relatório
    report = log.generate_report("test")
    print(f"📊 Relatório gerado: {report['report_id']}")
    
    # Mostrar resumo
    summary = log.get_performance_summary()
    print(f"📈 Resumo: {summary['performance_stats']}")
    
    print("✅ Teste do logger concluído!")