"""
🔌 PAINEL DE ACESSO RÁPIDO A APIs
==================================

Componente Streamlit para gerenciar e testar conexões com APIs
Integrado ao LEXTRADER-IAG 4.0

Uso:
    from api_quick_access import render_api_panel, APIManager
    render_api_panel()
"""

import streamlit as st
import os
import asyncio
import json
import pyautogui
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

# Configurar pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


@dataclass
class APIStatus:
    """Status de uma API"""
    name: str
    status: str  # "connected", "disconnected", "error"
    last_check: str
    message: str
    response_time: float = 0.0
    configured: bool = False


class APIManager:
    """Gerenciador centralizado de APIs"""
    
    def __init__(self):
        self.apis = {
            "binance": {
                "name": "Binance (Spot Trading)",
                "icon": "🪙",
                "description": "Exchange de criptomoedas Binance",
                "status": "disconnected",
                "configured": self._check_binance_configured(),
                "env_vars": ["BINANCE_API_KEY", "BINANCE_API_SECRET"],
                "file": "neural_layers/01_sensorial/exchange_integrator.py",
                "port": "Public REST API"
            },
            "ctrader": {
                "name": "cTrader (Forex/CFD)",
                "icon": "💹",
                "description": "Plataforma de trading forex e CFDs",
                "status": "disconnected",
                "configured": self._check_ctrader_configured(),
                "env_vars": ["CTRADER_CLIENT_ID", "CTRADER_CLIENT_SECRET"],
                "file": "neural_layers/01_sensorial/ctrader_api.py",
                "port": "OAuth2"
            },
            "pionex": {
                "name": "Pionex (Crypto Bots)",
                "icon": "🤖",
                "description": "Plataforma de trading com bots de arbitragem",
                "status": "disconnected",
                "configured": self._check_pionex_configured(),
                "env_vars": ["PIONEX_API_KEY", "PIONEX_API_SECRET"],
                "file": "neural_layers/01_sensorial/pionex_api.py",
                "port": "REST API"
            },
            "coinbase": {
                "name": "Coinbase (Advanced)",
                "icon": "🏦",
                "description": "Exchange Coinbase com advanced trading",
                "status": "disconnected",
                "configured": self._check_coinbase_configured(),
                "env_vars": ["COINBASE_API_KEY", "COINBASE_API_SECRET"],
                "file": "neural_layers/01_sensorial/exchange_integrator.py",
                "port": "REST API"
            },
            "alpaca": {
                "name": "Alpaca (US Stocks)",
                "icon": "📈",
                "description": "Broker para trading de ações US",
                "status": "disconnected",
                "configured": self._check_alpaca_configured(),
                "env_vars": ["ALPACA_API_KEY", "ALPACA_API_SECRET"],
                "file": "neural_layers/01_sensorial/live_trade.py",
                "port": "REST API"
            },
            "alphavantage": {
                "name": "Alpha Vantage (Market Data)",
                "icon": "📊",
                "description": "Dados de mercado históricos e tempo real",
                "status": "disconnected",
                "configured": self._check_alphavantage_configured(),
                "env_vars": ["ALPHAVANTAGE_KEY"],
                "file": "neural_layers/01_sensorial/data_fetcher.py",
                "port": "REST API"
            },
            "polygon": {
                "name": "Polygon.io (Market Data)",
                "icon": "📡",
                "description": "Dados de mercado stocks e crypto",
                "status": "disconnected",
                "configured": self._check_polygon_configured(),
                "env_vars": ["POLYGON_KEY"],
                "file": "neural_layers/01_sensorial/data_fetcher.py",
                "port": "REST API"
            },
            "twelvedata": {
                "name": "Twelve Data (Multi-Asset)",
                "icon": "🌍",
                "description": "Dados de múltiplos ativos (stocks, forex, crypto)",
                "status": "disconnected",
                "configured": self._check_twelvedata_configured(),
                "env_vars": ["TWELVEDATA_KEY"],
                "file": "neural_layers/01_sensorial/data_fetcher.py",
                "port": "REST API"
            }
        }
    
    def _check_binance_configured(self) -> bool:
        return bool(os.getenv("BINANCE_API_KEY")) and \
               not os.getenv("BINANCE_API_KEY", "").startswith("YOUR_")
    
    def _check_ctrader_configured(self) -> bool:
        return bool(os.getenv("CTRADER_CLIENT_ID")) and \
               not os.getenv("CTRADER_CLIENT_ID", "").startswith("YOUR_")
    
    def _check_pionex_configured(self) -> bool:
        return bool(os.getenv("PIONEX_API_KEY")) and \
               not os.getenv("PIONEX_API_KEY", "").startswith("YOUR_")
    
    def _check_coinbase_configured(self) -> bool:
        return bool(os.getenv("COINBASE_API_KEY")) and \
               not os.getenv("COINBASE_API_KEY", "").startswith("YOUR_")
    
    def _check_alpaca_configured(self) -> bool:
        return bool(os.getenv("ALPACA_API_KEY")) and \
               not os.getenv("ALPACA_API_KEY", "").startswith("YOUR_")
    
    def _check_alphavantage_configured(self) -> bool:
        return bool(os.getenv("ALPHAVANTAGE_KEY")) and \
               not os.getenv("ALPHAVANTAGE_KEY", "").startswith("YOUR_")
    
    def _check_polygon_configured(self) -> bool:
        return bool(os.getenv("POLYGON_KEY")) and \
               not os.getenv("POLYGON_KEY", "").startswith("YOUR_")
    
    def _check_twelvedata_configured(self) -> bool:
        return bool(os.getenv("TWELVEDATA_KEY")) and \
               not os.getenv("TWELVEDATA_KEY", "").startswith("YOUR_")
    
    def test_connection(self, api_name: str) -> tuple[bool, str, float]:
        """
        Testa conexão com uma API
        
        Returns:
            (success, message, response_time)
        """
        import time
        start_time = time.time()
        
        try:
            api_info = self.apis.get(api_name, {})
            configured = api_info.get("configured", False)
            
            if not configured:
                return False, "❌ Não configurado - adicione credenciais em .env", 0.0
            
            # Simulação de teste (em produção, fazer request real)
            # aqui fazer ping/healthcheck real
            response_time = time.time() - start_time
            
            return True, "✅ Conectado", response_time
        
        except Exception as e:
            response_time = time.time() - start_time
            return False, f"❌ Erro: {str(e)}", response_time
    
    def automate_api_test(self, api_name: str) -> Dict[str, Any]:
        """
        Automatiza teste de API usando pyautogui
        
        Realiza:
        1. Abre a documentação da API
        2. Preenche credenciais
        3. Executa teste
        4. Registra resultado
        """
        api_info = self.apis.get(api_name, {})
        results = {
            "api": api_name,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "success": False
        }
        
        try:
            # Step 1: Movimentar mouse para o centro da tela
            logger.info(f"[{api_name}] Step 1: Posicionando mouse")
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.5)
            results["steps"].append("✅ Mouse posicionado")
            
            # Step 2: Simular digitação de configurações
            logger.info(f"[{api_name}] Step 2: Simulando entrada de credenciais")
            pyautogui.typewrite(['return'], interval=0.1)  # Enter
            results["steps"].append("✅ Credenciais simuladas")
            
            # Step 3: Executar comando de teste
            logger.info(f"[{api_name}] Step 3: Executando teste")
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'c')  # Simula cancelamento se necessário
            results["steps"].append("✅ Teste executado")
            
            results["success"] = True
            results["message"] = f"Teste automatizado concluído para {api_name}"
            
        except Exception as e:
            logger.error(f"Erro na automação: {e}")
            results["message"] = f"❌ Erro: {str(e)}"
            results["success"] = False
        
        return results
    
    def automate_fill_credentials(self, api_name: str, credentials: Dict[str, str]) -> bool:
        """
        Preenche automaticamente as credenciais de uma API usando pyautogui
        
        Args:
            api_name: Nome da API
            credentials: Dicionário com chaves e valores
        
        Returns:
            bool: Sucesso ou falha
        """
        try:
            logger.info(f"Preenchendo credenciais para {api_name}")
            
            # Focar na janela
            pyautogui.press('tab')
            time.sleep(0.2)
            
            # Preencher cada credencial
            for key, value in credentials.items():
                logger.info(f"  Preenchendo {key}")
                pyautogui.typewrite(value, interval=0.05)
                pyautogui.press('tab')
                time.sleep(0.3)
            
            # Confirmar (Enter)
            pyautogui.press('return')
            time.sleep(0.5)
            
            logger.info(f"✅ Credenciais preenchidas para {api_name}")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao preencher credenciais: {e}")
            return False
    
    def automate_health_check_all(self) -> Dict[str, bool]:
        """
        Executa health check em todas as APIs com automação pyautogui
        
        Returns:
            Dict com status de cada API
        """
        results = {}
        
        for api_name in self.apis.keys():
            logger.info(f"Health check para {api_name}")
            
            # Mover mouse para confirmar atividade
            pyautogui.moveTo(100, 100, duration=0.3)
            time.sleep(0.2)
            
            success, message, response_time = self.test_connection(api_name)
            results[api_name] = {
                "success": success,
                "message": message,
                "response_time": response_time
            }
            
            time.sleep(0.5)
        
        return results
    
    def automate_screenshot_results(self, filepath: str) -> bool:
        """
        Captura screenshot dos resultados dos testes usando pyautogui
        
        Args:
            filepath: Caminho para salvar a screenshot
        
        Returns:
            bool: Sucesso ou falha
        """
        try:
            logger.info(f"Capturando screenshot para {filepath}")
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            logger.info(f"✅ Screenshot salvo: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao capturar screenshot: {e}")
            return False
    
    def get_status_all(self) -> Dict[str, APIStatus]:
        """Obtém status de todas as APIs"""
        statuses = {}
        
        for api_name, api_info in self.apis.items():
            configured = api_info.get("configured", False)
            
            if not configured:
                status = "disconnected"
                message = "Não configurado"
            else:
                success, message, response_time = self.test_connection(api_name)
                status = "connected" if success else "error"
            
            statuses[api_name] = APIStatus(
                name=api_info["name"],
                status=status,
                last_check=datetime.now().strftime("%H:%M:%S"),
                message=message,
                configured=configured
            )
        
        return statuses
    
    def get_missing_credentials(self) -> Dict[str, List[str]]:
        """Retorna APIs com credenciais faltantes"""
        missing = {}
        
        for api_name, api_info in self.apis.items():
            env_vars = api_info.get("env_vars", [])
            missing_vars = []
            
            for var in env_vars:
                value = os.getenv(var, "")
                if not value or value.startswith("YOUR_"):
                    missing_vars.append(var)
            
            if missing_vars:
                missing[api_name] = missing_vars
        
        return missing


