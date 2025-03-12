from flask import Flask, redirect, render_template, url_for, request, flash, jsonify
from models import User, Exercicio, DadosUserAluno, Treino,  obter_conexao
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime 
from flask_login import LoginManager, login_user, current_user,login_required, logout_user


login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ULTRAMEGADIFICIL'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form.get('senha') 
        confirmasenha = request.form['confirmasenha']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nascimento = request.form['data']
        tipo_usuario = request.form['tipoUsuario']
        genero = request.form['genero']
        dias_treino = request.form.get('dias_treino')
        horario_treino = request.form['horario_treino']
        dias_trabalho = request.form.get('dias_trabalho')
        horario_trabalho = request.form['horario_trabalho']

        if User.exists(email) == False:
            if senha == confirmasenha:
                id = User.inserir_users(nome, senha, email, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho)

                user = User(id=id, nome=nome, email=email, senha=senha, telefone=telefone, data_nascimento=data_nascimento, genero=genero, tipo_usuario=tipo_usuario, dias_treino=dias_treino, horario_treino=horario_treino, dias_trabalho=dias_trabalho, horario_trabalho=horario_trabalho)
                login_user(user)
               
                flash("Cadastro realizado com sucesso. Faça login agora!")
                return redirect(url_for('index')) 
            else:
                flash("As senhas não coincidem.")
        else:
            flash("Usuário já existente.")
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_by_email(email)
        
        if user and check_password_hash(user.senha, password):
            login_user(user)
            
            if user.tipo_usuario == 'Aluno' or user.tipo_usuario == 'aluno' :
                return redirect(url_for('profile'))
            else:
                return 'Personalllllllllllllll'
            
        else:
            flash('Credenciais inválidas')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    user_id = current_user.get_id() 
    user = User.get(user_id)  
    total_treinos = Treino.contar_treinos(user_id) 

    if user:
        user.total_treinos = total_treinos
        return render_template('profile.html', user_info=user)
    else:
        flash("Usuário não encontrado.")
        return redirect(url_for('index'))
    

@app.route('/cadastrar_exercicio', methods=['POST', 'GET'])
@login_required
def cadastrar_exercicio():
    if request.method == 'POST':
        nome = request.form['nome']
        link = request.form['link']
        tipo = request.form['tipo']
        nivel = request.form['nivel']
        Exercicio.inserir_exercicio(nome, link, tipo, nivel)
        flash("Exercício cadastrado com sucesso!")
        return redirect(url_for('exercise_page'))

    return render_template('cadastrar_exercicio.html')


@app.route('/exercise_page')
def exercise_page():
    exercicios = Exercicio.obter_exercicios()
    return render_template('exercise_page.html', exercicios=exercicios)

@app.route('/treinos')
def treinos():
    return render_template('treinos.html')


@app.route('/medidas', methods=['GET', 'POST'])
@login_required
def medidas():
    user_id = current_user.get_id()
    user = User.get(user_id)

    if not user:
        flash("Usuário não encontrado.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Verificar última inserção
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dau_alu_data_insercao 
            FROM dados_users_alunos 
            WHERE dau_alu_use_id = ? 
            ORDER BY dau_alu_data_insercao DESC 
            LIMIT 1
        """, (user_id,))
        last_submission_row = cursor.fetchone()
        conn.close()

        if last_submission_row:
            last_submission = datetime.strptime(last_submission_row[0], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            if (current_time - last_submission).days < 7:
                flash("Você só pode inserir medidas uma vez por semana. Aguarde 7 dias.")
                return redirect(url_for('medidas'))

        try:
            quadril = float(request.form.get('med-quadril', 0))
            peitoral = float(request.form.get('med-peito', 0))
            ombro = float(request.form.get('med-ombro', 0))
            gluteos = float(request.form.get('med-gluteo', 0))
            dorsal = float(request.form.get('med-dorsal', 0))
            cintura = float(request.form.get('med-cintura', 0))
            bic_esquerdo = float(request.form.get('med-biceps_esquerdo', 0))
            bic_direito = float(request.form.get('med-biceps_direito', 0))
            coxa_esquerda = float(request.form.get('med-coxa_esquerda', 0))
            coxa_direita = float(request.form.get('med-coxa_direita', 0))
            pan_esquerda = float(request.form.get('med-pantu_esquerda', 0))
            pan_direita = float(request.form.get('med-pantu_direita', 0))
           
        except ValueError:
            flash("Por favor, insira valores numéricos válidos.")
            return redirect(url_for('medidas'))

        conn = obter_conexao()
        try:
            DadosUserAluno.inserir_dados(
                user_id, quadril, peitoral, ombro, cintura, gluteos, dorsal,
                bic_esquerdo, bic_direito, coxa_esquerda, coxa_direita,
                pan_esquerda, pan_direita
            )
            flash("Medidas salvas com sucesso!")
        except Exception as e:
            flash(f"Erro ao salvar medidas: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

        return redirect(url_for('medidas'))

    return render_template('medidas.html', user_info=user)

@app.route('/registrar_treino', methods=['POST'])
@login_required
def registrar_treino():
    user_id = current_user.get_id()
    data_treino = request.form['data_treino']

    Treino.registrar_treino(user_id, data_treino)
    flash("Treino registrado com sucesso!")
    return redirect(url_for('profile'))


@app.route('/listar_treinos')
@login_required
def listar_treinos():
    user_id = current_user.get_id()
    treinos = Treino.obter_treinos(user_id)
    return jsonify({'treinos': treinos})


@app.route('/configuracoes', methods=['GET', 'POST'])
def configuracoes():
    userid = current_user.get_id()
    user = User.get(userid) 

    if request.method == 'POST':
        nome = request.form['nome_edit']
        email = request.form['email_edit']
        telefone = request.form['telefone_edit']
        data_nascimento = request.form['data_nascimento_edit']
        idade = request.form['idade_edit']
        peso = request.form['peso_edit']
        altura = request.form['altura_edit']
        foco_treino = request.form['foco_treino_edit']
                
        User.atualizar_dados(nome, email, telefone, data_nascimento, idade, peso, altura, foco_treino, userid)
        
    um_user = User.one(userid)
    return render_template('configuracoes.html', user=um_user, user_info=user)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
