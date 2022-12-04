from socket import *

# DNS Server's IP Address and Port Number
DNS_IP_Address = "127.0.0.1"
DNS_Port_Number = 5000

while True:

    # Receiving The Request
    Request = input("\nenter you Request:")

    # Remove The Spaces At The End
    while True:

        if Request[-1] == " ":

            Request = Request[0:len(Request)-1]

        else:

            break

    # DNS Command
    if Request[0:3].lower() == "dns":

        # Construction Of The UDP Connection (Client Side)
        Hostname = Request[4:]
        ClientSocket = socket(AF_INET, SOCK_DGRAM)
        ClientSocket.sendto(Hostname.encode("UTF-16"), (DNS_IP_Address, DNS_Port_Number))
        Answer, ServerAddress = ClientSocket.recvfrom(512)
        print("\nMessage From DSN Server:\n" + Answer.decode("UTF-16"))
        ClientSocket.close()

    # HTTP Command
    elif Request[0:4].lower() == "http":

        # Make The "Request" Compatible with TCP Connections (Client Side)
        if len(Request) >= 7:

            # UDP Connection To DNS Server
            ClientSocket = socket(AF_INET, SOCK_DGRAM)
            Hostname = "WEB_Server"
            Hostname = Hostname.encode("UTF-16")
            ClientSocket.sendto(Hostname, (DNS_IP_Address, DNS_Port_Number))
            Answer, ServerAddress = ClientSocket.recvfrom(512)
            Answer = Answer.decode("UTF-16")
            Specs = list(Answer.split(" "))
            ClientSocket.close()

            # TCP Connection To Web Server
            WEB_IP_Address = Specs[0]
            WEB_Port_Number = int(Specs[1])
            ClientSocket = socket(AF_INET, SOCK_STREAM)
            ClientSocket.connect((WEB_IP_Address, WEB_Port_Number))
            URL = Request[5:]

            Message = f"GET {URL} HTTP/1.1\r\n" \
                      f"Host: Web_Server.py\r\n" \
                      f"Connection: close\r\n" \
                      f"User-agent: Client_Server.py\r\n" \
                      f"Accept-language: en-US"

            ClientSocket.send(Message.encode("UTF-16"))
            Answer = ClientSocket.recv(512)
            print("\nMessage From Web Server:\n" + Answer.decode("UTF-16"))
            ClientSocket.close()

        else:

            print("\nhttp Requests should be 7 characters or more")

    # Exit Command
    elif Request.lower() == "exit":

        print("\nGoodbye, we hope to see you again soon :)")
        break

    # Invalid Commands
    else:

        print("\nERROR:\nInvalid Command (choose between dns, http and exit)")
