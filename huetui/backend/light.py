from typing import NamedTuple
from huetui.backend.utils import Util
from enum import Enum
import huetui.backend.bridge as Bridge
import colorsys


class RGB(NamedTuple):
    """Named tuple for RGB values.

    Args:
        NamedTuple (class): inherits from NamedTuple
    """

    r: int = 0
    g: int = 0
    b: int = 0


class HSV(NamedTuple):
    """Named tuple for HSV values.

    Args:
        NamedTuple (class): inherits from NamedTuple
    """

    h: int = 0
    s: int = 0
    v: int = 0


class Parameter(Enum):
    """
    Enum for the parameters of the light.
    """

    ON = "on"
    NAME = "name"
    BRIGHTNESS = "bri"
    HUE = "hue"
    SATURATION = "sat"
    REACHABLE = "reachable"


class Light(Util):
    """Class representing a light

    Args:
        Util (class): parent class containing some utility methods

    Attributes:
        _bridge (class): bridge the light is connected to
        _lid (int): id of the light
        _on (bool): on/off state of the light
        _name (str): name of the light
        _brightness (int): brightness of the light in percent
        _hue (int): hue of the light
        _saturation (int): saturation of the light
        _color (str): color of the light as rgb
        _reachable (bool): reachable state of the light
    """

    def __init__(self, bridge: Bridge, lid: int):
        """Contructor for Light class

        Args:
            bridge (class): bridge the light is connected to
            lid (int): id of the light
        """
        self._bridge = bridge

        self._lid = lid
        self._on = None
        self._name = None

        self._brightness = None
        self._hue = None
        self._saturation = None
        self._color = None

        self._reachable = None

        # try to get initial values from api
        try:
            self._on = self.get_api_param(Parameter.ON)
            self._brightness = self.get_api_param(Parameter.BRIGHTNESS)
            self._hue = self.get_api_param(Parameter.HUE)
            self._saturation = self.get_api_param(Parameter.SATURATION)
            self._reachable = self.get_api_param(Parameter.REACHABLE)

        except Exception:
            pass

    def __str__(self) -> str:
        return "<class 'Light'> lid: {}".format(self._lid)

    def __repr__(self) -> str:
        return "<class 'Light'> lid: {}".format(self._lid)

    def put_api_param(self, param: Parameter, value: str):
        """Update the light's state on the bridge

        Args:
            param (str): parameter to update
            value (str): value to update the parameter to

        Returns:
            bool: update successfull
        """
        try:

            data = f'{{"{param.value}":{value}}}'
            addr = self._bridge.url + f"/lights/{self._lid}/state"

            self.api_put(addr, data)

            return True

        except Exception as e:
            print(e)
            return False

    def get_api_param(self, param: Parameter):
        """Get the light's parameter from the api

        Args:
            param (str): parameter to get

        Returns:
            bool, str, int: value of the parameter
        """
        addr = self._bridge.url + f"/lights/{self._lid}"

        resp_dict = self.api_get(addr)
        val = resp_dict["state"][param.value]

        return val

    @staticmethod
    def hsv_to_rgb(h: int, s: int, v: int) -> RGB:
        """Converts hsv(65535, 100, 100) to rgb(255,255,255)

        Args:
            h (int): hue value
            s (int): saturation value
            v (int): brightness value

        Returns:
            RGB: red, green and blue, as a namedtuple
        """

        # normalize hue, saturation and brightness to 0-1
        h = h / 65535
        s = s / 100
        v = v / 100

        # convert to rgb
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)

        return RGB(round(r * 255), round(g * 255), round(b * 255))

    @staticmethod
    def rgb_to_hsv(r: int, g: int, b: int) -> HSV:
        """Converts rgb(255, 255, 255) to hsv(65535, 100, 100)

        Args:
            r (int): red value
            g (int): green value
            b (int): blue value

        Returns:
            HSV: hue, saturation and value, as a namedtuple
        """

        # normalize r, g, b to 0-1
        r = r / 255
        g = g / 255
        b = b / 255

        # convert to hsv
        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)

        return HSV(round(h * 65535), round(s * 100), round(v * 100))

    @property
    def lid(self) -> int:
        return self._lid

    @property
    def on(self) -> bool:
        # try to get value from api
        try:
            self._on = self.get_api_param(Parameter.ON)
        except Exception:
            pass

        return self._on

    @on.setter
    def on(self, value: bool) -> None:
        self._on = value
        self.put_api_param(Parameter.ON, str(self._on).lower())

    @property
    def name(self) -> str:
        # try to get value from api
        try:
            addr = self._bridge.url + f"/lights/{self._lid}"

            resp_dict = self.api_get(addr)
            val = resp_dict[Parameter.NAME.value]
            self._name = val

        except Exception as e:
            pass

        return self._name

    @property
    def brightness(self) -> int:
        # try to get value from api
        try:
            # convert value to percent
            self._brightness = self.value_to_percent(
                self.get_api_param(Parameter.BRIGHTNESS), 255
            )
        except Exception:
            pass

        return self._brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        # convert percentage to value (0-255)
        if value > 0 and value <= 100 and self.on and self.reachable:
            self._brightness = value
            self.put_api_param(
                Parameter.BRIGHTNESS, self.percent_to_value(self._brightness, 255)
            )

    @property
    def hue(self) -> int:
        # try to get value from api
        try:
            self._hue = self.get_api_param(Parameter.HUE)
        except Exception:
            pass

        return self._hue

    @hue.setter
    def hue(self, value: int) -> None:
        self._hue = value
        self.put_api_param(Parameter.HUE, self._hue)

    @property
    def saturation(self) -> int:
        # try to get value from api
        try:
            # convert value to percent
            self._saturation = self.value_to_percent(
                self.get_api_param(Parameter.SATURATION), 255
            )
        except Exception:
            pass

        return self._saturation

    @saturation.setter
    def saturation(self, value: int) -> None:
        # convert percentage to value (0-255)
        self._saturation = value
        self.put_api_param(
            Parameter.SATURATION, self.percent_to_value(self._saturation, 255)
        )

    @property
    def color(self) -> RGB:
        # try to get most recent values from api
        try:
            self._hue = self.get_api_param(Parameter.HUE)
            self._saturation = self.value_to_percent(
                self.get_api_param(Parameter.SATURATION), 255
            )
            self._brightness = self.value_to_percent(
                self.get_api_param(Parameter.BRIGHTNESS), 255
            )

        except Exception:
            pass

        self._color = self.hsv_to_rgb(self._hue, self._saturation, self._brightness)

        return self._color

    @color.setter
    def color(self, rgb: RGB) -> None:
        # convert rgb to hsv
        hsv = self.rgb_to_hsv(rgb.r, rgb.g, rgb.b)

        self._color = rgb

        self._hue = hsv.h
        self._saturation = hsv.s
        self._brightness = hsv.v

        # update api
        self.put_api_param(Parameter.HUE, self._hue)
        self.put_api_param(
            Parameter.SATURATION, self.percent_to_value(self._saturation, 255)
        )
        self.put_api_param(
            Parameter.BRIGHTNESS, self.percent_to_value(self._brightness, 255)
        )

    @property
    def reachable(self) -> bool:
        # try to get value from api
        try:
            self._reachable = self.get_api_param(Parameter.REACHABLE)
        except Exception:
            pass

        return self._reachable

    def toggle(self) -> None:
        """toggle a light on or off"""
        self.on = not self.on
