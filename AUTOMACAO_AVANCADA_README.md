# 🤖 Sistema de Automação Avançada - LEXTRADER-IAG 4.0

## 📋 Visão Geral

Sistema completo de automação inteligente que orquestra todos os componentes do LEXTRADER-IAG 4.0, executando análises, monitoramento e trading de forma autônoma.

---

## ✨ Funcionalidades Principais

### 1. Orquestração Inteligente
- ✅ Gerenciamento automático de tarefas
- ✅ Priorização dinâmica
- ✅ Retry automático em falhas
- ✅ Agendamento flexível
- ✅ Execução paralela

### 2. Análises Automatizadas
- ✅ Análise de criptomoedas (a cada 5 min)
- ✅ Análise de forex (a cada 10 min)
- ✅ Scan de arbitragem (a cada 3 min)
- ✅ Análise unificada (a cada 15 min)

### 3. Monitoramento Contínuo
- ✅ Métricas em tempo real
- ✅ Saúde do sistema
- ✅ Alertas automáticos
- ✅ Logs detalhados

### 4. Modos de Operação
- 🔵 **MANUAL**: Controle total do usuário
- 🟡 **SCHEDULED**: Execução agendada
- 🟢 **CONTINUOUS**: Execução contínua
- 🟣 **ADAPTIVE**: Adaptação inteligente

---

## 📦 Componentes

### 1. Advanced Automation Orchestrator
**Arquivo**: `advanced_automation_orchestrator.py`

Orquestrador principal que gerencia todas as tarefas de automação.

**Classes Principais**:
- `AdvancedAutomationOrchestrator`: Gerenciador principal
- `AutomationTask`: Representa uma tarefa
- `AutomationMetrics`: Métricas do sistema
- `SystemHealth`: Saúde do sistema

**Funcionalidades**:
- Criação e gerenciamento de tarefas
- Execução assíncrona
- Retry automático
- Agendamento recorrente
- Salvamento de estado

### 2. Automation CLI
**Arquivo**: `automation_cli.py`

Interface de linha de comando interativa para controle da automação.

**Comandos Disponíveis**:
```
init [mode]      - Inicializa orquestrador
start            - Inicia automação
stop             - Para automação
status           - Mostra status
tasks [filter]   - Lista tarefas
add              - Adiciona tarefa
remove <id>      - Remove tarefa
run              - Executa tarefas uma vez
save [file]      - Salva estado
load [file]      - Carrega estado
config           - Mostra configurações
clear            - Limpa tela
help             - Ajuda
quit/exit        - Sai
```

### 3. Start Automation
**Arquivo**: `start_automation.py`

Script de inicialização rápida com configurações padrão.

**Funcionalidades**:
- Inicialização automática
- Modo contínuo por padrão
- Salvamento automático de estado
- Estatísticas finais

---

## 🚀 Como Usar

### Opção 1: CLI Interativo (Recomendado)

```bash
python automation_cli.py
```

**Fluxo de uso**:
```
🤖 automation> init continuous
🤖 automation> start
🤖 automation> status
🤖 automation> tasks
🤖 automation> quit
```

### Opção 2: Inicialização Rápida

```bash
python start_automation.py
```

Sistema inicia automaticamente em modo contínuo.

### Opção 3: Programático

```python
from advanced_automation_orchestrator import (
    AdvancedAutomationOrchestrator,
    AutomationMode
)
import asyncio

async def main():
    # Criar orquestrador
    orchestrator = AdvancedAutomationOrchestrator(
        mode=AutomationMode.CONTINUOUS
    )
    
    # Inicializar
    await orchestrator.initialize_components()
    
    # Agendar tarefas
    orchestrator.schedule_recurring_tasks()
    
    # Executar
    await orchestrator.run_continuous()

asyncio.run(main())
```

---

## ⚙️ Configuração

### Modos de Operação

