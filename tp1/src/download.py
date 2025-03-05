from lib.cliente.download_implementation import Download 
from lib.log import Log 
from lib.config import DownloadConfig

if __name__ == "__main__":
    download = Download(Log(), DownloadConfig())
    download.run()