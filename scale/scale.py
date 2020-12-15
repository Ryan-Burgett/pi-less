#! /usr/bin/python2

import sys
import time

EMULATE_HX711 = False

referenceUnit = 533

URL = "http://127.0.0.1:5000/"

MIN_WEIGHT = 50

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    # from emulated_hx711 import HX711
    print("Error")




def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()


hx = HX711(5, 6)

# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

weights = [hx.get_weight(5)]
min_count = 0

while True:
    try:
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.

        if len(weights) >= 10:
            weights.pop(0)

        weights.append(hx.get_weight(5))

        average = sum(weights) / len(weights)

        print("Current weights: " + str(weights))
        print("Length: " + str(len(weights)))
        print("Average: " + str(average))

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

        if average < MIN_WEIGHT:
            min_count += 1

            if min_count > 20:
                print("Scale is below designated weight: Processing Order...")
                raise KeyboardInterrupt
        else:
            min_count = 0

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
