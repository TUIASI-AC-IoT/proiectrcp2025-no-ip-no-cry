#importarea modulelor necesare
import socket
import sys
import wmi
import psutil
import time
import threading

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
        # conectarea la WMI
        w = wmi.WMI(namespace="root\\wmi")
        
        # obtinerea temperaturii CPU
        temperatures = w.MSAcpi_ThermalZoneTemperature()

        if not temperatures:
             print("Eroare la citirea temperaturii CPU.")
             return
        
        print("Temperaturile citite :")

        for temp in temperatures:

            if tip == "Celsius":
                temp_celsius = (temp.CurrentTemperature / 10.0) - 273.15
                temp_str = f"{temp_celsius:.2f}°C"
                print(f"- Valoarea in Celsius: {temp_str}")

            elif tip == "Fahrenheit":
                temp_fahrenheit = ((temp.CurrentTemperature / 10.0) - 273.15) * 9/5 + 32
                temp_str = f"{temp_fahrenheit:.2f}°F"
                print(f"- Valoarea in Fahrenheit: {temp_str}")

            elif tip == "Kelvin":
                temp_kelvin = temp.CurrentTemperature / 10.0
                temp_str = f"{temp_kelvin:.2f}°K"
                print(f"- Valoarea in Kelvin: {temp_str}")

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

def get_network_load_psutil():
    try:
        net_io_1 = psutil.net_io_counters()
        time.sleep(0.5)
        net_io_2 = psutil.net_io_counters()
        
        upload = (net_io_2.bytes_sent - net_io_1.bytes_sent) / 1024 / 0.5
        download = (net_io_2.bytes_recv - net_io_1.bytes_recv) / 1024 / 0.5
        
        return f"Upload: {upload:.1f} KB/s, Download: {download:.1f} KB/s"
    except Exception as e:
        return f"Eroare: {e}"

def get_ram_usage_wmi():
    try:
        w = wmi.WMI()
        os_info = w.Win32_OperatingSystem()[0]
        
        total_ram = int(os_info.TotalVisibleMemorySize) / 1024
        free_ram = int(os_info.FreePhysicalMemory) / 1024
        used_ram = total_ram - free_ram
        ram_usage_percent = (used_ram / total_ram) * 100
        ram_usage_str = f"{used_ram:.2f} MB / {total_ram:.2f} MB ({ram_usage_percent:.2f}%)"

        return ram_usage_str
    except Exception as e:
        return f"Eroare: {e}"
    
def get_disk_usage_psutil():
    try:
        disk_usage = psutil.disk_usage('/')
        used = disk_usage.used / (1024 ** 3)
        total = disk_usage.total / (1024 ** 3)
        percent = disk_usage.percent
        disk_usage_str = f"{used:.2f} GB / {total:.2f} GB ({percent:.2f}%)"
        return disk_usage_str
    except Exception as e:
        return f"Eroare: {e}"
    


AGENT_PORT = 161
AGENT_IP = '127.0.0.1'  #get_wifi_ip()

## poti sa initializezi aici variabilele globale pentru threshold-uri, daca vrei
## sa le avem pe toate la un loc
## sa fie de genu threshold_cpu_load = 80  # procentaj
## sau threshold_temp = 75  # grade Celsius si tot asa



#### AM COMPLETAT CU THRESHOLD (completat de geo )====
#variabile globale
THRESHOLD_CPU_LOAD = 85  #  procente
THRESHOLD_RAM = 80       #  procente
THRESHOLD_DISK = 90      #  procente
THRESHOLD_TEMP = 75      #  grade Celsius
THRESHOLD_NET = 90       #  in procente


# Adresa de trap a managerului
TRAP_MANAGER_IP = '10.107.11.1' #IP MANAGER
TRAP_MANAGER_PORT = 162
ENTERPRISE_OID = '1.3.6.1.4.1.2.6.258'



## aici trebuie adaugata o functie pentru setarea valorilor primite de la manager
# COMPLETAT -GEO
def set_thresholds_from_manager(message):
    global THRESHOLD_CPU_LOAD
    global THRESHOLD_RAM
    global THRESHOLD_DISK
    global THRESHOLD_TEMP
    global THRESHOLD_NET

    try:
        lista = message.replace("SET THRESHOLD", "").strip().split()

        # lista de forma cheie-valoare
        for item in lista:
            key, value = item.split("=")
            value = float(value)

            if key == "CPU":
                THRESHOLD_CPU_LOAD = value
            elif key == "RAM":
                THRESHOLD_RAM = value
            elif key == "DISK":
                THRESHOLD_DISK = value
            elif key == "TEMP":
                THRESHOLD_TEMP = value
            elif key == "NET":
                THRESHOLD_NET = value

        print("[THRESHOLD UPDATE] Praguri actualizate:")
        print(f" CPU={THRESHOLD_CPU_LOAD}%")
        print(f" RAM={THRESHOLD_RAM}%")
        print(f" DISK={THRESHOLD_DISK}%")
        print(f" TEMP={THRESHOLD_TEMP}°C")
        print(f" NET={THRESHOLD_NET}%")

    except Exception as e:
        print(f"Eroare la setarea pragurilor: {e}")




 ## Functie pentru trimiterea trap-urilor - Geo
