import pygame
from plataforma_movel import PlataformaMovel, Botao_Plataforma_Movel
from jogador import Jogador
from foguinho import Foguinho
from agua import Agua
from diamante import DiamanteVermelho, DiamanteAzul

class Plataforma:
    def __init__(self, x, y, largura, altura):
        self.retangulo = pygame.Rect(x, y, largura, altura)
    def desenhar(self, tela):
        pygame.draw.rect(tela, (128, 128, 128), self.retangulo)

class Lago:
    def __init__(self, x, y, largura, altura, tipo):
        self.retangulo = pygame.Rect(x, y, largura, altura)
        self.tipo = tipo
    def desenhar(self, tela):
        cor = (173, 216, 230) if self.tipo == "agua" else (255, 100, 0)
        pygame.draw.rect(tela, cor, self.retangulo)

class Porta:
    def __init__(self, x, y):
        self.retangulo = pygame.Rect(x, y, 50, 80)
    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.retangulo, 3)

def criar_primeiro_nivel():
    ALTURA = 600

    plataformas = [
        Plataforma(0, ALTURA - 40, 800, 40),
        Plataforma(100, 480, 200, 20),
        Plataforma(500, 480, 200, 20),
        Plataforma(300, 380, 200, 20),
        Plataforma(0, 280, 200, 20),
        Plataforma(600, 280, 200, 20),
    ]

    botao_movel_1 = Botao_Plataforma_Movel(150, 460)
    botao_movel_2 = Botao_Plataforma_Movel(550, 460)
    plataforma_movel = PlataformaMovel(350, 430, 100, 20, end=200, vel=2)

    lagos = [
        Lago(300, ALTURA - 30, 80, 30, "agua"),
        Lago(420, ALTURA - 30, 80, 30, "lava")
    ]

    porta_fogo = Porta(50, 200)
    porta_agua = Porta(700, 200)

    jogador1 = Foguinho(100, ALTURA - 80, {"esquerda": pygame.K_a, "direita": pygame.K_d, "pular": pygame.K_w})
    jogador2 = Agua(200, ALTURA - 80, {"esquerda": pygame.K_LEFT, "direita": pygame.K_RIGHT, "pular": pygame.K_UP})

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