#importarea modulelor necesare
import socket
import select
import threading
from tkinter import *

# configurarea adreselor/porturilot agentilor
AGENT_1_ADDR = ('10.107.11.160', 161)         #laptop felicia,   ip : 10.107.11.160
AGENT_2_ADDR = ('10.107.11.199', 161)         #laptop georgiana, ip : 10.107.11.199
TRAP_PORT = 162

#crearea socket-ului UDP pentru manager
manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
manager_socket.bind(('0.0.0.0', 0)) 
manager_socket.setblocking(False) 


## socket pentru Traps
trap_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
trap_socket.bind(('0.0.0.0', TRAP_PORT))
trap_socket.setblocking(False)

# configurarea MIB-ului
mib = {
    "1.1.1" : "CPU_Load",
    "1.1.2" : "CPU_Temperature",
    "1.1.2.1" : "Temperature_Celsius",
    "1.1.2.2" : "Temperature_Fahrenheit",
    "1.1.2.3" : "Temperature_Kelvin",
    "1.2.1" : "RAM",
    "1.2.2" : "Disk",
    "1.3.1" : "Network_Load", 
    "f.f.f" : "close"
}

mib_order = [
    "1.1.1", "1.1.2", "1.1.2.1", "1.1.2.2", "1.1.2.3",
    "1.2.1", "1.2.2", "1.3.1", "f.f.f"
]

# interfata grafica
root = Tk()
root.title("SNMP v1 - Demonstrative Application")

####
auto_refresh = False
refresh_interval = 10000  # milisecunde (10 secunde)

def auto_update():
    global auto_refresh
    if not auto_refresh:
        return

    oid = e.get()
    if oid not in mib:
        add_response_label("[ERROR] OID invalid pentru auto-update")
    else:
        add_response_label(f"[AUTO] Se trimite cererea: {mib[oid]}...")
        manager_socket.sendto(mib[oid].encode(), AGENT_1_ADDR)
        manager_socket.sendto(mib[oid].encode(), AGENT_2_ADDR)

    root.after(refresh_interval, auto_update)
#####

frame_up = LabelFrame(root, padx=20, pady=20)
frame_response = LabelFrame(root, text="Responses", padx=20, pady=20)
frame_info = LabelFrame(root, text="MIB Tree", padx=20, pady=20)

frame_up.grid(row=0, column=0, padx=20, pady=10, columnspan=4)
frame_info.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
frame_response.grid(row=1, column=1, padx=20, pady=10, sticky="nsew", columnspan=3)

interval_entry = Entry(frame_up, width=10, font=("Times New Roman", 12))
interval_entry.insert(0, "5")  # default 5 secunde
interval_entry.grid(row=1, column=2)

setR = Entry(frame_up, width=50, borderwidth=5, font=("Times New Roman", 12))
setR.insert(0, "Introduceti tipul setarii: (Ex: SET THRESHOLD 1.1.1 = 70)")
setR.grid(row=1, column=0)

e = Entry(frame_up, width=50, borderwidth=5, font=("Times New Roman", 12))
e.insert(0, "Introduceti MIB-ul: (ex: pentru CPU Load: '1.1.1')")
e.grid(row=0, column=0)

##
combo_box = StringVar()
um_temp = OptionMenu(frame_up, combo_box, "Celsius", "Fahrenheit", "Kelvin")
combo_box.set("Celsius")  # valoare default
um_temp.grid(row=1, column=5)
##

