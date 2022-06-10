import socket
import json
import threading
from _thread import *
from prometheus_client import Gauge, start_http_server

def server(ip, port):
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind((ip, port))
    mysocket.listen(2)
    start_http_server(8080)
    print("ok")
    return mysocket

def accept(socket):
    connection, c_ip = socket.accept()
    return connection, c_ip

def read_message(connection):
    while True:
        data = connection[0].recv(1024)
        data = json.loads(data)
        print(data, "     ", connection[1])
        if not data:
            print("no data!!!")
            # print_lock.release()
            break
        # print(data)
        ram_metric.labels(f'agant{str(connection[1])}').set(data['ram_percent'])
        cpu_metric.labels(f'agant{connection[1]}').set(data['cpu_percent'])
        disk_metric.labels(f'agant{connection[1]}').set(data['disk_usage'])
        battery_metric.labels(f'agant{connection[1]}').set(data['sensors_battery'])
        connection[0].send("data received".encode('ascii'))
    connection[0].close()
 

if __name__ == '__main__':
    print_lock = threading.Lock()
    clientNum = 0
    ram_metric = Gauge('ram_usage_percent', 'usage of my ram',['agent_number'])
    cpu_metric = Gauge('cpu_usage_percent', 'usage of my cpu in 4 seconds',['agent_number'])
    battery_metric = Gauge('battery_capacity', 'usage of my ram in current proccess',['agent_number'])
    disk_metric = Gauge('disk_usage', 'usage of my disk in current proccess',['agent_number'])
    myServer = server('localhost', 8081)
    while True:
        connection, c_ip = accept(myServer)
        clientNum += 1
        connection = [connection, clientNum]
        # print_lock.acquire()
        start_new_thread(read_message, (connection,))
