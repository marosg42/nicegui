from typing import Optional

from nicegui import ui

from .mixins.value_element import ValueElement


class LinearProgress(ValueElement):
    VALUE_PROP = 'value'

    def __init__(self,
                 value: float = 0.0, *,
                 size: Optional[str] = None,
                 show_value: bool = True,
                 throttle: float = 0,
                 only_serverside_react: bool = False,
                 server_side_loopback: bool = False,
                 **kwargs) -> None:
        """Linear Progress

        A linear progress bar wrapping Quasar's
        `QLinearProgress <https://quasar.dev/vue-components/linear-progress>`_ component.

        :param value: the initial value of the field (from 0.0 to 1.0)
        :param size: the height of the progress bar (default: "20px" with value label and "4px" without)
        :param show_value: whether to show a value label in the center (default: `True`)
        """
        super().__init__(
            tag='q-linear-progress',
            value=value,
            on_value_change=None,
            throttle=throttle,
            only_serverside_react=only_serverside_react,
            server_side_loopback=server_side_loopback,
            **kwargs)
        self._props['size'] = size if size is not None else '20px' if show_value else '4px'

        if show_value:
            with self:
                ui.label().classes('absolute-center text-sm text-white').bind_text_from(self, 'value')


class CircularProgress(ValueElement):
    VALUE_PROP = 'value'

    def __init__(self,
                 value: float = 0.0, *,
                 min: float = 0.0,
                 max: float = 1.0,
                 size: str = 'xl',
                 show_value: bool = True,
                 throttle: float = 0,
                 only_serverside_react: bool = False,
                 server_side_loopback: bool = False,
                 **kwargs) -> None:
        """Circular Progress

        A circular progress bar wrapping Quasar's
        `QCircularProgress <https://quasar.dev/vue-components/circular-progress>`_.

        :param value: the initial value of the field
        :param size: the size of the progress circle (default: "xl")
        :param show_value: whether to show a value label in the center (default: `True`)
        """
        super().__init__(
            tag='q-circular-progress',
            value=value,
            on_value_change=None,
            throttle=throttle,
            only_serverside_react=only_serverside_react,
            server_side_loopback=server_side_loopback,
            **kwargs)
        self._props['min'] = min
        self._props['max'] = max
        self._props['size'] = size
        self._props['show-value'] = show_value
        self._props['color'] = 'primary'
        self._props['track-color'] = 'grey-4'

        if show_value:
            with self:
                ui.label().classes('absolute-center text-xs').bind_text_from(self, 'value')
