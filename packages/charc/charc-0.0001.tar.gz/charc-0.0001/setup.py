from setuptools import setup
setup(
        name="charc",
        version="0.0001",
        description="Command-line interface to easily train and test character classification ML",
        install_requires=['numpy', 'scipy', 'cloudpickle', 'termcolor'], 
        packages=["Charc",],
        scripts=["bin/config.py"],
        author="Heyaw Meteke",
        url="https://github.com/h3y4w/charc",
)

