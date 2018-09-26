from socket import *
import os 
import signal 
import sys 
import time 

#文件库
FILE_PATH = "/home/tarena/"

#实现功能模块
class TftpServer(object):
    pass 

#流程控制，创建套接字，创建并发，方法调用
def main():
    HOST = '0.0.0.0'
    PORT = 8888
    ADDR = (HOST,PORT)

    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try: 
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        print("客户端登录:",addr)

        #创建父子进程
        pid = os.fork()

        if pid == 0:
            sockfd.close()
            tftp = TftpServer()  # __init__传参
            while True:
                data = connfd.recv(1024).decode()
                if data == "list":
                    tftp.do_list()
                elif data == 'get':
                    tftp.do_get()
                elif data == 'put':
                    tftp.do_put()
                elif data == 'quit':
                    print("客户端退出")
                    sys.exit(0)
        else:
            connfd.close()
            continue

if __name__ == "__main__":
    main()
