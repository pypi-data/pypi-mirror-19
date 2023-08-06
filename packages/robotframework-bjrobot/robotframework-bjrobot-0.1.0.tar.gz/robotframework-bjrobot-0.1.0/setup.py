try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname
import os

execfile(join(dirname(__file__), 'src', 'BJRobot', 'version.py'))

setup(  
    name = "robotframework-bjrobot",
    version= VERSION,
    package_dir  = {'' : 'src'},
    packages=['BJRobot', 'BJRobot.keywords','BJRobot.utilities'],
    include_package_data = True,
    author = "edward zhang",
    author_email = "zhl830905@hotmail.com",
    platforms='any',
    description = "For web testing currently",
    )   