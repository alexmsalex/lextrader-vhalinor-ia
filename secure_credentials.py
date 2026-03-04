"""
🔐 GERENCIADOR SEGURO DE CREDENCIAIS PARA LEXTRADER-IAG 4.0

Módulo centralizado para gerenciamento seguro de credenciais de APIs,
com suporte a criptografia, validação e mascaramento.

Dependências:
    pip install python-dotenv cryptography

Uso:
    from neural_layers.config.secure_credentials import credentials
    
    # Acessar credenciais
    binance_key = credentials.binance.api_key
    
    # Validar todas as credenciais
    credentials.validate_all()
    
    # Obter dicionário seguro (mascarado)
    safe_config = credentials.get_safe_dict()
"""

import os
import json
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from pathlib import Path

# Configurar logging
logger = logging.getLogger(__name__)

# Carregar arquivo .env
load_dotenv()


@dataclass
class ExchangeConfig:
    """Configuração base para exchange/plataforma"""
    
    platform: str
    enabled: bool = True
    environment: str = "demo"  # demo ou live
    
    def validate(self):
        """Valida configuração básica"""
        if self.environment not in ["demo", "live"]:
            raise ValueError(f"Environment inválido: {self.environment}")
        return True


@dataclass
class BinanceConfig(ExchangeConfig):
    """Configuração Binance - Spot Trading"""
    
    api_key: str = "YOUR_BINANCE_API_KEY"
    api_secret: str = "YOUR_BINANCE_API_SECRET"
    testnet: bool = True
    platform: str = field(default="binance", init=False)
    
    def validate(self):
        """Valida credenciais Binance"""
        super().validate()
        
        if self.api_key == "YOUR_BINANCE_API_KEY":
            raise ValueError(
                "❌ Binance API Key não configurado.\n"
                "   Configure BINANCE_API_KEY em .env"
            )
        
        if self.api_secret == "YOUR_BINANCE_API_SECRET":
            raise ValueError(
                "❌ Binance API Secret não configurado.\n"
                "   Configure BINANCE_API_SECRET em .env"
            )
        
        if len(self.api_key) < 30:
            raise ValueError("❌ Binance API Key parece inválido (muito curto)")
        
        return True


@dataclass
class CTraderConfig(ExchangeConfig):
    """Configuração cTrader - Forex/CFD Trading"""
    
    client_id: str = "YOUR_CTRADER_CLIENT_ID"
    client_secret: str = "YOUR_CTRADER_CLIENT_SECRET"
    account_id: str = "YOUR_ACCOUNT_ID"
    username: str = ""
    password: str = ""
    platform: str = field(default="ctrader", init=False)
    environment: str = "demo"
    
    def validate(self):
        """Valida credenciais cTrader"""
        super().validate()
        
        if self.client_id == "YOUR_CTRADER_CLIENT_ID":
            raise ValueError(
                "❌ cTrader Client ID não configurado.\n"
                "   Configure CTRADER_CLIENT_ID em .env"
            )
        
        if self.client_secret == "YOUR_CTRADER_CLIENT_SECRET":
            raise ValueError(
                "❌ cTrader Client Secret não configurado.\n"
                "   Configure CTRADER_CLIENT_SECRET em .env"
            )
        
        return True


@dataclass
class PionexConfig(ExchangeConfig):
    """Configuração Pionex - Crypto Trading Bot Platform"""
    
    api_key: str = "YOUR_PIONEX_API_KEY"
    api_secret: str = "YOUR_PIONEX_API_SECRET"
    api_type: str = "spot"  # spot ou futures
    platform: str = field(default="pionex", init=False)
    
    def validate(self):
        """Valida credenciais Pionex"""
        super().validate()
        
        if self.api_key == "YOUR_PIONEX_API_KEY":
            raise ValueError(
                "❌ Pionex API Key não configurado.\n"
                "   Configure PIONEX_API_KEY em .env"
            )
        
        if self.api_secret == "YOUR_PIONEX_API_SECRET":
            raise ValueError(
                "❌ Pionex API Secret não configurado.\n"
                "   Configure PIONEX_API_SECRET em .env"
            )
        
        return True


