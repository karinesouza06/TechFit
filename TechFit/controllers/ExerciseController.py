from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import login_required
from models import Exercise


exercise_bp = Blueprint('exercise', __name__)

@exercise_bp.route('/cadastrar_exercicio', methods=['POST', 'GET'])
@login_required
def cadastrar_exercicio():
    if request.method == 'POST':
        nome = request.form['nome']
        nivel = request.form['nivel']
        link = request.form['link']
        Exercise.inserir_exercicio(nome, nivel, link)
        flash("Exercício cadastrado com sucesso!")
        return redirect(url_for('exercise.exercise_page'))

    return render_template('cadastrar_exercicio.html')

@exercise_bp.route('/exercise_page')
def exercise_page():
    exercicios = Exercise.obter_exercicios()
    return render_template('exercise_page.html', exercicios=exercicios)

@exercise_bp.route('/videos_admin')
def videos_admin():
    exercicios = Exercise.obter_exercicios()
    return render_template('videos_admin.html', exercicios=exercicios)

@exercise_bp.route('/videos_personal')
def videos_personal():
    exercicios = Exercise.obter_exercicios()
    return render_template('videos_personal.html', exercicios=exercicios)