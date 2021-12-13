"""
This file have the class for
create a server.
"""

from flask import Flask, jsonify, request, send_file
from helpers.utils import get_files_paths, get_files_object, validate_config_file, get_ip_client
from models.client import Client
from settings.port import PORT_DEFAULT
from optparse import OptionParser

class Server:
  """
  Create a server with a name
  and a port.
  """

  def __init__(self, nameServer:str):
    self.nameServer = nameServer

    # gettings the config file with the files path to convert to objects File
    self.options = self.get_options_config_file()
    config_file = self.options.config_file

    if validate_config_file(config_file):
        files_paths = get_files_paths(self.options.config_file)
        files = get_files_object(files_paths)

        # starting the server
        self.app = Flask(self.nameServer)
        print( f'\nServing {len(files)} Files from {config_file}... ' ) # showing a message

        @self.app.route('/', methods = ['GET'])
        @self.app.route('/home', methods = ['GET'])
        def principal():
            """
            This is for the principal route of the page.
            """

            # validating the ip
            ip_client = get_ip_client(request)

            client = Client(ip_client)
            isValid = client.validate_client()

            if not isValid:
                return jsonify({
                    "message": "Your machine not is permitied for this server :("
                })

            files_paths = get_files_paths(self.options.config_file)
            files = get_files_object(files_paths)

            return jsonify({
                "currentsFiles": {
                    "id": [f.id for f in files],
                    "paths": [f.path for f in files]
                }
            })


        @self.app.route('/get-file/<string:id>', methods=['GET'])
        def get_file(id):
            """
            Return the file
            segun the id passed for parameter
            """

            ip_client = get_ip_client(request)

            client = Client(ip_client)
            isValid = client.validate_client()

            if not isValid:
                return jsonify({
                    "message": "Your machine not is permitied for this server :("
                })

            files_paths = get_files_paths(self.options.config_file)
            files = get_files_object(files_paths)

            try:
                # getting for return it
                file_to_render = files[int(id)].path
                # return send_file(file_to_render)

                # getting the lines and returning the information
                try:
                    with open(file_to_render, 'r') as f:
                        lines = f.readlines()

                    return jsonify({
                        "id": id,
                        "path": file_to_render,
                        "content": lines
                    })

                # in case the request of the file be a fhoto or other.
                except UnicodeDecodeError:
                    lines = ''
                    with open(file_to_render, 'rb') as f:
                        lines = f.readlines()

                    # return jsonify({
                    #     "id": id,
                    #     "path": file_to_render,
                    #     "content-image": content
                    #     }) # sending the file

                    return jsonify({
                        "id": id,
                        "path": file_to_render,
                        "content": [str(line) for line in lines]
                        }) # sending the file

                    # return send_file(file_to_render) # this is form is discart

            # in case the file not found
            except FileNotFoundError:
                return jsonify({
                    "response": "The request is a file. Not found !!!"
                })

            # if is a directory
            except IsADirectoryError:
                return jsonify({
                    "response": "The request is a directory"
                })

            # if id not in the list
            except IndexError:
                return jsonify({
                    "response": "Id not found"
                })

        @self.app.route('/add-path/', methods = ['POST'])
        def add_path():
            """
            This is the route for add a path
            to file to configuration.
            """

            ip_client = get_ip_client(request)

            client = Client(ip_client)
            isValid = client.validate_client()

            if not isValid:
                return jsonify({
                    "message": "Your machine not is permitied for this server :("
                })

            files_paths = get_files_paths(self.options.config_file)
            files = get_files_object(files_paths)

            try:
                # getting path to add at the the file config.txt
                path_to_add = request.form['path']

                #  writing in the file
                with open(config_file, 'r') as f:
                    lines = f.readlines()

                with open(config_file, 'w') as f:
                    lines.append(path_to_add)

                    for line in lines:
                        f.write(line.strip('\n') + '\n')

                # gettings the new files after the writing
                files_paths = get_files_paths(self.options.config_file)
                files = get_files_object(files_paths)

                return jsonify({
                    "message": f"Adding the path {path_to_add} to {config_file}",
                    "currentsFiles": {
                        "id": [f.id for f in files],
                        "paths": [f.path for f in files]
                    }
                })

            except KeyError:
                return jsonify({
                    "message": "The request is invalid, must be path=data. Post failded."
                })

        @self.app.route('/update-path/<string:id>', methods = ['PUT'])
        def update_path(id):
            """
            This is the route for update
            a path in the file config.txt
            """

            ip_client = get_ip_client(request)

            client = Client(ip_client)
            isValid = client.validate_client()

            if not isValid:
                return jsonify({
                    "message": "Your machine not is permitied for this server :("
                })

            id = int(id)

            # getting for get the old and new path
            files_paths = get_files_paths(self.options.config_file)
            files = get_files_object(files_paths)

            try:
                # getting the old and new paths
                old_path = files[int(id)].path
                new_path = request.form['path']

                with open('config.txt', 'r+') as f:
                    f.readlines()
                # gettings the new files after the writing
                files_paths = get_files_paths(self.options.config_file)
                files = get_files_object(files_paths)

                # getting the new and old path of the config file
                new_path = str(request.form['path'])
                old_path = str(files[id].path)

                #  reading and writing in the file
                with open(config_file, 'r') as f:
                    lines = f.readlines()

                with open(config_file, 'w') as f:
                    for line in lines:
                        if line == old_path + '\n':
                            f.write(new_path + '\n')

                        else:
                            f.write(line)

                    f.truncate() # reloading the file

                # gettings the new files after the writing
                new_files_paths = get_files_paths(self.options.config_file)
                new_files = get_files_object(new_files_paths)

                return jsonify({
                    "message": f"Path number {id} upated",
                    "fileUpdated": {
                        "id": id,
                        "oldPath": old_path,
                        "newPath": new_path
                    },
                    "currentsFiles": {
                        "id": [f.id for f in new_files],
                        "path": [f.path for f in new_files]
                    }
                })

            # in case the request is invalid
            except KeyError:
                return jsonify({
                    "message": "The request data must be path=data. Put failded."
                })

            # in case the id of the request not found
            except IndexError:
                return jsonify({
                    "message": "Id not found"
                })

        @self.app.route('/delete-path/<string:id>', methods = ['DELETE'])
        def delete_path(id):
            """
            This route is for delete a
            path of the config file. For not 
            render in the server.
            """

            ip_client = get_ip_client(request)

            client = Client(ip_client)
            isValid = client.validate_client()

            if not isValid:
                return jsonify({
                    "message": "Your machine not is permitied for this server :("
                })

            # getting for get the old and new path
            files_paths = get_files_paths(self.options.config_file)
            files = get_files_object(files_paths)

            try:
                id = int(id)
                OLD_PATH = files[int(id)].path

                # this is the code for delete of the file
                with open('config.txt', 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        if line != OLD_PATH + '\n':
                            f.write(line)

                    f.truncate()

                return jsonify({
                    "message": f"Path number {id} deleted",
                    "fileDelete": {
                        "id": id,
                        "path": OLD_PATH
                    }
                })

            except IndexError:
                return jsonify({
                    "message": "The request is a file. Not found in the server !!"
                })
    else:
        print('\nPut a config file valid. Seee --help.')

  def start(self):
    """
    Start the server with the port
    passed for parameter in the constructor.
    """

    try:
        # getting and validating the port for runn the app
        PORT = int(self.options.port)
        self.app.run(host = '0.0.0.0', port = PORT, debug = True)

    except TypeError:
        self.app.run(host = '0.0.0.0', port = PORT_DEFAULT, debug = True)


  def get_options_config_file(self) -> tuple:
      """
      Return a tuple with the the files
      to render in the server.
      """

      parser = OptionParser()
      parser.add_option('-f', '--file', dest = 'config_file', help = 'Put the config file with the paths of the files for render.')
      parser.add_option('-p', '--port', dest = 'port', help = 'Put the port of the list the server. The port for default is 4000.')

      options, args = parser.parse_args()

      # validating in case not options passed
      if not options.config_file:
          parser.error('Put the config file to render. Help with --help')

      return options


  def __str__(self) -> str:
      return 'This is a Server for files.'
