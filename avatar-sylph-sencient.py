"""
avatar-sylph-sencient.py
Sistema de Avatar SYLPH com integração Sencient AI
Versão com avatar arrastável, movimentos fluidos e análise de projetos
Agora com avatar em 3D usando Three.js para renderização web-based com texturas realistas e animações 3D avançadas.
Animações avançadas incluem movimentos dinâmicos de respiração, balanço de braços, aceno de cabeça, e ajustes baseados em emoção e fala.
"""

import streamlit as st
import time
import random
import threading
import asyncio
import json
import numpy as np
from datetime import datetime, timedelta
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Callable, Tuple
import queue
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import os
from pathlib import Path
import base64
from math import sin, cos, pi, radians
from collections import deque
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import subprocess
import re

# ==================== ENUMS E TIPOS ====================
class Emotion(Enum):
    NEUTRAL = ("neutral", "#06b6d4")
    HAPPY = ("happy", "#10b981")
    EXCITED = ("excited", "#f59e0b")
    FOCUSED = ("focused", "#3b82f6")
    INTENSE = ("intense", "#8b5cf6")
    SURPRISED = ("surprised", "#f97316")
    SAD = ("sad", "#6b7280")
    ANALYZING = ("analyzing", "#6366f1")
    DEFENSIVE = ("defensive", "#ef4444")
    CALM = ("calm", "#14b8a6")
    SLEEPING = ("sleeping", "#374151")
   
    def __init__(self, emotion, color):
        self.emotion_name = emotion
        self.color = color

class AvatarState(Enum):
    ACTIVE = auto()
    SLEEPING = auto()
    LISTENING = auto()
    PROCESSING = auto()
    ALERT = auto()
    ERROR = auto()
    INITIALIZING = auto()

@dataclass
class ChatMessage:
    role: str
    text: str
    emotion: Emotion = Emotion.NEUTRAL
    timestamp: datetime = None
    data_points: Optional[Dict] = None
   
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

