# -*- coding: utf-8 -*-
"""
🎨 APP.PY IMPROVEMENTS & ENHANCEMENTS - LEXTRADER-IAG 4.0
========================================================

Melhorias para a interface principal do LEXTRADER, incluindo:
- Componentes reutilizáveis
- Validação de entrada
- Performance optimization
- Error handling robusto
"""

import streamlit as st
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Callable
from enum import Enum
import logging
from functools import wraps
from datetime import datetime
import time

logger = logging.getLogger(__name__)


# ============================================================================
# COMPONENTES REUTILIZÁVEIS
# ============================================================================

class ComponentSize(Enum):
    """Tamanhos para componentes"""
    SMALL = ("small", 1)
    MEDIUM = ("medium", 2)
    LARGE = ("large", 3)


@dataclass
class MetricValue:
    """Representação de métrica para dashboards"""
    label: str
    value: Any
    unit: str = ""
    delta: Optional[float] = None
    delta_color: str = "off"  # off, normal, inverse, red, green
    icon: str = "📊"
    
    def __str__(self):
        return f"{self.icon} {self.label}: {self.value}{self.unit}"


class UIBuilder:
    """Builder para construir componentes UI consistentes"""
    
    @staticmethod
    def render_metric_card(metric: MetricValue, width: Optional[int] = None) -> None:
        """Renderiza card de métrica"""
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write(metric.icon)
            
            with col2:
                st.metric(
                    label=metric.label,
                    value=metric.value,
                    delta=metric.delta,
                    delta_color=metric.delta_color,
                    label_visibility="visible"
                )
    
    @staticmethod
    def render_metrics_grid(metrics: List[MetricValue], columns: int = 3) -> None:
        """Renderiza grid de métricas"""
        cols = st.columns(columns)
        for i, metric in enumerate(metrics):
            with cols[i % columns]:
                UIBuilder.render_metric_card(metric)
    
    @staticmethod
    def render_status_indicator(status: str, status_text: str = "") -> None:
        """Renderiza indicador de status com cor apropriada"""
        status_colors = {
            "active": ("🟢", "#27ae60"),
            "inactive": ("⚫", "#95a5a6"),
            "warning": ("🟡", "#f39c12"),
            "error": ("🔴", "#e74c3c"),
        }
        
        icon, color = status_colors.get(status, ("⚪", "#bdc3c7"))
        st.markdown(f"<span style='color: {color}; font-size: 20px'>{icon} {status_text}</span>", unsafe_allow_html=True)
    
    @staticmethod
    def render_section(title: str, icon: str = "📋", collapsible: bool = False) -> None:
        """Renderiza seção com título formatado"""
        if collapsible:
            with st.expander(f"{icon} {title}", expanded=True):
                return True
        else:
            st.markdown(f"### {icon} {title}")
            return False
    
    @staticmethod
    def render_warning_box(message: str, title: str = "⚠️ Atenção") -> None:
        """Renderiza box de aviso"""
        st.warning(f"**{title}**\n\n{message}")
    
    @staticmethod
    def render_info_box(message: str, title: str = "ℹ️ Informação") -> None:
        """Renderiza box de informação"""
        st.info(f"**{title}**\n\n{message}")
    
    @staticmethod
    def render_success_box(message: str, title: str = "✅ Sucesso") -> None:
        """Renderiza box de sucesso"""
        st.success(f"**{title}**\n\n{message}")
    
    @staticmethod
    def render_error_box(message: str, title: str = "❌ Erro") -> None:
        """Renderiza box de erro"""
        st.error(f"**{title}**\n\n{message}")
    
    @staticmethod
    def render_key_value_table(data: Dict[str, Any], title: str = "Detalhes") -> None:
        """Renderiza tabela de chave-valor"""
        st.markdown(f"#### {title}")
        for key, value in data.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**{key}**")
            with col2:
                st.write(f"`{value}`")


# ============================================================================
# VALIDAÇÃO DE ENTRADA
# ============================================================================

class ValidationError(Exception):
    """Exceção de validação"""
    pass


