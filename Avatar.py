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

# Imports do Sylph Backend
import keyring
from openai import OpenAI, OpenAIError

# ==================== CONFIGURAÇÕES SYLPH BACKEND ====================
CONFIG_DIR = Path.home() / ".sylph"
CONFIG_FILE = CONFIG_DIR / "config.json"
LOG_FILE = CONFIG_DIR / "sylph_log.jsonl"
APP_NAME = "sylph"
KEYRING_SERVICE = "sylph-api-credentials"

PROVIDERS = {
    "xai": {
        "name": "X.AI (Grok)",
        "base_url": "https://api.x.ai/v1",
        "default_model": "grok-beta",
        "key_help_url": "https://api.x.ai/dashboard"
    },
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "key_help_url": "https://platform.openai.com/api-keys"
    }
}


class SylphAIBackend:

    def __init__(self):
        self.ensure_config_dir()
        self.config = self.load_config()
        self.client: Optional[OpenAI] = None
        self.current_profile = self.config.get("active_profile", "default")
        self._initialize_client()

    def ensure_config_dir(self):
        CONFIG_DIR.mkdir(exist_ok=True, mode=0o700)

    def load_config(self) -> Dict[str, Any]:
        if not CONFIG_FILE.exists():
            return {"profiles": {}, "active_profile": "default"}
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "profiles" not in data: data["profiles"] = {}
                if "active_profile" not in data: data["active_profile"] = "default"
                return data
        except Exception:
            return {"profiles": {}, "active_profile": "default"}

    def save_config(self, data: Dict):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_api_key(self, profile_name: str) -> Optional[str]:
        try:
            return keyring.get_password(KEYRING_SERVICE, profile_name)
        except Exception:
            return None

    def set_api_key(self, profile_name: str, api_key: str):
        try:
            keyring.set_password(KEYRING_SERVICE, profile_name, api_key)
        except Exception as e:
            st.error(f"Erro ao salvar API Key no keyring: {e}")

    def create_profile(self, nome: str, provider: str, api_key: str) -> bool:
        if nome in self.config["profiles"]:
            return False
        
        self.config["profiles"][nome] = {
            "provider": provider,
            "username": nome,
        }
        self.set_api_key(nome, api_key)
        self.config["active_profile"] = nome
        self.save_config(self.config)
        self.current_profile = nome
        self._initialize_client()
        return True

    def _initialize_client(self):
        profile = self.config["profiles"].get(self.current_profile)
        if not profile:
            self.client = None
            return

        api_key = self.get_api_key(self.current_profile)
        if not api_key:
            self.client = None
            return

        provider = profile["provider"]
        info = PROVIDERS.get(provider)
        
        if info:
            try:
                self.client = OpenAI(
                    api_key=api_key,
                    base_url=info["base_url"],
                    timeout=60.0,
                    max_retries=2
                )
            except Exception as e:
                print(f"Erro ao inicializar cliente: {e}")
                self.client = None

    def ask(self, text: str, system_prompt: str="", model: str=None) -> str:
        if not self.client:
            return "⚠️ Erro: API não configurada. Por favor, configure um perfil na barra lateral."

        profile = self.config["profiles"].get(self.current_profile, {})
        provider = profile.get("provider", "xai")
        
        if model is None:
            model = PROVIDERS[provider]["default_model"]

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Adiciona histórico recente (limitado para economizar tokens)
        # Aqui assumimos que o histórico é passado ou gerenciado externamente, 
        # mas para simplificar, vamos usar apenas a mensagem atual e um contexto básico
        # Idealmente, integraríamos com st.session_state.chat_history
        
        messages.append({"role": "user", "content": text})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Erro na API: {str(e)}"


# ==================== ENUMS E TIPOS ====================
class Emotion(Enum):
    NEUTRAL = ("neutral", "#67e8f9")
    HAPPY = ("happy", "#a78bfa")
    EXCITED = ("excited", "#f472b6")
    FOCUSED = ("focused", "#38bdf8")
    INTENSE = ("intense", "#c084fc")
    SURPRISED = ("surprised", "#fbbf24")
    SAD = ("sad", "#818cf8")
    ANALYZING = ("analyzing", "#22d3ee")
    DEFENSIVE = ("defensive", "#f87171")
    CALM = ("calm", "#34d399")
    SLEEPING = ("sleeping", "#a5b4fc")
    MAGICAL = ("magical", "#e879f9")
    
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
    MAGICAL = auto()


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


