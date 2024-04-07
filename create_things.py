import boto3
import json
import random
import string

thingArn = ''
thingId = ''
thingName = ''
defaultPolicyName = 'admin'
###################################################
def createThing(value):
  global thingName
  thingName = 'thing_' + str(value)
  print(thingName)
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = thingName
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  for element in data:
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
    createCertificate(value)

def createCertificate(value):
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
	with open(f'public_{value}.key', 'w+') as outfile:
		outfile.write(PublicKey)
	with open(f'private_{value}.key', 'w+') as outfile:
		outfile.write(PrivateKey)
	with open(f'cert_{value}.pem', 'w+') as outfile:
		outfile.write(certificatePem)
	response = thingClient.attach_policy(
		policyName = defaultPolicyName,
		target = certificateArn
	)
	global thingName
	response = thingClient.attach_thing_principal(
		thingName = thingName,
		principal = certificateArn
    )
thingClient = boto3.client('iot')
for i in range(5):
    createThing(i)