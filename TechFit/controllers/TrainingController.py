from flask import Blueprint, render_template, redirect, flash, jsonify, request, url_for
from flask_login import login_required, current_user
from models import Treino, DadosUserAluno, obter_conexao
from datetime import datetime

training_bp = Blueprint('training', __name__)

@training_bp.route('/treinos')
def treinos():
    return render_template('treinos.html')

@training_bp.route('/medidas', methods=['GET', 'POST'])
@login_required
def medidas():
    user_id = current_user.get_id()
    user = current_user.get(user_id)

    if not user:
        flash("Usuário não encontrado.")
        return redirect(url_for('index'))

    if request.method == 'POST':
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
                return redirect(url_for('training.medidas'))

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
    
    return render_template('medidas.html', user_info=current_user)

@training_bp.route('/registrar_treino', methods=['POST'])
@login_required
def registrar_treino():
    user_id = current_user.get_id()
    data_treino = request.form['data_treino']

    Treino.registrar_treino(user_id, data_treino)
    flash("Treino registrado com sucesso!")
    return redirect(url_for('profile.profile'))

@training_bp.route('/listar_treinos')
@login_required
def listar_treinos():
    user_id = current_user.get_id()
    treinos = Treino.obter_treinos(user_id)
    return jsonify({'treinos': treinos})