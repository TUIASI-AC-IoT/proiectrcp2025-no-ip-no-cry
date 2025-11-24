#importarea modulelor necesare
import socket
import select
import tkinter as tk

# configurarea adreselor/porturilot agentilor (localhost)
AGENT_1_ADDR = ('127.0.0.1', 12345)
AGENT_2_ADDR = ('127.0.0.1', 12346)

#crearea socket-ului UDP pentru manager
manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
manager_socket.bind(('0.0.0.0', 0)) 
manager_socket.setblocking(False) 
# manager_socket.setblocking(True) ar putea fi o alternativa mai buna pentru asteptarea infinita in lipsa lui select

print(f"Managerul asculta pe portul local: {manager_socket.getsockname()[1]}") 

# cereri catre agenti
requests = {
    AGENT_1_ADDR: b"GET /cpuTemp/ Agent 1",        # Cerere de Temperatura
    AGENT_2_ADDR: b"GET /sysUpTime/ Agent 2"       # Cerere de Uptime
}

#transmiterea cererilor catre agenti
for addr, payload in requests.items():
    print(f"\n[SEND] Trimit cererea catre {addr}: {payload.decode()}")
    manager_socket.sendto(payload, addr)

#asteptarea raspunsurilor cu select
responses_received = 0
expected_responses = len(requests)

print(f"\nAstept raspunsuri de la cei {expected_responses} agenti (se va astepta indefinit)...\n")

try:
    while responses_received < expected_responses:
        
        # Timeout-ul a fost ELIMINAT (al 4-lea argument este None)
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