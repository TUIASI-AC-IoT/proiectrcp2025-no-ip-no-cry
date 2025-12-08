#importarea modulelor necesare
import socket
import sys
import wmi
import psutil
import time
import threading
import pythoncom

# funnctie pentru obtinerea adresei IP a fiecarui agent(laptop)
def get_wifi_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '0.0.0.0'
    finally:
        s.close()
        return ip

# functia pentru obtinerea temperaturii CPU folosind WMI
def get_cpu_temp_wmi(tip = "Celsius"):
    try:
        # functie WMI necesita initializarea COM in thread-ul curent
        pythoncom.CoInitialize()       

        # conectarea la WMI
        w = wmi.WMI(namespace="root\\wmi")
        
        # obtinerea temperaturii CPU
        temperatures = w.MSAcpi_ThermalZoneTemperature()

        if not temperatures:
            return None
        
        print("Temperaturile citite:")

        temp = temperatures[0]
        # conversia temperaturii in unitatea de masura dorita
        if tip == "Celsius":
            temp_celsius = (temp.CurrentTemperature / 10.0) - 273.15
            temp_str = f"{temp_celsius:.2f}"
            print(f"- Valoarea in Celsius: {temp_str}")
        elif tip == "Fahrenheit":
            temp_fahrenheit = ((temp.CurrentTemperature / 10.0) - 273.15) * 9/5 + 32
            temp_str = f"{temp_fahrenheit:.2f}"
            print(f"- Valoarea in Fahrenheit: {temp_str}")
        elif tip == "Kelvin":
            temp_kelvin = temp.CurrentTemperature / 10.0
            temp_str = f"{temp_kelvin:.2f}"
            print(f"- Valoarea in Kelvin: {temp_str}")
            
        return temp_str

    except Exception as e:
        return None

    finally:
        #eliberarea COM
        pythoncom.CoUninitialize()

#functie pentru obtinerea CPU Load folosind WMI
def get_cpu_load_psutil():
    try:
        # psutil.cpu_percent() returneaza procentajul de utilizare CPU
        cpu_load = psutil.cpu_percent(interval=1) # Măsurare pe 1 secundă
        return f"{cpu_load:.2f}"
    except Exception as e:
        print(f"Eroare psutil CPU Load: {e}")
        return "0"

# functie pentru obtinerea Network Load folosind psutil
def get_network_load_psutil():
    try:
        # determinarea vitezei maxime a retelei
        net_stats = psutil.net_if_stats()
        max_bandwidth = 0

        for interface, stats in net_stats.items():
            #verificam daca interfata este activa
            if stats.isup and stats.speed > 0: 
                # actualizam viteza maxima
                max_bandwidth = max(max_bandwidth, stats.speed * 1_000_000)

        # daca nu se poate determina viteza maxima, presupunem o valoare implicita
        if max_bandwidth == 0:
            max_bandwidth = 100_000_000     # 100 Mbps

        # masurarea traficului de retea pe o perioada scurta
        net_io_1 = psutil.net_io_counters()
        time.sleep(0.5)
        net_io_2 = psutil.net_io_counters()
        
        upload = (net_io_2.bytes_sent - net_io_1.bytes_sent) * 8 / 0.5
        download = (net_io_2.bytes_recv - net_io_1.bytes_recv) * 8 / 0.5   # b/s

        total_percent = ((upload + download) / (max_bandwidth * 2)) * 100
        total_percent_str = f"{total_percent:.2f}"
        
        return total_percent_str
    except Exception as e:
        return f"Eroare: {e}"

# functie pentru obtinerea utilizarii RAM folosind WMI
def get_ram_usage_wmi():
    try:
        pythoncom.CoInitialize()
        w = wmi.WMI()

        # obtinerea informatiilor despre RAM
        os_info = w.Win32_OperatingSystem()[0]
        
        total_ram = int(os_info.TotalVisibleMemorySize) / 1024
        free_ram = int(os_info.FreePhysicalMemory) / 1024
        used_ram = total_ram - free_ram
        ram_usage_percent = (used_ram / total_ram) * 100
        ram_usage_str = f"{ram_usage_percent:.2f}"

        return ram_usage_str
    
    except Exception as e:
        return None
    
    finally:
        #eliberarea COM
        pythoncom.CoUninitialize()
    
