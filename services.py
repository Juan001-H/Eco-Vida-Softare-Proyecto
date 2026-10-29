from typing import List
from pydantic import BaseModel
import re
from datetime import datetime # <- Importación añadida

# ==========================================
# MODELOS PYDANTIC PARA VALIDACIÓN
# ==========================================
class ClienteCreate(BaseModel):
    cedula: str
    nombre: str
    tipo: str  # 'Particular', 'Convenio', 'EPS'

class ItemVenta(BaseModel):
    producto_id: int
    cantidad: int

class VentaCreate(BaseModel):
    cedula_cliente: str
    items: List[ItemVenta]


# ==========================================
# SERVICIO DE LÓGICA DE NEGOCIO
# ==========================================
class EcoVidaService:
    def __init__(self):
        # Base de datos en memoria (Stateful)
        self.clientes = [
            {"cedula": "1094000123", "id_interno": "CLI-1001", "nombre": "Ana María Gómez", "tipo": "EPS"},
            {"cedula": "1094000456", "id_interno": "CLI-1002", "nombre": "Carlos Alberto Ruiz", "tipo": "Convenio"}
        ]
        
        # Catálogo unificado con stock base de 50 unidades e imágenes estables
        self.productos = [
            {"id": 1, "nombre": "Kit de Cepillos de Bambú (x4)", "precio": 24900.0, "stock": 50, "categoria": "Hogar Sostenible", "imagen": "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=500&auto=format&fit=crop&q=80"},
            {"id": 2, "nombre": "Botella Térmica Acero Inoxidable", "precio": 65000.0, "stock": 50, "categoria": "Movilidad Eco", "imagen": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=80"},
            {"id": 3, "nombre": "Jabón Sólido Artesanal Orgánico", "precio": 12500.0, "stock": 50, "categoria": "Cuidado Personal", "imagen": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?w=500&auto=format&fit=crop&q=80"},
            {"id": 4, "nombre": "Bolsas Reutilizables de Tela (x3)", "precio": 18000.0, "stock": 50, "categoria": "Zero Waste", "imagen": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=500&auto=format&fit=crop&q=80"},
            {"id": 5, "nombre": "Esponja Natural de Lufa (x2)", "precio": 9500.0, "stock": 50, "categoria": "Hogar Sostenible", "imagen": "https://plus.unsplash.com/premium_photo-1661320820224-4e26b71099ff?fm=jpg&q=60&w=3000&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D=80"},
            {"id": 6, "nombre": "Pitillos de Acero Inoxidable (x4)", "precio": 15000.0, "stock": 50, "categoria": "Zero Waste", "imagen": "https://ambientegourmet.vtexassets.com/arquivos/ids/190727/12405.jpg?v=639117850613000000=80"}
        ]
        
        self.ventas = []
        self.contador_clientes = 1003
        self.contador_facturas = 5001

    def obtener_clientes(self) -> List[dict]:
        return self.clientes

    def registrar_cliente(self, cliente_data: ClienteCreate) -> dict:
        if not cliente_data.cedula.isdigit():
            return {"error": "La cédula solo debe contener números."}
        
        if not re.match(f"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]+$", cliente_data.nombre):
            return {"error": "El nombre solo debe contener letras."}

        for c in self.clientes:
            if c["cedula"] == cliente_data.cedula:
                return {"error": "Ya existe un cliente registrado con esta cédula."}
        
        nuevo_id = f"CLI-{self.contador_clientes}"
        self.contador_clientes += 1

        nombre_formateado = cliente_data.nombre.strip().title()

        nuevo_cliente = {
            "cedula": cliente_data.cedula,
            "id_interno": nuevo_id,
            "nombre": nombre_formateado,
            "tipo": cliente_data.tipo
        }
        self.clientes.append(nuevo_cliente)
        return {"message": "Cliente registrado exitosamente", "id_interno": nuevo_id, "cliente": nuevo_cliente}

    def actualizar_cliente(self, cedula: str, cliente_data: ClienteCreate) -> dict:
        if not cliente_data.cedula.isdigit():
            return {"error": "La cédula solo debe contener números."}
        if not re.match(f"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]+$", cliente_data.nombre):
            return {"error": "El nombre solo debe contener letras."}

        for c in self.clientes:
            if c["cedula"] == cedula:
                c["nombre"] = cliente_data.nombre.strip().title()
                c["tipo"] = cliente_data.tipo
                c["cedula"] = cliente_data.cedula
                return {"mensaje": "Cliente actualizado correctamente", "cliente": c}
        return {"error": "Cliente no encontrado."}

    def eliminar_cliente(self, cedula: str) -> dict:
        for i, c in enumerate(self.clientes):
            if c["cedula"] == cedula:
                eliminado = self.clientes.pop(i)
                return {"mensaje": "Cliente eliminado correctamente", "cliente": eliminado}
        return {"error": "Cliente no encontrado."}

    def obtener_productos(self) -> List[dict]:
        return self.productos

    def procesar_venta(self, venta_data: VentaCreate) -> dict:
        cliente = next((c for c in self.clientes if c["cedula"] == venta_data.cedula_cliente), None)
        if not cliente:
            return {"error": "Cliente no encontrado en el sistema."}

        subtotal_global = 0
        detalle_items = []

        for item in venta_data.items:
            producto = next((p for p in self.productos if p["id"] == item.producto_id), None)
            if not producto:
                return {"error": f"Producto con ID {item.producto_id} no encontrado."}
            
            if producto["stock"] < item.cantidad:
                return {"error": f"Stock insuficiente para {producto['nombre']}. Disponible: {producto['stock']}"}
            
            subtotal_item = producto["precio"] * item.cantidad
            subtotal_global += subtotal_item
            detalle_items.append({
                "nombre": producto["nombre"],
                "cantidad": item.cantidad,
                "precio": producto["precio"],
                "subtotal": subtotal_item
            })

        porcentaje_descuento = 0.0
        tipo_convenio_str = "Particular (Sin Descuento)"
        if cliente["tipo"] == "Convenio":
            porcentaje_descuento = 0.10
            tipo_convenio_str = "Convenio Institucional (10%)"
        elif cliente["tipo"] == "EPS":
            porcentaje_descuento = 0.15
            tipo_convenio_str = "Afiliado EPS (15%)"

        descuento_valor = subtotal_global * porcentaje_descuento
        total_pagar = subtotal_global - descuento_valor

        for item in venta_data.items:
            producto = next((p for p in self.productos if p["id"] == item.producto_id), None)
            if producto:
                producto["stock"] -= item.cantidad

        num_factura = f"FACT-{self.contador_facturas}"
        self.contador_facturas += 1

        nueva_venta = {
            "numeroFactura": num_factura,
            "fechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # <- LÍNEA REFACTORIZADA
            "cliente_cedula": cliente["cedula"],
            "cliente_nombre": cliente["nombre"],
            "tipo_convenio": tipo_convenio_str,
            "subtotal": subtotal_global,
            "descuento": descuento_valor,
            "total": total_pagar,
            "items": detalle_items
        }
        
        self.ventas.insert(0, nueva_venta)
        return {
            "message": "Venta procesada con éxito", 
            "numeroFactura": num_factura, 
            "total": total_pagar,
            "venta": nueva_venta # <- Agregado para evitar errores en el frontend
        }

    def obtener_ventas(self) -> List[dict]:
        return self.ventas

service = EcoVidaService()
