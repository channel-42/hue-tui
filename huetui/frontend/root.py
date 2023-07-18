from huetui.frontend.main_window import MainWindow, extPyCUI
from huetui.backend.bridge import Bridge
from huetui.backend.utils import Config


class Root:
    """Root class for the frontend."""
    def __init__(
        self, x: int, y: int, title: str, bridge: Bridge, config: Config
    ) -> None:
        root = extPyCUI(x, y, bridge)
        root.set_title(title)
        MainWindow(root, bridge, config)
        root.start()
        pass