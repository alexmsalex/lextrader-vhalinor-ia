import json
import hashlib
import uuid
import secrets
import time
from datetime import datetime
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import os
import pickle
import base64
from cryptography.fernet import Fernet
import getpass

class Theme(Enum):
    MATRIX = 'matrix'
    DARK = 'dark'
    LIGHT = 'light'
    OCEAN = 'ocean'
    CYBER = 'cyber'

@dataclass
class UserSettings:
    theme: Theme = Theme.MATRIX
    notifications: bool = True
    auto_trading: bool = False
    risk_level: str = 'medium'
    language: str = 'pt-BR'
    show_advanced: bool = False
    two_factor_auth: bool = False
    session_timeout: int = 3600  # segundos
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'theme': self.theme.value,
            'notifications': self.notifications,
            'auto_trading': self.auto_trading,
            'risk_level': self.risk_level,
            'language': self.language,
            'show_advanced': self.show_advanced,
            'two_factor_auth': self.two_factor_auth,
            'session_timeout': self.session_timeout
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserSettings':
        return cls(
            theme=Theme(data.get('theme', 'matrix')),
            notifications=data.get('notifications', True),
            auto_trading=data.get('auto_trading', False),
            risk_level=data.get('risk_level', 'medium'),
            language=data.get('language', 'pt-BR'),
            show_advanced=data.get('show_advanced', False),
            two_factor_auth=data.get('two_factor_auth', False),
            session_timeout=data.get('session_timeout', 3600)
        )

@dataclass
class UserProfile:
    id: str
    username: str
    email: Optional[str]
    password_hash: str
    salt: str
    neural_signature: str
    created_at: float
    last_login: float
    settings: UserSettings
    login_count: int = 0
    is_active: bool = True
    failed_attempts: int = 0
    last_failed_attempt: Optional[float] = None
    roles: list = None
    
    def __post_init__(self):
        if self.roles is None:
            self.roles = ['user']
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'neural_signature': self.neural_signature,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'settings': self.settings.to_dict(),
            'login_count': self.login_count,
            'is_active': self.is_active,
            'failed_attempts': self.failed_attempts,
            'last_failed_attempt': self.last_failed_attempt,
            'roles': self.roles
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(
            id=data['id'],
            username=data['username'],
            email=data.get('email'),
            password_hash=data['password_hash'],
            salt=data['salt'],
            neural_signature=data['neural_signature'],
            created_at=data['created_at'],
            last_login=data['last_login'],
            settings=UserSettings.from_dict(data['settings']),
            login_count=data.get('login_count', 0),
            is_active=data.get('is_active', True),
            failed_attempts=data.get('failed_attempts', 0),
            last_failed_attempt=data.get('last_failed_attempt'),
            roles=data.get('roles', ['user'])
        )