# ==================== SISTEMA DE ARTICULAÇÕES ====================
class JointSystem:
    """Sistema para movimentos fluidos das articulações (agora usado para animações 3D via JS)"""
   
    def __init__(self):
        # Ângulos das articulações (em graus)
        self.joints = {
            'head': {'angle': 0, 'target': 0, 'speed': 0.1},
            'neck': {'angle': 0, 'target': 0, 'speed': 0.08},
            'shoulder_left': {'angle': 0, 'target': 0, 'speed': 0.07},
            'shoulder_right': {'angle': 0, 'target': 0, 'speed': 0.07},
            'elbow_left': {'angle': 0, 'target': 0, 'speed': 0.09},
            'elbow_right': {'angle': 0, 'target': 0, 'speed': 0.09},
            'wrist_left': {'angle': 0, 'target': 0, 'speed': 0.12},
            'wrist_right': {'angle': 0, 'target': 0, 'speed': 0.12},
            'torso': {'angle': 0, 'target': 0, 'speed': 0.05},
        }
       
        # Posições dos membros (agora usadas para calcular rotações em 3D)
        self.limb_positions = {
            'head': {'x': 0, 'y': -20},
            'neck': {'x': 0, 'y': 0},
            'shoulder_left': {'x': -15, 'y': 0},
            'shoulder_right': {'x': 15, 'y': 0},
            'elbow_left': {'x': -30, 'y': 25},
            'elbow_right': {'x': 30, 'y': 25},
            'hand_left': {'x': -45, 'y': 50},
            'hand_right': {'x': 45, 'y': 50},
            'torso': {'x': 0, 'y': 15},
        }
       
        self.last_update = time.time()
        self.breath_phase = 0
        self.idle_movement_timer = 0
        self.current_pose = 'idle'
   
    def update(self, emotion: Emotion, is_speaking: bool = False):
        """Atualiza as posições das articulações"""
        current_time = time.time()
        dt = min(current_time - self.last_update, 0.033)
        self.last_update = current_time
       
        # Fase da respiração (suave movimento de subida/descida)
        self.breath_phase += dt * 2
        if self.breath_phase > 2 * pi:
            self.breath_phase -= 2 * pi
       
        # Movimento de respiração (aplicado ao torso)
        breath_offset = sin(self.breath_phase) * 0.5
       
        # Determinar pose baseada na emoção
        target_pose = self._get_pose_for_emotion(emotion, is_speaking)
       
        if target_pose != self.current_pose:
            self._transition_to_pose(target_pose)
       
        # Atualizar movimento ocioso
        self.idle_movement_timer += dt
        idle_offset = sin(self.idle_movement_timer * 0.5) * 2
       
        # Aplicar movimentos suaves a todas as articulações
        for joint_name, joint in self.joints.items():
            # Movimento suave em direção ao alvo
            angle_diff = joint['target'] - joint['angle']
            joint['angle'] += angle_diff * joint['speed'] * dt * 60
           
            # Adicionar micro-movimentos naturais
            if joint_name in ['head', 'neck']:
                joint['angle'] += idle_offset * 0.1
            if joint_name in ['shoulder_left', 'shoulder_right']:
                joint['angle'] += breath_offset * 0.2
       
        # Atualizar posições dos membros com base nas articulações
        self._update_limb_positions()
   
    def _get_pose_for_emotion(self, emotion: Emotion, is_speaking: bool) -> str:
        """Determina a pose baseada na emoção"""
        if is_speaking:
            return 'speaking'
       
        poses = {
            Emotion.HAPPY: 'happy',
            Emotion.SAD: 'sad',
            Emotion.FOCUSED: 'focused',
            Emotion.ANALYZING: 'thinking',
            Emotion.DEFENSIVE: 'defensive',
            Emotion.EXCITED: 'excited',
            Emotion.SURPRISED: 'surprised',
            Emotion.CALM: 'calm',
            Emotion.SLEEPING: 'sleeping',
        }
       
        return poses.get(emotion, 'idle')
   
    def _transition_to_pose(self, pose: str):
        """Transição suave para uma nova pose"""
        self.current_pose = pose
       
        # Definir ângulos alvo para cada pose
        pose_targets = {
            'idle': {
                'head': 0, 'neck': 0,
                'shoulder_left': -10, 'shoulder_right': 10,
                'elbow_left': 20, 'elbow_right': 20,
                'wrist_left': -5, 'wrist_right': -5,
                'torso': 0
            },
            'happy': {
                'head': 5, 'neck': 0,
                'shoulder_left': -15, 'shoulder_right': 15,
                'elbow_left': 30, 'elbow_right': 30,
                'wrist_left': 10, 'wrist_right': 10,
                'torso': 2
            },
            'speaking': {
                'head': 0, 'neck': 0,
                'shoulder_left': -5, 'shoulder_right': 5,
                'elbow_left': 15, 'elbow_right': 15,
                'wrist_left': -10, 'wrist_right': 20, # Gesticulação
                'torso': 0
            },
            'thinking': {
                'head': -10, 'neck': 5,
                'shoulder_left': -20, 'shoulder_right': 0,
                'elbow_left': 90, 'elbow_right': 45, # Mão no queixo
                'wrist_left': -30, 'wrist_right': 0,
                'torso': -5
            },
            'defensive': {
                'head': 0, 'neck': 0,
                'shoulder_left': 30, 'shoulder_right': 30, # Ombros levantados
                'elbow_left': 60, 'elbow_right': 60,
                'wrist_left': 0, 'wrist_right': 0,
                'torso': 0
            },
            'sleeping': {
                'head': -30, 'neck': 10,
                'shoulder_left': -5, 'shoulder_right': 5,
                'elbow_left': 10, 'elbow_right': 10,
                'wrist_left': 0, 'wrist_right': 0,
                'torso': 5
            }
        }
       
        targets = pose_targets.get(pose, pose_targets['idle'])
       
        for joint_name, target_angle in targets.items():
            if joint_name in self.joints:
                self.joints[joint_name]['target'] = target_angle
   
    def _update_limb_positions(self):
        """Atualiza posições dos membros com base nas articulações"""
        # Cabeça e pescoço
        head_angle = radians(self.joints['head']['angle'])
        neck_angle = radians(self.joints['neck']['angle'])
       
        self.limb_positions['head']['x'] = sin(head_angle + neck_angle) * 20
        self.limb_positions['head']['y'] = -20 + cos(head_angle + neck_angle) * 5
       
        # Braços
        for side in ['left', 'right']:
            shoulder_key = f'shoulder_{side}'
            elbow_key = f'elbow_{side}'
            wrist_key = f'wrist_{side}'
            hand_key = f'hand_{side}'
           
            shoulder_angle = radians(self.joints[shoulder_key]['angle'])
            elbow_angle = radians(self.joints[elbow_key]['angle'])
            wrist_angle = radians(self.joints[wrist_key]['angle'])
           
            # Cotovelo
            self.limb_positions[elbow_key]['x'] = (
                self.limb_positions[shoulder_key]['x'] +
                cos(shoulder_angle) * 25 * (1 if side == 'right' else -1)
            )
            self.limb_positions[elbow_key]['y'] = (
                self.limb_positions[shoulder_key]['y'] +
                sin(shoulder_angle) * 25
            )
           
            # Mão
            self.limb_positions[hand_key]['x'] = (
                self.limb_positions[elbow_key]['x'] +
                cos(elbow_angle + shoulder_angle) * 25 * (1 if side == 'right' else -1)
            )
            self.limb_positions[hand_key]['y'] = (
                self.limb_positions[elbow_key]['y'] +
                sin(elbow_angle + shoulder_angle) * 25
            )
       
        # Torso (movimento de respiração)
        torso_angle = radians(self.joints['torso']['angle'])
        self.limb_positions['torso']['y'] = 15 + sin(torso_angle) * 3
   
    def get_3d_avatar_html(self, emotion: Emotion, is_speaking: bool = False) -> str:
        """Gera HTML com Three.js para avatar 3D com texturas realistas e animações avançadas"""
        self.update(emotion, is_speaking)
       
        # Cores baseadas na emoção
        glow_color = f"{emotion.color}44"
       
        # Tamanho do avatar
        width = 120
        height = 180
       
        # Converter ângulos das articulações para rotações em 3D (em radianos para JS)
        joint_rotations = {k: radians(v['angle']) for k, v in self.joints.items()}
       
        # Texturas realistas (URLs públicas para exemplo; substitua por suas texturas)
        skin_texture_url = "https://threejs.org/examples/textures/uv_grid_opengl.jpg"  # Exemplo de textura de pele (substitua por real)
        clothing_texture_url = "https://threejs.org/examples/textures/crate.gif"  # Exemplo de textura de roupa
        
        emotion_name = emotion.emotion_name
        is_speaking_js = 'true' if is_speaking else 'false'
        
        # Script Three.js para renderizar o avatar 3D
        three_js_script = f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            const width = {width};
            const height = {height};
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(width, height);
            document.getElementById('avatar-3d-canvas').appendChild(renderer.domElement);
            
            // Luzes
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);
            
            // Texturas
            const textureLoader = new THREE.TextureLoader();
            const skinTexture = textureLoader.load('{skin_texture_url}');
            const clothingTexture = textureLoader.load('{clothing_texture_url}');
            
            // Materiais com texturas realistas
            const skinMaterial = new THREE.MeshStandardMaterial({{ map: skinTexture, roughness: 0.5, metalness: 0.2 }});
            const clothingMaterial = new THREE.MeshStandardMaterial({{ map: clothingTexture, color: '{emotion.color}', roughness: 0.7, metalness: 0.1 }});
            
            // Modelagem do avatar 3D com formas básicas (humanóide simples)
            // Torso
            const torsoGeometry = new THREE.CylinderGeometry(5, 5, 20, 32);
            const torso = new THREE.Mesh(torsoGeometry, clothingMaterial);
            torso.position.y = 0;
            torso.rotation.z = {joint_rotations['torso']};
            scene.add(torso);
            
            // Cabeça
            const headGeometry = new THREE.SphereGeometry(6, 32, 32);
            const head = new THREE.Mesh(headGeometry, skinMaterial);
            head.position.y = 15;
            head.rotation.z = {joint_rotations['head']};
            scene.add(head);
            
            // Pescoço
            const neckGeometry = new THREE.CylinderGeometry(3, 3, 5, 32);
            const neck = new THREE.Mesh(neckGeometry, skinMaterial);
            neck.position.y = 10;
            neck.rotation.z = {joint_rotations['neck']};
            scene.add(neck);
            
            // Braço esquerdo
            const shoulderLeftGeometry = new THREE.CylinderGeometry(2, 2, 10, 32);
            const shoulderLeft = new THREE.Mesh(shoulderLeftGeometry, skinMaterial);
            shoulderLeft.position.set(-5, 5, 0);
            shoulderLeft.rotation.z = {joint_rotations['shoulder_left']};
            scene.add(shoulderLeft);
            
            const elbowLeftGeometry = new THREE.CylinderGeometry(2, 2, 10, 32);
            const elbowLeft = new THREE.Mesh(elbowLeftGeometry, skinMaterial);
            elbowLeft.position.set(-10, 0, 0);
            elbowLeft.rotation.z = {joint_rotations['elbow_left']};
            scene.add(elbowLeft);
            
            // Braço direito (similar)
            const shoulderRightGeometry = new THREE.CylinderGeometry(2, 2, 10, 32);
            const shoulderRight = new THREE.Mesh(shoulderRightGeometry, skinMaterial);
            shoulderRight.position.set(5, 5, 0);
            shoulderRight.rotation.z = {joint_rotations['shoulder_right']};
            scene.add(shoulderRight);
            
            const elbowRightGeometry = new THREE.CylinderGeometry(2, 2, 10, 32);
            const elbowRight = new THREE.Mesh(elbowRightGeometry, skinMaterial);
            elbowRight.position.set(10, 0, 0);
            elbowRight.rotation.z = {joint_rotations['elbow_right']};
            scene.add(elbowRight);
            
            // Posição da câmera
            camera.position.z = 40;
            
            // Parâmetros de emoção e fala
            const emotion = '{emotion_name}';
            const isSpeaking = {is_speaking_js};
            
            // Animação avançada
            let time = 0;
            function animate() {{
                requestAnimationFrame(animate);
                time += 0.01;
                
                // Amplitude baseada na emoção
                let amplitude = 1;
                let breathSpeed = 2;
                if (emotion === 'excited' || emotion === 'happy') {{
                    amplitude = 1.5;
                    breathSpeed = 3;
                }} else if (emotion === 'sad' || emotion === 'sleeping') {{
                    amplitude = 0.5;
                    breathSpeed = 1;
                }} else if (emotion === 'defensive' || emotion === 'intense') {{
                    amplitude = 1.2;
                    breathSpeed = 2.5;
                }}
                
                // Respiração avançada (escala e leve rotação do torso)
                torso.scale.y = 1 + Math.sin(time * breathSpeed) * 0.05 * amplitude;
                torso.rotation.y = Math.sin(time * breathSpeed / 2) * 0.05 * amplitude;
                
                // Movimento idle da cabeça (balanço e aceno)
                head.rotation.y = Math.sin(time * 0.5) * 0.2 * amplitude;
                head.rotation.x = Math.cos(time * 0.3) * 0.1 * amplitude;
                
                // Balanço dos braços (swing natural)
                shoulderLeft.rotation.z = {joint_rotations['shoulder_left']} + Math.sin(time * 1.5) * 0.3 * amplitude;
                shoulderRight.rotation.z = {joint_rotations['shoulder_right']} + Math.sin(time * 1.5 + Math.PI) * 0.3 * amplitude;
                
                // Dobramento dos cotovelos (gesticulação)
                elbowLeft.rotation.z = {joint_rotations['elbow_left']} + Math.sin(time * 2) * 0.2 * amplitude;
                elbowRight.rotation.z = {joint_rotations['elbow_right']} + Math.sin(time * 2 + Math.PI / 2) * 0.2 * amplitude;
                
                // Animações específicas para fala (gestos de cabeça e braços)
                if (isSpeaking) {{
                    head.rotation.x += Math.sin(time * 10) * 0.05; // Aceno rápido
                    shoulderLeft.rotation.z += Math.sin(time * 5) * 0.1; // Gesticulação
                    shoulderRight.rotation.z += Math.cos(time * 5) * 0.1;
                }}
                
                // Efeito de surpresa ou foco (pulos leves no torso para excitação)
                if (emotion === 'surprised' || emotion === 'excited') {{
                    torso.position.y = Math.abs(Math.sin(time * 5)) * 0.5 * amplitude;
                }}
                
                renderer.render(scene, camera);
            }}
            animate();
        </script>
        """
       
        return f'''
            <div id="avatar-3d-canvas" style="width: {width}px; height: {height}px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));"></div>
            {three_js_script}
        '''

# ==================== ANIMAÇÃO DE PARTÍCULAS ====================
class ParticleSystem:
    def __init__(self, max_particles=200):
        self.particles = []
        self.max_particles = max_particles
        self.last_update = time.time()
       
    def emit(self, x: float, y: float, count: int = 10,
             color: str = "#06b6d4", symbol: str = "•",
             velocity_range: Tuple[float, float] = (-1, 1)):
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            vx = random.uniform(*velocity_range)
            vy = random.uniform(*velocity_range)
            life = random.uniform(0.5, 1.5)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'life': life,
                'max_life': life,
                'color': color,
                'symbol': symbol,
                'size': random.uniform(0.5, 1.5)
            })
   
    def update(self, dt: float):
        current_time = time.time()
        dt = min(current_time - self.last_update, 0.033)
        self.last_update = current_time
       
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt * 60
            p['y'] += p['vy'] * dt * 60
            p['life'] -= dt
           
            p['vy'] += 0.1 * dt * 60
            if p['life'] < p['max_life'] * 0.3:
                p['vx'] *= 0.9
                p['vy'] *= 0.9
           
            if p['life'] <= 0:
                self.particles.remove(p)
   
    def render_html(self) -> str:
        if not self.particles:
            return ""
       
        particles_html = []
        for p in self.particles:
            opacity = p['life'] / p['max_life']
            size = p['size'] * (0.5 + opacity * 0.5)
            particles_html.append(
                f'<div style="position: absolute; left: {p["x"]}px; top: {p["y"]}px; '
                f'color: {p["color"]}; opacity: {opacity}; font-size: {size}rem; '
                f'transform: translate(-50%, -50%); pointer-events: none;">{p["symbol"]}</div>'
            )
       
        return ''.join(particles_html)

# ==================== SISTEMA DE ARQUIVOS LEXTRADER-IAG ====================
class SistemaArquivos:
    """Sistema de análise de arquivos do projeto LEXTRADER-IAG"""
    def __init__(self, caminho_base=None):
        # Tentar detectar caminho automaticamente
        if caminho_base is None:
            # Tentar caminhos comuns
            possiveis_caminhos = [
                "C:\\Users\\ALEXMS-PC\\Desktop\\LEXTRADER-IAG 3.0",
                os.path.join(os.path.expanduser("~"), "Desktop", "LEXTRADER-IAG 3.0"),
                os.path.join(os.path.dirname(__file__), ".."),
            ]
           
            for caminho in possiveis_caminhos:
                if os.path.exists(caminho):
                    self.caminho_base = caminho
                    break
            else:
                self.caminho_base = os.path.dirname(__file__)
        else:
            self.caminho_base = caminho_base
       
        self.arquivos_analisados = {}
        self.estatisticas = {}
        self.ultima_analise = None
       
        # Palavras-chave para análise de trading
        self.keywords_trading = {
            'estratégias': ['estrategia', 'strategy', 'trading', 'algoritmo', 'bot'],
            'indicadores': ['rsi', 'macd', 'ema', 'sma', 'bollinger', 'stochastic'],
            'risco': ['stop loss', 'take profit', 'risco', 'drawdown', 'volatilidade'],
            'dados': ['csv', 'json', 'database', 'historico', 'candlestick'],
            'cripto': ['bitcoin', 'ethereum', 'binance', 'crypto', 'blockchain']
        }
       
    def escanear_projeto(self):
        """Escaneia todo o projeto LEXTRADER-IAG"""
        estrutura = {
            'caminho': self.caminho_base,
            'pastas': [],
            'arquivos': [],
            'total_arquivos': 0,
            'total_pastas': 0,
            'tamanho_total': 0
        }
       
        try:
            for raiz, pastas, arquivos in os.walk(self.caminho_base):
                # Limitar profundidade para performance
                if len(estrutura['pastas']) > 50:
                    break
               
                # Adicionar pasta atual
                pasta_info = {
                    'nome': os.path.basename(raiz),
                    'caminho': raiz,
                    'arquivos': []
                }
               
                # Analisar arquivos na pasta
                for arquivo in arquivos:
                    caminho_completo = os.path.join(raiz, arquivo)
                    try:
                        tamanho = os.path.getsize(caminho_completo)
                       
                        arquivo_info = {
                            'nome': arquivo,
                            'caminho': caminho_completo,
                            'tamanho': tamanho,
                            'extensao': os.path.splitext(arquivo)[1].lower(),
                            'modificacao': datetime.fromtimestamp(
                                os.path.getmtime(caminho_completo)
                            ).strftime('%Y-%m-%d %H:%M:%S')
                        }
                       
                        # Detectar tipo de conteúdo
                        arquivo_info['tipo'] = self.detectar_tipo_arquivo(arquivo_info)
                       
                        pasta_info['arquivos'].append(arquivo_info)
                        estrutura['arquivos'].append(arquivo_info)
                        estrutura['tamanho_total'] += tamanho
                        estrutura['total_arquivos'] += 1
                    except:
                        continue
               
                estrutura['pastas'].append(pasta_info)
                estrutura['total_pastas'] += 1
                   
        except Exception as e:
            st.warning(f"⚠️ Erro ao escanear: {e}")
       
        self.ultima_analise = datetime.now()
        self.estrutura_projeto = estrutura
       
        # Analisar conteúdo específico
        self.analisar_arquivos_trading()
       
        return estrutura
   
    def detectar_tipo_arquivo(self, arquivo_info):
        """Detecta o tipo de arquivo baseado no nome e extensão"""
        nome = arquivo_info['nome'].lower()
        extensao = arquivo_info['extensao']
       
        if extensao == '.py':
            if 'bot' in nome or 'trading' in nome:
                return 'bot_trading'
            elif 'estrategia' in nome or 'strategy' in nome:
                return 'estrategia'
            elif 'indicador' in nome or 'indicator' in nome:
                return 'indicador'
            else:
                return 'codigo_python'
               
        elif extensao == '.csv':
            return 'dados_mercado'
        elif extensao == '.json':
            return 'configuracao'
        elif extensao == '.txt' or extensao == '.md':
            return 'documentacao'
        elif extensao == '.ipynb':
            return 'notebook_analise'
        else:
            return 'outro'
   
    def analisar_arquivos_trading(self):
        """Analisa arquivos específicos de trading"""
        self.arquivos_trading = []
        self.metricas_projeto = {}
       
        if not hasattr(self, 'estrutura_projeto'):
            return
       
        for arquivo in self.estrutura_projeto['arquivos']:
            if arquivo['tipo'] in ['bot_trading', 'estrategia', 'indicador', 'dados_mercado']:
               
                # Análise básica do arquivo
                analise = {
                    'arquivo': arquivo['nome'],
                    'caminho': arquivo['caminho'],
                    'tipo': arquivo['tipo'],
                    'tamanho_kb': arquivo['tamanho'] / 1024,
                    'keywords_encontradas': [],
                    'complexidade': 'baixa',
                    'potencial_risco': 'baixo'
                }
               
                # Tentar ler conteúdo para análise mais profunda
                try:
                    with open(arquivo['caminho'], 'r', encoding='utf-8', errors='ignore') as f:
                        conteudo = f.read(5000) # Ler primeiros 5KB
                       
                        # Buscar keywords
                        for categoria, palavras in self.keywords_trading.items():
                            for palavra in palavras:
                                if palavra.lower() in conteudo.lower():
                                    analise['keywords_encontradas'].append(palavra)
                       
                        # Avaliar complexidade (simplificado)
                        linhas = conteudo.split('\n')
                        analise['linhas_amostra'] = len(linhas)
                       
                        if len(linhas) > 200:
                            analise['complexidade'] = 'alta'
                        elif len(linhas) > 50:
                            analise['complexidade'] = 'media'
                       
                        # Detectar possíveis riscos
                        riscos = ['sleep', 'time.sleep', 'while True', 'infinite']
                        for risco in riscos:
                            if risco in conteudo:
                                analise['potencial_risco'] = 'medio'
                               
                except:
                    pass
               
                self.arquivos_trading.append(analise)
       
        # Calcular métricas gerais
        self.metricas_projeto = {
            'total_arquivos_trading': len(self.arquivos_trading),
            'estrategias': len([a for a in self.arquivos_trading if a['tipo'] == 'estrategia']),
            'bots': len([a for a in self.arquivos_trading if a['tipo'] == 'bot_trading']),
            'indicadores': len([a for a in self.arquivos_trading if a['tipo'] == 'indicador']),
            'conjuntos_dados': len([a for a in self.arquivos_trading if a['tipo'] == 'dados_mercado']),
            'arquivos_com_risco': len([a for a in self.arquivos_trading if a['potencial_risco'] != 'baixo'])
        }
   
    def buscar_por_padrao(self, padrao):
        """Busca arquivos por padrão específico"""
        resultados = []
        padrao_lower = padrao.lower()
       
        if not hasattr(self, 'estrutura_projeto'):
            return resultados
       
        for arquivo in self.estrutura_projeto['arquivos']:
            if padrao_lower in arquivo['nome'].lower():
                resultados.append(arquivo)
            elif arquivo['tipo'] in ['bot_trading', 'estrategia', 'indicador']:
                try:
                    with open(arquivo['caminho'], 'r', encoding='utf-8', errors='ignore') as f:
                        conteudo = f.read(2000)
                        if padrao_lower in conteudo.lower():
                            resultados.append(arquivo)
                except:
                    continue
       
        return resultados
   
    def gerar_relatorio(self):
        """Gera um relatório completo do projeto"""
        if not hasattr(self, 'estrutura_projeto'):
            return "Projeto ainda não foi escaneado."
       
        relatorio = f"""
