import sys
import subprocess


def get_xrdb_colors() -> dict[str, str] | None:
    """
    Returns:
        None: if no xrdb is present on system
        dict[str, str]: a dict of color names and corresponding hex values
    """
    colors = bytearray()
    err = None
    if sys.platform == "linux":
        try:
            colors, err = subprocess.Popen(
                ["xrdb", "-query"], stdout=subprocess.PIPE
            ).communicate()
        # parse colors
        except Exception:
            pass
        finally:
            if err is None and len(colors) > 0:
                # xrdb is working
                colors = colors.decode().split("\n")
                colors = [
                    col.split("\t")[1] for col in colors if col.startswith("*.color")
                ]
                return {
                    "black": colors[0],
                    "gray": colors[1],
                    "red": colors[2],
                    "light red": colors[3],
                    "green": colors[4],
                    "light green": colors[5],
                    "yellow": colors[6],
                    "light yellow": colors[7],
                    "blue": colors[8],
                    "light blue": colors[9],
                    "magenta": colors[10],
                    "light magenta": colors[11],
                    "cyan": colors[12],
                    "light cyan": colors[13],
                    "white": colors[14],
                    "light white": colors[15],
                }
    return None
