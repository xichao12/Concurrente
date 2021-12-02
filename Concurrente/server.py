import socket
import threading

host = '127.0.0.1'
port = 55555

historial = [] #Guardamos el historial de los mensajes


# Vamos a utilizar un socket tipo internet y el protocolo tcp
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port))
server.listen()
print(f"Server running on {host}:{port}")

# Creamos listas
clients = [] #almacenamos las conexiones de los clientes
usernames = [] #almacenamos los  usernames de los clientes

#Envia un mensaje a todos los clientes
def broadcast(message,_client):
    for client in clients: 
        if client != _client:
            client.send(message)

#Funcion manejar los mensajes de cada cliente
def handle_messages(client):
    while True:
        try:
            message = client.recv(1024) #peso maximo que puede recibir la funcion en bytes
            broadcast(message,client)

            # Guardamos el historial de mensajes
            historial.append(message)
            with open("u22015640Al1.txt", "w") as output:
                output.write(str(historial))

        except:
            #Obtenemos el username del usuario que se desconecta
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'))
            clients.remove(client)
            username.remove(username)
            client.close #Cerramos conexion del cliente

#Funcion que acepta las conexiones de los clientes
def receive_connection():
    while True:
        client,address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        #mensaje anunciante de usuario conectado
        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message,client)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages,args=(client,))
        thread.start()

receive_connection()
    
