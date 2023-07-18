import py_cui.keys as Keys
import py_cui.grid as Grid
import py_cui.widgets as Widgets
import subprocess

from py_cui.debug import PyCUILogger as Logger
from huetui.backend.bridge import Bridge
from huetui.backend.light import RGB


class GroupMenu(Widgets.ScrollMenu):
    """Group menu widget.

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
        # get colors from xrdb
        colors, err = subprocess.Popen(
            ["xrdb", "-query"], stdout=subprocess.PIPE
        ).communicate()
        # parse colors
        if err is None and len(colors) > 0:
            # xrdb is working
            colors = colors.decode().split("\n")
            colors = [col.split("\t")[1] for col in colors if col.startswith("*.color")]
            self.colors = {
                "black": colors[0],
                "gray": colors[1],
                "red": colors[2],
                "light red": colors[3],
                "green": colors[4],
                "light green": colors[5],
                "yellow": colors[6],
                "light yellow": colors[7],
                "blue": colors[8],
                "light blue": colors[9],
                "magenta": colors[10],
                "light magenta": colors[11],
                "cyan": colors[12],
                "light cyan": colors[13],
                "white": colors[14],
                "light white": colors[15],
            }
        else:
            # xrdb is not working, use fallback colors
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
        self.master = master
        self.groups = bridge.groups
        super(GroupMenu, self).__init__(
            id, title, grid, row, column, row_span, column_span, padx, pady, logger
        )
        self.set_help_text(
            "Groups: arrow keys to navigate,"
            " j and k to change brightness,"
            " c to set color, Enter to toggle,"
            " ESC to exit"
        )
        self.add_item_list([group.name for group in self.groups])
        self.add_key_command(Keys.KEY_ENTER, self.toggle)
        self.add_key_command(Keys.KEY_K_LOWER, command=self.inc_bri)
        self.add_key_command(Keys.KEY_J_LOWER, command=self.dec_bri)
        self.add_key_command(Keys.KEY_C_LOWER,
                                         self.popup)

    def toggle(self) -> None:
        """Toggle group on/off."""
        self.groups[self.get_selected_item_index()].all_on = not self.groups[
            self.get_selected_item_index()
        ].all_on

    def inc_bri(self) -> None:
        """Increase brightness of group."""
        self.groups[self.get_selected_item_index()].brightness += 10

    def dec_bri(self) -> None:
        """Decrease brightness of group."""
        self.groups[self.get_selected_item_index()].brightness -= 10

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
        self.groups[self.get_selected_item_index()].on = True
        for light in self.groups[self.get_selected_item_index()].lights:
            light.color = rgbCol

