# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 10:37:43 2019

@author: Mohammad_Younesi
"""

import socket
import threading
import time

ENCODING = 'utf-8'
maxActiveConnection = 10

class Receiver(threading.Thread):
    def __init__(self,myHost,myPort):
        threading.Thread.__init__(self, name = "receiver")
        self.host = myHost
        self.port = myPort
        self.is_alive = True
    
    def listen(self):
        mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySock.bind((self.host, self.port))
        mySock.listen(maxActiveConnection)
        connection, clientAddress = mySock.accept()
        while(True):
            data = connection.recv(1024)
            message = data.decode(ENCODING)
            if not data:
                break
            print("{}: {}".format(clientAddress, message.strip()))
                
        connection.close()
    def run(self):
        self.listen()

class Sender(threading.Thread):
    def __init__(self,myPeerHost,myPeerPort):
        threading.Thread.__init__(self, name="sender")
        self.host = myPeerHost
        self.port = myPeerPort
        self.is_alive = True
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host,self.port))
        msg = input("")
        while(msg != 'exit'):
            s.sendall(msg.encode(ENCODING))
            msg = input("")
    
        s.close()
            
def main():
    myHost = input("please enter my host: ")
    myPort = int(input("please enter my port number: "))
    receiver = Receiver(myHost , myPort)
    print("a user at " + receiver.host + " with port number: " + str(receiver.port) + " is waiting for a peer to join." )
    print("Connecting ... ")
    time.sleep(1)
    myPeerHost = input("please enter the peer's host: ")
    myPeerPort = int(input("please enter the peer's port number: "))
    sender = Sender(myPeerHost,myPeerPort)
    print("Connecting ... ")
    time.sleep(1)
    print("peer has joined. ")
    receiver.start()
    sender.start()
    
    
if __name__ == '__main__':
    main()
    
                
                        
                    
        