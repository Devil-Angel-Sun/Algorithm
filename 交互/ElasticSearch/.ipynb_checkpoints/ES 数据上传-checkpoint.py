from random import randint, uniform
import pandas as pd
import time,datetime
import json, time
from confluent_kafka import Producer
from tqdm import tqdm
def trans(x):
    return int(time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S")))

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        pass

class Create():
    def __init__(self, both_config,single_configs):# single_configs可以是多个metric，both_config为这多个Metric的共同信息
        self.config = both_config
        self.configs = single_configs
        
    def handle_times(self, timestamp, timestamp_range):
        startTime = (timestamp + datetime.timedelta(minutes =- timestamp_range['before_datetime'])).strftime("%Y-%m-%d %H:%M:%S")
        endTime = (timestamp + datetime.timedelta(minutes =+ timestamp_range['after_datetime'])).strftime("%Y-%m-%d %H:%M:%S")
        if timestamp_range['interval'] != '0':
            timestamps = [trans(str(i)) for i in pd.date_range(startTime,endTime,freq = timestamp_range['interval'])]
        else:
            timestamps = [trans(str(i)) for i in pd.date_range(startTime,endTime,freq = 'min')]
        return timestamps
    
    def handle_values(self, value):
        if value['valuetype'] == 'int':
            values = randint(value['minvalue'], value['maxvalue'])
        elif value['valuetype'] == 'float':
            values = uniform(value['minvalue'], value['maxvalue'])
        elif value['valuetype'] == 'max':
            values = value['value']
        return values
            
    def main(self):
        results = []
        for single_config in self.configs:
            timestamp = self.handle_times(self.config['timestamp'], single_config['timestamp_range'])
            for index,t in enumerate(timestamp):
                result = {}
                result.update(self.config)
                
                result['timestamp'] = t
                result['metric'] = single_config['metric']
                result['metricsVal'] = self.handle_values(single_config['value'])
                result['collector'] = single_config['metric'].split('.')[0]
                result['collectorType'] = single_config['metric'].split('.')[1]
                result['tags'] = [':'.join(['host', self.config['host']]), ':'.join(['host_id', self.config['host_id']])]
                result['tag'] = {'host':self.config['host'], 'host_id':self.config['host_id']}
                results.append(result)
        return results
                
    def future(self,delay):
        future_results = []
        for single_config in self.configs:
            result = {}
            result.update(self.config)
            result['metric'] = single_config['metric']
            result['timestamp'] = trans((self.config['timestamp']+datetime.timedelta(minutes=+delay)).strftime("%Y-%m-%d %H:%M:%S"))
            result['metricsVal'] = self.handle_values(single_config['value'])
            result['collector'] = single_config['metric'].split('.')[0]
            result['collectorType'] = single_config['metric'].split('.')[1]
            result['tags'] = [':'.join(['host', self.config['host']]), ':'.join(['host_id', self.config['host_id']])]
            result['tag'] = {'host':self.config['host'], 'host_id':self.config['host_id']}
            future_results.append(result)
        return future_results
    
if __name__ == "__main__":
    config = {
        'apiKey':'NzhEMjlBOTk3MzkxRjk5MjQyMzMzQzI4',
        'type':'gauge',
        'host':'host160',
        'host_id':'3fc4e60c6dcde9f22e9af8598fd98801',
        'saveIndex':'dc_source_metrics_66324f8c50d5199aa0fe830ea2e062ce_20220818',
        'timestamp':datetime.datetime.now(),
    }
    config1 = {
        'metric':'tomcat.threads.busy',
        'timestamp_range':{'before_datetime':10, 'after_datetime':3, 'interval':'0'}, # 为'0'时采用1min间隔，若为’10s'，则间隔为10s
        'value':{'minvalue':0.7, 'maxvalue':0.9, 'valuetype':'float'} # 可以为'int',也可以为'float'
    }
    config2 = {
        'metric':'tomcat.threads.max',
        'timestamp_range':{'before_datetime':10, 'after_datetime':3, 'interval':'0'},
        'value':{'value':1, 'valuetype':'max'} 
    }
    # CreateObj = Create(config, [config1, config2])
    # results = CreateObj.main()
    
    # 传历史数据
    publisher = Producer({'bootstrap.servers': '192.168.50.110:19092'})
    CreateObj = Create(config, [config1, config2])
    results = CreateObj.main()
    for i in tqdm(results):
        publisher.poll(1)
        publisher.produce('dc_databuff_metric', json.dumps(i).encode('utf-8'),callback=delivery_report, timestamp = i['timestamp']*1000)
        publisher.flush()

    # 实时传数据
    for i in range(4,14):
        result = CreateObj.future(i)
        for j in result:
            publisher.poll(1)
            publisher.produce('dc_databuff_metric', json.dumps(j).encode('utf-8'),callback=delivery_report, timestamp = j['timestamp']*1000)
            publisher.flush()
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(j['timestamp'])))
            time.sleep(59)