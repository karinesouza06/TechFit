
import sqlite3

conn = sqlite3.connect('database.db')

with open('db/flask-sqlite.sql', encoding='utf-8') as arquivo:
    conn.executescript(arquivo.read())


