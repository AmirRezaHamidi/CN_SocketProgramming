from socket import *
import json
import sys

# DNS Server's IP Address and Port Number
DNS_IP_Address = "127.0.0.1"
DNS_Port_Number = 5000

# Default Value Of IP Address And Port Number For Web Server
Web_IP_Address = "127.0.0.1"
Web_Port_Number = 8080

# Construction Of The UDP Connection (Server Side)
ServerSocket = socket(AF_INET, SOCK_DGRAM)
ServerSocket.bind((DNS_IP_Address, DNS_Port_Number))
print("\nThe DNS server is ready to receive")
print(f"IP Address = {DNS_IP_Address}, Port Number = {DNS_Port_Number}")

while True:

    Message, ClientAddress = ServerSocket.recvfrom(512)
    Message = Message.decode("UTF-16")

    if Message[0:5] == "Specs":

        Specs = list(Message.split(" "))
        Web_IP_Address = Specs[1]
        Web_Port_Number = Specs[2]
        Answer = "DNS Server has received Web Specification"
        ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

    elif Message == "WEB_Server":

        Answer = f"{Web_IP_Address} {Web_Port_Number}"
        ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

    else:

        n = len(Message) - 1
        dns_data = open("DNS_Database.json")

        if len(sys.argv) == 2:

            dns_data = open(sys.argv[1])

        host2ip = json.load(dns_data)

        if n >= 0:

            # Finding The First "." Symbol
            while Message[n] != ".":

                n = n-1

                if n <= 0:

                    break

            # "." Symbol Is In The Middle
            if n != 0:

                Suffix = Message[n + 1:]
                n = n-1
                Suf = host2ip["root"]["domains"]   # .com, .edu, .org

                if Suffix in Suf:

                    # Finding The Second "." Symbol (If Exists)
                    while Message[n] != ".":

                        n = n-1

                        if n == 0:

                            break

                    # Available Domains In Each Suf, Like google.com In .com Suf
                    Dom = Suf[Suffix]

                    # Main Domain Is Requested
                    if n == 0:

                        Domain = Message

                        if Domain in Dom:

                            IP = Dom[Domain]["ip"]
                            Port = Dom[Domain]["port"]
                            Answer = f"IP = {IP}, Port: {Port}"
                            ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

                        else:

                            Answer = "This hostname is not valid"
                            ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

                    # Subdomain Is Requested
                    else:

                        Domain = Message[n + 1:]
                        SubDomain = Message

                        if Domain in Dom:

                            Sub = Dom[Domain]["subdomain"]
                            # For Example sub1.google.com In google.com

                            if SubDomain in Sub:

                                IP = Sub[SubDomain]["ip"]
                                Port = Sub[SubDomain]["port"]
                                Answer = f"IP = {IP}, Port: {Port}"
                                ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

                            else:

                                Answer = "This Hostname is not valid"
                                ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

                        else:

                            Answer = "This Hostname is not valid"
                            ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

                else:

                    Answer = "This Hostname is not valid"
                    ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

            else:

                Answer = "This Hostname is not valid"
                ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)

        else:

            Answer = "This Hostname is not valid"
            ServerSocket.sendto(Answer.encode("UTF-16"), ClientAddress)
