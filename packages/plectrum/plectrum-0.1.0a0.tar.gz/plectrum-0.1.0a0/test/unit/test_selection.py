# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import pytest

import plectrum.selection


@pytest.mark.parametrize('items, expected', [
    ([], set()),
    ([1, 2, 3], {1, 2, 3}),
    ([1, 1, 2], {1, 2})
], ids=[
    'empty',
    'unique',
    'duplicates'
])
def test_initial_items(items, expected):
    '''Initialise selection with specific items.'''
    selection = plectrum.selection.Selection(items=items)
    assert selection == expected


def test_add():
    '''Add non present item to selection.'''
    selection = plectrum.selection.Selection()
    item = 1
    assert item not in selection
    selection.add(item)
    assert item in selection


def test_add_existing():
    '''Add already present item to selection.'''
    item = 1
    selection = plectrum.selection.Selection(items=[item])
    assert item in selection
    selection.add(item)
    assert item in selection


def test_remove():
    '''Remove present item from selection.'''
    item = 1
    selection = plectrum.selection.Selection(items=[item])
    assert item in selection
    selection.remove(item)
    assert item not in selection


def test_remove_missing():
    '''Fail to remove item not present in selection.'''
    selection = plectrum.selection.Selection()
    item = 1
    assert item not in selection
    with pytest.raises(KeyError):
        selection.remove(item)


@pytest.mark.parametrize('item, expected', [
    (1, set()),
    (2, {1, 2})
], ids=[
    'existing',
    'missing'
])
def test_toggle(item, expected):
    '''Toggle item in selection.'''
    selection = plectrum.selection.Selection(items=[1])
    selection.toggle(item)
    assert selection == expected


@pytest.mark.parametrize('items', [
    [],
    [1, 2, 3]
], ids=[
    'empty',
    'populated'
])
def test_clear(items):
    '''Clear selection.'''
    selection = plectrum.selection.Selection(items=items)
    selection.clear()
    assert not set(selection)


def test_iter():
    '''Iterate over items in order added.'''
    items = [3, 1, 2]
    selection = plectrum.selection.Selection(items=items)
    for item, entry in zip(items, selection):
        assert item == entry


@pytest.mark.parametrize('candidate', [
    [1, 2, 3],
    {1, 1, 2, 3},
    plectrum.selection.Selection({1, 2, 3})
], ids=[
    'convertible-to-set',
    'set',
    'selection'
])
def test_equal(candidate):
    '''Compare equality with equal objects.'''
    selection = plectrum.selection.Selection(items=[1, 2, 3])
    assert selection == candidate


@pytest.mark.parametrize('candidate', [
    object(),
    [1, 2],
    plectrum.selection.Selection({1, 2})
], ids=[
    'inconvertible-to-set',
    'different-set',
    'different-selection'
])
def test_unequal(candidate):
    '''Compare equality with unequal objects.'''
    selection = plectrum.selection.Selection(items=[1, 2, 3])
    assert selection != candidate


def test_on_selection_changed_initial_items(mocker):
    '''Selection changed not issued for initial items.'''
    callback = mocker.Mock()

    plectrum.selection.Selection(
        items=[1, 2, 3], on_selection_changed=callback
    )
    assert callback.called is False


@pytest.mark.parametrize('item, called', [
    (1, False),
    (4, True)
], ids=[
    'existing-item',
    'new-item'
])
def test_on_selection_changed_add_item(mocker, item, called):
    '''Selection changed for added item.'''
    callback = mocker.Mock()
    selection = plectrum.selection.Selection(
        items=[1, 2, 3], on_selection_changed=callback
    )

    selection.add(item)
    assert callback.called is called


def test_on_selection_changed_remove_item(mocker):
    '''Selection changed for removed item.'''
    callback = mocker.Mock()
    selection = plectrum.selection.Selection(
        items=[1, 2, 3], on_selection_changed=callback
    )

    selection.remove(2)
    assert callback.called is True


@pytest.mark.parametrize('items, call_count', [
    ([], 0),
    ([1, 2, 3], 1)
], ids=[
    'empty',
    'items-present'
])
def test_on_selection_changed_clear_items(mocker, items, call_count):
    '''Selection changed for cleared items.'''
    callback = mocker.Mock()
    selection = plectrum.selection.Selection(
        items=items, on_selection_changed=callback
    )

    selection.clear()
    assert callback.call_count is call_count
