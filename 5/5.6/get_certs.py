#!/usr/bin/env python


import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cisco_sdwan import CiscoSDWAN



def main():
    
    # invoke instance of CiscoSDWAN object using always on sandbox
    sdwan = CiscoSDWAN.get_instance_always_on()

    # create folder called "backup_certs"
    cert_path = "backup_certs"
    if not os.path.exists(cert_path):
        os.makedirs(cert_path)
    
    # request controller certs and back them up
    for cert in sdwan.get_controller_certs().json()["data"]:
        backup_and_print_cert(
            cert_path, cert["host-name"], cert["deviceEnterpriseCertificate"]
        )

    # get root cert and back it up 
    root_cert= sdwan.get_root_cert().json()["rootcertificate"]
    backup_and_print_cert(cert_path, "root", root_cert)


# function to backup certificates
def backup_and_print_cert(path,name,data):
    
    # write cert data to file
    with open(f"{path}/{name}.pem", "w") as handle:
        handle.write(data)
    
    # encode cert data in utf-8
    cert= x509.load_pem_x509_certificate(bytes(data, "utf-8"), default_backend())

    # print cert info
    print(f"Cert info for {name} / serial {cert.serial_number}")
    subject_items = cert.subject.rfc4514_string().replace(",", "\n")
    print(subject_items + "\n")
    


