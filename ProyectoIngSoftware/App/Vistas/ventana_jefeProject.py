import customtkinter as ctk
from PIL import Image
import BaseDeDatos.UsersMongoDB as db


#creamos la clase ventana para el jefe de proyecto
class JP(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.n_proyectos = 1 
        self.proyecto_id = 111
        self.geometry("800x540")
        self.title("PaltaEstimateApp")
        #self.resizable(False, False)
        self.Paneles()
        self.controles_sidebar()
        self.contenido_body()
        #self.contenido_top_panel()
        self.contenido_subpanel()
        self.contenido_image()

        

        self.mainloop() 
    
    def Paneles(self):#FRAMES
        #sección izquierda
        self.side_bar = ctk.CTkFrame(self, fg_color="blue", width=200, corner_radius=0)
        self.side_bar.pack(side="left", fill="y", expand=False)
        #cuerpo principal
        self.body = ctk.CTkFrame(self, fg_color="black", corner_radius=0)
        self.body.pack(side="right", fill="both", expand=True)
        #frame que contiene ID del proyecto actual
        self.top_subpanel = ctk.CTkFrame(self.body, fg_color="transparent", height=120, corner_radius=0)
        self.top_subpanel.pack(side=ctk.TOP, fill="x", expand=False)
        #frame para la imágen
        self.topimage = ctk.CTkFrame(self.top_subpanel, fg_color="transparent", corner_radius=0)
        self.topimage.pack(side=ctk.RIGHT, expand=False)

    def controles_sidebar(self):
        texto= "PRO-"+str(self.proyecto_id)
        self.mis_proyectos = ctk.CTkLabel(self.side_bar, text="Mis Proyectos", font=("Comic Sans", -20), fg_color="black")
        self.mis_proyectos.pack(side=ctk.TOP, pady=5, fill="both")
        self.boton_proyecto = ctk.CTkButton(self.side_bar, text=texto, fg_color="orange",font=("Arial", -20),
                                            width=200, height=65, corner_radius=0, command=lambda: self.boton_clickeado_global(texto))
        self.boton_proyecto.pack(side=ctk.TOP, pady=10)

        self.boton_nuevo_proyecto = ctk.CTkButton(self.side_bar, text="Crear Proyecto +", font=("Comic Sans", -20),
                                                fg_color="red", width=200, height=65, corner_radius=0, command= self.crear_proyecto)
        self.boton_nuevo_proyecto.pack(side=ctk.BOTTOM, pady=10)

    def contenido_body(self):
        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.body, height=400)
        tabview.pack(padx=5, pady=5, fill="x")
        #Agregamos Tabs
        tab1 = tabview.add("Integrantes")  
        tab2 = tabview.add("Requerimientos")  
        tab3 = tabview.add("Métricas")  
        
        ##Objetos de tab1
        button = ctk.CTkButton(master=tab1)#Para colocar elementos, solo se especifica el tab
        button.pack(side=ctk.BOTTOM, padx=20, pady=20)

        ##Objetos de tab2
        scroll = ctk.CTkScrollableFrame(master=tab2)
        scroll.pack(fill="both",expand=True)
        texto = ctk.CTkLabel(master=scroll, font=("Calibri", -15, "italic"), text="· REQ-111: ")
        texto.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)
        
        
        ##Objetos de tab3

        ##objetos del body
        self.eliminar_proyecto = ctk.CTkButton(self.body, text="Eliminar Proyecto", fg_color="Red", font=("Comic Sans", -15),
                                        width=150, height=35, corner_radius=25)
        self.eliminar_proyecto.pack(side=ctk.RIGHT, anchor=ctk.SW, pady=5, padx=5)

        self.administrar  = ctk.CTkButton(self.body, text="Administración\nCompleta", text_color="black",fg_color="white", font=("Comic Sans", -15, "bold"),
                                        width=150, height=35, corner_radius=25)
        self.administrar.pack(side=ctk.LEFT, anchor=ctk.SE, pady=5, padx=5)

    def contenido_subpanel(self):
        texto_boton = self.boton_proyecto.cget("text")#se obtiene la info del proyecto seleccionado, para mostrar en la ventana
        self.proyecto_actual = ctk.CTkLabel(self.top_subpanel, text=texto_boton, font=("Comic Sans", -25))
        self.proyecto_actual.pack(side=ctk.TOP)

    def contenido_image(self):
        self.logo = ctk.CTkImage(light_image=Image.open("E:\Repositorios GitHub\IngDeSoft\ProyectoIngSoftware\App\Vistas\LOGO.png"),
                    size=(60, 60))
        self.logo_label = ctk.CTkLabel(self.topimage, image=self.logo, text="")
        self.logo_label.pack(padx=5, pady=5)

    def crear_proyecto(self):
        self.n_proyectos += 1
        if self.n_proyectos > 3:
            self.mostrar_ventana_emergente()
        else:
            self.proyecto_id += 1
            texto = "PRO-" + str(self.proyecto_id)
            self.new_proyect = ctk.CTkButton(self.side_bar, text=texto, fg_color="orange",font=("Arial", -20),
                                                width=200, height=65, corner_radius=0, command=lambda: self.boton_clickeado_global(texto))
            self.new_proyect.pack(side=ctk.TOP, pady=10)

    def cambiar_proyecto(self, texto):
        switch_project = self.proyecto_actual.configure(text=texto)

    def boton_clickeado(self, texto):
        self.cambiar_proyecto(texto)

    def boton_clickeado_global(self, texto):
        self.boton_clickeado(texto)

    def mostrar_ventana_emergente(self):
        ventana_emergente = ctk.CTkToplevel(JP)
        ventana_emergente.configure(fg_color="white")
        etiqueta = ctk.CTkLabel(ventana_emergente, font=("Arial", -15, "bold"), text_color="black",
                                text="Error: No se puede crear otro proyecto.\n\nMotivo: Límite de proyectos activos alcanzado.")
        etiqueta.pack(padx=20, pady=20)
        # Centra la ventana emergente con respecto a la ventana principal
        ancho_ventana_principal = JP.winfo_width()
        alto_ventana_principal = JP.winfo_height()
        x_ventana_emergente = JP.winfo_rootx() + ancho_ventana_principal // 2 - ventana_emergente.winfo_reqwidth() // 2
        y_ventana_emergente = JP.winfo_rooty() + alto_ventana_principal // 2 - ventana_emergente.winfo_reqheight() // 2
        ventana_emergente.geometry("+{}+{}".format(x_ventana_emergente, y_ventana_emergente))
        ventana_emergente.title("Error")
        ventana_emergente.attributes('-topmost' , 1)
        ventana_emergente.focus()

