# Estratégia de Debugging: Exceções

'''
Este script demonstra técnicas de debugging usando exceções:
- Captura e análise de exceções para identificar problemas
- Criação de exceções personalizadas para debugging
- Uso de try/except/finally para rastreamento de erros
- Técnicas para obter informações detalhadas sobre exceções
'''

import traceback
import sys

# Exceções personalizadas para facilitar o debugging
class ErroValidacaoDados(Exception):
    """Exceção lançada quando os dados não passam na validação."""
    def __init__(self, mensagem, dados=None):
        self.mensagem = mensagem
        self.dados = dados
        super().__init__(self.mensagem)
    
    def __str__(self):
        if self.dados:
            return f"{self.mensagem} - Dados problemáticos: {self.dados}"
        return self.mensagem

class ErroProcessamento(Exception):
    """Exceção lançada quando ocorre um erro durante o processamento."""
    def __init__(self, mensagem, operacao=None, detalhes=None):
        self.mensagem = mensagem
        self.operacao = operacao
        self.detalhes = detalhes
        super().__init__(self.mensagem)
    
    def __str__(self):
        resultado = self.mensagem
        if self.operacao:
            resultado += f" (durante operação: {self.operacao})"
        if self.detalhes:
            resultado += f"\nDetalhes: {self.detalhes}"
        return resultado

# Função que valida dados usando exceções para debugging
def validar_usuario(dados_usuario):
    """Valida os dados de um usuário."""
    try:
        # Verificando se todos os campos obrigatórios existem
        campos_obrigatorios = ["nome", "email", "idade"]
        for campo in campos_obrigatorios:
            if campo not in dados_usuario:
                raise ErroValidacaoDados(
                    f"Campo obrigatório ausente: {campo}", 
                    dados_usuario
                )
        
        # Validando o formato do email (simplificado)
        email = dados_usuario["email"]
        if "@" not in email or "." not in email:
            raise ErroValidacaoDados(
                "Formato de email inválido", 
                {"email": email}
            )
        
        # Validando a idade
        idade = dados_usuario["idade"]
        if not isinstance(idade, (int, float)):
            raise ErroValidacaoDados(
                "Idade deve ser um número", 
                {"idade": idade}
            )
        
        if idade < 0 or idade > 120:
            raise ErroValidacaoDados(
                "Idade fora do intervalo válido (0-120)", 
                {"idade": idade}
            )
        
        return True
    
    except ErroValidacaoDados as e:
        print(f"Erro de validação: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado durante validação: {type(e).__name__}: {e}")
        return False

# Função que usa exceções para debugging durante processamento
def processar_dados_usuario(dados_usuario):
    """Processa os dados de um usuário após validação."""
    try:
        # Primeiro validamos os dados
        if not validar_usuario(dados_usuario):
            return {"status": "erro", "mensagem": "Falha na validação de dados"}
        
        # Processamento dos dados
        try:
            # Simulando diferentes etapas de processamento
            # Etapa 1: Normalização
            nome_normalizado = dados_usuario["nome"].strip().title()
            
            # Etapa 2: Cálculo (com possível erro)
            try:
                # Bug proposital: divisão por zero se idade for zero
                fator_idade = 100 / dados_usuario["idade"]
            except ZeroDivisionError as e:
                # Capturando e re-lançando com mais contexto
                raise ErroProcessamento(
                    "Erro no cálculo do fator de idade",
                    "normalização",
                    f"Divisão por zero: {e}"
                )
            
            # Etapa 3: Transformação final
            resultado = {
                "usuario": nome_normalizado,
                "email": dados_usuario["email"].lower(),
                "fator_idade": fator_idade,
                "categoria": "adulto" if dados_usuario["idade"] >= 18 else "menor"
            }
            
            return {"status": "sucesso", "dados": resultado}
            
        except ErroProcessamento as e:
            # Capturando nossa exceção personalizada
            print(f"Erro de processamento: {e}")
            return {"status": "erro", "mensagem": str(e)}
        except Exception as e:
            # Capturando qualquer outra exceção e obtendo o traceback
            traceback_str = traceback.format_exc()
            print(f"Erro inesperado: {type(e).__name__}: {e}")
            print("Traceback:")
            print(traceback_str)
            return {"status": "erro", "mensagem": f"Erro interno: {str(e)}"}
    
    except Exception as e:
        # Capturando qualquer exceção não tratada
        print(f"Erro crítico: {type(e).__name__}: {e}")
        return {"status": "erro", "mensagem": "Erro crítico no sistema"}

