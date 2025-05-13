# Estratégia de Debugging: Testes Unitários

'''
Este script demonstra como usar testes unitários como estratégia de debugging:
- Criação de testes unitários com unittest
- Uso de assertions para verificar comportamentos esperados
- Identificação de bugs através de testes
- TDD (Test-Driven Development) como abordagem para prevenir bugs
'''

import unittest
import random

# Classe com funções a serem testadas (com bugs propositais)
class Calculadora:
    """Uma calculadora simples com operações básicas."""
    
    def somar(self, a, b):
        """Soma dois números."""
        return a + b
    
    def subtrair(self, a, b):
        """Subtrai b de a."""
        return a - b
    
    def multiplicar(self, a, b):
        """Multiplica dois números."""
        return a * b
    
    def dividir(self, a, b):
        """Divide a por b."""
        # Bug proposital: não verifica divisão por zero
        return a / b
    
    def media(self, numeros):
        """Calcula a média de uma lista de números."""
        # Bug proposital: não verifica lista vazia
        return sum(numeros) / len(numeros)
    
    def maior_valor(self, numeros):
        """Retorna o maior valor de uma lista."""
        if not numeros:  # Verifica se a lista está vazia
            return None
        
        # Bug proposital: implementação incorreta
        maior = numeros[0]
        # O bug está aqui: começa do índice 0 novamente
        for i in range(0, len(numeros)):
            # Deveria ser: for i in range(1, len(numeros)):
            if numeros[i] > maior:
                maior = numeros[i]
        return maior

# Classe de teste para a Calculadora
class TestCalculadora(unittest.TestCase):
    """Testes unitários para a classe Calculadora."""
    
    def setUp(self):
        """Método executado antes de cada teste."""
        self.calc = Calculadora()
        self.numeros_teste = [10, 5, 20, 15, 30]
    
    def test_somar(self):
        """Testa a função de soma."""
        self.assertEqual(self.calc.somar(5, 3), 8)
        self.assertEqual(self.calc.somar(-1, 1), 0)
        self.assertEqual(self.calc.somar(0, 0), 0)
    
    def test_subtrair(self):
        """Testa a função de subtração."""
        self.assertEqual(self.calc.subtrair(5, 3), 2)
        self.assertEqual(self.calc.subtrair(1, 5), -4)
        self.assertEqual(self.calc.subtrair(0, 0), 0)
    
    def test_multiplicar(self):
        """Testa a função de multiplicação."""
        self.assertEqual(self.calc.multiplicar(5, 3), 15)
        self.assertEqual(self.calc.multiplicar(-2, 3), -6)
        self.assertEqual(self.calc.multiplicar(0, 5), 0)
    
    def test_dividir(self):
        """Testa a função de divisão."""
        self.assertEqual(self.calc.dividir(6, 3), 2)
        self.assertEqual(self.calc.dividir(5, 2), 2.5)
        
        # Testando o bug de divisão por zero
        with self.assertRaises(ZeroDivisionError):
            self.calc.dividir(5, 0)
    
    def test_media(self):
        """Testa a função de média."""
        self.assertEqual(self.calc.media([2, 4, 6]), 4)
        self.assertEqual(self.calc.media([1, 2, 3, 4, 5]), 3)
        
        # Testando o bug de lista vazia
        with self.assertRaises(ZeroDivisionError):
            self.calc.media([])
    
    def test_maior_valor(self):
        """Testa a função de encontrar o maior valor."""
        # Teste básico
        self.assertEqual(self.calc.maior_valor([1, 5, 3]), 5)
        
        # Teste com lista vazia
        self.assertIsNone(self.calc.maior_valor([]))
        
        # Teste para verificar o bug (quando o maior valor não é o primeiro)
        # Este teste deve passar mesmo com o bug, pois o algoritmo ainda funciona
        # para este caso específico
        self.assertEqual(self.calc.maior_valor([1, 5, 3]), 5)
        
        # Teste que expõe o bug (quando o maior valor é o primeiro)
        # Este teste deve falhar devido ao bug na implementação
        self.assertEqual(self.calc.maior_valor([10, 5, 3]), 10)

# Versão corrigida da Calculadora
class CalculadoraCorrigida(Calculadora):
    """Versão corrigida da Calculadora, com os bugs consertados."""
    
    def dividir(self, a, b):
        """Divide a por b, com verificação de divisão por zero."""
        if b == 0:
            raise ValueError("Não é possível dividir por zero")
        return a / b
    
    def media(self, numeros):
        """Calcula a média de uma lista de números, com verificação de lista vazia."""
        if not numeros:
            raise ValueError("Não é possível calcular a média de uma lista vazia")
        return sum(numeros) / len(numeros)
    
    def maior_valor(self, numeros):
        """Retorna o maior valor de uma lista, implementação corrigida."""
        if not numeros:
            return None
        
        # Implementação corrigida
        return max(numeros)  # Usando a função built-in max

