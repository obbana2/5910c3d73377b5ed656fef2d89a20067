import io
import os
import requests
from flask import Flask, jsonify, request, send_file, make_response, abort


# Configuration
LISTEN_PORT = os.getenv('LISTEN_PORT', 5002)


app = Flask(__name__)


@app.route('/api/actions/genchart', methods=['POST'])
def generate_chart():
    error = None
    try:
        content = request.get_json()

        data = {
            'infile': {
                'title': {
                    'text': 'Result Chart'
                },
                'xAxis': {
                    'type': 'datetime',
                    'showFirstLabel': True,
                    'showLastLabel': True,
                },
                'series': [
                    {
                        'data': content['data'],
                        'dataGrouping': {
                            'forced': True,
                            'units': [['day', [1]]],
                        },
                    }
                ]
            }
        }

        response = requests.post('http://highcharts:8080', json=data)
        if response.status_code != 200:
            error = 'Hightcharts return {} HTTP status'
        else:
            return send_file(io.BytesIO(response.content),
                             attachment_filename='chart.png',
                             mimetype='image/png')

    except Exception as e:
        error = str(e)

    return make_response(jsonify({
        'service': 'service3',
        'status': 'error',
        'message': error,
    }), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=LISTEN_PORT)
