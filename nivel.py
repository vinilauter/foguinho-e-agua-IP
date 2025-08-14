import pygame
from nova_plataforma_movel import Plataforma_Movel, Botao
from foguinho import Foguinho
from agua import Agua
from diamante import DiamanteVermelho, DiamanteAzul
from porta_final import Porta_final
from plataforma_vertical_alavanca import Plataforma_movel_vertical
from alavanca import Alavanca
from powerupvelocidade import PUP_Velocidade

import pygame

class Plataforma:
    def __init__(self, x, y, largura, altura, tipo="piso"):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.tipo = tipo

        if self.tipo == "piso":
            try:
                self.img_canto_esq = pygame.image.load("imagens/plataforma_canto_esq.png").convert_alpha()
                self.img_meio = pygame.image.load("imagens/plataforma_meio.png").convert_alpha()
                self.img_canto_dir = pygame.image.load("imagens/plataforma_canto_dir.png").convert_alpha()
                self.image = self.img_meio
            except FileNotFoundError:
                # Cria blocos genéricos quando as imagens não existem
                self.img_canto_esq = pygame.Surface((largura, altura))
                self.img_meio = pygame.Surface((largura, altura))
                self.img_canto_dir = pygame.Surface((largura, altura))

                self.img_canto_esq.fill((128, 128, 128))
                self.img_meio.fill((128, 128, 128))
                self.img_canto_dir.fill((128, 128, 128))

                self.image = self.img_meio

        elif self.tipo == "parede":
            try:
                self.blocos_parede = [
                    pygame.image.load("imagens/parede1.png").convert_alpha(),
                    pygame.image.load("imagens/parede2.png").convert_alpha(),
                    pygame.image.load("imagens/parede3.png").convert_alpha()
                ]
                self.image = self.blocos_parede[0]
            except FileNotFoundError:
                # Bloco cinza genérico se não encontrar imagem
                self.image = pygame.Surface((largura, altura))
                self.image.fill((100, 100, 100))

    def desenhar(self, janela):
        if self.tipo == "piso":
            largura_bloco = self.img_meio.get_width()
            altura_bloco = self.img_meio.get_height()
            num_blocos = self.rect.width // largura_bloco

            for i in range(num_blocos):
                if i == 0:
                    janela.blit(self.img_canto_esq, (self.rect.x, self.rect.y))
                elif i == num_blocos - 1:
                    janela.blit(self.img_canto_dir, (self.rect.x + i * largura_bloco, self.rect.y))
                else:
                    janela.blit(self.img_meio, (self.rect.x + i * largura_bloco, self.rect.y))

        elif self.tipo == "parede":
            altura_bloco = self.image.get_height()
            num_blocos = self.rect.height // altura_bloco
            for i in range(num_blocos):
                janela.blit(self.image, (self.rect.x, self.rect.y + i * altura_bloco))

class PisoSimples:
    def __init__(self, x, y, largura, altura, caminho_imagem):
        self.rect = pygame.Rect(x, y, largura, altura)
        try:
            self.image_bloco = pygame.image.load(caminho_imagem).convert_alpha()
            self.image_bloco = pygame.transform.scale(self.image_bloco, (self.rect.height, self.rect.height))
        except FileNotFoundError as e:
            self.image_bloco = pygame.Surface((self.rect.height, self.rect.height))
            self.image_bloco.fill((128, 128, 128))
            
    def desenhar(self, tela):
        largura_bloco = self.image_bloco.get_width()
        for x in range(self.rect.left, self.rect.right, largura_bloco):
            tela.blit(self.image_bloco, (x, self.rect.y))

    def update(self):
        pass

class Lago:
    def __init__(self, x, y, largura, altura, tipo):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.tipo = tipo

        self.frames = []
        self.frame_atual = 0
        self.velocidade_animacao = 250
        self.ultimo_update = pygame.time.get_ticks()
        
        mapeamento = {
            "agua": {
                "nomes": ["lago-azul.png", "lago-azul1.png", "lago-azul2.png", "lago-azul3.png", "lago-azul4.png"],
                "cor": (173, 216, 230)
            },
            "fogo": {
                "nomes": ["lago-vermelho.png", "lago-vermelho1.png", "lago-vermelho2.png", "lago-vermelho3.png", "lago-vermelho4.png"],
                "cor": (255, 100, 0)
            },
            "verde": {
                "nomes": ["lago-verde (1).png", "lago-verde (2).png", "lago-verde (3).png", "lago-verde (4).png", "lago-verde (5).png"],
                "cor": (100, 200, 50)
            }
        }

        carregamento_bem_sucedido = True
        if self.tipo in mapeamento:
            info_lago = mapeamento[self.tipo]
            for nome_arquivo in info_lago["nomes"]:
                try:
                    caminho_imagem = f"Imagens/{nome_arquivo}"
                    imagem = pygame.image.load(caminho_imagem).convert_alpha()
                    imagem_redimensionada = pygame.transform.scale(imagem, (largura, altura))
                    self.frames.append(imagem_redimensionada)
                except FileNotFoundError:
                    carregamento_bem_sucedido = False
                    break
            
            if not carregamento_bem_sucedido or not self.frames:
                self.frames = [pygame.Surface((largura, altura))]
                self.frames[0].fill(info_lago["cor"])
        else:
            self.frames = [pygame.Surface((largura, altura))]
            self.frames[0].fill((128, 128, 128))
        
        self.image = self.frames[self.frame_atual]

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.velocidade_animacao:
            self.ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.image = self.frames[self.frame_atual]

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

