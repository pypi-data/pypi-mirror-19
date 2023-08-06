# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 11:39:20 2016

@author: Krounet
e-mail : krounet@gmail.com
"""

import paramiko
import sys


class clienttoRasp:
    
   
    
    def __init__(self,hostname='1.1.1.1',port=22,identifier='pi',password='raspberry'):
        
        """Initialisation of the parameters. hostname : address of the raspberry on your Local Network,
        port=22 : port use for a SSH connection, identifier : identifier of the Raspberry,
        password : password of the Raspberry"""
        
        global ssh
        ssh=paramiko.SSHClient()
        self.hostname=hostname
        self.port=port        
        self.identifier=identifier
        self.password=password
        
        
    
    def connecting(self):
        
        """Function to connect to the Raspberry. This function return a feedback
        of the connection"""
        
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
        try:
            ssh.connect(self.hostname,self.port,self.identifier,self.password)
            feedback = '***Connection Established***'
            return feedback
            
        except Exception as e:
            feedback= '***Connection failed : '+str(e)+'***'
            return feedback
            sys.exit(1)
    
    def sendCommand(self,command):
        
        """Function to send a shell command to the Raspberry via SSH"""        
        
        try:
            stdin,stdout,stderr=ssh.exec_command(command)
            feedback= '*** Command is sent***'
            return feedback,stdin,stdout,stderr
        except Exception as e :
            print '***Command sending failed :'+str(e)+'***'
            sys.exit(1)
    
    def closeConnection(self):
        
        """Function to close the SSH connection with the Raspberry"""        
        
        try:
            ssh.close()
            feedback= '***Connection Closed***'
            return feedback
        except Exception as e:
            feedback= '***Connection failed to close :'+str(e)+'***'
            return feedback
            sys.exit(1)
        
            
if __name__ == '__main__':
    """Test of the class clienttoRasp. Don't forget to change the hostname
    to match with the Raspberry address on your local network.
    Do it too for the identifier and the password if you changed these parameters
    on your Raspberry"""
    import time
    print 'It is a test'
    a=ClienttoRasp(hostname='192.168.1.16',port=22,identifier='pi',password='raspberry')
    feedback_connecting=a.connecting()
    print feedback_connecting        
    feedback_sendCommand=a.sendCommand('ls')
    print feedback_sendCommand
    print '\n'.join(feedback_sendCommand[2].readlines())    
    feedback_closeConnection=a.closeConnection()
    print feedback_closeConnection
    print 'Good Bye'
    time.sleep(2)
    

         