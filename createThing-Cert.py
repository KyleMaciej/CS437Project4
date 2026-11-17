################################################### Connecting to AWS
import boto3

import json
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
thingArn = ''
thingId = ''
policies = [
	"Thing1Subscribe",
	"Thing1Recieve",
	"Thing1Publish",
	"Thing1Policy",
]
###################################################

def createThing(num):
    global thingClient
	
    name = str(num)
    thingResponse = thingClient.create_thing(
        thingName = name
    )
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    for element in data: 
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']
        createCertificate(name)

def createCertificate(thingName):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
			setAsActive = True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
	for element in data: 
			if element == 'certificateArn':
					certificateArn = data['certificateArn']
			elif element == 'keyPair':
					PublicKey = data['keyPair']['PublicKey']
					PrivateKey = data['keyPair']['PrivateKey']
			elif element == 'certificatePem':
					certificatePem = data['certificatePem']
			elif element == 'certificateId':
					certificateId = data['certificateId']
							
	with open('public.key', 'w') as outfile:
			outfile.write(PublicKey)
	with open('private.key', 'w') as outfile:
			outfile.write(PrivateKey)
	with open('cert.pem', 'w') as outfile:
			outfile.write(certificatePem)
	for policy in policies:
		response = thingClient.attach_policy(
	        policyName = policy,
			target = certificateArn
		)
	response = thingClient.attach_thing_principal(
		thingName = thingName,
		principal = certificateArn
	)
	response = thingClient.add_thing_to_thing_group(
		thingName = thingName,
		thingGroupName = "ThingGroup"
	)

thingClient = boto3.client('iot')
for i in range(10):
	createThing(i)
