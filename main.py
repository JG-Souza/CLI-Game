from personagem import Personagem
from torre import Torre
from database import criar_tabelas
from monstro import Monstro

if __name__ == '__main__':
    criar_tabelas()
    Personagem.carregar_personagens_do_db()
    Torre.carregar_torres_do_db()
    Personagem.inicio()

    espada_alada = "Espada Alada"  # Exemplo de string como recompensa

    dragao = Monstro('Dragão', hp_max=50, hp_atual=50, atk=10, dfs=6, spd=4, level=10)
    esqueleto = Monstro('Esqueleto', hp_max=10, hp_atual=10, atk=2, dfs=2, spd=2, level=1)

    torre_do_poder = Torre(nome= 'torre do poder',monstro = dragao, capanga = esqueleto, recompensa= espada_alada)

    jg = Personagem('jg', 20, 20, 4, 4, 4, 0, 20, 1)



        