import pygame
from pytmx.util_pygame import load_pygame # Importa a função para carregar mapas TMX

# Cores
CINZA = (128, 128, 128)
AGUA_COR = (100, 150, 250)
FOGO_COR = (255, 100, 0)
VERMELHO_OBJ = (200, 50, 50)
AZUL_OBJ = (50, 100, 255)

class Plataforma:
    """Representa uma plataforma retangular sólida no jogo."""
    def __init__(self, x, y, largura, altura):
        self.retangulo = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, CINZA, self.retangulo)

class Lago:
    """Representa uma poça de água ou fogo, causando dano ao jogador errado."""
    def __init__(self, x, y, largura, altura, cor):
        self.retangulo = pygame.Rect(x, y, largura, altura)
        self.cor = cor # Pode ser AGUA_COR ou FOGO_COR

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.retangulo)

class Objetivo:
    """Representa o ponto final que os jogadores devem alcançar."""
    def __init__(self, x, y, cor):
        self.retangulo = pygame.Rect(x, y, 40, 60)
        self.cor = cor # Cor do jogador que deve atingir este objetivo

    def desenhar(self, tela):
        # Desenha apenas o contorno para indicar que é um objetivo
        pygame.draw.rect(tela, self.cor, self.retangulo, 3)

class PlataformaAngulada:
    """Representa uma plataforma com formato não retangular, como uma rampa."""
    def __init__(self, x, y, imagem_path):
        # Carrega a imagem da rampa e a converte com canal alpha para transparência
        self.imagem_original = pygame.image.load(imagem_path).convert_alpha()
        self.imagem = self.imagem_original
        # Obtém o retângulo que envolve a imagem
        self.rect = self.imagem.get_rect(topleft=(x, y))
        # Cria uma máscara de pixel a partir da imagem para colisões precisas
        self.mask = pygame.mask.from_surface(self.imagem)

    def desenhar(self, tela):
        """Desenha a plataforma angulada na tela."""
        tela.blit(self.imagem, self.rect)

class Nivel1:
    """Define a estrutura e os elementos do Nível 1 do jogo, carregados de um mapa Tiled."""
    def __init__(self, largura, altura, arquivo_mapa_tmx):
        self.largura = largura
        self.altura = altura
        self.plataformas = [] 
        self.perigos = [] 
        self.objetivos = []
        self.plataformas_anguladas = []
        
        # Carrega o mapa Tiled
        self.tmx_data = load_pygame(arquivo_mapa_tmx)
        
        # Calcula o tamanho total do mapa em pixels
        self.mapa_largura_px = self.tmx_data.width * self.tmx_data.tilewidth
        self.mapa_altura_px = self.tmx_data.height * self.tmx_data.tileheight
        
        # Cria uma superfície para renderizar as camadas de tiles (fundo)
        # Isso é mais eficiente, pois desenha o mapa uma vez e depois apenas "blita" essa superfície
        self.bg_surface = pygame.Surface((self.mapa_largura_px, self.mapa_altura_px), pygame.SRCALPHA)
        self._desenhar_camadas_de_tiles()

        self._criar_elementos_do_mapa()

    def _desenhar_camadas_de_tiles(self):
        """Desenha todas as camadas de tiles do Tiled na superfície de fundo."""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'): # Verifica se é uma camada de tiles
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Desenha o tile na posição correta na superfície de fundo
                        self.bg_surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def _criar_elementos_do_mapa(self):
        """Cria as instâncias dos objetos (plataformas, perigos, etc.) a partir das camadas de objeto do Tiled."""
        for obj_group in self.tmx_data.objectgroups:
            if obj_group.name == 'Plataformas':
                for obj in obj_group:
                    self.plataformas.append(Plataforma(obj.x, obj.y, obj.width, obj.height))
            
            elif obj_group.name == 'Perigos':
                for obj in obj_group:
                    cor_str = obj.properties.get('cor', 'agua') # 'agua' é o padrão se a propriedade não existir
                    cor_map = AGUA_COR if cor_str == 'agua' else FOGO_COR
                    self.perigos.append(Lago(obj.x, obj.y, obj.width, obj.height, cor_map))

            elif obj_group.name == 'Objetivos':
                for obj in obj_group:
                    cor_str = obj.properties.get('cor', 'vermelho') # 'vermelho' é o padrão
                    cor_map = VERMELHO_OBJ if cor_str == 'vermelho' else AZUL_OBJ
                    self.objetivos.append(Objetivo(obj.x, obj.y, cor_map))

            elif obj_group.name == 'Rampas':
                for obj in obj_group:
                    imagem_path = obj.properties.get('imagem')
                    if imagem_path:
                        self.plataformas_anguladas.append(PlataformaAngulada(obj.x, obj.y, imagem_path))


    def desenhar(self, tela):
        """Desenha todos os elementos do nível na tela."""
        # Desenha a superfície de fundo pré-renderizada
        tela.blit(self.bg_surface, (0, 0))
        
        # Desenha os objetos interativos
        for plataforma in self.plataformas:
            plataforma.desenhar(tela)
        for perigo in self.perigos:
            perigo.desenhar(tela)
        for objetivo in self.objetivos:
            objetivo.desenhar(tela)
        for plataforma_angulada in self.plataformas_anguladas:
            plataforma_angulada.desenhar(tela)
