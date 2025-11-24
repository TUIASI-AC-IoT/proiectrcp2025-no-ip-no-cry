#importarea modulelor necesare
import socket
import select

# configurarea adreselor/porturilot agentilor (localhost)
AGENT_1_ADDR = ('10.107.11.160', 12345)         #laptop felicia
AGENT_2_ADDR = ('10.107.11.199', 12346)         #laptop georgiana

#crearea socket-ului UDP pentru manager
manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
manager_socket.bind(('10.107.11.0', 0))
manager_socket.setblocking(False) 

print(f"Managerul asculta pe portul local: {manager_socket.getsockname()[1]}") 

# cereri catre agenti
requests = {
    AGENT_1_ADDR: b"GET /cpuTemp/ Agent 1",        # Cerere de Temperatura
    AGENT_2_ADDR: b"GET /cpuLoad/ Agent 2"       # Cerere de CPU Load
}

#transmiterea cererilor catre agenti
for addr, payload in requests.items():
    print(f"\nTrimit cererea catre {addr}: {payload.decode()}")
    manager_socket.sendto(payload, addr)

#asteptarea raspunsurilor cu select
responses_received = 0
expected_responses = len(requests)

print(f"\nAstept raspunsuri de la cei {expected_responses} agenti...\n")

try:
    while responses_received < expected_responses:
        
        ready_to_read, _, _ = select.select([manager_socket], [], [], None) 
        
        if manager_socket in ready_to_read:

            data, addr = manager_socket.recvfrom(1024)

            # raspunsul primit de la agent
            response_msg = data.decode()
            
            print(f"--- [RECV] Raspuns primit de la {addr} ---")
            
            if addr == AGENT_1_ADDR and "CPU Temperature" in response_msg:
                print(f"Temperatura agentului 1: {response_msg.split('=')[-1].strip()}")
            elif addr == AGENT_2_ADDR:
                print(f"CPU Load-ul agentului 2: {response_msg.split('=')[-1].strip()}")
            else:
                print(f"Raspuns: {response_msg}")

            responses_received += 1

except KeyboardInterrupt:
    print("\nManagerul oprit de utilizator.")

manager_socket.close()
print("Managerul s-a inchis.")