import customtkinter as ctk
from PIL import Image
#import BaseDeDatos.UsersMongoDB as db
#import Vistas.VentanaEjemplo2 as vis2

#creamos la clase ventana para la bienvenida
class Welcome(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x540")
        self.title("PaltaEstimateApp")
        #self.resizable(False, False)
        self.Contenido()

    def Contenido(self):#Frames
        nombre_company = ctk.CTkLabel(self, text="PaltaEstimateApp", font=("Comic Sans", -25, "italic"))
        nombre_company.place(relx=0.05, rely=0.025)
        bienvenido = ctk.CTkLabel(self, text="¡Bienvenido!", font=("Comic Sans", -60, "bold"))
        bienvenido.place(relx=0.15, rely=0.15)
        subtext = ctk.CTkLabel(self, text="Inicia sesión para continuar...", font=("Comic Sans", -20))
        subtext.place(relx=0.15, rely=0.3)

        email = ctk.CTkLabel(self, text="Correo", font=("Comic Sans", -25, "bold"))
        email.place(relx=0.15, rely=0.43)
        email_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu email...", width=250)
        email_entry.place(relx=0.15, rely=0.5)

        passw = ctk.CTkLabel(self, text="Contraseña", font=("Comic Sans", -25, "bold"))
        passw.place(relx=0.15, rely=0.58)
        passw_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu contraseña...", width=250, show="*")
        passw_entry.place(relx=0.15, rely=0.65)

        iniciar_btn = ctk.CTkButton(self, width=100, height=45, corner_radius=25, text="Iniciar sesión", font=("Comic Sans", -20))
        iniciar_btn.place(relx=0.15, rely=0.8)

        logo = ctk.CTkImage(light_image=Image.open("E:\Repositorios GitHub\IngDeSoft\ProyectoIngSoftware\App\Vistas\LOGO.png"),
            size=(250, 250))
        logo_label = ctk.CTkLabel(self, image=logo, text="")
        logo_label.place(relx=0.6, rely=0.25)

        no_email = ctk.CTkLabel(self, text="¿No tienes cuenta?", font=("Comic Sans", -15, "italic", "underline"))
        no_email.place(relx=0.65, rely=0.81)
        no_email_btn = ctk.CTkButton(self, width=85, height=25, corner_radius=25, text="Crear cuenta", font=("Comic Sans", -15))
        no_email_btn.place(relx=0.815, rely=0.815)


    def get_email(self):
        ...
    
    def get_passw(self):
        ...









    #self.mainloop() !! BORRAR EL COMENTARIO PARA USO FINAL














#Borrar para uso final
app = Welcome()
app.mainloop()