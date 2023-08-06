# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import ordered_set


class Selection(object):
    '''Represent a selection of items.'''

    def __init__(self, items=None, on_selection_changed=None):
        '''Initialise with initial *items*.

        *on_selection_changed* should be an optional callable to call, with no
        arguments, whenever the selection changes.

        .. note::

            No selection changed notification should be issued for initial
            items.

        '''
        super(Selection, self).__init__()
        self.on_selection_changed = on_selection_changed
        self._items = ordered_set.OrderedSet(items)

    def _notify_selection_changed(self):
        '''Call selection changed callback if set.'''
        if self.on_selection_changed:
            self.on_selection_changed()

    def __iter__(self):
        '''Return iterator over items in order added to selection.'''
        return iter(self._items)

    def __eq__(self, other):
        '''Return whether equal to *other*.'''
        return other == self._items

    def add(self, item):
        '''Add *item* to selection.

        *item* must be keyable.

        Issue selection changed notification if *item* newly added.

        If *item* already in selection, raise no error and issue no selection
        changed notification.

        '''
        if item not in self:
            self._items.add(item)
            self._notify_selection_changed()

    def remove(self, item):
        '''Remove *item* from selection.

        Raise :exc:`KeyError` if *item* not in selection.

        Issue selection changed notification if *item* removed.

        '''
        self._items.remove(item)
        self._notify_selection_changed()

    def clear(self):
        '''Remove all items from selection.

        Issue a single selection changed notification if items were removed.

        '''
        if self._items:
            self._items.clear()
            self._notify_selection_changed()

    def toggle(self, item):
        '''Toggle inclusion of *item* in selection.

        If *item* present in selection, remove it. Otherwise add it.

        '''
        if item in self:
            self.remove(item)
        else:
            self.add(item)
