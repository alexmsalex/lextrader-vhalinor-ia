from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Callable
import threading
import time
import math
import random
import html

def _escape(s: Optional[str]) -> str:
    return html.escape(s or "")

def _cn(*classes: Optional[str]) -> str:
    return " ".join(filter(None, classes))

# Data classes
@dataclass
class SynapticConnection:
    id: str
    from_neuron_id: str
    to_neuron_id: str
    weight: float
    strength: float
    plasticity: float
    frequency: float
    latency: float
    neurotransmitter: str
    is_excitatory: bool
    last_fired: float
    adaptation_rate: float
    refraction_period: float
    connection_type: str

@dataclass
class NeuralCluster:
    id: str
    name: str
    region: str
    specialization: str
    neurons: int
    connections: int
    activity: float
    coherence: float
    network_position: Dict[str, float]
    activation_threshold: float
    learning_rate: float
    memory_capacity: int
    processing_speed: int

@dataclass
class NetworkTopology:
    small_world_index: float = 0.0
    clustering_coefficient: float = 0.0
    path_length: float = 0.0
    network_efficiency: float = 0.0
    modularity_score: float = 0.0
    hub_connectivity: float = 0.0
    neural_density: float = 0.0
    information_flow: float = 0.0
    synchronization: float = 0.0
    plasticity: float = 0.0

@dataclass
class BrainwavePattern:
    frequency: float
    amplitude: float
    type: str
    phase: float
    coherence: float
    timestamp: float

