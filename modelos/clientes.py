from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Cliente:
    id: int
    nombre: str
    email: str
    telefono: str
    direccion: str

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