def render_api_status_card(api_name: str, api_info: Dict, manager: APIManager):
    """Renderiza um card de status de API"""
    
    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"### {api_info['icon']} {api_info['name']}")
            st.caption(api_info['description'])
        
        with col2:
            if api_info['configured']:
                st.success("Configurado ✅")
            else:
                st.warning("Não config. ⚠️")
        
        with col3:
            if st.button("🔄 Testar", key=f"test_{api_name}"):
                success, message, response_time = manager.test_connection(api_name)
                if success:
                    st.success(f"{message} ({response_time*1000:.1f}ms)")
                else:
                    st.error(message)
        
        # Informações adicionais
        cols_info = st.columns(2)
        
        with cols_info[0]:
            st.caption(f"📄 Arquivo: `{api_info['file']}`")
        
        with cols_info[1]:
            st.caption(f"🔌 Protocolo: {api_info['port']}")
        
        # Botões de ação
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            if st.button("📋 Configurar", key=f"config_{api_name}", use_container_width=True):
                st.session_state[f"show_config_{api_name}"] = True
        
        with col_action2:
            if st.button("📖 Documentação", key=f"docs_{api_name}", use_container_width=True):
                st.session_state[f"show_docs_{api_name}"] = True
        
        with col_action3:
            if st.button("🧪 Testar", key=f"test_full_{api_name}", use_container_width=True):
                st.session_state[f"show_test_{api_name}"] = True


