# Estratégia de Debugging: Profiling

'''
Este script demonstra técnicas de profiling para debugging:
- Identificação de gargalos de performance
- Uso do módulo cProfile para análise de tempo de execução
- Uso do módulo time para medições simples
- Análise de complexidade de algoritmos
- Otimização de código com base em dados de profiling
'''

import cProfile
import pstats
import io
import time
import random
import os

# Diretório para armazenar resultados de profiling
PROFILE_DIR = "profile_results"
if not os.path.exists(PROFILE_DIR):
    os.mkdir(PROFILE_DIR)

# Função ineficiente para demonstrar profiling
def ordenar_ineficiente(lista):
    """Implementação ineficiente de ordenação (bubble sort)."""
    n = len(lista)
    lista_copia = lista.copy()  # Trabalhamos com uma cópia para não modificar a original
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_copia[j] > lista_copia[j + 1]:
                lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
    
    return lista_copia

# Função eficiente para comparação
def ordenar_eficiente(lista):
    """Implementação eficiente de ordenação (usando sorted())."""
    return sorted(lista)

# Função com um gargalo de performance
def encontrar_duplicatas_ineficiente(lista):
    """Encontra números duplicados em uma lista (implementação ineficiente)."""
    duplicatas = []
    
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            # Comparação O(n²)
            if lista[i] == lista[j] and lista[i] not in duplicatas:
                duplicatas.append(lista[i])
    
    return duplicatas

# Versão otimizada da função acima
def encontrar_duplicatas_eficiente(lista):
    """Encontra números duplicados em uma lista (implementação eficiente)."""
    vistos = set()
    duplicatas = set()
    
    for item in lista:
        if item in vistos:
            duplicatas.add(item)
        else:
            vistos.add(item)
    
    return list(duplicatas)

