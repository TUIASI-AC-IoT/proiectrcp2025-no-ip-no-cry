#importarea modulelor necesare
import socket
import sys
import wmi


# functia pentru obtinerea temperaturii CPU folosind WMI
def get_cpu_temp_wmi():
    try:
        # conectarea la WMI
        w = wmi.WMI(namespace="root\\wmi")
        
        # obtinerea temperaturii CPU
        temperatures = w.MSAcpi_ThermalZoneTemperature()

        if not temperatures:
             print("Eroare la citirea temperaturii CPU.")
             return
        
        print("Temperaturile citite :")
        # convertirea temperaturii din Kelvin*10 in Celsius
        for temp in temperatures:
            temp_k = temp.CurrentTemperature
            temp_celsius = (temp_k / 10.0) - 273.15
            
            temp_str = f"{temp_celsius:.2f}°C"
            
            print(f"- Valoarea in Celsius: {temp_celsius:.2f}°C")

            return temp_str

    except Exception as e:
        print(f"Eroare: {e}")

def get_cpu_load_wmi():
    try:
        w = wmi.WMI()
        cpu_loads = w.Win32_Processor()
        for cpu in cpu_loads:
            print(f"- Valoarea: {cpu.LoadPercentage}%")
            return f"{cpu.LoadPercentage}%"
    except Exception as e:
        print(f"Eroare: {e}")


#verificarea argumentelor din linia de comanda
if len(sys.argv) < 2:
    print("EROARE: Compilare incorecta! (ex: python agent.py 12345)")
    sys.exit(1)

try:
    AGENT_PORT = int(sys.argv[1])
except ValueError:
    print("EROARE: Numar invalid. (ex: python agent.py 12345)")
    sys.exit(1)

#crearea socket-ului UDP pentru agent
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#legarea socket-ului la adresa agentului
try:
    agent_socket.bind(('0.0.0.0', AGENT_PORT))
except OSError as e:
    print(f"EROARE: Nu pot lega socket-ul pe portul {AGENT_PORT}.\nMotiv: {e}")
    sys.exit(1)


print(f"Agentul asculta pe UDP 0.0.0.0:{AGENT_PORT}...")

try:
    # Bucla principala de asteptare
    while True:
        data, manager_addr = agent_socket.recvfrom(1024)
        
        request_msg = data.decode()
        print(f"\n[RECV] Cerere de la Manager ({manager_addr}): {request_msg}")

        # in portiunea asta facem un switch case pentru fiecare valoare MIB transmisa prin UDP
        # momentan avem doar functia pentru temperatura CPU si Load CPU
        if "GET /cpuTemp/" in request_msg and AGENT_PORT == 12345:
            temp = get_cpu_temp_wmi()
            response_data = f"Response: Thermal Temperature = {temp}".encode('utf-8')

        elif "GET /cpuLoad/ Agent 2" in request_msg:
            cpu_load = get_cpu_load_wmi()
            response_data = b"Response: CPU Load = " + cpu_load.encode('utf-8')

        else:
            response_data = b"Response: Unknown Request"

        agent_socket.sendto(response_data, manager_addr)
        print(f"[SEND] Raspuns trimis catre Manager.")
        
        break
        
except KeyboardInterrupt:
    print("\nAgentul oprit.")
    
agent_socket.close()