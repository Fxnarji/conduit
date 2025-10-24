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
    "main_bg": "#E5E9F0",            # nord5 — soft polar snow background
    "layout_bg": "#ECEFF4",          # nord6 — light surface for contrast
    "text_color": "#2E3440",         # nord0 — dark slate for strong contrast
    "accent": "#5E81AC",             # nord10 — Arctic blue accent
    "accent_text": "#ECEFF4",        # nord6 — crisp light text on accent
    "border_color": "#D8DEE9",       # nord4 — subtle divider tone
    "button_bg": "#ECEFF4",          # nord6 — slightly raised button surface
    "button_hover": "#D8DEE9",       # nord4 — hover feedback with soft shadow
    "scrollbar_bg": "#E5E9F0",       # nord5 — neutral track background
    "scrollbar_handle": "#81A1C1",   # nord9 — blue handle accent (matches theme)
    "title_bar": "#3B4252",          # nord1 — darker band for contrast at top
    "close_button": "#BF616A",       # nord11 — muted red close
    "close_button_hover": "#D08770", # nord12 — warm highlight on hover
}


DARK_THEME = {
    "main_bg": "#2b2b2b",
    "layout_bg": "#3a3a3a",
    "text_color": "#dddddd",
    "accent": "#826d38",
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
