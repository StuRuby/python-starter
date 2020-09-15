# 导入模块
import socket
# 创建tcp服务端socket
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口
tcp_server_socket.bind(("", 8095))
# 设置监听，把服务端socket由主动套接字改成被动套接字，只能接收客户端的连接请求
tcp_server_socket.listen(128)
while True:
    # 接收客户端信息
    client_socket, client_ip = tcp_server_socket.accept()
    print("客户端：", client_ip, "连接")
    # 接收下载信息
    #file_name_data = client_socket.recv(1024)
    # 解码下载信息
    #file_name = file_name_data.decode()
    file_name = "audio01.wav"

    # 服务端接收文件
    try:
        # 文件传输
        with open("C:/Users/MI/Desktop/" + file_name, "wb") as file:
            while True:
                # 接收数据
                file_data = client_socket.recv(1024)
                # 数据长度不为0写入文件
                if file_data:
                    file.write(file_data)
                # 数据长度为0表示下载完成
                else:
                    break
    # 下载出现异常时捕获异常
    except Exception as e:
        print("接收异常", e)
    # 无异常则下载成功
    else:
        print(file_name, "接收成功")

# 服务端发送文件
'''
    try:
        # 数据传输
        with open("/home/zeno/文档/" + file_name, "rb") as file:
            while True:
                # 读取文件数据
                file_data = file.read(1024)
                # 数据长度不为0表示还有数据没有写入
                if file_data:
                    client_socket.send(file_data)
                # 数据为0表示传输完成
                else:
                    print(file_name, "传输成功")
                    break
    except Exception as e:
        print("传输异常：", e)
'''

# 关闭客户端连接
client_socket.close()
