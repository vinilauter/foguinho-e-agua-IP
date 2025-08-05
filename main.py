﻿import pygame
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 600
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fogo & Água - Nível 1")
FPS = 60
GRAVIDADE = 0.5


# Música de fundo (SE FOR COLOCAR!!)
#pygame.mixer.music.load("musica.mp3") # Música fica no diretório do jogo
#pygame.mixer.music.play(-1)

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (200, 50, 50)
AZUL = (50, 100, 255)
CINZA = (128, 128, 128)
PRETO = (0, 0, 0)

# Estados do jogo
MENU, JOGANDO, VITORIA = "menu", "jogando", "vitoria"

class Jogador:
    def __init__(self, x, y, cor, controles):
        self.retangulo = pygame.Rect(x, y, 40, 60)
        self.cor = cor
        self.controles = controles
        self.vel_y = 0
        self.no_chao = False

    def controlar(self, teclas):
        if teclas[self.controles["esquerda"]]:
            self.retangulo.x -= 5
        if teclas[self.controles["direita"]]:
            self.retangulo.x += 5

        # Limites horizontais
        if self.retangulo.left < 0:
            self.retangulo.left = 0
        if self.retangulo.right > LARGURA:
            self.retangulo.right = LARGURA

        # Pular
        if teclas[self.controles["pular"]] and self.no_chao:
            self.vel_y = -15
            self.no_chao = False
            # som_pulo.play()  (COLOCA SE HOUVER SOM DE PULO)


    def aplicar_gravidade(self):
        self.retangulo.y += self.vel_y
        self.vel_y += GRAVIDADE

    def checar_colisao(self, plataformas):
        self.no_chao = False
        for plataforma in plataformas:
            if self.retangulo.colliderect(plataforma.retangulo):
                if self.vel_y > 0:
                    self.retangulo.bottom = plataforma.retangulo.top
                    self.vel_y = 0
                    self.no_chao = True

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.retangulo)

class Plataforma:
    def __init__(self, x, y, largura, altura):
        self.retangulo = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, CINZA, self.retangulo)

class Lago:
    def __init__(self, x, y, largura, altura):
        self.retangulo = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, (173, 216, 230), self.retangulo)


class Objetivo:
    def __init__(self, x, y, cor):
        self.retangulo = pygame.Rect(x, y, 40, 60)
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.retangulo, 3)

class Diamante:
    def __init__(self, x, y):
        self.retangulo = pygame.Rect(x, y, 20, 20)
        self.coletado = False

    def desenhar(self, tela):
        if not self.coletado:
            pontos = [
                (self.retangulo.centerx, self.retangulo.top),
                (self.retangulo.right, self.retangulo.centery),
                (self.retangulo.centerx, self.retangulo.bottom),
                (self.retangulo.left, self.retangulo.centery)
            ]
            pygame.draw.polygon(tela, (0, 255, 255), pontos)

class Porta:
    def __init__(self, x, y):
        self.retangulo = pygame.Rect(x, y, 50, 80)

    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.retangulo, 3)

class Jogo:
    def __init__(self):
        self.lago = Lago(300, ALTURA - 30, 200, 40)

        self.tempo_limite = 60
        self.tempo_inicial = pygame.time.get_ticks()

        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36)
        self.estado = MENU

        self.jogador1 = Jogador(100, 500, VERMELHO, {
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "pular": pygame.K_w
        })

        self.jogador2 = Jogador(200, 500, AZUL, {
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "pular": pygame.K_UP
        })

        self.plataformas = [
            Plataforma(0, ALTURA - 40, 300, 40),
            Plataforma(500, ALTURA - 40, 300, 40),
            Plataforma(150, 450, 500, 20),
            Plataforma(100, 300, 200, 20),
            Plataforma(500, 200, 200, 20)
        ]

        self.porta = Porta(700, ALTURA - 120)

        self.diamantes = [
            Diamante(180, 420),
            Diamante(550, 170),
            Diamante(250, 270),
        ]

    def executar(self):
        while True:
            self.relogio.tick(FPS)
            self.tratar_eventos()
            self.atualizar()
            self.desenhar()

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if self.estado == MENU and evento.key == pygame.K_SPACE:
                    self.estado = JOGANDO
                elif self.estado == VITORIA and evento.key == pygame.K_r:
                    self.__init__()  # reinicia o jogo

    def atualizar(self):
        teclas = pygame.key.get_pressed()

        if self.estado == JOGANDO:
            self.jogador1.controlar(teclas)
            self.jogador2.controlar(teclas)

            for jogador in [self.jogador1, self.jogador2]:
                jogador.aplicar_gravidade()
                jogador.checar_colisao(self.plataformas)

            # Verifica se o jogador caiu no lago
            for jogador in [self.jogador1, self.jogador2]:
                if jogador.retangulo.colliderect(self.lago.retangulo):
                    self.__init__()  # reinicia o jogo
                    return

            # Verifica coleta de diamantes
            for diamante in self.diamantes:
                for jogador in [self.jogador1, self.jogador2]:
                    if not diamante.coletado and jogador.retangulo.colliderect(diamante.retangulo):
                        diamante.coletado = True

            # Verifica se todos os diamantes foram coletados
            todos_coletados = all(d.coletado for d in self.diamantes)

            # Se todos os diamantes foram coletados, checa entrada na porta
            if todos_coletados:
                if (self.jogador1.retangulo.colliderect(self.porta.retangulo) and
                    self.jogador2.retangulo.colliderect(self.porta.retangulo)):
                    self.estado = VITORIA

        # Atualiza o tempo restante
        tempo_passado = (pygame.time.get_ticks() - self.tempo_inicial) / 1000
        self.tempo_restante = max(0, self.tempo_limite - int(tempo_passado))

        if self.tempo_restante == 0 and self.estado == JOGANDO:
            self.__init__()  # volta para o menu


    def desenhar(self):
        JANELA.fill(PRETO)

        if self.estado == MENU:
            self.desenhar_texto("Pressione ESPAÇO para começar", 200, 250)
        elif self.estado == JOGANDO:
            for plataforma in self.plataformas:
                plataforma.desenhar(JANELA)
            for diamante in self.diamantes:
                diamante.desenhar(JANELA)

            todos_coletados = all(d.coletado for d in self.diamantes)
            if todos_coletados:
                self.porta.desenhar(JANELA)
            self.jogador1.desenhar(JANELA)
            self.jogador2.desenhar(JANELA)
        elif self.estado == VITORIA:
            self.desenhar_texto("Vocês venceram! Pressione R para reiniciar", 180, 250)
        if self.estado == JOGANDO:
            self.lago.desenhar(JANELA)
            self.desenhar_texto(f"Tempo: {self.tempo_restante}", 10, 10)
            total = len(self.diamantes)
            coletados = sum(1 for d in self.diamantes if d.coletado)
            self.desenhar_texto(f"Diamantes: {coletados}/{total}", 10, 40)


        pygame.display.flip()

    def desenhar_texto(self, texto, x, y):
        rotulo = self.fonte.render(texto, True, BRANCO)
        JANELA.blit(rotulo, (x, y))

if __name__ == "__main__":
    Jogo().executar()