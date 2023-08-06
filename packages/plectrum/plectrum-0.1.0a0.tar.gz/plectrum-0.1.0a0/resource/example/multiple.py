# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import plectrum


def at_least_two(items, selection):
    errors = []
    if len(selection) < 2:
        errors.append('Select at least 2 items.')
    return errors


items = ['apple', 'pear', 'banana']
selected = plectrum.pick_multiple(
    items, message='Which are your favorite?', validator=at_least_two
)
if selected:
    print 'You chose:'
    for index in selected:
        print items[index]
else:
    print 'None of them took your fancy.'
