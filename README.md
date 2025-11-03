# SAT-GO — Colección de Postman (Clientes)

Esta colección contiene los endpoints para **crear tu KEY**, **obtener tokens** y **consumir los servicios de SAT-GO**.

> Si aún no te registras, hazlo en **[https://web.sat-go.com](https://web.sat-go.com)**.  
> Para soporte, escríbenos por WhatsApp al **+52 998 195 7130**.

---

## 📋 Contenido

- [Requisitos](#requisitos)
- [Importar la colección](#importar-la-colección)
  - [Opción A: desde un enlace (recomendado)](#opción-a-desde-un-enlace-recomendado)
  - [Opción B: archivo local](#opción-b-archivo-local)
- [Configurar variables](#configurar-variables)
- [Primeros pasos (flow recomendado)](#primeros-pasos-flow-recomendado)
- [Notas útiles](#notas-útiles)
- [FAQ rápida](#faq-rápida)

---

## ✅ Requisitos

- Tener instalada la aplicación **Postman** (desktop o web).
- Contar con una cuenta en **SAT-GO** y un **token temporal** obtenido desde  
  👉 [https://web.sat-go.com/consultar](https://web.sat-go.com/consultar).

---

## 🚀 Importar la colección

### Opción A: desde un enlace (recomendado)

1. Abre **Postman**.
2. Haz clic en **Import** → pestaña **Link**.
3. Pega este enlace **RAW** y presiona **Continue**:
https://raw.githubusercontent.com/hebertpena88/sat-go-cliente/main/postman/Sat-Go-Clientes.postman_collection.json
4. Confirma con **Import**.  
Verás la colección como **“Sat-Go-Clientes”**.

## ⚙️ Configurar variables

La colección usa **variables de colección** para manejar tokens dinámicamente:

| Variable       | Descripción |
|----------------|-------------|
| `tokenCliente` | Tu **token temporal** (obtenido desde [web.sat-go.com/consultar](https://web.sat-go.com/consultar)). |
| `KeyValue`     | Se **autollenará** al ejecutar el paso *Crear Llave*. |

### Cómo configurarlas

1. En Postman, abre la colección **Sat-Go-Clientes** → pestaña **Variables**.
2. En la columna **Current Value**, coloca:
- `tokenCliente` → tu token temporal.
- `KeyValue` → déjalo vacío (Postman lo llenará automáticamente).

> ⚠️ El request **“Paso 1 → Crear Llave”** utiliza `Bearer {{tokenCliente}}` y al ejecutarse guarda automáticamente el valor `KeyValue` en las variables de la colección.

---

## 🧭 Primeros pasos (flow recomendado)

1. **Coloca tu `tokenCliente`.**  
- Ve a la pestaña **Variables** de la colección y agrega tu token en `tokenCliente`.

2. **Ejecuta “Paso 1 → Crear Llave”.**  
- Endpoint: `POST https://api.sat-go.com/api/v1/Users/Createkey`
- Header: `Authorization: Bearer {{tokenCliente}}`
- Respuesta esperada: código **200 OK** con un JSON que contiene el campo `key`.
- Postman guardará automáticamente `KeyValue` con el valor devuelto.

3. **Usa la KEY generada.**  
- Los siguientes endpoints de la colección utilizan la variable `{{KeyValue}}` como tu clave de autenticación para generar tokens y acceder a los servicios SAT-GO.

---

## 💡 Notas útiles

- La colección se importa con el nombre **Sat-Go-Clientes**.
- No modifiques manualmente `KeyValue`: se actualiza automáticamente.
- Si el request **Crear Llave** falla:
- Verifica que tu `tokenCliente` esté vigente.
- Repite la copia desde el portal de SAT-GO y vuelve a ejecutar.

---

## ❓ FAQ rápida

**¿Dónde veo o edito las variables?**  
→ En la colección, pestaña **Variables**.

**¿Debo escribir `KeyValue` manualmente?**  
→ No, se llena solo al ejecutar *Crear Llave*.

**¿Cuál es el endpoint principal para crear la llave?**  
→ `POST https://api.sat-go.com/api/v1/Users/Createkey`

**¿Qué token uso en los siguientes pasos?**  
→ Usa `{{KeyValue}}` como tu clave dinámica en los demás endpoints.

---

## 🧩 Recursos

- 🌐 [Portal SAT-GO](https://web.sat-go.com)
- 📦 [Repositorio GitHub](https://github.com/hebertpena88/sat-go-cliente)
- 💬 Soporte: **+52 998 195 7130**

---

**Hecho con 💙 por el equipo de SAT-GO**
