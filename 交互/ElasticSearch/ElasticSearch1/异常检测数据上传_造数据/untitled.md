# 关于http://192.168.50.98:17302/ 的数据构建

elasticsearch的端口：192.168.50.98:19201

## 异常检测
index：dc_est_data
数据格式：
"properties": {
      "score": {
        "type": "double"
      },
      "itemid": {
        "type": "keyword"
      },
      "entity": {
        "type": "keyword"
      },
      "value": {
        "type": "double"
      },
      "forecast": {
        "type": "double"
      },
      "forecastup": {
        "type": "double"
      },
      "forecastdown": {
        "type": "double"
      },
      "timestamp": {
        "type": "date",
        "format": "epoch_second"
      }
    }

    
## 用户信息
index:dc_emp_data
数据格式：
"properties": {
        "score": {
          "type": "double"
        },
        "user": {
          "type": "keyword"
        },
        "scenario": {
          "type": "keyword"
        },
        "events": {
          "type": "text"
        },
        "date": {
          "type": "date",
          "format": "yyyy-MM-dd HH:mm:ss"
        }
      }
      
示例：
json_data = [{'user':'AKW0167', 
              'score':80, 
              'scenario':'敏感数据泄露', 
              'events':'{"2021-09-13 18:27:36": "aaaaaaaaaaaaaaaa","2021-09-13 18:24:36": "aaaaaaaaaaaaaaaa"}', 
              'date': '2021-09-13 17:00:00'},
            {'user':'AKW0167', 
              'score':70, 
              'scenario':'私人文件盗取', 
              'events':'{"2021-09-13 18:27:36": "aaaaaaaaaaaaaaaa","2021-09-13 18:24:36": "aaaaaaaaaaaaaaaa"}', 
              'date': '2021-09-13 17:00:00'}]