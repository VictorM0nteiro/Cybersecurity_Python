# Exemplo de Encapsulamento em Python

# O encapsulamento é um dos princípios fundamentais da POO
# Ele permite esconder detalhes internos da implementação de uma classe

class ContaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular        # Atributo público
        self.__saldo = saldo_inicial  # Atributo privado (com prefixo __)
        self._limite = 1000           # Atributo protegido (convenção, com prefixo _)
    
    # Métodos getter e setter para acessar e modificar o saldo de forma controlada
    def get_saldo(self):
        return self.__saldo
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return f"Depósito de R${valor} realizado com sucesso."
        return "Valor de depósito inválido."
    
    def sacar(self, valor):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            return f"Saque de R${valor} realizado com sucesso."
        return "Saldo insuficiente ou valor inválido."
    
    # Property - forma mais pythônica de implementar getters e setters
    @property
    def limite(self):
        return self._limite
    
    @limite.setter
    def limite(self, novo_limite):
        if novo_limite >= 0:
            self._limite = novo_limite
        else:
            print("Limite não pode ser negativo.")

# Criando uma conta
conta = ContaBancaria("Ana Silva", 1500)

# Acessando atributo público
print(f"Titular: {conta.titular}")

# Tentando acessar atributo privado diretamente causaria erro
# print(conta.__saldo)  # Isso geraria um AttributeError

# Forma correta de acessar o saldo (através do método getter)
print(f"Saldo atual: R${conta.get_saldo()}")

# Realizando operações na conta
print(conta.depositar(500))
print(f"Novo saldo: R${conta.get_saldo()}")

print(conta.sacar(200))
print(f"Saldo após saque: R${conta.get_saldo()}")

# Usando property para acessar e modificar o limite
print(f"Limite atual: R${conta.limite}")
conta.limite = 2000
print(f"Novo limite: R${conta.limite}")

# Tentando definir um limite inválido
conta.limite = -500  # Isso imprimirá a mensagem de erro

# Python não impede realmente o acesso a atributos privados
# É possível acessar usando name mangling (_NomeClasse__atributo)
print(f"Acessando atributo privado (não recomendado): R${conta._ContaBancaria__saldo}")