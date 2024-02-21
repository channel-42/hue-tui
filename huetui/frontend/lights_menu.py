import py_cui.keys as Keys
import py_cui.grid as Grid
import py_cui.widgets as Widgets

from py_cui.debug import PyCUILogger as Logger
from huetui.backend.bridge import Bridge
from huetui.backend.light import RGB
from huetui.frontend.utils import get_xrdb_colors


class LightMenu(Widgets.ScrollMenu):
    """Light menu widget.

    Args:
        title (str): menu title
        grid (Grid): grid object
        row (int): x position of the menu
        column (int): y position of the menu
        row_span (int): x width of the menu
        column_span (int): y height of the menu
        padx (int): x padding
        pady (int): y padding
        logger (Logger): logger object
        bridge (Bridge): bridge object
    """

    def __init__(
        self,
        id,
        title: str,
        grid: Grid,
        row: int,
        column: int,
        row_span: int,
        column_span: int,
        padx: int,
        pady: int,
        logger: Logger,
        bridge: Bridge,
        master,
    ) -> None:
        self.lights = bridge.lights
        self.master = master
        # set fallback colors in case xrdb is not available
        self.colors = {
            "black": "#000000",
            "gray": "#808080",
            "red": "#800000",
            "light red": "#ff0000",
            "green": "#008000",
            "light green": "#00ff00",
            "yellow": "#808000",
            "light yellow": "#ffff00",
            "blue": "#000080",
            "light blue": "#0000ff",
            "magenta": "#800080",
            "light magenta": "#ff00ff",
            "cyan": "#008080",
            "light cyan": "#00ffff",
            "white": "#c0c0c0",
            "light white": "#ffffff",
        }
        # try get colors from xrdb
        xrdb_colors = get_xrdb_colors()
        if xrdb_colors is not None:
            self.colors = xrdb_colors

        super(LightMenu, self).__init__(
            id, title, grid, row, column, row_span, column_span, padx, pady, logger
        )
        self.set_help_text(
            "Lights: arrow keys to navigate,"
            " j and k to change brightness,"
            " c to set color, Enter to toggle,"
            " ESC to exit"
        )
        self.add_item_list([light.name for light in self.lights])
        self.add_key_command(Keys.KEY_ENTER, self.toggle)
        self.add_key_command(Keys.KEY_K_LOWER, command=self.inc_bri)
        self.add_key_command(Keys.KEY_J_LOWER, command=self.dec_bri)
        self.add_key_command(Keys.KEY_C_LOWER, self.popup)

    def toggle(self) -> None:
        """Toggle light."""
        self.lights[self.get_selected_item_index()].toggle()

    def inc_bri(self) -> None:
        """Increase brightness."""
        self.lights[self.get_selected_item_index()].brightness += 10

    def dec_bri(self) -> None:
        """Increase brightness."""
        self.lights[self.get_selected_item_index()].brightness -= 10

    def popup(self) -> None:
        """Show color picker popup."""
        self.master.show_menu_popup("Color", self.colors.keys(), self.set_picked_color)

    def set_picked_color(self, color: str) -> None:
        """set picked color by converting it to rgb.

        Args:
            color (str): color name
        """
        selCol = self.colors[color].strip("#")
        rgbTup = tuple(int(selCol[i : i + 2], 16) for i in (0, 2, 4))
        rgbCol = RGB(rgbTup[0], rgbTup[1], rgbTup[2])
        self.lights[self.get_selected_item_index()].on = True
        self.lights[self.get_selected_item_index()].color = rgbCol
