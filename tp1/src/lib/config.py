import argparse
from lib.constantes import STOP_WAIT, SELECTIVE_REPEAT, VERBOSITY_ON, VERBOSITY_OFF

class Configuracion:
    "Se ocupa de parsear y guardar los argumentos introducido por el usurio, \
        acorde al comando "
        
    def __init__(self):
        """Inicializa la configuración base."""
        self.parser = argparse.ArgumentParser()


class UploadConfig(Configuracion):
    def __init__(self):
        """Configuración específica para el comando upload."""
        super().__init__()
        
        self.parser.description = "Comando upload: envía un archivo dado \
        al servidor para ser guardado con el nombre asignado"

        self.parser.usage = '%(prog)s [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ] [ - s FILEPATH ] [ - n FILENAME ] [-pro PROTOCOL]'
        
        self.parser.add_argument('-H', '--host', required=True, metavar='',type=str, help='server IP address')
        self.parser.add_argument('-p', '--port', required=True, metavar='', type=int, help='server port')
        self.parser.add_argument('-s', '--src', required=True,metavar='', type=str, help='source file path')
        self.parser.add_argument('-n', '--name', required=True,metavar='', type=str, help='file name')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
        self.parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
        self.parser.add_argument('-pro', '--protocol', required=True, type=str, help='select communication protocol')

        self.args = self.parser.parse_args()
        self.__verbose = False if self.args.quiet and (not self.args.verbose) else True 

          
    def ip_dest(self):
        "Devuelve la ip del servidor destino introducido por \
            el usario"
        return self.args.host 
    
    def puerto_dest(self):
        "Devuelve el puerto del servidor de estino introducido por \
            el usario"
        return self.args.port
    
    def path_archivo(self):
        "Devuelve la ubicacion del archivo a enviar introducido por \
            el usario"
        return self.args.src 
    
    def nombre_archivo(self):
        "Devuelve el nombre del archivo al ser guardado en el servidor \
            introdciodo por el usuario"
        return self.args.name
    
    def verbose(self):
        "Devuelve si esta activa o no verbose"
        return self.__verbose
    
    def stop_and_wait_esta_activo(self):
        "Devuelve si esta activa o no verbose"
        return self.args.stopandwait
    
    def protocolo(self):
        if self.args.protocol == 'sw':
            return STOP_WAIT
        elif self.args.protocol == 'sr':
            return SELECTIVE_REPEAT
    
class DownloadConfig(Configuracion):
    def __init__(self):
        """Configuración específica para el comando download."""
        super().__init__()
        
        self.parser.description = "Comando download: descarga un archivo especificado desde \
            el servidor"
        self.parser.usage = '%(prog)s [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ] [ - d FILEPATH ] [ - n FILENAME ] [-pro PROTOCOL]'

        self.parser.add_argument('-H', '--host', type=str,metavar='', required=True, help='server IP address')
        self.parser.add_argument('-p', '--port', type=int,metavar='', required=True, help='server port')
        self.parser.add_argument('-d', '--dst', type=str,metavar='', required=True, help='destination file path')
        self.parser.add_argument('-n', '--name', type=str,metavar='', required=True, help='file name')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
        self.parser.add_argument('-q', '--quiet',action='store_true', help='decrease output verbosity')
        self.parser.add_argument('-pro', '--protocol', metavar='', required=True, type=str, help='select communication protocol')

        self.args = self.parser.parse_args()
        self.__verbose = False if self.args.quiet and (not self.args.verbose) else True 

          
    def ip_dest(self):
        "Devuelve la ip del servidor destino introducido por \
            el usario"
        return self.args.host 
    
    def puerto_dest(self):
        "Devuelve el puerto del servidor de estino introducido por \
            el usario"
        return self.args.port
    
    def path_archivo(self):
        "Devuelve la ubicacion del archivo a enviar introducido por \
            el usario"
        return self.args.dst
    
    def nombre_archivo(self):
        "Devuelve el nombre del archivo al ser guardado en el servidor \
            introdciodo por el usuario"
        return self.args.name
    
    def verbose(self):
        "Devuelve si esta activa o no verbose"
        return self.__verbose
    
    def stop_and_wait_esta_activo(self):
        "Devuelve si esta activa o no verbose"
        return self.args.stopandwait
    
    def protocolo(self):
        if self.args.protocol == 'sw':
            return STOP_WAIT
        elif self.args.protocol == 'sr':
            return SELECTIVE_REPEAT

class ServidorConfig(Configuracion):
    def __init__(self):
        """Configuración específica para el comando servidor."""
        super().__init__()
        
        self.parser.description = "Inicia un servidor con la ip y puerto que proporciona descarga y subida de archivos"
        self.parser.usage = '%(prog)s [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ] [- s DIRPATH ]'
        
        self.parser.add_argument('-H', '--host', type=str, required=True, metavar='', help='server IP address')
        self.parser.add_argument('-p', '--port', type=int, required=True, metavar='', help='server port')
        self.parser.add_argument('-s', '--storage', type=str, required=True, metavar='', help='storage dir path')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
        self.parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')

        self.args = self.parser.parse_args()
        self.__verbose = False if self.args.quiet and (not self.args.verbose) else True 

          
    def ip_server(self):
        "Devuelve la ip del servidor destino introducido por \
            el usario"
        return self.args.host 
    
    def puerto_server(self):
        "Devuelve el puerto del servidor de estino introducido por \
            el usario"
        return self.args.port
    
    def path_repositorio(self):
        "Devuelve la ubicacion del repositorio introducido por \
            el usario para guardar los archivos"
        return self.args.storage
    
    def verbose(self):
        "Devuelve si esta activa o no verbose"
        return self.__verbose
    
    def stop_and_wait_esta_activo(self):
        "Devuelve si esta activa o no verbose"
        return self.args.stopandwait
