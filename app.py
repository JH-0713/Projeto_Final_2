from flask import Flask, flash
from flask import render_template, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import local_secao, Ator, Avaliacao, Diretor, Diretor_Filme, Filme, Filme_Ator, Genero, Genero_Filme, \
    Usuario
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('/cadastrar_usuario')


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
        if not request.form['form_imagem']:
            flash("preencha o URL da Imagem", "error")
        if not request.form['form_lancamento']:
            flash("preencha a data de lancamento", "error")
        dados_filme = Filme(titulo=request.form['form_titulo'], tempo_duracao_min=request.form['form_duracao'],
                            descricao=request.form['form_descricao'], imagem=request.form['form_imagem'],
                            data_lancamento=request.form['form_lancamento'])
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
    return render_template('Cadastrar_Filme.html')


@app.route('/detalhar_filme/<int:var_id>', methods=['GET'])
def info_filme(var_id):
    db_session = local_secao()
    try:
        detalhes_filme = select(Filme).where(Filme.id_filme == var_id)
        resultado_f = db_session.execute(detalhes_filme).scalar_one_or_none()

        detalhes_user = select(Usuario)
        var_user = db_session.execute(detalhes_user).scalar_one_or_none()

        sql_generos_filme = select(Genero).join(Genero_Filme, Genero.id_genero == Genero_Filme.tipo_genero).where(
            Genero_Filme.classe_filme == var_id)
        lista_generos = db_session.execute(sql_generos_filme).scalars()
        var_gf = db_session.execute(sql_generos_filme).first()

        sql_diretores_filme = select(Diretor).join(Diretor_Filme,
                                                   Diretor.id_diretor == Diretor_Filme.diretor_filme).where(
            Diretor_Filme.producao == var_id)
        lista_diretores = db_session.execute(sql_diretores_filme).scalars()
        var_df = db_session.execute(sql_diretores_filme).first()

        sql_atores_filme = select(Ator).join(Filme_Ator, Ator.id_ator == Filme_Ator.participacao).where(
            Filme_Ator.cena == var_id)
        lista_atores = db_session.execute(sql_atores_filme).scalars()
        var_af = db_session.execute(sql_atores_filme).first()

        detalhes_aval = select(Avaliacao).where(Avaliacao.movie == var_id)
        resultado_a = db_session.execute(detalhes_aval).scalar_one_or_none()
        sql_avaliacao_filme = select(Usuario).join(Avaliacao, Usuario.id_usuario == Avaliacao.usuario_id).where(
            Avaliacao.movie == var_id)
        var_ua = db_session.execute(sql_avaliacao_filme).scalars().all()
        return render_template('Dethalhes_Filmes.html', var_filmes=resultado_f,
                               var_generos=lista_generos, var_diretores=lista_diretores, var_atores=lista_atores,
                               var_user = var_user,var_aval=resultado_a,var_gf=var_gf, var_df=var_df, var_af=var_af,var_ua=var_ua)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
        flash(f"Erro na base de dados", 'danger')
        db_session.rollback()
        return redirect(url_for('listar_filmes'))
    except Exception as ex:
        print(f'Ocorreu um erro: {ex}')
        flash(f'Ocorreu um erro', 'error')
        return redirect(url_for('listar_filmes'))
    finally:
        db_session.close()



@app.route('/pesquisar_filme', methods=['POST'])
def pesquisar_filmes():
    db_session = local_secao()
    if request.method == 'POST':
        termo = request.form.get('pesquisa', '').strip()
        try:
            sql_busca = select(Filme).where(Filme.titulo.ilike(f"%{termo}%"))
            filmes = db_session.execute(sql_busca).scalars().all()
            return render_template("Resultado_Pesquisa.html", var_filmes=filmes, termo=termo)
        except SQLAlchemyError as e:
            print(f'Erro ao pesquisar filme: {e}')
            db_session.rollback()
        finally:
            db_session.close()
    return redirect(url_for('listar_filmes'))



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
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
        finally:
            db_session.close()
    return render_template('Cadastrar_Genero.html')


