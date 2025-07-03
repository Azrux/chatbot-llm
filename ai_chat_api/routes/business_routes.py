from flask import Blueprint, jsonify

business_bp = Blueprint('business', __name__)


@business_bp.route('/calculate-discount', methods=['GET'])
def calculate_discount():
    """
    Endpoint de ejemplo para lógica de negocio.
    Devuelve un descuento simulado para un producto.
    """
    # Lógica de negocio de ejemplo
    product_price = 100
    discount_percentage = 15
    discounted_price = product_price * (1 - discount_percentage / 100)

    return jsonify({
        'product_price': product_price,
        'discount_percentage': discount_percentage,
        'discounted_price': discounted_price,
        'status': 'success'
    })
