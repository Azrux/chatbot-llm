""" Business logic routes for car financing calculations. """

from flask import Blueprint, jsonify, request

business_bp = Blueprint('business', __name__)


def calculate_monthly_payment(principal, annual_rate, years):
    """
    Calculate monthly payment using the standard loan payment formula
    """
    monthly_rate = annual_rate / 12
    num_payments = years * 12

    if monthly_rate == 0:  # Handle 0% interest case
        return principal / num_payments

    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
        ((1 + monthly_rate) ** num_payments - 1)

    return monthly_payment


@business_bp.route('/calculate-financiation', methods=['GET'])
def calculate_financiation():
    """
    Endpoint to calculate financing details for a car purchase.
    """
    price = request.args.get('price', type=float)
    years = request.args.get('years', type=int)

    if price is None:
        return jsonify({'error': 'Price parameter is required'}), 400

    # Financing parameters
    down_payment_percentage = 0.20  # 20%
    annual_interest_rate = 0.10     # 10%

    down_payment_amount = price * down_payment_percentage
    financed_amount = price - down_payment_amount

    financing_options = []

    # TODO: Refactor this part to avoid code duplication
    if years is not None:
        # If years is provided, calculate for that specific term
        num_payments = years * 12
        monthly_payment = calculate_monthly_payment(
            financed_amount,
            annual_interest_rate,
            years
        )

        total_paid = down_payment_amount + (monthly_payment * num_payments)

        financing_options.append({
            'down_payment': f"{int(down_payment_percentage * 100)}%",
            'down_payment_amount': round(down_payment_amount, 2),
            'financed_amount': round(financed_amount, 2),
            'financing_term': f'{years} years',
            'interest_rate': f"{int(annual_interest_rate * 100)}%",
            'monthly_payment': round(monthly_payment, 2),
            'price': price,
            'final_price': round(total_paid, 2)
        })

        return jsonify(financing_options)

    for term in range(3, 7):  # Terms from 3 to 6 years
        num_payments = term * 12  # Define num_payments here

        monthly_payment = calculate_monthly_payment(
            financed_amount,
            annual_interest_rate,
            term
        )

        total_paid = down_payment_amount + (monthly_payment * num_payments)

        financing_options.append({
            'down_payment': f"{int(down_payment_percentage * 100)}%",
            'down_payment_amount': round(down_payment_amount, 2),
            'financed_amount': round(financed_amount, 2),
            'financing_term': f'{term} years',
            'interest_rate': f"{int(annual_interest_rate * 100)}%",
            'monthly_payment': round(monthly_payment, 2),
            'price': price,
            'final_price': round(total_paid, 2)
        })

    return jsonify(financing_options)