# functie pentru obtinerea utilizarii Disk folosind psutil
def get_disk_usage_psutil():
    try:
        # functia de obtinere a utilizarii Disk
        disk_usage = psutil.disk_usage('/')     #folosim '/' pentru path-ul radacina

        percent = disk_usage.percent
        disk_usage_str = f"{percent:.2f}"
        return disk_usage_str
    except Exception as e:
        return f"Eroare: {e}"
    

# definirea adreselor si porturilor agentilor
AGENT_PORT = 161
AGENT_IP = get_wifi_ip()

## poti sa initializezi aici variabilele globale pentru threshold-uri, daca vrei
## sa le avem pe toate la un loc
## sa fie de genu threshold_cpu_load = 80  # procentaj
## sau threshold_temp = 75  # grade Celsius si tot asa



#### AM COMPLETAT CU THRESHOLD (completat de geo )====
#variabile globale
THRESHOLD_CPU_LOAD = 85
THRESHOLD_CPU_TEMP_C = 75
THRESHOLD_CPU_TEMP_K = 348.15
THRESHOLD_CPU_TEMP_F = 167
THRESHOLD_RAM = 80
THRESHOLD_DISK = 90
THRESHOLD_NET_LOAD = 90


# Adresa de trap a managerului
ENTERPRISE_OID = '1.3.6.1.4.1.2.6.258'    

#lock pentru prevenirea citirilor/scrierilor concurente la variabilele de prag
threshold_lock = threading.Lock()

## aici trebuie adaugata o functie pentru setarea valorilor primite de la manager
# COMPLETAT -GEO
def set_thresholds_from_manager(lista):
    global THRESHOLD_CPU_LOAD
    global THRESHOLD_RAM
    global THRESHOLD_DISK
    global THRESHOLD_CPU_TEMP_C
    global THRESHOLD_CPU_TEMP_K
    global THRESHOLD_CPU_TEMP_F
    global THRESHOLD_NET_LOAD

    try:
        #blocheaza citirea la actualozarea pragurilor
        with threshold_lock:
            for item in lista:
                key = item[0]
                value = float(item[1])

                if key == "CPU_Load":
                    THRESHOLD_CPU_LOAD = value
                elif key == "RAM":
                    THRESHOLD_RAM = value
                elif key == "Disk":
                    THRESHOLD_DISK = value
                elif key == "Temperature_Celsius":
                    THRESHOLD_CPU_TEMP_C = value
                    THRESHOLD_CPU_TEMP_K = value + 273.15
                    THRESHOLD_CPU_TEMP_F = (value * 9/5) + 32
                elif key == "Temperature_Kelvin":
                    THRESHOLD_CPU_TEMP_K = value
                    THRESHOLD_CPU_TEMP_C = value - 273.15
                    THRESHOLD_CPU_TEMP_F = ((value - 273.15) * 9/5) + 32
                elif key == "Temperature_Fahrenheit":
                    THRESHOLD_CPU_TEMP_F = value
                    THRESHOLD_CPU_TEMP_C = (value - 32) * 5/9
                    THRESHOLD_CPU_TEMP_K = ((value - 32) * 5/9) + 273.15
                elif key == "Network_Load":
                    THRESHOLD_NET_LOAD = value

        print("[THRESHOLD UPDATE] Praguri actualizate:")
        print(f" CPU={THRESHOLD_CPU_LOAD}%")
        print(f" RAM={THRESHOLD_RAM}%")
        print(f" DISK={THRESHOLD_DISK}%")
        print(f" TEMP={THRESHOLD_CPU_TEMP_C}°C")
        print(f" TEMP={THRESHOLD_CPU_TEMP_K}°K")
        print(f" TEMP={THRESHOLD_CPU_TEMP_F}°F")
        print(f" NET={THRESHOLD_NET_LOAD}%")

    except Exception as e:
        print(f"Eroare la setarea pragurilor: {e}")


 ## Functie pentru trimiterea trap-urilor - Geo
def send_trap(specific, description, value, manager_addr):
    trap = (
        f"SNMPv1-TRAP | "
        f"Enterprise={ENTERPRISE_OID} | "
        f"Agent={AGENT_IP} | "
        f"Generic=6 | "
        f"Specific={specific} | "
        f"{description} | "
        f"Value={value}"
    )

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    trap_manager = (manager_addr[0], 162)
    s.sendto(trap.encode(), trap_manager)
    s.close()

    print(f"[TRAP SENT] {trap}")


# Functie pentru monitorizarea pragurilor - Geo

