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

@app.route('/cadastrar_usuario')
def cadastrar_usuario():


if __name__ == '__main__':
    app.run(debug=True)
