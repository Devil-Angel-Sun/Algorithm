# coding=UTF-8
import os
import sys

currentPath,_ = os.path.split(os.path.abspath(__file__))
# currentPath = os.path.dirname(__file__)
sys.path.append(os.path.join(currentPath, '..'))
from algorithms.forecast import Forecast
from algorithms.util import ETL, LogHandler
from flask import Flask, request, jsonify
import configparser

app = Flask(__name__)

conf = configparser.ConfigParser()
conf.read(os.path.join(currentPath, '../../config.ini'))
# LogClass
Log = LogHandler(os.path.join(currentPath, '../../logs/offline/'), name='api', level=20)
# ElasticSearch
http = conf.get('elasticsearch', 'http')
index_from = conf.get('elasticsearch', 'index_from')
index_to = conf.get('elasticsearch', 'offline_to')

try:
    ETLObj = ETL(http, index_from, index_to)
    FCTObj = Forecast()
    Log.info("initialize success")
except (SystemExit, KeyboardInterrupt):
    raise
except Exception:
    Log.error("initialize fail", exc_info=True)


@app.route('/offline', methods=['POST'])
def offline():
    try:
        parameters = request.get_json()
        print(parameters)
        entity = parameters['metricsEntity']
        itemid = parameters['metricsIdentify']
        start = int(parameters['startStamp'])
        end = int(parameters['endStamp'])
        timecut = int(parameters['metricsCollectInterval'])

        if not ETLObj.check(entity, itemid, start, end):
            data1,_ = ETLObj.download(entity, itemid, start, end)
            data2 = ETLObj.extract(data1)
            data3 = FCTObj.forecast(data2, days=7, timecut=timecut)
            data4 = ETLObj.merge(forecast=data3, entity=entity, itemid=itemid, start=start, end=end)
            ETLObj.upload(data4)
            Log.info("forecast success:{}".format(parameters))
        return jsonify({"data": "success"})
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        Log.error("forecast fail", exc_info=True)
