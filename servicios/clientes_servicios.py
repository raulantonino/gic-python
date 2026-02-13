import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from modelos.clientes import (
    Cliente,
    ClienteRegular,
    ClientePremium,
    ClienteCorporativo,
    ValidacionError,
)

DB_PATH = Path("base_datos") / "clientes.json"
LOG_PATH = Path("logs") / "actividad.log"


def _log(accion: str, detalle: str) -> None:
    """Registra actividades del sistema en logs/actividad.log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{timestamp} | {accion.upper()} | {detalle}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(linea)


def _asegurar_db() -> None:
    """Asegura que exista el archivo JSON de clientes."""
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        DB_PATH.write_text("[]", encoding="utf-8")


def cargar_clientes() -> List[Cliente]:
    _asegurar_db()

    contenido = DB_PATH.read_text(encoding="utf-8").strip()
    if not contenido:
        contenido = "[]"

    data: List[Dict[str, Any]] = json.loads(contenido)
    return [Cliente.from_dict(item) for item in data]


def guardar_clientes(clientes: List[Cliente]) -> None:
    _asegurar_db()
    data = [c.to_dict() for c in clientes]
    DB_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _siguiente_id(clientes: List[Cliente]) -> int:
    if not clientes:
        return 1
    return max(c.id for c in clientes) + 1


def _buscar_indice_por_id(clientes: List[Cliente], cliente_id: int) -> int:
    for i, c in enumerate(clientes):
        if c.id == cliente_id:
            return i
    return -1


def obtener_cliente_por_id(cliente_id: int) -> Cliente:
    clientes = cargar_clientes()
    idx = _buscar_indice_por_id(clientes, cliente_id)
    if idx == -1:
        raise ValidacionError(f"No existe cliente con id={cliente_id}.")
    return clientes[idx]


def crear_cliente(
    tipo: str,
    nombre: str,
    email: str,
    telefono: str,
    direccion: str,
    descuento: Optional[float] = None,
    razon_social: Optional[str] = None,
    rut_empresa: Optional[str] = None,
) -> Cliente:
    clientes = cargar_clientes()

    # Validaciones comunes
    Cliente.validar_texto_no_vacio(nombre, "Nombre")
    Cliente.validar_texto_no_vacio(direccion, "Dirección")
    Cliente.validar_email(email)
    Cliente.validar_telefono(telefono)

    tipo = tipo.strip().lower()
    nuevo_id = _siguiente_id(clientes)

    if tipo == "premium":
        if descuento is None:
            raise ValidacionError("Falta descuento para ClientePremium.")
        Cliente.validar_descuento(float(descuento))
        nuevo = ClientePremium(
            id=nuevo_id,
            nombre=nombre.strip(),
            email=email.strip(),
            telefono=telefono.strip(),
            direccion=direccion.strip(),
            descuento=float(descuento),
        )

    elif tipo == "corporativo":
        razon_social = "" if razon_social is None else razon_social
        rut_empresa = "" if rut_empresa is None else rut_empresa
        Cliente.validar_texto_no_vacio(razon_social, "Razón social")
        Cliente.validar_texto_no_vacio(rut_empresa, "RUT empresa")

        nuevo = ClienteCorporativo(
            id=nuevo_id,
            nombre=nombre.strip(),
            email=email.strip(),
            telefono=telefono.strip(),
            direccion=direccion.strip(),
            razon_social=razon_social.strip(),
            rut_empresa=rut_empresa.strip(),
        )

    else:
        nuevo = ClienteRegular(
            id=nuevo_id,
            nombre=nombre.strip(),
            email=email.strip(),
            telefono=telefono.strip(),
            direccion=direccion.strip(),
        )

    clientes.append(nuevo)
    guardar_clientes(clientes)

    _log("CREAR", f"id={nuevo.id} tipo={nuevo.tipo()} nombre={nuevo.nombre}")
    return nuevo


def listar_clientes() -> List[Cliente]:
    return cargar_clientes()


def editar_cliente(
    cliente_id: int,
    nombre: Optional[str] = None,
    email: Optional[str] = None,
    telefono: Optional[str] = None,
    direccion: Optional[str] = None,
    descuento: Optional[float] = None,
    razon_social: Optional[str] = None,
    rut_empresa: Optional[str] = None,
) -> Cliente:
    clientes = cargar_clientes()
    idx = _buscar_indice_por_id(clientes, cliente_id)
    if idx == -1:
        raise ValidacionError(f"No existe cliente con id={cliente_id}.")

    actual = clientes[idx]

    # Asignaciones condicionales (solo si vienen)
    if nombre is not None:
        Cliente.validar_texto_no_vacio(nombre, "Nombre")
        actual.nombre = nombre.strip()

    if direccion is not None:
        Cliente.validar_texto_no_vacio(direccion, "Dirección")
        actual.direccion = direccion.strip()

    if email is not None:
        Cliente.validar_email(email)
        actual.email = email.strip()

    if telefono is not None:
        Cliente.validar_telefono(telefono)
        actual.telefono = telefono.strip()

    # Campos extra según tipo
    if isinstance(actual, ClientePremium) and descuento is not None:
        Cliente.validar_descuento(float(descuento))
        actual.descuento = float(descuento)

    if isinstance(actual, ClienteCorporativo):
        if razon_social is not None:
            Cliente.validar_texto_no_vacio(razon_social, "Razón social")
            actual.razon_social = razon_social.strip()
        if rut_empresa is not None:
            Cliente.validar_texto_no_vacio(rut_empresa, "RUT empresa")
            actual.rut_empresa = rut_empresa.strip()

    guardar_clientes(clientes)
    _log("EDITAR", f"id={actual.id} tipo={actual.tipo()} nombre={actual.nombre}")
    return actual


def eliminar_cliente(cliente_id: int) -> Cliente:
    clientes = cargar_clientes()
    idx = _buscar_indice_por_id(clientes, cliente_id)
    if idx == -1:
        raise ValidacionError(f"No existe cliente con id={cliente_id}.")

    eliminado = clientes.pop(idx)
    guardar_clientes(clientes)
    _log("ELIMINAR", f"id={eliminado.id} tipo={eliminado.tipo()} nombre={eliminado.nombre}")
    return eliminado


def resetear_datos(confirmacion: str) -> None:
    """
    Reinicia la base de datos de clientes (clientes.json -> []).
    Se pide confirmación explícita para evitar borrados accidentales.
    """
    if confirmacion.strip().upper() != "RESET":
        raise ValidacionError("Confirmación inválida. Escribe RESET para confirmar.")

    _asegurar_db()
    DB_PATH.write_text("[]", encoding="utf-8")
    _log("RESET", "base_datos/clientes.json reiniciado a lista vacía")
