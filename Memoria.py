# Importar o sistema
from memory_architecture import UnifiedMemorySystem

# Criar instância
memory_system = UnifiedMemorySystem(storage_path="./memory_data")

# Processar dados de mercado
report = memory_system.process_input(market_data, volatility)

# Cometer experiência
memory_system.commit_experience(
    context="Trade de exemplo",
    actions=["analisar", "executar", "monitorar"],
    outcome=100.50,
    emotion=SentientState.CALM,
    engram=memory_engram
)

# Consultar memórias
memories = memory_system.long_term.retrieve_quantum([50, 0, 1.2, 0])