from ast import Pass
from turtle import bgcolor
import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import ttk, font
from BaseDeDatos.MainMongoDB import db

import BaseDeDatos.SueldosQuery as sueldos

import textwrap
import re
import os
import Clases.Componentes.Estilos as style
from bson.objectid import ObjectId



#creamos la clase ventana para el jefe de proyecto
class JP(ctk.CTk):
    def __init__(self, parent, user, proyecto, id_proyecto, miembros):
        super().__init__()
        
        self.parent = parent 
        self.user = user
        self.proyecto = proyecto
        self.id_proyecto = id_proyecto
        self.miembros = miembros

        self.geometry("1280x560")
        self.title("PaltaEstimateApp")
        #self.resizable(False, False)
        self.Paneles()
        self.contenido_body()
        
        self.after(0, lambda:self.state('zoomed') )
        self.mainloop() 
    
    def Paneles(self):#FRAMES
        #cuerpo principal
        self.body = ctk.CTkFrame(self, 
                                 fg_color=style.Colores.backgroundVariant, 
                                 corner_radius=0)
        self.body.pack(side="right", fill="both", expand=True)
        

    def contenido_body(self):
        nombre_proyecto = ctk.CTkLabel(self.body,
                                        text=self.proyecto, 
                                        text_color = style.Titulo.text_color,
                                        font = style.Titulo.font)
        nombre_proyecto.pack(anchor=ctk.CENTER, pady=5)
        self.proj = db['Invitaciones'].find_one({'nombre_proyecto' : self.proyecto, 'correo_invitado' : self.user})
        self.rol_usuario = self.proj['rol']
        self.rol = ctk.CTkLabel(self.body,
                            text=self.rol_usuario, 
                            text_color = style.Titulo.text_color,
                            font = style.Subtitulo.font)
        self.rol.pack(anchor = ctk.CENTER, pady = 5, padx= 5)
        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.body, 
                                 height=550,
                                 fg_color=style.Colores.background,
                                 segmented_button_fg_color=style.Colores.background,
                                 segmented_button_selected_color=style.BotonNormal.fg_color,
                                 segmented_button_selected_hover_color=style.BotonNormal.hover_color,
                                 segmented_button_unselected_color=style.BotonSecundario.fg_color,
                                 segmented_button_unselected_hover_color=style.BotonSecundario.hover_color)
        tabview.pack(padx=5, pady=5, fill="both")
        #Agregamos Tabs
        self.tab1 = tabview.add("Tabla PF")  
        self.tab5 = tabview.add("Complejidad")  
        self.tabSueldos = tabview.add("Sueldos")  
        
        ##Objetos de tab1

        vcmd = (self.register(self.callback))

        frame1 = ctk.CTkFrame(master=self.tab1,
                              border_width=0,
                              border_color=style.Colores.background,
                              bg_color=style.Colores.background,
                              fg_color=style.Colores.background)
        frame1.pack(side=ctk.TOP)
        frame2 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.backgroundVariant,
                              bg_color=style.Colores.backgroundVariant,
                              fg_color=style.Colores.backgroundVariant)
        frame2.pack(side=ctk.TOP)
        frame3 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.backgroundVariant,
                              bg_color=style.Colores.backgroundVariant,
                              fg_color=style.Colores.backgroundVariant)
        frame3.pack(side=ctk.TOP)
        frame4 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.backgroundVariant,
                              bg_color=style.Colores.backgroundVariant,
                              fg_color=style.Colores.backgroundVariant)
        frame4.pack(side=ctk.TOP)
        frame5 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.backgroundVariant,
                              bg_color=style.Colores.backgroundVariant,
                              fg_color=style.Colores.backgroundVariant)
        frame5.pack(side=ctk.TOP)
        frame6 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.backgroundVariant,
                              bg_color=style.Colores.backgroundVariant,
                              fg_color=style.Colores.backgroundVariant)
        frame6.pack(side=ctk.TOP)
        frame7 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.backgroundVariant,
                              bg_color=style.Colores.backgroundVariant,
                              fg_color=style.Colores.backgroundVariant)
        frame7.pack(side=ctk.TOP)
        frame8 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.backgroundVariant,
                              bg_color=style.Colores.backgroundVariant,
                              fg_color=style.Colores.backgroundVariant)
        frame8.pack(side=ctk.TOP)
        frame9 = ctk.CTkFrame(master=self.tab1,
                              border_color=style.Colores.background,
                              bg_color=style.Colores.background,
                              fg_color=style.Colores.background)
        frame9.pack(side=ctk.TOP)

        #FRAME1
        self.email_entry = ctk.CTkLabel(frame1, 
                                        text="Tabla de puntos de función", 
                                        state=ctk.DISABLED, 
                                        cursor="arrow",
                                        bg_color=style.Colores.background,
                                        text_color = style.Texto.text_color,
                                        font = style.Texto.font,
                                        width=600, 
                                        corner_radius=4)
        self.email_entry.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)

        #FRAME2

        lblDificultad = ctk.CTkLabel(frame2, 
                                     text="Dificultad", 
                                     state=ctk.DISABLED, 
                                     cursor="arrow", 
                                     text_color=style.Colores.Gray[4], 
                                     fg_color=style.Colores.MainColor[3], 
                                     width=140, 
                                     corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblDificultad.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        lblBaja = ctk.CTkLabel(frame2, text="Baja", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblBaja.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        lblMedia = ctk.CTkLabel(frame2, text="Media", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblMedia.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        lblAlta = ctk.CTkLabel(frame2, text="Alta", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblAlta.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME3
        lblAtributos = ctk.CTkLabel(frame3, text="Atributos", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblAtributos.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent11 = ctk.CTkEntry(frame3, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent11.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent12 = ctk.CTkEntry(frame3, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent12.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent13 = ctk.CTkEntry(frame3, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent13.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME4
        lblEntEx = ctk.CTkLabel(frame4, text="Entrada Externa", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblEntEx.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent21 = ctk.CTkEntry(frame4, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent21.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent22 = ctk.CTkEntry(frame4, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent22.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent23 = ctk.CTkEntry(frame4, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent23.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME5
        lblSalEx = ctk.CTkLabel(frame5, text="Salida externa", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblSalEx.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent31 = ctk.CTkEntry(frame5, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent31.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent32 = ctk.CTkEntry(frame5, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent32.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent33 = ctk.CTkEntry(frame5, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent33.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME6
        lblConEx = ctk.CTkLabel(frame6, text="Consulta externa", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblConEx.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent41 = ctk.CTkEntry(frame6, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent41.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent42 = ctk.CTkEntry(frame6, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent42.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent43 = ctk.CTkEntry(frame6, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent43.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME7
        lblALI = ctk.CTkLabel(frame7, text="Archivo L. interno", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblALI.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent51 = ctk.CTkEntry(frame7, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent51.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent52 = ctk.CTkEntry(frame7, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent52.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent53 = ctk.CTkEntry(frame7, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent53.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME8
        lblALE = ctk.CTkLabel(frame8, text="Archivo L. externo", state=ctk.DISABLED, cursor="arrow", text_color=style.Colores.Gray[4], fg_color=style.Colores.MainColor[3], width=140, corner_radius=4)#Para colocar elementos, solo se especifica el tab
        lblALE.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)
        
        self.ent61 = ctk.CTkEntry(frame8, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent61.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent62 = ctk.CTkEntry(frame8, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent62.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        self.ent63 = ctk.CTkEntry(frame8, 
                                  justify='center',
                                  validate='all', 
                                  validatecommand=(vcmd, '%P'),
                                  fg_color = style.EntryNormal.fg_color,
                                  border_color = style.EntryNormal.border_color,
                                  text_color = style.EntryNormal.text_color,
                                  font = style.EntryNormal.font,
                                  corner_radius = style.EntryNormal.corner_radius)
        self.ent63.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME9
        btnATPF = ctk.CTkButton(frame9, 
                                text="Actualizar tabla",
                                text_color = style.BotonNormal.text_color,
                                fg_color = style.BotonNormal.fg_color,
                                font = style.BotonNormal.font,
                                corner_radius = style.BotonNormal.corner_radius,
                                hover_color = style.BotonNormal.hover_color,
                                command=self.actualizarTablaPF)
        btnATPF.pack(side=ctk.LEFT, anchor=ctk.NW, pady=20)
        cerrar = ctk.CTkButton(frame9, text="Cerrar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.close_window)
        cerrar.pack(side=ctk.LEFT, anchor=ctk.NW, pady=20, padx=10)

        print("tab1")
        self.refrescarTablaPF()




        ##-------------------------------------------------------------Objetos de tab5

        #------------FRAMES
        
        frame1_1 = ctk.CTkFrame(master=self.tab5,
                                border_color=style.Colores.backgroundVariant,
                                bg_color=style.Colores.backgroundVariant,
                                fg_color=style.Colores.backgroundVariant)
        frame1_1.pack(side=ctk.LEFT)
        frame2_2 = ctk.CTkFrame(master=self.tab5,
                                border_color=style.Colores.backgroundVariant,
                                bg_color=style.Colores.backgroundVariant,
                                fg_color=style.Colores.backgroundVariant)
        frame2_2.pack()

        #------------STYLES

        style1 = ttk.Style()
        style1.configure("Treeview.Heading", font=style.Texto.font)
        style1.configure("Treeview", font=style.Texto.font, rowheight=80)
        small_font = font.Font(size=17)

        #------------LISTBOX

        self.selected_element = str()
        listbox = tk.Listbox(frame1_1, 
                             listvariable=self.selected_element, 
                             font=style.Texto.font,
                             height=14, 
                             width=30)
        for item in self.getLista():
            listbox.insert(tk.END, item)

        self.a()
        listbox.bind('<<ListboxSelect>>', self.actualizar_tabla) #al seleccionar un elemento de la lista, actualiza la tabla correspondiente
        listbox.pack(padx=10, pady=10)

        #------------TABLA

        #frame de la tabla
        self.tabla_frame = ctk.CTkFrame(frame2_2, fg_color=style.Colores.background, corner_radius=10)
        self.tabla_frame.pack()


        columns = ("Grado", "Descripción")
        self.tree = ttk.Treeview(self.tabla_frame, 
                                 columns=columns, 
                                 show="headings", 
                                 style="Treeview", 
                                 height=7)
        self.tree.heading("Grado", text="Grado")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.column("Grado", width=200, anchor="center")
        self.tree.column("Descripción", width=900, anchor="w")
        self.tree.tag_configure('monospace')
        self.tree.pack(fill="both")

        self.grado_label = ctk.CTkLabel(frame1_1, text="Grado actual registrado: {a}".format(a=self.currentGrado))
        self.grado_label.pack(pady=2)

        enviar_button = ctk.CTkButton(frame1_1, text="Mandar", command=self.mandar_grado)
        enviar_button.pack(pady=(5,0))

        #------------EXTRAS

        self.cargar_datos_iniciales()
        
        # CONTENIDO NUEVO
        ##Objetos de tab3
        texto_primero = ctk.CTkLabel(self.tabSueldos,
                     text="Tabla de sueldos del equipo",
                     text_color = style.Titulo.text_color,
                     font = style.Subtitulo.font
                     ).pack(pady=10)
        texto_segundo = ctk.CTkLabel(self.tabSueldos,
                     text="Agregar un sueldo nuevo o editar uno existente",
                     text_color = style.Titulo.text_color,
                     font = style.Subtitulo.font
                     ).pack(pady=5, anchor="w")
        self.new_sueldo_frame = ctk.CTkFrame(self.tabSueldos, fg_color="transparent")
        self.new_sueldo_frame.pack(fill="x", expand=True)
        text = ctk.CTkLabel(self.new_sueldo_frame,
                     text="Miembro: ",
                     text_color = style.Texto.text_color,
                     font = style.Texto.font
                     ).pack(side=ctk.LEFT, pady=5)
        self.miembros_box = ctk.CTkComboBox(self.new_sueldo_frame, width=200,
                                  values=[miembro for miembro in self.miembros])
        self.miembros_box.pack(side=ctk.LEFT, pady=5, padx=10)

        salary = ctk.CTkLabel(self.new_sueldo_frame,
                     text="Sueldo: ",
                     text_color = style.Texto.text_color,
                     font = style.Texto.font
                     ).pack(side=ctk.LEFT, pady=5, padx=10)
        
        self.salary_entry = ctk.CTkEntry(self.new_sueldo_frame,
                                    placeholder_text="Ingresa un monto (CLP)...", #Hay que transformarlo a UF para los cálculos
                                    placeholder_text_color="white",
                                    width=350, 
                                    height=35, 
                                    fg_color = style.EntryNormal.fg_color,
                                    border_color = style.EntryNormal.border_color,
                                    text_color = style.EntryNormal.text_color,
                                    font = style.EntryNormal.font,
                                    corner_radius = style.EntryNormal.corner_radius)
        self.salary_entry.pack(side=ctk.LEFT, pady=5, padx=10)

        agregar_boton = ctk.CTkButton(self.new_sueldo_frame,
                                      text="Agregar sueldo",
                                      text_color = style.BotonNormal.text_color,
                                      fg_color = style.BotonNormal.fg_color,
                                      font = style.BotonNormal.font,
                                      corner_radius = style.BotonNormal.corner_radius,
                                      hover_color = style.BotonNormal.hover_color,
                                      command=lambda: self.AgregarSueldo())
        agregar_boton.pack(side=ctk.LEFT, pady=5, padx=10)


        self.Contenido = ctk.CTkScrollableFrame(self.tabSueldos,
                                                fg_color=style.Colores.backgroundVariant,
                                                border_width=3,
                                                border_color=style.Colores.Gray[4])
        self.Contenido.pack(fill="both", expand=True)
        self.sueldos_proyecto = sueldos.ObtenerSueldos(self.id_proyecto)
        print(self.sueldos_proyecto)
        if self.sueldos_proyecto == []:
            texto = ctk.CTkLabel(self.Contenido, text="El proyecto aún no posee sueldos asignados",
                             text_color = style.Titulo.text_color,
                             font = style.Titulo.font).pack(pady=10)
        elif self.sueldos_proyecto == None:
            texto = ctk.CTkLabel(self.Contenido, text="El proyecto aún no posee tabla de sueldos",
                             text_color = style.Titulo.text_color,
                             font = style.Titulo.font).pack(pady=10)
        else:
            for sueldo in self.sueldos_proyecto:
                    texto = ctk.CTkLabel(self.Contenido, text=f"Miembro: {sueldo[0]}.    Sueldo: ${sueldo[1]}",
                                text_color = style.Texto.text_color,
                                font = style.Texto.font).pack(padx=10, pady=5, anchor=ctk.W)
    
    def AgregarSueldo(self):
        sueldos.AgregarSueldo(self.id_proyecto, self.miembros_box.get(), self.salary_entry.get())
        for widget in self.Contenido.winfo_children():
            widget.destroy()
        self.sueldos_proyecto = sueldos.ObtenerSueldos(self.id_proyecto)
        for sueldo in self.sueldos_proyecto:
                    texto = ctk.CTkLabel(self.Contenido, text=f"Miembro: {sueldo[0]}.    Sueldo: ${sueldo[1]}",
                                text_color = style.Texto.text_color,
                                font = style.Texto.font).pack(padx=10, pady=5, anchor=ctk.W)


    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def a(self):
        self.currentGrado = 1

    def getLista(self):
        lista = ["1.   Comunicacion De Datos",
                 "2.   Procesamiento Distribuido",
                 "3.   Objetivos De Rendimiento",
                 "4.   Configuracion Del Equipamiento",
                 "5.   Tasa De Transacciones",
                 "6.   Entrada De Datos En Linea",
                 "7.   Interfase Con El Usuario",
                 "8.   Actualizacion En Linea",
                 "9.   Procesamiento Complejo",
                 "10. Reusabilidad Del Codigo",
                 "11. Facilidad De Implementacion",
                 "12. Facilidad De Operacion",
                 "13. Instalaciones Multiples",
                 "14. Facilidad De Cambios"]
        return lista
    
    def refrescarTablaPF(self):
        #Busca si existe una TablaPF propia del projecto para cargar, de lo contrario, se carga la tabla por defecto.

        tabla = db["TablasPF"].find_one({'projectID':self.id_proyecto}) #Busca si hay una tablaPF con el id del proyecto

        if tabla != None: #Si existe una tabla propia del proyecto, se cargara esta
            pass
        else: #Si no hay tabla propia del proyecto, se carga la por defecto (ESTA SIEMPRE DEBERIA EXISTIR)
            tabla = db["TablasPF"].find_one({'defecto':0})

        #Cargar los datos a pantalla
            
        self.ent11.insert(0,tabla['atributos'][0])
        self.ent12.insert(0,tabla['atributos'][1])
        self.ent13.insert(0,tabla['atributos'][2])

        self.ent21.insert(0,tabla['EI'][0])
        self.ent22.insert(0,tabla['EI'][1])
        self.ent23.insert(0,tabla['EI'][2])

        self.ent31.insert(0,tabla['EO'][0])
        self.ent32.insert(0,tabla['EO'][1])
        self.ent33.insert(0,tabla['EO'][2])

        self.ent41.insert(0,tabla['EQ'][0])
        self.ent42.insert(0,tabla['EQ'][1])
        self.ent43.insert(0,tabla['EQ'][2])
        
        self.ent51.insert(0,tabla['ILF'][0])
        self.ent52.insert(0,tabla['ILF'][1])
        self.ent53.insert(0,tabla['ILF'][2])
        
        self.ent61.insert(0,tabla['ELF'][0])
        self.ent62.insert(0,tabla['ELF'][1])
        self.ent63.insert(0,tabla['ELF'][2])
        
            
    
        
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

        #Comprobar que ningun atributo este vacio

        e=[e11,e12,e13,e21,e22,e23,e31,e32,e33,e41,e42,e43,e51,e52,e53,e61,e62,e63]

        for i in e:
            if i == "":
                print("ERROR: Existen atributos vacios.")
                return 
            if int(i) == 0:
                print("ERROR: No pueden haber atributos con valor 0.")
                return


        #Guardar los datos
            
        tabla = db["TablasPF"].find_one({'projectID':self.id_proyecto}) #Busca si hay una tablaPF con el id del proyecto

        if tabla != None: #Si existe una tabla propia del proyecto, se usara esta
            pass
        else: #Si no hay tabla propia del proyecto, se carga la por defecto (ESTA SIEMPRE DEBERIA EXISTIR)
            db['TablasPF'].insert_one({'projectID':self.id_proyecto, #crea el documento nuevo
                                'defecto':0,
                                'atributos': [],
                                'EI': [],
                                'EO': [],
                                'EQ': [],
                                'ILF': [],
                                'ELF': [],
                                })

        nuevos_valores = {"$set": 
                          {"atributos": [e11,e12,e13],
                           "EI": [e21,e22,e23],
                           "EO": [e31,e32,e33],
                           "EQ": [e41,e42,e43],
                           "ILF": [e51,e52,e53],
                           "ELF": [e61,e62,e63]}}


        resultado = db["TablasPF"].update_one({'projectID':self.id_proyecto}, nuevos_valores) #actualiza los valores del documento
            
        if resultado.matched_count > 0:

            print("Actualizacion exitosa")
        else:
            print("Actualizacion erronea")

        #db.actualizarTablaPF(e)


    def mandar_grado(self): #Manda la query de que se selecciona un grado para la tabla
        curItem = self.tree.focus()
        curGrado = self.tree.item(curItem)["values"][0]
        curTab = self.tab_seleccionada
        #Mandar Query, en la tabla "curTab" se selecciona el curGrado
        print(curTab, curGrado)



    def actualizar_tabla(self, event):
        patron = r'^(.*?)\.'  # El patrón busca cualquier cosa (non-greedy) antes del primer punto
        coincidencia = re.search(patron, event.widget.get(event.widget.curselection()[0]))
        self.tab_seleccionada = coincidencia.group(1)
        print(self.tab_seleccionada)
        self.cargarTabla()

    def cargarTabla(self):
        #realizar query, extraer la tabla N°self.tab_seleccionada de los ajustes de complejidad de la BD y cargarla
        pass

    def cargar_datos_iniciales(self):
        datos = [
            ("0", "Aplicación puramente batch o funciona en una computadora aislada"),
            ("1", "La aplicación es batch, pero utiliza entrada de datos remota o impresión remota"),
            ("2", "La aplicación es batch, pero utiliza entrada de datos remota e impresión remota"),
            ("3", "La aplicación incluye entrada de datos on-line vía entrada de video o un procesador front-end para alimentar procesos batch o sistemas de consultas."),
            ("4", "La aplicación es más que una entrada on-line, y soporta apenas un protocolo de comunicación"),
            ("5", "La aplicación es más que una entrada on-line y soporta más de un protocolo de comunicación")
        ]
        for grado, descripcion in datos:
            self.tree.insert("", tk.END, values=(grado, self.wrap(descripcion))) #con saltos de linea

    def wrap(self,string, lenght=85): #realiza saltos de linea en la fila de largo lenght caracteres
        return '\n'.join(textwrap.wrap(string, lenght))

    def insert_with_line_breaks(self, text):
        lines = text.split("\n")
        for line in lines:
            self.tree.insert(tk.END, line)
    
    def close_window(self):
        if self.parent:
            self.parent.deiconify()  # Restaurar la ventana principal
        self.destroy() 


# appi = JP()
# appi.mainloop()