import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)

class PocaDeAgua:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.tipo = "agua"
    
    def draw(self, screen):
        pygame.draw.rect(screen, (100, 150, 250), self.rect)

class PocaDeFogo:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.tipo = "fogo"
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 100, 0), self.rect) 

class PocaDeLamaVerde:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.tipo = "lama" 
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 150, 0), self.rect)

class Nivel:
    def __init__(self):
        self.platforms = []
        self.water_pools = []
        self.fire_pools = [] 
        self.mud_pools = []  
        
        # Chão
        chao = Platform(x=0, y=550, width=800, height=50)
        self.platforms.append(chao)
        
        # Plataforma do meio
        plataforma_meio = Platform(x=200, y=400, width=400, height=30)
        self.platforms.append(plataforma_meio)

        
        poca_agua = PocaDeAgua(x=200, y=550, width=100, height=50) 
        self.water_pools.append(poca_agua)

        
        poca_fogo = PocaDeFogo(x=500, y=550, width=100, height=50) 
        self.fire_pools.append(poca_fogo)

       
        poca_lama = PocaDeLamaVerde(x=300, y=300, width=80, height=40)
        self.mud_pools.append(poca_lama)
    
    def draw(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
        
        for pool in self.water_pools:
            pool.draw(screen)
        
        for pool in self.fire_pools: 
            pool.draw(screen)
            
        for pool in self.mud_pools:  
            pool.draw(screen)
    
    def verificar_colisao_com_plataforma(self, player_rect):
        for platform in self.platforms:
            if player_rect.colliderect(platform.rect):
                return platform  # Retorna a plataforma para que o jogador possa ajustar sua posição
        return None

    def verificar_colisao_com_perigo(self, player_rect):
        for pool in self.water_pools:
            if player_rect.colliderect(pool.rect):
                return pool.tipo # Retorna "agua"
        
        for pool in self.fire_pools:
            if player_rect.colliderect(pool.rect):
                return pool.tipo # Retorna "fogo"
                
        for pool in self.mud_pools:
            if player_rect.colliderect(pool.rect):
                return pool.tipo # Retorna "lama"
                
        return None
