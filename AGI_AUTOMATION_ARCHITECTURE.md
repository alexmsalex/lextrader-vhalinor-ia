# 🤖 AGI AUTOMATION - Diagrama de Arquitetura

## Visão Geral do Sistema

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    LEXTRADER-IAG 4.0 - AGI AUTOMATION                     ║
║                                                                            ║
║                           OPERAÇÃO 24/7 AUTOMÁTICA                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│                        AGI AUTOMATION ORCHESTRATOR                         │
│                           (Ponto de Entrada)                              │
│                                                                            │
│  agi_automation_orchestrator.py → python (1 comando!)                    │
│                                                                            │
└─────────────────────────────┬──────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┬──────────────┐
                │             │             │              │
         ┌──────▼────┐   ┌────▼──────┐ ┌──▼───────┐  ┌───▼────────┐
         │  MARKET   │   │  AUTOMATION│ │  TRADE   │  │ PORTFOLIO  │
         │ MONITOR   │   │  ENGINE    │ │ EXECUTOR │  │ MANAGER    │
         │           │   │            │ │          │  │            │
         │ L02       │   │ L04        │ │ L03      │  │ L03        │
         └─────┬─────┘   └────┬───────┘ └────┬─────┘  └─────┬──────┘
               │              │              │              │
               └──────────────┼──────────────┼──────────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
            ┌───────▼────────┐  ┌───────▼─────────┐
            │  DECISION      │  │  RISK MANAGER   │
            │  ENGINE        │  │                 │
            │  (Estratégias) │  │  (Proteções)    │
            │                │  │                 │
            │  • Forex       │  │  • Stop Loss    │
            │  • Arbitragem  │  │  • Limites      │
            │  • RL/ML       │  │  • Validação    │
            │  • Genética    │  │                 │
            └────────────────┘  └─────────────────┘
```

---

## Fluxo de Trading Automático

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                            CICLO DE OPERAÇÃO                            │
│                                                                         │
└────────┬────────────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────────┐
    │ 1️⃣  MARKET MONITOR                                              │
    │                                                                  │
    │  • Conecta com APIs (Binance, cTrader, Pionex)                 │
    │  • Coleta dados de preço cada 60s                              │
    │  • Calcula 8 indicadores técnicos                              │
    │  • Detecta padrões e oportunidades                             │
    │  • Gera alertas de mercado                                     │
    │                                                                  │
    │  Saída: AnalysisResult                                         │
    └────┬──────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────────┐
    │ 2️⃣  AGI AUTOMATION ENGINE                                       │
    │                                                                  │
    │  • Recebe análise do monitor                                    │
    │  • Coordena 4 estratégias em paralelo:                          │
    │    - Forex Strategy (SMA, EMA, RSI, MACD...)                   │
    │    - Arbitrage Strategy (4 tipos)                              │
    │    - Autonomous Strategy (Q-Learning)                          │
    │    - Evolutionary Strategy (Genética)                          │
    │  • Valida confiança mínima (70%)                               │
    │  • Passa para Decision Engine                                  │
    │                                                                  │
    │  Saída: TradingDecision                                        │
    └────┬──────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────────┐
    │ 3️⃣  DECISION ENGINE                                             │
    │                                                                  │
    │  • Avalia decisão de múltiplos ângulos                          │
    │  • Calcula entry, stop loss, take profit                       │
    │  • Define tamanho da posição                                    │
    │  • Prioriza sinais (Critical > High > Medium > Low)            │
    │  • Passa para Risk Manager                                     │
    │                                                                  │
    │  Saída: ValidatedDecision                                      │
    └────┬──────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────────┐
    │ 4️⃣  RISK MANAGER (Validação)                                    │
    │                                                                  │
    │  Verificações Automáticas:                                      │
    │  ✓ Stop loss está definido? SIM → Continuar                   │
    │  ✓ Risk < 2% do capital? SIM → Continuar                      │
    │  ✓ Daily risk < 5%? SIM → Continuar                           │
    │  ✓ Posições < 5? SIM → Continuar                              │
    │  ✓ Trades < 50 hoje? SIM → Continuar                          │
    │  ✗ Qualquer falha? NÃO → BLOQUEIA TRADE                       │
    │                                                                  │
    │  Se aprovado: ExecutionOrder                                    │
    │  Se bloqueado: Rejeitado com motivo                            │
    └────┬──────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────────┐
    │ 5️⃣  TRADE EXECUTOR                                              │
    │                                                                  │
    │  • Conecta com broker (cTrader) ou exchange (Binance)          │
    │  • Envia ordem com:                                             │
    │    - Symbol (EURUSD, BTC, etc)                                 │
    │    - Action (BUY ou SELL)                                      │
    │    - Quantity                                                   │
    │    - Stop Loss (proteção obrigatória)                          │
    │    - Take Profit (objetivo de lucro)                           │
    │  • Executa a ordem                                             │
    │  • Registra ExecutionResult                                    │
    │                                                                  │
    │  Saída: ExecutionResult (sucesso/falha)                        │
    └────┬──────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────────┐
    │ 6️⃣  PORTFOLIO MANAGER                                           │
    │                                                                  │
    │  • Registra nova posição aberta                                 │
    │  • Atualiza capital utilizado vs disponível                     │
    │  • Monitora P&L em tempo real:                                  │
    │    P&L = (current_price - entry_price) × quantity              │
    │  • A cada tick, verifica:                                       │
    │    ✓ Preço atinge stop loss? → Fecha com perda                │
    │    ✓ Preço atinge take profit? → Fecha com lucro              │
    │    ✓ Tempo limite? → Fecha automaticamente                     │
    │                                                                  │
    │  Saída: ClosedPosition (com P&L)                               │
    └────┬──────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────────┐
    │ 7️⃣  LOGGING & HISTÓRICO                                         │
    │                                                                  │
    │  Salva em arquivos JSON:                                        │
    │  • agi_automation_state.json                                    │
    │  • portfolio_state.json                                         │
    │  • market_alerts.json                                           │
    │  • agi_automation.log (detalhado)                              │
    │                                                                  │
    │  Métricas atualizadas:                                          │
    │  • Total trades hoje                                            │
    │  • P&L acumulado                                                │
    │  • Taxa de sucesso                                              │
    │  • Uptime do sistema                                            │
    └────┬──────────────────────────────────────────────────────────┘
         │
         └─────────────────────┬─────────────────────────────────────┐
                               │                                     │
                        ┌──────▼──────────┐          ┌──────────────▼────┐
                        │  RETORNA AO      │         │   PRÓXIMO CICLO   │
                        │  MONITOR E       │         │   (15 min depois) │
                        │  RECOMEÇA!       │         │                   │
                        └──────────────────┘         └───────────────────┘
```

