try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='emailpysender',
    version='0.0.2',
    author='53r63rn4r',
    author_email='serbernar1@gmail.com',
    url='https://github.com/serbernar/emailpysender',
    description='Small library for sending html emails with attachments',
    download_url='https://github.com/serbernar/emailpysender/archive/master.zip',
    license='MIT',

    packages=['emailpysender'],
    install_requires=['premailer', 'ujson'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
