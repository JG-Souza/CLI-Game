import sqlite3 as sq
from database import conectar_db
from glb import lista_torres

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
        lista_personagens.append(self)
        self.salvar_no_db()

    @staticmethod
    def conectar_db():
        return conectar_db()

    @classmethod
    def criar_tabela(cls):
        with cls.conectar_db() as conn:
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
        if type(self) is Personagem:
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

    @classmethod
    def carregar_personagens_do_db(cls):
        with cls.conectar_db() as conn:
            cursor = conn.execute('SELECT * FROM jogadores')
            for row in cursor.fetchall():
                nome, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level = row
                personagem = cls(nome, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level)


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
        self.salvar_no_db()

        print(f'Nome: {self.nome}\nMax HP: {self.hp_max}\nAtaque: {self.atk}\nDefesa: {self.dfs}\nVelocidade: {self.spd}\nNível: {self.level}')

    def atacar(self, inimigo):
        dano = round(self.atk - (30 / 100 * inimigo.dfs))
        inimigo.hp_atual -= dano
        if inimigo.hp_atual < 0:
            inimigo.hp_atual = 0

    def lutar(self, inimigo):
        if self.hp_atual == 0:
            print('Você não possui HP suficiente, visite o médico')
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
        print('Oponentes Disponíveis: ')
        for personagem in lista_personagens:
            if personagem != self:
                print(personagem.nome)

    @staticmethod
    def escolhe_personagem():
        print('Personagens Disponíveis:')
        if not lista_personagens:
            print('Nenhum personagem disponível.')
        else:
            for personagem in lista_personagens:
                print(personagem.nome)


    def ir_ao_medico(self):
        self.hp_atual = self.hp_max
        print('Você restaurou seu HP com sucesso')
        self.salvar_no_db()

    def acoes(self):
        while True:
            print('=' * 40)
            acao = input('Qual ação você quer tomar agora?\n1. Ver seus Stats\n2. Lutar\n3. Ir ao médico\n4. Sentar e Descansar\n-> ')

            if acao == '1':
                self.ver_status()

            elif acao == '2':
                self.escolhe_oponente()
                oponente_nome = input('Com quem você quer lutar? ')
                oponente = next((p for p in lista_personagens if p.nome == oponente_nome), None)
                if oponente:
                    self.lutar(oponente)
                else:
                    print('Personagem não encontrado!')
                    break

            elif acao == '3':
                self.ir_ao_medico()

            elif acao == '4':
                break

    @classmethod
    def listar_torres(cls):  # Mudei para método de classe
        for torre in lista_torres:
            print(f'{torre.nome}')

        escolha = input('Escolha uma torre: ')
        torre_escolhida = next((torre for torre in lista_torres if torre.nome.lower() == escolha.lower()), None)
        if torre_escolhida:
            cls.ver_torre(torre_escolhida)
        else:
            print('Escolha inválida')

    @classmethod
    def ver_torre(cls, torre):  # Mudei para método de classe
        print(f'Nome: {torre.nome}\nMonstro: {torre.monstro.nome}\nHP: {torre.monstro.hp_atual}/{torre.monstro.hp_max}\nAtaque: {torre.monstro.atk}\nDefesa: {torre.monstro.dfs}\nVelocidade: {torre.monstro.spd}\nNível: {torre.monstro.level}')
        print(f'Capanga: {torre.capanga.nome}\nHP: {torre.capanga.hp_atual}/{torre.capanga.hp_max}\nAtaque: {torre.capanga.atk}\nDefesa: {torre.capanga.dfs}\nVelocidade: {torre.capanga.spd}\nNível: {torre.capanga.level}')

    @classmethod
    def inicio(cls):
        while True:
            print('=' * 40)
            acao_inicial = input('Qual ação você quer tomar agora?\n1. Ver personagens disponíveis\n2. Ver Torre do Poder\n3. Criar Personagem\n4. Sentar e Descansar\n-> ')
            if acao_inicial == '1':
                cls.escolhe_personagem()
                personagem_nome = input('Com qual personagem você quer jogar? ')
                personagem = next((p for p in lista_personagens if p.nome == personagem_nome), None)
                if personagem:
                    personagem.acoes()
                else:
                    print('Personagem não encontrado!')
            elif acao_inicial == '2':
                cls.listar_torres()  # Isso agora chamará o método de classe
            elif acao_inicial == '3':
                print('Criar Personagem (ainda não implementado)')
            elif acao_inicial == '4':
                break
            else:
                print('Opção inválida, tente novamente!')
