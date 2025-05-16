from flask import Flask, render_template
from flask_login import LoginManager
from controllers.AuthController import auth_bp
from controllers.ExerciseController import exercise_bp
from controllers.ProfileController import profile_bp
from controllers.TrainingController import training_bp
from controllers.PaymentController import payment_bp
from models.User import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ULTRAMEGADIFICIL'

# Configuração do Login Manager
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(exercise_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(training_bp)
app.register_blueprint(payment_bp) 

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
