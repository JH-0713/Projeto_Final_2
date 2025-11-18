# importar Biblioteca
from jinja2.lexer import integer_re
from sqlalchemy import Column, DateTime, func, ForeignKey, Integer, String, create_engine,Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Coneção banco de Dados
engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/cinema')

# Configura Seções locais
local_secao = sessionmaker(bind=engine)

# Formato de Efetuação
Base = declarative_base()

# Base
class Ator(Base):
    __tablename__ = 'ator'
    id_ator = Column(Integer, primary_key=True)
    nome_ator = Column(String, nullable=False)
    def __repr__(self):
        return f'<Ator {self.nome_ator}>'

class Avaliacao(Base):
    __tablename__ = 'avaliacao'
    id_avaliacao = Column(Integer, primary_key=True)
    critica = Column(Text, nullable=False)
    usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    movie = Column(Integer, ForeignKey('movies.id_movie'))
    def __repr__(self):
        return f'<Critica {self.critica}, Usuario: {self.usuario}, Movie: {self.movie}>'

class Diretor(Base):
    __tablename__ = 'diretor'
    id_diretor = Column(Integer, primary_key=True)
    nome_diretor = Column(String, nullable=False)
    def __repr__(self):
        return f'<Diretor {self.nome_diretor}>'

class Diretor_Filme(Base):
    __tablename__ = 'diretor_filme'
    id_diretor_filme = Column(Integer, primary_key=True)
    diretor_filme = Column(Integer, ForeignKey('diretor.id_diretor'))
    producao = Column(Integer, ForeignKey('filme.id_filme'))
    def __repr__(self):
        return f'< Diretor: {self.diretor_filme}, Producao: {self.producao}>'

class Filme(Base):
    __tablename__ = 'filme'
    id_filme = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    tempo_duracao_min = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    trailer = Column(Text, nullable=False)
    imagem = Column(Text, nullable=False)
    data_lancamento = Column(DateTime, nullable=False)
    def __repr__(self):
        return (f'< Titulo: {self.titulo}, Tempo: {self.tempo_duracao_min}, Descricao: {self.descricao}, '
                f' Trailer: {self.trailer}, Imagem: {self.imagem}, Data: {self.data_lancamento}>')


class Filme_Ator(Base):
    __tablename__ = 'filmes_ators'
    id_filme_ator = Column(Integer, primary_key=True)
    filmes = Column(Integer, ForeignKey('filme.id_filme'))
    participacao = Column(Integer, ForeignKey('ator.id_ator'))
    def __repr__(self):
        return f'<Filme {self.filmes}, Ator: {self.participacao}>'


class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    nome_usuario = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    def __repr__(self):
        return f'< Usuario: {self.nome_usuario}, Email: {self.email},Senha: {self.senha}>'

class Genero(Base):
    __tablename__ = 'genero'
    id_genero = Column(Integer, primary_key=True)
    nome_genero = Column(String, nullable=False)
    def __repr__(self):
        return f'< Genero: {self.genero}>'

class Genero_filme(Base):
    __tablename__ = 'genero_filme'
    id_genero_filme = Column(Integer, primary_key=True)
    tipo_genero = Column(Integer, ForeignKey('genero.id_genero'))
    classe_filme = Column(Integer, ForeignKey('filme.id_filme'))
    def __repr__(self):
        return f'< Genero: {self.tipo_genero}, Filme: {self.classe_filme}> >'