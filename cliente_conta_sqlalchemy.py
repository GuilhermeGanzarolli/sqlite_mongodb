from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column, func
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DECIMAL
from sqlalchemy import select

BASE = declarative_base()

class Cliente(BASE):
    __tablename__ = 'cliente'
    # Atributos
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50))
    cpf = Column(String(14))
    endereco = Column(String(70))
    conta = relationship(
        "Conta", back_populates = "cliente"
    )

    def __repr__(self):
        return f"Cliente(id = {self.id}, nome = {self.nome}, cpf = {self.cpf}, endereco = {self.endereco})"


class Conta(BASE):
    __tablename__ = 'conta'
    # Atributos
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(DECIMAL)
    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo = {self.saldo})"


#=======================================================================================================================
# Conexão com o banco de dados

engine = create_engine("sqlite://")

BASE.metadata.create_all(engine)

consulta = inspect(engine)

#Buscando nome das tabelas
print(f"Nome das tabelas = {consulta.get_table_names()}")

#Qual a chave estrangeira
print(consulta.get_foreign_keys('conta'))

#Consulta de existe uma tabela com este nome
tabela = 'cliente'
print(f"Existe a tabela {tabela} -> {consulta.has_table('cliente')}")

#=======================================================================================================================
# Inserindo dados no banco de dados

with Session(engine) as session:
    cristofer = Cliente(
        nome = "cristofer",
        cpf = "111.222.333-44",
        endereco = "Rua Ferro Velho",
        conta = [
            Conta(
            tipo="Conta Corrente",
            agencia = "002",
            num = 1111,
            saldo = 0
        ),
            Conta(
                tipo="Conta Poupança",
                agencia="002",
                num=1112,
                saldo=0
            )
        ]
    )

    estefani = Cliente(
        nome = "estefani",
        cpf = "555.222.777-99",
        endereco = "Rua Novo Lago",
    )

    julio = Cliente(
        nome = "julio",
        cpf = "123.456.789-98",
        endereco = "Rua Queda D'agua",
        conta = [
            Conta(
            tipo="Conta Corrente",
            agencia = "003",
            num = 1118,
            saldo = 0
        )]
    )

    session.add_all([cristofer, estefani, julio])
    session.commit()

#=======================================================================================================================
# Consultar as informações que foram percistidas
print("="*60)

stmt_Cliente = select(Cliente).where(Cliente.nome.in_(["cristofer", "julio", "estefani"]))

for usuarios in session.scalars(stmt_Cliente):
    print(usuarios)

stmt_Conta = select(Conta).where(Conta.id_cliente.in_([1]))

for conta in session.scalars(stmt_Conta):
    print(conta)

stmt_nome_desc = select(Cliente.nome).order_by(Cliente.nome.desc())

for result in session.scalars(stmt_nome_desc):
    print(result)

stmt_join = select(Cliente.nome, Conta.tipo).join_from(Conta, Cliente)

connection = engine.connect()
resultados = connection.execute(stmt_join).fetchall()

for resultado in resultados:
    print(resultado)


stmt_n_contas = select(func.count("*")).select_from(Cliente)
for result in session.scalars(stmt_n_contas):
    print(result)