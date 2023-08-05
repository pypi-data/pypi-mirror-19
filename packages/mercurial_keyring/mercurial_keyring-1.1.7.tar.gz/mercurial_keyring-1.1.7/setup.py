
VERSION = '1.1.7'

# pylint: disable=unused-import

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

LONG_DESCRIPTION = open("README.txt").read()

setup(
    name="mercurial_keyring",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='http://bitbucket.org/Mekk/mercurial_keyring',
    description='Mercurial Keyring Extension',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    py_modules=['mercurial_keyring'],
    keywords="mercurial hg keyring password",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control'
    ],
    install_requires=[
        'keyring>=0.3',
        'mercurial_extension_utils>=1.2.0',
    ],
    zip_safe=True,
)
