# Laboratorio 2 - Sistemas Distribuidos
## Universidad de las Fuerzas Armadas ESPE
### Grupo 1 - Sistemas Distribuidos

#### Integrantes:
- *Pamela Chipe*  
- *Jhordy Marcillo*
- *Camilo Orrico*  
- *Kleber Chávez*

## Introducción

Este proyecto se desarrolla en el contexto de aplicaciones distribuidas, implementando un sistema cliente-servidor que demuestra conceptos fundamentales de sistemas distribuidos. El proyecto aborda conceptos clave como **concurrencia**, **comunicación inter-servidores**, y **persistencia de datos**, aplicando principios del **teorema CAP** (Consistencia, Disponibilidad, Partición de red) en un entorno distribuido real.

El sistema implementa un modelo de **microservicios** donde diferentes servidores se especializan en funciones específicas, permitiendo la escalabilidad y mantenibilidad del sistema distribuido.

## Objetivos

### Objetivos Generales
- Implementar un sistema distribuido de gestión de calificaciones académicas
- Demostrar comunicación cliente-servidor utilizando sockets TCP/IP
- Aplicar conceptos de concurrencia y paralelismo en sistemas distribuidos
- Implementar persistencia de datos en sistemas distribuidos

### Objetivos Específicos
- Desarrollar un servidor de calificaciones con operaciones CRUD completas
- Implementar un servidor de validación NRC para verificación de materias
- Crear clientes que interactúen con los servidores mediante protocolo estructurado
- Comparar implementaciones secuenciales vs concurrentes
- Implementar comunicación inter-servidores para validación de datos
- Utilizar almacenamiento persistente en formato CSV
- Manejar concurrencia mediante threading en Python

## Metodología

### Tecnologías y Herramientas Utilizadas
- **Lenguaje**: Python 3.x
- **Comunicación**: Sockets TCP/IP
- **Concurrencia**: Threading
- **Persistencia**: Archivos CSV
- **Protocolo**: JSON para intercambio de datos
- **Arquitectura**: Microservicios distribuidos

### Diseño Modular
El sistema está diseñado con una arquitectura modular que separa responsabilidades:

1. **Servidor de Calificaciones**: Maneja operaciones CRUD sobre calificaciones
2. **Servidor NRC**: Valida códigos de materias (NRC)
3. **Clientes**: Interfaz de usuario para interactuar con el sistema
4. **Capa de Persistencia**: Almacenamiento en archivos CSV

### Manejo de Fallos
- Validación de entrada de datos
- Manejo de excepciones en comunicación de red
- Respuestas de error estructuradas
- Validación inter-servidores antes de operaciones críticas
- Recuperación automática de archivos de datos

## Descripción del Proyecto

Este proyecto implementa un **sistema distribuido de gestión de calificaciones** que permite la comunicación entre múltiples servidores y clientes utilizando sockets TCP. El sistema está diseñado para demostrar conceptos de sistemas distribuidos, incluyendo comunicación inter-servidores, concurrencia con hilos, y manejo de datos persistentes.

## Arquitectura del Sistema

El sistema está compuesto por:

1. **Servidor de Calificaciones** (Puerto 12345/12346)
2. **Servidor de NRC** (Puerto 12346) 
3. **Clientes** (Interfaz de usuario)
4. **Almacenamiento persistente** (Archivos CSV)

### Diagrama de Arquitectura

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente 1     │    │   Cliente 2     │    │   Cliente N     │
│   (Puerto 12345)│    │   (Puerto 12345)│    │   (Puerto 12345)│
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                     ┌────────────▼────────────┐
                     │  Servidor Calificaciones │
                     │     (Puerto 12345)       │
                     │   - Manejo de hilos       │
                     │   - CRUD calificaciones   │
                     └────────────┬────────────┘
                                  │
                     ┌────────────▼────────────┐
                     │    Servidor NRC         │
                     │    (Puerto 12346)       │
                     │   - Validación NRC      │
                     │   - Consulta materias   │
                     └─────────────────────────┘
