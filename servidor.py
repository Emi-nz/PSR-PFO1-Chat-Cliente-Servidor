import socket
import sqlite3
import threading
from datetime import datetime

#configuracion del servidor
HOST = "localhost" #Direccion donde escucha el servidor
PORT = 5000  #Puerto de escucha
DATABASE = "mensajes.db"

#inicializar la base de datos

def inicializar_db():
    try:
        conexion = sqlite3.connect(DATABASE)
        cursor = conexion.cursor()
        #Crea la base de datos SQLite y la tabla mensajes si no existen. La tabla tiene cuatro columnas: id (clave primaria autoincremental), contenido (texto del mensaje), fecha_envio (marca de tiempo) e ip_cliente (IP del cliente).
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)
        conexion.commit()
        conexion.close()
        print(f"[DB] base de datos '{DATABASE}' inicializada correctamente")

    except Exception as e:
        raise RuntimeError(f"[DB] No se pudo inicializar la base de datos: {e}")



def guardar_mensaje(contenido: str, ip_cliente: str) -> str: #Guarda un mensaje en la base de datos y retorna el timestamp de guardado
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conexion = sqlite3.connect(DATABASE)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)", (contenido, timestamp, ip_cliente))
        
        conexion.commit()
        conexion.close()
        print(f"[DB] Mensaje guardado correctamente de {ip_cliente} a las {timestamp}.")

    except Exception as e: #si la DB no es accesible, se registra el error pero el servidor continua funcionando
        print(f"[DB] Error al guardar el mensaje: {e}")

    return timestamp

   
def manejar_cliente(conn: socket.socket, direccion: tuple): #maneja la comunicacion con un cliente conectado en un hilo independiente
    ip_cliente = direccion[0]
    print(f"[SERVIDOR] Cliente conectado: {ip_cliente}:{direccion[1]}")

    try:
        while True: #Recibir datos del cliente, maximo 1024 bytes
            datos = conn.recv(1024)
            
            if not datos: # el cliente se desconecto
                print(f"[SERVIDOR] Conexion cerrada por el cliente {ip_cliente}.")
                break

            #Decodificamos el mensaje recibido
            mensaje = datos.decode("utf-8").strip()
            print(f"[SERVIDOR] Mensaje de {ip_cliente}: '{mensaje}'")

            # Guardamos en la base de datos y obtenemos el timestamp
            timestamp = guardar_mensaje(mensaje, ip_cliente)
 
            # Enviamos confirmación al cliente
            respuesta = f"Mensaje recibido: {timestamp}"
            conn.sendall(respuesta.encode("utf-8"))
 
    except ConnectionResetError:
        # El cliente se desconectó
        print(f"[SERVIDOR] {ip_cliente} se desconectó.")
 
    except Exception as e:
        print(f"[SERVIDOR] Error inesperado con {ip_cliente}: {e}")
 
    finally:
        # Siempre cerrar el socket del cliente al terminar
        conn.close()
        print(f"[SERVIDOR] Socket de {ip_cliente} cerrado.")



def inicializar_socket() -> socket.socket: #Crea y configura el socket TCP del servidor.
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Configuración del socket TCP/IP
        
        try:
            servidor_socket.bind((HOST, PORT)) #Asociar socket a dirección y puerto
            servidor_socket.listen(5) # Cola de hasta 5 conexiones pendientes
            print(f"[SERVIDOR] Escuchando en {HOST}:{PORT} ...")
            return servidor_socket

        except OSError as e: # Error puerto ya ocupado
            raise RuntimeError(
                f"[SERVIDOR] No se pudo iniciar el servidor en {HOST}:{PORT}. "
                f"¿El puerto esta ocupado? Detalle: {e}"
                )
 
 
def aceptar_conexiones(servidor_socket: socket.socket): #Bucle principal: acepta clientes entrantes y lanza un hilo por cada uno.

    print("[SERVIDOR] Esperando conexiones... (Ctrl+C para detener)\n")
 
    while True:
        try:
            #Bloquea hasta que un cliente se conecte
            conn, direccion = servidor_socket.accept()
 
            #Crea un hilo independiente para cada cliente
            hilo = threading.Thread(
                target=manejar_cliente,
                args=(conn, direccion),
                daemon=True   #El hilo finaliza si el programa principal termina
            )
            hilo.start()
 
        except KeyboardInterrupt:
            print("\n[SERVIDOR] Apagando servidor...")
            break
 
        except Exception as e:
            print(f"[SERVIDOR] Error al aceptar conexión: {e}")


if __name__ == "__main__": #Punto de entrada del programa
    try:
        #Inicializa la base de datos antes de aceptar clientes
        inicializar_db()
 
        #Crea y configura el socket del servidor
        srv_socket = inicializar_socket() 
 
        # Entra al bucle de aceptación de conexiones
        aceptar_conexiones(srv_socket)
 
    except RuntimeError as e:
        # Errores críticos de inicio (puerto ocupado o DB inaccesible)
        print(f"\n[ERROR CRÍTICO] {e}")
        print("[SERVIDOR] El servidor no pudo iniciarse.")
 
    finally:
        srv_socket.close()
        print("[SERVIDOR] Socket del servidor cerrado.")
