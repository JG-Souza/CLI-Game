import sqlite3 as sq

lista_personagens = []

class Personagem:
    def __init__(self, nome, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level):
        self.nome = nome
        self.hp_max = hp_max
        self.hp_atual = hp_atual
        self.atk = atk
        self.dfs = dfs
        self.spd = spd
        self.exp = exp
        self.exp_bar = exp_bar
        self.level = level
        self.carregar_do_db(nome)
        self.salvar_no_db()

        lista_personagens.append(self)

    @staticmethod
    def conectar_db():
        return sq.connect('jogadores.db')

    @classmethod
    def criar_tabela(cls):
        with self.conectar_db() as conn:
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

    def salvar_no_db(self):
        with self.conectar_db() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO jogadores (nome, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.nome, self.hp_max, self.hp_atual, self.atk, self.dfs, self.spd, self.exp, self.exp_bar, self.level))

    def carregar_do_db(self, nome):
        with self.conectar_db() as conn:
            cursor = conn.execute('SELECT * FROM jogadores WHERE nome = ?', (nome,))
            row = cursor.fetchone()
            if row:
                self.hp_max, self.hp_atual, self.atk, self.dfs, self.spd, self.exp, self.exp_bar, self.level = row[1:]

    def verifica_level_up(self):
        if self.exp >= self.exp_bar:
            self.level_up()

    def level_up(self):
        self.exp -= self.exp_bar
        self.exp_bar = int(round(self.exp_bar * 1.4))
        print('=' * 40)
        escolha = input('Onde você gostaria de colocar seu ponto de habilidade?\n1. Ataque\n2. Defesa\n3. Velocidade\n4. Max HP\n-> ')
        print('=' * 40)
        if escolha == '1':
            self.atk += 2
        elif escolha == '2':
            self.dfs += 2
        elif escolha == '3':
            self.spd += 2
        elif escolha == '4':
            self.hp_max += 3

        self.hp_max += 2
        self.level += 1
        self.salvar_no_db()  # Salva as alterações após o level up

        print(f'Nome: {self.nome}\nMax HP: {self.hp_max}\nAtaque: {self.atk}\nDefesa: {self.dfs}\nVelocidade: {self.spd}\nNível: {self.level}')

    def atacar(self, inimigo):
        dano = self.atk - (30 / 100 * inimigo.dfs)
        inimigo.hp_atual -= dano
        if inimigo.hp_atual < 0:
            inimigo.hp_atual = 0

    def lutar(self, inimigo):
        if self.hp_atual == 0:
            print('Você nã possui HP suficiente, visite o médico')
            return

        atacante, defensor = (self, inimigo) if self.spd > inimigo.spd else (inimigo, self)

        while self.hp_atual > 0 and inimigo.hp_atual > 0:
                atacante.atacar(defensor)
                if defensor.hp_atual > 0:
                    atacante, defensor = defensor, atacante

        if self.hp_atual > 0:
                self.exp += inimigo.level
                print('=' * 40)
                print(f'Você venceu a luta contra {inimigo.nome}, e ganhou {inimigo.level}xp')
                print(f'Você está com {self.exp}/{self.exp_bar} XP')
                self.verifica_level_up()
        else:
                print(f'Você foi derrotado por {inimigo.nome}')
        self.salvar_no_db()
        inimigo.salvar_no_db()

    def ver_status(self):
        print(f'Nome: {self.nome}\nHP: {self.hp_atual}/{self.hp_max}\nAtaque: {self.atk}\nDefesa: {self.dfs}\nVelocidade: {self.spd}\nNível: {self.level}\nEXP: {self.exp}/{self.exp_bar}')

    
    def escolhe_oponente(self):
        print('Oponente Disponíveis: ')
        for personagem in lista_personagens:
            if personagem != self:
                print(personagem.nome)


    def ir_ao_medico(self):
        self.hp_atual = self.hp_max
        print(f'Você restaurou seu hp com sucesso')
        self.salvar_no_db()

    def acoes(self):
        while True:
            print('=' * 40)
            acao = input('Qual ação você quer tomar agora?\n1. Ver seus Stats\n2. Lutar\n3. Ir ao médico\n4. Sentar e Descansar\n-> ')

            if acao == '1':
                self.ver_status()

            if acao == '2':
                self.escolhe_oponente()
                oponente_nome = input('Com quem você quer lutar? ')
                oponente = next((p for p in lista_personagens if p.nome == oponente_nome), None)
                if oponente:
                    self.lutar(oponente)
                else:
                    print('estou falhnado')
                    break

            if acao == '3':
                self.ir_ao_medico()

            if acao == '4':
                break
                

Jg = Personagem('JG', 20, 20, 4, 4, 4, 0, 20, 1)

Ty = Personagem('Ty', 16, 16, 4, 4, 4, 0, 20, 20)

Jg.acoes()


        