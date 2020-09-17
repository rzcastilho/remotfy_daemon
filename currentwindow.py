#!/usr/bin/python
# Prints list of windows in the current workspace.
import sys, time
if sys.platform == "darwin":
    from AppKit import NSWorkspace

if sys.platform == "darwin":
    while True:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        active_app_name = active_app.localizedName()
        active_app_url = active_app.executableURL()
        print(active_app_name)
        print(active_app_url)
        time.sleep(1.0)
elif sys.platform == "win32":
    (active_app_name, windowTitle) = _getActiveInfo_Win32()