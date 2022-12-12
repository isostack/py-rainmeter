import requests
import hourly
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import json
inbound = open("/home/baremetal/Dev Ops/all_tokens.json")
TOKENS =  json.load(inbound)

OPENWEATHERAUTH = TOKENS["openweathermap.com auth"]

# endpoint = "https://api.openweathermap.org/data/3.0/onecall"
# api_key = OPENWEATHERAUTH 
# parameters = {
#     "lat": 5.551167,
#     "lon": 0.200450,
#     "appid": api_key,
# }

# response = requests.get(endpoint, params=parameters)
# response.raise_for_status() 
# print(response.json())

h_data_main = hourly.hour_data[:10]

will_rain = False

condition_codes = [item["weather"][0]["id"] for item in h_data_main]
for item in condition_codes:
    if item < 700:
        will_rain = True 
        
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']

TWILIO_SID = TOKENS["twilio.com sid"]
TWILIO_AUTH = TOKENS["twilio.com auth"] 

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https':os.environ['https_proxy']}

    client = Client(TWILIO_SID, TWILIO_AUTH , http_client=proxy_client)
    message = client.messages \
                .create(
                     body="The twilio app and sms script is working! Remember to bring an umbrella.",
                     from_='+14255841393',
                     to='+233207926310'
                 )
    print(message.status)

