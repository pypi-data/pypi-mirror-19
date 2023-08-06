import os
with open("{}/.charc_info".format(os.path.expanduser("~")), "w+") as f:
    f.write("HELLO WOLRD!")
