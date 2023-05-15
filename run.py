# -*- coding: utf-8 -*-

from socketserver import StreamRequestHandler as Tcp, ThreadingTCPServer
from server import DYProxy
from getaddress import *
from config import *
import threading
import socket
import random
import socks
import time
import sys
import os


def logo():
    print(yellow+"""
*********************************************************************************
|  _____                     _____            _       _____            _        |
| |  __ \                   |  __ \          | |     / ____|          | |       |
| | |__) | __ _____  ___   _| |__) |__   ___ | |_  _| (___   ___   ___| | _____ |
| |  ___/ '__/ _ \ \/ / | | |  ___/ _ \ / _ \| \ \/ /\___ \ / _ \ / __| |/ / __||
| | |   | | | (_) >  <| |_| | |  | (_) | (_) | |>  < ____) | (_) | (__|   <\__ \\|
| |_|   |_|  \___/_/\_\\\__, |_|   \___/ \___/|_/_/\_\_____/ \___/ \___|_|\_\___/|
|                       __/ |                                                   |
|                      |___/                                                    |
|⭐Title: ProxyPoolxSocks                                                       |
|⭐Author: Anyyy                                                                |
|⭐Blog: https://www.anyiblog.top/                                              |
*********************************************************************************"""+end)

def start():
    print(green+"==========================================================")
    print('| 节点获取完毕！当前可用节点数量：'+yellow+str(len(nodes))+green)
    print('| 已成功搭建本地代理服务器 配置信息如下：')
    print('|',red+f"IP: 0.0.0.0 Port: {port} 账号: {[username if username else None][0]} 密码: {[password if password else None][0]} 协议: socks5 可连接"+green)
    print('|',yellow+f"请自行前往客户端添加你的 公网/内网 IP 例: x.x.x.x:{port}"+green)
    print("=========================================================="+end)
    if Record == 1:open(logname,'w',encoding='utf-8');print(yellow+f'Tips:日志已开始记录至 {logname}'+end)
    Server = ThreadingTCPServer(('0.0.0.0', port), DYProxy)
    Server.serve_forever()

def clear():
    platform = sys.platform

    if 'win' in platform:

        os.system('cls')

    elif 'linux' in platform:

        os.system('clear')

def setproxy(nodes):
    
    nodes_ = []

    maxcount = len(nodes)

    while True:
 
        try:
            
            # 选取随机节点
            node = nodes[random.randint(0,len(nodes)-1)] 

            nodes_.append(node)

            del nodes[nodes.index(node)]

            # 设置代理
            socks.set_default_proxy(node[0], node[1], int(node[2]),rdns=True,username=node[3], password=node[4])
            
            socket.socket = socks.socksocket

            server = node[1]+":"+node[2]

            if ServerLog == 1:

                print(f'{cyan}[{time.strftime("%X")}][Server]{yellow} [*] 服务端当前代理服务器为 ：{server} 当前剩余: {len(nodes)}{end}')

            # 延迟
            time.sleep(times / 1000)

            # 当一轮节点被用光时重新换一轮
            if nodes == []:

                print(f'{cyan}[{time.strftime("%X")}][Server]{yellow} [*] 本轮服务端代理节点已用完 已替换下一批次 预计下一轮将在 {round(maxcount * (times/1000))}s 左右完成{end}')
                
                nodes,nodes_ = nodes_,nodes
        
        except Exception as e:

            #print('代理服务器超时: '+server , str(e))

            pass

if __name__ == '__main__':
    
    try:

        logo()

        content = open('.nodedata','r').read()

        try:
            
            content = eval(content)

        except:

            content = []

        if content != []:

            if str(input('检测到已有的代理节点 是否读取?(Y/n)>')).upper() == 'N':

                print(f'{yellow}[{time.strftime("%X")}][Node] [*] 获取节点中...... {end}')

                nodes = getNode()
                
            else:
                
                nodes = content
        else:
            print(f'{yellow}[{time.strftime("%X")}][Node] [*] 获取节点中...... {end}')
            
            nodes = getNode()

        if len(nodes) != 0:

            clear()

            t = threading.Thread(target=start,args=())

            t.start()
            
            time.sleep(0.5)

            setproxy(nodes)

    except KeyboardInterrupt:

        if Record == 1:
            try:
                open(logname,'r')
                print('日志已保存至 '+logname)
            except:
                pass

        print('[*] Exit success!')

        os._exit(0)
    
