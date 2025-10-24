from Core.Settings import Constants
from string import Template
class StyleLoader:
    def __init__(self, theme="Light") -> None:
        self.theme = LIGHT_THEME if theme == "Light" else DARK_THEME

    def load_stylesheet(self) -> str:
        path = Constants.get_stylesheet()
        with open(path, "r") as f:
            content = f.read()
            return Template(content).substitute(self.theme)


LIGHT_THEME = {
    "main_bg": "#ffffff",
    "text_color": "#242424",
    "accent": "#555555",
    "accent_text": "#ffffff",
    "border_color": "#eeeeee",
    "button_bg": "#f8f8f8",
    "button_hover": "#eeeeee",
    "scrollbar_bg": "#f0f0f0",
    "scrollbar_handle": "#aaaaaa",
}

DARK_THEME = {
    "main_bg": "#2b2b2b",
    "text_color": "#dddddd",
    "accent": "#4a90e2",
    "accent_text": "#ffffff",
    "border_color": "#191919",
    "button_bg": "#3a3a3a",
    "button_hover": "#4a4a4a",
    "scrollbar_bg": "#2b2b2b",
    "scrollbar_handle": "#5a5a5a",
}
