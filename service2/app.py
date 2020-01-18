from datetime import timedelta, datetime
import psycopg2
from flask import Flask, jsonify, request, make_response, abort
import os

# Configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
LISTEN_PORT = os.getenv('LISTEN_PORT', 5001)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/actions/gendata', methods=['POST'])
def generate_data():
    try:
        content = request.get_json()

        func = content['func']
        dt = int(content['dt'])
        interval = int(content['interval'])

        conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                host=POSTGRES_HOST, port=POSTGRES_PORT)

        str_positions = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=interval)
        position = start_date
        while position < end_date:
            str_positions.append('(' + str(round(position.timestamp())) + ')')
            position = position + timedelta(hours=dt)

        if func in ('sin(t)', 't + 2/t'):
            query = (
                "SELECT t, ({}) AS result"
                " FROM (VALUES {}) AS tab (t);"
            ).format(func, ', '.join(str_positions))
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return jsonify({
                'service': 'service2',
                'status': 'success',
                'result': rows,
            })
        else:
            raise Exception(f'Unknown function "{func}"')
    except Exception as e:
        return make_response(jsonify({
            'service': 'service2',
            'status': 'error',
            'message': str(e),
        }), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=LISTEN_PORT)
