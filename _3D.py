import library as lib
import math
import random

def _3DProjection(x, y, z, color, ID, pygame, screen):
    scale = lib.DTS / (z + 0.0001)
    size = lib.objDrawSize * scale
    pygame.draw.rect(screen, lib.world[color], ((x * (lib.DTS / (z + 0.0001))) + (lib.ScreenW/2), (-y * (lib.DTS / (z + 0.0001))) + (lib.ScreenH/2),  lib.objDrawSize, lib.objDrawSize))

def AddObj(x,y,z,ID):
    lib.obj.append([x,y,z,ID])

def get_index(x, y, z, ID):
    if [x, y, z, ID] in lib.obj:
        return True
    return False

def createWorld():
    for y in range(lib.size[1]):
        for x in range(lib.size[2]):
            for z in range(lib.size[0]):
                gen = random.randint(0,5)
                if gen > 3:
                    rand = random.choice((lib.WHITE, lib.LGRAY, lib.DGRAY))
                    lib.world.append(rand)
                    AddObj(x * lib.objSize, y * lib.objSize, z * lib.objSize, 1)
                else:
                    lib.world.append(0)
                    AddObj(x * lib.objSize, y * lib.objSize, z * lib.objSize, 0)

def fillQuad(quad, color, x,y,z, i, pygame, screen):
    _3DProjection(x, y, z, color, i, pygame, screen)

def RotationMatrix(x,y,z, sin1,cos1,sin2,cos2):
    lib.objRot[0] = ((z * sin1) + (x * cos1))
    lib.objRot[2] = ((z * cos1) - (x * sin1))

    lib.objRot[1] = ((lib.objRot[2] * sin2) + (y * cos2))
    lib.objRot[2] = ((lib.objRot[2] * cos2) - (y * sin2))

    return lib.objRot[0], lib.objRot[1], lib.objRot[2]

def compute_normal(v0, v1, v2, v3):
    u1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
    v1 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
    normal1 = (u1[1] * v1[2] - u1[2] * v1[1], u1[2] * v1[0] - u1[0] * v1[2], u1[0] * v1[1] - u1[1] * v1[0])

    u2 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
    v2 = (v3[0] - v0[0], v3[1] - v0[1], v3[2] - v0[2])
    normal2 = (u2[1] * v2[2] - u2[2] * v2[1], u2[2] * v2[0] - u2[0] * v2[2], u2[0] * v2[1] - u2[1] * v2[0])

    normal = (
        (normal1[0] + normal2[0]) / 2,
        (normal1[1] + normal2[1]) / 2,
        (normal1[2] + normal2[2]) / 2
    )

    length = (normal[0]**2 + normal[1]**2 + normal[2]**2) ** 0.5
    normal = (normal[0] / length, normal[1] / length, normal[2] / length)

    return normal

def computeDotProduct(points, z):
    v0 = points[z[0]]
    v1 = points[z[1]]
    v2 = points[z[2]]
    v3 = points[z[3]]

    normal = compute_normal(v0, v1, v2, v3)

    quad_center = (
        (v0[0] + v1[0] + v2[0] + v3[0]) / 4,
        (v0[1] + v1[1] + v2[1] + v3[1]) / 4,
        (v0[2] + v1[2] + v2[2] + v3[2]) / 4
    )
        
    camera_vector = (
        quad_center[0] - lib.Cam[0],
        quad_center[1] - lib.Cam[1],
        quad_center[2] - lib.Cam[2]
    )

    dot_product = normal[0] * camera_vector[0] + normal[1] * camera_vector[1] + normal[2] * camera_vector[2]

    return dot_product

def transform_render(pygame, screen):
    CamXDirSin = math.sin(0 - lib.rot[0])
    CamXDirCos = math.cos(0 - lib.rot[0])
    CamYDirSin = math.sin(0 - lib.rot[1])
    CamYDirCos = math.cos(0 - lib.rot[1])
    
    transformed_objects = []
    objNumb = 0
    for obj in lib.obj:
        if obj[3] == 0:
            objNumb += 1
            continue
        
        noRend = [0,0,0,0,0,0]
        for i in range(6):
            idx = get_index(obj[0] + lib.check[i][0], obj[1] + lib.check[i][1], obj[2] + lib.check[i][2], 1)
            if idx:
                noRend[i] = 1
        if all(map(lambda ID: ID==1, noRend)):
            continue
        
        points = [
            [obj[0], obj[1], obj[2]], [(obj[0] + lib.objSize), obj[1], obj[2]],                                                               # 000 100
            [(obj[0] + lib.objSize), (obj[1] + lib.objSize), obj[2]], [obj[0], (obj[1] + lib.objSize), obj[2]],                               # 110 010
            [obj[0], obj[1], (obj[2] + lib.objSize)], [(obj[0] + lib.objSize), obj[1], (obj[2] + lib.objSize)],                               # 001 101
            [(obj[0] + lib.objSize), (obj[1] + lib.objSize), (obj[2] + lib.objSize)], [obj[0],(obj[1] + lib.objSize), (obj[2] + lib.objSize)] # 111 011
        ]

        for i, z in enumerate(lib.quad):
            if noRend[i] == 0:
                dP = computeDotProduct(points, z)
                if dP > 0:
                    continue
                for p in z:
                    rotX, rotY, rotZ = RotationMatrix(points[p][0] - lib.Cam[0], points[p][1] - lib.Cam[1], points[p][2] - lib.Cam[2], CamYDirSin, CamYDirCos, CamXDirSin, CamXDirCos)
                    transformed_objects.append((rotX, rotY, rotZ, obj, objNumb))
            

        sorted_objects = sorted(transformed_objects, key=lambda objs: objs[2], reverse=True)
        
        for tx, ty, tz, obj, color in sorted_objects:
            if 20 > tz > 0:
                #fillQuad(quad, color, tx, ty, tz, i, pygame, screen)
                _3DProjection(tx, ty, tz, color, i, pygame, screen)

        objNumb += 1
