import os, platform
from tkinter import Tk, Frame, BooleanVar, StringVar, DoubleVar
from tkinter.ttk import Label, Button, Entry, Checkbutton, Separator


class UI(Tk):
    """ Interfaz tkinter para manejar los parametros del entorno.

    Args:
        Tk (_type_): Tk :V
    """
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title('Projectile Test')
        self.resizable(0,0)
        self.color_selected = (255,255,255)

        #---------- Frame Top ----------#
        self.frame_topWidgets = Frame(master=self)

        #---------- Widgets ----------#
        self.var_fps = StringVar()
        self.l_fps = Label(master=self.frame_topWidgets, textvariable=self.var_fps)
        self.var_start_stop = StringVar(value='Stop')
        self.b_start_simulation = Button(
                            master=self.frame_topWidgets,
                            textvariable=self.var_start_stop
                            )
        self.b_reset_simulation = Button(
                            master=self.frame_topWidgets,
                            text='Reset simulation'
                            )
        self.direction_line = BooleanVar(value=True)
        self.show_center = BooleanVar()
        self.rb_show_center = Checkbutton(master=self.frame_topWidgets, 
                                    text='Draw center', 
                                    variable=self.show_center
                                    )
        

        #---------- Empaquetado ----------#
        self.frame_topWidgets.grid(row=0, column=0, columnspan=2)

        self.l_fps.pack(side='left')
        self.b_start_simulation.pack(side='left')
        self.b_reset_simulation.pack(side='left')
        self.rb_show_center.pack(side='left')
        

        #---------- Frame Right Enviroment ----------#
        self.frame_rEnviroment = Frame(master=self)

        #---------- Widgets ----------#
        self.l_g = Label(master=self.frame_rEnviroment, text='Gravity:')
        self.l_airres = Label(master=self.frame_rEnviroment, text='Air resistance:')
        self.var_g = DoubleVar(value=980.0)
        self.var_airres = DoubleVar(value=0.2)
        self.e_g = Entry(master=self.frame_rEnviroment, textvariable=self.var_g)
        self.e_airres = Entry(master=self.frame_rEnviroment, textvariable=self.var_airres)
        

        #---------- Empaquetado ----------#
        self.frame_rEnviroment.grid(row=1, column=1)

        self.l_g.grid(row=0, column=0)
        self.l_airres.grid(row=1, column=0)
        self.e_g.grid(row=0, column=1)
        self.e_airres.grid(row=1, column=1)
        
        
        #********** Frame Right Enviroment **********#
        #---------- Separator ----------#
        self.sep = Separator(master=self, orient='horizontal')
        self.sep.grid(row=2, column=1, sticky='ew')
        

        #---------- Inspector Frame ----------#
        self.inspector = InspectorFrame(master=self)
        self.inspector.grid(row=2, column=1)
        

        #---------- Enviroment Frame ----------#
        self.frame_pygame = Frame(master=self, width=768, height=768)
        self.frame_pygame.grid(row=1, rowspan=3, column=0)

        os.environ['SDL_WINDOWID'] = str(self.frame_pygame.winfo_id())
        if platform.system() == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'


class InspectorFrame(Frame):
    """ Frame personalizado para el inspector con los parametros de la particula a instanciar.

    Args:
        Frame (_type_): Frame :V
    """
    def __init__(self, master = None):
        super().__init__(master)
        self.name = 'Projectile'

        #---------- Widgets ----------#
        self.l_size = Label(master=self, text='Size:')
        self.b_color = Button(master=self, text='Color')
        self.l_mass = Label(master=self, text='Mass:')
        self.l_res = Label(master=self, text='Restitution:')

        self.e_size = Entry(master=self)
        self.l_color = Label(master=self, background= '#ffffff', width=20)
        self.e_mass = Entry(master=self)
        self.e_res = Entry(master=self)
        

        #---------- Empaquetado ----------#
        self.l_size.grid(row=0, column=0)
        self.b_color.grid(row=1, column=0)
        self.l_mass.grid(row=2, column=0)
        self.l_res.grid(row=3, column=0)

        self.e_size.grid(row=0, column=1)
        self.l_color.grid(row=1, column=1)
        self.e_mass.grid(row=2, column=1)
        self.e_res.grid(row=3, column=1)
        
    
    def get_inputs(self) -> list:
        """Return inputs from entry

        Returns:
            list: [size, mass, restitution]
        """
        try:
            size = int(self.e_size.get())
        except: size = 1
        try:
            m = float(self.e_mass.get())
        except: m = 1.0
        try:
            res = float(self.e_res.get())
        except: res = 1.0

        return [size, m, res]