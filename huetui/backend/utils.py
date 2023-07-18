from dataclasses import dataclass, field
from click import MissingParameter
import urllib3
from os import path
from sys import path as syspath
from os import makedirs 
import json

@dataclass
class Config:
    """
    Dataclass for huetui config.
    """

    tui_settings: dict = field(default_factory=dict)
    ip: str = ""
    api_user: str = ""


class Util:
    """
    Metaclass containing some utility methods
    """

    @staticmethod
    def value_to_percent(value, whole) -> int:
        """Converts a value to a percentage

        Args:
            value (number): value to convert
            whole (number): value of entire scale

        Returns:
            int: percentage
        """
        return round(((value / whole) * 100))

    @staticmethod
    def percent_to_value(percent, whole) -> int:
        """Converts a percentage to a value

        Args:
            percent (number): percentage to convert
            whole (number): value of entire scale

        Returns:
            int: value
        """
        return round((percent / 100) * whole)

    @staticmethod
    def api_get(address: str) -> dict:
        """Make a get request to the given address.

        Args:
            address (string): The address to make the request to. Defaults to None.

        Returns:
            dict: response from api.
        """
        if address:
            # try to create a connection
            http = urllib3.PoolManager()
            response = http.request("GET", address)

            # check if response ok
            if (response.status == 200) and not (
                response.data.decode("utf-8").startswith('[{"error":')
            ):
                payload = json.loads(response.data.decode("utf-8"))
                return dict(payload)

            else:
                raise Exception(
                    "Code: "
                    + str(response.status)
                    + "; API error: "
                    + response.data.decode("utf-8")
                )

        else:
            raise MissingParameter("adress")

    @staticmethod
    def api_put(address: str, data: str) -> bool:
        """Make a put request to the given address.

        Args:
            address (string, optional): The address to make the request to. Defaults to None.
            data (string, optional): The data to put. Defaults to None.

        Returns:
            bool: post successfull.
        """
        if address and data:
            http = urllib3.PoolManager()
            response = http.request(
                "PUT", address, body=data, headers={"Content-Type": "application/json"}
            )

            if (response.status == 200) and (
                response.data.decode("utf-8").startswith('[{"success":')
            ):
                return True
            else:
                raise Exception(
                    "Code: "
                    + str(response.status)
                    + "; API error: "
                    + response.data.decode("utf-8")
                )

        else:
            raise MissingParameter("adress or data")

    @staticmethod
    def __ensure_dir(paf: str) -> bool:
        dir = path.dirname(paf)
        if not path.exists(dir):
            makedirs(dir)
            return False
        else:
            return True
            
    @staticmethod
    def generate_config_file(ip: str, api_user: str, config_path: str) -> None:
        """Generate a config file with default values.
        """
        config = path.expanduser(config_path)
        Util._Util__ensure_dir(config)

        with open(config, 'w', encoding='utf-8') as f:
            f.write(
                "# sample config. Edit the dict to your liking.\n"
                "import py_cui.colors as colors\n"
                "from huetui.backend.utils import Config\n"
                "c = Config()\n"
                f"c.ip = \"{ip}\"\n"
                f"c.api_user = \"{api_user}\"\n"
                "c.tui_settings = {\n"
                "\t\"unicode\": True,\n"
                "\t\"wallpaper\": \"~/Path/To/Wallpaper.jpg\",\n"
                "\t\"uicolors\": {\n"
                "\t\t\"main_ui\": colors.WHITE_ON_BLACK,\n"
                "\t\t\"selected\": colors.CYAN_ON_BLACK,\n"
                "\t\t\"border\": colors.BLUE_ON_BLACK,\n"
                "\t\t\"logo\": colors.CYAN_ON_BLACK,\n"
                "\t\t\"status_bar\": colors.BLACK_ON_WHITE,\n"
                "\t\t\"title_bar\": colors.BLACK_ON_MAGENTA,\n"
                "\t},\n"
                "}\n"
            )
    
    @staticmethod
    def load_config_file(config_path: str) -> Config:
        """Load a config file and return config dataclass.

        Args:
            config_path (str): path to config file.

        Returns:
            Config: config object.
        """
        config = path.expanduser(config_path)
        syspath.append(path.dirname(path.expanduser(config_path)))
        try:
            from config import c
            return c
        except Exception as e:
            print("Config file not found. Generating a new config file.")
            ip = input("Bridge ip: ")
            api_user = input("Bridge api user: ")
            Util.generate_config_file(ip, api_user, config_path)
            from config import c
            return c           