import pygame
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 600
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fogo & Água - Nível 1")
FPS = 60
GRAVIDADE = 0.5


# Música de fundo (SE FOR COLOCAR!!)
#pygame.mixer.music.load("musica.mp3") # Música fica no diretório do jogo
#pygame.mixer.music.play(-1)

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (200, 50, 50)
AZUL = (50, 100, 255)
CINZA = (128, 128, 128)
PRETO = (0, 0, 0)

# Estados do jogo
MENU, JOGANDO, VITORIA = "menu", "jogando", "vitoria"

class Jogador:
    def __init__(self, x, y, cor, controles):
        self.retangulo = pygame.Rect(x, y, 40, 60)
        self.cor = cor
        self.controles = controles
        self.vel_y = 0
        self.no_chao = False

    def controlar(self, teclas):
        if teclas[self.controles["esquerda"]]:
            self.retangulo.x -= 5
        if teclas[self.controles["direita"]]:
            self.retangulo.x += 5

        # Limites horizontais
        if self.retangulo.left < 0:
            self.retangulo.left = 0
        if self.retangulo.right > LARGURA:
            self.retangulo.right = LARGURA

        # Pular
        if teclas[self.controles["pular"]] and self.no_chao:
            self.vel_y = -15
            self.no_chao = False
            # som_pulo.play()  (COLOCA SE HOUVER SOM DE PULO)


    def aplicar_gravidade(self):
        self.retangulo.y += self.vel_y
        self.vel_y += GRAVIDADE

    def checar_colisao(self, plataformas):
        self.no_chao = False
        for plataforma in plataformas:
            if self.retangulo.colliderect(plataforma.retangulo):
                if self.vel_y > 0:
                    self.retangulo.bottom = plataforma.retangulo.top
                    self.vel_y = 0
                    self.no_chao = True

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.retangulo)

class Plataforma:
    def __init__(self, x, y, largura, altura):
        self.retangulo = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, CINZA, self.retangulo)

class Lago:
    def __init__(self, x, y, largura, altura):
        self.retangulo = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, (173, 216, 230), self.retangulo)


class Objetivo:
    def __init__(self, x, y, cor):
        self.retangulo = pygame.Rect(x, y, 40, 60)
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.retangulo, 3)

class Jogo:
    def __init__(self):
        self.lago = Lago(300, 520, 200, 40)

        self.tempo_limite = 60
        self.tempo_inicial = pygame.time.get_ticks()

        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36)
        self.estado = MENU

        self.jogador1 = Jogador(100, 500, VERMELHO, {
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "pular": pygame.K_w
        })

        self.jogador2 = Jogador(200, 500, AZUL, {
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "pular": pygame.K_UP
        })

        self.plataformas = [
            Plataforma(0, ALTURA - 40, LARGURA, 40),
            Plataforma(150, 450, 500, 20),
            Plataforma(100, 300, 200, 20),
            Plataforma(500, 200, 200, 20)
        ]

        self.objetivo1 = Objetivo(100, 240, VERMELHO)
        self.objetivo2 = Objetivo(600, 140, AZUL)

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
                elif self.estado == VITORIA and evento.key == pygame.K_r:
                    self.__init__()  # reinicia o jogo

    def atualizar(self):
        teclas = pygame.key.get_pressed()

        if self.estado == JOGANDO:
            self.jogador1.controlar(teclas)
            self.jogador2.controlar(teclas)

            for jogador in [self.jogador1, self.jogador2]:
                jogador.aplicar_gravidade()
                jogador.checar_colisao(self.plataformas)

            if (self.jogador1.retangulo.colliderect(self.objetivo1.retangulo) and
                self.jogador2.retangulo.colliderect(self.objetivo2.retangulo)):
                self.estado = VITORIA

        tempo_passado = (pygame.time.get_ticks() - self.tempo_inicial) / 1000
        self.tempo_restante = max(0, self.tempo_limite - int(tempo_passado))

        if self.tempo_restante == 0 and self.estado == JOGANDO:
            self.__init__()

        for jogador in [self.jogador1, self.jogador2]:
            if jogador.retangulo.colliderect(self.lago.retangulo):
                self.__init__()  # volta para o menu


    def desenhar(self):
        JANELA.fill(PRETO)

        if self.estado == MENU:
            self.desenhar_texto("Pressione ESPAÇO para começar", 200, 250)
        elif self.estado == JOGANDO:
            for plataforma in self.plataformas:
                plataforma.desenhar(JANELA)
            self.objetivo1.desenhar(JANELA)
            self.objetivo2.desenhar(JANELA)
            self.jogador1.desenhar(JANELA)
            self.jogador2.desenhar(JANELA)
        elif self.estado == VITORIA:
            self.desenhar_texto("Vocês venceram! Pressione R para reiniciar", 180, 250)
        if self.estado == JOGANDO:
            self.lago.desenhar(JANELA)
            self.desenhar_texto(f"Tempo: {self.tempo_restante}", 10, 10)


        pygame.display.flip()

    def desenhar_texto(self, texto, x, y):
        rotulo = self.fonte.render(texto, True, BRANCO)
        JANELA.blit(rotulo, (x, y))

if __name__ == "__main__":
    Jogo().executar()
# main.py
# Importa a sua classe Nivel
from mechanics.level import Nivel

def main():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fireboy and Watergirl")

    # AQUI ESTÁ A CONEXÃO!
    # 1. Instancie (crie) o seu objeto Nivel
    nivel_atual = Nivel()
    
    # ... (Seu código para criar os jogadores Fireboy e Watergirl, que ainda
    #     estão no main.py, mas que futuramente serão movidos) ...

    running = True
    while running:
        # Processamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Lógica de atualização aqui (futuramente)
        
        # --------------------
        # Desenho
        # --------------------
        screen.fill((0, 0, 0))

        # 2. Chame o método 'draw' do seu objeto Nivel
        nivel_atual.draw(screen)
        
        # ... (código para desenhar os jogadores) ...
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()