#### MANUAL
```python
orchestrator = AdvancedAutomationOrchestrator(
    mode=AutomationMode.MANUAL
)
```
- Controle total do usuário
- Tarefas executadas sob demanda
- Ideal para testes

#### SCHEDULED
```python
orchestrator = AdvancedAutomationOrchestrator(
    mode=AutomationMode.SCHEDULED
)
```
- Execução agendada
- Intervalos configuráveis
- Ideal para análises periódicas

#### CONTINUOUS
```python
orchestrator = AdvancedAutomationOrchestrator(
    mode=AutomationMode.CONTINUOUS
)
```
- Execução contínua
- Loop infinito
- Ideal para produção

#### ADAPTIVE
```python
orchestrator = AdvancedAutomationOrchestrator(
    mode=AutomationMode.ADAPTIVE
)
```
- Adaptação inteligente
- Ajuste automático de intervalos
- Ideal para otimização

---

## 📊 Tarefas Padrão

### 1. Análise de Criptomoedas
- **Intervalo**: 5 minutos
- **Prioridade**: Alta
- **Símbolo**: BTC/USDT
- **Função**: Análise técnica completa

### 2. Análise de Forex
- **Intervalo**: 10 minutos
- **Prioridade**: Alta
- **Par**: EUR/USD
- **Função**: Análise de forex

### 3. Scan de Arbitragem
- **Intervalo**: 3 minutos
- **Prioridade**: Crítica
- **Assets**: BTC/USDT, ETH/USDT, BNB/USDT
- **Exchanges**: Binance, Coinbase, Kraken

### 4. Análise Unificada
- **Intervalo**: 15 minutos
- **Prioridade**: Média
- **Mercados**: Crypto, Forex, Arbitragem

### 5. Atualização de Métricas
- **Intervalo**: 1 minuto
- **Prioridade**: Baixa
- **Função**: Atualiza estatísticas

### 6. Verificação de Saúde
- **Intervalo**: 2 minutos
- **Prioridade**: Média
- **Função**: Monitora sistema

---

## 📈 Métricas e Monitoramento

### Métricas Disponíveis

```python
metrics = orchestrator.metrics

print(f"Total de Tarefas: {metrics.total_tasks}")
print(f"Concluídas: {metrics.completed_tasks}")
print(f"Falhadas: {metrics.failed_tasks}")
print(f"Taxa de Sucesso: {metrics.success_rate}%")
print(f"Tempo Médio: {metrics.average_execution_time}s")
```

### Saúde do Sistema

```python
health = orchestrator.health

print(f"Status: {health.status}")
print(f"CPU: {health.cpu_usage}%")
print(f"Memória: {health.memory_usage}%")
print(f"Disco: {health.disk_usage}%")
print(f"Uptime: {health.uptime_hours}h")
```

---

## 🔧 Criando Tarefas Customizadas

### Exemplo 1: Tarefa Simples

```python
def minha_funcao():
    print("Executando minha tarefa!")
    return "Sucesso"

task_id = orchestrator.create_task(
    name="Minha Tarefa",
    description="Descrição da tarefa",
    function=minha_funcao,
    priority=TaskPriority.MEDIUM
)
```

### Exemplo 2: Tarefa Assíncrona

```python
async def minha_funcao_async():
    await asyncio.sleep(1)
    return "Resultado"

task_id = orchestrator.create_task(
    name="Tarefa Assíncrona",
    description="Tarefa com async/await",
    function=minha_funcao_async,
    priority=TaskPriority.HIGH
)
```

### Exemplo 3: Tarefa Recorrente

```python
task_id = orchestrator.create_task(
    name="Tarefa Recorrente",
    description="Executa a cada 5 minutos",
    function=minha_funcao,
    priority=TaskPriority.MEDIUM,
    interval_minutes=5  # Recorrente
)
```

### Exemplo 4: Tarefa com Parâmetros

