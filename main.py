"""
This is the principal
file for execute the server.

You can put the paths of the files to render
in a file for example config.txt or other. Yout must put of this form, a for each line (without spaces in the end)):
/home/youUser/hola.txt
/home/youUser/Desktop/img.jpg

With the option -p or --port, you can pass a number port, for example 6000 (for default is the port 4000):
python3 main.py -f config.txt -p 6000

In alls the routes validate the client ip. If the ip of the client
not is permitied in the file ./settings/ip_allows.py. The client not can
recived the information.

"""

from models.server import Server

if __name__ == '__main__':
    filesServer = Server('files-server')
    filesServer.start()