import streamlit as st
import hashlib
import json
import time
import re
import os
from datetime import datetime
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, field
import pandas as pd
import bcrypt
import base64
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="LexTrader ASI - Autenticação Neural",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado estilo "Matrix"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: #000000 !important;
        color: #d1d5db !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Grid background */
    .matrix-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(51, 51, 51, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(51, 51, 51, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Main panel */
    .auth-panel {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        border: 1px solid #374151;
        border-radius: 20px;
        padding: 40px;
        position: relative;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 40px rgba(14, 165, 233, 0.1);
    }
    
    /* Top gradient bar */
    .gradient-bar {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, transparent, #06b6d4, transparent);
    }
    
    /* Brain icon */
    .brain-icon {
        background: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 50%;
        border: 1px solid rgba(6, 182, 212, 0.3);
        display: inline-block;
        position: relative;
    }
    
    .brain-ring {
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        border-radius: 50%;
        border: 1px solid rgba(6, 182, 212, 0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.2; }
        50% { transform: scale(1.1); opacity: 0.1; }
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid #374151 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 40px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 1px #06b6d4 !important;
    }
    
    /* Password strength */
    .strength-bar {
        height: 4px;
        background-color: #374151;
        border-radius: 2px;
        overflow: hidden;
        margin-top: 8px;
    }
    
    .strength-fill {
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 16px !important;
        font-weight: bold !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.2) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(6, 182, 212, 0.3) !important;
    }
    
    .stButton > button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }
    
    /* Checkbox */
    .stCheckbox > label {
        color: #9ca3af !important;
        font-size: 12px !important;
    }
    
    .stCheckbox > label:hover {
        color: #d1d5db !important;
    }
    
    /* Error message */
    .error-message {
        background-color: rgba(220, 38, 38, 0.2) !important;
        border: 1px solid #991b1b !important;
        color: #f87171 !important;
        padding: 16px !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        margin-bottom: 20px !important;
    }
    
    /* Scan overlay */
    .scan-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.9);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    
    .scan-progress {
        width: 256px;
        height: 2px;
        background-color: #374151;
        border-radius: 1px;
        overflow: hidden;
        margin-top: 20px;
    }
    
    .scan-progress-fill {
        height: 100%;
        background-color: #06b6d4;
        transition: width 0.3s ease;
    }
    
    /* API Key button */
    .api-key-btn {
        width: 100%;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 16px;
    }
    
    .api-key-btn-active {
        background-color: rgba(22, 163, 74, 0.1);
        border-color: rgba(22, 163, 74, 0.5);
        color: #4ade80;
    }
    
    .api-key-btn-inactive {
        background-color: rgba(147, 51, 234, 0.1);
        border-color: rgba(147, 51, 234, 0.5);
        color: #a855f7;
    }
    
    .api-key-btn-inactive:hover {
        background-color: rgba(147, 51, 234, 0.2);
    }
    
    /* Toggle link */
    .toggle-link {
        color: #6b7280;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        cursor: pointer;
        transition: color 0.3s ease;
        text-align: center;
        margin-top: 24px;
    }
    
    .toggle-link:hover {
        color: #06b6d4;
    }
</style>
""", unsafe_allow_html=True)

# Dataclasses e modelos
@dataclass
class User:
    username: str
    password_hash: str
    email: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True

class UserStorageService:
    """Serviço de armazenamento de usuários"""
    
    def __init__(self, storage_file: str = "users.json"):
        self.storage_file = Path(storage_file)
        self.users: Dict[str, User] = {}
        self.load_users()
    
    def load_users(self):
        """Carrega usuários do arquivo JSON"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    for username, user_data in data.items():
                        self.users[username] = User(
                            username=username,
                            password_hash=user_data['password_hash'],
                            email=user_data.get('email', ''),
                            created_at=datetime.fromisoformat(user_data['created_at']),
                            last_login=datetime.fromisoformat(user_data['last_login']) if user_data.get('last_login') else None,
                            is_active=user_data.get('is_active', True)
                        )
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.users = {}
    
    def save_users(self):
        """Salva usuários no arquivo JSON"""
        try:
            data = {}
            for username, user in self.users.items():
                data[username] = {
                    'password_hash': user.password_hash,
                    'email': user.email,
                    'created_at': user.created_at.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'is_active': user.is_active
                }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")
    
    def hash_password(self, password: str) -> str:
        """Cria hash da senha usando bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica senha contra hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    async def register_user(self, username: str, password: str, email: str = "") -> User:
        """Registra um novo usuário"""
        if username in self.users:
            raise ValueError("Identidade neural já registrada")
        
        # Validação básica
        if len(username) < 3:
            raise ValueError("Nome de usuário muito curto")
        
        if len(password) < 6:
            raise ValueError("Senha muito curta")
        
        # Cria usuário
        user = User(
            username=username,
            password_hash=self.hash_password(password),
            email=email
        )
        
        self.users[username] = user
        self.save_users()
        
        return user
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autentica um usuário"""
        user = self.users.get(username)
        
        if not user:
            return None
        
        if not user.is_active:
            raise ValueError("Conta desativada")
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        # Atualiza último login
        user.last_login = datetime.now()
        self.save_users()
        
        return user

