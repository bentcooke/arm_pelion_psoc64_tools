import os
from cysecuretools import CySecureTools
from cysecuretools.execute import provision_device as prov_device
# from cysecuretools.execute.sys_call import get_prov_details
from cysecuretools.execute.programmer.programmer import ProgrammingTool
from cysecuretools.execute.provisioning_lib.cyprov_pem import PemKey
from OpenSSL import crypto, SSL

cytools = CySecureTools('CY8CPROTO-064S2-SB', 'policy_single_stage_CM4_2m.json')

def create_app_keys():
    cytools.create_keys()

def read_device_pub_key():

    tool = ProgrammingTool.create(cytools.PROGRAMMING_TOOL)

    # Read Device Key and save
    if tool.connect(cytools.target_name):
        print('Reading public key from device')
        key = prov_device.read_public_key(tool, cytools.register_map)
        if not key:
            print('Error: Cannot read device public key.')
            return

        pub_key_json = 'device_pub_key.json'

        with open(pub_key_json, 'w') as json_file:
            json_file.write(key)

        tool.disconnect()    
        
    # Change from JWK to PEM
    pub_key_pem = 'device_pub_key.pem'
    if os.path.exists(pub_key_json) and os.stat(pub_key_json).st_size > 0:
        pem = PemKey(pub_key_json)
        pem.save(pub_key_pem, private_key=False)
    else:
        print('Failed to read device public key')
    print('Device public key has been read successfully.')

def generate_device_cert(
    dev_pub_key_path="device_pub_key.pem",
    ca_priv_key_path="factory_configurator_utility/keystore/fcu_private_key.pem",
    ca_cert_path="factory_configurator_utility/keystore/fcu.crt"):

    if True:
        # read device public key from previously read from the device
        dev_pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, open(dev_pub_key_path, 'r').read())
    else:
        # for development only, use public key from self generated private key
        dev_priv_key = crypto.load_privatekey(crypto.FILETYPE_ASN1, open("device_priv_key.der", 'rb').read())
        dev_pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, crypto.dump_publickey(crypto.FILETYPE_PEM, dev_priv_key))
    ca_privatekey = crypto.load_privatekey(crypto.FILETYPE_PEM, open(ca_priv_key_path, 'r').read())
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(ca_cert_path, 'r').read())
    
    dev_serial_num = input("Select unique device serial number for {}:\n".format(cytools.target_name.upper()))
    if not dev_serial_num.isnumeric():
        print('Error: device serial number not number')
        return

    # create cert signed by ca_cert
    cert = crypto.X509()
    cert.set_subject(ca_cert.get_subject())
    cert.get_subject().CN = cytools.target_name.upper() + '-' + str(dev_serial_num)
    cert.set_serial_number(int(dev_serial_num))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_pubkey(dev_pub_key)
    cert.sign(ca_privatekey, 'sha256')

    open("device_cert.pem", "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open("device_cert.der", "wb").write(crypto.dump_certificate(crypto.FILETYPE_ASN1, cert))
    print('Device certificate generated successfully.')

def create_provisioning_packet():
    cytools.create_provisioning_packet()

def provision_device():
    answer = input('Provision the device. Are you sure? (Y/n): ')
    if answer == 'Y':
        cytools.provision_device()
    else:
        print('Provision skipped.')

if __name__ == "__main__":
    #create_app_keys()
    read_device_pub_key()
    generate_device_cert()
    create_provisioning_packet()
    provision_device()
