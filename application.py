#importarea modulelor necesare
import socket
import select
from tkinter import *

# configurarea adreselor/porturilot agentilor
AGENT_1_ADDR = ('127.0.0.1', 161)         #laptop felicia,   ip : 10.107.11.160
AGENT_2_ADDR = ('127.0.0.2', 161)         #laptop georgiana, ip : 10.107.11.199

## GEO
TRAP_PORT = 162

#crearea socket-ului UDP pentru manager
manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
manager_socket.bind(('0.0.0.0', 161)) 
manager_socket.setblocking(False) 

## GEO
## socket pentru Traps
trap_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
trap_socket.bind(('0.0.0.0', TRAP_PORT))
trap_socket.setblocking(False)
print(f"Managerul asculta TRAP-urile pe portul {TRAP_PORT}")

# configurarea MIB-ului
mib = {
    "1.1.1" : "CPU Load",
    "1.1.2" : "CPU Temperature",
    "1.1.2.1" : "Temperature Celsius",
    "1.1.2.2" : "Temperature Fahrenheit",
    "1.1.2.3" : "Temperature Kelvin",
    "1.2.1" : "RAM",
    "1.2.2" : "Disk",
    "1.3.1" : "Network Load", 
    "f.f.f" : "close"
}

# interfata grafica

root = Tk()
root.title("SNMP v1 - Demonstrative Application")

frame_up = LabelFrame(root, padx=20, pady=20)
frame_response = LabelFrame(root, text="Responses", padx=20, pady=20)
frame_info = LabelFrame(root, text="MIB Tree", padx=20, pady=20)

frame_up.grid(row=0, column=0, padx=20, pady=10, columnspan=4)
frame_info.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
frame_response.grid(row=1, column=1, padx=20, pady=10, sticky="nsew", columnspan=3)
setR = Entry(frame_up, width=50, borderwidth=5, font=("Times New Roman", 12))
setR.insert(0, "Introduceti valoarea pentru Set Request")
setR.grid(row=0, column=4)

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

myLabl = Label(frame_response, text="Managerul asculta pe portul local 161(UDP)... ", font=("Times New Roman", 12), anchor = "w")
myLabl.grid(column=0, row=0, sticky="w")

e = Entry(frame_up, width=50, borderwidth=5, font=("Times New Roman", 12))
e.insert(0, "Introduceti MIB-ul: (ex: pentru CPU Load: '1.1.1')")
e.grid(row=0, column=0)


# handling responses
response_row = 1
responses_received = 0
expected_responses = 2
MAX_RESPONSES = 20 
response_labels = []

def add_response_label(text):
    global response_row, response_labels
    
    new_label = Label(frame_response, text=text,
                     font=("Times New Roman", 12), anchor="w")
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
    global response_row, responses_received
    
    try:
        ready_to_read, _, _ = select.select([manager_socket], [], [], 0.5)
        
        if manager_socket in ready_to_read:
            data, addr = manager_socket.recvfrom(1024)
            response_msg = data.decode()
            
            add_response_label(f"Raspuns primit de la {addr}: {response_msg}")
            responses_received += 1
            
            if responses_received < expected_responses:
                root.after(100, check_for_responses)
            else:
                responses_received = 0

        # ---- TRAP-URI receptionate -----(Geo)
        if trap_socket in ready_to_read:
            trap_data, trap_addr = trap_socket.recvfrom(1024)
            print("\n [TRAP PRIMIT]")
            print(f"De la agent: {trap_addr}")
            print(trap_data.decode())
            
    except Exception as e:
        print(f"Eroare la primirea raspunsului: {e}")
        root.after(100, check_for_responses)


def sendRequest():
    global response_row, responses_received
    
    responses_received = 0
    
    add_response_label(f"Se trimite cererea: {mib[e.get()]}...")
    
    manager_socket.sendto(mib[e.get()].encode('utf-8'), AGENT_1_ADDR)
    manager_socket.sendto(mib[e.get()].encode('utf-8'), AGENT_2_ADDR)
    
    add_response_label("Se asteapta raspunsurile... ")
    
    root.after(200, check_for_responses)


# din ce am inteles, asta trimite urmatoarea cerere din MIB
# adica, daca noi am cerut CPU Load, daca apasam pe SendNextRequest va fi CPU Temperature,
# adica urmatorul din dictionar
def SendNextRequest():
    global response_row, responses_received
    
    responses_received = 0
    
    add_response_label(f"Se trimite urmatoarea cerere: {mib[e.get()]}...")
    
    manager_socket.sendto(mib[e.get()].encode('utf-8'), AGENT_1_ADDR)
    manager_socket.sendto(mib[e.get()].encode('utf-8'), AGENT_2_ADDR)
    
    add_response_label("Se asteapta raspunsurile... ")
    
    root.after(100, check_for_responses)

# am introdus eu entry-ul pentru a seta threshold-urile 
# modifica functia asta, ca sa trimita si mib-ul si valoarea pe care vrem s-o setam
def setRequest():
    global response_row, responses_received
    
    responses_received = 0
    
    add_response_label(f"Se trimite setarea: {mib[e.get()]}...")
    
    manager_socket.sendto(mib[e.get()].encode('utf-8'), AGENT_1_ADDR)
    manager_socket.sendto(mib[e.get()].encode('utf-8'), AGENT_2_ADDR)
    
    add_response_label("Se asteapta raspunsurile... ")
    
    root.after(100, check_for_responses)

# buttons
send_button = Button(frame_up, text="Get Request", font=("Times New Roman", 14), width=20, command=sendRequest)
next_button = Button(frame_up, text="Get Next Request", font=("Times New Roman", 14), width=20, command=SendNextRequest)
set_button = Button(frame_up, text="Set Request", font=("Times New Roman", 14), width=20, command=setRequest)
send_button.grid(row=0, column=1)
next_button.grid(row=0, column=2)
set_button.grid(row=0, column=3)

root.mainloop()

## trebuie sa imi dau seama de ce nu primesc raspunsurile imediat cum le trimit,
## merge doar daca apas butonul de Send Request din nou
