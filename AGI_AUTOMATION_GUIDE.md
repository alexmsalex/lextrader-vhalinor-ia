# 🤖 AGI AUTOMATION - Guia Completo de Operação Automática

## 📋 Visão Geral

O sistema **AGI Automation** permite que a Inteligência Geral Artificial (AGI) do LEXTRADER-IAG 4.0 **opere completamente automaticamente** no mercado, executando:

- ✅ **Análise contínua do mercado** (24/7)
- ✅ **Geração automática de sinais de trading**
- ✅ **Tomada de decisão inteligente**
- ✅ **Execução automática de trades**
- ✅ **Monitoramento de posições abertas**
- ✅ **Gerenciamento de risco em tempo real**
- ✅ **Rebalanceamento automático de portfólio**

---

## 🏗️ Arquitetura de Automação

### Componentes Principais

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGI AUTOMATION ENGINE                        │
│         (Núcleo de Orquestração e Coordenação)                  │
└─────────────────────────────────────────────────────────────────┘
        ↓              ↓              ↓              ↓
   ┌─────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐
   │ MARKET  │  │ DECISION     │  │ TRADE    │  │PORTFOLIO │
   │MONITOR  │  │ ENGINE       │  │EXECUTOR  │  │MANAGER   │
   └─────────┘  └──────────────┘  └──────────┘  └──────────┘
        ↓              ↓              ↓              ↓
   Monitor      Analisa        Executa         Gerencia
   Mercado      Decisões       Trades          Posições
```

### Fluxo de Operação

```
1. MARKET MONITOR
   ├─ Monitora 24/7 múltiplos símbolos
   ├─ Detecta padrões e oportunidades
   └─ Gera alertas

2. AUTOMATION ENGINE
   ├─ Recebe dados do monitor
   ├─ Coordena análises
   └─ Orquestra fluxo de decisão

3. DECISION ENGINE (Layer 04)
   ├─ Analisa sinais e indicadores
   ├─ Avalia estratégias múltiplas
   ├─ Valida risco
   └─ Gera decisão de trading

4. TRADE EXECUTOR (Layer 03)
   ├─ Recebe decisão validada
   ├─ Conecta com broker/exchange
   ├─ Executa ordem
   └─ Registra trade

5. PORTFOLIO MANAGER
   ├─ Registra posição aberta
   ├─ Monitora P&L
   ├─ Aplica stop loss/take profit
   └─ Fecha quando atinge objetivo

6. RISK MANAGER
   └─ Valida tudo e bloqueia se necessário
```

---

## 🚀 Como Usar

### 1. **Iniciar Automação (Opção Recomendada)**

#### A. Via Python Script (Mais Controlado)

```bash
# Terminal PowerShell ou CMD
cd C:\Users\ALEXMS-PC\Desktop\LEXTRADER-IAG-4.0

# Iniciar automação completa
python agi_automation_orchestrator.py

# Saída esperada:
# ╔════════════════════════════════════════════════════════════╗
# ║        🤖 AGI AUTOMATION - INTELIGÊNCIA GERAL ARTIFICIAL  ║
# ║  O sistema está operando automaticamente no mercado.      ║
# ╚════════════════════════════════════════════════════════════╝
# ✅ Todos os componentes iniciados
```

#### B. Via CLI (Mais Flexível)

```bash
# Iniciar
python neural_layers/04_decisao/agi_cli.py start

# Monitorar status em tempo real
python neural_layers/04_decisao/agi_cli.py status

# Ver trades abertos
python neural_layers/04_decisao/agi_cli.py trades

# Ver alertas
python neural_layers/04_decisao/agi_cli.py alerts

# Ver portfólio
python neural_layers/04_decisao/agi_cli.py portfolio
```

#### C. Via GUI (Mais Visual)

```bash
# Abrir a interface gráfica
python lextrader_gui.py

# Ir na aba "Automação" e clicar em "Iniciar"
# (Será adicionado na próxima atualização)
```

### 2. **Configurar Antes de Iniciar**

#### A. Via CLI

```bash
# Ver configuração atual
python neural_layers/04_decisao/agi_cli.py config show

# Adicionar símbolo
python neural_layers/04_decisao/agi_cli.py config symbols add --symbol BTCUSD

# Remover símbolo
python neural_layers/04_decisao/agi_cli.py config symbols remove --symbol AUDCAD

# Listar símbolos
python neural_layers/04_decisao/agi_cli.py config symbols list

# Definir máximo de trades por dia
python neural_layers/04_decisao/agi_cli.py config set --key max_daily_trades --value 50