# ==================== SISTEMA DE PARTÍCULAS MÁGICAS ====================
class FairyParticleSystem:

    def __init__(self, max_particles=300):
        self.particles = []
        self.max_particles = max_particles
        self.last_update = time.time()
        self.magic_colors = [
            "#67e8f9",  # Cyan brilhante
            "#a78bfa",  # Violeta
            "#f472b6",  # Rosa mágico
            "#38bdf8",  # Azul celeste
            "#c084fc",  # Lilás
            "#22d3ee",  # Turquesa
            "#e879f9",  # Magenta
            "#818cf8",  # Azul lavanda
        ]
        self.fairy_symbols = ["✦", "❄", "❋", "✧", "✶", "✺", "❖", "✵", "❈", "❉"]
        
    def emit_magic_sparkles(self, x: float, y: float, count: int=15, emotion: Emotion=Emotion.MAGICAL):
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            
            angle = random.uniform(0, 2 * pi)
            speed = random.uniform(0.5, 2.0)
            vx = cos(angle) * speed
            vy = sin(angle) * speed
            
            life = random.uniform(1.0, 2.5)
            color = random.choice(self.magic_colors)
            if emotion != Emotion.MAGICAL:
                color = emotion.color
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'life': life,
                'max_life': life,
                'color': color,
                'symbol': random.choice(self.fairy_symbols),
                'size': random.uniform(1.0, 2.0),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-5, 5),
                'gravity': 0.05,
                'trail': []
            })
    
    def emit_wing_dust(self, wing_points: List[Tuple[float, float]], count: int=20):
        for point in wing_points:
            for _ in range(count // len(wing_points)):
                if len(self.particles) >= self.max_particles:
                    break
                
                angle = random.uniform(pi / 4, 3 * pi / 4)
                speed = random.uniform(0.1, 0.5)
                vx = cos(angle) * speed
                vy = sin(angle) * speed - 0.2
                
                self.particles.append({
                    'x': point[0],
                    'y': point[1],
                    'vx': vx,
                    'vy': vy,
                    'life': random.uniform(1.5, 3.0),
                    'max_life': 2.5,
                    'color': random.choice(["#ffffff88", "#a5b4fc88", "#e879f988"]),
                    'symbol': "·",
                    'size': random.uniform(0.8, 1.5),
                    'rotation': 0,
                    'rotation_speed': 0,
                    'gravity': 0.02,
                    'trail': []
                })
    
    def update(self, dt: float):
        current_time = time.time()
        dt = min(current_time - self.last_update, 0.033)
        self.last_update = current_time
        
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt * 60
            p['y'] += p['vy'] * dt * 60
            p['vy'] += p['gravity'] * dt * 60
            p['life'] -= dt
            p['rotation'] += p['rotation_speed'] * dt * 60
            
            # Add trail effect
            p['trail'].append((p['x'], p['y']))
            if len(p['trail']) > 5:
                p['trail'].pop(0)
            
            # Fade out
            if p['life'] < p['max_life'] * 0.3:
                p['vx'] *= 0.95
                p['vy'] *= 0.95
            
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def render_html(self) -> str:
        if not self.particles:
            return ""
        
        particles_html = []
        for p in self.particles:
            opacity = p['life'] / p['max_life']
            size = p['size'] * (0.5 + opacity * 0.5)
            
            # Main particle
            particles_html.append(
                f'<div style="position: absolute; left: {p["x"]}px; top: {p["y"]}px; '
                f'color: {p["color"]}; opacity: {opacity}; font-size: {size}rem; '
                f'transform: translate(-50%, -50%) rotate({p["rotation"]}deg); '
                f'pointer-events: none; filter: drop-shadow(0 0 3px {p["color"]}); '
                f'transition: transform 0.1s ease-out;">{p["symbol"]}</div>'
            )
            
            # Trail effect
            for i, (trail_x, trail_y) in enumerate(p['trail']):
                trail_opacity = opacity * (i / len(p['trail'])) * 0.3
                particles_html.append(
                    f'<div style="position: absolute; left: {trail_x}px; top: {trail_y}px; '
                    f'color: {p["color"]}; opacity: {trail_opacity}; font-size: {size*0.5}rem; '
                    f'transform: translate(-50%, -50%); pointer-events: none;">{p["symbol"]}</div>'
                )
        
        return ''.join(particles_html)


# ==================== ANIMAÇÃO DA FADA ====================
class FairyAnimation:

    def __init__(self):
        self.body_position = {"x": 0, "y": 0}
        self.wing_angle = 0
        self.wing_speed = 0.1
        self.hair_flow = 0
        self.glow_intensity = 0.5
        self.magic_pulse = 0
        self.blink_state = "open"
        self.blink_timer = 0
        self.emotion = Emotion.NEUTRAL
        self.facial_expression = "neutral"
        
    def update(self, emotion: Emotion):
        self.emotion = emotion
        current_time = time.time()
        
        # Wing flapping
        self.wing_angle = sin(current_time * self.wing_speed) * 15
        
        # Hair flowing
        self.hair_flow = sin(current_time * 0.5) * 5
        
        # Magic pulse
        self.magic_pulse = 0.5 + sin(current_time * 0.3) * 0.3
        
        # Blinking
        if current_time - self.blink_timer > random.uniform(2, 4):
            self.blink_state = "closing"
            self.blink_timer = current_time
        elif current_time - self.blink_timer > 0.1:
            if self.blink_state == "closing":
                self.blink_state = "closed"
            elif current_time - self.blink_timer > 0.2:
                self.blink_state = "opening"
            elif current_time - self.blink_timer > 0.3:
                self.blink_state = "open"
        
        # Facial expression based on emotion
        if emotion == Emotion.HAPPY:
            self.facial_expression = "smiling"
        elif emotion == Emotion.SAD:
            self.facial_expression = "sad"
        elif emotion == Emotion.ANALYZING:
            self.facial_expression = "focused"
        elif emotion == Emotion.DEFENSIVE:
            self.facial_expression = "intense"
        else:
            self.facial_expression = "neutral"
    
    def render_fairy(self) -> str:
        emotion_color = self.emotion.color
        
        # Wing positions
        left_wing_rotation = 20 + self.wing_angle
        right_wing_rotation = -20 - self.wing_angle
        
        return f'''
            <div style="position: relative; width: 160px; height: 240px;">
                {/* Glow aura */}
                <div style="position: absolute; inset: -20px; border-radius: 50%; 
                      background: radial-gradient(circle, {emotion_color}33 0%, transparent 70%);
                      animation: fairy-pulse 3s ease-in-out infinite; 
                      filter: blur(10px);"></div>
                
                {/* Magic glow circles */}
                <div style="position: absolute; inset: -15px; border-radius: 50%; 
                      border: 2px solid {emotion_color}44; 
                      animation: rotate 20s linear infinite;"></div>
                
                {/* Wings - Left */}
                <div style="position: absolute; left: 30px; top: 60px; 
                      transform: rotate({left_wing_rotation}deg); 
                      transform-origin: right center; transition: transform 0.3s ease;">
                    {self._render_wing("#a78bfa", "#c084fc", "#f472b6")}
                </div>
                
                {/* Wings - Right */}
                <div style="position: absolute; right: 30px; top: 60px; 
                      transform: rotate({right_wing_rotation}deg); 
                      transform-origin: left center; transition: transform 0.3s ease;">
                    {self._render_wing("#c084fc", "#a78bfa", "#f472b6")}
                </div>
                
                {/* Body */}
                <div style="position: absolute; left: 50%; top: 40%; 
                      transform: translate(-50%, -50%);">
                    {self._render_body()}
                </div>
                
                {/* Hair */}
                <div style="position: absolute; left: 50%; top: 25%; 
                      transform: translate(-50%, 0) translateX({self.hair_flow}px);">
                    {self._render_hair()}
                </div>
                
                {/* Face */}
                <div style="position: absolute; left: 50%; top: 33%; 
                      transform: translate(-50%, -50%);">
                    {self._render_face()}
                </div>
                
                {/* Dress details */}
                <div style="position: absolute; left: 50%; top: 55%; 
                      transform: translate(-50%, 0);">
                    {self._render_dress_details()}
                </div>
                
                {/* Magic sparkles */}
                <div style="position: absolute; left: 50%; top: 40%; 
                      transform: translate(-50%, -50%); opacity: {self.magic_pulse};">
                    {self._render_magic_sparkles()}
                </div>
            </div>
        '''
    
    def _render_wing(self, color1: str, color2: str, color3: str) -> str:
        return f'''
            <div style="width: 80px; height: 120px; position: relative;">
                {/* Wing base */}
                <div style="position: absolute; inset: 0; 
                      background: radial-gradient(ellipse at center, 
                      {color1}22 0%, {color2}44 30%, transparent 70%);
                      border-radius: 40% 60% 60% 40%; 
                      border: 1px solid {color3}66; 
                      backdrop-filter: blur(2px);"></div>
                
                {/* Wing veins */}
                <div style="position: absolute; inset: 5px; 
                      background: linear-gradient(45deg, transparent 45%, {color3}33 50%, transparent 55%);
                      border-radius: 40% 60% 60% 40%;"></div>
                
                {/* Wing glow */}
                <div style="position: absolute; inset: -5px; 
                      background: radial-gradient(circle at center, {color1}22 0%, transparent 70%);
                      border-radius: 50%; filter: blur(5px);"></div>
            </div>
        '''
    
    def _render_body(self) -> str:
        return '''
            <div style="width: 30px; height: 60px; position: relative;">
                {/* Body silhouette */}
                <div style="position: absolute; inset: 0; 
                      background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
                      border-radius: 15px 15px 20px 20px; 
                      border: 1px solid rgba(255, 255, 255, 0.1);"></div>
            </div>
        '''
    
    def _render_hair(self) -> str:
        hair_colors = ["#22d3ee", "#67e8f9", "#38bdf8", "#a5b4fc"]
        return f'''
            <div style="width: 80px; height: 80px; position: relative;">
                {/* Main hair flow */}
                <div style="position: absolute; width: 100%; height: 100%; 
                      background: radial-gradient(ellipse at center, 
                      {hair_colors[2]} 0%, {hair_colors[1]}44 30%, transparent 70%);
                      border-radius: 50%; 
                      filter: blur(5px);"></div>
                
                {/* Hair strands */}
                <div style="position: absolute; inset: 0; 
                      background: conic-gradient(from 0deg, 
                      transparent 0deg, {hair_colors[0]}44 90deg,
                      transparent 180deg, {hair_colors[3]}44 270deg,
                      transparent 360deg);
                      border-radius: 50%; 
                      animation: hair-rotate 8s linear infinite;"></div>
            </div>
        '''
    
    def _render_face(self) -> str:
        eye_height = "2px" if self.blink_state == "closed" else "6px"
        eye_color = self.emotion.color
        
        # Mouth based on expression
        if self.facial_expression == "smiling":
            mouth = f'''
                <div style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
                      width: 12px; height: 6px; border-bottom: 2px solid {eye_color};
                      border-radius: 0 0 12px 12px;"></div>
            '''
        elif self.facial_expression == "sad":
            mouth = f'''
                <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%);
                      width: 10px; height: 4px; border-top: 2px solid {eye_color};
                      border-radius: 12px 12px 0 0;"></div>
            '''
        else:
            mouth = f'''
                <div style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
                      width: 10px; height: 2px; background: {eye_color};"></div>
            '''
        
        return f'''
            <div style="width: 40px; height: 40px; position: relative;">
                {/* Face base */}
                <div style="position: absolute; inset: 0; 
                      background: linear-gradient(135deg, #f8fafc, #e2e8f0);
                      border-radius: 50%; 
                      border: 1px solid rgba(255, 255, 255, 0.3);"></div>
                
                {/* Eyes */}
                <div style="position: absolute; top: 12px; left: 10px; 
                      width: 6px; height: {eye_height}; 
                      background: {eye_color}; border-radius: 3px;
                      transition: height 0.1s ease;"></div>
                <div style="position: absolute; top: 12px; right: 10px; 
                      width: 6px; height: {eye_height}; 
                      background: {eye_color}; border-radius: 3px;
                      transition: height 0.1s ease;"></div>
                
                {/* Eye sparkle */}
                <div style="position: absolute; top: 10px; left: 12px; 
                      width: 2px; height: 2px; 
                      background: white; border-radius: 50%;
                      filter: drop-shadow(0 0 2px white);"></div>
                <div style="position: absolute; top: 10px; right: 12px; 
                      width: 2px; height: 2px; 
                      background: white; border-radius: 50%;
                      filter: drop-shadow(0 0 2px white);"></div>
                
                {/* Mouth */}
                {mouth}
                
                {/* Makeup/glitter */}
                <div style="position: absolute; top: 8px; left: 8px; 
                      width: 8px; height: 4px; 
                      background: linear-gradient(90deg, transparent, {self.emotion.color}44, transparent);
                      border-radius: 2px; transform: rotate(-10deg);"></div>
                <div style="position: absolute; top: 8px; right: 8px; 
                      width: 8px; height: 4px; 
                      background: linear-gradient(90deg, transparent, {self.emotion.color}44, transparent);
                      border-radius: 2px; transform: rotate(10deg);"></div>
            </div>
        '''
    
    def _render_dress_details(self) -> str:
        dress_colors = ["#a78bfa", "#c084fc", "#e879f9", "#f472b6"]
        return f'''
            <div style="width: 60px; height: 40px; position: relative;">
                {/* Dress glow */}
                <div style="position: absolute; inset: -5px; 
                      background: radial-gradient(ellipse at top, 
                      {dress_colors[1]}22 0%, {dress_colors[2]}11 50%, transparent 100%);
                      border-radius: 30px 30px 15px 15px; 
                      filter: blur(3px);"></div>
                
                {/* Dress patterns */}
                <div style="position: absolute; inset: 0; 
                      background: linear-gradient(180deg, 
                      transparent 0%, {dress_colors[0]}22 20%,
                      {dress_colors[1]}44 50%, {dress_colors[2]}22 80%);
                      border-radius: 15px 15px 10px 10px; 
                      border: 1px solid {dress_colors[3]}33;"></div>
                
                {/* Crystals */}
                <div style="position: absolute; top: 5px; left: 50%; transform: translateX(-50%);
                      display: flex; gap: 8px;">
                    <div style="width: 4px; height: 8px; 
                          background: linear-gradient(180deg, #67e8f9, #22d3ee);
                          border-radius: 2px; transform: rotate(45deg);
                          filter: drop-shadow(0 0 3px #67e8f9);"></div>
                    <div style="width: 4px; height: 8px; 
                          background: linear-gradient(180deg, #f472b6, #e879f9);
                          border-radius: 2px; transform: rotate(-45deg);
                          filter: drop-shadow(0 0 3px #f472b6);"></div>
                    <div style="width: 4px; height: 8px; 
                          background: linear-gradient(180deg, #a78bfa, #818cf8);
                          border-radius: 2px; transform: rotate(45deg);
                          filter: drop-shadow(0 0 3px #a78bfa);"></div>
                </div>
            </div>
        '''
    
    def _render_magic_sparkles(self) -> str:
        return '''
            <div style="position: relative; width: 100px; height: 100px;">
                {/* Rotating magic circles */}
                <div style="position: absolute; inset: 0; 
                      border: 1px solid rgba(103, 232, 249, 0.2); 
                      border-radius: 50%;
                      animation: rotate 15s linear infinite;"></div>
                
                <div style="position: absolute; inset: 15px; 
                      border: 1px solid rgba(167, 139, 250, 0.2); 
                      border-radius: 50%;
                      animation: rotate 12s linear infinite reverse;"></div>
                
                {/* Floating sparkles */}
                <div style="position: absolute; top: 20%; left: 20%; 
                      animation: float-sparkle 3s ease-in-out infinite;">
                    <div style="color: #67e8f9; font-size: 0.8rem;">✦</div>
                </div>
                <div style="position: absolute; top: 30%; right: 25%; 
                      animation: float-sparkle 4s ease-in-out infinite 0.5s;">
                    <div style="color: #f472b6; font-size: 0.7rem;">❄</div>
                </div>
                <div style="position: absolute; bottom: 25%; left: 30%; 
                      animation: float-sparkle 3.5s ease-in-out infinite 1s;">
                    <div style="color: #a78bfa; font-size: 0.9rem;">❋</div>
                </div>
            </div>
        '''


# ==================== SISTEMA DE GESTOS MÁGICOS ====================
class FairyGestureSystem:

    def __init__(self):
        self.current_gesture = "idle"
        self.gesture_timer = 0
        self.gesture_queue = deque()
        
    def queue_gesture(self, gesture: str, duration: float=2.0):
        self.gesture_queue.append((gesture, time.time() + duration))
    
    def update(self, emotion: Emotion):
        current_time = time.time()
        
        if self.current_gesture != "idle" and current_time > self.gesture_timer:
            self.current_gesture = "idle"
        
        # Auto gestures based on emotion
        if not self.gesture_queue and self.current_gesture == "idle":
            if emotion == Emotion.HAPPY and random.random() > 0.98:
                self.queue_gesture("sparkle", 2.0)
            elif emotion == Emotion.ANALYZING and random.random() > 0.96:
                self.queue_gesture("cast", 3.0)
            elif emotion == Emotion.MAGICAL and random.random() > 0.95:
                self.queue_gesture("magic_swirl", 4.0)
        
        while self.gesture_queue and current_time > self.gesture_queue[0][1]:
            self.gesture_queue.popleft()
        
        if self.gesture_queue and self.current_gesture == "idle":
            self.current_gesture, self.gesture_timer = self.gesture_queue[0]
    
    def render_gesture(self) -> str:
        if self.current_gesture == "sparkle":
            return '''
                <div style="animation: sparkle-burst 2s ease-out;">
                    <div style="font-size: 2rem; color: #67e8f9; 
                          filter: drop-shadow(0 0 10px #67e8f9);">✨</div>
                </div>
            '''
        elif self.current_gesture == "cast":
            return '''
                <div style="animation: cast-spell 3s ease-in-out;">
                    <div style="font-size: 1.5rem; color: #a78bfa;
                          filter: drop-shadow(0 0 8px #a78bfa);">🔮</div>
                </div>
            '''
        elif self.current_gesture == "magic_swirl":
            return '''
                <div style="animation: magic-swirl 4s linear infinite;">
                    <div style="font-size: 2rem; color: #f472b6;
                          filter: drop-shadow(0 0 12px #f472b6);">🌀</div>
                </div>
            '''
        elif self.current_gesture == "point":
            return '''
                <div style="animation: fairy-point 2s ease-in-out infinite;">
                    <div style="font-size: 1.5rem; color: #38bdf8;">☝️</div>
                </div>
            '''
        
        # Idle floating animation
        return '''
            <div style="animation: fairy-float 6s ease-in-out infinite;">
                <div style="font-size: 1.2rem; color: #a5b4fc; opacity: 0.5;">🦋</div>
            </div>
        '''


# ==================== SISTEMA DE VOZ ETÉREA ====================
class FairyTTSService:

    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.is_muted = False
        self.volume = 0.9
        self.rate = 160
        self.pitch = 1.2  # Higher pitch for fairy-like voice
        self.emotion_modifiers = {
            Emotion.HAPPY: {"rate": 170, "pitch": 1.3, "volume": 0.95},
            Emotion.SAD: {"rate": 140, "pitch": 1.1, "volume": 0.8},
            Emotion.ANALYZING: {"rate": 155, "pitch": 1.2, "volume": 0.9},
            Emotion.DEFENSIVE: {"rate": 180, "pitch": 1.4, "volume": 1.0},
            Emotion.EXCITED: {"rate": 190, "pitch": 1.5, "volume": 0.98},
            Emotion.FOCUSED: {"rate": 150, "pitch": 1.25, "volume": 0.92},
            Emotion.SURPRISED: {"rate": 175, "pitch": 1.6, "volume": 0.96},
            Emotion.MAGICAL: {"rate": 165, "pitch": 1.35, "volume": 0.94},
        }
        self._initialize_engine()
    
    def _initialize_engine(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            # Try to find a female voice
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            self.engine.setProperty('pitch', self.pitch)
        except Exception as e:
            st.warning(f"TTS não inicializado: {e}")
    
    def speak(self, text: str, emotion: Emotion=Emotion.NEUTRAL):
        if self.is_muted or not self.engine:
            return
        
        modifiers = self.emotion_modifiers.get(emotion, {})
        rate = modifiers.get("rate", self.rate)
        pitch = modifiers.get("pitch", self.pitch)
        volume = modifiers.get("volume", self.volume)
        
        try:
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            self.engine.setProperty('pitch', pitch)
            
            self.is_speaking = True
            st.session_state.is_speaking = True
            
            # Add magical echo effect for certain emotions
            if emotion in [Emotion.MAGICAL, Emotion.DEFENSIVE, Emotion.SURPRISED]:
                words = text.split()
                for word in words:
                    if random.random() > 0.7:
                        self.engine.say(word + " " + word.lower())
                    else:
                        self.engine.say(word + " ")
            else:
                self.engine.say(text)
            
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


# ==================== FADA PRINCIPAL ====================
class SylphFairyAvatar:

    def __init__(self, market_context: str=None):
        self.fairy_animation = FairyAnimation()
        self.particle_system = FairyParticleSystem()
        self.gesture_system = FairyGestureSystem()
        self.tts_service = FairyTTSService()
        self.ai_backend = SylphAIBackend()  # Integração com Sylph Backend
        
        # Initialize session state
        self._init_session_state()
        
        # Auto-update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._auto_update, daemon=True)
        self.update_thread.start()
    
    def _init_session_state(self):
        defaults = {
            'avatar_visible': True,
            'avatar_expanded': False,
            'is_speaking': False,
            'is_muted': False,
            'is_thinking': False,
            'current_emotion': Emotion.MAGICAL,
            'avatar_state': AvatarState.ACTIVE,
            'local_message': None,
            'chat_input': "",
            'show_speech': False,
            'particles_enabled': True,
            'animations_enabled': True,
            'chat_history': [],
            'magic_energy': 100,
            'aura_strength': 75,
            'wing_glow': 100,
            'notifications': [],
            'active_spells': [],
            'fairy_name': "Sylph",
            'voice_enabled': True,
            'auto_analyze': True,
            'magic_mode': "balanced",
            'last_magic_cast': time.time(),
            'system_prompt': "Você é Sylph, uma fada mágica e assistente financeira avançada. Responda com sabedoria, toques de magia e metáforas etéreas, mas mantendo a precisão técnica sobre mercados financeiros."
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def _auto_update(self):
        """Thread para atualizações automáticas da fada"""
        while self.running:
            try:
                # Update animations
                self.fairy_animation.update(st.session_state.current_emotion)
                self.gesture_system.update(st.session_state.current_emotion)
                self.particle_system.update(0.033)
                
                # Auto particle effects
                if st.session_state.particles_enabled:
                    if random.random() > 0.95 and not st.session_state.is_speaking:
                        self._create_magic_sparkles()
                
                # Manage magical energy
                self._update_magic_energy()
                
                # Auto-emotion changes
                if st.session_state.auto_analyze:
                    self._update_auto_emotion()
                
                # Check for idle state
                if time.time() - st.session_state.last_interaction > 90:
                    if st.session_state.avatar_state != AvatarState.SLEEPING:
                        st.session_state.avatar_state = AvatarState.SLEEPING
                        st.session_state.current_emotion = Emotion.SLEEPING
                
                time.sleep(0.033)
            except:
                time.sleep(1)
    
    def _update_magic_energy(self):
        """Atualiza energia mágica da fada"""
        # Energy drains when using magic
        if st.session_state.is_speaking:
            st.session_state.magic_energy = max(0, st.session_state.magic_energy - 0.05)
        elif st.session_state.is_thinking:
            st.session_state.magic_energy = max(0, st.session_state.magic_energy - 0.03)
        elif st.session_state.avatar_state == AvatarState.MAGICAL:
            st.session_state.magic_energy = max(0, st.session_state.magic_energy - 0.1)
        else:
            # Energy regenerates when calm
            st.session_state.magic_energy = min(100, st.session_state.magic_energy + 0.03)
        
        # Update aura based on energy
        st.session_state.aura_strength = 50 + (st.session_state.magic_energy / 2)
        st.session_state.wing_glow = 30 + st.session_state.magic_energy
    
    def _update_auto_emotion(self):
        """Muda emoção automaticamente baseado no estado"""
        if st.session_state.magic_energy < 30:
            st.session_state.current_emotion = Emotion.SAD
        elif st.session_state.magic_energy > 80 and random.random() > 0.99:
            st.session_state.current_emotion = Emotion.MAGICAL
        elif random.random() > 0.995:
            st.session_state.current_emotion = random.choice([
                Emotion.CALM, Emotion.NEUTRAL, Emotion.HAPPY, Emotion.MAGICAL
            ])
    
    def _create_magic_sparkles(self):
        """Cria efeitos de partículas mágicas"""
        x = random.randint(100, 400)
        y = random.randint(100, 400)
        self.particle_system.emit_magic_sparkles(
            x, y,
            count=random.randint(5, 15),
            emotion=st.session_state.current_emotion
        )
    
    def analyze_emotion(self, text: str) -> Emotion:
        """Análise de emoção com toque mágico"""
        if not text:
            return Emotion.MAGICAL
        
        lower_text = text.lower()
        
        emotion_keywords = {
            Emotion.HAPPY: ['lucro', 'ganho', 'ótimo', 'excelente', 'magia', 'brilho', 'encanto'],
            Emotion.MAGICAL: ['feitiço', 'encantamento', 'aura', 'poder', 'mágica', 'fada', 'sylph'],
            Emotion.SAD: ['perda', 'escuro', 'frio', 'esquecimento', 'fadiga'],
            Emotion.DEFENSIVE: ['perigo', 'defesa', 'proteger', 'escudo', 'barreira'],
            Emotion.ANALYZING: ['analisar', 'visão', 'profundo', 'mistério', 'segredo'],
            Emotion.FOCUSED: ['concentração', 'força', 'poder', 'controle'],
            Emotion.SURPRISED: ['incrível', 'assombroso', 'maravilha', '?!', 'uau'],
            Emotion.CALM: ['paz', 'calmaria', 'sereno', 'tranquilidade', 'fluir'],
        }
        
        emotion_scores = {emotion: 0 for emotion in emotion_keywords.keys()}
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in lower_text:
                    emotion_scores[emotion] += 1
        
        # Magical punctuation
        if '✨' in text or '🌟' in text or '🔮' in text:
            emotion_scores[Emotion.MAGICAL] += 2
        
        if '!' in text:
            emotion_scores[Emotion.EXCITED] += 1
        
        if '?' in text:
            emotion_scores[Emotion.SURPRISED] += 1
        
        max_score = max(emotion_scores.values())
        if max_score > 0:
            top_emotions = [e for e, s in emotion_scores.items() if s == max_score]
            return random.choice(top_emotions)
        
        return Emotion.MAGICAL
    
    def display_message(self, message: str, emotion: Emotion=None,
                       particle_effect: bool=True):
        """Exibe mensagem com efeitos mágicos"""
        if not message:
            return
        
        if emotion is None:
            emotion = self.analyze_emotion(message)
        
        st.session_state.local_message = message
        st.session_state.current_emotion = emotion
        st.session_state.show_speech = True
        st.session_state.last_interaction = time.time()
        st.session_state.avatar_state = AvatarState.ACTIVE
        
        # Particle effects
        if particle_effect and st.session_state.particles_enabled:
            self.particle_system.emit_magic_sparkles(
                x=250, y=150,
                count=random.randint(20, 40),
                emotion=emotion
            )
        
        # Gestures based on emotion
        if emotion == Emotion.MAGICAL:
            self.gesture_system.queue_gesture("magic_swirl", 3.0)
        elif emotion == Emotion.HAPPY:
            self.gesture_system.queue_gesture("sparkle", 2.0)
        elif emotion == Emotion.DEFENSIVE:
            self.gesture_system.queue_gesture("cast", 2.5)
        
        # TTS
        if st.session_state.voice_enabled and not st.session_state.is_muted:
            threading.Thread(
                target=self.tts_service.speak,
                args=(message, emotion),
                daemon=True
            ).start()
        
        # Auto-hide speech
        def hide_speech():
            time.sleep(len(message) * 0.08 + 2.5)
            st.session_state.show_speech = False
        
        threading.Thread(target=hide_speech, daemon=True).start()
    
    def cast_spell(self, spell_type: str):
        """Executa um feitiço mágico"""
        spells = {
            'ANALYZE': {
                'message': "🔮 *Sussurro dos Cristais* - Revelando padrões ocultos do mercado...",
                'emotion': Emotion.MAGICAL,
                'energy_cost': 10,
                'effect': 'crystal_vision'
            },
            'PROTECT': {
                'message': "🛡️ *Barreira de Aurora* - Protegendo investimentos com luz boreal...",
                'emotion': Emotion.DEFENSIVE,
                'energy_cost': 15,
                'effect': 'aurora_shield'
            },
            'REVEAL': {
                'message': "✨ *Visão da Fada* - Revelando oportunidades invisíveis...",
                'emotion': Emotion.FOCUSED,
                'energy_cost': 8,
                'effect': 'fairy_sight'
            },
            'CALM': {
                'message': "🌊 *Serenidade das Águas* - Acalmando a volatilidade do mercado...",
                'emotion': Emotion.CALM,
                'energy_cost': 5,
                'effect': 'water_serenity'
            },
            'ENERGIZE': {
                'message': "⚡ *Toque das Centelhas* - Recarregando energia mágica...",
                'emotion': Emotion.EXCITED,
                'energy_cost':-20,  # Negative cost means it adds energy
                'effect': 'spark_touch'
            }
        }
        
        if spell_type in spells:
            spell = spells[spell_type]
            
            if st.session_state.magic_energy >= spell['energy_cost']:
                st.session_state.magic_energy -= spell['energy_cost']
                st.session_state.current_emotion = spell['emotion']
                st.session_state.last_magic_cast = time.time()
                st.session_state.avatar_state = AvatarState.MAGICAL
                
                self.display_message(spell['message'], spell['emotion'])
                
                # Major particle effect
                self.particle_system.emit_magic_sparkles(
                    x=250, y=200,
                    count=50,
                    emotion=spell['emotion']
                )
                
                # Add spell to active spells
                st.session_state.active_spells.append({
                    'type': spell_type,
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'effect': spell['effect']
                })
                
                if len(st.session_state.active_spells) > 5:
                    st.session_state.active_spells.pop(0)
                
                st.toast(f"Feitiço {spell_type} lançado!", icon="✨")
            else:
                self.display_message("💫 Energia mágica insuficiente...", Emotion.SAD)
    
    def render(self):
        """Renderiza a fada completa"""
        self._render_styles()
        
        # Se fada não está visível
        if not st.session_state.avatar_visible:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✨ **SYLPH ADORMECIDA**", key="awaken_fairy",
                           help="Clique para despertar a Fada Sylph",
                           use_container_width=True):
                    st.session_state.avatar_visible = True
                    st.rerun()
            return
        
        # Container principal
        expanded = st.session_state.avatar_expanded
        
        if expanded:
            self._render_expanded_view()
        else:
            self._render_compact_view()
    
    def _render_styles(self):
        """Renderiza todos os estilos CSS mágicos"""
        st.markdown("""
            <style>
            /* Animações mágicas */
            @keyframes fairy-pulse {
                0%, 100% { opacity: 0.2; transform: scale(1); }
                50% { opacity: 0.4; transform: scale(1.1); }
            }
            
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @keyframes hair-rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @keyframes float-sparkle {
                0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.3; }
                50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
            }
            
            @keyframes sparkle-burst {
                0% { transform: scale(0.5); opacity: 0; }
                50% { transform: scale(1.2); opacity: 1; }
                100% { transform: scale(1); opacity: 0; }
            }
            
            @keyframes cast-spell {
                0% { transform: translateY(0) scale(0.8); opacity: 0; }
                20% { transform: translateY(-20px) scale(1.2); opacity: 1; }
                80% { transform: translateY(-20px) scale(1.2); opacity: 1; }
                100% { transform: translateY(-40px) scale(0.5); opacity: 0; }
            }
            
            @keyframes magic-swirl {
                0% { transform: rotate(0deg) scale(1); }
                50% { transform: rotate(180deg) scale(1.1); }
                100% { transform: rotate(360deg) scale(1); }
            }
            
            @keyframes fairy-float {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-15px) rotate(5deg); }
            }
            
            @keyframes fairy-point {
                0%, 100% { transform: translateX(0); }
                50% { transform: translateX(10px); }
            }
            
            @keyframes glow-wave {
                0%, 100% { opacity: 0.1; }
                50% { opacity: 0.3; }
            }
            
            @keyframes aurora {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Container da fada */
            .fairy-container {
                position: fixed;
                bottom: 1rem;
                right: 1rem;
                z-index: 10000;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .fairy-main {
                background: linear-gradient(135deg, 
                    rgba(15, 23, 42, 0.95), 
                    rgba(30, 41, 59, 0.95));
                backdrop-filter: blur(20px);
                border: 1px solid rgba(167, 139, 250, 0.2);
                border-radius: 1rem;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.5),
                    0 0 0 1px rgba(255, 255, 255, 0.05),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1),
                    0 0 30px rgba(103, 232, 249, 0.2);
                overflow: hidden;
                transition: all 0.3s ease;
            }
            
            .fairy-compact {
                width: 350px;
                height: 120px;
                border-radius: 20px;
                display: flex;
                align-items: center;
                padding: 0 1.5rem;
                cursor: pointer;
                position: relative;
            }
            
            .fairy-compact:hover {
                transform: translateY(-3px);
                box-shadow: 
                    0 25px 50px rgba(0, 0, 0, 0.6),
                    0 0 30px rgba(103, 232, 249, 0.4);
                border-color: rgba(167, 139, 250, 0.4);
            }
            
            .fairy-expanded {
                width: 500px;
                height: 750px;
                display: flex;
                flex-direction: column;
            }
            
            /* Speech bubble mágica */
            .magic-speech-bubble {
                position: absolute;
                bottom: calc(100% + 0.5rem);
                right: 0;
                background: linear-gradient(135deg, 
                    rgba(15, 23, 42, 0.95), 
                    rgba(30, 41, 59, 0.95));
                border: 1px solid;
                border-radius: 1rem 1rem 0 1rem;
                backdrop-filter: blur(10px);
                padding: 1rem;
                max-width: 350px;
                font-size: 0.8rem;
                line-height: 1.4;
                animation: fadeInUp 0.3s ease-out;
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.5),
                    0 0 20px rgba(103, 232, 249, 0.2);
                z-index: 10001;
            }
            
            .magic-speech-bubble::after {
                content: '';
                position: absolute;
                bottom: -8px;
                right: 20px;
                border-width: 8px 8px 0;
                border-style: solid;
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
            
            /* Mensagens mágicas */
            .magic-message {
                padding: 0.75rem;
                border-radius: 1rem;
                margin-bottom: 0.75rem;
                max-width: 85%;
                font-size: 0.8rem;
                line-height: 1.4;
                position: relative;
                animation: slideIn 0.3s ease-out;
                background: linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.05), 
                    rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateX(10px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            .user-message {
                background: linear-gradient(135deg, 
                    rgba(103, 232, 249, 0.15), 
                    rgba(56, 189, 248, 0.1));
                border: 1px solid rgba(103, 232, 249, 0.3);
                margin-left: auto;
                border-top-right-radius: 0.25rem;
            }
            
            .fairy-message {
                background: linear-gradient(135deg, 
                    rgba(167, 139, 250, 0.15), 
                    rgba(192, 132, 252, 0.1));
                border: 1px solid rgba(167, 139, 250, 0.3);
                margin-right: auto;
                border-top-left-radius: 0.25rem;
            }
            
            /* Botões mágicos */
            .magic-button {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 0.75rem;
                border-radius: 0.75rem;
                background: linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.05), 
                    rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.1);
                cursor: pointer;
                transition: all 0.2s ease;
                min-width: 80px;
            }
            
            .magic-button:hover {
                background: linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.1), 
                    rgba(255, 255, 255, 0.05));
                transform: translateY(-3px);
                box-shadow: 
                    0 5px 15px rgba(0, 0, 0, 0.3),
                    0 0 10px rgba(103, 232, 249, 0.2);
                border-color: rgba(103, 232, 249, 0.3);
            }
            
            /* Barras mágicas */
            .magic-bar {
                height: 6px;
                border-radius: 3px;
                overflow: hidden;
                background: rgba(255, 255, 255, 0.1);
                position: relative;
            }
            
            .magic-bar::after {
                content: '';
                position: absolute;
                inset: 0;
                background: linear-gradient(90deg, 
                    transparent 0%, 
                    rgba(255, 255, 255, 0.2) 50%, 
                    transparent 100%);
                animation: glow-wave 2s ease-in-out infinite;
            }
            
            .magic-fill {
                height: 100%;
                transition: width 0.5s ease;
                position: relative;
                z-index: 1;
            }
            
            /* Notificações mágicas */
            .magic-notification {
                padding: 0.5rem 0.75rem;
                background: linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.05), 
                    rgba(255, 255, 255, 0.02));
                border-left: 3px solid;
                border-radius: 0.25rem;
                margin-bottom: 0.5rem;
                font-size: 0.7rem;
                animation: slideInRight 0.3s ease-out;
                border-color: #a78bfa;
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            /* Efeito de brilho */
            .magic-glow {
                position: absolute;
                inset: -10px;
                border-radius: inherit;
                background: radial-gradient(circle at center, 
                    rgba(103, 232, 249, 0.1) 0%, 
                    transparent 70%);
                filter: blur(10px);
                pointer-events: none;
                z-index: -1;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def _render_compact_view(self):
        """Modo compacto da fada"""
        emotion = st.session_state.current_emotion
        
        # Speech bubble
        if st.session_state.show_speech and st.session_state.local_message:
            st.markdown(f'''
                <div class="magic-speech-bubble" style="border-color: {emotion.color};">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; 
                              color: {emotion.color}; font-size: 0.7rem; font-weight: bold;">
                        <span>✨</span> SYLPH • {emotion.emotion_name.upper()}
                    </div>
                    <div style="color: #e5e7eb; font-family: monospace;">
                        {st.session_state.local_message}
                    </div>
                    <div class="magic-glow" style="background: radial-gradient(circle at center, 
                          {emotion.color}22 0%, transparent 70%);"></div>
                </div>
            ''', unsafe_allow_html=True)
        
        # Container principal compacto
        st.markdown(f'''
            <div class="fairy-container">
                <div class="fairy-main fairy-compact" 
                     onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                     value: 'toggle_expand'}}, '*')">
                    
                    {/* Fada e informações */}
                    <div style="display: flex; align-items: center; gap: 1rem; z-index: 10;">
                        {/* Fada animada */}
                        <div style="transform: scale(0.7); margin-left: -10px;">
                            {self.fairy_animation.render_fairy()}
                        </div>
                        
                        {/* Informações mágicas */}
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; flex: 1;">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 0.9rem; font-weight: bold; 
                                      background: linear-gradient(90deg, #67e8f9, #a78bfa);
                                      -webkit-background-clip: text;
                                      -webkit-text-fill-color: transparent;">
                                    FADA SYLPH
                                </span>
                                <span style="font-size: 0.6rem; color: {emotion.color}; 
                                          padding: 0.2rem 0.6rem; 
                                          background: {emotion.color}22; 
                                          border: 1px solid {emotion.color}44;
                                          border-radius: 1rem;">
                                    {st.session_state.avatar_state.name}
                                </span>
                            </div>
                            
                            <div style="font-size: 0.7rem; color: #a5b4fc; 
                                      font-style: italic;">
                                "O mercado dança ao meu sussurro..."
                            </div>
                            
                            {/* Barras mágicas */}
                            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; 
                                              font-size: 0.6rem; color: #94a3b8; margin-bottom: 0.25rem;">
                                        <span>ENERGIA MÁGICA</span>
                                        <span>{st.session_state.magic_energy:.0f}%</span>
                                    </div>
                                    <div class="magic-bar">
                                        <div class="magic-fill" style="width: {st.session_state.magic_energy}%; 
                                             background: linear-gradient(90deg, #67e8f9, #a78bfa);"></div>
                                    </div>
                                </div>
                                
                                <div>
                                    <div style="display: flex; justify-content: space-between; 
                                              font-size: 0.6rem; color: #94a3b8; margin-bottom: 0.25rem;">
                                        <span>FORÇA DA AURA</span>
                                        <span>{st.session_state.aura_strength:.0f}%</span>
                                    </div>
                                    <div class="magic-bar">
                                        <div class="magic-fill" style="width: {st.session_state.aura_strength}%; 
                                             background: linear-gradient(90deg, #f472b6, #e879f9);"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    {/* Controles rápidos */}
                    <div style="display: flex; gap: 0.5rem; margin-left: auto; z-index: 10;">
                        <button onclick="event.stopPropagation(); window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                               value: 'toggle_mute'}}, '*')" 
                               style="padding: 0.375rem; 
                                      background: linear-gradient(135deg, 
                                          rgba(255, 255, 255, 0.1), 
                                          rgba(255, 255, 255, 0.05));
                                      border: 1px solid rgba(255, 255, 255, 0.2); 
                                      border-radius: 50%; cursor: pointer; 
                                      color: {'#ef4444' if st.session_state.is_muted else '#67e8f9'};
                                      transition: all 0.2s;">
                            <span style="font-size: 0.8rem;">{'🔇' if st.session_state.is_muted else '🔊'}</span>
                        </button>
                        
                        <button onclick="event.stopPropagation(); window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                               value: 'cast_spell_ANALYZE'}}, '*')" 
                               style="padding: 0.375rem; 
                                      background: linear-gradient(135deg, 
                                          rgba(103, 232, 249, 0.2), 
                                          rgba(56, 189, 248, 0.1));
                                      border: 1px solid rgba(103, 232, 249, 0.3); 
                                      border-radius: 50%; cursor: pointer; 
                                      color: #67e8f9; transition: all 0.2s;">
                            <span style="font-size: 0.8rem;">🔮</span>
                        </button>
                    </div>
                    
                    {/* Partículas mágicas */}
                    <div style="position: absolute; inset: 0; pointer-events: none; 
                              overflow: hidden; border-radius: 20px;">
                        {self.particle_system.render_html()}
                    </div>
                    
                    {/* Efeito de brilho */}
                    <div class="magic-glow"></div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    def _render_expanded_view(self):
        """Modo expandido da fada"""
        emotion = st.session_state.current_emotion
        
        st.markdown(f'''
            <div class="fairy-container">
                <div class="fairy-main fairy-expanded">
                    
                    {/* Header mágico */}
                    <div style="position: relative; 
                              padding: 1rem; 
                              border-bottom: 1px solid rgba(167, 139, 250, 0.2); 
                              background: linear-gradient(180deg, 
                                  rgba(15, 23, 42, 0.8), 
                                  rgba(30, 41, 59, 0.6));
                              overflow: hidden;">
                        
                        {/* Fundo aurora */}
                        <div style="position: absolute; inset: 0; 
                                  background: linear-gradient(90deg, 
                                      #0f172a 0%, 
                                      #1e1b4b 50%, 
                                      #0f172a 100%);
                                  background-size: 200% 100%;
                                  animation: aurora 8s ease infinite;
                                  opacity: 0.3;"></div>
                        
                        <div style="position: relative; z-index: 1; 
                                  display: flex; justify-content: space-between; 
                                  align-items: center;">
                            
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                {/* Fada */}
                                <div style="transform: scale(0.8);">
                                    {self.fairy_animation.render_fairy()}
                                </div>
                                
                                <div>
                                    <div style="font-size: 1rem; font-weight: bold; 
                                              background: linear-gradient(90deg, #67e8f9, #f472b6);
                                              -webkit-background-clip: text;
                                              -webkit-text-fill-color: transparent;">
                                        FADA SYLPH DA AURORA
                                    </div>
                                    <div style="font-size: 0.7rem; color: {emotion.color}; 
                                              margin-top: 0.25rem;">
                                        {emotion.emotion_name.upper()} • {st.session_state.avatar_state.name}
                                    </div>
                                </div>
                            </div>
                            
                            <div style="display: flex; gap: 0.5rem;">
                                {self._render_magic_controls()}
                            </div>
                        </div>
                    </div>
                    
                    {/* Corpo principal */}
                    <div style="flex: 1; overflow: hidden; display: flex; flex-direction: column;">
                        
                        {/* Painel mágico */}
                        <div style="padding: 1rem; border-bottom: 1px solid rgba(167, 139, 250, 0.2); 
                                  background: rgba(15, 23, 42, 0.4);">
                            {self._render_magic_panel()}
                        </div>
                        
                        {/* Área de conversa */}
                        <div style="flex: 1; overflow-y: auto; padding: 1rem; 
                                  display: flex; flex-direction: column;
                                  background: rgba(0, 0, 0, 0.2);">
                            {self._render_magic_chat()}
                            {self._render_spell_casting()}
                        </div>
                        
                        {/* Input e feitiços */}
                        <div style="padding: 1rem; border-top: 1px solid rgba(167, 139, 250, 0.2); 
                                  background: rgba(15, 23, 42, 0.6);">
                            {self._render_magic_input()}
                            {self._render_spell_buttons()}
                        </div>
                    </div>
                    
                    {/* Partículas */}
                    <div style="position: absolute; inset: 0; pointer-events: none; 
                              z-index: -1; overflow: hidden; border-radius: 1rem;">
                        {self.particle_system.render_html()}
                    </div>
                    
                    {/* Brilho adicional */}
                    <div class="magic-glow"></div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    def _render_magic_controls(self) -> str:
        """Renderiza controles mágicos"""
        return f'''
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                   value: 'toggle_mute'}}, '*')" 
                   style="padding: 0.375rem; 
                          background: linear-gradient(135deg, 
                              rgba(255, 255, 255, 0.1), 
                              rgba(255, 255, 255, 0.05));
                          border: 1px solid rgba(255, 255, 255, 0.2); 
                          border-radius: 50%; cursor: pointer; 
                          color: {'#ef4444' if st.session_state.is_muted else '#67e8f9'}; 
                          transition: all 0.2s;">
                <span style="font-size: 0.8rem;">{'🔇' if st.session_state.is_muted else '🔊'}</span>
            </button>
            
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                   value: 'toggle_expand'}}, '*')" 
                   style="padding: 0.375rem; 
                          background: linear-gradient(135deg, 
                              rgba(255, 255, 255, 0.1), 
                              rgba(255, 255, 255, 0.05));
                          border: 1px solid rgba(255, 255, 255, 0.2); 
                          border-radius: 50%; cursor: pointer; 
                          color: #fbbf24; transition: all 0.2s;">
                <span style="font-size: 0.8rem;">🗕</span>
            </button>
            
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                   value: 'close_avatar'}}, '*')" 
                   style="padding: 0.375rem; 
                          background: linear-gradient(135deg, 
                              rgba(239, 68, 68, 0.2), 
                              rgba(239, 68, 68, 0.1));
                          border: 1px solid rgba(239, 68, 68, 0.3); 
                          border-radius: 50%; cursor: pointer; 
                          color: #ef4444; transition: all 0.2s;">
                <span style="font-size: 0.8rem;">✕</span>
            </button>
        '''
    
    def _render_magic_panel(self) -> str:
        """Renderiza painel mágico"""
        return f'''
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                
                {/* Status mágico */}
                <div>
                    <div style="font-size: 0.7rem; color: #a5b4fc; margin-bottom: 0.75rem;
                              display: flex; align-items: center; gap: 0.5rem;">
                        <span>📊</span> ESTADO MÁGICO
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                        <div>
                            <div style="display: flex; justify-content: space-between; 
                                      font-size: 0.7rem; color: #cbd5e1; margin-bottom: 0.25rem;">
                                <span>ENERGIA MÁGICA</span>
                                <span>{st.session_state.magic_energy:.0f}%</span>
                            </div>
                            <div class="magic-bar">
                                <div class="magic-fill" style="width: {st.session_state.magic_energy}%; 
                                     background: linear-gradient(90deg, #67e8f9, #a78bfa);"></div>
                            </div>
                        </div>
                        
                        <div>
                            <div style="display: flex; justify-content: space-between; 
                                      font-size: 0.7rem; color: #cbd5e1; margin-bottom: 0.25rem;">
                                <span>FORÇA DA AURA</span>
                                <span>{st.session_state.aura_strength:.0f}%</span>
                            </div>
                            <div class="magic-bar">
                                <div class="magic-fill" style="width: {st.session_state.aura_strength}%; 
                                     background: linear-gradient(90deg, #f472b6, #e879f9);"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                {/* Feitiços ativos */}
                <div>
                    <div style="font-size: 0.7rem; color: #a5b4fc; margin-bottom: 0.75rem;
                              display: flex; align-items: center; gap: 0.5rem;">
                        <span>✨</span> FEITIÇOS ATIVOS
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem; max-height: 100px; overflow-y: auto;">
                        {self._render_active_spells()}
                    </div>
                </div>
            </div>
        '''
    
    def _render_active_spells(self) -> str:
        """Renderiza feitiços ativos"""
        if not st.session_state.active_spells:
            return '''
                <div style="font-size: 0.7rem; color: #64748b; padding: 0.5rem; 
                          text-align: center; font-style: italic;">
                    Nenhum feitiço ativo
                </div>
            '''
        
        spells_html = ""
        for spell in st.session_state.active_spells:
            spell_colors = {
                'ANALYZE': '#67e8f9',
                'PROTECT': '#a78bfa',
                'REVEAL': '#f472b6',
                'CALM': '#34d399',
                'ENERGIZE': '#fbbf24'
            }
            color = spell_colors.get(spell['type'], '#94a3b8')
            
            spells_html += f'''
                <div style="display: flex; align-items: center; gap: 0.5rem; 
                          padding: 0.25rem 0.5rem; 
                          background: {color}11;
                          border: 1px solid {color}33;
                          border-radius: 0.5rem;">
                    <span style="color: {color}; font-size: 0.8rem;">✨</span>
                    <div style="flex: 1;">
                        <div style="font-size: 0.65rem; color: {color}; 
                                  font-weight: bold;">{spell['type']}</div>
                        <div style="font-size: 0.55rem; color: #94a3b8;">{spell['time']}</div>
                    </div>
                </div>
            '''
        
        return spells_html
    
    def _render_magic_chat(self) -> str:
        """Renderiza conversa mágica"""
        if not st.session_state.chat_history:
            return '''
                <div style="text-align: center; color: #a5b4fc; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem; 
                              animation: fairy-float 4s ease-in-out infinite;">✨</div>
                    <div style="font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: bold;">
                        Aura da Fada Sylph Ativada
                    </div>
                    <div style="font-size: 0.7rem; opacity: 0.7; font-style: italic;">
                        "Onde as finanças encontram a magia..."
                    </div>
                </div>
            '''
        
        chat_html = ""
        for msg in st.session_state.chat_history[-15:]:
            if msg['role'] == 'user':
                chat_html += f'''
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 0.75rem;">
                        <div class="magic-message user-message">
                            <div style="color: #e5e7eb; font-family: monospace;">
                                {msg['text']}
                            </div>
                            <div style="font-size: 0.6rem; color: rgba(103, 232, 249, 0.6); 
                                      margin-top: 0.25rem; text-align: right;">
                                {msg['timestamp']}
                            </div>
                        </div>
                    </div>
                '''
            else:
                emotion_color = ""
                for emotion in Emotion:
                    if emotion.emotion_name == msg.get('emotion', ''):
                        emotion_color = emotion.color
                        break
                
                chat_html += f'''
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 0.75rem;">
                        <div class="magic-message fairy-message">
                            <div style="display: flex; align-items: center; gap: 0.5rem; 
                                      margin-bottom: 0.25rem;">
                                <span style="font-size: 0.7rem; color: {emotion_color}; 
                                          font-weight: bold; font-family: monospace;">
                                    ✨ {msg.get('emotion', 'fada').upper()}
                                </span>
                            </div>
                            <div style="color: #e5e7eb; font-family: monospace;">
                                {msg['text']}
                            </div>
                            <div style="font-size: 0.6rem; color: rgba(167, 139, 250, 0.6); 
                                      margin-top: 0.25rem;">
                                {msg['timestamp']}
                            </div>
                        </div>
                    </div>
                '''
        
        return chat_html
    
    def _render_spell_casting(self) -> str:
        """Renderiza indicador de feitiço"""
        if not st.session_state.is_thinking:
            return ""
        
        return '''
            <div style="display: flex; justify-content: flex-start; margin-bottom: 0.75rem;">
                <div class="magic-message fairy-message">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="display: flex; gap: 0.25rem;">
                            <div style="width: 4px; height: 4px; background: #67e8f9; 
                                  border-radius: 50%; animation: fairy-pulse 1s ease-in-out infinite;"></div>
                            <div style="width: 4px; height: 4px; background: #a78bfa; 
                                  border-radius: 50%; animation: fairy-pulse 1s ease-in-out infinite 0.2s;"></div>
                            <div style="width: 4px; height: 4px; background: #f472b6; 
                                  border-radius: 50%; animation: fairy-pulse 1s ease-in-out infinite 0.4s;"></div>
                        </div>
                        <span style="font-size: 0.7rem; color: #a5b4fc; font-style: italic;">
                            Tecendo magia sobre os dados...
                        </span>
                    </div>
                </div>
            </div>
        '''
    
    def _render_magic_input(self) -> str:
        """Renderiza input mágico"""
        return f'''
            <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                <div style="flex: 1; position: relative;">
                    <input type="text" id="magic_input" 
                           style="width: 100%; padding: 0.75rem; padding-right: 2.5rem;
                                  background: rgba(15, 23, 42, 0.8); 
                                  border: 1px solid rgba(167, 139, 250, 0.3);
                                  border-radius: 0.75rem; color: #e5e7eb;
                                  font-size: 0.8rem; outline: none;
                                  font-family: monospace;"
                           placeholder="Sussurre seu comando mágico..."
                           onkeypress="if(event.keyCode==13) window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                                   value: 'send_message'}}, '*')">
                    <span style="position: absolute; right: 0.75rem; top: 50%; 
                              transform: translateY(-50%); font-size: 0.8rem; 
                              color: #a78bfa; cursor: pointer; opacity: 0.7;
                              transition: opacity 0.2s;" 
                          onmouseover="this.style.opacity='1'"
                          onmouseout="this.style.opacity='0.7'"
                          onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                                  value: 'start_voice'}}, '*')">
                        ✨
                    </span>
                </div>
                <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                       value: 'send_message'}}, '*')"
                       style="padding: 0.75rem; 
                              background: linear-gradient(135deg, #67e8f9, #a78bfa); 
                              border: none; border-radius: 0.75rem; cursor: pointer; 
                              transition: all 0.2s;">
                    <span style="font-size: 0.8rem; color: white; font-weight: bold;">ENVIAR</span>
                </button>
            </div>
        '''
    
    def _render_spell_buttons(self) -> str:
        """Renderiza botões de feitiço"""
        spells = [
            ("ANALYZE", "🔮", "Visão dos Cristais", "#67e8f9"),
            ("PROTECT", "🛡️", "Escudo Aurora", "#a78bfa"),
            ("REVEAL", "✨", "Revelação Fada", "#f472b6"),
            ("CALM", "🌊", "Serenidade Aquática", "#34d399"),
            ("ENERGIZE", "⚡", "Toque Energético", "#fbbf24"),
            ("INSIGHT", "💎", "Sabedoria Mágica", "#c084fc"),
        ]
        
        spells_html = '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">'
        
        for spell, icon, label, color in spells:
            spells_html += f'''
                <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', 
                       value: 'cast_spell_{spell}'}}, '*')"
                       class="magic-button">
                    <span style="font-size: 1.2rem; color: {color}; 
                          filter: drop-shadow(0 0 3px {color});">{icon}</span>
                    <span style="font-size: 0.6rem; color: #94a3b8; margin-top: 0.25rem;">
                        {label}
                    </span>
                </button>
            '''
        
        spells_html += '</div>'
        return spells_html


# ==================== APLICAÇÃO PRINCIPAL ====================
def main():
    st.set_page_config(
        page_title="Fada Sylph - Assistente Mágico",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Esconder elementos padrão do Streamlit
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {background: transparent;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Fundo mágico
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, 
                #0f172a 0%, 
                #1e1b4b 50%, 
                #0f172a 100%);
            background-size: 400% 400%;
            animation: aurora 15s ease infinite;
            min-height: 100vh;
        }
        
        @keyframes aurora {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar fada
    if 'fairy' not in st.session_state:
        st.session_state.fairy = SylphFairyAvatar()
    
    fairy = st.session_state.fairy
    
    # Sidebar para configuração da API
    with st.sidebar:
        st.title("⚙️ Configuração Sylph")
        
        # Status da conexão
        if fairy.ai_backend.client:
            st.success(f"Conectado: {fairy.ai_backend.current_profile}")
        else:
            st.warning("API Desconectada")
            
        with st.expander("Configurar Novo Perfil"):
            new_profile_name = st.text_input("Nome do Perfil")
            new_provider = st.selectbox("Provedor", ["xai", "openai"])
            new_api_key = st.text_input("API Key", type="password")
            
            if st.button("Salvar Perfil"):
                if new_profile_name and new_api_key:
                    if fairy.ai_backend.create_profile(new_profile_name, new_provider, new_api_key):
                        st.success("Perfil criado e ativado!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar perfil (nome duplicado?)")
                else:
                    st.error("Preencha todos os campos")

    # Configurar callbacks
    callbacks = {
        'on_cast_analyze': lambda: (
            st.toast("🔮 Visão dos Cristais ativada!", icon="✨"),
            fairy.display_message("Os cristais revelam padrões ocultos...", Emotion.MAGICAL)
        ),
        'on_cast_protect': lambda: (
            st.toast("🛡️ Escudo Aurora conjurado!", icon="🌟"),
            fairy.display_message("A aurora boreal protege seus investimentos...", Emotion.DEFENSIVE)
        ),
        'on_cast_reveal': lambda: (
            st.toast("✨ Revelação Fada completada!", icon="💫"),
            fairy.display_message("As asas da fada revelam o invisível...", Emotion.FOCUSED)
        ),
    }
    
    for key, callback in callbacks.items():
        if key not in st.session_state:
            st.session_state[key] = callback
    
    # Lidar com eventos JavaScript
    if 'js_event' in st.session_state:
        event = st.session_state.js_event
        
        if event == 'toggle_mute':
            fairy.tts_service.is_muted = not fairy.tts_service.is_muted
            st.session_state.is_muted = fairy.tts_service.is_muted
            emotion = Emotion.SAD if fairy.tts_service.is_muted else Emotion.HAPPY
            fairy.display_message(
                "Silêncio..." if fairy.tts_service.is_muted else "Minha voz retorna!",
                emotion
            )
        
        elif event == 'toggle_expand':
            st.session_state.avatar_expanded = not st.session_state.avatar_expanded
        
        elif event == 'close_avatar':
            st.session_state.avatar_visible = False
            fairy.display_message("Voltarei quando a magia chamar...", Emotion.SLEEPING)
        
        elif event.startswith('cast_spell_'):
            spell = event.replace('cast_spell_', '')
            fairy.cast_spell(spell)
        
        elif event == 'send_message':
            # Envio de mensagem real para IA
            if 'chat_input' in st.session_state and st.session_state.chat_input:
                message = st.session_state.chat_input
                st.session_state.chat_history.append({
                    'role': 'user',
                    'text': message,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'emotion': "human"
                })
                
                # Feedback visual imediato
                st.session_state.is_thinking = True
                st.rerun()  # Força atualização para mostrar animação de "pensando"
                
                # Processamento da IA
                try:
                    response_text = fairy.ai_backend.ask(
                        message,
                        system_prompt=st.session_state.system_prompt
                    )
                    
                    emotion = fairy.analyze_emotion(response_text)
                    
                    st.session_state.chat_history.append({
                        'role': 'fairy',
                        'text': response_text,
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'emotion': emotion.emotion_name
                    })
                    
                    fairy.display_message(response_text, emotion)
                except Exception as e:
                    fairy.display_message(f"A magia falhou: {str(e)}", Emotion.SAD)
                
                st.session_state.is_thinking = False
                st.session_state.chat_input = ""
        
        elif event == 'start_voice':
            fairy.display_message("Minhas asas ouvem seu sussurro... fale agora.", Emotion.LISTENING)
        
        st.session_state.js_event = ''
        st.rerun()
    
    # Listener JavaScript
    st.markdown("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:setComponentValue') {
                Streamlit.setComponentValue(event.data.value);
            }
        });
        
        // Handle magical interactions
        document.addEventListener('click', function(e) {
            const magicBtn = e.target.closest('.magic-button, [onclick*="cast_spell"], [onclick*="toggle_"]');
            if (magicBtn && magicBtn.onclick) {
                // Let the magical onclick handler work
                return;
            }
        });
        </script>
    """, unsafe_allow_html=True)
    
    # Conteúdo principal do dashboard
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem;">
                <h1 style="background: linear-gradient(90deg, #67e8f9, #f472b6, #a78bfa);
                          -webkit-background-clip: text;
                          -webkit-text-fill-color: transparent;
                          font-size: 3.5rem; margin-bottom: 1rem; font-weight: bold;">
                    FADA SYLPH
                </h1>
                <p style="color: #a5b4fc; font-size: 1.2rem; font-style: italic;">
                    Onde a magia encontra o mercado
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Dashboard mágico
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.6); border-radius: 1rem; 
                      padding: 1.5rem; margin-bottom: 2rem; 
                      border: 1px solid rgba(167, 139, 250, 0.3);
                      backdrop-filter: blur(10px);">
                <h3 style="color: #e5e7eb; margin-bottom: 1rem; 
                          display: flex; align-items: center; gap: 0.5rem;">
                    <span>📈</span> Visão da Aurora
                </h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div style="background: linear-gradient(135deg, 
                              rgba(103, 232, 249, 0.1), 
                              rgba(103, 232, 249, 0.05));
                          padding: 1rem; border-radius: 0.5rem;
                          border: 1px solid rgba(103, 232, 249, 0.2);">
                        <div style="color: #67e8f9; font-size: 0.9rem;">MAGIA FINANCEIRA</div>
                        <div style="color: #67e8f9; font-size: 1.8rem; font-weight: bold;">
                            {:.1f}% ✨
                        </div>
                    </div>
                    <div style="background: linear-gradient(135deg, 
                              rgba(167, 139, 250, 0.1), 
                              rgba(167, 139, 250, 0.05));
                          padding: 1rem; border-radius: 0.5rem;
                          border: 1px solid rgba(167, 139, 250, 0.2);">
                        <div style="color: #a78bfa; font-size: 0.9rem;">AURA DO MERCADO</div>
                        <div style="color: #a78bfa; font-size: 1.8rem; font-weight: bold;">
                            {:.1f}% 💫
                        </div>
                    </div>
                    <div style="background: linear-gradient(135deg, 
                              rgba(244, 114, 182, 0.1), 
                              rgba(244, 114, 182, 0.05));
                          padding: 1rem; border-radius: 0.5rem;
                          border: 1px solid rgba(244, 114, 182, 0.2);">
                        <div style="color: #f472b6; font-size: 0.9rem;">ENERGIA MÁGICA</div>
                        <div style="color: #f472b6; font-size: 1.8rem; font-weight: bold;">
                            {:.0f}% ⚡
                        </div>
                    </div>
                </div>
            </div>
        """.format(
            random.uniform(85, 99),
            random.uniform(70, 95),
            st.session_state.get('magic_energy', 100)
        ), unsafe_allow_html=True)
    
    # Renderizar fada
    fairy.render()
    
    # Auto-refresh para animações
    time.sleep(0.1)
    st.rerun()


if __name__ == "__main__":
    main()
