"""
AI Configuration Manager - Gerenciador de Configuração da IA
============================================================
Sistema para gerenciar configurações, parâmetros e ajustes da IA integrada
"""

import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import os

logger = logging.getLogger(__name__)

@dataclass
class NeuralConfig:
    """Configuração da rede neural"""
    activation_threshold: float = 0.5
    learning_rate: float = 0.1
    energy_decay_rate: float = 0.01
    max_connections_per_neuron: int = 10
    plasticity_enabled: bool = True

@dataclass
class MemoryConfig:
    """Configuração do sistema de memória"""
    working_memory_size: int = 7
    short_term_memory_size: int = 100
    long_term_memory_limit: int = 10000
    cache_size: int = 1000
    importance_threshold: float = 0.7
    auto_consolidation: bool = True

@dataclass
class LearningConfig:
    """Configuração do sistema de aprendizado"""
    enable_online_learning: bool = True
    enable_transfer_learning: bool = True
    enable_meta_learning: bool = True
    batch_size: int = 32
    learning_rate: float = 0.001
    experience_buffer_size: int = 1000
    min_confidence_for_learning: float = 0.6

@dataclass
class DecisionConfig:
    """Configuração do sistema de decisão"""
    min_confidence_threshold: float = 0.6
    risk_tolerance: float = 0.3
    enable_ethical_constraints: bool = True
    enable_risk_assessment: bool = True
    decision_timeout: float = 30.0
    max_alternatives: int = 5

@dataclass
class AutomationConfig:
    """Configuração do sistema de automação"""
    enable_automation: bool = True
    automation_interval: float = 1.0
    enable_self_monitoring: bool = True
    enable_auto_optimization: bool = True
    maintenance_interval: float = 300.0
    auto_save_interval: float = 600.0

@dataclass
class TradingConfig:
    """Configuração específica para trading"""
    enable_live_trading: bool = False
    enable_paper_trading: bool = True
    max_concurrent_trades: int = 5
    max_daily_trades: int = 50
    risk_per_trade: float = 0.02
    max_daily_risk: float = 0.05
    symbols: List[str] = None
    
    def __post_init__(self):
        if self.symbols is None:
            self.symbols = [
                'EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD',
                'BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'XRP'
            ]

@dataclass
class AISystemConfig:
    """Configuração completa do sistema de IA"""
    neural: NeuralConfig = None
    memory: MemoryConfig = None
    learning: LearningConfig = None
    decision: DecisionConfig = None
    automation: AutomationConfig = None
    trading: TradingConfig = None
    
    # Configurações gerais
    system_name: str = "LEXTRADER-IAG"
    version: str = "4.0.0"
    debug_mode: bool = False
    log_level: str = "INFO"
    data_directory: str = "data"
    models_directory: str = "models"
    logs_directory: str = "logs"
    
    def __post_init__(self):
        if self.neural is None:
            self.neural = NeuralConfig()
        if self.memory is None:
            self.memory = MemoryConfig()
        if self.learning is None:
            self.learning = LearningConfig()
        if self.decision is None:
            self.decision = DecisionConfig()
        if self.automation is None:
            self.automation = AutomationConfig()
        if self.trading is None:
            self.trading = TradingConfig()

