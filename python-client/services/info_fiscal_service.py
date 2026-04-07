import logging
import requests
from config.api import BASE_URL, ENDPOINTS, TIMEOUT

logger = logging.getLogger(__name__)


def consultar_info_fiscal_fiel(rfc: str, authorization: str, contrasena: str,
                               llave_privada, certificado,
                               request_id: str = '') -> dict:
    """Consulta Información Fiscal del SAT usando FIEL (POST multipart)."""
    url = BASE_URL + ENDPOINTS['CONSULTAR_INFOFISCALFIEL']
    if request_id:
        url += f'?requestId={request_id}'

    try:
        files = {
            'llavePrivada': (llave_privada.filename, llave_privada.stream, 'application/octet-stream'),
            'Certificado':  (certificado.filename,   certificado.stream,   'application/octet-stream'),
        }
        data = {'Contrasena': contrasena}
        headers = {
            'RFC':           rfc,
            'Authorization': f'Bearer {authorization}',
            'Accept':        'application/json',
        }
        logger.info('>> INFO FISCAL FIEL REQUEST | URL=%s | headers=%s | files=%s',
                    url,
                    {k: (v[:20] + '...' if k == 'Authorization' else v) for k, v in headers.items()},
                    {'llavePrivada': llave_privada.filename, 'Certificado': certificado.filename})

        response = requests.post(url, headers=headers, data=data, files=files, timeout=TIMEOUT, verify=False)
        logger.info('<< INFO FISCAL FIEL RESPONSE | status=%s | content-type=%s | headers=%s',
                    response.status_code, response.headers.get('Content-Type'), dict(response.headers))

        if response.ok:
            try:
                json_data = response.json()
            except Exception:
                json_data = response.text
            req_id = response.headers.get('RequestId') or (json_data.get('requestId') if isinstance(json_data, dict) else None)
            logger.debug('<< INFO FISCAL FIEL BODY | request_id=%s | data=%s', req_id, str(json_data)[:500])
            return {'success': True, 'data': json_data, 'request_id': req_id, 'message': 'Información Fiscal obtenida exitosamente'}

        error_text = response.text
        logger.error('<< INFO FISCAL FIEL ERROR | status=%s | body=%s', response.status_code, error_text[:500])
        return {'success': False, 'error': error_text or f'Error {response.status_code}'}

    except Exception as exc:
        logger.exception('Excepción inesperada al consultar Información Fiscal FIEL')
        return {'success': False, 'error': str(exc)}


def consultar_info_fiscal_ciec(rfc: str, authorization: str, ciec: str,
                               request_id: str = '') -> dict:
    """Consulta Información Fiscal del SAT usando CIEC (GET)."""
    url = BASE_URL + ENDPOINTS['CONSULTAR_INFOFISCAL']
    params = {}
    if request_id:
        params['requestId'] = request_id

    try:
        headers = {
            'RFC':           rfc,
            'Authorization': f'Bearer {authorization}',
            'Secret':        ciec,
            'Accept':        'application/json',
        }
        logger.info('>> INFO FISCAL CIEC REQUEST | URL=%s | params=%s | headers=%s',
                    url, params,
                    {k: (v[:20] + '...' if k == 'Authorization' else ('***' if k == 'Secret' else v)) for k, v in headers.items()})

        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT, verify=False)
        logger.info('<< INFO FISCAL CIEC RESPONSE | status=%s | content-type=%s | headers=%s',
                    response.status_code, response.headers.get('Content-Type'), dict(response.headers))

        if response.ok:
            try:
                json_data = response.json()
            except Exception:
                json_data = response.text
            req_id = response.headers.get('RequestId') or (json_data.get('requestId') if isinstance(json_data, dict) else None)
            logger.debug('<< INFO FISCAL CIEC BODY | request_id=%s | data=%s', req_id, str(json_data)[:500])
            return {'success': True, 'data': json_data, 'request_id': req_id, 'message': 'Información Fiscal obtenida exitosamente'}

        error_text = response.text
        logger.error('<< INFO FISCAL CIEC ERROR | status=%s | body=%s', response.status_code, error_text[:500])
        return {'success': False, 'error': error_text or f'Error {response.status_code}'}

    except Exception as exc:
        logger.exception('Excepción inesperada al consultar Información Fiscal CIEC')
        return {'success': False, 'error': str(exc)}