class NeuralConnectionMatrix:
    """
    Módulo server-side que simula clusters neurais, conexões sinápticas e padrões de atividade.
    Use render_html() para obter bloco HTML com resumo; a visualização canvas deve ser implementada no cliente.
    """
    def __init__(self, activity_interval: float = 0.1):
        self.connections: List[SynapticConnection] = []
        self.clusters: List[NeuralCluster] = []
        self.topology = NetworkTopology()
        self.brainwaves: List[BrainwavePattern] = []

        self.is_active = True
        self.learning_active = False
        self.plasticity_level = 0.8
        self.synchronization_rate = 0.75
        self.neural_density = 0.6
        self.current_view = 'MATRIX'  # MATRIX | TOPOLOGY | BRAINWAVES | 3D

        self._activity_interval = activity_interval
        self._stop = threading.Event()
        self._activity_thread: Optional[threading.Thread] = None

        # Inicializa
        self.initialize_neural_clusters()
        self.generate_synaptic_connections()
        self.start_activity_loop()

        # registrar no barramento para outros módulos consultarem topologia/brainwaves
        try:
            from neural_bus import NeuralBus
            NeuralBus.get_instance().register("connection_matrix", self)
        except Exception:
            pass

    # Inicialização de clusters
    def initialize_neural_clusters(self) -> List[NeuralCluster]:
        new_clusters = [
            NeuralCluster('prefrontal_analysis', 'Córtex Pré-frontal Analítico', 'PREFRONTAL', 'ANALYSIS',
                          15000, 450000, 85.2, 92.1, {'x':0.2,'y':0.8,'z':0.9}, 0.65, 0.012, 2048, 150),
            NeuralCluster('temporal_pattern', 'Lobo Temporal de Padrões', 'TEMPORAL', 'PATTERN_RECOGNITION',
                          22000, 880000, 91.7, 87.3, {'x':0.7,'y':0.4,'z':0.6}, 0.58, 0.015, 4096, 200),
            NeuralCluster('parietal_decision', 'Córtex Parietal Decisório', 'PARIETAL', 'DECISION_MAKING',
                          18500, 740000, 88.9, 94.6, {'x':0.5,'y':0.9,'z':0.7}, 0.72, 0.009, 1536, 180),
            NeuralCluster('occipital_prediction', 'Córtex Occipital Preditivo', 'OCCIPITAL', 'PREDICTION',
                          12800, 384000, 82.4, 89.1, {'x':0.1,'y':0.1,'z':0.5}, 0.61, 0.018, 3072, 220),
            NeuralCluster('limbic_emotion', 'Sistema Límbico Emocional', 'LIMBIC', 'EMOTION',
                          8200, 246000, 95.3, 78.2, {'x':0.5,'y':0.5,'z':0.3}, 0.45, 0.025, 512, 300),
            NeuralCluster('cerebellum_memory', 'Cerebelo de Memória', 'CEREBELLUM', 'MEMORY',
                          35000, 1750000, 76.8, 96.7, {'x':0.8,'y':0.2,'z':0.4}, 0.55, 0.007, 8192, 120),
        ]
        self.clusters = new_clusters
        return new_clusters

    # Geração de conexões sinápticas
    def generate_synaptic_connections(self) -> List[SynapticConnection]:
        new_connections: List[SynapticConnection] = []
        cid = 0

        # Intra-cluster
        for cluster in self.clusters:
            intra = int(cluster.neurons * 0.3)
            for _ in range(intra):
                from_neuron = f"{cluster.id}_neuron_{random.randrange(cluster.neurons)}"
                to_neuron = f"{cluster.id}_neuron_{random.randrange(cluster.neurons)}"
                if from_neuron == to_neuron:
                    continue
                conn = SynapticConnection(
                    id=f"conn_{cid}",
                    from_neuron_id=from_neuron,
                    to_neuron_id=to_neuron,
                    weight=(random.random()-0.5)*2,
                    strength=random.random()*0.8 + 0.2,
                    plasticity=self.plasticity_level + (random.random()-0.5)*0.2,
                    frequency=random.random()*100 + 10,
                    latency=random.random()*5 + 1,
                    neurotransmitter=random.choice(['DOPAMINE','SEROTONIN','ACETYLCHOLINE','GABA','GLUTAMATE']),
                    is_excitatory=random.random() > 0.2,
                    last_fired=0.0,
                    adaptation_rate=random.random()*0.1 + 0.05,
                    refraction_period=random.random()*3 + 2,
                    connection_type='LATERAL'
                )
                new_connections.append(conn)
                cid += 1

        # Inter-cluster
        for i in range(len(self.clusters)):
            for j in range(i+1, len(self.clusters)):
                c1 = self.clusters[i]
                c2 = self.clusters[j]
                dist = math.sqrt((c1.network_position['x']-c2.network_position['x'])**2 +
                                 (c1.network_position['y']-c2.network_position['y'])**2 +
                                 (c1.network_position['z']-c2.network_position['z'])**2)
                compat = 1.0 / (1.0 + dist)
                count = int(compat * 500 * self.neural_density)
                for _ in range(count):
                    from_neuron = f"{c1.id}_neuron_{random.randrange(c1.neurons)}"
                    to_neuron = f"{c2.id}_neuron_{random.randrange(c2.neurons)}"
                    conn = SynapticConnection(
                        id=f"conn_{cid}",
                        from_neuron_id=from_neuron,
                        to_neuron_id=to_neuron,
                        weight=(random.random()-0.5)*1.5*compat,
                        strength=random.random()*0.6 + 0.1,
                        plasticity=self.plasticity_level * compat,
                        frequency=random.random()*80 + 5,
                        latency=random.random()*10 + dist*5,
                        neurotransmitter=random.choice(['DOPAMINE','ACETYLCHOLINE','GLUTAMATE']),
                        is_excitatory=random.random() > 0.15,
                        last_fired=0.0,
                        adaptation_rate=random.random()*0.05 + 0.02,
                        refraction_period=random.random()*4 + 3,
                        connection_type=random.choice(['SKIP','FEEDFORWARD'])
                    )
                    new_connections.append(conn)
                    cid += 1
                # feedback
                feedback = int(count*0.4)
                for _ in range(feedback):
                    from_neuron = f"{c2.id}_neuron_{random.randrange(c2.neurons)}"
                    to_neuron = f"{c1.id}_neuron_{random.randrange(c1.neurons)}"
                    conn = SynapticConnection(
                        id=f"conn_{cid}",
                        from_neuron_id=from_neuron,
                        to_neuron_id=to_neuron,
                        weight=(random.random()-0.5)*1.2*compat,
                        strength=random.random()*0.4 + 0.1,
                        plasticity=self.plasticity_level*0.8,
                        frequency=random.random()*60 + 5,
                        latency=random.random()*12 + dist*6,
                        neurotransmitter=random.choice(['GABA','SEROTONIN']),
                        is_excitatory=random.random() > 0.6,
                        last_fired=0.0,
                        adaptation_rate=random.random()*0.03 + 0.01,
                        refraction_period=random.random()*5 + 4,
                        connection_type='FEEDBACK'
                    )
                    new_connections.append(conn)
                    cid += 1

        # Recurrent for memory specializations
        for cluster in self.clusters:
            if cluster.specialization in ('MEMORY','DECISION_MAKING'):
                recurrent = int(cluster.neurons * 0.15)
                for _ in range(recurrent):
                    nid = f"{cluster.id}_neuron_{random.randrange(cluster.neurons)}"
                    conn = SynapticConnection(
                        id=f"conn_{cid}",
                        from_neuron_id=nid,
                        to_neuron_id=nid,
                        weight=random.random()*0.8 + 0.2,
                        strength=random.random()*0.9 + 0.1,
                        plasticity=self.plasticity_level * 1.2,
                        frequency=random.random()*40 + 30,
                        latency=0.5,
                        neurotransmitter='GLUTAMATE',
                        is_excitatory=True,
                        last_fired=0.0,
                        adaptation_rate=random.random()*0.08 + 0.03,
                        refraction_period=1.0,
                        connection_type='RECURRENT'
                    )
                    new_connections.append(conn)
                    cid += 1

        self.connections = new_connections

        # compute topology metrics
        total_conn = len(new_connections)
        total_neurons = sum(c.neurons for c in self.clusters)
        self.topology = NetworkTopology(
            small_world_index=0.68 + random.random()*0.2,
            clustering_coefficient=0.45 + random.random()*0.25,
            path_length=2.1 + random.random()*0.8,
            network_efficiency=0.78 + random.random()*0.15,
            modularity_score=0.52 + random.random()*0.18,
            hub_connectivity=(total_conn/total_neurons*100) if total_neurons else 0.0,
            neural_density=self.neural_density*100,
            information_flow=self.synchronization_rate*85 + random.random()*15,
            synchronization=self.synchronization_rate*100,
            plasticity=self.plasticity_level*100
        )

        # server-side feedback (no sonner); simply print
        print(f"Matriz neural inicializada: {len(new_connections):,} conexões sinápticas")
        return new_connections

    # Simulação de atividade neural
    def _simulate_activity_step(self):
        if not self.is_active:
            return
        # update clusters activity/coherence
        for idx, cluster in enumerate(self.clusters):
            delta = (random.random()-0.5)*5*self.synchronization_rate
            cluster.activity = max(0.0, min(100.0, cluster.activity + delta))
            cluster.coherence = max(50.0, min(100.0, cluster.coherence + (random.random()-0.5)*3))
            self.clusters[idx] = cluster

        # propagate through connections: simple plasticity model
        now = time.time()
        updated_conns = []
        for conn in self.connections:
            time_since = now - conn.last_fired if conn.last_fired else float('inf')
            new_strength = conn.strength * 0.995
            new_weight = conn.weight
            if self.learning_active and time_since > conn.refraction_period:
                if random.random() < conn.plasticity:
                    if conn.is_excitatory:
                        new_weight += conn.adaptation_rate * self.plasticity_level
                        new_strength = min(1.0, new_strength + 0.01)
                    else:
                        new_weight -= conn.adaptation_rate * self.plasticity_level * 0.5
                        new_strength = max(0.1, new_strength - 0.005)
                    if random.random() < 0.1:
                        conn.last_fired = now
            conn.strength = max(0.05, new_strength)
            conn.weight = max(-2.0, min(2.0, new_weight))
            conn.frequency = max(5.0, conn.frequency * 0.998)
            updated_conns.append(conn)
        self.connections = updated_conns

        # generate brainwaves snapshot
        t = time.time()
        self.brainwaves = [
            BrainwavePattern(frequency=3 + math.sin(t*0.001)*1, amplitude=random.random()*0.3+0.1, type='DELTA', phase=(t*0.003) % (2*math.pi),
                             coherence=random.random()*0.4+0.3, timestamp=t),
            BrainwavePattern(frequency=6 + math.sin(t*0.002)*2, amplitude=random.random()*0.5+0.2, type='THETA', phase=(t*0.006) % (2*math.pi),
                             coherence=random.random()*0.5+0.4, timestamp=t),
            BrainwavePattern(frequency=10 + math.sin(t*0.0015)*3, amplitude=random.random()*0.7+0.3, type='ALPHA', phase=(t*0.01) % (2*math.pi),
                             coherence=random.random()*0.6+0.5, timestamp=t),
            BrainwavePattern(frequency=20 + math.sin(t*0.003)*10, amplitude=random.random()*0.6+0.4, type='BETA', phase=(t*0.02) % (2*math.pi),
                             coherence=random.random()*0.7+0.6, timestamp=t),
            BrainwavePattern(frequency=50 + math.sin(t*0.004)*30, amplitude=random.random()*0.4+0.2, type='GAMMA', phase=(t*0.05) % (2*math.pi),
                             coherence=random.random()*0.8+0.7, timestamp=t),
        ]

    # Activity loop control
    def _activity_loop(self):
        while not self._stop.is_set():
            self._simulate_activity_step()
            time.sleep(self._activity_interval)

    def start_activity_loop(self):
        if self._activity_thread and self._activity_thread.is_alive():
            return
        self._stop.clear()
        self._activity_thread = threading.Thread(target=self._activity_loop, daemon=True)
        self._activity_thread.start()

    def stop(self):
        self._stop.set()
        if self._activity_thread and self._activity_thread.is_alive():
            self._activity_thread.join(timeout=1.0)

    def reset_network(self):
        self.initialize_neural_clusters()
        self.generate_synaptic_connections()
        print("Matriz neural reinicializada")

    # Render server-side HTML (simplificado)
    def render_html(self) -> str:
        # summary cards
        total_connections = len(self.connections)
        excitatory = sum(1 for c in self.connections if c.is_excitatory)
        inhibitory = total_connections - excitatory
        avg_strength = (sum(c.strength for c in self.connections)/total_connections*100) if total_connections else 0.0

        parts: List[str] = []
        parts.append('<div class="card trading-card">')
        parts.append('<div class="card-header"><h3>🧠 Matriz de Conexões Neurais Amplificada</h3></div>')
        parts.append('<div class="card-content">')

        parts.append('<div class="grid grid-cols-2 md:grid-cols-4 gap-4">')
        parts.append(f'<div class="p-3 text-center"><div class="font-bold">{total_connections:,}</div><div class="text-xs text-muted-foreground">Conexões Totais</div></div>')
        parts.append(f'<div class="p-3 text-center"><div class="font-bold">{excitatory:,}</div><div class="text-xs text-muted-foreground">Excitatórias</div></div>')
        parts.append(f'<div class="p-3 text-center"><div class="font-bold">{inhibitory:,}</div><div class="text-xs text-muted-foreground">Inibitórias</div></div>')
        parts.append(f'<div class="p-3 text-center"><div class="font-bold">{avg_strength:.0f}%</div><div class="text-xs text-muted-foreground">Força Média</div></div>')
        parts.append('</div>')

        # clusters summary
        parts.append('<h4 class="font-semibold mt-4">Clusters Neurais</h4>')
        parts.append('<div class="grid gap-4">')
        for cl in self.clusters:
            parts.append('<div class="border p-3 rounded">')
            parts.append(f'<div class="flex justify-between"><div><b>{_escape(cl.name)}</b> <small class="text-muted">({_escape(cl.specialization)})</small></div><div><small>{cl.region}</small></div></div>')
            parts.append(f'<div class="text-xs mt-2">Neurônios: {cl.neurons:,} • Conexões: {cl.connections:,} • Velocidade: {cl.processing_speed} Hz</div>')
            parts.append(f'<div class="mt-2"><div class="text-xs">Atividade: {cl.activity:.1f}%</div></div>')
            parts.append('</div>')
        parts.append('</div>')

        # topology summary
        t = self.topology
        parts.append('<h4 class="font-semibold mt-4">Topologia da Rede</h4>')
        parts.append('<div class="grid grid-cols-2 gap-4">')
        parts.append(f'<div class="p-3"><div>Small-World: <b>{t.small_world_index:.2f}</b></div></div>')
        parts.append(f'<div class="p-3"><div>Clustering: <b>{t.clustering_coefficient:.2f}</b></div></div>')
        parts.append(f'<div class="p-3"><div>Path Length: <b>{t.path_length:.2f}</b></div></div>')
        parts.append(f'<div class="p-3"><div>Eficiência: <b>{t.network_efficiency*100:.1f}%</b></div></div>')
        parts.append('</div>')

        # brainwaves snapshot
        parts.append('<h4 class="font-semibold mt-4">Padrões de Ondas Cerebrais</h4>')
        parts.append('<div class="grid gap-3">')
        for w in self.brainwaves:
            parts.append('<div class="border p-3 rounded">')
            parts.append(f'<div class="flex justify-between"><div><b>{_escape(w.type)}</b> - {w.frequency:.1f} Hz</div><div class="text-xs text-muted-foreground">Coerência: {(w.coherence*100):.0f}%</div></div>')
            parts.append('</div>')
        parts.append('</div>')

        parts.append('</div></div>')
        return "\n".join(parts)

# Exemplo de uso
if __name__ == "__main__":
    ncm = NeuralConnectionMatrix()
    try:
        time.sleep(1)
        print(ncm.render_html()[:800])
    finally:
        ncm.stop()
