import os, socket
import urllib.request

def handle_client(c):
    hdr = c.recv(1024).decode("utf-8")
    url = hdr.split(' ')[1]
    print(url, "=> downloading")
    data = urllib.request.urlopen(url).read()
    print(url, "=> fetched, len:", len(data))
    c.send("HTTP/1.1 200 OK\r\n".encode("utf-8"))
    c.send(("Content-Length: " + str(len(data)) + "\r\n").encode("utf-8"))
    c.send("Connection: close\r\n".encode("utf-8"))
    c.send("\r\n".encode("utf-8"))
    c.sendall(data)
    c.shutdown(socket.SHUT_RDWR)
    c.close()


# config proxy for urllib if needed
#proxy_handler = urllib.request.ProxyHandler({'http': 'http://PROXY_ADDRESS:PORT'})
#opener = urllib.request.build_opener(proxy_handler)
#urllib.request.install_opener(opener)


# set listen address and port here
host = "0.0.0.0"
port = 8080
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(100)

while True:
    c, addr = s.accept()
    pid = os.fork()
    if pid == 0:
        handle_client(c)
        break

