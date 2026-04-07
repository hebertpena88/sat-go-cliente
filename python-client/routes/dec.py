import base64
from flask import Blueprint, request, jsonify
from services import dec_service

bp = Blueprint('dec', __name__, url_prefix='/api/dec')


@bp.post('/descargar')
def descargar():
    """Descarga Declaraciones del SAT. Soporta FIEL y CIEC."""
    rfc           = request.form.get('rfc', '').strip()
    authorization = request.form.get('authorization', '').strip()
    metodo        = request.form.get('metodo', 'fiel').strip().lower()
    ejercicio     = request.form.get('ejercicio', '').strip()
    mes           = int(request.form.get('mes', 0))
    request_id    = request.form.get('request_id', '').strip()

    if not all([rfc, authorization, ejercicio]):
        return jsonify({'success': False, 'error': 'RFC, Token y Ejercicio son requeridos'}), 400

    if metodo == 'ciec':
        ciec = request.form.get('ciec', '').strip()
        if not ciec:
            return jsonify({'success': False, 'error': 'La Clave CIEC es requerida'}), 400
        resultado = dec_service.descargar_dec_ciec(rfc, authorization, ciec, ejercicio, mes, request_id)
    else:
        contrasena     = request.form.get('contrasena', '').strip()
        llave_privada  = request.files.get('llavePrivada')
        certificado    = request.files.get('certificado')
        tipo_documento = request.form.get('tipo_documento', 'declaracion').strip()

        if not all([contrasena, llave_privada, certificado]):
            return jsonify({'success': False, 'error': 'Contraseña, llave privada y certificado son requeridos para FIEL'}), 400

        resultado = dec_service.descargar_dec_fiel(
            rfc, authorization, contrasena, llave_privada, certificado,
            ejercicio, mes, tipo_documento, request_id
        )

    if resultado['success']:
        return jsonify({
            'success':      True,
            'file_base64':  base64.b64encode(resultado['file_bytes']).decode(),
            'file_name':    resultado['file_name'],
            'content_type': resultado['content_type'],
        })

    return jsonify({'success': False, 'error': resultado['error']}), 400
