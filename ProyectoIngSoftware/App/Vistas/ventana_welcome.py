import customtkinter as ctk
from PIL import Image
import Vistas.ventana_jefeProject as JEFE
import Vistas.ventana_crearCuenta as Crearc
import os
import BaseDeDatos.UsersQuery_new as db


#creamos la clase ventana para la bienvenida
class Welcome(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("PaltaEstimateApp")
        #ACÁ CENTRAMOS LA VENTANA MAIN
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
        self.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
        #self.resizable(False, False)
        self.Contenido()

        # Vincular la tecla 'Enter' a la función IniciarSesion para la ventana principal
        self.bind('<Return>', self.IniciarSesion)

        self.mainloop()

    def Contenido(self):#Frames
        # Imágen del logo
        # Obtener la ruta absoluta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
        logo = ctk.CTkImage(light_image=Image.open(logo_path),
            size=(250, 250))
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
        
        nombre_company = ctk.CTkLabel(self, text="PaltaEstimateApp", font=("Comic Sans MS", -25, "italic"))
        nombre_company.place(relx=0.05, rely=0.025)
        bienvenido = ctk.CTkLabel(self, text="¡Bienvenido!", font=("Comic Sans MS", -60, "bold"))
        bienvenido.place(relx=0.15, rely=0.15)
        subtext = ctk.CTkLabel(self, text="Inicia sesión para continuar...", font=("Comic Sans MS", -20))
        subtext.place(relx=0.15, rely=0.3)

        email = ctk.CTkLabel(self, text="Correo", font=("Comic Sans MS", -25, "bold"))
        email.place(relx=0.15, rely=0.43)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu email...", width=250)
        self.email_entry.insert(0, "prueba2@gmail.com")
        self.email_entry.place(relx=0.15, rely=0.5)

        passw = ctk.CTkLabel(self, text="Contraseña", font=("Comic Sans MS", -25, "bold"))
        passw.place(relx=0.15, rely=0.58)
        self.passw_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu contraseña...", width=250, show="*")
        self.passw_entry.place(relx=0.15, rely=0.65)
        self.passw_entry.insert(0, "123456")
        # Vincular la tecla 'Enter' al CTkEntry de contraseña
        self.passw_entry.bind('<Return>', self.IniciarSesion)

        self.passw_peak = ctk.CTkButton(self, image=self.ojo_cerrado,fg_color="transparent",hover_color="#4E4E4E",
                                        text="", height=10, width=10, corner_radius=100,
                                        command=self.peak)
        self.passw_peak.place(relx=0.415, rely=0.645)

        

        no_email = ctk.CTkLabel(self, text="¿No tienes cuenta?", font=("Comic Sans MS", -15, "italic", "underline"))
        no_email.place(relx=0.65, rely=0.81)
        no_email_btn = ctk.CTkButton(self, width=85, height=25, corner_radius=25, command=self.cambiar_ventana,
                                    text="Crear cuenta", font=("Comic Sans MS", -15))
        no_email_btn.place(relx=0.815, rely=0.815)

        iniciar_btn = ctk.CTkButton(self, width=100, height=45, corner_radius=25, text="Iniciar sesión",
                                    font=("Comic Sans MS", -20), command=self.IniciarSesion)
        iniciar_btn.place(relx=0.15, rely=0.8)

        
        

    def peak(self):
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
    
    
            
    def cambiar_ventana(self) -> None:
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
        
#borrar para uso final
# app = Welcome()
# app.mainloop()
