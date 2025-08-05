
class Alavanca(pygame.sprite.Sprite):

    def __init__(self, posicao, cor, ativada=False):
        super().__init__()

        caminho_ligada = f"foguinho-e-agua-IP/Imagens/alavanca_{cor}_ON.png"
        caminho_desligada = f"foguinho-e-agua-IP/Imagens/alavanca_{cor}_OFF.png"

        self.img_ligada = pygame.image.load(caminho_ligada)
        self.img_desligada = pygame.image.load(caminho_desligada)
        self.image = self.img_desligada

        self.rect = self.img_desligada.get_rect(midbottom=posicao)
        
        self.posicao = posicao
        self.ativada = ativada
    
    def update(self):
        if self.ativada:
            self.image = self.img_ligada
        else:
            self.image = self.img_desligada
    
    def toggle(self):
        self.ativada = not self.ativada
        self.update()

