from setuptools import setup

setup(
    name='baytech',
    version='0.2',
    description='Control Baytech products via telnet.',
    url='https://github.com/arnaudcoquelet/python-baytech/',
    download_url = 'https://github.com/arnaudcoquelet/python-baytech/tarball/0.2',
    license='MIT',
    author='arnaudcoquelet',
    author_email='arcoquel@gmail.com',
    packages=['baytech'],
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
