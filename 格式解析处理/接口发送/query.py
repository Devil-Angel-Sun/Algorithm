import requests, time, json
from ..src.util.store import Kafka
from ..src.util.log import LogHandler


class postdata:
    def __init__(self):
        with open('./util/config.json','r') as json_file:
            self.params = json.load(json_file)
        self.kafkaobj = Kafka(self.params)
        self.LogForest = LogHandler("query", "INFO").logger_basic()
        self.get_cmdb_token()     
    
    def get_cmdb_token(self):
        self.session = requests.Session()
        login_data = {'username': self.params['token']['username'], 'password': self.params['token']['password']}
        app_token = json.loads(self.session.post(self.params['token']['login_url'], login_data).content)['token']
        self.session.cookies.update({'app_token': app_token})
        self.session.cookies.update({'csrftoken': self.params['cookies']['csrftoken']})
        self.session.headers.update({'X-CSRFToken': self.params['cookies']['X-CSRFToken']})
        self.session.get(self.params['cmdb']['cmdb_url'])

    def query_ci(self, query):
        # 请求微服务参数  ，cicat_id: 272 代表微服务环境
        if query == 'microservice':
            query_data = {{"exact":{"value":"","flag":"fuzzy"},"cicat_id":[272],"order":{},"define":[{"input_type":"select","servicestatus":["在用"]},{"input_type":"text","ssfw|fqdn":""},{"input_type":"text","ssfw|name":""},{"input_type":"relaAttr","ssfw|YYXT_SHXT":""},{"input_type":"text","ssfw|Eservername":""},{"input_type":"text","ssfw|YYXT_SHXT|fqdn":""},{"input_type":"text","ssfw|YYXT_SHXT|name":""},{"input_type":"text","ssfw|YYXT_SHXT|systemenbrief":""},{"input_type":"select","ssfw|YYXT_SHXT|yyxtyxzt":""}]}}

        # 请求虚拟机参数 260,333代表虚拟机
        if query == 'linux':
            query_data = {"exact":{"value":"","flag":"fuzzy"},"cicat_id":[260,333],"order":{},"define":[{"input_type":"select","sbzt":["在运"]}]}

        # 请求应用服务（中间件）参数 包括kafka，es
        if query == 'middleware':
            query_data ={"exact":{"value":"","flag":"fuzzy"},"cicat_id":[268],"order":{},"define":[{"input_type":"select","servicestatus":["在用"]},{"input_type":"select","servicename|servicestatus":["在用"]},{"input_type":"text","servicename|serviceip":""},{"input_type":"text","servicename|service_domain":""},{"input_type":"text","servicename|serverport1":""},{"input_type":"text","run_on|fqdn":""},{"input_type":"text","run_on|name":""},{"input_type":"select","run_on|sbzt":""},{"input_type":"date","run_on|putdate":""},{"input_type":"textNum","run_on|cpuvirtualcores":""}]}

        # 请求数据库，包括mongodb，redis，postgres，mysql，oracle
        if query == 'database':
            query_data = {"exact":{"value":"","flag":"fuzzy"},"cicat_id":[273,274,320],"order":{},"define":[{"input_type":"select","servicestatus":["在用"]}]}
        result = json.loads(self.session.post(url=self.params['cmdb']['query_url'], json=query_data).content)
        return result['data']
    
    def main(self,querys):
        for query in querys:
            t = {'timestamp':time.time()}
            try:
                results = self.query_ci(query)
                for result in results:
                    result.update(t)
                    self.kafkaobj.write(result,self.params['kafka']['topic'])
                    self.LogForest.info(f"当前数据{result}")
            except Exception:
                self.LogForest.error(f"数据上传失败", exc_info=True)

if __name__ == '__main__':
    querys = ['microservice', 'linux', 'database', 'middleware']
    postdata().main(querys)