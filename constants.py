import math

# Tamanho real do canvas (resolução da tela)
REAL_WIDTH = 1024
REAL_HEIGHT = 512

# Tamanho de cada pixel (PxP)
PIXEL_SIZE = 8

# Quantidade de pixels no canvas
WIDTH = math.floor(REAL_WIDTH / PIXEL_SIZE)
HEIGHT = math.floor(REAL_HEIGHT / PIXEL_SIZE)
