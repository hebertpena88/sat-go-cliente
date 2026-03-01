# SAT Go Cliente - React

Cliente web desarrollado en React + TypeScript + Vite para consumir la API de SAT-Go, permitiendo consultar facturas, descargar la Opinión de Cumplimiento y la Constancia de Situación Fiscal (CSF).

## Requisitos

- [Node.js](https://nodejs.org/) 18.x o superior
- npm o yarn

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd sat-go-cliente/react-cliente
```

2. Instalar dependencias:
```bash
npm install
```

## Ejecución

### Modo desarrollo

```bash
npm run dev
```

La aplicación estará disponible en: http://localhost:5173

### Compilar para producción

```bash
npm run build
```

Los archivos compilados se generarán en la carpeta `dist/`.

### Vista previa de producción

```bash
npm run preview
```

## Uso

### Datos FIEL Compartidos

La aplicación cuenta con una sección de **Información FIEL** en la parte superior que se comparte entre todas las funcionalidades:

- **RFC**: El RFC del contribuyente
- **Token de Autorización**: Token de API proporcionado por SAT-Go
- **Contraseña FIEL**: Contraseña de la Firma Electrónica
- **Llave Privada (.key)**: Archivo .key de la FIEL
- **Certificado (.cer)**: Archivo .cer de la FIEL

> Los datos FIEL se mantienen en memoria y se comparten entre todas las vistas sin perderse al cambiar de sección.

### Funcionalidades

#### 1. Consultar Facturas

Permite consultar los CFDI (facturas) del SAT.

**Parámetros disponibles:**
- **Request ID**: Para consultar resultados de una solicitud previa
- **Fecha Inicial / Final**: Rango de fechas para la consulta
- **Tipo de Solicitud**: CFDI o Metadata

**Endpoint API:** `POST /api/v2/Consultar/facfiel`

#### 2. Opinión de Cumplimiento

Descarga la Opinión de Cumplimiento de Obligaciones Fiscales en formato PDF.

**Endpoint API:** `POST /api/v2/Consultar/ocfiel`

#### 3. Constancia de Situación Fiscal (CSF)

Descarga la Constancia de Situación Fiscal en formato PDF.

**Endpoint API:** `POST /api/v2/Consultar/csffiel`

## Estructura del Proyecto

```
react-cliente/
├── public/                     # Archivos estáticos
├── src/
│   ├── components/
│   │   ├── ConsultaFacturaForm.tsx    # Formulario de consulta de facturas
│   │   ├── FacturaResultados.tsx      # Visualización de resultados
│   │   ├── FielDataForm.tsx           # Componente compartido de datos FIEL
│   │   ├── OpinionCumplimientoForm.tsx # Formulario de Opinión de Cumplimiento
│   │   ├── CsfForm.tsx                # Formulario de CSF
│   │   └── UIComponents.tsx           # Componentes UI reutilizables
│   ├── config/
│   │   └── api.ts                     # Configuración de la API
│   ├── services/
│   │   ├── FacturaService.ts          # Servicio para consultar facturas
│   │   ├── OcService.ts               # Servicio para Opinión de Cumplimiento
│   │   └── CsfService.ts              # Servicio para CSF
│   ├── types/
│   │   ├── FacturaTypes.ts            # Tipos para facturas
│   │   ├── OcTypes.ts                 # Tipos para Opinión de Cumplimiento
│   │   ├── CsfTypes.ts                # Tipos para CSF
│   │   └── FielTypes.ts               # Tipos para datos FIEL compartidos
│   ├── App.tsx                        # Componente principal
│   ├── App.css                        # Estilos de la aplicación
│   ├── main.tsx                       # Punto de entrada
│   └── index.css                      # Estilos globales
├── index.html                         # HTML principal
├── vite.config.ts                     # Configuración de Vite
├── tsconfig.json                      # Configuración de TypeScript
├── package.json                       # Dependencias y scripts
└── README.md                          # Este archivo
```

## API Base URL

```
https://api.sat-go.com/api/v2
```

## Tecnologías Utilizadas

- React 18
- TypeScript
- Vite
- React Bootstrap
- Fetch API

## Scripts Disponibles

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Inicia el servidor de desarrollo |
| `npm run build` | Compila para producción |
| `npm run preview` | Vista previa de la compilación |
| `npm run lint` | Ejecuta ESLint |

## Solución de Problemas

### Error de CORS

Si recibes errores de CORS, asegúrate de que la API de SAT-Go permita solicitudes desde tu dominio de desarrollo.

### Los archivos FIEL no se envían

Verifique que:
1. Los archivos .key y .cer estén seleccionados antes de enviar
2. Los archivos sean válidos y no estén corruptos
3. La contraseña FIEL sea correcta

### Error de TypeScript

Ejecuta la verificación de tipos:
```bash
npx tsc --noEmit
```

## Licencia

MIT License

