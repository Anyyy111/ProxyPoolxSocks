# ProxyPoolxSocks 自定义Socks代理池服务端自动化搭建

声明：本工具仅供以安全为目的的学习交流使用，任何人不得将其用于非法用途以及盈利等目的，否则后果自行承担。

## 0x01 介绍

作者: Anyyy

博客: https://www.anyiblog.top	

ProxyPoolxSocks 是一个代理池服务端工具，可以导入自定义的socks节点，理论来说只要你的代理够多，就可以有效防止Ban IP操作绕过一些WAF。

工具支持Windows和Linux系统。

## 0x02 安装

注意python环境3.7以上即可。

### 服务端

```
git clone https://github.com/Anyyy111/ProxyPoolxSocks.git
cd ProxyPoolxSocks
pip install -r requirements.txt
python3 run.py
```

详细配置请参考 **0x04 使用说明**

### 客户端

服务端配置好之后，修改client.py，运行即可测试可用性。

详细配置请参考 **0x04 使用说明**

```
git clone https://github.com/Anyyy111/ProxyPoolxSocks.git
cd ProxyPoolxSocks
python3 Client-check/client.py
```

测试可用之后可跳转至 **0x05 常见工具代理配置**



## 0x03 效果展示

![image-20230515161255262](imgs/image-20230515161255262.png)

![image-20230515161416289](imgs/image-20230515161416289.png)



## 0x04 使用说明

### 服务端配置

#### 1.设置config.py参数

```python
# -*- coding: utf-8 -*-
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
times: 代理切换速度 单位 ms 默认为 3 秒
"""
times = 3000

"""
可选参数
ServerLog: 显示服务端信息 1为开启 0为关闭
Record: 开启日志记录 1为开启 0为关闭    PS: 日志只记录 服务端 的连接记录
"""
ServerLog = 1
Record = 1


# 颜色参数 忽略即可
red = "\033[1;31m"
green = "\033[1;32m"
blue = "\033[1;34m"
cyan = "\033[1;36m"
yellow = "\033[1;33m"
end = "\033[0m"

# 日志名称 同样忽略即可
logname = f'Logs/Server_{time.strftime("%Y%m%d_%H%M%S")}.log'
```

配置文件我已经配置好了，你可以根据需求更改参数：

- username & password 服务端的连接账号密码**，如果留空则代表不需要密码，**如果填写必须二者都填写 且客户端连接要账密一致才能使用代理**
- port 服务端搭起的端口**，默认为12000，最终连接的端口就是这
- **times** **代理池之间代理切换的速度**，单位为毫秒，times越小切换越快，尽量不要太小容易出问题。
- ServerLog **显示服务端的信息**，设置为0则代表关闭 也就代表只显示客户端的连接信息。
- Record **开启日志文件记录**，设置为0则代表关闭 日志文件存放在 **Logs/Server_xxxx_xxxx.log**





#### 2.将socks节点添加至node.txt

node.txt是必须配置项，因为程序读取的节点就是来自这里。其中一行代表一个代理地址。

形式如下：

```
## socks://base64(username:password)@IP:PORT

socks://NTU1NTU6NTU1NTU=@8.xxx.xxx.12:59108#3
socks://YWFhYWE6YWFhYWE=@8.xxx.xxx.12:38810#1
socks://YWFhYWE6YWFhYWE=@152.xx.xxx.225:38829
socks://NTU1NTU6NTU1NTU=@47.xxx.xxx.214:59108#4
```

同样支持base64形式：

```
c29ja3M6Ly9OVFUxTlRVNk5UVTFOVFU9QDgueHh4Lnh4eC4xMjo1OTEwOCMzCnNvY2tzOi8vWVdGaFlXRTZZV0ZoWVdFPUA4Lnh4eC54eHguMTI6Mzg4MTAjMQpzb2NrczovL1YzRkRjazFvVlVsdFZUcGFSMjFsVVVOMGVVNWFAMTUyLnh4Lnh4eC4yMjU6Mzg4MjkKc29ja3M6Ly9OVFUxTlRVNk5UVTFOVFU9QDQ3Lnh4eC54eHguMjE0OjU5MTA4IzQ=
```

