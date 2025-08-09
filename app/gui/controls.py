from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys
import pygame
from pygame.locals import *
from math import pi
from fractals.CurvaKoch import CurvaKoch
from fractals.Sierpinski import Sierpinski
from fractals.ArbolRecursivo import ArbolRecursivo
from fractals.Julia import Julia
from fractals.Mandelbrot import Mandelbrot


pygame.init()
# Configuración de la ventana
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Fractales Interactivos")
koch = CurvaKoch()
SierpinskiF = Sierpinski()
arbol = ArbolRecursivo()
nameScreen = "Curva de Koch"
ruta_carpeta = os.path.join(os.path.dirname(__file__),"..", "capturas")
ruta_carpeta = os.path.abspath(ruta_carpeta)
boton_rect = pygame.Rect(300, 500, 200, 50)  # x, y, ancho, alto

# Crear instancias de Mandelbrot y Julia
mandelbrot = Mandelbrot(width=800, height=600)
julia = Julia(width=800, height=600)

angle = 0
scale = 100
pan_x = size[0] // 2
pan_y = size[1] // 2
step_angle = pi / 60
step_zoom = 10
step_pan = 5
iter = 1
resize = False
BLANCO = (255, 255, 255)
AZUL = (0, 102, 204)
AZUL_OSCURO = (0, 76, 153)
NEGRO = (0, 0, 0)
mostrar_boton = True
# Fuente
fuente = pygame.font.SysFont(None, 36)
# Leer modo_fractal desde argumentos si se pasa
if len(sys.argv) > 1:
    try:
        modo_fractal = int(sys.argv[1])
    except Exception:
        modo_fractal = 1
else:
    modo_fractal = 1

def manejar_transformaciones_seguidas():
    global angle, scale, pan_x, pan_y, step_angle, step_zoom, step_pan, iter, resize
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        scale += step_zoom
    if keys[pygame.K_DOWN]:
        scale = max(10, scale - step_zoom)  # Mínimo más alto para fractales complejos
    if keys[pygame.K_LEFT]:
        angle -= step_angle
    if keys[pygame.K_RIGHT]:
        angle += step_angle
    if keys[pygame.K_w]:
        pan_y -= step_pan
    if keys[pygame.K_s]:
        pan_y += step_pan
    if keys[pygame.K_a]:
        pan_x -= step_pan
    if keys[pygame.K_d]:
        pan_x += step_pan   
            
def manejar_eventos_teclado(event):
    global iter, modo_fractal, screen , nameScreen
    if event.key == pygame.K_e:
        iter = min(10, iter + 1)  # Limitar iteraciones máximas para rendimiento
    elif event.key == pygame.K_q:
        iter = max(1, iter - 1)
    elif event.key == pygame.K_1:
        modo_fractal = 1
    elif event.key == pygame.K_2:
        modo_fractal = 2
    elif event.key == pygame.K_3:
        modo_fractal = 3
<<<<<<< HEAD
    elif event.key == pygame.K_4:
        modo_fractal = 4
    elif event.key == pygame.K_5:
        modo_fractal = 5
=======

def guardar_captura():
    global nameScreen, ruta_carpeta
    nombre_archivo = datetime.now().strftime(nameScreen + "_%Y%m%d_%H%M%S.png")
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
    pygame.image.save(screen, ruta_completa)
    print(f"Captura guardada en: {ruta_completa}")



>>>>>>> 5ddb2e93bb99f81c9a79267e22e251ebde3590cd

def dibujar_sierpinski(screen, sierpinski, scale, angle, pan_x, pan_y, iter):
    segmentos = sierpinski.SierpinskiSegments(scale, angle, pan_x, pan_y, iter)
    for triangulos in segmentos:
        pygame.draw.polygon(screen, (255, 255, 255), triangulos, 1)

