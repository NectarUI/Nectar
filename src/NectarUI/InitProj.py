import os
import json
import subprocess

class NectarInit:
    def __init__(self, project_name="NectarApp"):
        self.project_name = project_name
        self.base_dir = os.path.join(os.getcwd(), project_name)
        self.web_dir = os.path.join(self.base_dir, "web")

    def create_project(self):
        os.makedirs(self.web_dir, exist_ok=True)

        # package.json
        package_json = {
            "name": self.project_name.lower(),
            "version": "1.0.0",
            "main": "main.js",
            "scripts": {"start": "electron ."},
            "dependencies": {"electron": "^26.2.0","custom-electron-titlebar": "^3.2.1"}
        }

        with open(os.path.join(self.base_dir, "package.json"), "w") as f:
            json.dump(package_json, f, indent=4)

        # main.js
        main_js = """const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        frame: false,
        webPreferences: {
            preload: path.join(__dirname, 'web', 'preload.js'),
            nodeIntegration: true,
            contextIsolation: false,
            webviewTag: true
        }
    });
    win.loadFile('web/index.html');
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if(process.platform !== 'darwin') app.quit(); });
"""
        with open(os.path.join(self.base_dir, "main.js"), "w") as f:
            f.write(main_js)

        # preload.js
        with open(os.path.join(self.web_dir, "preload.js"), "w") as f:
            f.write("// Preload file")

        # index.html
        index_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NectarUI App</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>Welcome to NectarUI!</h1>
<script src="renderer.js"></script>
</body>
</html>"""
        with open(os.path.join(self.web_dir, "index.html"), "w") as f:
            f.write(index_html)

        # renderer.js & style.css
        open(os.path.join(self.web_dir, "renderer.js"), "w").close()
        open(os.path.join(self.web_dir, "style.css"), "w").close()

        print(f"NectarUI project '{self.project_name}' initialized!")
        subprocess.run(["npm", "install"], cwd=self.base_dir)
