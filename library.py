import pygame

Cam = [0,0,-5]
Last = [0,0,-5]
rot = [0,0]
objRot = [0,0,0]
obj = []
vertexData = []
quadData = []
size = bytearray([7,10,7])
distToScreen = 100
objSize = 4
objDrawSize = 10
objFillSize = None
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

style = "Thumby"
if style == "Main":
    ScreenW, ScreenH = 1200, 740
elif style == "Thumby":
    ScreenW, ScreenH = 72, 40
elif style == "Playdate":
    ScreenW, ScreenH = 400, 240

check = [
    [0,0,-4],[0,0,4],
    [-4,0,0],[4,0,0],
    [0,4,0],[0,-4,0]
]

quad = [
    [3, 2, 1, 0],  # Front
    [4, 5, 6, 7],  # Back
    [3, 0, 4, 7],  # Left
    [1, 2, 6, 5],  # Right
    [2, 3, 7, 6],  # Top
    [0, 1, 5, 4],  # Bottom
]

pygame.font.init()
txtFont = pygame.font.SysFont('Arial', 20)

def text_to_screen(text, color, x, y, screen):
    img = txtFont.render(text, True, color)
    screen.blit(img, (x,y))