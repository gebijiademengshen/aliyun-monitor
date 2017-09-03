# -*- coding: utf8 -*-
import json,time
from aliyunsdkcore import client
from aliyunsdkcms.request.v20170301 import QueryMetricListRequest
class Setting(object):
    def __init__(self):
        #------时间换算-----begin-------
        times = time.strftime("%Y-%m-%d %H")
        clock_m = time.strftime("%M")
        values_1 = int(clock_m) - 10
        values_2 = values_1 + 5
        if values_1 < 10 and values_1 >= 0:
            self.start_time = times + ":0" + str(values_1) + ":" + "00"
        elif values_1 < 0:
            values_1 = abs(values_1)
            if values_1 >= 10:
                self.start_time = times + ":" + str(values_1) + ":" + "00"
            else:
                self.start_time = times + ":0" + str(values_1) + ":" + "00"
        else:
            self.start_time = times + ":" + str(values_1) + ":" + "00"
        if values_2 < 10 and values_2 >= 0:
            self.end_time = times + ":0" + str(values_2) + ":" + "00"
        elif values_2 < 0:
            values_2 = abs(values_2)
            if values_2 >= 10:
                self.end_time = times + ":" + str(values_2) + ":" + "00"
            else:
                self.end_time = times + ":0" + str(values_2) + ":" + "00"
        else:
            self.end_time = times + ":" + str(values_2) + ":" + "00"
        # ------时间换算-----end-------
        self.key = "your key"
        self.secret = "your secret"
        self.region = "your region"
        self.diskname = "diskname"  #分区名称
        self.maximum = "Maximum"    #磁盘利用率
        self.device = "device"      #挂载目录
        self.period = "600"     #1分钟获取一次
        self.project = ["acs_ecs_dashboard","acs_rds_dashboard","acs_kvstore"]    #实例类别<ECS/RDS>
        self.monitor_option = {'ConnectionUsage':'连接数','IOPSUsage':'IOPS','CpuUsage':'CPU使用率'}    #RDS查询条件
        self.monitor_option_ecs = ['diskusage_utilization']
        self.monitor_option_redis = ['ConnectionUsage','MemoryUsage']
        self.chargetype = ['PrePaid','PostPaid']    #包年包月和按量付费2种类型