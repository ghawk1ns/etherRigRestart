This is the script I use to physically control the power/reset buttons on my ethereum mining rigs. It works by powering relays off the GPIO pins on a Raspberry Pi. Powering a relay allows me to short the reset or power terminals on a rig in case it freezes or becomes remotely inaccessible


Each rig is defined in rigs.json where a GPIO.BCM pin is mapped to a power or reset terminal on the motherboard. 

# Usage 
usage: main.py [-h] [-r] [-c] [-t TIME] id

Control the physical power/restart buttons on a rig

positional arguments:
  id                    Rig id as defined in rigs.json

optional arguments:
  -h, --help            show this help message and exit
  -r, --restart         Control the restart button, by default the power button is controlled
  -c, --cycle           Power down / power on the power button
  -t TIME, --time TIME  Time in seconds to hold physical button down, default = 3

# example
rigs.json
```
{
 "rig1" : {
    "power" : 17,
    "reset" : 18
  }, 
   "rig3" : {
    "power" : 98,
    "reset" : 99
  }
}
```

As far as I know, sudo is required to access GPIO

Hold the power button down on rig1 for 5 seconds

`sudo python main.py rig1 -t 5`

Power cycle rig1

`sudo python main.py rig1 -c`

Hold rig1 reset button down (default -t is 3 seconds)

`sudo python main.py rig1 -r`

