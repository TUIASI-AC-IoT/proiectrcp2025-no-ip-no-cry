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

