# CHECKLIST DE INSTALACAO - LEXTRADER-IAG 4.0

Data: [PREENCHER]
Versao: 4.0.1
Status Final: [ ] COMPLETO [ ] INCOMPLETO [ ] COM ERROS

---

## ✅ FASE 1: VERIFICACOES INICIAIS

- [ ] Python 3.9+ instalado
- [ ] Python acessivel via `python --version`
- [ ] pip funcionando via `pip --version`
- [ ] Diretorio projeto LEXTRADER-IAG-4.0 existe
- [ ] Terminal aberto no diretorio correto

---

## ✅ FASE 2: ESTRUTURA DE DIRETORIOS

### Camadas Neurais

- [ ] `neural_layers/01_sensorial/` criado
- [ ] `neural_layers/02_processamento/` criado
- [ ] `neural_layers/03_memoria_saida/` criado
- [ ] `neural_layers/04_decisao/` criado
- [ ] `neural_layers/05_quantico/` criado
- [ ] `neural_layers/06_seguranca/` criado

### Diretorios Auxiliares

- [ ] `dashboards/` criado
- [ ] `components/` criado
- [ ] `lextrader_memory/` criado
- [ ] `logs/` criado

---

## ✅ FASE 3: DEPENDENCIAS PYTHON

### Essenciais (CRITICO)

- [ ] numpy: `pip list | findstr numpy`
- [ ] pandas: `pip list | findstr pandas`
- [ ] loguru: `pip list | findstr loguru`
- [ ] ccxt: `pip list | findstr ccxt`
- [ ] yfinance: `pip list | findstr yfinance`

### Importantes (NECESSARIO)

- [ ] matplotlib: `pip list | findstr matplotlib`
- [ ] python-dotenv: `pip list | findstr python-dotenv`
- [ ] python-binance: `pip list | findstr python-binance`
- [ ] ta: `pip list | findstr ta`
- [ ] schedule: `pip list | findstr schedule`

### Opcionais (RECOMENDADO)

- [ ] scikit-learn: `pip list | findstr scikit-learn`
- [ ] pytest: `pip list | findstr pytest`
- [ ] requests: `pip list | findstr requests`

---

## ✅ FASE 4: ARQUIVOS PRINCIPAIS

### Instalador e Launcher

- [ ] `start_lextrader.bat` existe e e executavel
- [ ] `LAUNCHER.bat` existe e e executavel
- [ ] `LEXTRADER_INSTALLER.py` existe

### Automacao (Raiz do Projeto)

- [ ] `agi_automation_orchestrator.py` existe
- [ ] `agi_automation_engine.py` existe (se presente)
- [ ] `market_monitor.py` existe (se presente)
- [ ] `portfolio_manager.py` existe (se presente)

### Interface

- [ ] `lextrader_gui.py` existe
- [ ] `START_AGI_AUTOMATION.py` existe

### Configuracao

- [ ] `agi_automation_config.json` existe
- [ ] `.env` existe ou foi criado

---

## ✅ FASE 5: VALIDACAO DE SINTAXE PYTHON

Executar:

```bash
python -m py_compile agi_automation_orchestrator.py
python -m py_compile lextrader_gui.py
python -m py_compile START_AGI_AUTOMATION.py
```

- [ ] Nenhum erro de sintaxe encontrado

---

## ✅ FASE 6: TESTE DE IMPORTS BASICOS

Executar:

```bash
python -c "import numpy, pandas, loguru, ccxt, yfinance; print('OK')"
```

- [ ] Todos os imports funcionam

---

## ✅ FASE 7: TESTE DE ARQUIVO DE CONFIGURACAO

Executar:

```bash
python -c "import json; json.load(open('agi_automation_config.json'))"
```

- [ ] JSON valido e pode ser parseado

---

## ✅ FASE 8: TESTE DE ARQUIVO .ENV

- [ ] `.env` existe e pode ser lido
- [ ] Contem estrutura basica
- [ ] API keys foram adicionadas (ou placeholder)

---

## ✅ FASE 9: TESTE DE EXECUCAO

### Teste 1: Verificacao de Instalacao

```bash
python LEXTRADER_INSTALLER.py
# Escolha opcao 2 - Verificar Instalacao
```

- [ ] Relatorio exibe sem erros
- [ ] Mostra Python version OK
- [ ] Mostra diretorios criados
- [ ] Mostra pacotes instalados

### Teste 2: Teste do Menu

```bash
start start_lextrader.bat
```

- [ ] Menu principal exibe corretamente
- [ ] Todas as opcoes estao numeradas (1-8)
- [ ] Nenhuma mensagem de erro

---

## ✅ FASE 10: DOCUMENTACAO

