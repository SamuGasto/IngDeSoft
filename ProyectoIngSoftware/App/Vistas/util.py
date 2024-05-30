
def centrarVentana(ventana, width:int, height:int):
    """
    Función para centrar en pantalla una ventana y otorgarle dimensiones.
    
    Argumentos:
        ventana (customtkinter frame): Ventana de CustomTKinter.
        width (int): Ancho de la ventana.
        height (int): Altura de la ventana.
    """
    #Obtenemos el largo y  ancho de la pantalla
    wtotal = ventana.winfo_screenwidth()
    htotal = ventana.winfo_screenheight()
    #Guardamos el largo y alto de la ventana
    wventana = width
    hventana = height
    #  Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    #  Se lo aplicamos a la geometría de la ventana
    ventana.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))