def monitorizare_thresholds(manager_addr):
    while True :
        try:
            with threshold_lock:
                cpu_threshold = THRESHOLD_CPU_LOAD
                ram_threshold = THRESHOLD_RAM
                disk_threshold = THRESHOLD_DISK
                temp_threshold_c = THRESHOLD_CPU_TEMP_C
                net_threshold = THRESHOLD_NET_LOAD

            #CPU LOAD
            cpu_val = round(float(get_cpu_load_psutil()),2)
            if cpu_val > cpu_threshold:
                send_trap(2, "CPU load depaseste pragul", cpu_val, manager_addr)

            #RAM 
            ram = round(float(get_ram_usage_wmi()),2)
            if ram > ram_threshold:
                send_trap(3, "RAM peste prag", ram, manager_addr)

            # DISK
            disk = round(float(get_disk_usage_psutil()), 2)
            if disk > disk_threshold:
                send_trap(4, "Disk aproape plin", disk, manager_addr)

            # TEMP
            temp_c = round(float(get_cpu_temp_wmi("Celsius")), 2)
            if temp_c > temp_threshold_c:
                send_trap(1, "Temperatura CPU ridicata", temp_c, manager_addr)

            # NETWORK LOAD
            net = round(float(get_network_load_psutil()), 2)
            if net > net_threshold:
                send_trap(5, "Reteaua este congestionata", net, manager_addr)

            time.sleep(10)
        except Exception as e:
            time.sleep(10)

##################




print(f"Agent IP: {AGENT_IP}")

#crearea socket-ului UDP pentru agent
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#legarea socket-ului la adresa agentului
try:
    agent_socket.bind((AGENT_IP, 161))
except OSError as e:
    sys.exit(1)

print(f"Agentul asculta pe UDP 10.107.11.0:{AGENT_PORT}...")

#variabila pentru a porni monitorizarea o singura data
monitoring_started = False

try:
    # Bucla principala de asteptare
    while True:
        data, manager_addr = agent_socket.recvfrom(4096)

        if not monitoring_started:
            threading.Thread(target=monitorizare_thresholds, args = (manager_addr,), daemon=True).start()
            monitoring_started = True
        
        request_msg = data.decode()
        print(f"\n[RECV] Cerere de la Manager ({manager_addr}): {request_msg}")

        response_data = None

        match request_msg:
            case "CPU_Temperature":
                temp = get_cpu_temp_wmi("Celsius")
                response_data = f"Response: CPU Temperature(default - Celsius) = {temp}".encode('utf-8')

            case "Temperature_Celsius":
                temp = get_cpu_temp_wmi("Celsius")
                response_data = f"Response: CPU Temperature = {temp}".encode('utf-8')

            case "Temperature_Fahrenheit":
                temp = get_cpu_temp_wmi("Fahrenheit")
                response_data = f"Response: CPU Temperature = {temp}".encode('utf-8')

            case "Temperature_Kelvin":
                temp = get_cpu_temp_wmi("Kelvin")
                response_data = f"Response: CPU Temperature = {temp}".encode('utf-8')

            case "CPU_Load":
                cpu_load = get_cpu_load_psutil()
                response_data = f"Response: CPU Load = {cpu_load}".encode('utf-8')

            case "Network_Load":
                net_load = get_network_load_psutil()
                response_data = f"Response: Network Load:  {net_load}".encode('utf-8')

            case "RAM":
                ram_usage = get_ram_usage_wmi()
                response_data = f"Response: RAM Usage = {ram_usage}".encode('utf-8')

            case "Disk":
                disk_usage = get_disk_usage_psutil()
                response_data = f"Response: Disk Usage = {disk_usage}".encode('utf-8')

            case _ if request_msg.startswith("SET THRESHOLD"):
                parts = request_msg.replace("SET THRESHOLD", "").strip().split("=")
                key = parts[0].strip()
                value = parts[1].strip()
                set_thresholds_from_manager([(key, value)])
                response_data = b"Threshold-uri actualizate cu succes"

            case "close":
                print("Inchidere...")
                agent_socket.close()
                sys.exit(1)

            case _:
                response_data = f"Eroare: Request necunoscut. {request_msg}".encode('utf-8')

        agent_socket.sendto(response_data, manager_addr)
        print(f"[SEND] Raspuns trimis catre Manager.")
        
except KeyboardInterrupt:
    print("\nAgent oprit de utilizator.")
    agent_socket.close()
    print("Agentul s-a inchis.")