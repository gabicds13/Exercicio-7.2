LIVROS_INICIAIS = [('Dom Casmurro', 'Machado de Assis', 29.9, 4), ('A Hora da Estrela', 'Clarice Lispector', 34.9, 2), ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 39.9, 0), ('Capitães da Areia', 'Jorge Amado', 32.5, 3)]

import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("livraria.db")


def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def iniciar():
    with conectar() as con:
        con.execute("CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, preco REAL, estoque INTEGER)")
        con.execute("CREATE TABLE IF NOT EXISTS reservas (livro_id INTEGER PRIMARY KEY, expira_em TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS desejos (livro_id INTEGER PRIMARY KEY)")
        if con.execute("SELECT COUNT(*) FROM livros").fetchone()[0] == 0:
            con.executemany("INSERT INTO livros (titulo,autor,preco,estoque) VALUES (?,?,?,?)", LIVROS_INICIAIS)
