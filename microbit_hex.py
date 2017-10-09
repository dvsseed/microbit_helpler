# micro:bit for Scratch Extension
from microbit import *

import music

REFRESH = 500

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
        bytestring = uart.readline()
        icon = str(bytestring, 'utf-8')
        if icon.find('OFF.') != -1:
            # Set the brightness of all LEDs to 0 (off).
            display.clear()
        elif icon.find('OFFRESET.') != -1:
            # Restart the board.
            reset()
        elif icon.find('OFFMUSIC.') != -1:
            # Stops all music playback on a given pin0.
            music.stop()
        elif icon.find('Image.') != -1:
            # LED
            # Display, x, y = 0~4, value = 0~9
            # display.set_pixel(x, y, value)

            # Image
            # image = Image("90009:"
            #            "09090:"
            #            "00900:"
            #            "09090:"
            #            "90009")
            display.show(getattr(Image, icon.split('.')[1]))
        elif icon.find('P0.') != -1 or icon.find('P1.') != -1 or icon.find('P2.') != -1:
            # Input/Output Pins
            # if pin0.is_touched():
            if icon[1:2] == '0':
                pin0.write_digital(int(icon.split('.')[1]))
            elif icon[1:2] == '1':
                pin1.write_digital(int(icon.split('.')[1]))
            elif icon[1:2] == '2':
                pin2.write_digital(int(icon.split('.')[1]))
        elif icon.find('music.') != -1:
            music.play(getattr(music, icon.split('.')[1]), wait=False, loop=str2bool(icon.split('.')[2]))
        else:
            display.show(icon)
    except:
        pass

def run():
    while True:
        # Do stuff
        sleep(REFRESH)
        get_sensor_data()
        sleep(REFRESH)
        read_uart()

display.show('M')

run()