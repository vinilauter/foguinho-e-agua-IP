import pygame

COR_DIAMANTE_VERMELHO = (255, 100, 100)
COR_DIAMANTE_AZUL = (100, 100, 255)

DIAMANTE_VERMELHO_SPRITE = None
DIAMANTE_AZUL_SPRITE = None

def carregar_sprites_diamantes() :
    """OBS: chame essa função no main.py depois de pygame.init()"""
    global DIAMANTE_VERMELHO_SPRITE, DIAMANTE_AZUL_SPRITE
    DIAMANTE_VERMELHO_SPRITE = pygame.image.load("Imagens/diamante_vermelho.png").convert_alpha()
    DIAMANTE_AZUL_SPRITE = pygame.image.load("Imagens/diamante_azul.png").convert_alpha()


class Diamante :
    """ Classe base para todos os diamantes"""
    
    def __init__(self, x, y):
        self.coletado = False
        self.tipo = None 
        self.image = None
        self.retangulo = None

    def desenhar(self, tela) :
        if not self.coletado :
            tela.blit(self.image, self.retangulo.topleft)
            
    def checar_coleta(self, jogador) :
        if self.coletado :
            return False

        if jogador.retangulo.colliderect(self.retangulo) :
            if jogador.cor == self.tipo :
                self.coletado = True
                return True
        return False

class DiamanteVermelho(Diamante) :
    """ Diamante só coletado pelo jogador vermelho """
    
    def __init__(self, x, y) :
        super().__init__(x, y)
        self.tipo = COR_DIAMANTE_VERMELHO
        self.image = DIAMANTE_VERMELHO_SPRITE
        # Eu posicionei a imagem pelo centro pq se não ia ter que cortar a sprite e pra o programa não faz sentido
        # pq quando o personagem toca no triângulo ele desaparece -> não tem colisão entre o triângulo e os personagens
        self.retangulo = self.image.get_rect(center = (x, y))

class DiamanteAzul(Diamante) :
    """ Diamante só coletado pelo jogador azul """
    
    def __init__(self, x, y) :
        super().__init__(x, y)
        self.tipo = COR_DIAMANTE_AZUL
        self.image = DIAMANTE_AZUL_SPRITE
        # Eu posicionei a imagem pelo centro pq se não ia ter que cortar a sprite e pra o programa não faz sentido
        # pq quando o personagem toca no triângulo ele desaparece -> não tem colisão entre o triângulo e os personagens
        self.retangulo = self.image.get_rect(center = (x, y))
