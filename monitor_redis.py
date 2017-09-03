# -*- coding: utf8 -*-
import time
import json
try:
    from aliyunsdkcore import client
    from aliyunsdkcms.request.v20170301 import QueryMetricListRequest
    from Setting import Setting
    from tables import WriterExcel
except:
    print "模块调用失败"
else:
    setting = Setting()
    clock = time.strftime("%H")
    clt = client.AcsClient(setting.key,setting.secret,setting.region)
    redis_id = ('r-bp1c396acd502854','r-bp13fc14b38c5da4','r-bp1ca7bd1db816c4','r-bp1bfff289c99a34','r-bp170ed51dcea844',
                'r-bp10b2fdcd961784','r-bp19a88b60bca4c4','r-bp1e579bcc5c5784','293f5f093674492f')
    redis_alias = ('redis-5678','hosts1-4539','hosts3-4539','快递员+浩哥广告','澳门','notification_center的缓存队列+快递员活动coupon',
                   'yellow-bag','夏世康-短信延迟','Newtest')
    redis_list = []
    redis_tuple = []
    def monitor_redis(redisid,option_redis):
        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('json')
        request.set_Project(setting.project[2])  #redis监控
        request.set_Metric(option_redis)
        start_time = setting.start_time
        end_time = setting.end_time
        print start_time
        print end_time
        timestamp_start = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        timestamp_end = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        request.set_StartTime(timestamp_start)  # 获取数据的开始时间
        request.set_EndTime(timestamp_end)      #截止时间
        request.set_Dimensions({'instanceId': redisid})  # 传入实例ID
        request.set_Period(setting.period)  # 间隔时间
        result = json.loads(clt.do_action_with_exception(request)).get('Datapoints')
        for line in result:
            if line.get(setting.maximum) == 0:
                redis_list.append('O')
            else:
                redis_list.append(line.get(setting.maximum))

    def All_monitor_redis():
        for ID in redis_id:     #传入redis的实例id
            for line in setting.monitor_option_redis:   #将redis的监控参数传入函数
                monitor_redis(ID,line)
        for separate in range(0,len(redis_list),2):    #将redis_tuple列表分隔为2个元素一组的新列表
            redis_tuple.append(redis_list[separate:separate+2])     #将分隔的新列表存放到redis_tuple
    def main():
        All_monitor_redis()
        Data = tuple(redis_tuple)
        Excel_name = 'monitor_redis.xlsx'
        Title = ('实例 ID','实例别名','已用容量[%]','已用连接数[%]')
        write_tables = WriterExcel(Excel_name,Title,redis_id,redis_alias,Data)  #将ECS数据写入表格
        write_tables.write_excel()
    if __name__ == '__main__':
        main()

