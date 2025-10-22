import socket
import csv
import json
import os
import threading

# Archivo principal de almacenamiento
ARCHIVO_CSV = '../calificaciones.csv'

# -------------------------------------------------------------
# Funciones auxiliares para manejo del CSV de calificaciones
# -------------------------------------------------------------
def leer_calificaciones():
    """Lee el CSV de calificaciones y devuelve una lista de dicts.
    Acepta archivos con encabezado o sin encabezado.
    Estructura: {ID_Estudiante, Nombre, Materia, Calificacion}
    """
    filas = []
    if not os.path.exists(ARCHIVO_CSV):
        return filas
    try:
        with open(ARCHIVO_CSV, 'r', newline='') as f:
            primera = f.readline()
            if not primera:
                return filas
            f.seek(0)
            # Detectar si tiene encabezado
            if 'ID_Estudiante' in primera and 'Calificacion' in primera:
                reader = csv.DictReader(f)
                for row in reader:
                    filas.append({
                        'ID_Estudiante': row.get('ID_Estudiante', '').strip(),
                        'Nombre': row.get('Nombre', '').strip(),
                        'Materia': row.get('Materia', '').strip(),
                        'Calificacion': row.get('Calificacion', '').strip(),
                    })
            else:
                reader = csv.reader(f)
                for cols in reader:
                    if not cols or len(cols) < 4:
                        continue
                    filas.append({
                        'ID_Estudiante': str(cols[0]).strip(),
                        'Nombre': str(cols[1]).strip(),
                        'Materia': str(cols[2]).strip(),
                        'Calificacion': str(cols[3]).strip(),
                    })
    except Exception:
        # En caso de error de lectura, devolvemos lo que haya (posiblemente vacío)
        return filas
    return filas

def escribir_calificaciones(filas):
    """Escribe la lista de dicts en el CSV, normalizando con encabezado."""
    with open(ARCHIVO_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])
        writer.writeheader()
        writer.writerows(filas)
def inicializar_csv():
    """Crea el archivo CSV de calificaciones si no existe."""
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])

# -------------------------------------------------------------
# Función para consultar al servidor de NRC (inter-servidores)
# -------------------------------------------------------------
def consultar_nrc(nrc):
    """Consulta al servidor de NRC si un código de materia es válido."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12346))
        client_socket.send(f'BUSCAR NRC|{nrc}'.encode('utf-8'))
        respuesta = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return json.loads(respuesta)
    except Exception as e:
        return {"status": "error", "mensaje": f"Error consultando NRC: {e}"}

# -------------------------------------------------------------
# Operaciones CRUD sobre calificaciones
# -------------------------------------------------------------
def agregar_calificacion(id_est, nombre, materia, calif):
    """Agrega una nueva calificación después de validar el NRC."""
    res_nrc = consultar_nrc(materia)
    if res_nrc["status"] != "ok":
        return {"status": "error", "mensaje": "Materia/NRC no válida o servidor NRC no disponible"}

    try:
        with open(ARCHIVO_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([id_est, nombre, materia, calif])
        return {"status": "ok", "mensaje": f"Calificación agregada para {nombre}"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def buscar_por_id(id_est):
    """Busca una calificación por ID."""
    try:
        filas = leer_calificaciones()
        for row in filas:
            if row.get('ID_Estudiante') == id_est:
                return {"status": "ok", "data": row}
        return {"status": "not_found", "mensaje": "ID no encontrado"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def actualizar_calificacion(id_est, nueva_calif):
    """Actualiza la calificación de un estudiante existente."""
    try:
        filas = leer_calificaciones()
        actualizado = False
        for row in filas:
            if row.get('ID_Estudiante') == id_est:
                row['Calificacion'] = str(nueva_calif)
                actualizado = True
                break

        if not actualizado:
            return {"status": "not_found", "mensaje": "ID no encontrado"}

        escribir_calificaciones(filas)
        return {"status": "ok", "mensaje": "Calificación actualizada correctamente"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def listar_todas():
    """Lista todas las calificaciones registradas."""
    try:
        data = leer_calificaciones()
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def eliminar_por_id(id_est):
    """Elimina una calificación por ID."""
    try:
        filas = leer_calificaciones()
        nueva_lista = [row for row in filas if row.get('ID_Estudiante') != id_est]
        if len(nueva_lista) == len(filas):
            return {"status": "not_found", "mensaje": "ID no encontrado"}
        escribir_calificaciones(nueva_lista)
        return {"status": "ok", "mensaje": "Registro eliminado correctamente"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

# -------------------------------------------------------------
# Procesador de comandos
# -------------------------------------------------------------
def procesar_comando(comando):
    """Procesa el comando enviado por el cliente."""
    partes = comando.strip().split('|')
    op = partes[0]

    if op == 'AGREGAR' and len(partes) == 5:
        return agregar_calificacion(partes[1], partes[2], partes[3], partes[4])
    elif op == 'BUSCAR' and len(partes) == 2:
        return buscar_por_id(partes[1])
    elif op == 'ACTUALIZAR' and len(partes) == 3:
        return actualizar_calificacion(partes[1], partes[2])
    elif op == 'LISTAR':
        return listar_todas()
    elif op == 'ELIMINAR' and len(partes) == 2:
        return eliminar_por_id(partes[1])
    else:
        return {"status": "error", "mensaje": "Comando inválido"}

# -------------------------------------------------------------
# Manejo de clientes concurrentes
# -------------------------------------------------------------
def manejar_cliente(client_socket, addr):
    """Atiende un cliente en un hilo independiente."""
    print(f"Cliente conectado desde {addr} en hilo {threading.current_thread().name}")
    try:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            respuesta = procesar_comando(data)
            client_socket.send(json.dumps(respuesta).encode('utf-8'))
    except Exception as e:
        print(f"Error en hilo: {e}")
    finally:
        client_socket.close()
        print(f"Cliente {addr} desconectado.")

# -------------------------------------------------------------
# Servidor principal con hilos
# -------------------------------------------------------------
def iniciar_servidor():
    """Inicia el servidor concurrente."""
    inicializar_csv()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Servidor concurrente de calificaciones escuchando en puerto 12345...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(client_socket, addr))
            hilo.start()
    except KeyboardInterrupt:
        print("Servidor detenido por el usuario.")
    finally:
        server_socket.close()

# -------------------------------------------------------------
# Punto de entrada
# -------------------------------------------------------------
if __name__ == '__main__':
    iniciar_servidor()
