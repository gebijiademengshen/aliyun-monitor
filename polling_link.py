# -*- coding: utf8 -*-
#钉钉机器人
import requests
import time
times = time.strftime("%Y-%m-%d/%H:%M")
url = 'https://oapi.dingtalk.com/robot/send?access_token=d2866759c21b3d84d4cfa3af8e7c4b7dd2eddb4b8c9654ec1e471f603f548dd3'
link = 'your web address'
def Data(weblink):
    info = {
        "msgtype":"markdown",
        "markdown":{
            "title":"巡检简报:%s\n"%times,
            "text": ">磁盘使用率超过85的ECS实例:" + "\n"
                    ">3天内需续费的ECS实例:" + "\n"
                    ">IOPS使用率超过85%的实例:" + "\n"
                    ">3天内需续费的RDS实例:" + "\n"
                    ">容量使用率超过85%的实例:" + "\n"
                    ">详情:"+weblink
        }
    }
    result = requests.post(url,json=info)
    print result
Data(link)
