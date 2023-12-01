# -*- coding: utf-8 -*-

from socketserver import StreamRequestHandler as Tcp
from config import *
import select
import socket
import struct
import socks
import time
import os

SOCKS_VERSION = 5

class DYProxy(Tcp):
    # 用户认证 用户名/密码

    username = username
    password = password
    
    if username == '' and password == '':pass 
    elif username != '' and password != '':pass 
    else:
        print(f'{red}[{time.strftime("%X")}][CONFIG] [-] 配置错误！账号密码不可选填其一{end}')
        exit()

    def handle(self):

        self.time = time.strftime("%X")
        """
        一、客户端认证请求
            +----+----------+----------+
            |VER | NMETHODS | METHODS  |
            +----+----------+----------+
            | 1  |    1     |  1~255   |
            +----+----------+----------+
        """
        # 从客户端读取并解包两个字节的数据
        header = self.connection.recv(2)
        VER, NMETHODS = struct.unpack("!BB", header)
        # 设置socks5协议，METHODS字段的数目大于0
        assert VER == SOCKS_VERSION, 'SOCKS版本错误'

        # 接受支持的方法
        # 无需认证：0x00    用户名密码认证：0x02
        # assert NMETHODS > 0
        methods = self.IsAvailable(NMETHODS)
        # 检查是否支持该方式，不支持则断开连接

        
        """ 
        二、服务端回应认证
            +----+--------+
            |VER | METHOD |
            +----+--------+
            | 1  |   1    |
            +----+--------+
        """
        # 发送协商响应数据包 
    
        if self.username != '' and self.password != '': ##账密都填写的情况
            if 2 not in set(methods):
                print(f"{blue}[{self.time}][Client]{red} [-] 客户端:  {self.client_address}  无账密信息，无法与客户端验证-已挂断连接{end}")
                self.logdata(f"[-] 客户端:  {self.client_address}  无账密信息，无法与客户端验证-已挂断连接")
                self.server.close_request(self.request)
                return
            self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 2))
            if not self.VerifyAuth():
                return
        elif self.username == '' and self.password == '':
            if 0 not in set(methods):
                self.server.close_request(self.request)
                return
            self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 0))

        """
        三、客户端连接请求(连接目的网络)
            +----+-----+-------+------+----------+----------+
            |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
            +----+-----+-------+------+----------+----------+
            | 1  |  1  |   1   |  1   | Variable |    2     |
            +----+-----+-------+------+----------+----------+
        """
        version, cmd, _, address_type = struct.unpack("!BBBB", self.connection.recv(4))
        assert version == SOCKS_VERSION, 'socks版本错误'
        if address_type == 1:       # IPv4
            # 转换IPV4地址字符串（xxx.xxx.xxx.xxx）成为32位打包的二进制格式（长度为4个字节的二进制字符串）
            address = socket.inet_ntoa(self.connection.recv(4))
        elif address_type == 3:     # Domain
            domain_length = ord(self.connection.recv(1))
            address = self.connection.recv(domain_length).decode()
        port = struct.unpack('!H', self.connection.recv(2))[0]

        """
        四、服务端回应连接
            +----+-----+-------+------+----------+----------+
            |VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
            +----+-----+-------+------+----------+----------+
            | 1  |  1  |   1   |  1   | Variable |    2     |
            +----+-----+-------+------+----------+----------+
        """
        # 响应，只支持CONNECT请求
        # 校验用户名和密码
        
        try:
            if cmd == 1:  # CONNECT
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                p=socks.getdefaultproxy()
                print(f'{blue}[{self.time}][Client]{green} [+] 客户端:  {self.client_address}  已建立连接: {address,str(port)} 代理服务器: {":".join([p[1],str(p[2])])}{end}')
                self.logdata(f'[+] 客户端:  {self.client_address}  已建立连接: {address,str(port)} 代理服务器: {":".join([p[1],str(p[2])])}')
            else:
                self.server.close_request(self.request)
            addr = struct.unpack("!I", socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, address_type, addr, port)
        except Exception as err:
            print(f'{blue}[{self.time}][Client]{red} [-] 客户端:  {self.client_address} 连接: {address,str(port)}  发生错误: {err}{end}')
            self.logdata(f'[-] 客户端:  {self.client_address} 连接: {address,str(port)}  发生错误: {err}')
            # 响应拒绝连接的错误
            reply = self.ReplyFaild(address_type, 5)
        self.connection.sendall(reply)      # 发送回复包

        # 建立连接成功，开始交换数据
        if reply[1] == 0 and cmd == 1:
            self.ExchangeData(self.connection, remote)
        self.server.close_request(self.request)


    def IsAvailable(self, n):
        """ 
        检查是否支持该验证方式 
        """
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods


    def VerifyAuth(self):
        """
        校验用户名和密码
        """
        version = ord(self.connection.recv(1))
        assert version == 1
        username_len = ord(self.connection.recv(1))
        username = self.connection.recv(username_len).decode('utf-8')
        password_len = ord(self.connection.recv(1))
        password = self.connection.recv(password_len).decode('utf-8')
        if username == self.username and password == self.password:
            # 验证成功, status = 0
            #print(f"{blue}[{self.time}][Client]{green} [+] 客户端:  {self.client_address}  密码验证成功!{end}")
            response = struct.pack("!BB", version, 0)
            self.connection.sendall(response)
            return True
        # 验证失败, status != 0
        print(f"{blue}[{self.time}][Client]{red} [-] 客户端:  {self.client_address}  密码验证错误 已断开连接!{end}")
        self.logdata(f"[-] 客户端:  {self.client_address}  密码验证错误 已断开连接!")

        response = struct.pack("!BB", version, 0xFF)
        self.connection.sendall(response)
        self.server.close_request(self.request)
        return False


    def ReplyFaild(self, address_type, error_number):
        """ 
        生成连接失败的回复包 
        """
        return struct.pack("!BBBBIH", SOCKS_VERSION, error_number, 0, address_type, 0, 0)


    def ExchangeData(self, client, remote):
        """ 
        交换数据 
        """
        while True:
            # 等待数据
            try:
                rs, ws, es = select.select([client, remote], [], [])
                if client in rs:
                    data = client.recv(4096)
                    if remote.send(data) <= 0:
                        break
                if remote in rs:
                    data = remote.recv(4096)
                    if client.send(data) <= 0:
                        break
            except Exception as err:
                print(f'{blue}[{self.time}][Client]{red} [-] 客户端:  {self.client_address}  发生错误: {err}{end}')
                self.logdata(f'[-] 客户端:  {self.client_address}  发生错误: {err}')
                pass
    
    def logdata(self,data):
        global Record

        if Record:
            
            if os.path.getsize(logname) > FileSize:

                print(f'{red}[{self.time}][Logger] [-] 当前日志大小超过最大文件大小（{FileSize} KB） 已停止记录')

                open(logname, 'a', encoding='utf-8').write(f'[{self.time}][Logger] [-] 日志文件大小超出设定大小（{FileSize} KB） 已停止记录')

                Record = 0

            else:

                logger.info(data)

                        