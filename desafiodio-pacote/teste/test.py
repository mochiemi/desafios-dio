from auladio_criandopacotes.functions import equalize, grayscale
from auladio_criandopacotes.tools import io, plot

imagem1 = io.read_image('samples\\imagem_1.jpg')
imagem2 = io.read_image('samples\\imagem_2.jpg')
imagem3 = io.read_image('samples\\imagem_3.jpg')
equalizado1 = equalize.equalizing(imagem1)
tonsdecinza1 = grayscale.grayscaling(imagem1)
equalizado2 = equalize.equalizing(imagem2)
tonsdecinza2 = grayscale.grayscaling(imagem2)
equalizado3 = equalize.equalizing(imagem3)
tonsdecinza3 = grayscale.grayscaling(imagem3)
plot.plot_result(imagem1, imagem2, imagem3, nome='normal')
plot.plot_result(equalizado1, equalizado2, equalizado3, nome='equalizado')
plot.plot_result(tonsdecinza1, tonsdecinza2, tonsdecinza3, nome='tons de cinza')