你可以直接从V2ray等代理软件里复制节点，选中节点并复制

![image-20230515163301348](imgs/image-20230515163301348.png)



或者如果你购买了机场，你可以在你的代理软件里找到你订阅的服务器地址，然后在文件夹输入以下命令即可：

（一般订阅地址长这样：`https://xxx.com/api/v1/client/subscribe?token=xxxxxx`）

```
curl https://xxx.com/api/v1/client/subscribe?token=xxxxxx -o node.txt
```

![image-20230515164116160](imgs/image-20230515164116160.png)

*程序只会调用订阅地址中存在socks协议的部分，其它部分忽略。



**注：测试的时候只拿了V2ray的socks节点来测试，如果你是其它的代理软件请将节点修改成符合以上的形式后写入node.txt中。**

**这里程序不提供免费的节点，如果你有socks节点就可以自定义添加。**



#### 3.运行run.py

在你的Windows/Linux系统下使用python3运行程序：

![image-20230515164753382](imgs/image-20230515164753382.png)



首次运行会读取节点并测试节点可用性，并会将可用的节点记录，等待下一次运行的时候可以直接调用可用节点：

![image-20230515165032157](imgs/image-20230515165032157.png)

等待测试完毕之后此时服务端就开启成功了：

![image-20230515171103341](imgs/image-20230515171103341.png)



**然后找到你自己的 公网/内网 IP地址，客户端使用socks5协议连接你服务端的 IP、端口、用户名、密码 即可**

这里以内网为例，我的服务端是192.168.31.226

![image-20230515165322694](imgs/image-20230515165322694.png)

### 客户端连接

客户端IP 192.168.31.225

#### 1.client.py测试连接可用性

找到 `Client-check/client.py` 文件，该文件作用是验证连接可用性。

```python
# -*- coding: utf-8 -*-
import requests
import socket
import socks
import os

print('Client 客户端测试代理连接脚本')

while 1:
    try:

        # 不存在密码就用这一条
        socks.set_default_proxy(socks.SOCKS5, "0.0.0.0", 12000)

        # 客户端存在密码用这一条
        ## socks.set_default_proxy(socks.SOCKS5, "0.0.0.0", 12000, username='aaa',password='bbb')
        
        socket.socket = socks.socksocket

        response = requests.get('https://ifconfig.me/',timeout=5).text
        
        print("测试成功 当前代理:",response)

    except KeyboardInterrupt:

        os._exit(0)
```

*注意要根据客户端账密是否配置 来选择注释代码的部分。

配置完成后，运行脚本：

```
python client.py
```



![image-20230515165842193](imgs/image-20230515165842193.png)

显示测试成功则代表客户端与服务端通信无误，这个时候你就可以将代理地址写入各个代理软件，开心耍了~

#### 2.服务端回显

此时服务端会显示连接信息：

![image-20230515170032093](imgs/image-20230515170032093.png)

同时会在 **Logs/Server_xxxx_xxxx.log** 记录服务端连接信息

![image-20230515170603642](imgs/image-20230515170603642.png)

## 0x05 常见工具代理配置



### Proxifier



#### 代理服务器配置



![image-20230515171813109](imgs/image-20230515171813109.png)

![image-20230515172006451](imgs/image-20230515172006451.png)



检查可用性：

![image-20230515172833070](imgs/image-20230515172833070.png)



这里测试设置中要记得勾去这一选项，不然会检验失败

这里其实也算是程序的一点缺陷，后续慢慢补全。

![image-20230515172818825](imgs/image-20230515172818825.png)

![image-20230515172755347](imgs/image-20230515172755347.png)

#### 规则设置

![image-20230515172153142](imgs/image-20230515172153142.png)

将想要使用代理的应用程序设置刚刚配置好的代理服务器即可

![image-20230515172112825](imgs/image-20230515172112825.png)



设置成这样就可以了，默认的localhost记得要勾上，不然会连不到 一个localhost 一个你想代理的应用。

![image-20230515172635381](imgs/image-20230515172635381.png)

#### 测试

访问ifconfig.m发现已经是代理IP了

![image-20230515172510772](imgs/image-20230515172510772.png)

