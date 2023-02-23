#!/usr/bin/env python

from cisco_sdwan import CiscoSDWAN


def main():
    
    sdwan = CiscoSDWAN.get_instance_reserved()

    temp_resp = sdwan.add_fd_vsmart_device_template()

    template_id = temp_resp.json()["templateId"]
    var_map = {"vsmart-01": ("100","10.10.20.254")}
    print(f"Added vSmart template (factory-defaults) with ID {template_id}")

    attach_resp = sdwan.attach_vsmart_device_template(template_id=template_id,var_map=var_map)
    data= attach_resp.json()["summary"]

    print(f"vSmart template attachment status: {data['status']}")
    print(f"Result counts: {data['count']}")


if __name__ == "__main__":
    main()