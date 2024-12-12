import math
import pygame as pg
from tkinter import BooleanVar
from particle import Particle
from physics import *


class Enviroment:
    """ Entorno de PyGame para la simulacion.
    """
    def __init__(self, width: int, height: int, fps_limit: float = 60.0) -> None:
        self.active: bool = False
        self.draw_c: BooleanVar # Boolean para saber si hay que dibujar el centro
        self.direction_line: BooleanVar # Boolean para saber si hay que dibujar linea de trayectoria
        self.gravity: float
        self.k: float # Constante de Friccion/Resistencia del aire
        self.width = width
        self.height = height
        self.center = pg.math.Vector2(self.width//2, self.height//2)
        self.fps: float = fps_limit
        self.deltatime = 0.0
        self.last_time = 0.0
        self.clock = pg.time.Clock()

        self.mouse_init_pos = (0,0)
        self.mouse_end_pos = (0,0)

        self.instances = []

    def init(self) -> None:
        """ Inicia el enviroment.
        """
        pg.display.init()
        self.display = pg.display.set_mode(size=(self.width, self.height))
        self.active = True
        self.refresh()

    def update(self) -> None:
        """ Actualiza las instancias en el entorno, el deltatime y clock.
        """
        self.calculate_deltatime()
        
        for i, obj1 in enumerate(self.instances):
            for obj2 in self.instances[i+1:]:
                if check_collision(obj1, obj2):
                    resolve_collision(obj1, obj2)
        
        for obj in self.instances:
            bounds_collision(obj, self.width, self.height)
        
        for obj in self.instances:
            obj.move()
        
        self.clock.tick(self.fps)
        self.refresh()
    
    def refresh(self) -> None:
        """Actualizar la pantalla
        """
        self.display.fill(color=(0,0,0))

        if self.draw_c.get():
            self.draw_center()
        if pg.mouse.get_pressed()[0] and self.direction_line.get():
            self.draw_direction_line()
        
        for obj in self.instances:
            obj.draw()

        pg.display.update()
    
    def clear_instances(self) -> None:
        """ Limpia la lista de instancias.
        """
        self.instances.clear()

    def calculate_deltatime(self) -> None:
        """ Almacena el deltatime en 'self.deltatime' y el anterior deltatime en 'self.last_time'.
        """
        current_time = pg.time.get_ticks() / 1000.0
        self.deltatime = current_time - self.last_time
        self.last_time = current_time
    
    def reset_deltatime(self) -> None:
        """ Resetea el deltatime para evitar errores de calculo en pausas.
        """
        self.last_time = pg.time.get_ticks() / 1000.0

    def instantiate(self, obj: Particle) -> None:
        """ Agrega una particula a la lista de instancias.

        Args:
            obj (Particle): Particula a instanciar.
        """
        self.instances.append(obj)
    
    def mouse_distance(self) -> float:
        """ Calcula la distancia entre la posicion inicial del mouse(mouse down) y la final(mouse up).

        Returns:
            float: Distancia.
        """
        return math.sqrt((self.mouse_init_pos[0] - self.mouse_end_pos[0])**2 + (self.mouse_init_pos[1] - self.mouse_end_pos[1])**2)

    def draw_center(self) -> None:
        """ Dibuja una cruz en el centro del entorno.
        """
        pg.draw.line(surface=self.display,
                    color=pg.Color(255,255,255),
                    start_pos=(self.center.x - 5, self.center.y),
                    end_pos=(self.center.x + 5, self.center.y)
                    )
        pg.draw.line(surface=self.display,
                    color=pg.Color(255,255,255),
                    start_pos=(self.center.x, self.center.y - 5),
                    end_pos=(self.center.x, self.center.y + 5)
                    )
        pg.draw.circle(surface=self.display,
                    color=pg.Color(0,0,0),
                    center=(self.center.x, self.center.y),
                    radius=1
                    )
    
    def draw_direction_line(self) -> None:
        """ Dibuja una linea usando las posiciones del mouse inicial y final.
        """
        self.mouse_end_pos = pg.mouse.get_pos()
        pg.draw.line(surface=self.display,
                        color=(255,255,255),
                        start_pos=self.mouse_init_pos,
                        end_pos=self.mouse_end_pos,
                        width=2
                        )