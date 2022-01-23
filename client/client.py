import requests
import socket
import json
import hashlib
from time import sleep


def get_private_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        private_ip = s.getsockname()[0]
    except Exception:
        private_ip = 'error'
    finally:
        s.close()

    return private_ip


def make_personal_json(name, private_ip):
    personal_json = {
        'name': name,
        'ip': private_ip
    }

    return json.dumps(personal_json)


def certificate_request(json):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post('http://127.0.0.1:5000/cert_request', data=json, headers=headers)

    return response


def download_file(url, file_name=None):
    if not file_name:
        file_name = url.split('/')[-1]

    with open(file_name, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)


def download_cert_key_and_crt_file(ip_hash_value):
    download_file(f'http://127.0.0.1:5000/cert/{ip_hash_value}.key', 'server.key')
    download_file(f'http://127.0.0.1:5000/cert/{ip_hash_value}.crt', 'server.crt')


if __name__ == '__main__':
    ip = get_private_ip_address()

    if ip == 'error':
        print('network error')
        exit()

    personal_json = make_personal_json('purplepig', ip)
    cert_req_response = certificate_request(personal_json)

    if cert_req_response.status_code == 200:
        print('Request Success!')
        sleep(5)
        ip_hash = hashlib.sha256(ip.encode())
        print(ip_hash.hexdigest())
        download_cert_key_and_crt_file(ip_hash.hexdigest())
