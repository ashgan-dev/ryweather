#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from decimal import Decimal
from flask import Flask, render_template

import requests


def get_cc():
    response = requests.get('https://api.bmsite.net/atys/weather?cycles=40&offset=0')
    decoded = json.loads(response.text)

    data = dict()
    for j in decoded['continents'].keys():
        data[j] = list()
        data['cycles'] = set()
        for k in decoded['continents'][j].values():
            data['cycles'].add(k['cycle'])
            data[j].append(float(Decimal(k['value']) * 100))
            data[j].append(float(Decimal(k['value']) * 100))

    data['cycles'] = list(data['cycles'])
    return data


app = Flask(__name__)


@app.route('/', methods=['GET'])
def start_page():
    data = get_cc()
    print(data)
    return render_template('index.html',
                           data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)