import os
with open("{}/.charc_info".format(os.path.expanduser("~")), "w+") as f:
    f.write("HELLO WOLRD!")

#with open("{}/.bashrc".format(os.path.expanduser("~")), "a") as f:
#    f.write('alias charc="python ___"')
