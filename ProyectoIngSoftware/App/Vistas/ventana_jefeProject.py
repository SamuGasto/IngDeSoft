import customtkinter as ctk
from PIL import Image
import os
import BaseDeDatos.UsersQuery as User
import BaseDeDatos.ProjectsQuery as Proj
from Vistas.util import centrarVentana
from functools import partial

#creamos la clase ventana para el jefe de proyecto
class JP(ctk.CTk):
    def __init__(self, email:str):
        super().__init__()
        #self.proyecto_id = 110
        self.title("PaltaEstimateApp")
        #ACÁ CENTRAMOS LA VENTANA 
        centrarVentana(self, 1200, 600)

        #VARIABLES
        self.participantes_entries = []
        self.participantes_rol = []
        self.requerimientos = []
        
        self.indice_participante = -1
        self.contador = 5
        self.user_email = email
        self.ID_activo = 0

        #FRAMES Y CONTENIDO
        self.Paneles()
        self.controles_sidebar()
        self.contenido_body()
        self.contenido_subpanel()
        self.contenido_image()
        
        
        if Proj.BuscarProyectos(self.user_email) == 0:
            pass
        else:
            self.ListarProyectoExistente()
        
        self.mainloop() 



    def Paneles(self):#FRAMES
        #sección izquierda
        self.side_bar = ctk.CTkFrame(self, fg_color="gray", width=200, corner_radius=0)
        self.side_bar.pack(side="left", fill="y", expand=False)
        #cuerpo principal
        self.body = ctk.CTkFrame(self, fg_color="black", corner_radius=0)
        self.body.pack(side="right", fill="both", expand=True)
        #frame que contiene Nombre del proyecto actual
        self.top_subpanel = ctk.CTkFrame(self.body, fg_color="transparent", height=120, corner_radius=0)
        self.top_subpanel.pack(side=ctk.TOP, fill="x", expand=False)
        #frame para la imágen
        self.topimage = ctk.CTkFrame(self.top_subpanel, fg_color="transparent", corner_radius=0)
        self.topimage.pack(side=ctk.RIGHT, expand=False)

    def controles_sidebar(self):

        self.mis_proyectos = ctk.CTkLabel(self.side_bar, text="Mis Proyectos", font=("Comic Sans", -20))
        self.mis_proyectos.pack(side=ctk.TOP, pady=5, padx=5)

        self.boton_nuevo_proyecto = ctk.CTkButton(self.side_bar, text="Crear Proyecto +", font=("Comic Sans", -20),
                                                fg_color="red", width=200, height=65, corner_radius=15, command= self.crear_proyecto)
        self.boton_nuevo_proyecto.pack(side=ctk.BOTTOM, pady=10, padx=5)

    def contenido_body(self):
        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.body, height=400)
        tabview.pack(padx=5, pady=5, fill="x")
        #Agregamos Tabs
        self.tab1 = tabview.add("Integrantes")  
        self.tab2 = tabview.add("Requerimientos")  
        self.tab3 = tabview.add("Métricas")  
        
        ##Objetos de tab1 (INTEGRANTES)
        button = ctk.CTkButton(master=self.tab1)#Para colocar elementos, solo se especifica el tab
        button.pack(side=ctk.BOTTOM, padx=20, pady=20)

        ##Objetos de tab2(REQUERIMIENTOS)
        self.principal = ctk.CTkFrame(master=self.tab2)
        self.principal.pack(fill="both",expand=True)

        self.agregarReq = ctk.CTkButton(self.principal, text="Agregar Requerimientos",
                                        text_color="black",fg_color="white", font=("Comic Sans", -15),
                                        width=150, height=35, corner_radius=10, command=self.AnadirRequerimiento)
        self.agregarReq.pack(side=ctk.TOP, anchor= ctk.N, pady=5)

        self.reques_texto = ctk.CTkScrollableFrame(self.principal)
        self.reques_texto.pack(side=ctk.TOP, fill="both", expand=True, anchor = ctk.N, pady=(5,0))


        
        
        ##Objetos de tab3(MÉTRICAS)

        ##objetos del body
        self.update_rq = ctk.CTkButton(self.body, text="Actualizar requerimientos", fg_color="light blue", text_color="black",
                                        font=("Comic Sans", -15), border_width=1.5, border_color="white",
                                        width=150, height=35, corner_radius=25, command=self.Update_reqs)
        self.update_rq.pack(side=ctk.RIGHT, anchor=ctk.SW, pady=5, padx=5)

        self.administrar  = ctk.CTkButton(self.body, text="Administración\nCompleta", text_color="black",fg_color="white", font=("Comic Sans", -15, "bold"),
                                        width=150, height=35, corner_radius=25)
        self.administrar.pack(side=ctk.LEFT, anchor=ctk.SE, pady=5, padx=5)

    def contenido_subpanel(self):
        #texto_boton = self.boton_proyecto.cget("text")#se obtiene la info del proyecto seleccionado, para mostrar en la ventana
        self.proyecto_actual = ctk.CTkLabel(self.top_subpanel, text="Selecciona o crea un proyecto", font=("Comic Sans", -25))
        self.proyecto_actual.pack(side=ctk.TOP)

    def Update_reqs(self):
        self.reques_proyecto_actual = Proj.ObtenerRequerimientos(self.user_email, self.ID_activo)
        for widget in self.reques_texto.winfo_children():
            widget.destroy()
        for req in self.reques_proyecto_actual:
            self.reque_label = ctk.CTkLabel(self.reques_texto, text="- Requerimiento: " + req, text_color="white",
                            font=("Comic Sans MS", -15, "bold"))
            self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)

    def contenido_image(self):
        # Obtener la ruta absoluta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
        logo = ctk.CTkImage(light_image=Image.open(logo_path),
            size=(60, 60))
        logo_label = ctk.CTkLabel(self.topimage, image=logo, text="")
        logo_label.pack(padx=5, pady=5)
    
    def ListarProyectoExistente(self):
        nombres = Proj.ObtenerNombresProyecto(self.user_email)
        proj_activos = Proj.BuscarProyectos(self.user_email)
        i=0
        while i < proj_activos:
            nombre_proyecto = nombres[i]
            self.proyecto_id = Proj.ObtenerIdProyecto(self.user_email, nombre_proyecto)
            texto = "PRO-" + str(self.proyecto_id)
            
            self.new_proyect = ctk.CTkButton(self.side_bar, text=texto, fg_color="orange",font=("Arial", -20),
                                                    width=200, height=65, corner_radius=15,command=partial(self.cambiar_proyecto, nombre_proyecto))
            self.new_proyect.pack(side=ctk.TOP, pady=10, padx=5)
            i+=1


    def crear_proyecto2(self):#Crea el botón en el lateral
        self.proyecto_id = Proj.ObtenerIdProyecto(self.user_email, self.Nombre_Proyecto)
        texto = "PRO-" + str(self.proyecto_id)
        nombre_proyecto = Proj.ObtenerDatosProyecto(self.user_email, self.proyecto_id)
        nombre_proyecto = nombre_proyecto[0]
        self.new_proyect = ctk.CTkButton(self.side_bar, text=texto, fg_color="orange",font=("Arial", -20),
                                                width=200, height=65, corner_radius=15, command=lambda: self.cambiar_proyecto(nombre_proyecto))
        self.new_proyect.pack(side=ctk.TOP, pady=10)

    def crear_proyecto(self):
        if Proj.BuscarProyectos(self.user_email) >= 3:
            self.mostrar_ventana_emergente("Error: No se puede crear otro proyecto.\n\nMotivo: Límite de proyectos activos alcanzado.")
            return
        else:
            self.window = ctk.CTkToplevel(self)
            self.window.configure(fg_color="white")
            centrarVentana(self.window, 800, 500)
            self.window.title("Error")
            self.window.attributes('-topmost' , 1)
            self.window.focus()

            titulo = ctk.CTkLabel(self.window, text_color="black", text="Crear un proyecto nuevo", font=("Verdana", -25, "bold"))
            titulo.pack(side=ctk.TOP, pady=5, anchor=ctk.NW)

            subtitulo = ctk.CTkLabel(self.window, text_color="black", text="Llena los campos con la información de tu proyecto", font=("Verdana", -15))
            subtitulo.pack(side=ctk.TOP, pady=3, anchor=ctk.NW)

            # Crear un frame para contener nombre y nombre_entry
            NOMBRE = ctk.CTkFrame(self.window, fg_color="white")
            NOMBRE.pack(side=ctk.TOP, pady=5, anchor=ctk.NW, fill=ctk.X)
            
            nombre = ctk.CTkLabel(NOMBRE, text="Nombre del proyecto (obligatorio):", text_color="black", font=("Verdana", -18))
            nombre.pack(side=ctk.LEFT, padx=2)
            
            self.nombre_entry = ctk.CTkEntry(NOMBRE, placeholder_text="Nombre del proyecto...", width=200)
            self.nombre_entry.pack(side=ctk.LEFT, padx=2)

            # Crear un frame para participantes
            self.PARTICIPANTES = ctk.CTkFrame(self.window, fg_color="blue")
            self.PARTICIPANTES.pack(side=ctk.TOP, pady=5, anchor=ctk.NW, fill=ctk.X, expand=True)
            
            participantes_label = ctk.CTkLabel(self.PARTICIPANTES, text="Introduce el correo de los miembros de tu proyecto para invitarlos:", font=("Verdana", -18), text_color="black")
            participantes_label.pack(side=ctk.TOP, pady=5, anchor=ctk.NW)

            # Crear subframes dentro de PARTICIPANTES
            
            self.indice_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color="white")
            self.indice_frame.pack(side=ctk.LEFT, padx=2, pady=2, anchor=ctk.NW)

            self.participantes_entries_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color="white")
            self.participantes_entries_frame.pack(side=ctk.LEFT, padx=2, pady=2, anchor=ctk.NW)

            self.Combobox_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color="white")
            self.Combobox_frame.pack(side=ctk.LEFT, padx=2, pady=2, anchor=ctk.NW)

            self.add_participante_entry()
            
            # Botón para agregar más participantes
            self.more_button_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color="transparent")
            self.more_button_frame.pack(side=ctk.LEFT, padx=5, pady=2,anchor=ctk.NW)
            
            more_button = ctk.CTkButton(self.more_button_frame, width=25, height=25, text="+", text_color="black", font=("Helvetica", -15), command=self.add_participante_entry)
            more_button.pack(anchor=ctk.CENTER)

            # Botón para mandar la query y crear proyecto
            crear_proyecto_button = ctk.CTkButton(self.window, text="Crear Proyecto", command=self.crear_proyecto_query)
            crear_proyecto_button.pack(side=ctk.BOTTOM, pady=10)

    def add_participante_entry(self):
        self.indice_participante += 1
        self.indice = ctk.CTkLabel(self.indice_frame,text=self.indice_participante, text_color="black")
        self.indice.pack(side=ctk.TOP, padx=2, pady=2)

        self.entry_participante = ctk.CTkEntry(self.participantes_entries_frame, placeholder_text="Correo...", width=200)
        self.entry_participante.pack(side=ctk.TOP, padx=2, pady=2, anchor=ctk.NW)
        self.participantes_entries.append(self.entry_participante)

        #command=partial(self.actualizar_rol_participante,int(self.indice.cget("text")))
        self.combobox_rol = ctk.CTkComboBox(self.Combobox_frame, values=["Administrador", "Desarrollador"]
                                            )
        self.combobox_rol.pack(side=ctk.TOP, padx=2, pady=2)
        self.combobox_rol.set("Seleccionar rol...")
        self.participantes_rol.append(self.combobox_rol)  
    

    def crear_proyecto_query(self):
        Proj.AumentarProyectos(self.user_email)
        print("Numero de proyectos activos: " + str(Proj.BuscarProyectos(self.user_email)))
        
        participantes_emails = [entry.get() for entry in self.participantes_entries]
        participantes_roles = [rol.get() for rol in self.participantes_rol]
        self.Nombre_Proyecto = self.nombre_entry.get()
        miembros = [(miembro, rol) for miembro, rol in zip(participantes_emails, participantes_roles)]

        Proj.CrearNuevoProyecto(self.Nombre_Proyecto, miembros, self.user_email)
        
        self.window.withdraw()
        self.mostrar_ventana_emergente("Proyecto creado exitosamente")
        self.participantes_entries = []
        participantes_emails = []
        self.crear_proyecto2()

    def cambiar_proyecto(self, texto): #Botón para mostrar el contenido de un proyecto (Botón lateral)
        for widget in self.tab1.winfo_children():
            widget.destroy()
        #cambiamos el texto del titulo en pantalla
        self.proyecto_actual.configure(text=texto)
        #Paso 1: Listar los integrantes del proyecto en pantalla, junto a su rol
        data = Proj.ObtenerDatosProyecto(self.user_email, Proj.ObtenerIdProyecto(self.user_email, texto))
        self.ID_activo = Proj.ObtenerIdProyecto(self.user_email, texto)
        self.miembros = data[1]
        for miembro in self.miembros:
            self.miembro_label = ctk.CTkLabel(self.tab1, text="- Correo: " + miembro[0] + ". Rol: " + miembro[1], text_color="white",
                                            font=("Comic Sans MS", -18, "bold"))
            self.miembro_label.pack(side=ctk.TOP, anchor=ctk.NW)

        #Paso 2: Listar los requerimientos del proyecto.
        self.reques_proyecto_actual = Proj.ObtenerRequerimientos(self.user_email, self.ID_activo)
        if self.reques_proyecto_actual == [] or None:
            self.reque_label = ctk.CTkLabel(self.reques_texto, text="El proyecto aún no posee requerimientos", text_color="white",
                                font=("Comic Sans MS", -15, "bold"))
            self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)
        else:
            for widget in self.reques_texto.winfo_children():
                widget.destroy()
            for req in self.reques_proyecto_actual:
                self.reque_label = ctk.CTkLabel(self.reques_texto, text="- Requerimiento: " + req, text_color="white",
                                font=("Comic Sans MS", -15, "bold"))
                self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)
        
        #Paso 3: Visualizar las métricas del proyecto.

    def mostrar_ventana_emergente(self, texto):
        ventana_emergente = ctk.CTkToplevel(self)
        ventana_emergente.configure(fg_color="white")
        etiqueta = ctk.CTkLabel(ventana_emergente, font=("Arial", -15, "bold"), text_color="black",
                                text=texto)
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

    def AnadirRequerimiento(self):
        ventana_emergente = ctk.CTkToplevel(self)
        ventana_emergente.configure(fg_color="#061d2c")
        centrarVentana(ventana_emergente, 700, 450)
        ventana_emergente.title("Añadir Requerimientos")
        ventana_emergente.attributes('-topmost' , 1)
        ventana_emergente.focus()


        
        titulo = ctk.CTkLabel(ventana_emergente, text="Ingresa requerimientos al proyecto", text_color="#ffffff",
                            font=("Poppins", -25, "bold"))
        titulo.pack(side=ctk.TOP, anchor=ctk.NW, padx=15, pady=3)
        subtitulo = ctk.CTkLabel(ventana_emergente, text="A cada requerimiento se le asignará un ID automáticamente.", text_color="#ffffff",
                            font=("Poppins", -17, "italic"))
        subtitulo.pack(side=ctk.TOP, anchor=ctk.NW, padx=15, pady=3)

        enviar = ctk.CTkButton(ventana_emergente, height=35, width=45, corner_radius=50, border_width=1.5, border_color="white",
                                    text="Agregar al proyecto", text_color="white", font=("Helvetica", -15, "bold"), command=self.reqs_query)
        enviar.pack(side=ctk.BOTTOM, anchor=ctk.S, pady=10)

        # Crear un frame para contener reques y el botón
        self.REQ = ctk.CTkScrollableFrame(ventana_emergente, fg_color="transparent")
        self.REQ.pack(side=ctk.TOP, pady=5, fill="both", expand=True)

        #Crear subframes dentro de self.REQ

        self.reques = ctk.CTkFrame(self.REQ, fg_color="transparent")
        self.reques.pack(side=ctk.LEFT, padx=5, pady=5, anchor=ctk.NW)


        # Botón para agregar más requerimientos
        self.more_button_frame2 = ctk.CTkFrame(self.REQ, fg_color="transparent")
        self.more_button_frame2.pack(side=ctk.LEFT, padx=5, pady=5, anchor=ctk.N)

        self.add_requerimiento_entry()

        self.more_button = ctk.CTkButton(self.more_button_frame2, height=35, width=45, corner_radius=50, border_width=1.5, border_color="white",
                                    text="+", text_color="black", font=("Helvetica", -20, "bold"), command=self.add_requerimiento_entry)
        self.more_button.pack(pady=(5,5), anchor=ctk.CENTER)
        
        

    def add_requerimiento_entry(self):
        self.req = ctk.CTkEntry(self.reques, placeholder_text="Ingresar requerimiento...", width=350, height=35, border_color="white",
                                text_color="white")
        self.req.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5) 

        if self.contador == 5:
            pass
        else:
            self.more_button.pack_configure(pady=(self.contador, 5))

        self.requerimientos.append(self.req)
        self.contador+=45
    
    def reqs_query(self):
        requerimientos = [entry.get() for entry in self.requerimientos]
        print(self.user_email, self.ID_activo, requerimientos)
        Proj.Ingresar_requerimientos(self.user_email, self.ID_activo, requerimientos)
        #mandar query con los requerimientos
        

        requerimientos= []
        self.requerimientos = []
        self.contador = 5