![image-20230515172549015](imgs/image-20230515172549015.png)



### Firefox

PS: 代理工具不要同时开好几个，不然会出问题的

打开火狐浏览器，设置-代理中：

![image-20230515173109942](imgs/image-20230515173109942.png)



这里要关闭 **使用 SOCKS v5 时代理 DNS 查询** 这一选项，不然会连接不上。



![image-20230515173210822](imgs/image-20230515173210822.png)

![image-20230515173220545](imgs/image-20230515173220545.png)



### ProxyChains4

修改proxychains4.conf配置文件：

```
vim /etc/proxychains4.conf
```

在最后一行写入socks5代理地址

![image-20230515173714217](imgs/image-20230515173714217.png)



同时这里 strict_chain 要记得注释掉。

![image-20230515173733682](imgs/image-20230515173733682.png)



输入以下命令即可调用代理：

```
proxychains4 bash
curl https://ifconfig.me
```



### Python脚本调用代理

#### 方法一

在你的脚本添加这些代码：

```python
import socks

# 不存在密码就用这一条
socks.set_default_proxy(socks.SOCKS5, "0.0.0.0", 12000)

# 客户端存在密码用这一条
## socks.set_default_proxy(socks.SOCKS5, "0.0.0.0", 12000, username='aaa',password='bbb')
        
socket.socket = socks.socksocket
```

#### 方法二

使用requests库的时候可以设置proxies参数

```python
import requests

## 带有密码的情况
# 格式: socks5://usernm:passwd@IP:PORT
proxies = { 
	'http':'socks5://aaa:bbb@0.0.0.0:12000'
	'https':'socks5://aaa:bbb@0.0.0.0:12000'
}

## 无密码的情况
# 格式: socks5://IP:PORT
proxies = { 
	'http':'socks5://0.0.0.0:12000'
	'https':'socks5://0.0.0.0:12000'
}

print(requests.get('https://ifconfig.me/').text)
```



### Curl调用

```
curl -x "socks5://0.0.0.0:12000" https://ifconfig.me // 无密码
curl -x "socks5://aaa:bbb@0.0.0.0:12000" https://ifconfig.me // 存在密码
```



## 0x06 程序原理



服务端运行时，程序首先会获取node.txt里的socks节点并测试socks节点可用性，然后添加到一个列表里，暂且称之为代理池；

之后是一个随机取的操作，将代理池的代理随机取出，并添加到另一个新的列表代理池中，当代理池代理用完之后就会换用新的代理池，这样就实现了循环代理；

使用socks模块将取出的代理服务器进行代理，同时服务端调用 `server.py` ，该脚本文件就是一个简单的socks5代理服务器实现。

根据搭起的socks5通道，**将先前代理流量分配到这个通道中，就实现了以一个代理服务器来代理服务端和客户端之间的通信，那么这时候客户端得到的就是代理服务器的流量**

那么再循环代理池的任一代理服务器给服务端，客户端请求服务端，这时候就实现了服务端的多个代理流量变换，客户端也就得到了一个 **可任意更换代理频率的代理服务器流量**

![image-20230515182500896](imgs/image-20230515182500896.png)

![1](imgs/flow.png)



## 0x07 参考文章

`Server.py`部分参考了这位大佬写的socks5代理代码：https://github.com/dyboy2017/DYPROXY/

原理讲的很详细，测试过来有些地方有bug我自己稍加修改了。

其它的代码部分都是用头发换的（



## 0x08 尾声End

**第一次正式的提交Github项目，其实我本人还是喜欢开发的，只是比较懒不想传github XD，之后有空我会将更多的实用项目分享出来。如果你认可我的工具那么不妨点一个Star或者提交Issue，这些都是我前进的动力。**

**测试过来程序还是存在很多bug，包括我后续想添加vmess、Shadowsocks等节点，奈何有些知识点太薄弱网上相关的文章又少，导致这不是一个完整的项目，还需要慢慢改进修改。师傅们有什么想法可以提交issue交流下。**

**同时欢迎各位师傅们学习交流，如果你觉得有说的不对的地方请指出~ 希望能让这个工具更加完善，更加适用！**

