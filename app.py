from flask import Flask, flash
from flask import render_template, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError
from models import local_secao, Ator, Avaliacao, Filme, Usuario
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('/pag_inicial')

@app.route('/pag_inicial')
def home():
    return render_template('Inicio.html')

@app.route('/filmes')
def listar_filmes():
    db_session = local_secao()
    try:
        sql_filmes = select(Filme)
        resultado = db_session.execute(sql_filmes)
        return render_template('Inicio.html', var_filmes=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar receitas: {ex}')
    finally:
        db_session.close()


if __name__ == '__main__':
    app.run(debug=True)
