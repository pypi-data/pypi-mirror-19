# :coding: utf-8
# :copyright: Copyright (c) 2017 Martin Pengelly-Phillips
# :license: Apache License, Version 2.0. See LICENSE.txt.

import prompt_toolkit.application
import prompt_toolkit.layout.containers
import prompt_toolkit.layout.controls
import prompt_toolkit.layout.dimension
import prompt_toolkit.filters
import prompt_toolkit.token
import prompt_toolkit.key_binding.manager
import prompt_toolkit.styles
import prompt_toolkit.keys

import plectrum.control


class AbstractSelectApplication(prompt_toolkit.application.Application):
    '''Provide interactive selection of items.'''

    def __init__(self, items, message=None, validator=None):
        '''Initialise application.

        *items* should be a list of items that can be selected from. *message*
        should be a string to display ahead of the selection (to instruct the
        user for example).

        *validator* should be an optional callable with signature
        ``(items, selection)``. It should be called when the selection is
        confirmed and is expected to return a list of validation errors found.
        If the returned list is empty then the selection is approved and
        confirmation continues. Otherwise the errors are displayed to the user
        and confirmation prevented.

        '''
        self._control = self._build_select_control(items)
        self._validator = validator

        self._show_help = False

        self._errors = []
        self._control.selection.on_selection_changed = (
            self._on_selection_changed
        )

        layout = self._build_layout(message)
        manager = (
            prompt_toolkit.key_binding.manager.KeyBindingManager.for_prompt()
        )
        self._register_key_bindings(manager.registry)
        style = self._get_style()

        super(AbstractSelectApplication, self).__init__(
            layout=layout, key_bindings_registry=manager.registry, style=style
        )

    @property
    def _help(self):
        '''Return help message.'''
        return (
            'Use <Up> / <Down> arrow keys to navigate and <Enter> to confirm.'
        )

    def _build_select_control(self, items):
        '''Return select control for *items*.'''
        raise NotImplementedError()

    def _build_layout(self, message):
        '''Return layout.

        *message* should be the optional instructional message to display prior
        to the select control.

        '''
        controls = prompt_toolkit.layout.controls
        containers = prompt_toolkit.layout.containers
        Dimension = prompt_toolkit.layout.dimension.LayoutDimension
        Token = prompt_toolkit.token.Token

        contents = []
        if message:
            contents.append(
                containers.Window(
                    height=Dimension.exact(1),
                    content=controls.TokenListControl(
                        get_tokens=lambda cli: [(Token.Message, message)]
                    )
                )
            )

        contents.append(
            containers.ConditionalContainer(
                containers.Window(
                    content=controls.TokenListControl(
                        get_tokens=lambda cli: [(Token.Help, self._help)]
                    ),
                    height=Dimension.exact(1)
                ),
                filter=(
                    ~prompt_toolkit.filters.IsDone() &
                    prompt_toolkit.filters.Condition(
                        lambda cli: self._show_help is not False
                    )
                )
            )
        )

        contents.append(
            containers.ConditionalContainer(
                containers.Window(
                    self._control,
                    height=Dimension(min=3)
                ),
                filter=~prompt_toolkit.filters.IsDone()
            )
        )

        contents.append(
            containers.ConditionalContainer(
                containers.Window(
                    controls.TokenListControl(
                        get_tokens=lambda cli: [
                            (Token.Error, error) for error in self._errors
                        ]
                    )
                ),
                filter=(
                    ~prompt_toolkit.filters.IsDone() &
                    prompt_toolkit.filters.Condition(
                        lambda cli: len(self._errors)
                    )
                )
            )
        )

        return containers.HSplit(contents)

    def _register_key_bindings(self, registry):
        '''Register key bindings against *registry*.

        *registry* should be an instance of
        :class:`prompt_toolkit.key_binding.registry.Registry`.

        '''
        Keys = prompt_toolkit.keys.Keys

        registry.add_binding(Keys.ControlC, eager=True)(
            self._on_cancel
        )
        registry.add_binding(Keys.Down, eager=True)(
            self._on_navigate_next_item
        )
        registry.add_binding(Keys.Up, eager=True)(
            self._on_navigate_previous_item
        )
        registry.add_binding(Keys.Enter, eager=True)(
            self._on_confirm_selection
        )
        registry.add_binding(Keys.Any, eager=True)(
            self._on_show_help
        )

    def _on_cancel(self, event):
        '''Handle cancel selection *event*.'''
        event.cli.set_return_value(None)

    def _on_navigate_next_item(self, event):
        '''Handle navigate to next item *event*.'''
        self._control.next_item()

    def _on_navigate_previous_item(self, event):
        '''Handle navigate to previous item *event*.'''
        self._control.previous_item()

    def _on_confirm_selection(self, event):
        '''Handle confirm selection *event*.'''
        selection = self._get_selection()
        if self._validator:
            self._errors = self._validator(self._control.items, selection)
            if self._errors:
                return

        event.cli.set_return_value(selection)

    def _on_show_help(self, event):
        '''Handle on show help *event*.'''
        self._show_help = True

    def _on_selection_changed(self):
        '''Handle selecton change.'''
        del self._errors[:]

    def _get_selection(self):
        '''Return current selection in appropriate form.'''
        return list(self._control.selection)

    def _get_style(self):
        '''Return style.'''
        Token = prompt_toolkit.token.Token
        return prompt_toolkit.styles.style_from_dict({
            Token.Selected: '#ansiturquoise',
            Token.Message: '',
            Token.Error: '#ansired',
            Token.Help: '#ansilightgray'
        })


class SingleSelectApplication(AbstractSelectApplication):
    '''Provide interactive selection of single item.'''

    def _build_select_control(self, items):
        '''Return select control for *items*.'''
        return plectrum.control.SingleSelectControl(items)

    def _get_selection(self):
        '''Return current selection in appropriate form.'''
        return list(self._control.selection)[0]


class MultiSelectApplication(AbstractSelectApplication):
    '''Provide interactive selection of multple items.'''

    @property
    def _help(self):
        '''Return help message.'''
        return (
            'Use <Up> / <Down> arrow keys to navigate, <Tab> to toggle '
            'selection, and <Enter> to confirm.'
        )

    def _build_select_control(self, items):
        '''Return select control for *items*.'''
        return plectrum.control.MultiSelectControl(items)

    def _register_key_bindings(self, registry):
        '''Register key bindings against *registry*.

        *registry* should be an instance of
        :class:`prompt_toolkit.key_binding.registry.Registry`.

        '''
        super(MultiSelectApplication, self)._register_key_bindings(registry)
        Keys = prompt_toolkit.keys.Keys

        registry.add_binding(Keys.Tab, eager=True)(
            self._on_toggle_current_item
        )

    def _on_toggle_current_item(self, event):
        '''Handle toggle current item *event*.'''
        self._control.toggle_current_item()
