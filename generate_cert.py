import hashlib
import os


def make_config_file(ip, ip_hash, name):
    with open(f'./cert/{ip_hash}.csr.cnf', 'w') as csr_cnf:
        content = f'''
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
        '''
        csr_cnf.write(content)

    with open(f'./cert/{ip_hash}.ext', 'w') as ext:
        content = f'''
            authorityKeyIdentifier=keyid,issuer
            basicConstraints=CA:FALSE
            keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
            subjectAltName = @alt_names

            [alt_names]
            IP.1 = {ip}
        '''
        ext.write(content)


def generate_sh_file(ip_hash):
    commands = f'''#!/bin/bash
    openssl genrsa -out ./cert/{ip_hash}.key 2048
    openssl req -new -sha256 -nodes -out ./cert/{ip_hash}.csr newkey rsa:2048 -keyout ./cert/{ip_hash}.key -config <( cat ./cert/{ip_hash}.csr.cnf )
    openssl x509 -req -in ./cert/{ip_hash}.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out ./cert/{ip_hash}.crt -days 500 -sha256 -extfile ./cert/{ip_hash}.ext
    '''

    with open(f'./{ip_hash}.sh', 'w') as sh:
        sh.write(commands)


def generate_key_and_crt_file(json):
    name = json['name']
    ip = json['ip']
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()

    make_config_file(ip, ip_hash, name)
    generate_sh_file(ip_hash)

    os.system(f'./{ip_hash}.sh')
