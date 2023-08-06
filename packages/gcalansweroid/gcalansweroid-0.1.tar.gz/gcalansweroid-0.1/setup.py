from distutils.core import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='gcalansweroid',
    packages=['gcalansweroid'],
    version='0.1',
    description='A helper for answeroid for helping on Q/A sites (https://pypi.python.org/pypi/answeroid/0.5)',
    author='Bahrom Matyakubov',
    author_email='bahrom.matyakubov@gmail.com',
    url='https://github.com/bahrom-matyakubov/gcal-answeroid',
    download_url='https://github.com/bahrom-matyakubov/gcal-answeroid/tarball/0.1',
    keywords=['Q&A', 'answer', 'question', 'help', 'bot', 'google calculator'],
    classifiers=[],
    install_requires=REQUIREMENTS,  # Yes, these could contain comments, but for this case should be good enough
)