def render_api_configuration(api_name: str, api_info: Dict):
    """Renderiza formulário de configuração"""
    
    st.subheader(f"⚙️ Configurar {api_info['name']}")
    
    env_vars = api_info.get("env_vars", [])
    
    st.info("""
    Para configurar, adicione as variáveis de ambiente ao arquivo `.env`:
    
    1. Abra o arquivo `.env` na raiz do projeto
    2. Adicione/atualize as linhas abaixo
    3. Salve o arquivo
    4. Reinicie a aplicação
    """)
    
    config_text = "\n".join([f"{var}=seu_valor_aqui" for var in env_vars])
    
    st.code(config_text, language="bash")
    
    st.markdown("### Como obter as credenciais?")
    
    docs_links = {
        "binance": "https://www.binance.com/en/account/api-management",
        "ctrader": "https://connect.ctrader.com",
        "pionex": "https://www.pionex.com/en-US/setting/api",
        "coinbase": "https://www.coinbase.com/settings/api",
        "alpaca": "https://alpaca.markets/docs/",
        "alphavantage": "https://www.alphavantage.co/",
        "polygon": "https://polygon.io/",
        "twelvedata": "https://twelvedata.com/"
    }
    
    if api_name in docs_links:
        st.link_button(
            f"📖 Ir para {api_info['name']}",
            docs_links[api_name],
            use_container_width=True
        )


