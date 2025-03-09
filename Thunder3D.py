import pygame
import pygame.freetype
import keyboard
import math
import _3D
import library as lib
import random

pygame.init()

i = 0
screen = pygame.display.set_mode((lib.ScreenW, lib.ScreenH))
pygame.display.set_caption("Thunder3D")
pygame.font.init()
text_font = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()

def text_to_screen(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def movement():
    move_delta = 0.5
    rot_delta = 0.1
    
    yaw = lib.rot[1]
    
    if keyboard.is_pressed('w'):
        lib.Cam[0] += move_delta * math.sin(yaw)
        lib.Cam[2] += move_delta * math.cos(yaw)

    if keyboard.is_pressed('s'):
        lib.Cam[0] -= move_delta * math.sin(yaw)
        lib.Cam[2] -= move_delta * math.cos(yaw)

    if keyboard.is_pressed('a'):
        lib.Cam[0] -= move_delta * math.cos(yaw)
        lib.Cam[2] += move_delta * math.sin(yaw)

    if keyboard.is_pressed('d'):
        lib.Cam[0] += move_delta * math.cos(yaw)
        lib.Cam[2] -= move_delta * math.sin(yaw)

    if keyboard.is_pressed('down'):
        lib.rot[0] -= rot_delta
    if keyboard.is_pressed('up'):
        lib.rot[0] += rot_delta
    if keyboard.is_pressed('right'):
        lib.rot[1] += rot_delta
    if keyboard.is_pressed('left'):
        lib.rot[1] -= rot_delta

    if keyboard.is_pressed('e'):
        lib.Cam[1] += move_delta

    if keyboard.is_pressed('q'):
        lib.Cam[1] -= move_delta

    if lib.rot[0] < -1.5:
        lib.rot[0] = -1.5
    if lib.rot[0] > 1.5:
        lib.rot[0] = 1.5
    if lib.rot[1] > 6.25:
        lib.rot[1] = 0
    if lib.rot[1] < 0:
        lib.rot[1] = 6.25

_3D.createWorld()
_3D.createWorldData()

running = True
while running:
    screen.fill((0, 0, 0))

    movement()
    _3D.transform_render(pygame, screen)
    posText = f"Player Position: ( X: {int(lib.Cam[0])}, Y: {int(lib.Cam[1])}, Z: {int(lib.Cam[2])} )"
    rotText = f"Player Rotation: ( RotX: {lib.rot[1]}, RotY: {lib.rot[0]} )"
    fpsText = f"FPS: {clock.get_fps()}"
    wldText = f"ChunkSize ( SizeX: {lib.size[0]}, SizeY: {lib.size[1]}, SizeZ: {lib.size[2]} )"
    text_to_screen(posText, text_font, lib.WHITE, 5, 5)
    text_to_screen(rotText, text_font, lib.WHITE, 5, 25)
    text_to_screen(fpsText, text_font, lib.WHITE, 5, 50)
    text_to_screen(wldText, text_font, lib.WHITE, 5, 75)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
