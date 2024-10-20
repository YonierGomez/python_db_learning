# Simulamos el archivo 'mi_modulo.py'

class RespuestaSimulada:
    def __init__(self, codigo, contenido):
        self.status_code = codigo
        self.text = contenido

def get(url):
    # Esta función simula hacer una solicitud GET
    print(f"Solicitando la URL: {url}")
    # Creamos un objeto de la clase RespuestaSimulada
    return RespuestaSimulada(200, "Contenido de la página simulada")
