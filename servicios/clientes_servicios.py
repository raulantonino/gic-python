import json
from pathlib import Path
from typing import List, Dict, Any

from modelos.clientes import Cliente


DB_PATH = Path("base_datos") / "clientes.json"


def cargar_clientes() -> List[Cliente]:
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        DB_PATH.write_text("[]", encoding="utf-8")

    contenido = DB_PATH.read_text(encoding="utf-8").strip()
    if not contenido:
        contenido = "[]"

    data: List[Dict[str, Any]] = json.loads(contenido)
    return [Cliente.from_dict(item) for item in data]


def guardar_clientes(clientes: List[Cliente]) -> None:
    data = [c.to_dict() for c in clientes]
    DB_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _siguiente_id(clientes: List[Cliente]) -> int:
    if not clientes:
        return 1
    return max(c.id for c in clientes) + 1


def crear_cliente(nombre: str, email: str, telefono: str, direccion: str) -> Cliente:
    clientes = cargar_clientes()
    nuevo = Cliente(
        id=_siguiente_id(clientes),
        nombre=nombre.strip(),
        email=email.strip(),
        telefono=telefono.strip(),
        direccion=direccion.strip(),
    )
    clientes.append(nuevo)
    guardar_clientes(clientes)
    return nuevo


def listar_clientes() -> List[Cliente]:
    return cargar_clientes()