@dataclass
class CoinbaseConfig(ExchangeConfig):
    """Configuração Coinbase - Crypto Exchange"""
    
    api_key: str = "YOUR_COINBASE_API_KEY"
    api_secret: str = "YOUR_COINBASE_API_SECRET"
    passphrase: str = "YOUR_PASSPHRASE"
    sandbox: bool = True
    platform: str = field(default="coinbase", init=False)
    
    def validate(self):
        """Valida credenciais Coinbase"""
        super().validate()
        
        if self.api_key == "YOUR_COINBASE_API_KEY":
            logger.warning("⚠️  Coinbase API Key não configurado (opcional)")
        
        return True


@dataclass
class DataProviderConfig:
    """Configuração de provedores de dados"""
    
    alphavantage: str = "YOUR_ALPHAVANTAGE_KEY"
    polygon: str = "YOUR_POLYGON_KEY"
    twelvedata: str = "YOUR_TWELVEDATA_KEY"
    newsapi: str = "YOUR_NEWSAPI_KEY"
    
    def validate(self):
        """Valida configuração de provedores"""
        missing = []
        
        if self.alphavantage == "YOUR_ALPHAVANTAGE_KEY":
            missing.append("ALPHAVANTAGE_KEY")
        
        if missing:
            logger.warning(f"⚠️  Provedores de dados não configurados: {', '.join(missing)}")
        
        return True


class EncryptedCredentialsManager:
    """Gerenciador seguro de credenciais com criptografia Fernet"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Inicializa o gerenciador de credenciais criptografadas
        
        Args:
            encryption_key: Chave Fernet (padrão: variável de ambiente ENCRYPTION_KEY)
        
        Raises:
            ValueError: Se chave não for válida
        """
        key_str = encryption_key or os.getenv("ENCRYPTION_KEY", "")
        
        if not key_str:
            logger.warning("⚠️  ENCRYPTION_KEY não configurado - criptografia desabilitada")
            self.cipher = None
            return
        
        try:
            # Remover espaços em branco
            key_str = key_str.strip()
            
            # Converter para bytes se necessário
            if isinstance(key_str, str):
                key_bytes = key_str.encode('utf-8')
            else:
                key_bytes = key_str
            
            self.cipher = Fernet(key_bytes)
            logger.info("✅ Gerenciador de criptografia inicializado com sucesso")
        
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar criptografia: {e}")
            raise ValueError(f"Chave de criptografia inválida: {e}")
    
    def encrypt(self, value: str) -> str:
        """
        Criptografa um valor
        
        Args:
            value: Valor a criptografar
        
        Returns:
            Valor criptografado em base64
        """
        if not self.cipher:
            return value
        
        try:
            encrypted = self.cipher.encrypt(value.encode('utf-8'))
            return encrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Erro ao criptografar: {e}")
            return value
    
    def decrypt(self, encrypted_value: str) -> str:
        """
        Descriptografa um valor
        
        Args:
            encrypted_value: Valor criptografado
        
        Returns:
            Valor descriptografado
        """
        if not self.cipher:
            return encrypted_value
        
        try:
            decrypted = self.cipher.decrypt(encrypted_value.encode('utf-8'))
            return decrypted.decode('utf-8')
        except InvalidToken:
            logger.error("❌ Token de criptografia inválido")
            return encrypted_value
        except Exception as e:
            logger.error(f"Erro ao descriptografar: {e}")
            return encrypted_value


