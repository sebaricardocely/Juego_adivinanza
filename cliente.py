#Sebastian Ricardo Alvarado Cely    CLIENTE-SERVIDOR

# importo biblioteca socket para la conexión
import socket
# Funcion para inciair conexión con el servidor
def iniciar_cliente(host='localhost', puerto=65434):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente_socket.connect((host, puerto))
        print(f"[+] Conectado al servidor en {host}:{puerto}")

        while True:
            datos = cliente_socket.recv(1024)
            if not datos:
                print("[-] El servidor ha cerrado la conexión.")
                break
            mensaje = datos.decode('utf-8')
            print(mensaje, end='')  
            # end='' para evitar doble salto de línea

            # Si el mensaje indica que el cliente adivinó correctamente, avisa y finaliza
            if "¡Correcto!" in mensaje:
                break

            # Solicitar al usuario que ingrese un intento
            intento = input("Tu intento: ")
            cliente_socket.sendall(intento.encode('utf-8'))

    except ConnectionRefusedError:
        print(f"[-] No se pudo conectar al servidor en {host}:{puerto}")
    except KeyboardInterrupt:
        print("\n[!] Cerrando cliente.")
    finally:
        cliente_socket.close()

if __name__ == "__main__":
    iniciar_cliente()
