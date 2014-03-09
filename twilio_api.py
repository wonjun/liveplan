from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''

TO_NUMBER = '5102464486'       # Your verified phone number
FROM_NUMBER = '5104021309'     # Your Twilio phone number
BODY = 'Hello! This was sent from our Twilio API' # SMS message

client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
client.sms.messages.create(to=TO_NUMBER, from_=FROM_NUMBER, body=BODY)

def send_text(to_number, from_number, body):
    client.sms.messages.create(to=to_number, from_=from_number, body=body)
