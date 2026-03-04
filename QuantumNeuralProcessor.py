from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import threading
import time
import math
import random
import html

# Registrar no NeuralBus
try:
    from neural_bus import NeuralBus
except ImportError:
    NeuralBus = None

def _escape(s: Optional[str]) -> str:
    return html.escape(s or "")

QUANTUM_CONSTANTS = {
    "MAX_QUBITS": 128,
    "ANIMATION_FPS": 60,
    "SIMULATION_INTERVAL": 0.2,
    "CANVAS_WIDTH": 600,
    "CANVAS_HEIGHT": 400,
    "MIN_COHERENCE": 0.5,
    "MAX_COHERENCE": 1.0,
    "MIN_TEMPERATURE": 0.001,
    "MAX_TEMPERATURE": 0.1
}

TRADING_CIRCUITS = [
    {"name": "Análise Quântica de Mercado", "description": "Processamento de dados de mercado com vantagem quântica", "qubits": 32, "focus": "market-analysis"},
    {"name": "Reconhecimento Quântico de Padrões", "description": "Detecção de padrões complexos em dados financeiros", "qubits": 32, "focus": "pattern-recognition"},
    {"name": "Otimização Quântica de Portfolio", "description": "Otimização de carteira usando algoritmos quânticos", "qubits": 32, "focus": "portfolio-optimization"},
    {"name": "Avaliação Quântica de Risco", "description": "Análise avançada de risco com computação quântica", "qubits": 32, "focus": "risk-assessment"},
]

LAYER_TYPE_COLORS = {
    "VARIATIONAL": "text-purple-400",
    "ADIABATIC": "text-blue-400",
    "QUANTUM_CNN": "text-green-400",
    "QUANTUM_RNN": "text-yellow-400",
    "QUANTUM_TRANSFORMER": "text-red-400",
}

@dataclass
class QuantumBit:
    id: str
    state: List[float]
    phase: float
    entangled: List[str]
    coherence_time: float
    fidelity: float
    position: Dict[str, float]
    last_measurement: float
    error_rate: float

@dataclass
class QuantumGate:
    id: str
    type: str
    qubits: List[str]
    matrix: List[List[float]]
    fidelity: float
    gate_time: float
    error_rate: float

@dataclass
class QuantumCircuit:
    id: str
    name: str
    qubits: List[QuantumBit]
    gates: List[QuantumGate]
    depth: int
    width: int
    entanglement_degree: float
    coherence_time: float
    total_fidelity: float

@dataclass
class NeuralQuantumLayer:
    id: str
    name: str
    type: str
    qubits: int
    parameters: int
    accuracy: float
    quantum_advantage: float
    classical_equivalent: int
    speedup: float
    noise_resilience: float

@dataclass
class QuantumMetrics:
    total_qubits: int = 0
    entanglement_entropy: float = 0.0
    quantum_volume: float = 0.0
    coherence_time: float = 0.0
    gate_operations: int = 0
    quantum_supremacy: float = 0.0
    error_correction_level: float = 0.0
    processing_power: float = 0.0

