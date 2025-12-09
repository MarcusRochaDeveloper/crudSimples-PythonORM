import sys
import os
import bcrypt
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
from cryptography.fernet import Fernet


Base = declarative_base()

def carregar_ou_criar_chave():
    arquivo_chave = 'secret.key'
    if os.path.exists(arquivo_chave):
        with open(arquivo_chave, 'rb') as chave:
            return chave.read()
    else:
        chave = Fernet.generate_key()
        with open(arquivo_chave, 'wb') as chave_arquivo:
            chave_arquivo.write(chave)
        return chave

chave_global = carregar_ou_criar_chave()
cipher = Fernet(chave_global)

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    senha_encriptada = Column(String(255), nullable=False)

    tarefas = relationship("Tarefa", back_populates="usuario", cascade="all, delete-orphan")

class Tarefa(Base):
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(255))
    status = Column(Enum('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA', name='status_enum'), default='PENDENTE')

    usuario = relationship("Usuario", back_populates="tarefas")

def garantir_banco_existente(host, port, user, password, dbname):
    conexao = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        password=password
    )
    cursor = conexao.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
    conexao.commit()
    conexao.close()

def configurar_banco():
    print("\n--- Configuracao de Conexao ---")
    host = input("Host (ex: localhost): ")
    port = input("Porta (ex: 3306): ")
    user = input("Usuario (ex: root): ")
    password = input("Senha do Banco: ")
    dbname = input("Nome do Banco de Dados: ")

    garantir_banco_existente(host, port, user, password, dbname)

    try:
        url_conexao = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
        engine = create_engine(url_conexao)
        connection = engine.connect()
        connection.close()
        print("Conexao estabelecida com sucesso.")
        return engine
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        sys.exit()

def criar_usuario(session):
    nome = input("Digite o nome: ")
    email = input("Digite o email: ")
    senha_real = input("Digite a senha: ")

    usuario_existente = session.query(Usuario).filter_by(email=email).first()
    if usuario_existente:
        print("Usuario com este email ja existe.")
        return

    salt = bcrypt.gensalt()
    hash_gerado = bcrypt.hashpw(senha_real.encode('utf-8'), salt).decode('utf-8')

    token_encriptado = cipher.encrypt(senha_real.encode('utf-8')).decode('utf-8')

    novo_usuario = Usuario(
        nome=nome, 
        email=email, 
        senha_hash=hash_gerado,
        senha_encriptada=token_encriptado
    )
    
    try:
        session.add(novo_usuario)
        session.commit()
        print("Usuario criado com sucesso (Hash e Criptografia gerados).")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao criar usuario: {e}")

def listar_usuarios(session):
    usuarios = session.query(Usuario).all()
    print("\n--- Lista de Usuarios ---")
    print(f"{'ID':<5} | {'Nome':<20} | {'Senha Original (Decifrada)':<25} | {'Hash (Bcrypt)':<60}")
    print("-" * 120)
    
    for u in usuarios:
        try:
            senha_original = cipher.decrypt(u.senha_encriptada.encode('utf-8')).decode('utf-8')
        except Exception:
            senha_original = "Erro Decriptacao"
            
        print(f"{u.id:<5} | {u.nome:<20} | {senha_original:<25} | {u.senha_hash[:50]}...") 

def criar_tarefa(session):
    listar_usuarios(session) 
    try:
        usuario_id = int(input("\nDigite o ID do usuario dono da tarefa: "))
        usuario = session.query(Usuario).get(usuario_id)
        
        if not usuario:
            print("Usuario nao encontrado.")
            return

        titulo = input("Digite o titulo da tarefa: ")
        descricao = input("Digite a descricao da tarefa: ")
        status_input = input("Digite o status (PENDENTE/EM_ANDAMENTO/CONCLUIDA/CANCELADA): ").upper()

        valid_status = ['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA']
        status = status_input if status_input in valid_status else 'PENDENTE'

        nova_tarefa = Tarefa(usuario_id=usuario_id, titulo=titulo, descricao=descricao, status=status)
        
        session.add(nova_tarefa)
        session.commit()
        print("Tarefa criada com sucesso.")
    except ValueError:
        print("Entrada invalida.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao criar tarefa: {e}")

def listar_tarefas(session):
    tarefas = session.query(Tarefa).all()
    print("\n--- Lista de Tarefas ---")
    for t in tarefas:
        print(f"ID: {t.id} | Titulo: {t.titulo} | Status: {t.status} | Dono: {t.usuario.nome}")

def editar_tarefa(session):
    try:
        id_tarefa = int(input("Digite o ID da tarefa para editar: "))
        tarefa = session.query(Tarefa).get(id_tarefa)

        if not tarefa:
            print("Tarefa nao encontrada.")
            return

        novo_status = input("Digite o novo status (PENDENTE/EM_ANDAMENTO/CONCLUIDA/CANCELADA): ").upper()
        valid_status = ['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA']
        
        if novo_status in valid_status:
            tarefa.status = novo_status
            session.commit()
            print("Tarefa atualizada.")
        else:
            print("Status invalido.")
    except ValueError:
        print("ID invalido.")

def editar_usuario(session):
    email_atual = input("Digite o email do usuario para editar: ")
    usuario = session.query(Usuario).filter_by(email=email_atual).first()

    if not usuario:
        print("Usuario nao encontrado.")
        return

    novo_nome = input("Digite o novo nome: ")
    if novo_nome.strip():
        usuario.nome = novo_nome
        session.commit()
        print("Usuario atualizado.")
    else:
        print("Nome invalido.")

def deletar_tarefa(session):
    try:
        id_tarefa = int(input("Digite o ID da tarefa para deletar: "))
        tarefa = session.query(Tarefa).get(id_tarefa)
        if tarefa:
            session.delete(tarefa)
            session.commit()
            print("Tarefa deletada.")
        else:
            print("Tarefa nao encontrada.")
    except ValueError:
        print("ID invalido.")

def deletar_usuario(session):
    try:
        id_usuario = int(input("Digite o ID do usuario para deletar: "))
        usuario = session.query(Usuario).get(id_usuario)
        if usuario:
            session.delete(usuario)
            session.commit()
            print("Usuario deletado.")
        else:
            print("Usuario nao encontrado.")
    except ValueError:
        print("ID invalido.")

def exibir_menu():
    print("\n========== MENU ==========")
    print("1 - Criar Usuario")
    print("2 - Criar Tarefa")
    print("3 - Editar Tarefa")
    print("4 - Editar Usuario")
    print("5 - Ver Tarefas")
    print("6 - Ver Usuarios (Senha Real + Hash)")
    print("7 - Deletar Tarefa")
    print("8 - Deletar Usuario")
    print("0 - Sair")

def principal():
    engine = configurar_banco()
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        exibir_menu()
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            criar_usuario(session)
        elif escolha == '2':
            criar_tarefa(session)
        elif escolha == '3':
            editar_tarefa(session)
        elif escolha == '4':
            editar_usuario(session)
        elif escolha == '5':
            listar_tarefas(session)
        elif escolha == '6':
            listar_usuarios(session)
        elif escolha == '7':
            deletar_tarefa(session)
        elif escolha == '8':
            deletar_usuario(session)
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opcao invalida.")

    session.close()

if __name__ == "__main__":
    principal()
