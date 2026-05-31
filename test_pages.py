"""
Test script to diagnose page loading issues
"""

import sys
import traceback
from PyQt6.QtWidgets import QApplication
from pathlib import Path

print("="*60)
print("TESTING PAGE INITIALIZATION")
print("="*60)

try:
    print("\n[1/6] Importing QueuePage...")
    from ui.tab_queue_pyqt import QueuePage
    print("[OK] QueuePage imported successfully")
except Exception as e:
    print(f"[ERROR] importing QueuePage:")
    traceback.print_exc()

try:
    print("\n[2/6] Importing SchedulerPage...")
    from ui.tab_scheduler_pyqt import SchedulerPage
    print("[OK] SchedulerPage imported successfully")
except Exception as e:
    print(f"[ERROR] importing SchedulerPage:")
    traceback.print_exc()

try:
    print("\n[3/6] Importing HistoryPage...")
    from ui.tab_history_pyqt import HistoryPage
    print("[OK] HistoryPage imported successfully")
except Exception as e:
    print(f"[ERROR] importing HistoryPage:")
    traceback.print_exc()

try:
    print("\n[4/6] Importing SettingsPage...")
    from ui.tab_settings_pyqt import SettingsPage
    print("[OK] SettingsPage imported successfully")
except Exception as e:
    print(f"[ERROR] importing SettingsPage:")
    traceback.print_exc()

try:
    print("\n[5/6] Importing LicensePage...")
    from ui.tab_license_pyqt import LicensePage
    print("[OK] LicensePage imported successfully")
except Exception as e:
    print(f"[ERROR] importing LicensePage:")
    traceback.print_exc()

try:
    print("\n[6/6] Importing AboutPage...")
    from ui.tab_about_pyqt import AboutPage
    print("[OK] AboutPage imported successfully")
except Exception as e:
    print(f"[ERROR] importing AboutPage:")
    traceback.print_exc()

print("\n" + "="*60)
print("TESTING PAGE INSTANTIATION")
print("="*60)

app = QApplication(sys.argv)

try:
    print("\n[1/6] Creating QueuePage...")
    page = QueuePage()
    print(f"[OK] QueuePage created: {page}")
    print(f"  Size: {page.size()}")
    print(f"  Visible: {page.isVisible()}")
except Exception as e:
    print(f"[ERROR] creating QueuePage:")
    traceback.print_exc()

try:
    print("\n[2/6] Creating SchedulerPage...")
    page = SchedulerPage()
    print(f"[OK] SchedulerPage created: {page}")
except Exception as e:
    print(f"[ERROR] creating SchedulerPage:")
    traceback.print_exc()

try:
    print("\n[3/6] Creating HistoryPage...")
    page = HistoryPage()
    print(f"[OK] HistoryPage created: {page}")
except Exception as e:
    print(f"[ERROR] creating HistoryPage:")
    traceback.print_exc()

try:
    print("\n[4/6] Creating SettingsPage...")
    page = SettingsPage()
    print(f"[OK] SettingsPage created: {page}")
except Exception as e:
    print(f"[ERROR] creating SettingsPage:")
    traceback.print_exc()

try:
    print("\n[5/6] Creating LicensePage...")
    page = LicensePage()
    print(f"[OK] LicensePage created: {page}")
except Exception as e:
    print(f"[ERROR] creating LicensePage:")
    traceback.print_exc()

try:
    print("\n[6/6] Creating AboutPage...")
    page = AboutPage()
    print(f"[OK] AboutPage created: {page}")
except Exception as e:
    print(f"[ERROR] creating AboutPage:")
    traceback.print_exc()

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
