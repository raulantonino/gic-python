from dataclasses import dataclass
from typing import Dict, Any
import re


class ValidacionError(Exception):
    """Error lanzado cuando un dato del cliente no cumple una validación."""
    pass


@dataclass
class Cliente:
    id: int
    nombre: str
    email: str
    telefono: str
    direccion: str

    @staticmethod
    def validar_email(email: str) -> None:
        email = email.strip()
        patron = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(patron, email):
            raise ValidacionError("Email inválido. Ej: nombre@dominio.com")

    @staticmethod
    def validar_telefono(telefono: str) -> None:
        telefono = telefono.strip()
        # Regla simple: solo dígitos y mínimo 8
        if (not telefono.isdigit()) or len(telefono) < 8:
            raise ValidacionError("Teléfono inválido. Debe tener solo números y mínimo 8 dígitos.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tipo": "regular",  # por ahora todos serán "regular"
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Cliente":
        return Cliente(
            id=int(data["id"]),
            nombre=str(data["nombre"]),
            email=str(data["email"]),
            telefono=str(data["telefono"]),
            direccion=str(data["direccion"]),
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} | {self.email} | {self.telefono} | {self.direccion}"