class CredentialsConfig:
    """
    Gerenciador centralizado de todas as credenciais do sistema
    
    Carrega credenciais de variáveis de ambiente e fornece acesso
    seguro com validação e mascaramento.
    """
    
    def __init__(self):
        """Inicializa carregando credenciais do .env"""
        
        # Instanciar gerenciador de criptografia
        self.crypto = EncryptedCredentialsManager()
        
        # BINANCE
        self.binance = BinanceConfig(
            api_key=os.getenv("BINANCE_API_KEY", "YOUR_BINANCE_API_KEY"),
            api_secret=os.getenv("BINANCE_API_SECRET", "YOUR_BINANCE_API_SECRET"),
            testnet=os.getenv("BINANCE_TESTNET", "true").lower() == "true",
            environment="testnet" if os.getenv("BINANCE_TESTNET", "true").lower() == "true" else "live"
        )
        
        # CTRADER
        self.ctrader = CTraderConfig(
            client_id=os.getenv("CTRADER_CLIENT_ID", "YOUR_CTRADER_CLIENT_ID"),
            client_secret=os.getenv("CTRADER_CLIENT_SECRET", "YOUR_CTRADER_CLIENT_SECRET"),
            account_id=os.getenv("CTRADER_ACCOUNT_ID", "YOUR_ACCOUNT_ID"),
            username=os.getenv("CTRADER_USERNAME", ""),
            password=os.getenv("CTRADER_PASSWORD", ""),
            environment=os.getenv("CTRADER_ENVIRONMENT", "demo")
        )
        
        # PIONEX
        self.pionex = PionexConfig(
            api_key=os.getenv("PIONEX_API_KEY", "YOUR_PIONEX_API_KEY"),
            api_secret=os.getenv("PIONEX_API_SECRET", "YOUR_PIONEX_API_SECRET"),
            api_type=os.getenv("PIONEX_API_TYPE", "spot")
        )
        
        # COINBASE (opcional)
        self.coinbase = CoinbaseConfig(
            api_key=os.getenv("COINBASE_API_KEY", "YOUR_COINBASE_API_KEY"),
            api_secret=os.getenv("COINBASE_API_SECRET", "YOUR_COINBASE_API_SECRET"),
            passphrase=os.getenv("COINBASE_PASSPHRASE", "YOUR_PASSPHRASE"),
            sandbox=os.getenv("COINBASE_SANDBOX", "true").lower() == "true"
        )
        
        # PROVEDORES DE DADOS
        self.data_providers = DataProviderConfig(
            alphavantage=os.getenv("ALPHAVANTAGE_KEY", "YOUR_ALPHAVANTAGE_KEY"),
            polygon=os.getenv("POLYGON_KEY", "YOUR_POLYGON_KEY"),
            twelvedata=os.getenv("TWELVEDATA_KEY", "YOUR_TWELVEDATA_KEY"),
            newsapi=os.getenv("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY")
        )
        
        # SEGURANÇA
        self.log_credentials = os.getenv("LOG_CREDENTIALS", "false").lower() == "true"
        self.session_timeout = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
        self.enable_2fa = os.getenv("ENABLE_2FA", "false").lower() == "true"
    
    def validate_all(self) -> bool:
        """
        Valida todas as configurações críticas
        
        Returns:
            True se todas as validações passarem
        
        Raises:
            ValueError: Se alguma credencial crítica não estiver configurada
        """
        errors = []
        
        # Validar Binance
        try:
            self.binance.validate()
            logger.info("✅ Binance: Validado")
        except ValueError as e:
            errors.append(str(e))
        
        # Validar cTrader
        try:
            self.ctrader.validate()
            logger.info("✅ cTrader: Validado")
        except ValueError as e:
            errors.append(str(e))
        
        # Validar Pionex
        try:
            self.pionex.validate()
            logger.info("✅ Pionex: Validado")
        except ValueError as e:
            errors.append(str(e))
        
        # Validar provedores
        try:
            self.data_providers.validate()
            logger.info("✅ Data Providers: Verificado")
        except ValueError as e:
            errors.append(str(e))
        
        if errors:
            error_msg = "\n".join(errors)
            logger.error(f"\n❌ Erros de Configuração:\n{error_msg}")
            raise ValueError(f"Configuração inválida: {error_msg}")
        
        logger.info("✅ Todas as configurações validadas com sucesso!")
        return True
    
    def mask_credential(self, value: str, visible: int = 8) -> str:
        """
        Mascara uma credencial para logging seguro
        
        Args:
            value: Valor a mascarar
            visible: Número de caracteres visíveis no início
        
        Returns:
            Valor mascarado (ex: qwertyuiop***)
        """
        if not value or len(value) <= visible:
            return "***"
        
        return f"{value[:visible]}***"
    
    def get_safe_dict(self) -> Dict[str, Any]:
        """
        Retorna dicionário de configuração com todas as credenciais mascaradas
        
        Seguro para logging e exibição
        
        Returns:
            Dicionário com credenciais mascaradas
        """
        return {
            "environment": {
                "LOG_CREDENTIALS": self.log_credentials,
                "SESSION_TIMEOUT_MINUTES": self.session_timeout,
                "ENABLE_2FA": self.enable_2fa,
                "ENCRYPTION_ENABLED": self.crypto.cipher is not None
            },
            "exchanges": {
                "binance": {
                    "api_key": self.mask_credential(self.binance.api_key),
                    "testnet": self.binance.testnet,
                    "environment": self.binance.environment
                },
                "ctrader": {
                    "client_id": self.mask_credential(self.ctrader.client_id),
                    "environment": self.ctrader.environment,
                    "account_configured": bool(self.ctrader.account_id and 
                                              not self.ctrader.account_id.startswith("YOUR_"))
                },
                "pionex": {
                    "api_key": self.mask_credential(self.pionex.api_key),
                    "api_type": self.pionex.api_type
                },
                "coinbase": {
                    "api_key": self.mask_credential(self.coinbase.api_key),
                    "sandbox": self.coinbase.sandbox
                }
            },
            "data_providers": {
                "alphavantage": "configured" if not self.data_providers.alphavantage.startswith("YOUR_") else "NOT_SET",
                "polygon": "configured" if not self.data_providers.polygon.startswith("YOUR_") else "NOT_SET",
                "twelvedata": "configured" if not self.data_providers.twelvedata.startswith("YOUR_") else "NOT_SET",
                "newsapi": "configured" if not self.data_providers.newsapi.startswith("YOUR_") else "NOT_SET"
            }
        }
    
    def get_status(self) -> Dict[str, bool]:
        """
        Obtém status de configuração de cada plataforma
        
        Returns:
            Dicionário com status de cada plataforma
        """
        return {
            "binance": not self.binance.api_key.startswith("YOUR_"),
            "ctrader": not self.ctrader.client_id.startswith("YOUR_"),
            "pionex": not self.pionex.api_key.startswith("YOUR_"),
            "coinbase": not self.coinbase.api_key.startswith("YOUR_"),
            "encryption": self.crypto.cipher is not None
        }


