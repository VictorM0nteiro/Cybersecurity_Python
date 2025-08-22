import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
import math
import random
import time
import json
import threading
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
from enum import Enum
from PIL import ImageGrab

class ParticleType(Enum):
    NORMAL = "normal"
    HEAVY = "heavy"
    LIGHT = "light"
    BOUNCY = "bouncy"
    STICKY = "sticky"
    MAGNETIC = "magnetic"
    EXPLOSIVE = "explosive"

class ForceType(Enum):
    GRAVITY = "gravity"
    WIND = "wind"
    MAGNETIC = "magnetic"
    ELECTRIC = "electric"
    VORTEX = "vortex"

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    size: float
    mass: float
    color: str
    particle_type: ParticleType
    trail: List[Tuple[float, float]]
    energy: float = 100.0
    charge: float = 0.0
    temperature: float = 20.0
    age: float = 0.0
    max_age: float = float('inf')
    is_selected: bool = False

class GravityField:
    def __init__(self, x: float, y: float, strength: float, radius: float):
        self.x = x
        self.y = y
        self.strength = strength
        self.radius = radius
        self.active = True

class AdvancedGravitySimulation:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulação Avançada de Gravidade e Física")
        self.master.geometry("1400x900")
        self.master.configure(bg='#1a1a1a')
        
        # Configurações físicas avançadas
        self.gravity = 0.5
        self.bounce_damping = 0.8
        self.air_resistance = 0.999
        self.collision_enabled = True
        self.particle_interaction = True
        self.temperature_effects = True
        self.aging_enabled = True
        self.max_particles = 1000
        
        # Forças ambientais
        self.wind_x = 0.0
        self.wind_y = 0.0
        self.magnetic_field = 0.0
        self.electric_field = 0.0
        
        # Listas de objetos
        self.particles: List[Particle] = []
        self.gravity_fields: List[GravityField] = []
        self.selected_particles: List[Particle] = []
        
        # Estado da simulação
        self.running = True
        self.show_trails = True
        self.show_vectors = False
        self.show_energy = False
        self.show_temperature = False
        self.show_grid = False
        self.collision_mode = "elastic"
        self.current_particle_type = ParticleType.NORMAL
        self.simulation_speed = 1.0
        
        # Estatísticas
        self.total_energy = 0.0
        self.total_momentum = 0.0
        self.fps = 0
        self.frame_count = 0
        self.last_fps_time = time.time()
        
        # Interface
        self.setup_ui()
        
        # Eventos
        self.setup_events()
        
        # Iniciar com algumas partículas
        self.create_demo_scene()
        
        # Loop de animação
        self.last_time = time.time()
        self.animate()
    
    def setup_ui(self):
        """Configura a interface completa"""
        # Frame principal
        main_frame = tk.Frame(self.master, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame esquerdo (controles)
        self.left_frame = tk.Frame(main_frame, bg='#2a2a2a', width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        self.left_frame.pack_propagate(False)
        
        # Canvas central
        canvas_frame = tk.Frame(main_frame, bg='#1a1a1a')
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#0a0a0a', highlightthickness=2, 
                               highlightbackground='#444444')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame direito (informações)
        self.right_frame = tk.Frame(main_frame, bg='#2a2a2a', width=250)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.right_frame.pack_propagate(False)
        
        # Configurar painéis
        self.setup_control_panel()
        self.setup_info_panel()
        
    def setup_control_panel(self):
        """Configura o painel de controles"""
        # Título
        title = tk.Label(self.left_frame, text="CONTROLES DE SIMULAÇÃO", 
                        font=('Arial', 12, 'bold'), fg='white', bg='#2a2a2a')
        title.pack(pady=10)
        
        # Notebook para organizar controles
        notebook = ttk.Notebook(self.left_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba Física
        physics_frame = ttk.Frame(notebook)
        notebook.add(physics_frame, text="Física")
        self.setup_physics_controls(physics_frame)
        
        # Aba Partículas
        particles_frame = ttk.Frame(notebook)
        notebook.add(particles_frame, text="Partículas")
        self.setup_particle_controls(particles_frame)
        
        # Aba Forças
        forces_frame = ttk.Frame(notebook)
        notebook.add(forces_frame, text="Forças")
        self.setup_forces_controls(forces_frame)
        
        # Aba Visual
        visual_frame = ttk.Frame(notebook)
        notebook.add(visual_frame, text="Visual")
        self.setup_visual_controls(visual_frame)
        
        # Aba Arquivo
        file_frame = ttk.Frame(notebook)
        notebook.add(file_frame, text="Arquivo")
        self.setup_file_controls(file_frame)
    
    def setup_physics_controls(self, parent):
        """Controles de física"""
        # Gravidade
        tk.Label(parent, text="Gravidade:").pack(anchor='w', padx=5, pady=(10,0))
        self.gravity_var = tk.DoubleVar(value=self.gravity)
        gravity_scale = tk.Scale(parent, from_=-2, to=5, resolution=0.1, orient=tk.HORIZONTAL,
                               variable=self.gravity_var, command=self.update_gravity)
        gravity_scale.pack(fill='x', padx=5)
        
        # Resistência do ar
        tk.Label(parent, text="Resistência do Ar:").pack(anchor='w', padx=5, pady=(10,0))
        self.air_var = tk.DoubleVar(value=self.air_resistance)
        air_scale = tk.Scale(parent, from_=0.9, to=1.0, resolution=0.001, orient=tk.HORIZONTAL,
                           variable=self.air_var, command=self.update_air_resistance)
        air_scale.pack(fill='x', padx=5)
        
        # Amortecimento
        tk.Label(parent, text="Amortecimento:").pack(anchor='w', padx=5, pady=(10,0))
        self.damping_var = tk.DoubleVar(value=self.bounce_damping)
        damping_scale = tk.Scale(parent, from_=0, to=1, resolution=0.05, orient=tk.HORIZONTAL,
                               variable=self.damping_var, command=self.update_damping)
        damping_scale.pack(fill='x', padx=5)
        
        # Velocidade da simulação
        tk.Label(parent, text="Velocidade:").pack(anchor='w', padx=5, pady=(10,0))
        self.speed_var = tk.DoubleVar(value=self.simulation_speed)
        speed_scale = tk.Scale(parent, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,
                             variable=self.speed_var, command=self.update_speed)
        speed_scale.pack(fill='x', padx=5)
        
        # Checkboxes
        self.collision_var = tk.BooleanVar(value=self.collision_enabled)
        tk.Checkbutton(parent, text="Colisões Habilitadas", variable=self.collision_var,
                      command=self.toggle_collisions).pack(anchor='w', padx=5, pady=5)
        
        self.interaction_var = tk.BooleanVar(value=self.particle_interaction)
        tk.Checkbutton(parent, text="Interação entre Partículas", variable=self.interaction_var,
                      command=self.toggle_interaction).pack(anchor='w', padx=5)
        
        self.temperature_var = tk.BooleanVar(value=self.temperature_effects)
        tk.Checkbutton(parent, text="Efeitos de Temperatura", variable=self.temperature_var,
                      command=self.toggle_temperature).pack(anchor='w', padx=5)
        
        self.aging_var = tk.BooleanVar(value=self.aging_enabled)
        tk.Checkbutton(parent, text="Envelhecimento", variable=self.aging_var,
                      command=self.toggle_aging).pack(anchor='w', padx=5)
    
    def setup_particle_controls(self, parent):
        """Controles de partículas"""
        # Tipo de partícula
        tk.Label(parent, text="Tipo de Partícula:").pack(anchor='w', padx=5, pady=(10,0))
        self.particle_type_var = tk.StringVar(value=ParticleType.NORMAL.value)
        type_combo = ttk.Combobox(parent, textvariable=self.particle_type_var,
                                 values=[t.value for t in ParticleType], state='readonly')
        type_combo.pack(fill='x', padx=5, pady=5)
        type_combo.bind('<<ComboboxSelected>>', self.change_particle_type)
        
        # Botões de ação
        button_frame = tk.Frame(parent)
        button_frame.pack(fill='x', padx=5, pady=10)
        
        tk.Button(button_frame, text="Pausar/Continuar", command=self.toggle_simulation,
                 bg='#4CAF50', fg='white').pack(fill='x', pady=2)
        
        tk.Button(button_frame, text="Limpar Tudo", command=self.clear_all,
                 bg='#f44336', fg='white').pack(fill='x', pady=2)
        
        tk.Button(button_frame, text="Explodir Selecionadas", command=self.explode_selected,
                 bg='#FF9800', fg='white').pack(fill='x', pady=2)
        
        tk.Button(button_frame, text="Criar Cena Demo", command=self.create_demo_scene,
                 bg='#2196F3', fg='white').pack(fill='x', pady=2)
        
        # Configurações de criação
        tk.Label(parent, text="Configurações:").pack(anchor='w', padx=5, pady=(10,0))
        
        # Tamanho das partículas
        tk.Label(parent, text="Tamanho Base:").pack(anchor='w', padx=5)
        self.size_var = tk.DoubleVar(value=10)
        size_scale = tk.Scale(parent, from_=2, to=50, orient=tk.HORIZONTAL,
                            variable=self.size_var)
        size_scale.pack(fill='x', padx=5)
        
        # Velocidade inicial
        tk.Label(parent, text="Velocidade Inicial:").pack(anchor='w', padx=5)
        self.initial_speed_var = tk.DoubleVar(value=5)
        speed_scale = tk.Scale(parent, from_=0, to=20, orient=tk.HORIZONTAL,
                             variable=self.initial_speed_var)
        speed_scale.pack(fill='x', padx=5)
        
        # Contador de partículas
        self.particle_count_label = tk.Label(parent, text="Partículas: 0")
        self.particle_count_label.pack(anchor='w', padx=5, pady=5)
    
    def setup_forces_controls(self, parent):
        """Controles de forças ambientais"""
        # Vento
        tk.Label(parent, text="Vento X:").pack(anchor='w', padx=5, pady=(10,0))
        self.wind_x_var = tk.DoubleVar(value=self.wind_x)
        wind_x_scale = tk.Scale(parent, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL,
                              variable=self.wind_x_var, command=self.update_wind_x)
        wind_x_scale.pack(fill='x', padx=5)
        
        tk.Label(parent, text="Vento Y:").pack(anchor='w', padx=5)
        self.wind_y_var = tk.DoubleVar(value=self.wind_y)
        wind_y_scale = tk.Scale(parent, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL,
                              variable=self.wind_y_var, command=self.update_wind_y)
        wind_y_scale.pack(fill='x', padx=5)
        
        # Campo magnético
        tk.Label(parent, text="Campo Magnético:").pack(anchor='w', padx=5, pady=(10,0))
        self.magnetic_var = tk.DoubleVar(value=self.magnetic_field)
        magnetic_scale = tk.Scale(parent, from_=-2, to=2, resolution=0.1, orient=tk.HORIZONTAL,
                                variable=self.magnetic_var, command=self.update_magnetic)
        magnetic_scale.pack(fill='x', padx=5)
        
        # Campo elétrico
        tk.Label(parent, text="Campo Elétrico:").pack(anchor='w', padx=5)
        self.electric_var = tk.DoubleVar(value=self.electric_field)
        electric_scale = tk.Scale(parent, from_=-2, to=2, resolution=0.1, orient=tk.HORIZONTAL,
                                variable=self.electric_var, command=self.update_electric)
        electric_scale.pack(fill='x', padx=5)
        
        # Botões de campo gravitacional
        tk.Button(parent, text="Modo Campo Gravitacional", 
                 command=self.toggle_gravity_field_mode,
                 bg='#9C27B0', fg='white').pack(fill='x', padx=5, pady=(10,2))
        
        tk.Button(parent, text="Limpar Campos", command=self.clear_gravity_fields,
                 bg='#795548', fg='white').pack(fill='x', padx=5, pady=2)
        
        # Presets de força
        tk.Label(parent, text="Presets:").pack(anchor='w', padx=5, pady=(10,0))
        preset_frame = tk.Frame(parent)
        preset_frame.pack(fill='x', padx=5)
        
        tk.Button(preset_frame, text="Zero G", command=lambda: self.apply_force_preset("zero_g"),
                 bg='#607D8B', fg='white', font=('Arial', 8)).pack(side='left', fill='x', expand=True, padx=1)
        tk.Button(preset_frame, text="Tornado", command=lambda: self.apply_force_preset("tornado"),
                 bg='#795548', fg='white', font=('Arial', 8)).pack(side='left', fill='x', expand=True, padx=1)
        tk.Button(preset_frame, text="Tempestade", command=lambda: self.apply_force_preset("storm"),
                 bg='#37474F', fg='white', font=('Arial', 8)).pack(side='left', fill='x', expand=True, padx=1)
    
    def setup_visual_controls(self, parent):
        """Controles visuais"""
        # Opções de visualização
        self.trails_var = tk.BooleanVar(value=self.show_trails)
        tk.Checkbutton(parent, text="Mostrar Rastros", variable=self.trails_var,
                      command=self.toggle_trails).pack(anchor='w', padx=5, pady=(10,0))
        
        self.vectors_var = tk.BooleanVar(value=self.show_vectors)
        tk.Checkbutton(parent, text="Mostrar Vetores de Velocidade", variable=self.vectors_var,
                      command=self.toggle_vectors).pack(anchor='w', padx=5)
        
        self.energy_var = tk.BooleanVar(value=self.show_energy)
        tk.Checkbutton(parent, text="Mostrar Energia", variable=self.energy_var,
                      command=self.toggle_energy_display).pack(anchor='w', padx=5)
        
        self.temp_display_var = tk.BooleanVar(value=self.show_temperature)
        tk.Checkbutton(parent, text="Mostrar Temperatura", variable=self.temp_display_var,
                      command=self.toggle_temperature_display).pack(anchor='w', padx=5)
        
        self.grid_var = tk.BooleanVar(value=self.show_grid)
        tk.Checkbutton(parent, text="Mostrar Grade", variable=self.grid_var,
                      command=self.toggle_grid).pack(anchor='w', padx=5)
        
        # Modo de colisão
        tk.Label(parent, text="Modo de Colisão:").pack(anchor='w', padx=5, pady=(10,0))
        self.collision_mode_var = tk.StringVar(value=self.collision_mode)
        collision_combo = ttk.Combobox(parent, textvariable=self.collision_mode_var,
                                     values=["elastic", "inelastic", "sticky", "explosive"],
                                     state='readonly')
        collision_combo.pack(fill='x', padx=5, pady=5)
        collision_combo.bind('<<ComboboxSelected>>', self.change_collision_mode)
        
        # Cor de fundo
        tk.Button(parent, text="Cor de Fundo", command=self.change_background_color,
                 bg='#424242', fg='white').pack(fill='x', padx=5, pady=(10,2))
        
        # Screenshot
        tk.Button(parent, text="Capturar Screenshot", command=self.take_screenshot,
                 bg='#4CAF50', fg='white').pack(fill='x', padx=5, pady=2)
    
    def setup_file_controls(self, parent):
        """Controles de arquivo"""
        tk.Button(parent, text="Salvar Simulação", command=self.save_simulation,
                 bg='#4CAF50', fg='white').pack(fill='x', padx=5, pady=(10,2))
        
        tk.Button(parent, text="Carregar Simulação", command=self.load_simulation,
                 bg='#2196F3', fg='white').pack(fill='x', padx=5, pady=2)
        
        tk.Button(parent, text="Exportar Dados", command=self.export_data,
                 bg='#FF9800', fg='white').pack(fill='x', padx=5, pady=2)
        
        tk.Button(parent, text="Configurações Avançadas", command=self.show_advanced_settings,
                 bg='#9C27B0', fg='white').pack(fill='x', padx=5, pady=(20,2))
        
        tk.Button(parent, text="Sobre", command=self.show_about,
                 bg='#607D8B', fg='white').pack(fill='x', padx=5, pady=2)
    
    def setup_info_panel(self):
        """Configura o painel de informações"""
        title = tk.Label(self.right_frame, text="INFORMAÇÕES DO SISTEMA", 
                        font=('Arial', 12, 'bold'), fg='white', bg='#2a2a2a')
        title.pack(pady=10)
        
        # Frame para estatísticas
        stats_frame = tk.Frame(self.right_frame, bg='#2a2a2a')
        stats_frame.pack(fill='x', padx=5, pady=5)
        
        self.fps_label = tk.Label(stats_frame, text="FPS: 0", fg='white', bg='#2a2a2a')
        self.fps_label.pack(anchor='w')
        
        self.energy_label = tk.Label(stats_frame, text="Energia Total: 0", fg='white', bg='#2a2a2a')
        self.energy_label.pack(anchor='w')
        
        self.momentum_label = tk.Label(stats_frame, text="Momento Total: 0", fg='white', bg='#2a2a2a')
        self.momentum_label.pack(anchor='w')
        
        self.temp_label = tk.Label(stats_frame, text="Temp. Média: 0°C", fg='white', bg='#2a2a2a')
        self.temp_label.pack(anchor='w')
        
        # Lista de partículas selecionadas
        tk.Label(self.right_frame, text="PARTÍCULAS SELECIONADAS", 
                font=('Arial', 10, 'bold'), fg='white', bg='#2a2a2a').pack(pady=(20,10))
        
        self.selected_listbox = tk.Listbox(self.right_frame, bg='#3a3a3a', fg='white',
                                          selectbackground='#555555')
        self.selected_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Mini gráfico de energia
        self.energy_history = []
        self.energy_canvas = tk.Canvas(self.right_frame, height=100, bg='#1a1a1a')
        self.energy_canvas.pack(fill='x', padx=5, pady=5)
    
    def setup_events(self):
        """Configura eventos de mouse e teclado"""
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<MouseWheel>", self.on_scroll)
        
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.focus_set()
        
        # Estado do mouse
        self.mouse_pressed = False
        self.drag_start = None
        self.gravity_field_mode = False
    
    # Eventos de mouse e teclado
    def on_left_click(self, event):
        """Clique esquerdo do mouse"""
        if self.gravity_field_mode:
            self.create_gravity_field(event.x, event.y)
        else:
            # Verificar se clicou em uma partícula
            clicked_particle = self.get_particle_at_pos(event.x, event.y)
            if clicked_particle:
                if clicked_particle not in self.selected_particles:
                    self.selected_particles.append(clicked_particle)
                    clicked_particle.is_selected = True
                else:
                    self.selected_particles.remove(clicked_particle)
                    clicked_particle.is_selected = False
            else:
                # Criar nova partícula
                self.create_particle_at_mouse(event.x, event.y)
        
        self.mouse_pressed = True
        self.drag_start = (event.x, event.y)
    
    def on_right_click(self, event):
        """Clique direito do mouse - criar explosão"""
        self.create_explosion(event.x, event.y, 50, 20)
    
    def on_drag(self, event):
        """Arrastar mouse"""
        if self.mouse_pressed and self.drag_start:
            # Criar efeito de rastro de partículas
            if not self.gravity_field_mode:
                dx = event.x - self.drag_start[0]
                dy = event.y - self.drag_start[1]
                if abs(dx) > 20 or abs(dy) > 20:  # Criar partícula a cada 20 pixels
                    self.create_particle_at_mouse(event.x, event.y)
                    self.drag_start = (event.x, event.y)
    
    def on_release(self, event):
        """Soltar botão do mouse"""
        self.mouse_pressed = False
        self.drag_start = None
    
    def on_motion(self, event):
        """Movimento do mouse"""
        # Atualizar posição do cursor para efeitos visuais
        pass
    
    def on_scroll(self, event):
        """Scroll do mouse - ajustar tamanho das partículas"""
        if event.delta > 0:
            self.size_var.set(min(50, self.size_var.get() + 2))
        else:
            self.size_var.set(max(2, self.size_var.get() - 2))
    
    def on_key_press(self, event):
        """Teclas pressionadas"""
        if event.char == ' ':  # Espaço - pausar/continuar
            self.toggle_simulation()
        elif event.char == 'c':  # C - limpar
            self.clear_all()
        elif event.char == 'g':  # G - modo campo gravitacional
            self.toggle_gravity_field_mode()
        elif event.char == 'e':  # E - explodir selecionadas
            self.explode_selected()
        elif event.char == 't':  # T - alternar rastros
            self.toggle_trails()
        elif event.char == 'v':  # V - alternar vetores
            self.toggle_vectors()
    
    # Métodos de criação e manipulação de partículas
    def create_particle_at_mouse(self, x: float, y: float):
        """Cria uma partícula na posição do mouse"""
        if len(self.particles) >= self.max_particles:
            return
        
        # Velocidade inicial baseada no controle
        speed = self.initial_speed_var.get()
        angle = random.uniform(0, 2 * math.pi)
        vx = math.cos(angle) * speed * random.uniform(0.5, 1.5)
        vy = math.sin(angle) * speed * random.uniform(0.5, 1.5)
        
        # Propriedades baseadas no tipo selecionado
        particle_type = ParticleType(self.particle_type_var.get())
        size, mass, color, charge = self.get_particle_properties(particle_type)
        
        particle = Particle(
            x=x, y=y, vx=vx, vy=vy,
            size=size, mass=mass, color=color,
            particle_type=particle_type,
            trail=[], charge=charge,
            temperature=random.uniform(15, 25),
            max_age=random.uniform(30, 120) if self.aging_enabled else float('inf')
        )
        
        self.particles.append(particle)
    
    def get_particle_properties(self, particle_type: ParticleType) -> Tuple[float, float, str, float]:
        """Retorna propriedades baseadas no tipo de partícula"""
        base_size = self.size_var.get()
        
        properties = {
            ParticleType.NORMAL: (base_size, base_size, '#4CAF50', 0.0),
            ParticleType.HEAVY: (base_size * 1.5, base_size * 3, '#795548', 0.0),
            ParticleType.LIGHT: (base_size * 0.7, base_size * 0.3, '#FFEB3B', 0.0),
            ParticleType.BOUNCY: (base_size, base_size * 0.8, '#E91E63', 0.0),
            ParticleType.STICKY: (base_size, base_size, '#9C27B0', 0.0),
            ParticleType.MAGNETIC: (base_size, base_size, '#FF5722', random.choice([-1, 1])),
            ParticleType.EXPLOSIVE: (base_size * 1.2, base_size * 0.9, '#FF9800', 0.0)
        }
        
        return properties.get(particle_type, properties[ParticleType.NORMAL])
    
    def get_particle_at_pos(self, x: float, y: float) -> Particle:
        """Encontra partícula na posição especificada"""
        for particle in self.particles:
            dx = particle.x - x
            dy = particle.y - y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance <= particle.size:
                return particle
        return None
    
    def create_explosion(self, x: float, y: float, force: float, count: int):
        """Cria uma explosão na posição especificada"""
        # Afetar partículas existentes
        for particle in self.particles:
            dx = particle.x - x
            dy = particle.y - y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < 200:  # Raio de explosão
                if distance > 0:
                    explosion_force = force / (distance + 1)
                    particle.vx += (dx / distance) * explosion_force
                    particle.vy += (dy / distance) * explosion_force
                    particle.temperature += explosion_force * 0.5
        
        # Criar novas partículas
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(force * 0.5, force)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = Particle(
                x=x, y=y, vx=vx, vy=vy,
                size=self.size_var.get(),
                mass=self.size_var.get(),
                color='#FF5722',
                particle_type=ParticleType.EXPLOSIVE,
                trail=[],
                temperature=100.0,
                max_age=random.uniform(5, 15)
            )
            
            self.particles.append(particle)
    
    def create_gravity_field(self, x: float, y: float):
        """Cria um campo gravitacional na posição especificada"""
        field = GravityField(
            x=x, y=y,
            strength=random.uniform(50, 150),
            radius=random.uniform(50, 150)
        )
        self.gravity_fields.append(field)
    
    def clear_all(self):
        """Limpa todas as partículas e campos"""
        self.particles.clear()
        self.gravity_fields.clear()
        self.selected_particles.clear()
    
    def clear_gravity_fields(self):
        """Limpa todos os campos gravitacionais"""
        self.gravity_fields.clear()
    
    def explode_selected(self):
        """Explode as partículas selecionadas"""
        for particle in self.selected_particles:
            self.create_explosion(particle.x, particle.y, 30, 10)
            self.particles.remove(particle)
        self.selected_particles.clear()
    
    # Métodos de atualização da simulação
    def animate(self):
        """Loop principal de animação"""
        if self.running:
            current_time = time.time()
            dt = (current_time - self.last_time) * self.simulation_speed
            self.last_time = current_time
            
            # Atualizar física
            self.update_physics(dt)
            
            # Atualizar interface
            self.update_ui()
            
            # Calcular FPS
            self.frame_count += 1
            if current_time - self.last_fps_time > 1.0:
                self.fps = self.frame_count
                self.frame_count = 0
                self.last_fps_time = current_time
        
        # Agendar próximo frame
        self.master.after(16, self.animate)
    
    def update_physics(self, dt: float):
        """Atualiza a física das partículas"""
        # Atualizar posições e velocidades
        for particle in self.particles[:]:  # Copiar lista para permitir remoção
            # Forças ambientais
            particle.vx += self.wind_x
            particle.vy += self.wind_y + self.gravity
            
            # Campos gravitacionais
            for field in self.gravity_fields:
                if field.active:
                    dx = field.x - particle.x
                    dy = field.y - particle.y
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance < field.radius:
                        force = field.strength / (distance + 1)
                        particle.vx += (dx / distance) * force * dt
                        particle.vy += (dy / distance) * force * dt
            
            # Campos magnéticos e elétricos
            if particle.charge != 0:
                particle.vx += self.magnetic_field * particle.vy * particle.charge
                particle.vy -= self.magnetic_field * particle.vx * particle.charge
                particle.vx += self.electric_field * particle.charge
            
            # Resistência do ar
            particle.vx *= self.air_resistance
            particle.vy *= self.air_resistance
            
            # Atualizar posição
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt
            
            # Atualizar rastro
            if self.show_trails:
                particle.trail.append((particle.x, particle.y))
                if len(particle.trail) > 50:  # Limitar tamanho do rastro
                    particle.trail.pop(0)
            
            # Colisões com bordas
            if particle.x < 0 or particle.x > self.canvas.winfo_width():
                particle.vx *= -self.bounce_damping
                particle.x = max(0, min(particle.x, self.canvas.winfo_width()))
            
            if particle.y < 0 or particle.y > self.canvas.winfo_height():
                particle.vy *= -self.bounce_damping
                particle.y = max(0, min(particle.y, self.canvas.winfo_height()))
            
            # Envelhecimento
            if self.aging_enabled:
                particle.age += dt
                if particle.age >= particle.max_age:
                    self.particles.remove(particle)
                    if particle in self.selected_particles:
                        self.selected_particles.remove(particle)
                    continue
            
            # Temperatura
            if self.temperature_effects:
                # Resfriamento natural
                particle.temperature = max(20, particle.temperature - dt * 2)
                # Efeito da temperatura no tamanho
                temp_scale = 1.0 + (particle.temperature - 20) * 0.001
                particle.size = self.get_particle_properties(particle.particle_type)[0] * temp_scale
        
        # Colisões entre partículas
        if self.collision_enabled:
            self.check_collisions()
    
    def check_collisions(self):
        """Verifica e resolve colisões entre partículas"""
        for i, p1 in enumerate(self.particles[:-1]):
            for p2 in self.particles[i+1:]:
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                distance = math.sqrt(dx*dx + dy*dy)
                min_dist = (p1.size + p2.size) * 0.5
                
                if distance < min_dist:
                    # Calcular velocidades pós-colisão
                    if self.collision_mode == "elastic":
                        # Colisão elástica
                        nx = dx / distance
                        ny = dy / distance
                        
                        # Velocidade relativa
                        vx = p1.vx - p2.vx
                        vy = p1.vy - p2.vy
                        
                        # Velocidade normal
                        vn = vx * nx + vy * ny
                        
                        # Massa reduzida
                        m1 = p1.mass
                        m2 = p2.mass
                        m_total = m1 + m2
                        
                        # Impulso
                        j = -(1 + self.bounce_damping) * vn
                        j = j * (m1 * m2) / m_total
                        
                        # Aplicar impulso
                        p1.vx += (j * nx) / m1
                        p1.vy += (j * ny) / m1
                        p2.vx -= (j * nx) / m2
                        p2.vy -= (j * ny) / m2
                        
                        # Transferência de temperatura
                        avg_temp = (p1.temperature + p2.temperature) * 0.5
                        p1.temperature = p2.temperature = avg_temp
                        
                    elif self.collision_mode == "sticky":
                        # Colisão com aderência
                        vx = (p1.vx * p1.mass + p2.vx * p2.mass) / (p1.mass + p2.mass)
                        vy = (p1.vy * p1.mass + p2.vy * p2.mass) / (p1.mass + p2.mass)
                        p1.vx = p2.vx = vx
                        p1.vy = p2.vy = vy
                        
                    elif self.collision_mode == "explosive":
                        # Colisão explosiva
                        self.create_explosion((p1.x + p2.x) * 0.5, (p1.y + p2.y) * 0.5, 20, 5)
                        if p1 in self.particles: self.particles.remove(p1)
                        if p2 in self.particles: self.particles.remove(p2)
                        if p1 in self.selected_particles: self.selected_particles.remove(p1)
                        if p2 in self.selected_particles: self.selected_particles.remove(p2)
                        return
                    
                    # Separar partículas
                    overlap = min_dist - distance
                    p1.x -= overlap * dx / distance * 0.5
                    p1.y -= overlap * dy / distance * 0.5
                    p2.x += overlap * dx / distance * 0.5
                    p2.y += overlap * dy / distance * 0.5
    
    def update_ui(self):
        """Atualiza a interface gráfica"""
        self.canvas.delete('all')
        
        # Desenhar grade
        if self.show_grid:
            self.draw_grid()
        
        # Desenhar campos gravitacionais
        for field in self.gravity_fields:
            self.canvas.create_oval(
                field.x - field.radius, field.y - field.radius,
                field.x + field.radius, field.y + field.radius,
                outline='#2196F3', dash=(2, 4)
            )
        
        # Desenhar partículas
        for particle in self.particles:
            # Desenhar rastro
            if self.show_trails and len(particle.trail) > 1:
                self.canvas.create_line(
                    *[coord for point in particle.trail for coord in point],
                    fill=particle.color, width=1, alpha=0.5
                )
            
            # Desenhar partícula
            self.canvas.create_oval(
                particle.x - particle.size, particle.y - particle.size,
                particle.x + particle.size, particle.y + particle.size,
                fill=particle.color,
                outline='white' if particle.is_selected else ''
            )
            
            # Desenhar vetor de velocidade
            if self.show_vectors:
                speed = math.sqrt(particle.vx*particle.vx + particle.vy*particle.vy)
                if speed > 0:
                    scale = 20 / speed
                    self.canvas.create_line(
                        particle.x, particle.y,
                        particle.x + particle.vx * scale,
                        particle.y + particle.vy * scale,
                        fill='white', arrow=tk.LAST
                    )
            
            # Mostrar energia/temperatura
            if self.show_energy or self.show_temperature:
                info = []
                if self.show_energy:
                    ke = 0.5 * particle.mass * (particle.vx*particle.vx + particle.vy*particle.vy)
                    info.append(f"E: {ke:.0f}")
                if self.show_temperature:
                    info.append(f"T: {particle.temperature:.0f}°C")
                
                self.canvas.create_text(
                    particle.x, particle.y - particle.size - 10,
                    text=" | ".join(info),
                    fill='white', font=('Arial', 8)
                )
        
        # Atualizar estatísticas
        self.update_stats()
        
        # Atualizar lista de seleção
        self.selected_listbox.delete(0, tk.END)
        for i, particle in enumerate(self.selected_particles):
            self.selected_listbox.insert(tk.END, f"Partícula {i+1} ({particle.particle_type.value})")
        
        # Atualizar gráfico de energia
        self.update_energy_graph()
    
    def update_stats(self):
        """Atualiza as estatísticas do sistema"""
        # Calcular energia total
        ke = sum(0.5 * p.mass * (p.vx*p.vx + p.vy*p.vy) for p in self.particles)
        pe = sum(p.mass * self.gravity * (self.canvas.winfo_height() - p.y) for p in self.particles)
        self.total_energy = ke + pe
        
        # Calcular momento total
        px = sum(p.mass * p.vx for p in self.particles)
        py = sum(p.mass * p.vy for p in self.particles)
        self.total_momentum = math.sqrt(px*px + py*py)
        
        # Temperatura média
        avg_temp = sum(p.temperature for p in self.particles) / len(self.particles) if self.particles else 20
        
        # Atualizar labels
        self.fps_label.config(text=f"FPS: {self.fps}")
        self.energy_label.config(text=f"Energia Total: {self.total_energy:.0f}")
        self.momentum_label.config(text=f"Momento Total: {self.total_momentum:.0f}")
        self.temp_label.config(text=f"Temp. Média: {avg_temp:.1f}°C")
        self.particle_count_label.config(text=f"Partículas: {len(self.particles)}")
    
    def update_energy_graph(self):
        """Atualiza o gráfico de energia"""
        self.energy_history.append(self.total_energy)
        if len(self.energy_history) > 100:
            self.energy_history.pop(0)
        
        self.energy_canvas.delete('all')
        if len(self.energy_history) > 1:
            max_energy = max(self.energy_history)
            if max_energy > 0:
                points = []
                for i, e in enumerate(self.energy_history):
                    x = i * self.energy_canvas.winfo_width() / 100
                    y = self.energy_canvas.winfo_height() * (1 - e/max_energy)
                    points.extend([x, y])
                
                self.energy_canvas.create_line(
                    points, fill='#4CAF50', width=2
                )
    
    def draw_grid(self):
        """Desenha uma grade de referência"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        # Linhas verticais
        for x in range(0, w, 50):
            self.canvas.create_line(x, 0, x, h, fill='#333333')
        
        # Linhas horizontais
        for y in range(0, h, 50):
            self.canvas.create_line(0, y, w, y, fill='#333333')
    
    # Métodos de controle da simulação
    def toggle_simulation(self):
        """Alterna entre pausar e continuar a simulação"""
        self.running = not self.running
    
    def toggle_gravity_field_mode(self):
        """Alterna o modo de criação de campo gravitacional"""
        self.gravity_field_mode = not self.gravity_field_mode
        self.canvas.config(cursor='cross' if self.gravity_field_mode else '')
    
    def toggle_trails(self):
        """Alterna a exibição de rastros"""
        self.show_trails = not self.show_trails
        if not self.show_trails:
            for particle in self.particles:
                particle.trail.clear()
    
    def toggle_vectors(self):
        """Alterna a exibição de vetores de velocidade"""
        self.show_vectors = not self.show_vectors
    
    def toggle_energy_display(self):
        """Alterna a exibição de energia"""
        self.show_energy = not self.show_energy
    
    def toggle_temperature_display(self):
        """Alterna a exibição de temperatura"""
        self.show_temperature = not self.show_temperature
    
    def toggle_grid(self):
        """Alterna a exibição da grade"""
        self.show_grid = not self.show_grid
    
    def toggle_collisions(self):
        """Alterna as colisões entre partículas"""
        self.collision_enabled = not self.collision_enabled
    
    def toggle_interaction(self):
        """Alterna a interação entre partículas"""
        self.particle_interaction = not self.particle_interaction
    
    def toggle_temperature(self):
        """Alterna os efeitos de temperatura"""
        self.temperature_effects = not self.temperature_effects
    
    def toggle_aging(self):
        """Alterna o envelhecimento das partículas"""
        self.aging_enabled = not self.aging_enabled
        if not self.aging_enabled:
            for particle in self.particles:
                particle.max_age = float('inf')
    
    def change_particle_type(self, event=None):
        """Altera o tipo de partícula selecionado"""
        self.current_particle_type = ParticleType(self.particle_type_var.get())
    
    def change_collision_mode(self, event=None):
        """Altera o modo de colisão"""
        self.collision_mode = self.collision_mode_var.get()
    
    def change_background_color(self):
        """Altera a cor de fundo do canvas"""
        color = colorchooser.askcolor(title="Escolher Cor de Fundo")[1]
        if color:
            self.canvas.config(bg=color)
    
    # Métodos de atualização de parâmetros
    def update_gravity(self, value):
        """Atualiza a gravidade"""
        self.gravity = float(value)
    
    def update_air_resistance(self, value):
        """Atualiza a resistência do ar"""
        self.air_resistance = float(value)
    
    def update_damping(self, value):
        """Atualiza o amortecimento"""
        self.bounce_damping = float(value)
    
    def update_speed(self, value):
        """Atualiza a velocidade da simulação"""
        self.simulation_speed = float(value)
    
    def update_wind_x(self, value):
        """Atualiza o vento horizontal"""
        self.wind_x = float(value)
    
    def update_wind_y(self, value):
        """Atualiza o vento vertical"""
        self.wind_y = float(value)
    
    def update_magnetic(self, value):
        """Atualiza o campo magnético"""
        self.magnetic_field = float(value)
    
    def update_electric(self, value):
        """Atualiza o campo elétrico"""
        self.electric_field = float(value)
    
    # Métodos de arquivo
    def save_simulation(self):
        """Salva o estado atual da simulação"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            data = {
                "particles": [
                    {
                        "x": p.x, "y": p.y,
                        "vx": p.vx, "vy": p.vy,
                        "size": p.size, "mass": p.mass,
                        "color": p.color,
                        "type": p.particle_type.value,
                        "temperature": p.temperature,
                        "age": p.age, "max_age": p.max_age
                    } for p in self.particles
                ],
                "gravity_fields": [
                    {
                        "x": f.x, "y": f.y,
                        "strength": f.strength,
                        "radius": f.radius
                    } for f in self.gravity_fields
                ],
                "settings": {
                    "gravity": self.gravity,
                    "air_resistance": self.air_resistance,
                    "bounce_damping": self.bounce_damping,
                    "collision_enabled": self.collision_enabled,
                    "particle_interaction": self.particle_interaction,
                    "temperature_effects": self.temperature_effects,
                    "aging_enabled": self.aging_enabled,
                    "wind_x": self.wind_x,
                    "wind_y": self.wind_y,
                    "magnetic_field": self.magnetic_field,
                    "electric_field": self.electric_field
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
    
    def load_simulation(self):
        """Carrega uma simulação salva"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Limpar simulação atual
            self.clear_all()
            
            # Carregar partículas
            for p_data in data["particles"]:
                particle = Particle(
                    x=p_data["x"], y=p_data["y"],
                    vx=p_data["vx"], vy=p_data["vy"],
                    size=p_data["size"], mass=p_data["mass"],
                    color=p_data["color"],
                    particle_type=ParticleType(p_data["type"]),
                    trail=[],
                    temperature=p_data["temperature"],
                    age=p_data["age"], max_age=p_data["max_age"]
                )
                self.particles.append(particle)
            
            # Carregar campos gravitacionais
            for f_data in data["gravity_fields"]:
                field = GravityField(
                    x=f_data["x"], y=f_data["y"],
                    strength=f_data["strength"],
                    radius=f_data["radius"]
                )
                self.gravity_fields.append(field)
            
            # Carregar configurações
            settings = data["settings"]
            self.gravity = settings["gravity"]
            self.gravity_var.set(self.gravity)
            
            self.air_resistance = settings["air_resistance"]
            self.air_var.set(self.air_resistance)
            
            self.bounce_damping = settings["bounce_damping"]
            self.damping_var.set(self.bounce_damping)
            
            self.collision_enabled = settings["collision_enabled"]
            self.collision_var.set(self.collision_enabled)
            
            self.particle_interaction = settings["particle_interaction"]
            self.interaction_var.set(self.particle_interaction)
            
            self.temperature_effects = settings["temperature_effects"]
            self.temperature_var.set(self.temperature_effects)
            
            self.aging_enabled = settings["aging_enabled"]
            self.aging_var.set(self.aging_enabled)
            
            self.wind_x = settings["wind_x"]
            self.wind_x_var.set(self.wind_x)
            
            self.wind_y = settings["wind_y"]
            self.wind_y_var.set(self.wind_y)
            
            self.magnetic_field = settings["magnetic_field"]
            self.magnetic_var.set(self.magnetic_field)
            
            self.electric_field = settings["electric_field"]
            self.electric_var.set(self.electric_field)
    
    def export_data(self):
        """Exporta dados da simulação para CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            with open(filename, 'w') as f:
                # Cabeçalho
                f.write("id,x,y,vx,vy,size,mass,type,temperature,age\n")
                
                # Dados das partículas
                for i, p in enumerate(self.particles):
                    f.write(f"{i},{p.x},{p.y},{p.vx},{p.vy},{p.size},{p.mass},")
                    f.write(f"{p.particle_type.value},{p.temperature},{p.age}\n")
    
    def show_advanced_settings(self):
        """Mostra janela de configurações avançadas"""
        dialog = tk.Toplevel(self.master)
        dialog.title("Configurações Avançadas")
        dialog.geometry("400x300")
        dialog.transient(self.master)
        
        # Número máximo de partículas
        tk.Label(dialog, text="Máximo de Partículas:").pack(anchor='w', padx=5, pady=(10,0))
        max_particles = tk.Scale(dialog, from_=100, to=5000, orient=tk.HORIZONTAL,
                               variable=tk.IntVar(value=self.max_particles))
        max_particles.pack(fill='x', padx=5)
        
        # Tamanho do rastro
        tk.Label(dialog, text="Tamanho do Rastro:").pack(anchor='w', padx=5, pady=(10,0))
        trail_size = tk.Scale(dialog, from_=10, to=200, orient=tk.HORIZONTAL,
                            variable=tk.IntVar(value=50))
        trail_size.pack(fill='x', padx=5)
        
        def apply_settings():
            self.max_particles = max_particles.get()
            dialog.destroy()
        
        tk.Button(dialog, text="Aplicar", command=apply_settings).pack(pady=20)
    
    def show_about(self):
         """Mostra informações sobre o programa"""
         messagebox.showinfo(
             "Sobre",
             "Simulação Avançada de Gravidade e Física\n\n"
             "Desenvolvido como exemplo educacional de física e programação.\n\n"
             "Características:\n"
             "- Simulação de partículas com física realista\n"
             "- Campos gravitacionais e forças ambientais\n"
             "- Interface gráfica interativa\n"
             "- Ferramentas de análise e visualização"
         )
     
     def take_screenshot(self):
         """Captura e salva uma imagem da simulação"""
         filename = filedialog.asksaveasfilename(
             defaultextension=".png",
             filetypes=[("PNG files", "*.png")]
         )
         if filename:
             # Obter dimensões do canvas
             x = self.canvas.winfo_rootx()
             y = self.canvas.winfo_rooty()
             w = self.canvas.winfo_width()
             h = self.canvas.winfo_height()
             
             # Capturar screenshot
             self.master.update()
             image = ImageGrab.grab(bbox=(x, y, x+w, y+h))
             image.save(filename)
    
    def create_demo_scene(self):
        """Cria uma cena de demonstração"""
        self.clear_all()
        
        # Criar algumas partículas
        for _ in range(20):
            x = random.uniform(100, self.canvas.winfo_width() - 100)
            y = random.uniform(100, self.canvas.winfo_height() - 100)
            self.create_particle_at_mouse(x, y)
        
        # Criar alguns campos gravitacionais
        for _ in range(3):
            x = random.uniform(100, self.canvas.winfo_width() - 100)
            y = random.uniform(100, self.canvas.winfo_height() - 100)
            self.create_gravity_field(x, y)

# Iniciar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedGravitySimulation(root)
    root.mainloop()