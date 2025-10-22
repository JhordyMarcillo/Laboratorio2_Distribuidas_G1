import socket
import csv
import json
import os

ARCHIVO_NRC = 'nrcs.csv'

def inicializar_nrcs():
    """Crea el archivo CSV de NRCs si no existe."""
    if not os.path.exists(ARCHIVO_NRC):
        with open(ARCHIVO_NRC, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['NRC', 'Materia'])
            # Ejemplo de NRCs válidos
            writer.writerow(['MAT101', 'Matemáticas'])
            writer.writerow(['PRO102', 'Programación'])
            writer.writerow(['BD103', 'Bases de Datos'])

def buscar_nrc(nrc):
    """Busca un NRC en el archivo y devuelve su información."""
    try:
        with open(ARCHIVO_NRC, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['NRC'] == nrc:
                    return {"status": "ok", "data": row}
        return {"status": "not_found", "mensaje": "NRC no existe"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def listar_nrcs():
    """Devuelve todos los NRCs disponibles."""
    try:
        with open(ARCHIVO_NRC, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def procesar_comando(comando):
    partes = comando.strip().split('|')
    op = partes[0]
    
    if op == 'BUSCAR NRC' and len(partes) == 2:
        return buscar_nrc(partes[1])
    elif op == 'LISTAR NRC':
        return listar_nrcs()
    else:
        return {"status": "error", "mensaje": "Comando inválido"}

def iniciar_servidor():
    inicializar_nrcs()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12346))
    server_socket.listen(5)
    print("Servidor de NRC escuchando en puerto 12346...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Cliente conectado desde {addr}")
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                respuesta = procesar_comando(data)
                client_socket.send(json.dumps(respuesta).encode('utf-8'))
            client_socket.close()
            print("Cliente desconectado.")
    except KeyboardInterrupt:
        print("Servidor NRC detenido.")
    finally:
        server_socket.close()

if __name__ == '__main__':
    iniciar_servidor()
