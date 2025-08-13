import pygame

class PUP_Velocidade(pygame.sprite.Sprite):
    def __init__(self, posicao):

        super().__init__()

        imagem_pup = pygame.image.load("Imagens/velocidade.png").convert_alpha()

        tamanho_pup = (50, 50)
        self.image = pygame.transform.smoothscale(imagem_pup, tamanho_pup)

        self.rect = self.image.get_rect(center=posicao)

    def checkar_colisao(self, jogador):
        if jogador.rect.colliderect(self.rect):
            self.kill()
            return True
        return False

