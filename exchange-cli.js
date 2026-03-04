
/**
 * LEXTRADER-IAG 4.0 - CLI Interface
 */
import chalk from 'chalk';

export class ExchangeCLI {
  constructor() {
    console.log(chalk.cyan('🚀 LEXTRADER CLI V4.0 - Núcleo AGI Ativo'));
  }

  showStatus(state) {
    console.log(chalk.gray(`Estado AGI: ${state.status} | Estabilidade: ${state.stability}%`));
  }

  logTrade(trade) {
    console.log(chalk.green(`[TRADE] ${trade.symbol} ${trade.side} @ ${trade.price}`));
  }
}