def criar_primeiro_nivel():
    ALTURA = 720
    LARGURA = 1280
    
    plataformas = [
        PisoSimples(20, ALTURA - 38, 252, 40, "Imagens/piso3.png"),
        PisoSimples(460, ALTURA - 38, 60, 40, "Imagens/piso3.png"),
        PisoSimples(700, ALTURA - 38, LARGURA - 623, 40, "Imagens/piso3.png"),

        Plataforma(0, 0, LARGURA, 20, "parede"),
        Plataforma(0, 0, 20, ALTURA, "parede"),
        Plataforma(LARGURA - 20, 0, 20, ALTURA, "parede"),

        Plataforma (20, 150, 216, 32, "piso"),
        Plataforma(100, 560, 216, 32, "piso"), 
        Plataforma(500, 560, 216, 32, "piso"), 
        Plataforma(300, 440, 216, 32, "piso"),
        Plataforma(800, 440, 216, 32, "piso"),
        Plataforma(20, 320, 752, 32, "piso"),
        Plataforma(908.9, 320, 96, 32, "piso"),
        Plataforma(290, 102, 216, 32, "piso"),
        Plataforma(600, 180, 100, 32, "piso"),
    ]

    botao_movel_1 = Botao(330, 440 - 12)
    botao_movel_2 = Botao(800, ALTURA - 40 - 12)
    plataforma_movel = Plataforma_Movel(1126, 200, 200, 60, 520, 2)

    lagos = [
        Lago(300, ALTURA - 30, 160, 30, "agua"),
        Lago(540, ALTURA - 30, 160, 30, "fogo"),
        Lago(752, ALTURA - 400, 160, 30, "verde")
    ]

    altura_porta = 119
    porta_agua = Porta_final((1200 , 812 - altura_porta), "agua", trancada=True)
    porta_fogo = Porta_final((80, 160), "fogo", trancada=True)

    jogador1 = Agua(100, ALTURA - 80, {"esquerda": pygame.K_a, "direita": pygame.K_d, "pular": pygame.K_w})
    jogador2 = Foguinho(200, ALTURA - 80, {"esquerda": pygame.K_LEFT, "direita": pygame.K_RIGHT, "pular": pygame.K_UP})

    diamantes = [
        DiamanteVermelho(120, 250),
        DiamanteAzul(660, 250),
        DiamanteVermelho(660, 450),
        DiamanteAzul(420, 720 - 60),
    ]



    #  power-ups
    powerup_1 = PUP_Velocidade((200, ALTURA - 180)) 
    powerup_2 = PUP_Velocidade((600, ALTURA - 50)) 

    # power-ups em uma lista
    powerups = [powerup_1, powerup_2]

    alavanca1 = Alavanca((500, 344), "verde")
    alavanca2 = Alavanca((600, 584), "azul")

    alavancas = [alavanca1, alavanca2]

    plataformas_verticais = [
        Plataforma_movel_vertical(
            posicao_inicial=(1000, 50),
            posicao_final=(1000, 500),
            alavanca_designada=alavanca2,
            cor="azul"
        ),
        Plataforma_movel_vertical(
            posicao_inicial=(150, 150),
            posicao_final=(150, 500),
            alavanca_designada=alavanca1,
            cor="verde"
        )
    ]

    return {
        "jogador1": jogador1,
        "jogador2": jogador2,
        "plataformas": plataformas,
        "botao_movel_1": botao_movel_1,
        "botao_movel_2": botao_movel_2,
        "plataforma_movel": plataforma_movel,
        "lagos": lagos,
        "porta_fogo": porta_fogo,
        "porta_agua": porta_agua,
        "diamantes": diamantes,
        "alavancas": alavancas,
        "plataformas_verticais": plataformas_verticais,
        "plataformas_moveis_alavanca": plataformas_verticais,
        "powerups": powerups 
    }
