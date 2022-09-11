# zim-extensions

findDeadLinks: scans a ZIM notebook for dead links.
Embed the script via "Tools->Custom Tools" and add a new entry here, e.g. as follows:

    /usr/bin/gnome-terminal -- /home/user/.config/zim/customtools/findDeadLinks.py --notebookpath %n --ignoreFolder Journal --noask --confirmExit


command line arguments:

    usage: findDeadLinks.py [-h] --notebookpath NOTEBOOKPATH [--ignoreFolder [IGNOREFOLDER ...]] [--proxy PROXY] [--noask]
                            [--confirmExit]

    options:
      -h, --help            show this help message and exit
      --notebookpath NOTEBOOKPATH
      --ignoreFolder [IGNOREFOLDER ...]
      --proxy PROXY
      --noask
      --confirmExit
