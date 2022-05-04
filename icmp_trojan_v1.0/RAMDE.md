# RAMDE
## 介绍
这是我的第一个 icmp 木马版本，主要使用了 socket 来进行编写，数据传输使用的是 AES-ECB-128 加密，该木马的通讯利用了 icmp 数据包后面的 data 数据部分来传递载荷。

参考资料：https://www.bbsmax.com/A/KE5QjaE4dL/



## 注意
##### **本工具仅用于学习研究，不要使用此工具来从事非法攻击行为，由此产生的一切后果均由使用者承担，本人不对此负责！**
##### **本工具仅用于学习研究，不要使用此工具来从事非法攻击行为，由此产生的一切后果均由使用者承担，本人不对此负责！**
##### **本工具仅用于学习研究，不要使用此工具来从事非法攻击行为，由此产生的一切后果均由使用者承担，本人不对此负责！**


## 使用介绍


##### 必须满足以下条件
1、目标机器可以正常被 ping 通

2、木马的运行权限 Windows为 Administrator ，Linux为 root

3、目前客户端仅支持Linux，所以客户端运行环境要为Linux，最好是使用 kali



##### 首先安装依赖
```bash
pip/pip3 install -r requirements.txt
```
##### 如果需要打包编译木马请使用 packtrojan.py ，并确保在打包之前已经确定 settings.py 文件的信息已经填写正确
```bash
python3/python packtrojan.py
```
##### 使用客户端连接木马，在连接之前请确保 settings.py 文件的信息已经正确，AES 验证密钥一定要确保正确。如果下达命令后控制台一直卡住则可能无法与木马建立通信。
```bash
python3 client.py 目标IP地址
```