class AIConfigManager:
    """Gerenciador de configuração da IA"""
    
    def __init__(self, config_path: str = "config/ai_config.yaml"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.config: AISystemConfig = AISystemConfig()
        self.config_history: List[Dict[str, Any]] = []
        
        # Carregar configuração existente
        self.load_config()
        
        logger.info(f"Gerenciador de configuração inicializado: {config_path}")
    
    def load_config(self) -> bool:
        """Carrega configuração do arquivo"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    if self.config_path.suffix.lower() == '.yaml':
                        config_data = yaml.safe_load(f)
                    else:
                        config_data = json.load(f)
                
                # Converter para objetos de configuração
                self.config = self._dict_to_config(config_data)
                logger.info("Configuração carregada com sucesso")
                return True
            else:
                # Criar configuração padrão
                self.save_config()
                logger.info("Configuração padrão criada")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return False
    
    def save_config(self) -> bool:
        """Salva configuração no arquivo"""
        try:
            # Adicionar timestamp ao histórico
            config_dict = asdict(self.config)
            config_dict['last_updated'] = datetime.now().isoformat()
            
            # Salvar histórico
            self.config_history.append({
                'timestamp': datetime.now().isoformat(),
                'config': config_dict.copy()
            })
            
            # Manter apenas últimas 10 configurações
            if len(self.config_history) > 10:
                self.config_history = self.config_history[-10:]
            
            # Salvar arquivo principal
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_path.suffix.lower() == '.yaml':
                    yaml.dump(config_dict, f, default_flow_style=False, 
                             allow_unicode=True, indent=2)
                else:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            # Salvar histórico
            history_path = self.config_path.parent / "config_history.json"
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_history, f, indent=2, ensure_ascii=False)
            
            logger.info("Configuração salva com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def _dict_to_config(self, config_data: Dict[str, Any]) -> AISystemConfig:
        """Converte dicionário para objeto de configuração"""
        # Extrair seções
        neural_data = config_data.get('neural', {})
        memory_data = config_data.get('memory', {})
        learning_data = config_data.get('learning', {})
        decision_data = config_data.get('decision', {})
        automation_data = config_data.get('automation', {})
        trading_data = config_data.get('trading', {})
        
        # Criar objetos de configuração
        neural_config = NeuralConfig(**neural_data)
        memory_config = MemoryConfig(**memory_data)
        learning_config = LearningConfig(**learning_data)
        decision_config = DecisionConfig(**decision_data)
        automation_config = AutomationConfig(**automation_data)
        trading_config = TradingConfig(**trading_data)
        
        # Extrair configurações gerais
        general_config = {k: v for k, v in config_data.items() 
                         if k not in ['neural', 'memory', 'learning', 'decision', 
                                    'automation', 'trading', 'last_updated']}
        
        return AISystemConfig(
            neural=neural_config,
            memory=memory_config,
            learning=learning_config,
            decision=decision_config,
            automation=automation_config,
            trading=trading_config,
            **general_config
        )
    
    def update_config(self, section: str, updates: Dict[str, Any]) -> bool:
        """Atualiza seção específica da configuração"""
        try:
            if hasattr(self.config, section):
                section_config = getattr(self.config, section)
                
                # Atualizar campos
                for key, value in updates.items():
                    if hasattr(section_config, key):
                        setattr(section_config, key, value)
                        logger.info(f"Configuração atualizada: {section}.{key} = {value}")
                    else:
                        logger.warning(f"Campo desconhecido: {section}.{key}")
                
                # Salvar configuração
                return self.save_config()
            else:
                logger.error(f"Seção desconhecida: {section}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao atualizar configuração: {e}")
            return False
    
    def get_config_section(self, section: str) -> Optional[Any]:
        """Retorna seção específica da configuração"""
        if hasattr(self.config, section):
            return getattr(self.config, section)
        return None
    
    def validate_config(self) -> Dict[str, List[str]]:
        """Valida configuração atual"""
        issues = {
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        # Validar configuração neural
        if self.config.neural.activation_threshold <= 0 or self.config.neural.activation_threshold > 1:
            issues['errors'].append("Neural: activation_threshold deve estar entre 0 e 1")
        
        if self.config.neural.learning_rate <= 0 or self.config.neural.learning_rate > 1:
            issues['warnings'].append("Neural: learning_rate muito alto pode causar instabilidade")
        
        # Validar configuração de memória
        if self.config.memory.working_memory_size < 3:
            issues['warnings'].append("Memory: working_memory_size muito baixo")
        
        if self.config.memory.cache_size < 100:
            issues['warnings'].append("Memory: cache_size muito baixo pode afetar performance")
        
        # Validar configuração de aprendizado
        if self.config.learning.batch_size < 1:
            issues['errors'].append("Learning: batch_size deve ser maior que 0")
        
        if self.config.learning.min_confidence_for_learning > 0.9:
            issues['warnings'].append("Learning: min_confidence_for_learning muito alto pode limitar aprendizado")
        
        # Validar configuração de decisão
        if self.config.decision.min_confidence_threshold > 0.9:
            issues['warnings'].append("Decision: min_confidence_threshold muito alto pode bloquear decisões")
        
        if self.config.decision.risk_tolerance > 0.8:
            issues['warnings'].append("Decision: risk_tolerance muito alto")
        
        # Validar configuração de trading
        if self.config.trading.enable_live_trading and self.config.trading.risk_per_trade > 0.05:
            issues['errors'].append("Trading: risk_per_trade muito alto para live trading")
        
        if self.config.trading.max_concurrent_trades > 20:
            issues['warnings'].append("Trading: max_concurrent_trades muito alto")
        
        # Informações gerais
        if self.config.debug_mode:
            issues['info'].append("Sistema em modo debug")
        
        if not self.config.automation.enable_automation:
            issues['info'].append("Automação desabilitada")
        
        return issues
    
    def reset_to_defaults(self) -> bool:
        """Reseta configuração para valores padrão"""
        try:
            self.config = AISystemConfig()
            return self.save_config()
        except Exception as e:
            logger.error(f"Erro ao resetar configuração: {e}")
            return False
    
    def export_config(self, export_path: str, format: str = 'yaml') -> bool:
        """Exporta configuração para arquivo"""
        try:
            export_path = Path(export_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            config_dict = asdict(self.config)
            config_dict['exported_at'] = datetime.now().isoformat()
            
            with open(export_path, 'w', encoding='utf-8') as f:
                if format.lower() == 'yaml':
                    yaml.dump(config_dict, f, default_flow_style=False, 
                             allow_unicode=True, indent=2)
                else:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuração exportada para: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar configuração: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Importa configuração de arquivo"""
        try:
            import_path = Path(import_path)
            
            if not import_path.exists():
                logger.error(f"Arquivo não encontrado: {import_path}")
                return False
            
            with open(import_path, 'r', encoding='utf-8') as f:
                if import_path.suffix.lower() == '.yaml':
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
            
            # Validar antes de importar
            temp_config = self._dict_to_config(config_data)
            
            # Se válido, aplicar
            self.config = temp_config
            success = self.save_config()
            
            if success:
                logger.info(f"Configuração importada de: {import_path}")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao importar configuração: {e}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Retorna resumo da configuração atual"""
        return {
            'system_info': {
                'name': self.config.system_name,
                'version': self.config.version,
                'debug_mode': self.config.debug_mode,
                'log_level': self.config.log_level
            },
            'neural_summary': {
                'activation_threshold': self.config.neural.activation_threshold,
                'learning_rate': self.config.neural.learning_rate,
                'plasticity_enabled': self.config.neural.plasticity_enabled
            },
            'memory_summary': {
                'working_memory_size': self.config.memory.working_memory_size,
                'cache_size': self.config.memory.cache_size,
                'auto_consolidation': self.config.memory.auto_consolidation
            },
            'learning_summary': {
                'online_learning': self.config.learning.enable_online_learning,
                'transfer_learning': self.config.learning.enable_transfer_learning,
                'meta_learning': self.config.learning.enable_meta_learning
            },
            'decision_summary': {
                'min_confidence': self.config.decision.min_confidence_threshold,
                'risk_tolerance': self.config.decision.risk_tolerance,
                'ethical_constraints': self.config.decision.enable_ethical_constraints
            },
            'automation_summary': {
                'enabled': self.config.automation.enable_automation,
                'interval': self.config.automation.automation_interval,
                'self_monitoring': self.config.automation.enable_self_monitoring
            },
            'trading_summary': {
                'live_trading': self.config.trading.enable_live_trading,
                'paper_trading': self.config.trading.enable_paper_trading,
                'max_concurrent_trades': self.config.trading.max_concurrent_trades,
                'risk_per_trade': self.config.trading.risk_per_trade
            }
        }

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def main():
    """Exemplo de uso do gerenciador de configuração"""
    # Criar gerenciador
    config_manager = AIConfigManager()
    
    # Validar configuração
    issues = config_manager.validate_config()
    print("Validação da configuração:")
    for level, messages in issues.items():
        if messages:
            print(f"{level.upper()}:")
            for msg in messages:
                print(f"  - {msg}")
    
    # Mostrar resumo
    summary = config_manager.get_config_summary()
    print(f"\nResumo da configuração:")
    for section, data in summary.items():
        print(f"{section}:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    
    # Exemplo de atualização
    config_manager.update_config('neural', {
        'learning_rate': 0.05,
        'activation_threshold': 0.6
    })
    
    # Exportar configuração
    config_manager.export_config('config/exported_config.yaml')
    
    print("\nGerenciador de configuração testado com sucesso!")

if __name__ == "__main__":
    main()