from socket import *
import threading
from config import *
from prompt_toolkit import prompt

class Client:
    def __init__(self, hostname, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((hostname, port))
        self.socket.settimeout(0.2)
        self.running     = True
        self.keep_alive  = True
        self.main_thread = threading.Thread(target=self.listen, args=(lambda:self.keep_alive, ))
        self.main_thread.start()
        self.last_private = ''
        while self.running:
            try:
                entry = prompt()

                if (not self.running):
                    print(build_message_text('SERVER', 'Chat', 'Falha ao enviar mensagem. Chat finalizado'))
                    raise Exception('')

                if(entry.startswith('/q')):
                    self.socket.send('/q'.encode())
                    self.socket.close()
                    self.keep_alive = False
                    self.running = False
                if(entry.startswith('/r')):
                    if len(self.last_private) >= 1:
                        entry_split = entry.split(' ')
                        action      = entry_split.pop(0)
                        entry_split.insert(0, f'/p {self.last_private}')
                        self.socket.send((' '.join(entry_split)).encode())
                    else:
                        print(build_message_text('SERVER', 'Chat', 'Nenhuma mensagem para responder'))
                else:
                    self.socket.send(entry.encode())
            except timeout:
                pass
            except Exception as e:
                self.socket.close()
                self.keep_alive = False
                self.running = False
                break

    def listen(self, keep_alive):
        while self.keep_alive:
            try:
                entry = self.socket.recv(4096).decode()

                if (len(entry) == 0):
                    print(build_message_text('SERVER', 'Chat', 'Chat finalizado'))
                    raise Exception('')

                if(entry.find('????') >= 0):
                    split_entry = entry.split(' ')
                    self.last_private = split_entry[7]
                print(f'\b{entry}')
            except error:
                pass
            except timeout:
                pass
            except Exception as e:
                self.socket.close()
                break

        self.keep_alive = False
        self.running = False

        return
            
try:
    client = Client(SERVER_HOST, SERVER_PORT)
except Exception as e:
    print(build_message_text('SERVER', 'Chat', f'{e}'))