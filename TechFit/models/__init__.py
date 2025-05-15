import sqlite3

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

from .User import User
from .Exercise import Exercise
from .StudentData import DadosUserAluno
from .Training import Treino
