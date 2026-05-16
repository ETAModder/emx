import socket
import hashlib

print('WELCOME TO THE EMX SERVER-HOST 3000')

def hash_message(message, key):
    return hashlib.sha256((message + key).encode()).hexdigest()

def server_program():
    host = '127.0.0.1' 
    port = int(input("Enter the port number to host the server on: "))

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print('Connection from: ' + str(address))

    key = input("Set a key for this session: ")
    conn.send(key.encode())

    received_key = conn.recv(1024).decode()
    if received_key == key:
        print("Client authenticated successfully.")
    else:
        print("Authentication failed.")
        conn.close()
        return

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        original_message = data.split(':')[0]
        received_hash = data.split(':')[1]
        computed_hash = hash_message(original_message, key)

        if received_hash == computed_hash:
            print('Received from client: ' + original_message)
        else:
            print('Message integrity check failed!')

        message = input('Reply to client: ')
        message_hash = hash_message(message, key)
        conn.send((message + ':' + message_hash).encode())

    conn.close()

if __name__ == '__main__':
    server_program()
