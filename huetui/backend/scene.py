from huetui.backend.group import Group
from huetui.backend.utils import Util
import huetui.backend.bridge as Bridge

class Scene(Util):
    """Class representing a scene.

    Args:
        Util (class): parent class containing some utility methods
    """
    def __init__(self, bridge: Bridge, sid: str, name: str, lights: list) -> None:
        self._bridge = bridge
        self._sid = sid
        self._name = name
        self._lights = lights

    def __str__(self) -> str:
        return "<class 'Scene'> sid: {}".format(self._sid)

    def __repr__(self) -> str:
        return "<class 'Scene'> sid: {}".format(self._sid)

    @property
    def sid(self) -> str:
        return self._sid

    @property
    def name(self) -> str:
        return self._name

    @property
    def lights(self) -> list:
        return self._lights

    def set_to_group(self, group: Group) -> bool:
        """Set a group to the scene.

        Args:
            group (class): group to set the scene to
        """
        addr = self._bridge._url + f"/groups/{group.gid}/action"
        payload = f"{{\"scene\": \"{self._sid}\"}}"
        return self.api_put(addr, payload)
