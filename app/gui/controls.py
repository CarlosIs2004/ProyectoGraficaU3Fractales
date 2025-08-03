import pygame
from pygame.locals import *
from math import  pi
from fractals.CurvaKoch import CurvaKoch
from fractals.Sierpinski import Sierpinski

pygame.init()
# Configuración de la ventana
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Fractales Interactivos")
koch = CurvaKoch()
Sierpinski = Sierpinski()

angle = 0
scale = 100
pan_x = size[0] // 2
pan_y = size[1] // 2
step_angle = pi / 60
step_zoom = 10
step_pan = 5
resize = False
iter = 1





def manejar_transformaciones():
    global resize, angle, scale, pan_x, pan_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        scale += step_zoom
        resize = True
    if keys[pygame.K_DOWN]:
        scale = max(0.1, scale - step_zoom)
        resize = True
    if keys[pygame.K_LEFT]:
        angle -= step_angle
        resize = True
    if keys[pygame.K_RIGHT]:
        angle += step_angle
        resize = True
    if keys[pygame.K_w]:
        pan_y -= step_pan
        resize = True
    if keys[pygame.K_s]:
        pan_y += step_pan
        resize = True
    if keys[pygame.K_a]:
        pan_x -= step_pan
        resize = True
    if keys[pygame.K_d]:
        pan_x += step_pan
        resize = True
        
            
    


def manejar_eventos():
    global running, iter, resize, angle, scale, pan_x, pan_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                screen.fill((0, 0, 0))
                dibujar_sierpinski(screen, Sierpinski, scale, angle, pan_x, pan_y, iter)
                pygame.display.flip()
            elif event.key == pygame.K_2:
                screen.fill((0, 0, 0))
                dibujar_koch(screen, koch, scale, angle, pan_x, pan_y, iter)
                pygame.display.flip()
            elif event.key == pygame.K_e:
                    iter += 1
                    resize = True
            elif event.key == pygame.K_q:
                    iter = max(1, iter - 1)
                    resize = True
            return True  



def dibujar_sierpinski(screen, Sierpinski, scale, angle, pan_x, pan_y, iter):
    segmentos = Sierpinski.SierpinskiSegments(scale, angle, pan_x, pan_y, iter)
    for triangulos in segmentos:
        pygame.draw.polygon(screen, (255, 255, 255), triangulos, 1)

def dibujar_koch(screen, koch, scale, angle, pan_x, pan_y, iter):
    segmentos = koch.copoVonKoch(scale, angle, pan_x, pan_y, iter)
    for start, end in segmentos:
        pygame.draw.line(screen, (255, 255, 255), start, end)

# Mantiene la ventana abierta hasta que la cierres
running = True
while running:
    running = manejar_eventos()
    if resize:
        manejar_transformaciones()
        resize = False
    pygame.time.Clock().tick(30)
pygame.quit()