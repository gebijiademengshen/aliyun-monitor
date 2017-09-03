# -*- coding: utf8 -*-
import json,time,os
try:
    from xlsxwriter import workbook
    from aliyunsdkcore import client
    from aliyunsdkcms.request.v20170301 import QueryMetricListRequest   #用于调用系统监控信息
    from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest #调用ecs的DescribeInstancesRequest接口，用于获取ECS列表
    from aliyunsdkecs.request.v20140526 import ModifyInstanceAutoRenewAttributeRequest  #用于触发ECS自动续费
    from Setting import Setting
    from tables import WriterExcel  #调用表格模块
except:
    print "模块调用失败！"
else:
    setting = Setting()
    clock = time.strftime("%H")
    ecs_instanceid = []    #用于存储获取的ECS实例ID
    ecs_alias = []  #存储ECS实例别名
    ecs_tuple = []
    clt = client.AcsClient(setting.key,setting.secret,setting.region)

    def ecs_list(number):   #获取ECS列表
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_PageNumber(number)   #定义页码变量，实例状态列表分页
        request.set_PageSize(100)   #请求100台机器
        request.set_Status('Running')  #ECS状态，Running\Starting\Stopped\Stopping
        request.set_InstanceChargeType(setting.chargetype[0])   #获取类型为包年包月的ECS
        result = json.loads(clt.do_action_with_exception(request)).get('Instances').get('Instance')
        for line in result:
            ecs_alias.append(line.get('InstanceName'))
            #print line.get('ExpiredTime')      #到期日期
            ecs_instanceid.append(line.get('InstanceId'))   #将获取的实例ID添加到ecs_instanceid列表
        return
    def All_Ecs_List():     #定义All_Ecs_List函数，和ecs_list函数关联
        for page in range(1,3):     #生成页码
            ecs_list(page)   #将生成的页码传入ecs_list函数
        return


    def monitor_disk(ecsid):     #获取磁盘监控信息
        DISK_LIST = []
        request = QueryMetricListRequest.QueryMetricListRequest()
        request.set_accept_format('json')   #输出格式
        request.set_Project(setting.project[0])
        request.set_Metric(setting.monitor_option_ecs[0])     #查询磁盘相关信息
        start_time = setting.start_time
        end_time = setting.end_time
        timestamp_start = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        timestamp_end = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        request.set_StartTime(timestamp_start)  # 获取数据的开始时间
        request.set_EndTime(timestamp_end)  # 截止时间
        request.set_Dimensions({'instanceId':ecsid})
        request.set_Period(setting.period)      #间隔时间900秒
        result = json.loads(clt.do_action_with_exception(request)).get("Datapoints")
        for line in result:
            DISK_LIST.append(line.get(setting.diskname))  #将信息追加到DISK_LIST列表
            DISK_LIST.append(line.get(setting.device))  # 挂载目录
            if line.get(setting.maximum) == 0:
                DISK_LIST.append('O')
            else:
                DISK_LIST.append(line.get(setting.maximum))   #磁盘最大使用率
        ecs_tuple.append(DISK_LIST)
        return
    def All_ecs_monitor():  #定义函数，获取所有的实例监控信息
        for line_ecs in ecs_instanceid:
            monitor_disk(str(line_ecs))      #需要遍历的列表内容转str再传入实例ID


    def renewal(Instanceid):  #续费
        request = ModifyInstanceAutoRenewAttributeRequest.ModifyInstanceAutoRenewAttributeRequest() #调用自动续费接口
        request.set_InstanceId(Instanceid)  #指定需要自动续费的实例ID，以逗号隔离
        request.set_Duration(1)     #自动续费的时长，可选择（1，2，3，6，12）
        request.set_AutoRenew('False')   #设定自动续费默认值为False
        result = json.loads(clt.do_action_with_exception(request))
    def All_renewall(): #定义All_renewal函数，和renewal函数关联
        ecs_instanceid_str1 = "%s" % ",".join(ecs_instanceid[0:100])  # 获取前100个实例并将ecs_instanceid列表转为以逗号隔开的str
        ecs_instanceid_str2 = "%s" % ",".join(ecs_instanceid[100:])  # 获取后第100个实例后的所有实例，并将ecs_instanceid列表转为以逗号隔开的str
        for instanceid_list in (ecs_instanceid_str1,ecs_instanceid_str2):    #将实例ID赋值给instanceid_list
            renewal(instanceid_list)     #将instanceid_all传入renewal函数
        return

    def main():
        All_Ecs_List()      #获取ECS信息开关
        #All_renewall()     #续费开关
        All_ecs_monitor()   #获取监控数据开关
        Data = tuple(ecs_tuple)
        Excel_name = 'monitor_ecs.xlsx'
        Title = ('实例 ID','实例别名','挂载目录1','使用率1[%]','磁盘1','挂载目录2','使用率2[%]','磁盘2','挂载目录3','使用率3[%]','磁盘3')
        write_tables = WriterExcel(Excel_name,Title,ecs_instanceid,ecs_alias,Data)  #将ECS数据写入表格
        write_tables.write_excel()
    if __name__ == '__main__':
        main()