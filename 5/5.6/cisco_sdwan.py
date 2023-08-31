#!/usr/bin/env python

import json,requests,time


# CiscoSDWAN connection object
class CiscoSDWAN:
        def __init__(self, host, port, username, password, verify=False) :

                # base URL of SDWAN controller
                self.base_url= f"https://{host}:{port}"

                # hostkey verify, use False for first time connection
                self.verify = verify
                if not self.verify:
                        requests.packages.urllib3.disable_warnings()

                # create session
                self.session = requests.session()

                # request auth headers 
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

                # REST API headers
                self.headers = {
                        "Accept": "application/json",
                        "Content-Type": "appication/json",
                }
        
        # get instance using SDWAN always-on sandbox info
        @staticmethod 
        def get_instance_always_on():
                return CiscoSDWAN(
                        host="https://sandbox-sdwan-2.cisco.com",
                        port=8443,
                        username="devnetuser",
                        password="RG!_Yw919_83",
                )
        
        # get instance using reserved SDWAN sandbox
        @staticmethod
        def get_instance_reserved():
                return CiscoSDWAN(
                        host="10.10.20.90", port=8443, username='admin', password='admin'
                )

        # run api requests and write output to file
        @staticmethod
        def run_api_calls(api_calls, filepath="data_ref"):
                for api_call in api_calls:
                        resp = api_call()
                        name = api_call.__name__
                        print(f"Executing '{name}' API Call")
                        with open(f"{filepath}/{name}.json", "w") as handle:
                                json.dump(resp.json(),handle,indent=2)

        # function for forming an api request
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

        # function for requesting device list
        def get_all_devices(self, model=None):
                params = {"device-model": model} if model else None
                return self._req("dataservice/device", params=params)
        
        # function for requesting list of device controllers
        def get_device_controllers(self, model=None):

                params = {"model":model} if model else None
                return self._req("dataservice/system/device/controllers", params=params)

        # function for requesting list of vEdge devices
        def get_device_vedges(self, model=None):

                params = {"model": model} if model else None
                return self._req("dataservice/system/device/vedges", params=params)

        # function for requesting template features
        def get_feature_templates(self):
                return self._req("dataservice/template/feature")

        # function for adding vsmart templates
        def add_fd_vsmart_device_template(self):
                all_temps= self.get_feature_templates()
                fd_temps = []
                for temp in all_temps.json()["data"]:

                        temp_type = temp["templateType"].lower()
                        if temp["factoryDefault"] and (
                                temp_type.endswith("vsmart") or temp_type== "aaa"
                        ):
                                fd_temps.append(
                                        {
                                        "templateId": temp["templateId"],
                                        "templateType": temp["templateType"],
                                        }
                                )
                body = {
                        "templateName": "Basic_template",
                        "templateDescription": "Collection of default templates",
                        "deviceType": "vsmart",
                        "configType": "template",
                        "factoryDefault": False,
                        "policyId": "",
                        "featureTemplateUidRange": [],
                        "generalTemplates": fd_temps,
                }

                return self._req(
                        "dataservice/template/device/feature", method="post", jsonbody=body
                                        
                )

        # function for attaching vsmart template to device
        def attach_vsmart_device_template(self, template_id, var_map):

                vsmarts = self.get_all_devices(model="vsmart")
                templates=[]

                for dev in vsmarts.json()["data"]:
                        site_id, def_gway = var_map[dev["host-name"]]
                        vsmart_dict= {
                                "csv-status": "complete",
                                "csv-deviceId": dev["uuid"],
                                "csv-deviceIP": dev["system-ip"],
                                "csv-host-name": dev["host-name"],
                                "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/address": def_gway,
                                "//system/host-name": dev["host-name"],
                                "//system/site-id": site_id,
                                "csv-templateId": template_id,
                        }   
                        templates.append(vsmart_dict)     

                body= {
                        "deviceTemplateList": [
                        {
                        "templateId": template_id,
                        "device": templates,
                        "isEdited": False,
                        "isMasterEdited": False,
                        }
                        ]
                }

                attach_resp = self._req(
                        "dataservice/template/device/config/attachfeature",
                        method="post",
                        jsonbody=body,
                )

                attach_id = attach_resp.json()["id"]
                return self._wait_for_device_action_done(attach_id)
        
        # function for waiting for completion of asynchronous operation
        def _wait_for_device_action_done(self, uuid, interval=20):

                while True:
                        time.sleep(interval)
                        check = self._req(f"dataservice/device/action/status/{uuid}")
                        if check.json()["summary"]["status"].lower() != "in_progress":
                                break
                return check

        # function for adding a policy template
        def _add_policy(self,obj_type,name,entries):

                body = {
                        "name": name,
                        "description": "Desc Not Required",
                        "type": obj_type,
                        "entries": entries,
                }
                
                return self._req(
                        f"dataservice/template/policy/list/{obj_type}",
                        method="post",
                        jsonbody=body,
                )
        
        # function for adding site policy
        def add_policy_site(self, name, site_list):

                entries= [{"siteId": str(site)} for site in site_list]
                return self._add_policy("site", name, entries)
        
        # function for adding vpn policy 
        def add_policy_vpn(self, name, vpn_list):

                entries=[{"vpn": str(vpn)} for vpn in vpn_list]
                return self._add_policy("vpn", name, entries=entries) 
        
        # function for adding SLA policy
        def add_policy_sla(self, name, sla_entries):

                return self._add_policy("sla", name, sla_entries)
        
        # function for adding mesh policy
        def add_policy_mesh(self, name, vpn_id, region_map, description="none"):

                regions=[]
                for region, site_id in region_map.items():
                        regions.append({"name": region, "siteLists": site_id})

                body = {
                        "name": name,
                        "type": "mesh",
                        "description": description,
                        "definition": {"vpnList": vpn_id, "regions": regions}
                }

                return self._req(
                        f"dataservice/template/policy/definition/mesh",
                        methog="post",
                        jsonbody=body,
                )
        
        # function for adding approute policy
        def add_policy_approute(
                        self, name, sla_id, dscp, pri_link, alt_link, description="none"
        ):
                body = {
                        "name": name,
                        "type": "appRoute",
                        "description": description,
                        "sequences": [
                                {
                                "sequenceId": 1,
                                "sequenceName": "App Route",
                                "sequenceType": "appRoute",
                                "match": {"entries":[{"field": "dscp", "value": str(dscp)}]},
                                "actions": [
                                        {
                                                "type": "slaClass",
                                                "parameter": [
                                                        {"field": "name", "ref": sla_id},
                                                        {"field": "preferredColor", "value": pri_link},
                                                ],
                                        },
                                        {
                                                "type": "backupSlaPreferredColor",
                                                "parameter": alt_link,
                                        },
                                ],
                                }
                        ]
                }

                return self._req(
                        f"dataservice/template/policy/definition/approute",
                        method="post",
                        jsonbody=body,
                )
        
        # function for requesting vsmart policy list
        def get_policy_vsmart(self):
                return self._req(f"dataservice/template/policy/vsmart")
        
        # function for adding vsmart policy
        def add_policy_vsmart(
                        self, name, sites,vpns, approute_id, mesh_id, descriptption="none"
        ):
                body = {
                        "policyDescritpion": descriptption,
                        "poicyType": "feature",
                        "policyName": name,
                        "plicyDefinition": {
                                "assembly": [
                                        {
                                                "definitionId": approute_id,
                                                "type": "appRoute",
                                                "entries": [{"siteLists": sites, "vpnLists": vpns}],
                                        },
                                        {"definitionId": mesh_id, "type": "mesh"},
                                ]
                        },
                        "isPolicyActivated": False,

                }

                self._req(
                        f"dataservice/template/policy/vsmart", method="post", jsonbody=body
                )

                policies = self.get_policy_vsmart()
                for policy in policies.json()["data"]:
                        if policy["policyName"] == name:
                                return policy
                
                return {"policyId":None}

        # function for activating vsmart policy
        def activate_policy_vsmart(self, policy_id):
                activate_resp = self_req(
                        f"dataservice/template/policy/vsmart/activate/{policy_id}",
                        method="post",
                        params={"confirm": "true"},
                        jsonbody={},

                )

                activate_id = activate_resp.json()["id"]
                return self._wait_for_device_action_done(activate_id)
        

        # Dashboard APIs

        def get_alarm_count(self):

                return self._req("dataservice/alarms/count")
        
        def get_certificate_summary(self):

                return self._req("dataservice/certificate/stats/summary")
        
        def get_control_status(self):

                return self._req("dataservice/device/control/count")
        


        #Real-time monitoring

        def get_device_tunnel_statistics(self, device_id):

                return self._req(
                        "dataservice/device/tunnel/statistics", params={"devicId": device_id}
                )
        
        def get_device_control_connections(self, device_id):

                return self._req(
                        "dataservice/device/control/connections",
                        params={"deviceId": device_id},
                )

        #Cert Management

        def get_controller_certs(self):

                return self._req("dataservice/certificate/vsmart/list")
        
        def get_root_cert(self):

                return self._req("dataservice/certificate/rootcertificate")


        # System statistics

        def get_system_stats(self, query):

                return self._req(
                        "dataservice/statistics/system/", method="post",jsonbody=query
                )
        

        #Administrative APIs

        def is_admin(self):

                resp = self._req("dataservice/admin/user/role")
                return resp.json()["isAdmin"]
        
        def get_audit_log(self):

                return self._req("dataservice/auditlog")

        def add_user_to_group(self, body):

                return self._req(
                        "dataservice/admin/usergroup", method="post", jsonbody=body
                )

        def add_user(self, username, fullname, group_list):

                body= {
                        "group": group_list,
                        "description": fullname,
                        "userName": username,
                        "password": "abc123",

                }
                return self._req("dataservice/admin/user", method="put", jsonbody=body)
        
        def update_password(self, username, password):

                body = {"userName": username, "password": password}

                return self._req("dataservice/admin/user/password/{username}", method="post", jsonbody=body)
