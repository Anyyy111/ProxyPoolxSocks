# -*- coding: utf-8 -*-
import logging
import time
"""
必要参数
username&password: 服务端要求验证的账号密码 留空代表不需要账号密码
"""
username= ""

password= ""

"""
必要参数
port: 服务端开放的端口
"""
port = 12000

"""
必要参数
times: 代理切换速度 单位 s 默认为 3 秒
detectTime: 更新可用节点的频率 单位 s 默认为 5 分钟 不启用添为0即可
"""
times = 3
detectTime = 60 * 5

"""
可选参数
ServerLog: 显示服务端信息 1为开启 0为关闭
Record: 开启日志记录 1为开启 0为关闭    PS: 日志只记录 服务端 的连接记录
FileSize: 日志文件最大大小 单位 kb 默认为 20 mb
"""
ServerLog = 1
Record = 1
FileSize = 1024 * 1024 * 20


# 颜色参数 忽略即可
red = "\033[1;31m"
green = "\033[1;32m"
blue = "\033[1;34m"
cyan = "\033[1;36m"
yellow = "\033[1;33m"
end = "\033[0m"

# 日志名称 同样忽略即可
logname = 'Logs/Server_{}.log'.format(time.strftime("%Y%m%d_%H'%M'%S"))
logger = logging.getLogger()
