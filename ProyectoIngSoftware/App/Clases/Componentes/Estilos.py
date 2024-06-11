
colores = {
    #Mas oscuro a mas claro
    "Primary" : ["#572020","#763226","#a2502f","#da7c39","#ffb943"],
    "Gray" : ["#151515","#787878","#a8a8a8","#cdcdcd","#ededed"],
    "Green": ["#132c13","#1e7625","#26a131","#2cc23b","#32df43"],
    "Yellow": ["#2c2713","#766c1e","#a19426","#c2b32c","#dfce32"],
    "Red" : ["#2c1313","#761e1e","#a12626","#c22c2c","#df3232"],
    "Blue" : ["#001023","#003253","#005c8d","#008fcf","#00cdff"],

    "MainColor" : ["#0b1e26","#18333d","#487070","#1c621b","#419310","#a5Ec60"],
}

class colores():
    def __init__(self) -> None:
        self.background = "#0b1e26"
        self.backgroundVariant = "#18333d"
        self.backgroundVariant2 = "#487070"
        self.MainColor = ["#0b1e26","#18333d","#487070","#1c621b","#419310","#a5Ec60"]
        self.Gray = ["#151515","#787878","#a8a8a8","#cdcdcd","#ededed"]
        self.Blue = ["#001023","#003253","#005c8d","#008fcf","#00cdff"]
Colores = colores()

class botonNormal():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.fg_color = Colores.MainColor[4]
        self.font = ("Segoe UI", -15, "bold")
        self.corner_radius = 12
        self.hover_color = Colores.MainColor[3]
BotonNormal = botonNormal()

"""
text_color = style.BotonNormal.text_color,
fg_color = style.BotonNormal.fg_color,
font = style.BotonNormal.font,
corner_radius = style.BotonNormal.corner_radius,
hover_color = style.BotonNormal.hover_color
"""

class botonLista():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.fg_color = Colores.MainColor[2]
        self.font = ("Segoe UI", -15, "bold")
        self.corner_radius = 12
        self.hover_color = Colores.MainColor[1]
BotonLista = botonLista()

"""
text_color = style.BotonLista.text_color,
fg_color = style.BotonLista.fg_color,
font = style.BotonLista.font,
corner_radius = style.BotonLista.corner_radius,
hover_color = style.BotonLista.hover_color
"""

class botonGrande():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.fg_color = Colores.MainColor[4]
        self.font = ("Segoe UI", -26, "bold")
        self.corner_radius = 12
        self.hover_color = Colores.MainColor[3]
BotonGrande = botonGrande()

"""
text_color = style.BotonGrande.text_color,
fg_color = style.BotonGrande.fg_color,
font = style.BotonGrande.font,
corner_radius = style.BotonGrande.corner_radius,
hover_color = style.BotonGrande.hover_color,
"""

class botonSecundario():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.fg_color = Colores.MainColor[2]
        self.font = ("Segoe UI", -15, "bold")
        self.corner_radius = 12
        self.hover_color = Colores.MainColor[1]
BotonSecundario = botonSecundario()

"""
text_color = style.BotonSecundario.text_color,
fg_color = style.BotonSecundario.fg_color,
font = style.BotonSecundario.font,
corner_radius = style.BotonSecundario.corner_radius,
hover_color = style.BotonSecundario.hover_color
"""

class megaTitulo():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.font = ("Segoe UI", -60, "bold")
MegaTitulo = megaTitulo()

"""
text_color = style.MegaTitulo.text_color,
font = style.MegaTitulo.font
"""

class titulo():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.font = ("Segoe UI", -40, "bold")
Titulo = titulo()

"""
text_color = style.Titulo.text_color,
font = style.Titulo.font
"""

class subtitulo():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.font = ("Segoe UI", -32)
Subtitulo = subtitulo()

"""
text_color = style.Subtitulo.text_color,
font = style.Subtitulo.font
"""

class texto():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.font = ("Segoe UI", -20)
Texto = texto()

"""
text_color = style.Texto.text_color,
font = style.Texto.font
"""

class textoItalica():
    def __init__(self):
        self.text_color = Colores.Gray[4]
        self.font = ("Segoe UI", -20, "italic")
TextoItalica = textoItalica()

"""
text_color = style.TextoItalica.text_color,
font = style.TextoItalica.font
"""


class entryNormal():
    def __init__(self):
        self.fg_color = Colores.MainColor[2]
        self.border_color = Colores.Gray[4]
        self.text_color = Colores.Gray[4]
        self.font = ("Segoe UI", -13)
        self.corner_radius = 6
EntryNormal = entryNormal()

"""
fg_color = style.EntryNormal.fg_color,
border_color = style.EntryNormal.border_color,
text_color = style.EntryNormal.text_color,
font = style.EntryNormal.font,
corner_radius = style.EntryNormal.corner_radius
"""