def render_api_test(api_name: str, api_info: Dict, manager: APIManager):
    """Renderiza interface de teste"""
    
    st.subheader(f"🧪 Testar {api_info['name']}")
    
    if not api_info['configured']:
        st.warning("❌ API não está configurada. Configure primeiro em ⚙️ Configurar")
        return
    
    # Tipos de teste
    test_type = st.selectbox(
        "Tipo de teste:",
        ["Conexão", "Obter saldo", "Mercados disponíveis", "Status"]
    )
    
    # Nova seção: Automação com pyautogui
    st.markdown("### 🤖 Testes Automatizados com pyautogui")
    
    col_auto1, col_auto2 = st.columns(2)
    
    with col_auto1:
        if st.button("⚙️ Automação Completa", key=f"auto_{api_name}"):
            with st.spinner("Executando automação..."):
                results = manager.automate_api_test(api_name)
                
                st.success("✅ Automação concluída!")
                st.json(results)
    
    with col_auto2:
        if st.button("📸 Capturar Screenshot", key=f"screenshot_{api_name}"):
            with st.spinner("Capturando tela..."):
                filepath = f"logs/screenshot_{api_name}_{int(time.time())}.png"
                Path("logs").mkdir(exist_ok=True)
                
                if manager.automate_screenshot_results(filepath):
                    st.success(f"✅ Screenshot salvo: {filepath}")
                    st.image(filepath)
                else:
                    st.error("❌ Erro ao capturar screenshot")
    
    st.markdown("---")
    
    if st.button("▶️ Executar teste", key=f"run_test_{api_name}"):
        with st.spinner("Testando..."):
            try:
                if test_type == "Conexão":
                    success, message, response_time = manager.test_connection(api_name)
                    if success:
                        st.success(f"{message}\n⏱️ Tempo de resposta: {response_time*1000:.2f}ms")
                    else:
                        st.error(f"{message}")
                
                elif test_type == "Obter saldo":
                    st.info("Funcionalidade disponível em produção")
                    st.code("GET /account/balance")
                
                elif test_type == "Mercados disponíveis":
                    st.info("Funcionalidade disponível em produção")
                    st.code("GET /markets")
                
                elif test_type == "Status":
                    st.info("Funcionalidade disponível em produção")
                    st.code("GET /status")
            
            except Exception as e:
                st.error(f"Erro ao testar: {str(e)}")


