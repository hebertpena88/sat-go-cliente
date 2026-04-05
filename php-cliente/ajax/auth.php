<?php

header('Content-Type: application/json');

require_once __DIR__ . '/../services/AuthService.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Método no permitido', 'message' => 'Solo se permiten peticiones POST']);
    exit;
}

try {
    $action = $_POST['action'] ?? '';

    if ($action === 'createKey') {
        $tokenPortal = trim($_POST['token_portal'] ?? '');
        if (empty($tokenPortal)) {
            throw new Exception('El token del portal es requerido');
        }
        echo json_encode(AuthService::createKey($tokenPortal));

    } elseif ($action === 'generarToken') {
        $key = trim($_POST['api_key'] ?? '');
        if (empty($key)) {
            throw new Exception('La API Key es requerida');
        }
        echo json_encode(AuthService::generarToken($key));

    } else {
        throw new Exception('Acción no válida. Use "createKey" o "generarToken"');
    }

} catch (Exception $e) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => $e->getMessage(), 'message' => 'Error de validación']);
}
