import sqlite3 as sq

def conectar_db():
    return sq.connect('jogadores.db')

def criar_tabelas():
    with conectar_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jogadores (
                nome TEXT PRIMARY KEY,
                hp_max INTEGER,
                hp_atual INTEGER,
                atk INTEGER,
                dfs INTEGER,
                spd INTEGER,
                exp INTEGER,
                exp_bar INTEGER,
                level INTEGER
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS monstros (
                nome TEXT PRIMARY KEY,
                hp_max INTEGER,
                hp_atual INTEGER,
                atk INTEGER,
                dfs INTEGER,
                spd INTEGER,
                level INTEGER
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS torres (
                nome TEXT PRIMARY KEY,
                monstro_nome TEXT,
                capanga_nome TEXT,
                recompensa TEXT
            )
        ''')


