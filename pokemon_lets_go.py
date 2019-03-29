#!/usr/bin/env python

import porygon

print(porygon)


def go_left(hold_delay=.1, rest_delay=.1):
    print('going left for {} seconds'.format(hold_delay))
    set_leftright(LR_NEUTRAL + 300)
    time.sleep(hold_delay)
    still()
    time.sleep(rest_delay)
