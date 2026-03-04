/**
 * Exchange Command Terminal
 */
export class CommandTerminal {
    execute(order) {
        console.log(`⚡ CMD_NEXUS: Executando ordem ${order.side} ${order.amount} ${order.symbol}`);
    }
}