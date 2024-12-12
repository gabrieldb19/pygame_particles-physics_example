import pygame as pg
import math


class Particle:
    """ Clase de implementacion de Particula para el entorno en PyGame.
    """
    def __init__(self,
                env,
                pos: pg.math.Vector2,
                v: float = 0.0, # En pixel/s
                direction: float = 0.0, # Direccion en grados
                rad: float = None, # Direccion en radianes
                mass: float = 1.0,
                restitution: float = 1.0, # Mantencion de vel al rebotar en %
                size: float = 1.0, # Pixeles
                color: pg.Color = pg.Color(255,255,255)
                ) -> None:
        
        self.enviroment = env
        self.position = pos
        self.size = size
        self.color = color
        self.direction = direction
        self.radians = rad
        theta = math.radians(direction) if not rad else rad
        self.vx = v * math.cos(theta)
        self.vy = -v * math.sin(theta)
        self.mass = mass
        self.restitution = restitution
    
    def move(self) -> None:
        """ Calcula el movimiento de la particula.
        """
        try:
            k = self.enviroment.k.get()
        except: k = 0
        try:
            g = self.enviroment.gravity.get()
        except: g = 0
        
        self.forcex = -k * self.vx
        self.forcey = self.mass * g - k * self.vy
        # Actualizar la velocidad con la que se desplaza.
        self.vx = self.vx + (self.forcex / self.mass) * self.enviroment.deltatime
        self.vy = self.vy + (self.forcey / self.mass) * self.enviroment.deltatime
        # Actualizar la posicion.
        self.position = pg.math.Vector2(
                    x= self.position.x + self.vx * self.enviroment.deltatime,
                    y= self.position.y + self.vy * self.enviroment.deltatime
                )

    def draw(self) -> None:
        """ Dibuja la particula en el entorno.
        """
        pg.draw.circle(
                self.enviroment.display, 
                self.color, 
                (int(self.position.x), int(self.position.y)), 
                self.size
                )