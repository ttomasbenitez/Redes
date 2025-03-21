PAYLOAD_SIZE = 1024
SEQ_NUM_SIZE = 4
ERROR_SIZE = 1
END_SIZE = 1

HEADER_SIZE = SEQ_NUM_SIZE + ERROR_SIZE + END_SIZE
PACK_SIZE = HEADER_SIZE + PAYLOAD_SIZE

PACK_END = 1
PACK_NOT_END = 0

UPLOAD = 0
DOWNLOAD = 1

TIMEOUT_SECONDS = 2
MAX_TIMEOUTS = 15
TIMEOUT_TWH = 3

STOP_WAIT = "SW"
SELECTIVE_REPEAT = "SR"

# Flags
VERBOSITY_OFF = 0
VERBOSITY_ON = 1

WINDOW_SIZE = 8

#colores
ROJO = "\033[31m"
RESET = "\033[0m" 

#error 
ERROR = 1 
NOTERROR = 0

INICIO = -1