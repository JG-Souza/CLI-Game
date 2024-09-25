from database import conectar_db
from personagem import Personagem

class Monstro(Personagem):
    def __init__(self, nome, hp_max, hp_atual, atk, dfs, spd, level):
        super().__init__(nome, hp_max, hp_atual, atk, dfs, spd, 0, 0, level)
        
        # Verifica se o monstro já existe no banco de dados antes de salvar
        if not self.existe_no_db():
            self.salvar_no_db()

    def existe_no_db(self):
        with self.conectar_db() as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM monstros WHERE nome = ?', (self.nome,))
            count = cursor.fetchone()[0]
            return count > 0

    def salvar_no_db(self):
        with self.conectar_db() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO monstros (nome, hp_max, hp_atual, atk, dfs, spd, level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.nome, self.hp_max, self.hp_atual, self.atk, self.dfs, self.spd, self.level))

