from huetui.backend.utils import Util
import huetui.backend.bridge as Bridge


class Group(Util):
    """Class representing a group of lights.

    Args:
        Util (class): parent class containing some utility methods

    Attributes:
        _bridge (class): bridge the group is defined on
        _gid (int): id of the group
        _name (str): name of the group
        _lights (list): list of lights in the group
        _all_on (bool): on/off state of the group
    """

    def __init__(self, bridge: Bridge, gid: int, name: str, lights: list) -> None:
        self._bridge = bridge
        self._gid = gid
        self._name = name
        self._lights = lights
        self._all_on = None
        self._brightness = None

    def __str__(self) -> str:
        return "<class 'Group'> gid: {}".format(self._gid)

    def __repr__(self) -> str:
        return "<class 'Group'> gid: {}".format(self._gid)

    @property
    def gid(self) -> int:
        return self._gid

    @property
    def name(self) -> str:
        return self._name

    @property
    def lights(self) -> list:
        return self._lights

    @property
    def all_on(self) -> bool:

        try:
            addr = self._bridge._url + f"/groups/{self._gid}"
            self._all_on = self._bridge.api_get(addr)["state"]["all_on"]

        except Exception:
            pass

        return self._all_on

    @all_on.setter
    def all_on(self, value: bool) -> None:
        for light in self._lights:
            light.on = value

    @property
    def brightness(self) -> int:
        try:
            addr = self._bridge._url + f"/groups/{self._gid}"
            self._brightness = self.value_to_percent(
                self.api_get(addr)["action"]["bri"], 255
            )

        except Exception:
            pass

        return self._brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        if value > 0 and value <= 100:
            self._brightness = value
            addr = self._bridge._url + f"/groups/{self._gid}/action"
            val = self.percent_to_value(self._brightness, 255)
            self.api_put(addr, f'{{"bri": {val}}}')
