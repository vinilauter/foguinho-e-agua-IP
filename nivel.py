import pygame
from nova_plataforma_movel import Plataforma_Movel, Botao
from foguinho import Foguinho
from agua import Agua
from diamante import DiamanteVermelho, DiamanteAzul
from porta_final import Porta_final

class Plataforma:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
    def desenhar(self, tela):
        pygame.draw.rect(tela, (128, 128, 128), self.rect)

class Lago:
    def __init__(self, x, y, largura, altura, tipo):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.tipo = tipo
    def desenhar(self, tela):
        cor = (173, 216, 230) if self.tipo == "agua" else (255, 100, 0)
        pygame.draw.rect(tela, cor, self.rect)

def criar_primeiro_nivel():
    ALTURA = 720
    LARGURA = 1280

    plataformas = [
        # chão
        Plataforma(0, ALTURA - 40, 300, 40),       # antes do lago de água
        Plataforma(460, ALTURA - 40, 60, 40),        # entre os dois lagos
        Plataforma(680, ALTURA - 40, LARGURA - 680, 40),  # depois do lago de lava

        # teto
        Plataforma(0, 0, LARGURA, 20),

        # parede esquerda
        Plataforma(0, 0, 20, ALTURA),

        # parede direita
        Plataforma(LARGURA - 20, 0, 20, ALTURA),

        # plataformas internas
        Plataforma (20, 150, 216, 24),
        Plataforma(100, 560, 216, 24),
        Plataforma(500, 560, 216, 24),
        Plataforma(300, 440, 216, 24),
        Plataforma(800, 440, 216, 24),
        Plataforma(20, 320, 1007, 24),
        Plataforma(400, 200, 216, 24),
    ]

    botao_movel_1 = Botao(150, 460)
    botao_movel_2 = Botao(550, 460)
    plataforma_movel = Plataforma_Movel(1007, 320, 100, 20, 200, 2)

    lagos = [
        Lago(300, ALTURA - 30, 160, 30, "agua"),
        Lago(520, ALTURA - 30, 160, 30, "fogo") # Fogo no lugar de lava para padronizar
    ]

    altura_porta = 121 # TENTAR COLOCAR A PORTA EM CIMA DE ALGUMA PLATAFORMA
    porta_agua = Porta_final((1200 , 812 - altura_porta), "agua", trancada=True)
    porta_fogo = Porta_final((80, 160), "fogo", trancada=True)

    jogador1 = Agua(100, ALTURA - 80, {"esquerda": pygame.K_a, "direita": pygame.K_d, "pular": pygame.K_w})
    jogador2 = Foguinho(200, ALTURA - 80, {"esquerda": pygame.K_LEFT, "direita": pygame.K_RIGHT, "pular": pygame.K_UP})

    diamantes = [
        DiamanteVermelho(120, 250),
        DiamanteAzul(660, 250),
        DiamanteVermelho(320, 350),
        DiamanteAzul(420, 350),
    ]

    return {
        "jogador1": jogador1,
        "jogador2": jogador2,
        "plataformas": plataformas,
        "botao_movel_1": botao_movel_1,
        "botao_movel_2": botao_movel_2,
        "plataforma_movel": plataforma_movel,
        "lagos": lagos,
        "porta_fogo": porta_fogo,
        "porta_agua": porta_agua,
        "diamantes": diamantes
    }
