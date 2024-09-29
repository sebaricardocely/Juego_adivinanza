#Sebastian Ricardo Alvarado Cely    CLIENTE-SERVIDOR

# Importo socket que permitirá la comunicación entre servidor y cliente, threading permitirá manejar varios clientes simuteneamente

import socket
import threading
import random


#funcion manejar cliente en la cual, genero un numero secreto y le envia mensajes al cliente para que intente adivinarlo.

def manejar_cliente(cliente_socket, direccion):
    print(f"[+] Conexión establecida con {direccion}")
    numero_secreto = random.randint(1, 100)
    intentos = 0
    cliente_socket.sendall("¡Bienvenido al Juego de Adivinanza de Números!\n".encode('utf-8'))
    cliente_socket.sendall("Estoy pensando en un número entre 1 y 100.\n".encode('utf-8'))
    cliente_socket.sendall("Intenta adivinarlo.\n".encode('utf-8'))
#Creacion de condicionales
    while True:
        try:
            datos = cliente_socket.recv(1024)
            if not datos:
                print(f"[-] Conexión cerrada por {direccion}")
                break
            intento = datos.decode('utf-8').strip()
            if not intento.isdigit():               
                mensaje = "Por favor, ingresa un número válido.\n"
                cliente_socket.sendall(mensaje.encode('utf-8'))
 #Si el cliente ingresa numero equivocado responde el anterior mensaje el servidor.       
    
                continue
            intento = int(intento)
            intentos += 1
#El cliente ingresa numero correcto y el servidor le indicara si el numero es mas alto o bajo.
            if intento < numero_secreto:
                mensaje = "Demasiado bajo. Intenta de nuevo.\n"
            elif intento > numero_secreto:
                mensaje = "Demasiado alto. Intenta de nuevo.\n"
            else:
                mensaje = f"¡Correcto! Adivinaste el número en {intentos} intentos.\n"
                cliente_socket.sendall(mensaje.encode('utf-8'))
                print(f"[+] {direccion} Has adivinado el numero {numero_secreto} en {intentos} intentos.")
                break
            cliente_socket.sendall(mensaje.encode('utf-8'))
        except ConnectionResetError:
            print(f"[-] Conexión inesperadamente cerrada por {direccion}")
            break
    cliente_socket.close()

def iniciar_servidor(host='0.0.0.0', puerto=65434):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_socket.bind((host, puerto))
    servidor_socket.listen(5)
    print(f"[+] Servidor escuchando en {host}:{puerto}")

    try:
        while True:
            cliente_socket, direccion = servidor_socket.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(cliente_socket, direccion))
            hilo.start()
    #se permite cerrar con el teclado el servidor
    except KeyboardInterrupt:
        print("\n[!] Cerrando servidor.")
    finally:
        servidor_socket.close()

if __name__ == "__main__":
    iniciar_servidor()
