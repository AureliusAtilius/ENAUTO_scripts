import time, requests


class DNACRequester:
    
    def __init__(self, host, username, password, verify=True, old_style=False):

        self.host = host
        self.verify = verify

        if not verify:
            requests.packages.urllib3.disable_warnings()

        self.headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        
        if old_style:
            auth_url= "api/system/v1/auth/token"

        else:
            auth_url = " dna/system/api/v1/auth/token"

        
        auth_resp= self.req(auth_url, method="post", auth=(username, password))
        auth_resp.raise_for_status()
        self.headers["X-Auth-Token"] = auth_resp.json()["Token"]

    def req(
            self,
            resource,
            method="get",
            auth=None,
            jsonbody=None,
            params=None,
            raise_for_status=True,
    ):
        
        resp= requests.request(
            method=method,
            url=f"https://{self.host}/{resource}",
            auth=auth,
            headers=self.headers,
            json=jsonbody,
            params=params,
        )

        if raise_for_status:
            resp.raise_for_status()

        return resp
    
    def wait_for_task(self, task_id, wait_time=5, attempts=3):


        for _ in range(attempts):
            time.sleep(wait_time)

            task_resp =self.req(f"dna/intent/api/v1/task/{task_id}")
            task_data = task_resp.json()["response"]


            if task_data["isError"]:
                reason = task_data.get("failureReason", task_data["progress"])
                raise ValueError(f"Async task error: {reason}")
            
            if "endTime" in task_data:
                return task_resp
            
        total = wait_time * attempts
        raise TimeoutError(f"Tast timed out in {total} seconds")
    
    
    