def send_trap(specific, description, value):
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
    s.sendto(trap.encode(), (TRAP_MANAGER_IP, TRAP_MANAGER_PORT))
    s.close()

    print(f"[TRAP SENT] {trap}")


# Functie pentru monitorizarea pragurilor - Geo

def monitorizare_thresholds():
    while True :

        #CPU LOAD
        cpu_load = get_cpu_load_wmi()
        if cpu_load:
            cpu_val = int(cpu_load.replace("%", ""))
            if cpu_val > THRESHOLD_CPU_LOAD:
                send_trap(
                    2,
                    "CPU load depaseste pragul",
                    f"{cpu_val}%"
                )

        #RAM 
        ram = get_ram_usage_wmi()
        if ram:
            procent = float(ram.split('(')[-1].replace('%)', ''))
            if procent > THRESHOLD_RAM:
                send_trap(3, "RAM peste prag",
                               f"{procent :.2f}%")


        # DISK
        disk = get_disk_usage_psutil()
        if disk:
            procent = float(disk.split('(')[-1].replace('%)', ''))
            if procent > THRESHOLD_DISK:
                send_trap(4, "Disk aproape plin",
                               f"{procent:.2f}%")

        # TEMP
        temp = get_cpu_temp_wmi("Celsius")
        if temp:
            t = float(temp.replace("°C", ""))
            if t > THRESHOLD_TEMP:
                send_trap(1, "Temperatura CPU ridicata", temp)

        time.sleep(5)
##################




print(f"Agent IP: {AGENT_IP}")

#crearea socket-ului UDP pentru agent
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#legarea socket-ului la adresa agentului
try:
    agent_socket.bind((AGENT_IP, 161))
    #adaugat - geo
    threading.Thread(target=monitorizare_thresholds, daemon=True).start()


except OSError as e:
    sys.exit(1)


print(f"Agentul asculta pe UDP 10.107.11.0:{AGENT_PORT}...")

try:
    # Bucla principala de asteptare
    while True:
        data, manager_addr = agent_socket.recvfrom(1024)
        
        request_msg = data.decode()
        print(f"\n[RECV] Cerere de la Manager ({manager_addr}): {request_msg}")

        match request_msg:
            case "Temperature Celsius":
                 temp = get_cpu_temp_wmi("Celsius")
                 response_data = f"Response: CPU Temperature = {temp}".encode('utf-8')

            case "Temperature Fahrenheit":
                 temp = get_cpu_temp_wmi("Fahrenheit")
                 response_data = f"Response: CPU Temperature = {temp}".encode('utf-8')

            case "Temperature Kelvin":
                temp = get_cpu_temp_wmi("Kelvin")
                response_data = f"Response: CPU Temperature = {temp}".encode('utf-8')

            case "CPU Load":
                cpu_load = get_cpu_load_wmi()
                response_data = f"Response: CPU Load = {cpu_load}".encode('utf-8')

            case "Network Load":
                net_load = get_network_load_psutil()
                response_data = f"Response: Network Load:  {net_load}".encode('utf-8')

            case "RAM":
                ram_usage = get_ram_usage_wmi()
                response_data = f"Response: RAM Usage = {ram_usage}".encode('utf-8')

            case "Disk":
                disk_usage = get_disk_usage_psutil()
                response_data = f"Response: Disk Usage = {disk_usage}".encode('utf-8')

            case _ if request_msg.startswith("SET THRESHOLD"):
                set_thresholds_from_manager(request_msg)
                response_data = b"Threshold-uri actualizate cu succes"

            case "close":
                print("Inchidere...")
                agent_socket.close()
                sys.exit(1)

            case _:
                response_data = f"Eroare: Request necunoscut.".encode('utf-8')

        agent_socket.sendto(response_data, manager_addr)
        print(f"[SEND] Raspuns trimis catre Manager.")
except KeyboardInterrupt:
    print("\nAgent oprit de utilizator.")
    agent_socket.close()
    print("Agentul s-a inchis.")