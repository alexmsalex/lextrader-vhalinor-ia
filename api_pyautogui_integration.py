#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 INTEGRAÇÃO PYAUTOGUI - LAYER 1 (SENSORIAL)
==============================================

Integração de pyautogui para automação de testes de APIs
Parte da camada sensorial do LEXTRADER-IAG 4.0

Responsabilidades:
- Capturar entrada de dados automaticamente
- Simular interações com a interface
- Realizar screenshots de status
- Validar estados da interface

Uso:
    from neural_layers.sensorial_01.api_pyautogui_integration import APIAutomationSensor
    
    sensor = APIAutomationSensor()
    sensor.capture_api_state("binance")
"""

import pyautogui
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import json

logger = logging.getLogger(__name__)

# Configurar pyautogui para segurança
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


@dataclass
class APIScreenCapture:
    """Captura de tela de um estado de API"""
    api_name: str
    timestamp: str
    filepath: str
    success: bool
    resolution: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    file_size: int = 0


@dataclass
class MouseEvent:
    """Evento de movimento de mouse"""
    x: int
    y: int
    timestamp: str
    action: str  # "move", "click", "drag"
    duration: float = 0.0


class APIAutomationSensor:
    """Sensor de automação para APIs (Layer 1 - Sensorial)"""
    
    def __init__(self, log_dir: str = "logs/automation/sensorial"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.captures: List[APIScreenCapture] = []
        self.mouse_events: List[MouseEvent] = []
        self.screen_size = pyautogui.size()
        
        logger.info(f"APIAutomationSensor inicializado")
        logger.info(f"Resolução da tela: {self.screen_size}")
    
    def capture_current_state(self, api_name: str, label: str = "") -> APIScreenCapture:
        """Captura estado atual da tela para uma API"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{api_name}_{label}_{timestamp}.png" if label else f"{api_name}_{timestamp}.png"
            filepath = self.log_dir / filename
            
            # Capturar screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            
            capture = APIScreenCapture(
                api_name=api_name,
                timestamp=datetime.now().isoformat(),
                filepath=str(filepath),
                success=True,
                resolution=self.screen_size,
                file_size=filepath.stat().st_size if filepath.exists() else 0
            )
            
            self.captures.append(capture)
            logger.info(f"Screenshot capturado: {filepath}")
            
            return capture
        
        except Exception as e:
            logger.error(f"Erro ao capturar screenshot: {e}")
            return APIScreenCapture(
                api_name=api_name,
                timestamp=datetime.now().isoformat(),
                filepath="",
                success=False,
                resolution=self.screen_size
            )
    
    def move_mouse_to_api_button(self, api_name: str, x_offset: int = 0, y_offset: int = 0) -> bool:
        """Move mouse para botão de API na interface"""
        
        try:
            # Calcular posição baseada no nome da API
            api_positions = {
                "binance": (100, 100),
                "ctrader": (200, 100),
                "pionex": (300, 100),
                "coinbase": (400, 100),
                "alpaca": (500, 100),
                "alphavantage": (100, 200),
                "polygon": (200, 200),
                "twelvedata": (300, 200)
            }
            
            base_x, base_y = api_positions.get(api_name.lower(), (50, 50))
            x = base_x + x_offset
            y = base_y + y_offset
            
            # Mover mouse
            pyautogui.moveTo(x, y, duration=0.5)
            
            # Registrar evento
            event = MouseEvent(
                x=x,
                y=y,
                timestamp=datetime.now().isoformat(),
                action="move",
                duration=0.5
            )
            self.mouse_events.append(event)
            
            logger.info(f"Mouse movido para {api_name} ({x}, {y})")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao mover mouse: {e}")
            return False
    
    def click_api_button(self, api_name: str, clicks: int = 1) -> bool:
        """Clica no botão de uma API"""
        
        try:
            # Primeiro mover para a API
            if not self.move_mouse_to_api_button(api_name):
                return False
            
            # Aguardar um pouco antes de clicar
            time.sleep(0.3)
            
            # Clicar
            pyautogui.click(clicks=clicks)
            
            # Registrar evento
            event = MouseEvent(
                x=pyautogui.position()[0],
                y=pyautogui.position()[1],
                timestamp=datetime.now().isoformat(),
                action="click",
                duration=0.0
            )
            self.mouse_events.append(event)
            
            logger.info(f"Clique em {api_name} ({clicks}x)")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao clicar: {e}")
            return False
    
    def simulate_api_interaction(self, api_name: str, action: str = "test") -> Dict[str, Any]:
        """Simula interação com API"""
        
        logger.info(f"Simulando {action} em {api_name}")
        
        results = {
            "api": api_name,
            "action": action,
            "steps": [],
            "success": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Passo 1: Capturar estado inicial
            capture_initial = self.capture_current_state(api_name, f"{action}_initial")
            results["steps"].append({
                "name": "Capturar estado inicial",
                "success": capture_initial.success,
                "file": capture_initial.filepath
            })
            
            # Passo 2: Mover mouse para API
            move_success = self.move_mouse_to_api_button(api_name)
            results["steps"].append({
                "name": "Mover mouse para API",
                "success": move_success
            })
            
            # Passo 3: Clicar em botão de teste
            click_success = self.click_api_button(api_name)
            results["steps"].append({
                "name": "Clicar em botão",
                "success": click_success
            })
            
            # Passo 4: Aguardar resultado
            time.sleep(1)
            
            # Passo 5: Capturar estado final
            capture_final = self.capture_current_state(api_name, f"{action}_final")
            results["steps"].append({
                "name": "Capturar estado final",
                "success": capture_final.success,
                "file": capture_final.filepath
            })
            
            # Determinar sucesso geral
            results["success"] = all(step.get("success", True) for step in results["steps"])
            
        except Exception as e:
            logger.error(f"Erro na simulação: {e}")
            results["error"] = str(e)
        
        return results
    
    def simulate_credential_entry(self, api_name: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Simula entrada de credenciais"""
        
        logger.info(f"Simulando entrada de credenciais para {api_name}")
        
        results = {
            "api": api_name,
            "fields_filled": 0,
            "success": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Capturar estado inicial
            self.capture_current_state(api_name, "credentials_initial")
            
            # Preencher cada credencial
            for field_name, field_value in credentials.items():
                logger.info(f"Preenchendo {field_name}")
                
                # Type field name (simular digitação)
                pyautogui.typewrite(field_value, interval=0.05)
                time.sleep(0.3)
                
                # Tab para próximo campo
                pyautogui.press("tab")
                time.sleep(0.2)
                
                results["fields_filled"] += 1
            
            # Capturar estado final
            self.capture_current_state(api_name, "credentials_final")
            
            results["success"] = True
        
        except Exception as e:
            logger.error(f"Erro ao preencher credenciais: {e}")
            results["error"] = str(e)
        
        return results
    
    def verify_api_status_visually(self, api_name: str) -> Dict[str, Any]:
        """Verifica status da API visualmente (screenshot + análise)"""
        
        logger.info(f"Verificando status visual de {api_name}")
        
        capture = self.capture_current_state(api_name, "status_check")
        
        return {
            "api": api_name,
            "capture_success": capture.success,
            "filepath": capture.filepath,
            "timestamp": capture.timestamp,
            "resolution": capture.resolution,
            "file_size": capture.file_size
        }
    
    def get_capture_history(self, api_name: Optional[str] = None) -> List[APIScreenCapture]:
        """Retorna histórico de capturas"""
        
        if api_name:
            return [c for c in self.captures if c.api_name == api_name]
        return self.captures
    
    def get_mouse_event_history(self) -> List[MouseEvent]:
        """Retorna histórico de eventos de mouse"""
        return self.mouse_events
    
    def export_session_data(self, filepath: Optional[str] = None) -> str:
        """Exporta dados da sessão para arquivo"""
        
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.log_dir / f"session_{timestamp}.json"
        
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "screen_resolution": self.screen_size,
            "captures_count": len(self.captures),
            "mouse_events_count": len(self.mouse_events),
            "captures": [
                {
                    "api_name": c.api_name,
                    "timestamp": c.timestamp,
                    "filepath": c.filepath,
                    "success": c.success,
                    "file_size": c.file_size
                }
                for c in self.captures
            ],
            "mouse_events": [
                {
                    "x": e.x,
                    "y": e.y,
                    "timestamp": e.timestamp,
                    "action": e.action,
                    "duration": e.duration
                }
                for e in self.mouse_events
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        logger.info(f"Dados da sessão exportados: {filepath}")
        return str(filepath)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    sensor = APIAutomationSensor()
    
    # Testar captura de estado
    capture = sensor.capture_current_state("binance", "test")
    print(f"Captura: {capture}")
    
    # Testar simulação de interação
    result = sensor.simulate_api_interaction("binance", "health_check")
    print(f"Resultado: {json.dumps(result, indent=2, default=str)}")
    
    # Exportar dados
    export_path = sensor.export_session_data()
    print(f"Dados exportados: {export_path}")
