import eel
import os
import json


class NectarWindow:
    def __init__(
        self,
        project_dir=".",
        web_folder="web",
        port=8000,
        size=(1200, 800),
        icon=None,
        disable_menu=True,
        use_custom_titlebar=False,
        titlebar_bg="transparent",
        titlebar_symbol="#ffffff",
        titlebar_height=30,
        titlebar_html=""  # <-- new: custom HTML inside titlebar
    ):
        """
        :param project_dir: path to the project folder
        :param web_folder: name of the web folder inside project_dir
        :param port: port for Eel server
        :param size: window size
        :param icon: icon path relative to project_dir; defaults to NectarUI/icons/icon.png
        :param disable_menu: whether to hide Electron menu bar
        :param use_custom_titlebar: enable native titlebar overlay
        :param titlebar_bg: titlebar overlay background color
        :param titlebar_symbol: traffic light symbol color
        :param titlebar_height: overlay height
        :param titlebar_html: optional HTML string to place inside titlebar
        """
        self.project_dir = os.path.abspath(project_dir)
        self.web_folder = os.path.join(self.project_dir, web_folder)
        self.port = port
        self.size = size
        self.disable_menu = disable_menu
        self.use_custom_titlebar = use_custom_titlebar
        self.titlebar_bg = titlebar_bg
        self.titlebar_symbol = titlebar_symbol
        self.titlebar_height = titlebar_height
        self.titlebar_html = titlebar_html

        # Default icon path: NectarUI/icons/icon.png inside the module
        if icon is None:
            module_dir = os.path.dirname(os.path.abspath(__file__))
            self.icon = os.path.join(module_dir, "icons", "icon.png")
        else:
            self.icon = os.path.join(self.project_dir, icon)

    def _ensure_electron_files(self):
        package_path = os.path.join(self.project_dir, "package.json")
        mainjs_path = os.path.join(self.project_dir, "main.js")

        # package.json
        if not os.path.exists(package_path):
            package = {
                "name": os.path.basename(self.project_dir).lower(),
                "main": "main.js"
            }
            with open(package_path, "w", encoding="utf-8") as f:
                json.dump(package, f, indent=4)

        # main.js
        icon_path_js = self.icon.replace("\\", "/")

        # Build BrowserWindow options
        browser_window_options = [
            f"width: {self.size[0]}",
            f"height: {self.size[1]}",
            f"icon: path.join(__dirname, '{icon_path_js}')",
            "webPreferences: { nodeIntegration: true }"
        ]

        if self.disable_menu:
            browser_window_options.append("autoHideMenuBar: true")

        if self.use_custom_titlebar:
            browser_window_options.append(
                f"titleBarStyle: 'hidden',\n        titleBarOverlay: {{ color: '{self.titlebar_bg}', symbolColor: '{self.titlebar_symbol}', height: {self.titlebar_height} }}"
            )

        browser_window_options_str = ",\n        ".join(browser_window_options)

        mainjs_content = f"""
const {{ app, BrowserWindow }} = require("electron");
const path = require("path");

function createWindow() {{
    const win = new BrowserWindow({{
        {browser_window_options_str}
    }});

    win.loadURL("http://localhost:{self.port}/index.html");
}}

app.whenReady().then(createWindow);
"""

        with open(mainjs_path, "w", encoding="utf-8") as f:
            f.write(mainjs_content)

        # Inject custom titlebar HTML + drag CSS
        if self.use_custom_titlebar:
            index_html = os.path.join(self.web_folder, "index.html")
            os.makedirs(self.web_folder, exist_ok=True)
            if not os.path.exists(index_html):
                with open(index_html, "w", encoding="utf-8") as f:
                    f.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n<title>App</title>\n</head>\n<body>\n</body>\n</html>")

            with open(index_html, "r", encoding="utf-8") as f:
                content = f.read()

            # Prepare drag style + titlebar HTML
            if "<style id='custom-titlebar-drag'>" not in content:
                custom_html = f"""
<!-- CustomTitlebarDrag -->
<style id='custom-titlebar-drag'>
  body {{
    margin: 0;
  }}
  #titlebar {{
    -webkit-app-region: drag;
    height: {self.titlebar_height}px;
    background-color: {self.titlebar_bg};
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    padding: 0 10px;
    gap: 10px;
  }}
  #titlebar * {{
    -webkit-app-region: no-drag;
  }}
</style>
<div id='titlebar'>
  {self.titlebar_html}
</div>
"""
                content = content.replace("</body>", custom_html + "\n</body>")

                with open(index_html, "w", encoding="utf-8") as f:
                    f.write(content)

    def start(self):
        os.makedirs(self.web_folder, exist_ok=True)
        self._ensure_electron_files()
        eel.init(self.web_folder)
        eel.start(
            "index.html",
            mode="electron",
            host="localhost",
            port=self.port,
            size=self.size
        )