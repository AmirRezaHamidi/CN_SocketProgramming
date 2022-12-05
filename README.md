# Application layer and socket programming

In this project, we have implemented a web system using python. A web system in its simplest form is comprised of three components. These three components are web client, web server, and DNS server. In the real world, each of the mentioned components is an intricate software system with enormous implementation considerations, but here we have implemented a simplified version of these systems.

<p align="center">
 <img src="Images/Overall%20System.png" >
</p>

In this simplified web system, a user enters a request using the web client. Then web client finds the request’s destination IP address and port from the DNS server. After that, the web client sends a request to the appropriate web server, and the web server searches in its file directory for the requested file. If the file exists, it sends back found file. Otherwise, replies with a 404 NOT FOUND.

## Part 1: DNS server
In a nutshell, DNS severs’ job is to receive domain names like google.com and translate them into IP addresses. In this part, you will implement software that uses a textbase file as its database, and whenever a request comes tries to translate the domain name stated in the request into an IP address and a port number and return these two to the client.
A single domain can have so many subdomains. As an example, take kntu.ac.ir as a domain. This domain has multiple subdomains like vc.kntu.ac.ir for its online class platform, ee.kntu.ac.ir for its electrical engineering website, and so on.
Here we have used a JSON file as the database for the DNS server. An example of this file in this project is as follow:

    {  
       "root": {  
           "domains": {  
               "com-network.com": {  
                   "ip": "192.168.1.103",  
                   "port": "8080",  
                   "domains": {
                       "sub1.com-network.com": {
                           "ip": "192.168.1.107",
                           "port": "8080",
                           "domains": {}
                       },
                       "sub2.com-network.com": {
                           "ip": "192.168.1.109",
                           "port": "8081",
                           "domains": {}
                       }
                   }
               }
           }
       }
    }

### Notes
1.	The format above is an example and we have used a different, bigger structure.
2.	DNS server runs above UDP protocol and port 53, but we have used port 5353 in this project.
3.	In communication with this DNS server, you can adopt whatever format (message structure) you like.
4.	Our program is be able to cope with dynamic changes in the jason file during runtime. So, for example, if you change one IP when the server is active, you get the updated IP in subsequent responses.
5.	We have used arguments for setting up the configurations instead of hard-coding them like port numbers.

### Steps
1.	a Generated JSON file as our database and we have putted it in our DNS server directory.
2.	a Created UDP socket with port 5353.
3.	Listen and wait for incoming requests on this port.
4.	Whenever we receive a request we will:  
  a.	Validate it, if it’s invalid, we will drop it.  
  b.	If it's valid, we look into our database for request objectives.  
  c.	Create a response and send it back to the client.  

## Part 2: Web Server
our web server listens on port 8080 for any incoming HTTP requests. After receiving a request, this server looks in its file directories for requested files. If it finds the requested file, it sends back that file. Otherwise, it sends back 404 NOT FOUND. A sample file directory structure for this web server can be seen below.
 
<p align="center">
 <img src="Images/Directory.png"  >
</p>

As you can see, this sample directory structure has similarities to our previous example, which was the DNS server’s database file.

### Notes
1.	our model is able to cope with modification of the files directory at runtime without restarting the server. These modifications include:  
  a.	Adding new domain directory  
  b.	Editing existing domains name  
  c.	Deleting existing domain  
  d.	Adding new file in any domain directory  
  e.	Editing any file in any domain directory  
  f.	Deleting any file in any domain directory  
2.	we have Used arguments for setting our configurations instead of hard-coding them. Like port numbers  

### Steps
1.	Created a file directory and generate some random files, and put them in our files directory.
2.	Created a TCP socket listening on port 8080.
3.	Listen and wait for incoming requests on this socket.
4.	Whenever we receive a request we will:  
  a.	Validate it to be a valid HTTP request.  
  b.	Parse its parameters and extract request file names.  
  c.	If we found these files in the appropriate domain, we will send them back to the client.  
  d.	Otherwise, we responde with 404 NOT FOUND.  


## Part 3: Web Client
In the real world, web clients are mostly web browsers, but we have implemented an interactive console-based web application in this project. This web client has three commands.
1.	exit
2.	http
3.	dns

with the exit command user simply closes the client app. The dns command is used when the user wants to send a DNS query to its DNS server. Usage of this command is as follow:

**dns google.com**

The result of this command is like this:

**[result] dns query result for google.com is 10.43.1.60 with port 80**

The last command is http. Using this command, you can send HTTP GET requests. An example of this command is:

**http com-network.com/tests?file=test.txt**

In this request, the web server looks for test.txt inside folder tests. The folder tests itself is inside the domain folder com-network.com. Upon receiving the response from the web server, the client will print the received response in the terminal.

### Steps
1.	Waiting for the user to enter a command.
2.	Upon receiving a command from the user, do as explained.
3.	Printing received result
4.	Repeating steps 1 to 3 until the user enters the exit command.
