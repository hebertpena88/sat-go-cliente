from flask import Blueprint, request, jsonify
from services import info_fiscal_service

bp = Blueprint('info_fiscal', __name__, url_prefix='/api/info-fiscal')


@bp.post('/consultar')
def consultar():
    """Consulta Información Fiscal del SAT. Soporta FIEL y CIEC."""
    rfc           = request.form.get('rfc', '').strip()
    authorization = request.form.get('authorization', '').strip()
    metodo        = request.form.get('metodo', 'fiel').strip().lower()
    request_id    = request.form.get('request_id', '').strip()

    if not all([rfc, authorization]):
        return jsonify({'success': False, 'error': 'RFC y Token son requeridos'}), 400

    if metodo == 'ciec':
        ciec = request.form.get('ciec', '').strip()
        if not ciec:
            return jsonify({'success': False, 'error': 'La Clave CIEC es requerida'}), 400
        resultado = info_fiscal_service.consultar_info_fiscal_ciec(rfc, authorization, ciec, request_id)
    else:
        contrasena    = request.form.get('contrasena', '').strip()
        llave_privada = request.files.get('llavePrivada')
        certificado   = request.files.get('certificado')

        if not all([contrasena, llave_privada, certificado]):
            return jsonify({'success': False, 'error': 'Contraseña, llave privada y certificado son requeridos para FIEL'}), 400

        resultado = info_fiscal_service.consultar_info_fiscal_fiel(
            rfc, authorization, contrasena, llave_privada, certificado, request_id
        )

    if resultado['success']:
        return jsonify({
            'success':    True,
            'data':       resultado['data'],
            'request_id': resultado.get('request_id'),
            'message':    resultado.get('message', 'Consulta exitosa'),
        })

    return jsonify({'success': False, 'error': resultado['error']}), 400
