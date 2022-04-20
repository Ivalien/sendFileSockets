import os
import socket
import tqdm
# Se crea un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Se une el socket creado a puerto local 10000
server_address = ('localhost', 5001)
sock.bind(server_address)
# Recibe 4096 bytes
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
# El servidor se mantiene a la escucha de una solicutd de conexion
sock.listen(1)
#Esperando la conexion mientras que no cambie el calor a 0
print('Esperando Conexion entrante')
connection, client_address = sock.accept()
print('Conexion desde: ', client_address)
# Se recibe la informacion del archivo entrante por medio del socket del cliente
received = connection.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
#Convierte el tamaño de archivo a entero
filesize = int(filesize)
#Barra de progreso que indica cuanta informacion se ha obtenido
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # Lee el valor del buffer que esta recibiendo
        bytes_read = connection.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        # Cuando termina de leer el budder escribe en un archivo los datos
        f.write(bytes_read)
        # Actualiza la barra de profreso
        progress.update(len(bytes_read))
#Se cierra la conexion cuando termina de recibir informacion
connection.close()