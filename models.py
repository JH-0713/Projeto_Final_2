# importar Biblioteca
from jinja2.lexer import integer_re
from sqlalchemy import Column, DateTime, func ,ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# Coneção banco de Dados
engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/cinema')

# Configura Seções locais
local_secao = sessionmaker(bind=engine)

# Formato de Efetuação
Base = declarative_base()

# Base
class Ator(Base):
    __tablename__ = 'autores'
    id_ator = Column(Integer, primary_key=True)
    nome_ator = Column(String(150), nullable=False)
    biografia = Column(String(255), nullable=False)
    papel_interpretado = Column(String(255), nullable=False)
    def __repr__(self):
        return (f'<Ator {self.nome_ator}, biografia: {self.biografia},papel_interpretado: {self.papel_interpretado} >')

class Genero(Base):
    __tablename__ = 'generos'
    id_genero = Column(Integer, primary_key=True)
    nome_genero = Column(String(50), nullable=False)
    descricao = Column(String(255), nullable=False)
    def __repr__(self):
        return (f'<Genero {self.nome_genero}, Descricao: {self.descricao}>')

class Diretor(Base):
    __tablename__ = 'diretores'
    id_diretor = Column(Integer, primary_key=True)
    nome_diretor = Column(String(100), nullable=False)
    biografia = Column(String(255), nullable=False)
    def __repr__(self):
        return (f'<Diretor {self.nome_diretor}, Biografia: {self.biografia}>')


class Filme(Base):
    __tablename__ = 'filmes'
    id_filme = Column(Integer, primary_key=True)
    titulo = Column(String(80), nullable=False)
    tempo_duracao_min = Column(Integer)
    descricao = Column(String(255), nullable=False)
    trailer = Column(String(255), nullable=False)
    data_lancamento = Column(String(255), nullable=False)
    id_genero = Column(Integer, ForeignKey('generos.id_genero'))
    id_diretor = Column(Integer, ForeignKey('diretores.id_diretor'))
    def __repr__(self):
        return (f'<Filme {self.titulo}, Tempo: {self.tempo_duracao_min}, Descrição: {self.descricao}, Trailer: {self.trailer}, Data lançamento: {self.data_lancamento}, Genero: {self.id_genero}, Diretor: {self.id_filme}>')

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id_avaliacao = Column(Integer, primary_key=True)
    critica = Column(String(255), nullable=False)
    id_filme = Column(Integer, ForeignKey('filmes.id_filme'))
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    def __repr__(self):
        return (f'<Avaliacao {self.critica}, Filme: {self.id_filme}, Usuario: {self.id_usuario}>')

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    senha = Column(String(255), nullable=False)
    def __repr__(self):
        return (f'<Usuario {self.nome}, Email: {self.email}, Senha: {self.senha}>')
