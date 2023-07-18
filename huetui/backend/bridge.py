from dataclasses import dataclass
from huetui.backend.utils import Util
from huetui.backend.light import Light, RGB
from huetui.backend.scene import Scene
from huetui.backend.group import Group
from os.path import expanduser
from sys import exit as sysexit
from traceback import print_exc
from colorthief import ColorThief

import random


@dataclass
class Info:
    """
    Dataclass for the bridge's metadata.
    """

    name: str
    id: str
    mac: str
    ip: str
    sw_version: str
    api_version: str


class Bridge(Util):
    """Class representing a philips hue bridge.

    Args:
        Util (class): parent class containing some utility methods

    Attributes:
        _url (str): url of the bridge
        _lights (list): list of lights connected to the bridge
        _scenes (list): list of scenes defined on bridge
        _groups (list): list of groups defined on bridge
        _info (class): bridge's metadata
    """

    def __init__(self, url: str) -> None:
        self._url = url
        self._lights = []
        self._scenes = []
        self._groups = []

        self._info: Info = None

        # init bridge from api
        try:
            self._init_lights_from_api()
            self._init_scenes_from_api()
            self._init_groups_from_api()
            self._init_info_from_api()
        except Exception:
            print("Could not connect to bridge. Reason:")
            print_exc(limit=1)
            sysexit(1)

    def _init_lights_from_api(self) -> None:
        """
        initialize all lights by querying the api
        """
        addr = self._url + f"/lights"
        lights = self.api_get(addr)

        for lid in lights:
            self._lights.append(Light(self, int(lid)))

    def _init_scenes_from_api(self) -> None:
        """
        initialize all scenes by querying the api
        """
        addr = self._url + f"/scenes"
        scenes = self.api_get(addr)

        # for each scene
        for sid in scenes:
            name = scenes[sid]["name"]
            lights = []

            # find lights from scene in bridge
            for lid in scenes[sid]["lights"]:
                light = self.light_by_id(int(lid))

                # check if light is found
                if light:
                    lights.append(light)

            # create scene object and append
            self._scenes.append(Scene(self, sid, name, lights))

    def _init_groups_from_api(self) -> None:
        """
        initialize all groups by querying the api
        """
        addr = self._url + f"/groups"
        groups = self.api_get(addr)

        # for each scene
        for gid in groups:
            name = groups[gid]["name"]
            lights = []

            # find lights from scene in bridge
            for lid in groups[gid]["lights"]:
                light = self.light_by_id(int(lid))

                # check if light is found
                if light:
                    lights.append(light)

            # create scene object and append
            self._groups.append(Group(self, int(gid), name, lights))

    def _init_info_from_api(self) -> None:
        """
        initialize the bridge's metadata by querying the api
        """
        addr = self._url + f"/config"
        info = self.api_get(addr)

        self._info = Info(
            name=info["name"],
            id=info["bridgeid"],
            mac=info["mac"],
            ip=info["ipaddress"],
            sw_version=info["swversion"],
            api_version=info["apiversion"],
        )

    def light_by_id(self, lid: int) -> Light:
        """find light by id

        Args:
            lid (int): id of the light

        Returns:
            Light: light object with passed id
        """
        for light in self._lights:
            if light.lid == lid:
                return light
        return None

    def light_by_name(self, name: str) -> Light:
        """find light by name

        Args:
            name (str): name of the light

        Returns:
            Light: light object with passed name
        """
        for light in self._lights:
            if light.name == name:
                return light
        return None

    def scene_by_id(self, sid: str) -> Scene:
        """find scene by id

        Args:
            sid (str): id of the scene

        Returns:
            Scene: scene object with passed id
        """
        for scene in self._scenes:
            if scene.sid == sid:
                return scene
        return None

    def scene_by_name(self, name: str) -> Scene:
        """find scene by name

        Args:
            name (str): name of the scene

        Returns:
            Scene: scene object with passed name
        """
        for scene in self._scenes:
            if scene.name == name:
                return scene
        return None

    def group_by_id(self, gid: int) -> Group:
        """find group by id

        Args:
            gid (str): id of the group

        Returns:
            Group: group object with passed id
        """
        for group in self._groups:
            if group.gid == gid:
                return group
        return None

    def group_by_name(self, name: str) -> Group:
        """find group by name

        Args:
            name (str): name of the group

        Returns:
            Group: group object with passed name
        """
        for group in self._groups:
            if group.name == name:
                return group
        return None

    def scene_by_name(self, name: str) -> Scene:
        """find scene by name

        Args:
            name (str): name of the scene

        Returns:
            Scene: scene object with passed name
        """
        for scene in self._scenes:
            if scene.name == name:
                return scene
        return None

    def set_scene(self, group: Group, scene: Scene) -> bool:
        """set a scene for a group

        Args:
            group (Group): group object
            scene (Scene): scene object

        Returns:
            bool: True if successful, False otherwise
        """
        return scene.set_to_group(group)

    @property
    def url(self) -> str:
        return self._url

    @property
    def lights(self) -> list:
        return self._lights

    @property
    def scenes(self) -> list:
        return self._scenes

    @property
    def groups(self) -> list:
        return self._groups

    @property
    def info(self) -> Info:
        return self._info

    def info_as_str(self) -> str:
        """return bridge's metadata as string

        Returns:
            str: bridge's metadata as string
        """
        return f"Name:\t {self._info.name}\nID:\t {self._info.id}\nIP:\t {self._info.ip}\nMAC:\t {self._info.mac}\nSW:\t v{self._info.sw_version}\nAPI:\t v{self._info.api_version}"

    def set_lights_from_image(self, file) -> None:
        """set lights from image

        Args:
            file (str): path to image file
        """
        colors = ColorThief(expanduser(file)).get_palette(color_count=5, quality=50)
        rgbs = [RGB(*c) for c in colors]

        for light in self.lights:
            if light.on:
                light.color = random.choice(rgbs)