# Instância do serviço de usuários
user_storage = UserStorageService()

class AuthScreen:
    """Tela de autenticação estilo Matrix/Neural"""
    
    def __init__(self):
        # Inicializar estado da sessão
        if 'auth_mode' not in st.session_state:
            st.session_state.auth_mode = 'LOGIN'
        if 'username' not in st.session_state:
            st.session_state.username = ""
        if 'password' not in st.session_state:
            st.session_state.password = ""
        if 'email' not in st.session_state:
            st.session_state.email = ""
        if 'show_password' not in st.session_state:
            st.session_state.show_password = False
        if 'remember_me' not in st.session_state:
            st.session_state.remember_me = True
        if 'error' not in st.session_state:
            st.session_state.error = ""
        if 'is_loading' not in st.session_state:
            st.session_state.is_loading = False
        if 'scan_step' not in st.session_state:
            st.session_state.scan_step = 0
        if 'api_key_status' not in st.session_state:
            st.session_state.api_key_status = False
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        
        # Carregar usuário lembrado
        self.load_remembered_user()
    
    def load_remembered_user(self):
        """Carrega usuário lembrado do armazenamento local"""
        # Em uma aplicação real, usaríamos cookies ou session storage
        # Aqui simulamos com session state
        if 'remembered_user' not in st.session_state:
            st.session_state.remembered_user = ""
    
    def save_remembered_user(self, username: str):
        """Salva usuário para lembrar"""
        st.session_state.remembered_user = username
    
    def calculate_password_strength(self, password: str) -> Tuple[int, str, str]:
        """Calcula força da senha"""
        strength = 0
        
        if len(password) > 5:
            strength += 1
        if len(password) > 8:
            strength += 1
        if re.search(r'[A-Z]', password):
            strength += 1
        if re.search(r'[0-9]', password):
            strength += 1
        if re.search(r'[^A-Za-z0-9]', password):
            strength += 1
        
        # Cores baseadas na força
        if strength <= 2:
            color = "#ef4444"  # Vermelho
            label = "FRACA"
        elif strength <= 4:
            color = "#f59e0b"  # Amarelo
            label = "MÉDIA"
        else:
            color = "#10b981"  # Verde
            label = "FORTE"
        
        return strength, color, label
    
    async def handle_scan_animation(self):
        """Executa animação de escaneamento"""
        st.session_state.is_loading = True
        
        for step in range(1, 4):
            st.session_state.scan_step = step
            # Forçar re-render
            st.rerun()
            await asyncio.sleep(0.6 if step < 3 else 0.4)
    
    async def handle_submit(self):
        """Processa submissão do formulário"""
        st.session_state.error = ""
        
        try:
            if not st.session_state.username or not st.session_state.password:
                raise ValueError("Parâmetros de identidade incompletos.")
            
            # Executar animação de escaneamento
            await self.handle_scan_animation()
            
            if st.session_state.auth_mode == 'REGISTER':
                # Registrar novo usuário
                strength, _, _ = self.calculate_password_strength(st.session_state.password)
                if strength < 3:
                    raise ValueError("Protocolo de segurança: Senha muito fraca.")
                
                await user_storage.register_user(
                    st.session_state.username,
                    st.session_state.password,
                    st.session_state.email
                )
                
                if st.session_state.remember_me:
                    self.save_remembered_user(st.session_state.username)
                
                st.session_state.current_user = st.session_state.username
                st.session_state.authenticated = True
                
            else:
                # Login
                user = await user_storage.authenticate_user(
                    st.session_state.username,
                    st.session_state.password
                )
                
                if user:
                    if st.session_state.remember_me:
                        self.save_remembered_user(st.session_state.username)
                    
                    st.session_state.current_user = st.session_state.username
                    st.session_state.authenticated = True
                else:
                    raise ValueError("Falha na autenticação: Assinatura Neural Inválida.")
            
        except Exception as e:
            st.session_state.error = str(e)
            st.session_state.is_loading = False
            st.session_state.scan_step = 0
    
    def check_api_key(self):
        """Verifica status da chave API (simulado)"""
        # Em uma aplicação real, verificaria se a chave está configurada
        st.session_state.api_key_status = True  # Simulado
    
    def handle_api_key_selection(self):
        """Manipula seleção de chave API (simulado)"""
        st.info("🔑 Seleção de Chave Mestra - Esta funcionalidade requer integração com Google AI Studio")
        st.session_state.api_key_status = True
    
    def render_scan_overlay(self):
        """Renderiza overlay de escaneamento"""
        if st.session_state.scan_step > 0:
            scan_messages = {
                1: "VERIFICANDO IDENTIDADE...",
                2: "ANALISANDO PADRÃO RETINIANO...",
                3: "SINCRONIZANDO LINK NEURAL..."
            }
            
            st.markdown(f"""
            <div class="scan-overlay">
                <div style="font-size: 64px; color: #06b6d4; animation: pulse 1s infinite;">🔬</div>
                <div style="color: #06b6d4; font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 2px; margin-top: 16px;">
                    {scan_messages.get(st.session_state.scan_step, "ESCANEANDO...")}
                </div>
                <div class="scan-progress">
                    <div class="scan-progress-fill" style="width: {st.session_state.scan_step * 33}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_brain_background(self):
        """Renderiza ícone de cérebro de fundo"""
        st.markdown("""
        <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                    opacity: 0.05; pointer-events: none; font-size: 400px; color: #06b6d4;
                    animation: pulse 3s infinite ease-in-out;">
            🧠
        </div>
        """, unsafe_allow_html=True)
    
    def render_panel(self):
        """Renderiza o painel principal de autenticação"""
        st.markdown("""
        <div class="matrix-grid"></div>
        <div class="auth-panel">
            <div class="gradient-bar"></div>
        """, unsafe_allow_html=True)
        
        # Header com ícone
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 32px;">
                <div style="position: relative; display: inline-block;">
                    <div class="brain-icon">
                        <span style="font-size: 48px;">🧠</span>
                    </div>
                    <div class="brain-ring"></div>
                </div>
                <h1 style="color: white; font-size: 24px; font-weight: bold; letter-spacing: 4px; margin: 16px 0 8px 0;">
                    LEXTRADER-ASI
                </h1>
                <div style="color: #06b6d4; font-size: 11px; font-family: 'JetBrains Mono', monospace; letter-spacing: 1px;">
                    UPLINK NEURAL SEGURO v2.1
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mensagem de erro
        if st.session_state.error:
            st.markdown(f"""
            <div class="error-message">
                🛡️ {st.session_state.error}
            </div>
            """, unsafe_allow_html=True)
        
        # Formulário
        with st.form("auth_form"):
            # Campo de usuário
            st.markdown("""
            <div style="font-size: 10px; color: #6b7280; font-family: 'JetBrains Mono', monospace; 
                        text-transform: uppercase; letter-spacing: 2px; margin-bottom: 4px;">
                Identidade Neural (Usuário)
            </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input(
                label="",
                placeholder="ex: Neo_Operator",
                value=st.session_state.username,
                key="username_input",
                disabled=st.session_state.is_loading,
                label_visibility="collapsed"
            )
            
            if username != st.session_state.username:
                st.session_state.username = username
            
            # Campo de email (apenas registro)
            if st.session_state.auth_mode == 'REGISTER':
                st.markdown("""
                <div style="font-size: 10px; color: #6b7280; font-family: 'JetBrains Mono', monospace; 
                            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 4px; margin-top: 16px;">
                    Canal de Contato (Email)
                </div>
                """, unsafe_allow_html=True)
                
                email = st.text_input(
                    label="",
                    placeholder="opcional@neural.net",
                    value=st.session_state.email,
                    key="email_input",
                    disabled=st.session_state.is_loading,
                    label_visibility="collapsed"
                )
                
                if email != st.session_state.email:
                    st.session_state.email = email
            
            # Campo de senha
            st.markdown("""
            <div style="font-size: 10px; color: #6b7280; font-family: 'JetBrains Mono', monospace; 
                        text-transform: uppercase; letter-spacing: 2px; margin-bottom: 4px; margin-top: 16px;">
                Chave de Acesso (Senha)
            </div>
            """, unsafe_allow_html=True)
            
            # Campo de senha com toggle de visibilidade
            col1, col2 = st.columns([9, 1])
            with col1:
                password_type = "text" if st.session_state.show_password else "password"
                password = st.text_input(
                    label="",
                    type=password_type,
                    placeholder="••••••••",
                    value=st.session_state.password,
                    key="password_input",
                    disabled=st.session_state.is_loading,
                    label_visibility="collapsed"
                )
            
            with col2:
                # Botão para mostrar/esconder senha
                eye_icon = "👁️" if st.session_state.show_password else "👁️‍🗨️"
                if st.button(eye_icon, key="toggle_password", help="Mostrar/Esconder senha"):
                    st.session_state.show_password = not st.session_state.show_password
                    st.rerun()
            
            if password != st.session_state.password:
                st.session_state.password = password
            
            # Medidor de força da senha (apenas registro)
            if st.session_state.auth_mode == 'REGISTER' and st.session_state.password:
                strength, color, label = self.calculate_password_strength(st.session_state.password)
                width = (strength / 5) * 100
                
                st.markdown(f"""
                <div style="margin-top: 8px;">
                    <div class="strength-bar">
                        <div class="strength-fill" style="width: {width}%; background-color: {color};"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                        <div style="font-size: 9px; color: #6b7280; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">
                            {label}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Checkbox "Lembrar-me"
            remember_me = st.checkbox(
                "Manter link neural ativo (Lembrar-me)",
                value=st.session_state.remember_me,
                key="remember_checkbox",
                disabled=st.session_state.is_loading
            )
            
            if remember_me != st.session_state.remember_me:
                st.session_state.remember_me = remember_me
            
            # Botão de submit
            submit_text = "AUTENTICAR BIOMETRIA" if st.session_state.auth_mode == 'LOGIN' else "GERAR NOVA IDENTIDADE"
            submit_icon = "🔐" if st.session_state.auth_mode == 'LOGIN' else "👤"
            
            submit_disabled = st.session_state.is_loading or not st.session_state.username or not st.session_state.password
            
            if st.form_submit_button(
                f"{submit_icon} {submit_text}",
                disabled=submit_disabled,
                use_container_width=True
            ):
                # Executar submit assíncrono
                import asyncio
                asyncio.run(self.handle_submit())
        
        # Botão de chave API
        st.markdown("""
        <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #374151;">
        """, unsafe_allow_html=True)
        
        api_btn_class = "api-key-btn-active" if st.session_state.api_key_status else "api-key-btn-inactive"
        api_btn_text = "CHAVE MESTRA: ACOPLADA" if st.session_state.api_key_status else "INSERIR CHAVE MESTRA (Google AI)"
        api_icon = "🔑"
        
        if st.button(f"{api_icon} {api_btn_text}", key="api_key_btn", use_container_width=True):
            self.handle_api_key_selection()
        
        if not st.session_state.api_key_status:
            st.markdown("""
            <div style="font-size: 9px; color: #6b7280; text-align: center; margin-top: 8px; display: flex; align-items: center; justify-content: center; gap: 4px;">
                ⚠️ Necessário para o Núcleo Senciente
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Link para alternar entre login/registro
        toggle_text = "[ INICIAR PROTOCOLO DE REGISTRO ]" if st.session_state.auth_mode == 'LOGIN' else "[ RETORNAR AO LOGIN ]"
        
        if st.button(toggle_text, key="toggle_auth", use_container_width=True):
            # Alternar modo e limpar campos
            st.session_state.auth_mode = 'REGISTER' if st.session_state.auth_mode == 'LOGIN' else 'LOGIN'
            st.session_state.error = ""
            st.session_state.password = ""
            if st.session_state.auth_mode == 'LOGIN':
                st.session_state.email = ""
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_dashboard(self):
        """Renderiza o dashboard após autenticação"""
        st.title(f"🧠 Bem-vindo, {st.session_state.current_user}!")
        st.markdown("### UPLINK NEURAL ESTABELECIDO")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status do Sistema", "OPERACIONAL", "100%")
        
        with col2:
            st.metric("Carga Neural", "42%", "-3%")
        
        with col3:
            st.metric("Latência", "12ms", "2ms")
        
        # Adicionar mais componentes do dashboard aqui...
        
        if st.button("🔓 Desconectar"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()
    
    def run(self):
        """Executa a tela de autenticação"""
        # Renderizar fundo
        self.render_brain_background()
        
        # Renderizar overlay de escaneamento se ativo
        if st.session_state.scan_step > 0:
            self.render_scan_overlay()
        
        # Verificar se está autenticado
        if st.session_state.authenticated and st.session_state.current_user:
            self.render_dashboard()
        else:
            self.render_panel()

# Função principal
def main():
    # Inicializar e executar tela de autenticação
    auth_screen = AuthScreen()
    auth_screen.run()

if __name__ == "__main__":
    main()