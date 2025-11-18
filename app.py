from flask import Flask, flash
from flask import render_template, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import local_secao, Ator, Avaliacao, Diretor, Diretor_Filme, Filme, Filme_Ator, Usuario, Genero, Genero_filme
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('/pag_cadastro')


@app.route('/pag_cadastro')
def cadastro():
    return render_template('Cadastrar_Usuario.html')

@app.route('/pag_login')
def login():
    return render_template('Login.html')


@app.route('/inicio')
def filmes():
    return render_template('Pag_Filmes.html')

@app.route('/genero')
def genero():
    return render_template('Genero.html')

@app.route('/listar_genero')
def get_genero():
    db_session = local_secao()
    try:
        sql_genero = select(Genero)
        resultado = db_session.execute(sql_genero).scalars()
        return render_template('Pag_Filmes.html', var_genero=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar pessoas: {ex}')
    finally:
        db_session.close()


@app.route('/listar_usuarios')
def get_cadastro():
    db_session = local_secao()
    try:
        sql_conta = select(Usuario)
        resultado = db_session.execute(sql_conta).scalars()
        return render_template('Cadastrar_Usuario.html', var_contas=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar pessoas: {ex}')
    finally:
        db_session.close()

@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_user():
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_nome']:
            flash("preencha o nome", "error")
        if not request.form['form_email']:
            flash("preencha o email", "error")
        if not request.form['form_senha']:
            flash("preencha o senha", "error")
        dados_usuario = Usuario(nome_usuario=request.form['form_nome'], email=request.form['form_email'],
                                senha=request.form['form_senha'])
        try:
            db_session.add(dados_usuario)
            db_session.commit()
            flash("Usuario cadastrado com sucesso", "success")
            return redirect(url_for('filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar usuario:{e}')
            db_session.rollback()
        finally:
            db_session.close()
    return render_template('Cadastrar_Usuario.html')

@app.route('/logar_usuario', methods=['GET', 'POST'])
def logar_usuario():
    db_session = local_secao()
    if request.method == 'POST':
        email = request.form['email_log']
        senha = request.form['senha_log']
        sql_email = select(Usuario).where(Usuario.email == email)
        resultado_email = db_session.execute(sql_email).scalar()
        print("Email:",resultado_email.nome_usuario)
        if resultado_email:
            if senha == resultado_email.senha:
                flash("Usuario logado", "success")
                return redirect(url_for('filmes'))
            else:
                flash("Senha incorreta", "error")
                print('erro ao logar')
                return redirect(url_for('logar_usuario'))
        try:
            flash('Usuario encontrado com sucesso', 'success')
            return redirect(url_for('filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao tentar logar usuario:{e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao tentar logar usuario:{ex}')
        finally:
            db_session.close()
    return render_template('Login.html')

if __name__ == '__main__':
    app.run(debug=True)
