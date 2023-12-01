# -*- coding: utf-8 -*-

from socketserver import StreamRequestHandler as Tcp, ThreadingTCPServer
from logging.handlers import RotatingFileHandler
from server import DYProxy
from getaddress import *
from config import *
import threading
import socket
import random
import socks
import time
import copy
import sys
import os

VERSION = "v1.3"

def logo():
    print(cyan+f"""
╭───────────────────────────────────────────────────────────────────────────────╮
│  _____                     _____            _       _____            _        ┃
│ |  __ \                   |  __ \          | |     / ____|          | |       ┃
│ | |__) | __ _____  ___   _| |__) |__   ___ | |_  _| (___   ___   ___| | _____ ┃
│ |  ___/ '__/ _ \ \/ / | | |  ___/ _ \ / _ \| \ \/ /\___ \ / _ \ / __| |/ / __|┃
│ | |   | | | (_) >  <| |_| | |  | (_) | (_) | |>  < ____) | (_) | (__|   <\__ \\┃
│ |_|   |_|  \___/_/\_\\\__, |_|   \___/ \___/|_/_/\_\_____/ \___/ \___|_|\_\___/┃
│                       __/ |                                                   ┃
│                      |___/                                                    ┃
│{blue}⭐Title: ProxyPoolxSocks{cyan}                                                       ┃
│{blue}⭐Author: Anyyy{cyan}                                                                ┃
│{cyan}⭐Blog: https://www.anyiblog.top/{cyan}                                              ┃
│{green}⭐Version: {VERSION}{cyan}                                                                ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"""+end)

def info():
    print(green+"==========================================================")
    print('| 节点获取完毕！当前可用节点数量：'+yellow+str(len(nodes))+f"{cyan} 每{detectTime / 60}分钟检测可用的节点 "+green)
    print('| 已成功搭建本地代理服务器 配置信息如下：')
    print('|',red+f"IP: 0.0.0.0 Port: {port} 账号: {[username if username else None][0]} 密码: {[password if password else None][0]} 协议: socks5 可连接"+green)
    print('|',yellow+f"请自行前往客户端添加你的 公网/内网 IP 例: x.x.x.x:{port}"+green)
    print("=========================================================="+end)
    if Record == 1:

        logger.setLevel(logging.DEBUG)
        file_handler = RotatingFileHandler(logname, encoding="utf-8", maxBytes=FileSize)
        formatter = logging.Formatter(fmt="[%(asctime)s][Client] %(message)s",datefmt="%H:%M:%S")

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print(yellow+f'Tips:日志已开始记录至 {logname} 文件最大可记录 {FileSize} KB'+end+'\n')


def start():
    info()
    Server = ThreadingTCPServer(('0.0.0.0', port), DYProxy)
    Server.serve_forever()

def clear():

    platform = sys.platform

    if 'win' in platform:

        os.system('cls')

    elif 'linux' in platform:

        os.system('clear')

def updatenode():
    global nodes,rounds
    
    rounds += 1
    print(f'{yellow}[{time.strftime("%X")}][Node] [*] Round: {rounds} 定时任务执行！ 正在更新节点...... (每{detectTime}秒更新){end}')
    nodes = getNode(initNodes) # getNode(initNodes)代表基于目前的节点进行更新迭代

    # nodes = getNode() #getNode()则代表每一次更新基于node.txt的所有节点
    # 嘿！我是注释！！==== 自行选择模式，个人认为现在修改后的版本最好 ====  
    clear()
    info()

    print(f'{green}[{time.strftime("%X")}][Node] [+] 节点更新成功 当前节点数量: {len(nodes)} {end}')

    setproxy(nodes)

def setproxy(nodes):
    
    nodes_ = []

    maxcount = len(nodes)

    t1 = time.perf_counter()

    while True:
 
        try:   

            t2 = time.perf_counter()

            if detectTime != 0 and t2 - t1 >= (detectTime): #超时重置节点

                updatenode()

                break

            # 选取随机节点
            node = nodes[random.randint(0,len(nodes)-1)] 

            nodes_.append(node)

            del nodes[nodes.index(node)]

            # 设置代理
            socks.set_default_proxy(node[0], node[1], int(node[2]),rdns=True,username=node[3], password=node[4])
            
            socket.socket = socks.socksocket

            server = node[1]+":"+node[2]

            if ServerLog == 1:

                print(f'{cyan}[{time.strftime("%X")}][Server]{yellow} [*] 服务端当前代理服务器为：{server} 当前剩余: {len(nodes)}{end}')

            # 延迟
            time.sleep(times)

            # 当一轮节点被用光时重新换一轮
            if nodes == []:

                print(f'{cyan}[{time.strftime("%X")}][Server]{yellow} [*] 本轮服务端代理节点已用完 已替换下一批次 预计下一轮将在 {round(maxcount * (times))}s 左右完成{end}')
                
                nodes,nodes_ = nodes_,nodes
        
        except Exception as e:

            #print('代理服务器超时: '+server , str(e))

            pass

if __name__ == '__main__':
    
    rounds = 0
    
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

            initNodes = copy.deepcopy(nodes)
            
            try:

                clear()

                threading.Thread(target=start,args=()).start()
                
                time.sleep(0.5)

                setproxy(nodes)

            except KeyboardInterrupt:

                if Record == 1:
                    try:
                        print('日志已保存至 '+logname)
                    except:
                        pass
                    
                print('[*] Exit success!')

                os._exit(0)

    except KeyboardInterrupt:

        print('[*] Exit success!')

        os._exit(0)
    
