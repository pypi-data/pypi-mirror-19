import codecs
from setuptools import setup
from gitx import __version__

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "gitx",
    version = __version__,
    description= 'A simple tool that help you speed up git clone',
    author = 'LiuLiqiu',
    author_email= 'liuliqiu@yunba.io',
    packages = ['gitx'],
    install_requires = ['requests'],
    entry_points = """
    [console_scripts]
    gitx = gitx.gitx:command_line_runner
    """,
    long_description = long_description,
)