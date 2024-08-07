#################################v2
from textwrap import fill
import tkinter
from xml.dom import HierarchyRequestErr
import customtkinter as ctk
from tkinter import Tk, ttk, Toplevel, StringVar, messagebox
import Clases.Componentes.Estilos as style
import BaseDeDatos.ReqCompQuery as Req
#creamos la clase ventana para el jefe de proyecto
class Dev(ctk.CTkToplevel):
    def __init__(self, parent, user, proyecto, id_proyecto):
        super().__init__(parent)
        self.parent = parent 
        self.user = user
        self.proyecto = proyecto
        self.id_proyecto = id_proyecto

        self.next_row_id = 1  # ID inicial para las filas
        self.filas = [] #Información filas

        #Listamos los requerimientos del proyecto, asignados al miembro
        self.lista_requerimientos, self.lista_componentes = Req.ObtenerRequerimientos(self.id_proyecto)
        self.filasReq = []
        for reque in self.lista_requerimientos:
            if reque[2] == self.user:
                if reque[3] == False:
                    estado = "Pendiente"
                else:
                    estado = "Revisado"
                self.filasReq.append(
                    {"ID": reque[0],
                    "Descripción": reque[1],
                    "Estado": estado
                    }
                )
            else:
                continue

        self.filasComponentes = []
        for comp in self.lista_componentes:
            for fila in self.filasReq:
                if (comp[0] == fila["ID"]):
                    self.filasComponentes.append({"IDReq": comp[0],
                                                  "ID": comp[1],
                                                  "Descripción": comp[2],
                                                  "Tipo":comp[3], 
                                                  "Atributos": comp[4], 
                                                  "Complejidad": comp[5], 
                                                  "Puntos de Función": comp[6], 
                                                  "Puntos de Función Personalizados" : comp[7],
                                                  "Razon": comp[8]})
        #Listamos las tareas asignadas al usuario (IMPLEMENTAR)
        self.filasTareas = [{"ID": "TAR-001", "Descripción": "Descripción Tarea 1", "Estado": "Pendiente"},
                            {"ID": "TAR-002", "Descripción": "Descripción Tarea 2", "Estado": "Realizada"}]
        
        self.complejidad = 0 #Complejidad
        self.geometry("1200x560")
        self.title("PaltaEstimateApp")
        self.Paneles()

        self.contenido_body()
        self.after(0, lambda:self.state('zoomed'))

        self.mainloop() 
    
    def Paneles(self):
        
        #cuerpo principal
        self.body = ctk.CTkFrame(self, fg_color=style.Colores.backgroundVariant, corner_radius=0)
        self.body.pack(side="right", fill="both", expand=True)
        

    
    
    #INICIAIZAR TABLAS----------------------------------------------------------------------------------
    def contenido_body(self):
        nombre_proyecto = ctk.CTkLabel(self.body,
                                        text=self.proyecto, 
                                        text_color = style.Titulo.text_color,
                                        font = style.Titulo.font)
        nombre_proyecto.pack(anchor=ctk.CENTER, pady=5)
        #Creamos TabView
        tabview = ctk.CTkTabview(master=self.body,
                                 fg_color=style.Colores.backgroundVariant2,
                                 segmented_button_fg_color=style.Colores.backgroundVariant2,
                                 segmented_button_selected_color=style.BotonNormal.fg_color,
                                 segmented_button_selected_hover_color=style.BotonNormal.hover_color,
                                 segmented_button_unselected_color=style.BotonSecundario.fg_color,
                                 segmented_button_unselected_hover_color=style.BotonSecundario.hover_color,)
        tabview.pack(padx=5, pady=5, fill="both", expand=True)
        #Agregamos Tabs
        self.tab2 = tabview.add("Requerimientos")
        self.tab1 = tabview.add("Agregar componentes")  
        self.tab3 = tabview.add("Tareas")
          
        
        ## Crear la tabla en la pestaña "Integrantes"
        self.create_table1(self.tab1)

        ## Crear la tabla en la pestaña "Requerimientos"
        self.create_table2(self.tab2)
        
        ## Crear la tabla en la pestaña "Tareas"
        self.create_table3(self.tab3)

    #TABLA PUNTOS DE FUNCIÓN----------------------------------------------------------------------------------
    def create_table1(self, parent):
        columns = ("col1", "col2", "col3", "col4", "col5", "col6","col7")

        # Crear un nuevo estilo
        custom_style = ttk.Style()
        
        # Configurar el estilo de la Treeview
        custom_style.configure("Custom.Treeview", 
                                background=style.BotonLista.fg_color,  # Cambiar el color de fondo
                                foreground=style.BotonLista.text_color,  # Cambiar el color del texto
                                font=("Helvetica", 11),  # Cambiar la fuente y tamaño del texto
                                highlightthickness=0,  # Eliminar el borde de resaltado
                                borderwidth=0,   # Eliminar el ancho del borde
                                rowheight=30)  #Permite que no se bugee el alto de las tablas al cambiar de ventanas.

        self.tree = ttk.Treeview(parent, columns=columns, show='headings', style="Custom.Treeview")
        self.tree.heading("col1", text="IDReq", anchor="center",)  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col2", text="ID", anchor="center", )  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col3", text="Descripción", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col4", text="Tipo", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col5", text="Número Atributos", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col6", text="Complejidad", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col7", text="Puntos de Función", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.pack(fill="both", expand=True, padx=10, pady=10 )
        
        
        
        # Configurar la alineación de las columnas de datos
        for col in columns:
            self.tree.column(col, anchor="center", )  # Centrar los valores de las columnas

        # Frame para contener los botones
        button_frame = ctk.CTkFrame(parent, fg_color=style.Colores.backgroundVariant2)
        button_frame.pack(pady=10)

        #BOTONES
        detalles_button = ctk.CTkButton(button_frame, text="Detalles",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.MostrarDetalles)
        detalles_button.grid(row=0, column=1, padx=5)

        update_db_button = ctk.CTkButton(button_frame, text="Ajustar Puntos de Función",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.AbrirVentanaModificarReglaEstimacion)
        update_db_button.grid(row=0, column=2, padx=5)

        cerrar = ctk.CTkButton(button_frame, text="Cerrar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.close_window)
        cerrar.grid(row=0, column=3, padx=5)

        return self.inicializar_componentes()
    
    def MostrarDetalles(self):
        row = self.tree.item(self.tree.focus(), "values")
        if (not row):
            messagebox.showinfo("Info","No hay detalles que mostrar")
            return

        originalComp = ""
        for comp in self.lista_componentes:
            if (comp[1] == row[1]):
                originalComp = comp
                break

        popup = ctk.CTkToplevel()
        popup.title("Detalles")

        # Agregar contenido a la ventana emergente (ejemplo)
        titulo = ctk.CTkLabel(popup, text=f"Razón de modificación \n de los puntos de función:", font=style.Titulo.font)
        titulo.pack(padx=20, pady=20)

        label = ctk.CTkLabel(popup,
                             text=f"{originalComp[8]}",
                             font=style.Texto.font)
        label.pack(padx=20,pady=20)

        cerrar = ctk.CTkButton(popup, text="Cerrar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=lambda: popup.destroy())
        cerrar.pack(padx=20,pady=20)


    def inicializar_requerimientos(self):#Agregar valores por defecto para demo funcionalidad REQUERIMIENTOS
        for req in self.filasReq:
            self.tree2.insert('', 'end', values=(req["ID"], req["Descripción"], req["Estado"], "Ver Componentes"))
    
    def inicializar_tareas(self):#Agregar valores por defecto para demo funcionalidad TAREAS
        for tarea in self.filasTareas:
            self.tree3.insert('', 'end', values=(tarea["ID"], tarea["Descripción"], tarea["Estado"]))

    def inicializar_componentes(self):#Carga los valores a la tabla componente.
        for comp in self.filasComponentes:
            if (comp["Puntos de Función Personalizados"] == ""):
                self.tree.insert('','end',values=(comp["IDReq"],
                                              comp["ID"], 
                                              comp["Descripción"], 
                                              comp["Tipo"], 
                                              comp["Atributos"],
                                              comp["Complejidad"],
                                              comp["Puntos de Función"]))
            else:
                self.tree.insert('','end',values=(comp["IDReq"],
                                              comp["ID"], 
                                              comp["Descripción"], 
                                              comp["Tipo"], 
                                              comp["Atributos"],
                                              comp["Complejidad"],
                                              (str(comp["Puntos de Función Personalizados"])+"*")))
            
            self.next_row_id += 1

    #TABLA REQUERIMIENTOS----------------------------------------------------------------------------------
    def create_table2(self, parent):
        columns = ("col1", "col2", "col3", "col4")

        # Crear un nuevo estilo
        custom_style = ttk.Style()
        
        # Configurar el estilo de la Treeview
        custom_style.configure("Custom.Treeview", 
                                background=style.BotonLista.fg_color,  # Cambiar el color de fondo
                                foreground=style.BotonLista.text_color,  # Cambiar el color del texto
                                font=("Helvetica", 11),  # Cambiar la fuente y tamaño del texto
                                highlightthickness=0,  # Eliminar el borde de resaltado
                                borderwidth=0,   # Eliminar el ancho del borde
                                rowheight=30)  #Permite que no se bugee el alto de las tablas al cambiar de ventanas.)  # Eliminar el ancho del borde
        
        self.tree2 = ttk.Treeview(parent, columns=columns, show='headings', style="Custom.Treeview")
        self.tree2.heading("col1", text="ID", anchor="center",)  # genera automaticamente ID
        self.tree2.heading("col2", text="descripcion", anchor="center")  # descripción
        self.tree2.heading("col3", text="Estado", anchor="center")  # Estados Pendiente y Revisado
        self.tree2.heading("col4", text="Componentes", anchor="center") # Botón para ver los componentes
        
        self.tree2.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar la alineación de las columnas de datos
        for col in columns:
            self.tree2.column(col, anchor="center")  # Centrar los valores de las columnas

        # FRAME para contener los botones
        button_frame = ctk.CTkFrame(parent, fg_color=style.Colores.backgroundVariant2)
        button_frame.pack(pady=10)

        # BOTONES
        editar_estado = ctk.CTkButton(button_frame, text="Editar estado",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.estadoRequerimiento)
        editar_estado.grid(row=0, column=3, padx=5)

        cerrar = ctk.CTkButton(button_frame, text="Cerrar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.close_window)
        cerrar.grid(row=0, column=5, padx=5)

        # Agregar un evento de clic en las celdas de la columna "Componentes"
        self.tree2.bind("<ButtonRelease-1>", self.on_component_click)
              
        return self.inicializar_requerimientos()
    
    def on_component_click(self, event):
        # Obtener la columna en la que se hizo clic
        region = self.tree2.identify('region', event.x, event.y)
        column = self.tree2.identify_column(event.x)

        if region == "cell" and column == "#4":  # Verificar si se hizo clic en la columna "Componentes"
            item = self.tree2.identify('item', event.x, event.y)
            self.ver_componentes(item)

    def AbrirVentanaModificarReglaEstimacion(self):
        row = self.tree.item(self.tree.focus(), "values")
        if (not row):
            return
        
        originalComp = ""
        for comp in self.lista_componentes:
            if (comp[1] == row[1]):
                originalComp = comp
                break
        popup = ctk.CTkToplevel()
        popup.title("Puntos de Función")

        # Agregar contenido a la ventana emergente (ejemplo)
        titulo = ctk.CTkLabel(popup, text=f"Puntos de función de:\n{row[1]}", font=style.Titulo.font)
        titulo.pack(padx=20, pady=20)

        label = ctk.CTkLabel(popup,
                             text=f"Valor original:\n{originalComp[6]}",
                             font=style.Texto.font)
        label.pack(padx=20,pady=20)

        label = ctk.CTkLabel(popup,
                             text=f"Valor anterior:\n{row[6].split('*')[0]}",
                             font=style.Texto.font)
        label.pack(padx=20,pady=20)


        label = ctk.CTkLabel(popup,
                             text=f"Nuevos puntos de función:",
                             font=style.Texto.font)
        label.pack()
        nuevosPuntos = ctk.CTkEntry(popup,
                             placeholder_text=row[6].split('*')[0],
                             font=style.Texto.font)
        nuevosPuntos.pack(padx=20,pady=20)

        label = ctk.CTkLabel(popup,
                             text=f"Razón:",
                             font=style.Texto.font)
        label.pack()
        razon = tkinter.Text(popup, 
                             height=5, 
                             width=25, 
                             wrap="word", 
                             font=style.Texto.font, 
                             bg=style.EntryNormal.fg_color, 
                             fg=style.EntryNormal.text_color,
                             highlightcolor=style.EntryNormal.border_color,
                             highlightbackground=style.EntryNormal.border_color,
                             insertbackground="white",
                             padx=10, 
                             pady=10)
        razon.pack(padx=20,pady=20)

        def Validar():
            try:
                int(nuevosPuntos.get())
            except:
                messagebox.showerror("Error", "Debes ingresar un nuevo valor.")
                return

            try:
                razon.get("1.0", tkinter.END)
            except:
                messagebox.showerror("Error", "Debes ingresar una razón válida.")
                return
            
            if (razon.get("1.0", tkinter.END).strip() == ""):
                messagebox.showerror("Error", "Debes ingresar una razón válida.")
                return

            Req.ModificarPuntosDeFuncion(self.id_proyecto,
                                         row[0],
                                         row[1],
                                         int(nuevosPuntos.get()),
                                         razon.get("1.0", tkinter.END).strip())
            self.tree.item(self.tree.focus(), values=(row[0],
                                                      row[1],
                                                      row[2],
                                                      row[3],
                                                      row[4],
                                                      row[5],
                                                      (nuevosPuntos.get() + "*")))
            for i in range(0,len(self.lista_componentes)):
                if (self.lista_componentes[i][1] == row[1]):
                    self.lista_componentes[i][8] = razon.get("1.0", tkinter.END).strip()
                    break
            popup.destroy()

        agregarComponente_button = ctk.CTkButton(popup, 
                                                text="Guardar", 
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color, 
                                                command=lambda: Validar())
        agregarComponente_button.pack(padx=5, pady=5)

    def ver_componentes(self, item):
        # Crear una ventana emergente CTkToplevel
        popup = ctk.CTkToplevel()
        popup.title("Componentes")

        # Agregar contenido a la ventana emergente (ejemplo)
        label = ctk.CTkLabel(popup, text=f"Componentes del item: {self.tree2.item(item, 'values')[1]}", font=style.Titulo.font)
        label.pack(padx=20, pady=20)
        
        #Frames para posicionar los botones y la tabla
        frame1 = ctk.CTkFrame(popup);
        frame1.pack()
        frame2 = ctk.CTkFrame(popup);
        frame2.pack()

        

        agregarComponente_button = ctk.CTkButton(frame1, 
                                                text="Agregar Componente", 
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color, 
                                                command=lambda: self.agregarComponenteVentana(self.tree2.item(item, 'values')[0]))
        agregarComponente_button.pack(padx=5, pady=5, side="left")

        delete_row_button = ctk.CTkButton(frame1, text="Eliminar Componente",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=lambda: self.eliminar_componente(self.tree2.item(item, 'values')[0]))
        delete_row_button.pack(padx=5, pady=5, side="left")

        #CREACIÓN DE LA TABLA CON COMPONENTES RELACIONADOS.
        columns = ("col1", "col2", "col3", "col4", "col5", "col6","col7")

        # Crear un nuevo estilo
        custom_style = ttk.Style()
        
        # Configurar el estilo de la Treeview
        custom_style.configure("Custom.Treeview", 
                                background=style.BotonLista.fg_color,  # Cambiar el color de fondo
                                foreground=style.BotonLista.text_color,  # Cambiar el color del texto
                                font=("Helvetica", 11),  # Cambiar la fuente y tamaño del texto
                                highlightthickness=0,  # Eliminar el borde de resaltado
                                borderwidth=0,   # Eliminar el ancho del borde
                                rowheight=30)  #Permite que no se bugee el alto de las tablas al cambiar de ventanas.

        self.treeC = ttk.Treeview(frame2, columns=columns, show='headings', style="Custom.Treeview")
        self.treeC.heading("col1", text="IDReq", anchor="center",)  # Configurar el anclaje para que el encabezado esté centrado
        self.treeC.heading("col2", text="ID", anchor="center", )  # Configurar el anclaje para que el encabezado esté centrado
        self.treeC.heading("col3", text="Descripción", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.treeC.heading("col4", text="Tipo", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.treeC.heading("col5", text="Número Atributos", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.treeC.heading("col6", text="Complejidad", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.treeC.heading("col7", text="Puntos de Función", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.treeC.pack(fill="both", expand=True, padx=10, pady=10 )
        
        
        
        # Configurar la alineación de las columnas de datos
        for col in columns:
            self.tree.column(col, anchor="center", )  # Centrar los valores de las columnas


        compRelacionados = []
        for comp in self.lista_componentes:
            if (comp[0] == self.tree2.item(item, 'values')[0]):
               compRelacionados.append(comp)

        for comp in compRelacionados:
            if (comp[7] == ""):
                self.treeC.insert('','end',values=(comp[0],
                                              comp[1], 
                                              comp[2], 
                                              comp[3], 
                                              comp[4],
                                              comp[5],
                                              comp[6]))
            else:
                self.treeC.insert('','end',values=(comp[0],
                                              comp[1], 
                                              comp[2], 
                                              comp[3], 
                                              comp[4],
                                              comp[5],
                                              (str(comp[7])+"*")))
        

    
    #TABLA TAREAS----------------------------------------------------------------------------------
    def create_table3(self, parent):
        columns = ("col1", "col2", "col3")

        # Crear un nuevo estilo
        custom_style = ttk.Style()
        
        # Configurar el estilo de la Treeview
        custom_style.configure("Custom.Treeview", 
                                background=style.BotonLista.fg_color,  # Cambiar el color de fondo
                                foreground=style.BotonLista.text_color,  # Cambiar el color del texto
                                font=("Helvetica", 11),  # Cambiar la fuente y tamaño del texto
                                highlightthickness=0,  # Eliminar el borde de resaltado
                                borderwidth=0,   # Eliminar el ancho del borde
                                rowheight=30)  #Permite que no se bugee el alto de las tablas al cambiar de ventanas.)  # Eliminar el ancho del borde
        
        self.tree3 = ttk.Treeview(parent, columns=columns, show='headings', style="Custom.Treeview")
        self.tree3.heading("col1", text="ID", anchor="center", )  # generado automaticamente ID
        self.tree3.heading("col2", text="Descripción", anchor="center")  # descripción
        self.tree3.heading("col3", text="Estado", anchor="center")  # Estados Pendiente y Revisado
        
        self.tree3.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar la alineación de las columnas de datos
        for col in columns:
            self.tree3.column(col, anchor="center")  # Centrar los valores de las columnas

        # FRAME para contener los botones
        button_frame = ctk.CTkFrame(parent, fg_color=style.Colores.backgroundVariant2)
        button_frame.pack(pady=10)

        # BOTONES
        update_db_button = ctk.CTkButton(button_frame, text="Editar estado",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.estadoTareas)
        update_db_button.grid(row=0, column=3, padx=5)

        cerrar = ctk.CTkButton(button_frame, text="Cerrar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.close_window)
        cerrar.grid(row=0, column=5, padx=5)
              
        return self.inicializar_tareas()

    #FUNCIONES TABLA Tareas----------------------------------------------------------------------------------
    def estadoTareas(self):#VENTANA EMERGENTE PARA EDITAR ESTADO DE UNA TAREA
        # Crear la ventana emergente
        estadoT_window = Toplevel(self)
        estadoT_window.title("Cambiar Estado de la Tarea")

        # Frame para los campos de texto
        frame_entries = ctk.CTkFrame(estadoT_window, fg_color=style.Colores.backgroundVariant)
        frame_entries.pack(padx=10, pady=10, anchor="w")

        # Etiqueta y ComboBox para seleccionar el ID del requerimiento
        id_label = ctk.CTkLabel(frame_entries, text="ID de la Tarea", fg_color=style.Colores.backgroundVariant)
        id_label.grid(row=0, column=0, padx=10, pady=5)

        # ComboBox con los IDs existentes
        existing_ids = [tarea["ID"] for tarea in self.filasTareas]
        id_var = StringVar(value=existing_ids[0])  # Valor por defecto
        id_combo = ttk.Combobox(frame_entries, textvariable=id_var, values=existing_ids, state="readonly")
        id_combo.grid(row=0, column=1, padx=10, pady=5)

        # Etiqueta y radiobuttons para seleccionar el nuevo estado
        estado_label = ctk.CTkLabel(frame_entries, text="Nuevo Estado:", fg_color=style.Colores.backgroundVariant)
        estado_label.grid(row=1, column=0, padx=10, pady=5)

        estado_var = StringVar(value="Pendiente")
        pendiente_radio = ctk.CTkRadioButton(frame_entries, text="Pendiente",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=estado_var, value="Pendiente")
        pendiente_radio.grid(row=1, column=1, padx=10, pady=5)

        revisado_radio = ctk.CTkRadioButton(frame_entries, text="Realizada",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=estado_var, value="Realizada")
        revisado_radio.grid(row=2, column=1, padx=10, pady=5)

        # Botón para confirmar el cambio de estado
        cambiar_button = ctk.CTkButton(frame_entries, text="Cambiar Estado",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=lambda: self.cambiar_estado_tarea(id_combo.get(), estado_var.get(), estadoT_window))
        cambiar_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def cambiar_estado_tarea(self, tarea_id, nuevo_estado, window): #ACTUALIZAR ESTADO EDITADO DE UNA TAREA
        # Buscar el requerimiento en la tabla y actualizar su estado
        for item in self.tree3.get_children():
            values = self.tree3.item(item, 'values')
            if values[0] == tarea_id:
                self.tree3.set(item, column="col3", value=nuevo_estado)
                messagebox.showinfo("Éxito", f"El estado de la tarea {tarea_id} ha sido cambiado a {nuevo_estado}.")
                window.destroy()
                return
        
        # Mostrar un mensaje de error si el ID no se encuentra
        messagebox.showerror("Error", f"No se encontró la tarea con ID {tarea_id}.")
        window.destroy()
    

    def estadoRequerimiento(self): #VENTANA EMERGENTE PARA EDITAR ESTADO DE UN REQUERIMIENTO
        # Crear la ventana emergente
        estado_window = Toplevel(self)
        estado_window.title("Cambiar Estado del Requerimiento")

        # Frame para los campos de texto
        frame_entries = ctk.CTkFrame(estado_window, fg_color=style.Colores.backgroundVariant)
        frame_entries.pack(padx=10, pady=10, anchor="w")

        # Etiqueta y ComboBox para seleccionar el ID del requerimiento
        id_label = ctk.CTkLabel(frame_entries, text="ID del Requerimiento:", fg_color=style.Colores.backgroundVariant)
        id_label.grid(row=0, column=0, padx=10, pady=5)

        # ComboBox con los IDs existentes
        existing_ids = [req["ID"] for req in self.filasReq]
        id_var = StringVar(value=existing_ids[0])  # Valor por defecto
        id_combo = ttk.Combobox(frame_entries, textvariable=id_var, values=existing_ids, state="readonly")
        id_combo.grid(row=0, column=1, padx=10, pady=5)

        # Etiqueta y radiobuttons para seleccionar el nuevo estado
        estado_label = ctk.CTkLabel(frame_entries, text="Nuevo Estado:", fg_color=style.Colores.backgroundVariant)
        estado_label.grid(row=1, column=0, padx=10, pady=5)

        estado_var = StringVar(value="Pendiente")
        pendiente_radio = ctk.CTkRadioButton(frame_entries, text="Pendiente",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=estado_var, value="Pendiente")
        pendiente_radio.grid(row=1, column=1, padx=10, pady=5)

        revisado_radio = ctk.CTkRadioButton(frame_entries, text="Revisado",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=estado_var, value="Revisado")
        revisado_radio.grid(row=2, column=1, padx=10, pady=5)

        # Botón para confirmar el cambio de estado
        cambiar_button = ctk.CTkButton(frame_entries, text="Cambiar Estado",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=lambda: self.cambiar_estado(id_combo.get(), estado_var.get(), estado_window))
        cambiar_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def cambiar_estado(self, req_id, nuevo_estado, window): #ACTUALIZAR ESTADO EDITADO DE UN REQUERIMIENTO
        # Buscar el requerimiento en la tabla y actualizar su estado
        for item in self.tree2.get_children():
            values = self.tree2.item(item, 'values')
            if values[0] == req_id:
                self.tree2.set(item, column="col3", value=nuevo_estado)
                messagebox.showinfo("Éxito", f"El estado del requerimiento {req_id} ha sido cambiado a {nuevo_estado}.")
                window.destroy()
                return
        
        # Mostrar un mensaje de error si el ID no se encuentra
        messagebox.showerror("Error", f"No se encontró el requerimiento con ID {req_id}.")
        window.destroy()


    def agregarComponenteVentana(self, id_req): #VENTANA EMERGENTE PARA AGREGAR NUEVO COMPONENTE A LA TABLA
        # Crear la ventana emergente
        agregarComponente_window = Toplevel(self)

        agregarComponente_window.title("Agregar Fila")

        # Frame para los campos de texto
        frame_entries = ctk.CTkFrame(agregarComponente_window, fg_color=style.Colores.backgroundVariant)
        frame_entries.pack(padx=10, pady=10, anchor="w")

        # Etiquetas para las columnas deseadas
        labels = ["Descripción:", "N° Atributos"]
        self.entries = [StringVar() for _ in labels]

        # Crear campos de entrada y etiquetas
        for i, label in enumerate(labels):
            frame = ctk.CTkFrame(frame_entries, fg_color=style.Colores.backgroundVariant)
            frame.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            ctk.CTkLabel(frame, text=label, ).pack(side="left", padx=(0, 10), )
            ctk.CTkEntry(frame, textvariable=self.entries[i], fg_color=style.Colores.backgroundVariant2).pack(side="left")

        # Agregar los radio buttons debajo de los campos de texto
        role_picker = ctk.CTkLabel(frame_entries, text="Tipo de componente:", text_color=style.BotonNormal.fg_color, font=("Comic Sans", -25, "bold"), fg_color=style.Colores.backgroundVariant)
        role_picker.grid(row=len(labels), column=0, padx=10, pady=10, sticky="w")

        self.radio_var = ctk.StringVar(value="")
        radiobutton_1 = ctk.CTkRadioButton(frame_entries, text="Entrada Externa",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=self.radio_var, value="Entrada Externa")
        radiobutton_1.grid(row=len(labels) + 1, column=0, padx=10, pady=5, sticky="w")
        radiobutton_2 = ctk.CTkRadioButton(frame_entries, text="Salida Externa",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=self.radio_var, value="Salida Externa")
        radiobutton_2.grid(row=len(labels) + 2, column=0, padx=10, pady=5, sticky="w")
        radiobutton_3 = ctk.CTkRadioButton(frame_entries, text="Consulta Externa",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=self.radio_var, value="Consulta Externa")
        radiobutton_3.grid(row=len(labels) + 3, column=0, padx=10, pady=5, sticky="w")
        radiobutton_4 = ctk.CTkRadioButton(frame_entries, text="Archivo lógico Interno",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=self.radio_var, value="Archivo lógico Interno")
        radiobutton_4.grid(row=len(labels) + 4, column=0, padx=10, pady=5, sticky="w")
        radiobutton_5 = ctk.CTkRadioButton(frame_entries, text="Archivo de interfaz externo",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                variable=self.radio_var, value="Archivo de interfaz externo")
        radiobutton_5.grid(row=len(labels) + 5, column=0, padx=10, pady=5, sticky="w")
        # Botón "Agregar"
        ctk.CTkButton(agregarComponente_window, text="Agregar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=lambda: self.agregarComponente(id_req)).pack(pady=10)
    
    def agregarComponente(self, id_req):#AGREGA NUEVO COMPONENTE A LA TABLA
        # Obtener los valores ingresados en los campos de texto
        descripcion = self.entries[0].get()
        num_atributos = self.entries[1].get()

        # Verificar si el número de atributos es un número
        if not num_atributos.isdigit():
            messagebox.showerror("Error", "El número de atributos debe ser un valor numérico.")
            return

        # Obtener el valor seleccionado del radio button
        tipo = self.radio_var.get()

        # Insertar la fila en la tabla
        id_fila = "COM-" + str(self.next_row_id).zfill(3)  # Formatear el ID con ceros a la izquierda
        values = [id_req,id_fila, descripcion, tipo, num_atributos, ""]
        self.tree.insert('', 'end', values=values)
        self.treeC.insert('','end',values=values)

        # Incrementar el contador de filas
        self.next_row_id += 1

        # Reiniciar los campos de texto y el radio button
        self.entries[0].set("")
        self.entries[1].set("")
        self.radio_var.set("")

        # Actualizar la complejidad si es necesario
        self.actualizar_complejidad(self.tree)
        self.actualizar_complejidad(self.treeC)

        # Agregar la nueva fila al diccionario self.filas
        nueva_fila = {
            "IDReq": id_req,
            "ID": id_fila,
            "Descripción": descripcion,
            "Tipo": tipo,
            "Atributos": num_atributos,
            "Clasificación": self.clasificación,
            "Puntos de Función": self.pf
        }
        nuevo_componente = (
            id_req,
            id_fila,
            descripcion,
            tipo,
            num_atributos,
            self.clasificación,
            self.pf
        )
        self.filas.append(nueva_fila)

        self.lista_componentes.append(nuevo_componente)

        # Imprimir el contenido del diccionario self.filas
        
        Req.AgregarComponentes(self.id_proyecto, id_req, nuevo_componente)



    def eliminar_componente(self, id_req):#VENTANA PARA SELECCIONAR Y ELEMINAR UN COMPONENTE DE LA TABLA
        # Crear la ventana emergente para seleccionar la fila a eliminar
        eliminar_window = Toplevel(self)
        eliminar_window.title("Eliminar Componente")

        # Frame para los campos de texto
        frame_entries = ctk.CTkFrame(eliminar_window, fg_color=style.Colores.backgroundVariant)
        frame_entries.pack(padx=10, pady=10, anchor="w")

        # Etiqueta y ComboBox para seleccionar la fila a eliminar
        id_label = ctk.CTkLabel(frame_entries, text="Seleccionar Componente:", fg_color=style.Colores.backgroundVariant)
        id_label.grid(row=0, column=0, padx=10, pady=5)

        # Obtener IDs de todas las filas
        all_ids = [self.treeC.item(item, 'values')[1] for item in self.treeC.get_children()]

        # ComboBox con los IDs existentes
        id_var = StringVar(value=all_ids[0])  # Valor por defecto
        id_combo = ttk.Combobox(frame_entries, textvariable=id_var, values=all_ids, state="readonly")
        id_combo.grid(row=0, column=1, padx=10, pady=5)

        # BOTON "Eliminar"
        eliminar_button = ctk.CTkButton(frame_entries, text="Eliminar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=lambda: self.eliminar_componente_seleccionado(id_req, id_combo.get(), eliminar_window))
        eliminar_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def eliminar_componente_seleccionado(self,id_req, id_seleccionado, window):#ELIMINA UN COMPONENTE DE LA TABLA´
        Req.EliminarComponente(self.id_proyecto,id_req, values)
        # Buscar el item por ID
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            print(values)
            if values[1] == id_seleccionado:
                self.tree.delete(item)  # Eliminar la fila correspondiente
                window.destroy()
                break

        for item in self.treeC.get_children():
            values = self.treeC.item(item, 'values')
            print(values)
            if values[1] == id_seleccionado:
                self.treeC.delete(item)  # Eliminar la fila correspondiente
                messagebox.showinfo("Éxito", f"Se ha eliminado el componente {id_seleccionado} correctamente.")
                window.destroy()
                return
        
        
        # Mostrar un mensaje de error si el ID no se encuentra
        messagebox.showerror("Error", f"No se encontró el componente con ID {id_seleccionado}.")
        window.destroy()


    def actualizar_complejidad(self, tree):#CALCULA LA COMPLEJIDA SEGUN TABLA ESTANDAR PPT4
        for item in tree.get_children():
            values = tree.item(item, 'values')
            
            print(f"Los values son: {values}")
            tipo = values[3]
            num_atributos = int(values[4])

            #VALORES SEGUN TIPO DE COMPONENTE
            if tipo == "Entrada Externa":
                if num_atributos <= 4:
                    tree.set(item, column="col6", value="Baja")
                    tree.set(item, column="col7", value=3)
                    self.clasificación = "Baja"
                    self.pf = 3
                elif num_atributos >= 5 and num_atributos <= 15:
                    tree.set(item, column="col6", value="Media")
                    tree.set(item, column="col7", value=4)
                    self.clasificación = "Media"
                    self.pf = 4
                else:
                    tree.set(item, column="col6", value="Alta")
                    tree.set(item, column="col7", value=6)
                    self.clasificación = "Alta"
                    self.pf = 6

            elif tipo == "Salida Externa":
                if num_atributos <= 5:
                    tree.set(item, column="col6", value="Baja")
                    tree.set(item, column="col7", value=4)
                    self.clasificación = "Baja"
                    self.pf = 4
                elif num_atributos >= 6 and num_atributos <= 19:
                    tree.set(item, column="col6", value="Media")
                    tree.set(item, column="col7", value=5)
                    self.clasificación = "Media"
                    self.pf = 5
                else:
                    tree.set(item, column="col6", value="Alta")
                    tree.set(item, column="col7", value=7)
                    self.clasificación = "Alta"
                    self.pf = 7

            elif tipo == "Consulta Externa":
                if num_atributos <= 4:
                    tree.set(item, column="col6", value="Baja")
                    tree.set(item, column="col7", value=3)
                    self.clasificación = "Baja"
                    self.pf = 3
                elif num_atributos >= 5 and num_atributos <= 15:
                    tree.set(item, column="col6", value="Media")
                    tree.set(item, column="col7", value=4)
                    self.clasificación = "Media"
                    self.pf = 4
                else:
                    tree.set(item, column="col6", value="Alta")
                    tree.set(item, column="col7", value=6)
                    self.clasificación = "Alta"
                    self.pf = 6
            
            elif tipo == "Archivo lógico Interno":
                if num_atributos <= 5:
                    tree.set(item, column="col6", value="Baja")
                    tree.set(item, column="col7", value=7)
                    self.clasificación = "Baja"
                    self.pf = 7
                elif num_atributos >= 6 and num_atributos <= 19:
                    tree.set(item, column="col6", value="Media")
                    tree.set(item, column="col7", value=10)
                    self.clasificación = "Media"
                    self.pf = 10
                else:
                    tree.set(item, column="col6", value="Alta")
                    tree.set(item, column="col7", value=15)
                    self.clasificación = "Alta"
                    self.pf = 15

            if tipo == "Archivo de interfaz externo":
                if num_atributos <= 4:
                    tree.set(item, column="col6", value="Baja")
                    tree.set(item, column="col7", value=5)
                    self.clasificación = "Baja"
                    self.pf = 5
                elif num_atributos >= 5 and num_atributos <= 15:
                    tree.set(item, column="col6", value="Media")
                    tree.set(item, column="col7", value=7)
                    self.clasificación = "Media"
                    self.pf = 7
                else:
                    tree.set(item, column="col6", value="Alta")
                    tree.set(item, column="col7", value=10)
                    self.clasificación = "Alta"
                    self.pf = 10
        

    def mensajeBase(self):#MENSAJE BOTON ACTUALIZAR BASE DE DATOS
        # Mostrar un mensaje de confirmación
        confirmado = messagebox.askokcancel("Confirmación", "¿Desea Actualizar la Base de Datos?")

        # Verificar si se confirmó la acción
        if confirmado:
            # Aquí puedes realizar las acciones que desees después de la confirmación
            print("Datos actualizados correctamente.")
        else:
            # Aquí puedes manejar lo que quieres hacer si se cancela la acción
            print("La actualización de datos fue cancelada.")    

    def close_window(self):
        if self.parent:
            self.parent.deiconify()  # Restaurar la ventana principal
        self.destroy()    

