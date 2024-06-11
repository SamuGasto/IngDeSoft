import customtkinter as ctk
from PIL import Image
import os
import BaseDeDatos.UsersQuery as User
import BaseDeDatos.ProjectsQuery as Proj
from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.Invitations as INV
from Vistas.util import centrarVentana
from functools import partial
import Clases.Componentes.Estilos as style

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
            self.ListarProyectosExistentes()
        
        if db['Invitaciones'].count_documents({"correo_invitado": self.user_email, "estado": "aceptada"}) == 0:
            pass
        else:
            self.ListarProyectosInvitados()
            
        self.after(100, self.verificar_invitaciones)
        
        self.mainloop()




    def Paneles(self):#FRAMES
        #sección izquierda
        self.side_bar = ctk.CTkFrame(self, 
                                     fg_color=style.Colores.background, 
                                     width=200, 
                                     corner_radius=0)
        self.side_bar.pack(side="left", fill="y", expand=False)
        #cuerpo principal
        self.body = ctk.CTkFrame(self, 
                                 fg_color=style.Colores.backgroundVariant, 
                                 corner_radius=0)
        self.body.pack(side="right", fill="both", expand=True)
        #frame que contiene Nombre del proyecto actual
        self.top_subpanel = ctk.CTkFrame(self.body, 
                                         fg_color=style.Colores.backgroundVariant, 
                                         height=120, 
                                         corner_radius=0)
        self.top_subpanel.pack(side=ctk.TOP, fill="x", expand=False)
        #frame para la imágen
        self.topimage = ctk.CTkFrame(self.top_subpanel, 
                                     fg_color=style.Colores.background, 
                                     corner_radius=0)
        self.topimage.pack(side=ctk.RIGHT, expand=False)

    def controles_sidebar(self):

        self.mis_proyectos = ctk.CTkLabel(self.side_bar, 
                                          text="Proyectos",
                                          text_color = style.Titulo.text_color,
                                          font = style.Titulo.font)
        self.mis_proyectos.pack(side=ctk.TOP, pady=5, padx=5)

        self.boton_nuevo_proyecto = ctk.CTkButton(self.side_bar,
                                                  text_color = style.BotonGrande.text_color,
                                                  fg_color = style.BotonGrande.fg_color,
                                                  font = style.BotonGrande.font,
                                                  corner_radius = style.BotonGrande.corner_radius,
                                                  hover_color = style.BotonGrande.hover_color,
                                                  text="Crear Proyecto +", 
                                                  width=200, height=65, 
                                                  command= self.crear_proyecto)
        self.boton_nuevo_proyecto.pack(side=ctk.BOTTOM, pady=10, padx=5)

        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.side_bar, 
                                 height=400,
                                 fg_color=style.Colores.background,
                                 segmented_button_fg_color=style.Colores.background,
                                 segmented_button_selected_color=style.BotonNormal.fg_color,
                                 segmented_button_selected_hover_color=style.BotonNormal.hover_color,
                                 segmented_button_unselected_color=style.BotonSecundario.fg_color,
                                 segmented_button_unselected_hover_color=style.BotonSecundario.hover_color,)
        tabview.pack(pady=(5,0), fill="both")
        #Agregamos Tabs
        self.tabBar1 = tabview.add("Mis proyectos")
        self.tabBar2 = tabview.add("Otros Proyectos")

        

    def contenido_body(self):
        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.body, 
                                 height=400,
                                 fg_color=style.Colores.backgroundVariant2,
                                 segmented_button_fg_color=style.Colores.backgroundVariant2,
                                 segmented_button_selected_color=style.BotonNormal.fg_color,
                                 segmented_button_selected_hover_color=style.BotonNormal.hover_color,
                                 segmented_button_unselected_color=style.BotonSecundario.fg_color,
                                 segmented_button_unselected_hover_color=style.BotonSecundario.hover_color,)
        tabview.pack(padx=5, pady=5, fill="x")
        #Agregamos Tabs
        self.tab1 = tabview.add("Integrantes")  
        self.tab2 = tabview.add("Requerimientos")  
        self.tab3 = tabview.add("Métricas")  
        
        ##Objetos de tab1 (INTEGRANTES)
        self.principal = ctk.CTkFrame(master=self.tab1,
                                      fg_color=style.Colores.backgroundVariant,
                                      border_width=3,
                                      border_color=style.Colores.Gray[4])
        self.principal.pack(fill="both",expand=True)

        ##Objetos de tab2(REQUERIMIENTOS)
        self.principal = ctk.CTkFrame(master=self.tab2,
                                      fg_color=style.Colores.backgroundVariant,
                                      border_width=3,
                                      border_color=style.Colores.Gray[4])
        self.principal.pack(fill="both",expand=True)

        self.agregarReq = ctk.CTkButton(self.principal, 
                                        text="Agregar Requerimientos",
                                        text_color = style.BotonNormal.text_color,
                                        fg_color = style.BotonNormal.fg_color,
                                        font = style.BotonNormal.font,
                                        corner_radius = style.BotonNormal.corner_radius,
                                        hover_color = style.BotonNormal.hover_color,
                                        width=150, 
                                        height=35, 
                                        command=self.AnadirRequerimiento)
        self.agregarReq.pack(side=ctk.TOP, anchor= ctk.N, pady=5)

        self.reques_texto = ctk.CTkScrollableFrame(self.principal,
                                                   fg_color=style.Colores.backgroundVariant,)
        self.reques_texto.pack(side=ctk.TOP, fill="both", expand=True, anchor = ctk.N, pady=(5,4), padx=4)
        
        ##Objetos de tab3(MÉTRICAS)
        self.principal = ctk.CTkFrame(master=self.tab3,
                                      fg_color=style.Colores.backgroundVariant,
                                      border_width=3,
                                      border_color=style.Colores.Gray[4])
        self.principal.pack(fill="both",expand=True)

    def contenido_subpanel(self):
        #texto_boton = self.boton_proyecto.cget("text")#se obtiene la info del proyecto seleccionado, para mostrar en la ventana
        self.proyecto_actual = ctk.CTkLabel(self.top_subpanel, 
                                            text="Selecciona o crea un proyecto", 
                                            text_color = style.Titulo.text_color,
                                            font = style.Titulo.font)
        self.proyecto_actual.pack(side=ctk.TOP)

    def Update_reqs(self): #Función para actualizar en pantalla los requerimientos de la base de datos
        self.reques_proyecto_actual = Proj.ObtenerRequerimientos(self.user_email, self.ID_activo)
        for widget in self.reques_texto.winfo_children():
            widget.destroy()
        for req in self.reques_proyecto_actual:
            self.reque_label = ctk.CTkLabel(self.reques_texto, text="- Requerimiento: " + req, 
                                            text_color = style.Texto.text_color,
                                            font = style.Texto.font)
            self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)

    def contenido_image(self): #Imagen compañía
        # Obtener la ruta absoluta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
        logo = ctk.CTkImage(light_image=Image.open(logo_path), 
                            dark_image=Image.open(logo_path),
                            size=(60, 60), )
        logo_label = ctk.CTkLabel(self.topimage, 
                                  image=logo, 
                                  text="", 
                                  bg_color=style.Colores.backgroundVariant)
        logo_label.pack(padx=5, pady=5)
    
    def ListarProyectosExistentes(self): #Funcion que busca y lista los proyectos del usuario
        nombres = Proj.ObtenerNombresProyecto(self.user_email)
        #proj_activos = Proj.BuscarProyectos(self.user_email)

        for nombre in nombres:
            nombre_proyecto = nombre
            self.proyecto_id = Proj.ObtenerIdProyecto(self.user_email, nombre_proyecto)
            texto = f"{nombre_proyecto}"
            
            self.new_proyect = ctk.CTkButton(self.tabBar1, 
                                             text=texto,
                                             text_color = style.BotonLista.text_color,
                                             fg_color = style.BotonLista.fg_color,
                                             font = style.BotonLista.font,
                                             corner_radius = style.BotonLista.corner_radius,
                                             hover_color = style.BotonLista.hover_color,
                                             border_width=2,
                                             border_color=style.Colores.Gray[4],
                                             width=200, 
                                             height=65, 
                                             command=partial(self.cambiar_proyecto, nombre_proyecto))
            self.new_proyect.pack(side=ctk.TOP, pady=10, fill="x")

    def ListarProyectosInvitados(self):
        proyectos_aceptados = INV.ObtenerProyectosAceptados(self.user_email)
        for proyecto in proyectos_aceptados:
            self.agregar_boton_proyecto(proyecto["nombre_proyecto"])
        

    def agregar_boton_proyecto(self, nombre_proyecto):
        texto = f"{nombre_proyecto}"
        self.proyecto_inv = ctk.CTkButton(self.tabBar2, 
                                          text=texto, 
                                          text_color = style.BotonLista.text_color,
                                          fg_color = style.BotonLista.fg_color,
                                          font = style.BotonLista.font,
                                          corner_radius = style.BotonLista.corner_radius,
                                          hover_color = style.BotonLista.hover_color,
                                          border_width=2,
                                          border_color=style.Colores.Gray[4],
                                          width=200, 
                                          height=65)
        self.proyecto_inv.pack(side=ctk.TOP, pady=10, fill="x")

    def crear_proyecto2(self): #Crea el botón de proyecto activo en el lateral
        self.proyecto_id = Proj.ObtenerIdProyecto(self.user_email, self.Nombre_Proyecto)
        texto = "PRO-" + str(self.proyecto_id)
        nombre_proyecto = Proj.ObtenerDatosProyecto(self.user_email, self.proyecto_id)
        nombre_proyecto = nombre_proyecto[0]
        self.new_proyect = ctk.CTkButton(self.tabBar1, 
                                         text=texto,
                                         text_color = style.BotonNormal.text_color,
                                         fg_color = style.BotonNormal.fg_color,
                                         font = style.BotonNormal.font,
                                         corner_radius = style.BotonNormal.corner_radius,
                                         hover_color = style.BotonNormal.hover_color,
                                         width=200, 
                                         height=65,
                                         command=lambda: self.cambiar_proyecto(nombre_proyecto))
        self.new_proyect.pack(side=ctk.TOP, pady=10)

    def crear_proyecto(self): #Ventana para crear un proyecto
        if Proj.BuscarProyectos(self.user_email) >= 3:
            ventana_aviso = self.mostrar_ventana_emergente("Error: No se puede crear otro proyecto.\n\nMotivo: Límite de proyectos activos alcanzado.")

            cerrar = ctk.CTkButton(ventana_aviso, text="Aceptar", command=ventana_aviso.withdraw)
            cerrar.pack(pady=(0,5))

            return
        else:
            self.window = ctk.CTkToplevel(self)
            self.window.configure(fg_color=style.Colores.background)
            centrarVentana(self.window, 800, 500)
            self.window.title("Error")
            self.window.attributes('-topmost' , 1)
            self.window.focus()

            titulo = ctk.CTkLabel(self.window,
                                  text="Crear un proyecto nuevo",
                                  text_color = style.Titulo.text_color,
                                  font = style.Titulo.font)
            titulo.pack(side=ctk.TOP, pady=5, anchor=ctk.NW)

            subtitulo = ctk.CTkLabel(self.window, 
                                     text="Llena los campos con la información de tu proyecto", 
                                     text_color = style.Titulo.text_color,
                                     font = style.Titulo.font)
            subtitulo.pack(side=ctk.TOP, pady=3, anchor=ctk.NW)

            # Crear un frame para contener nombre y nombre_entry
            NOMBRE = ctk.CTkFrame(self.window, fg_color=style.Colores.background)
            NOMBRE.pack(side=ctk.TOP, pady=5, anchor=ctk.NW, fill=ctk.X)
            
            nombre = ctk.CTkLabel(NOMBRE, 
                                  text="Nombre del proyecto (obligatorio):", 
                                  text_color = style.Titulo.text_color,
                                  font = style.Titulo.font)
            nombre.pack(side=ctk.LEFT, padx=2)
            
            self.nombre_entry = ctk.CTkEntry(NOMBRE, 
                                             placeholder_text="Nombre del proyecto...", 
                                             width=200,
                                             fg_color = style.EntryNormal.fg_color,
                                             border_color = style.EntryNormal.border_color,
                                             text_color = style.EntryNormal.text_color,
                                             font = style.EntryNormal.font,
                                             corner_radius = style.EntryNormal.corner_radius)
            self.nombre_entry.pack(side=ctk.LEFT, padx=2)

            # Crear un frame para participantes
            self.PARTICIPANTES = ctk.CTkFrame(self.window, fg_color=style.Colores.background)
            self.PARTICIPANTES.pack(side=ctk.TOP, pady=5, anchor=ctk.NW, fill=ctk.X, expand=True)
            
            participantes_label = ctk.CTkLabel(self.PARTICIPANTES, 
                                               text="Introduce el correo de los miembros de tu proyecto para invitarlos:", 
                                               text_color = style.Texto.text_color,
                                               font = style.Texto.font)
            participantes_label.pack(side=ctk.TOP, pady=5, anchor=ctk.NW)

            # Crear subframes dentro de PARTICIPANTES
            
            self.indice_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color=style.Colores.background)
            self.indice_frame.pack(side=ctk.LEFT, padx=2, pady=2, anchor=ctk.NW)

            self.participantes_entries_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color=style.Colores.background)
            self.participantes_entries_frame.pack(side=ctk.LEFT, padx=2, pady=2, anchor=ctk.NW)

            self.Combobox_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color=style.Colores.background)
            self.Combobox_frame.pack(side=ctk.LEFT, padx=2, pady=2, anchor=ctk.NW)

            self.add_participante_entry()
            
            # Botón para agregar más participantes
            self.more_button_frame = ctk.CTkFrame(self.PARTICIPANTES, fg_color=style.Colores.backgroundVariant)
            self.more_button_frame.pack(side=ctk.LEFT, padx=5, pady=2,anchor=ctk.NW)
            
            more_button = ctk.CTkButton(self.more_button_frame, 
                                        width=25, 
                                        height=25, 
                                        text="+",
                                        text_color = style.BotonNormal.text_color,
                                        fg_color = style.BotonNormal.fg_color,
                                        font = style.BotonNormal.font,
                                        corner_radius = style.BotonNormal.corner_radius,
                                        hover_color = style.BotonNormal.hover_color,
                                        command=self.add_participante_entry)
            more_button.pack(anchor=ctk.CENTER)

            # Botón para mandar la query y crear proyecto
            crear_proyecto_button = ctk.CTkButton(self.window, 
                                                  text="Crear Proyecto",
                                                  text_color = style.BotonNormal.text_color,
                                                  fg_color = style.BotonNormal.fg_color,
                                                  font = style.BotonNormal.font,
                                                  corner_radius = style.BotonNormal.corner_radius,
                                                  hover_color = style.BotonNormal.hover_color,
                                                  command=self.crear_proyecto_query)
            crear_proyecto_button.pack(side=ctk.BOTTOM, pady=10)

    def add_participante_entry(self):
        self.indice_participante += 1
        self.indice = ctk.CTkLabel(self.indice_frame,
                                   text=self.indice_participante, 
                                   text_color = style.Texto.text_color,
                                   font = style.Texto.font)
        self.indice.pack(side=ctk.TOP, padx=2, pady=2)

        self.entry_participante = ctk.CTkEntry(self.participantes_entries_frame, 
                                               placeholder_text="Correo...",
                                               fg_color = style.EntryNormal.fg_color,
                                               border_color = style.EntryNormal.border_color,
                                               text_color = style.EntryNormal.text_color,
                                               font = style.EntryNormal.font,
                                               corner_radius = style.EntryNormal.corner_radius,
                                               width=200)
        self.entry_participante.pack(side=ctk.TOP, padx=2, pady=2, anchor=ctk.NW)
        self.participantes_entries.append(self.entry_participante)

        #command=partial(self.actualizar_rol_participante,int(self.indice.cget("text")))
        self.combobox_rol = ctk.CTkComboBox(self.Combobox_frame, values=["Administrador", "Desarrollador"]
                                            )
        self.combobox_rol.pack(side=ctk.TOP, padx=2, pady=2)
        self.combobox_rol.set("Seleccionar rol...")
        self.participantes_rol.append(self.combobox_rol)  
    

    def crear_proyecto_query(self): #Query para añadir el proyecto la base de datos
        Proj.AumentarProyectos(self.user_email)
        print("Numero de proyectos activos: " + str(Proj.BuscarProyectos(self.user_email)))
        
        participantes_emails = [entry.get() for entry in self.participantes_entries]
        participantes_roles = [rol.get() for rol in self.participantes_rol]
        self.Nombre_Proyecto = self.nombre_entry.get()
        miembros = [(miembro, rol) for miembro, rol in zip(participantes_emails, participantes_roles)]

        Proj.CrearNuevoProyecto(self.Nombre_Proyecto, miembros, self.user_email)
        
        # Enviar invitaciones
        proyecto_id = Proj.ObtenerIdProyecto(self.user_email, self.Nombre_Proyecto)
        for correo, rol in zip(participantes_emails, participantes_roles):
            INV.IngresarInvitacion(self.user_email, proyecto_id, correo, rol, "pendiente")

        self.window.withdraw()
        self.mostrar_ventana_emergente("Proyecto creado exitosamente")
        self.participantes_entries = []
        participantes_emails = []
        participantes_roles = []
        self.crear_proyecto2()

    def cambiar_proyecto(self, texto): #Botón para mostrar el contenido de un proyecto (Botón lateral)
        for widget in self.tab1.winfo_children():
            widget.destroy()
        #cambiamos el texto del titulo en pantalla
        self.proyecto_actual.configure(text=texto)
        self.tab1.configure(fg_color=style.Colores.backgroundVariant,
                            border_width=3,
                            border_color=style.Colores.Gray[4])
        #Paso 1: Listar los integrantes del proyecto en pantalla, junto a su rol
        data = Proj.ObtenerDatosProyecto(self.user_email, Proj.ObtenerIdProyecto(self.user_email, texto))
        self.ID_activo = Proj.ObtenerIdProyecto(self.user_email, texto)
        self.miembros = data[1]
        for miembro in self.miembros:
            self.miembro_label = ctk.CTkLabel(self.tab1, text="- Correo: " + miembro[0] + ". Rol: " + miembro[1], 
                                              text_color = style.Texto.text_color,
                                              font = style.Texto.font,)
            self.miembro_label.pack(side=ctk.TOP, 
                                    anchor=ctk.NW,
                                    padx = 5,
                                    pady = 5)

        #Paso 2: Listar los requerimientos del proyecto.
        self.reques_proyecto_actual = Proj.ObtenerRequerimientos(self.user_email, self.ID_activo)
        if self.reques_proyecto_actual == [] or None:
            for widget in self.reques_texto.winfo_children():
                widget.destroy()
            self.reque_label = ctk.CTkLabel(self.reques_texto, 
                                            text="El proyecto aún no posee requerimientos", 
                                            text_color = style.Texto.text_color,
                                            font = style.Texto.font)
            self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)
        else:
            for widget in self.reques_texto.winfo_children():
                widget.destroy()
            for req in self.reques_proyecto_actual:
                self.reque_label = ctk.CTkLabel(self.reques_texto, text="- Requerimiento: " + req,
                                                text_color = style.Texto.text_color,
                                                font = style.Texto.font)
                self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)
        
        #Paso 3: Visualizar las métricas del proyecto.


    def mostrar_ventana_emergente(self, texto):
        ventana_emergente = ctk.CTkToplevel(self)
        ventana_emergente.configure(fg_color=style.Colores.background)
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

        return ventana_emergente

    def AnadirRequerimiento(self): #Ventana para añadir requerimientos al proyecto actual
        self.ventana_rq = ctk.CTkToplevel(self)
        self.ventana_rq.configure(fg_color="#061d2c")
        centrarVentana(self.ventana_rq, 700, 450)
        self.ventana_rq.title("Añadir Requerimientos")
        self.ventana_rq.attributes('-topmost' , 1)
        self.ventana_rq.focus()

        titulo = ctk.CTkLabel(self.ventana_rq, 
                              text="Ingresa requerimientos al proyecto", 
                              text_color = style.Titulo.text_color,
                              font = style.Titulo.font)
        titulo.pack(side=ctk.TOP, anchor=ctk.NW, padx=15, pady=3)
        subtitulo = ctk.CTkLabel(self.ventana_rq, text="A cada requerimiento se le asignará un ID automáticamente.", 
                                 text_color = style.Subtitulo.text_color,
                                 font = style.Subtitulo.font)
        subtitulo.pack(side=ctk.TOP, anchor=ctk.NW, padx=15, pady=3)

        enviar = ctk.CTkButton(self.ventana_rq, 
                               height=35, 
                               width=45,
                               text="Agregar al proyecto",
                               text_color = style.BotonNormal.text_color,
                               fg_color = style.BotonNormal.fg_color,
                               font = style.BotonNormal.font,
                               corner_radius = style.BotonNormal.corner_radius,
                               hover_color = style.BotonNormal.hover_color,
                               command=self.reqs_query)
        enviar.pack(side=ctk.BOTTOM, anchor=ctk.S, pady=10)

        # Crear un frame para contener reques y el botón
        self.REQ = ctk.CTkScrollableFrame(self.ventana_rq, fg_color=style.Colores.backgroundVariant)
        self.REQ.pack(side=ctk.TOP, pady=5, fill="both", expand=True)

        #Crear subframes dentro de self.REQ

        self.reques = ctk.CTkFrame(self.REQ, fg_color=style.Colores.backgroundVariant)
        self.reques.pack(side=ctk.LEFT, padx=5, pady=5, anchor=ctk.NW)


        # Botón para agregar más requerimientos
        self.more_button_frame2 = ctk.CTkFrame(self.REQ, fg_color=style.Colores.backgroundVariant)
        self.more_button_frame2.pack(side=ctk.LEFT, padx=5, pady=5, anchor=ctk.N)

        self.add_requerimiento_entry()

        self.more_button = ctk.CTkButton(self.more_button_frame2, 
                                         height=35,
                                         width=45,
                                         text="+",
                                         text_color = style.BotonNormal.text_color,
                                         fg_color = style.BotonNormal.fg_color,
                                         font = style.BotonNormal.font,
                                         corner_radius = style.BotonNormal.corner_radius,
                                         hover_color = style.BotonNormal.hover_color,
                                         command=self.add_requerimiento_entry)
        self.more_button.pack(pady=(5,5), anchor=ctk.CENTER)
        
        

    def add_requerimiento_entry(self): #Funcion para añadir más entrys para requerimientos
        self.req = ctk.CTkEntry(self.reques, 
                                placeholder_text="Ingresar requerimiento...", 
                                width=350, 
                                height=35, 
                                fg_color = style.EntryNormal.fg_color,
                                border_color = style.EntryNormal.border_color,
                                text_color = style.EntryNormal.text_color,
                                font = style.EntryNormal.font,
                                corner_radius = style.EntryNormal.corner_radius)
        self.req.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5) 

        if self.contador == 5:
            pass
        else:
            self.more_button.pack_configure(pady=(self.contador, 5))

        self.requerimientos.append(self.req)
        self.contador+=45
    
    def reqs_query(self): #Query para ingresar requerimientos al proyecto
        requerimientos = [entry.get() for entry in self.requerimientos]
        #Mandar la query con los requerimientos
        Proj.Ingresar_requerimientos(self.user_email, self.ID_activo, requerimientos)
        #Reiniciar variables
        requerimientos= []
        self.requerimientos = []
        self.contador = 5

        self.ventana_rq.withdraw()
        ventanita = self.mostrar_ventana_emergente("Requerimientos agregados exitosamente.")
        cerrar = ctk.CTkButton(ventanita, 
                               text="Aceptar",
                               text_color = style.BotonNormal.text_color,
                               fg_color = style.BotonNormal.fg_color,
                               font = style.BotonNormal.font,
                               corner_radius = style.BotonNormal.corner_radius,
                               hover_color = style.BotonNormal.hover_color,
                               command=ventanita.withdraw)
        cerrar.pack(pady=(0,5))
        self.Update_reqs()

    
    def verificar_invitaciones(self):
        invitaciones_pendientes = db['Invitaciones'].find({"correo_invitado": self.user_email, "estado": "pendiente"})
        for inv in invitaciones_pendientes:
            # Mostrar ventana de invitación
            self.InvitationWindow = self.mostrar_ventana_invitacion(inv)
            self.wait_window(self.InvitationWindow)

    def mostrar_ventana_invitacion(self, invitacion):
        ventana_invitacion = ctk.CTkToplevel(self)
        ventana_invitacion.configure(fg_color=style.Colores.background)
        centrarVentana(ventana_invitacion, 400, 200)
        ventana_invitacion.title("Invitación a Proyecto")
        ventana_invitacion.attributes('-topmost' , 1)

        mensaje = f"Has sido invitado por {invitacion['owner_proyecto']}\n al proyecto ID: {invitacion['proyecto_id']}\n como {invitacion['rol']}."
        etiqueta = ctk.CTkLabel(ventana_invitacion, 
                                text=mensaje, 
                                text_color = style.Texto.text_color,
                                font = style.Texto.font)
        etiqueta.pack(pady=20)

        aceptar_button = ctk.CTkButton(ventana_invitacion, 
                                       text="Aceptar",
                                       text_color = style.BotonNormal.text_color,
                                       fg_color = style.BotonNormal.fg_color,
                                       font = style.BotonNormal.font,
                                       corner_radius = style.BotonNormal.corner_radius,
                                       hover_color = style.BotonNormal.hover_color,
                                       command=lambda: self.responder_invitacion(invitacion, "aceptada"))
        aceptar_button.pack(side=ctk.LEFT, padx=20, pady=20)
        return ventana_invitacion

    def responder_invitacion(self, invitacion, respuesta):
        self.InvitationWindow.destroy()
        if respuesta == "aceptada":
            db['Invitaciones'].update_one({"_id": invitacion["_id"]}, {"$set": {"estado": respuesta}})
            window = self.mostrar_ventana_emergente(f"Invitación {respuesta}")
            cerrar = ctk.CTkButton(window, 
                                   text="Cerrar",
                                   text_color = style.BotonNormal.text_color,
                                   fg_color = style.BotonNormal.fg_color,
                                   font = style.BotonNormal.font,
                                   corner_radius = style.BotonNormal.corner_radius,
                                   hover_color = style.BotonNormal.hover_color, 
                                   command=window.destroy)
            cerrar.pack(pady=(0,5))
            self.wait_window(window)
            
            for widget in self.tabBar2.winfo_children():
                widget.destroy()
            self.ListarProyectosInvitados()
