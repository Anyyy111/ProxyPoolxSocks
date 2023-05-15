# -*- coding: utf-8 -*-
import requests
import socket
import socks
import os

print('Client 客户端测试代理连接脚本')

while 1:
    
    try:

        # 不存在密码就用这一条
        ## socks.set_default_proxy(socks.SOCKS5, "0.0.0.0", 12000)

        # 客户端存在密码用这一条
        socks.set_default_proxy(socks.SOCKS5, "0.0.0.0", 12000, username='aaa',password='bbb')
        
        socket.socket = socks.socksocket

        response = requests.get('https://ifconfig.me/',timeout=5).text
        
        print("测试成功 当前代理:",response)

    except KeyboardInterrupt:

        os._exit(0)