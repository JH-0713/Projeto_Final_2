from flask import Flask, flash
from flask import render_template, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import local_secao, Ator, Filme, Usuario
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('/pag_inicial')

@app.route('/pag_inicial')
def cadastro():
    return render_template('Cadastrar.html')

@app.route('/cadastrar_usuario', methods=['GET','POST'])
def cadastrar_usuario():
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_nome']:
            flash("preencha o nome", "error")
        if not request.form['form_email']:
            flash("preencha o email", "error")
        if not request.form['form_senha']:
            flash("preencha o senha", "error")
        dados_usuario = Usuario(nome_usuario=request.form['form_nome'],email=request.form['form_email'],senha=request.form['form_senha'])
        try:
            db_session.add(dados_usuario)
            db_session.commit()
            flash("Usuario cadastrado com sucesso", "success")
            return redirect(url_for('cadastro'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar usuario:{e}')
            db_session.rollback()
        finally:
            db_session.close()
    return redirect('Home.html')

@app.route('/incio')
def home():
    return render_template(url_for('Home.html'))


if __name__ == '__main__':
    app.run(debug=True)
