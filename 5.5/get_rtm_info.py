#!/usr/bin/env python


from cisco_sdwan import CiscoSDWAN


def main():
    

    sdwan = CiscoSDWAN.get_instance_always_on()

    resp = sdwan.get_device_vedges(model="vedge-cloud")
    data_list= resp.json()["data"]

    for vedge in data_list:
        if vedge.get("configStatusMessage", "").lower() == "in sysc":
            vedge_id= vedge["system-ip"]
            print(f"Starting vEdge {vedge_id} collection")

            tunnel= sdwan.get_device_tunnel_statistics(vedge_id)
            print(" Tunnel Statistics")
            for item in tunnel.json()["data"]:
                print(
                    f" pkts tx/rx: {item['tx_pkts']}/{item['rx_pkts']}"
                    f"proto: {item['tunnel-protocol']} to {item['dest-ip']}"
                )

        control = sdwan.get_device_control_connections(vedg_id)
        print(" Control connections")
