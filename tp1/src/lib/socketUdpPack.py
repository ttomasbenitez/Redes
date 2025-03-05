import socket
import math
from lib.paquete import *
from lib.constantes import *
from lib.barra_de_carga import ProgressBar, BarraIndeterminada


class FailedToConnect(Exception):
    def __init__(self, message= "Failed to connect to the server"):
        self.message = message
        super().__init__(self.message)
        
class SocketUdpR:

    def __init__(self):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.protocolo = None 
        self.operacion = None 
        self.portIp_comunicacion = None 
        self.error = NOTERROR


    def bind(self, miIp_miPuerto): 
        self.socket.bind(miIp_miPuerto)
    
    def listen(self):
        self.socket.settimeout(None)
        while True:
            paquete_bytes, addr = self.socket.recvfrom(PACK_SIZE)
            if len(paquete_bytes) == 0:
                return
            
            paquete = Paquete.bytes_a_paquete(paquete_bytes)
            msj_inicial = paquete.payload.decode()
            
            return msj_inicial, addr
            
    

    # Envía el nuevo puerto para el cliente
    def confirmar_comunicacion(self, direccion, protocolo, msj_respuesta, error = False):
        self.portIp_comunicacion = direccion
        self.protocolo = protocolo
        
        msj_respuesta_bytes = msj_respuesta.encode()
        paquete = Paquete(INICIO, int(error), PACK_NOT_END, msj_respuesta_bytes)
        
        self.socket.settimeout(TIMEOUT_SECONDS)
        timeouts = 0

        while True:
            try:
                self.socket.sendto(paquete.bytes, self.portIp_comunicacion)
                _, addr = self.socket.recvfrom(PACK_SIZE)
                if addr != self.portIp_comunicacion: 
                    continue
        
                break 
            except socket.timeout:
                timeouts += 1
                if timeouts > MAX_TIMEOUTS:
                    raise FailedToConnect()
                

    def connect(self, operacion, protocolo, file_name, portIp_comunicacion):
        self.portIp_comunicacion = portIp_comunicacion
        self.protocolo = protocolo
        
        payload = f"{operacion}&{file_name}&{protocolo}"
        paquete = Paquete(INICIO, NOTERROR, PACK_NOT_END, payload.encode())
        
        self.socket.settimeout(TIMEOUT_SECONDS)
        timeouts = 0

        while True:
            try:
                self.socket.sendto(paquete.bytes, self.portIp_comunicacion)
                paquete_bytes, addr = self.socket.recvfrom(PACK_SIZE)

                if addr[0] != socket.gethostbyname(self.portIp_comunicacion[0]): 
                    continue
                break
            except socket.timeout:
                timeouts += 1
                if timeouts > MAX_TIMEOUTS:
                    raise FailedToConnect(f"No se pudo establecer la conexion con {portIp_comunicacion}")


        paquete_recibido = Paquete.bytes_a_paquete(paquete_bytes)
        msj_respuesta = paquete_recibido.payload.decode()
        self.portIp_comunicacion = (self.portIp_comunicacion[0], addr[1])
        
        paquete_confirmacion = Paquete(INICIO, 0, PACK_END, b"")
        self.socket.sendto(paquete_confirmacion.bytes, self.portIp_comunicacion)
        
        if paquete_recibido.error: 
            raise Exception(msj_respuesta)
        
    def sendAll(self, mensaje:bytes, show_progress_bar = False):
        cantidadDePaquetes = math.ceil(len(mensaje) / PAYLOAD_SIZE)

        if self.protocolo == STOP_WAIT:
            self.send_stop_and_wait(mensaje, cantidadDePaquetes, show_progress_bar)
        elif self.protocolo == SELECTIVE_REPEAT:
            self.send_sack(mensaje, cantidadDePaquetes, show_progress_bar)
            
        return
    
    def recieveAll(self, show_progress_bar = False):
        if self.protocolo == STOP_WAIT:
            return self.recieve_stop_and_wait(show_progress_bar)
        elif self.protocolo == SELECTIVE_REPEAT:
            return self.recieve_sack(show_progress_bar)
    

    def send_stop_and_wait(self, mensaje: bytes, cantidadPaquetes : int, show_progress_bar):
        
        self.socket.settimeout(0.02)
        progress_bar = ProgressBar(cantidadPaquetes, prefix='Progreso')

        seqnumber = 0
        timeouts = 0

        while seqnumber < cantidadPaquetes:
            ack_llego = False
            inicio_men = seqnumber * PAYLOAD_SIZE    
            final_men = (seqnumber + 1) * PAYLOAD_SIZE

            if seqnumber == cantidadPaquetes - 1:
                payload = mensaje[inicio_men:]
                paquete = Paquete (seqnumber, self.error, PACK_END, payload)
            else:
                payload = mensaje[inicio_men:final_men]
                paquete = Paquete (seqnumber, self.error, PACK_NOT_END, payload)
            

            while ack_llego is False:
                try:
                    self.socket.sendto(paquete.bytes, self.portIp_comunicacion)
                    ack_paq = self.recibir_paqute()

                    if(ack_paq.seqnumber == seqnumber):
                        ack_llego = True
                        seqnumber += 1
                        timeouts = 0
                        if show_progress_bar:
                            progress_bar.update(seqnumber)

                except socket.timeout:
                    timeouts += 1
                    if timeouts > 50: 
                        if seqnumber == cantidadPaquetes - 1: # Es muy improbable que en 15 intentos con 10 % de perdida se pierda el paquete para evitar el bucle del ultimo ACK asumimos que llega
                            ack_llego = True
                            seqnumber += 1
                            if show_progress_bar:
                                progress_bar.update(seqnumber)
                        else: 
                            raise FailedToConnect(f"Se perdio la coneccion con {self.portIp_comunicacion}")
        
        self.socket.settimeout(None)
        if show_progress_bar:
            progress_bar.finish()


    def recieve_stop_and_wait(self, show_progress_bar):
        if show_progress_bar:
            barraDeCarga = BarraIndeterminada()

        self.socket.settimeout(5)
        mensajeFin = bytearray()
        fin = PACK_NOT_END

        ultimoSeqNumbRe = 0
        timeout = 0
        
        while fin == PACK_NOT_END:
            try:
                paquete = self.recibir_paqute()
                timeout = 0
                 
                if paquete.seqnumber == ultimoSeqNumbRe:                    
                    mensajeFin.extend(paquete.payload)
                    ultimoSeqNumbRe = 1 + ultimoSeqNumbRe
                    if show_progress_bar:
                        barraDeCarga.actualizar(len(paquete.payload))

                fin = paquete.fin  
    
                paqueteConf = Paquete(ultimoSeqNumbRe - 1, self.error, PACK_NOT_END, b"")
                self.socket.sendto(paqueteConf.bytes, self.portIp_comunicacion)

            except socket.timeout:
                timeout += 1
                if timeout > MAX_TIMEOUTS: 
                    raise FailedToConnect(f"Se perdio la coneccion con {self.portIp_comunicacion}")

        self.socket.settimeout(None)
        return mensajeFin

    
    def recibir_paqute(self):
        paq_bytes, _ = self.socket.recvfrom(PACK_SIZE)
        return Paquete.bytes_a_paquete(paq_bytes)


    def send_sack(self, mensaje: bytes, cantidad_paquetes : int, show_progress_bar):
        progress_bar = None
        cantidad_enviados = 0
        if show_progress_bar:
            progress_bar = ProgressBar(cantidad_paquetes, prefix='Progreso')
    
        self.socket.settimeout(0.01)
        acks = [False] * cantidad_paquetes
        base = 0
        timeout = 0
        
        while True:

            if base >= cantidad_paquetes:
                paquete_final = Paquete(0, NOTERROR, PACK_END, b"")
                for i in range(10):
                    self.socket.sendto(paquete_final.bytes, self.portIp_comunicacion)
                break
            
            for i in range(WINDOW_SIZE):
                seq = base + i
                if seq < len(acks) and not acks[seq]:
                    inicio_men = seq * PAYLOAD_SIZE
                    final_men = min((seq + 1) * PAYLOAD_SIZE, cantidad_paquetes * PAYLOAD_SIZE)
                    payload = mensaje[inicio_men:final_men]
                    paquete = Paquete(seq, NOTERROR, PACK_NOT_END, payload)
                    self.socket.sendto(paquete.bytes, self.portIp_comunicacion)
                   
                    
                    if seq + 1 == cantidad_paquetes:
                        for i in range(15):
                            self.socket.sendto(paquete.bytes, self.portIp_comunicacion)
                        break
            

            while True:
                if base >= cantidad_paquetes:
                    break
                
                try: 
                    paquete_sack = self.recibir_paqute()
                    timeout = 0
                    
                    if paquete_sack.seqnumber >= base: 
                        for i in range(base, paquete_sack.seqnumber + 1):
                            if show_progress_bar and not acks[i]:
                                cantidad_enviados += 1
                            acks[i] = True
                        
                        for _ in range(paquete_sack.seqnumber - base + 1):
                            seq = base + WINDOW_SIZE
                            base += 1
                            if seq < len(acks) and not acks[seq]:    
                                inicio_men = seq * PAYLOAD_SIZE
                                final_men = min((seq + 1) * PAYLOAD_SIZE, cantidad_paquetes * PAYLOAD_SIZE)
                                payload = mensaje[inicio_men:final_men]
                                paquete = Paquete(seq,0, PACK_NOT_END, payload)
                                self.socket.sendto(paquete.bytes, self.portIp_comunicacion)

                    
                    else:
                        seq = paquete_sack.seqnumber + 1 
                        inicio_men = seq *PAYLOAD_SIZE
                        final_men = min((seq + 1) *PAYLOAD_SIZE, cantidad_paquetes *PAYLOAD_SIZE)
                        payload = mensaje[inicio_men:final_men]
                        paquete = Paquete(seq, 0, PACK_NOT_END, payload)
                        self.socket.sendto(paquete.bytes, self.portIp_comunicacion)
                        
                    sack = self.unpack_sack_payload(paquete_sack.payload)
                    for inicio, fin in sack:
                        for i in range(inicio, fin + 1):
                            if show_progress_bar and not acks[i]:
                                cantidad_enviados += 1
                            acks[i] = True
                            
                    if show_progress_bar:
                        progress_bar.update(cantidad_enviados)
                        
                except socket.timeout:
                    timeout += 1
                    if timeout > MAX_TIMEOUTS: 
                        raise FailedToConnect(f"Se perdio la coneccion con {self.portIp_comunicacion}")
                    break
            
        if show_progress_bar:
            progress_bar.finish()

    def recieve_sack(self, show_progress_bar):
        if show_progress_bar:
            barraDeCarga = BarraIndeterminada()

        data = bytearray()
        self.socket.settimeout(0.1)
        received = {}
        ultimo_ack = -1  # Inicializamos el último ACK enviado
        sack_intervals = []  # Almacenará los intervalos de secuencias fuera de orden
        timeout = 0
        sack_payload = b""
        final = PACK_NOT_END
        
        while final == PACK_NOT_END: 
            try: 
                paquete = self.recibir_paqute()
                final = paquete.fin
                timeout = 0
                # me llega un seqnumber -1
                
                # Si es el siguiente en secuencia
                if paquete.seqnumber == ultimo_ack + 1:
                    # Actualizamos el último ACK y limpiamos los intervalos recibidos fuera de orden
                    ultimo_ack = paquete.seqnumber
                    received[ultimo_ack] = paquete.payload
                    if show_progress_bar :
                        barraDeCarga.actualizar(len(paquete.payload))

                    # Limpiamos intervalos SACK que ya fueron reconocidos
                    new_intervals = []
                    for inicio, fin in sack_intervals:
                        if fin <= ultimo_ack:
                            continue  # Ya ha sido reconocido
                        elif inicio <= ultimo_ack:
                            # Acortar el intervalo si ha avanzado
                            new_intervals.append((ultimo_ack + 1, fin))
                        else:
                            new_intervals.append((inicio, fin))
                    sack_intervals = new_intervals
                    # Después de actualizar los intervalos, verificamos si podemos avanzar más el ACK
                    # Si el siguiente paquete en el primer intervalo cubre el siguiente en secuencia, avanzamos el ACK
                    while sack_intervals and sack_intervals[0][0] == ultimo_ack + 1:
                        # Avanzamos el ACK al final del primer intervalo
                        ultimo_ack = sack_intervals[0][1]
                        sack_intervals.pop(0)  # Eliminamos el primer intervalo ya que está cubierto
                    

                else:
                    if paquete.seqnumber <= ultimo_ack:
                        # Reenviamos el último ACK y SACK sin modificar nada
                        paquete_sack = Paquete(ultimo_ack,0, 0, sack_payload)
                        self.socket.sendto(paquete_sack.bytes, self.portIp_comunicacion)
                        continue


                    # Paquete fuera de orden, agregamos el intervalo a sack_intervals
                
                    if paquete.seqnumber not in received:
                        received[paquete.seqnumber] = paquete.payload
                        if show_progress_bar:
                            barraDeCarga.actualizar(len(paquete.payload))

                    sack_intervals.append((paquete.seqnumber, paquete.seqnumber))
                    sack_intervals = self.merge_intervals(sack_intervals)  # Unimos intervalos si es necesario

                # Crear el paquete SACK con el último ACK y los intervalos de secuencias fuera de orden
                if paquete.seqnumber != -1: 
                    sack_payload = self.create_sack_payload(sack_intervals)
                    paquete_sack = Paquete(ultimo_ack, 0, 0, sack_payload)
                    self.socket.sendto(paquete_sack.bytes, self.portIp_comunicacion)
                
                
            except socket.timeout:
                timeout += 1
                if timeout > MAX_TIMEOUTS:
                    raise FailedToConnect(f"Se perdio la coneccion con {self.portIp_comunicacion}")

            
        sorted_mess = dict(sorted(received.items()))
        for value in sorted_mess.values():
            data.extend(value)

        return data
    
    def merge_intervals(self, intervals):
        if not intervals:
            return []
    
        # Ordenamos los intervalos por el inicio
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]

        for current in intervals[1:]:
            prev = merged[-1]
            if current[0] <= prev[1] + 1:  # Si se superpone o es contiguo, unir
                merged[-1] = (prev[0], max(prev[1], current[1]))
            else:
                merged.append(current)

        return merged
    

    def create_sack_payload(self, sack_intervals):
        payload = b""
        for inicio, fin in sack_intervals:
            payload += struct.pack("!II", inicio, fin)
        return payload
    
    def unpack_sack_payload(self, payload):
        sack_intervals = []
        tam_intervalo = 8  # 4 bytes por entero (inicio, fin)
        
        # Iterar sobre el payload en bloques de 8 bytes
        if len(payload) < 8 or len(payload) % 8 != 0:
            return []
        for i in range(0, len(payload), tam_intervalo):
            inicio, fin = struct.unpack("!II", payload[i:i + tam_intervalo])
            sack_intervals.append((inicio, fin))

        return sack_intervals

    def cierre(self):
        self.socket.close()
        
    def forzar_cierre(self):
        self.socket.shutdown(socket.SHUT_RDWR) 
        self.socket.close()