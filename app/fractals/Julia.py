import numpy as np
import pygame
from math import cos, sin

class Julia:
    def __init__(self, width, height, c=complex(-0.7, 0.27015), xmin=-2.0, xmax=2.0, ymin=-2.0, ymax=2.0, max_iter=50):
        self.width = width
        self.height = height
        self.c = c
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.max_iter = max_iter
        
        # Cache para optimización
        self.cached_data = None
        self.cached_params = None
        self.render_scale = 0.6  # Un poco mejor calidad que Mandelbrot
        self.effective_width = int(width * self.render_scale)
        self.effective_height = int(height * self.render_scale)
        
        # Superficie para cache de renderizado
        self.surface = None
        
        # Parámetros c predefinidos para variación rápida
        self.c_variations = [
            complex(-0.7, 0.27015),
            complex(-0.8, 0.156),
            complex(-0.75, 0.11),
            complex(0.285, 0.01),
            complex(-0.4, 0.6),
            complex(-0.123, 0.745),
            complex(-0.745, 0.113),
            complex(-0.235, -0.827)
        ]
        self.current_c_index = 0

    def julia_vectorized(self):
        """Versión vectorizada usando NumPy"""
        # Crear arrays de coordenadas
        x = np.linspace(self.xmin, self.xmax, self.effective_width)
        y = np.linspace(self.ymin, self.ymax, self.effective_height)
        X, Y = np.meshgrid(x, y)
        
        # Matriz inicial Z
        Z = X + 1j * Y
        
        # Array para iteraciones
        iterations = np.zeros(Z.shape, dtype=int)
        
        # Algoritmo optimizado
        for i in range(self.max_iter):
            # Máscara de puntos que no han divergido
            mask = np.abs(Z) <= 2
            
            # Solo calcular puntos activos
            Z[mask] = Z[mask]**2 + self.c
            iterations[mask] = i
            
            # Salir si todos han divergido
            if not np.any(mask):
                break
        
        return iterations

    def actualizar_parametros(self, scale, angle, pan_x, pan_y, max_iter):
        """Actualiza parámetros y cambia c dinámicamente"""
        # Zoom más controlado
        zoom = max(0.1, scale / 150.0)
        
        # Centro con menos sensibilidad
        center_x = (pan_x - self.width/2) / (self.width/4) / zoom
        center_y = (pan_y - self.height/2) / (self.height/4) / zoom
        
        # Aplicar rotación
        if abs(angle) > 0.05:
            cos_a = cos(angle)
            sin_a = sin(angle)
            new_center_x = center_x * cos_a - center_y * sin_a
            new_center_y = center_x * sin_a + center_y * cos_a
            center_x, center_y = new_center_x, new_center_y
        
        # Calcular límites
        range_x = 4.0 / zoom
        range_y = 4.0 / zoom
        
        new_xmin = center_x - range_x/2
        new_xmax = center_x + range_x/2
        new_ymin = center_y - range_y/2
        new_ymax = center_y + range_y/2
        new_max_iter = min(60, max_iter * 10)
        
        # Cambiar parámetro c basado en el ángulo de forma discreta para mejor rendimiento
        angle_normalized = (angle % (2 * 3.14159)) / (2 * 3.14159)
        new_c_index = int(angle_normalized * len(self.c_variations))
        
        if new_c_index != self.current_c_index:
            self.current_c_index = new_c_index
            self.c = self.c_variations[self.current_c_index]
        
        # Crear parámetros para comparar cambios
        new_params = (round(new_xmin, 3), round(new_xmax, 3), 
                     round(new_ymin, 3), round(new_ymax, 3), 
                     new_max_iter, self.current_c_index)
        
        # Solo recalcular si hay cambios significativos
        if self.cached_params != new_params:
            self.xmin, self.xmax = new_xmin, new_xmax
            self.ymin, self.ymax = new_ymin, new_ymax
            self.max_iter = new_max_iter
            self.cached_params = new_params
            return True
        return False

    def create_color_palette(self):
        """Paleta de colores optimizada para Julia"""
        colors = np.zeros((self.max_iter + 1, 3), dtype=np.uint8)
        
        for i in range(self.max_iter):
            t = i / self.max_iter
            
            # Paleta fría más suave
            if t < 0.25:
                ratio = t / 0.25
                r = int(20 + 80 * ratio)
                g = int(50 + 150 * ratio)
                b = int(100 + 155 * ratio)
            elif t < 0.5:
                ratio = (t - 0.25) / 0.25
                r = int(100 + 100 * ratio)
                g = int(200 + 50 * ratio)
                b = int(255 - 50 * ratio)
            elif t < 0.75:
                ratio = (t - 0.5) / 0.25
                r = int(200 + 50 * ratio)
                g = int(250 - 100 * ratio)
                b = int(205 - 80 * ratio)
            else:
                ratio = (t - 0.75) / 0.25
                r = int(250 + 5 * ratio)
                g = int(150 + 80 * ratio)
                b = int(125 + 100 * ratio)
            
            colors[i] = [r, g, b]
        
        # Negro para puntos del conjunto
        colors[self.max_iter] = [0, 0, 0]
        return colors

    def dibujar(self, screen, scale, angle, pan_x, pan_y, iter):
        """Renderizado optimizado"""
        # Solo recalcular cuando sea necesario
        needs_update = self.actualizar_parametros(scale, angle, pan_x, pan_y, iter)
        
        if needs_update or self.surface is None:
            # Calcular conjunto de Julia
            julia_data = self.julia_vectorized()
            
            # Crear colores
            colors = self.create_color_palette()
            
            # Superficie pequeña para renderizado rápido
            small_surface = pygame.Surface((self.effective_width, self.effective_height))
            
            # Convertir datos a colores
            color_data = colors[julia_data]
            
            # Renderizado rápido con surfarray
            pygame.surfarray.blit_array(small_surface, color_data.transpose(1, 0, 2))
            
            # Escalar al tamaño completo
            self.surface = pygame.transform.smoothscale(small_surface, (self.width, self.height))
        
        # Dibujar superficie cached
        if self.surface:
            screen.blit(self.surface, (0, 0))

    def get_current_c_info(self):
        """Obtener información del parámetro c actual"""
        return f"c = {self.c.real:.3f} + {self.c.imag:.3f}i"