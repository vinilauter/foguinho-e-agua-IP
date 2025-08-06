import pygame

pygame.init()
tela = pygame.display.set_mode((largura, altura)) # Tamanho da tela não definido | Criador do nível...

# Classe jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self, cor, controles):
        super().__init__()
        self.image = pygame.Surface((40, 60))  # Tamanho padrão do personagem | Só um exemplo, a gnt discute
        self.image.fill(cor)
        self.rect = self.image.get_rect()  # Posição inicial não definida | Criador do nível...

        self.controles = controles
        self.vel_x = 0
        self.vel_y = 0

    def update(self, teclas):
        self.vel_x = 0

        if teclas[self.controles['esquerda']]:
            self.vel_x = -5
        if teclas[self.controles['direita']]:
            self.vel_x = 5

        # Movimento lateral
        self.rect.x += self.vel_x


# Controles
controles_fogo = {
    'pular': pygame.K_UP,
    'esquerda': pygame.K_LEFT,
    'direita': pygame.K_RIGHT
}

controles_agua = {
    'pular': pygame.K_w,
    'esquerda': pygame.K_a,
    'direita': pygame.K_d
}

# Criação dos personagens
fogo = Jogador((255, 0, 0), controles_fogo)
agua = Jogador((0, 0, 255), controles_agua)

# Posição inicial não definida | Criador do nível...
# fogo.rect.topleft = (100, 300)
# agua.rect.topleft = (200, 300)

# Grupo de sprites
jogadores = pygame.sprite.Group()
jogadores.add(fogo, agua)