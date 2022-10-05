from urllib import response
import requests,json,sys





def get_login(username,password,url):
        auth_url=f"{url}/j_security_check"
        session = requests.session()
        login_body={
                'j_username':username,
                'j_password':password        
        }

        login_response=session.post(url=auth_url,data=login_body,verify=False)

        if not login_response.ok or login_response.text:
                print("*****LOGIN FAILED*****")
                sys.exit(1)
        else:
                print("*****LOGIN SUCCESS*****")
                print(login_response)
                return login_response
                
def get_certs(url,base_url):
        session = requests.session()
        cert_urls={
                'list':f'{base_url}/dataservice/certificate/vsmart/list',
                'root':f'{base_url}/dataservice/certificate/rootcertificate'
        }

        headers={
                'Accept':'application/json'
        }
        
        response=session.get(url=cert_urls[url],headers=headers,verify=False)
        print(response)
        response=response.json()
        print(json.dumps(response, indent=2))

if __name__=="__main__":
        base_url="https://sandbox-sdwan-2.cisco.com/"
        
        token=get_login('devnetuser','RG!_Yw919_83',base_url)
        get_certs('list',base_url)