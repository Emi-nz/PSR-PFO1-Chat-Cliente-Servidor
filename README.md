# PFO1 - Chat Básico Cliente-Servidor con Sockets y Base de Datos

## Descripción
Implementación de un chat básico utilizando sockets TCP en Python. El servidor recibe mensajes de clientes, los almacena en una base de datos SQLite y responde con una confirmación. 

Trabajo práctico de la materia **Programación de Redes** — IFTS 29, 3er año.

---

## Archivos
- `servidor.py` — Servidor TCP que escucha conexiones, recibe mensajes y los guarda en la base de datos.
- `cliente.py` — Cliente que se conecta al servidor y permite enviar múltiples mensajes.
- `mensajes.db` — Base de datos SQLite generada automáticamente al iniciar el servidor.

---

## Tecnologías utilizadas
- Python 3
- Módulo `socket` — comunicación TCP/IP
- Módulo `sqlite3` — base de datos local
- Módulo `threading` — manejo de múltiples clientes

---

## Cómo ejecutarlo

**1. Iniciá el servidor** (terminal 1):
```bash
py servidor.py
```

**2. Iniciá el cliente** (terminal 2):
```bash
py cliente.py
```

**3.** Escribí los mensajes que quieras. Para cerrar el cliente escribí:
```
exito
```

---

## Ejemplo de uso
```
[SERVIDOR] Escuchando en localhost:5000 ...
[SERVIDOR] Cliente conectado: 127.0.0.1

Vos → Hola
Servidor → Mensaje recibido: 2026-04-18 14:32:05

Vos → exito
[CLIENTE] Sesión finalizada por el usuario.
```

---

## Base de datos
Cada mensaje se guarda en `mensajes.db` con los siguientes campos:

| Campo | Descripción |
|---|---|
| id | Clave primaria autoincremental |
| contenido | Texto del mensaje |
| fecha_envio | Fecha y hora de recepción |
| ip_cliente | IP del cliente que envió el mensaje |
