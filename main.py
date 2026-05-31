"""
PDF Print Manager
Main Entry Point - PyQt6 Version

Author: Eng. Justo Torres
Email: ghost.jgtv@gmail.com
Date: May 2026

Copyright © 2026 JG Software
All rights reserved.
"""

import sys
import os

# Add current directory to path
if hasattr(sys, '_MEIPASS'):
    # Running in PyInstaller bundle
    os.chdir(sys._MEIPASS)

from app_pyqt import main as app_main


if __name__ == "__main__":
    try:
        app_main()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
