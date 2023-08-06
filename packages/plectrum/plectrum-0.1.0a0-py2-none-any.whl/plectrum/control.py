# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

from __future__ import unicode_literals

import copy

import prompt_toolkit.layout.controls
import prompt_toolkit.token

import plectrum.selection


class AbstractSelectControl(prompt_toolkit.layout.controls.TokenListControl):
    '''Manage selection of items.'''

    def __init__(self, items):
        '''Initialise control with *items* to select from.'''
        if not items:
            raise ValueError('At least one item must be specified.')

        self.selection = plectrum.selection.Selection()
        self._items = items
        self._count = len(self._items)
        self._maximum_item_width = max(map(len, self._items))
        self._current_index = 0
        self._indicator = ' > '
        self._spacer = ' ' * len(self._indicator)
        super(AbstractSelectControl, self).__init__(self._get_tokens)

    @property
    def items(self):
        '''Return items.

        .. note::

            Return copy to avoid indirect mutation.

        '''
        return copy.copy(self._items)

    def next_item(self):
        '''Move indicator to next item.'''
        self._current_index = (self._current_index + 1) % self._count

    def previous_item(self):
        '''Move indicator to previous item.'''
        self._current_index = (self._current_index - 1) % self._count

    def _get_tokens(self, interface):
        '''Return tokens to display for *interface*.

        *interface* should be an instance of
        :class:`prompt_toolkit.interface.CommandLineInterface`.

        '''
        tokens = []
        Token = prompt_toolkit.token.Token

        for index, item in enumerate(self._items):
            tokens.append(
                (
                    Token,
                    self._indicator if index == self._current_index
                    else self._spacer
                )
            )

            tokens.append(
                (
                    Token.Selected if index in self.selection else Token,
                    '{0:<{1}}'.format(item, self._maximum_item_width)
                )
            )

            tokens.append((Token, '\n'))

        return tokens


class SingleSelectControl(AbstractSelectControl):
    '''Manage selection of single item.'''

    def __init__(self, items):
        '''Initialise control with *items* to select from.'''
        super(SingleSelectControl, self).__init__(items)
        self.select_current_item()

    def select_current_item(self):
        '''Select current item, replacing any existing selection.'''
        self.selection.clear()
        self.selection.add(self._current_index)

    def next_item(self):
        '''Move indicator to next item and select it.'''
        super(SingleSelectControl, self).next_item()
        self.select_current_item()

    def previous_item(self):
        '''Move indicator to previous item and select it.'''
        super(SingleSelectControl, self).previous_item()
        self.select_current_item()


class MultiSelectControl(AbstractSelectControl):
    '''Manage selection of multiple items.'''

    def toggle_current_item(self):
        '''Toggle selection of current item.'''
        self.selection.toggle(self._current_index)
