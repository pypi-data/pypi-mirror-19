from setuptools import setup
setup(
        name="charc",
        version="0.001",
        description="Command-line interface to easily train and test character classification ML",
        install_requires=['numpy', 'scipy', 'cloudpickle', 'termcolor'], 
        packages=["charc",],
        scripts=["bin/setup.sh"],
        author="Heyaw Meteke",
        url="https://github.com/h3y4w/charc",
)

