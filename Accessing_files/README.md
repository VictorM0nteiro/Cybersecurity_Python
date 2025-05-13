# Manipulação de Arquivos em Python

Este diretório contém exemplos práticos de manipulação de arquivos em Python, com foco em aplicações para segurança da informação.

## Arquivos de Exemplo

1. **01_basico_arquivos.py** - Demonstra operações básicas com arquivos:
   - Abrir arquivos nos modos de leitura, escrita e append
   - Ler conteúdo de arquivos
   - Escrever em arquivos
   - Usar o gerenciador de contexto 'with'

2. **02_avancado_arquivos.py** - Demonstra operações mais avançadas:
   - Trabalhando com arquivos CSV
   - Trabalhando com arquivos JSON
   - Operações com diretórios
   - Verificação de existência de arquivos
   - Obtenção de informações sobre arquivos

3. **03_seguranca_arquivos.py** - Demonstra operações úteis para segurança:
   - Leitura e análise de arquivos de log
   - Verificação de integridade de arquivos (hashing)
   - Criptografia básica de arquivos
   - Monitoramento de alterações em arquivos

## Como Executar

Cada arquivo pode ser executado individualmente usando o interpretador Python:

```
python 01_basico_arquivos.py
python 02_avancado_arquivos.py
python 03_seguranca_arquivos.py
```

## Requisitos

Para o exemplo de criptografia no arquivo `03_seguranca_arquivos.py`, é necessário instalar a biblioteca `cryptography`:

```
pip install cryptography
```

## Aplicações em Segurança da Informação

A manipulação de arquivos é uma habilidade fundamental para profissionais de segurança da informação, sendo útil para:

- Análise de logs de segurança
- Verificação de integridade de arquivos críticos
- Detecção de alterações não autorizadas em arquivos
- Processamento de dados para análise forense
- Criptografia e proteção de dados sensíveis
- Automação de tarefas de segurança

Cada exemplo contém comentários explicativos sobre os conceitos demonstrados.