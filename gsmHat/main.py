import time
from gsmHat import GSMHat, SMS, GPS

gsm = GSMHat('/dev/ttyS0', 115200)
gsm.ColData()


def phone():
    print('Enter a phone number with \'+48\':')
    number = input()
    if is_proper_number(number):
        gsm.Call(number)        # This call hangs up automatically after 15 seconds
        time.sleep(10)          # Wait 10 seconds ...
        gsm.HangUp()            # Or you can HangUp by yourself earlier
        gsm.Call(number, 60)    # Or lets change the timeout to 60 seconds. It hangs up automatically after 60 seconds


def is_proper_number(number: str):
    if len(number) != 12 or number[0] != '+' or number[1] != '4' or number[2] != '8':
        print("That's not valid number. Please start with \'+48\' and then enter 9 numbers.")
        return False
    return True


def print_sms():
    new_sms = gsm.SMS_read()
    print('Got new SMS from number %s' % new_sms.Sender)
    print('It was received at %s' % new_sms.Date)
    print('The message is: %s' % new_sms.Message)


def show_all_messages():
    while gsm.SMS_available() > 0:
        print_sms()
        break


def show_n_messages(number):
    while number > 0:
        if gsm.SMS_available() > 0:
            print_sms()
        number -= number


def show_n_messages_or_wait(number):
    while True:
        if number > 0 and gsm.SMS_available() > 0:
            print_sms()
            number -= number
            break


def wait_for_new_sms():
    if gsm.SMS_available() > 0:
        print("\n\tYou have unread SMS(s):\n")
        show_all_messages()
        print("\n\tNow I'm waiting for new SMS\n")

    while True:
        if gsm.SMS_available() > 0:
            print_sms()
            break


def write_sms():
    print('Enter message:')
    message = input()
    print('Enter a phone number with \'+48\':')
    number = input()
    if is_proper_number(number):
        gsm.SMS_write(number, message)


def show_location():
    # Get actual GPS position
    gps_obj = gsm.GetActualGPS()

    # Print some values
    print('GNSS_status: %s' % str(gps_obj.GNSS_status))
    print('Fix_status: %s' % str(gps_obj.Fix_status))
    print('UTC: %s' % str(gps_obj.UTC))
    print('Latitude: %s' % str(gps_obj.Latitude))
    print('Longitude: %s' % str(gps_obj.Longitude))
    print('Altitude: %s' % str(gps_obj.Altitude))
    print('Speed: %s' % str(gps_obj.Speed))
    print('Course: %s' % str(gps_obj.Course))
    print('HDOP: %s' % str(gps_obj.HDOP))
    print('PDOP: %s' % str(gps_obj.PDOP))
    print('VDOP: %s' % str(gps_obj.VDOP))
    print('GPS_satellites: %s' % str(gps_obj.GPS_satellites))
    print('GNSS_satellites: %s' % str(gps_obj.GNSS_satellites))
    print('Signal: %s' % str(gps_obj.Signal))


def calculate_distance_between_two_places():
    gps_obj_one = GPS()
    print('Enter co-ordinates of the first place:\n')
    print('latitude: ')
    latitude = input()
    gps_obj_one.Latitude = float(latitude)
    print('longitude: ')
    longitude = input()
    gps_obj_one.Longitude = float(longitude)

    gps_obj_two = GPS()
    print('Enter co-ordinates of the second place:\n')
    print('latitude: ')
    latitude = input()
    gps_obj_two.Latitude = float(latitude)
    print('longitude: ')
    longitude = input()
    gps_obj_two.Longitude = float(longitude)

    print('Distance from this two places:')
    print(GPS.CalculateDeltaP(gps_obj_one, gps_obj_two))


def calculate_distance_between_your_position_and_sth_else():
    gps_obj_your = gsm.GetActualGPS()

    gps_obj_another = GPS()
    print('Enter co-ordinates of the another place:\n')
    print('latitude: ')
    latitude = input()
    gps_obj_another.Latitude = float(latitude)
    print('longitude: ')
    longitude = input()
    gps_obj_another.Longitude = float(longitude)

    print('Distance from you and another place:')
    print(GPS.CalculateDeltaP(gps_obj_your, gps_obj_another))


def print_menu():
    print('Menu:')
    print('1 - Phone')
    print('2 - Wait for sms')
    print('3 - Show unread messages')
    print('4 - Write sms')
    print('5 - Show location')
    print('6 - Calculate distance between two places')
    print('7 - Calculate distance between you and another place')


print('Welcome to SIM868')
while True:
    print_menu()
    what_to_do = input()

    if what_to_do == '1':
        phone()
    elif what_to_do == '2':
        wait_for_new_sms()
    elif what_to_do == '3':
        show_all_messages()
    elif what_to_do == '4':
        write_sms()
    elif what_to_do == '5':
        show_location()
    elif what_to_do == '6':
        calculate_distance_between_two_places()
    elif what_to_do == '7':
        calculate_distance_between_your_position_and_sth_else()
    else:
        print('That\'s not the proper option')

    time.sleep(2)
