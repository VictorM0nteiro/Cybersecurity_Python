# Estratégia de Debugging: Logging

'''
Este script demonstra o uso do módulo logging para debugging:
- Configuração de diferentes níveis de log
- Formatação de mensagens de log
- Redirecionamento de logs para arquivos
- Vantagens sobre o uso de prints simples
'''

import logging
import os
import random
import time

# Diretório para armazenar logs
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# Configuração básica de logging
def configurar_logging_basico():
    # Configuração básica: mensagens vão para o console
    logging.basicConfig(
        level=logging.DEBUG,  # Nível mínimo de log (DEBUG é o mais detalhado)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem
        datefmt='%Y-%m-%d %H:%M:%S'  # Formato da data/hora
    )
    
    print("\n===== LOGGING BÁSICO CONFIGURADO =====")
    print("Níveis de log (do menos ao mais severo):")
    print("DEBUG → INFO → WARNING → ERROR → CRITICAL")

# Configuração avançada de logging
def configurar_logging_avancado():
    # Resetando configurações anteriores
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Criando um logger
    logger = logging.getLogger('app_debug')
    logger.setLevel(logging.DEBUG)
    
    # Handler para console (INFO e acima)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    
    # Handler para arquivo (todos os níveis)
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'debug.log'))
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    
    # Adicionando handlers ao logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    print("\n===== LOGGING AVANÇADO CONFIGURADO =====")
    print(f"Logs detalhados serão salvos em: {os.path.join(LOG_DIR, 'debug.log')}")
    print("Apenas mensagens INFO e acima serão exibidas no console")
    
    return logger

# Função com bug para demonstrar o logging
def processar_dados(dados, logger=None):
    # Se nenhum logger for fornecido, usa o logging padrão
    if logger is None:
        logger = logging
    
    logger.debug(f"Iniciando processamento de {len(dados)} itens")
    
    resultados = []
    for i, item in enumerate(dados):
        logger.debug(f"Processando item {i}: {item}")
        
        try:
            # Simulando algum processamento com possível erro
            if random.random() < 0.3:  # 30% de chance de erro
                logger.warning(f"Item {i} pode causar problemas")
                if random.random() < 0.5:  # 50% de chance de erro grave
                    raise ValueError(f"Erro ao processar item {item}")
            
            # Processamento normal
            resultado = item * 2
            logger.debug(f"Item {i} processado com sucesso: {resultado}")
            resultados.append(resultado)
            
        except Exception as e:
            logger.error(f"Erro no item {i}: {str(e)}", exc_info=True)
    
    logger.info(f"Processamento concluído. {len(resultados)} de {len(dados)} itens processados com sucesso")
    return resultados

# Simulação de uma aplicação com logging
def simular_aplicacao():
    # Configurando logging avançado
    logger = configurar_logging_avancado()
    
    logger.info("Iniciando aplicação")
    
    # Simulando operações
    try:
        logger.debug("Gerando dados aleatórios")
        dados = [random.randint(1, 100) for _ in range(10)]
        
        logger.info(f"Dados gerados: {dados}")
        
        # Primeira operação
        logger.debug("Iniciando primeira operação")
        time.sleep(0.5)  # Simulando processamento
        logger.info("Primeira operação concluída")
        
        # Segunda operação (com possíveis erros)
        logger.debug("Iniciando processamento de dados")
        resultados = processar_dados(dados, logger)
        logger.info(f"Resultados obtidos: {resultados}")
        
        # Operação crítica simulada
        if len(resultados) < len(dados):
            logger.critical("Nem todos os dados foram processados! Verificar logs para detalhes.")
        else:
            logger.info("Todos os dados foram processados com sucesso")
            
    except Exception as e:
        logger.critical(f"Erro fatal na aplicação: {str(e)}", exc_info=True)
    
    logger.info("Aplicação encerrada")

# Demonstração de uso
if __name__ == "__main__":
    print("\n===== DEMONSTRAÇÃO DE LOGGING PARA DEBUGGING =====")
    
    # Exemplo 1: Logging básico
    print("\n>> Exemplo 1: Logging Básico")
    configurar_logging_basico()
    
    logging.debug("Esta é uma mensagem de DEBUG (detalhes para desenvolvedores)")
    logging.info("Esta é uma mensagem de INFO (informações gerais)")
    logging.warning("Esta é uma mensagem de WARNING (avisos)")
    logging.error("Esta é uma mensagem de ERROR (erros que não interrompem a aplicação)")
    logging.critical("Esta é uma mensagem de CRITICAL (erros graves)")
    
    # Exemplo 2: Logging em funções
    print("\n>> Exemplo 2: Logging em Funções")
    dados_teste = [5, 10, 15, 20, 25]
    resultados = processar_dados(dados_teste)
    print(f"Resultados do processamento: {resultados}")
    
    # Exemplo 3: Simulação de aplicação com logging avançado
    print("\n>> Exemplo 3: Simulação de Aplicação com Logging Avançado")
    simular_aplicacao()
    
    print("\n===== VANTAGENS DO LOGGING SOBRE PRINT DEBUGGING =====")
    print("1. Diferentes níveis de severidade (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    print("2. Pode ser facilmente ativado/desativado sem remover código")
    print("3. Pode ser direcionado para diferentes saídas (console, arquivo, email, etc.)")
    print("4. Inclui automaticamente informações como timestamp, nome do módulo, etc.")
    print("5. Pode capturar automaticamente informações de exceções (traceback)")
    print(f"\nVerifique o arquivo de log gerado em: {os.path.join(LOG_DIR, 'debug.log')}")