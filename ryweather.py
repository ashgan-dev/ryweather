#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
from decimal import Decimal

import arrow
import requests
from dateutil.rrule import rrule, MINUTELY
from flask import Flask, render_template


def get_cc():
    response = requests.get('https://api.bmsite.net/atys/weather?cycles=40&offset=0')
    decoded = json.loads(response.text)

    data = dict()
    data['cycles'] = list()

    for dt in rrule(MINUTELY, dtstart=datetime.utcnow(), interval=3, count=120):
        data['cycles'].append(arrow.get(dt).to('Europe/Paris').format('HH:mm:ss'))

    cycle_courant = str(decoded['cycle'])
    ingame_hour = Decimal(decoded['hour'])
    ingame_min = ingame_hour - int(ingame_hour)

    min_left = 60 - int(ingame_min * 60)
    real_delta_time = timedelta(seconds=min_left * 0.05 * 60)
    next_cc = arrow.utcnow() + real_delta_time

    if int(ingame_hour) % 3 == 0:
        for i in decoded['continents'].keys():
            data[i] = list()
            popped_cycle = decoded['continents'][i].pop(cycle_courant)

            data[i].append(float(Decimal(popped_cycle['value']) * 100))
            data[i].append(float(Decimal(popped_cycle['value']) * 100))
            data[i].append(float(Decimal(popped_cycle['value']) * 100))

            for j in decoded['continents'][i].values():
                data[i].append(float(Decimal(j['value']) * 100))
                data[i].append(float(Decimal(j['value']) * 100))
                data[i].append(float(Decimal(j['value']) * 100))
    elif int(ingame_hour) % 3 == 1:
        for i in decoded['continents'].keys():
            data[i] = list()
            popped_cycle = decoded['continents'][i].pop(cycle_courant)

            data[i].append(float(Decimal(popped_cycle['value']) * 100))
            data[i].append(float(Decimal(popped_cycle['value']) * 100))

            for j in decoded['continents'][i].values():
                data[i].append(float(Decimal(j['value']) * 100))
                data[i].append(float(Decimal(j['value']) * 100))
                data[i].append(float(Decimal(j['value']) * 100))
    else:
        print('etat: transition')
        for i in decoded['continents'].keys():
            data[i] = list()
            popped_cycle = decoded['continents'][i].pop(cycle_courant)

            data[i].append(float(Decimal(popped_cycle['value']) * 100))

            for j in decoded['continents'][i].values():
                data[i].append(float(Decimal(j['value']) * 100))
                data[i].append(float(Decimal(j['value']) * 100))
                data[i].append(float(Decimal(j['value']) * 100))

    return data


app = Flask(__name__)


@app.route('/', methods=['GET'])
def start_page():
    data = get_cc()
    return render_template('index.html',
                           data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)