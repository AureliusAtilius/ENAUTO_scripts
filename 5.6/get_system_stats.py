#!/usr/bin/env python

import json
from datetime import datetime, timezone
from cisco_sdwan import CiscoSDWAN



def main():
    
    sdwan = CiscoSDWAN.get_instance_always_on()


    with open("sys_stat_query.json", "r") as handle:
        query = json.load(handle)

    sys_stat_resp= sdwan.get_system_stats(query)

    outfile= "log_cpumem.csv"
    print(f"Creating '{outfile}' from vManage system stats")
    with open(outfile, "w") as handle:
        handle.write("dtg,cpu util%,mem util%\n")
        for stat in sys_stat_resp.json() ["data"]:
        dtg = datetime.fromtimestamp(stat["entry_time"] // 1000, timezone.utc)
        cpu = round(stat["cpu_user_new"], 2)
        mem = round(stat["mem_util"], 2)
        handle.write(f"{dtg},{cpu},{mem}\n")
    print(f"Use 'column -s, -t {outfile} | less -S' to viwe from shell")

if __name__ == "__main__":
    main()