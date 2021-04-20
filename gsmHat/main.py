import time

from gsmHat import GSMHat, SMS, GPS

gsm = GSMHat('/dev/ttyS0', 115200)


def phone():
    print('Enter a phone number with \'+48\':')
    number = input()
    if is_proper_number(number):
        gsm.Call(number)        # This call hangs up automatically after 15 seconds
        time.sleep(10)          # Wait 10 seconds ...
        gsm.HangUp()            # Or you can HangUp by yourself earlier
        gsm.Call(number, 60)    # Or lets change the timeout to 60 seconds. It hangs up automatically after 60 seconds


def is_proper_number(number: str):
    if len(number) != 12:
        return False
    if number[0] != '+':
        return False
    if number[1] != '4':
        return False
    if number[2] != '8':
        return False
    return True


def wait_for_sms():
    quit_option = input()
    print('To quit enter any letter:')
    while True:
        if gsm.SMS_available() > 0:
            new_sms = gsm.SMS_read()
            print('Got new SMS from number %s' % new_sms.Sender)
            print('It was received at %s' % new_sms.Date)
            print('The message is: %s' % new_sms.Message)
            break
        if type(quit_option) == str:
            break


def print_menu():
    print('Menu:')
    print('1 - Phone')
    print('2 - Wait for sms')


print('Welcome to SIM868')
while True:
    print_menu()
    what_to_do = input()

    if what_to_do == 1:
        phone()
    elif what_to_do == 2:
        wait_for_sms()
    elif what_to_do == 3:
        print('3')
    elif what_to_do == 4:
        print('4')
    elif what_to_do == 5:
        print('5')
    else:
        print('That\'s not the proper option')

    time.sleep(2)
