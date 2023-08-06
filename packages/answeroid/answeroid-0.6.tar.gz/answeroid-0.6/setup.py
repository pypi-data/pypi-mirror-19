from distutils.core import setup

setup(
    name='answeroid',
    packages=['answeroid', 'helpers', 'sites'],
    version='0.6',
    description='A simple bot for helping on Q/A sites',
    author='Bahrom Matyakubov',
    author_email='bahrom.matyakubov@gmail.com',
    url='https://github.com/bahrom-matyakubov/answeroid',
    download_url='https://github.com/bahrom-matyakubov/answeroid/tarball/0.6',
    keywords=['Q&A', 'answer', 'question', 'help', 'bot'],
    classifiers=[],
    install_requires=[
        'bs4',
        'requests',
        'wolframalpha'
    ],
)