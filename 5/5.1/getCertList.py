from urllib import response
import requests,json,sys



# function for requesting certificates
def get_certs(url,base_url):

        # connection data for connecting to Cisco SD-WAN controller
        auth_url=f"{base_url}/j_security_check"
        session = requests.session()
        login_body={
                'j_username':'devnetuser',
                'j_password':'RG!_Yw919_83'        
        }

        # send login request using connection info, check for successful connection response
        login_response=session.post(url=auth_url,data=login_body,verify=False)

        if not login_response.ok or login_response.text:
                print("*****LOGIN FAILED*****")
                sys.exit(1)
        else:
                print("*****LOGIN SUCCESS*****")
                print(login_response)
                
        # URLs for vSmart and root certificates
        cert_urls={
                'list':f'{base_url}/dataservice/certificate/vsmart/list',
                'root':f'{base_url}/dataservice/certificate/rootcertificate'
        }
        
        # REST header
        headers={
                'Accept':'application/json'
        }
        
        # send cert request and print output in human friendly format
        response=session.get(url=cert_urls[url],headers=headers,verify=False)
        print(response)
        response=response.json()
        print(json.dumps(response, indent=2))

if __name__=="__main__":
        base_url="https://sandbox-sdwan-2.cisco.com/"
        get_certs('list',base_url)