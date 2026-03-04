# Monitorar mudanças de regime
alerta = qfa.detect_regime_change(dados_mercado)
if alerta:
    print("ALERTA: Mudança de regime detectada!")
    # Ajustar estratégias automaticamente