import requests
import json

id = 'AWAgLZGGjdrCRV_yB_jL'
resp = requests.get('http://172.24.177.30:9200/futures_data/article/' + id)
print(resp.text)
respJson = json.loads(resp.text)
# content = respJson['_source']
# content['type_variety'] = 1
# # respJson['_source']['type_variety'] = 1
#
# resp = requests.put('http://172.24.177.30:9200/futures_data/article/' + id, data=json.dumps(dict(content)))
# print(resp.text)
