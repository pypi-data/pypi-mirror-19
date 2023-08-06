from distutils.core import setup

setup(
    name='gcalansweroid',
    packages=['gcalansweroid'],
    version='0.2',
    description='A helper for answeroid for helping on Q/A sites (https://pypi.python.org/pypi/answeroid/0.5)',
    author='Bahrom Matyakubov',
    author_email='bahrom.matyakubov@gmail.com',
    url='https://github.com/bahrom-matyakubov/gcal-answeroid',
    download_url='https://github.com/bahrom-matyakubov/gcal-answeroid/tarball/0.2',
    keywords=['Q&A', 'answer', 'question', 'help', 'bot', 'google calculator'],
    classifiers=[],
    install_requires=[
        'bs4',
        'requests',
    ],
)