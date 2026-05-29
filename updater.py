"""
Auto-Update Manager for PDF Print Manager
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
Date: May 2026
"""

import requests
import os
import sys
from pathlib import Path
import shutil
import subprocess
from packaging import version


class Updater:
    """Handles application auto-updates"""

    SERVER_URL = "http://143.110.130.78:8001"
    CURRENT_VERSION = "1.0"

    @classmethod
    def check_for_updates(cls) -> tuple[bool, str, str]:
        """
        Check if a new version is available

        Returns:
            tuple: (update_available, current_version, latest_version)
        """
        try:
            response = requests.get(f"{cls.SERVER_URL}/app/version", timeout=5)

            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("version", "1.0")
                file_exists = data.get("file_exists", False)

                if file_exists and version.parse(latest_version) > version.parse(cls.CURRENT_VERSION):
                    return True, cls.CURRENT_VERSION, latest_version
                else:
                    return False, cls.CURRENT_VERSION, latest_version
            else:
                return False, cls.CURRENT_VERSION, cls.CURRENT_VERSION

        except:
            return False, cls.CURRENT_VERSION, cls.CURRENT_VERSION

    @classmethod
    def download_and_install_update(cls, progress_callback=None) -> tuple[bool, str]:
        """
        Download and install update

        Args:
            progress_callback: Function to call with download progress (0-100)

        Returns:
            tuple: (success, message)
        """
        try:
            if progress_callback:
                progress_callback(10)

            # Download update
            response = requests.get(f"{cls.SERVER_URL}/app/download", stream=True, timeout=30)

            if response.status_code != 200:
                return False, "No se pudo descargar la actualización"

            if progress_callback:
                progress_callback(30)

            # Get executable path
            if getattr(sys, 'frozen', False):
                current_exe = Path(sys.executable)
            else:
                current_exe = Path(__file__).parent / "PDF_Print_Manager.exe"

            # Create temporary update file
            update_file = current_exe.parent / "PDF_Print_Manager.new"

            # Download to temp file
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(update_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size > 0:
                            progress = 30 + int((downloaded / total_size) * 50)
                            progress_callback(progress)

            if progress_callback:
                progress_callback(80)

            # Create update script
            update_script = current_exe.parent / "update.bat"
            script_content = f"""@echo off
timeout /t 2 /nobreak >nul
del "{current_exe}"
move "{update_file}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
"""

            with open(update_script, 'w') as f:
                f.write(script_content)

            if progress_callback:
                progress_callback(90)

            # Execute update script and exit
            subprocess.Popen([str(update_script)], shell=True)

            if progress_callback:
                progress_callback(100)

            return True, "Actualización descargada. La aplicación se reiniciará..."

        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
