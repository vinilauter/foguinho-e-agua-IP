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

    # Calcula a largura de cada metade da hitbox
        metade_largura = self.rect.width / 2

    # Cria o retângulo para a metade esquerda (agora para DESATIVAR)
        self.rect_desativar = pygame.Rect(self.rect.left, self.rect.top, metade_largura, self.rect.height)

    # Cria o retângulo para a metade direita (agora para ATIVAR)
        self.rect_ativar = pygame.Rect(self.rect.centerx, self.rect.top, metade_largura, self.rect.height)           

    def update(self):
        if self.ativada:
            self.image = self.img_ligada
        else:
            self.image = self.img_desligada
    
    def toggle(self):
        self.ativada = not self.ativada
        self.update()

    def check_colisao(self, jogador):
        tempo_atual = pygame.time.get_ticks()

        # A alavanca só pode ser alterada se o cooldown tiver passado
        if tempo_atual - self.ultimo_acionamento > 1000: # 1 segundo de cooldown

            # Lógica para ATIVAR a alavanca (se estiver desativada e o jogador tocar no lado esquerdo)
            if not self.ativada and jogador.rect.colliderect(self.rect_ativar):
                self.toggle() # Liga a alavanca
                self.ultimo_acionamento = tempo_atual # Reinicia o cooldown
                return True

            # Lógica para DESATIVAR a alavanca (se estiver ativada e o jogador tocar no lado direito)
            elif self.ativada and jogador.rect.colliderect(self.rect_desativar):
                self.toggle() # Desliga a alavanca
                self.ultimo_acionamento = tempo_atual # Reinicia o cooldown
                return True

        # Se nenhuma das condições for atendida (ou o cooldown não passou), ent não faz nada
        return False
