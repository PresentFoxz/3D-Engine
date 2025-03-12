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
                    AddObj(x * lib.objSize, y * lib.objSize, z * lib.objSize, random.randint(1,3))
                else:
                    AddObj(x * lib.objSize, y * lib.objSize, z * lib.objSize, 0)

def createWorldData():
    indx = 0
    for obj in lib.obj:
        if obj[3] == 0:
            print("Skip")
            continue
        noRend = [0,0,0,0,0,0]
        for i in range(6):
            idx = get_index(obj[0] + lib.check[i][0], obj[1] + lib.check[i][1], obj[2] + lib.check[i][2])
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
        
        for i in range(len(lib.quad)):
            if noRend[i] == 0:
                data = [lib.quad[i][0] + indx, lib.quad[i][1] + indx, lib.quad[i][2] + indx, lib.quad[i][3] + indx]
                lib.quadData.append(data)
                print(i, ": ", lib.quadData[len(lib.quadData) - 1])
        
        print(noRend)
        for p in points:
            lib.vertexData.append([p, obj[3]])
        
        indx += 8
        
    print("Length Verts: ", len(lib.vertexData))
    print("Length Quads: ", len(lib.quadData))
    print("Vert:", lib.vertexData)
    print("Quad:", lib.quadData)

def collide():
    for iD in range(len(lib.obj)):
        if (lib.obj[iD][0] + 5 < lib.Cam[0] < lib.obj[iD][0] - 1) and (lib.obj[iD][2] + 5 > lib.Cam[2] > lib.obj[iD][2] - 1) and ((lib.Cam[1] + 4 >= lib.obj[iD][1] + 5) or (lib.Cam[1] <= lib.obj[iD][1] - 1)):
            lib.Cam[0] = lib.Last[0]
            lib.Cam[2] = lib.Last[2]
            lib.Cam[1] = lib.Last[1]

def checkPos(points):
    v1 = points[0]
    v2 = points[1]
    v3 = points[2]
    v4 = points[3]

    xm = (v1[0] + v2[0] + v3[0] + v4[0])/4
    ym = (v1[1] + v2[1] + v3[1] + v4[1])/4
    zm = (v1[2] + v2[2] + v3[2] + v4[2])/4

    return (xm, ym, zm)


def transform_render(pygame, screen):
    CamXDirSin = math.sin(0 - lib.rot[0])
    CamXDirCos = math.cos(0 - lib.rot[0])
    CamYDirSin = math.sin(0 - lib.rot[1])
    CamYDirCos = math.cos(0 - lib.rot[1])
    
    transformed_objects = []
    all_quads = []
    pointDraw = False
    lineDraw = True
    for z in lib.quadData:
        dP = proj.computeDotProduct(lib.vertexData, z)
        quad_add = []
        saveMainPos = []
        if dP > 0:
            continue
        for p in z:
            rotX, rotY, rotZ = proj.RotationMatrix(lib.vertexData[p][0][0] - lib.Cam[0], lib.vertexData[p][0][1] - lib.Cam[1], lib.vertexData[p][0][2] - lib.Cam[2], CamYDirSin, CamYDirCos, CamXDirSin, CamXDirCos)
            proj_matrix = proj.perspective_matrix(lib.distToScreen, (lib.ScreenW / lib.ScreenH), 0, lib.maxDist)
            newX, newY, newZ = proj.apply_projection(proj_matrix, (rotX, rotY, rotZ))

            screenX, screenY = int((newX * (lib.distToScreen / (newZ + 0.1))) + (lib.ScreenW/2)), int((newY * (lib.distToScreen / (newZ + 0.1))) + (lib.ScreenH/2))
            col = lib.vertexData[p][1]
            if lineDraw:
                quad_add.append([screenX, screenY])
            if pointDraw:
                transformed_objects.append((screenX, screenY, int(lib.distToScreen / newZ), col))
            saveMainPos.append([int(newX), int(newY), int(newZ)])

        setX, setY, setZ = checkPos(saveMainPos)
        try:
            if -lib.maxDist < setZ < -1:
                all_quads.append([[setX, setY, setZ], quad_add, col])
        except Exception:
            continue

    if lineDraw:
        sorted_quads = sorted(all_quads, key=lambda quadSet: quadSet[0][2], reverse=False)

        for pos, allQuads, i in sorted_quads:
            try:
                if lib.style == "Main":
                    lMove, rMove = 4, 4
                if lib.style == "Thumby":
                    lMove, rMove = 7, 7
                    lib.objFillSize = 10
                if lib.style == "Playdate":
                    lMove, rMove = 4, 4
                    lib.objFillSize = 7
                proj.drawFilledQuads(screen, allQuads, i, lMove, rMove)
                proj.drawQuadLines(allQuads, 5, screen)
            except Exception as e:
                pass
    
    if pointDraw:
        sorted_objects = sorted(transformed_objects, key=lambda objs: objs[2], reverse=True)
        
        for tx, ty, s, c in sorted_objects:
            proj.projectRect(tx, ty, s, c, 0, screen)