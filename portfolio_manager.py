"""
Portfolio Manager - Gerenciador Automático de Portfólio
======================================================
Gerencia posições abertas, calcula P&L, rebalanceia portfólio
e otimiza alocação de capital automaticamente
"""

import threading
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from loguru import logger
except ImportError:
    import logging as logger_module
    logger = logger_module.getLogger(__name__)


class PositionStatus(Enum):
    """Status de uma posição"""
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING = "PENDING"
    ERROR = "ERROR"


@dataclass
class Position:
    """Representa uma posição aberta"""
    position_id: str
    symbol: str
    entry_price: float
    current_price: float
    quantity: float
    side: str  # 'LONG' or 'SHORT'
    entry_time: datetime
    stop_loss: float
    take_profit: float
    status: PositionStatus
    pnl: float = 0.0
    pnl_pct: float = 0.0
    data: Dict = None


@dataclass
class PortfolioMetrics:
    """Métricas gerais do portfólio"""
    timestamp: datetime
    total_capital: float
    used_capital: float
    available_capital: float
    total_positions: int
    open_positions: int
    closed_positions: int
    total_pnl: float
    total_pnl_pct: float
    win_rate: float
    avg_win: float
    avg_loss: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float


class PortfolioManager:
    """
    Gerenciador de portfólio que monitora e otimiza posições
    """

    def __init__(self, initial_capital: float = 100000, max_positions: int = 10):
        """
        Args:
            initial_capital: Capital inicial
            max_positions: Número máximo de posições abertas
        """
        self.initial_capital = initial_capital
        self.available_capital = initial_capital
        self.max_positions = max_positions
        
        # Posições
        self.open_positions: Dict[str, Position] = {}
        self.closed_positions: List[Position] = []
        
        # Histórico
        self.position_history: List[Dict] = []
        self.pnl_history: List[Dict] = []
        
        # Métricas
        self.metrics = None
        self.daily_pnl: Dict[str, float] = {}
        
        # Threading
        self.is_running = False
        self._stop_event = threading.Event()
        self._monitor_thread = None
        
        # Callbacks
        self._callbacks = {
            'on_position_opened': [],
            'on_position_closed': [],
            'on_rebalance': [],
            'on_metrics_update': [],
        }
        
        logger.info(f"✅ Portfolio Manager inicializado com ${initial_capital:.2f}")

    def register_callback(self, event_type: str, callback):
        """Registra callback para eventos"""
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)

    def _trigger_callbacks(self, event_type: str, data: Dict = None):
        """Dispara callbacks registrados"""
        if event_type in self._callbacks:
            for callback in self._callbacks[event_type]:
                try:
                    callback(data or {})
                except Exception as e:
                    logger.error(f"❌ Erro em callback {event_type}: {e}")

    def start(self):
        """Inicia gerenciador"""
        if self.is_running:
            return
        
        self.is_running = True
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("📊 Portfolio Manager iniciado")

    def stop(self):
        """Para gerenciador"""
        self.is_running = False
        self._stop_event.set()
        logger.info("📊 Portfolio Manager parado")

    def _monitoring_loop(self):
        """Loop de monitoramento e atualização"""
        while not self._stop_event.is_set():
            try:
                # Atualizar métricas a cada 30 segundos
                self.update_metrics()
                
                # Verificar stop loss e take profit a cada 10 segundos
                self._check_position_levels()
                
                # Rebalancear a cada 5 minutos
                if int(time.time()) % 300 == 0:
                    self.rebalance_portfolio()
                
                time.sleep(10)
            
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}")
                time.sleep(5)

    def open_position(self, symbol: str, entry_price: float, quantity: float,
                      side: str = 'LONG', stop_loss: float = None,
                      take_profit: float = None) -> Optional[Position]:
        """
        Abre nova posição
        """
        try:
            # Validar limite de posições
            if len(self.open_positions) >= self.max_positions:
                logger.warning(f"⚠️  Limite de posições atingido ({self.max_positions})")
                return None
            
            # Validar capital disponível
            capital_needed = entry_price * quantity
            if capital_needed > self.available_capital:
                logger.warning(f"⚠️  Capital insuficiente: ${capital_needed:.2f} > ${self.available_capital:.2f}")
                return None
            
            # Criar posição
            position_id = f"{symbol}_{datetime.now().timestamp()}"
            position = Position(
                position_id=position_id,
                symbol=symbol,
                entry_price=entry_price,
                current_price=entry_price,
                quantity=quantity,
                side=side,
                entry_time=datetime.now(),
                stop_loss=stop_loss or entry_price * (0.98 if side == 'LONG' else 1.02),
                take_profit=take_profit or entry_price * (1.02 if side == 'LONG' else 0.98),
                status=PositionStatus.OPEN,
            )
            
            # Atualizar capital
            self.available_capital -= capital_needed
            self.open_positions[position_id] = position
            
            logger.info(f"✅ Posição aberta: {position_id} {quantity} {symbol} @ ${entry_price}")
            self._trigger_callbacks('on_position_opened', asdict(position))
            
            return position
        
        except Exception as e:
            logger.error(f"❌ Erro ao abrir posição: {e}")
            return None

    def close_position(self, position_id: str, exit_price: float) -> bool:
        """
        Fecha uma posição
        """
        try:
            if position_id not in self.open_positions:
                logger.warning(f"⚠️  Posição não encontrada: {position_id}")
                return False
            
            position = self.open_positions[position_id]
            
            # Calcular P&L
            if position.side == 'LONG':
                pnl = (exit_price - position.entry_price) * position.quantity
            else:
                pnl = (position.entry_price - exit_price) * position.quantity
            
            pnl_pct = (pnl / (position.entry_price * position.quantity)) * 100
            
            # Atualizar posição
            position.current_price = exit_price
            position.status = PositionStatus.CLOSED
            position.pnl = pnl
            position.pnl_pct = pnl_pct
            
            # Liberar capital
            self.available_capital += exit_price * position.quantity
            
            # Mover para histórico
            self.closed_positions.append(position)
            del self.open_positions[position_id]
            
            logger.info(f"✅ Posição fechada: {position_id} P&L: ${pnl:.2f} ({pnl_pct:.2f}%)")
            self._trigger_callbacks('on_position_closed', {
                'position': asdict(position),
                'pnl': pnl,
                'pnl_pct': pnl_pct,
            })
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao fechar posição: {e}")
            return False

    def update_position_price(self, position_id: str, current_price: float):
        """Atualiza preço atual de uma posição"""
        if position_id in self.open_positions:
            position = self.open_positions[position_id]
            position.current_price = current_price
            
            # Calcular P&L
            if position.side == 'LONG':
                position.pnl = (current_price - position.entry_price) * position.quantity
            else:
                position.pnl = (position.entry_price - current_price) * position.quantity
            
            position.pnl_pct = (position.pnl / (position.entry_price * position.quantity)) * 100

    def _check_position_levels(self):
        """Verifica stop loss e take profit"""
        for position_id, position in list(self.open_positions.items()):
            try:
                price = position.current_price
                
                # Check stop loss
                if position.side == 'LONG' and price <= position.stop_loss:
                    logger.warning(f"⚠️  Stop loss atingido: {position_id}")
                    self.close_position(position_id, position.stop_loss)
                elif position.side == 'SHORT' and price >= position.stop_loss:
                    logger.warning(f"⚠️  Stop loss atingido: {position_id}")
                    self.close_position(position_id, position.stop_loss)
                
                # Check take profit
                if position.side == 'LONG' and price >= position.take_profit:
                    logger.info(f"✅ Take profit atingido: {position_id}")
                    self.close_position(position_id, position.take_profit)
                elif position.side == 'SHORT' and price <= position.take_profit:
                    logger.info(f"✅ Take profit atingido: {position_id}")
                    self.close_position(position_id, position.take_profit)
            
            except Exception as e:
                logger.error(f"❌ Erro ao verificar posição {position_id}: {e}")

    def update_metrics(self):
        """Atualiza métricas gerais do portfólio"""
        try:
            total_pnl = 0.0
            open_pnl = 0.0
            
            # P&L de posições fechadas
            for position in self.closed_positions:
                total_pnl += position.pnl
            
            # P&L de posições abertas
            for position in self.open_positions.values():
                total_pnl += position.pnl
                open_pnl += position.pnl
            
            # Win rate
            closed_wins = sum(1 for p in self.closed_positions if p.pnl > 0)
            closed_total = len(self.closed_positions)
            win_rate = (closed_wins / closed_total * 100) if closed_total > 0 else 0
            
            # Average win/loss
            wins = [p.pnl for p in self.closed_positions if p.pnl > 0]
            losses = [p.pnl for p in self.closed_positions if p.pnl < 0]
            avg_win = sum(wins) / len(wins) if wins else 0
            avg_loss = sum(losses) / len(losses) if losses else 0
            
            # Total capital
            used_capital = sum(p.entry_price * p.quantity for p in self.open_positions.values())
            
            self.metrics = PortfolioMetrics(
                timestamp=datetime.now(),
                total_capital=self.initial_capital + total_pnl,
                used_capital=used_capital,
                available_capital=self.available_capital,
                total_positions=len(self.open_positions) + len(self.closed_positions),
                open_positions=len(self.open_positions),
                closed_positions=len(self.closed_positions),
                total_pnl=total_pnl,
                total_pnl_pct=(total_pnl / self.initial_capital * 100),
                win_rate=win_rate,
                avg_win=avg_win,
                avg_loss=avg_loss,
                max_drawdown=0,  # Implementar cálculo
                sharpe_ratio=0,  # Implementar cálculo
                sortino_ratio=0,  # Implementar cálculo
            )
            
            self._trigger_callbacks('on_metrics_update', asdict(self.metrics))
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar métricas: {e}")

    def rebalance_portfolio(self):
        """Rebalanceia portfólio"""
        try:
            logger.info("🔄 Iniciando rebalanceamento de portfólio...")
            
            # Implementar lógica de rebalanceamento
            # Exemplos:
            # 1. Fechar posições com maior drawdown
            # 2. Reduzir exposição em símbolos correlacionados
            # 3. Realizar rotação de portfólio
            # 4. Otimizar alocação de capital
            
            self._trigger_callbacks('on_rebalance', {
                'timestamp': datetime.now(),
                'positions': len(self.open_positions),
            })
            
            logger.info("✅ Rebalanceamento concluído")
        
        except Exception as e:
            logger.error(f"❌ Erro ao rebalancear: {e}")

    def get_metrics(self) -> Optional[Dict]:
        """Retorna métricas atuais"""
        if self.metrics:
            return asdict(self.metrics)
        return None

    def get_positions_summary(self) -> Dict:
        """Retorna resumo de posições"""
        return {
            'open_positions': len(self.open_positions),
            'closed_positions': len(self.closed_positions),
            'open_symbols': list(self.open_positions.keys()),
            'total_pnl': sum(p.pnl for p in list(self.open_positions.values()) + self.closed_positions),
        }

    def export_portfolio_state(self, filepath: str):
        """Exporta estado do portfólio"""
        try:
            state = {
                'timestamp': datetime.now().isoformat(),
                'metrics': asdict(self.metrics) if self.metrics else None,
                'open_positions': [asdict(p) for p in self.open_positions.values()],
                'recent_closed_positions': [asdict(p) for p in self.closed_positions[-50:]],
            }
            
            with open(filepath, 'w') as f:
                json.dump(state, f, indent=2, default=str)
            
            logger.info(f"💾 Estado do portfólio exportado para {filepath}")
        except Exception as e:
            logger.error(f"❌ Erro ao exportar portfólio: {e}")
