# Auction App - API

Este es un sistema de subastas desarrollado en **FastAPI**, desplegable en **AWS** mediante **AWS CDK** y utilizando **DynamoDB** como base de datos.

## Instalación y ejecución local

### Clonar el repositorio
```bash
git clone https://github.com/anderson-riano/auction-app.git
cd auction-app
```

### Crear y activar entorno virtual (opcional pero recomendado)
```bash
python -m venv .venv
source .venv/bin/activate  # En macOS/Linux
.venv\Scripts\activate    # En Windows
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Crear archivo `.env`
Antes de ejecutar la aplicación, crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```env
AWS_REGION={AWS_REGION}
AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY}
DYNAMODB_ITEMS_TABLE=AuctionAppStack-ItemsTable
DYNAMODB_BIDS_TABLE=AuctionAppStack-BidsTable
```

### Ejecutar localmente con Uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
La API estará disponible en [http://localhost:8000](http://localhost:8000).

### Ejecutar con Docker
Asegúrate de tener Docker instalado y que el daemon esté corriendo. Luego ejecuta:
```bash
docker build -t auction-app .
docker run -p 8000:8000 auction-app
```

---
## Despliegue en AWS con CDK

### Instalar AWS CDK
Si no tienes instalado CDK, instálalo con:
```bash
npm install -g aws-cdk
```

### Configurar credenciales de AWS
Asegúrate de tener configuradas tus credenciales con:
```bash
aws configure
```

### Bootstrap CDK (solo la primera vez)
```bash
cdk bootstrap
```

### Desplegar en AWS
```bash
cdk deploy --all
```
Cuando termine el despliegue, CDK mostrará la URL pública de la API.

### Eliminar el despliegue (si es necesario)
```bash
cdk destroy --all
```

---

## Archivo Lambda

Encontramos tambien el archivo **lambda\lambda_function.py**, que es la funcion para **AWS Lambda**
Esta se ejecuta como un evento continuo cada minuto
Funciona para validar y cerrar el subasta, cuando el tiempo expira
Adicional envia un correo tanto al ganador de la subasta, como a los demas postores, que pujaron en la subasta, informacion la terminacion de la subasta

---
## Ejemplos de uso de la API

Puedes usar la colección de Postman incluida en el repositorio para probar todos los endpoints fácilmente. La colección está ubicada en el archivo:

```
postman/auction-api.postman_collection.json
```

Para usarla:
1. Abre Postman.
2. Haz clic en "Import".
3. Selecciona el archivo mencionado arriba.

---
## Ejemplos con curl

### Realizar una subasta 
### /items/

Crea la subasta donde inicializa el precio actual en 0, y segun el tiempo asignado de minutos de duracion calcula el tiempo de expiracion

```bash
curl --location 'http://localhost:8000/items/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "name": "Name item",
    "description": "Descripcion item",
    "starting_price": 800,
    "user_email": "test@test.com",
    "minutes": 30
    }'
```

### Consultar una subasta
### /items/{item_id}

Obtiene la informacion de las subasta por medio del ID

```bash
curl --location 'http://localhost:8000/items/544ce0d3-4593-4d08-8a26-c7a580635e07'
```

### Consultar subastas activas
### /items/active/

Obtiene la lista de subastas activas, que aun no han expirado

```bash
curl --location 'http://localhost:8000/items/active/'
```

### Consultar todas las subastas
### /items/

Obtiene la lista de todas las subastas

```bash
curl --location 'http://localhost:8000/items/'
```

### Realizar una oferta
### /bids/

Crea la puja teniendo en cuenta las siguientes validaciones:
1. El item debe seguir vigente y no haber expirado aun
2. El usuario que creo la subasta no puede pujar a esta misma
3. En caso de ser la primer puja del item, debe ser mayor al precio inicial
4. Si la subasta ya tiene pujas, esta debe ser mayor al precio mayor pujado actualmente
5. Actualiza el valor actual mas alto de puja para el item

```bash
curl --location 'http://localhost:8000/bids/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "item_id": "544ce0d3-4593-4d08-8a26-c7a580635e07",
        "user_email": "test1@test.com",
        "amount": 800
    }'
```

### Obtener los 5 mejores postores 
### /bids/top-bidders/
```bash
curl -X GET "http://localhost:8000/bids/top-bidders/" -H "Content-Type: application/json"
```

---
## Pruebas automáticas con Pytest

### Ejecutar pruebas

```bash
pytest tests/test_auction.py
```

### Casos cubiertos

- Crear un ítem de subasta.
- Realizar una puja válida.
- Rechazar pujas que:
  - Sean menores al precio inicial.
  - Provengan del mismo creador de la subasta.
- Consultar al ganador de una subasta (si existen pujas).


---

## Toques Adicionales
1. Validaciones para pujar a un subasta activa y con montos correctos.
2. Envio de correos automatico a ganadores y perdedores, al terminar la subasta.
3. Listar subastas unicamentes activas y listar todas las subastas, para seguimiento de esta informacion.
4. Top de los 5 postores y sus cantidades de subastas ganadas.
---