import pygame
from jogador import Jogador

class Agua(Jogador):
    def __init__(self, posicao_x, posicao_y, controles):
        super().__init__(posicao_x, posicao_y, controles)
        self.image = pygame.image.load("").convert_alpha() # Definir sprite
        self.image = pygame.transform.scale(self.image, (40, 60)) 
