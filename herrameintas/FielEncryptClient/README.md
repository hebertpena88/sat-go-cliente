# FielEncryptClient

Herramienta de línea de comandos para cifrar (JWE, `RSA-OAEP-256` + `A256GCM`) los archivos
de la FIEL (`.key` / `.pfx`) o la contraseña, antes de enviarlos al endpoint de SatGo.

## Requisitos

- Windows con el **.NET 10 Runtime** instalado (es un build framework-dependent, no self-contained).
  Si al ejecutar `FielEncryptClient.exe` aparece un error de "runtime no encontrado", instala el
  runtime desde https://dotnet.microsoft.com/download/dotnet/10.0.

## Archivos

```
FielEncryptClient.exe              ← ejecutable
FielEncryptClient.dll
FielEncryptClient.deps.json
FielEncryptClient.runtimeconfig.json
jose-jwt.dll                       ← dependencia (librería JWE)
fiel-enc-prod.pub.pem              ← llave pública de cifrado (producción)
```

Los 5 primeros archivos deben permanecer juntos en la misma carpeta.

## Uso

Todos los comandos se ejecutan desde una consola (cmd / PowerShell) ubicada en esta carpeta:

```powershell
.\FielEncryptClient.exe <comando> [opciones]
```

### 1) Cifrar la llave privada de la FIEL (`.key`)

```powershell
.\FielEncryptClient.exe encrypt --pem fiel-enc-prod.pub.pem --infile fiel.key --outfile llave.jwe
```

### 1b) Cifrar el archivo `.pfx` de la FIEL

```powershell
.\FielEncryptClient.exe encrypt --pem fiel-enc-prod.pub.pem --infile fiel.pfx --outfile pfx.jwe
```

### 2) Cifrar la contraseña de la FIEL

```powershell
.\FielEncryptClient.exe encrypt --pem fiel-enc-prod.pub.pem --intext "mi-password"
```

El JWE resultante se imprime en consola (o se guarda con `--outfile`).

> `fiel-enc-prod.pub.pem` (incluido en esta carpeta) es la llave pública de producción, la misma
> que devuelve el campo `publicKeyPem` de `GET /api/v1/secretprovider/fiel-encryption-key`. Si
> necesitas usar otra, guárdala en un archivo `.pem` y pásala con `--pem`, o directamente como
> texto con `--pemtext "-----BEGIN PUBLIC KEY----- ..."`.

## Notas

- El cifrado usa `RSA-OAEP-256` + `A256GCM` (JWE compacto), igual que espera el backend de SatGo.
- Ningún comando envía información por red: todo el cifrado ocurre localmente.
