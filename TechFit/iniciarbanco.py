import sqlite3

conn = sqlite3.connect('database.db')

with open('db/flask-sqlite.sql') as arquivo:
    conn.executescript(arquivo.read())


#lembrar de instalar a extensão SQlite Viewer
