# Exemplo de Métodos Especiais (Dunder Methods) em Python

# Os métodos especiais (também chamados de métodos dunder - double underscore)
# permitem que você personalize o comportamento de suas classes
# para operações internas do Python

class Produto:
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
    
    # Representação oficial do objeto (para desenvolvedores)
    def __repr__(self):
        return f"Produto('{self.nome}', {self.preco}, {self.quantidade})"
    
    # Representação em string do objeto (para usuários)
    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} ({self.quantidade} unidades)"
    
    # Permite usar o operador + para somar quantidades de produtos
    def __add__(self, outro):
        if isinstance(outro, Produto) and self.nome == outro.nome:
            return Produto(self.nome, self.preco, self.quantidade + outro.quantidade)
        elif isinstance(outro, int):
            return Produto(self.nome, self.preco, self.quantidade + outro)
        else:
            raise TypeError("Não é possível somar tipos incompatíveis")
    
    # Permite comparar produtos pelo preço usando <
    def __lt__(self, outro):
        if isinstance(outro, Produto):
            return self.preco < outro.preco
        return NotImplemented
    
    # Permite comparar produtos pelo preço usando ==
    def __eq__(self, outro):
        if isinstance(outro, Produto):
            return self.nome == outro.nome and self.preco == outro.preco
        return NotImplemented
    
    # Permite usar o operador len() para obter a quantidade
    def __len__(self):
        return self.quantidade
    
    # Permite usar o produto como um valor booleano
    def __bool__(self):
        return self.quantidade > 0
    
    # Permite acessar o produto como um dicionário
    def __getitem__(self, chave):
        if chave == 'nome':
            return self.nome
        elif chave == 'preco':
            return self.preco
        elif chave == 'quantidade':
            return self.quantidade
        else:
            raise KeyError(f"Chave '{chave}' não encontrada")

# Criando produtos
produto1 = Produto("Notebook", 3500.00, 5)
produto2 = Produto("Mouse", 120.00, 20)
produto3 = Produto("Notebook", 3500.00, 3)

# Demonstrando __str__ e __repr__
print(f"String: {produto1}")  # Usa __str__
print(f"Representação: {repr(produto1)}")  # Usa __repr__

# Demonstrando __add__
produto_somado = produto1 + produto3  # Soma produtos iguais
print(f"Após somar produtos: {produto_somado}")

produto_mais_unidades = produto2 + 10  # Adiciona unidades
print(f"Após adicionar unidades: {produto_mais_unidades}")

# Demonstrando __lt__ (menor que)
produtos = [produto1, produto2, produto3]
produtos_ordenados = sorted(produtos)  # Ordena por preço
print("\nProdutos ordenados por preço:")
for p in produtos_ordenados:
    print(f"  {p}")

# Demonstrando __eq__ (igual a)
print(f"\nproduto1 == produto3? {produto1 == produto3}")  # Mesmo nome e preço
produto3.preco = 3600.00
print(f"Após mudar o preço: produto1 == produto3? {produto1 == produto3}")  # Preço diferente

# Demonstrando __len__
print(f"\nQuantidade do produto1 (usando len): {len(produto1)}")

# Demonstrando __bool__
produto_vazio = Produto("Teclado", 150.00, 0)
print(f"produto1 tem estoque? {'Sim' if produto1 else 'Não'}")  # True, tem estoque
print(f"produto_vazio tem estoque? {'Sim' if produto_vazio else 'Não'}")  # False, sem estoque

# Demonstrando __getitem__
print(f"\nAcessando como dicionário: produto1['nome'] = {produto1['nome']}")
print(f"Acessando como dicionário: produto1['preco'] = {produto1['preco']}")

# Outros métodos especiais comuns incluem:
# __call__: Permite que o objeto seja chamado como uma função
# __iter__ e __next__: Para iteração
# __enter__ e __exit__: Para uso com o gerenciador de contexto (with)
# __getattr__, __setattr__: Para controlar acesso a atributos