class UserStorageService:
    def __init__(self, storage_file: str = 'users_vault.json'):
        self.STORAGE_KEY = 'LEXTRADER_USERS_VAULT_V3'
        self.storage_file = storage_file
        self.users_cache: Dict[str, UserProfile] = {}
        self.current_user: Optional[UserProfile] = None
        self.session_token: Optional[str] = None
        self.session_expiry: Optional[float] = None
        self.encryption_key = None
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Inicializa o sistema de armazenamento"""
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(self.storage_file) if os.path.dirname(self.storage_file) else '.', exist_ok=True)
        
        # Carregar chave de encriptação
        self._load_encryption_key()
        
        # Carregar usuários
        self._load_users()
    
    def _load_encryption_key(self):
        """Carrega ou gera chave de encriptação"""
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
    
    def _encrypt_data(self, data: str) -> str:
        """Encripta dados sensíveis"""
        if not self.encryption_key:
            return data
        fernet = Fernet(self.encryption_key)
        return base64.urlsafe_b64encode(fernet.encrypt(data.encode())).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decripta dados sensíveis"""
        if not self.encryption_key:
            return encrypted_data
        try:
            fernet = Fernet(self.encryption_key)
            decrypted = fernet.decrypt(base64.urlsafe_b64decode(encrypted_data))
            return decrypted.decode()
        except:
            return encrypted_data
    
    def _generate_salt(self) -> str:
        """Gera um salt criptográfico"""
        return secrets.token_hex(16)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Gera hash da senha usando SHA-256 com salt"""
        # Usar PBKDF2 para maior segurança
        password_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        
        # Usar algoritmo mais seguro
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            100000,  # Número de iterações
            dklen=32  # Tamanho da chave
        )
        return key.hex()
    
    def _generate_neural_signature(self) -> str:
        """Gera uma assinatura neural única"""
        timestamp = int(time.time() * 1000)
        random_part = secrets.token_hex(4).upper()
        return f"NS-{timestamp:016X}-{random_part}"
    
    def _save_users(self):
        """Salva usuários no armazenamento persistente"""
        try:
            users_dict = {username: user.to_dict() for username, user in self.users_cache.items()}
            
            # Encriptar dados sensíveis antes de salvar
            for user_data in users_dict.values():
                user_data['password_hash'] = self._encrypt_data(user_data['password_hash'])
                user_data['salt'] = self._encrypt_data(user_data['salt'])
            
            with open(self.storage_file, 'w') as f:
                json.dump(users_dict, f, indent=2)
            
            # Backup opcional
            self._create_backup()
            
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")
    
    def _load_users(self):
        """Carrega usuários do armazenamento persistente"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    users_dict = json.load(f)
                
                # Decriptar dados sensíveis
                for username, user_data in users_dict.items():
                    user_data['password_hash'] = self._decrypt_data(user_data['password_hash'])
                    user_data['salt'] = self._decrypt_data(user_data['salt'])
                    self.users_cache[username] = UserProfile.from_dict(user_data)
            else:
                self.users_cache = {}
                # Criar usuário admin padrão
                self._create_default_admin()
                
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.users_cache = {}
            self._create_default_admin()
    
    def _create_default_admin(self):
        """Cria um usuário administrador padrão"""
        admin_profile = UserProfile(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@lextrader.ai",
            password_hash=self._hash_password("admin123", "default_salt"),
            salt="default_salt",
            neural_signature=self._generate_neural_signature(),
            created_at=time.time(),
            last_login=time.time(),
            settings=UserSettings(theme=Theme.MATRIX, auto_trading=True),
            login_count=1,
            roles=['admin', 'user']
        )
        self.users_cache["admin"] = admin_profile
        self._save_users()
    
    def _create_backup(self):
        """Cria backup dos dados de usuário"""
        try:
            backup_file = f"{self.storage_file}.backup.{int(time.time())}"
            import shutil
            shutil.copy2(self.storage_file, backup_file)
            
            # Manter apenas os 5 backups mais recentes
            backups = sorted([f for f in os.listdir('.') if f.startswith(f"{self.storage_file}.backup.")])
            for old_backup in backups[:-5]:
                os.remove(old_backup)
                
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
    
    def _validate_password_strength(self, password: str) -> tuple[bool, str]:
        """Valida a força da senha"""
        if len(password) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        
        if not any(c.isupper() for c in password):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        
        if not any(c.islower() for c in password):
            return False, "Senha deve conter pelo menos uma letra minúscula"
        
        if not any(c.isdigit() for c in password):
            return False, "Senha deve conter pelo menos um número"
        
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in password):
            return False, "Senha deve conter pelo menos um caractere especial"
        
        return True, "Senha válida"
    
    def _is_account_locked(self, username: str) -> bool:
        """Verifica se a conta está bloqueada por muitas tentativas falhas"""
        user = self.users_cache.get(username)
        if not user:
            return False
        
        # Resetar tentativas se passou muito tempo
        if user.last_failed_attempt and (time.time() - user.last_failed_attempt) > 1800:  # 30 minutos
            user.failed_attempts = 0
            user.last_failed_attempt = None
            self.users_cache[username] = user
            self._save_users()
            return False
        
        # Bloquear após 5 tentativas falhas
        return user.failed_attempts >= 5
    
    def register_user(self, username: str, password: str, email: Optional[str] = None) -> UserProfile:
        """Registra um novo usuário"""
        print(f"🔐 Registrando identidade neural: {username}")
        
        # Validar nome de usuário
        if not username or len(username) < 3:
            raise ValueError("Nome de usuário deve ter pelo menos 3 caracteres")
        
        if username in self.users_cache:
            raise ValueError("Identidade neural já registrada")
        
        # Validar força da senha
        is_valid, message = self._validate_password_strength(password)
        if not is_valid:
            raise ValueError(f"Senha fraca: {message}")
        
        # Validar email se fornecido
        if email and '@' not in email:
            raise ValueError("Email inválido")
        
        # Gerar salt e hash da senha
        salt = self._generate_salt()
        password_hash = self._hash_password(password, salt)
        
        # Criar perfil do usuário
        new_user = UserProfile(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt,
            neural_signature=self._generate_neural_signature(),
            created_at=time.time(),
            last_login=time.time(),
            settings=UserSettings(),
            login_count=1
        )
        
        # Salvar usuário
        self.users_cache[username] = new_user
        self._save_users()
        
        print(f"✅ Identidade neural {username} registrada com sucesso!")
        print(f"   Assinatura Neural: {new_user.neural_signature}")
        print(f"   Criado em: {datetime.fromtimestamp(new_user.created_at).strftime('%d/%m/%Y %H:%M:%S')}")
        
        return new_user
    
    def authenticate_user(self, username: str, password: str) -> Optional[UserProfile]:
        """Autentica um usuário"""
        print(f"🔐 Autenticando identidade neural: {username}")
        
        # Simular delay para efeito de segurança
        time.sleep(0.8)
        
        # Verificar se conta está bloqueada
        if self._is_account_locked(username):
            print("❌ Conta temporariamente bloqueada devido a muitas tentativas falhas")
            return None
        
        user = self.users_cache.get(username)
        if not user:
            # Tentativa falha para usuário inexistente também registra
            print("❌ Identidade neural não encontrada")
            return None
        
        # Verificar se conta está ativa
        if not user.is_active:
            print("❌ Conta desativada")
            return None
        
        # Verificar senha
        password_hash = self._hash_password(password, user.salt)
        
        if password_hash == user.password_hash:
            # Login bem-sucedido
            user.last_login = time.time()
            user.login_count += 1
            user.failed_attempts = 0
            user.last_failed_attempt = None
            
            # Gerar token de sessão
            self.current_user = user
            self.session_token = secrets.token_urlsafe(32)
            self.session_expiry = time.time() + user.settings.session_timeout
            
            self.users_cache[username] = user
            self._save_users()
            
            print(f"✅ Autenticação bem-sucedida!")
            print(f"   Bem-vindo, {user.username}!")
            print(f"   Login #{user.login_count}")
            print(f"   Assinatura Neural: {user.neural_signature}")
            
            return user
        else:
            # Login falhou
            user.failed_attempts += 1
            user.last_failed_attempt = time.time()
            self.users_cache[username] = user
            self._save_users()
            
            print(f"❌ Autenticação falhou - Tentativa #{user.failed_attempts}")
            
            # Notificar sobre bloqueio iminente
            if user.failed_attempts >= 3:
                remaining = 5 - user.failed_attempts
                print(f"⚠️  Atenção: {remaining} tentativa(s) restante(s) antes do bloqueio da conta")
            
            return None
    
    def logout(self):
        """Encerra a sessão do usuário atual"""
        if self.current_user:
            print(f"👋 Até logo, {self.current_user.username}!")
            self.current_user = None
            self.session_token = None
            self.session_expiry = None
        else:
            print("Nenhuma sessão ativa para encerrar")
    
    def validate_session(self) -> bool:
        """Valida se a sessão atual é válida"""
        if not self.current_user or not self.session_token or not self.session_expiry:
            return False
        
        if time.time() > self.session_expiry:
            print("⏰ Sessão expirada")
            self.logout()
            return False
        
        # Renovar sessão se estiver perto de expirar
        if time.time() > (self.session_expiry - 300):  # 5 minutos antes de expirar
            self.session_expiry = time.time() + self.current_user.settings.session_timeout
            print("🔄 Sessão renovada")
        
        return True
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Altera a senha do usuário"""
        user = self.users_cache.get(username)
        if not user:
            return False
        
        # Verificar senha antiga
        old_hash = self._hash_password(old_password, user.salt)
        if old_hash != user.password_hash:
            print("❌ Senha atual incorreta")
            return False
        
        # Validar nova senha
        is_valid, message = self._validate_password_strength(new_password)
        if not is_valid:
            print(f"❌ {message}")
            return False
        
        # Gerar novo salt e hash
        new_salt = self._generate_salt()
        new_hash = self._hash_password(new_password, new_salt)
        
        # Atualizar usuário
        user.password_hash = new_hash
        user.salt = new_salt
        self.users_cache[username] = user
        self._save_users()
        
        print("✅ Senha alterada com sucesso!")
        return True
    
    def update_user_settings(self, username: str, settings: UserSettings) -> bool:
        """Atualiza as configurações do usuário"""
        user = self.users_cache.get(username)
        if not user:
            return False
        
        user.settings = settings
        self.users_cache[username] = user
        self._save_users()
        
        print(f"✅ Configurações de {username} atualizadas")
        return True
    
    def get_user_public_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Obtém informações públicas do usuário"""
        user = self.users_cache.get(username)
        if not user:
            return None
        
        # Remover dados sensíveis
        user_dict = user.to_dict()
        user_dict.pop('password_hash', None)
        user_dict.pop('salt', None)
        user_dict.pop('failed_attempts', None)
        user_dict.pop('last_failed_attempt', None)
        
        return user_dict
    
    def list_all_users(self) -> list[Dict[str, Any]]:
        """Lista todos os usuários (apenas informações públicas)"""
        users_list = []
        for username, user in self.users_cache.items():
            public_info = self.get_user_public_info(username)
            if public_info:
                users_list.append(public_info)
        
        return sorted(users_list, key=lambda x: x.get('last_login', 0), reverse=True)
    
    def deactivate_user(self, username: str, admin_username: str) -> bool:
        """Desativa um usuário (apenas admin)"""
        admin = self.users_cache.get(admin_username)
        if not admin or 'admin' not in admin.roles:
            print("❌ Apenas administradores podem desativar usuários")
            return False
        
        user = self.users_cache.get(username)
        if not user:
            print(f"❌ Usuário {username} não encontrado")
            return False
        
        user.is_active = False
        self.users_cache[username] = user
        self._save_users()
        
        print(f"✅ Usuário {username} desativado")
        return True
    
    def reset_password(self, username: str, email: str) -> bool:
        """Inicia processo de recuperação de senha"""
        user = self.users_cache.get(username)
        if not user or user.email != email:
            print("❌ Usuário ou email não correspondem")
            return False
        
        # Gerar token de recuperação
        reset_token = secrets.token_urlsafe(16)
        reset_expiry = time.time() + 3600  # 1 hora
        
        # Em um sistema real, enviaria email com o token
        print(f"📧 Token de recuperação (SIMULAÇÃO): {reset_token}")
        print(f"⚠️  Token válido por 1 hora")
        
        # Aqui normalmente salvaria o token no banco de dados
        # Por simplicidade, retornamos o token
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema de usuários"""
        total_users = len(self.users_cache)
        active_users = sum(1 for user in self.users_cache.values() if user.is_active)
        today = datetime.now().date()
        logins_today = sum(1 for user in self.users_cache.values() 
                          if datetime.fromtimestamp(user.last_login).date() == today)
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'logins_today': logins_today,
            'storage_file': self.storage_file,
            'cache_size': len(self.users_cache)
        }


# Instância global do serviço
user_storage = UserStorageService()


# Interface de linha de comando para interação
class UserCLI:
    """Interface de linha de comando para gerenciamento de usuários"""
    
    def __init__(self, storage_service: UserStorageService):
        self.storage = storage_service
        self.running = True
    
    def run(self):
        """Executa a interface CLI"""
        print("=" * 60)
        print("🔐 LEXTRADER - Gerenciamento de Identidades Neurais")
        print("=" * 60)
        
        while self.running:
            if self.storage.current_user:
                self._show_main_menu()
            else:
                self._show_auth_menu()
    
    def _show_auth_menu(self):
        """Menu de autenticação"""
        print("\n" + "=" * 40)
        print("MENU DE AUTENTICAÇÃO")
        print("=" * 40)
        print("1. 🔐 Login")
        print("2. 📝 Registrar")
        print("3. 🔑 Recuperar Senha")
        print("4. 📊 Estatísticas")
        print("5. ❌ Sair")
        print("=" * 40)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            self._login()
        elif choice == "2":
            self._register()
        elif choice == "3":
            self._recover_password()
        elif choice == "4":
            self._show_statistics()
        elif choice == "5":
            self.running = False
            print("\n👋 Até logo!")
        else:
            print("❌ Opção inválida!")
    
    def _show_main_menu(self):
        """Menu principal após login"""
        user = self.storage.current_user
        print(f"\n" + "=" * 40)
        print(f"👤 {user.username} | Assinatura: {user.neural_signature[:12]}...")
        print("=" * 40)
        print("1. 👁️  Ver Perfil")
        print("2. ⚙️  Configurações")
        print("3. 🔑 Alterar Senha")
        print("4. 👥 Listar Usuários (Admin)")
        print("5. 🚪 Logout")
        print("=" * 40)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            self._show_profile()
        elif choice == "2":
            self._manage_settings()
        elif choice == "3":
            self._change_password()
        elif choice == "4":
            self._list_users()
        elif choice == "5":
            self.storage.logout()
        else:
            print("❌ Opção inválida!")
    
    def _login(self):
        """Interface de login"""
        print("\n" + "=" * 30)
        print("🔐 LOGIN")
        print("=" * 30)
        
        username = input("Identidade Neural: ").strip()
        password = getpass.getpass("Senha: ").strip()
        
        user = self.storage.authenticate_user(username, password)
        if user:
            print(f"\n✅ Bem-vindo de volta, {user.username}!")
        else:
            print("\n❌ Falha na autenticação")
    
    def _register(self):
        """Interface de registro"""
        print("\n" + "=" * 30)
        print("📝 REGISTRO DE IDENTIDADE NEURAL")
        print("=" * 30)
        
        username = input("Escolha seu Identificador Neural: ").strip()
        email = input("Email (opcional): ").strip() or None
        
        while True:
            password = getpass.getpass("Crie sua senha: ").strip()
            confirm = getpass.getpass("Confirme a senha: ").strip()
            
            if password != confirm:
                print("❌ Senhas não coincidem. Tente novamente.")
                continue
            
            try:
                user = self.storage.register_user(username, password, email)
                print(f"\n🎉 Registro concluído com sucesso!")
                print(f"   Seu ID: {user.id}")
                print(f"   Sua Assinatura Neural: {user.neural_signature}")
                break
            except ValueError as e:
                print(f"❌ Erro: {e}")
                retry = input("Tentar novamente? (s/n): ").strip().lower()
                if retry != 's':
                    break
    
    def _show_profile(self):
        """Mostra perfil do usuário atual"""
        user = self.storage.current_user
        if not user:
            return
        
        print("\n" + "=" * 40)
        print(f"👤 PERFIL: {user.username}")
        print("=" * 40)
        
        created_date = datetime.fromtimestamp(user.created_at).strftime('%d/%m/%Y %H:%M:%S')
        last_login_date = datetime.fromtimestamp(user.last_login).strftime('%d/%m/%Y %H:%M:%S')
        
        print(f"ID: {user.id}")
        print(f"Email: {user.email or 'Não informado'}")
        print(f"Assinatura Neural: {user.neural_signature}")
        print(f"Criado em: {created_date}")
        print(f"Último login: {last_login_date}")
        print(f"Total de logins: {user.login_count}")
        print(f"Status: {'🟢 Ativo' if user.is_active else '🔴 Inativo'}")
        print(f"Funções: {', '.join(user.roles)}")
        
        input("\nPressione Enter para continuar...")
    
    def _manage_settings(self):
        """Gerencia configurações do usuário"""
        user = self.storage.current_user
        if not user:
            return
        
        print("\n" + "=" * 40)
        print("⚙️  CONFIGURAÇÕES")
        print("=" * 40)
        
        print(f"Tema atual: {user.settings.theme.value}")
        print(f"Notificações: {'✅ Ativadas' if user.settings.notifications else '❌ Desativadas'}")
        print(f"Auto Trading: {'✅ Ativado' if user.settings.auto_trading else '❌ Desativado'}")
        print(f"Nível de Risco: {user.settings.risk_level}")
        print(f"Idioma: {user.settings.language}")
        print(f"Timeout da Sessão: {user.settings.session_timeout // 60} minutos")
        
        print("\n1. Alterar Tema")
        print("2. Alternar Notificações")
        print("3. Alternar Auto Trading")
        print("4. Alterar Nível de Risco")
        print("5. Voltar")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            self._change_theme()
        elif choice == "2":
            user.settings.notifications = not user.settings.notifications
            self.storage.update_user_settings(user.username, user.settings)
        elif choice == "3":
            user.settings.auto_trading = not user.settings.auto_trading
            self.storage.update_user_settings(user.username, user.settings)
        elif choice == "4":
            self._change_risk_level()
    
    def _change_theme(self):
        """Altera o tema da interface"""
        user = self.storage.current_user
        if not user:
            return
        
        print("\n🎨 Temas disponíveis:")
        for i, theme in enumerate(Theme, 1):
            print(f"{i}. {theme.value}")
        
        try:
            choice = int(input("\nEscolha um tema: ").strip()) - 1
            if 0 <= choice < len(Theme):
                theme = list(Theme)[choice]
                user.settings.theme = theme
                self.storage.update_user_settings(user.username, user.settings)
                print(f"✅ Tema alterado para: {theme.value}")
        except (ValueError, IndexError):
            print("❌ Escolha inválida")
    
    def _change_risk_level(self):
        """Altera o nível de risco"""
        user = self.storage.current_user
        if not user:
            return
        
        print("\n⚠️  Níveis de Risco:")
        print("1. Baixo (Conservador)")
        print("2. Médio (Balanceado)")
        print("3. Alto (Agressivo)")
        
        choice = input("\nEscolha um nível: ").strip()
        
        if choice == "1":
            user.settings.risk_level = 'low'
        elif choice == "2":
            user.settings.risk_level = 'medium'
        elif choice == "3":
            user.settings.risk_level = 'high'
        else:
            print("❌ Escolha inválida")
            return
        
        self.storage.update_user_settings(user.username, user.settings)
        print(f"✅ Nível de risco alterado para: {user.settings.risk_level}")
    
    def _change_password(self):
        """Interface para alterar senha"""
        user = self.storage.current_user
        if not user:
            return
        
        print("\n" + "=" * 30)
        print("🔑 ALTERAR SENHA")
        print("=" * 30)
        
        old_password = getpass.getpass("Senha atual: ").strip()
        new_password = getpass.getpass("Nova senha: ").strip()
        confirm_password = getpass.getpass("Confirme a nova senha: ").strip()
        
        if new_password != confirm_password:
            print("❌ As novas senhas não coincidem")
            return
        
        success = self.storage.change_password(user.username, old_password, new_password)
        if success:
            print("✅ Senha alterada com sucesso!")
        else:
            print("❌ Falha ao alterar senha")
    
    def _list_users(self):
        """Lista todos os usuários (apenas admin)"""
        user = self.storage.current_user
        if not user or 'admin' not in user.roles:
            print("❌ Apenas administradores podem listar usuários")
            return
        
        users = self.storage.list_all_users()
        
        print("\n" + "=" * 60)
        print("👥 LISTA DE IDENTIDADES NEURAIS")
        print("=" * 60)
        
        for i, user_info in enumerate(users, 1):
            status = "🟢" if user_info.get('is_active', True) else "🔴"
            last_login = datetime.fromtimestamp(user_info.get('last_login', 0)).strftime('%d/%m/%Y %H:%M')
            
            print(f"{i}. {status} {user_info['username']}")
            print(f"   Email: {user_info.get('email', 'N/A')}")
            print(f"   Último login: {last_login}")
            print(f"   Logins: {user_info.get('login_count', 0)}")
            print(f"   Funções: {', '.join(user_info.get('roles', []))}")
            print()
    
    def _recover_password(self):
        """Interface para recuperação de senha"""
        print("\n" + "=" * 30)
        print("🔑 RECUPERAR SENHA")
        print("=" * 30)
        
        username = input("Identidade Neural: ").strip()
        email = input("Email registrado: ").strip()
        
        success = self.storage.reset_password(username, email)
        if success:
            print("✅ Instruções de recuperação enviadas (simulação)")
        else:
            print("❌ Falha na recuperação")
    
    def _show_statistics(self):
        """Mostra estatísticas do sistema"""
        stats = self.storage.get_statistics()
        
        print("\n" + "=" * 40)
        print("📊 ESTATÍSTICAS DO SISTEMA")
        print("=" * 40)
        
        print(f"Total de usuários: {stats['total_users']}")
        print(f"Usuários ativos: {stats['active_users']}")
        print(f"Usuários inativos: {stats['inactive_users']}")
        print(f"Logins hoje: {stats['logins_today']}")
        print(f"Arquivo de armazenamento: {stats['storage_file']}")
        print(f"Usuários em cache: {stats['cache_size']}")


# Função principal
def main():
    """Função principal"""
    print("Inicializando Sistema de Gerenciamento de Usuários...")
    
    # Criar e executar CLI
    cli = UserCLI(user_storage)
    cli.run()


# Executar se este arquivo for o principal
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário")