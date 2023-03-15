#!/usr/bin/env python

import sys, getpass
from datetime import datetime, timezone
from cisco_sdwan import CiscoSDWAN


def main():
    sdwan= CiscoSDWAN.get_instance_always_on()

    if not sdwan.is_admin():
        print("You are not currently authenticated as an 'admin' user.")
        sys.exit()
    
    group_name= "audit"
    body = {
        "groupName": group_name,
        "tasks": [
            {
                "feature": "Audit Log",
                "read": True,
                "enabled": True,
                "write": False,

            },
            {
                "feature": "Interface",
                "read": True,
                "enabled": True,
                "write": False,
            },
            {"feature": "System", "read": True, "enabled": True, "write": False},
        ],
    }

    sdwan.add_user_to_group(body)
    
    sdwan.add_user("jdoe", "jane doe", [group_name])

    user_password = getpass.getpass("Enter password for jdoe: ")
    sdwan.update_password("jdoe", user_password)

    audit = CiscoSDWAN(
        host="10.10.20.90", port= 8443, username="jdoe", password=user_password
    )

    audit_resp = audit.get_audit_log()

    outfile = "log_useraudit.csv"
    print(f"Creating {outfile} from vManage audit log")

    with open(outfile, "w") as handle:
        handle.write("dtg,device,user,msg\n")
        for log in audit_resp.json()["data"]:
            dtg = datetime.fromtimestamp(log["entry_time"] // 1000, timezone.utc)
            device = log.get("logdeviceid","none")
            user = log.get("loguser", "none")
            msg = log.get("logmessage", "none")
            handle.write(f"{dtg},{device},{user},{msg}\n")
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__=="__main__":
    main()