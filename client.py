import socket
import psutil
import json
import time

def create_client(host, port):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # connect to server on local computer
        s.connect((host,port))
        print("ok")
        while True:
            dictionary = {}
            dictionary['cpu_percent'] = psutil.cpu_percent(4)
            dictionary['disk_usage'] = psutil.disk_usage('/').percent
            dictionary['ram_percent'] = psutil.virtual_memory().percent
            dictionary['sensors_battery'] = psutil.sensors_battery().percent
            # message sent to server
            s.send(json.dumps(dictionary).encode('ascii'))
            # message received from server
            data = s.recv(1024)
            # print the received message
            # here it would be a reverse of sent message
            print('Received from the server :',str(data.decode('ascii')))
            # sleep for 2 seconds
            time.sleep(2)
    except Exception as e:                
        print(e)
        s.close()
        # ask the client whether he wants to continue
        ans = input('\nconnection failed! Do you want to continue(y/n)?! :')
        if ans == 'y' or ans == 'Y':
            create_client('localhost', 8081)

if __name__ == "__main__":
    create_client('localhost', 8081)