import requests
import json

url = "https://speech.googleapis.com/v1/speech:longrunningrecognize?"
key=r"AIzaSyDtKtpqWrJoCGShlr_fs-Bu5AVFdsZ9AL0"
payload = {
    "config": {
      "encoding": "LINEAR16",
      "sample_rate_hertz": 48000,
      "language_code": "en-US"
    },
    "audio": {
        "uri": "gs://bucket45858/sound.mp3"
    }
}


def main():
    global url
    r = requests.post(url, data=json.dumps(payload))
    print r.json()
    # json_resp = r.json()
    # token_resp = json_resp['']
    # url = "https://speech.googleapis.com/v1/operations/" + str(token_resp) + key
    # content_response = requests.get(url)
    # content_json = content_response.json()
    # print content_json
    # print content_response
    # print token_resp
    # print r

if __name__=="__main__":
    main()