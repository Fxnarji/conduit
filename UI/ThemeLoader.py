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
    "main_bg": "#DBDBDB",
    "layout_bg": "#EBEBEB",
    "text_color": "#323232",
    "accent": "#87A1BA",
    "accent_text": "#ECECEC",
    "border_color": "#9AA6B2",
    "button_bg": "#EBEBEB",
    "button_hover": "#D8DEE9",
    "scrollbar_bg": "#E5E9F0",
    "scrollbar_handle": "#A4CBF1",
    "title_bar": "#DBDBDB",
    "close_button": "#961f1f",
    "close_button_hover": "#e12525",
}


DARK_THEME = {
    "main_bg": "#2b2b2b",
    "layout_bg": "#3a3a3a",
    "text_color": "#dddddd",
    "accent": "#386382",
    "accent_text": "#ffffff",
    "border_color": "#191919",
    "button_bg": "#3a3a3a",
    "button_hover": "#4a4a4a",
    "scrollbar_bg": "#2b2b2b",
    "scrollbar_handle": "#5a5a5a",
    "title_bar": "#1e1e1e",
    "close_button": "#961f1f",
    "close_button_hover": "#e12525",
}