- [ ] `GUIA_INSTALADOR.md` existe
- [ ] `.github/copilot-instructions.md` existe
- [ ] `AGI_AUTOMATION_GUIDE.md` existe (se presente)
- [ ] `AGI_AUTOMATION_README.md` existe (se presente)

---

## ✅ FASE 11: INTEGRACAO E COMPATIBILIDADE

- [ ] Sistema Windows 10+ (se aplicavel)
- [ ] Terminal reconhece arquivos .bat
- [ ] Python esta no PATH
- [ ] pip esta no PATH
- [ ] Sem conflitos de portas (se rede)

---

## ✅ FASE 12: SEGURANCA

- [ ] `.env` nao esta em version control (adicionar a .gitignore)
- [ ] API keys nao estao expostas no repositorio
- [ ] Permissoes de arquivo apropriadas
- [ ] Sem hardcoding de secrets em Python files

---

## ⚠️ PROBLEMAS CONHECIDOS E RESOLUCOES

### Problema: Python nao reconhecido

```
Solucao:
- [ ] Adicionar Python ao PATH do Windows
- [ ] Usar caminho completo: C:\Python39\python.exe
- [ ] Reinstalar Python com "Add to PATH" marcado
```

### Problema: pip nao encontrado

```
Solucao:
- [ ] Executar: python -m pip install --upgrade pip
- [ ] Verificar: python -m pip --version
- [ ] Se persistir, reinstalar Python
```

### Problema: Modulo nao encontrado

```
Solucao:
- [ ] Listar instalados: pip list
- [ ] Instalar faltantes: pip install NOME_DO_MODULO
- [ ] Atualizar todos: pip install -r requirements_autotrader.txt --upgrade
```

### Problema: JSON invalido em agi_automation_config.json

```
Solucao:
- [ ] Validar JSON em https://jsonlint.com/
- [ ] Verificar acentos e caracteres especiais
- [ ] Recriar arquivo usando LEXTRADER_INSTALLER.py (Opcao 3)
```

### Problema: AGI Automation nao inicia

```
Solucao:
- [ ] Verificar logs em logs/
- [ ] Confirmar API keys no .env
- [ ] Testar importacoes: python -c "from agi_automation_orchestrator import *"
- [ ] Re-executar INSTALLER (Opcao 1)
```

---

## 🎯 PROXIMOS PASSOS (POS-INSTALACAO)

1. [ ] Configurar API keys das exchanges:
   - [ ] Binance (BINANCE_KEY, BINANCE_SECRET)
   - [ ] cTrader (CTRADER_ID, CTRADER_SECRET)
   - [ ] Pionex (PIONEX_KEY, PIONEX_SECRET)

2. [ ] Revisar e customizar `agi_automation_config.json`:
   - [ ] Adicionar/remover simbolos
   - [ ] Ajustar intervalos de analise
   - [ ] Configurar limites de risco
   - [ ] Ativar/desativar estrategias

3. [ ] Testar com conta de papel (nao real):
   - [ ] Validar decisoes de mercado
   - [ ] Confirmar logica de risco
   - [ ] Monitorar por 1-2 dias

4. [ ] Implementar monitoramento:
   - [ ] Configurar alertas
   - [ ] Registrar logs
   - [ ] Revisar P&L diariamente

5. [ ] Opcional: Customizacoes avancadas:
   - [ ] Adicionar estrategias customizadas
   - [ ] Integrar com mais exchanges
   - [ ] Implementar webhooks
   - [ ] Criar alertas personalizados

---

## 📊 RESULTADOS FINAIS

### Teste de Performance

- [ ] Sistema inicia em < 10 segundos
- [ ] Monitor de mercado funciona
- [ ] CLI responde a comandos
- [ ] Sem erros em logs

### Capacidades Ativadas

- [ ] Leitura de dados Binance
- [ ] Leitura de dados Forex (se configurado)
- [ ] Analise de oportunidades de arbitragem
- [ ] Decisoes autonomas em tempo real
- [ ] Gerenciamento automatico de risco

### Status Final

```
[ ] COMPLETO - Tudo funcionando
[ ] COMPLETO COM AVISOS - Sistema funciona mas com alguns itens pendentes
[ ] INCOMPLETO - Alguns componentes faltam
[ ] ERRO CRITICO - Sistema nao funciona
```

---

## 📝 Observacoes e Notas

(Preencher com qualquer informacao adicional, problemas encontrados, customizacoes feitas, etc.)

```
[ESCREVER AQUI]




```

---

## ✍️ Assinatura de Confirmacao

Instalador: ___________________________
Data: ___________________________
Status: [ ] Aprovado [ ] Rejeita Aprovacao Pendente [ ] Falhou

---

**LEXTRADER-IAG 4.0** © 2025
Versao do Checklist: 1.0
