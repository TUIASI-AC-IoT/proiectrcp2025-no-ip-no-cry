#importarea modulelor necesare
import socket
import select
from tkinter import *

# configurarea adreselor/porturilot agentilor (localhost)
AGENT_1_ADDR = ('127.0.0.1', 12345)
AGENT_2_ADDR = ('127.0.0.1', 12346)

#crearea socket-ului UDP pentru manager
manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
manager_socket.bind(('0.0.0.0', 0)) 
manager_socket.setblocking(False) 


mib = {
    "1.1.1" : "CPU Load",
    "1.1.2" : "CPU Temperature",
    "1.1.2.1" : "Temperature Celsius",
    "1.1.2.2" : "Temperature Fahrenheit",
    "1.1.2.3" : "Temperature Kelvin",
    "1.2.1" : "RAM",
    "1.2.2" : "Disk",
    "1.3.1" : "Network Load"    
}

# interfata grafica

root = Tk()
root.title("SNMP v1 - Demonstrative Application")

frame_up = LabelFrame(root, padx=20, pady=20)
frame_response = LabelFrame(root, text="Responses", padx=20, pady=20)
frame_info = LabelFrame(root, text="MIB Tree", padx=20, pady=20)

frame_up.grid(row=0, column=0, padx=20, pady=10, columnspan=3)
frame_info.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
frame_response.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

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

myLabl = Label(frame_response, text="Managerul asculta pe portul local... ", font=("Times New Roman", 12), anchor = "w")
myLabl.grid(column=0, row=0, sticky="w")

e = Entry(frame_up, width=50, borderwidth=5, font=("Times New Roman", 12))
e.insert(0, "Insert function call here (ex: GET /cpuTemp/ )")
e.grid(row=0, column=0)


# handling responses
response_row = 1

#in fiecare functie se va face cate un switch case pentru fiecare tip de request
def sendRequest():
    global response_row
    myLabl = Label(frame_response, text="Se trimite cererea "+ e.get() + "..."  , font=("Times New Roman", 12), anchor ="w")
    myLabl.grid(row=response_row, column=0, sticky="w", pady=2)
    response_row += 1


def SendNextRequest():
    global response_row
    myLabl = Label(frame_response, text="Send Next Request for " + e.get() , font=("Times New Roman", 12), anchor ="w")
    myLabl.grid(row=response_row, column=0, sticky="w", pady=2)
    response_row += 1

def setRequest():
    global response_row
    myLabl = Label(frame_response, text="Set Request for " + e.get() , font=("Times New Roman", 12), anchor ="w")
    myLabl.grid(row=response_row, column=0, sticky="w", pady=2)
    response_row += 1

# buttons
send_button = Button(frame_up, text="Get Request", font=("Times New Roman", 14), width=20, command=sendRequest)
next_button = Button(frame_up, text="Get Next Request", font=("Times New Roman", 14), width=20, command=SendNextRequest)
set_button = Button(frame_up, text="Set Request", font=("Times New Roman", 14), width=20, command=setRequest)
send_button.grid(row=0, column=1)
next_button.grid(row=0, column=2)
set_button.grid(row=0, column=3)

root.mainloop()