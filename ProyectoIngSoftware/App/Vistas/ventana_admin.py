import customtkinter as ctk
from PIL import Image
import os
#import BaseDeDatos.UsersQuery as db


#creamos la clase ventana para el jefe de proyecto
class JP(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.n_proyectos = 1 
        self.proyecto_id = 111
        self.geometry("1280x720")
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
        self.side_bar = ctk.CTkFrame(self, fg_color="blue", width=200, corner_radius=25)
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
        self.mis_proyectos = ctk.CTkLabel(self.side_bar, text="Mis Proyectos", font=("Comic Sans", -20))
        self.mis_proyectos.pack(side=ctk.TOP, pady=5, fill="both")
        self.boton_proyecto = ctk.CTkButton(self.side_bar, text=texto, fg_color="orange",font=("Arial", -20),
                                            width=200, height=65, corner_radius=0, command=lambda: self.boton_clickeado_global(texto))
        self.boton_proyecto.pack(side=ctk.TOP, pady=10)

        self.boton_nuevo_proyecto = ctk.CTkButton(self.side_bar, text="Crear Proyecto +", font=("Comic Sans", -20),
                                                fg_color="red", width=200, height=65, corner_radius=0, command= self.crear_proyecto)
        self.boton_nuevo_proyecto.pack(side=ctk.BOTTOM, pady=10)

    def contenido_body(self):
        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.body, height=550)
        tabview.pack(padx=5, pady=5, fill="both")
        #Agregamos Tabs
        tab1 = tabview.add("Integrantes")  
        tab2 = tabview.add("Requerimientos")  
        tab3 = tabview.add("Métricas")  
        
        ##Objetos de tab1

        vcmd = (self.register(self.callback))

        frame1 = ctk.CTkFrame(master=tab1)
        frame1.pack(side=ctk.TOP)
        frame2 = ctk.CTkFrame(master=tab1)
        frame2.pack(side=ctk.TOP)
        frame3 = ctk.CTkFrame(master=tab1)
        frame3.pack(side=ctk.TOP)
        frame4 = ctk.CTkFrame(master=tab1)
        frame4.pack(side=ctk.TOP)
        frame5 = ctk.CTkFrame(master=tab1)
        frame5.pack(side=ctk.TOP)
        frame6 = ctk.CTkFrame(master=tab1)
        frame6.pack(side=ctk.TOP)
        frame7 = ctk.CTkFrame(master=tab1)
        frame7.pack(side=ctk.TOP)
        frame8 = ctk.CTkFrame(master=tab1)
        frame8.pack(side=ctk.TOP)
        frame9 = ctk.CTkFrame(master=tab1)
        frame9.pack(side=ctk.TOP)

        #FRAME1
        self.email_entry = ctk.CTkLabel(frame1, text="Tabla de puntos de función", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="dodger blue", width=600, corner_radius=4)
        self.email_entry.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)

        #FRAME2

        lblDificultad = ctk.CTkLabel(frame2, text="Dificultad", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblDificultad.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        lblBaja = ctk.CTkLabel(frame2, text="Baja", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblBaja.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        lblMedia = ctk.CTkLabel(frame2, text="Media", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblMedia.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        lblAlta = ctk.CTkLabel(frame2, text="Alta", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblAlta.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME3
        lblAtributos = ctk.CTkLabel(frame3, text="Atributos", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblAtributos.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent11 = ctk.CTkEntry(frame3, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent11.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent12 = ctk.CTkEntry(frame3, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent12.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent13 = ctk.CTkEntry(frame3, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent13.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME4
        lblEntEx = ctk.CTkLabel(frame4, text="Entrada Externa", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblEntEx.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent21 = ctk.CTkEntry(frame4, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent21.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent22 = ctk.CTkEntry(frame4, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent22.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent23 = ctk.CTkEntry(frame4, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent23.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME5
        lblSalEx = ctk.CTkLabel(frame5, text="Salida externa", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblSalEx.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent31 = ctk.CTkEntry(frame5, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent31.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent32 = ctk.CTkEntry(frame5, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent32.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent33 = ctk.CTkEntry(frame5, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent33.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME6
        lblConEx = ctk.CTkLabel(frame6, text="Consulta externa", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblConEx.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent41 = ctk.CTkEntry(frame6, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent41.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent42 = ctk.CTkEntry(frame6, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent42.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent43 = ctk.CTkEntry(frame6, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent43.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME7
        lblALI = ctk.CTkLabel(frame7, text="Archivo L. interno", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblALI.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent51 = ctk.CTkEntry(frame7, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent51.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent52 = ctk.CTkEntry(frame7, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent52.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent53 = ctk.CTkEntry(frame7, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent53.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME8
        lblALE = ctk.CTkLabel(frame8, text="Archivo L. externo", state=ctk.DISABLED, cursor="arrow", text_color="black", fg_color="deep sky blue", width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblALE.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent61 = ctk.CTkEntry(frame8, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent61.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent62 = ctk.CTkEntry(frame8, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent62.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent63 = ctk.CTkEntry(frame8, justify='center',validate='all', validatecommand=(vcmd, '%P'))#Para colocar elementos, solo se especifica el tab
        self.ent63.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME9
        btnATPF = ctk.CTkButton(frame9, text="Actualizar tabla", command=self.actualizarTablaPF)#Para colocar elementos, solo se especifica el tab
        btnATPF.pack(side=ctk.LEFT, anchor=ctk.NW, pady=20)




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

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def actualizarTablaPF(self):

    
        e11 = self.user_email = self.ent11.get() #Atributos para dificultad baja
        e12 = self.user_email = self.ent12.get() #Atributos para dificultad media
        e13 = self.user_email = self.ent13.get() #Atributos para dificultad alta

        #El resto son los PF de cada [Tipo de entrada,dificultad]

        e21 = self.user_email = self.ent21.get()
        e22 = self.user_email = self.ent22.get()
        e23 = self.user_email = self.ent23.get()
        
        e31 = self.user_email = self.ent31.get()
        e32 = self.user_email = self.ent32.get()
        e33 = self.user_email = self.ent33.get()
        
        e41 = self.user_email = self.ent41.get()
        e42 = self.user_email = self.ent42.get()
        e43 = self.user_email = self.ent43.get()
        
        e51 = self.user_email = self.ent51.get()
        e52 = self.user_email = self.ent52.get()
        e53 = self.user_email = self.ent53.get()
        
        e61 = self.user_email = self.ent61.get()
        e62 = self.user_email = self.ent62.get()
        e63 = self.user_email = self.ent63.get()

        e=[e11,e12,e13,e21,e22,e23,e31,e32,e33,e41,e42,e43,e51,e52,e53,e61,e62,e63]

        #db.actualizarTablaPF(e)



    def contenido_subpanel(self):
        texto_boton = self.boton_proyecto.cget("text")#se obtiene la info del proyecto seleccionado, para mostrar en la ventana
        self.proyecto_actual = ctk.CTkLabel(self.top_subpanel, text=texto_boton, font=("Comic Sans", -25))
        self.proyecto_actual.pack(side=ctk.TOP)

    def contenido_image(self):
        # Obtener la ruta absoluta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
        logo = ctk.CTkImage(light_image=Image.open(logo_path),
            size=(60, 60))
        logo_label = ctk.CTkLabel(self.topimage, image=logo, text="")
        logo_label.pack(padx=5, pady=5)

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
        ventana_emergente = ctk.CTkToplevel(self)
        ventana_emergente.configure(fg_color="white")
        etiqueta = ctk.CTkLabel(ventana_emergente, font=("Arial", -15, "bold"), text_color="black",
                                text="Error: No se puede crear otro proyecto.\n\nMotivo: Límite de proyectos activos alcanzado.")
        etiqueta.pack(padx=20, pady=20)
        # Centra la ventana emergente con respecto a la ventana principal
        ancho_ventana_principal = self.winfo_width()
        alto_ventana_principal = self.winfo_height()
        x_ventana_emergente = self.winfo_rootx() + ancho_ventana_principal // 2 - ventana_emergente.winfo_reqwidth() // 2
        y_ventana_emergente = self.winfo_rooty() + alto_ventana_principal // 2 - ventana_emergente.winfo_reqheight() // 2
        ventana_emergente.geometry("+{}+{}".format(x_ventana_emergente, y_ventana_emergente))
        ventana_emergente.title("Error")
        ventana_emergente.attributes('-topmost' , 1)
        ventana_emergente.focus()

appi = JP()
appi.mainloop()