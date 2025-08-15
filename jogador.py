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

        self.forca_pulo = -12.5
        self.gravidade = 0.5
        self.vel_y_max = 10

        self.velocidade_normal = 4
        self.velocidade_atual = self.velocidade_normal
        self.powerup_ativo = False
        self.tempo_fim_powerup = 0

    def update(self, teclas):
        if self.powerup_ativo and pygame.time.get_ticks() > self.tempo_fim_powerup:
            self.desativar_powerup_velocidade()

        self.vel_x = 0
        if teclas[self.controles["esquerda"]]:
            self.vel_x = -self.velocidade_atual
        if teclas[self.controles["direita"]]:
            self.vel_x = self.velocidade_atual

        if teclas[self.controles["pular"]] and self.pode_pular:
            self.vel_y = self.forca_pulo
            self.pode_pular = False

    def ativar_powerup_velocidade(self, duracao_ms):
        self.powerup_ativo = True
        self.velocidade_atual = self.velocidade_normal * 1.75
        self.tempo_fim_powerup = pygame.time.get_ticks() + duracao_ms

    def desativar_powerup_velocidade(self):
        self.powerup_ativo = False
        self.velocidade_atual = self.velocidade_normal

    def aplicar_gravidade(self):
        if self.vel_y < self.vel_y_max:
            self.vel_y += self.gravidade

    def checar_colisao(self, plataformas):
        self.rect.x += self.vel_x
        
        if hasattr(self, 'hitbox'):
            self.hitbox.centerx = self.rect.centerx
            for plataforma in plataformas:
                rect_plataforma = plataforma.rect if hasattr(plataforma, 'rect') else plataforma
                if self.hitbox.colliderect(rect_plataforma):
                    if self.vel_x > 0:
                        self.hitbox.right = rect_plataforma.left
                    if self.vel_x < 0:
                        self.hitbox.left = rect_plataforma.right
                    self.rect.centerx = self.hitbox.centerx
        
        self.rect.y += self.vel_y
        self.pode_pular = False
        
        if hasattr(self, 'hitbox'):
            self.hitbox.centery = self.rect.centery
            for plataforma in plataformas:
                rect_plataforma = plataforma.rect if hasattr(plataforma, 'rect') else plataforma
                if self.hitbox.colliderect(rect_plataforma):
                    if self.vel_y > 0:
                        self.hitbox.bottom = rect_plataforma.top
                        self.pode_pular = True
                        self.vel_y = 0
                    if self.vel_y < 0:
                        self.hitbox.top = rect_plataforma.bottom
                        self.vel_y = 0
                    self.rect.centery = self.hitbox.centery
    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
