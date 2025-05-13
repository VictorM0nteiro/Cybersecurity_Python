# Estratégia de Debugging: PDB (Python Debugger)

'''
Este script demonstra o uso do debugger integrado do Python (pdb):
- Como inserir breakpoints no código
- Navegação pelo código durante a execução
- Inspeção de variáveis em tempo de execução
- Comandos úteis do pdb
'''

import pdb
import random

# Função com um bug para demonstrar o debugging
def encontrar_maior_valor(lista):
    '''
    Função que deveria encontrar o maior valor em uma lista.
    Contém um bug proposital para demonstração.
    '''
    if not lista:
        return None
    
    maior = lista[0]  # Inicializa com o primeiro elemento
    
    # Bug proposital: começa do índice 0 novamente, comparando o primeiro elemento com ele mesmo
    for i in range(0, len(lista)):
        # O correto seria: for i in range(1, len(lista)):
        if lista[i] > maior:
            maior = lista[i]
    
    return maior

# Função para demonstrar o uso de breakpoint()
def processar_lista(lista):
    '''
    Função que processa uma lista de números.
    Usada para demonstrar o uso de breakpoint().
    '''
    print(f"Processando lista: {lista}")
    
    # Em Python 3.7+, você pode usar a função breakpoint() em vez de pdb.set_trace()
    # Descomente a linha abaixo para ativar o breakpoint durante a execução
    # breakpoint()
    
    resultado = []
    for i, num in enumerate(lista):
        # Processamento simples
        valor_processado = num * 2
        resultado.append(valor_processado)
        
        # Outro lugar onde você poderia inserir um breakpoint condicional
        # if valor_processado > 50:
        #     breakpoint()
    
    return resultado

# Função com bug mais complexo para demonstrar debugging
def calcular_estatisticas(dados):
    '''
    Calcula estatísticas básicas de uma lista de dados.
    Contém bugs propositais para demonstração.
    '''
    if not dados:
        return {"erro": "Lista vazia"}
    
    # Calculando estatísticas
    try:
        # Bug 1: Não verifica se todos os itens são numéricos
        soma = sum(dados)
        media = soma / len(dados)
        
        # Bug 2: Ordenação incorreta para encontrar a mediana
        # O correto seria: sorted_data = sorted(dados)
        sorted_data = dados.copy()  # Não ordena os dados
        
        meio = len(sorted_data) // 2
        if len(sorted_data) % 2 == 0:
            # Bug 3: Cálculo incorreto da mediana para listas de tamanho par
            # O correto seria: mediana = (sorted_data[meio-1] + sorted_data[meio]) / 2
            mediana = sorted_data[meio]
        else:
            mediana = sorted_data[meio]
        
        return {
            "soma": soma,
            "media": media,
            "mediana": mediana,
            "min": min(dados),
            "max": max(dados)
        }
    except Exception as e:
        return {"erro": str(e)}