class QuantumNeuralProcessor:
    def __init__(self):
        self.qubits: List[QuantumBit] = []
        self.circuits: List[QuantumCircuit] = []
        self.quantum_layers: List[NeuralQuantumLayer] = []
        self.metrics = QuantumMetrics()

        self.is_active = True
        self.quantum_coherence = 0.95
        self.entanglement_strength = 0.8
        self.error_correction_level = 0.7
        self.temperature_kelvin = 0.015
        self.quantum_compute_mode = False

        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        self.initialize_quantum_system()
        self.start()
        
        # Registrar no NeuralBus para comunicação entre módulos
        if NeuralBus:
            try:
                NeuralBus.get_instance().register(
                    "quantum_neural_processor",
                    self,
                    {"type": "QuantumNeuralProcessor", "file": "QuantumNeuralProcessor.py"}
                )
            except Exception:
                pass

    # --- generators ---
    def generate_qubits(self, count: int) -> List[QuantumBit]:
        qb_list: List[QuantumBit] = []
        for i in range(count):
            phase = random.random() * 2 * math.pi
            amp0 = math.cos(phase / 2)
            amp1 = math.sin(phase / 2)
            qb = QuantumBit(
                id=f"qubit_{i}",
                state=[amp0, amp1],
                phase=phase,
                entangled=[],
                coherence_time=100 + random.random() * 50,
                fidelity=0.99 + random.random() * 0.009,
                position={"x": math.cos(i * 0.1) * (i * 2), "y": math.sin(i * 0.1) * (i * 2), "z": i * 0.5},
                last_measurement=0.0,
                error_rate=0.001 + random.random() * 0.002
            )
            qb_list.append(qb)
        # create entanglement pairs
        for i in range(len(qb_list)-1):
            if random.random() < self.entanglement_strength:
                partner = i + 1 + random.randint(0, min(4, max(0, len(qb_list)-i-2)))
                if partner < len(qb_list):
                    qb_list[i].entangled.append(qb_list[partner].id)
                    qb_list[partner].entangled.append(qb_list[i].id)
        return qb_list

    def generate_quantum_gates(self, qubits: List[QuantumBit]) -> List[QuantumGate]:
        gates: List[QuantumGate] = []
        gid = 0
        for q in qubits:
            if random.random() < 0.3:
                gates.append(QuantumGate(
                    id=f"gate_{gid}", type="HADAMARD", qubits=[q.id],
                    matrix=[[1/math.sqrt(2),1/math.sqrt(2)],[1/math.sqrt(2),-1/math.sqrt(2)]],
                    fidelity=0.995 + random.random()*0.004, gate_time=20+random.random()*10, error_rate=0.0001 + random.random()*0.0002
                ))
                gid += 1
        for i in range(len(qubits)-1):
            if random.random() < 0.4:
                gates.append(QuantumGate(
                    id=f"gate_{gid}", type="CNOT", qubits=[qubits[i].id, qubits[i+1].id],
                    matrix=[[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],
                    fidelity=0.98 + random.random()*0.015, gate_time=50+random.random()*20, error_rate=0.001 + random.random()*0.002
                ))
                gid += 1
        for q in qubits:
            if random.random() < 0.25:
                phase = random.random() * 2 * math.pi
                gates.append(QuantumGate(
                    id=f"gate_{gid}", type="PHASE", qubits=[q.id],
                    matrix=[[1,0],[0,math.cos(phase)]],
                    fidelity=0.997 + random.random()*0.002, gate_time=15+random.random()*5, error_rate=0.0005 + random.random()*0.0003
                ))
                gid += 1
        return gates

    def generate_circuits(self, qubits: List[QuantumBit]) -> List[QuantumCircuit]:
        circuits: List[QuantumCircuit] = []
        for idx, cfg in enumerate(TRADING_CIRCUITS):
            start = idx * cfg["qubits"]
            end = start + cfg["qubits"]
            subset = qubits[start:end]
            circuits.append(QuantumCircuit(
                id=f"{cfg['focus']}_circuit",
                name=cfg["name"],
                qubits=subset,
                gates=self.generate_quantum_gates(subset),
                depth=15 + random.randint(0,9),
                width=len(subset),
                entanglement_degree=0.6 + random.random()*0.2,
                coherence_time=80 + random.random()*20,
                total_fidelity=0.98 + random.random()*0.015
            ))
        return circuits

    def generate_quantum_layers(self) -> List[NeuralQuantumLayer]:
        configs = [
            ("VARIATIONAL","Análise Variacional de Mercado",32,256),
            ("QUANTUM_CNN","CNN Quântica - Padrões Financeiros",24,192),
            ("ADIABATIC","Otimizador Adiabático - Portfolio",16,128),
            ("QUANTUM_RNN","RNN Quântica - Séries Temporais",20,160),
            ("QUANTUM_TRANSFORMER","Transformer Quântico - Correlações",36,288),
        ]
        layers = []
        for i,c in enumerate(configs):
            layers.append(NeuralQuantumLayer(
                id=f"quantum_layer_{i}", name=c[1], type=c[0],
                qubits=c[2], parameters=c[3], accuracy=94+random.random()*5,
                quantum_advantage=10+random.random()*50, classical_equivalent=c[3]*8,
                speedup=10+random.random()*50, noise_resilience=75+random.random()*20
            ))
        return layers

    # --- initialization ---
    def initialize_quantum_system(self):
        with self._lock:
            new_qubits = self.generate_qubits(QUANTUM_CONSTANTS["MAX_QUBITS"])
            new_layers = self.generate_quantum_layers()
            new_circuits = self.generate_circuits(new_qubits)
            self.qubits = new_qubits
            self.quantum_layers = new_layers
            self.circuits = new_circuits

            total_entanglement = sum(len(q.entangled) for q in new_qubits) / 2 if new_qubits else 0
            avg_coh = sum(q.coherence_time for q in new_qubits)/len(new_qubits) if new_qubits else 0

            self.metrics = QuantumMetrics(
                total_qubits=len(new_qubits),
                entanglement_entropy=(total_entanglement / len(new_qubits) * math.log2(len(new_qubits))) if new_qubits else 0.0,
                quantum_volume=2 ** min(len(new_qubits), 20),
                coherence_time=avg_coh,
                gate_operations=sum(len(c.gates) for c in new_circuits),
                quantum_supremacy=sum(l.quantum_advantage for l in new_layers)/len(new_layers) if new_layers else 0.0,
                error_correction_level=self.error_correction_level * 100,
                processing_power=len(new_qubits) * self.quantum_coherence * 1000
            )

    # --- simulation ---
    def simulate_step(self):
        if not self.is_active:
            return
        with self._lock:
            now = time.time()
            # evolve qubits
            updated = []
            for q in self.qubits:
                decoherence = (1.0 / q.coherence_time) * (self.temperature_kelvin / 0.015)
                new_fidelity = max(0.1, q.fidelity * (1 - decoherence * 0.001))
                time_evo = math.sin(time.time() * 0.001 + q.phase) * 0.05
                new_amp0 = max(0.0, min(1.0, q.state[0] + time_evo * self.quantum_coherence))
                new_amp1 = math.sqrt(max(0.0, 1.0 - new_amp0 * new_amp0))
                q.state = [new_amp0, new_amp1]
                q.fidelity = new_fidelity
                q.phase = (q.phase + random.random() * 0.05) % (2 * math.pi)
                q.error_rate = max(0.0001, q.error_rate * (1 - self.error_correction_level * 0.3))
                updated.append(q)
            self.qubits = updated

            # update metrics
            self.metrics.entanglement_entropy = max(0.0, self.metrics.entanglement_entropy + (random.random()-0.5)*0.05)
            self.metrics.coherence_time *= 1 + (self.quantum_coherence - 0.5) * 0.005
            self.metrics.gate_operations += random.randint(0,50)
            self.metrics.processing_power = self.metrics.total_qubits * self.quantum_coherence * 1000 * (1 + math.sin(time.time()*0.001)*0.05)

            # optionally adjust layers in compute mode
            if self.quantum_compute_mode:
                for l in self.quantum_layers:
                    l.accuracy = min(99.9, max(90.0, l.accuracy + (random.random()-0.4)*0.05))
                    l.quantum_advantage = max(1.0, l.quantum_advantage + (random.random()-0.4)*1.0)
                    l.noise_resilience = min(100.0, max(70.0, l.noise_resilience + (random.random()-0.4)*0.2))

    def _loop(self):
        interval = QUANTUM_CONSTANTS["SIMULATION_INTERVAL"]
        while not self._stop.is_set():
            start = time.time()
            self.simulate_step()
            elapsed = time.time() - start
            to_wait = max(0.0, interval - elapsed)
            time.sleep(to_wait)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)

    def reset(self):
        with self._lock:
            self.initialize_quantum_system()

    # --- rendering server-side simplified ---
    def render_html(self) -> str:
        with self._lock:
            avg_fidelity = (sum(q.fidelity for q in self.qubits)/len(self.qubits))*100 if self.qubits else 0.0
            avg_error = (sum(q.error_rate for q in self.qubits)/len(self.qubits))*100 if self.qubits else 0.0
            entangled_count = sum(1 for q in self.qubits if q.entangled)
            parts = []
            parts.append('<div class="card w-full">')
            parts.append('<div class="card-header"><h3>⚛️ Processador Neural Quântico - LEXTRADER IAG</h3></div>')
            parts.append('<div class="card-content">')
            parts.append('<div class="grid grid-cols-2 md:grid-cols-4 gap-4">')
            parts.append(f'<div class="p-3 text-center"><div class="font-bold">{self.metrics.total_qubits}</div><div class="text-xs text-muted-foreground">Qubits</div></div>')
            parts.append(f'<div class="p-3 text-center"><div class="font-bold">{self.metrics.quantum_supremacy:.1f}x</div><div class="text-xs text-muted-foreground">Vantagem</div></div>')
            parts.append(f'<div class="p-3 text-center"><div class="font-bold">{self.metrics.processing_power/1000:.1f}K</div><div class="text-xs text-muted-foreground">QFLOPS</div></div>')
            parts.append(f'<div class="p-3 text-center"><div class="font-bold">{avg_fidelity:.1f}%</div><div class="text-xs text-muted-foreground">Fidelidade Média</div></div>')
            parts.append('</div>')
            parts.append(f'<p class="text-sm mt-4">Emaranhados: {entangled_count} • Erro médio: {avg_error:.4f}% • Coerência média: {self.metrics.coherence_time:.1f}μs</p>')
            parts.append('</div></div>')
            return "\n".join(parts)

# Exemplo rápido de uso
if __name__ == "__main__":
    qnp = QuantumNeuralProcessor()
    try:
        time.sleep(1)
        print(qnp.render_html()[:800])
    finally:
        qnp.stop()