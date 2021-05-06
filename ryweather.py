#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from decimal import Decimal
from flask import Flask, render_template

import requests


def get_cc():
    response = requests.get('https://api.bmsite.net/atys/weather?cycles=40&offset=0')
    decoded = json.loads(response.text)

    start_hour = Decimal(decoded['hour'])
    ig_hours = int(start_hour) % 24
    ig_min = int((start_hour - int(start_hour)) * 60)
    ig_time = '{}:{}'.format(ig_hours, ig_min)

    data = dict()
    for j in decoded['continents'].keys():
        data[j] = list()
        data['ig-start_time'] = ig_time
        data['cycles'] = list()
        cycle_en_cours = ig_hours
        for k in decoded['continents'][j].values():
            data['cycles'].append(cycle_en_cours)
            data[j].append(float(Decimal(k['value']) * 100))
            if cycle_en_cours == 23:
                cycle_en_cours = 0
            else:
                cycle_en_cours += 1
            data[j].append(float(Decimal(k['value']) * 100))
            data['cycles'].append(cycle_en_cours)
            if cycle_en_cours == 23:
                cycle_en_cours = 0
            else:
                cycle_en_cours += 1
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
