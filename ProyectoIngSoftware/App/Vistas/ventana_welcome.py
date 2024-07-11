import customtkinter as ctk
from PIL import Image
import os

import Vistas.ventana_jefeProject as JEFE
import Vistas.ventana_crearCuenta as Crearc
import BaseDeDatos.UsersQuery as db
import Clases.Componentes.Estilos as style


#creamos la clase ventana para la bienvenida
class Welcome(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("PaltaEstimateApp")
        self.configure(fg_color=style.Colores.background)
        
        self.after(0, lambda:self.state('zoomed'))
        """#ACÁ CENTRAMOS LA VENTANA MAIN
        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = self.winfo_screenwidth()
        htotal = self.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 960
        hventana = 640
        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)
        #  Se lo aplicamos a la geometría de la ventana
        self.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))"""
        #self.resizable(False, False)
        self.Contenido()

        # Vincular la tecla 'Enter' a la función IniciarSesion para la ventana principal
        self.bind('<Return>', self.IniciarSesion)

        #self.after(200, self.configure(state=self.state('zoomed')))

        self.mainloop()

    def Contenido(self):#Frames
        # Imágen del logo
        # Obtener la ruta absoluta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
        logo = ctk.CTkImage(light_image=Image.open(logo_path),
            size=(500, 500))
        logo_label = ctk.CTkLabel(self, image=logo, text="")
        logo_label.place(relx=0.6, rely=0.25)

        # Imagen ojo abierto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ojo_abierto_path = os.path.join(current_dir, "../Imagenes/ojo_abierto.png")
        self.ojo_abierto = ctk.CTkImage(light_image=Image.open(ojo_abierto_path),size=(25,25))

        # Imagen ojo cerrado
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ojo_cerrado_path = os.path.join(current_dir, "../Imagenes/ojo_cerrado.png")
        self.ojo_cerrado = ctk.CTkImage(light_image=Image.open(ojo_cerrado_path),size=(25,25))
        
        nombre_company = ctk.CTkLabel(self, 
                                      text="PaltaEstimateApp", 
                                      text_color = style.Titulo.text_color,
                                      font = style.Titulo.font)
        nombre_company.place(relx=0.03, rely=0.025)
        bienvenido = ctk.CTkLabel(self,
                                  text="¡Bienvenido!",
                                  font=style.MegaTitulo.font)
        bienvenido.place(relx=0.15, rely=0.15)
        subtext = ctk.CTkLabel(self, 
                               text="Inicia sesión para continuar...", 
                               font=style.Subtitulo.font)
        subtext.place(relx=0.15, rely=0.3)

        email = ctk.CTkLabel(self, 
                             text="Correo", 
                             font=style.Texto.font)
        email.place(relx=0.15, rely=0.43)
        self.email_entry = ctk.CTkEntry(self, 
                                        placeholder_text="Ingresa tu email...",
                                        fg_color = style.EntryNormal.fg_color,
                                        border_color = style.EntryNormal.border_color,
                                        text_color = style.EntryNormal.text_color,
                                        font = style.EntryNormal.font,
                                        corner_radius = style.EntryNormal.corner_radius,
                                        width=250)
        self.email_entry.insert(0, "prueba@gmail.com")
        self.email_entry.place(relx=0.15, rely=0.5)

        passw = ctk.CTkLabel(self, text="Contraseña", font=style.Texto.font)
        passw.place(relx=0.15, rely=0.58)
        self.passw_entry = ctk.CTkEntry(self, 
                                        placeholder_text="Ingresa tu contraseña...",
                                        fg_color = style.EntryNormal.fg_color,
                                        border_color = style.EntryNormal.border_color,
                                        text_color = style.EntryNormal.text_color,
                                        font = style.EntryNormal.font,
                                        corner_radius = style.EntryNormal.corner_radius,
                                        width=250, 
                                        show="*")
        self.passw_entry.place(relx=0.15, rely=0.65)
        self.passw_entry.insert(0, "123456")
        # Vincular la tecla 'Enter' al CTkEntry de contraseña
        self.passw_entry.bind('<Return>', self.IniciarSesion)

        self.passw_peak = ctk.CTkButton(self, image=self.ojo_cerrado,
                                        fg_color="transparent",
                                        hover_color="#4E4E4E",
                                        text="", 
                                        height=10, 
                                        width=10, 
                                        corner_radius=100,
                                        command=self.peak)
        self.passw_peak.place(relx=0.282, rely=0.648)

        

        no_email = ctk.CTkLabel(self, 
                                text="¿No tienes cuenta?", 
                                font=style.TextoItalica.font)
        no_email.place(relx=0.720, rely=0.81)
        no_email_btn = ctk.CTkButton(self, 
                                     width=85, 
                                     height=25,  
                                     command=self.cambiar_ventana,
                                     text="Crear cuenta",
                                     text_color = style.BotonNormal.text_color,
                                     fg_color = style.BotonNormal.fg_color,
                                     font = style.BotonNormal.font,
                                     corner_radius = style.BotonNormal.corner_radius,
                                     hover_color = style.BotonNormal.hover_color)
        no_email_btn.place(relx=0.815, rely=0.815)

        iniciar_btn = ctk.CTkButton(self, width=100, 
                                    height=45,  
                                    text="Iniciar sesión",
                                    text_color = style.BotonGrande.text_color,
                                    fg_color = style.BotonGrande.fg_color,
                                    font = style.BotonGrande.font,
                                    corner_radius = style.BotonGrande.corner_radius,
                                    hover_color = style.BotonGrande.hover_color,
                                    command=self.IniciarSesion)
        iniciar_btn.place(relx=0.15, rely=0.8)

    def peak(self):#Funcion que muestra la contraseña escrita
        if self.passw_entry.cget("show") == "*":
            self.passw_entry.configure(show="")
            self.passw_peak.configure(image=self.ojo_abierto)
        else:
            self.passw_entry.configure(show="*")
            self.passw_peak.configure(image=self.ojo_cerrado)

    def IniciarSesion(self, event=None):
        #obtenemos los datos del usuario
        self.user_email = self.email_entry.get()
        self.user_passsw = self.passw_entry.get()
        #Mandamos la query para comprobar que el usuario existe,
        if db.ValidarUsuario(self.user_email, self.user_passsw) == True:
            self.destroy()
            JEFE.JP(self.user_email)
        else:
            self.mostrar_ventana_emergente()
          
    def cambiar_ventana(self) -> None:#Funcion que cambia a la ventana de crear cuenta
        self.destroy()
        Crearc.Crear_cuenta()

    def mostrar_ventana_emergente(self):
        ventana_emergente = ctk.CTkToplevel(self)
        ventana_emergente.configure(fg_color="white")
        etiqueta = ctk.CTkLabel(ventana_emergente, font=("Arial", -15, "bold"), text_color="black",
                                text="Error: Correo o contraseña incorrectos.")
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
