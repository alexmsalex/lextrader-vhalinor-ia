#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AUTOMACAO AVANCADA COM PYAUTOGUI
====================================

Módulo para automação avançada de testes de APIs usando pyautogui
Realiza: testes completos, preenchimento de formulários, capturas de tela

Uso:
    from api_automation import APIAutomationBot, AutomationScheduler
    
    bot = APIAutomationBot()
    bot.run_full_test("binance")
"""

import pyautogui
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
import schedule
import threading

logger = logging.getLogger(__name__)

# Configurar pyautogui para segurança
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


@dataclass
class AutomationConfig:
    """Configuração de automação"""
    failsafe_enabled: bool = True
    pause_between_actions: float = 0.1
    screenshot_enabled: bool = True
    log_enabled: bool = True
    max_retries: int = 3
    timeout_seconds: int = 30


@dataclass
class AutomationStep:
    """Um passo de automação"""
    name: str
    action: str  # "type", "click", "screenshot", "wait", "hotkey"
    args: Dict[str, Any] = field(default_factory=dict)
    expected_result: Optional[str] = None


class APIAutomationBot:
    """Bot de automação para testes de APIs"""
    
    def __init__(self, config: AutomationConfig = None):
        self.config = config or AutomationConfig()
        self.log_dir = Path("logs/automation")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.execution_history: List[Dict] = []
        self.current_session = self._create_session()
    
    def _create_session(self) -> Dict:
        """Cria uma nova sessão de automação"""
        return {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now(),
            "steps_executed": 0,
            "steps_failed": 0,
            "steps_passed": 0,
            "screenshots": []
        }
    
    def execute_step(self, step: AutomationStep) -> bool:
        """Executa um passo de automação"""
        
        logger.info(f"Executando: {step.name}")
        
        try:
            if step.action == "type":
                text = step.args.get("text", "")
                interval = step.args.get("interval", 0.05)
                pyautogui.typewrite(text, interval=interval)
            
            elif step.action == "click":
                x = step.args.get("x", pyautogui.size()[0] // 2)
                y = step.args.get("y", pyautogui.size()[1] // 2)
                clicks = step.args.get("clicks", 1)
                pyautogui.click(x, y, clicks=clicks)
            
            elif step.action == "hotkey":
                keys = step.args.get("keys", [])
                pyautogui.hotkey(*keys)
            
            elif step.action == "screenshot":
                filepath = step.args.get("filepath", f"{self.log_dir}/auto_{int(time.time())}.png")
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                self.current_session["screenshots"].append(filepath)
                logger.info(f"Screenshot salvo: {filepath}")
            
            elif step.action == "wait":
                wait_time = step.args.get("seconds", 1)
                time.sleep(wait_time)
            
            elif step.action == "movemouse":
                x = step.args.get("x", 0)
                y = step.args.get("y", 0)
                duration = step.args.get("duration", 0.5)
                pyautogui.moveTo(x, y, duration=duration)
            
            self.current_session["steps_passed"] += 1
            return True
        
        except Exception as e:
            logger.error(f"Erro ao executar {step.name}: {e}")
            self.current_session["steps_failed"] += 1
            return False
        
        finally:
            self.current_session["steps_executed"] += 1
    
    def run_automation_sequence(self, steps: List[AutomationStep]) -> Dict:
        """Executa uma sequência de automação"""
        
        results = {
            "session_id": self.current_session["session_id"],
            "total_steps": len(steps),
            "passed": 0,
            "failed": 0,
            "steps_details": []
        }
        
        for step in steps:
            success = self.execute_step(step)
            results["steps_details"].append({
                "step": step.name,
                "success": success,
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        self.execution_history.append(results)
        return results
    
    def run_full_test(self, api_name: str) -> Dict:
        """Executa teste completo de uma API"""
        
        logger.info(f"Iniciando teste completo para {api_name}")
        
        # Definir sequência de passos para o teste
        steps = [
            AutomationStep(
                name="Movimentar mouse",
                action="movemouse",
                args={"x": 100, "y": 100, "duration": 0.5}
            ),
            AutomationStep(
                name="Aguardar 1 segundo",
                action="wait",
                args={"seconds": 1}
            ),
            AutomationStep(
                name="Capturar screenshot inicial",
                action="screenshot",
                args={"filepath": f"{self.log_dir}/{api_name}_start.png"}
            ),
            AutomationStep(
                name="Simular entrada de comando",
                action="type",
                args={"text": f"test_api {api_name}", "interval": 0.05}
            ),
            AutomationStep(
                name="Executar (Enter)",
                action="hotkey",
                args={"keys": ["return"]}
            ),
            AutomationStep(
                name="Aguardar resultado",
                action="wait",
                args={"seconds": 2}
            ),
            AutomationStep(
                name="Capturar screenshot final",
                action="screenshot",
                args={"filepath": f"{self.log_dir}/{api_name}_end.png"}
            )
        ]
        
        return self.run_automation_sequence(steps)
    
    def run_health_check_sequence(self) -> Dict:
        """Executa health check em múltiplas APIs"""
        
        logger.info("Iniciando health check automatizado")
        
        steps = [
            AutomationStep(
                name="Inicializar health check",
                action="movemouse",
                args={"x": 50, "y": 50, "duration": 0.3}
            ),
            AutomationStep(
                name="Aguardar",
                action="wait",
                args={"seconds": 1}
            ),
            AutomationStep(
                name="Executar script de health check",
                action="hotkey",
                args={"keys": ["ctrl", "shift", "h"]}
            ),
            AutomationStep(
                name="Capturar resultado",
                action="screenshot",
                args={"filepath": f"{self.log_dir}/health_check_{int(time.time())}.png"}
            )
        ]
        
        return self.run_automation_sequence(steps)
    
    def get_session_report(self) -> Dict:
        """Gera relatório da sessão"""
        
        end_time = datetime.now()
        duration = (end_time - self.current_session["start_time"]).total_seconds()
        
        return {
            "session_id": self.current_session["session_id"],
            "duration_seconds": duration,
            "steps_executed": self.current_session["steps_executed"],
            "steps_passed": self.current_session["steps_passed"],
            "steps_failed": self.current_session["steps_failed"],
            "success_rate": (self.current_session["steps_passed"] / 
                           max(self.current_session["steps_executed"], 1)) * 100,
            "screenshots_captured": len(self.current_session["screenshots"]),
            "screenshots": self.current_session["screenshots"]
        }
    
    def save_report(self, filepath: Optional[str] = None) -> str:
        """Salva relatório em arquivo"""
        
        if filepath is None:
            filepath = self.log_dir / f"report_{self.current_session['session_id']}.json"
        
        report = self.get_session_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Relatório salvo: {filepath}")
        return str(filepath)


class AutomationScheduler:
    """Agenda testes de automação"""
    
    def __init__(self):
        self.bot = APIAutomationBot()
        self.jobs: List[Dict] = []
    
    def schedule_api_test(self, api_name: str, interval_hours: int = 1):
        """Agenda teste periódico de uma API"""
        
        def job():
            logger.info(f"Executando teste agendado para {api_name}")
            result = self.bot.run_full_test(api_name)
            logger.info(f"Resultado: {result}")
        
        schedule.every(interval_hours).hours.do(job)
        
        self.jobs.append({
            "api": api_name,
            "interval_hours": interval_hours,
            "next_run": schedule.next_run()
        })
        
        logger.info(f"Teste agendado para {api_name} a cada {interval_hours} hora(s)")
    
    def schedule_health_check(self, interval_minutes: int = 30):
        """Agenda health check periódico"""
        
        def job():
            logger.info("Executando health check agendado")
            result = self.bot.run_health_check_sequence()
            logger.info(f"Resultado: {result}")
        
        schedule.every(interval_minutes).minutes.do(job)
        
        self.jobs.append({
            "type": "health_check",
            "interval_minutes": interval_minutes,
            "next_run": schedule.next_run()
        })
        
        logger.info(f"Health check agendado a cada {interval_minutes} minuto(s)")
    
    def run_scheduler(self):
        """Inicia o scheduler em thread separada"""
        
        def scheduler_loop():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        thread = threading.Thread(target=scheduler_loop, daemon=True)
        thread.start()
        
        logger.info("Scheduler iniciado em background")
    
    def get_scheduled_jobs(self) -> List[Dict]:
        """Retorna lista de jobs agendados"""
        return self.jobs


if __name__ == "__main__":
    # Exemplo de uso
    logging.basicConfig(level=logging.INFO)
    
    bot = APIAutomationBot()
    
    # Executar teste completo
    result = bot.run_full_test("binance")
    print("Resultado do teste:", json.dumps(result, indent=2, default=str))
    
    # Salvar relatório
    report_path = bot.save_report()
    print(f"Relatório salvo em: {report_path}")
    
    # Exibir relatório
    report = bot.get_session_report()
    print("Relatório da sessão:")
    print(json.dumps(report, indent=2, default=str))