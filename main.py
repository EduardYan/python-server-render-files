"""
This is the principal
file for execute the server.
"""

from flask import Flask, jsonify, request
from optparse import OptionParser
from helpers.utils import get_files_paths, get_files_object, validate_config_file
from settings.port import PORT

def get_options_config_file() -> tuple:
    """
    Return a tuple with the the files
    to render in the server.
    """

    parser = OptionParser()
    parser.add_option('-f', '--file', dest = 'config_file', help = 'Put the config file with the paths of the files for render.')

    options, args = parser.parse_args()

    if not options.config_file:
        parser.error('Put the config file to render. Help with --help')

    return options


# gettings the config file with the files path to convert to objects File
options = get_options_config_file()
config_file = options.config_file

if validate_config_file(config_file):
    files_paths = get_files_paths(options.config_file)
    files = get_files_object(files_paths)

    # starting the server
    app = Flask(__name__)
    print( f'\nServing {len(files)} Files from {config_file}... ' ) # showing a message

    @app.route('/', methods = ['GET'])
    @app.route('/home', methods = ['GET'])
    def principal():
        """
        This is for the principal route of the page.
        """

        files_paths = get_files_paths(options.config_file)
        files = get_files_object(files_paths)

        return jsonify({
            "currentFiles": {
                "id": [f.id for f in files],
                "paths": [f.path for f in files]
            }
        })


    @app.route('/get-file/<string:id>', methods=['GET'])
    def get_file(id):
        """
        Return the file
        segun the id passed for parameter
        """

        files_paths = get_files_paths(options.config_file)
        files = get_files_object(files_paths)

        try:
            # getting for return it
            file_to_render = files[int(id)].path
            # return send_file(file_to_render)

            # getting the lines and returning the information
            with open(file_to_render, 'r') as f:
                lines = f.readlines()

            return jsonify({
                "id": id,
                "path": file_to_render,
                "content": lines
            })

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

    @app.route('/add-path/', methods = ['POST'])
    def add_path():
        """
        This is the route for add a path
        to file to configuration.
        """

        path_to_add = request.form['path']

        return jsonify({
            "message": "Adding the path {path_to_add} to {config_file}"
        })

    @app.route('/update-path/<string:id>', methods = ['PUT'])
    def update_path(id):
        """
        This is the route for update
        a path in the file config.txt
        """

        id = int(id)

        return jsonify({
            "message": f"Path number {id} upated",
        })

    @app.route('/delete-path/<string:id>', methods = ['DELETE'])
    def delete_path(id):
        """
        This route is for delete a
        path of the config file. For not 
        render in the server.
        """

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
            f.close()

        return jsonify({
            "message": f"Path number {id} deleted",
            "fileDelete": {
                "id": id,
                "path": OLD_PATH
            },
        })

    @app.route('/test')
    def test():
        """
        This is a route
        for make test.
        """

        return 'testing'

    # running the app
    app.run(host = '0.0.0.0', port = PORT, debug = True)

else:
    print('\nPut a config file valid.')