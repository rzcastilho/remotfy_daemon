import sys
import os
import time
import argparse
import logging
import daemon
from daemon import pidfile

if sys.platform == "darwin":
    from AppKit import NSWorkspace

def get_active_window():
    if sys.platform == "darwin":
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        active_app.localizedName()
    else:
        root_check = ''
        root = Popen(['xprop', '-root'],  stdout=PIPE)

        if root.stdout != root_check:
            root_check = root.stdout

            for i in root.stdout:
                if '_NET_ACTIVE_WINDOW(WINDOW):' in i:
                    id_ = i.split()[4]
                    id_w = Popen(['xprop', '-id', id_], stdout=PIPE)
            id_w.wait()
            buff = []
            for j in id_w.stdout:
                buff.append(j)

             for line in buff:
                match = re.match("WM_NAME\((?P<type>.+)\) = (?P<name>.+)", line)
                if match != None:
                    type = match.group("type")
                    if type == "STRING" or type == "COMPOUND_TEXT":
                        return match.group("name")
            return "Active window not found"

def process(logf):
    logger = logging.getLogger('remotfy')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf)
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    while True:
        logger.info(f'Active Window: {get_active_window()}')
        time.sleep(5)

def start_daemon(pidf, logf):
    with daemon.DaemonContext(
        working_directory='/var/lib/remotfy_daemon',
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf)):
        process(logf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remotfy Daemon")
    parser.add_argument('-p', '--pid-file', default='/var/run/remotfy_daemon.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/remotfy_daemon.log')

    args = parser.parse_args()

    start_daemon(pidf=args.pid_file, logf=args.log_file)
