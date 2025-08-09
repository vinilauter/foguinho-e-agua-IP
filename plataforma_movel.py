import pygame

VERMELHO = (200, 50, 50)
CINZA_ESCURO = (80, 80, 80)

class Botao_Plataforma_Movel:
    def __init__(self, x, y):
        self.pressionado = False

        self.imagem_levantado = pygame.image.load('Imagens/botao_roxo.png').convert_alpha()
        self.imagem_abaixado = pygame.image.load('Imagens/botao_roxo.png').convert_alpha()  # Podem deixar só essa imagem pq eu fiz com que qnd o botão fosse acionado ela mudasse e parecesse pressionada

        self.rect = self.imagem_levantado.get_rect(center=(x, y + 30))

        # Hitbox fixa em 32x32, centralizada na imagem original
        self.hitbox = pygame.Rect(0, 0, 32, 32)
        self.hitbox.center = self.rect.center

        self.y_original = self.rect.y

    def verificar_ativacao(self, jogadores):
        self.pressionado = False
        for jogador in jogadores:
            # Verifica se a parte inferior central do jogador está sobre a hitbox do botão
            if self.hitbox.collidepoint(jogador.rect.centerx, jogador.rect.bottom):
                self.pressionado = True
                break

    def desenhar(self, tela):
        if self.pressionado:
            self.rect.y = self.y_original + 4
            # Criar uma cópia da imagem e aplicar um filtro para escurecer (exemplo simples)
            imagem = self.imagem_levantado.copy()
            imagem.fill((50, 50, 50, 100), special_flags=pygame.BLEND_RGBA_SUB)
        else:
            self.rect.y = self.y_original
            imagem = self.imagem_levantado

        self.hitbox.center = self.rect.center
        tela.blit(imagem, self.rect)

class PlataformaMovel:
    """ Plataforma que se move entre duas posições dependendo do estado do botão """

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
