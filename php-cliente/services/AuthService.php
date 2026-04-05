<?php

require_once __DIR__ . '/../config/api.php';

/**
 * Servicio de autenticación para SAT-GO
 *
 * Flujo:
 *  1. createKey($tokenPortal)  → POST /api/v1/Users/CreateKey → devuelve API Key permanente
 *  2. generarToken($key)        → POST /api/Auth/token?key=... → devuelve access_token (JWT)
 */
class AuthService
{
    /**
     * Ejecuta una petición cURL con body vacío (solo headers).
     * Usar CURLOPT_CUSTOMREQUEST evita que cURL agregue automáticamente
     * Content-Type: application/x-www-form-urlencoded y Content-Length: 0.
     */
    private static function curlPost(string $url, array $headers): array
    {
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL            => $url,
            CURLOPT_CUSTOMREQUEST  => 'POST',
            CURLOPT_HTTPHEADER     => $headers,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => ApiConfig::TIMEOUT,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_SSL_VERIFYHOST => false
        ]);

        $response   = curl_exec($ch);
        $http_code  = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);

        return [$response, $http_code, $curl_error];
    }

    /**
     * Intenta extraer un valor de string de la respuesta de la API.
     * Maneja: string plano, JSON string, JSON objeto (plano o anidado como tokens.access.value).
     *
     * @param  string   $raw      Respuesta cruda de la API
     * @param  string[] $fields   Nombre de campos planos a buscar en un objeto JSON
     * @return string|null
     */
    private static function extractStringValue(string $raw, array $fields): ?string
    {
        $raw = trim($raw);

        $data = json_decode($raw, true);

        if (json_last_error() === JSON_ERROR_NONE) {
            // JSON string válido: ej. "eyJ..."
            if (is_string($data)) {
                return $data;
            }

            if (is_array($data)) {
                // Estructura SAT-GO: tokens.access.value
                if (!empty($data['tokens']['access']['value'])) {
                    return $data['tokens']['access']['value'];
                }

                // Campos planos conocidos
                foreach ($fields as $field) {
                    if (!empty($data[$field]) && is_string($data[$field])) {
                        return $data[$field];
                    }
                }
            }

            return null;
        }

        // No es JSON → asumir texto plano (ej. UUID o JWT sin comillas)
        return $raw ?: null;
    }

    // -------------------------------------------------------------------------

    /**
     * Crea o recupera la API Key permanente usando el token obtenido desde el portal web.
     *
     * @param  string $tokenPortal  Token del portal (web.sat-go.com), campo tokens.access.value
     * @return array  ['success', 'key' | 'error', 'message', 'raw_response']
     */
    public static function createKey(string $tokenPortal): array
    {
        try {
            $url = ApiConfig::BASE_URL_V1 . ApiConfig::AUTH_ENDPOINTS['CREATE_KEY'];

            [$response, $http_code, $curl_error] = self::curlPost($url, [
                'Authorization: Bearer ' . $tokenPortal,
                'Accept: application/json, text/plain, */*',
                'User-Agent: PHP-SAT-Client/1.0',
                'Cache-Control: no-cache'
            ]);

            if ($curl_error) {
                return ['success' => false, 'error' => 'Error de conexión: ' . $curl_error, 'message' => 'No se pudo conectar con la API'];
            }

            if ($http_code >= 200 && $http_code < 300) {
                $key = self::extractStringValue($response, ['key', 'Key', 'apiKey', 'ApiKey', 'data', 'result', 'value']);
                return [
                    'success'      => true,
                    'key'          => $key ?? $response,
                    'message'      => 'API Key obtenida correctamente',
                    'raw_response' => $response
                ];
            }

            $data = json_decode($response, true);
            return [
                'success'      => false,
                'error'        => $data['message'] ?? $data['title'] ?? $data['detail'] ?? ('Error HTTP ' . $http_code),
                'message'      => 'Error al crear la API Key',
                'raw_response' => $response,
                'http_code'    => $http_code
            ];

        } catch (Exception $e) {
            return ['success' => false, 'error' => $e->getMessage(), 'message' => 'Error inesperado al crear la API Key'];
        }
    }

    /**
     * Genera un token JWT de corta duración a partir de la API Key permanente.
     *
     * @param  string $key  API Key obtenida con createKey()
     * @return array  ['success', 'access_token' | 'error', 'message', 'raw_response']
     */
    public static function generarToken(string $key): array
    {
        try {
            $url = ApiConfig::BASE_URL_V1 . ApiConfig::AUTH_ENDPOINTS['AUTH_TOKEN']
                 . '?' . http_build_query(['key' => $key]);

            [$response, $http_code, $curl_error] = self::curlPost($url, [
                'Accept: application/json, text/plain, */*',
                'User-Agent: PHP-SAT-Client/1.0',
                'Cache-Control: no-cache'
            ]);

            if ($curl_error) {
                return ['success' => false, 'error' => 'Error de conexión: ' . $curl_error, 'message' => 'No se pudo conectar con la API'];
            }

            if ($http_code >= 200 && $http_code < 300) {
                $token = self::extractStringValue($response, ['access_token', 'accessToken', 'token', 'Token', 'jwt', 'value', 'data', 'result']);
                return [
                    'success'      => true,
                    'access_token' => $token ?? $response,
                    'message'      => 'Token generado correctamente',
                    'raw_response' => $response
                ];
            }

            $data = json_decode($response, true);
            return [
                'success'      => false,
                'error'        => $data['message'] ?? $data['title'] ?? $data['detail'] ?? ('Error HTTP ' . $http_code),
                'message'      => 'Error al generar el token',
                'raw_response' => $response,
                'http_code'    => $http_code
            ];

        } catch (Exception $e) {
            return ['success' => false, 'error' => $e->getMessage(), 'message' => 'Error inesperado al generar el token'];
        }
    }
}