# Instância global de configuração
credentials = CredentialsConfig()


def print_status():
    """Exibe status de configuração no console"""
    print("\n" + "="*70)
    print("🔐 STATUS DE CONFIGURAÇÃO - LEXTRADER-IAG 4.0")
    print("="*70)
    
    status = credentials.get_status()
    safe_config = credentials.get_safe_dict()
    
    print("\n📊 EXCHANGES:")
    for exchange, configured in status.items():
        if exchange != "encryption":
            symbol = "✅" if configured else "❌"
            print(f"  {symbol} {exchange.upper()}")
    
    print("\n🔒 SEGURANÇA:")
    encryption = status.get("encryption")
    symbol = "✅" if encryption else "⚠️"
    print(f"  {symbol} Criptografia: {'Ativa' if encryption else 'Inativa'}")
    
    print("\n📋 DETALHES (Mascarados):")
    print(json.dumps(safe_config, indent=2, ensure_ascii=False))
    
    print("="*70 + "\n")


def validate_and_report():
    """Valida configurações e gera relatório"""
    print("\n" + "="*70)
    print("🔍 VALIDAÇÃO DE CONFIGURAÇÕES")
    print("="*70 + "\n")
    
    try:
        credentials.validate_all()
        print_status()
        print("✅ Sistema pronto para operação!")
        return True
    
    except ValueError as e:
        print(f"\n❌ Erro de Configuração:\n{e}\n")
        print("📝 Próximos passos:")
        print("  1. Crie arquivo .env na raiz do projeto")
        print("  2. Copie conteúdo de .env.example")
        print("  3. Preencha com suas credenciais reais")
        print("  4. Execute este script novamente\n")
        return False


if __name__ == "__main__":
    validate_and_report()
