""" Database routes for car stock filtering."""

import os
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import pandas as pd
from ai_chat_api.models.stock_filter import StockDataFilter
from ai_chat_api.models.stock_model import StockData

db_bp = Blueprint('db', __name__)

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), '..', '..', 'sample_caso_ai_engineer.csv')

BOOL_COLUMNS = ['bluetooth', 'car_play']


@db_bp.route('/cars', methods=['GET'])
def get_cars():
    """
    Returns a list of cars filtering by params
    """

    filters = request.args.to_dict()
    print(f"Received filters: {filters}")

    try:
        print("Creating StockDataFilter model with filters:", filters)
        stock_filter = StockDataFilter(**filters)  # type: ignore
        print("StockDataFilter created successfully:", stock_filter)
    except ValidationError as e:
        print("Validation error occurred:", e)
        return jsonify({
            'error': 'Invalid filter parameters',
            'details': e.errors()
        }), 400

    # Check if the CSV file exists
    if not os.path.exists(CSV_PATH):
        return jsonify({'error': f'Cannot find CSV path in: {CSV_PATH}'}), 404

    # Read CSV file
    df = pd.read_csv(CSV_PATH)
    print(f"CSV file loaded successfully with {len(df)} records.")

    # Convert columns to appropriate types
    for bool_col in BOOL_COLUMNS:
        if bool_col in df.columns:
            df[bool_col] = df[bool_col].apply(
                lambda x: str(x).strip().lower(
                ) == "sí" if pd.notnull(x) else False
            )

    # Apply filters dynamically, using alias for DataFrame columns
    for field, value in stock_filter.model_dump(exclude_none=True).items():
        if value is None:
            continue

        print(f"Processing filter: {field} with value: {value}")

        # Get the alias (column name in CSV)
        field_info = getattr(StockDataFilter, "model_fields").get(field)
        alias = getattr(field_info, "alias", field) if field_info else field

        print(f"Using alias: {alias} for field: {field}")

        if alias not in df.columns:
            print(
                f"Alias '{alias}' not found in DataFrame columns: {df.columns.tolist()}")
            continue  # Skip this filter instead of returning error

        # Handle boolean fields specifically
        if field in BOOL_COLUMNS:
            if value is True:
                df = df[df[alias] == True]
            elif value is False:
                df = df[(df[alias] == False) | (df[alias].isnull())]
        # Handle numeric fields with type conversion
        elif isinstance(value, (int, float)):
            try:
                numeric_col = pd.to_numeric(df[alias], errors='coerce')
                df = df[numeric_col == float(value)]
            except Exception:
                df = df[df[alias] == value]
        else:
            df = df[df[alias] == value]

        print(f"After filtering by {field}: {len(df)} records remaining")

    # Handle missing boolean values in the output
    for bool_col in BOOL_COLUMNS:
        if bool_col in df.columns:
            df[bool_col] = df[bool_col].fillna(False)

    # Convert DataFrame to list of dictionaries
    cars_list = []
    for row in df.to_dict(orient='records'):
        # Convert keys to string for consistency
        row_str_keys = {str(k): v for k, v in row.items()}

        # Convert boolean fields from string to boolean
        for bool_field in BOOL_COLUMNS:
            if bool_field in row_str_keys and isinstance(row_str_keys[bool_field], str):
                row_str_keys[bool_field] = row_str_keys[bool_field].strip(
                ).lower() == "sí"

        try:
            car = StockData(**row_str_keys)
            cars_list.append(car.model_dump(by_alias=False))
        except Exception as e:
            print(f"Error parsing row: {row_str_keys} - {e}")

    if not cars_list:
        return jsonify({'message': 'No cars found matching the filters'}), 200

    return jsonify({
        'cars': cars_list,
        'count': len(cars_list),
        'status': 'success'
    }), 200