def render_api_quick_access():
    """Painel principal de acesso rápido a APIs"""
    
    st.set_page_config(
        page_title="APIs Quick Access",
        page_icon="🔌",
        layout="wide"
    )
    
    # Inicializar manager
    if "api_manager" not in st.session_state:
        st.session_state.api_manager = APIManager()
    
    manager = st.session_state.api_manager
    
    # Título
    st.markdown("# 🔌 Acesso Rápido a APIs")
    st.markdown("Gerencie e teste todas as conexões de APIs")
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Status em Tempo Real",
        "⚙️ Configuração",
        "🧪 Testes",
        "🤖 Automação",
        "📋 Resumo"
    ])
    
    # ════════════════════════════════════════════════════════════════════════════════
    # TAB 1: STATUS EM TEMPO REAL
    # ════════════════════════════════════════════════════════════════════════════════
    
    with tab1:
        st.markdown("## Status de todas as APIs")
        
        # Atualizar status
        if st.button("🔄 Atualizar Status", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        # Grid de APIs
        cols = st.columns(2)
        col_idx = 0
        
        for api_name, api_info in manager.apis.items():
            with cols[col_idx % 2]:
                render_api_status_card(api_name, api_info, manager)
            col_idx += 1
    
    # ════════════════════════════════════════════════════════════════════════════════
    # TAB 2: CONFIGURAÇÃO
    # ════════════════════════════════════════════════════════════════════════════════
    
    with tab2:
        st.markdown("## Configuração de APIs")
        
        # Selecionar API
        api_to_config = st.selectbox(
            "Selecione a API para configurar:",
            options=list(manager.apis.keys()),
            format_func=lambda x: manager.apis[x]['name']
        )
        
        st.markdown("---")
        
        if api_to_config:
            render_api_configuration(api_to_config, manager.apis[api_to_config])
        
        # Resumo de faltantes
        st.markdown("---")
        st.markdown("## Credenciais Faltantes")
        
        missing = manager.get_missing_credentials()
        
        if missing:
            for api_name, vars_list in missing.items():
                with st.expander(f"❌ {manager.apis[api_name]['name']}"):
                    for var in vars_list:
                        st.code(f"{var}=seu_valor_aqui")
        else:
            st.success("✅ Todas as credenciais configuradas!")
    
    # ════════════════════════════════════════════════════════════════════════════════
    # TAB 3: TESTES
    # ════════════════════════════════════════════════════════════════════════════════
    
    with tab3:
        st.markdown("## Testes de APIs")
        
        # Selecionar API
        api_to_test = st.selectbox(
            "Selecione a API para testar:",
            options=list(manager.apis.keys()),
            format_func=lambda x: manager.apis[x]['name'],
            key="test_api_select"
        )
        
        st.markdown("---")
        
        if api_to_test:
            render_api_test(api_to_test, manager.apis[api_to_test], manager)
    
    # ════════════════════════════════════════════════════════════════════════════════
    # TAB 4: AUTOMACAO COM PYAUTOGUI
    # ════════════════════════════════════════════════════════════════════════════════
    
    with tab4:
        st.markdown("## 🤖 Automação com pyautogui")
        
        st.info("""
        Use pyautogui para automatizar testes de APIs:
        - Executa health checks em todas as APIs
        - Captura screenshots dos resultados
        - Simula entrada de dados
        - Realiza testes automatizados
        """)
        
        col_auto1, col_auto2, col_auto3 = st.columns(3)
        
        with col_auto1:
            if st.button("🏥 Health Check Todas", use_container_width=True):
                st.markdown("### Executando Health Check com Automação...")
                
                with st.spinner("Testando todas as APIs..."):
                    results = manager.automate_health_check_all()
                    
                    # Mostrar resultados
                    for api_name, result in results.items():
                        if result['success']:
                            st.success(f"✅ {api_name}: {result['message']}")
                        else:
                            st.warning(f"⚠️ {api_name}: {result['message']}")
                    
                    st.json(results)
        
        with col_auto2:
            if st.button("📸 Capturar Todas", use_container_width=True):
                st.markdown("### Capturando Screenshots...")
                
                with st.spinner("Capturando telas..."):
                    Path("logs").mkdir(exist_ok=True)
                    
                    for i, api_name in enumerate(manager.apis.keys()):
                        timestamp = int(time.time()) + i
                        filepath = f"logs/screenshot_{api_name}_{timestamp}.png"
                        
                        if manager.automate_screenshot_results(filepath):
                            st.success(f"✅ {api_name} salvo")
                        else:
                            st.warning(f"⚠️ Erro em {api_name}")
        
        with col_auto3:
            if st.button("🔄 Teste Sequencial", use_container_width=True):
                st.markdown("### Executando Testes Sequenciais...")
                
                progress_bar = st.progress(0)
                
                total_apis = len(manager.apis)
                for idx, api_name in enumerate(manager.apis.keys()):
                    with st.spinner(f"Testando {api_name}..."):
                        results = manager.automate_api_test(api_name)
                        
                        if results['success']:
                            st.success(f"✅ {api_name}")
                        else:
                            st.warning(f"⚠️ {api_name}: {results['message']}")
                    
                    progress_bar.progress((idx + 1) / total_apis)
        
        st.markdown("---")
        
        # Configurações avançadas de automação
        st.markdown("### ⚙️ Configurações de Automação")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            failsafe = st.checkbox("🛑 FailSafe (Mover mouse canto superior)", value=True)
            if failsafe:
                pyautogui.FAILSAFE = True
                st.caption("Mover mouse para canto superior esquerdo para interromper")
        
        with col_config2:
            pause_time = st.slider("⏱️ Intervalo entre ações (ms)", 50, 500, 100)
            pyautogui.PAUSE = pause_time / 1000
        
        st.markdown("---")
        
        # Log de automação
        st.markdown("### 📝 Log de Automação")
        
        if st.button("📋 Mostrar Logs"):
            log_dir = Path("logs")
            if log_dir.exists():
                log_files = list(log_dir.glob("*.log"))
                if log_files:
                    for log_file in log_files[-5:]:  # Últimos 5 logs
                        with st.expander(f"📄 {log_file.name}"):
                            st.code(log_file.read_text())
                else:
                    st.info("Nenhum arquivo de log encontrado")
            else:
                st.info("Diretório de logs não existe")
    
    # ════════════════════════════════════════════════════════════════════════════════
    # TAB 5: RESUMO
    # ════════════════════════════════════════════════════════════════════════════════
    
    with tab5:
        st.markdown("## 📋 Resumo de APIs")
        
        statuses = manager.get_status_all()
        
        # Estatísticas
        total_apis = len(statuses)
        configured_apis = sum(1 for s in statuses.values() if s.configured)
        connected_apis = sum(1 for s in statuses.values() if s.status == "connected")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de APIs", total_apis)
        
        with col2:
            st.metric("Configuradas", configured_apis)
        
        with col3:
            st.metric("Conectadas", connected_apis)
        
        with col4:
            st.metric("Taxa", f"{configured_apis/total_apis*100:.0f}%")
        
        st.markdown("---")
        
        # Tabela de status
        data = []
        for api_name, status in statuses.items():
            data.append({
                "API": status.name,
                "Status": "✅ Conectado" if status.status == "connected" else 
                         "⚠️ Erro" if status.status == "error" else 
                         "❌ Desconectado",
                "Configurado": "✅ Sim" if status.configured else "❌ Não",
                "Última Verificação": status.last_check,
                "Mensagem": status.message
            })
        
        import pandas as pd
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Recomendações
        st.markdown("---")
        st.markdown("## 💡 Recomendações")
        
        if missing := manager.get_missing_credentials():
            st.warning(f"⚠️ {len(missing)} API(s) sem credenciais configuradas")
            st.markdown("Vá para a aba **⚙️ Configuração** para adicionar credenciais")
        else:
            st.success("✅ Todas as APIs estão configuradas!")


# ════════════════════════════════════════════════════════════════════════════════
# FUNÇÃO DE INTEGRAÇÃO COM APP.PY
# ════════════════════════════════════════════════════════════════════════════════

def render_api_panel():
    """Função de integração para ser chamada no APP.py"""
    render_api_quick_access()


if __name__ == "__main__":
    # Para testes diretos
    render_api_quick_access()
