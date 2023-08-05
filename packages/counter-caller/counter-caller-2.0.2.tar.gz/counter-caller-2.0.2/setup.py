from setuptools import setup, find_packages

VERSION = '2.0.2'
DEPENDS = [
    'Flask==0.10.1',
    'Flask-Bower',
    'Flask-SocketIO',
    'eventlet',
    'click',
]

setup(name='counter-caller', version=VERSION,
      packages=find_packages(), install_requires=DEPENDS,
      include_package_data=True,
      entry_points={
        'console_scripts': ['counter-caller = counter_caller.cli:run']
      }
)
