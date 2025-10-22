import socket
import json

def mostrar_menu():
	print('\n--- Men\u00fa de Calificaciones ---')
	print('1. Agregar calificaci\u00f3n')
	print('2. Buscar por ID')
	print('3. Actualizar calificaci\u00f3n')
	print('4. Listar todas')
	print('5. Eliminar por ID')
	print('6. Salir')
	# devolver entero para comparación
	try:
		return int(input('Elija opci\u00f3n: '))
	except ValueError:
		return -1


def enviar_comando(comando):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(('localhost', 12346))
	# usar sendall y terminar con salto de linea para delimitar mensajes si el servidor lo espera
	client_socket.sendall(comando.encode('utf-8'))
	respuesta = client_socket.recv(4096).decode('utf-8')
	client_socket.close()
	try:
		return json.loads(respuesta)
	except json.JSONDecodeError:
		return {'status': 'error', 'mensaje': 'Respuesta no JSON: ' + respuesta}


while True:
	opcion = mostrar_menu()
	if opcion == 1:
		id_est = input('ID: ')
		nombre = input('Nombre: ')
		materia = input('Materia: ')
		calif = input('Calificaci\u00f3n: ')
		res = enviar_comando(f'AGREGAR|{id_est}|{nombre}|{materia}|{calif}')
		print(res.get('mensaje', res))
	elif opcion == 2:
		id_est = input('ID: ')
		res = enviar_comando(f'BUSCAR|{id_est}')
		if isinstance(res, dict) and res.get('status') == 'ok':
			data = res.get('data', {})
			print(f"Nombre: {data.get('Nombre')}, Materia: {data.get('Materia')}, Calif: {data.get('Calif')}")
		else:
			print(res.get('mensaje', res))
	elif opcion == 3:
		id_est = input('ID: ')
		nueva_calif = input('Nueva calificaci\u00f3n: ')
		res = enviar_comando(f'ACTUALIZAR|{id_est}|{nueva_calif}')
		print(res.get('mensaje', res))
	elif opcion == 4:
		res = enviar_comando('LISTAR')
		if isinstance(res, dict) and res.get('status') == 'ok':
			for row in res.get('data', []):
				print(row)
		else:
			print(res.get('mensaje', res))
	elif opcion == 5:
		id_est = input('ID: ')
		res = enviar_comando(f'ELIMINAR|{id_est}')
		print(res.get('mensaje', res))
	elif opcion == 6:
		break
	else:
		print('Opci\u00f3n inv\u00e1lida')