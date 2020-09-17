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