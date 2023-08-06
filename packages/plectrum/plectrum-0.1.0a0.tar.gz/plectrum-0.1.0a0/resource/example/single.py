# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import plectrum


def only_apple(items, selection):
    errors = []
    if items[selection] != 'apple':
        errors.append('Must select apple!.')

    return errors


items = ['apple', 'pear', 'banana']
selected = plectrum.pick_single(
    items, message='Which is your favorite?', validator=only_apple
)
if selected is not None:
    print 'What a surprise, you chose: {}'.format(items[selected])
