#!/usr/bin/env python

import json,requests

class CiscoSDWAN:
        def __init__(self, host, port, username, password, verify=False) :

                self.base_url= f"https://{host}:{port}"

                self.verify = verify
                if not self.verify:
                        requests.packages.urllib3.disable_warnings()

                self.session = requests.session()
                auth_resp = self.session.post(
                        f"{self.base_url}/j_security_check",
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        data={"j_username": username, "j_password": password},
                        verify=self.verify,
                )

                if auth_resp.text:
                        auth_resp.status_code = 401
                        auth_resp.reason = "UNAUTHORIZED; check username/password"
                        auth_resp.raise_for_status()

                self.headers = {
                        "Accept": "application/json",
                        "Content-Type": "appication/json",
                }
        
        @staticmethod 
        def get_instance_always_on():
                return CiscoSDWAN(
                        host="sandboxsdwan.cisco.com",
                        port=8443,
                        username="devnetuser",
                        password="Cisco123!",
                )
        @staticmethod
        def get_instance_reserverd():
                return CiscoSDWAN(
                        host="10.10.20.90", port=8443, username='admin', password='admin'
                )

        @staticmethod
        def run_api_calls(api_calls, filepath="data_ref"):
                for api_call in api_calls:
                        resp = api_call()
                        name = api_call.__name__
                        print(f"Executing '{name}' API Call")
                        with open(f"{filepath}/{name}.json", "w") as handle:
                                json.dump(resp.json(),handle,indent=2)


        def _req(self, resource, method="get", params=None, jsonbody=None):

                resp = self.session.request(
                        method=method,
                        url=f"{self.base_url}/{resource}",
                        headers=self.headers,
                        params=params,
                        json=jsonbody,
                        verify=self.verify,
                )
                resp.raise_for_status()
                return resp

        def get_all_devices(self, model=None):
                params = {"device-model": model} if model else None
                return self._req("dataservice/device", params=params)
        
        def get_device_controllers(self, model=None):

                params = {"model":model} if model else None
                return self._req("dataservice/system/device/controllers", params=params)

        def get_device_vedges(self, model=None):

                params = {"model": model} if model else None
                return self._req("dataservice/system/device/vedges", params=params)