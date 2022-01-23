import hashlib
import os


def make_config_file(ip, ip_hash, name):
    with open(f'./cert/{ip_hash}.conf', 'w') as conf:
        content = f'''
            [req]
            default_bits = 2048
            prompt = no
            default_md = sha256
            distinguished_name = dn

            [dn]
            C=KR
            ST=CC
            L=DJ
            O=UO
            OU={ip}
            emailAddress={name}.email.com
            CN={ip}
            
            
            [req_ext]
            authorityKeyIdentifier=keyid,issuer
            basicConstraints=CA:FALSE
            keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
            subjectAltName = @alt_names
            
            [alt_names]
            IP.1 = {ip}
        '''
        conf.write(content)


def generate_sh_file(ip_hash):
    commands = f'''#!/bin/bash
    openssl genrsa -out ./cert/{ip_hash}.key 2048
    openssl req -sha256 -out ./cert/{ip_hash}.csr -key ./cert/{ip_hash}.key -config ./cert/{ip_hash}.conf
    openssl x509 -req -in ./cert/{ip_hash}.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out ./cert/{ip_hash}.crt -days 500 -sha256 -extfile ./cert/{ip_hash}.conf -extensions req_ext
    '''

    with open(f'./{ip_hash}.sh', 'w') as sh:
        sh.write(commands)


def generate_key_and_crt_file(json):
    name = json['name']
    ip = json['ip']
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()

    make_config_file(ip, ip_hash, name)
    generate_sh_file(ip_hash)

    os.chmod(f'{ip_hash}', 0o755)
    os.system(f'./{ip_hash}.sh')
