# Exemplo de Composição em Python

# A composição é um tipo de associação onde uma classe contém objetos de outras classes
# Representa uma relação "tem um" entre classes

# Classe que será usada na composição
class Motor:
    def __init__(self, tipo, potencia):
        self.tipo = tipo
        self.potencia = potencia
    
    def ligar(self):
        return f"Motor {self.tipo} de {self.potencia}cv ligado!"
    
    def desligar(self):
        return f"Motor {self.tipo} desligado."

# Classe que será usada na composição
class Roda:
    def __init__(self, aro):
        self.aro = aro
    
    def girar(self):
        return f"Roda aro {self.aro} girando."

# Classe principal que usa composição
class Carro:
    def __init__(self, modelo, cor, tipo_motor, potencia_motor):
        self.modelo = modelo
        self.cor = cor
        # Composição: Carro tem um Motor
        self.motor = Motor(tipo_motor, potencia_motor)
        # Composição: Carro tem quatro Rodas
        self.rodas = [Roda(17) for _ in range(4)]
    
    def ligar_carro(self):
        return f"{self.modelo} {self.cor}: {self.motor.ligar()}"
    
    def desligar_carro(self):
        return f"{self.modelo} {self.cor}: {self.motor.desligar()}"
    
    def mover(self):
        rodas_girando = [roda.girar() for roda in self.rodas]
        return f"{self.modelo} em movimento com as 4 rodas girando."

# Outro exemplo de composição
class Endereco:
    def __init__(self, rua, numero, cidade, estado):
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.estado = estado
    
    def endereco_completo(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

class Cliente:
    def __init__(self, nome, email, rua, numero, cidade, estado):
        self.nome = nome
        self.email = email
        # Composição: Cliente tem um Endereco
        self.endereco = Endereco(rua, numero, cidade, estado)
    
    def info_cliente(self):
        return f"Cliente: {self.nome}\nEmail: {self.email}\nEndereço: {self.endereco.endereco_completo()}"

# Criando um carro usando composição
meu_carro = Carro("Fusca", "Azul", "Gasolina", 1600)

# Usando os métodos que internamente usam os objetos compostos
print(meu_carro.ligar_carro())
print(meu_carro.mover())
print(meu_carro.desligar_carro())

# Acessando diretamente o objeto composto
print(f"Tipo do motor: {meu_carro.motor.tipo}")
print(f"Aro das rodas: {meu_carro.rodas[0].aro}")

# Criando um cliente usando composição
cliente = Cliente(
    "Maria Silva", 
    "maria@email.com", 
    "Rua das Flores", 
    123, 
    "São Paulo", 
    "SP"
)

# Exibindo informações do cliente
print("\n" + cliente.info_cliente())

# Acessando diretamente o objeto composto
print(f"Cidade do cliente: {cliente.endereco.cidade}")

# Diferença entre composição e herança:
# - Na herança, uma classe é um tipo de outra classe (relação "é um")
# - Na composição, uma classe contém objetos de outra classe (relação "tem um")