#!/usr/bin/python

import threading, socket, sys, optparse
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
    parser = optparse.OptionParser('Usage of program: ' + '[-t <threads>] <target host>')
    parser.add_option('-t', dest='thr', type='int', help='specify number of threads')
    (options, args) = parser.parse_args()
    
    # If it gets only 1 argument, this will be the host name
    if len(sys.argv) == 2:
        tgtHost = sys.argv[1]
        thr = 5
    
    # If it gets 3 arguments, should be the flag and the host name 
    elif len(sys.argv) == 4:
        tgtHost = sys.argv[3]
        thr = int(options.thr)

    # Any other ammount of arguments is not valid
    else:
        print(parser.usage)
        sys.exit()
    
    # If you want to double check the Target host and number of threads, uncomment next 2 lines
    # print("Target host: ", tgtHost)
    # print("Threads: ", thr)

    # it gets the IP address from the host name
    tgtIP = hostScan(tgtHost)
    if (tgtIP):
        # it allows only the given number of threads (thr)
        for p in range(thr):
            t = threading.Thread(target=threader, args=(tgtIP,))
            t.daemon = True     # the thread will die when the main dies
            t.start()
        # the number of jobs assigned to threads is the number of ports I want to scan
        for worker in range(1, ports):
            q.put(worker)
        # it waits until the thread terminates
        q.join()

if __name__ == '__main__':
    main()