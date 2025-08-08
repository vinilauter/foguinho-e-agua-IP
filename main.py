import pygame
import sys
from nivel import criar_primeiro_nivel, Lago
from plataforma_movel import PlataformaMovel, Botao_Plataforma_Movel
from alavanca import Alavanca
from jogador import Jogador
from foguinho import Foguinho
from agua import Agua
from diamante import (carregar_sprites_diamantes, DiamanteVermelho, DiamanteAzul)
from cronometro import Cronometro
from porta_final import Porta_final
from plataforma_vertical_alavanca import Plataforma_movel_vertical

pygame.init()
LARGURA, ALTURA = 800, 600
JANELA = pygame.display.set_mode((LARGURA, ALTURA))

carregar_sprites_diamantes()
pygame.display.set_caption("Fogo & Água: Python Version")
FPS = 60

BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
PRETO = (0, 0, 0)

MENU, JOGANDO, VITORIA = "menu", "jogando", "vitoria"

class Jogo:
    def __init__(self):
        self.alavancas = pygame.sprite.Group()
        self.alavancas.add(Alavanca((400, 430), "branca"), Alavanca((600, 170), "azul"))
        
        self.relogio = pygame.time.Clock()
        self.fonte_geral = pygame.font.Font(None, 36)
        self.fonte_titulo = pygame.font.Font(None, 74)
        self.estado = MENU
        self.cronometro = Cronometro(fonte=self.fonte_geral, posicao=(0,0), cor=BRANCO)

        # <-- MUDANÇA: Carrega a imagem da moldura
        self.moldura_timer_img = pygame.image.load("Imagens/moldura_timer.png").convert_alpha()
        self.moldura_timer_img = pygame.transform.scale(self.moldura_timer_img, (120, 50))  # Novo tamanho
        self.moldura_timer_rect = self.moldura_timer_img.get_rect(midtop=(LARGURA // 2, 10))  # Centraliza no topo
        
        # <-- MUDANÇA: Ajusta a posição e a fonte do cronômetro para caber dentro da moldura
        self.cronometro.posicao = self.moldura_timer_rect.center # Define a posição do texto como o centro da moldura
        self.cronometro.fonte = pygame.font.Font(None, 28) # Ajusta a fonte para um tamanho menor
        self.cronometro.centralizado = True # Ativa a flag de centralização do texto
        
        nivel = criar_primeiro_nivel()

        self.jogador1 = nivel["jogador1"]
        self.jogador2 = nivel["jogador2"]
        self.plataformas = nivel["plataformas"]
        self.botao_movel_1 = nivel["botao_movel_1"]
        self.botao_movel_2 = nivel["botao_movel_2"]
        self.plataforma_movel = nivel["plataforma_movel"]
        self.lagos = nivel["lagos"]
        self.porta_fogo = nivel["porta_fogo"]
        self.porta_agua = nivel["porta_agua"]
        self.diamantes = nivel["diamantes"]

    def executar(self):
        while True:
            self.relogio.tick(FPS)
            self.tratar_eventos()
            self.atualizar()
            self.desenhar()

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if self.estado == MENU and evento.key == pygame.K_SPACE:
                    self.estado = JOGANDO
                    self.cronometro.reset()
                elif self.estado == VITORIA and evento.key == pygame.K_r:
                    self.__init__()

    def atualizar(self):
        if self.estado != JOGANDO: return

        teclas = pygame.key.get_pressed()
        self.jogador1.update(teclas)
        self.jogador2.update(teclas)
        self.alavancas.update()
        self.cronometro.update()

        for jogador in [self.jogador1, self.jogador2]:
            jogador.aplicar_gravidade()
            jogador.checar_colisao(self.plataformas)

        self.botao_movel_1.verificar_ativacao([self.jogador1, self.jogador2])
        self.botao_movel_2.verificar_ativacao([self.jogador1, self.jogador2])
        
        # Ativa a plataforma se pelo menos um botão estiver pressionado
        ativado = self.botao_movel_1.pressionado or self.botao_movel_2.pressionado
        self.plataforma_movel.atualizar(ativado)

        for jogador in [self.jogador1, self.jogador2]:
            for lago in self.lagos:
                if jogador.rect.colliderect(lago.retangulo):
                    # Lógica de morte/reinício
                    self.__init__()
                    return

        for diamante in self.diamantes:
            for jogador in [self.jogador1, self.jogador2]:
                diamante.checar_coleta(jogador)

        for alavanca in self.alavancas:
            for jogador in [self.jogador1, self.jogador2]:
                if jogador.rect.colliderect(alavanca.rect) and not alavanca.ativada:
                    alavanca.toggle()

        todos_coletados = all(d.coletado for d in self.diamantes)
        if todos_coletados and self.jogador1.rect.colliderect(self.porta.retangulo) and self.jogador2.rect.colliderect(self.porta.retangulo):
            self.estado = VITORIA
            
    def desenhar_menu(self):
        JANELA.fill(PRETO)
        texto_titulo = self.fonte_titulo.render("Fogo & Água", True, BRANCO)
        rect_titulo = texto_titulo.get_rect(center=(LARGURA / 2, ALTURA / 3))
        texto_instrucao = self.fonte_geral.render("Pressione ESPAÇO para começar", True, CINZA)
        rect_instrucao = texto_instrucao.get_rect(center=(LARGURA / 2, ALTURA / 2))
        JANELA.blit(texto_titulo, rect_titulo)
        JANELA.blit(texto_instrucao, rect_instrucao)

    def desenhar(self):
        JANELA.fill(PRETO)

        if self.estado == MENU:
            self.desenhar_menu()
        elif self.estado == JOGANDO:
            for plataforma in self.plataformas: plataforma.desenhar(JANELA)
            for diamante in self.diamantes: diamante.desenhar(JANELA)
            
            todos_coletados = all(d.coletado for d in self.diamantes)
            if todos_coletados: self.porta.desenhar(JANELA)

            self.alavancas.draw(JANELA)
            self.jogador1.desenhar(JANELA)
            self.jogador2.desenhar(JANELA)
            self.botao_movel_1.desenhar(JANELA)
            self.botao_movel_2.desenhar(JANELA)
            self.plataforma_movel.desenhar(JANELA)
            for lago in self.lagos:
                lago.desenhar(JANELA)
            
            # <-- MUDANÇA: Desenha a moldura PRIMEIRO
            JANELA.blit(self.moldura_timer_img, self.moldura_timer_rect)
            # <-- MUDANÇA: Desenha o cronômetro DEPOIS, para que fique por cima
            self.cronometro.desenhar(JANELA)
            
            total = len(self.diamantes)
            coletados = sum(1 for d in self.diamantes if d.coletado)
            # Usei a fonte_geral para o texto dos diamantes
            self.desenhar_texto(f"Diamantes: {coletados}/{total}", 10, 50, self.fonte_geral)

        elif self.estado == VITORIA:
            self.desenhar_texto("Vocês venceram! Pressione R para reiniciar", 180, 250, self.fonte_titulo)

        pygame.display.flip()

    def desenhar_texto(self, texto, x, y, fonte):
        rotulo = fonte.render(texto, True, BRANCO)
        JANELA.blit(rotulo, (x, y))

if __name__ == "__main__":
    Jogo().executar()