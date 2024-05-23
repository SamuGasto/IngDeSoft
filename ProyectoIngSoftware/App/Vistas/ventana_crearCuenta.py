import customtkinter as ctk
from PIL import Image
import os
import Vistas.ventana_welcome as inicio
import BaseDeDatos.UsersQuery as db


#creamos la clase ventana para crear la cuenta
class Crear_cuenta(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
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
        

        Crear_btn = ctk.CTkButton(self, width=100, height=40, corner_radius=25, text="Crear cuenta",
                                    font=("Comic Sans", -20), command=self.getAccountInfo)
        Crear_btn.place(relx=0.6, rely=0.87)

        self.error = ctk.CTkLabel(self, text="Las contraseñas no coinciden.",text_color="Red",
                                font=("Comic Sans", -15, "bold"), state="disabled")
        self.error.place(relx=0.15, rely=0.85)
        self.error.place_forget()
        

    def getAccountInfo(self):
        if self.passw_entry.get()=="" or self.passw2_entry.get()=="" or self.email_entry.get()=="" or self.user_name_entry.get()=="":
            self.mostrar_ventana_emergente("Error: Se deben llenar todos los campos\npara crear la cuenta.")
            return
        if self.comprobar_gmail(self.email_entry.get()):
            if db.BuscarUsuario(self.email_entry.get()):
                self.mostrar_ventana_emergente(f"Ya existe una cuenta con el correo {self.email_entry.get()}.")
                return
        else:
            self.mostrar_ventana_emergente("El correo debe terminar en '@gmail.com'")
            return
        if db.BuscarUsername(self.user_name_entry.get()):
            self.mostrar_ventana_emergente("El nombre de usuario ya existe.\nPrueba otro.")
            return
        if self.passw_entry.get() == self.passw2_entry.get():
            self.error.place_forget()
        else:
            self.error.place(relx=0.15, rely=0.85)
            return
        self.user_email = self.email_entry.get()
        self.user_passsw = self.passw_entry.get()
        self.user_username = self.user_name_entry.get()
        self.RoleSelected = "Jefe de proyecto"
        
        db.AnadirUsuario(self.user_email, 
                        self.user_username, 
                        self.user_passsw, 
                        self.RoleSelected)
        
        success = self.mostrar_ventana_emergente("La cuenta se ha creado con éxito.\nAhora puedes acceder a tu cuenta.")
        self.wait_window(success)
        self.destroy()
        inicio.Welcome()

    def mostrar_ventana_emergente(self, texto):
        ventana_emergente = ctk.CTkToplevel(self)
        ventana_emergente.configure(fg_color="white")
        etiqueta = ctk.CTkLabel(ventana_emergente, font=("Arial", -15, "bold"), text_color="black",
                                text=texto)
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
        return ventana_emergente  # Asegúrate de retornar la ventana emergente
    def comprobar_gmail(self, cadena):
        return cadena.endswith("@gmail.com")

