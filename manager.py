#importarea modulelor necesare
import socket
import select

# configurarea adreselor/porturilot agentilor (localhost)
AGENT_1_ADDR = ('10.107.11.160', 161)         #laptop felicia
AGENT_2_ADDR = ('10.107.11.199', 161)         #laptop georgiana

## GEO
TRAP_PORT = 162

#crearea socket-ului UDP pentru manager
manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
manager_socket.bind(('0.0.0.0', 0))
manager_socket.setblocking(False)

## GEO
## socket pentru Traps
trap_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
trap_socket.bind(('0.0.0.0', TRAP_PORT))
trap_socket.setblocking(False)
print(f"Managerul asculta TRAP-urile pe portul {TRAP_PORT}")



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


while True:
    try:
        ready_to_read, _, _ = select.select(
            [manager_socket, trap_socket],
            [], [], None
        )

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

        # ---- TRAP-URI receptionate -----(Geo)
        if trap_socket in ready_to_read:
            trap_data, trap_addr = trap_socket.recvfrom(1024)
            print("\n [TRAP PRIMIT]")
            print(f"De la agent: {trap_addr}")
            print(trap_data.decode())

    except KeyboardInterrupt:
        print("\nManagerul oprit de utilizator.")
        manager_socket.close()
        trap_socket.close()
        print("Managerul s-a inchis.")
        break
