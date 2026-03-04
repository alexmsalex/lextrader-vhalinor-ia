import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import threading
import time
import uuid

# --- TYPES ---
class TransferStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class TransferType(str, Enum):
    PROFIT_WITHDRAWAL = "PROFIT_WITHDRAWAL"
    DEPOSIT = "DEPOSIT"
    MAINTENANCE = "MAINTENANCE"

class TransferTrigger(str, Enum):
    MANUAL = "MANUAL"
    AUTO_RISK_RULE = "AUTO_RISK_RULE"
    SCHEDULED = "SCHEDULED"
    AGI_DIRECTED = "AGI_DIRECTED"

@dataclass
class BankAccount:
    id: str
    bank_name: str
    account_number: str
    account_type: str
    holder_name: str
    agency: Optional[str] = None
    is_default: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None

@dataclass
class FinancialSnapshot:
    total_applications: float
    total_realized_bank: float
    pending_transfers: float
    last_update: datetime
    available_for_withdrawal: float = 0.0
    risk_score: float = 0.0

@dataclass
class BankTransfer:
    id: str
    amount: float
    date: datetime
    status: TransferStatus
    type: TransferType
    destination_account: str
    trigger: TransferTrigger
    description: Optional[str] = None
    processed_at: Optional[datetime] = None
    confirmation_code: Optional[str] = None

@dataclass
class TransferConfig:
    auto_transfer_enabled: bool = False
    profit_threshold: float = 1000.0
    transfer_percentage: int = 50
    safety_cushion: float = 5000.0
    risk_integration: bool = True
    max_daily_transfer: float = 50000.0
    min_transfer_amount: float = 100.0
    notification_enabled: bool = True

