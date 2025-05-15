import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')

with open('database/flask-sqlite.sql', encoding='utf-8') as arquivo:
    conn.executescript(arquivo.read())

# Verificar e criar usuário administrador
cursor = conn.cursor()
admin_email = 'admin@example.com'
cursor.execute("SELECT use_id FROM users WHERE use_email = ?", (admin_email,))
admin_existente = cursor.fetchone()

if not admin_existente:
    senha_admin = generate_password_hash('admin123')
    cursor.execute(
        '''INSERT INTO users 
        (use_nome, use_email, use_senha, use_telefone, use_data_nascimento, use_genero, use_tipo_usuario, use_dias_treino, use_horario_treino, use_dias_trabalho, use_horario_trabalho) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ('Administrador', admin_email, senha_admin, '00000000000', '2000-01-01', 'masculino', 'admin', 0, '00:00:00', 0, '00:00:00')
    )
    conn.commit()

conn.close()



