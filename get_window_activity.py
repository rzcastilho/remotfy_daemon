import os, re, sys, time
from subprocess import PIPE, Popen

if sys.platform == "darwin":
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
    )

def get_activityname():
    if sys.platform == "linux":

        root = Popen( ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout = PIPE )
        stdout, stderr = root.communicate()
        m = re.search( b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout )

        if m is not None:
            window_id   = m.group( 1 )

            windowname  = None
            window = Popen( ['xprop', '-id', window_id, 'WM_NAME'], stdout = PIPE )
            stdout, stderr = window.communicate()
            wmatch = re.match( b'WM_NAME\(\w+\) = (?P<name>.+)$', stdout )
            if wmatch is not None:
                windowname = wmatch.group( 'name' ).decode( 'UTF-8' ).strip( '"' )

            processname1, processname2 = None, None
            process = Popen( ['xprop', '-id', window_id, 'WM_CLASS'], stdout = PIPE )
            stdout, stderr = process.communicate()
            pmatch = re.match( b'WM_CLASS\(\w+\) = (?P<name>.+)$', stdout )
            if pmatch is not None:
                processname1, processname2 = pmatch.group( 'name' ).decode( 'UTF-8' ).split( ', ' )
                processname1 = processname1.strip( '"' )
                processname2 = processname2.strip( '"' )

            pidnumber = None
            pid = Popen( ['xprop', '-id', window_id, '_NET_WM_PID'], stdout = PIPE )
            stdout, stderr = pid.communicate()
            pidmatch = re.match( b'_NET_WM_PID\(\w+\) = (?P<pid>[0-9]+)$', stdout )
            if pidmatch is not None:
                pidnumber = pidmatch.group( 'pid' ).decode( 'UTF-8')

            return {
                'windowname':   windowname,
                'processname1': processname1,
                'processname2': processname2,
                'pid': pidnumber
                }

        return {
            'windowname':   None,
            'processname1': None,
            'processname2': None,
            'pid': None
            }
    elif sys.platform == "darwin":
        curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        curr_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
        curr_app_name = curr_app.localizedName()
        options = kCGWindowListOptionOnScreenOnly
        windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
        for window in windowList:
            pid = window['kCGWindowOwnerPID']
            windowNumber = window['kCGWindowNumber']
            ownerName = window['kCGWindowOwnerName']
            geometry = window['kCGWindowBounds']
            windowTitle = window.get('kCGWindowName', u'Unknown')
            if curr_pid == pid:
                return {
                    'windowname':   windowTitle,
                    'processname1': ownerName,
                    'processname2': None,
                    'pid': pid
                    }
    elif sys.platform == "win32":
        print("Not implemented for win32 platform!")
        return {
            'windowname':   None,
            'processname1': None,
            'processname2': None,
            'pid': None
            }
    else:
        print("Unknown platform! - " + sys.platform)
        return {
            'windowname':   None,
            'processname1': None,
            'processname2': None,
            'pid': None
            }


if __name__ == '__main__':
    while True:
        a = get_activityname()
        print( '''
        'windowname':   %s,
        'processname1': %s,
        'processname2': %s,
        'pid':          %s
        ''' % ( a['windowname'], a['processname1'], a['processname2'], a['pid'] ) )
        time.sleep(1)