@app.route('/detalhar_generos/<var_id>', methods=['GET'])
def detalhar_genero(var_id):
    db_session = local_secao()
    try:
        detalhes_genero = select(Genero).where(Genero.id_genero == var_id)
        resultado_g = db_session.execute(detalhes_genero).scalar_one_or_none()
        detalhes_filme = select(Filme).join(Genero_Filme, Filme.id_filme == Genero_Filme.classe_filme).where(
            Genero_Filme.tipo_genero == var_id)
        resultado_f = db_session.execute(detalhes_filme).scalars().all()
        print('hju', resultado_g)
        print('gft', resultado_f)
        return render_template('Detalhar_Generos.html',
                               var_generos=resultado_g, var_filmes=resultado_f)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
        flash(f"Erro na base de dados", 'danger')
        db_session.rollback()
        return redirect(url_for('get_generos'))
    except Exception as ex:
        print(f'Ocorreu um erro: {ex}')
        flash(f'Ocorreu um erro', 'error')
        return redirect(url_for('get_generos'))
    finally:
        db_session.close()


@app.route('/detalhar_filme/definir_genero/<int:var_id>', methods=['GET', 'POST'])
def definir_genero(var_id):
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_genero']:
            flash("preencha o nome do genero", "error")
        try:
            generos_escolhidos = request.form.getlist("form_genero")
            dados_filme = select(Filme).where(Filme.id_filme == var_id)
            resultado_f = db_session.execute(dados_filme).scalar_one_or_none()
            print('asd', generos_escolhidos)
            for id_genero in generos_escolhidos:
                definir_gf = Genero_Filme(tipo_genero=int(id_genero), classe_filme=resultado_f.id_filme)
                db_session.add(definir_gf)
            db_session.commit()
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
            return redirect(url_for('listar_filmes'))
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
            return redirect(url_for('listar_filmes'))
        finally:
            db_session.close()
    dados_genero = select(Genero)
    dados_filme = select(Filme).where(Filme.id_filme == var_id)
    resultado_g = db_session.execute(dados_genero).scalars()
    resultado_f = db_session.execute(dados_filme).scalar_one_or_none()

    print('jjk', resultado_f.id_filme)
    return render_template('Definir_Genero.html', var_id_f=resultado_f.id_filme, var_generos=resultado_g,
                           var_filme=resultado_f)



