import pygame
from jogador import Jogador

class Agua(Jogador):
    def __init__(self, pos_x, pos_y, controles):
        cor = (50, 100, 255)
        super().__init__(pos_x, pos_y, cor, controles)
        self.image = pygame.image.load("Imagens/watergirl.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 70))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
