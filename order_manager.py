#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Order Manager - Gerencia ordens abertas e fechadas"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Order:
    """Ordem de trading"""
    order_id: str
    symbol: str
    action: str
    quantity: float
    price: float
    status: str
    created_at: datetime = field(default_factory=datetime.now)
    closed_at: datetime = None

class OrderManager:
    """Gerencia ordens abertas e histórico"""
    
    def __init__(self):
        self.open_orders: List[Order] = []
        self.closed_orders: List[Order] = []
    
    def create_order(self, symbol: str, action: str, quantity: float, price: float) -> Order:
        """Cria nova ordem"""
        order = Order(
            order_id=f"ORD_{datetime.now().timestamp()}",
            symbol=symbol,
            action=action,
            quantity=quantity,
            price=price,
            status="OPEN"
        )
        self.open_orders.append(order)
        return order
    
    def close_order(self, order_id: str) -> bool:
        """Fecha uma ordem"""
        for order in self.open_orders:
            if order.order_id == order_id:
                order.status = "CLOSED"
                order.closed_at = datetime.now()
                self.closed_orders.append(order)
                self.open_orders.remove(order)
                return True
        return False
    
    def get_open_orders(self) -> List[Order]:
        """Retorna ordens abertas"""
        return self.open_orders

if __name__ == "__main__":
    manager = OrderManager()
    print("OrderManager initialized")