# Função que demonstra como obter informações detalhadas de exceções
def demonstrar_info_excecao():
    """Demonstra como obter informações detalhadas sobre exceções."""
    try:
        # Provocando um erro
        lista = [1, 2, 3]
        valor = lista[10]  # IndexError
    except Exception as e:
        print("\n===== INFORMAÇÕES DETALHADAS DA EXCEÇÃO =====")
        print(f"Tipo da exceção: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        
        # Obtendo informações do traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("\nTraceback completo:")
        traceback_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print(''.join(traceback_lines))
        
        # Obtendo apenas a última linha do traceback
        print("\nÚltima linha do traceback:")
        print(traceback.format_exception_only(exc_type, exc_value)[0].strip())
        
        # Obtendo a pilha de chamadas
        print("\nPilha de chamadas:")
        for frame in traceback.extract_tb(exc_traceback):
            filename, line, func, text = frame
            print(f"  Arquivo: {filename}, Linha: {line}, Função: {func}")
            print(f"  Código: {text}")
            print()

# Demonstração de uso
if __name__ == "__main__":
    print("===== DEMONSTRAÇÃO DE DEBUGGING COM EXCEÇÕES =====")
    
    # Exemplo 1: Validação de dados com exceções personalizadas
    print("\n>> Exemplo 1: Validação com exceções personalizadas")
    
    # Dados válidos
    usuario_valido = {"nome": "Ana Silva", "email": "ana@exemplo.com", "idade": 30}
    print(f"Validando usuário válido: {usuario_valido}")
    resultado = validar_usuario(usuario_valido)
    print(f"Resultado da validação: {resultado}")
    
    # Dados inválidos - campo faltando
    usuario_invalido1 = {"nome": "João", "idade": 25}
    print(f"\nValidando usuário com campo faltando: {usuario_invalido1}")
    resultado = validar_usuario(usuario_invalido1)
    print(f"Resultado da validação: {resultado}")
    
    # Dados inválidos - email incorreto
    usuario_invalido2 = {"nome": "Maria", "email": "maria-exemplo", "idade": 22}
    print(f"\nValidando usuário com email inválido: {usuario_invalido2}")
    resultado = validar_usuario(usuario_invalido2)
    print(f"Resultado da validação: {resultado}")
    
    # Exemplo 2: Processamento com tratamento de exceções
    print("\n>> Exemplo 2: Processamento com tratamento de exceções")
    
    # Processamento normal
    print(f"Processando usuário válido: {usuario_valido}")
    resultado = processar_dados_usuario(usuario_valido)
    print(f"Resultado: {resultado}")
    
    # Processamento com erro (idade zero)
    usuario_problema = {"nome": "Carlos", "email": "carlos@exemplo.com", "idade": 0}
    print(f"\nProcessando usuário com idade zero: {usuario_problema}")
    resultado = processar_dados_usuario(usuario_problema)
    print(f"Resultado: {resultado}")
    
    # Exemplo 3: Informações detalhadas de exceções
    print("\n>> Exemplo 3: Obtendo informações detalhadas de exceções")
    demonstrar_info_excecao()
    
    print("\n===== DICAS PARA DEBUGGING COM EXCEÇÕES =====")
    print("1. Crie exceções personalizadas para diferentes tipos de erros")
    print("2. Inclua informações de contexto nas exceções (dados, operação, etc.)")
    print("3. Use try/except apenas em torno do código que pode falhar, não blocos inteiros")
    print("4. Capture exceções específicas em vez de usar 'except Exception' genérico")
    print("5. Use sys.exc_info() e traceback para obter informações detalhadas")
    print("6. Re-lance exceções com mais contexto quando necessário")
    print("7. Combine exceções com logging para um debugging mais eficaz")