📊 RELATÓRIO DO PROJETO LEXTRADER-IAG 📊
{'='*50}
📍 Localização: {self.caminho_base}
📅 Última análise: {self.ultima_analise.strftime('%Y-%m-%d %H:%M:%S') if self.ultima_analise else 'Nunca'}
📁 ESTRUTURA DO PROJETO:
   • Pastas encontradas: {self.estrutura_projeto['total_pastas']}
   • Arquivos totais: {self.estrutura_projeto['total_arquivos']}
   • Tamanho total: {self.estrutura_projeto['tamanho_total'] / (1024*1024):.2f} MB
🎯 ARQUIVOS DE TRADING IDENTIFICADOS:
   • Estratégias: {self.metricas_projeto.get('estrategias', 0)}
   • Bots/robôs: {self.metricas_projeto.get('bots', 0)}
   • Indicadores: {self.metricas_projeto.get('indicadores', 0)}
   • Conjuntos de dados: {self.metricas_projeto.get('conjuntos_dados', 0)}
   • Total: {self.metricas_projeto.get('total_arquivos_trading', 0)}
"""
       
        return relatorio

# ==================== SISTEMA DE VOZ ====================
class AdvancedTTSService:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.is_muted = False
        self.volume = 0.9
        self.rate = 170
        self.pitch = 1.0
        self.emotion_modifiers = {
            Emotion.HAPPY: {"rate": 180, "pitch": 1.1, "volume": 0.95},
            Emotion.SAD: {"rate": 140, "pitch": 0.9, "volume": 0.8},
            Emotion.ANALYZING: {"rate": 160, "pitch": 1.0, "volume": 0.9},
            Emotion.DEFENSIVE: {"rate": 220, "pitch": 1.2, "volume": 1.0},
            Emotion.EXCITED: {"rate": 200, "pitch": 1.3, "volume": 0.98},
            Emotion.FOCUSED: {"rate": 155, "pitch": 1.05, "volume": 0.92},
            Emotion.SURPRISED: {"rate": 190, "pitch": 1.4, "volume": 0.96},
        }
        self._initialize_engine()
   
    def _initialize_engine(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
           
            # Priorizar voz feminina em português
            voz_feminina_encontrada = False
            for voice in voices:
                if 'portuguese' in str(voice.languages).lower() or 'pt' in str(voice.languages).lower():
                    if 'female' in voice.name.lower() or 'mulher' in voice.name.lower() or 'feminina' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        voz_feminina_encontrada = True
                        break
           
            # Se não encontrou voz feminina, usar qualquer voz em português
            if not voz_feminina_encontrada:
                for voice in voices:
                    if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                    elif 'female' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
           
            # Configurar propriedades da voz
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            self.engine.setProperty('pitch', self.pitch)
        except Exception as e:
            st.warning(f"TTS não inicializado: {e}")
   
    def speak(self, text: str, emotion: Emotion = Emotion.NEUTRAL):
        if self.is_muted or not self.engine:
            return
       
        modifiers = self.emotion_modifiers.get(emotion, {})
        rate = modifiers.get("rate", self.rate)
        pitch = modifiers.get("pitch", self.pitch)
        volume = modifiers.get("volume", self.volume)
       
        try:
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
           
            self.is_speaking = True
            st.session_state.is_speaking = True
           
            words = text.split()
            for i, word in enumerate(words):
                if emotion in [Emotion.DEFENSIVE, Emotion.EXCITED] and random.random() > 0.8:
                    self.engine.setProperty('rate', rate + random.randint(-10, 10))
               
                self.engine.say(word + " ")
               
                if emotion == Emotion.ANALYZING and i % 5 == 4:
                    time.sleep(0.05)
                elif emotion == Emotion.DEFENSIVE and "!" in word:
                    time.sleep(0.1)
           
            self.engine.runAndWait()
           
        except Exception as e:
            st.error(f"Erro na fala: {e}")
        finally:
            self.is_speaking = False
            st.session_state.is_speaking = False
   
    def stop(self):
        if self.engine:
            self.engine.stop()
        self.is_speaking = False
        st.session_state.is_speaking = False

# ==================== SISTEMA DE MARKET DATA ====================
class MarketDataSystem:
    def __init__(self):
        self.prices = {
            "NASDAQ": deque([100 + random.random() * 10 for _ in range(100)], maxlen=100),
            "S&P500": deque([4500 + random.random() * 100 for _ in range(100)], maxlen=100),
            "DOW": deque([35000 + random.random() * 200 for _ in range(100)], maxlen=100),
            "BTC": deque([50000 + random.random() * 5000 for _ in range(100)], maxlen=100),
        }
        self.volumes = {k: deque([random.randint(1000, 10000) for _ in range(50)], maxlen=50) for k in self.prices.keys()}
        self.last_update = time.time()
        self.trends = {k: 0 for k in self.prices.keys()}
   
    def update(self):
        current_time = time.time()
        if current_time - self.last_update > 1:
            for symbol in self.prices.keys():
                last_price = self.prices[symbol][-1]
                movement = random.gauss(0, 0.5)
                if symbol == "BTC":
                    movement = random.gauss(0, 2)
               
                new_price = last_price + movement
                self.prices[symbol].append(new_price)
               
                last_volume = self.volumes[symbol][-1]
                volume_change = random.randint(-500, 500)
                self.volumes[symbol].append(max(1000, last_volume + volume_change))
               
                if len(self.prices[symbol]) > 10:
                    recent = list(self.prices[symbol])[-10:]
                    if recent[-1] > recent[0]:
                        self.trends[symbol] = 1
                    elif recent[-1] < recent[0]:
                        self.trends[symbol] = -1
                    else:
                        self.trends[symbol] = 0
           
            self.last_update = current_time
   
    def get_market_context(self) -> str:
        contexts = []
        for symbol, trend in self.trends.items():
            if trend == 1:
                contexts.append(f"{symbol} ↗")
            elif trend == -1:
                contexts.append(f"{symbol} ↘")
            else:
                contexts.append(f"{symbol} →")
       
        if sum(self.trends.values()) > 1:
            return f"Mercado em alta: {', '.join(contexts)}"
        elif sum(self.trends.values()) < -1:
            return f"Mercado em baixa: {', '.join(contexts)}"
        else:
            return f"Mercado misto: {', '.join(contexts[:3])}"

# ==================== SISTEMA DE INTERAÇÃO AVANÇADA ====================
class SistemaInteracao:
    """Sistema de interação avançada com análise de arquivos"""
    def __init__(self, avatar, sistema_voz, sistema_arquivos):
        self.avatar = avatar
        self.voz = sistema_voz
        self.arquivos = sistema_arquivos
        self.historico_conversa = deque(maxlen=20)
        self.estado_emocional = "feliz"
        self.usuario_nome = None
        self.interacoes = 0
       
        # Comandos disponíveis
        self.comandos = {
            'analisar': self.comando_analisar,
            'buscar': self.comando_buscar,
            'relatorio': self.comando_relatorio,
            'estrutura': self.comando_estrutura,
            'ajuda': self.comando_ajuda,
            'estado': self.comando_estado,
            'nome': self.comando_nome,
            'obrigado': self.comando_obrigado
        }
       
        # Iniciar escaneamento do projeto em background
        threading.Thread(target=self._escanear_background, daemon=True).start()
   
    def _escanear_background(self):
        """Escaneia o projeto em background"""
        try:
            self.arquivos.escanear_projeto()
        except:
            pass
   
    def processar_comando(self, texto):
        """Processa o comando do usuário"""
        self.interacoes += 1
        self.historico_conversa.append({
            'usuario': texto,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
       
        # Detectar nome do usuário
        if self.usuario_nome is None and 'meu nome é' in texto.lower():
            partes = texto.lower().split('meu nome é')
            if len(partes) > 1:
                self.usuario_nome = partes[1].strip().split()[0].capitalize()
                self.avatar.display_message(f"Prazer em conhecê-lo, {self.usuario_nome}!", Emotion.HAPPY)
                return f"Prazer em conhecê-lo, {self.usuario_nome}!"
       
        # Verificar estado emocional do usuário
        self.detectar_emocao_usuario(texto)
       
        # Processar comandos específicos
        for comando, funcao in self.comandos.items():
            if comando in texto.lower():
                resposta = funcao(texto)
               
                # Atualizar emoção do avatar baseada na resposta
                self.atualizar_emocao_avatar(resposta)
               
                # Responder com voz
                if self.voz and not st.session_state.get('is_muted', False):
                    threading.Thread(
                        target=self.voz.speak,
                        args=(resposta, Emotion.HAPPY),
                        daemon=True
                    ).start()
               
                return resposta
       
        # Resposta padrão
        respostas_padrao = [
            "Interessante! Gostaria que eu analise algum arquivo específico do seu projeto?",
            f"Como posso ajudar você{' ' + self.usuario_nome if self.usuario_nome else ''} com o projeto LEXTRADER-IAG?",
            "Estou aqui para ajudar na análise do seu sistema de trading. O que gostaria de saber?",
            "Posso analisar estratégias, buscar arquivos ou mostrar o relatório do projeto."
        ]
       
        resposta = random.choice(respostas_padrao)
        if self.voz and not st.session_state.get('is_muted', False):
            threading.Thread(
                target=self.voz.speak,
                args=(resposta, Emotion.NEUTRAL),
                daemon=True
            ).start()
        return resposta
   
    def comando_analisar(self, texto):
        """Comando: analisar projeto/arquivos"""
        relatorio = self.arquivos.gerar_relatorio()
       
        # Resumo falado
        resumo = f"""
        Analisei seu projeto LEXTRADER-IAG.
        Encontrei {self.arquivos.metricas_projeto.get('total_arquivos_trading', 0)} arquivos relacionados a trading,
        incluindo {self.arquivos.metricas_projeto.get('estrategias', 0)} estratégias e {self.arquivos.metricas_projeto.get('bots', 0)} bots.
        """
       
        # Mostrar relatório no console
        st.info(relatorio)
       
        self.avatar.display_message(resumo.strip(), Emotion.ANALYZING)
        return resumo.strip()
   
    def comando_buscar(self, texto):
        """Comando: buscar por padrão específico"""
        padrao = texto.lower().replace('buscar', '').replace('por', '').strip()
       
        if not padrao:
            return "O que você gostaria que eu busque nos arquivos?"
       
        resultados = self.arquivos.buscar_por_padrao(padrao)
       
        if not resultados:
            return f"Não encontrei nada relacionado a '{padrao}' no projeto."
       
        resposta = f"Encontrei {len(resultados)} resultados para '{padrao}':\n"
       
        for i, resultado in enumerate(resultados[:3]): # Mostrar apenas 3
            resposta += f"{i+1}. {resultado['nome']} ({resultado['tipo']})\n"
       
        if len(resultados) > 3:
            resposta += f"... e mais {len(resultados) - 3} resultados."
       
        self.avatar.display_message(resposta, Emotion.HAPPY)
        return resposta
   
    def comando_relatorio(self, texto):
        """Comando: mostrar relatório completo"""
        relatorio = self.arquivos.gerar_relatorio()
        st.info(relatorio)
       
        return "Relatório completo exibido. Posso destacar alguma parte específica?"
   
    def comando_estrutura(self, texto):
        """Comando: mostrar estrutura de pastas"""
        if not hasattr(self, 'estrutura_projeto'):
            return "Projeto ainda não foi escaneado. Aguarde um momento..."
       
        estrutura = self.arquivos.estrutura_projeto
       
        resposta = f"Estrutura do projeto ({estrutura['total_pastas']} pastas, {estrutura['total_arquivos']} arquivos):\n"
       
        # Mostrar principais pastas
        for pasta in estrutura['pastas'][:5]:
            resposta += f"📁 {pasta['nome']} ({len(pasta['arquivos'])} arquivos)\n"
       
        return resposta
   
    def comando_ajuda(self, texto):
        """Comando: mostrar ajuda"""
        ajuda = """
        Comandos disponíveis:
       
        • "Analisar projeto" - Analisa todo o sistema LEXTRADER-IAG
        • "Buscar por [termo]" - Busca em arquivos e conteúdo
        • "Mostrar relatório" - Exibe relatório completo
        • "Mostrar estrutura" - Mostra organização de pastas
        • "Como estou?" - Mostra meu estado emocional
        • "Meu nome é [nome]" - Eu lembrarei seu nome
       
        Você também pode conversar normalmente comigo!
        """
       
        st.info(ajuda)
        return "Mostrei os comandos disponíveis. Como posso ajudar?"
   
    def comando_estado(self, texto):
        """Comando: verificar estado emocional"""
        estados = {
            "feliz": ["Estou radiante! Pronta para analisar seus trades!", "Me sinto ótima, obrigada!"],
            "curiosa": ["Estou muito curiosa sobre seu projeto de trading!", "Quero saber mais sobre suas estratégias!"],
            "concentrada": ["Estou totalmente focada na análise dos dados!", "Concentrada em encontrar insights valiosos!"],
            "empolgada": ["Estou empolgada com as possibilidades do seu projeto!", "Mal posso esperar para explorar mais!"]
        }
       
        resposta = random.choice(estados.get(self.estado_emocional, ["Estou bem, obrigada!"]))
        self.avatar.display_message(resposta, Emotion.HAPPY)
        return resposta
   
    def comando_nome(self, texto):
        """Comando: definir nome do usuário"""
        if self.usuario_nome:
            return f"Eu já sei que você se chama {self.usuario_nome}! É um prazer!"
        else:
            return "Ainda não sei seu nome. Pode me dizer qual é?"
   
    def comando_obrigado(self, texto):
        """Resposta a agradecimentos"""
        respostas = [
            "De nada! É um prazer ajudar!",
            "Por nada! Estou aqui para isso!",
            "Fico feliz em poder ajudar!",
            "O prazer é todo meu!"
        ]
       
        # Alterar emoção para mais feliz
        self.estado_emocional = "feliz"
       
        resposta = random.choice(respostas)
        self.avatar.display_message(resposta, Emotion.HAPPY)
        return resposta
   
    def detectar_emocao_usuario(self, texto):
        """Detecta emoção do usuário baseada no texto"""
        texto_lower = texto.lower()
       
        # Palavras-chave para diferentes emoções
        emocional_positivo = ['obrigado', 'grato', 'incrível', 'maravilhoso', 'ótimo', 'excelente']
        emocional_negativo = ['problema', 'erro', 'não funciona', 'difícil', 'complicado']
        emocional_urgencia = ['urgente', 'rápido', 'agora', 'imediatamente']
       
        if any(palavra in texto_lower for palavra in emocional_urgencia):
            self.estado_emocional = "concentrada"
            self.avatar.display_message("Entendido! Focando na tarefa urgente!", Emotion.FOCUSED)
        elif any(palavra in texto_lower for palavra in emocional_negativo):
            self.estado_emocional = "preocupada"
            self.avatar.display_message("Vou ajudar a resolver isso!", Emotion.DEFENSIVE)
        elif any(palavra in texto_lower for palavra in emocional_positivo):
            self.estado_emocional = "feliz"
            self.avatar.display_message("Fico feliz em ajudar!", Emotion.HAPPY)
        else:
            self.estado_emocional = "curiosa"
   
    def atualizar_emocao_avatar(self, resposta):
        """Atualiza emoção do avatar baseada na resposta"""
        if any(palavra in resposta.lower() for palavra in ['encontrei', 'descobri', 'achei', 'sucesso']):
            self.avatar.display_message("Sucesso!", Emotion.HAPPY)
        elif any(palavra in resposta.lower() for palavra in ['erro', 'problema', 'não encontrei', 'cuidado']):
            self.avatar.display_message("Problema detectado!", Emotion.DEFENSIVE)
        elif any(palavra in resposta.lower() for palavra in ['analisando', 'processando', 'calculando']):
            self.avatar.display_message("Processando...", Emotion.ANALYZING)

# ==================== AVATAR PRINCIPAL ARRASTÁVEL ====================
class DraggableAvatar:
    def __init__(self):
        self.market_system = MarketDataSystem()
        self.particle_system = ParticleSystem()
        self.joint_system = JointSystem()
        self.tts_service = AdvancedTTSService()
       
        # Inicializar sistemas avançados
        self.sistema_arquivos = SistemaArquivos()
        self.sistema_interacao = SistemaInteracao(self, self.tts_service, self.sistema_arquivos)
       
        # Inicializar estado da sessão
        self._init_session_state()
       
        # Thread de atualização automática
        self.running = True
        self.update_thread = threading.Thread(target=self._auto_update, daemon=True)
        self.update_thread.start()
   
    def _init_session_state(self):
        defaults = {
            'avatar_visible': True,
            'is_speaking': False,
            'is_muted': False,
            'current_emotion': Emotion.NEUTRAL,
            'avatar_state': AvatarState.ACTIVE,
            'local_message': None,
            'show_speech': False,
            'particles_enabled': True,
            'animations_enabled': True,
            'chat_history': [],
            'interaction_cooldown': 0,
            'last_interaction': time.time(),
            'health': 100,
            'energy': 100,
            'mood': 75,
            'voice_enabled': True,
            'auto_analyze': True,
           
            # Posição do avatar (agora é arrastável)
            'avatar_position': {'x': 50, 'y': 50}, # Posição inicial
            'is_dragging': False,
            'drag_start': {'x': 0, 'y': 0},
           
            # Sistema de interação avançada
            'comando_usuario': '',
            'mostrar_console': False,
        }
       
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
   
    def _auto_update(self):
        """Thread para atualizações automáticas"""
        while self.running:
            try:
                self.market_system.update()
               
                # Auto-emotion baseado no mercado
                if st.session_state.auto_analyze and not st.session_state.is_speaking:
                    self._update_auto_emotion()
               
                # Check for idle state
                if time.time() - st.session_state.last_interaction > 60:
                    if st.session_state.avatar_state != AvatarState.SLEEPING:
                        st.session_state.avatar_state = AvatarState.SLEEPING
                        st.session_state.current_emotion = Emotion.SLEEPING
               
                time.sleep(0.033) # ~30 FPS
            except:
                time.sleep(1)
   
    def _update_auto_emotion(self):
        """Atualiza emoção automaticamente baseado no mercado"""
        market_trend = sum(self.market_system.trends.values())
       
        if market_trend >= 2:
            st.session_state.current_emotion = Emotion.HAPPY
        elif market_trend <= -2:
            st.session_state.current_emotion = Emotion.DEFENSIVE
        elif abs(market_trend) == 1:
            st.session_state.current_emotion = Emotion.FOCUSED
        elif random.random() > 0.99:
            st.session_state.current_emotion = random.choice([
                Emotion.CALM, Emotion.NEUTRAL, Emotion.FOCUSED
            ])
   
    def analyze_emotion(self, text: str) -> Emotion:
        """Análise de emoção"""
        if not text:
            return Emotion.NEUTRAL
       
        lower_text = text.lower()
       
        emotion_keywords = {
            Emotion.HAPPY: ['lucro', 'ganho', 'ótimo', 'excelente', 'positivo', 'alta', 'profit'],
            Emotion.EXCITED: ['oportunidade', 'chance', 'rápido', 'urgente', 'agora'],
            Emotion.SAD: ['perda', 'prejuízo', 'triste', 'queda', 'baixa', 'loss'],
            Emotion.DEFENSIVE: ['risco', 'perigo', 'stop', 'pânico', 'defesa', 'cuidado', 'alerta'],
            Emotion.ANALYZING: ['analisar', 'processar', 'varredura', 'scan', 'dados', 'estatística'],
            Emotion.FOCUSED: ['foco', 'atenção', 'importante', 'crucial', 'prioridade'],
            Emotion.SURPRISED: ['incrível', 'uau', 'surpresa', 'inesperado', '?', 'como'],
        }
       
        emotion_scores = {emotion: 0 for emotion in emotion_keywords.keys()}
       
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in lower_text:
                    emotion_scores[emotion] += 1
       
        if '!' in text:
            if '!' * 3 in text:
                emotion_scores[Emotion.DEFENSIVE] += 2
            else:
                emotion_scores[Emotion.EXCITED] += 1
       
        if '?' in text:
            emotion_scores[Emotion.SURPRISED] += 1
       
        max_score = max(emotion_scores.values())
        if max_score > 0:
            top_emotions = [e for e, s in emotion_scores.items() if s == max_score]
            return random.choice(top_emotions)
       
        return Emotion.NEUTRAL
   
    def display_message(self, message: str, emotion: Emotion = None,
                       particle_effect: bool = True):
        """Exibe mensagem com efeitos visuais"""
        if not message:
            return
       
        if emotion is None:
            emotion = self.analyze_emotion(message)
       
        st.session_state.local_message = message
        st.session_state.current_emotion = emotion
        st.session_state.show_speech = True
        st.session_state.last_interaction = time.time()
        st.session_state.avatar_state = AvatarState.ACTIVE
       
        # TTS
        if st.session_state.voice_enabled and not st.session_state.is_muted:
            threading.Thread(
                target=self.tts_service.speak,
                args=(message, emotion),
                daemon=True
            ).start()
       
        # Auto-hide speech bubble
        def hide_speech():
            time.sleep(len(message) * 0.1 + 3)
            st.session_state.show_speech = False
       
        threading.Thread(target=hide_speech, daemon=True).start()
   
    def _create_particle_effect(self, emotion: Emotion):
        """Cria efeito de partículas baseado na emoção"""
        symbols = ["•", "✦", "⭓", "⭔", "◈", "○", "□"]
        colors = {
            Emotion.HAPPY: ["#10b981", "#34d399", "#a7f3d0"],
            Emotion.DEFENSIVE: ["#ef4444", "#f87171", "#fca5a5"],
            Emotion.ANALYZING: ["#3b82f6", "#60a5fa", "#93c5fd"],
            Emotion.EXCITED: ["#f59e0b", "#fbbf24", "#fcd34d"],
            Emotion.SURPRISED: ["#f97316", "#fb923c", "#fdba74"],
        }
       
        particle_colors = colors.get(emotion, ["#06b6d4", "#22d3ee", "#67e8f9"])
        count = random.randint(15, 30)
       
        # Emitir da posição do avatar
        pos = st.session_state.avatar_position
        for _ in range(count):
            self.particle_system.emit(
                x=pos['x'] + random.randint(-20, 20),
                y=pos['y'] + random.randint(-20, 20),
                count=1,
                color=random.choice(particle_colors),
                symbol=random.choice(symbols),
                velocity_range=(-2, 2)
            )
   
    def render(self):
        """Renderiza o avatar arrastável"""
        self._render_styles()
       
        if not st.session_state.avatar_visible:
            return
       
        emotion = st.session_state.current_emotion
        pos = st.session_state.avatar_position
       
        # Balão de fala
        speech_html = ""
        if st.session_state.show_speech and st.session_state.local_message:
            speech_html = f'''
                <div class="speech-bubble" style="left: {pos['x'] + 60}px; top: {pos['y'] - 100}px;
                      border-color: {emotion.color};">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;
                              color: {emotion.color}; font-size: 0.7rem; font-weight: bold;">
                        <span>📻</span> SYLPH • {emotion.emotion_name.upper()}
                    </div>
                    <div style="color: #e5e7eb;">
                        {st.session_state.local_message}
                    </div>
                </div>
            '''
       
        # Avatar 3D HTML com Three.js
        avatar_html_3d = self.joint_system.get_3d_avatar_html(
            emotion,
            st.session_state.is_speaking
        )
       
        # Renderizar avatar arrastável
        avatar_html = f'''
            <div class="avatar-draggable-container">
                {speech_html}
               
                <div id="draggable-avatar" class="draggable-avatar"
                     style="left: {pos['x']}px; top: {pos['y']}px;"
                     data-emotion="{emotion.emotion_name}">
                   
                    <!-- Aura -->
                    <div class="avatar-aura" style="border-color: {emotion.color};"></div>
                   
                    <!-- Avatar 3D -->
                    <div class="avatar-3d-container">
                        {avatar_html_3d}
                    </div>
                   
                    <!-- Status -->
                    <div class="avatar-status">
                        <div class="status-bar">
                            <div class="status-fill" style="width: {st.session_state.energy}%;
                                 background: {emotion.color};"></div>
                        </div>
                        <div class="status-text">
                            {emotion.emotion_name.upper()}
                        </div>
                    </div>
                </div>
               
                <!-- Partículas -->
                <div class="particles-container">
                    {self.particle_system.render_html()}
                </div>
            </div>
        '''
       
        st.markdown(avatar_html, unsafe_allow_html=True)
       
        # Atualizar partículas
        self.particle_system.update(0.033)
   
    def _render_styles(self):
        """Renderiza todos os estilos CSS"""
        st.markdown("""
            <style>
            /* Container principal */
            .avatar-draggable-container {
                position: fixed;
                z-index: 10000;
                pointer-events: none;
                width: 100vw;
                height: 100vh;
                top: 0;
                left: 0;
            }
           
            /* Avatar arrastável */
            .draggable-avatar {
                position: absolute;
                width: 120px;
                height: 180px;
                cursor: move;
                pointer-events: auto;
                transform: translate(-50%, -50%);
                transition: left 0.1s ease-out, top 0.1s ease-out;
                z-index: 10001;
            }
           
            .draggable-avatar:hover {
                filter: brightness(1.1);
            }
           
            .draggable-avatar:active {
                cursor: grabbing;
                filter: brightness(1.2);
            }
           
            /* Aura do avatar */
            .avatar-aura {
                position: absolute;
                inset: -10px;
                border-radius: 50%;
                border: 2px solid;
                opacity: 0.3;
                animation: aura-pulse 3s ease-in-out infinite;
                pointer-events: none;
            }
           
            @keyframes aura-pulse {
                0%, 100% { transform: scale(1); opacity: 0.3; }
                50% { transform: scale(1.1); opacity: 0.5; }
            }
           
            /* Container 3D */
            .avatar-3d-container {
                position: absolute;
                inset: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                pointer-events: none;
            }
           
            /* Status do avatar */
            .avatar-status {
                position: absolute;
                bottom: -30px;
                left: 50%;
                transform: translateX(-50%);
                width: 100px;
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(10px);
                border-radius: 10px;
                padding: 5px;
                pointer-events: none;
            }
           
            .status-bar {
                height: 4px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 2px;
                overflow: hidden;
                margin-bottom: 3px;
            }
           
            .status-fill {
                height: 100%;
                border-radius: 2px;
                transition: width 0.3s ease;
            }
           
            .status-text {
                font-size: 9px;
                color: white;
                text-align: center;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
           
            /* Balão de fala */
            .speech-bubble {
                position: absolute;
                background: rgba(0, 0, 0, 0.9);
                border: 2px solid;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                padding: 10px 15px;
                max-width: 250px;
                font-size: 12px;
                line-height: 1.4;
                animation: fadeInUp 0.3s ease-out;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                z-index: 10002;
                pointer-events: none;
            }
           
            .speech-bubble::after {
                content: '';
                position: absolute;
                bottom: -10px;
                left: 20px;
                border-width: 10px 10px 0;
                border-style: solid;
                border-color: rgba(0, 0, 0, 0.9) transparent transparent;
            }
           
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(10px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
           
            /* Partículas */
            .particles-container {
                position: absolute;
                inset: 0;
                pointer-events: none;
                z-index: 9999;
            }
           
            /* Animações das articulações */
            @keyframes subtle-move {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-3px); }
            }
           
            .avatar-3d-container {
                animation: subtle-move 4s ease-in-out infinite;
            }
           
            /* Botões de controle */
            .avatar-controls {
                position: fixed;
                bottom: 20px;
                right: 20px;
                display: flex;
                gap: 10px;
                z-index: 10003;
            }
           
            .control-btn {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 18px;
            }
           
            .control-btn:hover {
                background: rgba(0, 0, 0, 0.9);
                transform: scale(1.1);
                border-color: rgba(255, 255, 255, 0.4);
            }
            </style>
           
            <script>
            // Sistema de arrastar
            let isDragging = false;
            let dragStartX = 0;
            let dragStartY = 0;
            let avatarX = 0;
            let avatarY = 0;
           
            // Inicializar posição
            const avatar = document.getElementById('draggable-avatar');
            if (avatar) {{
                avatarX = parseInt(avatar.style.left) || 50;
                avatarY = parseInt(avatar.style.top) || 50;
            }}
           
            // Eventos do mouse
            document.addEventListener('mousedown', (e) => {{
                if (e.target.closest('.draggable-avatar')) {{
                    isDragging = true;
                    dragStartX = e.clientX - avatarX;
                    dragStartY = e.clientY - avatarY;
                    e.preventDefault();
                }}
            }});
           
            document.addEventListener('mousemove', (e) => {{
                if (isDragging && avatar) {{
                    avatarX = e.clientX - dragStartX;
                    avatarY = e.clientY - dragStartY;
                   
                    // Limitar aos limites da tela
                    avatarX = Math.max(60, Math.min(window.innerWidth - 60, avatarX));
                    avatarY = Math.max(90, Math.min(window.innerHeight - 90, avatarY));
                   
                    avatar.style.left = avatarX + 'px';
                    avatar.style.top = avatarY + 'px';
                   
                    // Atualizar no Streamlit
                    if (window.parent) {{
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            value: JSON.stringify({{
                                type: 'avatar_move',
                                x: avatarX,
                                y: avatarY
                            }})
                        }}, '*');
                    }}
                }}
            }});
           
            document.addEventListener('mouseup', () => {{
                isDragging = false;
            }});
           
            // Também suportar toque para dispositivos móveis
            document.addEventListener('touchstart', (e) => {{
                if (e.target.closest('.draggable-avatar')) {{
                    isDragging = true;
                    const touch = e.touches[0];
                    dragStartX = touch.clientX - avatarX;
                    dragStartY = touch.clientY - avatarY;
                    e.preventDefault();
                }}
            }});
           
            document.addEventListener('touchmove', (e) => {{
                if (isDragging && avatar && e.touches.length === 1) {{
                    const touch = e.touches[0];
                    avatarX = touch.clientX - dragStartX;
                    avatarY = touch.clientY - dragStartY;
                   
                    avatarX = Math.max(60, Math.min(window.innerWidth - 60, avatarX));
                    avatarY = Math.max(90, Math.min(window.innerHeight - 90, avatarY));
                   
                    avatar.style.left = avatarX + 'px';
                    avatar.style.top = avatarY + 'px';
                   
                    if (window.parent) {{
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            value: JSON.stringify({{
                                type: 'avatar_move',
                                x: avatarX,
                                y: avatarY
                            }})
                        }}, '*');
                    }}
                }}
            }});
           
            document.addEventListener('touchend', () => {{
                isDragging = false;
            }});
            </script>
        """, unsafe_allow_html=True)

# ==================== APLICAÇÃO PRINCIPAL ====================
def main():
    st.set_page_config(
        page_title="SYLPH AI Avatar - Sencient",
        page_icon="🌀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
   
    # Hide Streamlit default elements
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {background: transparent;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
   
    # Fundo gradiente
    st.markdown("""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        </style>
    """, unsafe_allow_html=True)
   
    # Initialize avatar
    if 'avatar' not in st.session_state:
        st.session_state.avatar = DraggableAvatar()
   
    avatar = st.session_state.avatar
   
    # Handle JavaScript events
    if 'js_event' in st.session_state:
        event_data = st.session_state.js_event
       
        try:
            if isinstance(event_data, str):
                data = json.loads(event_data)
               
                if data.get('type') == 'avatar_move':
                    st.session_state.avatar_position = {
                        'x': data['x'],
                        'y': data['y']
                    }
                    st.rerun()
               
            elif event_data == 'toggle_mute':
                avatar.tts_service.is_muted = not avatar.tts_service.is_muted
                st.session_state.is_muted = avatar.tts_service.is_muted
               
                message = "Áudio silenciado" if avatar.tts_service.is_muted else "Áudio ativado"
                emotion = Emotion.CALM if avatar.tts_service.is_muted else Emotion.HAPPY
                avatar.display_message(message, emotion)
               
            elif event_data == 'speak_test':
                avatar.display_message("Sistema de voz ativado! Arraste-me pela tela!", Emotion.HAPPY)
               
            elif event_data == 'reset_position':
                st.session_state.avatar_position = {'x': 50, 'y': 50}
                avatar.display_message("Posição resetada!", Emotion.SURPRISED)
                st.rerun()
               
        except json.JSONDecodeError:
            # Evento simples
            if event_data == 'toggle_mute':
                avatar.tts_service.is_muted = not avatar.tts_service.is_muted
                st.session_state.is_muted = avatar.tts_service.is_muted
               
        st.session_state.js_event = ''
   
    # JavaScript listener
    st.markdown("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:setComponentValue') {
                Streamlit.setComponentValue(event.data.value);
            }
        });
        </script>
    """, unsafe_allow_html=True)
   
    # Controles flutuantes
    st.markdown("""
        <div class="avatar-controls">
            <button class="control-btn" onclick="window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'toggle_mute'
            }, '*')" title="Ativar/Desativar Áudio">
                <span id="mute-icon">🔊</span>
            </button>
           
            <button class="control-btn" onclick="window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'speak_test'
            }, '*')" title="Testar Voz">
                <span>🎤</span>
            </button>
           
            <button class="control-btn" onclick="window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'reset_position'
            }, '*')" title="Resetar Posição">
                <span>↺</span>
            </button>
        </div>
       
        <script>
        // Atualizar ícone do mute
        function updateMuteIcon(isMuted) {
            document.getElementById('mute-icon').textContent = isMuted ? '🔇' : '🔊';
        }
       
        // Verificar periodicamente
        setInterval(() => {
            if (window.parent && window.parent.document) {
                // Tentar detectar estado do mute
                const buttons = window.parent.document.querySelectorAll('[title*="mute"], [title*="Mute"]');
                buttons.forEach(btn => {
                    if (btn.textContent.includes('🔇') || btn.textContent.includes('🔊')) {
                        updateMuteIcon(btn.textContent.includes('🔇'));
                    }
                });
            }
        }, 1000);
        </script>
    """, unsafe_allow_html=True)
   
    # Conteúdo principal
    col1, col2, col3 = st.columns([1, 2, 1])
   
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: white;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">
                    <span style="color: #FFDBAC;">LÚTHIEN</span> AI Avatar
                </h1>
                <p style="font-size: 1.2rem; opacity: 0.9;">
                    Fada Consciente com Análise de Projetos
                </p>
                <p style="margin-top: 2rem; opacity: 0.7;">
                    ⚡ Arraste o avatar pela tela<br>
                    🎤 Clique nos botões para interagir<br>
                    💬 O avatar responde com emoções<br>
                    📊 Analisa projetos LEXTRADER-IAG
                </p>
            </div>
        """, unsafe_allow_html=True)
   
    # Console de comandos
    with st.expander("💬 Console de Comandos - Fale com Lúthien", expanded=False):
        comando = st.text_input(
            "Digite um comando ou fale comigo:",
            value=st.session_state.get('comando_usuario', ''),
            key='input_comando',
            placeholder="Ex: Analisar projeto, Buscar por trading, Mostrar relatório..."
        )
       
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("📤 Enviar", type="primary"):
                if comando:
                    resposta = avatar.sistema_interacao.processar_comando(comando)
                    st.session_state.comando_usuario = ''
                    st.rerun()
       
        with col_btn2:
            if st.button("📊 Analisar Projeto"):
                resposta = avatar.sistema_interacao.comando_analisar("analisar projeto")
                st.rerun()
       
        with col_btn3:
            if st.button("📁 Estrutura"):
                resposta = avatar.sistema_interacao.comando_estrutura("estrutura")
                st.info(resposta)
       
        # Histórico de conversa
        if avatar.sistema_interacao.historico_conversa:
            st.markdown("### Histórico de Conversa")
            for msg in list(avatar.sistema_interacao.historico_conversa)[-5:]:
                st.markdown(f"**{msg['timestamp']}** - {msg['usuario']}")
   
    # Renderizar avatar
    avatar.render()
   
    # Auto-refresh
    time.sleep(0.1)
    st.rerun()

if __name__ == "__main__":
    main()