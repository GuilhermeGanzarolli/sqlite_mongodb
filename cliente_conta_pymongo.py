
import pymongo as pym

client = pym.MongoClient("mongodb+srv://pymongo:")

# Criando o bando de dados

db = client.cliente_conta
collection = db.cliente_conta_collection

# Criando o documento

informacoes = [{
    "nome": "Guilherme",
    "cpf": "111.222.333-44",
    "endereco": "Rua Ferro Velho",
    "conta": "11111111-1",
    "agencia": "0001",
    "tipo": "Poupança",
    "saldo": 0
    },
    {"nome": "Willian",
     "cpf": "444.222.333-55",
     "endereco": "Rua Beira Lago",
     "conta": "11111333-1",
     "agencia": "0014",
     "tipo": "Corrente",
     "saldo": 0
     },
    {"nome": "Joana",
     "cpf": "555.222.777-99",
     "endereco": "Rua Canta Galo",
     "conta": "11174133-1",
     "agencia": "0010",
     "tipo": "Corrente",
     "saldo": 0
     },
    {"nome": "Patrick",
     "cpf": "555.888.111-99",
     "endereco": "Rua Bela Vista",
     "conta": "11174483-4",
     "agencia": "0003",
     "tipo": "Poupança",
     "saldo": 0
     }]

criar = db.contas
#enviar = criar.insert_many(informacoes)

print("Lista de usuários:")
for usuario in criar.find():
    print(usuario)

# Verificar quantos usuários tem dentro do banco
total = criar.count_documents({})
print(f"\nUsuários cadastrados -> {total}")

agencia = "0001"
# Retorna o(s) usuário(s) que estão na agencia 0001
print(f"\nUsuários da agência -> {agencia}")
for usuario in criar.find({"agencia": agencia}):
    print(usuario)


