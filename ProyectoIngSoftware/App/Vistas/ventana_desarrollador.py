#################################v2
from xml.dom import HierarchyRequestErr
import customtkinter as ctk
from tkinter import ttk, Toplevel, StringVar, messagebox
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
        #Listamos los requerimientos del proyecto
        lista_requerimientos = Req.ObtenerRequerimientos(self.id_proyecto)


        """ self.filasReq = [{"ID": "REQ-001", "Descripción": "Descripción del requerimiento 1", "Estado": "Pendiente"},
                        {"ID": "REQ-002", "Descripción": "Descripción del requerimiento 2", "Estado": "Revisado"}]"""
        self.filasReq = []
        for reque in lista_requerimientos:
            if reque[2] == False:
                estado = "Pendiente"
            else:
                estado = "Revisado"
            self.filasReq.append(
                {"ID": f"REQ-{reque[0]}",
                 "Descripción": reque[1],
                 "Estado": estado
                 }
            )

        #Listamos las tareas asignadas al usuario (IMPLEMENTAR)
        self.filasTareas = [{"ID": "TAR-001", "Descripción": "Descripción Tarea 1", "Estado": "Pendiente"},
                            {"ID": "TAR-002", "Descripción": "Descripción Tarea 2", "Estado": "Realizada"}]
        
        self.complejidad = 0 #Complejidad
        self.geometry("1200x560")
        self.title("PaltaEstimateApp")
        self.Paneles()
        #self.controles_sidebar()
        self.contenido_body()
        self.after(0, lambda:self.state('zoomed'))

        #self.contenido_subpanel()
        self.mainloop() 
    
    def Paneles(self):
        
        #cuerpo principal
        self.body = ctk.CTkFrame(self, fg_color=style.Colores.backgroundVariant, corner_radius=0)
        self.body.pack(side="right", fill="both", expand=True)
        

    
    
    #INICIAIZAR TABLAS----------------------------------------------------------------------------------
    def contenido_body(self):
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
        columns = ("col1", "col2", "col3", "col4", "col5", "col6")

        # Crear un nuevo estilo
        custom_style = ttk.Style()
        
        # Configurar el estilo de la Treeview
        custom_style.configure("Custom.Treeview", 
                                background=style.BotonLista.fg_color,  # Cambiar el color de fondo
                                foreground=style.BotonLista.text_color,  # Cambiar el color del texto
                                font=("Helvetica", 11),  # Cambiar la fuente y tamaño del texto
                                highlightthickness=0,  # Eliminar el borde de resaltado
                                borderwidth=0)  # Eliminar el ancho del borde

        self.tree = ttk.Treeview(parent, columns=columns, show='headings', style="Custom.Treeview")
        self.tree.heading("col1", text="ID", anchor="center", )  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col2", text="Componente Funcional", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col3", text="Tipo", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col4", text="Número Atributos", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col5", text="Complejidad", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.heading("col6", text="Puntos de Función", anchor="center")  # Configurar el anclaje para que el encabezado esté centrado
        self.tree.pack(fill="both", expand=True, padx=10, pady=10, )
        
        
        
        # Configurar la alineación de las columnas de datos
        for col in columns:
            self.tree.column(col, anchor="center", )  # Centrar los valores de las columnas
        
        # Frame para contener los botones
        button_frame = ctk.CTkFrame(parent, fg_color=style.Colores.backgroundVariant2)
        button_frame.pack(pady=10)

        # Botones
        agregarComponente_button = ctk.CTkButton(button_frame, 
                                                text="Agregar Componente", 
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color, 
                                                command=self.agregarComponenteVentana)
        agregarComponente_button.grid(row=0, column=0, padx=5)

        delete_row_button = ctk.CTkButton(button_frame, text="Eliminar Componente",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.eliminar_componente)
        delete_row_button.grid(row=0, column=1, padx=5)

        update_db_button = ctk.CTkButton(button_frame, text="Regla de Estimación",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=None)
        update_db_button.grid(row=0, column=2, padx=5)

        estimation_rule_button = ctk.CTkButton(button_frame, text="Actualizar Base de Datos",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.mensajeBase)
        estimation_rule_button.grid(row=0, column=3, padx=5)

        cerrar = ctk.CTkButton(button_frame, text="Cerrar",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.close_window)
        cerrar.grid(row=0, column=4, padx=5)
    
    def inicializar_requerimientos(self):#Agregar valores por defecto para demo funcionalidad REQUERIMIENTOS
        for req in self.filasReq:
            self.tree2.insert('', 'end', values=(req["ID"], req["Descripción"], req["Estado"]))
    
    def inicializar_tareas(self):#Agregar valores por defecto para demo funcionalidad TAREAS
        for tarea in self.filasTareas:
            self.tree3.insert('', 'end', values=(tarea["ID"], tarea["Descripción"], tarea["Estado"]))


    #TABLA REQUERIMIENTOS----------------------------------------------------------------------------------
    def create_table2(self, parent):
        columns = ("col1", "col2", "col3")

        # Crear un nuevo estilo
        custom_style = ttk.Style()
        
        # Configurar el estilo de la Treeview
        custom_style.configure("Custom.Treeview", 
                                background=style.BotonLista.fg_color,  # Cambiar el color de fondo
                                foreground=style.BotonLista.text_color,  # Cambiar el color del texto
                                font=("Helvetica", 11),  # Cambiar la fuente y tamaño del texto
                                highlightthickness=0,  # Eliminar el borde de resaltado
                                borderwidth=0)  # Eliminar el ancho del borde
        
        self.tree2 = ttk.Treeview(parent, columns=columns, show='headings', style="Custom.Treeview")
        self.tree2.heading("col1", text="ID", anchor="center",)  # genera automaticamente ID
        self.tree2.heading("col2", text="descripcion", anchor="center")  # descripción
        self.tree2.heading("col3", text="Estado", anchor="center")  # Estados Pendiente y Revisado
        
        self.tree2.pack(fill="both", expand=True, padx=10, pady=10,)

        # Configurar la alineación de las columnas de datos
        for col in columns:
            self.tree2.column(col, anchor="center")  # Centrar los valores de las columnas

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
                                                command=self.estadoRequerimiento)
        update_db_button.grid(row=0, column=3, padx=5)

        estimation_rule_button = ctk.CTkButton(button_frame, text="Actualizar Base de Datos",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.mensajeBase)
        estimation_rule_button.grid(row=0, column=4, padx=5)
              
        return self.inicializar_requerimientos()
    
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
                                borderwidth=0)  # Eliminar el ancho del borde
        
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

        estimation_rule_button = ctk.CTkButton(button_frame, text="Actualizar Base de Datos",
                                                text_color = style.BotonNormal.text_color,
                                                fg_color = style.BotonNormal.fg_color,
                                                font = style.BotonNormal.font,
                                                corner_radius = style.BotonNormal.corner_radius,
                                                hover_color = style.BotonNormal.hover_color,
                                                command=self.mensajeBase)
        estimation_rule_button.grid(row=0, column=4, padx=5)
              
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
    
    #FUNCIONES TABLA REQUERIMIENTOS----------------------------------------------------------------------------------
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

    #FUNCIONES TABLA PUNTOS DE FUNCION----------------------------------------------------------------------------------
    def agregarComponenteVentana(self): #VENTANA EMERGENTE PARA AGREGAR NUEVO COMPONENTE A LA TABLA
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
                                                command=self.agregarComponente).pack(pady=10)
    
    def agregarComponente(self):#AGREGA NUEVO COMPONENTE A LA TABLA
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
        id_fila = "ID-" + str(self.next_row_id).zfill(3)  # Formatear el ID con ceros a la izquierda
        values = [id_fila, descripcion, tipo, num_atributos, ""]
        self.tree.insert('', 'end', values=values)

        # Incrementar el contador de filas
        self.next_row_id += 1

        # Reiniciar los campos de texto y el radio button
        self.entries[0].set("")
        self.entries[1].set("")
        self.radio_var.set("")

        # Actualizar la complejidad si es necesario
        self.actualizar_complejidad()

        # Agregar la nueva fila al diccionario self.filas
        nueva_fila = {
            "ID": id_fila,
            "Descripción": descripcion,
            "Tipo": tipo,
            "Número de Atributos": num_atributos,
            "Clasificación": "",
            "Puntos de Función": ""
        }
        self.filas.append(nueva_fila)

        # Imprimir el contenido del diccionario self.filas
        print(self.filas)


    # Dentro de la clase Dev

    def eliminar_componente(self):#VENTANA PARA SELECCIONAR Y ELEMINAR UN COMPONENTE DE LA TABLA
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
        all_ids = [self.tree.item(item, 'values')[0] for item in self.tree.get_children()]

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
                                                command=lambda: self.eliminar_componente_seleccionado(id_combo.get(), eliminar_window))
        eliminar_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def eliminar_componente_seleccionado(self, id_seleccionado, window):#ELIMINA UN COMPONENTE DE LA TABLA
        # Buscar el item por ID
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values[0] == id_seleccionado:
                self.tree.delete(item)  # Eliminar la fila correspondiente
                messagebox.showinfo("Éxito", f"Se ha eliminado el componente {id_seleccionado} correctamente.")
                window.destroy()
                return
        
        # Mostrar un mensaje de error si el ID no se encuentra
        messagebox.showerror("Error", f"No se encontró el componente con ID {id_seleccionado}.")
        window.destroy()


    def actualizar_complejidad(self):#CALCULA LA COMPLEJIDA SEGUN TABLA ESTANDAR PPT4
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            tipo = values[2]
            num_atributos = int(values[3])

            #VALORES SEGUN TIPO DE COMPONENTE
            if tipo == "Entrada Externa":
                if num_atributos <= 4:
                    self.tree.set(item, column="col5", value="Baja")
                    self.tree.set(item, column="col6", value=3)
                elif num_atributos >= 5 and num_atributos <= 15:
                    self.tree.set(item, column="col5", value="Media")
                    self.tree.set(item, column="col6", value=4)
                else:
                    self.tree.set(item, column="col5", value="Alta")
                    self.tree.set(item, column="col6", value=6)

            elif tipo == "Salida Externa":
                if num_atributos <= 5:
                    self.tree.set(item, column="col5", value="Baja")
                    self.tree.set(item, column="col6", value=4)
                elif num_atributos >= 6 and num_atributos <= 19:
                    self.tree.set(item, column="col5", value="Media")
                    self.tree.set(item, column="col6", value=5)
                else:
                    self.tree.set(item, column="col5", value="Alta")
                    self.tree.set(item, column="col6", value=7)

            elif tipo == "Consulta Externa":
                if num_atributos <= 4:
                    self.tree.set(item, column="col5", value="Baja")
                    self.tree.set(item, column="col6", value=3)
                elif num_atributos >= 5 and num_atributos <= 15:
                    self.tree.set(item, column="col5", value="Media")
                    self.tree.set(item, column="col6", value=4)
                else:
                    self.tree.set(item, column="col5", value="Alta")
                    self.tree.set(item, column="col6", value=6)
            
            elif tipo == "Archivo lógico Interno":
                if num_atributos <= 5:
                    self.tree.set(item, column="col5", value="Baja")
                    self.tree.set(item, column="col6", value=7)
                elif num_atributos >= 6 and num_atributos <= 19:
                    self.tree.set(item, column="col5", value="Media")
                    self.tree.set(item, column="col6", value=10)
                else:
                    self.tree.set(item, column="col5", value="Alta")
                    self.tree.set(item, column="col6", value=15)

            if tipo == "Archivo de interfaz externo":
                if num_atributos <= 4:
                    self.tree.set(item, column="col5", value="Baja")
                    self.tree.set(item, column="col6", value=5)
                elif num_atributos >= 5 and num_atributos <= 15:
                    self.tree.set(item, column="col5", value="Media")
                    self.tree.set(item, column="col6", value=7)
                else:
                    self.tree.set(item, column="col5", value="Alta")
                    self.tree.set(item, column="col6", value=10)

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
    

    """def mostrar_ventana_emergente(self):
        ventana_emergente = ctk.CTkToplevel(app)
        ventana_emergente.configure(fg_color="white")
        etiqueta = ctk.CTkLabel(ventana_emergente, font=("Arial", -15, "bold"), text_color="black",
                                text="Error: No se puede crear otro proyecto.\n\nMotivo: Límite de proyectos activos alcanzado.")
        etiqueta.pack(padx=20, pady=20)
        ancho_ventana_principal = app.winfo_width()
        alto_ventana_principal = app.winfo_height()
        x_ventana_emergente = app.winfo_rootx() + ancho_ventana_principal // 2 - ventana_emergente.winfo_reqwidth() // 2
        y_ventana_emergente = app.winfo_rooty() + alto_ventana_principal // 2 - ventana_emergente.winfo_reqheight() // 2
        ventana_emergente.geometry("+{}+{}".format(x_ventana_emergente, y_ventana_emergente))
        ventana_emergente.title("Error")
        ventana_emergente.attributes('-topmost' , 1)
        ventana_emergente.focus()"""

# #Borrar para uso final
# app = Dev()
# app.mainloop()



"""
- Solicitudes LISTO
- Clasificacion LISTO
- Calculo de puntos LISTO
- Boton de eliminar LISTO
- Boton de Actualizar BD LISTO
- Boton cambiar regla de estimacion NO LISTO

"""

"""
    # Agregar texto decorativo junto a cada campo de texto
        decor_labels = ["Texto 1", "Texto 2", "Texto 3", "Texto 4", "Texto 5"]
        for i, decor_label in enumerate(decor_labels):
            frame = ctk.CTkFrame(agregarComponente_window)
            frame.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
            ctk.CTkLabel(frame, text=decor_label, fg_color="gray").pack(side="left", padx=(0, 10))
        
    """