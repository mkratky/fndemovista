import json
import sys, os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.environ["PUBNUB_SUBSCRIBE_KEY"]
pnconfig.publish_key = os.environ["PUBNUB_PUBLISH_KEY"]
pnconfig.ssl = False
pn = PubNub(pnconfig)

def getPayload():
    std_in = sys.stdin.read()
    sys.stderr.write("std_in -----------> " + std_in)
    return json.loads(std_in)

def callback(message):
     print message

def main():
    # get payload
    payload = getPayload()
    message_json = json.loads(payload["Message"])

    # extract data
    bucket_name = message_json["Records"][0]["s3"]["bucket"]["name"]
    print "Bucket: " + bucket_name

    image_key = message_json["Records"][0]["s3"]["object"]["key"]
    print "Image Key: " + image_key

    url = "https://s3.amazonaws.com/"+bucket_name+"/" + image_key;

    message = {'url': url, 'id': image_key}
    message_json = json.dumps(message)

    print "message: " + str(message_json)

    pn.publish().channel(bucket_name).message([message_json]).use_post(True).sync()

if __name__ == "__main__":
    main()
