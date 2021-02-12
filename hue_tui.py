#!/usr/bin/env python3
'''
HUE-TUI
written by channel-42
'''
import sys
import json
import os
import time
import random
import subprocess
import py_cui as cui
from colorthief import ColorThief
from PIL import ImageColor
from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color
from os.path import expanduser
from hue_snek_pkg.hue_snek import Hue, Light
# change config path here if needed
CONFIG_PATH = "~/.config/hue-tui/config.py"
sys.path.append(os.path.dirname(os.path.expanduser(CONFIG_PATH)))
import config
HOME = expanduser("~")


def ensure_dir(file_path):
    """ensure_dir.
    makes sure that directory exists and creates one should
    the directory not exist
    Args:
        file_path: path to file
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def login():
    """login.
    checks if userdata has been inserted into json file
    """
    try:
        with open(f"{HOME}/.config/hue-tui/login.json") as f:
            data = json.load(f)
            ip = data["ip"]
            user = data["user"]
        if (ip != "") and (user != ""):
            return data
    except Exception:
        return 1


class LoginMaker:
    """LoginMaker.
    Main login creator
    """

    def __init__(self, master):
        self.master = master

        self.ip_field = self.master.add_text_box("Enter bridge's IP", 0, 0, 1,
                                                 2)
        self.user_field = self.master.add_text_box("Enter the API user", 1, 0,
                                                   1, 2)
        self.submit_button = self.master.add_button("Make Login",
                                                    2,
                                                    0,
                                                    1,
                                                    2,
                                                    command=self.make_login)

    def make_login(self):
        """make_login.
        Gets field data and dumps it as json to a file
        """
        ip = self.ip_field.get()
        user = self.user_field.get()
        open(f"{HOME}/.config/hue-tui/login.json", "w").close()
        data = {"ip": ip, "user": user, "wpp": None}
        with open(f"{HOME}/.config/hue-tui/login.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.master.show_message_popup("File created, please restart hue-tui",
                                       f'ip: {ip}, user: {user}')
        return 0


class HueTui:
    def __init__(self, master):
        """__init__.

        Args:
            master: py_cui root module
        """
        self.master = master
        self.scene = None
        self.bridge = []  # bridge info array
        self.active = list()
        self.step = config.STEP_SIZE
        self.disco = False
        self.WALL = None
        # used for changing light and group color
        self.color_dict = config.COLOR_DICT
        self.colors = ["red", "blue", "green", "purple", "teal"]

        # UI COLORS
        self.color = config.COLOR
        self.selected_color = config.SELECTED_COLOR
        self.border_color = config.BORDER_COLOR
        self.logo_color = config.LOGO_COLOR
        self.statusbar_color = config.STATUSBAR_COLOR
        self.titlebar_color = config.TITLEBAR_COLOR
        # will be added when fixed
        # self.border_selected_color = None
        # set unicode borders
        if config.UNICODE:
            self.master.toggle_unicode_borders()
        # add banner
        self.logo = self.master.add_block_label(
                str(self.get_logo_text()), 0, 0, 1, 2)

        # items for each menu
        self.lights = H.get_lights("name").values()
        self.groups = H.get_groups("name").values()
        self.scenes = H.get_scenes("name").values()
        # add items to bridge array (dict -> array)
        for param, val in H.get_bridge_info().items():
            self.bridge.append(f"{param}: {val}")
        counter = 0
        for light in H.get_lights():
            counter += 1
        self.bridge.append(f"detected lights: {counter}")
        # creating each menu
        self.lights_menu = self.master.add_scroll_menu("Lights", 1, 0, 2, 2)
        self.groups_menu = self.master.add_scroll_menu("Groups", 3, 0, 2, 2)
        self.scenes_menu = self.master.add_scroll_menu("Scenes", 1, 2, 2, 2)
        self.active_box = self.master.add_scroll_menu("Active", 3, 2, 2, 2)
        # add active lights and groups to self.active
        # this also inits self.active_box with text
        self.is_active()
        self.active_box.set_selectable(False)
        self.bridge_information = self.master.add_scroll_menu(
            "Hue Bridge", 0, 2, 1, 2)
        self.xdrb_random = self.master.add_button("random XRDB colors",
                                                  5,
                                                  0,
                                                  1,
                                                  2,
                                                  command=self.set_xrdb_colors)
        self.wallpaper_color = self.master.add_button(
            "wallpaper colors", 5, 2, 1, 2, command=self.set_wallpaper_colors)
        # adding items to each menu
        self.lights_menu.add_item_list(self.lights)
        self.groups_menu.add_item_list(self.groups)
        self.scenes_menu.add_item_list(self.scenes)
        self.bridge_information.add_item_list(self.bridge)

        self.master.set_widget_cycle_key(cui.keys.KEY_TAB)
        # adding keycommands
        # LIGHTS
        self.lights_menu.add_key_command(cui.keys.KEY_ENTER, self.toggle_light)
        self.lights_menu.add_key_command(cui.keys.KEY_K_LOWER,
                                         command=self.inc_light_bri)
        self.lights_menu.add_key_command(cui.keys.KEY_J_LOWER,
                                         command=self.dec_light_bri)
        self.lights_menu.add_key_command(cui.keys.KEY_D_LOWER,
                                         self.disco_toggle)
        self.lights_menu.add_key_command(cui.keys.KEY_C_LOWER,
                                         self.light_color_popup)

        # GROUPS
        self.groups_menu.add_key_command(cui.keys.KEY_ENTER, self.toggle_group)
        self.groups_menu.add_key_command(cui.keys.KEY_K_LOWER,
                                         self.inc_group_bri)
        self.groups_menu.add_key_command(cui.keys.KEY_J_LOWER,
                                         self.dec_group_bri)
        self.groups_menu.add_key_command(cui.keys.KEY_C_LOWER,
                                         self.group_color_popup)
        # SCENES
        self.scenes_menu.add_key_command(cui.keys.KEY_ENTER,
                                         command=self.scene_popup)
        # setup colors
        self.load_wpp()
        for key in self.master._widgets.keys():
            self.master.get_widgets()[key].set_color(self.color)
            self.master.get_widgets()[key].set_selected_color(
                    self.selected_color)
            self.master.get_widgets()[key].set_border_color(self.border_color)
            # broken for some reason
            # self.master.get_widgets()[key].set_focus_border_color(self.border_selected_color)
        self.logo.set_color(self.logo_color)
        self.master.status_bar.set_color(self.statusbar_color)
        self.master.title_bar.set_color(self.titlebar_color)

    def load_wpp(self):
        """load_wpp.
        Load user wallpaper if set in config.py
        """
        # load wallpaper from given path or feh
        if config.WPP is None:
            try:
                with open(f"{HOME}/.fehbg", "r") as bgf:
                    bg_data = bgf.read().replace("\n", "").replace(
                        "#!/bin/shfeh --no-fehbg --bg-fill '",
                        "").replace("' ", "")
                    self.WALL = bg_data
            except Exception:
                None
        else:
            self.WALL = config.WPP

    def toggle_light(self):
        """toggle_light.
        Toggles a light on or off
        """
        # toggle a light
        states = H.get_lights()
        for light in states.items():
            if str(self.lights_menu.get()) == str(light[1].name):
                if light[1].state:
                    H.set_light(light[0], "on", "false")
                else:
                    H.set_light(light[0], "on", "true")

        self.is_active()

    def toggle_group(self):
        """toggle_group.
        Toggle a entire group on or off
        """
        # toggle a group
        states = H.get_groups()
        for group in states.items():
            if str(self.groups_menu.get()) == str(group[1]["name"]):
                if group[1]["action"]["on"]:
                    H.set_group(group[0], "on", "false")
                else:
                    H.set_group(group[0], "on", "true")

        self.is_active()

    def scene_popup(self):
        """scene_popup.
        Generates popup to select group to apply scene
        """
        # main scene menu with popup to select which group is affected
        groups = list(H.get_groups("name").values())

        self.scene = str(self.scenes_menu.get())

        self.master.show_menu_popup(
            "Select to which group the scene should be applied", groups,
            self.enable_scene)

    def enable_scene(self, inp):
        """enable_scene.

        Args:
            inp: the selected group from the popup menu
        """
        # enable scene
        group = str(inp)
        groups = H.get_groups("name")

        if group in groups.values():
            group_id = list(groups.keys())[list(groups.values()).index(group)]

            H.set_scene(group_id, self.scene)

    def get_logo_text(self):
        """get_logo_text.
            makes the logo banner with linebreaks
        """
        # make banner

        logo =        '██╗  ██╗██╗   ██╗███████╗              ████████╗██╗   ██╗██╗\n'
        logo = logo + '██║  ██║██║   ██║██╔════╝              ╚══██╔══╝██║   ██║██║\n'
        logo = logo + '███████║██║   ██║█████╗      █████╗       ██║   ██║   ██║██║\n'
        logo = logo + '██╔══██║██║   ██║██╔══╝      ╚════╝       ██║   ██║   ██║██║\n'
        logo = logo + '██║  ██║╚██████╔╝███████╗                 ██║   ╚██████╔╝██║\n'
        logo = logo + '╚═╝  ╚═╝ ╚═════╝ ╚══════╝                 ╚═╝    ╚═════╝ ╚═╝\n'

        return logo

    def is_active(self):
        """is_active.
        checks what lights and groups are active and adds them to a string
        """
        self.active.clear()
        self.active_box.clear()
        self.active.append("Lights:")
        for ident, light in H.get_lights().items():
            if light.state:
                light = str(light.name)
                self.active.append(light)

        self.active.append("")
        self.active.append("Groups:")

        for ident, value in H.get_groups().items():
            if value["action"]["on"]:
                group = str(H.get_group(int(ident), "name"))
                self.active.append(group)

        self.active_box.add_item_list(self.active)
        """
        self.active = "Lights:\n"
        for ident, light in H.get_lights().items():
            if light.state:
                light = str(light.name)
                self.active += f'{light}\n'

        self.active += '\nGroups:\n'

        for ident, value in H.get_groups().items():
            if value["action"]["on"]:
                group = str(H.get_group(int(ident), "name"))
                self.active += f'{group}\n'

        self.active_box.clear()
        self.active_box.write(self.active)
        """

    def hex_to_xy(self, hex_color):
        """hex_to_xyz.
        Converts a hex color to a xy
        Args:
            hex_color: Hex color as string and with #
        Returns:
            A tupel with X, Y values (normalized)
        """
        rgb_tuple = ImageColor.getrgb(str(hex_color))
        rgb_obj = sRGBColor(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        xyz = convert_color(
            rgb_obj,
            XYZColor,
        )
        tup = xyz.get_value_tuple()
        if tup[0] + tup[1] + tup[2] > 0:
            X = tup[0] / (tup[0] + tup[1] + tup[2])
            Y = tup[1] / (tup[0] + tup[1] + tup[2])
        else:
            X = 0
            Y = 0.001
        return (X, Y)

    def get_xresources(self):
        """get_xresources.
        Gets as colors from the users .Xresources file
        Returns:
            A array with all colors in hex
        """
        cmd = "xrdb -query|grep 'color'|cut -f 2|sort -u"
        hex_array = subprocess.check_output(
            cmd, shell=True, universal_newlines=True).split('\n')[:-1]
        return hex_array

    def set_xrdb_colors(self):
        """set_xrdb_colors.
        Selects random colors from .Xresources and sets all lights to them
        """
        random_xy = []
        for color in self.get_xresources():
            xy_color = self.hex_to_xy(color)
            random_xy.append(xy_color)

        self.toggle_light()
        for light in H.get_lights('id'):
            random_color = random.choice(random_xy)
            x = random_color[0] + 0.05
            y = random_color[1] + 0.05
            H.set_light(light, "on", "true")
            H.set_light(light, "bri", "250")
            H.set_light(light, "xy", f"[{x}, {y}]")
            self.master.show_message_popup(
                "Info:", "Setting your lights to your XRDB colors")
        return 0

    def get_main_colors(self, file):
        """get_main_colors.
        gets main 4 colors from a given image file
        Args:
            file: path to image file
        """
        color_thief = ColorThief(file)
        return color_thief.get_palette(color_count=3, quality=50)

    def rgb_to_xy(self, rgb_color):
        """rgb_to_xy.
        convert a rgb tuple to a xy tuple
        Args:
            rgb_color: rgb tuple
        """
        rgb_obj = sRGBColor(rgb_color[0], rgb_color[1], rgb_color[2])
        xyz = convert_color(
            rgb_obj,
            XYZColor,
        )
        tup = xyz.get_value_tuple()
        if tup[0] + tup[1] + tup[2] > 0:
            X = tup[0] / (tup[0] + tup[1] + tup[2])
            Y = tup[1] / (tup[0] + tup[1] + tup[2])
        else:
            X = 0
            Y = 0.001
        return (X, Y)

    def set_wallpaper_colors(self):
        """set_wallpaper_colors.
        sets lights to main colors of wallpaper defined in the config
        """
        try:
            main_colors = self.get_main_colors(self.WALL)
        except Exception:
            self.master.show_error_popup(
                "No wallpaper set",
                "Check the config. e.g.: /home/<user>/path/to/file.jpg")
            return 1
        xy_colors = []
        for color in main_colors:
            xy_colors.append(self.rgb_to_xy(color))

        self.toggle_light()
        for light in H.get_lights('id'):
            random_color = random.choice(xy_colors)
            x = random_color[0] + 0.05
            y = random_color[1] + 0.05
            H.set_light(light, "on", "true")
            H.set_light(light, "bri", "250")
            H.set_light(light, "xy", f"[{x}, {y}]")
            self.master.show_message_popup(
                "Info:", "Setting your lights to your wallpaper colors")
        return 0

    def inc_light_bri(self):
        """inc_light_bri.
        increases a lights brightness by 30 steps
        """
        lights = H.get_lights()
        keys = list(lights.keys())
        for light, ident in zip(lights.items(), keys):
            if str(self.lights_menu.get()) == str(light[1].name):
                current = light[1].brightness
                new = int(current) + self.step
                if new > 255:
                    new = 255
                Light(ident, H).set("bri", f"{new}")
                return 0

    def dec_light_bri(self):
        """inc_light_bri.
        decreases a lights brightness by 30 steps
        """
        lights = H.get_lights()
        keys = list(lights.keys())
        for light, ident in zip(lights.items(), keys):
            if str(self.lights_menu.get()) == str(light[1].name):
                current = light[1].brightness
                new = int(current) - self.step
                if new > 255:
                    new = 255
                Light(ident, H).set("bri", f"{new}")
                return 0

    def inc_group_bri(self):
        """inc_group_bri.
        increases a groups brightness
        """
        groups = H.get_groups()
        keys = list(groups.keys())
        for group, ident in zip(groups.items(), keys):
            if str(self.groups_menu.get()) == str(group[1]["name"]):
                current = H.get_group(ident, "bri")
                new = int(current) + self.step
                if new > 255:
                    new = 255
                H.set_group(ident, "bri", f"{new}")
                return 0

    def dec_group_bri(self):
        """inc_group_bri.
        increases a groups brightness
        """
        groups = H.get_groups()
        keys = list(groups.keys())
        for group, ident in zip(groups.items(), keys):
            if str(self.groups_menu.get()) == str(group[1]["name"]):
                current = H.get_group(ident, "bri")
                new = int(current) - self.step
                if new > 255:
                    new = 255
                H.set_group(ident, "bri", f"{new}")
                return 0

    def disco_toggle(self):
        """disco_toggle.
        show popup and toggle disco mode
        """
        self.master.show_yes_no_popup(
            "Disco Mode? Once activated, press STRG+C to quit ",
            self.disco_mode)
        return 0

    def disco_mode(self, dummy):
        """disco_mode.
            toggle disco mode :^)
        """
        if not dummy:
            return 1
        lights = H.get_lights()
        try:
            for light in lights.items():
                H.set_light(light[0], "bri", '150')
            while True:
                for light in lights.items():
                    random_hue = random.randrange(0, 50000)
                    random_sat = random.randrange(0, 255)
                    H.set_light(light[0], "hue", f'{random_hue}')
                    H.set_light(light[0], "sat", f'{random_sat}')
                time.sleep(0.5)
        except KeyboardInterrupt:
            return 1

    def light_color_popup(self):
        """group_color_popup.
        Popup for selecting and setting a lights's color
        """
        self.light = str(self.lights_menu.get())
        self.master.show_menu_popup("Which color should be applied?",
                                    self.colors, self.set_light_color)

    def set_light_color(self, inp):
        """set_group_color.
        Sets whole light's color to passed color
        Args:
            inp: color name passed by popup menu
        """
        color = self.color_dict[f"{inp}"]
        lights = H.get_lights()
        x = self.hex_to_xy(color)[0]
        y = self.hex_to_xy(color)[1]
        for light in lights.items():
            if str(self.lights_menu.get()) == str(light[1].name):
                H.set_light(light[0], "on", "true")
                H.set_light(light[0], "xy", f"[{x}, {y}]")
        return 0

    def group_color_popup(self):
        """group_color_popup.
        Popup for selecting and setting a group's color
        """
        self.group = str(self.groups_menu.get())
        self.master.show_menu_popup("Which color should be applied?",
                                    self.colors, self.set_group_color)

    def set_group_color(self, inp):
        """set_group_color.
        Sets whole group's color to passed color
        Args:
            inp: color name passed by popup menu
        """
        color = self.color_dict[f"{inp}"]
        groups = H.get_groups()
        x = self.hex_to_xy(color)[0]
        y = self.hex_to_xy(color)[1]
        for group in groups.items():
            if str(self.groups_menu.get()) == str(group[1]['name']):
                H.set_group(group[0], "on", "true")
                H.set_group(group[0], "xy", f"[{x}, {y}]")
        return 0


# check if config directory exists
ensure_dir(f"{HOME}/.config/hue-tui/")
# START-UP PROCEDURE
# check if config exists, then check for connection to Bridge
if login() == 1:
    log = cui.PyCUI(3, 2)
    log.set_title("Login Maker")
    Login = LoginMaker(log)
    log.start()

else:
    H = Hue(login()["ip"], login()["user"])

    if int(H.checkup()) == 1:
        raise Exception("Error while connecting to the Hue API")
        sys.exit(0)

    root = cui.PyCUI(6, 4)
    root.set_title("Hue TUI")
    Main = HueTui(root)
    root.start()
