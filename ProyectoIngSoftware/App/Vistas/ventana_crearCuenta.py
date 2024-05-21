import customtkinter as ctk
from PIL import Image
import os
import BaseDeDatos.UsersQuery as db


#creamos la clase ventana para crear la cuenta
class Crear_cuenta(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x540")
        self.title("PaltaEstimateApp")
        #self.resizable(False, False)
        self.Contenido()

        
        self.mainloop() #!! BORRAR EL COMENTARIO PARA USO FINAL

    def Contenido(self):#Frames
        nombre_company = ctk.CTkLabel(self, text="PaltaEstimateApp", font=("Comic Sans", -25, "italic"))
        nombre_company.place(relx=0.05, rely=0.025)
        bienvenido = ctk.CTkLabel(self, text="¡Crea tu cuenta!", font=("Comic Sans", -50, "bold"))
        bienvenido.place(relx=0.135, rely=0.15)

        # Obtener la ruta absoluta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Imagenes/LOGO.png")

        logo = ctk.CTkImage(light_image=Image.open(logo_path),
            size=(125, 125))
        logo_label = ctk.CTkLabel(self, image=logo, text="")
        logo_label.place(relx=0.75, rely=0.1)

        email = ctk.CTkLabel(self, text="Correo", font=("Comic Sans", -25, "bold"))
        email.place(relx=0.55, rely=0.43)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu email...", width=250)
        self.email_entry.place(relx=0.55, rely=0.5)

        user_name = ctk.CTkLabel(self, text="Nombre de usuario", font=("Comic Sans", -25, "bold"))
        user_name.place(relx=0.15, rely=0.43)
        self.user_name_entry = ctk.CTkEntry(self, placeholder_text="Ingresa un nombre de usuario...", width=250)
        self.user_name_entry.place(relx=0.15, rely=0.5)

        passw = ctk.CTkLabel(self, text="Contraseña", font=("Comic Sans", -25, "bold"))
        passw.place(relx=0.15, rely=0.58)
        self.passw_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu contraseña...", width=250, show="*")
        self.passw_entry.place(relx=0.15, rely=0.65)

        passw2 = ctk.CTkLabel(self, text="Repite la contraseña", font=("Comic Sans", -25, "bold"))
        passw2.place(relx=0.15, rely=0.73)
        self.passw2_entry = ctk.CTkEntry(self, placeholder_text="Ingresa tu contraseña...", width=250, show="*")
        self.passw2_entry.place(relx=0.15, rely=0.8)

        role_picker = ctk.CTkLabel(self, text="Elige tu rol:", font=("Comic Sans", -25, "bold"))
        role_picker.place(relx=0.55, rely=0.58)

        self.radio_var = ctk.StringVar(value="")
        radiobutton_1 = ctk.CTkRadioButton(self, text="Jefe de proyecto", font=("Comic Sans", -18), variable= self.radio_var, value="Jefe de proyecto")
        radiobutton_1.place(relx=0.55, rely=0.65)
        radiobutton_2 = ctk.CTkRadioButton(self, text="Administrador", font=("Comic Sans", -18), variable= self.radio_var, value="Administrador")
        radiobutton_2.place(relx=0.55, rely=0.7)
        radiobutton_3 = ctk.CTkRadioButton(self, text="Desarrollador", font=("Comic Sans", -18), variable= self.radio_var, value="Desarrollador")
        radiobutton_3.place(relx=0.55, rely=0.75)

        Crear_btn = ctk.CTkButton(self, width=100, height=40, corner_radius=25, text="Crear cuenta",
                                    font=("Comic Sans", -20), command=self.getAccountInfo)
        Crear_btn.place(relx=0.6, rely=0.87)

    def getAccountInfo(self):

        self.user_email = self.email_entry.get()
        self.user_passsw = self.passw_entry.get()
        self.user_username = self.user_name_entry.get()
        self.RoleSelected = self.radio_var.get()
        print("email: " + self.user_email)
        print("pass: " + self.user_passsw)
        db.AnadirUsuario(self.user_email, 
                         self.user_username, 
                         self.user_passsw, 
                         self.RoleSelected)

