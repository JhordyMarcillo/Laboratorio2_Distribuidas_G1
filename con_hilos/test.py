import socket
import json
import random
import time
import threading
from locust import User, task, between

HOST = "localhost"
PORT = 12345

# Pool compartido de IDs agregados para usarlos en BUSCAR/ACTUALIZAR/ELIMINAR
_id_pool = set()
_id_lock = threading.Lock()

# Conjunto de NRC válidos esperados por serverNRC (asegúrate de tener ese server activo)
NRC_VALIDOS = ["MAT101", "PRO102", "BD103"]


def _tcp_request(command: str, timeout: float = 3.0) -> bytes:
    """Envía un comando al servidor TCP y devuelve la respuesta completa en bytes.
    Conecta, envía, lee hasta que el servidor cierre la conexión, y retorna los bytes.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((HOST, PORT))
        s.send(command.encode("utf-8"))
        chunks = []
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                chunks.append(data)
            except socket.timeout:
                break
        return b"".join(chunks)
    finally:
        try:
            s.close()
        except Exception:
            pass


def _fire_metric(env, name: str, start_time: float, response: bytes = b"", exc: Exception | None = None):
    """Registra una métrica de request personalizada en Locust."""
    total_ms = (time.perf_counter() - start_time) * 1000.0
    if exc is None:
        env.events.request.fire(
            request_type="TCP",
            name=name,
            response_time=total_ms,
            response_length=len(response),
            response=bytes(response),
        )
    else:
        env.events.request.fire(
            request_type="TCP",
            name=name,
            response_time=total_ms,
            response_length=0,
            exception=exc,
        )


class CalificacionesUser(User):
    wait_time = between(0.2, 0.8)

    def _enviar_comando(self, name: str, command: str):
        start = time.perf_counter()
        try:
            raw = _tcp_request(command)
            _fire_metric(self.environment, name, start, raw, None)
            if not raw:
                raise RuntimeError("Respuesta vacía")
            data = json.loads(raw.decode("utf-8"))
            return data
        except Exception as e:
            _fire_metric(self.environment, name, start, b"", e)
            # También relanzamos para que se vea en logs de consola
            raise

    # Pesos orientativos: más lecturas que escrituras
    @task(5)
    def buscar(self):
        # Elegir un ID conocido si hay; si no, un ID aleatorio que probablemente no exista
        with _id_lock:
            id_elegido = random.choice(list(_id_pool)) if _id_pool else str(random.randint(1, 9999))
        cmd = f"BUSCAR|{id_elegido}"
        self._enviar_comando("BUSCAR", cmd)

    @task(3)
    def listar(self):
        self._enviar_comando("LISTAR", "LISTAR")

    @task(3)
    def agregar(self):
        # Generar datos válidos (NRC debe existir en serverNRC)
        id_est = str(random.randint(100000, 999999))
        nombre = random.choice(["Ana", "Luis", "María", "Carlos", "Elena"]) + f"_{random.randint(1,999)}"
        materia = random.choice(NRC_VALIDOS)
        calif = str(random.randint(0, 20))
        cmd = f"AGREGAR|{id_est}|{nombre}|{materia}|{calif}"
        res = self._enviar_comando("AGREGAR", cmd)
        if isinstance(res, dict) and res.get("status") == "ok":
            with _id_lock:
                _id_pool.add(id_est)

    @task(2)
    def actualizar(self):
        with _id_lock:
            if not _id_pool:
                return  # Nada que actualizar aún
            id_est = random.choice(list(_id_pool))
        nueva = str(random.randint(0, 20))
        cmd = f"ACTUALIZAR|{id_est}|{nueva}"
        self._enviar_comando("ACTUALIZAR", cmd)

    @task(1)
    def eliminar(self):
        with _id_lock:
            if not _id_pool:
                return
            id_est = random.choice(list(_id_pool))
        cmd = f"ELIMINAR|{id_est}"
        res = self._enviar_comando("ELIMINAR", cmd)
        if isinstance(res, dict) and res.get("status") == "ok":
            with _id_lock:
                _id_pool.discard(id_est)
