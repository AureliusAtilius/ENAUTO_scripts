import requests

#Disable any warnings that might come from making a request and clean up the output for data
requests.packages.urllib3.disable_warnings()

#Header variable stores the content-type sent to the API for authentication
HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

#auth_rul stores the URL for vManage and the resource path for authentication
auth_url = "https://sandbox-sdwan-2.cisco.com/j_security_check"

#Credentials contain key-value pairs for credentials
credentials = {"j_username": "devnetuser", "j_password": "RG!_Yw919_83"}

#response variable stores the POST request repsonse. The last parameter verify=FALSE disables the authenticity check of a self-signed certificate.
response = requests.post(auth_url, headers= HEADERS, data=credentials, verify=False)

#prints the response status code
print(response.status_code)

#prints the cookies object used for subsequent requests
print(response.cookies)


#Now we're authenticated we can make a new request
url = "https://sandbox-sdwan-2.cisco.com/dataservice/template/feature"

#A new get response is created. the get request uses the previously obtained cookie
response = requests.get(url, cookies=response.cookies, verify=False)

print(response.status_code)