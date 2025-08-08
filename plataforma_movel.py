import pygame

VERMELHO = (200, 50, 50)
CINZA_ESCURO = (80, 80, 80)

class Botao_Plataforma_Movel :
    def __init__(self, x, y) :
        self.pressionado = False

        self.imagem_levantado = pygame.image.load('Imagens/botao_solto.png').convert_alpha()
        self.imagem_abaixado = pygame.image.load('Imagens/botao_pressionado.png').convert_alpha()
        # Não consegui achar as sprites dos botões do jogo então editei umas mas acho que ficou meio estranho

        self.retangulo = self.imagem_levantado.get_rect(center=(x, y + 30))

        # Hitbox fixa em 32x32, centralizada na imagem original
        # Precisa ajustar para quando o botão é pressionado porque a imagem ta muito estranha -> personagem flutuando
        self.hitbox = pygame.Rect(0, 0, 32, 32)
        self.hitbox.center = self.retangulo.center

        self.y_original = self.retangulo.y

    def verificar_ativacao(self, jogadores) :
        self.pressionado = False
        for jogador in jogadores :
            if self.hitbox.collidepoint(jogador.retangulo.centerx, jogador.retangulo.bottom) :
                self.pressionado = True
                break

    def desenhar(self, tela) :
        if self.pressionado :
            self.retangulo.y = self.y_original + 4
        else:
            self.retangulo.y = self.y_original

        imagem = self.imagem_abaixado if self.pressionado else self.imagem_levantado
        tela.blit(imagem, self.retangulo)

class PlataformaMovel :
    """ Plataforma se move de acordo com o estado do botão """

    def __init__(self, x, y, largura, altura, end, vel):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.pos_inicial = x
        self.pos_final = end
        self.vel = vel
        self.direcao = 1

    def atualizar(self, ativado):
        if ativado:
            self.rect.x += self.vel * self.direcao
            if self.rect.x <= min(self.pos_inicial, self.pos_final) or self.rect.x >= max(self.pos_inicial, self.pos_final):
                self.direcao *= -1

    def desenhar(self, tela):
        pygame.draw.rect(tela, (150, 0, 255), self.rect)