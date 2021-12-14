"""
This is the principal
file for execute the server.

You can put the paths of the files to render
in a file for example config.txt or other. Yout must put of this form, a for each line (without spaces in the end)):
/home/youUser/hola.txt
/home/youUser/Desktop/img.jpg

With the option -p or --port, you can pass a number port, for example 6000 (for default is the port 4000):
Sample: python3 main.py -f config.txt -p 6000
(You can change the port for default in ./settings/port.py)

You can choice the method for validate the ip of the client.

In alls the routes validate the client ip. if the ip of the client not is valid, with the method of the
list or range, not can recived the information.

With the option -i or --ips, you can choice the file, where is the ips allows in the server.
If the option -i or --ips, not is pass. For default the method for validate the ip of the client
is range.

If your choice the method for range, you must edit the list in this file: ./settings/ip_allows.py,
must put the first ip of the range, and the second ip of the range.

"""

from models.server import Server

if __name__ == '__main__':
    # creating and starting the server
    filesServer = Server('files-server')
    filesServer.start()