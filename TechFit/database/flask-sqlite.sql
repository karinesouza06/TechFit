/*TABELA DE USUÁRIOS*/
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
    use_horario_trabalho TIME,
    use_idade INT,
    use_peso FLOAT,
    use_altura FLOAT,
    use_foco_treino VARCHAR(90), /*foco do treino que o aluno quer desenvolver*/
    use_tipo_treino VARCHAR(90), /*tipo do treino que o personal gosta de ensinar*/
    use_contador INTEGER DEFAULT 0
);


/*TABELA COM DADOS DOS USUÁRIOS DO TIPO: ALUNO*/
CREATE TABLE IF NOT EXISTS dados_users_alunos(
    dau_alu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dau_alu_quadril FLOAT,
    dau_alu_peitoral FLOAT,
    dau_alu_ombro FLOAT,
    dau_alu_cintura FLOAT,
    dau_alu_gluteos FLOAT,
    dau_alu_dorsal FLOAT,

    dau_alu_biceps_esquerdo FLOAT,
    dau_alu_biceps_direito FLOAT,
    dau_alu_coxa_esquerda FLOAT,
    dau_alu_coxa_direita FLOAT,
    dau_alu_panturrilha_esquerda FLOAT,
    dau_alu_panturrilha_direita FLOAT,
    dau_alu_data_insercao DATETIME DEFAULT CURRENT_TIMESTAMP,

    dau_alu_use_id INT,
    FOREIGN KEY  (dau_alu_use_id) REFERENCES users(use_id)
);


/*TABELA COM DADOS DOS USUÁRIOS DO TIPO: PERSONAL*/
CREATE TABLE IF NOT EXISTS dados_users_personais(
    dau_per_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    dau_per_formacao VARCHAR(200), /*formação acadêmica*/
    dau_per_cursos VARCHAR(200), /*cursos de especialização*/
    dau_per_tempo_trabalho VARCHAR(200), /*tempo de trabalhando na area*/
    dau_per_tipo_aluno VARCHAR(200), /*tipos de alunos preferível (ex: iniciantes, atletas, reabilitação)*/
    dau_per_ambiente_trabalho VARCHAR(200) /*ambientes que já trabalhou (ex: academia, escolas, plataformas de treinos online,...)*/
);

/*TABELA DE EXERCÍCIOS*/
CREATE TABLE IF NOT EXISTS exercicios (
            exe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            exe_nome TEXT NOT NULL,
            exe_nivel TEXT NOT NULL,
            exe_link TEXT NOT NULL
        );

/*TABELA PARA REGISTRAR DIAS DE TREINO*/
CREATE TABLE IF NOT EXISTS dias_treino (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    data_treino DATE,
    FOREIGN KEY (user_id) REFERENCES users(use_id)
);


