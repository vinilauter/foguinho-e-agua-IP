# mechanics/level.py

import pygame

class Platform:
    # A classe da sua plataforma
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)

class PocaDeAgua:
    # A classe da sua poça de água
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.tipo = "agua"
    
    def draw(self, screen):
        pygame.draw.rect(screen, (100, 150, 250), self.rect)
        
class Nivel:
    def __init__(self):
        self.platforms = []
        self.water_pools = []

        # Chão
        chao = Platform(x=0, y=550, width=800, height=50)
        self.platforms.append(chao)
        
        # Plataforma do meio
        plataforma_meio = Platform(x=200, y=400, width=400, height=30)
        self.platforms.append(plataforma_meio)

        # Poça de água
        poca = PocaDeAgua(x=500, y=500, width=100, height=50)
        self.water_pools.append(poca)

    def draw(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
        
        for pool in self.water_pools:
            pool.draw(screen)