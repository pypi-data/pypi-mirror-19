from setuptools import setup
from setuptools.command.install import install
import os

class Make(install):
    def run(self):
        
        with open("{}/.charc_info".format(os.path.expanduser("~"))) as f:
            f.write("HELLO ASDJSNAJDNSAJKNDKNSJKAND")

        install.run(self)
setup(
        name="charc",
        version="0.00001",
        description="Command-line interface to easily train and test character classification ML",
        install_requires=['numpy', 'scipy', 'cloudpickle', 'termcolor'], 
        packages=["charc",],
        cmdclass={"install":Make},
        author="Heyaw Meteke",
        url="https://github.com/h3y4w/charc",
)

