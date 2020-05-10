#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, make_response, request
from nt import abort

app = Flask(__name__)

mks = [
    {
        'id': '1234',
        'Configure': True
    },
    {
        'id': '12345',
        'Configure': False
    }
]


@app.route('/mk', methods=['GET'])
def get_mks():
    return jsonify({'mk': mks})


@app.route('/mk', methods=['POST'])
def create_mk():
    if not request.json:  # or not 'id' in request.json:
        abort(400)
    for row in request.json:
        mk = {
            'id': row['id'],
            'Configure': row['Configure']
        }
        mks.append(mk)
    # mk = {
    #     'id': request.json['id'],
    #     'Configure': request.json['Configure']
    # }
    # mks.append(mk)
    # return jsonify({'mk': mk}), 201
    return jsonify(request.json), 201


@app.route('/')
def index():
    return "Hello, World!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    return 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