# Função que realiza várias operações para demonstrar profiling
def processar_dados(tamanho, usar_eficiente=False):
    """Processa uma lista de dados, demonstrando diferentes operações."""
    # Gerando dados aleatórios
    dados = [random.randint(1, tamanho // 2) for _ in range(tamanho)]
    
    # Operação 1: Ordenação
    if usar_eficiente:
        dados_ordenados = ordenar_eficiente(dados)
    else:
        dados_ordenados = ordenar_ineficiente(dados)
    
    # Operação 2: Encontrar duplicatas
    if usar_eficiente:
        duplicatas = encontrar_duplicatas_eficiente(dados)
    else:
        duplicatas = encontrar_duplicatas_ineficiente(dados)
    
    # Operação 3: Cálculos estatísticos
    soma = sum(dados)
    media = soma / len(dados)
    maximo = max(dados)
    minimo = min(dados)
    
    return {
        "ordenados": dados_ordenados[:10],  # Primeiros 10 elementos
        "duplicatas": duplicatas[:10] if len(duplicatas) > 10 else duplicatas,  # Até 10 duplicatas
        "estatisticas": {
            "soma": soma,
            "media": media,
            "maximo": maximo,
            "minimo": minimo
        }
    }

# Função para demonstrar profiling simples com time
def demonstrar_profiling_simples():
    """Demonstra profiling simples usando o módulo time."""
    print("\n===== PROFILING SIMPLES COM TIME =====")
    
    tamanhos = [100, 1000, 5000]
    
    for tamanho in tamanhos:
        print(f"\nProcessando lista de tamanho {tamanho}:")
        
        # Versão ineficiente
        inicio = time.time()
        processar_dados(tamanho, usar_eficiente=False)
        fim = time.time()
        print(f"  Versão ineficiente: {fim - inicio:.6f} segundos")
        
        # Versão eficiente
        inicio = time.time()
        processar_dados(tamanho, usar_eficiente=True)
        fim = time.time()
        print(f"  Versão eficiente: {fim - inicio:.6f} segundos")

# Função para demonstrar profiling detalhado com cProfile
def demonstrar_profiling_detalhado():
    """Demonstra profiling detalhado usando cProfile."""
    print("\n===== PROFILING DETALHADO COM CPROFILE =====")
    
    # Profiling da versão ineficiente
    print("\nProfiler para versão ineficiente:")
    pr = cProfile.Profile()
    pr.enable()
    
    # Executando a função que queremos analisar
    processar_dados(1000, usar_eficiente=False)
    
    pr.disable()
    
    # Formatando e exibindo os resultados
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(15)  # Mostra as 15 funções que mais consumiram tempo
    print(s.getvalue())
    
    # Salvando os resultados em um arquivo
    arquivo_resultado = os.path.join(PROFILE_DIR, "profile_ineficiente.txt")
    with open(arquivo_resultado, 'w') as f:
        ps = pstats.Stats(pr, stream=f).sort_stats('cumulative')
        ps.print_stats()
    print(f"Resultados completos salvos em: {arquivo_resultado}")
    
    # Profiling da versão eficiente
    print("\nProfiler para versão eficiente:")
    pr = cProfile.Profile()
    pr.enable()
    
    # Executando a função otimizada
    processar_dados(1000, usar_eficiente=True)
    
    pr.disable()
    
    # Formatando e exibindo os resultados
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(15)  # Mostra as 15 funções que mais consumiram tempo
    print(s.getvalue())
    
    # Salvando os resultados em um arquivo
    arquivo_resultado = os.path.join(PROFILE_DIR, "profile_eficiente.txt")
    with open(arquivo_resultado, 'w') as f:
        ps = pstats.Stats(pr, stream=f).sort_stats('cumulative')
        ps.print_stats()
    print(f"Resultados completos salvos em: {arquivo_resultado}")

# Função para demonstrar profiling de funções específicas
def demonstrar_profiling_funcoes():
    """Demonstra profiling de funções específicas."""
    print("\n===== PROFILING DE FUNÇÕES ESPECÍFICAS =====")
    
    # Gerando uma lista grande com alguns números duplicados
    tamanho = 5000
    dados = [random.randint(1, tamanho // 2) for _ in range(tamanho)]
    
    # Profiling da função de encontrar duplicatas (versão ineficiente)
    print("\nProfiler para encontrar_duplicatas_ineficiente:")
    inicio = time.time()
    cProfile.runctx('encontrar_duplicatas_ineficiente(dados)', globals(), locals())
    fim = time.time()
    print(f"Tempo total: {fim - inicio:.6f} segundos")
    
    # Profiling da função de encontrar duplicatas (versão eficiente)
    print("\nProfiler para encontrar_duplicatas_eficiente:")
    inicio = time.time()
    cProfile.runctx('encontrar_duplicatas_eficiente(dados)', globals(), locals())
    fim = time.time()
    print(f"Tempo total: {fim - inicio:.6f} segundos")

# Função para demonstrar análise de complexidade
def demonstrar_analise_complexidade():
    """Demonstra análise de complexidade de algoritmos."""
    print("\n===== ANÁLISE DE COMPLEXIDADE DE ALGORITMOS =====")
    
    tamanhos = [100, 500, 1000, 2000, 5000]
    
    print("\nAnálise de ordenação:")
    print("Tamanho | Ineficiente (s) | Eficiente (s) | Razão")
    print("-" * 60)
    
    for tamanho in tamanhos:
        # Gerando dados
        dados = [random.randint(1, 10000) for _ in range(tamanho)]
        
        # Medindo tempo da versão ineficiente
        inicio = time.time()
        ordenar_ineficiente(dados)
        tempo_ineficiente = time.time() - inicio
        
        # Medindo tempo da versão eficiente
        inicio = time.time()
        ordenar_eficiente(dados)
        tempo_eficiente = time.time() - inicio
        
        # Calculando a razão entre os tempos
        razao = tempo_ineficiente / tempo_eficiente if tempo_eficiente > 0 else float('inf')
        
        print(f"{tamanho:7d} | {tempo_ineficiente:15.6f} | {tempo_eficiente:13.6f} | {razao:5.1f}x")
    
    print("\nAnálise de busca de duplicatas:")
    print("Tamanho | Ineficiente (s) | Eficiente (s) | Razão")
    print("-" * 60)
    
    for tamanho in tamanhos:
        # Gerando dados com duplicatas garantidas
        dados = [random.randint(1, tamanho // 2) for _ in range(tamanho)]
        
        # Medindo tempo da versão ineficiente
        inicio = time.time()
        encontrar_duplicatas_ineficiente(dados)
        tempo_ineficiente = time.time() - inicio
        
        # Medindo tempo da versão eficiente
        inicio = time.time()
        encontrar_duplicatas_eficiente(dados)
        tempo_eficiente = time.time() - inicio
        
        # Calculando a razão entre os tempos
        razao = tempo_ineficiente / tempo_eficiente if tempo_eficiente > 0 else float('inf')
        
        print(f"{tamanho:7d} | {tempo_ineficiente:15.6f} | {tempo_eficiente:13.6f} | {razao:5.1f}x")

# Demonstração de uso
if __name__ == "__main__":
    print("===== DEMONSTRAÇÃO DE PROFILING PARA DEBUGGING =====")
    print("O profiling é uma técnica de debugging que ajuda a identificar gargalos de performance.")
    
    # Demonstração de profiling simples
    demonstrar_profiling_simples()
    
    # Demonstração de profiling detalhado
    demonstrar_profiling_detalhado()
    
    # Demonstração de profiling de funções específicas
    demonstrar_profiling_funcoes()
    
    # Demonstração de análise de complexidade
    demonstrar_analise_complexidade()
    
    print("\n===== DICAS PARA PROFILING EFICAZ =====")
    print("1. Comece com medições simples para identificar áreas problemáticas")
    print("2. Use cProfile para análise detalhada de funções críticas")
    print("3. Analise tanto o tempo total quanto o número de chamadas de função")
    print("4. Compare diferentes implementações para identificar otimizações")
    print("5. Considere a complexidade algorítmica (O(n), O(n²), etc.) ao analisar performance")
    print("6. Otimize apenas o código que realmente precisa ser otimizado (gargalos)")
    print("7. Use ferramentas como line_profiler para análise linha a linha de funções críticas")
    print("8. Combine profiling com logging para identificar padrões de uso que causam lentidão")
    
    print(f"\nResultados detalhados de profiling foram salvos no diretório: {PROFILE_DIR}")