#!/usr/bin/env python


from cisco_sdwan import CiscoSDWAN

def main():
    
    sdwan = CiscoSDWAN.get_instance_always_on()

    api_calls = [
        sdwan.get_alarm_count,
        sdwan.get_certificate_summary,
        sdwan.get_control_status,
    ]
    CiscoSDWAN.run_api_calls(api_calls)

if __name__=="__main__":
    main()