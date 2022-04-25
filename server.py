#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  server.py
#  
#  Copyright 2022 cyber venom <venom@V3N0M>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
"""
 Implements a simple HTTP/1.0 Server

"""

import socket,sys
ip = socket.gethostbyname(socket.gethostname())
# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = int(input("Enter the port number in which you'll set up the http service: "))
ex = 0
if SERVER_PORT > 65536:
	ex = 1
if SERVER_PORT > 11000:
	ex = 1
if SERVER_PORT <10000:
	ex = 1

if ex == 1:
	print("ERROR MAKE SURE PORT ARGUMENTS ARE LESS THAN 65536 AND BETWEEN 10000 TO 11000.")
	sys.exit()
else:
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)
    ctl, addr = server_socket.accept()

    while True:    
	
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        if "GET" in request:
            #port_c= request[request.index('username-')+1:request.rindex('="')]
            print(f"{addr}:GET")
            print(request)
            # Parse HTTP headers
            headers = request.split('\n')
            filename = headers[0].split()[1]

            # Get the content of the file
            if filename == '/':
                filename = '/index.html'

            try:
                with open('/opt/lampp/htdocs/chaty/'+filename, encoding="utf8", errors='ignore') as f: #errors generated are ignored remember to change the path to your desired file path
                    #f = open('/opt/lampp/htdocs/chaty/' + filename) #this line is avoided because the server may crash when sending image files
                    content = f.read()
                    f.close()
                    response = 'HTTP/1.0 200 OK\n\n' + content
            except FileNotFoundError:
                with open('/opt/lampp/htdocs/chaty/404err.html', encoding="utf8", errors='ignore') as e:
                    cont = e.read()
                    e.close()
                    response = 'HTTP/1.0 404 NOT FOUND\n\n'+cont
    
            # Send HTTP response
            client_connection.sendall(response.encode())
            client_connection.close()
        elif "PUT" in request:
            print("PUT")
    # Close socket
    server_socket.close()
			