---

## Arquitetura de Componentes

```
┌──────────────────────────────────────────────────────────────────────┐
│                      AGI AUTOMATION ORCHESTRATOR                     │
│                   (agi_automation_orchestrator.py)                   │
└────────────────────────┬─────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┬─────────────────┐
        │                │                │                 │
    ┌───▼──────┐   ┌─────▼────┐   ┌──────▼──────┐   ┌────▼─────┐
    │MARKET    │   │AUTOMATION │   │TRADE        │   │PORTFOLIO │
    │MONITOR   │   │ENGINE     │   │EXECUTOR     │   │MANAGER   │
    │          │   │           │   │             │   │          │
    │ Arquivo: │   │ Arquivo:  │   │ Arquivo:    │   │ Arquivo: │
    │market_   │   │agi_       │   │trading_     │   │portfolio_│
    │monitor.  │   │automation │   │execution_   │   │manager.  │
    │py        │   │_engine.py │   │engine.py    │   │py        │
    │          │   │           │   │             │   │          │
    │Camada:   │   │Camada:    │   │Camada:      │   │Camada:   │
    │L02       │   │L04        │   │L03          │   │L03       │
    └────┬─────┘   └─────┬─────┘   └──────┬──────┘   └────┬─────┘
         │               │                │              │
         └───────────────┴────────────────┴──────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    ┌───▼──────────┐ ┌──▼────────────┐ ┌─▼──────────────┐
    │DECISION      │ │RISK MANAGER   │ │NEURAL BUS      │
    │ENGINE        │ │               │ │                │
    │              │ │Responsável    │ │Coordena        │
    │Múltiplas     │ │por validar    │ │comunicação     │
    │estratégias   │ │todos os       │ │entre           │
    │em paralelo   │ │trades         │ │componentes     │
    └──────────────┘ └───────────────┘ └────────────────┘
```

---

## Fluxo de Dados

