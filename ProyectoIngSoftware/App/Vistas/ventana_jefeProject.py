from ast import Return
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import os
from functools import partial
from bson.objectid import ObjectId
from fpdf import FPDF
from regex import D

import BaseDeDatos.UsersQuery as User
import BaseDeDatos.ProjectsQuery as Proj
from BaseDeDatos.MainMongoDB import db
import BaseDeDatos.Invitations as INV
import BaseDeDatos.ReqCompQuery as Req
import Vistas.ventana_desarrollador as DEV
import Vistas.ventana_admin as ADMIN
import BaseDeDatos.SueldosQuery as sueldos
import Vistas.ventana_welcome as inicio

from Vistas.util import centrarVentana
import Clases.Componentes.Estilos as style

#creamos la clase ventana para el jefe de proyecto
class JP(ctk.CTk):
    def __init__(self, email:str):
        super().__init__()
        self.title("PaltaEstimateApp")
        #ACÁ CENTRAMOS LA VENTANA 
        centrarVentana(self, 1200, 600)
        self.after(0, lambda:self.state('zoomed'))
        self.attributes('-topmost', 0)

        #VARIABLES
        self.participantes_entries = []
        self.participantes_rol = []
        self.requerimientos = []
        
        self.indice_participante = -1
        self.contador = 5
        self.user_email = email
        self.ID_activo = 0
        self.object_id = None
        #FRAMES Y CONTENIDO
        self.Paneles()
        self.controles_sidebar()
        self.contenido_body()
        self.contenido_subpanel()
        self.contenido_image()
        
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
        self.boton_nuevo_proyecto.pack(side=ctk.BOTTOM, pady=(0, 10), padx=5)

        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.side_bar,
                                 fg_color=style.Colores.background,
                                 segmented_button_fg_color=style.Colores.background,
                                 segmented_button_selected_color=style.BotonNormal.fg_color,
                                 segmented_button_selected_hover_color=style.BotonNormal.hover_color,
                                 segmented_button_unselected_color=style.BotonSecundario.fg_color,
                                 segmented_button_unselected_hover_color=style.BotonSecundario.hover_color)
        tabview.pack(pady=(5,0), fill="both", expand=True)
        #Agregamos Tabs
        self.tabBar1 = tabview.add("Mis proyectos")
        self.tabBar2 = tabview.add("Otros Proyectos")

        self.proyectos = ctk.CTkScrollableFrame(self.tabBar1,
                                                fg_color=style.Colores.background, 
                                                width=200, 
                                                corner_radius=0)
        self.proyectos.pack(side=ctk.TOP, pady=(10,5), fill="both", expand=True)

        self.otros_proyectos = ctk.CTkScrollableFrame(self.tabBar2,
                                                fg_color=style.Colores.background, 
                                                width=200, 
                                                corner_radius=0)
        self.otros_proyectos.pack(side=ctk.TOP, pady=(10,5), fill="both", expand=True)

        

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
        tabview.pack(padx=5, pady=5, fill="both", expand = True)
        #Agregamos Tabs
        self.tab1 = tabview.add("Integrantes")  
        self.tab2 = tabview.add("Requerimientos")  
        self.tab3 = tabview.add("Estimación")  
        
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

        self.superior = ctk.CTkFrame(master=self.principal,
                                      fg_color=style.Colores.backgroundVariant)
        self.superior.pack(side=ctk.TOP, fill="both")
        
        self.agregarReq_frame = ctk.CTkFrame(master=self.superior,
                                            fg_color=style.Colores.backgroundVariant)
        self.agregarReq_frame.pack(side=ctk.LEFT, anchor= ctk.N, pady=5)

        self.editar_miembro_frame = ctk.CTkFrame(master=self.superior,
                                            fg_color=style.Colores.backgroundVariant)
        self.editar_miembro_frame.pack(side=ctk.RIGHT, anchor= ctk.N, pady=5)


        self.agregarReq = ctk.CTkButton(self.agregarReq_frame, 
                                        text="Agregar Requerimientos",
                                        text_color = style.BotonNormal.text_color,
                                        fg_color = style.BotonNormal.fg_color,
                                        font = style.BotonNormal.font,
                                        corner_radius = style.BotonNormal.corner_radius,
                                        hover_color = style.BotonNormal.hover_color,
                                        command=self.AnadirRequerimiento)
        self.agregarReq.pack(anchor=ctk.N, pady=5, padx=35)

        self.editar_miembro = ctk.CTkButton(self.editar_miembro_frame, 
                                        text="Editar miembro asignado",
                                        text_color = style.BotonNormal.text_color,
                                        fg_color = style.BotonNormal.fg_color,
                                        font = style.BotonNormal.font,
                                        corner_radius = style.BotonNormal.corner_radius,
                                        hover_color = style.BotonNormal.hover_color,
                                        command = self.editar_miembro_asignado)
        self.editar_miembro.pack(anchor=ctk.N, pady=5, padx=35)

        self.reques_frame = ctk.CTkScrollableFrame(self.principal,
                                                   fg_color=style.Colores.backgroundVariant)
        self.reques_frame.pack(side=ctk.TOP, fill="both", expand=True, anchor = ctk.N, pady=(5,4), padx=4)

        self.reques_texto = ctk.CTkScrollableFrame(self.reques_frame,
                                        fg_color=style.Colores.backgroundVariant,
                                        orientation = "horizontal",
                                        width=500,
                                        height=780)
        self.reques_texto.pack(side=ctk.LEFT, padx=4, pady=(4,0), fill="both", expand=True)

        self.reques_asignado = ctk.CTkFrame(self.reques_frame,
                                        fg_color=style.Colores.backgroundVariant,
                                        height=780)
        self.reques_asignado.pack(side=ctk.LEFT, padx=4, pady=(4,0), fill="both", expand=True)

        self.reques_miembros = ctk.CTkFrame(self.reques_frame,
                                            fg_color=style.Colores.backgroundVariant,
                                        height=780)
        self.reques_miembros.pack(side=ctk.LEFT, padx=4, pady=(4,0), fill="both", expand=True)

        
        ##Objetos de tab3(ESTIMACIÓN)
        self.principal = ctk.CTkFrame(master=self.tab3,
                                      fg_color=style.Colores.backgroundVariant,
                                      border_width=3,
                                      border_color=style.Colores.Gray[4])
        self.principal.pack(fill="both",expand=True)

        estimacion = ctk.CTkLabel(self.principal,
                                        text="Generar estimación completa", 
                                        text_color = style.Subtitulo.text_color,
                                        font = style.Titulo.font)
        estimacion.pack(padx=10, pady=(5,8))
        cuerpo = ctk.CTkLabel(self.principal,
                                        text="Para generar la estimación, llene los siguientes campos:", 
                                        text_color = style.Texto.text_color,
                                        font = style.Subtitulo.font)
        cuerpo.pack(padx=10, pady=7)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Jornadas por mes de Jefe de proyecto -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        jornadas_JP = ctk.CTkEntry(self.principal,
                                    placeholder_text="Número...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        jornadas_JP.pack(padx=200, pady=5)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Jornadas por mes de Administradores -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        jornadas_ADMIN = ctk.CTkEntry(self.principal,
                                    placeholder_text="Número...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        jornadas_ADMIN.pack(padx=200, pady=5)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Jornadas por mes de Desarrolladores -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        jornadas_DEV = ctk.CTkEntry(self.principal,
                                    placeholder_text="Número...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        jornadas_DEV.pack(padx=200, pady=5)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Duración del proyecto (en meses) -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        duracion = ctk.CTkEntry(self.principal,
                                    placeholder_text="MESES...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        duracion.pack(padx=200, pady=5)

        estimar = ctk.CTkButton(self.principal,
                                width=25, 
                                height=25, 
                                text="Estimar Proyecto",
                                text_color = style.BotonGrande.text_color,
                                fg_color = style.BotonGrande.fg_color,
                                font = style.BotonGrande.font,
                                corner_radius = style.BotonGrande.corner_radius,
                                hover_color = style.BotonGrande.hover_color)
        estimar.pack(pady=10)
    
    def GenerarEstimacion(self, jornadas_jp, jornadas_admin, jornadas_dev, duracion):
        """
        Función para generar la estimación del proyecto
        """
        


    def contenido_subpanel(self):
        self.proyecto_actual = ctk.CTkLabel(self.top_subpanel, 
                                            text="Selecciona o crea un proyecto", 
                                            text_color = style.Titulo.text_color,
                                            font = style.Titulo.font)
        self.proyecto_actual.pack(side=ctk.TOP)

    def Update_reqs(self): #Función para actualizar en pantalla los requerimientos de la base de datos
        print(self.ID_activo)
        self.documento = db['Projects'].find_one({'owner': self.user_email, 'id': self.ID_activo})
        if self.documento:
            self.object_id = self.documento['_id']
        else:
            print("No se encontró el proyecto")
            return

        self.reques_proyecto_actual, lista_componentes = Req.ObtenerRequerimientos(self.object_id)
        if self.reques_proyecto_actual == [] or None:
            for widget in self.reques_texto.winfo_children():
                widget.destroy()
            for widget in self.reques_asignado.winfo_children():
                widget.destroy()
            for widget in self.reques_miembros.winfo_children():
                widget.destroy()
            self.reque_label = ctk.CTkLabel(self.reques_texto, 
                                            text="El proyecto aún no posee requerimientos", 
                                            text_color = style.Texto.text_color,
                                            font = style.Texto.font)
            self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)
        else:
            for widget in self.reques_texto.winfo_children():
                widget.destroy()
            for widget in self.reques_asignado.winfo_children():
                widget.destroy()
            for widget in self.reques_miembros.winfo_children():
                widget.destroy()

            for req in self.reques_proyecto_actual:
                if req[2] is None:
                    miembro_asignado = "Miembro no asignado"
                else:
                    miembro_asignado = req[2]
                self.reque_label = ctk.CTkLabel(self.reques_texto, text=f"- ID: {req[0]}. Descripción: {req[1]}",
                                                height=30,
                                                text_color = style.Texto.text_color,
                                                font = style.Texto.font)
                self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)
                
                self.req_mem = ctk.CTkLabel(self.reques_asignado, text="Miembro Asignado: ",
                                                height=30,
                                                text_color = style.Texto.text_color,
                                                font = style.Texto.font)
                self.req_mem.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)

                self.req_member = ctk.CTkLabel(self.reques_miembros, text=miembro_asignado,
                                                height=30,
                                                text_color = style.Texto.text_color,
                                                font = style.Texto.font)
                self.req_member.pack(side=ctk.TOP, anchor=ctk.NW, pady=5)

    def contenido_image(self): #Imagen compañía
        # Obtener la ruta absoluta del directorio actual del script
        frame = ctk.CTkFrame(self.topimage, fg_color=style.Colores.backgroundVariant, corner_radius=0)
        frame.pack()

        cerrarSesion_button = ctk.CTkButton(frame, 
                                                text="Cerrar Sesión", 
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color, 
                                                command=self.Salir)
        cerrarSesion_button.pack(padx=5, pady=5, side="left")


        nombreUsuario = ctk.CTkLabel(frame, text=self.user_email, font=("Segoe UI", -16))
        nombreUsuario.pack(padx=5, pady=5, side="left")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
        logo = ctk.CTkImage(light_image=Image.open(logo_path), 
                            dark_image=Image.open(logo_path),
                            size=(60, 60), )
        logo_label = ctk.CTkLabel(frame, 
                                  image=logo, 
                                  text="", 
                                  bg_color=style.Colores.backgroundVariant)
        logo_label.pack(padx=5, pady=5, side="left")
    
    def Salir(self):
        self.destroy()
        inicio.Welcome()

    def ListarProyectosExistentes(self): #Funcion que busca y lista los proyectos del usuario
        nombres = Proj.ObtenerNombresProyecto(self.user_email)
        for nombre in nombres:
            nombre_proyecto = nombre
            self.proyecto_id = Proj.ObtenerIdProyecto(self.user_email, nombre_proyecto)
            texto = f"{nombre_proyecto}"
            self.new_proyect = ctk.CTkButton(self.proyectos, 
                                         text=texto,
                                         text_color = style.BotonNormal.text_color,
                                         fg_color = style.BotonNormal.fg_color,
                                         font = style.BotonNormal.font,
                                         corner_radius = style.BotonNormal.corner_radius,
                                         hover_color = style.BotonNormal.hover_color,
                                         width=200, 
                                         height=65,
                                         command=partial(self.cambiar_proyecto, nombre_proyecto))
            self.new_proyect.pack(side=ctk.TOP, pady=10)

    def ListarProyectosInvitados(self): #Funcion que busca y lista los proyectos invitados del usuario
        proyectos_aceptados = INV.ObtenerProyectosAceptados(self.user_email)
        for proyecto in proyectos_aceptados:
            self.agregar_boton_proyecto(proyecto["nombre_proyecto"])
        

    def agregar_boton_proyecto(self, nombre_proyecto):#Botón para agregar los proyectos a los que te invitaron
        texto = f"{nombre_proyecto}"
        self.Nombre_Proyecto_Invitado = nombre_proyecto
        self.proyecto_inv = ctk.CTkButton(self.otros_proyectos, 
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
                                          command=partial(self.SwitchWindow, self.Nombre_Proyecto_Invitado))
        self.proyecto_inv.pack(side=ctk.TOP, pady=10, fill="x")

    def SwitchWindow(self, nombre_proyecto):
        proj = db['Invitaciones'].find_one({'nombre_proyecto' : nombre_proyecto, 'correo_invitado' : self.user_email})
        print(proj['rol'])

        #Buscamos y guardamos en variables los datos del proyecto
        self.objectId_Proy_invitado = db['Projects'].find_one({'owner': proj['owner_proyecto'], 'id': proj['proyecto_id']})['_id']#ObjectId para buscar la coleccion de requerimientos del proyecto
        self.objectId_Proy_invitado = ObjectId(self.objectId_Proy_invitado)
        self.Nombre_Proyecto_Invitado = db['Projects'].find_one({'owner': proj['owner_proyecto'], 'id': proj['proyecto_id']})['nombre']
        self.data_proyecto =  Proj.ObtenerDatosProyecto(proj["owner_proyecto"], Proj.ObtenerIdProyecto(proj["owner_proyecto"], self.Nombre_Proyecto_Invitado))
        self.miembros_proyecto = []
        for name in self.data_proyecto[1]:
            self.miembros_proyecto.append(name[0])
        self.miembros_proyecto.append(proj["owner_proyecto"])
        print(self.miembros_proyecto)
        if proj['rol'] == "Administrador":
            self.iconify()
            self.nueva = ADMIN.JP(self, self.user_email, self.Nombre_Proyecto_Invitado, self.objectId_Proy_invitado, self.miembros_proyecto)
        elif proj['rol'] == "Desarrollador":
            self.iconify()
            self.nueva = DEV.Dev(self, self.user_email, self.Nombre_Proyecto_Invitado, self.objectId_Proy_invitado)  # Pasar la referencia de la ventana principal
        else:
            print(f"Ocurrió un problema al buscar el rol en el proyecto {self.Nombre_Proyecto_Invitado}")
        

    def crear_proyecto2(self): #Crea el botón de proyecto activo en el lateral
        self.proyecto_id = Proj.ObtenerIdProyecto(self.user_email, self.Nombre_Proyecto)
        nombre_proyecto = Proj.ObtenerDatosProyecto(self.user_email, self.proyecto_id)
        nombre_proyecto = nombre_proyecto[0]
        texto = f"{nombre_proyecto}"
        self.new_proyect = ctk.CTkButton(self.proyectos, 
                                         text=texto,
                                         text_color = style.BotonNormal.text_color,
                                         fg_color = style.BotonNormal.fg_color,
                                         font = style.BotonNormal.font,
                                         corner_radius = style.BotonNormal.corner_radius,
                                         hover_color = style.BotonNormal.hover_color,
                                         width=200, 
                                         height=65,
                                         command=partial(self.cambiar_proyecto, nombre_proyecto))
        self.new_proyect.pack(side=ctk.TOP, pady=10)

    def crear_proyecto(self): #Ventana para crear un proyecto
        self.participantes_entries = []
        self.window = ctk.CTkToplevel(self)
        self.window.configure(fg_color=style.Colores.background)
        centrarVentana(self.window, 800, 500)

        self.after(100, lambda: self.window.state("zoomed"))
        self.window.title("Crear un proyecto")
        self.window.attributes('-topmost' , 1)
        self.window.focus()

        titulo = ctk.CTkLabel(self.window,
                                text="Crear un proyecto nuevo",
                                text_color = style.Titulo.text_color,
                                font = style.MegaTitulo.font)
        titulo.pack(side=ctk.TOP, pady=5, anchor=ctk.NW)

        subtitulo = ctk.CTkLabel(self.window, 
                                    text="Llena los campos con la información de tu proyecto", 
                                    text_color = style.Titulo.text_color,
                                    font = style.Subtitulo.font)
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
        participantes_emails = [entry.get() for entry in self.participantes_entries]
        participantes_roles = [rol.get() for rol in self.participantes_rol]
        self.Nombre_Proyecto = self.nombre_entry.get()
        if self.Nombre_Proyecto == "":
            messagebox.showerror("Error","Debes asignar un nombre al proyecto", parent=self.window)
            return
        for correo in participantes_emails:
            user = User.BuscarUsuario(correo)
            if user == False:
                messagebox.showerror("Error",f"El usuario con correo '{correo}' no existe.", parent=self.window)
                return
        
        miembros = [(miembro, rol) for miembro, rol in zip(participantes_emails, participantes_roles)]

        Proj.CrearNuevoProyecto(self.Nombre_Proyecto, miembros, self.user_email)
        Proj.AumentarProyectos(self.user_email)
        # Enviar invitaciones
        proyecto_id = Proj.ObtenerIdProyecto(self.user_email, self.Nombre_Proyecto)
        for correo, rol in zip(participantes_emails, participantes_roles):
            INV.IngresarInvitacion(self.user_email, proyecto_id, correo, rol, "pendiente")

        self.window.withdraw()
        win = self.mostrar_ventana_emergente("Proyecto creado exitosamente")
        win.title("Éxito")
        self.participantes_entries = []
        participantes_emails = []
        participantes_roles = []
        self.participantes_rol = []
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
        self.data_cambiar = Proj.ObtenerDatosProyecto(self.user_email, Proj.ObtenerIdProyecto(self.user_email, texto))
        self.ID_activo = Proj.ObtenerIdProyecto(self.user_email, texto)
        self.miembros = self.data_cambiar[1]
        for miembro in self.miembros:
            self.miembro_label = ctk.CTkLabel(self.tab1, text="- Correo: " + miembro[0] + ". Rol: " + miembro[1], 
                                              text_color = style.Texto.text_color,
                                              font = style.Texto.font,)
            self.miembro_label.pack(side=ctk.TOP, 
                                    anchor=ctk.NW,
                                    padx = 5,
                                    pady = 5)

        #Paso 2: Listar los requerimientos del proyecto.
        self.documento = db['Projects'].find_one({'owner': self.user_email, 'id': self.ID_activo})
        if self.documento:
            self.object_id = self.documento['_id']
        else:
            print("No se encontró el proyecto")

        self.reques_proyecto_actual, lista_componentes = Req.ObtenerRequerimientos(self.object_id)
        if self.reques_proyecto_actual == [] or None:
            for widget in self.reques_texto.winfo_children():
                widget.destroy()
            for widget in self.reques_asignado.winfo_children():
                widget.destroy()
            for widget in self.reques_miembros.winfo_children():
                widget.destroy()

            self.reque_label = ctk.CTkLabel(self.reques_texto, 
                                            text="El proyecto aún no posee requerimientos", 
                                            text_color = style.Texto.text_color,
                                            font = style.Texto.font)
            self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW)
        else:
            for widget in self.reques_texto.winfo_children():
                widget.destroy()
            for widget in self.reques_asignado.winfo_children():
                widget.destroy()
            for widget in self.reques_miembros.winfo_children():
                widget.destroy()

            for req in self.reques_proyecto_actual:
                if req[2] is None:
                    miembro_asignado = "Miembro no asignado"
                else:
                    miembro_asignado = req[2]
                self.reque_label = ctk.CTkLabel(self.reques_texto, text=f"- ID: {req[0]}. Descripción: {req[1]}",
                                                height=30,
                                                text_color = style.Texto.text_color,
                                                font = style.Texto.font)
                self.reque_label.pack(side=ctk.TOP, anchor=ctk.NW, pady=5)

                self.req_mem = ctk.CTkLabel(self.reques_asignado, text="Miembro Asignado: ",
                                                height=30,
                                                text_color = style.Texto.text_color,
                                                font = style.Texto.font)
                self.req_mem.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)

                self.req_member = ctk.CTkLabel(self.reques_miembros, text=miembro_asignado,
                                                height=30,
                                                text_color = style.Texto.text_color,
                                                font = style.Texto.font)
                self.req_member.pack(side=ctk.TOP, anchor=ctk.NW, pady=5)
        #Paso 3: Visualizar la estimación del proyecto.
        for widget in self.principal.winfo_children():
                widget.destroy()
        cuerpo = ctk.CTkLabel(self.principal,
                                        text="Para generar la estimación, llene los siguientes campos:", 
                                        text_color = style.Texto.text_color,
                                        font = style.Subtitulo.font)
        cuerpo.pack(padx=10, pady=7)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Jornadas por mes de Jefe de proyecto -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        self.jornadas_JP = ctk.CTkEntry(self.principal,
                                    placeholder_text="Número...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        self.jornadas_JP.pack(padx=200, pady=5)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Jornadas por mes de Administradores -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        self.jornadas_ADMIN = ctk.CTkEntry(self.principal,
                                    placeholder_text="Número...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        self.jornadas_ADMIN.pack(padx=200, pady=5)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Jornadas por mes de Desarrolladores -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        self.jornadas_DEV = ctk.CTkEntry(self.principal,
                                    placeholder_text="Número...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        self.jornadas_DEV.pack(padx=200, pady=5)

        cuerpo = ctk.CTkLabel(self.principal,
                                        text="----- Duración del proyecto (en meses) -----", 
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font)
        cuerpo.pack(padx=10, pady=10)

        self.duracion = ctk.CTkEntry(self.principal,
                                    placeholder_text="MESES...",
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    width=75)
        self.duracion.pack(padx=200, pady=5)

        estimar = ctk.CTkButton(self.principal,
                                width=25, 
                                height=25, 
                                text="Estimar Proyecto",
                                text_color = style.BotonGrande.text_color,
                                fg_color = style.BotonGrande.fg_color,
                                font = style.BotonGrande.font,
                                corner_radius = style.BotonGrande.corner_radius,
                                hover_color = style.BotonGrande.hover_color,
                                command = self.Estimar_Proyecto)
        estimar.pack(pady=10)


    def Estimar_Proyecto(self):#Función que realiza la estimación del proyecto, generando un PDF
        # Puntos de función totales: suma_de_pf_componentes
        PF_Total = Req.CalcularpfTotal(self.object_id)

        # Obtener total Factor de ajuste de complejidad
        tabla_vac = self.data_cambiar[3]
        Total_VAC = sum(tabla_vac.values())
        print(f"Total VAC: {Total_VAC}")

        # PFA = PF * (0.65 + 0.01 * FAC)
        pfa = PF_Total * (0.65 + (0.01 * Total_VAC))
        print(f"pfa: {pfa}")

        # Jornadas por mes de los miembros
        jornadas_jefe = int(self.jornadas_JP.get())
        jornadas_admin = int(self.jornadas_ADMIN.get())
        jornadas_dev = int(self.jornadas_DEV.get())
        
        # Duración del proyecto
        duracion = int(self.duracion.get())

        # PF por mes= PFA/duración
        PF_mes = pfa/duracion
        print(f"PF_mes: {round(PF_mes, 2)}")

        # jornadas totales al mes por roles del equipo (equipo de trabajo)
        ## jornadas_por_mes x Cant_miembro_por_rol
        devs = 0
        admins = 0
        for miembro in self.miembros:
            if miembro[1] == "Desarrollador":
                devs += 1
            else:
                admins += 1
        print(devs)
        print(admins)
        #corresponde a las jornadas al mes por rol
        jornadas_totales_jefe = jornadas_jefe * duracion
        jornadas_totales_admin = (jornadas_admin * admins) * duracion
        jornadas_totales_dev = (jornadas_dev * devs) * duracion

        # Producción de PF por jornada por rol
        ## PF_mes / jornadas_totales_por_mes
        pf_jornada_jefe = round(PF_mes / jornadas_totales_jefe, 2) #pf por jornada
        pf_jornada_admin = round(PF_mes / jornadas_totales_admin, 2)
        pf_jornada_dev = round(PF_mes / jornadas_totales_dev, 2)

        # Sueldos de los miembros por rol
        sueldos_proyecto = sueldos.ObtenerSueldos(self.object_id)

        # Crear un diccionario para roles
        roles = {miembro[0]: miembro[1] for miembro in self.miembros}

        sueldo_total_devs = 0
        sueldo_total_admins = 0
        sueldo_jefe_proyecto = 0

        for persona in sueldos_proyecto:
            email = persona[0]
            sueldo = persona[1]

            if email in roles:
                if roles[email] == "Desarrollador":
                    sueldo_total_devs += sueldo
                    print(f"Miembro_dev: {email}")
                elif roles[email] == "Administrador":
                    sueldo_total_admins += sueldo
                    print(f"Miembro_adm: {email}")
            else:
                sueldo_jefe_proyecto += sueldo
                print(f"Miembro_jefe: {email}")

        print(f"Sueldo total desarrolladores: {sueldo_total_devs}")
        print(f"Sueldo total administradores: {sueldo_total_admins}")
        print(f"Sueldo jefe proyecto: {sueldo_jefe_proyecto}")


        # Total de gastos = sum(sueldos_miembros)
        Total = sueldo_jefe_proyecto + sueldo_total_devs + sueldo_total_admins

        # Costo por unidad de medida = total_gastos/PF_por_mes
        Costo_unidad_de_medida = Total/PF_mes

        # Presupuesto del proyecto
        ## costo_unidad_medida * PFA
        Presupuesto = Costo_unidad_de_medida * pfa
        formateado = f"{Presupuesto:,}"
        print(f"El presupuesto total del proyecto es ${formateado}")
        
        final = f"""Estimación del proyecto '{self.proyecto_actual.cget("text")}':
                                
                - Puntos de función: {PF_Total} PF.
                - Puntos de función ajustados: {pfa} PF.
                - Puntos de función necesarios por mes: {PF_mes} PF.

                - Sueldos: {sueldos_proyecto}.

                - Jornadas totales de trabajo:
                ·) Jornadas jefe de proyecto: {jornadas_totales_jefe}.
                ·) Jornadas administradores: {jornadas_totales_admin}.
                ·) Jornadas desarrolladores: {jornadas_totales_dev}.

                - Productividad esperada por roles del equipo:
                ·) Equipo de desarrollo: {pf_jornada_dev} PF por jornada.
                ·) Equipo de administradores: {pf_jornada_admin} PF por jornada.
                ·) Jefe de proyecto: {pf_jornada_jefe} PF por jornada.

                - Duración: {duracion} meses.

                - Presupuesto total: ${formateado} (CLP)."""
        ventana_Final = ctk.CTkToplevel(self)
        ventana_Final.configure(fg_color=style.Colores.background)
        centrarVentana(ventana_Final, 400, 200)
        ventana_Final.title("Invitación a Proyecto")
        ventana_Final.attributes('-topmost' , 1)
        ventana_Final.after(0, lambda:ventana_Final.state('zoomed'))

        mensaje = final
        etiqueta = ctk.CTkLabel(ventana_Final,
                                text=mensaje,
                                text_color = style.Texto.text_color,
                                font = style.Texto.font,
                                anchor="w",  # Alineación a la izquierda
                                justify="left") # Justificación a la izquierda
        etiqueta.pack(side=ctk.TOP, pady=10, padx=5,anchor=ctk.W)

        final = f"""Estimación del proyecto '{self.proyecto_actual.cget("text")}':
                                
                - Puntos de función: {PF_Total} PF.
                - Puntos de función ajustados: {pfa} PF.
                - Puntos de función necesarios por mes: {PF_mes} PF.

                - Sueldos:

                - Jornadas totales de trabajo:
                    ·) Jornadas jefe de proyecto: {jornadas_totales_jefe}.
                    ·) Jornadas administradores: {jornadas_totales_admin}.
                    ·) Jornadas desarrolladores: {jornadas_totales_dev}.

                - Productividad esperada por roles del equipo:
                    ·) Equipo de desarrollo: {pf_jornada_dev} PF por jornada.
                    ·) Equipo de administradores: {pf_jornada_admin} PF por jornada.
                    ·) Jefe de proyecto: {pf_jornada_jefe} PF por jornada.

                - Duración: {duracion} meses.

Presupuesto total: ${formateado} (CLP)."""

        self.GenerarPDF(final, sueldos_proyecto)


    def GenerarPDF(self,mensaje, sueldos):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font(family="Arial",size=11)

        mensajeSplit = mensaje.split("\n")

        i = 0
        other_i = 0
        for j in range(0, 7):
            pdf.cell(200,10,mensajeSplit[j],
                     ln=i,align="L")
            i += 1
            other_i += 1

        for j in sueldos:
            pdf.cell(200,10,"                    "+str(j),
                     ln=i,align="L")
            i += 1
        
        for j in range(other_i,len(mensajeSplit)):
            if (j == len(mensajeSplit)-1):
                pdf.cell(200,10,mensajeSplit[j],
                     ln=i,align="C")
            else:
                pdf.cell(200,10,mensajeSplit[j],
                         ln=i,align="L")
            i += 1

        pdf.output(name=f"Estimación Proyecto PRO-{self.proyecto_id}.pdf", dest="F")

    def mostrar_ventana_emergente(self, texto):
        ventana_emergente = ctk.CTkToplevel(self)
        ventana_emergente.configure(fg_color=style.Colores.background)
        etiqueta = ctk.CTkLabel(ventana_emergente, 
                                text_color = style.Texto.text_color,
                                font = style.Texto.font,
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
        if (self.object_id == None):
            messagebox.showerror("Error","Debes seleccionar un proyecto primero")
            return
        self.contador = 5
        self.requerimientos = []
        self.ventana_rq = ctk.CTkToplevel(self)
        self.ventana_rq.configure(fg_color="#061d2c")
        centrarVentana(self.ventana_rq, 700, 450)
        self.ventana_rq.title("Añadir Requerimientos")
        self.ventana_rq.attributes('-topmost' , 1)
        self.ventana_rq.focus()
        self.desarrolladores = []
        for miembro in self.miembros:
            if miembro[1] == "Desarrollador":
                self.desarrolladores.append(miembro[0])
        
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

        #Frame para el texto del requerimiento
        self.reques = ctk.CTkFrame(self.REQ, fg_color=style.Colores.backgroundVariant)
        self.reques.pack(side=ctk.LEFT, padx=5, pady=5, anchor=ctk.NW)

        #Frame para el miembro del equipo
        self.member = ctk.CTkFrame(self.REQ, fg_color=style.Colores.backgroundVariant)
        self.member.pack(side=ctk.LEFT, padx=5, pady=5, anchor=ctk.NW)


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

        self.memb = ctk.CTkComboBox(self.member, 
                                    width=300, 
                                    height=35, 
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    values = [person for person in self.desarrolladores]
                                    )
        self.memb.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)

        if self.contador == 5:
            pass
        else:
            self.more_button.pack_configure(pady=(self.contador, 5))

        self.requerimientos.append(self.req)
        self.contador+=45
    
    def reqs_query(self): #Query para ingresar requerimientos al proyecto
        requerimientos = [entry.get() for entry in self.requerimientos]
        #obtenemos el ObjectId del proyecto
        self.documento = db['Projects'].find_one({'owner' : self.user_email, 'id' : self.ID_activo})
        if self.documento:
            self.object_id = self.documento['_id']
            #Mandar la query con los requerimientos
            Req.AgregarRequerimientos(self.object_id, requerimientos)

            self.ventana_rq.withdraw()
            ventanita = self.mostrar_ventana_emergente("Requerimientos agregados exitosamente.")
            ventanita.title("Éxito")
            cerrar = ctk.CTkButton(ventanita, 
                                text="Aceptar",
                                text_color = style.BotonNormal.text_color,
                                fg_color = style.BotonNormal.fg_color,
                                font = style.BotonNormal.font,
                                corner_radius = style.BotonNormal.corner_radius,
                                hover_color = style.BotonNormal.hover_color,
                                command=ventanita.withdraw)
            cerrar.pack(pady=(0,5))
        else:
            print("Documento no encontrado")
            return

        #Reiniciar variables
        requerimientos= []
        self.requerimientos = []
        self.contador = 5

        
        self.Update_reqs()
        print(self.ID_activo)

    
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

        mensaje = f"Has sido invitado por: '{invitacion['owner_proyecto']}'\nAl proyecto: '{invitacion['nombre_proyecto']}'\nCon el rol de: '{invitacion['rol']}'"
        etiqueta = ctk.CTkLabel(ventana_invitacion,
                                text=mensaje,
                                text_color = style.Texto.text_color,
                                font = style.Texto.font,
                                anchor="w",  # Alineación a la izquierda
                                justify="left") # Justificación a la izquierda
        etiqueta.pack(side=ctk.TOP, pady=10, padx=5,anchor=ctk.W)

        aceptar_button = ctk.CTkButton(ventana_invitacion,
                                       text="Aceptar",
                                       text_color = style.BotonNormal.text_color,
                                       fg_color = style.BotonNormal.fg_color,
                                       font = style.BotonNormal.font,
                                       corner_radius = style.BotonNormal.corner_radius,
                                       hover_color = style.BotonNormal.hover_color,
                                       command=lambda: self.responder_invitacion(invitacion, "aceptada"))
        aceptar_button.pack(side=ctk.TOP)
        return ventana_invitacion

    def responder_invitacion(self, invitacion, respuesta):
        self.InvitationWindow.destroy()
        if respuesta == "aceptada":
            db['Invitaciones'].update_one({"_id": invitacion["_id"]}, {"$set": {"estado": respuesta}})
            window = self.mostrar_ventana_emergente(f"Invitación {respuesta}")
            window.title("Éxito")
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
            for widget in self.otros_proyectos.winfo_children():
                widget.destroy()
            self.ListarProyectosInvitados()

    def editar_miembro_asignado(self):
        if (self.object_id == None):
            messagebox.showerror("Error","Debes seleccionar un proyecto primero")
            return

        self.win = ctk.CTkToplevel(self)
        self.win.configure(fg_color=style.Colores.background)
        centrarVentana(self.win, 650, 300)
        self.win.title("Editar")
        self.win.attributes('-topmost' , 1)
        self.win.focus()

        requerimiento = ctk.CTkLabel(self.win, 
                                    text="Seleccionar requerimiento",
                                    text_color = style.Texto.text_color,
                                    font = style.Texto.font)
        requerimiento.grid(row=0, column=0, sticky="w",padx=5)

        miembro = ctk.CTkLabel(self.win, 
                            text="Seleccionar miembro",
                            text_color = style.Texto.text_color,
                            font = style.Texto.font)
        miembro.grid(row=1, column=0, sticky="w", padx=5)

        self.reques_box = ctk.CTkComboBox(self.win, 
                                    width=250, 
                                    height=30, 
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    border_width=2,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    values = [req[1] for req in self.reques_proyecto_actual])
        self.reques_box.grid(row=0, column = 1)
        self.reques_box.set("Selecciona un requerimiento")

        self.miembro_box = ctk.CTkComboBox(self.win, 
                                    width=250, 
                                    height=30, 
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    border_width=2,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius,
                                    values = [person[0] for person in self.miembros if person[1] == "Desarrollador"]
                                    )
        self.miembro_box.grid(row=1, column = 1)
        self.miembro_box.set("Selecciona un miembro")

        asignar_miembro = ctk.CTkButton(self.win,
                                        text="Asignar Miembro",
                                        text_color = style.BotonNormal.text_color,
                                        fg_color = style.BotonNormal.fg_color,
                                        font = style.BotonNormal.font,
                                        corner_radius = style.BotonNormal.corner_radius,
                                        hover_color = style.BotonNormal.hover_color,
                                        command=self.switch_project)
        asignar_miembro.grid(row=2, column=0, sticky="ew")

    def switch_project(self):
        Req.AsignarMiembro(self.object_id, self.miembro_box.get(), self.reques_box.get())
        self.Update_reqs()



