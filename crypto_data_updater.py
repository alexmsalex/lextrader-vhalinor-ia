"""
Atualizador Automático de Dados de Criptomoedas
================================================
Atualiza os dados históricos e em tempo real periodicamente
"""

import json
import logging
import os
import time
from datetime import datetime

from crypto_data_collector import CryptoDataCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CryptoDataUpdater:
    """Atualizador automático de dados"""

    def __init__(self, update_interval: int = 3600):
        """
        Args:
            update_interval: Intervalo de atualização em segundos (padrão: 1 hora)
        """
        self.collector = CryptoDataCollector()
        self.update_interval = update_interval
        self.data_path = 'neural_layers/01_sensorial/crypto_data'
        self.log_file = f"{self.data_path}/update_log.json"

    def update_realtime_only(self):
        """Atualiza apenas dados em tempo real (mais rápido)"""
        logger.info("🔄 Atualizando dados em tempo real...")

        try:
            realtime = self.collector.collect_all_realtime()

            # Log da atualização
            self._log_update('realtime', len(realtime))

            return realtime

        except Exception as e:
            logger.error(f"❌ Erro na atualização: {e}")
            return {}

    def update_historical_incremental(self):
        """Atualiza dados históricos incrementalmente (apenas novos dados)"""
        logger.info("📊 Atualizando dados históricos incrementalmente...")

        try:
            # Coletar apenas os últimos 7 dias
            historical = self.collector.collect_all_historical(timeframe='1d')

            # Log da atualização
            self._log_update('historical', len(historical))

            return historical

        except Exception as e:
            logger.error(f"❌ Erro na atualização histórica: {e}")
            return {}

    def _log_update(self, update_type: str, count: int):
        """Registra atualização no log"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': update_type,
            'cryptos_updated': count,
            'status': 'success' if count > 0 else 'failed'
        }

        # Carregar log existente
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)

        # Adicionar nova entrada
        logs.append(log_entry)

        # Manter apenas últimas 100 entradas
        logs = logs[-100:]

        # Salvar log
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)

        logger.info(f"✅ Log atualizado: {update_type} - {count} criptos")

    def run_continuous(self):
        """Executa atualizações contínuas"""
        logger.info("="*70)
        logger.info("🚀 INICIANDO ATUALIZADOR AUTOMÁTICO")
        logger.info("="*70)
        logger.info(f"Intervalo de atualização: {self.update_interval}s")
        logger.info(f"Próxima atualização em: {self.update_interval/60:.1f} minutos")
        logger.info("="*70)

        iteration = 0

        try:
            while True:
                iteration += 1
                logger.info(f"\n{'='*70}")
                logger.info(f"🔄 ATUALIZAÇÃO #{iteration}")
                logger.info(f"{'='*70}")

                # Atualizar dados em tempo real
                self.update_realtime_only()

                # A cada 24 iterações (24 horas se intervalo = 1h), atualizar histórico
                if iteration % 24 == 0:
                    self.update_historical_incremental()

                # Aguardar próxima atualização
                logger.info(f"\n⏰ Próxima atualização em {self.update_interval/60:.1f} minutos...")
                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            logger.info("\n\n⚠️  Atualizador interrompido pelo usuário")
            logger.info("="*70)

    def run_once(self):
        """Executa uma única atualização"""
        logger.info("="*70)
        logger.info("🔄 EXECUTANDO ATUALIZAÇÃO ÚNICA")
        logger.info("="*70)

        # Atualizar dados em tempo real
        realtime = self.update_realtime_only()

        logger.info("\n" + "="*70)
        logger.info("✅ ATUALIZAÇÃO CONCLUÍDA")
        logger.info("="*70)
        logger.info(f"Dados em tempo real: {len(realtime)} criptomoedas")
        logger.info("="*70)

def main():
    """Função principal"""
    import sys

    updater = CryptoDataUpdater(update_interval=3600)  # 1 hora

    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        # Modo contínuo
        updater.run_continuous()
    else:
        # Modo único
        updater.run_once()

if __name__ == "__main__":
    main()
