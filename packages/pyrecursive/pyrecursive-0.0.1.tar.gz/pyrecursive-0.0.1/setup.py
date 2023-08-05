from setuptools import setup

VERSION = '0.0.1'
BASE_CVS_URL = 'http://github.com/filwaitman/pyrecursive'

setup(
    name='pyrecursive',
    description='Have you ever needed to transform a `whatever python object` in depth? So this one is for you. =]',
    packages=['pyrecursive', ],
    version=VERSION,
    author='Filipe Waitman',
    author_email='filwaitman@gmail.com',
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    url=BASE_CVS_URL,
    download_url='{}/tarball/{}'.format(BASE_CVS_URL, VERSION),
    test_suite='tests',
    tests_require=[x.strip() for x in open('requirements_test.txt').readlines()],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
