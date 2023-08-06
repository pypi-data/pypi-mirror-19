from setuptools import setup
VERSION = '0.3'

setup(
        name='md2conf',
        version=VERSION,
        description='Upload .md file to Confluence',
        author='Nic Roland',
        author_email='nicroland9@gmail.com',
        url = 'https://github.com/nicr9/daftpunk',
        download_url = 'https://github.com/nicr9/daftpunk/tarball/%s' % VERSION,
        install_requires=[
            'requests',
            'beautifulsoup4',
            'markdown',
            ],
        scripts=['bin/md2conf'],
        )
