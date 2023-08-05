# -*- coding: utf-8 -*-
import uuid
import socket
import os


def ping(config_file_path, save_ping_result_to_file):
    """
    在当前执行机器上Ping 定义在config_file_path文件中的目标机器，并将结果写入save_ping_result_to_file指定的文件中
    :param config_file_path: 待测试的机器列表的文件
    :param save_ping_result_to_file: 保存Ping之后的结果
    :return:
    """
    of = open(config_file_path, 'r')
    ofw = open(save_ping_result_to_file, 'a')
    for f in of:
        server = f.split(',')[0]
        print server
        ping_result = os.popen('ping %s -c 1' % server).readlines()
        # convert list to string
        ping_result_s = ''.join(ping_result)
        # find string "Destination Host Unreachable"
        if ping_result_s.find('Destination Host Unreachable') <> -1:
            print '%s is not reached' % server
        else:
            print '%s is reached' % server
            ofw.write('%s is reached\n' % server)
    of.close()
    ofw.close()


def telnet_port(server_ip, port):
    """
    检查远端服务器端口是否打开
    :param server_ip: Server IP
    :param port: 待检查的端口号
    :return:
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)  # 设置超时时间
    try:
        sk.connect((server_ip, port))
        print 'OK!'
    except Exception:
        print 'Telnet Failed'
    sk.close()


def get_mac_address():
    """
    取得本机的MAC地址
    :return:
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def get_ip_address():
    """
    获取本机ip(含公网IP和本地IP)
    :return:
    """
    ip_address = socket.gethostbyname_ex(get_machine_name())
    return ip_address


def get_machine_name():
    """
    获取本机电脑名
    :return:
    """
    machine_name = socket.getfqdn(socket.gethostname())
    return machine_name


def ip2int(ip_address_string):
    result = 0
    ip_address_string = ip_address_string.split('.')

    for i in range(4):
        result += int(ip_address_string[i]) * (256 ** (3 - i))
    return result


def int2ip(number):
    xin = []
    for i in range(3):
        number, modum = divmod(number, 256)
        xin.insert(0, str(modum))
    xin.insert(0, str(number))
    return '.'.join(xin)


def test():
    ipadd = input('Enter an ip address:')
    print(ip2int(ipadd))
    number = int(input('Enter a number:'))
    print(int2ip(number))


def main():
    print get_ip_address()
    print get_mac_address()


if __name__ == '__main__':
    main()
    test()
