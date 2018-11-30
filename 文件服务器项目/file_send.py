# file_send.py

from socket import *
from time import sleep
import sys

# 基本文件操作功能


class FtpClient(object):
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')  # 发送请求

        # 等待回复

        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
            print('文件列表展示完毕\n')
        else:
            # 服务器请求失败原因
            print(data)

    def do_get(self, filename):
        self.sockfd.send(('G ' + filename).encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            fd = open(filename, 'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
            print('%s 下载完毕' % filename)

        else:
            print(data)

    def upload_file(self, filename):
        try:
            fd = open(filename, 'rb')
        except:
            print('文件打开失败')
            return
        self.sockfd.send(('C ' + filename).encode())
        data = self.sockfd.recv(1024).decode()

        if data == 'OK':

            sleep(0.1)
            while True:
                data = fd.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            print('上传完毕')
            fd.close()
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
# 网络连接


def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)  # 文件服务器地址

    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except:
        print('连接服务器失败')
        return
    ftp = FtpClient(sockfd)  # 功能类对象
    while True:
        print('*********************************')
        print('1:查看服务端文件库中所有文件')
        print('2:下载文件库的文件到本地')
        print('3:将本地文件上传到服务端文件库')
        print('4:退出')
        print('*********************************')

        cmd = input('请输入命令>>>')
        if cmd.strip() == '1':
            ftp.do_list()
        elif cmd[0] == '2':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[0] == '3':
            filename = cmd.split(' ')[-1]
            ftp.upload_file(filename)
        elif cmd.strip() == '4':
            ftp.do_quit()
            sockfd.close()
            sys.exit('谢谢使用')
        else:
            print('请输入正确命令')


if __name__ == '__main__':
    main()
