import pygame
from jogador import Jogador

class Foguinho(Jogador):
    def __init__(self, posicao_x, posicao_y, controles):
        cor = (200, 50, 50)  # Vermelho
        super().__init__(posicao_x, posicao_y, cor, controles)
        self.image = pygame.image.load("fireboy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.retangulo = self.image.get_rect(topleft=(posicao_x, posicao_y))
