from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def get_webook_json():
        webhook_data = json.dumps(request.json, indent=4)

        #Print message
        print("WebHook POST Received\n{}").format(webhook_data)
        return "ok"

if __name__=="__main__":
        app.run(host="0.0.0.0",port=5005, debug=False)