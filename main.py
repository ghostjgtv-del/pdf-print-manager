"""
PDF Print Manager
Main Entry Point

Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
Email: ghost.jgtv@gmail.com
Date: May 2026

Copyright © 2026 Lagudis Fresh Food Group
All rights reserved.
"""

import sys
import os

# Add current directory to path
if hasattr(sys, '_MEIPASS'):
    # Running in PyInstaller bundle
    os.chdir(sys._MEIPASS)

from app import PDFPrintManagerApp


def main():
    """Application entry point"""
    try:
        app = PDFPrintManagerApp()
        app.run()
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
