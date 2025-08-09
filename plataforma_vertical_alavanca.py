import pygame
from alavanca import Alavanca

class Plataforma_movel_vertical(pygame.sprite.Sprite):
    def __init__(self, posicao_inicial, posicao_final, alavanca_designada, cor, ativada=False):
        super().__init__()
        caminho_imagem = f"Imagens/plataforma_movel_vertical_{cor}.png"
        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        self.rect = self.image.get_rect(midbottom=posicao_inicial)

        self.posicao_inicial = posicao_inicial[1]
        self.posicao_final = posicao_final[1]
        self.alavanca_designada = alavanca_designada
        self.ativada = ativada
        self.velocidade = 1
        self.posicao_alvo = self.posicao_inicial  # posição alvo inicial

    def update(self):
        # Atualiza posição alvo de acordo com o estado da alavanca designada
        if self.alavanca_designada.ativada:
            self.posicao_alvo = self.posicao_final
        else:
            self.posicao_alvo = self.posicao_inicial

        # Move a plataforma verticalmente até a posição alvo com velocidade constante
        if self.rect.y < self.posicao_alvo:
            self.rect.y += self.velocidade
            if self.rect.y > self.posicao_alvo:
                self.rect.y = self.posicao_alvo
        elif self.rect.y > self.posicao_alvo:
            self.rect.y -= self.velocidade
            if self.rect.y < self.posicao_alvo:
                self.rect.y = self.posicao_alvo
