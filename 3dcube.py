import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial.transform import Rotation as R

# --- 1. Definição dos Vértices do Cubo ---
# Um cubo de lado 2, centrado na origem (0,0,0).
# Cada linha representa um ponto [x, y, z].
vertices = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
])

# --- 2. Definição das Arestas do Cubo ---
# Cada par de números se refere aos índices dos vértices que formam uma aresta.
# Por exemplo, [0, 1] conecta o primeiro e o segundo vértice.
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Face de baixo
    [4, 5], [5, 6], [6, 7], [7, 4],  # Face de cima
    [0, 4], [1, 5], [2, 6], [3, 7]   # Arestas verticais
]

# --- 3. Rotação Inicial para Equilibrar no Vértice ---
# Para o cubo ficar sobre um vértice, precisamos alinhar sua diagonal principal
# (que vai de um vértice ao seu oposto, ex: de [-1,-1,-1] a [1,1,1]) com o eixo Z.
# Primeiro, rotacionamos 45 graus no eixo Z.
rotation_z = R.from_euler('z', 45, degrees=True)
# Depois, rotacionamos aproximadamente 54.7 graus no eixo Y.
rotation_y = R.from_euler('y', 54.7, degrees=True)
# Combinamos as rotações.
initial_rotation = rotation_y * rotation_z
# Aplicamos a rotação a todos os vértices.
vertices = initial_rotation.apply(vertices)


# --- 4. Configuração do Gráfico 3D ---
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Ajusta os limites dos eixos para o cubo ficar bem visível.
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_zlabel('Eixo Z')
ax.set_title('Cubo Girando Sobre um Vértice')


# --- 5. Função de Animação ---
# Esta função será chamada para cada "quadro" da animação.
def update(frame):
    ax.cla() # Limpa o gráfico anterior para desenhar o próximo quadro.
    
    # Configura os eixos novamente, pois o cla() os remove.
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Cubo Girando Sobre um Vértice')

    # Define a rotação para o quadro atual.
    # O cubo vai girar em torno do eixo Z (vertical).
    # A velocidade da rotação depende do multiplicador de 'frame'.
    rotation_speed = 2 # Altere este valor para girar mais rápido ou mais devagar
    angle = frame * rotation_speed
    spin_rotation = R.from_euler('z', angle, degrees=True)
    
    # Aplica a rotação de giro aos vértices já equilibrados.
    rotated_vertices = spin_rotation.apply(vertices)
    
    # Desenha as arestas do cubo.
    for edge in edges:
        # Pega os dois pontos que formam a aresta.
        points = rotated_vertices[edge]
        # 'points[:, 0]' pega todos os valores de X, 'points[:, 1]' os de Y, etc.
        ax.plot3D(points[:, 0], points[:, 1], points[:, 2], color='b')

# --- 6. Cria e Executa a Animação ---
# FuncAnimation chama a função 'update' repetidamente.
# 'frames=180' cria 180 quadros. 'interval=50' define 50 milissegundos entre quadros.
ani = FuncAnimation(fig, update, frames=180, interval=50, blit=False)

# Mostra o gráfico com a animação.
plt.show()