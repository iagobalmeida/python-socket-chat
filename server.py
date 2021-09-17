from socket import *
import threading
from config import *

class Server:
    def __init__(self, hostname, port):
        self.clients    = {}
        self.keep_alive = True
        self.socket     = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((hostname, port))
        self.socket.listen(5)

    def sendMessage(self, author, message_raw, destiny=None):
        def send(message, destiny=None):
            if not destiny:
                for username, connection in list(self.clients.items()):
                    if username != author:
                        connection.send(message.encode())
            else:
                print(destiny)
                print(self.clients)
                if destiny in self.clients:
                    self.clients[destiny].send(message.encode())
                else:
                    self.clients[author].send(f'{bcolors.WARNING}Ops, usuário {destiny} não encontrado...{bcolors.ENDC}'.encode())

                
        if author == 'server':
            send(message_raw)
        elif message_raw.startswith(COMMANDS['QUIT']):
            print(f'> {username} quer sair do chat...')
        elif message_raw.startswith(COMMANDS['PRIVATE']):
            message_split   = message_raw.split()
            action          = message_split.pop(0)
            destiny         = message_split.pop(0)
            message         = f'{bcolors.BOLD}📧\t{author} | {bcolors.ENDC} {" ".join(message_split)}'
            send(message, destiny)
        else:
            message = f'{bcolors.OKBLUE}🌎\t{author} | {bcolors.ENDC} {message_raw}'
            send(message, destiny)



    def handleConnection(self, connection):
        connection.send('Digite seu apelido: '.encode())
        username = connection.recv(1024).decode()
        while username in self.clients:
            connection.send('Esse apelido já está sendo usado, tente outro: '.encode())
            username = connection.recv(1024).decode()
        print(f'> {username} entrou no chat')
        self.clients[username] = connection
        self.sendMessage('server', f'👤\t{username} | entrou no bate-papo')
        while True:
            message = connection.recv(4026).decode()
            self.sendMessage(username, message)
    
    def start(self):
        print('Starting server...')
        while self.keep_alive:
            try:
                connection, addr = self.socket.accept()
                thread = threading.Thread(target=self.handleConnection, args=(connection,))
                thread.start()
            except e:
                print('ERROR', e)
        print('Ending...')


server = Server(SERVER_HOST, SERVER_PORT)
server.start()
