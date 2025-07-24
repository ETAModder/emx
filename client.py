import socket
import hashlib

print('WELCOME TO THE EMX CLIENT')

def hash_message(message, key):
    return hashlib.sha256((message + key).encode()).hexdigest()

def client_program():
    host = input("Enter the server IP address to connect to: ")
    port = int(input("Enter the port number to connect to: "))

    client_socket = socket.socket()
    client_socket.connect((host, port))

    key = client_socket.recv(1024).decode()
    print("Received key from server:", key)

    input_key = input("Enter the key to authenticate: ")
    client_socket.send(input_key.encode())

    if input_key != key:
        print("Authentication failed.")
        client_socket.close()
        return

    message = input("Enter message: ")
    while message.lower().strip() != 'bye':
        message_hash = hash_message(message, key)
        client_socket.send((message + ':' + message_hash).encode())

        data = client_socket.recv(1024).decode()
        original_message = data.split(':')[0]
        received_hash = data.split(':')[1]
        computed_hash = hash_message(original_message, key)

        if received_hash == computed_hash:
            print('Received from server: ' + original_message)
        else:
            print('Message integrity check failed!')

        message = input("Enter message: ")

    client_socket.close()

if __name__ == '__main__':
    client_program()
