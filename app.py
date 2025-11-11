from flask import Flask, flash
from flask import render_template, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError
from models import local_secao, Ator, Avaliacao, Diretor, Filme, Genero, Usuario
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('/pag_inicial')

@app.route('/pag_inicial')
def home():
    return render_template('Pag_inicio.html')


@app.route('/filmes')
def get_filmes():
    db_session = local_secao()
    try:
        sql_filmes = select(Filme)
        resultado = db_session.execute(sql_filmes).scalars()
        return render_template('Pag_inicio.html', var_filmes=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro: {ex}')
    finally:
        db_session.close()

@app.route('/cadastrar_filme', methods=['GET', 'POST'])
def post_filme():
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form('titulo'):
            flash("preencha o titulo", "error")
        if not request.form('duracao'):
            flash("preencha o duração", "error")
        if not request.form('descricao'):
            flash("preencha o descrição", "error")
        if not request.form('trailer'):
            flash("preencha o trailer", "error")
        if not request.form('lancamento'):
            flash("preencha o lançamento", "error")
        if not request.form('genero'):
            flash("preencha o genero", "error")
        if not request.form('diretor'):
            flash("preencha o diretor", "error")
        dados_filme = Filme(titulo=request.form['titulo'],tempo_duracao_min=request.form['duracao'],descricao=request.form['descricao'], trailer=request.form['trailer'],data_lancamento=request.form['lanamento'], id_genero=request.form['genero'],id_diretor=request.form['diretor'])
        try:
            db_session.add(dados_filme)
            db_session.commit()
            flash("Cadastrado com sucesso!", "success")
            return redirect(url_for('/pag_inicial'))
        except SQLAlchemyError as e:
            print(f"Erro ao cadastrar pessoa: {e}")
            db_session.rollback()
        finally:
            db_session.close()
    return render_template('Cadastrar.html')


if __name__ == '__main__':
    app.run(debug=True)
