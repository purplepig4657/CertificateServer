from flask import Flask, send_from_directory, request, jsonify
from generate_cert import generate_key_and_crt_file

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/cert/<filename>')
def cert_download(filename):
    return send_from_directory('cert', filename)


@app.route('/cert_request', methods=['POST'])
def cert_request():
    personal_json = request.get_json()
    generate_key_and_crt_file(personal_json)
    return jsonify(personal_json)


if __name__ == '__main__':
    app.run()
