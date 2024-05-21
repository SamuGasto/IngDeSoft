import customtkinter as ctk
from PIL import Image
import Vistas.ventana_jefeProject as JEFE
import Vistas.ventana_crearCuenta as Crearc
import os
import BaseDeDatos.UsersQuery as db

#creamos la clase ventana para la bienvenida
class Welcome(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x540")
        self.title("PaltaEstimateApp")
        #self.resizable(False, False)
        self.Contenido()



        self.mainloop()

    def Contenido(self):#Frames
        nombre_company = ctk.CTkLabel(self, text="PaltaEstimateApp", font=("Comic Sans", -25, "italic"))
        nombre_company.place(relx=0.05, rely=0.025)
        bienvenido = ctk.CTkLabel(self, text="¡Bienvenido!", font=("Comic Sans", -60, "bold"))
        bienvenido.place(relx=0.15, rely=0.15)
        subtext = ctk.CTkLabel(self, text="Inicia sesión para continuar...", font=("Comic Sans", -20))
        subtext.place(relx=0.15, rely=0.3)

        email = ctk.CTkLabel(self, text="Correo", font=("Comic Sans", -25, "bold"))
        email.place(relx=0.15, rely=0.43)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu email...", width=250)
        self.email_entry.place(relx=0.15, rely=0.5)

        passw = ctk.CTkLabel(self, text="Contraseña", font=("Comic Sans", -25, "bold"))
        passw.place(relx=0.15, rely=0.58)
        self.passw_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu contraseña...", width=250, show="*")
        self.passw_entry.place(relx=0.15, rely=0.65)

        passw_peak = ctk.CTkButton(self, text="O", width=20, height=20, corner_radius=100, command=self.peak)
        passw_peak.place(relx=0.47, rely=0.66)

        # Imágen del logo
        # Obtener la ruta absoluta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")
        logo = ctk.CTkImage(light_image=Image.open(logo_path),
            size=(250, 250))
        logo_label = ctk.CTkLabel(self, image=logo, text="")
        logo_label.place(relx=0.6, rely=0.25)

        no_email = ctk.CTkLabel(self, text="¿No tienes cuenta?", font=("Comic Sans", -15, "italic", "underline"))
        no_email.place(relx=0.65, rely=0.81)
        no_email_btn = ctk.CTkButton(self, width=85, height=25, corner_radius=25, command=self.cambiar_ventana,
                                    text="Crear cuenta", font=("Comic Sans", -15))
        no_email_btn.place(relx=0.815, rely=0.815)

        iniciar_btn = ctk.CTkButton(self, width=100, height=45, corner_radius=25, text="Iniciar sesión",
                                    font=("Comic Sans", -20), command=self.IniciarSesion)
        iniciar_btn.place(relx=0.15, rely=0.8)
        #Implementar lógica para iniciar la sesión, mandando la query a la BD.


    def peak(self):
        if self.passw_entry.cget("show") == "*":
            self.passw_entry.configure(show="")
        else:
            self.passw_entry.configure(show="*")

    def IniciarSesion(self):
        #obtenemos los datos del usuario
        self.user_email = self.email_entry.get()
        self.user_passsw = self.passw_entry.get()
        #Mandamos la query para comprobar que el usuario existe,
        if db.ValidarUsuario(self.user_email, self.user_passsw) == True:
            self.destroy()
            JEFE.JP()
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
#app = Welcome()
#app.mainloop()