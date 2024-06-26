from turtle import bgcolor
import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import ttk, font
import textwrap
import re
import os
import Estilos as style

#import Clases.Componentes.Estilos as style
#import BaseDeDatos.UsersQuery as db


#creamos la clase ventana para el jefe de proyecto
class JP(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.n_proyectos = 1 
        self.proyecto_id = 111
        self.geometry("1280x560")
        self.title("PaltaEstimateApp")
        #self.resizable(False, False)
        self.Paneles()
        self.controles_sidebar()
        self.contenido_body()
        #self.contenido_top_panel()
        #self.contenido_subpanel()
        #self.contenido_image()

        

        #self.mainloop() 
    
    def Paneles(self):#FRAMES
        #cuerpo principal
        self.body = ctk.CTkFrame(self, 
                                 fg_color=style.Colores.backgroundVariant, 
                                 corner_radius=0)
        self.body.pack(side="right", fill="both", expand=True)
        #frame que contiene Nombre del proyecto actual
        #self.top_subpanel = ctk.CTkFrame(self.body, 
        #                                 fg_color=style.Colores.backgroundVariant, 
        #                                 height=120, 
        #                                 corner_radius=0)
        #self.top_subpanel.pack(side=ctk.TOP, fill="x", expand=False)
        #frame para la imágen
        #self.topimage = ctk.CTkFrame(self.top_subpanel, 
        #                             fg_color=style.Colores.background, 
        #                             corner_radius=0)
        #self.topimage.pack(side=ctk.RIGHT, expand=False)

    def controles_sidebar(self):
        texto= "PRO-"+str(self.proyecto_id)
        

    def contenido_body(self):
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
        self.tab2 = tabview.add("Complejidad")  
        self.tab3 = tabview.add("Métricas")  
        
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
                                  corner_radius = style.EntryNormal.corner_radius)#Para colocar elementos, solo se especifica el tab
        self.ent63.pack(side=ctk.LEFT, anchor=ctk.NW, padx=5, pady=5)

        #FRAME9
        btnATPF = ctk.CTkButton(frame9, 
                                text="Actualizar tabla",
                                text_color = style.BotonNormal.text_color,
                                fg_color = style.BotonNormal.fg_color,
                                font = style.BotonNormal.font,
                                corner_radius = style.BotonNormal.corner_radius,
                                hover_color = style.BotonNormal.hover_color,
                                command=self.actualizarTablaPF)#Para colocar elementos, solo se especifica el tab
        btnATPF.pack(side=ctk.LEFT, anchor=ctk.NW, pady=20)




        ##-------------------------------------------------------------Objetos de tab2

        #------------FRAMES
        
        frame1_1 = ctk.CTkFrame(master=self.tab2,
                                border_color=style.Colores.backgroundVariant,
                                bg_color=style.Colores.backgroundVariant,
                                fg_color=style.Colores.backgroundVariant)
        frame1_1.pack(side=ctk.LEFT)
        frame2_2 = ctk.CTkFrame(master=self.tab2,
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
        
        
        ##Objetos de tab3

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

    #def contenido_subpanel(self):
    #    texto_boton = self.boton_proyecto.cget("text")#se obtiene la info del proyecto seleccionado, para mostrar en la ventana
    #    self.proyecto_actual = ctk.CTkLabel(self.top_subpanel, text=texto_boton, font=("Comic Sans", -25))
    #    self.proyecto_actual.pack(side=ctk.TOP)

    #def contenido_image(self):
        # Obtener la ruta absoluta del directorio actual del script
    #    current_dir = os.path.dirname(os.path.abspath(__file__))
    #    logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
    #    logo = ctk.CTkImage(light_image=Image.open(logo_path),
    #        size=(60, 60))
    #    logo_label = ctk.CTkLabel(self.topimage, image=logo, text="")
    #    logo_label.pack(padx=5, pady=5)

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
        ventana_emergente.configure(fg_color=style.Colores.background)
        etiqueta = ctk.CTkLabel(ventana_emergente, font=("Arial", -15, "bold"), text_color=style.Colores.Gray[4],
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