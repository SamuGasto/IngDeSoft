
class TablaVAC():
    def __init__(self) -> None:
        self.ComunicacionDeDatos = 0
        self.ProcesamientoDistribuido = 0
        self.ObjetivosDeRendimiento = 0
        self.ConfiguracionDelEquipamiento = 0
        self.TasaDeTransacciones = 0
        self.EntradaDeDatosEnLinea = 0
        self.InterfaseConElUsuario = 0
        self.ActualizacionEnLinea = 0
        self.ProcesamientoComplejo = 0
        self.ReusabilidadDelCodigo = 0
        self.FacilidadDeImplementacion = 0
        self.FacilidadDeOperacion = 0
        self.InstalacionesMultiples = 0
        self.FacilidadDeCambios = 0
        self.TotalFactorAjuste = 0

    def ActTotalFactorAjuste(self) -> None:
        sum = (
            self.ComunicacionDeDatos +
            self.ProcesamientoDistribuido +
            self.ObjetivosDeRendimiento +
            self.ConfiguracionDelEquipamiento +
            self.TasaDeTransacciones +
            self.EntradaDeDatosEnLinea +
            self.InterfaseConElUsuario +
            self.ActualizacionEnLinea +
            self.ProcesamientoComplejo +
            self.ReusabilidadDelCodigo +
            self.FacilidadDeImplementacion +
            self.FacilidadDeOperacion +
            self.InstalacionesMultiples +
            self.FacilidadDeCambios
        )
        self.TotalFactorAjuste = sum