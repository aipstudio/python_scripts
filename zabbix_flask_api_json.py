#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, make_response, request, abort
import threading
import os

app = Flask(__name__)

mks = []

@app.route('/mk', methods=['GET'])
def get_mks():
    return jsonify({'mk': mks})


@app.route('/mk', methods=['POST'])
def create_mk():
    if not request.json:  # or not 'id' in request.json:
        return make_response(jsonify({'error': 'Wrong JSON'}), 400)
        abort(400)
    for row in request.json:
        mk = {
            'id': row['id'],
            'Configure': False
        }
        mks.append(mk)
    
    def do_work(value):
        for row in mks:
            print(row['id'])
            #os.system('zabbix_sender -z '+server+' -s '+row['id'].lower()+' -k mikrotik_trap -o "Микротик нуждается в конфигурировании."')

    
    thread = threading.Thread(target=do_work(mks))
    thread.start()
    # mk = {
    #     'id': request.json['id'],
    #     'Configure': request.json['Configure']
    # }
    # mks.append(mk)
    # return jsonify({'mk': mk}), 201
    #return jsonify(request.json), 201
    return jsonify('{STATUS: OK}'), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    return 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
