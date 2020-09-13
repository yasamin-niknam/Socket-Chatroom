import socket 
from threading import Thread 


class ClientThread(Thread): 
 
    def __init__(self,ip,port, conn): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        self.conn = conn
        self.id = ""
        print("[+] New server socket thread started for " + ip + ":" + str(port) )
 
    def run(self): 

        global listening_threads

        self.id = (self.conn.recv(2048)).decode('ascii')
        
        OK = "OK"
        conn.send(OK.encode('ascii')) 

        while True : 
            data = (self.conn.recv(2048)).decode('ascii')
            list_of_words = data.split(" ")

            if list_of_words[0] == "List":
                MESSAGE = "\nYou can see the list of clients below: \n"
                for index in range(len(threads)):
                    MESSAGE += str(index+1) 
                    MESSAGE += ". "
                    MESSAGE += threads[index].id 
                    MESSAGE += "\n"
  
                self.conn.send(MESSAGE.encode('ascii'))
            
            elif list_of_words[0] == "Exit":
                for index in range(len(threads)):
                    if self.id == threads[index].id:
                        del threads[index]
                        break

            elif list_of_words[0] == "Send":
                dest_id = list_of_words[1]
                addition = ""
                str_to_send = "\nInterrupt: "
                for k in range(len(listening_threads)):
                    if listening_threads[k] == dest_id:
                        addition += "\n\nSent from " + self.id +" \n" 
                        str_to_send = "\n"
                        del listening_threads[k]
                        break

                temp = list_of_words[0] + " " +list_of_words[1] + " "
                description = data.replace(temp, '')
                description += addition

                for index in range(len(threads)):
                    if threads[index].id == dest_id:
                        threads[index].send_msg(description, str_to_send)
            
            elif list_of_words[0] == "Receive":
                listening_threads.append(self.id)
            else:
                MESSAGE = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
                if MESSAGE == 'exit':
                    break
                self.conn.send(MESSAGE.encode('ascii'))

    def send_msg(self, description, str_to_send):
        str_to_send += "You have recieved a message: \n"
        str_to_send += description
        str_to_send += " \n"
        str_to_send += "You can now enter your command again. \n"
        self.conn.send(str_to_send.encode('ascii'))


TCP_IP = socket.gethostname()
TCP_PORT = 9000 
BUFFER_SIZE = 2000
listening_threads = []

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print("Multithreaded Python server : Waiting for connections from TCP clients..." )
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port, conn) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join()    