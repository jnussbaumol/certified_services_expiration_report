"""
This script iterates through all the services identified in scan_ports.py and attempts to determine:
1. If the service requires a certificate.
2. If it does:
    2a. What is the name of the certificate?
    2b. When was the certificate created?
    2c. When will the certificate expire?

This information will be compiled into a report and generated for review.

The hostname should be a string containing the ip address or FQDN of the host. The port should be an integer.

If the file is run on its own, it will run a test by gathering the certificate of the website www.python.org on port 443
"""
import socket
import ssl
from cryptography import x509

# this function doesn't work atm, cause self-signed certs are causing issues
# def gather_certificate(hostname, port):
#     context = ssl.create_default_context() 
#     conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
#     conn.connect((hostname, port))
#     cert = conn.getpeercert()
#     return cert # this returns a python dictionary.

# this is not ideal, but works around self-signed cert issues
def extract_certificate(hostname, port):
    try:
        pem_cert = ssl.get_server_certificate(addr=(hostname, port)) # gets the cert as a PEM encrypted string
    except:
        print(f'Something weird happened with {hostname}:{port}.')
        return None
    der_cert = ssl.PEM_cert_to_DER_cert(pem_cert) # turns that PEM into bytes in DER format for the x509 decoding
    cert = x509.load_der_x509_certificate(der_cert) # decodes the DER formatted certificate and makes a Certificate object out of the information.
    return cert # this returns a Certificate object.

# # this function will need to change if gather_certificate gets working, or we need to make a separate function 
def determine_certificate_information(cert):
    if cert == None:
        return {'NotBefore':'UNKNOWN', 'NotAfter':'UNKNOWN', 'Organization':'UNKNOWN', 'CommonName':'UNKOWN'}
    # print(cert)
    cert_creation_date = cert.not_valid_before
    cert_expiration_date = cert.not_valid_after
    cert_issuer_O = cert.issuer.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)
    if len(cert_issuer_O) > 0:
        cert_issuer_O = cert_issuer_O[0].value
    else:
        cert_issuer_O = 'Unknown'
    cert_common_name = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    if len(cert_common_name) > 0:
        cert_common_name = cert_common_name[0].value
    else:
        cert_common_name = 'Unknown'
    return {'NotBefore':cert_creation_date, 'NotAfter':cert_expiration_date, 'Organization':cert_issuer_O, 'CommonName':cert_common_name,}

if __name__ == '__main__':
    print(f'Testing certifiate validation...')
    hostname = "www.python.org"
    port = 443
    certificate = extract_certificate(hostname, port)
    # gathered_certificate = gather_certificate(hostname, port)
    print('Certificate extracted, reading results...')
    # print(gathered_certificate)
    information = determine_certificate_information(certificate)
    print(f'{hostname} has a certificate for the service on port {port}.')
    print(information)
    # print(f'Organization: {information["Organization"]}, Server Common Name: {information["CommonName"]}, Created On: {information["NotBefore"]}, Expires: {information["NotAfter"]}')
