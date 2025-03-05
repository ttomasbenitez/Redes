import struct
from lib.constantes import HEADER_SIZE
# seqnumber |   error   |    operacion   |   fin    |
#----------------------------------------------
#                   PAYLOAD
#
class Paquete:

    def __init__(self, seqnumber : int, error: int, fin: int, payload: bytes):
        
        self.seqnumber = seqnumber
        self.error = error
        self.fin = fin
        self.payload = payload

        largue = len(payload)

        # Usar pack es mucho mas eficiente to_bytes (Para 1M de casos 0.26 contra 0.31)
        self.bytes = struct.pack(f"!i 2b {largue}s", seqnumber, error, fin, payload)

    def get_bytes(self):
        return self.bytes
    
    @staticmethod
    def bytes_a_paquete(paq_bytes: bytes):
        # Unpack with signed integer for seqnumber
        seqnumber, error, fin = struct.unpack("!i 2b", paq_bytes[0:HEADER_SIZE])
        payload = paq_bytes[HEADER_SIZE:]

        return Paquete(seqnumber, error, fin, payload)


#ejemplo de paquete

#pak = Paquete(1,0,1,0,b"F40000011")
#print(pak.returnBytes())
#pak.paqueteBytesnormal(pak.bytes)
        # seqnumber |   error   |    operacion   |   fin    | payload