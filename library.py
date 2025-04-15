import pygame
import random

Cam = [0,0,-5]
Last = [0,0,-5]
rot = [0,0,0]
rotSpeed = [0,0,0]
obj = []
vertexData = []
triData = []
size = bytearray([1, 1, 1])
objSize = 4
objDrawSize = 10
maxDist = 20

BLACK = (0, 0, 0)
LGRAY = (150, 150, 150)
WHITE = (255, 255, 255)
DGRAY = (50, 50, 50)

color = [
    BLACK,
    WHITE,
    LGRAY,
    DGRAY
]

style = "Main"
if style == "Main":
    ScreenW, ScreenH = 1200, 740
    objFillSize = 10
    distToScreen = 30
elif style == "Thumby":
    ScreenW, ScreenH = 72, 40
    objFillSize = 10
    distToScreen = 30
elif style == "Playdate":
    ScreenW, ScreenH = 400, 240
    objFillSize = 10
    distToScreen = 30

tree = pygame.image.load("images/grayscaleW.png")
dirt = pygame.image.load("images/grayscaleD.png")

check = [
    [0,0,-4],[0,0,4],
    [-4,0,0],[4,0,0],
    [0,4,0],[0,-4,0]
]

tri = [
    [3, 2, 1],  # Front (first triangle)
    [3, 1, 0],  # Front (second triangle)
    
    #[4, 5, 6],  # Back (first triangle)
    #[4, 6, 7],  # Back (second triangle)
    
    #[3, 0, 4],  # Left (first triangle)
    #[3, 4, 7],  # Left (second triangle)
    
    #[1, 2, 6],  # Right (first triangle)
    #[1, 6, 5],  # Right (second triangle)
    
    #[2, 3, 7],  # Top (first triangle)
    #[2, 7, 6],  # Top (second triangle)
    
    #[0, 1, 5],  # Bottom (first triangle)
    #[0, 5, 4]  # Bottom (second triangle)
]

uv_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
uv = [
    [(1, 0), (1, 1), (0, 1)],
    [(0, 0), (1, 0), (0, 1)],

    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 1), (0, 1)],

    [(0, 0), (1, 0), (0, 1)],
    [(0, 0), (0, 1), (1, 1)],

    [(1, 0), (1, 1), (0, 1)],
    [(0, 0), (1, 0), (0, 1)],

    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 1), (0, 1)],

    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 1), (0, 1)]
]


pygame.font.init()
txtFont = pygame.font.SysFont('Arial', 20)

def text_to_screen(text, color, x, y, screen):
    img = txtFont.render(text, True, color)
    screen.blit(img, (x,y))