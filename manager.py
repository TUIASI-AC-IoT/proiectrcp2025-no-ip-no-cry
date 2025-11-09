#importarea modulelor necesare
import socket
import select

#configurarea adreselor agentilor pe localhost
AGENT_1_ADDR = ('127.0.0.1', 12345)
AGENT_2_ADDR = ('127.0.0.1', 12346)

#crearea socket-ului UDP pentru manager
manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#legarea socket-ului la o adresa locala
manager_socket.bind(('0.0.0.0', 0))         # OS-ul alege un port liber automat
manager_socket.setblocking(False)           # asigura simultanietatea procesarii

#afisarea portului local al managerului
print(f"Managerul ascultă pe portul local: {manager_socket.getsockname()[1]}") 

#cererile catre agenti
requests = {
    AGENT_1_ADDR: b"GET /sysDescr/ Agent 1",        #b - reprezinta un sir de bytes
    AGENT_2_ADDR: b"GET /sysUpTime/ Agent 2"
}

#transmiterea cererilor catre agenti
for addr, payload in requests.items():
    print(f"\n[SEND] Trimit cererea catre {addr}: {payload.decode()}")
    manager_socket.sendto(payload, addr)

#asteptarea raspunsurilor cu select
timeout = 5.0 # Asteapta raspunsuri timp de 5 secunde
responses_received = 0
expected_responses = len(requests)

print(f"\n[SELECT] Aștept răspunsuri de la cei {expected_responses} Agenți (timeout: {timeout}s)...")

try:
    #cat timp nu am primit toate raspunsurile asteptate
    while responses_received < expected_responses:
        

        #selecteaza socket-urile pregatite pentru citire
        ready_to_read, _, _ = select.select([manager_socket], [], [], timeout)      # _ - variabile neutilizate
        
        #daca socket-ul managerului este pregatit pentru citire
        if manager_socket in ready_to_read:

            #primeste datele si adresa sursa
            data, addr = manager_socket.recvfrom(1024)

            #afisarea raspunsului primit
            print(f"--- [RECV] Răspuns primit de la {addr} ---")
            print(f"Răspuns: {data.decode()}")

            #contorizarea raspunsurilor primite
            responses_received += 1

        else:
            #daca s-a atins timeout-ul, iesim din bucla
            print("\nTimeout: Nu s-au primit toate răspunsurile la timp.")
            break

#exceptia pentru oprirea managerului cu Ctrl+C
except KeyboardInterrupt:
    print("\nManagerul oprit de utilizator.")

#inchiderea socket-ului managerului
manager_socket.close()
print("Managerul s-a închis.")