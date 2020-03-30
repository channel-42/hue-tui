#!/usr/bin/env python3
'''
New features from last realese: xrdb colors,
'''
import sys
import json
import re, subprocess, fnmatch, random
import py_cui as cui
import os
from PIL import ImageColor
from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color
from os.path import expanduser
from hue_snek_pkg.hue_snek import Hue, Light

HOME = expanduser("~")


def ensure_dir(file_path):
    """ensure_dir.
    makes sure that directory exists and creates one should the directory not exist
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
    except:
        #raise Exception("No IP and/or API user found")
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
        data = {"ip": ip, "user": user}
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
        self.bridge = []  #bridge info array
        self.active = ""

        #add banner
        self.master.add_block_label(str(self.get_logo_text()), 0, 0, 1, 2)

        #items for each menu
        self.lights = H.get_lights("name").values()
        self.groups = H.get_groups("name").values()
        self.scenes = H.get_scenes("name").values()

        #add items to bridge array (dict -> array)
        for param, val in H.get_bridge_info().items():
            self.bridge.append(f"{param}: {val}")

        #creating each menu
        self.lights_menu = self.master.add_scroll_menu("Lights", 1, 0, 2, 2)
        self.groups_menu = self.master.add_scroll_menu("Groups", 3, 0, 2, 2)
        self.scenes_menu = self.master.add_scroll_menu("Scenes", 1, 2, 2, 2)
        self.active_box = self.master.add_text_block("Active", 3, 2, 2, 2)
        self.bridge_information = self.master.add_scroll_menu(
            "Hue Bridge", 0, 2, 1, 1)
        self.xdrb_random = self.master.add_button(
            "Set active lights to random XRDB colors",
            0,
            3,
            1,
            1,
            command=self.set_xrdb_colors)

        #adding items to each menu
        self.lights_menu.add_item_list(self.lights)
        self.groups_menu.add_item_list(self.groups)
        self.scenes_menu.add_item_list(self.scenes)
        self.bridge_information.add_item_list(self.bridge)

        self.is_active()

        #adding keycommands
        self.lights_menu.add_key_command(cui.keys.KEY_ENTER, self.toggle_light)
        self.groups_menu.add_key_command(cui.keys.KEY_ENTER, self.toggle_group)
        self.scenes_menu.add_key_command(cui.keys.KEY_ENTER,
                                         command=self.scene_popup)

    def toggle_light(self):
        """toggle_light.
        Toggles a light on or off
        """
        #toggle a light
        states = H.get_lights()
        for light in states.items():
            if str(self.lights_menu.get()) == str(light[0].name):
                if light[1].state == True:
                    H.set_light(light[0], "on", "false")
                else:
                    H.set_light(light[0], "on", "true")

        self.is_active()

    def toggle_group(self):
        """toggle_group.
        Toggle a entire group on or off
        """
        #toggle a group
        states = H.get_groups()
        for group in states.items():
            if str(self.groups_menu.get()) == str(group[1]["name"]):
                if group[1]["action"]["on"] == True:
                    H.set_group(group[0], "on", "false")
                else:
                    H.set_group(group[0], "on", "true")

        self.is_active()

    def scene_popup(self):
        """scene_popup.
        Generates popup to select group to apply scene
        """
        #main scene menu with popup to select which group is affected
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
        #enable scene
        group = str(inp)
        groups = H.get_groups("name")

        if group in groups.values():
            group_id = list(groups.keys())[list(groups.values()).index(group)]

            H.set_scene(group_id, self.scene)

    def get_logo_text(self):
        """get_logo_text.
            makes the logo banner with linebreaks
        """
        #make banner

        logo = '██╗  ██╗██╗   ██╗███████╗              ████████╗██╗   ██╗██╗\n'
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
        self.active = "Lights:\n"

        for ident, light in H.get_lights().items():
            if light.state == True:
                light = str(light.name)
                self.active += f'{light}\n'

        self.active += '\nGroups:\n'

        for ident, value in H.get_groups().items():
            if value["action"]["on"] == True:
                group = str(H.get_group(int(ident), "name"))
                self.active += f'{group}\n'

        self.active_box.clear()
        self.active_box.write(self.active)

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
        X = tup[0] / (tup[0] + tup[1] + tup[2])
        Y = tup[1] / (tup[0] + tup[1] + tup[2])
        return (X, Y)

    def get_xresources(self):
        """get_xresources.
        Gets as colors from the users .Xresources file 
        Returns:
            A array with all colors in hex    
        """
        hex_array = []
        cmd = ['xrdb', '-query', '|', 'grep', '"*color"']
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        out_error_tuple = proc.communicate()
        list_out = out_error_tuple[0].decode("ascii").split("\n")
        matches = fnmatch.filter(list_out, '*color*')
        for entry in matches:
            cl = re.sub(r'.*#', '#', entry)
            hex_array.append(cl)

        return hex_array

    def set_xrdb_colors(self):
        """set_xrdb_colors.
        Selects random colors from .Xresources and sets all lights to them
        """
        random_xy = []
        for color in self.get_xresources():
            xy_color = self.hex_to_xy(color)
            random_xy.append(xy_color)

        for light in H.get_lights('id'):
            random_color = random.choice(random_xy)
            x = random_color[0]
            y = random_color[1]
            H.set_light(light, "xy", f"[{x}, {y}]")
            self.master.show_message_popup(
                "Info:", "Setting your lights to your XRDB colors")


#check if config directory exists
ensure_dir(f"{HOME}/.config/hue-tui/")

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

    root = cui.PyCUI(5, 4)
    root.set_title("Hue TUI")
    Main = HueTui(root)
    root.start()
