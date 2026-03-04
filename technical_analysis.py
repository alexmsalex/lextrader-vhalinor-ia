#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An�lise T�cnica - C�lculo de indicadores"""

import numpy as np
from typing import List, Dict, Any

class TechnicalAnalyzer:
    """Calcula indicadores t�cnicos (SMA, EMA, RSI, MACD, etc)"""
    
    @staticmethod
    def sma(prices: List[float], period: int = 20) -> float:
        """Simple Moving Average"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        return sum(prices[-period:]) / period
    
    @staticmethod
    def ema(prices: List[float], period: int = 20) -> float:
        """Exponential Moving Average"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        for price in prices[period:]:
            ema = price * multiplier + ema * (1 - multiplier)
        return ema
    
    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> float:
        """Relative Strength Index"""
        if len(prices) < period:
            return 50.0
        gains = [max(prices[i] - prices[i-1], 0) for i in range(1, len(prices))]
        losses = [max(prices[i-1] - prices[i], 0) for i in range(1, len(prices))]
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def macd(prices: List[float]) -> Dict[str, float]:
        """MACD Indicator"""
        ema12 = TechnicalAnalyzer.ema(prices, 12)
        ema26 = TechnicalAnalyzer.ema(prices, 26)
        macd_line = ema12 - ema26
        signal = (ema12 + ema26) / 2
        histogram = macd_line - signal
        return {"macd": macd_line, "signal": signal, "histogram": histogram}

if __name__ == "__main__":
    analyzer = TechnicalAnalyzer()
    print("TechnicalAnalyzer initialized")