class InputValidator:
    """Validador de entrada para formulários"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Valida chave de API (mínimo 20 caracteres)"""
        return len(api_key.strip()) >= 20
    
    @staticmethod
    def validate_number_range(value: float, min_val: float, max_val: float) -> bool:
        """Valida número dentro de range"""
        return min_val <= value <= max_val
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Valida formato de símbolo"""
        import re
        pattern = r'^[A-Z]{1,5}(/[A-Z]{1,5})?$'
        return re.match(pattern, symbol) is not None
    
    @staticmethod
    def validate_percentage(value: float) -> bool:
        """Valida percentual (0-100)"""
        return 0 <= value <= 100
    
    @staticmethod
    def validate_positive(value: float) -> bool:
        """Valida número positivo"""
        return value > 0


# ============================================================================
# PERFORMANCE MONITORING
# ============================================================================

class PerformanceMonitor:
    """Monitora performance de operações"""
    
    def __init__(self):
        self.operations: Dict[str, List[float]] = {}
        self.slowest_ops: List[tuple] = []
    
    def record(self, operation: str, duration: float) -> None:
        """Registra operação"""
        if operation not in self.operations:
            self.operations[operation] = []
        
        self.operations[operation].append(duration)
        
        if len(self.slowest_ops) < 10:
            self.slowest_ops.append((operation, duration))
        elif duration > min(self.slowest_ops, key=lambda x: x[1])[1]:
            self.slowest_ops.remove(min(self.slowest_ops, key=lambda x: x[1]))
            self.slowest_ops.append((operation, duration))
    
    def get_average(self, operation: str) -> float:
        """Retorna tempo médio de operação"""
        if operation in self.operations and self.operations[operation]:
            return sum(self.operations[operation]) / len(self.operations[operation])
        return 0.0
    
    def get_slowest(self, top: int = 5) -> List[tuple]:
        """Retorna operações mais lentas"""
        return sorted(self.slowest_ops, key=lambda x: x[1], reverse=True)[:top]
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas"""
        return {
            "total_operations": sum(len(v) for v in self.operations.values()),
            "tracked_operations": len(self.operations),
            "slowest": self.get_slowest(5),
            "averages": {k: self.get_average(k) for k in self.operations.keys()}
        }


# ============================================================================
# DECORATORS
# ============================================================================

def timing_decorator(func: Callable) -> Callable:
    """Decorator para medir tempo de execução"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start
            logger.info(f"{func.__name__} took {duration:.3f}s")
    return wrapper


def error_handler(default_return=None):
    """Decorator para tratamento de erros"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Erro em {func.__name__}: {str(e)}")
                st.error(f"❌ Erro: {str(e)}")
                return default_return
        return wrapper
    return decorator


def cache_result(ttl_seconds: int = 300):
    """Decorator para cache simples com TTL"""
    cache = {}
    cache_time = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            
            if key in cache and (now - cache_time[key]) < ttl_seconds:
                logger.info(f"Cache hit para {func.__name__}")
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            cache_time[key] = now
            return result
        
        return wrapper
    return decorator


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def example_usage():
    """Exemplo de uso dos componentes"""
    st.set_page_config(page_title="LEXTRADER Improvements", layout="wide")
    
    st.title("🚀 Melhorias - LEXTRADER-IAG 4.0")
    
    # Exemplo 1: Métricas
    st.header("Exemplo 1: Dashboard de Métricas")
    
    metrics = [
        MetricValue(label="Saldo", value="$10,250.50", delta=250.50, icon="💰"),
        MetricValue(label="Win Rate", value="65.5%", delta=+5.2, icon="📈"),
        MetricValue(label="PnL Hoje", value="$150.75", delta=+150, icon="🎯"),
    ]
    
    UIBuilder.render_metrics_grid(metrics, columns=3)
    
    st.divider()
    
    # Exemplo 2: Status
    st.header("Exemplo 2: Indicadores de Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        UIBuilder.render_status_indicator("active", "Sistema Ativo")
    with col2:
        UIBuilder.render_status_indicator("warning", "API em Limite")
    with col3:
        UIBuilder.render_status_indicator("error", "Conexão Perdida")
    
    st.divider()
    
    # Exemplo 3: Validação
    st.header("Exemplo 3: Validação de Entrada")
    
    email = st.text_input("Email")
    if email and InputValidator.validate_email(email):
        st.success("✅ Email válido")
    elif email:
        st.error("❌ Email inválido")
    
    st.divider()
    
    # Exemplo 4: Performance
    st.header("Exemplo 4: Monitor de Performance")
    
    monitor = PerformanceMonitor()
    monitor.record("data_fetch", 0.5)
    monitor.record("data_fetch", 0.45)
    monitor.record("analysis", 1.2)
    
    stats = monitor.get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Operações", stats["total_operations"])
    with col2:
        st.metric("Operações Rastreadas", stats["tracked_operations"])
    
    st.write("Operações mais lentas:")
    for op, duration in monitor.get_slowest(3):
        st.write(f"  - {op}: {duration:.3f}s")


if __name__ == "__main__":
    example_usage()
