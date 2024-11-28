import src.fines.graphs.colors as colors

background_color = []
hover_background_color = []

for i in range(0, 10): 
    color = colors.retornar_rgb_aleatorio()
    while (not colors.verificar_cor_diferente_das_existentes(background_color, color)): # irá gerar outra cor caso não for diferente das demais já existentes
        color = colors.retornar_rgb_aleatorio()

    background_color.append(color) 
    hover_background_color.append(colors.clarear_cor(color)) # adiciona a cor clereada nesta lista

print(background_color)
print(hover_background_color)