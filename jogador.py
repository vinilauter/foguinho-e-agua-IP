import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, controles):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(cor)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.controles = controles
        self.vel_x = 0
        self.vel_y = 0
        self.pode_pular = False

        self.forca_pulo = -10       # Pulo com força moderada
        self.gravidade = 0.5        # Gravidade mais suave
        self.vel_y_max = 10         # Velocidade terminal na queda

    def update(self, teclas):
        self.vel_x = 0

        if teclas[self.controles["esquerda"]]:
            self.vel_x = -4 
        if teclas[self.controles["direita"]]:
            self.vel_x = 4

        if teclas[self.controles["pular"]] and self.pode_pular:
            self.vel_y = self.forca_pulo
            self.pode_pular = False  # Impede pulo duplo

        self.rect.x += self.vel_x

    def aplicar_gravidade(self):
        if self.vel_y < self.vel_y_max:
            self.vel_y += self.gravidade
        self.rect.y += self.vel_y

    # Pular apenas quando estiver no chão
    def checar_colisao(self, plataformas):
        self.pode_pular = False

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.retangulo):
                if self.vel_y > 0 and self.rect.bottom <= plataforma.retangulo.bottom:
                    self.rect.bottom = plataforma.retangulo.top
                    self.vel_y = 0
                    self.pode_pular = True
                elif self.vel_y < 0:
                    self.rect.top = plataforma.retangulo.bottom
                    self.vel_y = 0

    # Desenha o personagem no local de caida
    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
