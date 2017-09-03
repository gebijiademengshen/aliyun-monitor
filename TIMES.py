#--ucoding=utf8---
import pytz
from datetime import datetime
class DayS(object):
    def __init__(self,utc_time_str):
        self.utc_time_str = utc_time_str    #接收外部传入的UTC时间
        self.utc_format = "%Y-%m-%dT%H:%M:%SZ"
        self.local_tz = pytz.timezone('Asia/Chongqing')     #时区
        self.local_format = "%Y-%m-%d %H:%M:%S"     #格式化格式
        self.local_times = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取本地实时时间
    def days_values(self):
        utc_dt = datetime.strptime(self.utc_time_str, self.utc_format)   #调整UTC格式
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(self.local_tz)    #转换UTC为本地时间，加8小时
        self.time_str = local_dt.strftime(self.local_format)     #格式化时间
        UTC = datetime.strptime(self.time_str,"%Y-%m-%d %H:%M:%S")   #将格式化后的utc时间的数据类型转换至datetime.datetime格式
        LOCAL = datetime.strptime(self.local_times,"%Y-%m-%d %H:%M:%S")     #将本地实时时间的数据类型转换至datetime.datetime格式
        day_values = (UTC-LOCAL).days  #计算时间差
        return day_values   #返回结果