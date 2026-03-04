# Entrada
ativos = ["BTC", "ETH", "AAPL", "GOOGL"]
retornos = dados_historicos

# Processamento
portfolio = qfa.quantum_portfolio_optimization(ativos, retornos)

# Saída
print(f"Alocações: {portfolio['weights']}")
print(f"Sharpe Ratio: {portfolio['sharpe_ratio']}")