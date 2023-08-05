from setuptools import setup

setup(
    name='dashtable',
    packages=['dashtable'],
    version='1.2.4',
    description='A library for converting a HTML tables into ASCII tables',
    author='doakey3',
    author_email='dashtable.dmodo@spamgourmet.com',
    url='https://github.com/doakey3/DashTable',
    download_url='https://github.com/doakey3/DashTable/tarball/1.2.4',
    license='MIT',
    install_requires=['beautifulsoup4'],
    entry_points={'console_scripts': ['dashtable = DashTable.html2rst:cmdline']}
)
