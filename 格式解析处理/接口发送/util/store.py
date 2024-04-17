from confluent_kafka import Producer
import json
class Kafka(object):
    def __init__(self, config):
        # kafka produce
        self.p = Producer({"bootstrap.servers": config["kafka"]["http"],
                           "message.max.bytes": 20000000})

    def write(self, value, topic):
        # self.p.poll(0)
        self.p.produce(
            # config["kafka"]["topic.rca"],
            topic,
            json.dumps(value).encode("utf-8"),
            callback=self.delivery_report,
        )
        self.p.flush()
        
    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print('消息发送失败:', err)
        else:
            print('消息发送成功:', msg.topic(), msg.partition())