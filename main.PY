import pygame
import sys

# Importa todas as classes e constantes necessárias do módulo level
from mechanics.level import Plataforma, Lago, Objetivo, Nivel1, AGUA_COR, FOGO_COR, PlataformaAngulada

# Inicialização do Pygame
pygame.init()

# Dimensões da janela do jogo
LARGURA, ALTURA = 1200, 800
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fogo & Água - Nível 1") # Título da janela
FPS = 60 # Taxa de quadros por segundo
GRAVIDADE = 0.5 # Força da gravidade

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (200, 50, 50)
AZUL = (50, 100, 255)
PRETO = (0, 0, 0)

# Estados do jogo
MENU, JOGANDO, VITORIA = "menu", "jogando", "vitoria"

class Jogador:
    """Representa um jogador no jogo (Fogo ou Água)."""
    def __init__(self, x, y, cor, controles):
        self.retangulo = pygame.Rect(x, y, 30, 45) # Retângulo de colisão do jogador
        self.cor = cor # Cor do jogador (VERMELHO para Fogo, AZUL para Água)
        self.controles = controles # Dicionário com as teclas de controle
        self.vel_y = 0 # Velocidade vertical (para gravidade e pulo)
        self.no_chao = False # Indica se o jogador está no chão
        # Máscara de colisão para detecção de colisão precisa com plataformas anguladas
        # Cria uma superfície temporária e a preenche com uma cor sólida para garantir que a máscara seja um retângulo sólido.
        temp_surface = pygame.Surface(self.retangulo.size, pygame.SRCALPHA) # SRCALPHA para transparência
        temp_surface.fill((255, 255, 255, 255)) # Preenche a superfície com cor sólida (totalmente opaca)
        self.mask = pygame.mask.from_surface(temp_surface) # Cria a máscara a partir da superfície

    def controlar(self, teclas):
        """Processa a entrada do teclado para mover o jogador."""
        # Acessa diretamente o estado da tecla usando []
        if teclas[self.controles["esquerda"]]:
            self.retangulo.x -= 5
        if teclas[self.controles["direita"]]:
            self.retangulo.x += 5

        # Limita o jogador dentro dos limites da janela
        if self.retangulo.left < 0:
            self.retangulo.left = 0
        if self.retangulo.right > LARGURA:
            self.retangulo.right = LARGURA

        # Pulo
        if teclas[self.controles["pular"]] and self.no_chao:
            self.vel_y = -15
            self.no_chao = False

    def aplicar_gravidade(self):
        """Aplica a gravidade ao jogador."""
        self.retangulo.y += self.vel_y
        self.vel_y += GRAVIDADE

    def checar_colisao(self, nivel):
        """
        Verifica a colisão do jogador com plataformas retangulares e anguladas.
        Ajusta a posição do jogador após a colisão.
        """
        # Assume que o jogador não está no chão até colidir com algo sólido
        on_ground_this_frame = False 

        # Colisão com plataformas retangulares
        for plataforma in nivel.plataformas:
            if self.retangulo.colliderect(plataforma.retangulo):
                # Colisão pelo topo (jogador caindo em cima da plataforma)
                if self.vel_y > 0 and self.retangulo.bottom <= plataforma.retangulo.top + 15:
                    self.retangulo.bottom = plataforma.retangulo.top
                    self.vel_y = 0
                    on_ground_this_frame = True # Jogador está no chão
                # Colisão pela parte de baixo (jogador pulando e batendo na parte de baixo)
                elif self.vel_y < 0 and self.retangulo.top >= plataforma.retangulo.bottom - 15:
                    self.retangulo.top = plataforma.retangulo.bottom
                    self.vel_y = 0
                # Colisão pelas laterais (jogador andando contra a parede)
                elif self.retangulo.right > plataforma.retangulo.left and self.retangulo.left < plataforma.retangulo.right:
                     if self.retangulo.right >= plataforma.retangulo.left and self.retangulo.centerx < plataforma.retangulo.centerx:
                         self.retangulo.right = plataforma.retangulo.left
                     if self.retangulo.left <= plataforma.retangulo.right and self.retangulo.centerx > plataforma.retangulo.centerx:
                         self.retangulo.left = plataforma.retangulo.right
        
        # Colisão com plataformas anguladas (usando máscaras para precisão)
        for plataforma_angulada in nivel.plataformas_anguladas:
            # Calcula o offset da máscara da plataforma em relação à máscara do jogador
            offset_x = plataforma_angulada.rect.x - self.retangulo.x
            offset_y = plataforma_angulada.rect.y - self.retangulo.y
            
            # Verifica se as máscaras se sobrepõem
            if self.mask.overlap(plataforma_angulada.mask, (offset_x, offset_y)):
                # Lógica de colisão para plataformas anguladas (rampas)

                # Determina o ponto X relativo ao qual verificar na rampa (geralmente o centro da base do jogador)
                player_check_x_rel = self.retangulo.centerx - plataforma_angulada.rect.x

                # Garante que o ponto de verificação esteja dentro dos limites horizontais da imagem da rampa
                player_check_x_rel = max(0, min(player_check_x_rel, plataforma_angulada.rect.width - 1))

                # Encontra a altura da rampa no X do jogador
                # Itera de cima para baixo na máscara da rampa para encontrar o primeiro pixel sólido (topo da superfície)
                ramp_surface_y_rel_to_ramp_top = -1
                for y_scan in range(plataforma_angulada.rect.height):
                    if plataforma_angulada.mask.get_at((player_check_x_rel, y_scan)):
                        ramp_surface_y_rel_to_ramp_top = y_scan
                        break
                
                if ramp_surface_y_rel_to_ramp_top != -1:
                    # Calcula a posição Y absoluta onde o jogador deveria estar na rampa
                    target_y_on_ramp = plataforma_angulada.rect.y + ramp_surface_y_rel_to_ramp_top
                    # ------------------> IMPORTANTE <------------------
                    # Se o jogador está caindo ou já está na rampa, e seus pés estão abaixo/na superfície da rampa
                    # Adicionamos uma pequena margem (e.g., -2) para garantir que o jogador "grude" na rampa e não caia através
                    if self.vel_y >= 0 and self.retangulo.bottom >= target_y_on_ramp - 2:
                        self.retangulo.bottom = target_y_on_ramp
                        self.vel_y = 0
                        on_ground_this_frame = True # Jogador está no chão por causa da rampa
                    # Se o jogador está pulando e colide com a parte de baixo da rampa
                    elif self.vel_y < 0 and self.retangulo.centery < plataforma_angulada.rect.centery:
                        self.vel_y = 0 

        self.no_chao = on_ground_this_frame # Atualiza o estado no_chao do jogador após todas as verificações

    def desenhar(self, tela):
        """Desenha o jogador na tela."""
        pygame.draw.rect(tela, self.cor, self.retangulo)

