from socket import *
import threading
from config import *

class Server:
    def __init__(self, hostname, port):
        self.hostname   = hostname
        self.port       = port
        self.clients    = {}
        self.threads    = []
        self.keep_alive = True
        self.socket     = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(2.0)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((hostname, port))
        self.socket.listen(5)
        self.main_thread = threading.Thread(target=self.update, args=(lambda:self.keep_alive,))

    def sendMessage(self, author, message_raw, destiny=None):
        def send(message, destiny=None):
            if not destiny:
                for username, connection in list(self.clients.items()):
                    if username != author:
                        connection['conn'].send(message.encode())
            else:
                if destiny in self.clients:
                    self.clients[destiny]['conn'].send(message.encode())
                else:
                    error_message = build_message_text('SERVER', 'Chat', f'Ops, usuário {destiny} não encontrato...')
                    self.clients[author]['conn'].send(error_message.encode())

                
        if author == 'server':
            send(message_raw)
        elif message_raw.startswith(COMMANDS['LIST']):
            message_text =  f'{author} aqui está uma lista de todos os usuários disponíveis:'
            for username, connection in list(self.clients.items()):
                if username != author:
                    message_text += f"\n{build_message_text('SERVER', username, '')}"
            message = build_message_text('SERVER', 'Chat', message_text)
            send(message, author)
        elif message_raw.startswith(COMMANDS['QUIT']):
            message = build_message_text('SERVER', 'Chat', f'{author} está saindo do chat...')
            send(message)
            self.endConnection(author)
        elif message_raw.startswith(COMMANDS['PRIVATE']):
            message_split   = message_raw.split()
            action          = message_split.pop(0)
            destiny         = message_split.pop(0)
            message         = build_message_text('PRIVATE', author, " ".join(message_split))
            send(message, destiny)
        else:
            message         = build_message_text('GLOBAL', author, message_raw)
            send(message, destiny)

    def handleConnection(self, keep_alive, username):
        connection = self.clients[username]
        print(build_message_text('USER', username, f'Inicializando...'))
        while connection['keep_alive']:
            try:
                message = connection['conn'].recv(4026).decode()
                self.sendMessage(username, message)
            except timeout:
                pass
            except Exception as e:
                print(build_message_text('SERVER', 'ERROR', f'{username} - {e}'))
                print(build_message_text('SERVER', 'ERROR', f'Interrompendo conexão de {username}'))
                self.endConnection(username)
                break
        return

    def endConnection(self, username):
        try:
            print(build_message_text('SERVER', 'Chat', f'{username} - Desligando KeepAlive ...'))
            self.clients[username]['keep_alive'] = False
            print(build_message_text('SERVER', 'Chat', f'{username} - Unindo Thread...'))
            self.clients[username]['thread'].join()
            print(build_message_text('SERVER', 'Chat', f'{username} - Fechando conexão'))
            self.clients[username]['conn'].close()
            print(build_message_text('SERVER', 'Chat', f'{username} - Apagando dados'))
            del self.clients[username]['thread']
            del self.clients[username]['conn']
            del self.clients[username]
        except Exception as e:
            del self.clients[username]['thread']
            del self.clients[username]['conn']
            del self.clients[username]
            print(build_message_text('SERVER', 'ERROR', f'{username} - {e}'))


    def update(self, keep_alive):
        print(build_message_text('SERVER', 'Chat', f'Servidor aberto em {self.hostname}:{self.port}'))
        while keep_alive():
            try:
                connection, addr = self.socket.accept()

                message = build_message_text('SERVER', 'Chat', 'Digite seu apelido')
                connection.send(message.encode())
                username = connection.recv(1024).decode()
                while username in self.clients:
                    message = build_message_text('SERVER', 'Chat', 'Esse apelido já está sendo usado, tente outro')
                    connection.send(message.encode())
                    username = connection.recv(1024).decode()
                connection.settimeout(0.2)
                
                message = build_message_text('SERVER', 'Chat', 'Seja bem vindo! \n\tUtilize o comando /l para listar os usuários onlines \n\tUtilize o comando /p para mandar mensagens privadas \n\t Utilize o comando /r responder a última mensagem privada recebida \n\t Utilize o comado /q para sair')
                connection.send(message.encode())

                self.clients[username] = {
                    'conn':         connection,
                    'username':     username,
                    'thread':       {},
                    'keep_alive':   True
                }
                print(build_message_text('USER', username, f'Entrou no chat'))
                self.sendMessage('server', build_message_text('USER', username, 'entrou no bate-papo'))
                
                self.clients[username]['thread'] = threading.Thread(target=self.handleConnection, args=(lambda:self.clients[username]['keep_alive'], username))
                self.clients[username]['thread'].start()
            except timeout:
                pass
            except Exception as e:
                print(build_message_text('SERVER', 'ERROR', f'{e}'))
        return
    
    def start(self):
        print(build_message_text('SERVER', 'Chat', 'Inicializando servidor...'))
        self.main_thread.start()
        print(build_message_text('SERVER', 'Chat', 'Pressione qualquer tecla para parar a execução...'))
        input()
        print(build_message_text('SERVER', 'Chat', 'Parando thread principal...'))
        self.keep_alive = False
        self.main_thread.join()
        for username, connection in list(self.clients.items()):
            self.endConnection(username)
        print(build_message_text('SERVER', 'Chat', 'Saindo...'))

server = Server(SERVER_HOST, SERVER_PORT)
server.start()