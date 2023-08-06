from distutils.core import setup


setup(
    name='wolfansweroid',
    packages=['wolfansweroid'],
    version='0.3',
    description='A helper for answeroid for helping on Q/A sites (https://pypi.python.org/pypi/answeroid/0.5)',
    author='Bahrom Matyakubov',
    author_email='bahrom.matyakubov@gmail.com',
    url='https://github.com/bahrom-matyakubov/wolf-answeroid',
    download_url='https://github.com/bahrom-matyakubov/wolf-answeroid/tarball/0.3',
    keywords=['Q&A', 'answer', 'question', 'help', 'bot', 'wolframalpha'],
    classifiers=[],
    install_requires=[
        'wolframalpha'
    ],
)