# 🔴 Camada Sensorial - Neural Layer 01

## Descrição
Esta camada é responsável pela **entrada de dados** e **percepção sensorial** do sistema LEXTRADER-IAG 4.0.

## Função Principal
- **Coleta de dados** de mercado em tempo real
- **Análise de feeds** de preços e volumes
- **Processamento de sinais** de entrada
- **Detecção de padrões** iniciais

## Componentes Principais

### Análise de Mercado
- `crypto_analysis_advanced.py` - Análise de criptomoedas
- `forex_analysis_advanced.py` - Análise de forex
- `arbitrage_analysis_advanced.py` - Análise de arbitragem
- `unified_market_analyzer.py` - Análise unificada de mercados

### Sistema de Dados de Criptomoedas ⭐
- `crypto_data_collector.py` - Coletor de dados das top 20 criptos
- `crypto_data_updater.py` - Atualizador automático de dados
- `crypto_data_analyzer.py` - Analisador estatístico de dados
- `crypto_data/` - Diretório com 19,602 registros históricos

### Sistema de Dados de Forex ⭐ NOVO
- `forex_data_collector.py` - Coletor de dados dos top 20 pares
- `forex_data_analyzer.py` - Analisador estatístico de dados
- `forex_data/` - Diretório com 21,900 registros históricos

### APIs e Integrações
- `binance_api.py` - Integração com Binance
- `ctrader_api.py` - Integração com cTrader
- `oracle_data.py` - Oráculo de dados

### Diagnósticos
- `deep_diagnostics.py` - Diagnósticos profundos do sistema

## 📊 Dados de Criptomoedas

### Estatísticas
- **20 criptomoedas** coletadas
- **19,602 registros** históricos (3 anos)
- **Retorno médio**: +201.31%
- **Volatilidade média**: 4.24%

### Top 5 Criptomoedas por Retorno
1. SOL (Solana) - +903.80%
2. XRP (Ripple) - +588.84%
3. BTC (Bitcoin) - +456.96%
4. TRX (Tron) - +447.78%
5. BCH (Bitcoin Cash) - +360.40%

### Uso
```bash
# Coletar dados
python crypto_data_collector.py

# Atualizar dados
python crypto_data_updater.py

# Analisar dados
python crypto_data_analyzer.py
```

## 💱 Dados de Forex

### Estatísticas
- **20 pares forex** coletados (7 Majors + 13 Cross)
- **21,900 registros** históricos (3 anos)
- **Retorno médio**: -1.97%
- **Volatilidade média**: 0.687%

### Top 5 Pares por Retorno
1. EUR/AUD - +36.70% (+6,135 pips)
2. GBP/AUD - +31.77% (+6,137 pips)
3. USD/JPY - +26.79% (+398,596 pips)
4. EUR/USD - +20.90% (+2,247 pips)
5. CAD/JPY - +17.14% (+190,010 pips)

### Uso
```bash
# Coletar dados
python forex_data_collector.py

# Analisar dados
python forex_data_analyzer.py
```

## 📈 Resumo Total de Dados

| Tipo | Ativos | Registros | Período | Retorno Médio |
|------|--------|-----------|---------|---------------|
| **Criptomoedas** | 20 | 19,602 | 3 anos | +201.31% |
| **Forex** | 20 | 21,900 | 3 anos | -1.97% |
| **TOTAL** | 40 | 41,502 | 3 anos | +99.67% |

## Cor de Identificação
🔴 **Vermelho** - Representa a entrada vital de dados no sistema

## Fluxo de Dados
```
Mercado → APIs → Coleta → Validação → Armazenamento → Próxima Camada
```

## Status
✅ Estrutura completa e operacional
✅ Sistema de dados de criptomoedas implementado
✅ Sistema de dados de forex implementado
✅ 41,502 registros históricos coletados
✅ 40 ativos disponíveis para análise