from alavanca import Alavanca
import pygame

class Plataforma_movel_vertical(pygame.sprite.Sprite):
    def __init__(self, posicao_inicial, posicao_final, alavanca_designada, cor, ativada=False):
        super().__init__()
        
        caminho_imagem= f"plataforma_movel_vertica_{cor}.png"

        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        self.rect = self.image.get_rect(midbottom=posicao_inicial)

        self.posicao_inicial = posicao_inicial[1]
        self.posicao_final = posicao_final[1]

        self.alavanca_designada = alavanca_designada
        self.ativada = ativada

        self.velocidade = 1


        def update(self):
            if self.rect.y < self.posicao_alvo:
                self.rect.y += self.velocidade
                if self.rect.y > self.posicao_alvo:
                    self.rect.y = self.posicao_alvo
            elif self.rect.y > self.posicao_alvo:
                self.rect.y -= self.velocidade
                if self.rect.y < self.posicao_alvo:
                    self.rect.y = self.posicao_alvo

# para implementar na main: 
#   if alavancaX.ativada:
#      self.posicao_alvo_y = self.posicao_final_y
#   else:
#      self.posicao_alvo_y = self.posicao_inicial_y     