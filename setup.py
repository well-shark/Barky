# Modify from https://github.com/navdeep-G/setup.py/blob/master/setup.py
import os
import re
import sys
from setuptools import setup, find_packages, Command

__path__ = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = "Barky"
DESCRIPTION = 'Push notifications to your iPhone with Bark.'
URL = 'https://github.com/well-shark/Barky'
EMAIL = 'wellshark.net@gmail.com'
AUTHOR = 'WellShark'
REQUIRES_PYTHON = '>=3.4.0'

REQUIRED = []

# https://github.com/wookayin/gpustat/blob/master/setup.py
def read_readme():
    with open("README.md", "r") as f:
        return f.read()

def read_version():
    with open(os.path.join(__path__, 'barky/__init__.py')) as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                  f.read(), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find __version__ string")

__version__ = read_version()

# brought from https://github.com/kennethreitz/setup.py
class DeployCommand(Command):
    description = 'Build and deploy the package to PyPI.'
    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass

    @staticmethod
    def status(s):
        print(s)

    def run(self):
        import twine  # we require twine locally

        assert 'dev' not in __version__, (
            "Only non-devel versions are allowed. "
            "__version__ == {}".format(__version__))

        with os.popen("git status --short") as fp:
            git_status = fp.read().strip()
            if git_status:
                print("Error: git repository is not clean.\n")
                os.system("git status --short")
                sys.exit(1)

        try:
            from shutil import rmtree
            self.status('Removing previous builds ...')
            rmtree(os.path.join(__path__, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution ...')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine ...')
        ret = os.system('twine upload dist/*')
        if ret != 0:
            sys.exit(ret)

        # self.status('Creating git tags ...')
        # os.system('git tag v{0}'.format(__version__))
        # os.system('git tag --list')
        sys.exit()


setup(
    name=NAME,
    version=read_version(),
    python_requires=REQUIRES_PYTHON,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    keywords='Bark, Push, Notification, iPhone, iOS',
    license="MIT",
    url=URL,
    packages=find_packages(),
    zip_safe=True,
    install_requires=REQUIRED,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points= {
        'console_scripts': ['bark=bark:main'],
    },
    cmdclass={
        'deploy': DeployCommand,
    },
)