# Manipulação de Arquivos para Aplicações de Segurança

'''
Este script demonstra operações com arquivos úteis para segurança:
- Leitura e análise de arquivos de log
- Verificação de integridade de arquivos (hashing)
- Criptografia básica de arquivos
- Monitoramento de alterações em arquivos
'''

import os
import hashlib
import time
import re
import base64
import datetime
from cryptography.fernet import Fernet

# Diretório para os exemplos
DIR_EXEMPLO = "arquivos_seguranca"
if not os.path.exists(DIR_EXEMPLO):
    os.mkdir(DIR_EXEMPLO)
    print(f"✓ Diretório '{DIR_EXEMPLO}' criado com sucesso!")

# 1. Criando um arquivo de log simulado
print("\n1. Criando e analisando um arquivo de log:")
try:
    # Criando um arquivo de log simulado
    log_file = os.path.join(DIR_EXEMPLO, "access_log.txt")
    
    # Entradas de log simuladas
    log_entries = [
        "[2023-10-15 08:23:45] INFO: Usuário admin logado com sucesso IP=192.168.1.5",
        "[2023-10-15 08:25:12] WARNING: Múltiplas tentativas de login para usuário root IP=45.67.89.123",
        "[2023-10-15 08:30:45] ERROR: Tentativa de acesso não autorizado à pasta /etc/shadow IP=45.67.89.123",
        "[2023-10-15 09:15:22] INFO: Usuário analista logado com sucesso IP=192.168.1.10",
        "[2023-10-15 09:45:18] WARNING: Arquivo de configuração modificado por usuário admin",
        "[2023-10-15 10:12:33] INFO: Backup automático iniciado",
        "[2023-10-15 10:30:45] ERROR: Falha na conexão com servidor de backup IP=192.168.1.100",
        "[2023-10-15 11:05:22] INFO: Usuário analista desconectado",
        "[2023-10-15 11:45:18] WARNING: Múltiplas tentativas de login para usuário admin IP=45.67.89.123",
        "[2023-10-15 12:12:33] INFO: Firewall atualizado com novas regras"
    ]
    
    with open(log_file, 'w') as f:
        for entry in log_entries:
            f.write(entry + "\n")
    print(f"✓ Arquivo de log criado em: {log_file}")
    
    # Analisando o arquivo de log
    print("\nAnalisando o arquivo de log:")
    
    # Padrões para busca
    padrao_ip = r'IP=(\d+\.\d+\.\d+\.\d+)'
    padrao_erro = r'ERROR:'
    padrao_aviso = r'WARNING:'
    
    # Contadores
    ips = {}
    erros = 0
    avisos = 0
    
    with open(log_file, 'r') as f:
        for linha in f:
            # Contando IPs
            match_ip = re.search(padrao_ip, linha)
            if match_ip:
                ip = match_ip.group(1)
                ips[ip] = ips.get(ip, 0) + 1
            
            # Contando erros e avisos
            if re.search(padrao_erro, linha):
                erros += 1
                print(f"  ❌ Erro encontrado: {linha.strip()}")
            elif re.search(padrao_aviso, linha):
                avisos += 1
                print(f"  ⚠️ Aviso encontrado: {linha.strip()}")
    
    print(f"\nResumo da análise:")
    print(f"  - Total de erros: {erros}")
    print(f"  - Total de avisos: {avisos}")
    print(f"  - IPs encontrados:")
    for ip, count in ips.items():
        print(f"    * {ip}: {count} ocorrências")
    
    # Identificando possíveis ameaças
    print("\nPossíveis ameaças identificadas:")
    for ip, count in ips.items():
        if count >= 3:
            print(f"  ⚠️ IP suspeito: {ip} com {count} ocorrências")
            
except Exception as e:
    print(f"Erro ao trabalhar com arquivo de log: {e}")

# 2. Verificação de integridade de arquivos (hashing)
print("\n2. Verificação de integridade de arquivos:")
try:
    # Criando um arquivo para verificação
    arquivo_verificacao = os.path.join(DIR_EXEMPLO, "dados_importantes.txt")
    with open(arquivo_verificacao, 'w') as f:
        f.write("Estes são dados importantes que não devem ser modificados.\n")
        f.write("Qualquer alteração neste arquivo deve ser detectada.\n")
    print(f"✓ Arquivo criado em: {arquivo_verificacao}")
    
    # Função para calcular o hash de um arquivo
    def calcular_hash(caminho_arquivo, algoritmo='sha256'):
        hash_obj = hashlib.new(algoritmo)
        with open(caminho_arquivo, 'rb') as f:
            # Lê o arquivo em blocos para economizar memória
            for bloco in iter(lambda: f.read(4096), b""):
                hash_obj.update(bloco)
        return hash_obj.hexdigest()
    
    # Calculando o hash original
    hash_original = calcular_hash(arquivo_verificacao)
    print(f"Hash original (SHA-256): {hash_original}")
    
    # Salvando o hash em um arquivo
    arquivo_hash = os.path.join(DIR_EXEMPLO, "hash_verificacao.txt")
    with open(arquivo_hash, 'w') as f:
        f.write(f"{hash_original}  {os.path.basename(arquivo_verificacao)}\n")
    print(f"✓ Hash salvo em: {arquivo_hash}")
    
    # Simulando uma verificação posterior
    print("\nVerificando integridade do arquivo:")
    hash_atual = calcular_hash(arquivo_verificacao)
    
    with open(arquivo_hash, 'r') as f:
        linha_hash = f.readline().strip()
        hash_salvo = linha_hash.split()[0]
    
    if hash_atual == hash_salvo:
        print("✅ Integridade verificada: O arquivo não foi modificado!")
    else:
        print("❌ ALERTA: O arquivo foi modificado!")
        print(f"  Hash esperado: {hash_salvo}")
        print(f"  Hash atual: {hash_atual}")
    
    # Simulando uma modificação no arquivo
    print("\nSimulando uma modificação no arquivo...")
    with open(arquivo_verificacao, 'a') as f:
        f.write("Esta linha foi adicionada posteriormente!\n")
    
    # Verificando novamente
    hash_modificado = calcular_hash(arquivo_verificacao)
    print("Verificando integridade após modificação:")
    if hash_modificado == hash_salvo:
        print("✅ Integridade verificada: O arquivo não foi modificado!")
    else:
        print("❌ ALERTA: O arquivo foi modificado!")
        print(f"  Hash esperado: {hash_salvo}")
        print(f"  Hash atual: {hash_modificado}")
        
