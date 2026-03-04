"""Wrapper module that exposes the real `integrated_trading_system`
located in `neural_layers/04_decisao` under the package
`neural_layers.decisao` so imports like
`from neural_layers.decisao.integrated_trading_system import IntegratedTradingSystem`
funcionem sem alterar a estrutura existente.
"""
import importlib.util
import os
import sys

_this_dir = os.path.dirname(__file__)
_real_path = os.path.normpath(os.path.join(_this_dir, '..', '04_decisao', 'integrated_trading_system.py'))

if not os.path.exists(_real_path):
    raise ImportError(f"Arquivo esperado não encontrado: {_real_path}")

# Assegura que a pasta com o código real esteja no sys.path para
# permitir imports absolutos usados internamente (ex: `trading_execution_engine`).
_real_dir = os.path.dirname(_real_path)
if _real_dir not in sys.path:
    sys.path.insert(0, _real_dir)

spec = importlib.util.spec_from_file_location(__name__, _real_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Copia atributos públicos do módulo real para este módulo wrapper
for _attr in dir(module):
    if not _attr.startswith('__'):
        globals()[_attr] = getattr(module, _attr)

__all__ = [name for name in globals() if not name.startswith('_')]
