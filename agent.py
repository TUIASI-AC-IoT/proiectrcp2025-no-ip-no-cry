# import socket

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('127.0.0.1', 12345))

# server_socket.listen(5)

# while True:
#     print("Waiting for a connection...")
#     client_socket, addr = server_socket.accept()
#     print(f"Connection from %s has been established!" % str(addr))

#     while True:
#         data = client_socket.recv(1024)
#         if not data or data .decode('utf-8') == 'END':
#             break
#         print("Received:", data.decode('utf-8'))
        
#         try:
#             client_socket.send(bytes("Hey client", 'utf-8'))
#         except:
#             print("Exit by user")
#     client_socket.close()
# server_socket.close()

import socket

agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agent_socket.connect(('127.0.0.1', 12345))

payload = 'Hey Server'

try:
    while True:
        agent_socket.send(payload.encode('utf-8'))
        data = agent_socket.recv(1024)
        print(str(data))

        more = input('Wnat to send more data? (y/n): ')
        if more.lower() == 'y':
            payload = input('Enter data to send: ')
        else:
            break

except KeyboardInterrupt:
    print("Exit by user")

agent_socket.close()

