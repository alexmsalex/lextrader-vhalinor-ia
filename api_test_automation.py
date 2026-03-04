#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTES AUTOMATIZADOS COM PYAUTOGUI
====================================

Suite completa de testes para APIs com automação visual
Integra pyautogui para validação de interface

Uso:
    python api_test_automation.py
    pytest api_test_automation.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyautogui
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
import json

# Importar sensor de automação
try:
    from neural_layers.sensorial_01.api_pyautogui_integration import APIAutomationSensor
except ImportError:
    from api_pyautogui_integration import APIAutomationSensor

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Resultado de um teste"""
    test_name: str
    api_name: str
    success: bool
    duration: float
    error: str = ""
    details: Dict[str, Any] = None


class APITestAutomation:
    """Suite de testes automatizados para APIs"""
    
    def __init__(self):
        self.sensor = APIAutomationSensor()
        self.test_results: List[TestResult] = []
        self.apis = [
            "binance",
            "ctrader",
            "pionex",
            "coinbase",
            "alpaca",
            "alphavantage",
            "polygon",
            "twelvedata"
        ]
    
    def test_api_connection(self, api_name: str) -> TestResult:
        """Testa conexão com uma API"""
        
        start_time = time.time()
        
        try:
            logger.info(f"Testando conexão com {api_name}")
            
            # Simular teste
            result = self.sensor.simulate_api_interaction(api_name, "connection_test")
            
            success = result.get("success", False)
            
            test_result = TestResult(
                test_name="api_connection",
                api_name=api_name,
                success=success,
                duration=time.time() - start_time,
                details=result
            )
        
        except Exception as e:
            test_result = TestResult(
                test_name="api_connection",
                api_name=api_name,
                success=False,
                duration=time.time() - start_time,
                error=str(e)
            )
        
        self.test_results.append(test_result)
        return test_result
    
    def test_api_health_check(self, api_name: str) -> TestResult:
        """Testa health check de uma API"""
        
        start_time = time.time()
        
        try:
            logger.info(f"Executando health check em {api_name}")
            
            result = self.sensor.simulate_api_interaction(api_name, "health_check")
            success = result.get("success", False)
            
            test_result = TestResult(
                test_name="health_check",
                api_name=api_name,
                success=success,
                duration=time.time() - start_time,
                details=result
            )
        
        except Exception as e:
            test_result = TestResult(
                test_name="health_check",
                api_name=api_name,
                success=False,
                duration=time.time() - start_time,
                error=str(e)
            )
        
        self.test_results.append(test_result)
        return test_result
    
    def test_api_screenshot(self, api_name: str) -> TestResult:
        """Testa captura de screenshot para uma API"""
        
        start_time = time.time()
        
        try:
            logger.info(f"Capturando screenshot de {api_name}")
            
            # Mover mouse para API
            self.sensor.move_mouse_to_api_button(api_name)
            
            # Capturar screenshot
            capture = self.sensor.verify_api_status_visually(api_name)
            
            success = capture.get("capture_success", False)
            
            test_result = TestResult(
                test_name="screenshot",
                api_name=api_name,
                success=success,
                duration=time.time() - start_time,
                details=capture
            )
        
        except Exception as e:
            test_result = TestResult(
                test_name="screenshot",
                api_name=api_name,
                success=False,
                duration=time.time() - start_time,
                error=str(e)
            )
        
        self.test_results.append(test_result)
        return test_result
    
    def test_mouse_automation(self) -> TestResult:
        """Testa automação de mouse"""
        
        start_time = time.time()
        
        try:
            logger.info("Testando automação de mouse")
            
            # Salvar posição inicial
            initial_pos = pyautogui.position()
            
            # Mover para centro da tela
            center_x, center_y = pyautogui.size()
            center_x //= 2
            center_y //= 2
            
            pyautogui.moveTo(center_x, center_y, duration=1.0)
            
            # Verificar posição
            current_pos = pyautogui.position()
            success = (abs(current_pos[0] - center_x) < 10 and 
                      abs(current_pos[1] - center_y) < 10)
            
            # Retornar à posição inicial
            pyautogui.moveTo(initial_pos[0], initial_pos[1], duration=0.5)
            
            test_result = TestResult(
                test_name="mouse_automation",
                api_name="system",
                success=success,
                duration=time.time() - start_time,
                details={
                    "initial_pos": initial_pos,
                    "target_pos": (center_x, center_y),
                    "final_pos": current_pos
                }
            )
        
        except Exception as e:
            test_result = TestResult(
                test_name="mouse_automation",
                api_name="system",
                success=False,
                duration=time.time() - start_time,
                error=str(e)
            )
        
        self.test_results.append(test_result)
        return test_result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Executa todos os testes"""
        
        logger.info("Iniciando suite completa de testes")
        
        # Testar mouse automation
        logger.info("=== TESTE 1: Automação de Mouse ===")
        self.test_mouse_automation()
        
        # Testar cada API
        for api_name in self.apis:
            logger.info(f"\n=== TESTES PARA {api_name.upper()} ===")
            
            # Teste de conexão
            logger.info(f"Teste 1: Conexão")
            self.test_api_connection(api_name)
            time.sleep(0.5)
            
            # Teste de health check
            logger.info(f"Teste 2: Health Check")
            self.test_api_health_check(api_name)
            time.sleep(0.5)
            
            # Teste de screenshot
            logger.info(f"Teste 3: Screenshot")
            self.test_api_screenshot(api_name)
            time.sleep(0.5)
        
        return self.get_results_summary()
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Retorna resumo dos testes"""
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.success)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        total_duration = sum(r.duration for r in self.test_results)
        
        # Agrupar por API
        results_by_api = {}
        for result in self.test_results:
            if result.api_name not in results_by_api:
                results_by_api[result.api_name] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "tests": []
                }
            
            api_results = results_by_api[result.api_name]
            api_results["total"] += 1
            if result.success:
                api_results["passed"] += 1
            else:
                api_results["failed"] += 1
            
            api_results["tests"].append({
                "name": result.test_name,
                "success": result.success,
                "duration": result.duration,
                "error": result.error
            })
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "total_duration": f"{total_duration:.2f}s"
            },
            "by_api": results_by_api,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_results(self, filepath: str = "logs/test_results.json"):
        """Salva resultados em arquivo"""
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        summary = self.get_results_summary()
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Resultados salvos em: {filepath}")
        return filepath
    
    def print_results(self):
        """Imprime resultados formatados"""
        
        summary = self.get_results_summary()
        
        print("\n" + "="*60)
        print("📊 RESUMO DOS TESTES")
        print("="*60)
        
        print(f"\nTotal de testes: {summary['summary']['total_tests']}")
        print(f"✅ Passed: {summary['summary']['passed']}")
        print(f"❌ Failed: {summary['summary']['failed']}")
        print(f"📈 Taxa de sucesso: {summary['summary']['success_rate']}")
        print(f"⏱️  Tempo total: {summary['summary']['total_duration']}")
        
        print("\n" + "="*60)
        print("RESULTADOS POR API")
        print("="*60)
        
        for api_name, api_results in summary['by_api'].items():
            print(f"\n🔌 {api_name.upper()}")
            print(f"   Total: {api_results['total']} | ✅ {api_results['passed']} | ❌ {api_results['failed']}")
            
            for test in api_results['tests']:
                status = "✅" if test['success'] else "❌"
                print(f"   {status} {test['name']}: {test['duration']:.2f}s")
                if test['error']:
                    print(f"      Erro: {test['error']}")


def main():
    """Função principal"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n🤖 INICIANDO SUITE DE TESTES COM PYAUTOGUI")
    print("=" * 60)
    print(f"Timestamp: {datetime.now()}")
    print(f"Resolução da tela: {pyautogui.size()}")
    print("=" * 60 + "\n")
    
    # Criar suite de testes
    test_suite = APITestAutomation()
    
    # Executar todos os testes
    test_suite.run_all_tests()
    
    # Imprimir resultados
    test_suite.print_results()
    
    # Salvar resultados
    test_suite.save_results()
    
    # Salvar dados da sessão do sensor
    sensor_export = test_suite.sensor.export_session_data()
    print(f"\n📁 Dados da sessão salvos em: {sensor_export}")


if __name__ == "__main__":
    main()
