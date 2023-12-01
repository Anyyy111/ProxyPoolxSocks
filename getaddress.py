# -*- coding: utf-8 -*-

from config import *
import requests
import threading
import base64
import socks
import time
import sys
import os

"""
读取 node.txt 配置信息
"""
def readconfig():
    content = open('node.txt','r').read()
    # base64节点解码
    try: 

        content = base64.b64decode(content).decode()

    except:

        pass
    
    # 判断节点信息中是否存在socks节点
    if "socks://" not in content:

        return False
    
    return content.split('\n')
    

"""
socks5 协议处理
"""
def socks5(node):
    if "#" in node:node = node.split('#')[0]
    #proxy_type=None, addr=None, port=None, rdns=True, username=None, password=None
    proxy_type = socks.SOCKS5

    if "@" in node:

        b64_user_pass = node.split('@')[0].split('socks://')[1]

        addr, port = node.split('@')[1].split(':')

        username, password = base64.b64decode(b64_user_pass).decode().split(':')

    else: #没有带@的情况，默认账密为空

        addr, port = node.split('socks://')[1].split(':')

        username, password = '',''
    
    return (proxy_type,addr,port,username,password)



"""
vmess 协议处理
PS: 网上没有找到Python调用vmess节点之类的资料 先填个坑
"""
#def vmess(node):
#    pass


def check(node):

    global newlist

    CHECKTIME = 5

    CHECKURL = "http://123.156.230.90"

    # 构造socks5代理
    proxies = {
        'https':'socks5://{}:{}@{}:{}'.format(node[3],node[4],node[1],node[2]),
        'http':'socks5://{}:{}@{}:{}'.format(node[3],node[4],node[1],node[2])
    }

    try:

        requests.get(CHECKURL,proxies=proxies,timeout=CHECKTIME)
        newlist.append(node)

    except:

        pass


def getNode(nodes=[]):
    global newlist

    node_list = []


    if nodes != []: ## detect检测并迭代原先的node

        node_list = nodes

        newlist = []

        for node in node_list:

            t = (threading.Thread(target=check,args=(node,)))
                
            t.start()


        while True:

            count = len(threading.enumerate())

            print(f"\r[*] 剩余节点数量:{count}",end='\t')

            sys.stdout.flush()

            if count <= 3:
                    
                open('.nodedata','w').write(str(newlist))

                return newlist
    
    else: ## 只检测node.txt的节点 不迭代原先节点

        nodes = readconfig()

        # 选取包含socks的协议

        if nodes:
        
            print(f'{yellow}[{time.strftime("%X")}][Node] [+] 节点读取成功! {end}')

            for node in nodes:
                
                if node != '':

                    if "socks://" in node:

                        node_list.append(socks5(node))
                    
            if node_list == []:

                print(f'{red}[{time.strftime("%X")}][Config] [-] 当前节点为空，已退出运行。请在 node.txt 设置节点信息{end}')
                
                os._exit(0)

            # 对剩下的节点进行速度筛选 选去不可用的节点

            print(f'{yellow}[{time.strftime("%X")}][Node] [*] 已开始测试可用节点 -> 当前测试节点共有: {len(node_list)}个 {end}')

            newlist = []

            for node in node_list:

                t = (threading.Thread(target=check,args=(node,)))
                
                t.start()


            while True:

                count = len(threading.enumerate())

                print(f"\r[*] 剩余节点数量:{count}",end='\t')

                sys.stdout.flush()

                if count <= 3:
                    
                    open('.nodedata','w').write(str(newlist))

                    return newlist
        else:
            
            print(f'{red}[{time.strftime("%X")}][Config] [-] 当前节点为空，已退出运行。请在 node.txt 设置节点信息{end}')
        
            os._exit(0)