# Demonstração de uso do pdb
def demonstracao_pdb():
    print("\n===== DEMONSTRAÇÃO DO PDB (PYTHON DEBUGGER) =====")
    print("\nPara usar o PDB, você pode:")
    print("1. Inserir 'import pdb; pdb.set_trace()' no seu código")
    print("2. Usar a função 'breakpoint()' (Python 3.7+)")
    print("3. Executar seu script com 'python -m pdb seu_script.py'")
    
    print("\nQuando o debugger for ativado, você verá um prompt (Pdb) onde pode digitar comandos.")
    print("\nComandos úteis do PDB:")
    print("h (help)      - Mostra ajuda")
    print("n (next)      - Executa a próxima linha (sem entrar em funções)")
    print("s (step)      - Executa a próxima linha (entrando em funções)")
    print("c (continue)  - Continua a execução até o próximo breakpoint")
    print("q (quit)      - Sai do debugger")
    print("l (list)      - Mostra o código ao redor da linha atual")
    print("p expressão   - Avalia e imprime uma expressão")
    print("pp expressão  - Avalia e imprime uma expressão formatada")
    print("w (where)     - Mostra a pilha de chamadas atual")
    print("b linha       - Define um breakpoint na linha especificada")
    print("r (return)    - Continua até o return da função atual")
    
    # Exemplo prático
    print("\n>> Exemplo Prático:")
    print("Vamos demonstrar como usar o PDB para encontrar bugs.")
    
    # Criando dados de teste
    dados_teste = [random.randint(1, 100) for _ in range(8)]
    print(f"\nDados de teste: {dados_teste}")
    
    # Exemplo 1: Função com bug simples
    print("\n1. Função com bug simples:")
    maior = encontrar_maior_valor(dados_teste)
    print(f"Maior valor encontrado: {maior}")
    print("Para debugar esta função, você poderia inserir 'pdb.set_trace()' antes do loop for.")
    
    # Exemplo 2: Função com breakpoint()
    print("\n2. Função com breakpoint():")
    print("A função processar_lista() contém um breakpoint() comentado.")
    print("Descomente-o e execute novamente para iniciar o debugger naquele ponto.")
    resultado = processar_lista(dados_teste[:3])
    print(f"Resultado do processamento: {resultado}")
    
    # Exemplo 3: Função com bugs mais complexos
    print("\n3. Função com bugs mais complexos:")
    try:
        # Adicionando um valor não numérico para provocar erro
        dados_com_erro = dados_teste + ["texto"]
        estatisticas = calcular_estatisticas(dados_com_erro)
        print(f"Estatísticas calculadas: {estatisticas}")
    except Exception as e:
        print(f"Erro capturado: {type(e).__name__}: {e}")
        print("Este é um exemplo perfeito para usar o PDB e rastrear o erro!")
    
    print("\nPara debugar este código com PDB, você poderia:")
    print("1. Adicionar 'import pdb; pdb.set_trace()' antes da linha problemática")
    print("2. Executar o script com 'python -m pdb 03_pdb_debugger.py'")
    print("3. Usar o comando 'python -c "import 03_pdb_debugger; 03_pdb_debugger.calcular_estatisticas([1,2,'texto'])"'")

# Exemplo de como você poderia usar o PDB em um caso real
def exemplo_caso_real():
    print("\n===== EXEMPLO DE CASO REAL =====")
    print("Imagine que você está depurando um problema em produção.")
    print("Você pode adicionar código como este em pontos estratégicos:")
    print("""\ndef funcao_problematica(dados):
    # Código normal...
    
    # Quando uma condição específica ocorrer, ative o debugger
    if condicao_problematica:
        import pdb; pdb.set_trace()
        # ou: breakpoint()
    
    # Continue o código...
""")
    
    print("\nOu você pode usar o módulo 'remote-pdb' para depurar aplicações remotas:")
    print("""\nfrom remote_pdb import RemotePdb

def funcao_problematica(dados):
    # Quando o problema ocorrer, inicie um PDB remoto
    if condicao_problematica:
        RemotePdb('127.0.0.1', 4444).set_trace()
    
    # Continue o código...
""")
    print("Isso iniciará um servidor PDB na porta 4444 que você pode acessar remotamente.")

# Demonstração de uso
if __name__ == "__main__":
    # Demonstração principal do PDB
    demonstracao_pdb()
    
    # Exemplo de caso real
    exemplo_caso_real()
    
    print("\n===== DICAS PARA USAR O PDB EFETIVAMENTE =====")
    print("1. Use 'p' e 'pp' para inspecionar variáveis durante a depuração")
    print("2. Use 'n' para executar linha a linha e 's' para entrar em funções")
    print("3. Defina breakpoints condicionais com 'b linha, condição'")
    print("4. Use 'w' para ver a pilha de chamadas quando estiver perdido")
    print("5. Combine PDB com outras técnicas como logging para debugging eficaz")
    print("\nLembre-se: O PDB é uma ferramenta poderosa que permite interagir com seu código durante a execução!")