#showing the MIB Tree
system = Label(frame_info, text="^ System (1)", font=("Times New Roman", 12, "bold"))
cpu = Label(frame_info, text="  |- CPU (1)", font=("Times New Roman", 12))
cpu_load = Label(frame_info, text="  |      |---- CPU Load (1)", font=("Times New Roman", 12))
cpu_temp = Label(frame_info, text="  |      |---- CPU Temperature (2)", font=("Times New Roman", 12))
temp_c = Label(frame_info, text="  |                    |---- Temperature Celsius (1)", font=("Times New Roman", 12))
temp_f = Label(frame_info, text="  |                    |---- Temperature Fahrenheit (2)", font=("Times New Roman", 12))
temp_K = Label(frame_info, text="  |                    |---- Temperature Kelvin (3)", font=("Times New Roman", 12))
mem = Label(frame_info, text="  |- Memory (2)", font=("Times New Roman", 12))
ram = Label(frame_info, text="  |      |---- RAM (1)", font=("Times New Roman", 12))
disk = Label(frame_info, text="  |      |---- Disk (2)", font=("Times New Roman", 12))
net = Label(frame_info, text="  |- Network (3)", font=("Times New Roman", 12))
net_load = Label(frame_info, text="         |---- Network Load (1)", font=("Times New Roman", 12))

system.grid(column=0, row=0, sticky="w")
cpu.grid(column=0, row=1, sticky="w")
cpu_load.grid(column=0, row=2, sticky="w")
cpu_temp.grid(column=0, row=3, sticky="w")
temp_c.grid(column=0, row=4, sticky="w")
temp_f.grid(column=0, row=5, sticky="w")
temp_K.grid(column=0, row=6, sticky="w")
mem.grid(column=0, row=7, sticky="w")
ram.grid(column=0, row=8, sticky="w")
disk.grid(column=0, row=9, sticky="w")
net.grid(column=0, row=10, sticky="w")
net_load.grid(column=0, row=11, sticky="w")

myLabl = Label(frame_response, text="Managerul asculta pe portul local 161(raspunsuri) si 162(trap-uri)... ", font=("Times New Roman", 12), anchor = "w")
myLabl.grid(column=0, row=0, sticky="w")

####
Label(frame_up, text="Interval (sec)", font=("Times New Roman", 12)).grid(row=1, column=1)
###

def start_auto_refresh():
    global auto_refresh, refresh_interval

    try:
        sec = int(interval_entry.get())
        refresh_interval = sec * 1000
    except ValueError:
        add_response_label("[ERROR] Interval invalid")
        return

    auto_refresh = True
    add_response_label("[INFO] Actualizare automată pornită")
    auto_update()


def stop_auto_refresh():
    global auto_refresh
    auto_refresh = False
    add_response_label("[INFO] Actualizare automată oprită")


 ###
start_button = Button(frame_up, text="Start Auto Update", font=("Times New Roman", 14), width=20, command=start_auto_refresh)
stop_button = Button(frame_up, text="Stop Auto Update", font=("Times New Roman", 14), width=20, command=stop_auto_refresh)

start_button.grid(row=0, column=4)
stop_button.grid(row=0, column=5)
###


# handling responses
response_row = 1
MAX_RESPONSES = 20 
response_labels = []

def add_response_label(text):
    global response_row, response_labels
    
    new_label = Label(frame_response, text=text, font=("Times New Roman", 12), anchor="w")
    new_label.grid(row=response_row, column=0, sticky="w", pady=2)
    response_row += 1
    
    response_labels.append(new_label)
    
    if len(response_labels) > MAX_RESPONSES:
        old_label = response_labels.pop(0)
        old_label.destroy()
        
        for idx, label in enumerate(response_labels):
            label.grid(row=idx + 1, column=0, sticky="w", pady=2)
        
        response_row = len(response_labels) + 1

def check_for_responses():    
    while True:
        try:
            ready_to_read, _, _ = select.select([manager_socket, trap_socket], [], [], 0.1)

            if manager_socket in ready_to_read:
                data, addr = manager_socket.recvfrom(1024)
                response_msg = data.decode()
                
                root.after(0, add_response_label, f"[RESPONSE] {addr[0]}:{addr[1]} : {response_msg}")

            # ---- TRAP-URI receptionate -----(Geo)
            if trap_socket in ready_to_read:
                data, addr = trap_socket.recvfrom(1024)
                trap_msg = data.decode()
                root.after(0, add_response_label, f"[TRAP] {addr[0]}:{TRAP_PORT} : {trap_msg}")
                
        except Exception as e:
            print(f"Eroare la primirea raspunsului: {e}")

