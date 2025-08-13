import pygame
import sys
from nivel import criar_primeiro_nivel
from alavanca import Alavanca
from cronometro import Cronometro
from diamante import carregar_sprites_diamantes, DiamanteAzul, DiamanteVermelho

pygame.init()
LARGURA, ALTURA = 1280, 720
JANELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Fogo & Água: Python Version")
FPS = 60

BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
PRETO = (0, 0, 0)

MENU, JOGANDO, VITORIA = "menu", "jogando", "vitoria"

class Jogo:
    def __init__(self):
        carregar_sprites_diamantes()  # Não esqueça de chamar essa função antes de criar os diamantes!

        self.relogio = pygame.time.Clock()
        self.fonte_geral = pygame.font.Font(None, 36)
        self.fonte_titulo = pygame.font.Font(None, 74)
        self.estado = MENU
        self.cronometro = Cronometro(fonte=self.fonte_geral, posicao=(0,0), cor=BRANCO)

        # Moldura do timer
        self.moldura_timer_img = pygame.image.load("Imagens/moldura_timer.png").convert_alpha()
        self.moldura_timer_img = pygame.transform.scale(self.moldura_timer_img, (150, 65))
        self.moldura_timer_rect = self.moldura_timer_img.get_rect(midtop=((LARGURA // 2), 0))

        
        # Ajuste do cronômetro para ficar centralizado na moldura do timer
        self.cronometro.fonte = pygame.font.Font(None, 28)
        self.cronometro.centralizado = True
        self.cronometro.posicao = (
            self.moldura_timer_rect.centerx,
            self.moldura_timer_rect.top + self.moldura_timer_rect.height // 2
        )

        # Carrega background e ajusta tamanho
        self.background = pygame.image.load("Imagens/background.png").convert()
        self.background = pygame.transform.scale(self.background, (LARGURA, ALTURA))
        
        # Imagem do menu
        self.imagem_menu = pygame.image.load("Imagens/tela_inicial_jogo.png").convert_alpha()
        self.imagem_menu = pygame.transform.scale(self.imagem_menu, (LARGURA, ALTURA))  # ajusta para a tela toda

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
        self.alavancas = pygame.sprite.Group()
        for alavanca in nivel["alavancas"]:
            self.alavancas.add(alavanca)
        self.plataformas_verticais = pygame.sprite.Group(nivel["plataformas_verticais"])
        self.plataformas_moveis_alavanca = nivel["plataformas_moveis_alavanca"]

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
        if self.estado != JOGANDO: 
            return

        teclas = pygame.key.get_pressed()
        self.jogador1.update(teclas)
        self.jogador2.update(teclas)

        # Aplicar gravidade e checar colisões (encapsulado para cada jogador)
        for jogador in [self.jogador1, self.jogador2]:
            jogador.aplicar_gravidade()
        
            # lagos sólidos para jogador de mesmo tipo do lago
            lagos_solidos = [lago for lago in self.lagos if lago.tipo == jogador.tipo]
        
            # passa plataformas + lagos sólidos para colisão
            jogador.checar_colisao(self.plataformas + [self.plataforma_movel] + list(self.plataformas_moveis_alavanca) + lagos_solidos)
        
        # depois, verifica se jogador colidiu com lago que não é dele — para matar
        for jogador in [self.jogador1, self.jogador2]:
            for lago in self.lagos:
                if jogador.rect.colliderect(lago.rect):
                    if lago.tipo != jogador.tipo:
                        # jogador caiu no lago errado → reinicia jogo
                        self.__init__()
                        return

        # Atualizar ativação dos botões (assumindo que o método se chama atualizar e recebe lista de jogadores)
        self.botao_movel_1.atualizar([self.jogador1, self.jogador2])
        self.botao_movel_2.atualizar([self.jogador1, self.jogador2])
        ativado = self.botao_movel_1.pressionado or self.botao_movel_2.pressionado
        self.plataforma_movel.atualizar(ativado)

        # Mover jogadores junto com a plataforma se estiverem em cima dela
        for jogador in [self.jogador1, self.jogador2]:
            if jogador.rect.colliderect(self.plataforma_movel.rect):
                # Checa se está em cima da plataforma (não do lado ou dentro)
                if abs(jogador.rect.bottom - self.plataforma_movel.rect.top) <= 5:
                    jogador.rect.y += self.plataforma_movel.velocidade_y

        # Reiniciar nível se jogador cair na água ou lava
        for jogador in [self.jogador1, self.jogador2]:
            for lago in self.lagos:
                if jogador.rect.colliderect(lago.rect): # Só reinicia se Fogo cair na Àgua e vice-versa
                    if (jogador.tipo == "fogo" and lago.tipo == "agua") or (jogador.tipo == "agua" and lago.tipo == "fogo"):
                        self.__init__()
                        return

        # Checar coleta dos diamantes para cada jogador
        for jogador in [self.jogador1, self.jogador2]:
            for diamante in self.diamantes[:]:
                if jogador.tipo == "agua" and isinstance(diamante, DiamanteAzul) and jogador.rect.colliderect(diamante.rect):
                    self.diamantes.remove(diamante)
                elif jogador.tipo == "fogo" and isinstance(diamante, DiamanteVermelho) and jogador.rect.colliderect(diamante.rect):
                    self.diamantes.remove(diamante)

        # Atualiza cronômetro e alavancas
        self.alavancas.update()
        self.cronometro.update()
        for jogador in [self.jogador1, self.jogador2]:
            for alavanca in self.alavancas:
                alavanca.check_colisao(jogador)
        for plataforma in self.plataformas_moveis_alavanca:
            plataforma.update()
        self.plataformas_verticais.update()

        # Destrancar portas se todos os diamantes coletados
        todos_coletados = not self.diamantes

        # Define jogadores por tipo
        jogadores = [self.jogador1, self.jogador2]
        jogador_fogo = next((j for j in jogadores if j.tipo == "fogo"), None)
        jogador_agua = next((j for j in jogadores if j.tipo == "agua"), None)

        # Destranca portas apenas quando jogador certo encostar, e todos os diamantes forem coletados
        if todos_coletados:
            if jogador_fogo and jogador_fogo.rect.colliderect(self.porta_fogo.rect):
                self.porta_fogo.destrancar()
            if jogador_agua and jogador_agua.rect.colliderect(self.porta_agua.rect):
                self.porta_agua.destrancar()

            # Verifica vitória: ambos jogadores nas portas destrancadas
            if (jogador_fogo and not self.porta_fogo.trancada and jogador_fogo.rect.colliderect(self.porta_fogo.rect) and
                jogador_agua and not self.porta_agua.trancada and jogador_agua.rect.colliderect(self.porta_agua.rect)):
                self.estado = VITORIA

    def desenhar_menu(self):
        JANELA.blit(self.imagem_menu, (0, 0))

        # Retângulo semitransparente atrás do texto para destacar
        s = pygame.Surface((LARGURA, 150), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        JANELA.blit(s, (0, ALTURA//3 - 50))
        texto_instrucao = self.fonte_geral.render("Pressione ESPAÇO para começar", True, CINZA)
        rect_instrucao = texto_instrucao.get_rect(center=(LARGURA / 2, ALTURA / 2.75))
        JANELA.blit(texto_instrucao, rect_instrucao)

    def desenhar(self):
        # Desenha o background primeiro para ficar atrás de tudo
        JANELA.blit(self.background, (0, 0))

        if self.estado == MENU:
            self.desenhar_menu()

        elif self.estado == JOGANDO:
            for plataforma in self.plataformas:
                plataforma.desenhar(JANELA)
            for plataforma in self.plataformas_moveis_alavanca:
                JANELA.blit(plataforma.image, plataforma.rect)
            for plataforma in self.plataformas_verticais:
                plataforma.desenhar(JANELA)
            for diamante in self.diamantes:
                diamante.desenhar(JANELA)

            # Desenha as portas sempre (imagem já muda conforme trancada/destrancada)
            self.porta_fogo.desenhar(JANELA)
            self.porta_agua.desenhar(JANELA)

            self.alavancas.draw(JANELA)
            
            # Desenha jogadores antes dos botões para que botões fiquem na frente
            self.jogador1.desenhar(JANELA)
            self.jogador2.desenhar(JANELA)

            self.botao_movel_1.desenhar(JANELA)
            self.botao_movel_2.desenhar(JANELA)
            self.plataforma_movel.desenhar(JANELA)

            for lago in self.lagos:
                lago.desenhar(JANELA)

            # Moldura do timer e cronometro
            JANELA.blit(self.moldura_timer_img, self.moldura_timer_rect)
            self.cronometro.desenhar(JANELA)

            # Lógica original de contagem de diamantes
            total_diamantes = 4 # Defina o total de diamantes do seu nível
            coletados = total_diamantes - len(self.diamantes)
            self.desenhar_texto(f"    Diamantes: {coletados}/{total_diamantes}", 10, 50, self.fonte_geral)

        elif self.estado == VITORIA:
            self.desenhar_texto("Vocês venceram! Pressione R para reiniciar", 100, 200, self.fonte_titulo)

        
        pygame.display.flip()

    def desenhar_texto(self, texto, x, y, fonte):
        rotulo = fonte.render(texto, True, BRANCO)
        JANELA.blit(rotulo, (x, y))

def main():
    carregar_sprites_diamantes()
    jogo = Jogo()
    jogo.executar()

if __name__ == "__main__":
    main()
