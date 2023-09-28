from mongoengine import Document, StringField, IntField, FloatField, connect, ListField, ReferenceField


# Nada aqui é obrigatório, apenas para facilitar o entendimento
# Função para conectar ao banco de dados
def conectar_banco_dados():
    try:
        uri = "mongodb+srv://felipe:senha@projetodb2.do1ihit.mongodb.net/test?retryWrites=true&w=majority"
        connect(host=uri, alias='default')
        print("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print("Erro ao conectar ao banco de dados: ", e)

# Definindo os modelos (esquemas)
# Definindo o esquema do produto
class Produto(Document):
    nome = StringField(required=True)
    preco = FloatField()
    descricao = StringField()

# Definindo o esquema do usuário
class Usuario(Document):
    nome = StringField(required=True)
    idade = IntField()
    email = StringField()
    produtos = ListField(ReferenceField(Produto))  # Lista de referências para produtos

# Função para criar os esquemas
def criar_esquemas():
    
    try:
        # Criando os índices se necessário (opcional)
        Usuario.create_index([('nome', 1)], unique=False)
        Produto.create_index([('nome', 1)], unique=False)
        bdcriado=True
        print("Esquemas criados com sucesso!\n")
    except Exception as e:
        print("Erro ao criar os esquemas: \n", e)

def inserir_dados():
    # Inserindo um produto
    produto1 = Produto(nome='Celular', preco=1000.0, descricao='Um celular novo')
    produto1.save()

    # Inserindo um usuário com produtos relacionados
    produto2 = Produto(nome='Notebook', preco=2500.0, descricao='Um notebook potente')
    produto2.save()

    usuario1 = Usuario(nome='Maria', idade=30, email='joao@example.com', produtos=[produto1, produto2])
    usuario1.save()

    print("Dados inseridos com sucesso!\n")

def ler_dados():
    # Lendo todos os produtos
    produtos = Produto.objects()
    for produto in produtos:
        print(f"Produto: {produto.nome}, Preço: {produto.preco}, Descrição: {produto.descricao}")
    """
    SELECT nome, preco, descricao FROM Produto;
    """
    # Lendo todos os usuários
    usuarios = Usuario.objects()
    for usuario in usuarios:
        print(f"Usuário: {usuario.nome}, Idade: {usuario.idade}, Email: {usuario.email}")
        print("Produtos:")
        for produto in usuario.produtos:
            print(f"  - {produto.nome}")
    print("\n")
    """
    SELECT Usuario.nome, Usuario.idade, Usuario.email, Produto.nome AS nome_produto
    FROM Usuario
    LEFT JOIN Produto ON Usuario._id = Produto.produtos_id;
    """


def atualizar_dados():
    # Atualizando o nome e o preço de um produto específico
    produto = Produto.objects(nome='Celular').first()
    if produto:
        produto.nome = 'Smartphone'
        produto.preco = 1200.0
        produto.descricao = 'Um Smartphone de última geração'
        produto.save()
    """
    UPDATE produtos
    SET nome = 'Smartphone', preco = 1200.0
    WHERE nome = 'Celular';
    """

    # Atualizando o nome de um usuário específico
    usuario = Usuario.objects(nome='Maria').first()
    if usuario:
        usuario.nome = 'João Silva'
        usuario.save()

    print("Dados atualizados com sucesso!")

def deletar_dados():
    # Deletando um produto específico
    produto = Produto.objects(nome='Notebook').first()
    if produto:
        produto.delete()

    """
    DELETE FROM produtos
    WHERE nome = 'Notebook';

    """

    # Deletando um usuário específico
    usuario = Usuario.objects(nome='João Silva').first()
    if usuario:
        usuario.delete()
    
    """
    DELETE FROM usuarios
    WHERE nome = 'João Silva';

    """
    print("Dados deletados com sucesso!\n")

if __name__ == "__main__":
    conectar_banco_dados()
    opt = -1
    esquema = 0
    while opt != 0:
        print("1 - Criar esquemas")
        print("2 - Inserir dados")
        print("3 - Ler dados")
        print("4 - Atualizar dados")
        print("5 - Deletar dados")
        print("0 - Sair")
        opt = int(input("Digite a opção desejada: "))
        if opt == 1:
            if esquema == False:
                esquema = True
                criar_esquemas()
            else:
                print("Esquemas já criados!")
        elif opt == 2:
            inserir_dados()
            
        elif opt == 3:
            ler_dados()
        elif opt == 4:
            atualizar_dados()
            
        elif opt == 5:
            deletar_dados()
            
        elif opt == 0:
            print("Saindo...")
