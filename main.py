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
        carregar_sprites_diamantes()

        self.relogio = pygame.time.Clock()
        self.fonte_geral = pygame.font.Font(None, 36)
        self.fonte_titulo = pygame.font.Font(None, 74)
        self.estado = MENU
        self.cronometro = Cronometro(fonte=self.fonte_geral, posicao=(0,0), cor=BRANCO)

        # Moldura do timer
        self.moldura_timer_img = pygame.image.load("Imagens/moldura_timer.png").convert_alpha()
        self.moldura_timer_img = pygame.transform.scale(self.moldura_timer_img, (150, 65))
        self.moldura_timer_rect = self.moldura_timer_img.get_rect(midtop=((LARGURA // 2), 0))

        # Ajuste do cronômetro
        self.cronometro.fonte = pygame.font.Font(None, 28)
        self.cronometro.centralizado = True
        self.cronometro.posicao = (self.moldura_timer_rect.centerx, self.moldura_timer_rect.top + self.moldura_timer_rect.height // 2)

        # Background e Imagem do menu
        self.background = pygame.image.load("Imagens/background.png").convert()
        self.background = pygame.transform.scale(self.background, (LARGURA, ALTURA))
        self.imagem_menu = pygame.image.load("Imagens/tela_inicial_jogo.png").convert_alpha()
        self.imagem_menu = pygame.transform.scale(self.imagem_menu, (LARGURA, ALTURA))

        # Carregamento do nível
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
        if "alavancas" in nivel:
            for alavanca in nivel["alavancas"]:
                self.alavancas.add(alavanca)
        self.plataformas_verticais = pygame.sprite.Group(nivel.get("plataformas_verticais", []))
        self.plataformas_moveis_alavanca = nivel.get("plataformas_moveis_alavanca", [])
        self.powerups = pygame.sprite.Group()
        if "powerups" in nivel:
            for powerup in nivel["powerups"]:
                self.powerups.add(powerup)
        
        # Inicialização de todos os contadores e bandeiras de rastreamento
        self.botoes_unicos_ativados = 0
        self.alavancas_unicas_ativadas = 0
        self.powerups_usados = 0
        self.botao_1_ja_foi_contado = False
        self.botao_2_ja_foi_contado = False
        
        try:
            self.alavancas_ja_foram_contadas = {alavanca: alavanca.ativada for alavanca in self.alavancas}
        except AttributeError:
            self.alavancas_ja_foram_contadas = {alavanca: False for alavanca in self.alavancas}

        # Contador de diamantes dinâmico
        self.total_diamantes_nivel = len(self.diamantes)

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

        # Colisões e movimento
        plataformas_colidiveis = self.plataformas + [self.plataforma_movel] + list(self.plataformas_moveis_alavanca) + list(self.plataformas_verticais)
        for jogador in [self.jogador1, self.jogador2]:
            jogador.aplicar_gravidade()
            lagos_solidos = [lago for lago in self.lagos if lago.tipo == jogador.tipo]
            jogador.checar_colisao(plataformas_colidiveis + lagos_solidos)
        
        # Lógica de morte nos lagos
        for jogador in [self.jogador1, self.jogador2]:
            for lago in self.lagos:
                if jogador.rect.colliderect(lago.rect) and lago.tipo != jogador.tipo:
                    self.__init__()
                    return

        # Botões e plataforma
        self.botao_movel_1.atualizar([self.jogador1, self.jogador2])
        self.botao_movel_2.atualizar([self.jogador1, self.jogador2])
        ativado = self.botao_movel_1.pressionado or self.botao_movel_2.pressionado
        self.plataforma_movel.atualizar(ativado)

        # Lógica original ("remendo") para mover o jogador com a plataforma
        for jogador in [self.jogador1, self.jogador2]:
            if jogador.rect.colliderect(self.plataforma_movel.rect):
                # Checa se está em cima da plataforma (não do lado ou dentro)
                if abs(jogador.rect.bottom - self.plataforma_movel.rect.top) <= 5:
                    jogador.rect.y += getattr(self.plataforma_movel, 'velocidade_y', 0)
                    # Adicionado para também mover horizontalmente
                    jogador.rect.x += getattr(self.plataforma_movel, 'velocidade_x', 0)

        # Contagem de ativações ÚNICAS para botões
        if self.botao_movel_1.pressionado and not self.botao_1_ja_foi_contado:
            self.botoes_unicos_ativados += 1
            self.botao_1_ja_foi_contado = True

        if self.botao_movel_2.pressionado and not self.botao_2_ja_foi_contado:
            self.botoes_unicos_ativados += 1
            self.botao_2_ja_foi_contado = True

        # Coleta de diamantes
        for jogador in [self.jogador1, self.jogador2]:
            for diamante in self.diamantes[:]:
                if (jogador.tipo == "agua" and isinstance(diamante, DiamanteAzul) and jogador.rect.colliderect(diamante.rect)) or \
                   (jogador.tipo == "fogo" and isinstance(diamante, DiamanteVermelho) and jogador.rect.colliderect(diamante.rect)):
                    self.diamantes.remove(diamante)

        # Contagem de POWER-UPS
        for jogador in [self.jogador1, self.jogador2]:
            for powerup in self.powerups.copy(): 
                if powerup.checkar_colisao(jogador):
                    jogador.ativar_powerup_velocidade(5000)
                    self.powerups_usados += 1
                    powerup.kill()

        # Alavancas e outras plataformas
        self.alavancas.update()
        for jogador in [self.jogador1, self.jogador2]:
            for alavanca in self.alavancas:
                alavanca.check_colisao(jogador)
        
        for plataforma in self.plataformas_moveis_alavanca:
            plataforma.update()
        self.plataformas_verticais.update()
        
        # Contagem de ativações ÚNICAS para alavancas
        for alavanca in self.alavancas:
            if getattr(alavanca, 'ativada', False) and not self.alavancas_ja_foram_contadas[alavanca]:
                self.alavancas_unicas_ativadas += 1
                self.alavancas_ja_foram_contadas[alavanca] = True

        self.cronometro.update()
        
        # Lógica de vitória
        todos_coletados = not self.diamantes
        jogadores = [self.jogador1, self.jogador2]
        jogador_fogo = next((j for j in jogadores if j.tipo == "fogo"), None)
        jogador_agua = next((j for j in jogadores if j.tipo == "agua"), None)
        if todos_coletados:
            if jogador_fogo and jogador_fogo.rect.colliderect(self.porta_fogo.rect):
                self.porta_fogo.destrancar()
            if jogador_agua and jogador_agua.rect.colliderect(self.porta_agua.rect):
                self.porta_agua.destrancar()
            if (jogador_fogo and not self.porta_fogo.trancada and jogador_fogo.rect.colliderect(self.porta_fogo.rect) and
                jogador_agua and not self.porta_agua.trancada and jogador_agua.rect.colliderect(self.porta_agua.rect)):
                self.estado = VITORIA

    def desenhar_menu(self):
        JANELA.blit(self.imagem_menu, (0, 0))
        s = pygame.Surface((LARGURA, 150), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        JANELA.blit(s, (0, ALTURA//3 - 50))
        texto_instrucao = self.fonte_geral.render("Pressione ESPAÇO para começar", True, CINZA)
        rect_instrucao = texto_instrucao.get_rect(center=(LARGURA / 2, ALTURA / 2.75))
        JANELA.blit(texto_instrucao, rect_instrucao)

    def desenhar(self):
        JANELA.blit(self.background, (0, 0))

        if self.estado == MENU:
            self.desenhar_menu()

        elif self.estado == JOGANDO:
            # Desenho dos elementos do jogo
            for plataforma in self.plataformas:
                plataforma.desenhar(JANELA)
            for plataforma in self.plataformas_moveis_alavanca:
                JANELA.blit(plataforma.image, plataforma.rect)
            for plataforma in self.plataformas_verticais:
                plataforma.desenhar(JANELA)
            for diamante in self.diamantes:
                diamante.desenhar(JANELA)
            self.powerups.draw(JANELA)
            self.porta_fogo.desenhar(JANELA)
            self.porta_agua.desenhar(JANELA)
            self.alavancas.draw(JANELA)
            self.jogador1.desenhar(JANELA)
            self.jogador2.desenhar(JANELA)
            self.botao_movel_1.desenhar(JANELA)
            self.botao_movel_2.desenhar(JANELA)
            self.plataforma_movel.desenhar(JANELA)
            for lago in self.lagos:
                lago.desenhar(JANELA)

            # UI e Contadores
            JANELA.blit(self.moldura_timer_img, self.moldura_timer_rect)
            self.cronometro.desenhar(JANELA)

            # Exibição de todos os contadores no canto superior direito
            coletados = self.total_diamantes_nivel - len(self.diamantes)
            self.desenhar_texto_direita(f"Diamantes: {coletados}/{self.total_diamantes_nivel}", 20, self.fonte_geral)
            self.desenhar_texto_direita(f"Botões : {self.botoes_unicos_ativados}", 50, self.fonte_geral)
            self.desenhar_texto_direita(f"Alavancas : {self.alavancas_unicas_ativadas}", 80, self.fonte_geral)
            self.desenhar_texto_direita(f"Power-ups : {self.powerups_usados}", 110, self.fonte_geral)

        elif self.estado == VITORIA:
            self.desenhar_texto("Vocês venceram! Pressione R para reiniciar", 100, 200, self.fonte_titulo)
        
        pygame.display.flip()

    def desenhar_texto(self, texto, x, y, fonte):
        rotulo = fonte.render(texto, True, BRANCO)
        JANELA.blit(rotulo, (x, y))

    # Função auxiliar para desenhar texto alinhado à direita
    def desenhar_texto_direita(self, texto, y, fonte, cor=BRANCO, margem=20):
        """Desenha um texto na janela, alinhado ao canto superior direito."""
        superficie_texto = fonte.render(texto, True, cor)
        rect_texto = superficie_texto.get_rect(topright=(LARGURA - margem, y))
        JANELA.blit(superficie_texto, rect_texto)

def main():
    carregar_sprites_diamantes()
    jogo = Jogo()
    jogo.executar()

if __name__ == "__main__":
    main()