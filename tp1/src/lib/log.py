from datetime import datetime

class Log:
    def __init__(self, file_path = ".log"):
        """Inicializa la clase Log con la dirección del archivo."""
        self.file_path = file_path

    def loggear(self, message):
        """Escribe el mensaje recibido en el archivo con un timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} | {message}"
        
        try:
            with open(self.file_path, 'a') as file:  # 'a' para agregar al final del archivo
                file.write(log_entry + '\n')
        except Exception as e:
            print(f"Error al escribir en el archivo: {e}")
            
            
