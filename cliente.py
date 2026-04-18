import socket

#Configuracon de conexion 
HOST = "localhost"   # Dirección del servidor al que nos conectamos
PORT = 5000          # Puerto del servidor
BUFFER = 1024        # Tamaño máximo del buffer de recepción (bytes)
SALIDA = "exito"     # Palabra clave para cerrar el cliente


def iniciar_cliente():

  # Configuración del socket TCP/IP para el cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    try:
        #Intentar conectarse al servidor
        cliente_socket.connect((HOST, PORT))
        print(f"[CLIENTE] Conectado al servidor {HOST}:{PORT}")
        print(f"[CLIENTE] Escribí tus mensajes. Para salir, escribí '{SALIDA}'.\n")  

        while True: #Bucle de envio hasta recibir la palabra de salida 
            #Lee mensaje desde la entrada estándar
            mensaje = input("Vos → ").strip()
 
            #Valida que el mensaje no esté vacío
            if not mensaje:
                print("[CLIENTE] El mensaje no puede estar vacío. Intentá de nuevo.")
                continue

            #Envia el mensaje al servidor codificado en UTF-8
            cliente_socket.sendall(mensaje.encode("utf-8"))
 
            # Verifica si el usuario quiere terminar la sesión
            if mensaje.lower() == SALIDA:
                print("[CLIENTE] Sesión finalizada por el usuario.")
                
                
                break

            #Espera y muestra la respuesta del servidor
            try:
                respuesta = cliente_socket.recv(BUFFER).decode("utf-8")
                print(f"Servidor → {respuesta}\n")
 
            except ConnectionResetError:
                #El servidor cerró la conexión inesperadamente
                print("[CLIENTE] El servidor cerró la conexión.")
                break

    except ConnectionRefusedError:
        #El servidor no está corriendo o el puerto es incorrecto
        print(
            f"[ERROR] No se pudo conectar a {HOST}:{PORT}.\n"
            "Asegurate de que el servidor esté corriendo antes de iniciar el cliente."
        )
 
    except KeyboardInterrupt:
        #El usuario interrumpió con Ctrl+C
        print("\n[CLIENTE] Interrumpido por el usuario.")
 
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}")
 
    finally:
        #Siempre cerrar el socket al terminar, sin importar como salimos
        cliente_socket.close()
        print("[CLIENTE] Conexión cerrada.")




#Punto de entrada 
if __name__ == "__main__":
    iniciar_cliente()


