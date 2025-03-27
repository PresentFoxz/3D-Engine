import library as lib
import pygame
import math

def projectRect(x, y, scale, ID, draw, screen):
    pygame.draw.rect(screen, lib.color[ID], (x, y, scale, scale))
    if draw == 1:
        lib.text_to_screen(str(i), (255, 0, 0), x, y - 30, screen)

def drawQuadLines(quads, size, pygame, screen):
    v1 = quads[0]
    v2 = quads[1]
    v3 = quads[2]
    v4 = quads[3]

    print("drawing")
    def draw_line(p1, p2):
        x1, y1 = int(p1[0]), int(p1[1])
        x2, y2 = int(p2[0]), int(p2[1])
        pygame.draw.line(screen, (0, 0, 0), (x1,y1),(x2,y2), size)
        print("done")

    draw_line(v1, v2)
    draw_line(v3, v4)
    draw_line(v1, v4)
    draw_line(v2, v3)

def drawFilledTris(screen, triangle, iD, x_step, y_step):
    min_y = max(0, int(triangle[0][1]))
    max_y = min(lib.ScreenH, int(triangle[-1][1]))

    for y in range(min_y, max_y, y_step):
        intersections = []

        for i in range(3):
            v1, v2 = triangle[i], triangle[(i + 1) % 3]
                
            if (v1[1] <= y < v2[1]) or (v2[1] <= y < v1[1]):
                dy = (v2[1] - v1[1])
                if dy != 0:
                    t = (y - v1[1]) / dy
                    x_intersect = v1[0] + t * (v2[0] - v1[0])
                    intersections.append(int(x_intersect))

        if len(intersections) == 2:
            x_start, x_end = sorted(intersections)
            x_start = max(0, x_start)
            x_end = min(lib.ScreenW, x_end)

            for x in range(x_start, x_end, x_step):
                if x_step == 1 and y_step == 1:
                    screen.set_at((x, y), lib.color[iD])
                else:
                    pygame.draw.rect(screen, lib.color[iD], (x, y, lib.objFillSize, lib.objFillSize))

def drawFilledQuads(screen, vertices, iD, x_step, y_step):
    triangle1 = sorted([vertices[0], vertices[1], vertices[2]], key=lambda v: v[1])
    triangle2 = sorted([vertices[2], vertices[3], vertices[0]], key=lambda v: v[1])

    def fill_triangle(triangle):
        min_y = max(0, int(triangle[0][1]))
        max_y = min(lib.ScreenH, int(triangle[-1][1]))

        for y in range(min_y, max_y, y_step):
            intersections = []

            for i in range(3):
                v1, v2 = triangle[i], triangle[(i + 1) % 3]
                
                if (v1[1] <= y < v2[1]) or (v2[1] <= y < v1[1]):
                    dy = (v2[1] - v1[1])
                    if dy != 0:
                        t = (y - v1[1]) / dy
                        x_intersect = v1[0] + t * (v2[0] - v1[0])
                        intersections.append(int(x_intersect))

            if len(intersections) == 2:
                x_start, x_end = sorted(intersections)
                x_start = max(0, x_start)
                x_end = min(lib.ScreenW, x_end)

                for x in range(x_start, x_end, x_step):
                    if x_step == 1 and y_step == 1:
                        screen.set_at((x, y), lib.color[iD])
                    else:
                        pygame.draw.rect(screen, lib.color[iD], (x, y, lib.objFillSize, lib.objFillSize))

    fill_triangle(triangle1)
    fill_triangle(triangle2)

def RotationMatrix(x, y, z, sin1, cos1, sin2, cos2, sin3, cos3):
    tempX = (z * sin1) + (x * cos1)
    tempZ = (z * cos1) - (x * sin1)

    tempY = (tempZ * sin2) + (y * cos2)
    finalZ = (tempZ * cos2) - (y * sin2)

    finalX = (tempX * cos3) - (tempY * sin3)
    finalY = (tempX * sin3) + (tempY * cos3)

    return finalX, finalY, finalZ


def compute_normal(v0, v1, v2, v3):
    u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
    v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])

    normal = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

    length = ((normal[0]**2 + normal[1]**2 + normal[2]**2) ** 0.5) + 0.0001
    normal = (normal[0] / length, normal[1] / length, normal[2] / length)

    return normal

def computeDotProduct(points, z):
    v0 = points[z[0]][0]
    v1 = points[z[1]][0]
    v2 = points[z[2]][0]
    v3 = points[z[3]][0]

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

def perspective_matrix(fov, aspect, near, far):
    tan_half_fov = math.tan(math.radians(fov) / 2)
    
    return [
        [1 / (aspect * tan_half_fov), 0, 0, 0],
        [0, 1 / tan_half_fov, 0, 0],
        [0, 0, -((far + near) / (far - near)), -((2 * far * near) / (far - near))],
        [0, 0, -1, 0]
    ]

def apply_projection(matrix, point):
    x, y, z = point
    w = 1

    projected_x = (matrix[0][0] * x) + (matrix[0][2] * z)
    projected_y = (matrix[1][1] * y) + (matrix[1][2] * z)
    projected_z = (matrix[2][2] * z) + (matrix[2][3] * w)
    projected_w = (matrix[3][2] * z) + (matrix[3][3] * w)

    #print(projected_x, projected_y, projected_z, projected_w)
    
    #if projected_w != 0:
    #    projected_x /= projected_w
    #    projected_y /= projected_w
    #    projected_z /= projected_w

    return (projected_x, projected_y, projected_z)

def project2D(point):
    x, y, z = point

    if z == 0:
        z = 0.0001
    
    f = 1 / (lib.distToScreen / 2)

    projected_x = (x / z) * f
    projected_y = (y / z) * f

    screen_x = int((projected_x + 1) * 0.5 * lib.ScreenW)
    screen_y = int((1 - projected_y) * 0.5 * lib.ScreenH)

    return screen_x, screen_y

def checkPos(points):
    xm = sum(v[0] for v in points) / len(points)
    ym = sum(v[1] for v in points) / len(points)
    zm = sum(v[2] for v in points) / len(points)
    
    return (xm, ym, zm)

def easeX(amt, cap):
    lib.rot[2] += amt
    if cap > 0:
        if lib.rot[2] > cap:
            lib.rot[2] = cap
    elif cap < 0:
        if lib.rot[2] < cap:
            lib.rot[2] = cap

def easeY(amt, cap):
    lib.rotSpeed[2] += amt
    if cap > 0:
        if lib.rotSpeed[2] > cap:
            lib.rotSpeed[2] = cap
    elif cap < 0:
        if lib.rotSpeed[2] < cap:
            lib.rotSpeed[2] = cap