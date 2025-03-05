from socket import *
from lib.socketUdpPack import SocketUdpR
from lib.constantes import DOWNLOAD, ROJO, RESET


class Download:

    def __init__(self, log, download_config) -> None:
        self.log = log
        self.config = download_config

    def _anotar_msj(self, msj):
        if self.config.verbose(): 
          print(f"{msj}")
        self.log.loggear(msj)
    
    def guardar_bytes_a_archivo(self, contenido_bytes):
        with open(self.config.path_archivo(), 'wb') as archivo:
            archivo.write(contenido_bytes)

        self._anotar_msj(f"\nSe descargó correctamente y se guardó en {self.config.path_archivo()}")

    def run(self):
        try:
            socket_cliente = SocketUdpR()
            self._anotar_msj("[Cliente] - Iniciando download")
            
            self._anotar_msj(f"[Cliente] - Conectando con {self.config.ip_dest()}:{self.config.puerto_dest()}")
            socket_cliente.connect(DOWNLOAD, 
                                   self.config.protocolo(),
                                   self.config.nombre_archivo(), 
                                   (self.config.ip_dest(), self.config.puerto_dest()))
            self._anotar_msj(f"[Cliente] - Se conecto con {self.config.ip_dest()}:{self.config.puerto_dest()}")
            
            self._anotar_msj(f"[Cliente] - Recibiendo el archivo {self.config.path_archivo()}") 
            contenido = socket_cliente.recieveAll(self.config.verbose())
            
            self.guardar_bytes_a_archivo(contenido)
            self._anotar_msj(f"[Cliente] - Se recibió correctamente el archivo {self.config.path_archivo()}")
            
        except Exception as err:
            self._anotar_msj(ROJO + f"[Error] - {err}" + RESET)
        except KeyboardInterrupt as err: 
            self._anotar_msj(ROJO + f"[Error] - Se corto la ejecucion" + RESET)
        
        socket_cliente.socket.close()
