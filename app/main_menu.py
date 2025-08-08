import pygame
from pygame.locals import *

WIDTH, HEIGHT = 1280, 820

CONTROLS = [
    "Controles:",
    "Flechas: Rotar/Escalar (arriba/abajo: zoom, izq/der: rotar)",
    "W/S/A/D: Trasladar (arriba/abajo/izq/der)",
    "Q/E: Disminuir/Aumentar iteración",
    "1, 2, 3: Selección rápida",
    "ENTER: Abrir fractal seleccionado",
    "ESC: Salir"
]

import sys
import subprocess

class MenuPrincipal:
    def draw_gradient(self, color_top, color_bottom):
        """Dibuja un fondo con gradiente vertical"""
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fractales Interactivos - Menú Principal")
        self.font = pygame.font.SysFont("Segoe UI", 38, bold=True)
        self.fractal_font = pygame.font.SysFont("Segoe UI", 32)
        # Usar una fuente más atractiva para los controles
        available_fonts = [f.lower() for f in pygame.font.get_fonts()]
        if "montserrat" in available_fonts:
            self.control_font = pygame.font.SysFont("Montserrat", 27)
        elif "arialroundedmtbold" in available_fonts:
            self.control_font = pygame.font.SysFont("Arial Rounded MT Bold", 27)
        else:
            self.control_font = pygame.font.SysFont("Arial", 27)
        self.title_font = pygame.font.SysFont("Segoe UI", 54, bold=True)
        self.running = True
        self.fractales = ["Copo de Koch", "Triángulo de Sierpinski", "Árbol Recursivo"]
        self.selected = 0
    def draw_menu(self):
        # Fondo con gradiente
        self.draw_gradient((25, 40, 80), (10, 10, 30))

        # Título
        title = self.title_font.render("Fractales Interactivos", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        fractal_col_x = 80
        fractal_col_width = 500
        boton_espaciado = 80
        espacio_extra = 100  # antes 40
        y_offset = 170 + espacio_extra

        # Subtítulo alineado a la izquierda sobre los botones
        subtitle = self.font.render("Selecciona un fractal:", True, (200, 220, 255))
        self.screen.blit(subtitle, (fractal_col_x, y_offset - 70))

        icon_size = 38
        icon_gap = 24
        list_item_height = 56
        for i, nombre in enumerate(self.fractales):
            y = y_offset + i * (list_item_height + 8)
            # Ícono a la izquierda
            icon_x = fractal_col_x
            icon_y = y + list_item_height//2
            if i == 0:
                # Copo de Koch: círculo azul
                pygame.draw.circle(self.screen, (80, 160, 255), (icon_x + icon_size//2, icon_y), icon_size//2)
            elif i == 1:
                # Sierpinski: triángulo verde
                points = [
                    (icon_x + icon_size//2, icon_y - icon_size//2),
                    (icon_x, icon_y + icon_size//2),
                    (icon_x + icon_size, icon_y + icon_size//2)
                ]
                pygame.draw.polygon(self.screen, (80, 220, 120), points)
            elif i == 2:
                # Árbol: rectángulo marrón y círculo verde
                trunk = pygame.Rect(icon_x + icon_size//2 - 5, icon_y + 6, 10, 18)
                pygame.draw.rect(self.screen, (120, 80, 40), trunk)
                pygame.draw.circle(self.screen, (60, 180, 60), (icon_x + icon_size//2, icon_y), icon_size//2 - 6)

            # Texto del fractal
            color = (60, 180, 255) if i == self.selected else (40, 40, 60)
            text = self.fractal_font.render(f"{i+1}. {nombre}", True, color)
            tx = icon_x + icon_size + icon_gap
            ty = y + list_item_height//2 - text.get_height()//2
            self.screen.blit(text, (tx, ty))

        # Mantener controles a la misma altura que los botones
        controls_rect = pygame.Rect(WIDTH - 520, y_offset - 80, 440, 400)
        pygame.draw.rect(self.screen, (35, 60, 120), controls_rect, border_radius=22)
        pygame.draw.rect(self.screen, (120, 180, 255), controls_rect, 4, border_radius=22)

        # --- Controles alineados en filas ---
        key_font = pygame.font.SysFont("Segoe UI", 18, bold=True)
        arrow_font = pygame.font.SysFont("Segoe UI Symbol", 18, bold=True)
        available_fonts = [f.lower() for f in pygame.font.get_fonts()]
        control_text_font = pygame.font.SysFont("Montserrat", 18) if "montserrat" in available_fonts else pygame.font.SysFont("Arial", 18)

        controles_info = [
            # (icono, tipo, texto)
            ("↑/↓", "flecha_dual", "Escalar (arriba/abajo: zoom)"),
            ("←/→", "flecha_dual", "Rotar (izq/der: rotar)"),
            (["W", "A", "S", "D"], "teclas_wasd", "Trasladar (arriba/abajo/izq/der)"),
            ("Q", "tecla", "Disminuir iteración"),
            ("E", "tecla", "Aumentar iteración"),
            ("ENTER", "tecla_larga", "Abrir fractal seleccionado"),
            ("ESC", "tecla_larga", "Salir"),
        ]
        # Título 'Controles' dentro del recuadro
        controles_title = self.font.render("Controles", True, (255, 255, 180))
        self.screen.blit(controles_title, (controls_rect.x + 30, controls_rect.y + 18))
        espacio_titulo = 18  # espacio extra debajo del título

        # --- Sección de explicación de fractales ---
        explicaciones = [
            "Curva fractal que genera un copo de nieve a partir de subdivisiones recursivas.",
            "Triángulo subdividido recursivamente, creando un patrón de huecos en forma de triángulo.",
            "Árbol generado por ramas que se bifurcan recursivamente, simulando el crecimiento natural."
        ]
        exp_rect = pygame.Rect(80, y_offset + 3 * (list_item_height + 8) + 160, WIDTH - 160, 110)
        pygame.draw.rect(self.screen, (30, 38, 60), exp_rect, border_radius=18)
        pygame.draw.rect(self.screen, (120, 180, 255), exp_rect, 3, border_radius=18)
        exp_title_font = pygame.font.SysFont("Segoe UI", 26, bold=True)
        exp_text_font = pygame.font.SysFont("Segoe UI", 20)
        exp_title = exp_title_font.render("¿Qué hace este fractal?", True, (255, 255, 200))
        self.screen.blit(exp_title, (exp_rect.x + 24, exp_rect.y + 16))
        exp_text = explicaciones[self.selected]
        exp_text_render = exp_text_font.render(exp_text, True, (220, 230, 255))
        self.screen.blit(exp_text_render, (exp_rect.x + 24, exp_rect.y + 56))
        y = controls_rect.y + 60 + espacio_titulo
        for icono, tipo, texto in controles_info:
                if tipo == "flecha_dual":
                    # Dibuja dos flechas en una sola celda
                    rect = pygame.Rect(controls_rect.x + 30, y, 48, 28)
                    pygame.draw.rect(self.screen, (255, 255, 220), rect, border_radius=6)
                    pygame.draw.rect(self.screen, (180, 180, 80), rect, 2, border_radius=6)
                    if icono == "↑/↓":
                        self.screen.blit(arrow_font.render("↑", True, (80, 80, 40)), (rect.x+5, rect.y+1))
                        self.screen.blit(arrow_font.render("↓", True, (80, 80, 40)), (rect.x+25, rect.y+1))
                    else:
                        self.screen.blit(arrow_font.render("←", True, (80, 80, 40)), (rect.x+5, rect.y+1))
                        self.screen.blit(arrow_font.render("→", True, (80, 80, 40)), (rect.x+25, rect.y+1))
                    # Mostrar el texto a la derecha del icono
                    txt = control_text_font.render(texto, True, (220, 240, 255))
                    self.screen.blit(txt, (rect.right + 16, rect.y + rect.height//2 - txt.get_height()//2))
                    y += 40
                    continue
                if tipo == "teclas_wasd":
                    # Dibuja las 4 teclas W, A, S, D en línea
                    rects = []
                    x0 = controls_rect.x + 30
                    for i, letra in enumerate(icono):
                        rx = x0 + i*32
                        rect = pygame.Rect(rx, y, 28, 28)
                        rects.append(rect)
                        pygame.draw.rect(self.screen, (220, 230, 255), rect, border_radius=6)
                        pygame.draw.rect(self.screen, (80, 120, 200), rect, 2, border_radius=6)
                        self.screen.blit(key_font.render(letra, True, (40, 60, 120)), (rect.x+6, rect.y+2))
                    last_rect = rects[-1]
                    txt = control_text_font.render(texto, True, (220, 240, 255))
                    self.screen.blit(txt, (last_rect.right + 16, last_rect.y + last_rect.height//2 - txt.get_height()//2))
                    y += 40
                    continue
                if tipo == "tecla":
                    rect = pygame.Rect(controls_rect.x + 30, y, 28, 28)
                    pygame.draw.rect(self.screen, (220, 230, 255), rect, border_radius=6)
                    pygame.draw.rect(self.screen, (80, 120, 200), rect, 2, border_radius=6)
                    self.screen.blit(key_font.render(icono, True, (40, 60, 120)), (rect.x+6, rect.y+2))
                    txt = control_text_font.render(texto, True, (220, 240, 255))
                    self.screen.blit(txt, (rect.right + 16, rect.y + rect.height//2 - txt.get_height()//2))
                    y += 40
                    continue
                if tipo == "tecla_larga":
                    rect = pygame.Rect(controls_rect.x + 30, y, 60, 28)
                    color = (220, 255, 220) if icono == "ENTER" else (255, 220, 220)
                    border = (80, 180, 80) if icono == "ENTER" else (180, 80, 80)
                    text_color = (40, 80, 40) if icono == "ENTER" else (120, 40, 40)
                    pygame.draw.rect(self.screen, color, rect, border_radius=6)
                    pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)
                    if icono == "ENTER":
                        enter_font = pygame.font.SysFont("Segoe UI", 15, bold=True)
                        enter_text = enter_font.render("ENTER", True, text_color)
                        self.screen.blit(enter_text, (rect.x + (rect.width - enter_text.get_width())//2, rect.y + (rect.height - enter_text.get_height())//2))
                    else:
                        self.screen.blit(key_font.render(icono, True, text_color), (rect.x+8, rect.y+2))
                    txt = control_text_font.render(texto, True, (220, 240, 255))
                    self.screen.blit(txt, (rect.right + 16, rect.y + rect.height//2 - txt.get_height()//2))
                    y += 40
                    continue


        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.fractales)
                    elif event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.fractales)
                    elif event.key in (K_1, K_2, K_3):
                        # Ejecutar la visualización del fractal seleccionado por número
                        pass
                    

if __name__ == "__main__":
    menu = MenuPrincipal()
    clock = pygame.time.Clock()
    while menu.running:
        menu.draw_menu()
        for event in pygame.event.get():
            if event.type == QUIT:
                menu.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu.running = False
                elif event.key == K_DOWN:
                    menu.selected = (menu.selected + 1) % len(menu.fractales)
                elif event.key == K_UP:
                    menu.selected = (menu.selected - 1) % len(menu.fractales)
                elif event.key == K_RETURN:
                    # Abrir el fractal seleccionado
                    fractal_num = menu.selected + 1
                    import os
                    script_path = os.path.join(os.path.dirname(__file__), "gui", "controls.py")
                    subprocess.Popen([sys.executable, script_path, str(fractal_num)])
                elif event.key in (K_1, K_2, K_3):
                    pass
        clock.tick(60)
