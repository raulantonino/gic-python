import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from modelos.clientes import (
    Cliente,
    ClienteRegular,
    ClientePremium,
    ClienteCorporativo,
    ValidacionError,
)


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
        # default: regular
        nuevo = ClienteRegular(
            id=nuevo_id,
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
