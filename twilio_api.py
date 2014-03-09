from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = 'AC2c313b72d07eaaaaadf1dee5589e5b30'
TWILIO_AUTH_TOKEN = '521864f710990889f1470f84385c2ce2'

TO_NUMBER = '5102464486'       # Your verified phone number
FROM_NUMBER = '5104021309'     # Your Twilio phone number
BODY = 'Hello! This was sent from our Twilio API' # SMS message

client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_text(to_number, from_number, body):
    client.sms.messages.create(to=to_number, from_=from_number, body=body)
