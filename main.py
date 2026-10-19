from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services import service, ClienteCreate, VentaCreate

app = FastAPI(title="Comercializadora EcoVida S.A.S. - POS API", version="1.0.0")

# Configuración de CORS para permitir consumo desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del sistema POS de Comercializadora EcoVida S.A.S."}

@app.get("/clientes")
def get_clientes():
    return service.obtener_clientes()

@app.post("/clientes")
def create_cliente(cliente: ClienteCreate):
    resultado = service.registrar_cliente(cliente)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@app.put("/clientes/{cedula}")
def update_cliente(cedula: str, cliente: ClienteCreate):
    resultado = service.actualizar_cliente(cedula, cliente)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@app.delete("/clientes/{cedula}")
def delete_cliente(cedula: str):
    resultado = service.eliminar_cliente(cedula)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado

@app.get("/productos")
def get_productos():
    return service.obtener_productos()

@app.post("/ventas")
def create_venta(venta: VentaCreate):
    resultado = service.procesar_venta(venta)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@app.get("/ventas")
def get_ventas():
    return service.obtener_ventas()