# SAT Go Cliente - Python

Cliente web desarrollado en Python con Flask para consumir la API de SAT-Go, permitiendo consultar facturas, descargar la Opinión de Cumplimiento y la Constancia de Situación Fiscal (CSF).

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd sat-go-cliente/python-client
```

2. Crear y activar un entorno virtual (recomendado):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

La aplicación estará disponible en: http://localhost:8000

## Uso

### Datos FIEL Compartidos

La sección **Datos FIEL** en la parte superior se comparte entre todas las pestañas:

- **RFC**: El RFC del contribuyente
- **Token de Autorización**: Token Bearer de la API SAT-Go
- **Contraseña FIEL**: Contraseña de la Firma Electrónica
- **Llave Privada (.key)**: Archivo .key de la FIEL
- **Certificado (.cer)**: Archivo .cer de la FIEL

> RFC, Token y Contraseña se guardan en `localStorage` del navegador. Los archivos se conservan en memoria mientras la pestaña esté abierta.

### Funcionalidades

#### 1. Consultar Facturas

**Endpoint interno:** `POST /api/facturas/consultar`  
**Endpoint SAT-Go:** `POST /api/v2/Consultar/facfiel`

Parámetros disponibles:
- **Request ID** — para reutilizar una sesión previa
- **Fecha inicial / final** — rango de búsqueda
- **Tipo** — Recibidos / Emitidos
- **Estatus** — Todos / Vigente / Cancelada

#### 2. Opinión de Cumplimiento

**Endpoint interno:** `POST /api/oc/descargar`  
**Endpoint SAT-Go:** `POST /api/v2/Consultar/ocfiel`

Descarga el PDF de Opinión de Cumplimiento directamente en el navegador.

#### 3. Constancia de Situación Fiscal (CSF)

**Endpoint interno:** `POST /api/csf/descargar`  
**Endpoint SAT-Go:** `POST /api/v2/Consultar/csffiel`

Descarga el PDF de Constancia de Situación Fiscal directamente en el navegador.

## Estructura del Proyecto

```
python-client/
├── app.py                       # Punto de entrada de Flask
├── requirements.txt             # Dependencias Python
├── config/
│   ├── __init__.py
│   └── api.py                   # URL base y endpoints de la API
├── services/
│   ├── __init__.py
│   ├── factura_service.py       # Lógica de consulta de facturas
│   ├── oc_service.py            # Lógica de descarga de OC
│   └── csf_service.py           # Lógica de descarga de CSF
├── routes/
│   ├── __init__.py
│   ├── facturas.py              # Blueprint /api/facturas
│   ├── oc.py                    # Blueprint /api/oc
│   └── csf.py                   # Blueprint /api/csf
├── templates/
│   └── index.html               # Plantilla principal con pestañas
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js               # AJAX + persistencia localStorage
└── README.md                    # Este archivo
```

## Tecnologías Utilizadas

- Python 3 + Flask
- requests (llamadas HTTP a la API)
- Bootstrap 5 + Bootstrap Icons
- JavaScript (Fetch API)

## Solución de Problemas

### Error de SSL

El cliente deshabilita la verificación SSL en modo desarrollo. Para producción, edita `services/*.py` y cambia `verify=False` por `verify=True` o la ruta al certificado CA.

### Puerto ocupado

Cambia el puerto en `app.py`:
```python
app.run(debug=True, port=9000)
```

### Módulo no encontrado

Asegúrate de haber activado el entorno virtual antes de ejecutar:
```bash
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/macOS
pip install -r requirements.txt
```

## Licencia

MIT License