response_thread = threading.Thread(target=check_for_responses, daemon=True)
response_thread.start()


def sendRequest():
    global e
    
    oid = e.get()

    if oid == "1.1.2":
        unitate = combo_box.get()
        if unitate == "Celsius":
            oid = "1.1.2.1"
        elif unitate == "Fahrenheit":
            oid = "1.1.2.2"
        elif unitate == "Kelvin":
            oid = "1.1.2.3"
    
    add_response_label(f"Se trimite cererea: {mib[oid]}...")
    
    manager_socket.sendto(mib[oid].encode('utf-8'), AGENT_1_ADDR)
    manager_socket.sendto(mib[oid].encode('utf-8'), AGENT_2_ADDR)
    
    add_response_label("Se asteapta raspunsurile... ")
    


# din ce am inteles, asta trimite urmatoarea cerere din MIB
# adica, daca noi am cerut CPU Load, daca apasam pe SendNextRequest va fi CPU Temperature,
# adica urmatorul din dictionar
def SendNextRequest():
    global e
    
    current_oid = e.get()

    if current_oid == "1.1.2":
        unitate = combo_box.get()
        if unitate == "Celsius":
            current_oid = "1.1.2.1"
        elif unitate == "Fahrenheit":
            current_oid = "1.1.2.2"
        elif unitate == "Kelvin":
            current_oid = "1.1.2.3"

    current_index = mib_order.index(current_oid)
    if current_index + 1 >= len(mib_order):
        add_response_label("[INFO] Ajuns la sfârșitul MIB-ului")
        return

    next_oid = mib_order[current_index + 1]
    next_msg = mib[next_oid]

    e.delete(0, END)
    e.insert(0, next_oid)
    
    add_response_label(f"Se trimite urmatoarea cerere: {next_msg}...")
    
    manager_socket.sendto(next_msg.encode('utf-8'), AGENT_1_ADDR)
    manager_socket.sendto(next_msg.encode('utf-8'), AGENT_2_ADDR)
    
    add_response_label("Se asteapta raspunsurile... ")


# am introdus eu entry-ul pentru a seta threshold-urile 
# modifica functia asta, ca sa trimita si mib-ul si valoarea pe care vrem s-o setam
def setRequest():
    global setR
    
    set_command = setR.get().strip()

    parts = set_command.replace("SET THRESHOLD", "").strip().split("=")

    set_oid = parts[0].strip()
    set_value = parts[1].strip()

    set_name = mib[set_oid]
    set_msg = f"SET THRESHOLD {set_name} = {set_value}"

    add_response_label(f"Se trimite setarea: {set_msg}...")
    
    manager_socket.sendto(set_msg.encode('utf-8'), AGENT_1_ADDR)
    manager_socket.sendto(set_msg.encode('utf-8'), AGENT_2_ADDR)
    
    add_response_label("Se asteapta confirmarea... ")

# buttons
send_button = Button(frame_up, text="Get Request", font=("Times New Roman", 14), width=20, command=sendRequest)
next_button = Button(frame_up, text="Get Next Request", font=("Times New Roman", 14), width=20, command=SendNextRequest)
set_button = Button(frame_up, text="Set Request", font=("Times New Roman", 14), width=20, command=setRequest)
send_button.grid(row=0, column=1)
next_button.grid(row=0, column=2)
set_button.grid(row=0, column=3)

root.mainloop()

manager_socket.close()
trap_socket.close()

## trebuie adaugat inca un entry de selectare a unitarii de masuru
## o sa folosesc un combobox din tkinter
## cu optiunile: Celsius, Fahrenheit, Kelvin