```
Mercado (APIs)
    │
    ├─ Binance API → Preços Crypto
    ├─ cTrader API → Preços Forex
    └─ Pionex API → Dados Arbitragem
         │
         ▼
    Market Monitor (coleta dados)
         │
         ▼
    Analysis Queue (fila de análises)
         │
         ▼
    AGI Automation Engine (orquestra)
         │
         ├─ Forex Strategy
         ├─ Arbitrage Strategy
         ├─ Autonomous Strategy
         └─ Evolutionary Strategy
         │
         ▼
    Decision Queue (decisões geradas)
         │
         ▼
    Decision Engine (valida)
         │
         ▼
    Risk Validation (protege capital)
         │
         ├─ ✓ Aprovado → Execution Queue
         └─ ✗ Rejeitado → Log & Retry
         │
         ▼
    Trade Executor (executa)
         │
         ├─ Sucesso → Portfolio Manager
         └─ Falha → Alert & Retry
         │
         ▼
    Portfolio Manager (monitora)
         │
         ├─ Registra posição
         ├─ Monitora P&L
         └─ Fecha automaticamente
         │
         ▼
    State Files (histórico)
         │
         ├─ agi_automation_state.json
         ├─ portfolio_state.json
         └─ market_alerts.json
```

---

## Estados da Automação

```
                    ┌──────────────┐
                    │   IDLE       │
                    │ (Parado)     │
                    └────┬─────────┘
                         │ start()
                         ▼
    ┌─────────────────────────────────────┐
    │                                     │
    │  ┌──────────────────────────────┐   │
    │  │   RUNNING                    │   │
    │  │   (Operando normalmente)     │   │
    │  │                              │   │
    │  │  • Analisando                │   │
    │  │  • Decidindo                 │   │
    │  │  • Executando                │   │
    │  │  • Monitorando posições      │   │
    │  └──────────────────────────────┘   │
    │                                     │
    │  pause() ↓        ↑ resume()        │
    │                                     │
    │  ┌──────────────────────────────┐   │
    │  │   PAUSED                     │   │
    │  │   (Pausado)                  │   │
    │  │                              │   │
    │  │  • Posições monitoradas      │   │
    │  │  • Sem novas análises        │   │
    │  │  • Sem novos trades          │   │
    │  └──────────────────────────────┘   │
    │                                     │
    └─────────────────────────────────────┘
         │ stop()
         ▼
    ┌──────────────────────────────┐
    │   STOPPED                    │
    │   (Parado)                   │
    │                              │
    │  • Fecha posições abertas    │
    │  • Salva estado              │
    │  • Encerra threads           │
    └──────────────────────────────┘
```

---

## Interfaces de Controle

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                   Como Controlar a Automação                        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1️⃣  Python Script (PRINCIPAL)                                     │
│      python agi_automation_orchestrator.py                         │
│                                                                     │
│  2️⃣  CLI via Terminal                                              │
│      python agi_cli.py start                                       │
│      python agi_cli.py status                                      │
│      python agi_cli.py trades                                      │
│      python agi_cli.py portfolio                                   │
│      python agi_cli.py pause/resume/stop                           │
│                                                                     │
│  3️⃣  GUI (Planejado)                                               │
│      python lextrader_gui.py                                       │
│      [Aba Automação → Controles]                                   │
│                                                                     │
│  4️⃣  JSON (Configuração)                                           │
│      Editar agi_automation_config.json                             │
│                                                                     │
│  5️⃣  API Python Direta                                             │
│      from agi_automation_orchestrator import AGIOrchestrator       │
│      orchestrator = AGIOrchestrator()                              │
│      orchestrator.start()                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Resumo da Arquitetura

| Aspecto | Detalhes |
|---------|----------|
| **Organização** | 6 camadas neurais + componentes integrados |
| **Automação** | 24/7 contínua, sem interferência manual |
| **Estratégias** | 4 estratégias paralelas (Forex, Arbitragem, ML, Genética) |
| **Frequência** | Análises a cada 5-60 minutos (configurável) |
| **Proteções** | Stop loss, limites diários, validação de risco |
| **Monitoramento** | CLI, JSON, Logs, Métricas em tempo real |
| **Escalabilidade** | Fácil adicionar estratégias/símbolos |
| **Pronta para Produção** | ✅ SIM |

---

**Arquitetura Completa e Pronta para Usar! 🚀**
