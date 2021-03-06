# python-socket-chat

## ✨ Motivação
Trabalho desenvolvido na disciplina de Sistemas Distribuídos como pré-requisito para aprovação na mesma

## 🔎 Definição do problema
Desenvolvimento de um chat que possui comunicação privada, em grupos e com todos conectados. Esse chat deveria ser desenvolvido sem a utilização de ferramentas de controle de socket e threads já existentes.

## ⚙️ Arquitetura
A aplicação é constituída de duas classes, uma delas é o Client, responsável por receber informações do usuário e também exibir as informações vindas do servidor e a outra é o Server, responsável por gerenciar as conexões em TCP de todos os Clients, assim como as mensagens que são enviadas aos Clients, sejam elas mensagens do próprio servidor ou  mensagens enviadas por outros usuários.

Além dessas duas classes, a aplicação conta com um arquivo adicional chamado config.py que fornece funções auxiliares e valores constantes, que são utilizados pelas duas classes principais.

Cada classe possui uma Thread principal, cuja função é ouvir as possíveis mensagens vindas da conexão servidor-cliente. No caso do Server, existe ainda um conjunto de Threads responsáveis por gerenciar as mensagens dos usuários, que são criadas quando um  novo usuário se conecta e fornece um nome de usuário. 

## ⛓️ Regras de aplicação
Para a inicialização do chat por um cliente, ele deve obrigatoriamente inserir um username. Esse username deve ser único no chat entre todos os clientes conectados.

O chat fornece o uso de comandos através de prefixos, que podem ser digitados pelo usuário na entrada da mensagem. Os comandos disponíveis são:

    /g ou ‘’ <mensagem> - Envia uma mensagem no chat global;
    /p <username> <mensagem> - Envia uma mensagem privada para o usuário;
    /r  <mensagem> - Responde a última mensagem privada recebida;
    /l - Lista todos os usuários conectados.


## 🧪 Como rodar
É necessário instalar a biblioteca prompt_toolkit através do pip.

    pip install prompt_toolkit

Para rodar o servidor basta digitar no terminal:

    python3 server.py
    ou
    python server.py

Para parar o servidor aperte enter no terminal e espere o cliente finalizar.

Para rodar o cliente basta digitar no terminal:

    python3 client.py
    ou
    python client.py

Para parar o cliente utilize o comando \q e espere o cliente finalizar.
