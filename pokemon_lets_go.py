#!/usr/bin/env python

from porygon import \
        init_pi, press, read_cropped_image, still, tilt_x, tilt_y, \
        A, B, X, Y, HOME
import time

DIALOG_UPPER_LEFT_X = 365
DIALOG_UPPER_LEFT_Y = 442

DIALOG_CARD = (
        DIALOG_UPPER_LEFT_X,
        DIALOG_UPPER_LEFT_Y,
        DIALOG_UPPER_LEFT_X + 380,
        DIALOG_UPPER_LEFT_Y + 33
)


def go_left(hold_delay=.1, rest_delay=.1):
    print('going left for {} seconds'.format(hold_delay))
    tilt_x(300)
    time.sleep(hold_delay)
    still()
    time.sleep(rest_delay)


def go_right(hold_delay=.1, rest_delay=.1):
    print('going right for {} seconds'.format(hold_delay))
    tilt_x(-300)
    time.sleep(hold_delay)
    still()
    time.sleep(rest_delay)


def go_up(hold_delay=.1, rest_delay=.1):
    print('going up for {} seconds'.format(hold_delay))
    tilt_y(300)
    time.sleep(hold_delay)
    still()
    time.sleep(rest_delay)


def go_down(hold_delay=.1, rest_delay=.1):
    print('going down for {} seconds'.format(hold_delay))
    tilt_y(-300)
    time.sleep(hold_delay)
    still()
    time.sleep(rest_delay)


def fly():
    press(X, rest_delay=1)
    press(A, rest_delay=2)  # Wait for menu load.
    go_right(.1)  # Charizard is in the 2nd slot.
    press(A, rest_delay=1)
    go_down()
    go_down()
    press(A, rest_delay=3)  # "charizard will travel along side..."
    press(A, rest_delay=1)  # make message go away
    press(B, rest_delay=1)
    press(B)


def land():
    press(X, rest_delay=1)
    press(A, rest_delay=1)  # Wait for menu load.
    go_right(.1)  # Charizard is in the 2nd slot.
    press(A, rest_delay=1)
    go_down()
    go_down()
    press(A, rest_delay=1)  # Unsummoned
    press(B, rest_delay=1)
    press(B)


def soft_reset():
    press(HOME, rest_delay=1)
    press(X, rest_delay=1)
    press(A, rest_delay=4)  # Yes, exit... Give time to close
    press(A, rest_delay=12)  # start again, get to controller pairing menu
    press(A, hold_delay=2, rest_delay=3)  # Pair controller
    press(A, rest_delay=2)  # Done pairing
    press(A, rest_delay=30)  # Confirm controller. Get through title screen.
    press(A, rest_delay=5)  # start the game!
    press(A, rest_delay=3)  # continue my adventure...


def pickup():
    press(A, rest_delay=3)  # Find the item, wait for message display
    for _ in range(3):  # power issues with the camera require a retry loop :<
        retval = read_cropped_image(DIALOG_CARD)
        if retval:
            break
    press(A, rest_delay=2)
    press(A, rest_delay=2)  # Dismiss message
    return retval


def item1_from_start():
    go_up(.5)
    go_left(3)


def item2_from_item1():
    go_right(.8)
    go_up(3.6)


def item3_from_item2():
    go_down(1)
    go_right(4.6)


def item4_from_item3():
    go_right(.6)
    go_down(1.8)
    go_right(.5)


def item6_from_item2():
    go_down(.8)
    go_right(2.5)
    go_down(.5)


def item3_from_item6():
    go_up(.8)
    go_right(2.2)


def item5_from_item4():
    go_right(1.8)
    go_up(0.8)


def entrance_from_item5():
    go_left(2)
    go_down(1)
    go_left(1.5)
    go_down(2)
    go_left(2.5)
    go_down(1, rest_delay=3)
    go_up(1)


def save():
    press(X, rest_delay=1)
    go_right()
    go_right()
    press(A, rest_delay=3)
    press(A, rest_delay=3)
    press(A, rest_delay=3)
    press(B)


def fetch_items(pick=True, path=(1, 2, 3, 4, 5, 6)):
    retval = []

    def maybe_pickup():
        if pick:
            retval.append(pickup())

    if 1 in path:
        item1_from_start()
        maybe_pickup()

    if 2 in path:
        item2_from_item1()
        maybe_pickup()

    if 3 in path:
        item6_from_item2()
        maybe_pickup()

    if 4 in path:
        item3_from_item6()
        maybe_pickup()

    if 5 in path:
        item4_from_item3()
        maybe_pickup()

    if 6 in path:
        item5_from_item4()
        maybe_pickup()

    if 7 in path:
        entrance_from_item5()

    return retval


def do_round(*args):
    soft_reset()
    args = args or [1, 2, 3, 4, 5, 6]
    return fetch_items(path=args)


if __name__ == '__main__':
    init_pi()
    found = {}
    while True:
        pprint.pprint(found)
        items_found = [x.lower().strip() for x in do_round()]
        for item in items_found:
            count = found.setdefault(item, 0)
            found[item] = count + 1
            if any('gold' in x for x in found):
                print('Done!')
                sys.exit()
