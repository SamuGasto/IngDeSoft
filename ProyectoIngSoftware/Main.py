import customtkinter
#import DataBase as db
import DBMongoDB as db

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x150")

        self.button = customtkinter.CTkButton(self, text="Conectar con base de Datos", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

        self.button = customtkinter.CTkButton(self, text="Mostrar tablas", command=self.ImprimirTablas)
        self.button.pack(padx=20, pady=20)

    def button_callbck(self) -> None:
        db.AnadirUsuario('samuel.55321@gmail.com','55321')

    def ImprimirTablas(self):
        raise NotImplementedError('Aun no implementamos la feature')

app = App()
app.mainloop()