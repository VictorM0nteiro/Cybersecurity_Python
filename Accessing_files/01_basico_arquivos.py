# Exemplo Básico de Manipulação de Arquivos em Python

'''
Este script demonstra operações básicas com arquivos:
- Abrir arquivos nos modos de leitura, escrita e append
- Ler conteúdo de arquivos
- Escrever em arquivos
- Usar o gerenciador de contexto 'with'
'''

# Criando um arquivo e escrevendo nele
print("\n1. Criando e escrevendo em um arquivo:")
try:
    # Modo 'w' - Escrita (cria um novo arquivo ou sobrescreve se já existir)
    arquivo = open("exemplo.txt", "w")
    arquivo.write("Primeira linha de texto.\n")
    arquivo.write("Segunda linha de texto.\n")
    arquivo.write("Terceira linha de texto.\n")
    arquivo.close()  # Importante sempre fechar o arquivo
    print("✓ Arquivo criado com sucesso!")
except Exception as e:
    print(f"Erro ao criar arquivo: {e}")

# Lendo o conteúdo do arquivo
print("\n2. Lendo o conteúdo completo do arquivo:")
try:
    # Modo 'r' - Leitura
    arquivo = open("exemplo.txt", "r")
    conteudo = arquivo.read()
    arquivo.close()
    print(conteudo)
except Exception as e:
    print(f"Erro ao ler arquivo: {e}")

# Adicionando mais conteúdo ao arquivo (append)
print("\n3. Adicionando mais conteúdo ao arquivo:")
try:
    # Modo 'a' - Append (adiciona ao final do arquivo)
    arquivo = open("exemplo.txt", "a")
    arquivo.write("Esta linha foi adicionada posteriormente.\n")
    arquivo.write("Mais uma linha adicionada.\n")
    arquivo.close()
    print("✓ Conteúdo adicionado com sucesso!")
except Exception as e:
    print(f"Erro ao adicionar conteúdo: {e}")

# Lendo o arquivo linha por linha
print("\n4. Lendo o arquivo linha por linha:")
try:
    arquivo = open("exemplo.txt", "r")
    for i, linha in enumerate(arquivo, 1):
        print(f"Linha {i}: {linha}", end="")
    arquivo.close()
except Exception as e:
    print(f"Erro ao ler arquivo linha por linha: {e}")

# Usando o gerenciador de contexto 'with' (forma recomendada)
print("\n\n5. Usando o gerenciador de contexto 'with':")
try:
    # O 'with' garante que o arquivo será fechado automaticamente
    with open("exemplo.txt", "r") as arquivo:
        print("\nConteúdo do arquivo:")
        print(arquivo.read())
    # Aqui o arquivo já está fechado automaticamente
    print("✓ Arquivo foi fechado automaticamente!")
except Exception as e:
    print(f"Erro ao usar with: {e}")

print("\nTodas as operações foram concluídas!")