except Exception as e:
    print(f"Erro na verificação de integridade: {e}")

# 3. Criptografia básica de arquivos
print("\n3. Criptografia básica de arquivos:")
try:
    # Criando um arquivo com dados sensíveis
    arquivo_sensivel = os.path.join(DIR_EXEMPLO, "dados_sensiveis.txt")
    with open(arquivo_sensivel, 'w') as f:
        f.write("Usuário: administrador\n")
        f.write("Senha: S3nh@_S3cr3t@\n")
        f.write("API Key: a1b2c3d4e5f6g7h8i9j0\n")
    print(f"✓ Arquivo com dados sensíveis criado em: {arquivo_sensivel}")
    
    # Gerando uma chave de criptografia
    chave = Fernet.generate_key()
    arquivo_chave = os.path.join(DIR_EXEMPLO, "chave.key")
    with open(arquivo_chave, 'wb') as f:
        f.write(chave)
    print(f"✓ Chave de criptografia salva em: {arquivo_chave}")
    
    # Criptografando o arquivo
    cipher = Fernet(chave)
    
    with open(arquivo_sensivel, 'rb') as f:
        dados = f.read()
    
    dados_criptografados = cipher.encrypt(dados)
    
    arquivo_criptografado = os.path.join(DIR_EXEMPLO, "dados_sensiveis.enc")
    with open(arquivo_criptografado, 'wb') as f:
        f.write(dados_criptografados)
    print(f"✓ Arquivo criptografado salvo em: {arquivo_criptografado}")
    
    # Descriptografando o arquivo
    print("\nDescriptografando o arquivo:")
    with open(arquivo_criptografado, 'rb') as f:
        dados_enc = f.read()
    
    with open(arquivo_chave, 'rb') as f:
        chave_lida = f.read()
    
    cipher = Fernet(chave_lida)
    dados_descriptografados = cipher.decrypt(dados_enc)
    
    print("Conteúdo descriptografado:")
    print(dados_descriptografados.decode())
    
except Exception as e:
    print(f"Erro na criptografia de arquivos: {e}")
    print("Nota: Este exemplo requer a biblioteca 'cryptography'. Instale com 'pip install cryptography'")

# 4. Monitoramento de alterações em arquivos
print("\n4. Monitoramento de alterações em arquivos:")
try:
    # Criando um arquivo para monitorar
    arquivo_monitorado = os.path.join(DIR_EXEMPLO, "arquivo_monitorado.txt")
    with open(arquivo_monitorado, 'w') as f:
        f.write("Conteúdo inicial do arquivo monitorado.\n")
    print(f"✓ Arquivo para monitoramento criado em: {arquivo_monitorado}")
    
    # Função para obter informações do arquivo
    def obter_info_arquivo(caminho):
        stat = os.stat(caminho)
        return {
            'tamanho': stat.st_size,
            'modificado': stat.st_mtime,
            'criado': stat.st_ctime,
            'hash': calcular_hash(caminho)
        }
    
    # Obtendo informações iniciais
    info_inicial = obter_info_arquivo(arquivo_monitorado)
    print("\nInformações iniciais do arquivo:")
    print(f"  - Tamanho: {info_inicial['tamanho']} bytes")
    print(f"  - Modificado em: {datetime.datetime.fromtimestamp(info_inicial['modificado']).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  - Hash: {info_inicial['hash']}")
    
    # Simulando um monitoramento
    print("\nSimulando monitoramento (modificando o arquivo)...")
    
    # Modificando o arquivo
    time.sleep(2)  # Pausa para garantir timestamp diferente
    with open(arquivo_monitorado, 'a') as f:
        f.write("Esta linha foi adicionada durante o monitoramento.\n")
    
    # Verificando alterações
    info_atual = obter_info_arquivo(arquivo_monitorado)
    
    print("\nVerificando alterações:")
    if info_atual['tamanho'] != info_inicial['tamanho']:
        print(f"⚠️ Tamanho alterado: {info_inicial['tamanho']} -> {info_atual['tamanho']} bytes")
    
    if info_atual['modificado'] != info_inicial['modificado']:
        data_anterior = datetime.datetime.fromtimestamp(info_inicial['modificado']).strftime('%Y-%m-%d %H:%M:%S')
        data_atual = datetime.datetime.fromtimestamp(info_atual['modificado']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"⚠️ Data de modificação alterada: {data_anterior} -> {data_atual}")
    
    if info_atual['hash'] != info_inicial['hash']:
        print(f"⚠️ Hash alterado: {info_inicial['hash']} -> {info_atual['hash']}")
        
    # Exibindo o conteúdo atual
    print("\nConteúdo atual do arquivo:")
    with open(arquivo_monitorado, 'r') as f:
        print(f.read())
    
except Exception as e:
    print(f"Erro no monitoramento de arquivos: {e}")

print("\n✅ Todas as operações de segurança foram concluídas!")