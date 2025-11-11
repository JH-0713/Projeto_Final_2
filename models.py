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
class Filme(Base):
    __tablename__ = 'filmes'
    id_filme = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    tempo_duracao_min = Column(String(50), nullable=False)
    descricao = Column(String, nullable=False)
    trailer = Column(String(255), nullable=False)
    data_lancamento = Column(String, nullable=False)
    genero_filme = Column(String(50), nullable=False)
    filme_diretor = Column(Integer, ForeignKey('diretores.id_diretor'), nullable=False)
    filme_ator = Column(Integer, ForeignKey('atores.id_ator'), nullable=False)
    def __repr__(self):
        return (f'<Filme {self.titulo}, Tempo: {self.tempo_duracao_min}, Descricao: {self.descricao}, Trailer: {self.trailer}, '
                f'data_lancamento: {self.data_lancamento}, genero: {self.genero_filme}, filme do diretor: {self.filme_diretor},'
                f'filme do ator: {self.filme_ator}>')

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id_avaliacao = Column(Integer, primary_key=True)
    nota = Column(String(5), nullable=False)
    critica = Column(String, nullable=False)
    def __repr__(self):
        return f'<Avaliacao: {self.nota} critica: {self.critica}>'

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nome_usuario = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    senha = Column(String(255), nullable=False)
    def __repr__(self):
        return f'<Usuario: {self.nome_usuario}, Email: {self.email}, Senha: {self.senha}>'

class Ator(Base):
    __tablename__ = 'atores'
    id_ator = Column(Integer, primary_key=True)
    nome_ator = Column(String(150), nullable=False)
    def __repr__(self):
        return f'<Ator: {self.nome_ator}>'

class Diretor(Base):
    __tablename__ = 'diretors'
    id_diretor = Column(Integer, primary_key=True)
    nome_diretor = Column(String(255), nullable=False)
    def __repr__(self):
        return f'<Diretor: {self.nome_diretor}>'


