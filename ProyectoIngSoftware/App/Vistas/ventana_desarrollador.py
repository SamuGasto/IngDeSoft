import customtkinter as ctk
from tkinter import ttk, Toplevel, StringVar

#creamos la clase ventana para el jefe de proyecto
class Dev(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.n_proyectos = 1 
        self.proyecto_id = 111
        self.geometry("1200x720")
        self.title("PaltaEstimateApp")
        self.Paneles()
        self.controles_sidebar()
        self.contenido_body()
        self.contenido_subpanel()
        #self.mainloop() !! BORRAR EL COMENTARIO PARA USO FINAL
    
    def Paneles(self):
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
        self.tab1 = tabview.add("Puntos de Función")  
        tab2 = tabview.add("Requerimientos")  
        tab3 = tabview.add("Tareas")  
        
        ## Crear la tabla en la pestaña "Integrantes"
        self.create_table(self.tab1)

        ##Objetos de tab2
        scroll = ctk.CTkScrollableFrame(master=tab2)
        scroll.pack(fill="both",expand=True)
        texto = ctk.CTkLabel(master=scroll, font=("Calibri", -15, "italic"), text="· REQ-111: ")
        texto.pack(side=ctk.TOP, anchor=ctk.NW, padx=5, pady=5)
        
        ##Objetos de tab3

        ##objetos del body
        self.administrar  = ctk.CTkButton(self.body, text="Administración\nCompleta", text_color="black",fg_color="white", font=("Comic Sans", -15, "bold"),
                                        width=150, height=35, corner_radius=25)
        self.administrar.pack(side=ctk.LEFT, anchor=ctk.SE, pady=5, padx=5)

    def create_table(self, parent):
        columns = ("col1", "col2", "col3", "col4", "col5")
        self.tree = ttk.Treeview(parent, columns=columns, show='headings')
        self.tree.heading("col1", text="ID")
        self.tree.heading("col2", text="Descripción")
        self.tree.heading("col3", text="Tipo")
        self.tree.heading("col4", text="Número Atributos")
        self.tree.heading("col5", text="Clasificación")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        add_row_button = ctk.CTkButton(parent, text="Agregar Fila", command=self.open_add_row_window)
        add_row_button.pack(pady=10)

    def open_add_row_window(self):
        add_row_window = Toplevel(self)
        add_row_window.title("Agregar Fila")

    # Frame para los campos de texto y los radio buttons
        frame_entries_and_radios = ctk.CTkFrame(add_row_window)
        frame_entries_and_radios.pack(padx=10, pady=10, anchor="w")

        labels = ["Columna 1:", "Columna 2:", "Columna 3:", "Columna 4:", "Columna 5:"]
        self.entries = [StringVar() for _ in labels]

        for i, label in enumerate(labels):
            frame = ctk.CTkFrame(frame_entries_and_radios)
            frame.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            ctk.CTkLabel(frame, text=label).pack(side="left", padx=(0, 10))

            if label != "Columna 3:":  # Si no es la columna 3, agregar campo de entrada normal
                ctk.CTkEntry(frame, textvariable=self.entries[i]).pack(side="left")
            else:  # Si es la columna 3, agregar los radio buttons
                role_picker = ctk.CTkLabel(frame, text="Elige tu rol:", font=("Comic Sans", -25, "bold"))
                role_picker.pack(side="left", padx=(0, 10))

                self.radio_var = ctk.StringVar(value="")
                radiobutton_1 = ctk.CTkRadioButton(frame, text="Entrada Externa", font=("Comic Sans", -18), variable=self.radio_var, value="Entrada Externa")
                radiobutton_1.pack(side="left", padx=10, pady=5)
                radiobutton_2 = ctk.CTkRadioButton(frame, text="Salida Externa", font=("Comic Sans", -18), variable=self.radio_var, value="Salida Externa")
                radiobutton_2.pack(side="left", padx=10, pady=5)
                radiobutton_3 = ctk.CTkRadioButton(frame, text="Archivo logico Interno", font=("Comic Sans", -18), variable=self.radio_var, value="Archivo logico Interno")
                radiobutton_3.pack(side="left", padx=10, pady=5)

    # Botón "Agregar"
        ctk.CTkButton(add_row_window, text="Agregar", command=self.add_row).pack(pady=10)



    """# Agregar texto decorativo junto a cada campo de texto
        decor_labels = ["Texto 1", "Texto 2", "Texto 3", "Texto 4", "Texto 5"]
        for i, decor_label in enumerate(decor_labels):
            frame = ctk.CTkFrame(add_row_window)
            frame.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
            ctk.CTkLabel(frame, text=decor_label, fg_color="gray").pack(side="left", padx=(0, 10))
        """

    def add_row(self):
        values = [entry.get() for entry in self.entries[:-1]]  # Excluimos el campo de texto para el rol
        values.append(self.radio_var.get())  # Agregar el valor seleccionado en el radiobutton
        self.tree.insert('', 'end', values=values)

        for entry in self.entries:
            entry.set("")

    def contenido_subpanel(self):
        texto_boton = self.boton_proyecto.cget("text")#se obtiene la info del proyecto seleccionado, para mostrar en la ventana
        self.proyecto_actual = ctk.CTkLabel(self.top_subpanel, text=texto_boton, font=("Comic Sans", -25))
        self.proyecto_actual.pack(side=ctk.TOP)

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
        self.proyecto_actual.configure(text=texto)

    def boton_clickeado(self, texto):
        self.cambiar_proyecto(texto)

    def boton_clickeado_global(self, texto):
        self.boton_clickeado(texto)

    def mostrar_ventana_emergente(self):
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
        ventana_emergente.focus()

#Borrar para uso final
app = Dev()
app.mainloop()
