from lib.servidor.server import Servidor 
from lib.log import Log 
from lib.config import ServidorConfig

if __name__ == "__main__":
    servidor = Servidor(Log(".logserver"), ServidorConfig())
    servidor.correr()