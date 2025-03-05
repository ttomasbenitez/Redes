from socket import *
from lib.socketUdpPack import SocketUdpR
from lib.constantes import UPLOAD, ROJO, RESET

class Upload:

    def __init__(self, log, upload_config) -> None:
        self.log = log
        self.config = upload_config

    def _anotar_msj(self, msj):
        if self.config.verbose(): 
          print(f"{msj}")
        self.log.loggear(msj)
    
    def leer_archivo_a_bytes(self):
        with open(self.config.path_archivo(), 'rb') as archivo:
            contenido_bytes = archivo.read()   
        
        if self.config.verbose():
            self._anotar_msj(f"[Cliente] - Se leyo correctamente {self.config.path_archivo()} de archivo exitosa")

        return contenido_bytes

    def correr(self):
        try:
            self._anotar_msj("[Cliente] - Iniciando upload")
            socket_cliente = SocketUdpR()
            
            self._anotar_msj(f"[Cliente] - Conectando con {self.config.ip_dest()}:{self.config.puerto_dest()}")
            
            socket_cliente.connect(UPLOAD, 
                                   self.config.protocolo(),
                                   self.config.nombre_archivo(), 
                                   (self.config.ip_dest(), self.config.puerto_dest()))
            self._anotar_msj(f"[Cliente] - Se conecto con {self.config.ip_dest()}:{self.config.puerto_dest()}")
           
            contenido = self.leer_archivo_a_bytes()
            
            self._anotar_msj(f"[Cliente] - Enviando {self.config.path_archivo()} a {self.config.ip_dest()}:{self.config.puerto_dest()}")
            socket_cliente.sendAll(contenido,self.config.verbose())

            
            self._anotar_msj(f"[Cliente] - Se envio correctamente el archivo {self.config.path_archivo()}")

        except Exception as err:
            self._anotar_msj(ROJO + f"[Error] - {err}\n" + RESET)
        except KeyboardInterrupt as err: 
            self._anotar_msj(ROJO + f"[Error] - Se corto la ejecuacion\n" + RESET)
            
            socket_cliente.socket.close()



    


