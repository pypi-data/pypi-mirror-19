from setuptools import setup, find_packages

VERSION = '2.0.3rc5'
DEPENDS = [
    'Flask==0.10.1',
    'Flask-Bower',
    'Flask-SocketIO',
    'eventlet',
    'click',
]

setup(name='counter-caller', version=VERSION,
      packages=find_packages(), install_requires=DEPENDS,
      author='Lewis Eason', author_email='me@lewiseason.co.uk',
      include_package_data=True,
      package_data={
        'counter-caller': ['*.html', '*.css', '*.js', '*.mp3']
      },
      entry_points={
        'console_scripts': ['counter-caller = counter_caller.cli:run']
      }
)
