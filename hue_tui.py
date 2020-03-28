#!/bin/python3

import sys
import json
import py_cui as cui
sys.path.append('/path')
from hue_snek import hue, Light


def login():
    """login.
    checks if userdate has been inserted into json file
    """
    with open("login.json") as f:
        data = json.load(f)
        ip = data["ip"]
        user = data["user"]
    if (ip != "") and (user != ""):
        return data
    else:
        raise Exception("No IP and/or API user found")
        return 1


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
        self.master.add_block_label(str(self.get_logo_text()), 0, 0)

        #items for each menu
        self.lights = H.get_lights("name").values()
        self.groups = H.get_groups("name").values()
        self.scenes = H.get_scenes("name").values()

        #add items to bridge array (dict -> array)
        for param, val in H.get_bridge_info().items():
            self.bridge.append(f"{param}: {val}")

        #creating each menu
        self.lights_menu = self.master.add_scroll_menu("Lights", 1, 0, 2, 1)
        self.groups_menu = self.master.add_scroll_menu("Groups", 3, 0, 2, 1)
        self.scenes_menu = self.master.add_scroll_menu("Scenes", 1, 1, 2, 1)
        self.active_box = self.master.add_text_block("Active", 3, 1, 2, 1)
        self.bridge_information = self.master.add_scroll_menu(
            "Hue Bridge", 0, 1, 1, 1)

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
            if str(self.lights_menu.get()) == str(light[1].name):
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


H = hue(login()["ip"], login()["user"])

if int(H.checkup()) == 1:
    print("Error while connecting to the Hue API")
    sys.exit(0)

root = cui.PyCUI(5, 2)
root.set_title("Hue TUI")
Main = HueTui(root)
root.start()
