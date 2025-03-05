import sys
class ProgressBar:
    def __init__(self, total, prefix='', length=40, fill='█'):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.fill = fill
        self.current = 0

    def update(self, value):
        self.current = value
        self.current = min(self.current, self.total)  # Evitar que exceda el total
        percent = (self.current / self.total) * 100
        filled_length = int(self.length * self.current // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent:.2f}% Completo')
        sys.stdout.flush()

    def finish(self):
        sys.stdout.write('\n')  # Para finalizar la línea
        sys.stdout.flush()

class BarraIndeterminada:
    def __init__(self):
        self.longitud_barra = 40
        self.posicion = 0
        self.paquetes_recibidos = 0

    def actualizar(self, payload):
        self.paquetes_recibidos += payload
        self.posicion = (self.posicion + 1) % self.longitud_barra
        barra = ['-'] * self.longitud_barra
        barra[self.posicion] = '█'
        sys.stdout.write(f"\r[{''.join(barra)}]")  
        sys.stdout.write(f"   Bytes  Recibidos: {self.paquetes_recibidos} Bytes")
        sys.stdout.flush()

