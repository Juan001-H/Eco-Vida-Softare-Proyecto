from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re

class ClienteCreate(BaseModel):
    cedula: str = Field(..., min_length=5, max_length=15)
    nombre: str
    tipo: str = Field(default="Particular") # Acepta "Particular", "Convenio", "EPS"

    @field_validator('cedula')
    @classmethod
    def validar_cedula(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("La cédula debe contener solo números")
        return v

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v_limpio = v.strip()
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", v_limpio):
            raise ValueError("El nombre solo debe contener letras y espacios")
        return v_limpio

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        tipos_validos = ["Particular", "Convenio", "EPS"]
        if v not in tipos_validos:
            raise ValueError("El tipo de afiliación debe ser Particular, Convenio o EPS")
        return v

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_limpio = v.strip()
            if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", v_limpio):
                raise ValueError("El nombre solo debe contener letras y espacios")
            return v_limpio
        return v

class ItemVenta(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)

class VentaRequest(BaseModel):
    cedula_cliente: str
    items: List[ItemVenta]
    