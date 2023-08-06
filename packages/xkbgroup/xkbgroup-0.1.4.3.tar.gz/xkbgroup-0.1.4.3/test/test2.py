import subprocess
import time

import xkbgroup


xkb = xkbgroup.XKeyboard()
print(xkb.groups_data)

subprocess.call([
    "setxkbmap",
    "-option", ""])
subprocess.call([
    "setxkbmap",
    "-layout", "br",
    "-model", "abnt2",
    "-option", "terminate:ctrl_alt_bksp",
    "-verbose"])

time.sleep(0.5)
print(xkb.groups_data)

subprocess.call([
    "setxkbmap",
    "-option", ""])
subprocess.call([
    "setxkbmap",
    "-layout", "us,ru,ua,vn",
    "-option", "grp:alt_shift_toggle",
    "-verbose"])

time.sleep(0.5)
print(xkb.groups_data)
