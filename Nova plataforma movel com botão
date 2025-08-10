# Eu acho que fazer assim fica melhor, sem a colisão com o bloco la pq tava dando muito problema aí vcs decidem como preferem
# Quando for fazer o main faz o draw do botão por último depois do personagem que eu acho que fica
# mais bonito, mas se não quiser fazer nessa ordem tudo bem também.
# (o botão fica na frente do personagem, mas eu fiz um for com as imagens para ele descer e é bem rápido)

import pygame
import os

class Botao :
    """Em vez do botão ser um bloco com colisão é melhor uma zona de ativação"""
    # Colisão tava dando jitter ai preferi fazer uma zona de ativação
    # Ai fiz um for com as imagens para simular o botão abaixando

    def __init__(self, x, y, num_frames=5) :
        self.pressionado = False
        self.frames = []
        
        # O botão ficou muito grande ai dividi pela metade (metade de 111x47)
        tamanho_final = (111 // 2, 47 // 2) # Resultado : (55, 23)

        # ANIMAÇÃO DO BOTÃO para contornar o jitter
        for i in range(5) :
            caminho_frame = os.path.join(f'Imagens/botao_frame_{i}.png')
            frame = pygame.image.load(caminho_frame).convert_alpha()
            frame_redimensionado = pygame.transform.scale(frame, tamanho_final)
            self.frames.append(frame_redimensionado)

        self.frame_atual = 0
        self.velocidade_animacao = 100 # ms
        self.ultimo_update = pygame.time.get_ticks()
        
        # O rect é usado para desenhar e checar ativação, não para colisão física
        self.rect = self.frames[0].get_rect(center=(x, y)) if self.frames else pygame.Rect(x,y,0,0)

    def atualizar(self, jogadores):
        self.pressionado = False
        for jogador in jogadores:
            if self.rect.colliderect(jogador.rect):
                self.pressionado = True
                break

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.velocidade_animacao:
            if self.pressionado:
                if self.frame_atual < len(self.frames) - 1:
                    self.frame_atual += 1
            else:
                if self.frame_atual > 0:
                    self.frame_atual -= 1
            self.ultimo_update = agora

    def desenhar(self, tela) :
        if self.frames :
            tela.blit(self.frames[self.frame_atual], self.rect)

class Plataforma_Movel :
    def __init__(self, x, y, largura, altura, y_final, velocidade) :
        self.y_inicial = y
        self.y_final = y_final
        self.velocidade_vertical = velocidade
        self.movendo = False 

        caminho_ativada = os.path.join('Imagens/plataforma_movel_horizontal_ativada.png')
        caminho_desativada = os.path.join('Imagens/plataforma_movel_horizontal_desativada.png')
        self.imagem_ativada = pygame.image.load(caminho_ativada).convert_alpha()
        self.imagem_desativada = pygame.image.load(caminho_desativada).convert_alpha()
        self.imagem_ativada = pygame.transform.scale(self.imagem_ativada, (largura, altura))
        self.imagem_desativada = pygame.transform.scale(self.imagem_desativada, (largura, altura))
        self.imagem_atual = self.imagem_desativada

        self.rect = self.imagem_atual.get_rect(topleft=(x, y))

    def atualizar(self, ativado) :
        self.movendo = False
        if ativado :
            if self.rect.y < self.y_final :
                movimento = min(self.velocidade_vertical, self.y_final - self.rect.y)
                self.rect.y += movimento
                self.movendo = True
        else :
            if self.rect.y > self.y_inicial :
                movimento = min(self.velocidade_vertical, self.rect.y - self.y_inicial)
                self.rect.y -= movimento
                self.movendo = True

        if self.movendo or self.rect.y == self.y_final :
            self.imagem_atual = self.imagem_ativada
        else :
            self.imagem_atual = self.imagem_desativada 

    def desenhar(self, tela) :
        tela.blit(self.imagem_atual, self.rect)
