import sys
from distutils.core import setup

from setuptools import find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    name='py_w3c',
    version='0.3.1',
    author='Kazbek Byasov',
    author_email='nmb.ten@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/py_w3c/',
    license='LICENSE.txt',
    description='W3C services for python.',
    long_description=open('README.txt').read(),
    install_requires=[],
    entry_points={
        'console_scripts':
            ['w3c_validate = py_w3c.validators.html.validator:main']
    },
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
