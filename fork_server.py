from socket import * 
import os,sys 
import signal 


# 客户端处理函数：收发消息
def client_handler(c):
    print("处理子进程的请求",c.getpeername())  # 获取客户端连接套接字的对应地址？？
    try:
        while True:
            data = c.recv(1024).decode()
            if not data:
                break 
            print(data.decode())
            c.send("收到客户端请求".encode())
    except (KeyboardInterrupt,SystemExit):
        sys.exit("退出进程")
    except Exception as e:
        print(e)  
		c.close()  # 
    c.close()
    sys.exit(0) #子进程关闭 ！！！

#创建套接字
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)


#在父进程中忽略子进程状态改变，子进程退出自动由系统处理（处理僵尸进程）
signal.signal(signal.SIGCHLD,signal.SIG_IGN)  # 子进程状态改变时，会发送给父进程

# 等待接收客户端请求，并未客户端创建子进程与之相对应
while True:
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:  #服务器一般不会退出，人为退出会异常，此行为是为了让更优雅的退出
        s.close()
        sys.exit("服务器退出")
    except Exception as e:
        print('error:', e)
        continue  # 如果其他异常继续等待客户端连接
		
    #为客户端创建新的进程，处理请求
    pid = os.fork()

    if pid == 0: # 子进程处理具体请求
        s.close()   # 在子进程中关闭服务端套接字s,因为里面用不到了，防止误操作
        #处理客户端请求
        client_handler(c)  # c对于子进程是全局变量，可不传，如想为别人提供函数接口，保险起见
		
	# 父进程或者创建失败都继续等待下个客户端连接
    else:            
        c.close()  # 在父进程中关闭服务端套接字c
        continue 

