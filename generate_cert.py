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


def generate_key_and_crt_file(json):
    name = json['name']
    ip = json['ip']
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()

    make_config_file(ip, ip_hash, name)

    os.system('openssl genrsa -out server.key 2048 ')
    os.system(f'openssl req -new -sha256 -nodes -out server.csr newkey rsa:2048 -keyout server.key config <( cat {ip_hash}.csr.cnf )')
    os.system(f'openssl x509 -req -in server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server.crt -days 500 -sha256 -extfile {ip_hash}.ext')



