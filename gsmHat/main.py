import time

from gsmHat import GSMHat, SMS, GPS

gsm = GSMHat('/dev/ttyS0', 115200)

Number = '+48787504781'
gsm.Call(Number)        # This call hangs up automatically after 15 seconds
time.sleep(10)          # Wait 10 seconds ...
gsm.HangUp()            # Or you can HangUp by yourself earlier
gsm.Call(Number, 60)    # Or lets change the timeout to 60 seconds. This call hangs up automatically after 60 seconds


def print_sms():
    new_sms = gsm.SMS_read()

    print('Got new SMS from number %s' % new_sms.Sender)
    print('It was received at %s' % new_sms.Date)
    print('The message is: %s' % new_sms.Message)


while True:
    time.sleep(2)
    print('Main loop working')
    if gsm.SMS_available() > 0:
        print_sms()


