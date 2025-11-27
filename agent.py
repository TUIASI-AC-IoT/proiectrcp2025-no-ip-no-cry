#importarea modulelor necesare
import socket
import sys
import wmi
import psutil
import time

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

def get_network_load_wmi():
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

AGENT_PORT = 161
AGENT_IP = '127.0.0.2'  #get_wifi_ip()

print(f"Agent IP: {AGENT_IP}")

#crearea socket-ului UDP pentru agent
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#legarea socket-ului la adresa agentului
try:
    agent_socket.bind((AGENT_IP, 161))
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
                net_load = get_network_load_wmi()
                response_data = f"Response: Network Load:  {net_load}".encode('utf-8')

            case "RAM":
                ram_usage = get_ram_usage_wmi()
                response_data = f"Response: RAM Usage = {ram_usage}".encode('utf-8')

            case default:
                agent_socket.close()
                sys.exit(1)


        agent_socket.sendto(response_data, manager_addr)
        print(f"[SEND] Raspuns trimis catre Manager.")
except KeyboardInterrupt:
    print("\nAgent oprit de utilizator.")
    agent_socket.close()
    print("Agentul s-a inchis.")