import os
import json

class DisableMenu:
    """
    Utility to disable the default Electron menu bar for NectarUI projects.
    This modifies the generated main.js to set autoHideMenuBar = true.
    """

    @staticmethod
    def apply(project_dir="."):
        """
        :param project_dir: The folder where main.js exists
        """
        project_dir = os.path.abspath(project_dir)
        mainjs_path = os.path.join(project_dir, "main.js")

        if not os.path.exists(mainjs_path):
            raise FileNotFoundError(f"main.js not found in {project_dir}")

        with open(mainjs_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if autoHideMenuBar is already set
        if "autoHideMenuBar" in content:
            return  # Already applied

        # Insert autoHideMenuBar: true into BrowserWindow options
        content = content.replace(
            "new BrowserWindow({",
            "new BrowserWindow({\n        autoHideMenuBar: true,"
        )

        with open(mainjs_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[NectarUI] Menu bar disabled in {mainjs_path}")