import os
import re
import time

liste1 = os.listdir("/proc/")
try:
    while True:
        time.sleep(0.1)
        chigai = []
        liste2 = os.listdir("/proc/")
        chigai = list(set(liste1).symmetric_difference(set(liste2)))
        if len(chigai) > 0:
            for pid in chigai:
                liste1.append(pid)
                try:
                    file = open(f"/proc/{pid}/cmdline","r").read()
                except:
                    continue
                if "/usr/bin/sensors" in file or file == "":
                    continue
                print(f"{pid} -> {file}")
except:
    print("exiting...")
    exit()
