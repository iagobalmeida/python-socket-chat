from socket import *
import threading
from config import *

class Client:
    def __init__(self, hostname, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((hostname, port))
        self.main_thread = threading.Thread(target=self.listen)
        self.main_thread.start()
        self.last_private = ''
        while True:
            entry = input()
            if(entry.startswith('/r')):
                if len(self.last_private) >= 1:
                    entry_split = entry.split(' ')
                    action = entry_split.pop(0)
                    entry_split.insert(0, f'/p {self.last_private}')
                    self.socket.send((' '.join(entry_split)).encode())
                else:
                    print('Nenhuma mensagem para responder')
            else:
                self.socket.send(entry.encode())

    def listen(self):
        while True:
            entry = self.socket.recv(4096).decode()
            if(entry.startswith('📧')):
                self.last_private = entry.split(' ')[2].replace(':', '')
            print(entry)
            
client = Client(SERVER_HOST, SERVER_PORT)
