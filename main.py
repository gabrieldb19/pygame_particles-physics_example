from gui import UI
from enviroment import Enviroment
from particle import Particle
import pygame as pg
import math
from tkinter import colorchooser
from tkinter.ttk import Label


class Main:
    """ Clase Main que integra la UI con el Enviroment y configura las funcionalidades de la UI.
    """
    def __init__(self) -> None:
        self.active = False
        self.is_paused = False
        self.main = UI()
        self.env = Enviroment(768,768)

        self.env.draw_c = self.main.show_center
        self.env.direction_line = self.main.direction_line
        self.env.gravity = self.main.var_g
        self.env.k = self.main.var_airres
        self.main.inspector.b_color.configure(command=lambda label=self.main.inspector.l_color: self.open_color_dialog(label))

        self.main.b_start_simulation.configure(command=self.start_stop_simulation)
        self.main.b_reset_simulation.configure(command=self.reset_instances)

        self.main.protocol("WM_DELETE_WINDOW", self.on_close)


    def init(self):
        """ Inicia el bucle de la interfaz y el enviroment.
        """
        self.active = True
        self.env.init()
        self.loop()


    def loop(self):
        """ Bucle de la interfaz.

            Captura eventos de click y cierre. Actualiza el enviroment e interfaz.
        """
        while self.active:
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        pg.quit()
                        exit()
                    # -*****- Spawn de particulas -*****-
                    case pg.MOUSEBUTTONDOWN:
                        self.env.mouse_init_pos = pg.mouse.get_pos()
                    case pg.MOUSEBUTTONUP:
                        dx =  self.env.mouse_init_pos[0] - self.env.mouse_end_pos[0]
                        dy =  -(self.env.mouse_init_pos[1] - self.env.mouse_end_pos[1])
                        self.add_particle(pos=self.env.mouse_init_pos, rad=math.atan2(dy,dx))
                    # -*****- Spawn de particulas -*****-
            if self.env.active:
                self.env.update()
                self.main.var_fps.set(round(self.env.clock.get_fps(), 2)) # Refresh fps counter
            self.main.update()


    def start_stop_simulation(self):
        """ Funcion de start/stop para el boton de pausa.
        """
        t = self.main.var_start_stop.get()
        match t:
            case 'Start':
                self.env.active = True
                self.env.reset_deltatime()
                self.main.var_start_stop.set('Stop')
            case 'Stop':
                self.env.active = False
                self.main.var_start_stop.set('Start')


    def reset_instances(self):
        """ Limpia la lista de instancias y refresca la pantalla.
        """
        self.env.clear_instances()
        self.env.refresh()


    def on_close(self):
        """ Funcion para el cierre de ventana.
        """
        self.active = False
        self.main.destroy()


    def add_particle(self, pos, rad):
        """ Agrega una particula a la lista de instancias en el enviroment.

        Args:
            pos (tuple): Posicion de la particula a instanciar.
            rad (float): Direccion de la particula en radianes.
        """
        values = self.main.inspector.get_inputs()

        self.env.instantiate(Particle(
                    env= self.env,
                    pos= self.env.center if not pos else pg.math.Vector2(pos[0],pos[1]),
                    v= self.env.mouse_distance() * 2, # Multiplico la distancia para que tenga mas velocidad
                    rad= rad,
                    size= values[0], 
                    color= self.main.color_selected,
                    mass= values[1],
                    restitution= values[2])
                    )
        self.env.refresh()

    def open_color_dialog(self, label: Label):
        """ Abre una ventana para seleccionar un color para la particula.

        Args:
            label (Label): Label donde se muestra el color seleccionado.
        """
        self.env.active = False
        rgb, color = colorchooser.askcolor()
        if rgb:
            self.main.color_selected = rgb
            label.configure(background=color)

        self.env.active = True
        self.env.reset_deltatime()