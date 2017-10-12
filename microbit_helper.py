#!/usr/local/bin/python

# -*- coding: utf-8 -*-

"""
Created on Tue Oct 10 12:49:59 2017
@author: Davis, Tseng @Taiwan
Copyright (c) 2017-18 Davis Tseng  All right reserved.

This program is free software;
you can redistribute it and/or modify it under the terms of the GNU 
Lesser General Public License as published by the Free Software Foundation;
either version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library;
if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
"""

from __future__ import unicode_literals

import os
import sys
import time
import serial
import serial.tools.list_ports
import thread

from blockext import *


acc_x = 0
acc_y = 0
acc_z = 0
comp_x = 0
comp_y = 0
comp_z = 0
btn_a = False
btn_b = False
pins = ''
melodys = ''
temp_t = 0
show_led = ''
clear_led = False
clear_music = False
clear_mb = False

class BBCmicrobit:

    def __init__(self):
        self.led = ''
        self.cls = False
        self.sm = False
        self.rst = False

    def _is_connected(self):
        return

    def _problem(self):
        if time.time() % 8 > 4:
            return "The Scratch Sensor board is not connected. Foo."

    def _on_reset(self):
        global show_led
        show_led = ''
        global pins
        pins = ''
        global melodys
        melodys = ''
        print("""
        Reset! The red stop button has been clicked,
        And now everything is how it was.
        If you want to stop this shell scripting,
        please use <Ctrl-C> to exit.
        """)

    @reporter("acc_x")
    def acc_x(self):
        return acc_x

    @reporter("acc_y")
    def acc_y(self):
        return acc_y

    @reporter("acc_z")
    def acc_z(self):
        return acc_z

    @reporter("comp_x")
    def comp_x(self):
        return comp_x

    @reporter("comp_y")
    def comp_y(self):
        return comp_y

    @reporter("comp_z")
    def comp_z(self):
        return comp_z

    @reporter("btn_a")
    def btn_a(self):
        return str(btn_a).lower()

    @reporter("btn_b")
    def btn_b(self):
        return str(btn_b).lower()

    @command("%m.status : Write on %m.inputs digital value %m.high_low", defaults=["off", "P0", "0"])
    def show_pin(self, status, inputs, high_low):
        global pins
        if status == 'on':
            pins = inputs + '.' + high_low
        else:
            pins = ''
        return pins

    @command("%m.status : Play built-in melody %m.musics Loop %m.bools", defaults=["off", "music.BIRTHDAY", "false"])
    def play_music(self, status, musics, bools):
        global melodys
        if status == 'on':
            melodys = musics + '.' + bools
        else:
            melodys = ''
        return melodys

    @command("Stop music")
    def stop_music(self):
        global clear_music
        self.sm = True
        clear_music = self.sm

    @reporter("stop")
    def get_stop(self):
        return self.sm

    @reporter("temp_t")
    def temp_t(self):
        return temp_t

    @reporter("Image of %m.imgs", defaults=["Image.HAPPY"])
    def show_image(self, imgs):
        return imgs

    @command("%m.status : Set LED to %s", defaults=["off", ""])
    def set_led(self, status, value):
        global show_led
        if status == 'on':
            self.led = value
            show_led = value
        else:
            show_led = ''
        return show_led

    @reporter("led")
    def get_led(self):
        return self.led

    @command("Clear display")
    def off_led(self):
        global clear_led
        self.cls = True
        clear_led = self.cls

    @reporter("clear")
    def get_clear(self):
        return self.cls

    @command("Reset microbit")
    def reset_mb(self):
        global clear_mb
        self.rst = True
        clear_mb = self.rst

    @reporter("reset")
    def get_reset(self):
        return self.rst

