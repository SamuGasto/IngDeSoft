import customtkinter
import BaseDeDatos.UsersQuery as db
import Vistas.VentanaEjemplo2 as vis2

class V1(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.width = 1280
        self.height = 720
 
        self.screen_width = self.winfo_screenwidth()  # Ancho de la pantalla
        self.screen_height = self.winfo_screenheight() # Alto de la pantalla
 
        # Calcula el x e y para centrar la ventana
        self.x = (self.screen_width/2) - (self.width/2)
        self.y = (self.screen_height/2) - (self.height/2)
 
        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')

        self.textUser = customtkinter.CTkLabel(self,text='Nombre de usuario:')
        self.textUser.pack()
        self.entryUser = customtkinter.CTkEntry(self)
        self.entryUser.pack(padx=20, pady=20)

        self.textPws = customtkinter.CTkLabel(self,text='Contraseña:')
        self.textPws.pack()
        self.entryPws = customtkinter.CTkEntry(self)
        self.entryPws.pack(padx=20, pady=20)

        self.addUser = customtkinter.CTkButton(self, text="Añadir Usuario", command=self.AddUser)
        self.addUser.pack(padx=20, pady=20)

        self.updPwd = customtkinter.CTkButton(self, text="Actualizar Contraseña", command=self.AddUser)
        self.updPwd.pack(padx=20, pady=20)

        self.valUser = customtkinter.CTkButton(self, text="Validar Usuario", command=self.ValUser)
        self.valUser.pack(padx=20, pady=20)
        
        self.delUser = customtkinter.CTkButton(self, text="Eliminar Usuario", command=self.DelUser)
        self.delUser.pack(padx=20, pady=20)

        self.changeView = customtkinter.CTkButton(self, text="Cambiar a vista 2", command=self.CambiarVista2)
        self.changeView.pack(padx=20, pady=20)
        
        self.VentanaEmergente = None
        # Main loop permite que la vista se mantenga en pantalla
        self.mainloop()

    def AddUser(self) -> None:
        db.AnadirUsuario(self.entryUser.get(),self.entryPws.get())

    def ValUser(self)->None:
        r = str(db.ValidarUsuario(self.entryUser.get(),self.entryPws.get()))
        self.CrearMensajeEmergente(r)
    
    def DelUser(self)->None:
        if (db.ValidarUsuario(self.entryUser.get(),self.entryPws.get())):
            val = customtkinter.CTkInputDialog(text="Ingresa la contraseña nuevamente:", title="¿Estás seguro?")
            value = val.get_input()
            if (value == None):
                self.CrearMensajeEmergente('No se eliminó al usuario.')
            else:
                if (value and db.ValidarUsuario(self.entryUser.get(),value)):
                    db.EliminarUsuario(self.entryUser.get())
                else:
                    self.CrearMensajeEmergente('Contraseña incorrecta.')
        else:
            self.CrearMensajeEmergente('Usuario o contraseña incorrecta.')

    def CrearMensajeEmergente(self,mensaje):
        if self.VentanaEmergente is None or not self.VentanaEmergente.winfo_exists():
            self.VentanaEmergente = VentanaConMensaje(mensaje)
        else:
            self.VentanaEmergente.focus()  # if window exists focus it

    def CambiarVista2(self) -> None:
        self.destroy()
        vis2.V2()

class VentanaConMensaje(customtkinter.CTkToplevel):
    def __init__(self, mensaje):
        super().__init__()

        self.label = customtkinter.CTkLabel(self,text=mensaje)
        self.label.pack(padx=20, pady=20)

        self.exitButton = customtkinter.CTkButton(self,text='Cerrar', command=self.Cerrar)
        self.exitButton.pack()
        
        self.attributes("-topmost",True)
    def Cerrar(self):
        self.destroy()