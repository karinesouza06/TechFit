CREATE TABLE IF NOT EXISTS dados_usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone INT NOT NULL,
    data_nascimento DATE NOT NULL,
    genero TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL,
    dias_treino INT NOT NULL,
    horario_treino DATE NOT NULL,
    dias_trabalho INT NOT NULL,
    horario_trabalho DATE NOT NULL

);
