import socket

def main():
    host = "0.0.0.0"
    port = 8000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print("Server listening on port", port)
    
    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)
        
        with open("received_file.txt", "wb") as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                
        print("File received successfully")
        client_socket.close()

if __name__ == "__main__":
    main()
