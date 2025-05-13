# Exemplo de Classe Básica em Python

# Em Python, uma classe é definida usando a palavra-chave 'class'
class Pessoa:
    # O método __init__ é o construtor da classe
    # self representa a instância da classe (similar ao 'this' em outras linguagens)
    def __init__(self, nome, idade):
        # Atributos da classe
        self.nome = nome
        self.idade = idade
    
    # Métodos da classe
    def apresentar(self):
        return f"Olá, meu nome é {self.nome} e tenho {self.idade} anos."
    
    def fazer_aniversario(self):
        self.idade += 1
        return f"{self.nome} agora tem {self.idade} anos."

# Criando objetos (instâncias) da classe Pessoa
pessoa1 = Pessoa("Maria", 30)
pessoa2 = Pessoa("João", 25)

# Acessando atributos
print(f"Nome da pessoa1: {pessoa1.nome}")
print(f"Idade da pessoa1: {pessoa1.idade}")

# Chamando métodos
print(pessoa1.apresentar())
print(pessoa2.apresentar())

# Modificando atributos
pessoa1.nome = "Maria Silva"
print(pessoa1.apresentar())

# Chamando outro método
print(pessoa1.fazer_aniversario())

# Demonstração de múltiplas instâncias independentes
print(f"Idade da pessoa1: {pessoa1.idade}")
print(f"Idade da pessoa2: {pessoa2.idade}")