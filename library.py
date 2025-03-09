Cam = [0,0,-5]
Last = [0,0,-5]
rot = [0,0]
objRot = [0,0,0]
obj = []
vertexData = []
quadData = []
size = bytearray([1,1,1])
DTS = 100
objSize = 4
objDrawSize = 10
objFillSize = 10
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