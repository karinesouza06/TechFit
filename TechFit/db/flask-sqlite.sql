CREATE TABLE IF NOT EXISTS users (
    use_id INTEGER PRIMARY KEY AUTOINCREMENT,
    use_nome TEXT NOT NULL,
    use_senha TEXT NOT NULL,
    use_email TEXT NOT NULL,
    use_telefone TEXT NOT NULL,
    use_data_nascimento DATE NOT NULL,
    use_genero TEXT NOT NULL,
    use_tipo_usuario TEXT NOT NULL,
    use_dias_treino INT,
    use_horario_treino TIME,
    use_dias_trabalho INT ,
    use_horario_trabalho TIME 

);