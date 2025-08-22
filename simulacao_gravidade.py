#gemini 2.5 pro

import pygame
import random
import math

# --- Constantes e Configurações ---
LARGURA_TELA = 1280
ALTURA_TELA = 720
FPS = 60

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CORES_PARTICULAS = [
    (255, 87, 34), (255, 193, 7), (139, 195, 74), 
    (0, 188, 212), (33, 150, 243), (103, 58, 183)
]

# Configurações de Física
GRAVIDADE = pygame.Vector2(0, 0.3)  # Vetor de gravidade
ELASTICIDADE = 0.85                 # Coeficiente de restituição (0.0 a 1.0)
RESISTENCIA_AR = 0.01               # Coeficiente de arrasto (0.0 a 1.0)

# --- Classe da Partícula ---
class Particle:
    """ Representa uma partícula circular com propriedades físicas. """
    def __init__(self, x, y, radius):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.radius = radius
        self.mass = self.radius ** 2  # Massa proporcional à área
        self.color = random.choice(CORES_PARTICULAS)

    def update(self, gravidade_ativa):
        """ Atualiza o estado da partícula (movimento e forças). """
        # Aplicar gravidade se estiver ativa
        if gravidade_ativa:
            self.vel += GRAVIDADE

        # Aplicar resistência do ar (arrasto)
        # Força de arrasto = -k * v^2 * (direção de v)
        if self.vel.length() > 0:
            arrasto_magnitude = self.vel.length_squared() * RESISTENCIA_AR
            arrasto = self.vel.normalize() * -arrasto_magnitude
            self.vel += arrasto

        # Atualizar posição
        self.pos += self.vel

        # Checar colisões com as bordas da tela
        self.check_boundary_collision()

    def check_boundary_collision(self):
        """ Inverte a velocidade e aplica elasticidade ao colidir com as bordas. """
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -ELASTICIDADE
        elif self.pos.x + self.radius > LARGURA_TELA:
            self.pos.x = LARGURA_TELA - self.radius
            self.vel.x *= -ELASTICIDADE

        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -ELASTICIDADE
        elif self.pos.y + self.radius > ALTURA_TELA:
            self.pos.y = ALTURA_TELA - self.radius
            self.vel.y *= -ELASTICIDADE

    def draw(self, screen):
        """ Desenha a partícula na tela. """
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))

def handle_collisions(particles):
    """ Gerencia a colisão entre todas as partículas. """
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]

            dist_vec = p1.pos - p2.pos
            dist_mag = dist_vec.length()
            
            # Checa se há colisão
            if dist_mag < p1.radius + p2.radius:
                # Resolve a sobreposição
                overlap = (p1.radius + p2.radius) - dist_mag
                p1.pos += (dist_vec.normalize() * overlap / 2)
                p2.pos -= (dist_vec.normalize() * overlap / 2)
                
                # Calcula a resposta da colisão (física de colisão elástica 2D)
                normal = dist_vec.normalize()
                tangent = pygame.Vector2(-normal.y, normal.x)

                # Velocidades no eixo normal e tangencial
                v1n = p1.vel.dot(normal)
                v1t = p1.vel.dot(tangent)
                v2n = p2.vel.dot(normal)
                v2t = p2.vel.dot(tangent)

                # As velocidades tangenciais não mudam
                # As velocidades normais trocam momento
                m1, m2 = p1.mass, p2.mass
                new_v1n = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
                new_v2n = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

                # Converte as velocidades escalares de volta para vetores
                vec_v1n = new_v1n * normal * ELASTICIDADE
                vec_v1t = v1t * tangent
                vec_v2n = new_v2n * normal * ELASTICIDADE
                vec_v2t = v2t * tangent

                # Define as novas velocidades
                p1.vel = vec_v1n + vec_v1t
                p2.vel = vec_v2n + vec_v2t

def draw_hud(screen, font, num_particles, fps, paused, gravidade_ativa):
    """ Desenha as informações (HUD) na tela. """
    instrucoes1 = "Clique para adicionar | P: Pausar | R: Resetar | G: Gravidade"
    status_gravidade = "ON" if gravidade_ativa else "OFF"
    status_pausa = "PAUSADO" if paused else f"FPS: {fps:.1f}"
    
    info_text = f"Partículas: {num_particles} | {status_pausa} | Gravidade: {status_gravidade}"

    inst_render = font.render(instrucoes1, True, BRANCO)
    info_render = font.render(info_text, True, BRANCO)

    screen.blit(inst_render, (10, 10))
    screen.blit(info_render, (10, 35))


# --- Função Principal ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Simulação de Física Avançada")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    particles = []
    paused = False
    gravidade_ativa = True
    
    running = True
    while running:
        dt = clock.tick(FPS)

        # Processamento de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Botão esquerdo
                    x, y = pygame.mouse.get_pos()
                    radius = random.randint(10, 30)
                    particles.append(Particle(x, y, radius))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r:
                    particles.clear()
                if event.key == pygame.K_g:
                    gravidade_ativa = not gravidade_ativa

        # Atualização da Lógica
        if not paused:
            for p in particles:
                p.update(gravidade_ativa)
            handle_collisions(particles)

        # Desenho
        screen.fill(PRETO)
        for p in particles:
            p.draw(screen)
        
        draw_hud(screen, font, len(particles), clock.get_fps(), paused, gravidade_ativa)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()