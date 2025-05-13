# Exemplo de Polimorfismo em Python

# O polimorfismo permite que objetos de diferentes classes sejam tratados de maneira uniforme
# Isso ocorre quando classes diferentes implementam métodos com o mesmo nome

# Definindo uma classe base
class Forma:
    def __init__(self, nome):
        self.nome = nome
    
    def calcular_area(self):
        # Método a ser sobrescrito pelas subclasses
        pass
    
    def descricao(self):
        return f"Esta é uma forma chamada {self.nome}"

# Subclasses que implementam o método calcular_area de formas diferentes
class Retangulo(Forma):
    def __init__(self, largura, altura):
        super().__init__("Retângulo")
        self.largura = largura
        self.altura = altura
    
    def calcular_area(self):
        return self.largura * self.altura

class Circulo(Forma):
    def __init__(self, raio):
        super().__init__("Círculo")
        self.raio = raio
    
    def calcular_area(self):
        import math
        return math.pi * (self.raio ** 2)

class Triangulo(Forma):
    def __init__(self, base, altura):
        super().__init__("Triângulo")
        self.base = base
        self.altura = altura
    
    def calcular_area(self):
        return (self.base * self.altura) / 2

# Função que demonstra polimorfismo
def imprimir_area(forma):
    # Esta função aceita qualquer objeto que tenha o método calcular_area
    # Demonstrando o polimorfismo - mesmo método, comportamentos diferentes
    print(f"A área da {forma.nome} é: {forma.calcular_area():.2f}")

# Criando instâncias de diferentes formas
retangulo = Retangulo(5, 4)
circulo = Circulo(3)
triangulo = Triangulo(6, 8)

# Chamando a mesma função com diferentes objetos
imprimir_area(retangulo)  # Usa o método calcular_area do Retangulo
imprimir_area(circulo)    # Usa o método calcular_area do Circulo
imprimir_area(triangulo)  # Usa o método calcular_area do Triangulo

# Armazenando objetos diferentes em uma lista
formas = [retangulo, circulo, triangulo]

# Iterando sobre a lista e chamando o mesmo método em cada objeto
print("\nCalculando áreas de todas as formas:")
for forma in formas:
    imprimir_area(forma)

# Outro exemplo de polimorfismo com duck typing
class Pato:
    def falar(self):
        return "Quack!"
    
    def andar(self):
        return "Andando como um pato"

class Pessoa:
    def falar(self):
        return "Olá!"
    
    def andar(self):
        return "Andando como uma pessoa"

# Função que demonstra duck typing
def fazer_barulho(objeto):
    # Se o objeto tem um método falar, podemos chamá-lo
    # Não importa qual é a classe do objeto
    print(objeto.falar())

# Usando a função com diferentes objetos
pato = Pato()
pessoa = Pessoa()

print("\nDemonstrando duck typing:")
fazer_barulho(pato)    # Chama pato.falar()
fazer_barulho(pessoa)  # Chama pessoa.falar()