@app.route('/diretor')
def get_diretores():
    db_session = local_secao()
    try:
        sql_diretores = select(Diretor)
        resultado = db_session.execute(sql_diretores).scalars()
        return render_template('Diretores.html', var_diretores=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar generos: {ex}')
    finally:
        db_session.close()


@app.route('/cadastrar_diretor', methods=['GET', 'POST'])
def cadastro_diretor():
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_nome_diretor']:
            flash("preencha o nome do genero", "error")
        try:
            dados_genero = Diretor(nome_diretor=request.form['form_nome_diretor'])
            db_session.add(dados_genero)
            db_session.commit()
            flash("Genero cadastrado com sucesso", "success")
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
        finally:
            db_session.close()
    return render_template('Cadastrar_Diretor.html')


@app.route('/detalhar_diretores/<var_id>', methods=['GET'])
def detalhar_diretor(var_id):
    db_session = local_secao()
    try:
        detalhes_diretor = select(Diretor).where(Diretor.id_diretor == var_id)
        resultado_d = db_session.execute(detalhes_diretor).scalar_one_or_none()
        detalhes_filme = select(Filme).join(Diretor_Filme, Diretor_Filme.producao == Filme.id_filme).where(
            Diretor_Filme.diretor_filme == var_id)
        resultado_f = db_session.execute(detalhes_filme).scalars().all()
        print('hju', resultado_d)
        print('gft', resultado_f)
        return render_template('Detalhar_Diretores.html', var_diretores=resultado_d, var_filmes=resultado_f)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
        flash(f"Erro na base de dados", 'danger')
        db_session.rollback()
        return redirect(url_for('get_diretores'))
    except Exception as ex:
        print(f'Ocorreu um erro: {ex}')
        flash(f'Ocorreu um erro', 'error')
        return redirect(url_for('get_diretores'))
    finally:
        db_session.close()


@app.route('/detalhar_filme/definir_diretor/<int:var_id>', methods=['GET', 'POST'])
def definir_diretor(var_id):
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_diretor']:
            flash("preencha o nome do genero", "error")
        try:
            diretores_escolhidos = request.form.getlist("form_diretor")
            dados_filme = select(Filme).where(Filme.id_filme == var_id)
            resultado_f = db_session.execute(dados_filme).scalar_one_or_none()
            print('asd', diretores_escolhidos)
            for id_diretor in diretores_escolhidos:
                definir_df = Diretor_Filme(diretor_filme=int(id_diretor), producao=resultado_f.id_filme)
                db_session.add(definir_df)
            db_session.commit()
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
            return redirect(url_for('listar_filmes'))
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
            return redirect(url_for('listar_filmes'))
        finally:
            db_session.close()
    dados_diretor = select(Diretor)
    dados_filme = select(Filme).where(Filme.id_filme == var_id)
    resultado_d = db_session.execute(dados_diretor).scalars()
    resultado_f = db_session.execute(dados_filme).scalar_one_or_none()
    print('jjk', resultado_f.id_filme)
    return render_template('Definir_Diretor.html', var_id_f=resultado_f.id_filme, var_diretores=resultado_d,
                           var_filme=resultado_f)



@app.route('/ator')
def get_atores():
    db_session = local_secao()
    try:
        sql_atores = select(Ator)
        resultado = db_session.execute(sql_atores).scalars()
        return render_template('Atores.html', var_atores=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar generos: {ex}')
    finally:
        db_session.close()


@app.route('/cadastrar_ator', methods=['GET', 'POST'])
def cadastro_ator():
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_nome_ator']:
            flash("preencha o nome do genero", "error")
        try:
            dados_ator = Ator(nome_ator=request.form['form_nome_ator'])
            db_session.add(dados_ator)
            db_session.commit()
            flash("Genero cadastrado com sucesso", "success")
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
        finally:
            db_session.close()
    return render_template('Cadastrar_Ator.html')


@app.route('/detalhar_atores/<var_id>', methods=['GET'])
def detalhar_ator(var_id):
    db_session = local_secao()
    try:
        detalhes_ator = select(Ator).where(Ator.id_ator == var_id)
        resultado_a = db_session.execute(detalhes_ator).scalar_one_or_none()
        detalhes_filme = select(Filme).join(Filme_Ator, Filme_Ator.cena == Filme.id_filme).where(
            Filme_Ator.participacao == var_id)
        resultado_f = db_session.execute(detalhes_filme).scalars().all()
        print('hju', resultado_a)
        print('gft', resultado_f)
        return render_template('Detalhar_Atores.html', var_atores=resultado_a, var_filmes=resultado_f)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
        flash(f"Erro na base de dados", 'danger')
        db_session.rollback()
        return redirect(url_for('get_atores'))
    except Exception as ex:
        print(f'Ocorreu um erro: {ex}')
        flash(f'Ocorreu um erro', 'error')
        return redirect(url_for('get_atores'))
    finally:
        db_session.close()


@app.route('/detalhar_filme/definir_ator/<int:var_id>', methods=['GET', 'POST'])
def definir_ator(var_id):
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_ator']:
            flash("preencha o nome do ator", "error")
        try:
            atores_escolhidos = request.form.getlist("form_ator")
            dados_filme = select(Filme).where(Filme.id_filme == var_id)
            resultado_f = db_session.execute(dados_filme).scalar_one_or_none()
            print('asd', atores_escolhidos)
            for id_ator in atores_escolhidos:
                definir_af = Filme_Ator(participacao=int(id_ator), cena=resultado_f.id_filme)
                db_session.add(definir_af)
            db_session.commit()
            return redirect(url_for('listar_filmes'))
        except SQLAlchemyError as e:
            print(f'Erro ao cadastrar genero:{e}')
            db_session.rollback()
            return redirect(url_for('listar_filmes'))
        except Exception as ex:
            print(f'Erro ao cadastrar genero:{ex}')
            return redirect(url_for('listar_filmes'))
        finally:
            db_session.close()
    dados_ator = select(Ator)
    dados_filme = select(Filme).where(Filme.id_filme == var_id)
    resultado_a = db_session.execute(dados_ator).scalars()
    resultado_f = db_session.execute(dados_filme).scalar_one_or_none()
    print('jjk', resultado_f.id_filme)
    return render_template('Definir_Ator.html', var_id_f=resultado_f.id_filme, var_atores=resultado_a,
                           var_filme=resultado_f)


@app.route('/usuario')
def get_usuario():
    db_session = local_secao()
    try:
        sql_usuario = select(Usuario)
        resultado = db_session.execute(sql_usuario).scalars().first()
        return render_template('Usuario.html', var_usuario=resultado)
    except SQLAlchemyError as e:
        print(f"Erro na base de dados: {e}")
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar usuários: {ex}')
    finally:
        db_session.close()

@app.route('/alterar_usuario/<var_id>', methods=['GET', 'POST'])
def alterar_usuario(var_id):
    db_session = local_secao()
    edit_usuario = select(Usuario).where(Usuario.id_usuario == var_id)
    resultado = db_session.execute(edit_usuario).scalar_one_or_none()
    if request.method == 'POST':
        novo_username = request.form.get('form_nome')
        novo_email = request.form.get('form_email')
        novo_senha = request.form.get('form_senha')
        if novo_username != '':
            resultado.nome_usuario = novo_username
        if novo_email != '':
            resultado.email = novo_email
        if novo_senha != '':
            resultado.senha = novo_senha
        try:
            db_session.commit()
            flash("Pessoa alterada com sucesso!", "success")
            return redirect(url_for('get_usuario'))
        except SQLAlchemyError as e:
            print(f"Erro na base de dados: {e}")
            flash(f"Erro no banco ao alterar pessoa", 'danger')
            db_session.rollback()
            return redirect(url_for('get_usuario'))
        except Exception as ex:
            print(f'Ocorreu um erro ao alterar pessoa: {ex}')
            flash(f'Ocorreu um erro ao alterar pessoa', 'error')
            return redirect(url_for('get_usuario'))
        finally:
            db_session.close()
    return render_template('Editar_Usuario.html', dados_user=resultado)

@app.route('/detalhar_filme/avaliar/<int:var_u>/<int:var_id>', methods=['GET', 'POST'])
def avaliar_filme(var_u, var_id):
    db_session = local_secao()
    if request.method == 'POST':
        if not request.form['form_nota']:
            flash('preencha o campo de nota')
        if not request.form['form_critica']:
            flash("preencha o campo de critica", "error")
        try:
            nova_avaliacao = Avaliacao(nota=request.form['form_nota'],critica=request.form["form_critica"],usuario_id=var_u,movie=var_id)
            db_session.add(nova_avaliacao)
            db_session.commit()
            flash("Avaliação registrada com sucesso!", "success")
            return redirect(url_for('info_filme', var_id=var_id))
        except SQLAlchemyError as e:
            print(f"Erro ao salvar avaliação: {e}")
            db_session.rollback()
            flash("Erro ao salvar avaliação", "error")
        finally:
            db_session.close()
    sql_filme = select(Filme).where(Filme.id_filme == var_id)
    filme = db_session.execute(sql_filme).scalar_one_or_none()
    sql_user = select(Usuario).where(Usuario.id_usuario  == var_u)
    user = db_session.execute(sql_user).scalar_one_or_none()
    return render_template('Avaliar_Filme.html',var_filme=filme,var_user=user)

if __name__ == '__main__':
    app.run(debug=True)