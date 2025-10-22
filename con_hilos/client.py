import socket
import json
import threading

def mostrar_menu():
    print("\n--- Menú de Calificaciones ---")
    print("1. Agregar calificación")
    print("2. Buscar por ID")
    print("3. Actualizar calificación")
    print("4. Listar todas")
    print("5. Eliminar por ID")
    print("6. Salir")
    return input("Elija opción: ")

def enviar_comando(comando):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.send(comando.encode('utf-8'))
        respuesta = client_socket.recv(4096).decode('utf-8')
        client_socket.close()
        return json.loads(respuesta)
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def ejecutar_cliente():
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            id_est = input("ID: ")
            nombre = input("Nombre: ")
            materia = input("Materia (NRC): ")
            calif = input("Calificación: ")
            res = enviar_comando(f"AGREGAR|{id_est}|{nombre}|{materia}|{calif}")
            print(res.get("mensaje", res))
        elif opcion == "2":
            id_est = input("ID: ")
            res = enviar_comando(f"BUSCAR|{id_est}")
            print(res)
        elif opcion == "3":
            id_est = input("ID: ")
            nueva = input("Nueva calificación: ")
            res = enviar_comando(f"ACTUALIZAR|{id_est}|{nueva}")
            print(res.get("mensaje", res))
        elif opcion == "4":
            res = enviar_comando("LISTAR")
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif opcion == "5":
            id_est = input("ID: ")
            res = enviar_comando(f"ELIMINAR|{id_est}")
            print(res.get("mensaje", res))
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    ejecutar_cliente()
