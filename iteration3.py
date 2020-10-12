#!/usr/bin/python

import threading, socket, sys, time
from optparse import OptionParser
from queue import Queue
from termcolor import colored

# no more than one thread will access this variable at the same time
# this is to prevent race condition
print_lock = threading.Lock()
# creates the queue
q = Queue()
# defines the number of ports that will be scanned
ports = 1024


# Validates if the given host is a valid host
def hostScan(tgtHost):
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
    return tgtIP


# This will scan ports without using threads
def portScan(tgtHost):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
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


# This will scan ports using the given number of threads
def threadScan(thr, tgtIP):
    # this allows only the given number of threads (thr)
    for p in range(thr):
        t = threading.Thread(target=threader, args=(tgtIP,))
        t.daemon = True     # the thread will die when the main dies
        t.start()
    # the number of jobs assigned to threads is the number of ports I want to scan
    for worker in range(1, ports):
        q.put(worker)
    # it waits until the thread terminates
    q.join()


# Scans a port in the given host, this is the job for the threads
def scan(port, tgtHost):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        try:
            con = sock.connect((tgtHost, port))
            with print_lock:
                print(colored(str(port) + ' Open', 'green'))
            con.close()
        except:
            pass
            # in case you want to print closed ports, uncomment next 2 lines and delete the pass statement
            # but this won't be efficient using threads
            # with print_lock:
            #     print(colored(str(port) + ' Closed', 'red'))
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


# it pulls a worker from the queue and processes it
def threader(tgtHost):
    while True:
        worker = q.get()
        scan(worker, tgtHost)
        q.task_done()

def main():
    usage = "usage: %prog [-t <threads>] [-f] -H <host>"
    parser = OptionParser(usage = usage)
    parser.add_option('-t', dest='thr', type='int', help='specify number of threads')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-f', action='store_true', help='uses threads')
    (options, args) = parser.parse_args()

    if options.tgtHost is None:
        parser.error("Incorrect number of arguments")
    else:
        tgtHost = options.tgtHost

    # sets the number of threads in 5 by default
    if options.thr is None:
        thr = 5
    else:
        thr = options.thr

    tgtIP = hostScan(tgtHost)
    if (tgtIP != 0):
        if options.f == True:
            print("Scanning without using threads...")
            portScan(tgtIP)
        else:
            print("Scanning using threads...")
            threadScan(thr, tgtHost)


if __name__ == '__main__':
    main()