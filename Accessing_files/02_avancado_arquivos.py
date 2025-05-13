# Exemplo Avançado de Manipulação de Arquivos em Python

'''
Este script demonstra operações mais avançadas com arquivos:
- Trabalhando com arquivos CSV
- Trabalhando com arquivos JSON
- Operações com diretórios
- Verificação de existência de arquivos
- Obtenção de informações sobre arquivos
'''

import os
import csv
import json
import shutil
import datetime

# Criando um diretório para os exemplos
DIR_EXEMPLO = "arquivos_exemplo"
if not os.path.exists(DIR_EXEMPLO):
    os.mkdir(DIR_EXEMPLO)
    print(f"✓ Diretório '{DIR_EXEMPLO}' criado com sucesso!")
else:
    print(f"O diretório '{DIR_EXEMPLO}' já existe.")

# 1. Trabalhando com arquivos CSV
print("\n1. Trabalhando com arquivos CSV:")
try:
    # Criando um arquivo CSV
    dados_csv = [
        ['Nome', 'Idade', 'Profissão'],
        ['Ana', 28, 'Engenheira de Segurança'],
        ['Carlos', 35, 'Analista de Sistemas'],
        ['Maria', 31, 'Desenvolvedora'],
        ['João', 42, 'Administrador de Redes']
    ]
    
    caminho_csv = os.path.join(DIR_EXEMPLO, "funcionarios.csv")
    
    with open(caminho_csv, 'w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerows(dados_csv)
    print(f"✓ Arquivo CSV criado em: {caminho_csv}")
    
    # Lendo o arquivo CSV
    print("\nLendo o arquivo CSV:")
    with open(caminho_csv, 'r') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        for i, linha in enumerate(leitor):
            print(f"  Linha {i}: {linha}")
            
    # Usando DictReader para ler CSV como dicionários
    print("\nLendo CSV como dicionários:")
    with open(caminho_csv, 'r') as arquivo_csv:
        leitor_dict = csv.DictReader(arquivo_csv)
        for linha in leitor_dict:
            print(f"  {linha['Nome']} - {linha['Idade']} anos - {linha['Profissão']}")
            
except Exception as e:
    print(f"Erro ao trabalhar com CSV: {e}")

# 2. Trabalhando com arquivos JSON
print("\n2. Trabalhando com arquivos JSON:")
try:
    # Criando dados para o JSON
    dados_json = {
        "empresa": "Segurança Digital Ltda",
        "ano_fundacao": 2010,
        "areas": ["Cibersegurança", "Análise de Vulnerabilidades", "Resposta a Incidentes"],
        "funcionarios": [
            {"id": 1, "nome": "Ana", "departamento": "Segurança"},
            {"id": 2, "nome": "Carlos", "departamento": "Desenvolvimento"},
            {"id": 3, "nome": "Maria", "departamento": "Análise"}
        ]
    }
    
    caminho_json = os.path.join(DIR_EXEMPLO, "empresa.json")
    
    # Escrevendo no arquivo JSON
    with open(caminho_json, 'w') as arquivo_json:
        json.dump(dados_json, arquivo_json, indent=4)  # indent para formatação bonita
    print(f"✓ Arquivo JSON criado em: {caminho_json}")
    
    # Lendo o arquivo JSON
    print("\nLendo o arquivo JSON:")
    with open(caminho_json, 'r') as arquivo_json:
        dados_lidos = json.load(arquivo_json)
        print(f"  Empresa: {dados_lidos['empresa']}")
        print(f"  Fundação: {dados_lidos['ano_fundacao']}")
        print(f"  Áreas de atuação: {', '.join(dados_lidos['areas'])}")
        print("  Funcionários:")
        for func in dados_lidos['funcionarios']:
            print(f"    - {func['nome']} ({func['departamento']})")
            
except Exception as e:
    print(f"Erro ao trabalhar com JSON: {e}")

# 3. Operações com diretórios e informações de arquivos
print("\n3. Operações com diretórios e informações de arquivos:")
try:
    # Listando arquivos em um diretório
    print(f"\nArquivos no diretório '{DIR_EXEMPLO}':")
    for item in os.listdir(DIR_EXEMPLO):
        caminho_completo = os.path.join(DIR_EXEMPLO, item)
        if os.path.isfile(caminho_completo):
            # Obtendo informações do arquivo
            tamanho = os.path.getsize(caminho_completo)  # tamanho em bytes
            data_mod = os.path.getmtime(caminho_completo)  # timestamp da última modificação
            data_formatada = datetime.datetime.fromtimestamp(data_mod).strftime('%d/%m/%Y %H:%M:%S')
            
            print(f"  📄 {item}")
            print(f"     - Tamanho: {tamanho} bytes")
            print(f"     - Última modificação: {data_formatada}")
            print(f"     - Caminho absoluto: {os.path.abspath(caminho_completo)}")
        elif os.path.isdir(caminho_completo):
            print(f"  📁 {item} (diretório)")
    
    # Criando um subdiretório
    subdir = os.path.join(DIR_EXEMPLO, "subdiretorio")
    if not os.path.exists(subdir):
        os.mkdir(subdir)
        print(f"\n✓ Subdiretório criado: {subdir}")
    
    # Criando um arquivo no subdiretório
    arquivo_teste = os.path.join(subdir, "teste.txt")
    with open(arquivo_teste, 'w') as f:
        f.write("Este é um arquivo de teste no subdiretório.")
    print(f"✓ Arquivo criado em: {arquivo_teste}")
    
    # Verificando se um arquivo existe
    arquivo_verificar = os.path.join(DIR_EXEMPLO, "nao_existe.txt")
    if os.path.exists(arquivo_verificar):
        print(f"O arquivo {arquivo_verificar} existe.")
    else:
        print(f"O arquivo {arquivo_verificar} não existe.")
    
    # Copiando um arquivo
    arquivo_origem = os.path.join(DIR_EXEMPLO, "empresa.json")
    arquivo_destino = os.path.join(DIR_EXEMPLO, "empresa_copia.json")
    shutil.copy2(arquivo_origem, arquivo_destino)
    print(f"\n✓ Arquivo copiado: {arquivo_origem} -> {arquivo_destino}")
    
    # Renomeando um arquivo
    novo_nome = os.path.join(DIR_EXEMPLO, "empresa_renomeado.json")
    os.rename(arquivo_destino, novo_nome)
    print(f"✓ Arquivo renomeado: {arquivo_destino} -> {novo_nome}")
    
except Exception as e:
    print(f"Erro nas operações com diretórios: {e}")

print("\n✅ Todas as operações avançadas foram concluídas!")