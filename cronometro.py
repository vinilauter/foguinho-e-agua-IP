import pygame

class Cronometro:
    def __init__(self, fonte, posicao, cor):
        """
        Inicializa o cronômetro progressivo.
        :param fonte: O objeto pygame.font.Font para renderizar o texto.
        :param posicao: Uma tupla (x, y) para a posição do texto na tela.
        :param cor: A cor do texto.
        """
        self.fonte = fonte
        self.posicao = posicao
        self.cor = cor
        self.tempo_inicial = 0
        self.tempo_decorrido_segundos = 0
        self.reset()

    def reset(self):
        """Reinicia o cronômetro, zerando o tempo."""
        self.tempo_inicial = pygame.time.get_ticks()
        self.tempo_decorrido_segundos = 0

    def update(self):
        """Atualiza o tempo decorrido. Deve ser chamado uma vez por frame."""
        self.tempo_decorrido_segundos = (pygame.time.get_ticks() - self.tempo_inicial) / 1000

    def desenhar(self, tela):
        """Desenha o tempo decorrido no formato MM:SS na tela."""
        # Converte o total de segundos para minutos e segundos
        total_segundos_int = int(self.tempo_decorrido_segundos)
        minutos = total_segundos_int // 60
        segundos = total_segundos_int % 60
        
        # Formata o texto para sempre ter dois dígitos (ex: 01:05)
        texto = f"Tempo: {minutos:02d}:{segundos:02d}"
        
        rotulo = self.fonte.render(texto, True, self.cor)
        tela.blit(rotulo, self.posicao)
