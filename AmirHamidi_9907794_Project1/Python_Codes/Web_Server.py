from socket import *
import os
import sys

# DNS Server's IP Address and Port Number
DNS_IP_Address = "127.0.0.1"
DNS_Port_Number = 5000

# Default Value Of IP Address And Port Number For Web Server
Web_IP_Address = "127.0.0.1"
Web_Port_Number = 8080

# Deliver IP Address And Port Number With Argument Values (Optional)
if len(sys.argv) == 3:

    if sys.argv[1] == "-i":

        Web_IP_Address = sys.argv[2]

    elif sys.argv[1] == "-p":

        Web_Port_Number = int(sys.argv[2])

elif len(sys.argv) == 5:

    if (sys.argv[1] == "-i") & (sys.argv[3] == "-p"):

        Web_IP_Address = sys.argv[2]
        Web_Port_Number = int(sys.argv[4])

    elif(sys.argv[1] == "-p") & (sys.argv[3] == "-i"):

        Web_IP_Address = sys.argv[4]
        Web_Port_Number = int(sys.argv[2])

SpecsSocket = socket(AF_INET, SOCK_DGRAM)
Hostname = f"Specs {Web_IP_Address} {Web_Port_Number}".encode("UTF-16")
SpecsSocket.sendto(Hostname, (DNS_IP_Address, DNS_Port_Number))
Answer, ServerAddress = SpecsSocket.recvfrom(512)
SpecsSocket.close()

# Construction Of The TCP Connection (Server Side)
Web_ServerSocket = socket(AF_INET, SOCK_STREAM)
Web_ServerSocket.bind((Web_IP_Address, Web_Port_Number))
Web_ServerSocket.listen(1)
print(f"\n{Answer.decode('UTF-16')}")
print("The Web server is ready to receive")
print(f"IP Address = {Web_IP_Address}, Port Number = {Web_Port_Number}\n")


while True:

    ConnectionSocket, ClientAddress = Web_ServerSocket.accept()
    Message = ConnectionSocket.recv(512).decode("UTF-16")

    spaces = 0
    First_Space = 0
    Second_Space = 0

    # Parsing Different Parameters Of The Message
    for i in range(len(Message)):

        if Message[i] == " ":

            spaces += 1

            if spaces == 1:

                First_Space = i

            elif spaces == 2:

                Second_Space = i
                break

    cr_lf = "\r\n"
    m = len(cr_lf)
    F_cr_lf = 0

    # cr_lf
    for i in range(len(Message)-m):

        if Message[i:i+m] == cr_lf:

            F_cr_lf = i
            break

    Method = Message[0:First_Space]
    URL = Message[First_Space+1:Second_Space]
    Version = Message[Second_Space+1:F_cr_lf]

    print("Hypertext Transfer Protocol:")
    print(f"Request Method: {Method}")
    print(f"Request URL: {URL}")
    print(f"Request Version: {Version}")
    print(f"{Message[F_cr_lf + len(cr_lf):]}\n")

    # Extracting Different Part Of URL And Finding Requested File (If Exists)
    Number_of_Slashes = 0
    n = len(URL)
    a = 0

    if n >= 1:

        for i in range(n):

            if URL[i] == "/":
                Number_of_Slashes += 1

        k = list(range(Number_of_Slashes))

        for i in range(n):

            if URL[i] == "/":
                k[a] = i
                a += 1

        if Number_of_Slashes == 1:

            Part1 = URL[0:k[0]]
            Part2 = URL[k[0] + 1:]
            f1 = 0
            f2 = 0
            g = 0

            while g == 0:

                sub0 = os.listdir("Files Directory")

                if sub0[f1] == Part1:

                    sub1 = os.listdir("Files Directory" + "/" + Part1)

                    while g == 0:

                        if sub1[f2] == Part2:

                            data = open("Files Directory" + "/" + Part1 + "/" + Part2)
                            Answer = data.read()
                            data.close()
                            ConnectionSocket.send(Answer.encode("UTF-16"))
                            ConnectionSocket.close()
                            g = 1

                        else:

                            f2 = f2 + 1

                            if f2 == len(sub1):

                                Answer = "404 NOT FOUND"
                                ConnectionSocket.send(Answer.encode("UTF-16"))
                                ConnectionSocket.close()
                                g = 1

                else:

                    f1 = f1 + 1

                    if f1 == len(sub0):

                        Answer = "404 NOT FOUND"
                        ConnectionSocket.send(Answer.encode("UTF-16"))
                        ConnectionSocket.close()
                        g = 1

        elif Number_of_Slashes == 2:

            Part1 = URL[0:k[0]]
            Part2 = URL[k[0] + 1:k[1]]
            Part3 = URL[k[1] + 1:]
            f1 = 0
            f2 = 0
            f3 = 0
            g = 0

            while g == 0:

                sub0 = os.listdir("Files Directory")

                if sub0[f1] == Part1:

                    sub1 = os.listdir("Files Directory" + "/" + Part1)

                    while g == 0:

                        if sub1[f2] == Part2:

                            sub2 = os.listdir("Files Directory" + "/" + Part1 + "/" + Part2)

                            while g == 0:

                                if sub2[f3] == Part3:

                                    data = open("Files Directory" +
                                                "/" + Part1 + "/" + Part2 + "/" + Part3)
                                    Answer = data.read()
                                    data.close()
                                    ConnectionSocket.send(Answer.encode("UTF-16"))
                                    ConnectionSocket.close()
                                    g = 1

                                else:

                                    f3 = f3 + 1

                                    if f3 == len(sub2):
                                        Answer = "404 NOT FOUND"
                                        ConnectionSocket.send(Answer.encode("UTF-16"))
                                        ConnectionSocket.close()
                                        g = 1

                        else:

                            f2 = f2 + 1

                            if f2 == len(sub1):
                                Answer = "404 NOT FOUND"
                                ConnectionSocket.send(Answer.encode("UTF-16"))
                                ConnectionSocket.close()
                                g = 1

                else:

                    f1 = f1 + 1

                    if f1 == len(sub0):
                        Answer = "404 NOT FOUND"
                        ConnectionSocket.send(Answer.encode("UTF-16"))
                        ConnectionSocket.close()
                        g = 1

        else:

            Answer = "404 NOT FOUND"
            ConnectionSocket.send(Answer.encode("UTF-16"))
            ConnectionSocket.close()

    else:

        Answer = "404 NOT FOUND"
        ConnectionSocket.send(Answer.encode("UTF-16"))
        ConnectionSocket.close()
