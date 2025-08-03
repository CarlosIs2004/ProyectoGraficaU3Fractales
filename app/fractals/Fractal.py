
from math import cos, sin, pi

class fractal:
    def __init__(self):
        pass

    def triangulo_equilatero(self, cx, cy, r, angulo_inicial):
        vertices_originales = []
        for i in range(3):
            x = (int)(cx + r * cos(angulo_inicial))
            y = int(cy + r * sin(angulo_inicial))
            angulo_inicial = angulo_inicial +  (2 * pi / 3)
            vertices_originales.append((x, y))
        return vertices_originales
    
    

    def copoVonKoch(self,lado,angle, pan_x , pan_y ,depth):
        vertices = self.triangulo_equilatero(pan_x,pan_y, lado, angle)
        segmentos = []
        segmentos += self.get_koch_curve(vertices[0], vertices[1], depth)
        segmentos += self.get_koch_curve(vertices[1], vertices[2], depth)
        segmentos += self.get_koch_curve(vertices[2], vertices[0], depth)
        return segmentos

    def get_koch_curve(self, start, end, depth):
            if depth == 0:
                return [(start, end)]
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            
            p1 = (start[0] + (dx / 3), start[1] + (dy / 3))
            p3 = (end[0]-( dx / 3), end[1]- (dy / 3))
            sumvx = (p1[0] + p3[0]) 
            resvx = (p3[0] - p1[0]) 
            sumvy = (p1[1] + p3[1]) 
            resvy = (p3[1] - p1[1]) 
            # Calcular el punto del "pico"
            angle = pi/3
            px2 = (sumvx* cos(angle)) + (resvy * sin(angle)) 
            py2 = (sumvy* cos(angle)) - (resvx * sin(angle))
            p2 = (px2, py2)
            return (
                self.get_koch_curve(start, p1, depth-1) +
                self.get_koch_curve(p1, p2, depth-1) +
                self.get_koch_curve(p2, p3, depth-1) +
                self.get_koch_curve(p3, end, depth-1)
            )
    
    def dibujar_triangulo(self,vertices, profundidad):
        if profundidad == 0:
            return [vertices] 
        else:
            # Calcular los puntos medios de los lados del triángulo
            p1 = ( (vertices[0][0] + vertices[1][0]) /2   , (vertices[0][1] + vertices[1][1]) /2 )
            p2 = ( (vertices[1][0] + vertices[2][0]) /2   , (vertices[1][1] + vertices[2][1]) /2 )
            p3 = ( (vertices[2][0] + vertices[0][0]) /2   , (vertices[2][1] + vertices[0][1]) /2 )
            # Dibujar los triángulos internos
            return (
                self.dibujar_triangulo([vertices[0], p1, p3], profundidad - 1) +
                self.dibujar_triangulo([p1, vertices[1], p2], profundidad - 1) +
                self.dibujar_triangulo([p3, p2, vertices[2]], profundidad - 1)
            )
        
    def SierpinskiSegments(self, lado,angle, pan_x , pan_y, profundidad):
        segmentos = []
        segmentos.append(self.triangulo_equilatero(pan_x, pan_y, lado, angle))

        segmentos+=self.dibujar_triangulo(segmentos[0], profundidad)
        return segmentos