def serial_proc():
    global acc_x
    global acc_y
    global acc_z
    global comp_x
    global comp_y
    global comp_z
    global btn_a
    global btn_b
    global pins
    global melodys
    global temp_t
    global show_led
    global clear_mb
    global clear_music
    global clear_led

    # the port will depend on your computer
    # for a raspberry pi it will probably be /dev/ttyACM0
    # for windows it will be COM(something)
    PORT = None
    if len(sys.argv) == 2:
        PORT = str(sys.argv[1])
    else:
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            sp = str(p)
            if sp.find('COM') != -1 and sp.find('mbed') != -1 and os.name == "nt":
                lslice = sp.find('(') + 1
                rslice = sp.find(')')
                PORT = sp[lslice:rslice]
                # PORT = "COM14"
            elif sp.find('usb') != -1 and os.name == "posix":
                PORT = sp[0:sp.find(' ')]
                # PORT = "/dev/cu.usbmodem1412"
                # PORT = "/dev/cu.usbmodem1422"
            else:
                PORT = "/dev/ttyACM0"
    if PORT is None:
        print('The micro:bit should be plugged into a USB socket, please.')
        # to exit the entire thread
        os._exit(1)

    #
    BAUD = 115200
    s = serial.Serial(PORT)
    s.baudrate = BAUD
    s.parity = serial.PARITY_NONE
    s.databits = serial.EIGHTBITS
    s.stopbits = serial.STOPBITS_ONE

    # s.flushInput()  # flush input buffer, discarding all its contents
    # s.flushOutput()  # flush output buffer, aborting current output

    play_time = None

    try:
        while True:
            # Serial Communication (Receiving)
            # read a line from the microbit, decode it and
            # strip the whitespace at the end
            data = s.readline().decode('utf-8')
            # split the accelerometer data into ax, ay, az...
            data_list = data.rstrip().split(' ')
            ax, ay, az, cx, cy, cz, ba, bb, tp = data_list
            acc_x = ax.replace('\x00', '')
            acc_y = ay
            acc_z = az
            comp_x = cx
            comp_y = cy
            comp_z = cz
            btn_a = ba
            btn_b = bb
            temp_t = tp

            #print(acc_x, acc_y, acc_z, comp_x, comp_y, comp_z, btn_a, btn_b, temp_t)
            # time.sleep(0.2)

            # Serial Communication (Sending)
            # Writing Data
            send_to_mb = ''
            if clear_led:
                send_to_mb = send_to_mb + 'OFF:'
                clear_led = False
            else:
                send_to_mb = send_to_mb + 'none:'
            if clear_mb:
                send_to_mb = send_to_mb + 'OFFRESET:'
                clear_mb = False
            else:
                send_to_mb = send_to_mb + 'none:'
            if clear_music:
                send_to_mb = send_to_mb + 'OFFMUSIC:'
                clear_music = False
            else:
                send_to_mb = send_to_mb + 'none:'
            if show_led != '':
                send_to_mb = send_to_mb + show_led + ':'
            else:
                send_to_mb = send_to_mb + 'none:'
            if pins != '':
                send_to_mb = send_to_mb + pins + ':'
            else:
                send_to_mb = send_to_mb + 'none:'
            if melodys != '':
                # replay music must be limited for 15 seconds
                if play_time == None or int(time.time() - play_time) > 15:
                    play_time = time.time()
                    send_to_mb = send_to_mb + melodys
                else:
                    send_to_mb = send_to_mb + 'none'
            else:
                send_to_mb = send_to_mb + 'none'

            s.write(send_to_mb.encode('utf-8'))
            # print(send_to_mb)
            # time.sleep(0.2)

    finally:
        # Close serial port
        s.close()

def run_server():
    print 'Starting HTTPServer, use <Ctrl-C> to stop.'
    extension.run_forever(debug=True)

def get_decorated_blocks_from_class(cls, selectors=None):
    if selectors:
        cls_vars = vars(cls)
        values = map(cls_vars.get, selectors)
    else:
        values = vars(cls).values()

    functions = []
    for value in values:
        if callable(value) and hasattr(value, '_block'):
            functions.append(value)
    functions.sort(key=lambda func: func._block_id)
    return [f._block for f in functions]

descriptor = Descriptor(
    name = "BBC micro:bit Extension",
    port = 54321,
    blocks = get_decorated_blocks_from_class(BBCmicrobit),
    menus = dict(
        status = ["on", "off"],
        inputs = ["P0", "P1", "P2"],
        high_low = ["0", "1"],
        bools = ["true", "false"],
        musics = ["music.DADADADUM", "music.ENTERTAINER", "music.PRELUDE", "music.ODE", "music.NYAN", "music.RINGTONE", "music.FUNK", "music.BLUES", "music.BIRTHDAY", "music.WEDDING", "music.FUNERAL", "music.PUNCHLINE", "music.PYTHON", "music.BADDY", "music.JUMP_UP", "music.JUMP_DOWN", "music.POWER_UP", "music.POWER_DOWN"],
        imgs = ["Image.HEART", "Image.HAPPY", "Image.SMILE", "Image.ANGRY", "Image.YES", "Image.NO", "Image.CLOCK12", "Image.CLOCK11", "Image.CLOCK10", "Image.CLOCK9", "Image.CLOCK8", "Image.CLOCK7", "Image.CLOCK6", "Image.CLOCK5", "Image.CLOCK4", "Image.CLOCK3", "Image.CLOCK2", "Image.CLOCK1", "Image.ALL_CLOCKS", "Image.ARROW_N", "Image.ARROW_NE", "Image.ARROW_E", "Image.ARROW_SE", "Image.ARROW_S", "Image.ARROW_SW", "Image.ARROW_W", "Image.ARROW_NW", "Image.ALL_ARROWS"],
    ),
)

extension = Extension(BBCmicrobit, descriptor)


if __name__ == "__main__":
    try:
        thread.start_new_thread(serial_proc, ())
        thread.start_new_thread(run_server, ())
    except:
        pass

    while 1:
        pass
