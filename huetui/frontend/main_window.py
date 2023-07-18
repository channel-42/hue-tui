import py_cui as cui
from py_cui import keys as Keys

from huetui.backend.bridge import Bridge
from huetui.backend.utils import Config

from huetui.frontend.lights_menu import LightMenu
from huetui.frontend.groups_menu import GroupMenu
from huetui.frontend.scenes_menu import SceneMenu

import time, threading


class extPyCUI(cui.PyCUI):
    """Extends the PyCUI class to add a light menu widget.

    Args:
        x (int): width of the window
        y (int): height of the window
        bridge (Bridge): bridge object
    """

    def __init__(self, x: int, y: int, bridge: Bridge) -> None:
        self.bridge = bridge
        super(extPyCUI, self).__init__(x, y)

    def add_light_menu(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int,
        column_span: int,
        padx=1,
        pady=1,
    ) -> None:
        """Adds a light menu widget to the root.

        Args:
            title (str): menu title
            row (int): x position of the menu
            column (int): y position of the menu
            row_span (int): x width of the menu
            column_span (int): y height of the menu
            padx (int, optional): x padding .Defaults to 0.
            pady (int, optional): y padding. Defaults to 0.

        """
        id = f"Widget{len(self._widgets.keys())}"
        new_light_menu = LightMenu(
            id,
            title,
            self._grid,
            row,
            column,
            row_span,
            column_span,
            padx,
            pady,
            self._logger,
            self.bridge,
            self,
        )
        self._widgets[id] = new_light_menu
        if self.set_selected_widget is None:
            self.set_selected_widget(id)
        return new_light_menu

    def add_group_menu(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int,
        column_span: int,
        padx=1,
        pady=1,
    ) -> None:
        """Adds a group menu widget to the root.

        Args:
            title (str): menu title
            row (int): x position of the menu
            column (int): y position of the menu
            row_span (int): x width of the menu
            column_span (int): y height of the menu
            padx (int, optional): x padding .Defaults to 0.
            pady (int, optional): y padding. Defaults to 0.

        """
        id = f"Widget{len(self._widgets.keys())}"
        new_group_menu = GroupMenu(
            id,
            title,
            self._grid,
            row,
            column,
            row_span,
            column_span,
            padx,
            pady,
            self._logger,
            self.bridge,
            self,
        )
        self._widgets[id] = new_group_menu
        if self.set_selected_widget is None:
            self.set_selected_widget(id)
        return new_group_menu

    def add_scene_menu(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int,
        column_span: int,
        padx=1,
        pady=1,
    ) -> None:
        """Adds a scene menu widget to the root.

        Args:
            title (str): menu title
            row (int): x position of the menu
            column (int): y position of the menu
            row_span (int): x width of the menu
            column_span (int): y height of the menu
            padx (int, optional): x padding .Defaults to 0.
            pady (int, optional): y padding. Defaults to 0.

        """
        id = f"Widget{len(self._widgets.keys())}"
        new_scene_menu = SceneMenu(
            id,
            title,
            self._grid,
            row,
            column,
            row_span,
            column_span,
            padx,
            pady,
            self._logger,
            self.bridge,
            self,
        )
        self._widgets[id] = new_scene_menu
        if self.set_selected_widget is None:
            self.set_selected_widget(id)
        return new_scene_menu


