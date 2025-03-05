from lib.cliente.upload_implementation import Upload 
from lib.log import Log 
from lib.config import UploadConfig

if __name__ == "__main__":
    upload = Upload(Log(), UploadConfig())
    upload.correr()