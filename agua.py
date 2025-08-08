import pygame
from jogador import Jogador

class Agua(Jogador):
    def __init__(self, posicao_x, posicao_y, controles):
        cor = (50, 100, 255)  # Azul 
        super().__init__(posicao_x, posicao_y, cor, controles)
        self.image = pygame.image.load("watergirl.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.retangulo = self.image.get_rect(topleft=(posicao_x, posicao_y))