# Ativar modo LIVE (⚠️ CUIDADO!)
python neural_layers/04_decisao/agi_cli.py config set --key enable_live_trading --value true
```

#### B. Via Arquivo JSON

Editar `agi_automation_config.json`:

```json
{
  "analysis_frequency": "NORMAL",
  "max_concurrent_trades": 5,
  "max_daily_trades": 50,
  "risk_per_trade": 0.02,
  "max_daily_risk": 0.05,
  "enable_live_trading": false,
  "enable_paper_trading": true,
  "symbols": [
    "EURUSD",
    "GBPUSD",
    "AUDUSD",
    "BTC",
    "ETH",
    "BNB"
  ]
}
```

### 3. **Controlar Durante Execução**

```bash
# Pausar (posições continuam monitoradas)
python neural_layers/04_decisao/agi_cli.py pause

# Retomar
python neural_layers/04_decisao/agi_cli.py resume

# Parar (fechar tudo)
python neural_layers/04_decisao/agi_cli.py stop

# Monitorar em tempo real
python neural_layers/04_decisao/agi_cli.py status
```

---

## 📊 Componentes Detalhados

### 1. **AGI Automation Engine** (`agi_automation_engine.py`)

**Responsabilidades:**
- Coordena análise, decisão e execução
- Gerencia threads de processamento
- Controla limites diários de risco
- Mantém histórico de operações

**Configuração:**
```python
from agi_automation_engine import AGIAutomationEngine, AutomationConfig, AnalysisFrequency

config = AutomationConfig(
    analysis_frequency=AnalysisFrequency.NORMAL,  # FAST (5m), NORMAL (15m), SLOW (60m)
    max_concurrent_trades=5,
    max_daily_trades=50,
    risk_per_trade=0.02,      # 2% por trade
    max_daily_risk=0.05,      # 5% máximo diário
    enable_live_trading=False,
    symbols=['EURUSD', 'GBPUSD', 'BTC', 'ETH']
)

engine = AGIAutomationEngine(config)
engine.start()
```

### 2. **Market Monitor** (`market_monitor.py`)

**Responsabilidades:**
- Monitora preços em tempo real
- Detecta oportunidades de trading
- Gera alertas de mercado
- Calcula métricas técnicas

**Exemplo de Uso:**
```python
from market_monitor import MarketMonitor

monitor = MarketMonitor(
    symbols=['EURUSD', 'BTC', 'ETH'],
    update_frequency=60  # A cada 60 segundos
)

# Registrar callback para oportunidades
def on_opportunity(data):
    print(f"Oportunidade encontrada: {data}")

monitor.register_callback('on_opportunity', on_opportunity)
monitor.start()
```

### 3. **Portfolio Manager** (`portfolio_manager.py`)

**Responsabilidades:**
- Gerencia posições abertas
- Calcula P&L em tempo real
- Aplica stop loss e take profit
- Rebalanceia portfólio

**Exemplo de Uso:**
```python
from portfolio_manager import PortfolioManager

portfolio = PortfolioManager(
    initial_capital=100000,
    max_positions=10
)

# Abrir posição
position = portfolio.open_position(
    symbol='EURUSD',
    entry_price=1.0850,
    quantity=10,
    stop_loss=1.0830,
    take_profit=1.0900
)

# Monitorar
metrics = portfolio.get_metrics()
print(f"P&L Total: ${metrics['total_pnl']}")

# Fechar posição
portfolio.close_position(position.position_id, exit_price=1.0900)
```

---

## 📈 Fluxo de Trading Automático

### Exemplo Completo

```
SEGUNDA-FEIRA, 09:30 AM
├─ Market Monitor detecta breakout em EURUSD
│  └─ Preço acima de resistência, volume alto, RSI positivo
│
├─ AGI Automation Engine recebe sinal
│  └─ Coordena análise multi-estratégia
│
├─ Decision Engine analisa:
│  ├─ Estratégia Forex: BUY com 87% confiança
│  ├─ Estratégia de Arbitragem: Oportunidade detectada
│  ├─ Estratégia Autônoma: Sinal BUY
│  └─ Risk Manager: ✅ Trade aprovado
│
├─ Trade Executor executa BUY
│  ├─ Conecta com cTrader
│  ├─ Coloca ordem de 10 lotes
│  ├─ Entry price: 1.0850
│  ├─ Stop Loss: 1.0830 (20 pips)
│  └─ Take Profit: 1.0900 (50 pips)
│
├─ Portfolio Manager registra posição
│  ├─ Posição ID: EURUSD_1234567890
│  ├─ Capital utilizado: $10,850
│  └─ Posição monitorada continuamente
│
├─ DURANTE OS PRÓXIMOS 2 HORAS
│  ├─ Price sobe para 1.0875 → P&L: +$250
│  ├─ Market Monitor gera alerta de consolidação
│  ├─ Portfolio monitora stop loss continuamente
│  └─ P&L atualizado em tempo real
│
└─ 11:45 AM - TAKE PROFIT ATINGIDO
   ├─ Preço atinge 1.0900
   ├─ Portfolio Manager fecha posição automaticamente
   ├─ Trade finalizado com lucro de $500 (4.6%)
   ├─ Estatísticas atualizadas
   └─ P&L total do dia: +$500
