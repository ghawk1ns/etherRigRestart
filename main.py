import argparse
import RPi.GPIO as GPIO
import json
import time

def switch(pin, t=3, cycle=False):
    print 'pin=%s time=%s cycle=%s' % (pin, t, cycle)
    try:
        # Reads the pins by their "Broadcom SOC channel" number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT, initial=1)
        # The relay I use is active=low
        GPIO.output(pin, 0)
        time.sleep(t)
        GPIO.output(pin, 1)
        if cycle:
            time.sleep(5)
            GPIO.output(pin, 0)
            time.sleep(t)
            GPIO.output(pin, 1)
    finally:
        GPIO.cleanup()
'''
    Restart Button: 
        1. Restart
    Power Button:
        1. Shutdown
        2. Power Cycle
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control the physical power/restart buttons on a rig')
    parser.add_argument('id', type=str, help='Rig id as defined in rigs.json')
    parser.add_argument('-r', '--restart', action='store_true', help='Control the restart button, '
                                                                     'by default the power button is controlled')
    parser.add_argument('-c', '--cycle', action='store_true', help='Power down / power on the power button')
    parser.add_argument("-t", "--time", type=int, default=3,
                        help="Time in seconds to hold physical button down, default = 3")
    args = parser.parse_args()

    with open('rigs.json') as data_file:
            rigs = json.load(data_file)
            if args.id in rigs:
                rigInfo = rigs[args.id]
                # Are we flipping the restart or power relay?
                k = 'restart' if args.restart else 'power'
                if k in rigInfo:
                    pin = int(rigInfo[k])
                    if pin < 0:
                        raise ValueError('Invalid val for pin/port (%s) must be >= 0' % pin)
                    print pin
                    switch(pin, args.time, args.cycle)
                else:
                    raise ValueError('Undefined port for ' + k)
            else:
                raise ValueError('Invalid rig id')