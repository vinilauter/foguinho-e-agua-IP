import pygame

class Porta_final(pygame.sprite.Sprite):
    def __init__(self, posicao, elemento, trancada=True):
        super().__init__()
        self.posicao = posicao
        self.trancada = trancada

        # Imagem da porta trancada (diferente para cada elemento)
        self.image_trancada = pygame.image.load(f'Imagens/porta_{elemento}_trancada.png').convert_alpha()
        # Imagem da porta destrancada (fundo da porta aberta)
        self.image_destrancada = pygame.image.load('Imagens/porta_aberta.png').convert_alpha()
        # Imagem extra que será mostrada dentro da porta quando destrancada
        self.imagem_extra = pygame.image.load('Imagens/interior_porta.png').convert_alpha()
        
        self.image = self.image_trancada if trancada else self.image_destrancada
        self.rect = self.image.get_rect(midbottom=posicao)

    def destrancar(self, diamantes_coletados):
        if diamantes_coletados and self.trancada:
            self.trancada = False
            self.image = self.image_destrancada
            self.rect = self.image.get_rect(midbottom=self.posicao)  # Atualiza o retângulo

    def desenhar(self, tela):
        # Desenha a porta
        tela.blit(self.image, self.rect)

        # Se destrancada, desenha a imagem extra dentro da porta
        if not self.trancada:
            # Posicione a imagem extra no centro da porta
            pos_x = self.rect.centerx - self.imagem_extra.get_width() // 2
            pos_y = self.rect.centery - self.imagem_extra.get_height() // 2
            tela.blit(self.imagem_extra, (pos_x, pos_y))
