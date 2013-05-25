#!/usr/bin/python3

import mailbox, getpass, os, signal, sys

# get args
paths = []
for arg in sys.argv[1:]:
    if os.path.isfile(arg) and not os.path.islink(arg):
        paths.append(arg)
    else:
        print("weird arg: " + arg)

# use mail spool if no other mboxes asked for
if not paths:
    paths = ['/var/spool/mail/' + getpass.getuser()]
    print("No paths passed - looking for your default mail spool")

# set up mailbox data structures
boxen = []
for path in paths:
    try:
        box = mailbox.mbox(path)
        box.path = path
        boxen.append(box)
    except:
        print("Could not open mailbox: " + path)

# make the mailboxes safe
def cleanup(sig,frm):
    global boxen
    for box in boxen:
        box.close()

signal.signal(signal.SIGABRT, cleanup)
signal.signal(signal.SIGCONT, cleanup)
signal.signal(signal.SIGHUP, cleanup)
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGQUIT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGTSTP, cleanup)

# process mailboxes
for box in boxen:
    print("processing mailbox: " + box.path)

cleanup