# Classe de teste para a CalculadoraCorrigida
class TestCalculadoraCorrigida(unittest.TestCase):
    """Testes unitários para a classe CalculadoraCorrigida."""
    
    def setUp(self):
        """Método executado antes de cada teste."""
        self.calc = CalculadoraCorrigida()
    
    def test_dividir(self):
        """Testa a função de divisão corrigida."""
        self.assertEqual(self.calc.dividir(6, 3), 2)
        self.assertEqual(self.calc.dividir(5, 2), 2.5)
        
        # Testando a verificação de divisão por zero
        with self.assertRaises(ValueError):
            self.calc.dividir(5, 0)
    
    def test_media(self):
        """Testa a função de média corrigida."""
        self.assertEqual(self.calc.media([2, 4, 6]), 4)
        
        # Testando a verificação de lista vazia
        with self.assertRaises(ValueError):
            self.calc.media([])
    
    def test_maior_valor(self):
        """Testa a função de encontrar o maior valor corrigida."""
        # Teste com o maior valor no início
        self.assertEqual(self.calc.maior_valor([10, 5, 3]), 10)
        
        # Teste com o maior valor no meio
        self.assertEqual(self.calc.maior_valor([5, 10, 3]), 10)
        
        # Teste com o maior valor no final
        self.assertEqual(self.calc.maior_valor([3, 5, 10]), 10)
        
        # Teste com lista vazia
        self.assertIsNone(self.calc.maior_valor([]))

# Exemplo de TDD (Test-Driven Development)
def demonstrar_tdd():
    """Demonstra o processo de TDD para criar uma nova função."""
    print("\n===== DEMONSTRAÇÃO DE TDD (TEST-DRIVEN DEVELOPMENT) =====")
    print("TDD segue o ciclo: Escrever teste → Executar teste (falha) → Implementar código → Executar teste (sucesso) → Refatorar")
    
    print("\n1. Primeiro, escrevemos um teste para a funcionalidade desejada:")
    print('''
    def test_ordenar_crescente(self):
        """Testa a função de ordenação crescente."""
        self.assertEqual(self.calc.ordenar_crescente([3, 1, 4, 2]), [1, 2, 3, 4])
        self.assertEqual(self.calc.ordenar_crescente([]), [])
    ''')
    
    print("\n2. Executamos o teste, que falha porque a função ainda não existe")
    
    print("\n3. Implementamos a função para passar no teste:")
    print('''
    def ordenar_crescente(self, numeros):
        """Ordena uma lista de números em ordem crescente."""
        return sorted(numeros)
    ''')
    
    print("\n4. Executamos o teste novamente, que agora deve passar")
    
    print("\n5. Refatoramos o código se necessário, mantendo os testes passando")

# Demonstração de uso
def executar_testes():
    """Executa os testes unitários."""
    # Criando um test suite com nossas classes de teste
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCalculadora))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCalculadoraCorrigida))
    
    # Executando os testes
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Analisando os resultados
    print(f"\nResultados dos testes:")
    print(f"Testes executados: {resultado.testsRun}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")
    
    # Mostrando detalhes das falhas
    if resultado.failures:
        print("\nDetalhes das falhas:")
        for i, (test, error) in enumerate(resultado.failures, 1):
            print(f"\nFalha {i}: {test}")
            print(f"Mensagem de erro: {error}")

if __name__ == "__main__":
    print("===== DEMONSTRAÇÃO DE TESTES UNITÁRIOS PARA DEBUGGING =====")
    
    print("\n>> Exemplo 1: Identificando bugs com testes unitários")
    print("Executando testes na classe Calculadora (com bugs)...")
    print("Observe que alguns testes falharão, indicando a presença de bugs.")
    
    # Executando os testes
    executar_testes()
    
    # Demonstração de TDD
    demonstrar_tdd()
    
    print("\n===== VANTAGENS DOS TESTES UNITÁRIOS PARA DEBUGGING =====")
    print("1. Identificam bugs de forma automática e repetível")
    print("2. Documentam o comportamento esperado do código")
    print("3. Facilitam a refatoração segura do código")
    print("4. Previnem regressões (bugs que reaparecem)")
    print("5. Permitem testar casos extremos e condições de erro")
    print("6. Incentivam um design de código mais modular e testável")
    
    print("\n===== DICAS PARA TESTES EFICAZES =====")
    print("1. Teste uma única funcionalidade por teste")
    print("2. Use nomes descritivos para os testes")
    print("3. Siga o padrão AAA: Arrange (preparar), Act (agir), Assert (verificar)")
    print("4. Teste casos normais, casos extremos e condições de erro")
    print("5. Mantenha os testes independentes entre si")
    print("6. Considere usar frameworks como pytest para testes mais avançados")