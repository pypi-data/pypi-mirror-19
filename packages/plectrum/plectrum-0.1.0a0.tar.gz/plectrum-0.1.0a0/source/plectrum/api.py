# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import prompt_toolkit.shortcuts
import prompt_toolkit.interface

import plectrum.application


def _pick(application):
    '''Execute *application* in command line interface and return selection.'''
    event_loop = prompt_toolkit.shortcuts.create_eventloop()
    try:
        interface = prompt_toolkit.interface.CommandLineInterface(
            application=application, eventloop=event_loop
        )
        return interface.run(reset_current_buffer=False)
    finally:
        event_loop.close()


def pick_single(items, message=None, validator=None):
    '''Return index of selected item from *items*.

    *message* should be an optional string to display to the user prior to the
    select control (an instruction for example).

    *validator* should be an optional callable with signature
    ``(items, selection)``. It should be called when the selection is confirmed
    and is expected to return a list of validation errors found. If the returned
    list is empty then the selection is approved and confirmation continues.
    Otherwise the errors are displayed to the user and confirmation prevented.

    If cancelled, return None.

    '''
    return _pick(
        plectrum.application.SingleSelectApplication(
            items, message=message, validator=validator
        )
    )


def pick_multiple(items, message=None, validator=None):
    '''Return indexes of selected items from *items*.

    *message* should be an optional string to display to the user prior to the
    select control (an instruction for example).

    *validator* should be an optional callable with signature
    ``(items, selection)``. It should be called when the selection is confirmed
    and is expected to return a list of validation errors found. If the returned
    list is empty then the selection is approved and confirmation continues.
    Otherwise the errors are displayed to the user and confirmation prevented.

    If cancelled, return None.

    '''
    return _pick(
        plectrum.application.MultiSelectApplication(
            items, message=message, validator=validator
        )
    )
