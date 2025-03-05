import os
import select
import sys
from lib.socketUdpPack import SocketUdpR, FailedToConnect
from lib.constantes import UPLOAD, DOWNLOAD, ROJO, RESET
from threading import Event, Thread

class Servidor: 

    def __init__(self, log_server, servidor_config):
        self.log = log_server
        self.config = servidor_config
        self.socket = SocketUdpR()
        self.socket.bind((self.config.ip_server(), self.config.puerto_server()))
        self.activo = True
        
    def _anotar_msj(self, msj):
        if self.config.verbose(): 
          print(f"{msj}")
        self.log.loggear(msj)

    def correr(self):
        self._anotar_msj(f"[Servidor] - Se inicio el servidor en {self.config.ip_server()}:{self.config.puerto_server()}")
        
        thread_exit = Thread(target=self._control_entrada)
        thread_exit.start()
        
        threads = []

        while self.activo:
            try:
                solicitud = self.socket.listen()
                
                if solicitud is None: 
                    break
                
                msj_inicial, direccionPeticion  = solicitud
                nueva_conexion = Thread(target=self._trabajador, args=(msj_inicial, direccionPeticion))
                
                threads.append(nueva_conexion)
                nueva_conexion.start()
                threads = [thread for thread in threads if thread.is_alive()]
    
            except KeyboardInterrupt:
                break
        
        self._cerrar_servidor(threads)
        
    def _cerrar_servidor(self, threads = []):
        self.activo = False
        self._anotar_msj(f"[Servidor] - Cerrando ...")
        
        for thread in threads:
            thread.join()

        self.socket.cierre()
        self._anotar_msj(f"[Servidor] - Cerrado")
    
        

    def _control_entrada(self):
        while self.activo:
            ready, _, _ = select.select([sys.stdin], [], [], 1.0)

            if ready:
                comando = sys.stdin.readline().strip().lower()
                if comando in ['q', 'exit', 'quit', '^C']:
                    try:
                        self.socket.forzar_cierre()
                    except:
                        break
            else:
                if not self.activo:
                    break 
                 
            
    def _trabajador(self, msj_inicial, direccion):
        try:
            socket_nuevo = SocketUdpR() #crea un nuevo socket para la comunicación
            socket_nuevo.bind((self.config.ip_server(), 0))
            
            operacion,nombre_archivo,protocolo = msj_inicial.split("&")
            operacion = int(operacion)

            msj_respuesta,error = self._confirmar_parametros(nombre_archivo, operacion)
            
            self._anotar_msj(f"[Servidor] - Conectandose con {direccion}")
            socket_nuevo.confirmar_comunicacion(direccion, protocolo, msj_respuesta, error) # envía el puerto de comunicación al cliente
            self._anotar_msj(f"[Servidor] - Conectando con {direccion}")
             
            if operacion == DOWNLOAD and not error:
                self._download(nombre_archivo, socket_nuevo, direccion)
            elif operacion == UPLOAD and not error:
                self._upload(socket_nuevo, nombre_archivo, direccion)
                
        except Exception as e:
            self._anotar_msj(ROJO + f"[Error] - {e}" + RESET)
            
            
        socket_nuevo.cierre()

    def _confirmar_parametros(self, archivo, operacion):
        archivo_path = self.config.path_repositorio() + archivo
        if (not os.path.exists(archivo_path)) and (operacion == DOWNLOAD):
            return "No existe el archivo", True
        elif (not os.path.isfile(archivo_path)) and (operacion == DOWNLOAD): 
            return  "No se puede mandar lo solicitado", True
        
        return "",False
        
    def _download(self, nombre_archivo, socket_nuevo, direccion):        
        datos = self._leer_archivo(nombre_archivo)   

        self._anotar_msj(f"[Servidor] - Enviando archivo {nombre_archivo} a {direccion}")

        socket_nuevo.sendAll(datos)
        
        self._anotar_msj(f"[Servidor] - Archivo {nombre_archivo} enviado a {direccion}")
        
        
    def _leer_archivo(self, nombre_archivo):
        archivo_path = self.config.path_repositorio() + nombre_archivo
        self._anotar_msj(f"[Servidor] - Intentando leer archivo {nombre_archivo} en {archivo_path}")
            
        with open(archivo_path, 'rb') as archivo:
            return archivo.read()
    
    def _upload(self, socket_nuevo, nombre_archivo, direccion):
        datos = socket_nuevo.recieveAll()
        self._crear_archivo(datos, nombre_archivo)  
        self._anotar_msj(f"[Servidor] - Recibidos {len(datos)} bytes desde {direccion}")

    def _crear_archivo(self, datos, nombre_archivo):
        archivo = self.config.path_repositorio() + nombre_archivo
        with open(archivo, 'wb') as archivo:
            archivo.write(datos)
            