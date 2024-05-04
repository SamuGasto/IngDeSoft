import customtkinter
import App.BaseDeDatos.UsersQuery as db
import Vistas.VentanaEjemplo as vis1

class V2(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x150")

        self.button = customtkinter.CTkButton(self, text="Añadir Usuario", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

        self.button = customtkinter.CTkButton(self, text="Cambiar a vista 1", command=self.CambiarVista1)
        self.button.pack(padx=20, pady=20)

        # Main loop permite que la vista se mantenga en pantalla
        self.mainloop()

    def button_callbck(self) -> None:
        db.AnadirUsuario('samuel.55321@gmail.com','55321')

    def CambiarVista1(self) -> None:
        self.destroy()
        vis1.V1()