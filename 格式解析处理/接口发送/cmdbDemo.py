import requests
import json
session = requests.Session()
login_url = "http://ywmh.sh.sgcc.com.cn/sso/api-token-auth/"
username = "mahayana"
password = "MAha_6997_yana"
login_data = {"username": username,"password": password}
app_token = json.loads(session.post(login_url, login_data).content)['token']
session.cookies.update({'app_token': app_token})
cmdb_url = 'http://ywmh.sh.sgcc.com.cn/cmdb/index/'
session.get(cmdb_url)
url = "http://ywmh.sh.sgcc.com.cn/cmdb/search/query_ci/"
data = {
    'cicat_id': [260],
    'exact': {},
    'define': [],
    'order': {}
}
headers = {
    'X-CSRFToken': session.cookies.get('csrftoken')
}
res = session.post(url=url, json=data, headers=headers)
df = res.json()
data = df['data']

import time
t = {'timestamp':time.time()}

from confluent_kafka import Producer

topic = 'dc_gw_cmdb'
http = '10.131.142.24:19092,10.131.142.25:19092'
p = Producer({'bootstrap.servers':http})
for I in data:
	I.update(t)
	p.produce(topic,value=json.jumps(I))
	p.poll(0)
