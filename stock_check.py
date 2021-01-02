import sys
import os
import requests
import time
import argparse
from twilio.rest import Client
from html.parser import HTMLParser

parser = argparse.ArgumentParser()
parser.add_argument('--url')
parser.add_argument('--tag')
parser.add_argument('--from-file')
parser.add_argument('--dest-msisdn')
parser.add_argument('--src-msisdn')
parser.add_argument('--test-only')
parser.add_argument('--check-frequency', type=int, default=30)

args = parser.parse_args()

if args.from_file is not None:
	import csv
	with open(args.from_file, newline='') as csvfile:
		items = list(csv.DictReader(csvfile))
else:
	if args.url is None:
		raise RuntimeError("Need to pass either a URL or a text file of URLs")
	items = [{"url": args.url, "tag": args.tag}]

account_sid     = os.environ['TWILIO_ACCOUNT_SID']
auth_token      = os.environ['TWILIO_AUTH_TOKEN']
sold_out_msgs   = ["CURRENTLY SOLD OUT", "OUT OF STOCK"]
client          = Client(account_sid, auth_token)

def is_in_stock(item_url):
	for msg in sold_out_msgs:
		r = requests.get(item_url)
		if msg in r.text:
			return False
		else:
			continue
	return True

def send_message(list_item):
	if args.test_only:
		print("%s is in stock at %s" %(list_item['tag'], list_item['url']))
	else:
		message = client.messages \
					.create(
						body   ="%s is in stock at %s" %(list_item['tag'], list_item['url']),
						from_  = args.src_msisdn,
						to     = args.dest_msisdn
					)
		print("Sending message to %s" %(args.dest_msisdn))

while len(items) > 0:
	for item in items:
		if is_in_stock(item['url']):
			if args.test_only:
				print("%s is in stock at %s" %(item['tag'], item['url']))
			else:
				send_message(item)
			# Remove item from watch list once it's found in stock
			items.remove(item)
		else:
			print("%s not in stock" %(item['tag']))
	time.sleep(args.check_frequency)