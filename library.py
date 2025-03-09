Cam = [0,0,-5]
rot = [0,0]
objRot = [0,0,0]
obj = []
world = []
vertexData = []
quadData = []
size = bytearray([7,7,7])
DTS = 100
objSize = 4
objDrawSize = 10

LGRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DGRAY = (50, 50, 50)

ScreenW, ScreenH = 1200, 740

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