class Jogo:
    """Classe principal do jogo, gerencia o estado e o loop do jogo."""
    def __init__(self):
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36) # Fonte para o texto do tempo/mensagens
        self.estado = MENU # Estado inicial do jogo
        self.tempo_limite = 120 # Tempo máximo para completar o nível (em segundos)
        self.tempo_inicial = pygame.time.get_ticks() # Tempo inicial do jogo

        # --- CAMINHO DO SEU ARQUIVO TMX ---
        # Certifique-se de que este caminho está correto para o seu arquivo .tmx!
        # Agora o mapa está em 'assets/maps/'
        MAPA_DO_NIVEL = "assets/maps/map-demo-sem-lago-com-camada.tmx" 

        self.nivel_atual = Nivel1(LARGURA, ALTURA, MAPA_DO_NIVEL) 

        # Criação dos jogadores
        self.jogador1 = Jogador(200, 700, VERMELHO, {
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "pular": pygame.K_w
        })
        self.jogador2 = Jogador(1000, 700, AZUL, {
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "pular": pygame.K_UP
        })

    def executar(self):
        """Inicia e mantém o loop principal do jogo."""
        while True:
            self.relogio.tick(FPS) # Controla a taxa de quadros
            self.tratar_eventos() # Lida com eventos do usuário
            self.atualizar() # Atualiza o estado do jogo
            self.desenhar() # Desenha os elementos na tela

    def tratar_eventos(self):
        """Processa eventos do Pygame (fechar janela, pressionar teclas)."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
            elif evento.type == pygame.KEYDOWN:

                if self.estado == MENU and evento.key == pygame.K_SPACE:
                    self.estado = JOGANDO
                    self.tempo_inicial = pygame.time.get_ticks() 
                # Reinicia o jogo a partir da vitória ou durante o jogo
                elif self.estado in (VITORIA, JOGANDO) and evento.key == pygame.K_r:
                    self.__init__() # reinicia o jogo (chama o construtor novamente)

    def atualizar(self):
        """Atualiza o estado de todos os objetos do jogo."""
        teclas = pygame.key.get_pressed() # pega o estado de todas as teclas pressionadas

        if self.estado == JOGANDO:
            # Controla e atualiza os jogadores
            self.jogador1.controlar(teclas)
            self.jogador2.controlar(teclas)

            for jogador in [self.jogador1, self.jogador2]:
                jogador.aplicar_gravidade()
                # Passa o objeto nivel_atual para que o jogador possa checar colisão com todos os tipos de plataforma (retangular e angulada)
                jogador.checar_colisao(self.nivel_atual)
                
                # Checa colisão com perigos (lagos de água/fogo)
                for perigo in self.nivel_atual.perigos:
                    if jogador.retangulo.colliderect(perigo.retangulo):
                        if (jogador.cor == VERMELHO and perigo.cor == AGUA_COR) or \
                           (jogador.cor == AZUL and perigo.cor == FOGO_COR):
                            self.__init__() # Reinicia o jogo

            # Checa condição de vitória: ambos os jogadores atingiram seus objetivos
            if (self.jogador1.retangulo.colliderect(self.nivel_atual.objetivos[0].retangulo) and
                self.jogador2.retangulo.colliderect(self.nivel_atual.objetivos[1].retangulo)):
                self.estado = VITORIA

            # Atualiza e checa o tempo restante
            tempo_passado = (pygame.time.get_ticks() - self.tempo_inicial) / 1000
            self.tempo_restante = max(0, self.tempo_limite - int(tempo_passado))

            # Se o tempo acabar, reinicia o jogo
            if self.tempo_restante == 0:
                self.__init__()

    def desenhar(self):
        """Desenha todos os elementos do jogo na tela."""
        JANELA.fill(PRETO) # Preenche a tela de preto a cada frame

        if self.estado == MENU:
            self.desenhar_texto("Pressione ESPAÇO para começar", LARGURA // 2 - 200, ALTURA // 2 - 25)
        elif self.estado == JOGANDO:
            self.nivel_atual.desenhar(JANELA) # Desenha o nível (plataformas, perigos, objetivos)
            self.jogador1.desenhar(JANELA) # Desenha o jogador 1
            self.jogador2.desenhar(JANELA) # Desenha o jogador 2
            self.desenhar_texto(f"Tempo: {self.tempo_restante}", 10, 10) # Desenha o tempo restante
        elif self.estado == VITORIA:
            self.desenhar_texto("Vocês venceram! Pressione R para reiniciar", LARGURA // 2 - 220, ALTURA // 2 - 25)

        pygame.display.flip() # Atualiza a tela

    def desenhar_texto(self, texto, x, y):
        """Função auxiliar para desenhar texto na tela."""
        rotulo = self.fonte.render(texto, True, BRANCO)
        JANELA.blit(rotulo, (x, y))

if __name__ == "__main__":
    Jogo().executar()
