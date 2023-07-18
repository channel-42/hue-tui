import py_cui.keys as Keys
import py_cui.grid as Grid
import py_cui.widgets as Widgets

from py_cui.debug import PyCUILogger as Logger
from huetui.backend.bridge import Bridge


class SceneMenu(Widgets.ScrollMenu):
    """Scene menu widget.

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
        self.bridge = bridge
        self.scenes = bridge.scenes
        self.groups = bridge.groups
        self.master = master
        super(SceneMenu, self).__init__(
            id, title, grid, row, column, row_span, column_span, padx, pady, logger
        )
        self.set_help_text(
            "Scenes: arrow keys to navigate,"
            " ENTER to select,"
            " ESC to exit"
        )
        self.add_item_list([scene.name for scene in self.scenes])
        self.add_key_command(Keys.KEY_ENTER, self.popup)

    def popup(self) -> None:
        """popup to select which group to set the scene to"""
        groups = [group.name for group in self.groups]
        self.master.show_menu_popup(
            "To which group?", [group.name for group in self.groups], self.set_scene
        )

    def set_scene(self, group: str) -> None:
        """set scene to a group. needs to be called from popup.

        Args:
            group (str): group name to set the scene to
        """
        scene = self.scenes[self.get_selected_item_index()]
        target = self.bridge.group_by_name(group)
        scene.set_to_group(target)
