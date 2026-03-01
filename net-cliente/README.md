# SAT Go Cliente - .NET MVC

Cliente web desarrollado en ASP.NET Core MVC para consumir la API de SAT-Go, permitiendo consultar facturas, descargar la Opinión de Cumplimiento y la Constancia de Situación Fiscal (CSF).

## Requisitos

- [.NET 9 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) o superior
- Visual Studio 2022, VS Code o cualquier editor compatible

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd sat-go-cliente/net-cliente/SatGoCliente
```

2. Restaurar dependencias:
```bash
dotnet restore
```

3. Compilar el proyecto:
```bash
dotnet build
```

## Ejecución

### Modo desarrollo

```bash
cd SatGoCliente
dotnet run
```

La aplicación estará disponible en:
- https://localhost:5001
- http://localhost:5000

### Modo watch (recarga automática)

```bash
dotnet watch run
```

## Uso

### Datos FIEL Compartidos

La aplicación cuenta con una sección de **Datos FIEL** en la parte superior que se comparte entre todas las funcionalidades:

- **RFC**: El RFC del contribuyente
- **Token de Autorización**: Token de API proporcionado por SAT-Go
- **Contraseña FIEL**: Contraseña de la Firma Electrónica
- **Llave Privada (.key)**: Archivo .key de la FIEL
- **Certificado (.cer)**: Archivo .cer de la FIEL

> ⚠️ Los campos de texto (RFC, Token, Contraseña) se guardan en localStorage del navegador para persistencia. Los archivos se mantienen en memoria mientras la página esté abierta.

### Funcionalidades

#### 1. Consultar Facturas

Permite consultar los CFDI (facturas) del SAT.

**Parámetros disponibles:**
- **Request ID**: Para consultar resultados de una solicitud previa
- **Fecha Inicial / Final**: Rango de fechas para la consulta
- **RFC Emisor / Receptor**: Filtrar por RFC específico
- **Tipo de Solicitud**: CFDI o Metadata
- **Tipo de Comprobante**: Ingreso, Egreso, Traslado, Nómina, Pago

**Endpoint API:** `POST /api/v2/Consultar/facfiel`

#### 2. Opinión de Cumplimiento

Descarga la Opinión de Cumplimiento de Obligaciones Fiscales en formato PDF.

**Endpoint API:** `POST /api/v2/Consultar/ocfiel`

#### 3. Constancia de Situación Fiscal (CSF)

Descarga la Constancia de Situación Fiscal en formato PDF.

**Endpoint API:** `POST /api/v2/Consultar/csffiel`

## Estructura del Proyecto

```
SatGoCliente/
├── Controllers/
│   ├── ConsultaSatController.cs    # Controlador principal unificado
│   ├── FacturasController.cs       # Controlador de facturas (legacy)
│   └── OpinionCumplimientoController.cs
├── Models/
│   ├── ConsultaSatViewModel.cs     # ViewModel unificado
│   ├── ConsultaFacturaViewModel.cs
│   └── OpinionCumplimientoViewModel.cs
├── Services/
│   ├── IFacturaService.cs          # Interface de facturas
│   ├── FacturaService.cs           # Servicio de facturas
│   ├── IOpinionCumplimientoService.cs
│   ├── OpinionCumplimientoService.cs
│   ├── ICsfService.cs              # Interface de CSF
│   └── CsfService.cs               # Servicio de CSF
├── Views/
│   ├── ConsultaSat/
│   │   └── Index.cshtml            # Vista principal con pestañas
│   └── Shared/
│       └── _Layout.cshtml          # Layout principal
└── Program.cs                       # Configuración de la aplicación
```

## API Base URL

```
https://api.sat-go.com/api/v2
```

## Tecnologías Utilizadas

- ASP.NET Core MVC 9.0
- Bootstrap 5
- JavaScript (Fetch API para llamadas AJAX)
- Inyección de dependencias con HttpClient

## Solución de Problemas

### El proyecto no compila

Asegúrese de tener instalado .NET 9 SDK:
```bash
dotnet --version
```

### Error de certificado SSL

En desarrollo, puede ser necesario confiar en el certificado de desarrollo:
```bash
dotnet dev-certs https --trust
```

### Los archivos FIEL no se envían

Verifique que:
1. Los archivos .key y .cer estén seleccionados antes de enviar
2. Los archivos sean válidos y no estén corruptos
3. La contraseña FIEL sea correcta

## Licencia

MIT License