# --- SIMULATED AGI CORE ---
class SentientCore:
    """Simulação do núcleo AGI para integração de risco"""
    
    def __init__(self):
        self.stability = 75.0
        self.confidence = 80.0
        self.risk_tolerance = 60.0
        self.thoughts = []
    
    def get_vector(self) -> Dict[str, float]:
        """Retorna vetor emocional atual"""
        # Simular pequenas variações
        self._update_emotions()
        return {
            "stability": self.stability,
            "confidence": self.confidence,
            "risk_tolerance": self.risk_tolerance
        }
    
    def _update_emotions(self):
        """Atualiza emoções com variação suave"""
        for attr in ['stability', 'confidence', 'risk_tolerance']:
            current = getattr(self, attr)
            change = (id(self) % 100) / 1000  # Deterministic but varying
            new_value = max(0, min(100, current + change))
            setattr(self, attr, new_value)
    
    def add_thought(self, thought: str):
        """Adiciona um pensamento ao registro"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.thoughts.append(f"[{timestamp}] {thought}")
        if len(self.thoughts) > 50:
            self.thoughts.pop(0)
        print(f"🧠 AGI: {thought}")

# --- BANKING SERVICE ---
class BankingService:
    """Serviço bancário para gerenciamento de contas e transferências"""
    
    def __init__(self, storage_file: str = "banking_data.json"):
        self.storage_file = storage_file
        self.accounts: List[BankAccount] = []
        self.transfer_history: List[BankTransfer] = []
        self.config = TransferConfig()
        
        # Saldos simulados
        self.brokerage_balance: float = 25000.00
        self.personal_bank_balance: float = 0.0
        self.daily_transfers_today: float = 0.0
        
        # AGI Integration
        self.sentient_core = SentientCore()
        
        # Lock para thread safety
        self._lock = threading.Lock()
        
        # Load data
        self.load_data()
        print("🏦 Banking Service inicializado")
    
    def load_data(self):
        """Carrega dados do arquivo de armazenamento"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Load accounts
                self.accounts = [
                    BankAccount(
                        id=acc['id'],
                        bank_name=acc['bank_name'],
                        account_number=acc['account_number'],
                        account_type=acc['account_type'],
                        holder_name=acc['holder_name'],
                        agency=acc.get('agency'),
                        is_default=acc.get('is_default', False),
                        created_at=datetime.fromisoformat(acc['created_at']),
                        last_used=datetime.fromisoformat(acc['last_used']) if acc.get('last_used') else None
                    )
                    for acc in data.get('accounts', [])
                ]
                
                # Load transfer history
                self.transfer_history = [
                    BankTransfer(
                        id=t['id'],
                        amount=t['amount'],
                        date=datetime.fromisoformat(t['date']),
                        status=TransferStatus(t['status']),
                        type=TransferType(t['type']),
                        destination_account=t['destination_account'],
                        trigger=TransferTrigger(t['trigger']),
                        description=t.get('description'),
                        processed_at=datetime.fromisoformat(t['processed_at']) if t.get('processed_at') else None,
                        confirmation_code=t.get('confirmation_code')
                    )
                    for t in data.get('transfer_history', [])
                ]
                
                # Load config
                if 'config' in data:
                    self.config = TransferConfig(**data['config'])
                
                # Load balances
                self.brokerage_balance = data.get('brokerage_balance', 25000.0)
                self.personal_bank_balance = data.get('personal_bank_balance', 0.0)
                self.daily_transfers_today = data.get('daily_transfers_today', 0.0)
                
                print(f"📂 Dados bancários carregados: {len(self.accounts)} contas, {len(self.transfer_history)} transferências")
                
        except Exception as e:
            print(f"⚠️ Erro ao carregar dados bancários: {e}")
            # Initialize with default data
            self._create_default_account()
    
    def save_data(self):
        """Salva dados no arquivo de armazenamento"""
        try:
            with self._lock:
                data = {
                    'accounts': [
                        {
                            'id': acc.id,
                            'bank_name': acc.bank_name,
                            'account_number': acc.account_number,
                            'account_type': acc.account_type,
                            'holder_name': acc.holder_name,
                            'agency': acc.agency,
                            'is_default': acc.is_default,
                            'created_at': acc.created_at.isoformat(),
                            'last_used': acc.last_used.isoformat() if acc.last_used else None
                        }
                        for acc in self.accounts
                    ],
                    'transfer_history': [
                        {
                            'id': t.id,
                            'amount': t.amount,
                            'date': t.date.isoformat(),
                            'status': t.status.value,
                            'type': t.type.value,
                            'destination_account': t.destination_account,
                            'trigger': t.trigger.value,
                            'description': t.description,
                            'processed_at': t.processed_at.isoformat() if t.processed_at else None,
                            'confirmation_code': t.confirmation_code
                        }
                        for t in self.transfer_history
                    ],
                    'config': asdict(self.config),
                    'brokerage_balance': self.brokerage_balance,
                    'personal_bank_balance': self.personal_bank_balance,
                    'daily_transfers_today': self.daily_transfers_today,
                    'last_save': datetime.now().isoformat()
                }
                
                with open(self.storage_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Dados bancários salvos em {self.storage_file}")
                
        except Exception as e:
            print(f"❌ Erro ao salvar dados bancários: {e}")
    
    def _create_default_account(self):
        """Cria uma conta padrão se não houver contas"""
        if not self.accounts:
            default_account = BankAccount(
                id=f"BANK-{int(time.time())}",
                bank_name="Banco do Brasil",
                account_number="12345-6",
                account_type="CONTA_CORRENTE",
                holder_name="Trader Automatizado",
                agency="0001",
                is_default=True
            )
            self.accounts.append(default_account)
            print(f"✅ Conta padrão criada: {default_account.bank_name}")
    
    # --- CONTAS BANCÁRIAS ---
    
    def add_account(self, account_data: Dict[str, Any]) -> BankAccount:
        """Adiciona uma nova conta bancária"""
        # Generate ID
        account_id = f"BANK-{int(time.time())}"
        
        # Create account object
        new_account = BankAccount(
            id=account_id,
            bank_name=account_data['bank_name'],
            account_number=account_data['account_number'],
            account_type=account_data['account_type'],
            holder_name=account_data['holder_name'],
            agency=account_data.get('agency'),
            is_default=False  # Will be set below if first account
        )
        
        with self._lock:
            # If first account, set as default
            if not self.accounts:
                new_account.is_default = True
            
            self.accounts.append(new_account)
            self.save_data()
        
        print(f"✅ Conta adicionada: {new_account.bank_name} - {new_account.account_number}")
        return new_account
    
    def get_accounts(self) -> List[BankAccount]:
        """Retorna todas as contas bancárias"""
        return self.accounts.copy()
    
    def set_default_account(self, account_id: str) -> bool:
        """Define uma conta como padrão"""
        with self._lock:
            # Clear all default flags
            for account in self.accounts:
                account.is_default = False
            
            # Set new default
            target_account = next((acc for acc in self.accounts if acc.id == account_id), None)
            if target_account:
                target_account.is_default = True
                target_account.last_used = datetime.now()
                self.save_data()
                print(f"✅ Conta padrão definida: {target_account.bank_name}")
                return True
            
            return False
    
    def remove_account(self, account_id: str) -> bool:
        """Remove uma conta bancária"""
        with self._lock:
            initial_count = len(self.accounts)
            self.accounts = [acc for acc in self.accounts if acc.id != account_id]
            
            if len(self.accounts) < initial_count:
                # If we removed the default account and there are others, set a new default
                if not any(acc.is_default for acc in self.accounts) and self.accounts:
                    self.accounts[0].is_default = True
                
                self.save_data()
                print(f"✅ Conta removida: {account_id}")
                return True
            
            return False
    
    # --- TRANSFERÊNCIAS & FINANCEIRO ---
    
    def get_financial_snapshot(self) -> FinancialSnapshot:
        """Retorna um snapshot financeiro atual"""
        # Calculate pending transfers
        pending_amount = sum(
            t.amount for t in self.transfer_history 
            if t.status == TransferStatus.PENDING
        )
        
        # Calculate available for withdrawal
        available = max(0, self.brokerage_balance - self.config.safety_cushion)
        
        # Get AGI risk score
        agi_vector = self.sentient_core.get_vector()
        risk_score = (100 - agi_vector['stability']) / 100
        
        return FinancialSnapshot(
            total_applications=self.brokerage_balance,
            total_realized_bank=self.personal_bank_balance,
            pending_transfers=pending_amount,
            available_for_withdrawal=available,
            risk_score=risk_score,
            last_update=datetime.now()
        )
    
    def request_transfer(self, amount: float, transfer_type: TransferType = TransferType.PROFIT_WITHDRAWAL) -> BankTransfer:
        """Solicita uma transferência bancária"""
        # Validations
        if amount <= 0:
            raise ValueError("O valor da transferência deve ser positivo")
        
        if amount < self.config.min_transfer_amount:
            raise ValueError(f"Valor mínimo para transferência: R${self.config.min_transfer_amount:.2f}")
        
        # Check daily transfer limit
        if self.daily_transfers_today + amount > self.config.max_daily_transfer:
            raise ValueError(f"Limite diário de transferência excedido. Disponível: R${self.config.max_daily_transfer - self.daily_transfers_today:.2f}")
        
        # Check safety cushion
        available = self.brokerage_balance - self.config.safety_cushion
        if amount > available:
            raise ValueError(f"Saldo insuficiente considerando margem de segurança. Disponível: R${available:.2f}")
        
        # AGI Risk Validation
        if self.config.risk_integration:
            risk_vector = self.sentient_core.get_vector()
            if risk_vector['stability'] < 30:
                self.sentient_core.add_thought("Bloqueio de saque preventivo. Volatilidade alta detectada. Margem necessária.")
                raise PermissionError("Saque bloqueado pelo Gerenciador de Risco Autônomo.")
        
        # Get default account
        default_account = next((acc for acc in self.accounts if acc.is_default), None)
        if not default_account:
            raise ValueError("Nenhuma conta bancária padrão configurada")
        
        # Create transfer record
        transfer = BankTransfer(
            id=f"TRF-{int(time.time())}",
            amount=amount,
            date=datetime.now(),
            status=TransferStatus.PENDING,
            type=transfer_type,
            destination_account=default_account.bank_name,
            trigger=TransferTrigger.MANUAL,
            description=f"Transferência {transfer_type.value}"
        )
        
        with self._lock:
            # Update daily transfer total
            self.daily_transfers_today += amount
            
            # Add to history
            self.transfer_history.insert(0, transfer)
            self.save_data()
        
        print(f"📤 Transferência solicitada: R${amount:.2f} para {default_account.bank_name}")
        
        # Start processing in background
        self._process_transfer_async(transfer.id)
        
        return transfer
    
    def _process_transfer_async(self, transfer_id: str):
        """Processa transferência de forma assíncrona (simulada)"""
        def process():
            # Simulate bank processing delay
            time.sleep(3)
            
            with self._lock:
                transfer = next((t for t in self.transfer_history if t.id == transfer_id), None)
                if transfer and transfer.status == TransferStatus.PENDING:
                    # Update status
                    transfer.status = TransferStatus.COMPLETED
                    transfer.processed_at = datetime.now()
                    transfer.confirmation_code = f"CONF-{int(time.time())}"
                    
                    # Update balances
                    self.brokerage_balance -= transfer.amount
                    self.personal_bank_balance += transfer.amount
                    
                    self.save_data()
                    
                    # AGI notification
                    self.sentient_core.add_thought(f"Transferência de R${transfer.amount:.2f} confirmada para conta pessoal.")
                    
                    print(f"✅ Transferência {transfer_id} processada com sucesso")
                    
                    # Notification (simulated)
                    if self.config.notification_enabled:
                        print(f"📧 Notificação: Transferência de R${transfer.amount:.2f} concluída")
        
        # Start processing thread
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def cancel_transfer(self, transfer_id: str) -> bool:
        """Cancela uma transferência pendente"""
        with self._lock:
            transfer = next((t for t in self.transfer_history if t.id == transfer_id), None)
            if transfer and transfer.status == TransferStatus.PENDING:
                transfer.status = TransferStatus.CANCELLED
                
                # Return amount to daily transfer limit
                self.daily_transfers_today -= transfer.amount
                
                self.save_data()
                print(f"❌ Transferência {transfer_id} cancelada")
                return True
        
        return False
    
    def get_transfer_history(self, limit: int = 20) -> List[BankTransfer]:
        """Retorna histórico de transferências"""
        return self.transfer_history[:limit]
    
    # --- AUTOMAÇÃO ---
    
    def update_config(self, new_config: Dict[str, Any]):
        """Atualiza configurações de automação"""
        with self._lock:
            # Update only provided fields
            for key, value in new_config.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            
            self.save_data()
            print(f"⚙️ Configurações atualizadas: {new_config}")
    
    def check_auto_transfer(self, current_profit: float):
        """Verifica e executa transferência automática baseada em lucro"""
        if not self.config.auto_transfer_enabled:
            return
        
        # Check profit threshold
        if current_profit >= self.config.profit_threshold:
            # Calculate transfer amount
            amount = current_profit * (self.config.transfer_percentage / 100)
            
            # Ensure minimum amount
            if amount < self.config.min_transfer_amount:
                return
            
            # Check safety cushion
            available = self.brokerage_balance - self.config.safety_cushion
            if amount > available:
                self.sentient_core.add_thought(f"Automação: Transferência de R${amount:.2f} não segura. Disponível: R${available:.2f}")
                return
            
            # Check daily limit
            if self.daily_transfers_today + amount > self.config.max_daily_transfer:
                self.sentient_core.add_thought("Automação: Limite diário de transferência atingido")
                return
            
            # Get default account
            default_account = next((acc for acc in self.accounts if acc.is_default), None)
            if not default_account:
                return
            
            # Create auto transfer
            transfer = BankTransfer(
                id=f"AUTO-TRF-{int(time.time())}",
                amount=amount,
                date=datetime.now(),
                status=TransferStatus.PENDING,
                type=TransferType.PROFIT_WITHDRAWAL,
                destination_account=default_account.bank_name,
                trigger=TransferTrigger.AUTO_RISK_RULE,
                description=f"Transferência automática - Lucro: R${current_profit:.2f}"
            )
            
            with self._lock:
                # Update daily transfer total
                self.daily_transfers_today += amount
                
                # Add to history
                self.transfer_history.insert(0, transfer)
                self.save_data()
            
            # AGI notification
            self.sentient_core.add_thought(f"Automação Bancária: Lucro de R${current_profit:.2f} detectado. Agendando transferência de R${amount:.2f}.")
            
            print(f"🤖 Transferência automática agendada: R${amount:.2f}")
            
            # Process transfer
            self._process_transfer_async(transfer.id)
    
    def simulate_profit(self, amount: float):
        """Simula um lucro (para testes)"""
        with self._lock:
            self.brokerage_balance += amount
            self.save_data()
        
        print(f"💰 Lucro simulado: R${amount:.2f}")
        
        # Check for auto transfer
        self.check_auto_transfer(amount)
    
    def reset_daily_transfers(self):
        """Reseta contador de transferências diárias"""
        with self._lock:
            self.daily_transfers_today = 0
            self.save_data()
        print("🔄 Contador diário de transferências resetado")
    
    def get_agi_thoughts(self, limit: int = 10) -> List[str]:
        """Retorna pensamentos recentes da AGI"""
        return self.sentient_core.thoughts[:limit]

# --- INSTÂNCIA GLOBAL ---
banking_service = BankingService()

# --- INTERFACE STREAMLIT ---
def create_streamlit_interface():
    """Cria interface Streamlit para o serviço bancário"""
    import streamlit as st
    
    st.set_page_config(
        page_title="Sistema Bancário Automatizado",
        page_icon="🏦",
        layout="wide"
    )
    
    st.title("🏦 Sistema Bancário Automatizado")
    st.markdown("---")
    
    # Initialize session state
    if 'refresh_key' not in st.session_state:
        st.session_state.refresh_key = 0
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Controles")
        
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            banking_service.load_data()
            st.session_state.refresh_key += 1
            st.rerun()
        
        if st.button("🔁 Resetar Diário", use_container_width=True):
            banking_service.reset_daily_transfers()
            st.success("Contador diário resetado!")
            st.rerun()
        
        st.markdown("---")
        st.header("📊 Status do Sistema")
        
        snapshot = banking_service.get_financial_snapshot()
        st.metric("Saldo Brokerage", f"R${snapshot.total_applications:,.2f}")
        st.metric("Saldo Banco", f"R${snapshot.total_realized_bank:,.2f}")
        st.metric("Transferências Pendentes", f"R${snapshot.pending_transfers:,.2f}")
        
        risk_color = "red" if snapshot.risk_score > 0.7 else "orange" if snapshot.risk_score > 0.4 else "green"
        st.markdown(f"**Score de Risco AGI:** <span style='color:{risk_color}'>{snapshot.risk_score:.2%}</span>", 
                   unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💳 Contas Bancárias",
        "💰 Transferências", 
        "⚙️ Configurações",
        "🧠 Logs AGI"
    ])
    
    with tab1:
        st.header("💳 Gerenciamento de Contas")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # List accounts
            accounts = banking_service.get_accounts()
            
            if accounts:
                st.subheader("Contas Cadastradas")
                for account in accounts:
                    with st.container():
                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        
                        with col_a:
                            st.markdown(f"**{account.bank_name}**")
                            st.markdown(f"Conta: {account.account_number} | Agência: {account.agency}")
                            st.markdown(f"Titular: {account.holder_name}")
                        
                        with col_b:
                            if account.is_default:
                                st.success("🔘 Padrão")
                        
                        with col_c:
                            if not account.is_default:
                                if st.button("Definir Padrão", key=f"set_default_{account.id}"):
                                    banking_service.set_default_account(account.id)
                                    st.rerun()
                            
                            if st.button("🗑️", key=f"remove_{account.id}"):
                                if banking_service.remove_account(account.id):
                                    st.success("Conta removida!")
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("Nenhuma conta cadastrada")
        
        with col2:
            # Add new account form
            st.subheader("Nova Conta")
            
            with st.form("add_account_form"):
                bank_name = st.text_input("Nome do Banco", "Banco do Brasil")
                account_number = st.text_input("Número da Conta", "12345-6")
                account_type = st.selectbox("Tipo de Conta", ["CONTA_CORRENTE", "CONTA_POUPANCA", "CONTA_SALARIO"])
                holder_name = st.text_input("Nome do Titular", "Trader Automatizado")
                agency = st.text_input("Agência (Opcional)", "0001")
                
                if st.form_submit_button("➕ Adicionar Conta", use_container_width=True):
                    account_data = {
                        'bank_name': bank_name,
                        'account_number': account_number,
                        'account_type': account_type,
                        'holder_name': holder_name,
                        'agency': agency if agency else None
                    }
                    
                    try:
                        banking_service.add_account(account_data)
                        st.success("Conta adicionada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
    
    with tab2:
        st.header("💰 Transferências")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Transfer history
            st.subheader("Histórico de Transferências")
            transfers = banking_service.get_transfer_history(15)
            
            if transfers:
                for transfer in transfers:
                    status_color = {
                        "PENDING": "orange",
                        "COMPLETED": "green",
                        "FAILED": "red",
                        "CANCELLED": "gray"
                    }.get(transfer.status.value, "black")
                    
                    with st.container():
                        col_a, col_b, col_c = st.columns([2, 1, 1])
                        
                        with col_a:
                            st.markdown(f"**R${transfer.amount:,.2f}**")
                            st.markdown(f"Destino: {transfer.destination_account}")
                            st.markdown(f"Tipo: {transfer.type.value}")
                        
                        with col_b:
                            st.markdown(f"<span style='color:{status_color}'><strong>{transfer.status.value}</strong></span>", 
                                       unsafe_allow_html=True)
                            st.markdown(f"<small>{transfer.date.strftime('%d/%m %H:%M')}</small>", 
                                       unsafe_allow_html=True)
                        
                        with col_c:
                            if transfer.status == TransferStatus.PENDING:
                                if st.button("❌", key=f"cancel_{transfer.id}"):
                                    if banking_service.cancel_transfer(transfer.id):
                                        st.success("Transferência cancelada!")
                                        st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("Nenhuma transferência realizada")
        
        with col2:
            # New transfer form
            st.subheader("Nova Transferência")
            
            snapshot = banking_service.get_financial_snapshot()
            available = snapshot.available_for_withdrawal
            
            st.markdown(f"**Disponível para saque:** R${available:,.2f}")
            
            with st.form("new_transfer_form"):
                amount = st.number_input(
                    "Valor (R$)",
                    min_value=100.0,
                    max_value=float(available),
                    value=min(1000.0, available),
                    step=100.0
                )
                
                transfer_type = st.selectbox(
                    "Tipo de Transferência",
                    [t.value for t in TransferType],
                    format_func=lambda x: x.replace("_", " ").title()
                )
                
                description = st.text_input("Descrição (Opcional)", "Transferência manual")
                
                if st.form_submit_button("📤 Solicitar Transferência", use_container_width=True):
                    try:
                        transfer_type_enum = TransferType(transfer_type)
                        transfer = banking_service.request_transfer(amount, transfer_type_enum)
                        st.success(f"Transferência solicitada! ID: {transfer.id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
            
            # Simulate profit
            st.markdown("---")
            st.subheader("💰 Simulação de Lucro")
            
            profit_amount = st.number_input("Valor do Lucro (R$)", min_value=100.0, max_value=10000.0, value=1000.0, step=100.0)
            
            if st.button("🎯 Simular Lucro", use_container_width=True):
                banking_service.simulate_profit(profit_amount)
                st.success(f"Lucro de R${profit_amount:,.2f} simulado!")
                st.rerun()
    
    with tab3:
        st.header("⚙️ Configurações de Automação")
        
        config = banking_service.config
        
        with st.form("config_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                auto_transfer = st.checkbox(
                    "Transferência Automática Habilitada",
                    value=config.auto_transfer_enabled,
                    help="Ativa transferências automáticas baseadas em lucro"
                )
                
                risk_integration = st.checkbox(
                    "Integração com AGI de Risco",
                    value=config.risk_integration,
                    help="Permite que a AGI bloqueie transferências em momentos de alto risco"
                )
                
                notifications = st.checkbox(
                    "Notificações Habilitadas",
                    value=config.notification_enabled,
                    help="Envia notificações sobre transferências"
                )
                
                profit_threshold = st.number_input(
                    "Limite de Lucro para Auto-transferência (R$)",
                    min_value=100.0,
                    max_value=10000.0,
                    value=config.profit_threshold,
                    step=100.0
                )
            
            with col2:
                transfer_percentage = st.slider(
                    "Percentual de Transferência Automática (%)",
                    min_value=10,
                    max_value=100,
                    value=config.transfer_percentage,
                    step=5
                )
                
                safety_cushion = st.number_input(
                    "Margem de Segurança (R$)",
                    min_value=1000.0,
                    max_value=50000.0,
                    value=config.safety_cushion,
                    step=1000.0
                )
                
                max_daily = st.number_input(
                    "Limite Diário de Transferência (R$)",
                    min_value=1000.0,
                    max_value=100000.0,
                    value=config.max_daily_transfer,
                    step=1000.0
                )
                
                min_transfer = st.number_input(
                    "Valor Mínimo por Transferência (R$)",
                    min_value=10.0,
                    max_value=1000.0,
                    value=config.min_transfer_amount,
                    step=10.0
                )
            
            if st.form_submit_button("💾 Salvar Configurações", use_container_width=True):
                new_config = {
                    'auto_transfer_enabled': auto_transfer,
                    'profit_threshold': profit_threshold,
                    'transfer_percentage': transfer_percentage,
                    'safety_cushion': safety_cushion,
                    'risk_integration': risk_integration,
                    'max_daily_transfer': max_daily,
                    'min_transfer_amount': min_transfer,
                    'notification_enabled': notifications
                }
                
                banking_service.update_config(new_config)
                st.success("Configurações salvas!")
                st.rerun()
    
    with tab4:
        st.header("🧠 Logs da AGI")
        
        thoughts = banking_service.get_agi_thoughts(20)
        
        if thoughts:
            for thought in thoughts:
                # Color code by keyword
                if "Transferência" in thought or "confirmada" in thought:
                    color = "green"
                elif "Bloqueio" in thought or "risco" in thought or "não segura" in thought:
                    color = "red"
                elif "Automação" in thought:
                    color = "blue"
                else:
                    color = "gray"
                
                st.markdown(f"<span style='color:{color}'>• {thought}</span>", unsafe_allow_html=True)
        else:
            st.info("Nenhum pensamento registrado pela AGI")

if __name__ == "__main__":
    # Create Streamlit interface
    create_streamlit_interface()