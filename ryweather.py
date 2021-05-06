#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from decimal import Decimal

import arrow
import requests
from dateutil.rrule import rrule, MINUTELY
from flask import Flask, render_template


def get_cc():
    response = requests.get('https://api.bmsite.net/atys/weather?cycles=40&offset=1')
    decoded = json.loads(response.text)

    data = dict()
    data['cycles'] = list()
    data['cycles'].append(arrow.utcnow().to('Europe/Paris').shift(minutes=-3).format('HH:mm'))
    for dt in rrule(MINUTELY, dtstart=datetime.now(), interval=3, count=79):
        data['cycles'].append(arrow.get(dt).to('Europe/Paris').format('HH:mm'))

    for j in decoded['continents'].keys():
        data[j] = list()

        for k in decoded['continents'][j].values():
            data[j].append(float(Decimal(k['value']) * 100))
            data[j].append(float(Decimal(k['value']) * 100))

    return data


app = Flask(__name__)


@app.route('/', methods=['GET'])
def start_page():
    data = get_cc()
    with open('/tmp/data.js', 'w') as data_file:
        json.dump(data, data_file)
    return render_template('index.html',
                           data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)