# es存储、读取
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import math
import time
import logging
from logging.handlers import RotatingFileHandler
import os


class ETL(object):
    """docstring for ES."""

    def __init__(self, http, index_from, index_to):
        self.es = Elasticsearch(http,timeout=30, max_retries=10, retry_on_timeout=True)
        self.index_from = index_from
        self.index_to = index_to
        if not self.es.indices.exists(index=index_from):
            "not exist {}".format(index_from)
        if not self.es.indices.exists(index=index_to):
            self.es.indices.create(index=index_to)

    def delete(self, index, entity, itemid):
        # 条件删除
        body = {
            'query': {
                'bool': {
                    'must': [{'term': {'entity': entity}},
                             {'term': {'itemid': itemid}}
                             ]
                }
            }
        }
        self.es.delete_by_query(index=index, body=body, doc_type='_doc')

    def check(self, entity, itemid, start, end):
        body = {
            'query': {
                'bool': {
                    'must': [{'term': {'entity': entity}},
                             {'term': {'itemid': itemid}},
                             {'term': {'start': start}},
                             {'term': {'end': end}}
                             ]
                }
            }
        }
        queryData = self.es.search(index=self.index_to, body=body)
        total = queryData["hits"]["total"]
        if total > 0:
            return True
        else:
            return False

    def download(self, entity, itemid, start, end):
        """
        根据entity,itemid以及开始、结束时间，从es获取数据
        """
        body = {
            'query': {
                'bool': {
                    'must': [{'term': {'entity': entity}},
                             {'term': {'itemid': itemid}},
                             {'range': {'timestamp': {'gte': start, 'lte': end}}}
                             ]
                }
            },
            "aggs": {
                "maxVal": {
                    "max": {
                        "field": "timestamp"
                    }
                }
            }
        }
        batches = 100  # 每一批数据量大小
        queryData = self.es.search(index=self.index_from, scroll='5m', timeout='60s', size=batches, body=body)

        metadata = queryData.get("hits").get("hits")
        scroll_id = queryData["_scroll_id"]
        # total = queryData["hits"]["total"]#Elasticsearch_v6.7
        total = queryData["hits"]["total"]['value']#Elasticsearch_v7.9
        maxVal = int(queryData['aggregations']['maxVal']['value_as_string']) if total>0 else None
        for i in range(int(total / batches)):
            res = self.es.scroll(scroll_id=scroll_id, scroll='5m')  # scroll参数必须指定否则会报错
            metadata += res["hits"]["hits"]
        data = pd.DataFrame([x['_source'] for x in metadata])
        self.es.clear_scroll(scroll_id=scroll_id)
        return data,maxVal

    def upload(self, data):
        """
        data数据格式为[{},{}]
        """
        total = len(data)
        batches = 1000
        for i in range(int(math.ceil(total * 1.0 / batches))):
            action = [{
                '_index': self.index_to,
                '_type': '_doc',
                '_source': l
            } for l in data[i * batches:i * batches + batches]]
            helpers.bulk(self.es, action)

    def extract(self, data):
        df = data.sort_values(by='timestamp', ascending=True)
        df['ds'] = df['timestamp'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)))
        df['y'] = df['value']
        return df

    def merge(self, forecast, entity, itemid, start, end):
        forecast['timestamp'] = forecast['ds'].apply(
            lambda x: int(time.mktime(time.strptime(str(x), "%Y-%m-%d %H:%M:%S"))))
        data = forecast[
            ['timestamp', 'yhat', 'yhat_lower', 'yhat_upper', 'trend', 'daily', 'dutyday', 'holiday', 'workday']]
        data['entity'] = entity
        data['itemid'] = itemid
        data['start'] = start
        data['end'] = end

        data.rename(columns={'yhat': 'forecast', 'yhat_lower': 'forecastdown', 'yhat_upper': 'forecastup'},
                    inplace=True)
        data_dict = data.to_dict(orient='index')
        results = list(data_dict.values())
        return results


def makeDirsExist(dirname):
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError:
            pass


class LogHandler(logging.Logger):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # cls._instance = object.__new__(cls, *args, **kwargs)#Python2的写法
            cls._instance = object.__new__(cls)  # Python3的写法
        return cls._instance

    def __init__(self, path, name, level=30):
        self.path = path
        self.name = name
        self.level = level
        self.formatter = logging.Formatter(
            '%(asctime)s-%(filename)s[line:%(lineno)d]-%(funcName)s-%(levelname)s-%(message)s')
        super(LogHandler, self).__init__(name=name, level=level)

        makeDirsExist(self.path)
        self.__setFileHandler__()

    def __setFileHandler__(self):
        file = os.path.join(self.path, self.name + '.log')
        handler = RotatingFileHandler(file, maxBytes=104857600, backupCount=5)
        handler.setFormatter(self.formatter)
        self.addHandler(handler)
