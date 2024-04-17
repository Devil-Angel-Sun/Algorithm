# coding=UTF-8
import os
import sys
import configparser
import pymysql
import time
import multiprocessing

currentPath,_ = os.path.split(os.path.abspath(__file__))
sys.path.append(os.path.join(currentPath, '..'))
from algorithms.util import ETL, LogHandler
from algorithms.forecast import Forecast

conf = configparser.ConfigParser()
conf.read(os.path.join(currentPath, '../../config.ini'))
# ElasticSearch
http = conf.get('elasticsearch', 'http')
index_from = conf.get('elasticsearch', 'index_from')
index_to = conf.get('elasticsearch', 'online_to')
# LogClass
Log = LogHandler(os.path.join(currentPath, '../../logs/online/'), name='api', level=20)

# initialize
try:
    # MySQL
    host = conf.get('mysql', 'host')
    port = int(conf.get('mysql', 'port'))
    user = conf.get('mysql', 'user')
    password = conf.get('mysql', 'password')
    database = conf.get('mysql', 'database')
    table = conf.get('mysql', 'table')
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset="utf8")
    cursor = db.cursor()
    cursor.execute("SELECT metrics_entity AS entity,metrics_identify AS itemid,metrics_data_source AS source,"
                   "metrics_collect_interval as timecut FROM {} WHERE metrics_algorithm LIKE '%Forecast%'".format(table))
    results = cursor.fetchall()
    db.close()

    FCTObj = Forecast()
    Log.info("initialize success")
except (SystemExit, KeyboardInterrupt):
    raise
except Exception:
    Log.error("initialize fail", exc_info=True)


def online(value):
    try:
        entity = value[0]
        itemid = value[1]
        source = value[2]
        timecut = value[3]
        if source == 'bpc':
            timespan = 12960000 #5months
        elif source == 'zabbix':
            timespan = 7776000 #3months
        else:
            timespan = 12960000 #5months
        end = int(time.time())
        start = end-timespan
        ETLObj = ETL(http, index_from, index_to)
        data1,maxTime = ETLObj.download(entity, itemid, start, end)
        if data1.empty or (not maxTime):
            pass
        elif end-maxTime<518400: #6days
            data2 = ETLObj.extract(data1)
            num = int((max(data2.timestamp) - min(data2.timestamp)) / (86400)) + 1
            days = num if num < 8 else 8
            data3 = FCTObj.forecast(data2, days=days, timecut=timecut)  # 往后预测8天的数据
            data4 = ETLObj.merge(forecast=data3, entity=entity, itemid=itemid, start=start, end=end)
            ETLObj.delete(index=index_to, entity=entity, itemid=itemid)
            ETLObj.upload(data4)
        else:
            pass
        Log.info("forecast success")
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        Log.error("forecast fail", exc_info=True)


def run():
    pool = multiprocessing.Pool(2)
    pool.map_async(online, results).get(999999)


if __name__ == "__main__":
    run()
