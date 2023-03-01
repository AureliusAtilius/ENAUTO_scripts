#!/usr/bin/env python


import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cisco_sdwan import CiscoSDWAN



def main():
    

    sdwan = CiscoSDWAN.get_instance_always_on()

    cert_path = "backup_certs"
    if not os.path.exists(cert_path):
        os.makedirs(cert_path)
    
    for cert in sdwan.get_controller_certs().json()["data"]:
        backup_and_print_cert(
            cert_path, cert["host-name"], cert["deviceEnterpriseCertificate"]
        )


    root_cert= sdwan.get_root_cert().json()["rootcertificate"]
    backup_and_print_cert(cert_path, "root", root_cert)


def backup_and_print_cert(path,name,data):
    
    with open(f"{path}/{name}.pem", "w") as handle:
        handle.write(data)
    
    cert= x509.load_pem_x509_certificate(bytes(data, "utf-8"), default_backend())


    print(f"Cert info for {name} / serial {cert.serial_number}")
    subject_items = cert.subject.rfc4514_string().replace(",", "\n")
    print(subject_items + "\n")
    


