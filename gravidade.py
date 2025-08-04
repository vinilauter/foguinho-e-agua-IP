gravidade=0.8

def aplicar_gravidade():

    objeto.velocidade_y+=gravidade
    objeto.rect.y+=objeto.velocidade_y

    if objeto.rect.bottom>=altura_do_chao:
        objeto.rect.bottom=altura_do_chao
        objeto.velocidade_y=0