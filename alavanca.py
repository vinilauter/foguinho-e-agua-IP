import pygame

class Alavanca(pygame.sprite.Sprite):

    def __init__(self, posicao, cor, ativada=False):
        super().__init__()

        caminho_ligada = f"Imagens/alavanca_{cor}_ON.png"
        caminho_desligada = f"Imagens/alavanca_{cor}_OFF.png"

        self.img_ligada = pygame.image.load(caminho_ligada).convert_alpha()
        self.img_desligada = pygame.image.load(caminho_desligada).convert_alpha()

        self.img_ligada = pygame.transform.scale(self.img_ligada, (self.img_ligada.get_width() // 2, self.img_ligada.get_height() // 2))
        self.img_desligada = pygame.transform.scale(self.img_desligada, (self.img_desligada.get_width() // 2, self.img_desligada.get_height() // 2))

        self.image = self.img_desligada
        self.rect = self.img_desligada.get_rect(midbottom=posicao)
        
        self.posicao = posicao
        self.ativada = ativada

        self.ultimo_acionamento = 0

    def update(self):
        if self.ativada:
            self.image = self.img_ligada
        else:
            self.image = self.img_desligada
    
    def toggle(self):
        self.ativada = not self.ativada
        self.update()
    
    def check_colisao(self, jogador):
        if jogador.rect.colliderect(self.rect):
            tempo_atual = pygame.time.get_ticks()
            
            # Verifica se passou mais de 1 segundo (1000 ms)
            if tempo_atual - self.ultimo_acionamento > 1000:
                self.toggle()
                self.ultimo_acionamento = tempo_atual
                return True
        return False
