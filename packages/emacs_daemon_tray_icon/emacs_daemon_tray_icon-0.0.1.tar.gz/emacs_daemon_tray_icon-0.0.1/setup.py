import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "emacs_daemon_tray_icon",
    version = "0.0.1",
    author = "Michał Chałupczak",
    author_email = "michal@chalupczak.info",
    description = ("Emacs daemon systray icon"),
    license = "BSD",
    keywords = "emacs editor tool",
    packages=['src'],
    entry_points={
        'console_scripts': [
            'emacs_daemon_tray_icon = src.__init__:main'
        ]
    },
    install_requires= [
        'Pillow',
        'psutil',
        'pystray'
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)




