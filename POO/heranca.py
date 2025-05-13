# Exemplo de Herança em Python

# A herança permite que uma classe (subclasse) herde atributos e métodos de outra classe (superclasse)
# Isso promove a reutilização de código e estabelece uma relação "é um" entre classes

# Classe base (superclasse)
class Animal:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
    
    def emitir_som(self):
        return "Som genérico de animal"
    
    def descricao(self):
        return f"{self.nome} é um animal com {self.idade} anos."

# Subclasse que herda de Animal
class Cachorro(Animal):
    def __init__(self, nome, idade, raca):
        # Chamando o construtor da classe pai
        super().__init__(nome, idade)
        self.raca = raca
    
    # Sobrescrevendo o método da classe pai
    def emitir_som(self):
        return "Au Au!"
    
    # Método específico da subclasse
    def abanar_rabo(self):
        return f"{self.nome} está abanando o rabo!"

# Outra subclasse que herda de Animal
class Gato(Animal):
    def __init__(self, nome, idade, cor):
        super().__init__(nome, idade)
        self.cor = cor
    
    def emitir_som(self):
        return "Miau!"
    
    def ronronar(self):
        return f"{self.nome} está ronronando..."

# Criando instâncias
animal = Animal("Animal Genérico", 5)
cachorro = Cachorro("Rex", 3, "Pastor Alemão")
gato = Gato("Mimi", 2, "Cinza")

# Demonstrando herança
print(animal.descricao())
print(cachorro.descricao())  # Método herdado da classe pai
print(gato.descricao())      # Método herdado da classe pai

# Demonstrando sobrescrita de métodos
print(f"Som do animal: {animal.emitir_som()}")
print(f"Som do cachorro: {cachorro.emitir_som()}")  # Método sobrescrito
print(f"Som do gato: {gato.emitir_som()}")          # Método sobrescrito

# Métodos específicos das subclasses
print(cachorro.abanar_rabo())
print(gato.ronronar())

# Verificando relações de herança
print(f"Cachorro é um Animal? {isinstance(cachorro, Animal)}")
print(f"Gato é um Animal? {isinstance(gato, Animal)}")
print(f"Animal é um Cachorro? {isinstance(animal, Cachorro)}")

# Herança múltipla (Python suporta)
class AnimalAquatico:
    def nadar(self):
        return "Nadando na água"

class Pato(Animal, AnimalAquatico):
    def __init__(self, nome, idade):
        Animal.__init__(self, nome, idade)
    
    def emitir_som(self):
        return "Quack!"

# Criando um pato que herda de duas classes
pato = Pato("Donald", 1)
print(pato.descricao())      # Método da classe Animal
print(pato.emitir_som())     # Método sobrescrito
print(pato.nadar())          # Método da classe AnimalAquatico