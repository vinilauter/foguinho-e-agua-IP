import pygame
from sys import exit

# Inicialização

pygame.init()
JANELA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fireboy and Watergirl: Python Version")
clock = pygame.time.Clock()

# Música de fundo (SE FOR COLOCAR!!)
#pygame.mixer.music.load("musica.mp3") # Música fica no diretório do jogo
#pygame.mixer.music.play(-1)

# Estados do jogo
MENU, JOGANDO, VITORIA = "menu", "jogando", "vitoria"


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
        JANELA.fill('Black')

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)