```
graph TD
    subgraph Cliente (Navegador Web)
        A[Frontend Web (React/JS)]
    end

    subgraph Servidor (Backend - server.py)
        B[API REST (Flask)]
        C[Gestor WebSocket (Socket.IO)]
    end

    subgraph Almacenamiento
        D[Base de Datos (MongoDB)]
        E[Almacenamiento de Archivos (Cloudinary)]
    end

    %% --- Flujos de Comunicacion ---
    
    %% Flujo 1: API (ej. crear sala, ver salas)
    A -- Peticiones HTTP (ej. /rooms) --> B
    B -- Escribe/Lee --> D[users, rooms]
    B -- Respuestas JSON --> A

    %% Flujo 2: Tiempo Real (ej. enviar mensaje)
    A -- Conexión WS (ej. @socketio.on('send_message')) --> C
    C -- Escribe Mensaje --> D[messages]
    C -- Emite Evento ('message') --> A

    %% Flujo 3: Subida de Archivos
    A -- Sube archivo (POST /upload) --> E
    E -- Retorna URL --> A
    A -- Envía URL por WS (ej. 'send_message') --> C

## Estructura del Proyecto

```
Laboratorio2_Distribuidas_G1/
├── con_hilos/                    # Implementación con concurrencia
│   ├── server.py                 # Servidor con hilos (Puerto 12345)
│   └── client.py                 # Cliente para servidor con hilos
├── sin_hilos/                    # Implementación secuencial
│   ├── server.py                 # Servidor secuencial (Puerto 12346)
│   └── client.py                 # Cliente para servidor secuencial
├── serverNRC.py                  # Servidor de validación NRC (Puerto 12346)
├── calificaciones.csv            # Base de datos de calificaciones
├── nrcs.csv                      # Base de datos de NRCs válidos
└── README.md                     # Documentación del proyecto
```

## Funcionalidades Implementadas

### Operaciones CRUD de Calificaciones
- **AGREGAR**: Añadir nueva calificación (con validación NRC)
- **BUSCAR**: Buscar calificación por ID de estudiante
- **ACTUALIZAR**: Modificar calificación existente
- **LISTAR**: Mostrar todas las calificaciones
- **ELIMINAR**: Eliminar calificación por ID

### Comunicación Inter-Servidores
- **Validación NRC**: El servidor de calificaciones consulta al servidor NRC
- **Protocolo de comunicación**: Comandos estructurados con separador `|`
- **Respuestas JSON**: Formato estandarizado para todas las respuestas

### Concurrencia
- **Servidor con hilos**: Manejo concurrente de múltiples clientes
- **Servidor secuencial**: Procesamiento uno a la vez (para comparación)
- **Threading**: Cada cliente se maneja en un hilo independiente

## Instalación y Configuración

### Requisitos Previos
- Python 3.6 o superior
- Sistema operativo Windows/Linux/Mac

### Configuración de Puertos
```python
# Servidor con hilos (con_hilos/)
PUERTO_CALIFICACIONES = 12345

# Servidor secuencial (sin_hilos/)  
PUERTO_CALIFICACIONES = 12346

