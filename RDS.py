# -*- coding: utf8 -*-
import json,time
try:
    from aliyunsdkcore import client
    from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
    from aliyunsdkcms.request.v20170301 import QueryMetricListRequest
    from Setting import Setting
    from TIMES import DayS
except:
    print "模块调用失败！"
else:
    setting = Setting()
    clock = time.strftime("%H")
    clt = client.AcsClient(setting.key, setting.secret, setting.region)
    monitor_info_list = []  # 存储获取的监控数据
    monitor_tuple = []      #存储将monitor_info_list分隔后的小列表
    names = {}  #用于存储实例ID和实例别名
    rds_times = {}   #用于存储过期时间
    def rds_list(): #定义rds_list函数，用于获取所有的rds实例ID
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_Engine('MySQL') #请求的RDS类型
        request.set_PageSize(100)   #允许请求的RDS最大数量
        result = json.loads(clt.do_action_with_exception(request)).get('Items').get('DBInstance')
        for line in result:
            names[line.get('DBInstanceId')] = line.get('DBInstanceDescription')
            alias = line.get('DBInstanceDescription')
            if line.get('ExpireTime') != '':
                expiretime = line.get('ExpireTime')
                days = DayS(expiretime)
                print "还有%s"%days.days_values()+"天到期","实例:",line.get('DBInstanceDescription')
    def monitor_info(rds_id,monitor_option,param):
        name = param
        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('json')   #输出格式
        request.set_Project(setting.project[1])
        request.set_Metric(monitor_option)     #查询通过接收传入的查询条件获取RDS相关信息
        start_time = setting.start_time
        end_time = setting.end_time
        timestamp_start = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        timestamp_end = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        request.set_StartTime(timestamp_start)  # 获取数据的开始时间
        request.set_EndTime(timestamp_end)  # 截止时间
        request.set_Dimensions({'instanceId':rds_id})   #传入实例ID
        request.set_Period(setting.period)      #间隔时间900秒
        result = json.loads(clt.do_action_with_exception(request)).get("Datapoints")
        for line in result:
            if line.get("Average") >= 50:   #获取数据
                print line.get("Average")
                print "偏高:%s"%param,"实例id:%s"%rds_id
    def rds_monitor_all():      #定义rds_monitor_all函数，和monitor_info关联
        for ID in names.keys():
            for option_key,option_values in setting.monitor_option.items():   #将查找条件赋值给option变量
                monitor_info(str(ID),option_key,option_values)    #将获取的查找条件传给monitor_info函数
    def main():
        rds_list()
        rds_monitor_all()
    if __name__ == '__main__':
        main()
