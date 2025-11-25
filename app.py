from flask import Flask, flash
from flask import render_template, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import local_secao, Ator, Avaliacao, Diretor, Diretor_Filme, Filme, Filme_Ator, Genero, Genero_filme, \
    Usuario
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('/cadastrar_usuario')


@app.route('/Filmes')
def listar_filmes():
    db_session = local_secao()
    try:
        sql_filmes = select(Filme)
        resultado = db_session.execute(sql_filmes).scalars()
        return render_template('Filmes.html', var_filmes=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar filmes: {ex}')
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
            return redirect(url_for('listar_filmes'))
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
        if resultado_email:
            if senha == resultado_email.senha:
                flash("Usuario logado", "success")
                return redirect(url_for('listar_filmes'))
            else:
                flash("Senha incorreta", "error")
                print('erro ao logar')
                return redirect(url_for('logar_usuario'))
        try:
            flash('Usuario encontrado com sucesso', 'success')
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao tentar logar usuario:{e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao tentar logar usuario:{ex}')
        finally:
            db_session.close()
    return render_template('Login.html')


@app.route('/cadastrar_filme', methods=['GET', 'POST'])
def cadastrar_filme():
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_titulo']:
            flash("preencha o titulo", "error")
        if not request.form['form_duracao']:
            flash("preencha o Tempo de Duração", "error")
        if not request.form['form_descricao']:
            flash("preencha a Descrição", "error")
        if not request.form['form_trailer']:
            flash("preencha o URL do Trailer", "error")
        if not request.form['form_imagem']:
            flash("preencha o URL da Imagem", "error")
        if not request.form['form_lancamento']:
            flash("preencha a data de lancamento", "error")
        dados_filme = Filme(titulo=request.form['form_titulo'], tempo_duracao_min=request.form['form_duracao'],
                            descricao=request.form['form_descricao'], trailer=request.form['form_trailer'],
                            imagem=request.form['form_imagem'], data_lancamento=request.form['form_lancamento'])
        try:
            db_session.add(dados_filme)
            db_session.commit()

            flash("Filme cadastrado com sucesso", "success")
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar filme:{e}')
            db_session.rollback()
        finally:
            db_session.close()
    sql_generos = select(Genero)
    resultado = db_session.execute(sql_generos).scalars()
    return render_template('Cadastrar_Filme.html', var_generos=resultado)


@app.route('/detalhar_filme/<var_id>', methods=['GET'])
def info_filme(var_id):
    db_session = local_secao()
    try:
        detalhes_filme = select(Filme).where(Filme.id_filme == var_id)
        resultado = db_session.execute(detalhes_filme).scalar_one_or_none()
        return render_template('Detalhes_Filmes.html', var_filmes=resultado)
    except SQLAlchemyError as e:
        # mostra erro no terminal
        print(f"Erro na base de dados: {e}")
        # mostrar mensagem de erro no navegador
        flash(f"Erro na base de dados", 'danger')
        # retorna o valor inicial
        db_session.rollback()
        return redirect(url_for('listar_filmes'))
    except Exception as ex:
        print(f'Ocorreu um erro: {ex}')
        flash(f'Ocorreu um erro', 'error')
        return redirect(url_for('listar_filmes'))
    finally:
        # fechar ligação com o banco
        db_session.close()


@app.route('/generos')
def get_generos():
    db_session = local_secao()
    try:
        sql_generos = select(Genero)
        resultado = db_session.execute(sql_generos).scalars()
        return render_template('Generos.html', var_generos=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar generos: {ex}')
    finally:
        db_session.close()


@app.route('/detalhar_generos/<var_id>', methods=['GET'])
def detalhar_genero(var_id):
    db_session = local_secao()
    try:
        detalhes_genero = select(Genero).where(Genero.id_genero == var_id)
        resultado = db_session.execute(detalhes_genero).scalar_one_or_none()
        return render_template('Tipos_Generos.html', var_generos=resultado)
    except SQLAlchemyError as e:
        # mostra erro no terminal
        print(f"Erro na base de dados: {e}")
        # mostrar mensagem de erro no navegador
        flash(f"Erro na base de dados", 'danger')
        # retorna o valor inicial
        db_session.rollback()
        return redirect(url_for('get_generos'))
    except Exception as ex:
        print(f'Ocorreu um erro: {ex}')
        flash(f'Ocorreu um erro', 'error')
        return redirect(url_for('get_generos'))
    finally:
        # fechar ligação com o banco
        db_session.close()


@app.route('/cadastrar_genero', methods=['GET', 'POST'])
def cadastro_genero():
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_nome_genero']:
            flash("preencha o nome do genero", "error")
        try:
            dados_genero = Genero(nome_genero=request.form['form_nome_genero'])
            db_session.add(dados_genero)
            db_session.commit()
            flash("Genero cadastrado com sucesso", "success")
            return redirect(url_for('get_generos'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
        finally:
            db_session.close()
    return render_template('Cadastrar_Genero.html')


@app.route('/definir_genero/<var_id>', methods=['GET', 'POST'])
def definir_genero(var_id):
    db_session = local_secao()
    if request.method == 'POST':
        try:
            dados_genero = select(Genero)
            resultado_g = db_session.execute(dados_genero).scalars()
            dados_filme = select(Filme).where(Filme.id_filme == var_id)
            resultado_f = db_session.execute(dados_filme).scalar_one_or_none()
            return render_template('Definir_Genero.html', var_generos=resultado_g, var_filme=resultado_f)
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
            return redirect(url_for('definir_genero'))
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
            return redirect(url_for('definir_genero'))
        finally:
            db_session.close()
    dados_genero = select(Genero)
    resultado_g = db_session.execute(dados_genero).scalars()
    dados_filme = select(Filme).where(Filme.id_filme == var_id)
    resultado_f = db_session.execute(dados_filme).scalar_one_or_none()
    dados_filme = select(Filme).where(Filme.id_filme == var_id)
    resultado = db_session.execute(dados_filme).scalar_one_or_none()
    print('jjk', resultado.id_filme)
    return render_template('Definir_Genero.html', var_id_f=resultado.id_filme, var_generos=resultado_g,
                           var_filme=resultado_f)



if __name__ == '__main__':
    app.run(debug=True)
