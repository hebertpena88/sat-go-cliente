# SAT Go Cliente - Python

Cliente web desarrollado en Python con Flask para consumir la API de SAT-Go. Soporta autenticación FIEL y CIEC, y permite consultar facturas, descargar documentos fiscales y obtener información del contribuyente.

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

### Credenciales Compartidas (FIEL / CIEC)

La sección superior se comparte entre todas las pestañas. Use el selector para elegir el método de autenticación:

**FIEL:**
- **RFC** — RFC del contribuyente
- **Token de Autorización** — Token Bearer de la API SAT-Go
- **Contraseña FIEL** — Contraseña de la Firma Electrónica
- **Llave Privada (.key)** — Archivo .key de la FIEL
- **Certificado (.cer)** — Archivo .cer de la FIEL

**CIEC:**
- **RFC** — RFC del contribuyente
- **Token de Autorización** — Token Bearer de la API SAT-Go
- **Clave CIEC** — Contraseña CIEC del portal del SAT

> RFC, Token y credenciales de texto se guardan en `localStorage`. Los archivos FIEL se conservan en memoria mientras la pestaña esté abierta.

### Módulos disponibles

#### 0. Autenticación

Genera el Token de Autorización en dos pasos:

**Paso 1 — Obtener API Key**

**Endpoint interno:** `POST /api/auth/crear-key`
**Endpoint SAT-Go:** `POST /api/v1/Users/CreateKey`

Recibe el token del portal [web.sat-go.com](https://web.sat-go.com) y devuelve una API Key permanente.

**Paso 2 — Generar Token de acceso**

**Endpoint interno:** `POST /api/auth/generar-token`
**Endpoint SAT-Go:** `POST /api/Auth/token`

Usa la API Key del paso anterior para obtener un JWT de corta duración. El botón **"Usar como Token"** lo aplica automáticamente al campo compartido.

---

#### 1. Consultar Facturas

| Método | Endpoint interno | Endpoint SAT-Go |
|--------|-----------------|-----------------|
| FIEL | `POST /api/facturas/consultar` | `POST /api/v2/Consultar/facfiel` |
| CIEC | `POST /api/facturas/consultar` | `GET /api/v2/Consultar/fac` |

Parámetros:
- **Request ID** — para reutilizar una sesión previa
- **Fecha inicial / final** — rango de búsqueda (solo FIEL)
- **Tipo** — Recibidos / Emitidos
- **Estatus** — Todos / Vigente / Cancelada

---

#### 2. Opinión de Cumplimiento

| Método | Endpoint interno | Endpoint SAT-Go |
|--------|-----------------|-----------------|
| FIEL | `POST /api/oc/descargar` | `POST /api/v2/Consultar/ocfiel` |
| CIEC | `POST /api/oc/descargar` | `GET /api/v2/Consultar/oc` |

Descarga el PDF de Opinión de Cumplimiento directamente en el navegador.

---

#### 3. Constancia de Situación Fiscal (CSF)

| Método | Endpoint interno | Endpoint SAT-Go |
|--------|-----------------|-----------------|
| FIEL | `POST /api/csf/descargar` | `POST /api/v2/Consultar/csffiel` |
| CIEC | `POST /api/csf/descargar` | `GET /api/v2/Consultar/csf` |

Descarga el PDF de Constancia de Situación Fiscal directamente en el navegador.

---

#### 4. Declaraciones

| Método | Endpoint interno | Endpoint SAT-Go |
|--------|-----------------|-----------------|
| FIEL | `POST /api/dec/descargar` | `POST /api/v2/Consultar/decfiel` |
| CIEC | `POST /api/dec/descargar` | `GET /api/v2/Consultar/dec` |

Parámetros:
- **Ejercicio** — Año fiscal (requerido)
- **Mes** — 0 = todo el año, 1–12 = mes específico
- **Tipo de Documento** — `declaracion` o `pago` (solo FIEL)
- **Request ID** — para continuar una sesión previa (opcional)

Descarga un archivo ZIP con las declaraciones.

---

#### 5. Información Fiscal

| Método | Endpoint interno | Endpoint SAT-Go |
|--------|-----------------|-----------------|
| FIEL | `POST /api/info-fiscal/consultar` | `POST /api/v2/Consultar/informacionfiscalfiel` |
| CIEC | `POST /api/info-fiscal/consultar` | `GET /api/v2/Consultar/informacionfiscal` |

Parámetros:
- **Request ID** — omitir en la primera consulta; usar el devuelto en respuestas posteriores

Devuelve JSON con la información fiscal del contribuyente.

---

## Estructura del Proyecto

```
python-client/
├── app.py                           # Punto de entrada de Flask
├── requirements.txt                 # Dependencias Python
├── config/
│   ├── __init__.py
│   └── api.py                       # URL base y endpoints de la API
├── services/
│   ├── __init__.py
│   ├── auth_service.py              # Lógica de autenticación (CreateKey + token)
│   ├── factura_service.py           # Consulta de facturas (FIEL y CIEC)
│   ├── oc_service.py                # Descarga de OC (FIEL y CIEC)
│   ├── csf_service.py               # Descarga de CSF (FIEL y CIEC)
│   ├── dec_service.py               # Descarga de declaraciones (FIEL y CIEC)
│   └── info_fiscal_service.py       # Consulta de información fiscal (FIEL y CIEC)
├── routes/
│   ├── __init__.py
│   ├── auth.py                      # Blueprint /api/auth
│   ├── facturas.py                  # Blueprint /api/facturas
│   ├── oc.py                        # Blueprint /api/oc
│   ├── csf.py                       # Blueprint /api/csf
│   ├── dec.py                       # Blueprint /api/dec
│   └── info_fiscal.py               # Blueprint /api/info-fiscal
├── templates/
│   └── index.html                   # Plantilla principal con pestañas
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js                   # AJAX + persistencia localStorage
└── README.md                        # Este archivo
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
