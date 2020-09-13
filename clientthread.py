from threading import Event
import socket , sys, threading


port = 9000
BUFFER_SIZE = 2000 
receive_event = Event()
host = socket.gethostname() 

def recieveMessages():
    global receive_event
    for message in iter(lambda: client.recv(1024).decode(), ''):
        print(message)
        receive_event.set()

def process_msg(msg):
    global receive_event
    end = False
    if msg == "Exit":
        end = True
        client.send(msg.encode('ascii'))

    elif msg == "Send":
        destination = input("Please enter the client ID: \n")
        description = input("Write what you want to send. \n")     
        str_to_send = "Send "
        str_to_send += destination
        str_to_send += " "
        str_to_send += description
        client.send(str_to_send.encode('ascii'))    
            

    elif msg == "Receive":
        receive_event.clear()
        client.send(msg.encode('ascii'))
        print("Client is waiting")
        receive_event.wait()
    
    elif msg == "List":
        receive_event.clear()
        client.send(msg.encode('ascii'))     
        receive_event.wait()
    else:
        print("The command you enteres was not correct. Please try again.") 
    return end

name = input("Please enter your ID name: \n")  
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((host, port))


client.send(name.encode('ascii'))     
handshaking_msg = client.recv(BUFFER_SIZE)
while handshaking_msg.decode('ascii') != "OK":
    handshaking_msg = client.recv(BUFFER_SIZE)

recieveThread = threading.Thread(target = recieveMessages)
recieveThread.daemon = True
recieveThread.start()


end = False
while not end:
    print("Enter your command please:")
    msg = input() 
    end = process_msg(msg)

client.close() 
