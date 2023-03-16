import os,sys,time,requests
from meraki_helpers import get_network_id,req

def main(org_name, net_name, timestamp):

    snapshot_dir = "snapshots"
    if not os.path.exists(snapshot_dir):
        os.makedirs(snapshot_dir)

    net_id = get_network_id(net_name, org_name)

    cameras = req(f"networks/{net_id}/devices").json()

    for camera in cameras:

        sn= camera["serial"]

        video_link = req(f"networks/{net_id}/cameras/{sn}/videoLink").json()

        print(f"Video link for camera {sn}: \n{video_link['url']}")

        if timestamp:
            params = {"timestamp": timestamp}

        else:
            params = None
        
        snapshot_link = req(
            f"networks/{net_id}/cameras/{sn}/snapshot",
            method="post",
            params=params
        ).json()

        for _ in range(5):

            time.sleep(3)

            image = requests.get(snapshot_link["url"])

            if image.status_code == 200:
                break

        else: print(f"Could not collect snapshot for camera {sn} right now")
        continue

        with open(f"{snapshot_dir}/{sn}.jpg", "wb") as handle:

            handle.write(image.content)

        print(f"Snapshot for camera {sn} saved")

if __name__ =="__main__":

    org = os.environ.get("MERAKI_ORG_NAME", "Devnet Sandbox")

    net =os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    timest = None
    if len(sys.argv) > 1:
        timest = sys.argv[1]

    main(org, net, timest)
