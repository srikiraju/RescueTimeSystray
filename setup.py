from setuptools import setup

APP = ['productivity_feedback.py']
OPTIONS = {'argv_emulation': False,
           'plist': {'LSBackgroundOnly': True},
           'resources' : 'key.cfg'
          }

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
