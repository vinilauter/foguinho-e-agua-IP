import pygame
from foguinho import Foguinho
from agua import Agua

class Porta_final(pygame.sprite.Sprite):
    def __init__(self, posicao, elemento, trancada=True):
        super().__init__()

        self.posicao = posicao
        self.trancada = trancada

        self.image = pygame.image.load(f'porta_{elemento}.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=posicao)

        tamanho_porta=self.rect.size
        self.img_destrancada = pygame.Surface(tamanho_porta, pygame.SRCALPHA)

    def destrancar(self,diamantes_coletados):

        if diamantes_coletados:
            self.trancada = False

        