```python
def analisar_simbolo(symbol: str, timeframe: str):
    print(f"Analisando {symbol} em {timeframe}")
    return f"Análise de {symbol} concluída"

task_id = orchestrator.create_task(
    name="Análise Customizada",
    description="Análise de símbolo específico",
    function=analisar_simbolo,
    args=('ETH/USDT', '1h'),
    priority=TaskPriority.HIGH
)
```

---

## 💾 Persistência de Estado

### Salvar Estado

```python
# Salvar em arquivo padrão
orchestrator.save_state()

# Salvar em arquivo específico
orchestrator.save_state("meu_estado.json")
```

### Carregar Estado

```python
# Carregar de arquivo padrão
state = orchestrator.load_state()

# Carregar de arquivo específico
state = orchestrator.load_state("meu_estado.json")
```

### Formato do Estado

```json
{
  "mode": "CONTINUOUS",
  "start_time": "2026-01-15T01:30:00",
  "metrics": {
    "total_tasks": 42,
    "completed_tasks": 38,
    "failed_tasks": 4,
    "success_rate": 90.5
  },
  "health": {
    "status": "HEALTHY",
    "cpu_usage": 45.2,
    "memory_usage": 62.8
  },
  "tasks": {
    "task_123": {
      "name": "Análise BTC",
      "status": "COMPLETED",
      "result": "..."
    }
  }
}
```

---

## 🎯 Casos de Uso

### 1. Trading Automatizado

```python
# Inicializar em modo contínuo
orchestrator = AdvancedAutomationOrchestrator(
    mode=AutomationMode.CONTINUOUS
)

# Adicionar análises frequentes
orchestrator.create_task(
    name="Análise BTC",
    function=analyze_btc,
    interval_minutes=1,  # A cada minuto
    priority=TaskPriority.CRITICAL
)

# Executar
await orchestrator.run_continuous()
```

### 2. Monitoramento de Mercado

```python
# Modo agendado para análises periódicas
orchestrator = AdvancedAutomationOrchestrator(
    mode=AutomationMode.SCHEDULED
)

# Análises a cada 15 minutos
for symbol in ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']:
    orchestrator.create_task(
        name=f"Monitor {symbol}",
        function=monitor_symbol,
        args=(symbol,),
        interval_minutes=15
    )
```

### 3. Backtesting Automatizado

```python
# Modo manual para controle preciso
orchestrator = AdvancedAutomationOrchestrator(
    mode=AutomationMode.MANUAL
)

# Adicionar testes
for strategy in strategies:
    orchestrator.create_task(
        name=f"Backtest {strategy.name}",
        function=run_backtest,
        args=(strategy,),
        priority=TaskPriority.HIGH
    )

# Executar todos de uma vez
await orchestrator.process_task_queue()
```

---

## 📊 Dashboard e Visualização

### Status em Tempo Real

```python
# Obter status completo
status = orchestrator.get_status()

print(f"Modo: {status['mode']}")
print(f"Uptime: {status['uptime_hours']:.2f}h")
print(f"Taxa de Sucesso: {status['metrics']['success_rate']:.1f}%")
```

### Imprimir Status Formatado

```python
# Mostra dashboard completo
orchestrator.print_status()
```

**Saída**:
```
================================================================================
🤖 STATUS DO ORQUESTRADOR DE AUTOMAÇÃO
================================================================================

📊 Informações Gerais:
  Modo: CONTINUOUS
  Status: 🟢 ATIVO
  Uptime: 2.5 horas

📈 Métricas:
  Total de Tarefas: 42
  Concluídas: 38
  Falhadas: 4
  Taxa de Sucesso: 90.5%
  Tempo Médio: 1.23s

🏥 Saúde do Sistema:
  Status: 🟢 HEALTHY
  CPU: 45.2%
  Memória: 62.8%
  Disco: 35.1%

📋 Tarefas:
  Total: 42
  Pendentes: 0
  Em Execução: 0
  Concluídas: 38
  Falhadas: 4

================================================================================
```