class MainWindow:
    """Main HueTUI window class."""

    def __init__(self, master: extPyCUI, bridge: Bridge, config: Config) -> None:
        self.master = master
        self.bridge = bridge
        self._update_thread = None
        self.config = config

        # add menus to root
        self.logo = self.master.add_block_label(self._get_logo_text(), 0, 0, 1, 2)
        self.logo.set_selectable(False)
        self.info_menu = self.master.add_text_block(
            "Bridge", 0, 2, 1, 1, initial_text=self.bridge.info_as_str()
        )
        self.info_menu.set_selectable(False)
        self.key_menu = self.master.add_text_block(
            "Usage",
            0,
            3,
            1,
            1,
            initial_text="Movement: arrow-keys\nSelect: enter\nExit: esc\nQuit: q\nWallpaper colors: w",
        )
        self.key_menu.set_selectable(False)
        self.light_menu = self.master.add_light_menu("Lights", 1, 0, 2, 2)
        self.group_menu = self.master.add_group_menu("Groups", 3, 0, 2, 2)
        self.scene_menu = self.master.add_scene_menu("Scenes", 1, 2, 2, 2)
        self.active_menu = self.master.add_scroll_menu("Active", 3, 2, 2, 2, 1, 1)
        self.active_menu.set_selectable(False)

        # add keybindings
        self.master.add_key_command(Keys.KEY_W_LOWER, self._set_wallpaper_colors)

        # hook stop function to exit
        self.master.run_on_exit(self._stop_active_devices_thread)

        # refresh every 10ms
        self.master.set_refresh_timeout(0.1)

        # toggle unicode
        if config.tui_settings["unicode"]:
            self.master.toggle_unicode_borders()

        # start update thread
        self._init_active_devices_thread()

        # set ui colors
        for id in self.master._widgets.keys():
            self.master._widgets[id].set_color(
                config.tui_settings["uicolors"]["main_ui"]
            )
            self.master._widgets[id].set_selected_color(
                config.tui_settings["uicolors"]["selected"]
            )
            self.master._widgets[id].set_border_color(
                config.tui_settings["uicolors"]["border"]
            )
            self.master.status_bar.set_color(
                config.tui_settings["uicolors"]["status_bar"]
            )
            self.master.title_bar.set_color(
                config.tui_settings["uicolors"]["title_bar"]
            )
            self.logo.set_color(config.tui_settings["uicolors"]["logo"])

        self.active_menu.set_selected_color(config.tui_settings["uicolors"]["main_ui"])

    def _update_active_menu(self) -> None:
        """update the active menu with the active devices"""
        t = threading.currentThread()

        # should de thread be running?
        while getattr(t, "do_run", True):
            # list for all active devices
            active = []

            for light in self.bridge.lights:
                if light.on:
                    # add light to active list
                    format_str = f"({light.brightness}%) {light.name}"
                    active.append(format_str)

            # refresh active menu
            self.active_menu.clear()
            self.active_menu.add_item_list(active)

            time.sleep(0.1)

    def _init_active_devices_thread(self) -> None:
        """initializes the thread that updates the active devices menu"""
        # create new thread and start it
        self._update_thread = threading.Thread(target=self._update_active_menu)
        self._update_thread.start()

    def _stop_active_devices_thread(self) -> None:
        """stops the active devices update thread"""
        # stop the thread
        self._update_thread.do_run = False

    def _get_logo_text(self) -> str:
        """returns the logo banner with linebreaks"""

        logo = "                                                            \n"
        logo += "██╗  ██╗██╗   ██╗███████╗              ████████╗██╗   ██╗██╗\n"
        logo += "██║  ██║██║   ██║██╔════╝              ╚══██╔══╝██║   ██║██║\n"
        logo += "███████║██║   ██║█████╗      █████╗       ██║   ██║   ██║██║\n"
        logo += "██╔══██║██║   ██║██╔══╝      ╚════╝       ██║   ██║   ██║██║\n"
        logo += "██║  ██║╚██████╔╝███████╗                 ██║   ╚██████╔╝██║\n"
        logo += "╚═╝  ╚═╝ ╚═════╝ ╚══════╝                 ╚═╝    ╚═════╝ ╚═╝\n"

        return logo

    def _set_wallpaper_colors(self) -> None:
        """wrapper function to set the wallpaper colors and showing a status message"""
        self.master.show_loading_icon_popup(
            "Wallpaper colors", "Extracting and setting colors"
        )
        thread = threading.Thread(target=self._thread_set_wallpaper_colors)
        thread.start()

    def _thread_set_wallpaper_colors(self):
        """sets the lights color to the current colors of the wallpaper"""
        try:
            self.bridge.set_lights_from_image(self.config.tui_settings["wallpaper"])
            self.master.stop_loading_popup()
        except FileNotFoundError or KeyError:
            self.master.stop_loading_popup()
            self.master.show_error_popup(
                "Error",
                "Wallpaper "
                + self.config.tui_settings["wallpaper"]
                + " not found. Enter to continue.",
            )
