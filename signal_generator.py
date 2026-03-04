#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerador de Sinais - Gera sinais de compra/venda"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TradingSignal:
    """Sinal de trading gerado"""
    symbol: str
    action: str  # "BUY", "SELL", "HOLD"
    confidence: float
    price: float
    timestamp: datetime
    reason: str

class SignalGenerator:
    """Gera sinais de trading baseado em an�lise t�cnica"""
    
    def generate_signal(self, symbol: str, indicators: Dict[str, float]) -> TradingSignal:
        """Gera sinal baseado em indicadores"""
        
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", 0)
        price = indicators.get("price", 100)
        
        # L�gica simples
        if rsi < 30 and macd > 0:
            action = "BUY"
            confidence = 0.7
            reason = "RSI oversold + MACD positive"
        elif rsi > 70 and macd < 0:
            action = "SELL"
            confidence = 0.7
            reason = "RSI overbought + MACD negative"
        else:
            action = "HOLD"
            confidence = 0.5
            reason = "No clear signal"
        
        return TradingSignal(
            symbol=symbol,
            action=action,
            confidence=confidence,
            price=price,
            timestamp=datetime.now(),
            reason=reason
        )

if __name__ == "__main__":
    generator = SignalGenerator()
    print("SignalGenerator initialized")
