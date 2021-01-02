import sys
import os
import requests
import time
from twilio.rest import Client
from html.parser import HTMLParser

url             = sys.argv[1]
tag             = sys.argv[2]
dest_msisdn     = sys.argv[3]
src_msisdn      = "+19283623011"
account_sid     = os.environ['TWILIO_ACCOUNT_SID']
auth_token      = os.environ['TWILIO_AUTH_TOKEN']
sold_out_msgs   = ["CURRENTLY SOLD OUT", "OUT OF STOCK"]
client          = Client(account_sid, auth_token)

if dest_msisdn[:2] != "+1":
	dest_msisdn = "+1" + dest_msisdn

def is_in_stock(item_url):
	for msg in sold_out_msgs:
		r = requests.get(item_url)
		if msg in r.text:
			return False
		else:
			continue
	return True

while(True):
	if is_in_stock(url):
		message = client.messages \
			.create(
				body   ="%s is in stock at %s" %(tag, url),
				from_  = src_msisdn,
				to     = dest_msisdn
			)
		print("Sending message to %s" %(dest_msisdn))
		break
	print("Item not in stock")
	time.sleep(30)