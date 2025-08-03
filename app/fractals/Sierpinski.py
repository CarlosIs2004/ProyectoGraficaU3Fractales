
from math import cos, sin, pi

class Sierpinski:
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

