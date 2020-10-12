# Programming challenge

This is a programming challenge given by Wildlife. It consists in 5 iterations.

For solving this challenge, I used Python 3 on my MacBook Pro with macOS Catalina V10.15.5. In order to test the Port Scanners, I used a virtual machine with Metasploitable 2 and my localhost.

## Iteration 1
This is a simple port scanner. For this iteration, I used the modules sys, socket and termcolod. 

Usage of the program:
```
$ iteration1.py <target host>
```

## Iteration 2
This is a port scanner that uses threads in order to optimize the work. You can specify the number of thread with the optional flag -t otherwise it will use 5 by default. For this iteration I used the modules sys, socket, threading, optparse, queue and termcolor.

Usage of the program:
```
$ iteration2.py [-t <threads>] <target host>
``` 

## Iteration 3
This port scanner allows you to decide if you want to use threads or not. Threads are used by default, if you use the flag -f the threads will not be used, even if you specified them.

Usage of the program:
```
$ iteration3.py [-t <threads>] [-f] -H <target host>
``` 

## Iteration 4
This port scanner is very simmilar to the last one, but it will also tell you if the open port is a HTTP server. 

Usage of the program:
```
$ iteration4.py [-t <threads>] [-f] -H <target host>
``` 

![Results from Iteration 4](https://github.com/Seraffina-93/wildlife/blob/master/demo.png)

## Iteration 5
For this iteration a dockerized the Port Scanner from Iteration 4. 
Usage of the program:
```
$ iteration1.py [-t <threads>] [-f] -H <target host>
``` 
