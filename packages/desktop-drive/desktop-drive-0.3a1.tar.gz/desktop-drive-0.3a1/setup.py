from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='desktop-drive',
    version='0.3a1',
    description='Bash-like file operations on Google Drives "mounted" on the local filesystem.',
    long_description=long_description,
    
    author='Kevin Beaufume, Thomas Saglio, Louis Senez',
    author_email='from.math.import.pi@gmail.com',
    license='GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: File Sharing',
        'Topic :: Desktop Environment :: File Managers',
    ],
    keywords='files google drive bash',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['google-api-python-client', 'pyqt5'],
    package_data={
        'desktop_drive': ['client_id.json'],
    },
    entry_points = {
            'console_scripts': ['desktop-drive=desktop_drive.main:main'],
        }
)

"""entry_points={
    'console_scripts': [
        'desktop-drive=main.py',
    ],
},"""