# Servidor NRC
PUERTO_NRC = 12346
```

## Instrucciones de Ejecución

### 1. Ejecutar Servidor NRC (Requerido primero)
```bash
# Terminal 1
python serverNRC.py
```

### 2. Ejecutar Servidor de Calificaciones

#### Opción A: Servidor con Hilos (Concurrente)
```bash
# Terminal 2
cd con_hilos
python server.py
```

#### Opción B: Servidor Secuencial
```bash
# Terminal 2  
cd sin_hilos
python server.py
```

### 3. Ejecutar Cliente
```bash
# Terminal 3
cd con_hilos  # o sin_hilos según el servidor elegido
python client.py
```

## Formato de Datos

### Estructura de Calificaciones (calificaciones.csv)
```csv
ID_Estudiante,Nombre,Materia,Calificacion
12345,Juan Pérez,PRO102,18.5
67890,María García,MAT101,16.0
```

### Estructura de NRCs (nrcs.csv)
```csv
NRC,Materia
MAT101,Matemáticas
PRO102,Programación
BD103,Bases de Datos
```

## Protocolo de Comunicación

### Comandos del Cliente al Servidor
```
AGREGAR|ID|Nombre|NRC|Calificacion
BUSCAR|ID
ACTUALIZAR|ID|NuevaCalificacion
LISTAR
ELIMINAR|ID
```

### Respuestas del Servidor
```json
{
  "status": "ok|error|not_found",
  "mensaje": "Descripción del resultado",
  "data": { /* Datos adicionales si aplica */ }
}
```

## Ejemplos de Uso

### Ejemplo 1: Agregar Calificación con NRC Válido
```
Comando: AGREGAR|12345|Juan Pérez|PRO102|18.5
Respuesta: {"status": "ok", "mensaje": "Calificación agregada para Juan Pérez"}
```

### Ejemplo 2: Buscar Calificación
```
Comando: BUSCAR|12345
Respuesta: {"status": "ok", "data": {"ID_Estudiante": "12345", "Nombre": "Juan Pérez", "Materia": "PRO102", "Calificacion": "18.5"}}
```

### Ejemplo 3: NRC Inválido
```
Comando: AGREGAR|12345|Juan Pérez|INVALID|18.5
Respuesta: {"status": "error", "mensaje": "Materia/NRC no válida o servidor NRC no disponible"}
```

## Diferencias entre Implementaciones

| Característica | Con Hilos | Sin Hilos |
|----------------|-----------|-----------|
| **Concurrencia** | Múltiples clientes simultáneos | Un cliente a la vez |
| **Puerto** | 12345 | 12346 |
| **Rendimiento** | Alto (paralelo) | Bajo (secuencial) |
| **Complejidad** | Mayor | Menor |
| **Uso de recursos** | Mayor | Menor |

## Pruebas de Concurrencia

### Cómo Probar Concurrencia

1. **Ejecutar servidor con hilos**:
   ```bash
   cd con_hilos
   python server.py
   ```

2. **Abrir múltiples terminales** y ejecutar clientes simultáneamente:
   ```bash
   # Terminal 1
   cd con_hilos
   python client.py
   
   # Terminal 2
   cd con_hilos
   python client.py
   
   # Terminal 3
   cd con_hilos
   python client.py
   ```

3. **Realizar operaciones simultáneas** en diferentes clientes para observar el manejo concurrente.

### Limitaciones del Sistema

- **Puerto único**: Solo un servidor puede usar el mismo puerto simultáneamente
- **Dependencia NRC**: El servidor de calificaciones requiere que el servidor NRC esté activo
- **Almacenamiento local**: Los datos se almacenan en archivos CSV locales
- **Sin autenticación**: No hay sistema de autenticación implementado
- **Sin transacciones**: No hay manejo de transacciones ACID

## Solución de Problemas

### Error: Puerto en uso
```
OSError: [WinError 10048] Solo se permite un uso de cada dirección de socket
```
**Solución**: Cambiar el puerto en el código o cerrar el proceso que lo usa.

### Error: Servidor NRC no disponible
```
{"status": "error", "mensaje": "Materia/NRC no válida o servidor NRC no disponible"}
```
**Solución**: Asegurarse de que el servidor NRC esté ejecutándose en el puerto 12346.

## Resultados

### Evidencia de Pruebas

#### Logs de Ejecución Secuencial
```
Servidor secuencial escuchando en puerto 12346...
Cliente conectado desde ('127.0.0.1', 54321)
Cliente desconectado.
```

#### Logs de Ejecución Concurrente
```
Servidor concurrente de calificaciones escuchando en puerto 12345...
Cliente conectado desde ('127.0.0.1', 54321) en hilo Thread-1
Cliente conectado desde ('127.0.0.1', 54322) en hilo Thread-2
Cliente ('127.0.0.1', 54321) desconectado.
Cliente ('127.0.0.1', 54322) desconectado.
```

#### Contenido de CSV post-pruebas
```csv
ID_Estudiante,Nombre,Materia,Calificacion
12345,Juan Pérez,PRO102,18.5
67890,María García,MAT101,16.0
11111,Ana López,BD103,17.2
```

## Características Técnicas

### Manejo de Errores
- Validación de entrada de datos
- Manejo de excepciones en sockets
- Respuestas de error estructuradas

### Persistencia de Datos
- Almacenamiento en archivos CSV
- Inicialización automática de archivos
- Lectura/escritura atómica

### Seguridad
- Validación de NRC antes de agregar calificaciones
- Sanitización de datos de entrada
- Manejo seguro de archivos

## Conclusiones

### Desafíos Enfrentados

1. **Comunicación Inter-Servidores**: La implementación de validación entre servidores requirió el diseño de un protocolo de comunicación robusto y manejo de fallos de conectividad.

2. **Concurrencia**: El manejo de múltiples clientes simultáneos presentó desafíos en la sincronización y el manejo de recursos compartidos.

3. **Persistencia de Datos**: La implementación de operaciones CRUD con persistencia en archivos CSV requirió manejo cuidadoso de la integridad de datos.

### Lecciones Aprendidas

- **Importancia de la validación**: La validación inter-servidores mejora significativamente la integridad de los datos.
- **Beneficios de la concurrencia**: El uso de hilos permite atender múltiples clientes simultáneamente, mejorando la experiencia del usuario.
- **Diseño modular**: La separación de responsabilidades facilita el mantenimiento y la escalabilidad del sistema.

### Sugerencias de Mejoras

1. **Implementar autenticación**: Agregar sistema de usuarios y contraseñas.
2. **Base de datos**: Migrar de CSV a una base de datos relacional (SQLite/PostgreSQL).
3. **Logging**: Implementar sistema de logs para auditoría y debugging.
4. **Transacciones**: Implementar manejo de transacciones ACID.
5. **API REST**: Crear una API REST para facilitar la integración con otros sistemas.
6. **Docker**: Containerizar la aplicación para facilitar el despliegue.

## Referencias

- [Documentación de Sockets en Python](https://docs.python.org/3/library/socket.html)
- [Threading en Python](https://docs.python.org/3/library/threading.html)
- [CSV en Python](https://docs.python.org/3/library/csv.html)
- [Teorema CAP en Sistemas Distribuidos](https://en.wikipedia.org/wiki/CAP_theorem)
