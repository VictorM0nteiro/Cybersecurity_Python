
"""
gravidade_avancado.py
Simula��o avan�ada de gravidade com GUI (tkinter).
Funcionalidades destacadas:
- Integrador semi-impl�cito com substepping ajust�vel
- Arrasto do ar (linear e quadr�tico)
- Campo de vento global e local (vortex / noise simples)
- Po�os de gravidade (point-mass gravity wells)
- Colis�es el�sticas entre bolas com restitui��o individual e fric��o tangencial (simples)
- Broadphase por Spatial Hashing para melhorar desempenho com muitas bolas
- Trilhas (traces) configur�veis
- Vetores de velocidade e valores de debug (energia, contagem de colis�es)
- Presets (padr�es iniciais), salvar/carregar cena (JSON) e exportar dados CSV
- Ferramentas: pausar/step, slowmotion, limpar, adicionar N bolas, editar par�metros por bola via clique
- Interface responsiva com sliders, menus e teclas de atalho
Requisitos: Python 3.x (Windows/macOS/Linux), Tkinter dispon�vel (vem por padr�o na maioria das instala��es).
Execute: python gravidade_avancado.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox, colorchooser
import random, math, time, json, csv, os
from collections import defaultdict
# -*- coding: utf-8 -*-

# Canvas size
WIDTH, HEIGHT = 1000, 700
GROUND_Y = HEIGHT - 40

# Helper utilities
def clamp(v, a, b): return max(a, min(b, v))
def vec_len(x, y): return math.hypot(x, y)
def normalize(x, y):
    d = vec_len(x, y)
    if d == 0: return 0.0, 0.0
    return x/d, y/d

# Spatial hash for broadphase collision detection
class SpatialHash:
    def __init__(self, cell_size=80):
        self.cell_size = cell_size
        self.cells = defaultdict(list)
    def _cell_coords(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)
    def clear(self):
        self.cells.clear()
    def insert(self, obj):
        minx = obj.x - obj.radius
        miny = obj.y - obj.radius
        maxx = obj.x + obj.radius
        maxy = obj.y + obj.radius
        x0, y0 = self._cell_coords(minx, miny)
        x1, y1 = self._cell_coords(maxx, maxy)
        for i in range(x0, x1+1):
            for j in range(y0, y1+1):
                self.cells[(i,j)].append(obj)
    def candidates(self, obj):
        seen = set()
        minx = obj.x - obj.radius
        miny = obj.y - obj.radius
        maxx = obj.x + obj.radius
        maxy = obj.y + obj.radius
        x0, y0 = self._cell_coords(minx, miny)
        x1, y1 = self._cell_coords(maxx, maxy)
        for i in range(x0, x1+1):
            for j in range(y0, y1+1):
                for o in self.cells.get((i,j), ()):
                    if o is not obj and o not in seen:
                        seen.add(o)
                        yield o

# Ball class
class Ball:
    def __init__(self, canvas, x, y, vx=0, vy=0, radius=18, color=None, mass=None, restitution=0.8, friction=0.15, drag_coeff=0.0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.mass = mass if mass is not None else math.pi*radius*radius/1000.0 + 0.2
        self.restitution = restitution
        self.friction = friction  # tangential friction during collision
        self.drag_coeff = drag_coeff  # extra per-ball drag multiplier
        self.color = color or self.random_color()
        self.id = canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.color, outline='black', width=1)
        self.trace = []  # list of past positions for trail
        self.max_trace = 150
        self.show_trace = False
        self.selected = False
        # optional label for mass/speed etc
        self.label_id = None
    def random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)
    def update_canvas(self, draw_velocity=False, draw_label=False):
        self.canvas.coords(self.id, self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)
        if self.show_trace and self.trace:
            # draw trace as line segments (low cost)
            if hasattr(self, "_trace_id"):
                self.canvas.delete(self._trace_id)
            pts = []
            for tx, ty in self.trace:
                pts.extend([tx, ty])
            if len(pts) >= 4:
                self._trace_id = self.canvas.create_line(*pts, smooth=True, width=1)
        if draw_velocity:
            vx_line = (self.x, self.y, self.x + self.vx*0.08, self.y + self.vy*0.08)
            if hasattr(self, "_vel_id"):
                self.canvas.coords(self._vel_id, *vx_line)
            else:
                self._vel_id = self.canvas.create_line(*vx_line, arrow='last')
        if draw_label:
            text = f"m={self.mass:.2f}\nv={vec_len(self.vx,self.vy):.1f}"
            if self.label_id is None:
                self.label_id = self.canvas.create_text(self.x, self.y - self.radius - 10, text=text, font=("TkDefaultFont", 8))
            else:
                self.canvas.coords(self.label_id, self.x, self.y - self.radius - 10)
                self.canvas.itemconfigure(self.label_id, text=text)
    def step_trace(self):
        if self.show_trace:
            self.trace.append((self.x, self.y))
            if len(self.trace) > self.max_trace:
                self.trace.pop(0)
        else:
            if self.trace:
                self.trace.clear()
                if hasattr(self, "_trace_id"):
                    self.canvas.delete(self._trace_id)
                    delattr(self, "_trace_id")
    def to_dict(self):
        return {
            "x": self.x, "y": self.y, "vx": self.vx, "vy": self.vy,
            "radius": self.radius, "mass": self.mass, "color": self.color,
            "restitution": self.restitution, "friction": self.friction, "drag_coeff": self.drag_coeff
        }

# Gravity well (point mass)
class GravityWell:
    def __init__(self, x, y, strength=50000.0, radius=120, color="#660000"):
        self.x = x
        self.y = y
        self.strength = strength  # G * massEquivalent in arbitrary units
        self.radius = radius
        self.color = color
        self.id = None

# Main App
class GravitySimApp:
    def __init__(self, root):
        self.root = root
        root.title("Simula��o Avan�ada de Gravidade - Victor (Avan�ada)")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=20, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        # draw ground
        self.ground = self.canvas.create_rectangle(0, GROUND_Y, WIDTH, HEIGHT, fill="#eee", outline="#aaa")
        # UI frame
        self.ui = ttk.Frame(root)
        self.ui.grid(row=0, column=1, sticky="ns", padx=6, pady=6)
        # world parameters
        self.gravity = tk.DoubleVar(value=980.0)  # px/s^2
        self.global_drag = tk.DoubleVar(value=0.001)  # base air drag (quadratic scaling)
        self.linear_drag = tk.DoubleVar(value=0.0)  # linear drag term
        self.wind_x = tk.DoubleVar(value=0.0)
        self.wind_y = tk.DoubleVar(value=0.0)
        self.substeps = tk.IntVar(value=2)
        self.spatial_cell = tk.IntVar(value=80)
        self.trails_enabled = tk.BooleanVar(value=False)
        self.draw_vectors = tk.BooleanVar(value=False)
        self.show_labels = tk.BooleanVar(value=False)
        self.slowmotion = tk.DoubleVar(value=1.0)  # global time scale
        self.paused = False
        self.last_time = time.time()
        self.step_once = False
        self.balls = []
        self.wells = []
        self.spatial = SpatialHash(cell_size=self.spatial_cell.get())
        self.collision_count = 0
        # build UI controls
        ttk.Label(self.ui, text="Mundo").pack(anchor="w")
        ttk.Label(self.ui, text="Gravidade (px/s�)").pack(anchor="w")
        ttk.Scale(self.ui, from_=0, to=2000, variable=self.gravity, orient="horizontal").pack(fill="x")
        ttk.Label(self.ui, text="Drag quadr�tico (global)").pack(anchor="w")
        ttk.Scale(self.ui, from_=0.0, to=0.01, variable=self.global_drag, orient="horizontal").pack(fill="x")
        ttk.Label(self.ui, text="Drag linear (global)").pack(anchor="w")
        ttk.Scale(self.ui, from_=0.0, to=1.0, variable=self.linear_drag, orient="horizontal").pack(fill="x")
        ttk.Label(self.ui, text="Vento X").pack(anchor="w")
        ttk.Scale(self.ui, from_=-500, to=500, variable=self.wind_x, orient="horizontal").pack(fill="x")
        ttk.Label(self.ui, text="Vento Y").pack(anchor="w")
        ttk.Scale(self.ui, from_=-500, to=500, variable=self.wind_y, orient="horizontal").pack(fill="x")
        ttk.Label(self.ui, text="Substeps (simula��o por frame)").pack(anchor="w")
        ttk.Spinbox(self.ui, from_=1, to=8, textvariable=self.substeps).pack(fill="x")
        ttk.Label(self.ui, text="Spatial cell size").pack(anchor="w")
        ttk.Spinbox(self.ui, from_=40, to=200, textvariable=self.spatial_cell, command=self._update_spatial_cell).pack(fill="x")
        ttk.Separator(self.ui).pack(fill="x", pady=4)
        ttk.Checkbutton(self.ui, text="Rastro (trails)", variable=self.trails_enabled, command=self._toggle_trails).pack(anchor="w")
        ttk.Checkbutton(self.ui, text="Desenhar vetores de velocidade", variable=self.draw_vectors).pack(anchor="w")
        ttk.Checkbutton(self.ui, text="Mostrar labels", variable=self.show_labels).pack(anchor="w")
        ttk.Label(self.ui, text="Slow motion (time scale)").pack(anchor="w")
        ttk.Scale(self.ui, from_=0.05, to=2.0, variable=self.slowmotion, orient="horizontal").pack(fill="x")
        ttk.Button(self.ui, text="Adicionar bola aleat�ria", command=self.add_random_ball).pack(fill="x", pady=4)
        ttk.Button(self.ui, text="Adicionar 50 bolas", command=lambda: self.add_many(50)).pack(fill="x", pady=2)
        ttk.Button(self.ui, text="Limpar bolas", command=self.clear_balls).pack(fill="x", pady=2)
        ttk.Button(self.ui, text="Adicionar po�o de gravidade (clique)", command=self._enter_add_well_mode).pack(fill="x", pady=2)
        ttk.Separator(self.ui).pack(fill="x", pady=4)
        ttk.Button(self.ui, text="Salvar cena", command=self.save_scene).pack(fill="x", pady=2)
        ttk.Button(self.ui, text="Carregar cena", command=self.load_scene).pack(fill="x", pady=2)
        ttk.Button(self.ui, text="Exportar CSV (pos/vel)", command=self.export_csv).pack(fill="x", pady=2)
        ttk.Separator(self.ui).pack(fill="x", pady=4)
        self.pause_btn = ttk.Button(self.ui, text="Pausar (P)", command=self.toggle_pause)
        self.pause_btn.pack(fill="x", pady=2)
        ttk.Button(self.ui, text="Step (1 frame)", command=self.step_frame).pack(fill="x", pady=2)
        ttk.Button(self.ui, text="Reset c�mera (centrar)", command=self.reset_view).pack(fill="x", pady=2)
        ttk.Separator(self.ui).pack(fill="x", pady=4)
        self.status_label = ttk.Label(self.ui, text="Status: pronto")
        self.status_label.pack(fill="x", pady=4)
        # bind canvas click to add ball
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        root.bind("p", lambda e: self.toggle_pause())
        root.bind("<space>", lambda e: self.step_frame())
        root.bind("c", lambda e: self.clear_balls())
        root.bind("t", lambda e: self.trails_enabled.set(not self.trails_enabled.get()) or self._toggle_trails())
        # start with some balls
        for _ in range(8):
            self.add_random_ball()
        # some debug draws
        self._draw_wells()
        # main loop
        self._update()

    def _update_spatial_cell(self):
        self.spatial = SpatialHash(cell_size=self.spatial_cell.get())

    def _toggle_trails(self):
        for b in self.balls:
            b.show_trace = self.trails_enabled.get()
            if not b.show_trace:
                b.trace.clear()
                if hasattr(b, "_trace_id"):
                    try: self.canvas.delete(b._trace_id)
                    except: pass

    def add_random_ball(self):
        r = random.randint(8, 28)
        x = random.uniform(r+5, WIDTH - r - 5)
        y = random.uniform(50, HEIGHT/2)
        vx = random.uniform(-200, 200)
        vy = random.uniform(-50, 50)
        restitution = random.uniform(0.4, 0.95)
        friction = random.uniform(0.0, 0.25)
        drag_coeff = random.uniform(0.0, 0.02)
        b = Ball(self.canvas, x, y, vx, vy, r, mass=None, restitution=restitution, friction=friction, drag_coeff=drag_coeff)
        b.show_trace = self.trails_enabled.get()
        self.balls.append(b)

    def add_many(self, n):
        for _ in range(n):
            self.add_random_ball()

    def clear_balls(self):
        for b in self.balls:
            try:
                self.canvas.delete(b.id)
                if b.label_id: self.canvas.delete(b.label_id)
                if hasattr(b, "_vel_id"): self.canvas.delete(b._vel_id)
                if hasattr(b, "_trace_id"): self.canvas.delete(b._trace_id)
            except: pass
        self.balls.clear()
        self.collision_count = 0

    def _enter_add_well_mode(self):
        messagebox.showinfo("Adicionar po�o", "Clique no canvas para adicionar um po�o de gravidade.\nClique direito para cancelar.")
        self._adding_well = True

    def on_click(self, event):
        # if adding well mode
        if getattr(self, "_adding_well", False):
            w = GravityWell(event.x, event.y, strength=50000.0, radius=120)
            self.wells.append(w)
            self._adding_well = False
            self._draw_wells()
            return
        # otherwise add ball
        self.add_ball(event.x, event.y)

    def on_right_click(self, event):
        # select ball under cursor and open edit dialog
        b = self._find_ball_at(event.x, event.y)
        if b:
            self._edit_ball_dialog(b)
        else:
            # right click can remove wells
            w = self._find_well_at(event.x, event.y)
            if w:
                try:
                    self.wells.remove(w)
                    self._draw_wells()
                except: pass

    def _find_ball_at(self, x, y):
        for b in reversed(self.balls):  # topmost
            if vec_len(b.x-x, b.y-y) <= b.radius:
                return b
        return None

    def _find_well_at(self, x, y):
        for w in reversed(self.wells):
            if vec_len(w.x-x, w.y-y) <= w.radius:
                return w
        return None

    def add_ball(self, x, y, vx=0, vy=0, radius=18, mass=None):
        b = Ball(self.canvas, x, y, vx, vy, radius, mass=mass)
        b.show_trace = self.trails_enabled.get()
        self.balls.append(b)

    def _edit_ball_dialog(self, b):
        dlg = tk.Toplevel(self.root)
        dlg.title("Editar bola")
        ttk.Label(dlg, text="Restitui��o").grid(row=0, column=0)
        rest = tk.DoubleVar(value=b.restitution)
        ttk.Entry(dlg, textvariable=rest).grid(row=0, column=1)
        ttk.Label(dlg, text="Fric��o").grid(row=1, column=0)
        fr = tk.DoubleVar(value=b.friction)
        ttk.Entry(dlg, textvariable=fr).grid(row=1, column=1)
        ttk.Label(dlg, text="Drag coef").grid(row=2, column=0)
        dc = tk.DoubleVar(value=b.drag_coeff)
        ttk.Entry(dlg, textvariable=dc).grid(row=2, column=1)
        def apply_edit():
            b.restitution = float(rest.get())
            b.friction = float(fr.get())
            b.drag_coeff = float(dc.get())
            dlg.destroy()
        ttk.Button(dlg, text="Aplicar", command=apply_edit).grid(row=3, column=0, columnspan=2)

    def _draw_wells(self):
        # remove old well drawings
        for w in self.wells:
            if w.id: 
                try: self.canvas.delete(w.id)
                except: pass
        for w in self.wells:
            w.id = self.canvas.create_oval(w.x-w.radius, w.y-w.radius, w.x+w.radius, w.y+w.radius, outline=w.color, width=2)
            self.canvas.create_text(w.x, w.y, text=f"{int(w.strength)}", fill=w.color)

    def save_scene(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not path: return
        data = {
            "balls": [b.to_dict() for b in self.balls],
            "wells": [{"x":w.x,"y":w.y,"strength":w.strength,"radius":w.radius} for w in self.wells],
            "params": {"gravity": self.gravity.get(), "global_drag": self.global_drag.get(), "linear_drag": self.linear_drag.get()}
        }
        with open(path, "w") as f: json.dump(data, f, indent=2)
        messagebox.showinfo("Salvar cena", f"Cena salva em:\n{path}")

    def load_scene(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not path: return
        with open(path, "r") as f: data = json.load(f)
        self.clear_balls()
        for bd in data.get("balls", []):
            b = Ball(self.canvas, bd["x"], bd["y"], bd.get("vx",0), bd.get("vy",0), bd.get("radius",18), bd.get("color"), bd.get("mass", None), bd.get("restitution",0.8), bd.get("friction",0.15), bd.get("drag_coeff",0.0))
            b.show_trace = self.trails_enabled.get()
            self.balls.append(b)
        self.wells.clear()
        for wd in data.get("wells", []):
            self.wells.append(GravityWell(wd["x"], wd["y"], wd.get("strength",50000.0), wd.get("radius",120)))
        params = data.get("params", {})
        self.gravity.set(params.get("gravity", self.gravity.get()))
        self.global_drag.set(params.get("global_drag", self.global_drag.get()))
        self.linear_drag.set(params.get("linear_drag", self.linear_drag.get()))
        self._draw_wells()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        with open(path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["time","id","x","y","vx","vy","radius","mass"])
            t = time.time()
            for i,b in enumerate(self.balls):
                writer.writerow([t, i, b.x, b.y, b.vx, b.vy, b.radius, b.mass])
        messagebox.showinfo("Exportar CSV", f"Exportado para {path}")

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Retomar (P)" if self.paused else "Pausar (P)")
        if not self.paused:
            self.last_time = time.time()

    def step_frame(self):
        # perform one frame advance
        self.step_once = True
        if self.paused:
            self._simulate(1/60.0 * self.slowmotion.get())

    def reset_view(self):
        # could implement camera transform; for now just center status
        self.canvas.xview_moveto(0.0)
        self.canvas.yview_moveto(0.0)

    def _simulate(self, dt_frame):
        """Simulate physics for dt_frame seconds, splitted into substeps"""
        sub = max(1, int(self.substeps.get()))
        dt = dt_frame / sub
        g = self.gravity.get()
        wind = (self.wind_x.get(), self.wind_y.get())
        # spatial hash update
        self.spatial.clear()
        for b in self.balls:
            self.spatial.insert(b)
        for s in range(sub):
            # apply forces
            for b in self.balls:
                # gravity
                b.vy += g * dt
                # wind + per-ball drag
                rel_vx = b.vx - wind[0]
                rel_vy = b.vy - wind[1]
                speed = vec_len(rel_vx, rel_vy)
                # quadratic drag: F = -k * v * |v| (simulate by acceleration: a = F/m)
                k = self.global_drag.get() + b.drag_coeff
                if speed > 0:
                    drag_ax = -k * rel_vx * speed / b.mass
                    drag_ay = -k * rel_vy * speed / b.mass
                else:
                    drag_ax = drag_ay = 0.0
                # linear drag (optional)
                lin = self.linear_drag.get()
                drag_ax += -lin * rel_vx / b.mass
                drag_ay += -lin * rel_vy / b.mass
                b.vx += drag_ax * dt
                b.vy += drag_ay * dt
                # integrate (semi-implicit euler)
                b.x += b.vx * dt
                b.y += b.vy * dt
                # traces
                b.step_trace()
            # gravity wells forces (point mass attraction)
            for w in self.wells:
                for b in self.balls:
                    dx = w.x - b.x
                    dy = w.y - b.y
                    dist2 = dx*dx + dy*dy + 1e-6
                    force = w.strength / dist2  # inverse-square law scaled
                    ax = force * dx / b.mass
                    ay = force * dy / b.mass
                    b.vx += ax * dt
                    b.vy += ay * dt
            # collisions (broadphase + narrow)
            checked = set()
            for b in list(self.balls):
                for o in self.spatial.candidates(b):
                    if (b,o) in checked or (o,b) in checked: continue
                    checked.add((b,o))
                    self._resolve_ball_collision(b, o)
            # wall collisions
            for b in self.balls:
                # floor
                if b.y + b.radius > GROUND_Y:
                    b.y = GROUND_Y - b.radius
                    if b.vy > 0:
                        b.vy = -b.vy * b.restitution
                        # friction reduces horizontal speed on floor contact
                        b.vx *= (1 - b.friction)
                        self.collision_count += 1
                # ceiling
                if b.y - b.radius < 0:
                    b.y = b.radius
                    if b.vy < 0:
                        b.vy = -b.vy * b.restitution
                        self.collision_count += 1
                # left wall
                if b.x - b.radius < 0:
                    b.x = b.radius
                    if b.vx < 0:
                        b.vx = -b.vx * b.restitution
                        self.collision_count += 1
                # right wall
                if b.x + b.radius > WIDTH:
                    b.x = WIDTH - b.radius
                    if b.vx > 0:
                        b.vx = -b.vx * b.restitution
                        self.collision_count += 1

    def _resolve_ball_collision(self, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            # jitter
            dist = 0.01
            dx = 0.01
        overlap = a.radius + b.radius - dist
        if overlap > 0:
            # push apart proportional to inverse mass
            nx = dx / dist
            ny = dy / dist
            total_inv_mass = (1.0/a.mass) + (1.0/b.mass)
            if total_inv_mass == 0: return
            # positional correction (to avoid sinking)
            percent = 0.8  # positional correction factor
            correction = (overlap / total_inv_mass) * percent
            a.x -= correction * (1.0/a.mass) * nx
            a.y -= correction * (1.0/a.mass) * ny
            b.x += correction * (1.0/b.mass) * nx
            b.y += correction * (1.0/b.mass) * ny
            # relative velocity
            rvx = b.vx - a.vx
            rvy = b.vy - a.vy
            vel_along_normal = rvx*nx + rvy*ny
            if vel_along_normal > 0:
                return
            # restitution (use min of two restitutions)
            e = min(a.restitution, b.restitution)
            # impulse scalar
            j = -(1 + e) * vel_along_normal
            j /= total_inv_mass
            ix = j * nx
            iy = j * ny
            a.vx -= ix * (1.0/a.mass)
            a.vy -= iy * (1.0/a.mass)
            b.vx += ix * (1.0/b.mass)
            b.vy += iy * (1.0/b.mass)
            # simple tangential friction - reduce tangential velocity component
            # compute tangent
            tx = -ny
            ty = nx
            vel_tangent = rvx*tx + rvy*ty
            # average friction coefficient
            mu = (a.friction + b.friction) * 0.5
            # friction impulse (clamped)
            jt = -vel_tangent
            jt /= total_inv_mass
            # clamp friction magnitude
            max_jt = j * mu
            jt = clamp(jt, -abs(max_jt), abs(max_jt))
            a.vx -= jt * tx * (1.0/a.mass)
            a.vy -= jt * ty * (1.0/a.mass)
            b.vx += jt * tx * (1.0/b.mass)
            b.vy += jt * ty * (1.0/b.mass)
            self.collision_count += 1

    def _update(self):
        now = time.time()
        dt = now - self.last_time if not self.paused else 0.0
        if dt > 0.05: dt = 0.05
        self.last_time = now
        timescale = max(0.0001, self.slowmotion.get())
        if not self.paused or self.step_once:
            self._simulate(dt * timescale)
            self.step_once = False
        # redraw items
        for b in self.balls:
            # remove previous vel/label/trace items to avoid duplicates (lightweight approach)
            if hasattr(b, "_vel_id"):
                try: self.canvas.delete(b._vel_id)
                except: pass
                delattr(b, "_vel_id")
            if b.label_id:
                try: self.canvas.delete(b.label_id)
                except: pass
                b.label_id = None
            if hasattr(b, "_trace_id"):
                try: self.canvas.delete(b._trace_id)
                except: pass
                delattr(b, "_trace_id")
            b.update_canvas(draw_velocity=self.draw_vectors.get(), draw_label=self.show_labels.get())
        # redraw wells
        self._draw_wells()
        # update status
        ke = sum(0.5*b.mass*(b.vx*b.vx + b.vy*b.vy) for b in self.balls)
        pe = sum(b.mass * self.gravity.get() * (GROUND_Y - b.y) for b in self.balls)
        self.status_label.config(text=f"Bolas: {len(self.balls)}  Colis�es: {self.collision_count}  KE: {ke:.1f}  PE: {pe:.1f}")
        # schedule next frame
        self.root.after(16, self._update)

def main():
    root = tk.Tk()
    app = GravitySimApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
