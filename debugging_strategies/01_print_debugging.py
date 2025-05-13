# Estratégia de Debugging: Print Debugging

'''
Este script demonstra a técnica mais básica de debugging: o uso de prints.
Embora simples, esta técnica é muito útil para:
- Rastrear o fluxo de execução
- Visualizar valores de variáveis em pontos críticos
- Identificar onde o código está falhando
'''

# Função com um bug para demonstrar o debugging
def calcular_media(lista_numeros):
    print(f"[DEBUG] Iniciando cálculo da média. Lista recebida: {lista_numeros}")
    
    # Bug proposital: não verifica se a lista está vazia
    soma = 0
    for numero in lista_numeros:
        print(f"[DEBUG] Processando número: {numero}")
        soma += numero
        print(f"[DEBUG] Soma atual: {soma}")
    
    media = soma / len(lista_numeros)  # Causará erro se lista_numeros estiver vazia
    print(f"[DEBUG] Média calculada: {media}")
    return media

# Função com verificação para evitar o bug
def calcular_media_segura(lista_numeros):
    print(f"\n[DEBUG] Iniciando cálculo seguro. Lista recebida: {lista_numeros}")
    
    # Verificação para evitar divisão por zero
    if not lista_numeros:  # Se a lista estiver vazia
        print("[DEBUG] Lista vazia detectada! Retornando None.")
        return None
    
    soma = 0
    for i, numero in enumerate(lista_numeros):
        print(f"[DEBUG] Processando item {i}: valor = {numero}")
        soma += numero
        print(f"[DEBUG] Soma após item {i}: {soma}")
    
    media = soma / len(lista_numeros)
    print(f"[DEBUG] Média calculada: {media}")
    return media

# Função que usa formatação mais elaborada para os prints de debug
def calcular_estatisticas(lista_numeros):
    print("\n" + "="*50)
    print("[INÍCIO] Calculando estatísticas da lista")
    print("-"*50)
    
    if not lista_numeros:
        print("[ERRO] Lista vazia detectada!")
        return None
    
    print(f"[INFO] Tamanho da lista: {len(lista_numeros)}")
    print(f"[INFO] Conteúdo da lista: {lista_numeros}")
    
    # Calculando estatísticas
    soma = sum(lista_numeros)
    media = soma / len(lista_numeros)
    maximo = max(lista_numeros)
    minimo = min(lista_numeros)
    
    print(f"[RESULTADO] Soma: {soma}")
    print(f"[RESULTADO] Média: {media}")
    print(f"[RESULTADO] Máximo: {maximo}")
    print(f"[RESULTADO] Mínimo: {minimo}")
    print("="*50)
    
    return {
        "soma": soma,
        "media": media,
        "maximo": maximo,
        "minimo": minimo
    }

# Demonstração de uso
if __name__ == "__main__":
    print("\n===== DEMONSTRAÇÃO DE PRINT DEBUGGING =====")
    
    # Exemplo 1: Função com bug
    print("\n>> Exemplo 1: Função com bug potencial")
    try:
        numeros = [10, 20, 30, 40, 50]
        print(f"Calculando média de {numeros}")
        resultado = calcular_media(numeros)
        print(f"Resultado: {resultado}")
        
        # Tentando com lista vazia (causará erro)
        print("\nTentando calcular média de lista vazia...")
        resultado = calcular_media([])
        print(f"Resultado: {resultado}")  # Esta linha não será executada devido ao erro
    except Exception as e:
        print(f"[ERRO CAPTURADO] {type(e).__name__}: {e}")
        print("O erro acima foi capturado graças aos prints de debug que nos ajudaram a identificar o problema!")
    
    # Exemplo 2: Função corrigida
    print("\n>> Exemplo 2: Função com verificação de segurança")
    numeros = [15, 25, 35, 45, 55]
    print(f"Calculando média segura de {numeros}")
    resultado = calcular_media_segura(numeros)
    print(f"Resultado: {resultado}")
    
    print("\nTentando calcular média segura de lista vazia...")
    resultado = calcular_media_segura([])
    print(f"Resultado: {resultado}")
    
    # Exemplo 3: Prints formatados
    print("\n>> Exemplo 3: Prints de debug formatados")
    numeros = [5, 10, 15, 20, 25]
    estatisticas = calcular_estatisticas(numeros)
    print(f"Estatísticas obtidas: {estatisticas}")
    
    print("\n===== DICAS PARA PRINT DEBUGGING =====")
    print("1. Use prefixos como [DEBUG], [INFO], [ERRO] para facilitar a identificação")
    print("2. Inclua informações de contexto nos prints (valores de variáveis, estado atual)")
    print("3. Use formatação visual (linhas, espaçamento) para melhorar a legibilidade")
    print("4. Remova ou desative os prints de debug antes de enviar para produção")
    print("5. Considere usar o módulo logging para casos mais complexos (veja 02_logging_debug.py)")