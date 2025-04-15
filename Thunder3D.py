import pygame
import pygame.freetype
import keyboard
import math
import _3D
import library as lib
import projection as proj

pygame.init()

i = 0
screen = pygame.display.set_mode((lib.ScreenW, lib.ScreenH))
pygame.display.set_caption("Thunder3D")
clock = pygame.time.Clock()

def movement():
    move_delta = 0.5
    rotY_delta = -0.1
    rotX_delta = -0.1
    rot_delta = 0.1
    
    yaw = lib.rot[1]

    lib.Last[0] = lib.Cam[0]
    lib.Last[1] = lib.Cam[1]
    lib.Last[2] = lib.Cam[2]
    
    if keyboard.is_pressed('w'):
        lib.Cam[0] += move_delta * math.sin(yaw)
        lib.Cam[2] += move_delta * math.cos(yaw)
        #proj.easeY(0.13, 0.15)

    if keyboard.is_pressed('s'):
        lib.Cam[0] -= move_delta * math.sin(yaw)
        lib.Cam[2] -= move_delta * math.cos(yaw)
        #proj.easeY(0.13, 0.15)

    if keyboard.is_pressed('d'):
        lib.Cam[0] -= move_delta * math.cos(yaw)
        lib.Cam[2] += move_delta * math.sin(yaw)
        #proj.easeX(-0.13, -0.15)

    if keyboard.is_pressed('a'):
        lib.Cam[0] += move_delta * math.cos(yaw)
        lib.Cam[2] -= move_delta * math.sin(yaw)
        #proj.easeX(0.13, 0.15)

    if keyboard.is_pressed('up'):
        lib.rot[0] -= rot_delta
    if keyboard.is_pressed('down'):
        lib.rot[0] += rot_delta
    if keyboard.is_pressed('left'):
        lib.rot[1] += rot_delta
    if keyboard.is_pressed('right'):
        lib.rot[1] -= rot_delta

    if keyboard.is_pressed('q'):
        lib.Cam[1] += move_delta

    if keyboard.is_pressed('e'):
        lib.Cam[1] -= move_delta
    
    camClamp()
    
    #_3D.collide()

def camClamp():
    if -0.1 < lib.rot[2] < 0.1:
        lib.rot[2] = 0
    if lib.rot[2] != 0:
        if lib.rot[2] > 0:
            lib.rot[2] -= 0.05
        else:
            lib.rot[2] += 0.05
    
    for a in range(3):
        if -0.001 < lib.rotSpeed[a] < 0.001:
            lib.rotSpeed[a] = 0
        if lib.rotSpeed[a] != 0:
            if lib.rotSpeed[a] > 0:
                lib.rotSpeed[a] -= 0.05
            else:
                lib.rotSpeed[a] += 0.05
            
            if lib.rotSpeed[a] > 1:
                lib.rotSpeed[a] = 1
            elif lib.rotSpeed[a] < -1:
                lib.rotSpeed[a] = -1
    
    lib.rot[1] += lib.rotSpeed[0]
    lib.rot[0] += lib.rotSpeed[1]
    
    if lib.rot[0] < -1.5:
        lib.rot[0] = -1.5
    if lib.rot[0] > 1.5:
        lib.rot[0] = 1.5
    if lib.rot[1] > 6.25:
        lib.rot[1] = 0.1
    if lib.rot[1] < 0.1:
        lib.rot[1] = 6.25

_3D.createWorld()
_3D.createWorldData()

def __Init__(x,y,z,rx,ry):
    lib.Cam[0] = x
    lib.Cam[1] = y
    lib.Cam[2] = z
    lib.rot[0] = rx
    lib.rot[1] = ry

#__Init__(random.randint(2, (lib.size[0] * 4) - 2), random.randint((lib.size[1] * 4) + 2, (lib.size[1] * 4) + 10), random.randint(2, (lib.size[2] * 4) - 2), 0, 0)

running = True
while running:
    #print("Start")
    screen.fill((0, 0, 0))

    movement()
    _3D.transform_render(pygame, screen)
    if lib.style == "Main":
        posText = f"Player Position: ( X: {int(lib.Cam[0]/4)}, Y: {int(lib.Cam[1]/4)}, Z: {int(lib.Cam[2]/4)} )"
        rotText = f"Player Rotation: ( RotX: {lib.rot[1]}, RotY: {lib.rot[0]}, RotZ: {lib.rot[2]} )"
        fpsText = f"FPS: {clock.get_fps()}"
        wldText = f"ChunkSize ( SizeX: {lib.size[0]}, SizeY: {lib.size[1]}, SizeZ: {lib.size[2]} )"
        lib.text_to_screen(posText, lib.WHITE, 5, 5, screen)
        lib.text_to_screen(rotText, lib.WHITE, 5, 25, screen)
        lib.text_to_screen(fpsText, lib.WHITE, 5, 50, screen)
        lib.text_to_screen(wldText, lib.WHITE, 5, 75, screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

    #print("Finish")

pygame.quit()
