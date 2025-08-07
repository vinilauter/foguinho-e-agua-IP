import pygame
import sys
from alavanca import Alavanca
from jogador import Jogador
from foguinho import Foguinho
from agua import Agua
from plataforma_movel import (Botao_Plataforma_Movel, PlataformaMovel)
from diamantes import (carregar_sprites_diamantes, DiamanteVermelho, DiamanteAzul, COR_DIAMANTE_VERMELHO, COR_DIAMANTE_AZUL)

pygame.init()
LARGURA, ALTURA = 800, 600
JANELA = pygame.display.set_mode((LARGURA, ALTURA))

carregar_sprites_diamantes()
pygame.display.set_caption("Fogo & Água: Python Version")
FPS = 60

BRANCO = (255, 255, 255)
VERMELHO = (200, 50, 50)
AZUL = (50, 100, 255)
CINZA = (128, 128, 128)
PRETO = (0, 0, 0)

MENU, JOGANDO, VITORIA = "menu", "jogando", "vitoria"

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

class Porta:
    def __init__(self, x, y):
        self.retangulo = pygame.Rect(x, y, 50, 80)

    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.retangulo, 3)

class Jogo:
    def __init__(self):
        self.lago = Lago(300, ALTURA - 30, 200, 40)
        self.alavancas = pygame.sprite.Group()
        self.alavancas.add(Alavanca((400, 430), "branca"), Alavanca((600, 170), "azul"))
        self.tempo_limite = 60
        self.tempo_inicial = pygame.time.get_ticks()

        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36)
        self.estado = MENU

        self.jogador1 = Foguinho(100, 500, {
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "pular": pygame.K_w
        })

        self.jogador2 = Agua(200, 500, {
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

        self.diamantes = [DiamanteVermelho(180, 420), DiamanteAzul(550, 170), DiamanteVermelho(250, 270)]

        # Instanciar botão e plataforma móvel
        self.botao_movel = Botao_Plataforma_Movel(350, 280)
        self.plataforma_movel = PlataformaMovel(350, 250, 100, 20, 350, velocidade=2)

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
                    self.__init__()

    def atualizar(self):
        teclas = pygame.key.get_pressed()

        if self.estado == JOGANDO:
            self.jogador1.update(teclas)
            self.jogador2.update(teclas)
            self.alavancas.update()

            for jogador in [self.jogador1, self.jogador2]:
                jogador.aplicar_gravidade()
                jogador.checar_colisao(self.plataformas)

            # Atualizar botão e plataforma móvel
            self.botao_movel.verificar_ativacao([self.jogador1, self.jogador2])
            self.plataforma_movel.atualizar(self.botao_movel)

            for jogador in [self.jogador1, self.jogador2]:
                if jogador.rect.colliderect(self.lago.retangulo):
                    self.__init__()
                    return

            for diamante in self.diamantes:
                for jogador in [self.jogador1, self.jogador2]:
                    diamante.checar_coleta(jogador)

            for alavanca in self.alavancas:
                for jogador in [self.jogador1, self.jogador2]:
                    if jogador.rect.colliderect(alavanca.rect) and not alavanca.ativada:
                        alavanca.toggle()

            todos_coletados = all(d.coletado for d in self.diamantes)

            if todos_coletados:
                if (self.jogador1.rect.colliderect(self.porta.retangulo) and
                    self.jogador2.rect.colliderect(self.porta.retangulo)):
                    self.estado = VITORIA

        tempo_passado = (pygame.time.get_ticks() - self.tempo_inicial) / 1000
        self.tempo_restante = max(0, self.tempo_limite - int(tempo_passado))

        if self.tempo_restante == 0 and self.estado == JOGANDO:
            self.__init__()

    def desenhar(self):
        JANELA.fill(PRETO)

        if self.estado == MENU:
            self.desenhar_texto("Pressione ESPAÇO para começar", 200, 250)
        elif self.estado == JOGANDO:
            for plataforma in self.plataformas:
                plataforma.desenhar(JANELA)
            for diamante in self.diamantes:
                diamante.desenhar(JANELA)
            for alavanca in self.alavancas:
                JANELA.blit(alavanca.image, alavanca.rect.topleft)

            todos_coletados = all(d.coletado for d in self.diamantes)
            if todos_coletados:
                self.porta.desenhar(JANELA)
            self.alavancas.draw(JANELA)
            self.jogador1.desenhar(JANELA)
            self.jogador2.desenhar(JANELA)

            # Desenhar botão e plataforma móvel
            self.botao_movel.desenhar(JANELA)
            self.plataforma_movel.desenhar(JANELA)

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
