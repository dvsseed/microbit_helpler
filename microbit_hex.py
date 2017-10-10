# micro:bit for Scratch Extension
from microbit import *

import music

REFRESH = 150

def get_sensor_data():
    # Gestures/Accelerometer
    ax, ay, az = accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()

    # Compass
    cx, cy, cz = compass.get_x(), compass.get_y(), compass.get_z()

    # Buttons
    # Temperature in degrees Celcius
    ba, bb, tp = button_a.was_pressed(), button_b.was_pressed(), temperature()

    print(ax, ay, az, cx, cy, cz, ba, bb, tp)

def str2bool(s):
    if s == 'true':
         return True
    elif s == 'false':
         return False
    else:
         raise ValueError

def read_uart():
    uart.init(115200, bits=8, parity=None, stop=1)
    try:
        # bytestring = uart.readline()
        # icon = str(bytestring, 'utf-8')
        bytestring = uart.readline()
        data_list = str(bytestring, 'utf-8').split(':')
        off_0, offreset_1, offmusic_2, led_3, pin_4, music_5 = data_list
        if off_0 != 'none':
            # Set the brightness of all LEDs to 0 (off).
            display.clear()
        if offreset_1 != 'none':
            # Restart the board.
            reset()
        if offmusic_2 != 'none':
            # Stops all music playback on a given pin0.
            music.stop()
        if led_3 != 'none':
            if led_3.find('Image.') != -1:
                # LED
                # Display, x, y = 0~4, value = 0~9
                # display.set_pixel(x, y, value)

                # Image
                # image = Image("90009:"
                #            "09090:"
                #            "00900:"
                #            "09090:"
                #            "90009")
                display.show(getattr(Image, led_3.split('.')[1]))
            else:
                display.show(led_3.split('.')[1])                
        if pin_4 != 'none':
            # Input/Output Pins
            # if pin0.is_touched():
            if pin_4[1:2] == '0':
                pin0.write_digital(int(pin_4.split('.')[1]))
            elif pin_4[1:2] == '1':
                pin1.write_digital(int(pin_4.split('.')[1]))
            elif pin_4[1:2] == '2':
                pin2.write_digital(int(pin_4.split('.')[1]))
        if music_5 != 'none':
            music.play(getattr(music, music_5.split('.')[1]), wait=False, loop=str2bool(music_5.split('.')[2]))
    except:
        pass

def run():
    while True:
        # Do stuff
        get_sensor_data()
        sleep(REFRESH)
        read_uart()
        sleep(REFRESH)

display.show('M')

run()