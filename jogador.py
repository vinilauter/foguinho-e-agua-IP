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

        self.forca_pulo = -15  # Força inicial do pulo (negativa para subir)
        self.gravidade = 0.5   # Aceleração da gravidade (queda)
        self.vel_y_max = 10    # Velocidade máxima na queda

    def update(self, teclas):
        self.vel_x = 0

        if teclas[self.controles["esquerda"]]:
            self.vel_x = -4
        if teclas[self.controles["direita"]]:
            self.vel_x = 4

        if teclas[self.controles["pular"]] and self.pode_pular:
            self.vel_y = self.forca_pulo
            self.pode_pular = False

    def aplicar_gravidade(self):
        """Atualiza velocidade vertical do jogador."""
        if self.vel_y < self.vel_y_max:
            self.vel_y += self.gravidade
        # Não atualiza a posição aqui para evitar movimento duplo

    def checar_colisao(self, plataformas):
        self.pode_pular = False

        # Movimento e colisão no eixo X
        self.rect.x += self.vel_x
        for plataforma in plataformas:
            # Verifica se 'plataforma' tem o atributo 'rect'; se não, assume que é pygame.Rect direto
            rect_plataforma = plataforma.rect if hasattr(plataforma, 'rect') else plataforma
            if self.rect.colliderect(rect_plataforma):
                if self.vel_x > 0:
                    self.rect.right = rect_plataforma.left
                elif self.vel_x < 0:
                    self.rect.left = rect_plataforma.right
                self.vel_x = 0

        # Movimento e colisão no eixo Y
        self.rect.y += self.vel_y
        for plataforma in plataformas:
            rect_plataforma = plataforma.rect if hasattr(plataforma, 'rect') else plataforma
            if self.rect.colliderect(rect_plataforma):
                if self.vel_y > 0 and self.rect.bottom <= rect_plataforma.bottom:
                    self.rect.bottom = rect_plataforma.top
                    self.vel_y = 0
                    self.pode_pular = True
                elif self.vel_y < 0:
                    self.rect.top = rect_plataforma.bottom
                    self.vel_y = 0


    def desenhar(self, tela):
        """Desenha o jogador na tela."""
        tela.blit(self.image, self.rect)