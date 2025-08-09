import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, controles):
        super().__init__()
        self.cor = cor
        self.image = pygame.Surface((40, 60))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.controles = controles
        self.vel_x = 0
        self.vel_y = 0
        self.pode_pular = False

        self.forca_pulo = -10  # Força inicial do pulo (negativa para subir)
        self.gravidade = 0.5   # Aceleração da gravidade (queda)
        self.vel_y_max = 10    # Velocidade máxima na queda

    def update(self, teclas):
        """Atualiza o movimento horizontal e aplica o pulo."""
        self.vel_x = 0

        if teclas[self.controles["esquerda"]]:
            self.vel_x = -4
        if teclas[self.controles["direita"]]:
            self.vel_x = 4

        if teclas[self.controles["pular"]] and self.pode_pular:
            self.vel_y = self.forca_pulo
            self.pode_pular = False

        self.rect.x += self.vel_x

    def aplicar_gravidade(self):
        """Aplica gravidade ao jogador e atualiza sua posição vertical."""
        if self.vel_y < self.vel_y_max:
            self.vel_y += self.gravidade
        self.rect.y += self.vel_y

    def checar_colisao(self, plataformas):
        """
        Verifica colisões verticais com plataformas e ajusta posição e estado de pulo.
        Considera somente colisões na vertical (pulo/queda).
        """
        self.pode_pular = False

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vel_y > 0 and self.rect.bottom <= plataforma.rect.bottom:
                    # Colisão descendo (pouso)
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.pode_pular = True
                elif self.vel_y < 0:
                    # Colisão subindo (batida na cabeça)
                    self.rect.top = plataforma.rect.bottom
                    self.vel_y = 0

    def desenhar(self, tela):
        """Desenha o jogador na tela."""
        tela.blit(self.image, self.rect)
