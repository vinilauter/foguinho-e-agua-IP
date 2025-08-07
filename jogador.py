import pygame
from foguinho import Foguinho
from agua import Agua

class Jogador(pygame.sprite.Sprite):
    def __init__(self, posicao_x, posicao_y, controles):
        super().__init__()
        self.image = pygame.Surface((40, 60))  # Substituído pelas imagens nas subclasses
        self.rect = self.image.get_rect()
        self.rect.topleft = (posicao_x, posicao_y)

        self.controles = controles
        self.vel_x = 0
        self.vel_y = 0

    def update(self, teclas):
        self.vel_x = 0
        if teclas[self.controles['esquerda']]:
            self.vel_x = -5
        if teclas[self.controles['direita']]:
            self.vel_x = 5
        self.rect.x += self.vel_x

# Controles dos personagens
controles_fogo = {
    'pular': pygame.K_UP,
    'esquerda': pygame.K_LEFT,
    'direita': pygame.K_RIGHT   
}

controles_agua = {
    'pular': pygame.K_w,
    'esquerda': pygame.K_a,
    'direita': pygame.K_d
}

# Jogadores
foguinho = Foguinho(posicao_x, posicao_y, controles_fogo)
agua = Agua(posicao_x, posicao_y, controles_agua)

jogadores = pygame.sprite.Group()
jogadores.add(foguinho)
jogadores.add(agua)
