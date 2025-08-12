import pygame

class Plataforma_movel_vertical(pygame.sprite.Sprite):
    def __init__(self, posicao_inicial, posicao_final, alavanca_designada, cor):
        super().__init__()
        caminho_imagem = f"Imagens/plataforma_movel_vertical_{cor}.png"
        self.image = pygame.image.load(caminho_imagem).convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.image.get_width() *3// 5, self.image.get_height() *3// 5))

        self.rect = self.image.get_rect()
        
        # Guarda posições Y como números (e X também pra manter fixo)
        self.posicao_inicial = posicao_inicial[1]
        self.posicao_final = posicao_final[1]
        self.rect.x = posicao_inicial[0]
        self.rect.y = self.posicao_inicial  # começa na posição inicial

        self.alavanca_designada = alavanca_designada
        self.velocidade = 1

    def update(self):
        if self.alavanca_designada.ativada:
            # Move para a posição final (para cima ou para baixo)
            if self.rect.y < self.posicao_final:
                self.rect.y += self.velocidade
                if self.rect.y > self.posicao_final:
                    self.rect.y = self.posicao_final
            elif self.rect.y > self.posicao_final:
                self.rect.y -= self.velocidade
                if self.rect.y < self.posicao_final:
                    self.rect.y = self.posicao_final
        else:
            # Move para a posição inicial (para cima ou para baixo)
            if self.rect.y < self.posicao_inicial:
                self.rect.y += self.velocidade
                if self.rect.y > self.posicao_inicial:
                    self.rect.y = self.posicao_inicial
            elif self.rect.y > self.posicao_inicial:
                self.rect.y -= self.velocidade
                if self.rect.y < self.posicao_inicial:
                    self.rect.y = self.posicao_inicial
    
    def desenhar(self, tela):
        tela.blit(self.image, self.rect)