def dibujar_koch(screen, koch, scale, angle, pan_x, pan_y, iter):
    segmentos = koch.copoVonKoch(scale, angle, pan_x, pan_y, iter)
    for start, end in segmentos:
        pygame.draw.line(screen, (255, 255, 255), start, end)

def dibujar_arbol(screen, arbol, scale, angle, pan_x, pan_y, iter):
    # El árbol crece hacia arriba desde el centro inferior
    segmentos = arbol.generar_arbol(pan_x, pan_y + scale//2, 90 + angle * 180/pi, scale, iter+2)
    for start, end in segmentos:
        pygame.draw.line(screen, (0, 255, 0), start, end, 1)

<<<<<<< HEAD
def mostrar_info_fractal(screen, modo_fractal, iter, scale, angle):
    """Muestra información del fractal actual en pantalla"""
    font = pygame.font.SysFont("Arial", 20)
    nombres = ["", "Copo de Koch", "Triángulo de Sierpinski", "Árbol Recursivo", 
               "Conjunto de Mandelbrot", "Conjunto de Julia"]
    
    info_lines = [
        f"Fractal: {nombres[modo_fractal]}",
        f"Iteraciones: {iter}",
        f"Escala: {int(scale)}",
        f"Ángulo: {int(angle * 180/pi)}°"
    ]
    
    for i, line in enumerate(info_lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 25))
=======
import pygame

def crear_boton(screen, rect, texto, color_fondo, color_texto):
    # Dibujar el fondo del botón
    pygame.draw.rect(screen, color_fondo, rect)
    fuente = pygame.font.SysFont(None, 24)
    texto_renderizado = fuente.render(texto, True, color_texto)
    texto_rect = texto_renderizado.get_rect(center=rect.center)
    screen.blit(texto_renderizado, texto_rect)

>>>>>>> 5ddb2e93bb99f81c9a79267e22e251ebde3590cd

# Mantiene la ventana abierta hasta que la cierres
running = True
clock = pygame.time.Clock()
print("Controles:")
print("Flechas: Escalar (↑↓) y Rotar (←→)")
print("WASD: Mover")
print("Q/E: Cambiar iteraciones")
print("1-5: Cambiar fractal")
print("ESC: Salir")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
<<<<<<< HEAD
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                manejar_eventos_teclado(event)
=======
            manejar_eventos_teclado(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(event.pos):
                guardar_captura()
>>>>>>> 5ddb2e93bb99f81c9a79267e22e251ebde3590cd
    
    manejar_transformaciones_seguidas()
    screen.fill((0, 0, 0))
    
    if modo_fractal == 1:
        nameScreen = "curva de Koch"
        dibujar_koch(screen, koch, scale, angle, pan_x, pan_y, iter)
    elif modo_fractal == 2:
        nameScreen = "sierpinski"
        dibujar_sierpinski(screen, SierpinskiF, scale, angle, pan_x, pan_y, iter)
    elif modo_fractal == 3:
        nameScreen = "Arbol Recursivo"
        dibujar_arbol(screen, arbol, scale, angle, pan_x, pan_y, iter)
<<<<<<< HEAD
    elif modo_fractal == 4:
        mandelbrot.dibujar(screen, scale, angle, pan_x, pan_y, iter)
    elif modo_fractal == 5:
        julia.dibujar(screen, scale, angle, pan_x, pan_y, iter)
    
    # Mostrar información del fractal
    mostrar_info_fractal(screen, modo_fractal, iter, scale, angle)
=======
    crear_boton(screen, boton_rect, "Captura", AZUL, BLANCO)   
>>>>>>> 5ddb2e93bb99f81c9a79267e22e251ebde3590cd
    

    pygame.display.flip()
    
    # Reducir FPS para fractales complejos
    if modo_fractal in [4, 5]:
        clock.tick(10)  # 10 FPS para Mandelbrot y Julia
    else:
        clock.tick(50)  # 50 FPS para fractales geométricos

pygame.quit()