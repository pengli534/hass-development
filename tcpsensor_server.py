__author__ = 'pl534'

import socket
import argparse

host = '0.0.0.0'
data_payload = 2048
backlog = 5
ack = '23.24'

def echo_server(port):
    sock = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (host, port)
    print "Starting up echo server on %s port %s" % server_address
    sock.bind(server_address)
    sock.listen(backlog)

    while True:
        print 'Waiting to receiving message from client'
        client, address = sock.accept()
        data = client.recv(data_payload)
        if data:
            print 'Data: %s' % data
            # there is big difference comapare to sock.sendall(msg) in the client
            client.send(ack)
            print 'Sent: %s back to %s' % (ack, address)
        client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action='store', dest='port', type=int, required=True)
    given_arg = parser.parse_args()
    port = given_arg.port
    echo_server(port)

