import library as lib
import projection as proj
import math
import random
import keyboard

def AddObj(x,y,z,ID):
    lib.obj.append([x,y,z,ID])

def get_index(x, y, z):
    if ([x, y, z, 1] in lib.obj) or ([x, y, z, 2] in lib.obj) or ([x, y, z, 3] in lib.obj):
        return True
    return False

def createWorld():
    for y in range(lib.size[1]):
        for x in range(lib.size[2]):
            for z in range(lib.size[0]):
                gen = random.randint(0,5)
                if gen > 2:
                    AddObj(x * lib.objSize, y * lib.objSize, z * lib.objSize, random.randint(1,2))
                else:
                    AddObj(x * lib.objSize, y * lib.objSize, z * lib.objSize, 0)

def createWorldData():
    indx = 0
    for obj in lib.obj:
        if obj[3] == 0:
            print("Skip")
            continue
        noRend = [0]*len(lib.tri)
        move = 0
        for i in range(6):
            idx = get_index(obj[0] + lib.check[i][0], obj[1] + lib.check[i][1], obj[2] + lib.check[i][2])
            if idx:
                noRend[move] = 1
                noRend[move + 1] = 1
            move += 2
        if all(map(lambda ID: ID==1, noRend)):
            continue
        
        points = [
            [obj[0], obj[1], obj[2]], [(obj[0] + lib.objSize), obj[1], obj[2]],                                                               # 000 100
            [(obj[0] + lib.objSize), (obj[1] + lib.objSize), obj[2]], [obj[0], (obj[1] + lib.objSize), obj[2]],                               # 110 010
            [obj[0], obj[1], (obj[2] + lib.objSize)], [(obj[0] + lib.objSize), obj[1], (obj[2] + lib.objSize)],                               # 001 101
            [(obj[0] + lib.objSize), (obj[1] + lib.objSize), (obj[2] + lib.objSize)], [obj[0],(obj[1] + lib.objSize), (obj[2] + lib.objSize)] # 111 011
        ]
        
        for i in range(len(lib.tri)):
            if noRend[i] == 0:
                data = [lib.tri[i][0] + indx, lib.tri[i][1] + indx, lib.tri[i][2] + indx]
                lib.triData.append([data, i])
                print(i, ": ", lib.triData[len(lib.triData) - 1])
        
        print(noRend)
        for p in points:
            lib.vertexData.append([p, obj[3]])
        
        indx += 8
        
    print("Length Verts: ", len(lib.vertexData))
    print("Length Tris: ", len(lib.triData))
    print("Vert:", lib.vertexData)
    print("Tri:", lib.triData)

def collide():
    for iD in range(len(lib.obj)):
        if (lib.obj[iD][0] + 5 < lib.Cam[0] < lib.obj[iD][0] - 1) and (lib.obj[iD][2] + 5 > lib.Cam[2] > lib.obj[iD][2] - 1) and ((lib.Cam[1] + 4 >= lib.obj[iD][1] + 5) or (lib.Cam[1] <= lib.obj[iD][1] - 1)):
            lib.Cam[0] = lib.Last[0]
            lib.Cam[2] = lib.Last[2]
            lib.Cam[1] = lib.Last[1]

def transform_render(pygame, screen):
    CamXDirSin = -math.sin(lib.rot[0] + lib.rotSpeed[2])
    CamXDirCos = math.cos(lib.rot[0] + lib.rotSpeed[2])
    CamYDirSin = -math.sin(lib.rot[1])
    CamYDirCos = math.cos(lib.rot[1])
    CamZDirSin = -math.sin(lib.rot[2])
    CamZDirCos = math.cos(lib.rot[2])

    transformed_objects = []
    all_tris = []
    pointDraw = False
    lineDraw = True
    for z, triangle in enumerate(lib.triData):
        tri = triangle[0]
        idx = triangle[1]
        dP = proj.computeDotProduct(lib.vertexData, tri)
        tri_add = []
        saveMainPos = []
        if dP > 0:
            continue
        for i in range(3):
            rot = proj.RotationMatrix(lib.vertexData[tri[i]][0][0] - lib.Cam[0], lib.vertexData[tri[i]][0][1] - lib.Cam[1], lib.vertexData[tri[i]][0][2] - lib.Cam[2], CamYDirSin, CamYDirCos, CamXDirSin, CamXDirCos, CamZDirSin, CamZDirCos)
            if rot[2] < 0:
                rot[2] = 0
            proj_matrix = proj.perspective_matrix(lib.distToScreen, (lib.ScreenW / lib.ScreenH), 0.1, lib.maxDist)
            newPoints = proj.apply_projection(proj_matrix, rot)

            screenX, screenY = proj.project2D([newPoints[0], newPoints[1], newPoints[2]])
            col = lib.vertexData[tri[i]][1]
            if lineDraw:
                tri_add.append([screenX, screenY])
            if pointDraw:
                transformed_objects.append([screenX, screenY, newPoints[2], int(lib.distToScreen / (-newPoints[2] + 0.001)), col, tri[i]])
            saveMainPos.append([int(newPoints[0]), int(newPoints[1]), int(newPoints[2])])
        uv_coords = lib.uv[idx]

        if lineDraw:
            setX, setY, setZ = proj.checkPos(saveMainPos)
            if setZ >= 0:
                continue
            else:
                point = sorted([tri_add[0], tri_add[1], tri_add[2]], key=lambda v: v[1])
                if col == 1:
                    texu = lib.tree
                else:
                    texu = lib.dirt
                all_tris.append([[setX, setY, setZ], uv_coords, texu, point])

    if lineDraw:
        sorted_tris = sorted(filter(lambda triSet: triSet[0][2] > -10, all_tris), key=lambda triSet: triSet[0][2], reverse=False)
        
        for pos, uv, texture, allTris in sorted_tris:
            if lib.style == "Main":
                lMove, rMove = 7, 7
            if lib.style == "Thumby":
                lMove, rMove = 7, 7
            if lib.style == "Playdate":
                lMove, rMove = 7, 7
            proj.drawFilledTris(screen, texture, allTris, uv, lMove, rMove)

            #print(pos)

            if pos[2] > -5:
                proj.drawTriLines(allTris, 1, pygame, screen)
    
    if pointDraw:
        sorted_points = sorted(filter(lambda obj: obj[2] > -10, transformed_objects), key=lambda objs: objs[2], reverse=True)
        
        for tx, ty, z, s, c, p in sorted_points:
            proj.projectRect(tx, ty, 10, c, 1, p, screen)
            