#importarea modulelor necesare
import socket
import sys

#verificarea argumentelor din linia de comanda
if len(sys.argv) < 2:
    print("EROARE: Compilare incorecta! (ex: python agent.py 12345)")
    sys.exit(1)

try:
    AGENT_PORT = int(sys.argv[1])
except ValueError:
    print("EROARE: Numar invalid. (ex: python agent.py 12345)")
    sys.exit(1)

#configurarea adresei agentului
if(sys.argv[1] == '12345'):
    AGENT_ADDR = ('192.168.95.233', AGENT_PORT)
else:
    AGENT_ADDR = ('192.168.60.49', AGENT_PORT)

#crearea socket-ului UDP pentru agent
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#setarea timpului de expirare pentru recvfrom
agent_socket.settimeout(5.0)  #timeout de 5 secunde  

#legarea socket-ului la adresa agentului
try:
    agent_socket.bind(('0.0.0.0', AGENT_PORT))
except OSError as e:
    print(f"EROARE: Nu pot lega socket-ul pe portul {AGENT_PORT}.\nMotiv: {e}")
    sys.exit(1)


print(f"Agentul asculta pe UDP {AGENT_ADDR}...")

try:
    while True:
        try:
            #primirea cererii de la manager
            data, manager_addr = agent_socket.recvfrom(1024)
            
            #afisarea cererii primite
            request_msg = data.decode()
            print(f"\n[RECV] Cerere de la Manager ({manager_addr}): {request_msg}")

            #pregatirea raspunsului in functie de cerere
            if "Agent 1" in request_msg:
                response_data = b"Response: System Description - Port 12345 OK"
            elif "Agent 2" in request_msg:
                response_data = b"Response: System UpTime - Port 12346 OK"
            else:
                response_data = b"Response: Unknown Request"

            #trimiterea raspunsului catre manager
            agent_socket.sendto(response_data, manager_addr)
            print(f"[SEND] Răspuns trimis către Manager.")
            
        except socket.timeout:
            #daca nu s-au primit cereri in timpul de asteptare
            pass

#exceptia pentru oprirea agentului cu Ctrl+C
except KeyboardInterrupt:
    print("\nAgentul oprit.")
    
#inchiderea socket-ului agentului
agent_socket.close()