```

---

## 🎯 Estratégias Ativas

A automação suporta múltiplas estratégias simultâneas:

### 1. **Estratégia Forex** (8 indicadores)
- SMA, EMA, RSI, MACD, Bollinger Bands, etc.
- Análise multi-timeframe
- Gestão de risco com ATR

### 2. **Estratégia de Arbitragem** (4 tipos)
- Arbitragem Espacial
- Arbitragem Triangular
- Arbitragem Estatística
- Arbitragem Cross-Market

### 3. **Estratégia Autônoma** (Q-Learning)
- Aprendizado por reforço
- Adaptação contínua ao mercado
- Melhoria de performance

### 4. **Estratégia Evolutiva** (Algoritmos Genéticos)
- Otimização de parâmetros
- Evolução de estratégias

---

## ⚠️ Limites e Proteções de Risco

### Limites Automáticos

- **Max Daily Trades**: 50 trades por dia
- **Max Daily Risk**: 5% do capital
- **Risk per Trade**: 2% do capital
- **Max Concurrent Positions**: 5 posições abertas
- **Daily Loss Limit**: 5% leva a pausa automática

### Stop Loss Obrigatório

```python
# SEMPRE definir stop loss
position = portfolio.open_position(
    symbol='EURUSD',
    entry_price=1.0850,
    quantity=10,
    stop_loss=1.0830,  # ← OBRIGATÓRIO
    take_profit=1.0900
)
```

### Validação de Risco

```python
# Risk Manager valida cada trade
risk_check = risk_manager.check_trade(decision)
if not risk_check['allowed']:
    print(f"Trade bloqueado: {risk_check['reason']}")
```

---

## 📊 Monitoramento em Tempo Real

### Via CLI

```bash
# Status completo
python agi_cli.py status

# Saída:
# Estado: RUNNING
# Uptime: 2h 34m 12s
# Análises: 156 (última 2 min atrás)
# Decisões: 23 (BUY: 8, SELL: 7, HOLD: 8)
# Trades: 3 abertos, 5 hoje
# Portfolio: Capital $100k → $101,230.50 (+1.23%)
```

### Via Arquivo JSON

```bash
# Importar estado
import json

with open('agi_automation_state.json') as f:
    state = json.load(f)
    
print(f"Análises: {state['stats']['total_analyses']}")
print(f"P&L: ${state['stats']['total_profit']}")
```

---

## 🔧 Integração Avançada

### Registrar Callbacks Customizados

```python
from agi_automation_orchestrator import AGIOrchestrator

orchestrator = AGIOrchestrator()

def custom_on_trade_executed(data):
    """Callback customizado para notificar webhook"""
    import requests
    requests.post(
        'https://seu-webhook.com/trade',
        json=data
    )

orchestrator.automation_engine.register_callback(
    'on_trade_executed',
    custom_on_trade_executed
)

orchestrator.start()
```

### Usar Componentes Individuais

```python
# Usar apenas o monitor
from market_monitor import MarketMonitor

monitor = MarketMonitor(['EURUSD', 'BTC'])
monitor.start()

# Verificar alertas
for alert in monitor.alerts:
    print(f"{alert.severity}: {alert.message}")
```

---

## 📝 Logging e Debugging

### Arquivos de Log

- `agi_automation.log` - Log principal
- `market_monitor.log` - Monitor de mercado
- `portfolio_manager.log` - Gerenciador de portfólio
- `decision_engine.log` - Motor de decisão

### Ajustar Nível de Log

```python
from loguru import logger

# Verbose (mostra tudo)
logger.add("agi_detailed.log", level="DEBUG")

# Normal (informações importantes)
logger.add("agi.log", level="INFO")

# Apenas erros
logger.add("agi_errors.log", level="ERROR")
```

---

## ✅ Checklist de Implementação

- [ ] Instalar dependências: `pip install -r requirements_autotrader.txt`
- [ ] Configurar API keys nos arquivos `.env`
- [ ] Definir símbolos em `agi_automation_config.json`
- [ ] Testar em Paper Trading (recomendado)
- [ ] Ajustar limites de risco conforme seu perfil
- [ ] Revisar histórico de trades em backtesting
- [ ] Monitorar primeira semana em tempo real
- [ ] Ativar Live Trading apenas se tudo funcionar

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| Nenhum trade executado | Verificar `agi_automation_config.json`, aumentar frequência de análise |
| Perda rápida de capital | Reduzir `risk_per_trade`, aumentar `stop_loss_pct` |
| Automação congela | Reiniciar: `python agi_cli.py stop` → `python agi_cli.py start` |
| Erro de API | Verificar API keys, testar conectividade com broker |
| Memory leak | Monitorar com `python -m memory_profiler` |

---

## 📞 Suporte

- Logs: `agi_automation.log`
- Histórico de decisões: `agi_automation_state.json`
- Estado de portfólio: `portfolio_state.json`

---

**Última Atualização**: Janeiro 16, 2026
**Versão**: 1.0
**Status**: ✅ Produção Pronta
