import logging
import requests
from urllib.parse import urlencode
from config.api import BASE_URL, ENDPOINTS, TIMEOUT

logger = logging.getLogger(__name__)


def descargar_dec_fiel(rfc: str, authorization: str, contrasena: str,
                       llave_privada, certificado,
                       ejercicio: str, mes: int = 0,
                       tipo_documento: str = 'declaracion',
                       request_id: str = '') -> dict:
    """Descarga declaraciones del SAT usando FIEL (POST multipart)."""
    params = {'ejercicio': ejercicio, 'mes': mes, 'tipoDocumento': tipo_documento}
    if request_id:
        params['requestId'] = request_id

    url = BASE_URL + ENDPOINTS['CONSULTAR_DECFIEL'] + '?' + urlencode(params)

    try:
        files = {
            'llavePrivada': (llave_privada.filename, llave_privada.stream, 'application/octet-stream'),
            'Certificado':  (certificado.filename,   certificado.stream,   'application/octet-stream'),
        }
        data = {'Contrasena': contrasena}
        headers = {
            'RFC':           rfc,
            'Authorization': f'Bearer {authorization}',
            'Accept':        '*/*',
        }
        logger.info('>> DEC FIEL REQUEST | URL=%s | headers=%s | files=%s',
                    url,
                    {k: (v[:20] + '...' if k == 'Authorization' else v) for k, v in headers.items()},
                    {'llavePrivada': llave_privada.filename, 'Certificado': certificado.filename})

        response = requests.post(url, headers=headers, data=data, files=files, timeout=TIMEOUT, verify=False)
        logger.info('<< DEC FIEL RESPONSE | status=%s | content-type=%s | headers=%s',
                    response.status_code, response.headers.get('Content-Type'), dict(response.headers))

        if response.ok:
            content_type = response.headers.get('Content-Type', 'application/zip')
            file_name = _extract_filename(response, 'declaracion.zip')
            logger.debug('<< DEC FIEL FILE | file=%s | size=%d bytes', file_name, len(response.content))
            return {'success': True, 'file_bytes': response.content, 'file_name': file_name, 'content_type': content_type}

        if response.status_code == 403:
            try:
                json_data = response.json()
                if 'featureCode' in json_data or 'dailyLimit' in json_data:
                    logger.error('<< DEC FIEL LIMITE | %s', json_data)
                    return {
                        'success':       False,
                        'error_type':    'limit_exceeded',
                        'error':         json_data.get('message', 'Límite excedido'),
                        'daily_limit':   json_data.get('dailyLimit'),
                        'monthly_limit': json_data.get('monthlyLimit'),
                    }
            except Exception:
                pass

        error_text = response.text
        logger.error('<< DEC FIEL ERROR | status=%s | body=%s', response.status_code, error_text[:500])
        return {'success': False, 'error': error_text or f'Error {response.status_code}'}

    except Exception as exc:
        logger.exception('Excepción inesperada al descargar Declaración FIEL')
        return {'success': False, 'error': str(exc)}


def descargar_dec_ciec(rfc: str, authorization: str, ciec: str,
                       ejercicio: str, mes: int = 0,
                       request_id: str = '') -> dict:
    """Descarga declaraciones del SAT usando CIEC (GET)."""
    params = {'ejercicio': ejercicio, 'mes': mes}
    if request_id:
        params['requestId'] = request_id

    url = BASE_URL + ENDPOINTS['CONSULTAR_DEC']

    try:
        headers = {
            'RFC':           rfc,
            'Authorization': f'Bearer {authorization}',
            'Secret':        ciec,
            'Accept':        '*/*',
        }
        logger.info('>> DEC CIEC REQUEST | URL=%s | params=%s | headers=%s',
                    url, params,
                    {k: (v[:20] + '...' if k == 'Authorization' else ('***' if k == 'Secret' else v)) for k, v in headers.items()})

        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT, verify=False)
        logger.info('<< DEC CIEC RESPONSE | status=%s | content-type=%s | headers=%s',
                    response.status_code, response.headers.get('Content-Type'), dict(response.headers))

        if response.ok:
            content_type = response.headers.get('Content-Type', 'application/zip')
            file_name = _extract_filename(response, 'declaracion.zip')
            logger.debug('<< DEC CIEC FILE | file=%s | size=%d bytes', file_name, len(response.content))
            return {'success': True, 'file_bytes': response.content, 'file_name': file_name, 'content_type': content_type}

        if response.status_code == 403:
            try:
                json_data = response.json()
                if 'featureCode' in json_data or 'dailyLimit' in json_data:
                    logger.error('<< DEC CIEC LIMITE | %s', json_data)
                    return {
                        'success':       False,
                        'error_type':    'limit_exceeded',
                        'error':         json_data.get('message', 'Límite excedido'),
                        'daily_limit':   json_data.get('dailyLimit'),
                        'monthly_limit': json_data.get('monthlyLimit'),
                    }
            except Exception:
                pass

        error_text = response.text
        logger.error('<< DEC CIEC ERROR | status=%s | body=%s', response.status_code, error_text[:500])
        return {'success': False, 'error': error_text or f'Error {response.status_code}'}

    except Exception as exc:
        logger.exception('Excepción inesperada al descargar Declaración CIEC')
        return {'success': False, 'error': str(exc)}


def _extract_filename(response: requests.Response, default: str) -> str:
    """Extrae el nombre de archivo del header Content-Disposition."""
    cd = response.headers.get('Content-Disposition', '')
    for part in cd.split(';'):
        part = part.strip()
        if part.startswith('filename='):
            return part[len('filename='):].strip('"')
    return default
