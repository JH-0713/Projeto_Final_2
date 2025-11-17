# importar Biblioteca
from jinja2.lexer import integer_re
from sqlalchemy import Column, DateTime, func, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Coneção banco de Dados
engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/cinema')

# Configura Seções locais
local_secao = sessionmaker(bind=engine)

# Formato de Efetuação
Base = declarative_base()

# Base
class Ator(Base):
    __tablename__ = 'atores'
    id_ator = Column(Integer, primary_key=True)
    nome_ator = Column(String, nullable=False)
    def __repr__(self):
        return f'<Ator {self.nome_ator}>'

class Filme_Ator(Base):
    __tablename__ = 'filmes_ators'
    id_filme_ator = Column(Integer, primary_key=True)
    id_filme = Column(Integer, ForeignKey('filmes.id_filme'), nullable=False)
    id_ator = Column(Integer, ForeignKey('atores.id_ator'), nullable=False)
    def __repr__(self):
        return f'<Filme {self.id_filme}, Ator: {self.id_ator}>'

class Filme(Base):
    __tablename__ = 'filmes'
    id_filme = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    tempo_duracao_min = Column(Integer, nullable=False)
    descricao = Column(String, nullable=False)
    trailer = Column(String, nullable=False)
    data_lancamento = Column(String, nullable=False)
    genero_filme = Column(String, nullable=False)
    filme_diretor = Column(String, nullable=False)
    avaliacao = Column(String, nullable=False)
    def __repr__(self):
        return (f'<Filme {self.titulo}, Tempo: {self.tempo_duracao_min}, Descricao: {self.descricao},'
                f' Trailer: {self.trailer}, Data: {self.data_lancamento}, Genero: {self.genero_filme},'
                f' Diretor: {self.filme_diretor}, Avaliacao: {self.avaliacao}>')


class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    nome_usuario = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    def __repr__(self):
        return f'< Usuario: {self.nome_usuario}, Email: {self.email}, Email: {self.email},Senha: {self.senha}>'
