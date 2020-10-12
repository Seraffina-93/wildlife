#!/usr/bin/python

from termcolor import colored
import sys, socket

# defines the number of ports that will be scanned
ports = 1024

# checks if IP is valid and scans first 1024 forts
def portScan(tgtHost):
    # validates if hostname/IP is valid
    try:
        tgtIP = socket.gethostbyname(tgtHost)
    except:
        print(colored("[!!] Unknown host %s " % tgtHost, 'red'))
        sys.exit()
    try:
        tgtName = socket.gethostbyaddr(tgtIP)
        print("[+] Scan results for: " + tgtName[0])
    except:
        print("[+] Scan results for: " + tgtIP)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)

    # this will scan ports between 1 and 1024
    try:
        for port in range(1, ports):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                con = sock.connect((tgtHost, port))
                print(colored("%d Open" % port, 'green'))
                con.close()
            except:
                pass
                #in case you want to print closed ports, uncomment next line and delete the pass statement
                #print(colored("%d Closed" % port, 'red'))
            finally:
                sock.close()     
    
    except KeyboardInterrupt: 
        print(colored("[!!] Exitting program", 'red')) 
        sys.exit() 
    except socket.gaierror: 
        print(colored("[!!] Hostname could bot be resolved", 'red')) 
        sys.exit() 
    except socket.error: 
        print(colored("[!!] Server not responding", 'red')) 
        sys.exit()


def main():
    # verifies that the host name is given
    if len(sys.argv) == 2:
        tgtHost = sys.argv[1]
        portScan(tgtHost)
    else:
        print("Invalid ammount of aguments")


if __name__ == '__main__':
    main()
