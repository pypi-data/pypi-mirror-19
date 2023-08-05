from setuptools import setup
from linuxacademy_dl import __title__, __version__,\
        __author__, __email__, __license__
import subprocess
import tempfile


try:
    with tempfile.NamedTemporaryFile('wb+') as rst_file:
        subprocess.call(
            [
             "pandoc", "README.md", "-f", "markdown", "-t", "rst",
             "-o", rst_file.name
            ]
        )
        rst_file.seek(0)
        long_description = rst_file.read()
except OSError:
    print 'error'
    long_description = open('README.md').read()


setup(
    name=__title__,
    version=__version__,

    description='Download videos from Linux Academy (linuxacademy.com)'
                ' for personal offline use',
    long_description=long_description,

    author=__author__,
    author_email=__email__,
    url='https://github.com/vassim/{}'.format(__title__),
    license=__license__,

    packages=['linuxacademy_dl'],
    install_requires=map(
        lambda x: x.strip(),
        open('requirements.txt').readlines()
    ),
    entry_points={
        'console_scripts': [
            '{}=linuxacademy_dl.__main__:main'.format(__title__)
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Terminals',
        'Topic :: Utilities',
        'Topic :: Multimedia :: Video'
    ],
)
