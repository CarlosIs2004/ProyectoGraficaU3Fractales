import numpy as np
import pygame
from math import cos, sin

class Mandelbrot:
    def __init__(self, width, height, xmin=-2.0, xmax=1.0, ymin=-1.5, ymax=1.5, max_iter=50):
        self.width = width
        self.height = height
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.max_iter = max_iter
        
        # Cache para optimización
        self.cached_data = None
        self.cached_params = None
        self.render_scale = 0.5  # Renderizar a menor resolución para optimización
        self.effective_width = int(width * self.render_scale)
        self.effective_height = int(height * self.render_scale)
        
        # Superficie para cache de renderizado
        self.surface = None

    def mandelbrot_vectorized(self):
        """Versión vectorizada usando NumPy para mejor rendimiento"""
        # Crear arrays de coordenadas
        x = np.linspace(self.xmin, self.xmax, self.effective_width)
        y = np.linspace(self.ymin, self.ymax, self.effective_height)
        X, Y = np.meshgrid(x, y)
        
        # Crear matriz de números complejos
        C = X + 1j * Y
        Z = np.zeros_like(C)
        
        # Array para almacenar las iteraciones
        iterations = np.zeros(C.shape, dtype=int)
        
        # Algoritmo optimizado con vectorización
        for i in range(self.max_iter):
            # Máscara de puntos que no han divergido
            mask = np.abs(Z) <= 2
            
            # Solo calcular puntos que no han divergido
            Z[mask] = Z[mask]**2 + C[mask]
            iterations[mask] = i
            
            # Si todos los puntos han divergido, salir del bucle
            if not np.any(mask):
                break
        
        return iterations

    def actualizar_parametros(self, scale, angle, pan_x, pan_y, max_iter):
        """Actualiza parámetros solo si han cambiado significativamente"""
        # Reducir sensibilidad para evitar recálculos constantes
        zoom = max(0.1, scale / 200.0)  # Mayor factor de zoom para mejor control
        
        # Calcular centro con menos sensibilidad
        center_x = (pan_x - self.width/2) / (self.width/6) / zoom
        center_y = (pan_y - self.height/2) / (self.height/6) / zoom
        
        # Aplicar rotación solo si es significativa
        if abs(angle) > 0.1:
            cos_a = cos(angle)
            sin_a = sin(angle)
            new_center_x = center_x * cos_a - center_y * sin_a
            new_center_y = center_x * sin_a + center_y * cos_a
            center_x, center_y = new_center_x, new_center_y
        
        # Calcular nuevos límites
        range_x = 3.0 / zoom
        range_y = 3.0 / zoom
        
        new_xmin = center_x - range_x/2
        new_xmax = center_x + range_x/2
        new_ymin = center_y - range_y/2
        new_ymax = center_y + range_y/2
        new_max_iter = min(80, max_iter * 8)  # Limitar iteraciones máximas
        
        # Crear tupla de parámetros para comparar cambios
        new_params = (round(new_xmin, 4), round(new_xmax, 4), 
                     round(new_ymin, 4), round(new_ymax, 4), new_max_iter)
        
        # Solo recalcular si los parámetros han cambiado significativamente
        if self.cached_params != new_params:
            self.xmin, self.xmax = new_xmin, new_xmax
            self.ymin, self.ymax = new_ymin, new_ymax
            self.max_iter = new_max_iter
            self.cached_params = new_params
            return True
        return False

    def create_color_palette(self):
        """Crear paleta de colores optimizada"""
        colors = np.zeros((self.max_iter + 1, 3), dtype=np.uint8)
        
        for i in range(self.max_iter):
            # Paleta de colores más suave y rápida
            t = i / self.max_iter
            
            # Gradiente azul-púrpura-naranja
            if t < 0.33:
                ratio = t / 0.33
                r = int(50 * ratio)
                g = int(100 * ratio)
                b = int(255 * (1 - ratio * 0.3))
            elif t < 0.66:
                ratio = (t - 0.33) / 0.33
                r = int(50 + 150 * ratio)
                g = int(100 + 100 * ratio)
                b = int(200 - 100 * ratio)
            else:
                ratio = (t - 0.66) / 0.34
                r = int(200 + 55 * ratio)
                g = int(200 - 50 * ratio)
                b = int(100 * (1 - ratio))
            
            colors[i] = [r, g, b]
        
        # Negro para puntos dentro del conjunto
        colors[self.max_iter] = [0, 0, 0]
        return colors

    def dibujar(self, screen, scale, angle, pan_x, pan_y, iter):
        """Versión optimizada del renderizado"""
        # Solo recalcular si es necesario
        needs_update = self.actualizar_parametros(scale, angle, pan_x, pan_y, iter)
        
        if needs_update or self.surface is None:
            # Calcular conjunto de Mandelbrot
            mandelbrot_data = self.mandelbrot_vectorized()
            
            # Crear paleta de colores
            colors = self.create_color_palette()
            
            # Crear superficie a escala reducida
            small_surface = pygame.Surface((self.effective_width, self.effective_height))
            
            # Convertir datos a imagen usando NumPy (más rápido)
            color_data = colors[mandelbrot_data]
            
            # Usar surfarray para renderizado rápido
            pygame.surfarray.blit_array(small_surface, color_data.transpose(1, 0, 2))
            
            # Escalar la superficie al tamaño completo usando smoothscale para mejor calidad
            self.surface = pygame.transform.smoothscale(small_surface, (self.width, self.height))
        
        # Dibujar la superficie cached
        if self.surface:
            screen.blit(self.surface, (0, 0))