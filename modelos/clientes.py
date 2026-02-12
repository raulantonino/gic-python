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

    # ---------- Validaciones ----------
    @staticmethod
    def validar_email(email: str) -> None:
        email = email.strip()
        patron = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(patron, email):
            raise ValidacionError("Email inválido. Ej: nombre@dominio.com")

    @staticmethod
    def validar_telefono(telefono: str) -> None:
        telefono = telefono.strip()
        if (not telefono.isdigit()) or len(telefono) < 8:
            raise ValidacionError("Teléfono inválido. Debe tener solo números y mínimo 8 dígitos.")

    @staticmethod
    def validar_descuento(descuento: float) -> None:
        if descuento < 0 or descuento > 1:
            raise ValidacionError("Descuento inválido. Debe estar entre 0 y 1 (ej: 0.10).")

    @staticmethod
    def validar_texto_no_vacio(valor: str, nombre_campo: str) -> None:
        if not valor or not valor.strip():
            raise ValidacionError(f"{nombre_campo} no puede estar vacío.")

    # ---------- Polimorfismo ----------
    def beneficio(self) -> float:
        """Método polimórfico: cada tipo de cliente puede devolver un beneficio distinto."""
        return 0.0

    def tipo(self) -> str:
        """Tipo del cliente para persistencia y reconstrucción."""
        return "regular"

    # ---------- Persistencia ----------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tipo": self.tipo(),
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Cliente":
        """
        Fábrica: crea la instancia correcta según data['tipo'].
        Si no existe 'tipo' (datos viejos), asume 'regular'.
        """
        tipo = str(data.get("tipo", "regular")).lower()

        base_kwargs = dict(
            id=int(data["id"]),
            nombre=str(data["nombre"]),
            email=str(data["email"]),
            telefono=str(data["telefono"]),
            direccion=str(data["direccion"]),
        )

        if tipo == "premium":
            descuento = float(data.get("descuento", 0.0))
            return ClientePremium(**base_kwargs, descuento=descuento)

        if tipo == "corporativo":
            razon_social = str(data.get("razon_social", "")).strip()
            rut_empresa = str(data.get("rut_empresa", "")).strip()
            return ClienteCorporativo(**base_kwargs, razon_social=razon_social, rut_empresa=rut_empresa)

        # default: regular
        return ClienteRegular(**base_kwargs)

    def __str__(self) -> str:
        return (
            f"[{self.id}] ({self.tipo()}) {self.nombre} | {self.email} | "
            f"{self.telefono} | {self.direccion} | beneficio={self.beneficio():.2f}"
        )


@dataclass
class ClienteRegular(Cliente):
    def beneficio(self) -> float:
        return 0.0

    def tipo(self) -> str:
        return "regular"


@dataclass
class ClientePremium(Cliente):
    descuento: float = 0.0

    def beneficio(self) -> float:
        # Beneficio = descuento (por ejemplo 0.10)
        return float(self.descuento)

    def tipo(self) -> str:
        return "premium"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["descuento"] = float(self.descuento)
        return data


@dataclass
class ClienteCorporativo(Cliente):
    razon_social: str = ""
    rut_empresa: str = ""

    def beneficio(self) -> float:
        # Por ahora lo dejamos en 0.0 para no inventar reglas
        return 0.0

    def tipo(self) -> str:
        return "corporativo"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["razon_social"] = self.razon_social
        data["rut_empresa"] = self.rut_empresa
        return data
