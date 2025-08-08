from math import cos, sin, radians

class ArbolRecursivo:
    def __init__(self):
        pass

    def ramas(self, x, y, angulo, longitud, profundidad, factor_angulo=30, factor_longitud=0.7):
        """
        Genera los segmentos de un árbol fractal recursivo.
        Retorna una lista de tuplas: [(start, end), ...]
        """
        if profundidad == 0 or longitud < 2:
            return []
        # Calcular el punto final de la rama actual
        x2 = x + longitud * cos(radians(angulo))
        y2 = y - longitud * sin(radians(angulo))
        segmento = [((x, y), (x2, y2))]
        # Recursivamente crear ramas izquierda y derecha
        segmento += self.ramas(x2, y2, angulo - factor_angulo, longitud * factor_longitud, profundidad - 1, factor_angulo, factor_longitud)
        segmento += self.ramas(x2, y2, angulo + factor_angulo, longitud * factor_longitud, profundidad - 1, factor_angulo, factor_longitud)
        return segmento

    def generar_arbol(self, x, y, angulo, longitud, profundidad):
        """
        Interfaz principal para obtener todos los segmentos del árbol.
        """
        return self.ramas(x, y, angulo, longitud, profundidad)
