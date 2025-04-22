# # Exemplos de manipulação de estruturas de dados em Python

# print("===== MANIPULAÇÃO DE LISTAS =====\n")

# # Criando uma lista
# lista = [10, 20, 30, 40, 50]
# print(f"Lista original: {lista}")

# # Adicionando elementos
# lista.append(60)  # Adiciona ao final da lista
# print(f"Após append(60): {lista}")

# lista.insert(2, 25)  # Insere na posição 2
# print(f"Após insert(2, 25): {lista}")

# # Removendo elementos
# elemento_removido = lista.pop()  # Remove o último elemento
# print(f"Elemento removido com pop(): {elemento_removido}")
# print(f"Lista após pop(): {lista}")

# elemento_removido = lista.pop(2)  # Remove o elemento na posição 2
# print(f"Elemento removido com pop(2): {elemento_removido}")
# print(f"Lista após pop(2): {lista}")

# lista.remove(40)  # Remove o elemento com valor 40
# print(f"Lista após remove(40): {lista}\n")


# print("===== MANIPULAÇÃO DE TUPLAS =====\n")

# # Criando uma tupla
# tupla = (10, 20, 30, 40, 50)
# print(f"Tupla original: {tupla}")

# # Tuplas são imutáveis, não podemos adicionar ou remover elementos diretamente
# # Mas podemos converter para lista, modificar e converter de volta

# # Convertendo para lista para adicionar elementos
# lista_da_tupla = list(tupla)
# lista_da_tupla.append(60)
# lista_da_tupla.insert(0, 5)
# tupla_modificada = tuple(lista_da_tupla)
# print(f"Tupla após conversão e adição: {tupla_modificada}")

# # Convertendo para lista para remover elementos
# lista_da_tupla = list(tupla)
# lista_da_tupla.remove(30)
# tupla_modificada = tuple(lista_da_tupla)
# print(f"Tupla após conversão e remoção: {tupla_modificada}\n")


# print("===== MANIPULAÇÃO DE PILHAS (STACK) =====\n")

# # Em Python, podemos implementar pilhas usando listas
# pilha = []
# print(f"Pilha vazia: {pilha}")

# # Adicionando elementos (push)
# pilha.append(10)
# pilha.append(20)
# pilha.append(30)
# print(f"Pilha após push de elementos: {pilha}")

# # Removendo elementos (pop) - LIFO (Last In, First Out)
# elemento = pilha.pop()
# print(f"Elemento removido do topo: {elemento}")
# print(f"Pilha após pop: {pilha}")

# elemento = pilha.pop()
# print(f"Elemento removido do topo: {elemento}")
# print(f"Pilha após pop: {pilha}\n")


# print("===== MANIPULAÇÃO DE FILAS (QUEUE) =====\n")

# # Para filas, é melhor usar collections.deque para operações eficientes
# from collections import deque

# fila = deque()
# print(f"Fila vazia: {fila}")

# # Adicionando elementos (enqueue)
# fila.append(10)
# fila.append(20)
# fila.append(30)
# print(f"Fila após enqueue de elementos: {fila}")

# # Removendo elementos (dequeue) - FIFO (First In, First Out)
# elemento = fila.popleft()
# print(f"Elemento removido do início: {elemento}")
# print(f"Fila após dequeue: {fila}")

# elemento = fila.popleft()
# print(f"Elemento removido do início: {elemento}")
# print(f"Fila após dequeue: {fila}")

# # Também podemos adicionar elementos no início da fila
# fila.appendleft(5)
# print(f"Fila após appendleft(5): {fila}")

my_list = [1, 2, 3, 4, 5]
my_list[2] = "b"
print(my_list)

my_sec_list = ["a","b","c","d","e"]
my_sec_list = my_list + my_sec_list
my_sec_list[7] = "f"
print("before adding",my_sec_list)

my_sec_list.insert(0,"batata") #position and element to be added
print("after adding",my_sec_list)

my_sec_list.remove("e") #element to be removed
print("after removing",my_sec_list)