from distutils.core import setup

# To register (first time):
# python setup.py register -r pypi
# To upload, create a new tag (git tag version, git push --tags origin master), then run:
# python setup.py sdist upload -r pypi

setup(
    name='answeroid',
    packages=['answeroid', 'helpers', 'sites'],
    version='0.7',
    description='A simple bot for helping on Q/A sites',
    author='Bahrom Matyakubov',
    author_email='bahrom.matyakubov@gmail.com',
    url='https://github.com/bahrom-matyakubov/answeroid',
    download_url='https://github.com/bahrom-matyakubov/answeroid/tarball/0.7',
    keywords=['Q&A', 'answer', 'question', 'help', 'bot'],
    classifiers=[],
    install_requires=[
        'bs4',
        'requests',
        'wolframalpha',
        'sympy'
    ],
)