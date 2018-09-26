from socket import *
import sys 
import time 

#实现各种功能请求
class TftpClient(object):
    pass 

#创建套接字建立连接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    sockfd = socket()
    sockfd.connect(ADDR)

    tftp = TftpClient()   #__init__是否需要传参

    while True:
        print("打印界面")

        cmd = input("输入命令>>")

        if cmd == "list":
            tftp.do_list()


if __name__ == "__main__":
    main()