---

## 🔔 Alertas e Notificações

### Sistema de Alertas (Futuro)

```python
# Configurar alertas
orchestrator.configure_alerts(
    email="seu@email.com",
    telegram_token="seu_token",
    slack_webhook="seu_webhook"
)

# Alertas automáticos para:
# - Tarefas falhadas
# - CPU/Memória alta
# - Oportunidades de trading
# - Erros críticos
```

---

## 🛠️ Troubleshooting

### Problema: Tarefas não executam

**Solução**:
```python
# Verificar se orquestrador está rodando
if not orchestrator.is_running:
    orchestrator.start()

# Verificar fila de tarefas
print(f"Tarefas pendentes: {len(orchestrator.task_queue)}")

# Processar manualmente
await orchestrator.process_task_queue()
```

### Problema: Alto uso de CPU

**Solução**:
```python
# Aumentar intervalo entre tarefas
for task in orchestrator.tasks.values():
    if task.interval_minutes and task.interval_minutes < 5:
        task.interval_minutes = 5

# Reduzir número de tarefas simultâneas
# Implementar throttling
```

### Problema: Tarefas falhando

**Solução**:
```python
# Ver tarefas falhadas
failed_tasks = [
    t for t in orchestrator.tasks.values()
    if t.status == TaskStatus.FAILED
]

for task in failed_tasks:
    print(f"Tarefa: {task.name}")
    print(f"Erro: {task.error}")
    print(f"Tentativas: {task.retry_count}/{task.max_retries}")
```

---

## 📚 Dependências

### Obrigatórias
```bash
pip install asyncio schedule
```

### Opcionais (Recomendadas)
```bash
pip install psutil  # Para métricas de sistema
```

---

## 🎓 Exemplos Avançados

### Exemplo 1: Pipeline de Análise

```python
async def pipeline_completo():
    orchestrator = AdvancedAutomationOrchestrator(
        mode=AutomationMode.SCHEDULED
    )
    
    await orchestrator.initialize_components()
    
    # Etapa 1: Coleta de dados
    orchestrator.create_task(
        name="Coleta de Dados",
        function=coletar_dados,
        priority=TaskPriority.CRITICAL
    )
    
    # Etapa 2: Análise técnica
    orchestrator.create_task(
        name="Análise Técnica",
        function=analisar_tecnicamente,
        priority=TaskPriority.HIGH
    )
    
    # Etapa 3: Geração de sinais
    orchestrator.create_task(
        name="Geração de Sinais",
        function=gerar_sinais,
        priority=TaskPriority.HIGH
    )
    
    # Etapa 4: Execução de trades
    orchestrator.create_task(
        name="Execução de Trades",
        function=executar_trades,
        priority=TaskPriority.CRITICAL
    )
    
    # Executar pipeline
    await orchestrator.process_task_queue()
```

### Exemplo 2: Monitoramento Multi-Exchange

```python
exchanges = ['binance', 'coinbase', 'kraken', 'bitfinex']
symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']

for exchange in exchanges:
    for symbol in symbols:
        orchestrator.create_task(
            name=f"Monitor {exchange} - {symbol}",
            function=monitor_exchange,
            args=(exchange, symbol),
            interval_minutes=2,
            priority=TaskPriority.HIGH
        )
```

---

## ✨ Conclusão

O Sistema de Automação Avançada do LEXTRADER-IAG 4.0 oferece:

- ✅ Automação completa de análises
- ✅ Orquestração inteligente de tarefas
- ✅ Monitoramento contínuo
- ✅ Métricas em tempo real
- ✅ Interface CLI interativa
- ✅ Persistência de estado
- ✅ Retry automático
- ✅ Priorização dinâmica

**Status**: ✅ PRONTO PARA PRODUÇÃO

---

**Data**: 15/01/2026
**Versão**: 1.0.0
**Autor**: Kiro AI Assistant
