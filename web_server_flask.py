

from flask import request
from target_lib import TargetLib
from ota_interface import ProcessesManagement
import flask
import tempfile
import os
from flask import Flask
import logging
import json
import traceback
from flask_cors import CORS


app = Flask(__name__, static_url_path='', static_folder='dist')
CORS(app)

jobs = ProcessesManagement()
target_lib = TargetLib()


@app.route("/check", methods=["GET"])
def check():
    statuses = jobs.get_status()
    return flask.jsonify(statuses)


@app.route("/check/<uuid:id>", methods=["GET"])
def check_with_id(id):
    status = jobs.get_status_by_ID(id=id)
    return flask.jsonify(status)


@app.route("/file", methods=["GET"])
def list_builds():
    file_list = target_lib.get_builds()
    return flask.jsonify(file_list)


@app.route("/run/<uuid:id>", methods=["POST"])
def generate_ota(id):
    try:
        config = request.json
        jobs.ota_generate(config, id=str(id))
        return flask.jsonify({"success": True, "msg": "OTA Generator started running"})
    except Exception as e:
        traceback.print_exc()
        return flask.Response(json.dumps({"success": False, "msg": str(e)}), status=501, mimetype=app.config["JSONIFY_MIMETYPE"])


@app.route("/file/<filename>", methods=["POST"])
def upload_build(filename):
    file_length = request.content_length
    # Unwrap the uploaded file first (due to the usage of FormData)
    # The wrapper has a boundary line at the top and bottom
    # and some file information in the beginning
    # There are a file content line, a file name line, and an empty line
    # The boundary line in the bottom is 4 bytes longer than the top one
    # Please refer to the following links for more details:
    # https://stackoverflow.com/questions/8659808/how-does-http-file-upload-work
    # https://datatracker.ietf.org/doc/html/rfc1867
    upper_boundary = request.stream.readline()
    file_length -= len(upper_boundary) * 2 + 4
    file_length -= len(request.stream.readline())
    file_length -= len(request.stream.readline())
    file_length -= len(request.stream.readline())
    BUFFER_SIZE = 1024*1024
    with tempfile.NamedTemporaryFile(filename, "w+") as fp:
        for offset in range(0, file_length, BUFFER_SIZE):
            chunk = request.stream.read(
                min(file_length-offset, BUFFER_SIZE))
            fp.write(chunk)
        target_lib.new_build(filename, fp.name)
        if not os.path.exists(fp.name):
            # if tempfile gets deleted/moved, exit block will yield an error
            # therefore touch it if does not exist
            with open(fp.name, 'wb'):
                pass
    return flask.Response(status=200)


@app.route("/download/<path>")
def download_output(path):
    if not path.startswith(jobs.working_dir):
        return flask.Response("{} is forbidden, only files in {} can be downloaded".format(path, jobs.working_dir), status=403)
    return flask.send_from_directory(".", path)

# Force re-write all paths to index.html,
# as we are serving a Single Page Application


@app.route('/', defaults={'path': ''}, methods=["GET"])
@app.route('/<string:path>', methods=["GET"])
def index(path):
    return flask.send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run()
