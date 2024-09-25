# torre.py
from database import conectar_db
from monstro import Monstro
from glb import lista_torres

class Torre:
    def __init__(self, nome, monstro, capanga, recompensa):
        self.nome = nome
        self.monstro = monstro
        self.capanga = capanga
        self.recompensa = recompensa
        lista_torres.append(self)

        if not self.existe_no_db():
            self.salvar_no_db()

    def existe_no_db(self):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM torres WHERE nome = ?', (self.nome,))
            count = cursor.fetchone()[0]
            return count > 0

    def salvar_no_db(self):
        with conectar_db() as conn:
            conn.execute('''
                INSERT INTO torres (nome, monstro_nome, capanga_nome, recompensa) VALUES (?, ?, ?, ?)
            ''', (self.nome, self.monstro.nome, self.capanga.nome, self.recompensa))

    @classmethod
    def carregar_torres_do_db(cls):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT nome, monstro_nome, capanga_nome, recompensa FROM torres')
            for row in cursor.fetchall():
                nome, monstro_nome, capanga_nome, recompensa = row
                
                # Busca o monstro e capanga pelos nomes armazenados
                monstro = cls.buscar_monstro(monstro_nome)
                capanga = cls.buscar_capanga(capanga_nome)
                
                # Se não forem encontrados, você pode optar por criar novas instâncias ou lidar de outra forma
                if not monstro:
                    print(f'Monstro "{monstro_nome}" não encontrado, criando uma nova instância.')
                    monstro = Monstro(nome=monstro_nome, hp_max=50, hp_atual=50, atk=10, dfs=6, spd=4, level=10)
                if not capanga:
                    print(f'Capanga "{capanga_nome}" não encontrado, criando uma nova instância.')
                    capanga = Monstro(nome=capanga_nome, hp_max=10, hp_atual=10, atk=2, dfs=2, spd=2, level=1)

                # Cria a instância da torre
                cls(nome, monstro, capanga, recompensa)

    @staticmethod
    def buscar_monstro(nome):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT * FROM monstros WHERE nome = ?', (nome,))
            row = cursor.fetchone()
            if row:
                return Monstro(*row)  # Retorna a instância existente
            return None  # Retorna None se não encontrado

    @staticmethod
    def buscar_capanga(nome):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT * FROM monstros WHERE nome = ?', (nome,))
            row = cursor.fetchone()
            if row:
                return Monstro(*row)  # Retorna a instância existente
            return None  # Retorna None se não encontrado

