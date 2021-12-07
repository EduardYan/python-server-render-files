"""
This is the principal
file for execute the server.
"""

from flask import Flask, send_file, jsonify
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
    print('\nServing Files ...')

    @app.route('/')
    def principal():
        """
        This is for the principal route of the page.
        """

        return jsonify({
            "currentFiles": [
                [f.id for f in files],
                [f.path for f in files]
            ]
        })

    @app.route('/get-file/<string:id>')
    def get_file(id):
        """
        Return the file
        segun the id passed for parameter
        """

        try:
            # getting for return it
            file_to_render = files[int(id)].path
            return send_file(file_to_render)

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


    app.run(host = '0.0.0.0', port = PORT, debug = True)

else:
    print('\nPut a config file valid.')